# Email Generation Assistant (AI Engineer Assessment)



**How to Set Up and Run:**

1. Install Ollama
2. Pull the model:

```
ollama pull qwen2.5:7b
```

3. Run the evaluation:

```
python3 assistant.py
python3 run_evaluation.py
```

This will:

* Generate emails for 10 scenarios
* Evaluate both models
* Output results in `results.csv` and `results.json`
* Print a final summary

---

## What this project does

This project builds an AI system that:

* Generates professional emails using an LLM
* Evaluates output quality using custom metrics
* Compares two different prompting strategies

---

## Project Files

* `assistant.py` → Email generation (Model A – optimized)
* `run_evaluation.py` → Runs full evaluation + comparison
* `evaluator.py` → Custom metrics
* `scenarios.py` → 10 test cases + reference emails
* `results.csv / results.json` → Output results

---

## Models Compared

### Model A (Optimized)

* Strong system prompt
* Few-shot examples
* Low temperature
* Focus: accuracy and consistency

### Model B (Naive)

* No system prompt
* No examples
* Higher temperature
* Focus: baseline comparison

---

## Evaluation Metrics (Custom)

1. **Fact Recall**

   * Checks if all key facts are included
   * Score = (facts included / total facts) × 10

2. **Tone Adherence**

   * Measures how well the tone matches the requirement
   * Scored using LLM (1–10)

3. **Conciseness & Clarity**

   * Combines:

     * brevity (length + filler penalties)
     * fluency (LLM-based)
   * Final = 0.5 × fluency + 0.5 × brevity

---

## Results Summary

```
Model A (Optimized)
Fact Recall      : 9.80
Tone Adherence   : 8.60
Conciseness      : 9.25
Composite Score  : 9.22

Model B (Naive)
Fact Recall      : 9.30
Tone Adherence   : 8.80
Conciseness      : 9.12
Composite Score  : 9.07
```

---

## Conclusion

* Model A performs better overall due to stronger prompting and control
* Model B performs well but is less consistent
* Prompt design significantly impacts output quality even with the same base model



