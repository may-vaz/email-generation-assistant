"""
Evaluation Engine — 3 Custom Metrics (exactly your original code)
"""

import re
import json
import ollama

FILLER_PHRASES = [
    "i hope this email finds you", "i hope this finds you well", "please do not hesitate",
    "feel free to reach out", "i am writing to", "as per our conversation", "going forward",
    "at your earliest convenience", "please find attached", "i wanted to touch base",
    "circle back", "synergy", "leverage", "deep dive",
]


def _judge_call(prompt: str, model: str = "qwen2.5:7b") -> str:
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1, "num_ctx": 8192, "num_predict": 512}
    )
    return response['message']['content'].strip()


def _extract_json(raw: str) -> dict:
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not extract JSON from: {raw[:200]}")


def fact_recall_score(generated_email: str, facts: list[str], model: str = "qwen2.5:7b") -> dict:
    facts_block = "\n".join(f"{i+1}. {f}" for i, f in enumerate(facts))
    prompt = f"""You are evaluating whether an email correctly includes specific facts.

FACTS THAT MUST APPEAR IN THE EMAIL:
{facts_block}

EMAIL:
{generated_email}

For each fact, decide: is it meaningfully present in the email? (yes or no)
Respond ONLY with a JSON object in this exact format (no markdown):
{{"fact_1": "yes", "fact_2": "no", ...}}
Use keys fact_1, fact_2, ... up to fact_{len(facts)}."""

    raw = _judge_call(prompt, model)
    try:
        result = _extract_json(raw)
    except ValueError:
        result = {f"fact_{i+1}": "no" for i in range(len(facts))}

    present = sum(1 for v in result.values() if str(v).lower() == "yes")
    score = round((present / len(facts)) * 10, 2) if facts else 0.0
    return {"score": score, "facts_present": present, "total_facts": len(facts), "detail": result}


def tone_adherence_score(generated_email: str, requested_tone: str, model: str = "qwen2.5:7b") -> dict:
    prompt = f"""You are a professional writing coach evaluating tone accuracy.

REQUESTED TONE: {requested_tone}

EMAIL:
{generated_email}

Rate how well the email's vocabulary, sentence structure, and overall register match the requested tone on a scale from 1 to 10.
Respond ONLY with a JSON object (no markdown):
{{"score": <number 1-10>, "reason": "<one sentence explanation>"}}"""

    raw = _judge_call(prompt, model)
    try:
        result = _extract_json(raw)
        score = float(result.get("score", 5))
        score = max(1.0, min(10.0, score))
        reason = result.get("reason", "")
    except (ValueError, KeyError):
        score, reason = 5.0, "Could not parse judge response."

    return {"score": round(score, 2), "reason": reason}


def conciseness_clarity_score(generated_email: str, facts: list[str], model: str = "qwen2.5:7b") -> dict:
    email_lower = generated_email.lower()
    filler_hits = [p for p in FILLER_PHRASES if p in email_lower]
    word_count = len(generated_email.split())
    expected_words = 40 + 30 * len(facts)
    length_ratio = word_count / expected_words

    brevity_penalty = len(filler_hits) * 0.5
    if length_ratio > 1.8:
        brevity_penalty += 2.0
    elif length_ratio > 1.4:
        brevity_penalty += 1.0

    brevity_score = max(1.0, 10.0 - brevity_penalty)

    prompt = f"""You are a writing editor. Rate the clarity and fluency of this email on a scale of 1–10:
EMAIL:
{generated_email}

Respond ONLY with a JSON object (no markdown):
{{"score": <number 1-10>, "reason": "<one sentence>"}}"""

    raw = _judge_call(prompt, model)
    try:
        result = _extract_json(raw)
        fluency = float(result.get("score", 7))
        fluency = max(1.0, min(10.0, fluency))
        fluency_reason = result.get("reason", "")
    except (ValueError, KeyError):
        fluency, fluency_reason = 7.0, "Could not parse judge response."

    combined = round(0.5 * fluency + 0.5 * brevity_score, 2)

    return {
        "score": combined,
        "fluency_score": round(fluency, 2),
        "brevity_score": round(brevity_score, 2),
        "word_count": word_count,
        "filler_phrases_found": filler_hits,
        "fluency_reason": fluency_reason,
    }


def evaluate_email(scenario: dict, generated_email: str, judge_model: str = "qwen2.5:7b") -> dict:
    facts = scenario["facts"]
    tone = scenario["tone"]

    m1 = fact_recall_score(generated_email, facts, judge_model)
    m2 = tone_adherence_score(generated_email, tone, judge_model)
    m3 = conciseness_clarity_score(generated_email, facts, judge_model)

    composite = round((m1["score"] + m2["score"] + m3["score"]) / 3, 2)

    return {
        "scenario_id": scenario["id"],
        "intent": scenario["intent"],
        "tone": tone,
        "generated_email": generated_email,
        "metric_1_fact_recall": m1,
        "metric_2_tone_adherence": m2,
        "metric_3_conciseness_clarity": m3,
        "composite_score": composite,
    }