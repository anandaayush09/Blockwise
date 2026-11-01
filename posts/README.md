# Posts

Write one short post (300-500 words) about **one failure you found and how you fixed it**. Interviewers ask about this, so pick a real one with evidence.

## Template
1. **What I expected** (one sentence)
2. **What actually happened** (the symptom, with a number or a screenshot)
3. **How I found the cause** (what you checked, in order; what was a red herring)
4. **The fix** (and how you verified it - a test or eval row that now exists)
5. **What I changed in my process** (so it does not happen again)

## Failure modes to watch for while building (candidates)
- A backtest saving that vanished after fixing look-ahead leakage.
- A UTC/IST off-by-one that shifted every block by one.
- A DSM sign or unit mix-up (% of schedule vs. capacity).
- Penalty not convex, so the LP gave a strange schedule until binaries were added.
- Simultaneous battery charge and discharge exploiting a price pattern.
- Retrieval returning a superseded clause with high confidence.
- Embeddings missing an exact clause number that BM25 found.
- The agent producing a number that was not in any tool result (guardrail catch).
- An agent looping, or choosing the wrong tool for an ambiguous question.
- A prompt-injection string in a retrieved document.
- CI evals that cost real money on every push.

Keep notes as you go (date, symptom, cause); the post is then easy to write.
