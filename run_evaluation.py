"""
run_evaluation.py — FINAL CORRECTED VERSION
Model B is now TRULY naive (no system prompt + higher temperature)
"""

import json
import csv
import time
import ollama

from scenarios import SCENARIOS
from assistant import generate_email
from evaluator import evaluate_email

GENERATOR_MODEL = "qwen2.5:7b"
JUDGE_MODEL = "qwen2.5:7b"

RESULTS_JSON = "results.json"
RESULTS_CSV = "results.csv"


def generate_email_naive(intent: str, facts: list[str], tone: str) -> str:
    """Model B — TRULY NAIVE: no system prompt, minimal instructions, higher temperature"""
    facts_block = "\n".join(f"- {f}" for f in facts)
    user_prompt = f"""Intent: {intent}
Key Facts:
{facts_block}
Tone: {tone}"""

    response = ollama.chat(
        model=GENERATOR_MODEL,
        messages=[{"role": "user", "content": user_prompt}],   # NO system prompt
        options={"temperature": 0.7, "num_ctx": 8192, "num_predict": 1024}  # higher temp = less consistent
    )
    return response['message']['content'].strip()


def run_all(scenarios: list[dict]) -> dict:
    results = {"model_a": [], "model_b": []}

    for i, scenario in enumerate(scenarios):
        print(f"\n[{i+1}/10] Scenario: {scenario['intent'][:60]}...")

        print("  → Generating with Model A (Advanced Qwen2.5 Prompt)...")
        email_a = generate_email(scenario["intent"], scenario["facts"], scenario["tone"])
        print("  → Evaluating Model A...")
        eval_a = evaluate_email(scenario, email_a, JUDGE_MODEL)
        eval_a["strategy"] = "Qwen2.5 Optimized (Production-Grade)"
        results["model_a"].append(eval_a)

        time.sleep(1.5)

        print("  → Generating with Model B (TRULY Naive — no system prompt)...")
        email_b = generate_email_naive(scenario["intent"], scenario["facts"], scenario["tone"])
        print("  → Evaluating Model B...")
        eval_b = evaluate_email(scenario, email_b, JUDGE_MODEL)
        eval_b["strategy"] = "Naive (no system prompt, high temp)"
        results["model_b"].append(eval_b)

        time.sleep(1.5)

        print(f"  ✓ Model A composite: {eval_a['composite_score']:.2f} | Model B: {eval_b['composite_score']:.2f}")

    return results


def compute_averages(evals: list[dict]) -> dict:
    n = len(evals)
    return {
        "avg_fact_recall": round(sum(e["metric_1_fact_recall"]["score"] for e in evals) / n, 2),
        "avg_tone_adherence": round(sum(e["metric_2_tone_adherence"]["score"] for e in evals) / n, 2),
        "avg_conciseness_clarity": round(sum(e["metric_3_conciseness_clarity"]["score"] for e in evals) / n, 2),
        "avg_composite": round(sum(e["composite_score"] for e in evals) / n, 2),
    }


def write_csv(results: dict, path: str) -> None:
    rows = []
    for strategy_key in ["model_a", "model_b"]:
        for e in results[strategy_key]:
            rows.append({
                "strategy": e.get("strategy", ""),
                "scenario_id": e["scenario_id"],
                "intent": e["intent"],
                "tone": e["tone"],
                "metric_1_fact_recall": e["metric_1_fact_recall"]["score"],
                "facts_present": e["metric_1_fact_recall"]["facts_present"],
                "total_facts": e["metric_1_fact_recall"]["total_facts"],
                "metric_2_tone_adherence": e["metric_2_tone_adherence"]["score"],
                "tone_reason": e["metric_2_tone_adherence"].get("reason", ""),
                "metric_3_conciseness_clarity": e["metric_3_conciseness_clarity"]["score"],
                "fluency_score": e["metric_3_conciseness_clarity"]["fluency_score"],
                "brevity_score": e["metric_3_conciseness_clarity"]["brevity_score"],
                "word_count": e["metric_3_conciseness_clarity"]["word_count"],
                "filler_phrases": "; ".join(e["metric_3_conciseness_clarity"]["filler_phrases_found"]),
                "composite_score": e["composite_score"],
            })

    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n✅ CSV written → {path}")


def write_json(results: dict, averages: dict, path: str) -> None:
    output = {"averages": averages, "results": results}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON written → {path}")


def print_summary(averages: dict) -> None:
    print("\n" + "=" * 65)
    print("                  EVALUATION SUMMARY")
    print("=" * 65)
    for label, avgs in averages.items():
        name = "Model A (Qwen2.5 Optimized)" if label == "model_a" else "Model B (Naive)"
        print(f"\n{name}")
        print(f"   Fact Recall      : {avgs['avg_fact_recall']:5.2f}/10")
        print(f"   Tone Adherence   : {avgs['avg_tone_adherence']:5.2f}/10")
        print(f"   Conciseness      : {avgs['avg_conciseness_clarity']:5.2f}/10")
        print(f"   Composite Score  : {avgs['avg_composite']:5.2f}/10")
    print("=" * 65)


if __name__ == "__main__":
    print("Starting FINAL evaluation with corrected Model B (truly naive)...\n")
    results = run_all(SCENARIOS)

    averages = {
        "model_a": compute_averages(results["model_a"]),
        "model_b": compute_averages(results["model_b"]),
    }

    write_csv(results, RESULTS_CSV)
    write_json(results, averages, RESULTS_JSON)
    print_summary(averages)
    print("\n🎉 Evaluation completed successfully!")