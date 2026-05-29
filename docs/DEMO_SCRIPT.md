# Demo Script (2-3 Minutes)

## 1. Open With the Problem (20-30s)
- "Multilingual LLMs are often assumed to be neutral across scripts."
- "In practice, tokenizer behavior can inflate token counts for some languages."
- "That can increase cost, latency proxy metrics, and reduce equitable access."
- "PolyglotBench makes these disparities measurable in a live dashboard."

## 2. English Baseline Walkthrough (30-40s)
- Paste English text:
  - `Artificial intelligence is changing how people build software.`
- Select a few models and keep baseline as `gpt-4o-mini`.
- Click **Analyze**.
- Highlight:
  - token count
  - fertility
  - fairness score

## 3. Multilingual Contrast (40-50s)
- Replace text with Hindi or Arabic:
  - Hindi: `कृत्रिम बुद्धिमत्ता सॉफ्टवेयर बनाने के तरीके को बदल रही है।`
  - Arabic: `الذكاء الاصطناعي يغير طريقة بناء البرمجيات.`
- Analyze again with the same model set.
- Compare token multiplier and fairness score against the English run.
- Explain that higher inflation tends to lower fairness in the current metric design.

## 4. Visual Dashboard (20-30s)
- Point to charts:
  - Token count comparison
  - Token multiplier / estimated latency
  - Fairness score
- Mention estimated latency is currently a token-inflation proxy, not live runtime latency.

## 5. Leaderboard + Persistence (30-40s)
- Click **View Fairness Leaderboard**.
- Show ranked models by average fairness across curated multilingual benchmark samples.
- Save current run with **Save this analysis**.
- Open **Recent Community Analyses** and show the new row.

## 6. Export + Impact Close (20-30s)
- Export results as CSV.
- Mention research workflows:
  - spreadsheet analysis
  - benchmark tracking
  - reproducible reporting
- Close with: "PolyglotBench helps teams spot tokenization-driven disparities earlier and design fairer multilingual AI systems."
