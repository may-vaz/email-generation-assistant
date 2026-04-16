# Email Generation Assistant (AI Engineer Assessment)

## 🔹 What this project is

This project is a simple but complete system that:

1. **Generates professional emails using an LLM**
2. **Evaluates how good those emails are using custom metrics**
3. **Compares two different prompting strategies**

The goal is not just to generate emails, but to **prove which approach works better and why**.

---

## 🔹 What problem I am solving

Most AI-generated emails:

* Miss important details
* Don’t match the correct tone
* Add unnecessary filler

So instead of just generating emails, I built a system that:

* Forces the model to include all important facts
* Controls tone properly
* Measures output quality in a structured way

---

## 🔹 How the system works (simple view)

For each test case:

1. Give the AI:

   * Intent (why the email is written)
   * Key facts (must be included)
   * Tone (style of writing)

2. Generate an email

3. Evaluate the email using 3 custom metrics

4. Repeat this for:

   * Model A (optimized)
   * Model B (naive)

5. Compare results

---

## 🔹 Project Structure

* `assistant.py` → Generates emails (Model A)
* `run_evaluation.py` → Runs full pipeline + comparison
* `evaluator.py` → Scores emails using 3 metrics
* `scenarios.py` → 10 test cases + human reference emails
* `results.csv / results.json` → Final evaluation output

---

## 🔹 Why I created 3 custom metrics

The assignment required custom evaluation, so I didn’t use generic metrics like BLEU.

Instead, I asked:
👉 *What actually makes an email “good”?*

I broke it into 3 core qualities:

---

### ✅ 1. Fact Recall (Most Important)

**Why this matters:**
If the email misses key facts, it is useless.

**Example:**
If the fact says:

* “Deadline is April 18”

And the model misses it → email fails.

**How I measure it:**

* I use an LLM as a judge
* It checks each fact individually
* Marks: yes / no

**Formula:**
Score = (facts included / total facts) × 10

---

### ✅ 2. Tone Adherence

**Why this matters:**
Same email can sound:

* polite
* aggressive
* casual

Tone changes everything.

**How I measure it:**

* LLM evaluates:

  * wording
  * sentence style
  * overall feel

**Output:**

* Score from 1–10
* Short explanation

---

### ✅ 3. Conciseness & Clarity

**Why this matters:**
Good emails are:

* clear
* not too long
* not full of useless phrases

**This metric has 2 parts:**

#### A. Brevity (rule-based)

Penalizes:

* filler phrases (like “hope this finds you well”)
* overly long emails

#### B. Fluency (LLM-based)

* checks readability and clarity

**Final formula:**
Score = 0.5 × Fluency + 0.5 × Brevity

---

## 🔹 Why I used these formulas

* Fact Recall → ensures correctness
* Tone → ensures communication quality
* Conciseness → ensures usability

Together, they cover:
👉 correctness + style + readability

---

## 🔹 Test Scenarios

I created **10 different scenarios** with:

* Different tones (formal, urgent, apologetic, etc.)
* Different contexts (job, startup, academic, support)
* 4–5 facts each

Each scenario also has a:
👉 **Human-written reference email** (ideal output)

---

## 🔹 Model Comparison

### 🔵 Model A (Optimized)

Uses:

* Strong system prompt
* Strict rules (fact inclusion is mandatory)
* Few-shot examples
* Low temperature (more controlled output)

👉 Goal: maximum accuracy and consistency

---

### 🔴 Model B (Naive)

Uses:

* No system prompt
* No examples
* Only basic input
* Higher temperature (more randomness)

👉 Goal: simulate a simple/default usage

---

## 🔹 Important Clarification

Both models use the **same base model (Qwen2.5:7B)**

The difference is:
👉 **how the model is instructed**

This shows:

* Prompt engineering can significantly change output quality

---

## 🔹 Results

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

## 🔹 What I learned from results

### 1. Model A performs better overall

* Best at including all facts
* More structured and reliable

### 2. Model B is still strong

* Slightly better tone flexibility
* But less consistent with facts

---

## 🔹 Key Insight (Important)

Even with the **same model**, results change based on:

* prompt design
* constraints
* temperature

 This proves prompt engineering is critical

---

## 🔹 Final Conclusion

 **Model A** 

* It guarantees fact inclusion
* Produces consistent outputs
* Is more controllable

Model B is useful for:

* quick drafts
* less critical use cases

---

## 🔹 How to run

1. Install Ollama
2. Pull model:

```
ollama pull qwen2.5:7b
```

3. Run:

```
python run_evaluation.py
```

---

