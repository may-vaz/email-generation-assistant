# Email Generation Assistant

An AI-powered email generation and evaluation system built with Google's Gemini API (free tier). Designed as an end-to-end assessment covering prompt engineering, custom evaluation metrics, and model comparison.

---

## Project Structure

```
email-assistant/
├── assistant.py        # Email generator with Few-Shot + CoT prompt
├── scenarios.py        # 10 test scenarios + human reference emails
├── evaluator.py        # 3 custom evaluation metrics (LLM-as-a-Judge)
├── run_evaluation.py   # Full evaluation runner, outputs CSV + JSON
├── requirements.txt
└── README.md
```

No unnecessary folders. Every file has a single, clear responsibility.

---

## Setup (Mac M1 / Apple Silicon)

**1. Get a free Gemini API key**

Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with a Google account, and create an API key. The free tier gives you 1,500 requests/day on `gemini-2.5-flash` with no billing required.

**2. Clone and set up the environment**

```bash
git clone <your-repo-url>
cd email-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

**3. Set your API key**

```bash
export GEMINI_API_KEY="your_key_here"
```

Add this to your `~/.zshrc` to avoid repeating it:
```bash
echo 'export GEMINI_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Running the Project

**Quick smoke test (single email generation):**
```bash
python assistant.py
```

**Full evaluation (all 10 scenarios, both strategies, all 3 metrics):**
```bash
python run_evaluation.py
```

This takes approximately 4–6 minutes due to rate-limit pauses on the free tier. It outputs:
- `results.csv` — full evaluation data in tabular format
- `results.json` — complete results with per-fact breakdowns and reasoning

---

## Prompting Strategy: Few-Shot + Chain-of-Thought

**Model A** (the main assistant) uses a combined technique:

- **Few-Shot Examples:** Two worked examples are embedded in the system prompt. These anchor the model's understanding of format, length, and professional register — far more reliably than description alone.
- **Chain-of-Thought (silent):** The system prompt instructs the model to reason through audience, fact priority, and tone before writing. The reasoning is internal — only the final email is returned. This prevents the model from defaulting to generic templates.

**Model B** (baseline comparison) uses the same underlying model (`gemini-2.5-flash`) but with a bare three-line system prompt and no examples. This is an ablation test: it isolates the contribution of prompt engineering, rather than attributing differences to a different model's capabilities.

---

## Custom Evaluation Metrics

### Metric 1 — Fact Recall Score (0–10)
**Definition:** Measures whether the generated email includes each of the key facts provided as input.  
**Logic:** An LLM judge reviews each fact and returns yes/no per fact. Score = (facts present / total facts) × 10.  
**Why it matters:** An email assistant that drops facts is functionally broken. Fluency means nothing if the client is missing the deadline or the link they need.

### Metric 2 — Tone Adherence Score (0–10)
**Definition:** Measures how accurately the email's vocabulary, register, and sentence structure match the requested tone.  
**Logic:** LLM-as-a-Judge rates tone match on a 1–10 scale with a one-sentence justification. Prompt is deliberately constrained to prevent grade inflation.  
**Why it matters:** The same information delivered in the wrong tone can damage relationships. A "firm and urgent" email that reads as passive fails its purpose entirely.

### Metric 3 — Conciseness & Clarity Score (0–10)
**Definition:** Measures whether the email communicates efficiently — no filler, no bloat.  
**Logic:** Two sub-scores averaged:
- **Brevity (automated):** Checks for a curated list of filler phrases (e.g., "I hope this email finds you well", "please do not hesitate") and penalises proportional to word count vs. expected length.
- **Fluency (LLM judge):** Rates readability and structural clarity from 1–10.  

**Why it matters:** Concise writing is a professional skill. Filler phrases inflate word count without adding meaning and are a reliable signal of low-quality generation.

---

