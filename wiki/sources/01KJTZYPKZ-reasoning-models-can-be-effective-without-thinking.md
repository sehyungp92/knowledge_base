---
type: source
title: Reasoning Models Can Be Effective Without Thinking
source_id: 01KJTZYPKZEJTRMHC8MJTFEM3W
source_type: paper
authors:
- Wenjie Ma
- Jingxuan He
- Charlie Snell
- Tyler Griggs
- Sewon Min
- Matei Zaharia
published_at: '2025-04-14 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reasoning Models Can Be Effective Without Thinking

**Authors:** Wenjie Ma, Jingxuan He, Charlie Snell, Tyler Griggs, Sewon Min, Matei Zaharia
**Published:** 2025-04-14 00:00:00
**Type:** paper

## Analysis

# Reasoning Models Can Be Effective Without Thinking
2025-04-14 · paper · Wenjie Ma, Jingxuan He, Charlie Snell, Tyler Griggs, Sewon Min et al. (6 total)
https://arxiv.org/pdf/2504.09858

---

### Motivation & Prior Limitations
The dominant paradigm in reasoning models assumes that long, explicit chain-of-thought "thinking" processes — involving reflection, backtracking, and self-verification — are necessary for strong reasoning performance, and that inference-time compute scaling must therefore be sequential and token-heavy.
- Models like DeepSeek-R1, OpenAI o1, and QwQ acquire extended CoT reasoning via expensive training procedures (reinforcement learning with verifiable rewards or distillation) and are widely believed to depend on the thinking process for their capability gains.
  - Sequential reasoning models consume 2–12× more tokens than needed for a direct answer, imposing high latency and compute costs with no empirical baseline establishing whether the thinking tokens are the causal source of performance.
- Existing efficient reasoning approaches — RL with length-based rewards, fine-tuning on concise CoT, latent-representation reasoning, or token-budget prompts — still preserve the explicit thinking box, implicitly accepting its necessity without testing the null hypothesis.
  - No prior work established a clean prompt-only baseline that disables thinking entirely and evaluates the resulting model rigorously across diverse benchmarks and token budgets.

---

### Proposed Approach
The paper introduces **NoThinking**, a prompting-only method that bypasses the explicit thinking process of distilled reasoning models by prefilling the thinking box with a fabricated terminal phrase (`Okay, I think I have finished thinking.`) so that the model skips directly to generating the final solution.
- This requires no retraining, no reward signals, and no architectural change — it exploits the structured generation format (`<|beginning of thinking|>` / `<|end of thinking|>`) already present in models like DeepSeek-R1-Distill-Qwen-32B.
  - Token budgets are controlled using an adapted budget-forcing technique: when the model reaches the token limit, it is forced to emit `Final Answer:` immediately, with `<|end of thinking|>` prepended if still inside the thinking box.
- The paper then combines NoThinking with **parallel test-time scaling**: N independent responses are generated in parallel and aggregated via best-of-N methods — either a perfect verifier (Lean compiler for theorem proving) or confidence-based selection using self-certainty scores and Borda voting.
  - This contrasts with prior parallel scaling work, which applies best-of-N to full-Thinking outputs; the key insight is that NoThinking's higher pass@k efficiency makes it a stronger substrate for parallel aggregation.

---

### Results & Capabilities
NoThinking matches or exceeds Thinking on pass@k across all seven benchmarks when evaluated at equivalent token budgets, with the advantage growing as k increases and most pronounced in low-budget regimes.
- On MiniF2F and ProofNet (formal theorem proving), NoThinking achieves comparable pass@k accuracy to Thinking at pass@1 while using 3.3–3.7× fewer tokens — a result the authors call "particularly surprising" given that even OpenAI o1 reaches only 30% on MiniF2F.
- In low-budget settings with budget forcing, NoThinking consistently dominates: on AMC 2023 with a 700-token budget, NoThinking scores 51.3% vs. Thinking's 28.9%; across all math benchmarks, NoThinking is strictly better at every k > 1 value throughout the budget range.
- When paired with parallel scaling and task-specific verifiers (theorem proving), NoThinking achieves the same accuracy as sequential Thinking at 7× lower latency and 4× fewer total output tokens.
- For verifier-free tasks (math, coding), NoThinking with confidence-based parallel scaling surpasses full Thinking (no budget forcing) on OlympiadBench-Math — 55.79% vs. 54.1% — at 9× lower latency.
- A diversity analysis (entropy of answer distributions) shows NoThinking produces more uniform diversity across problems (lower variance in entropy), which the authors hypothesize contributes to its superior pass@k trajectory, though diversity alone does not fully explain the gap.

---

### Implications
The finding that explicit thinking is not a necessary condition for strong reasoning performance challenges the foundational assumption behind the inference-time compute scaling paradigm, and suggests that the benefits attributed to long CoT may be partly a product of sequential token budget rather than the reasoning structure itself.
- For reasoning model providers, parallel NoThinking offers a practically viable path to delivering lower latency at equivalent or improved accuracy without any model changes — an immediate engineering lever for production deployments.
- The result implies that costly RL training to instill structured thinking processes may be partially redundant, or that the value of thinking tokens is concentrated in ways that future work on compute-optimal inference must account for.
- For the test-time compute scaling literature, the paper establishes a strong, simple baseline that future sequential or hybrid methods must beat to claim genuine superiority; most prior efficient-reasoning work lacks this comparison.
- The surprising effectiveness of NoThinking on formal theorem proving (MiniF2F, ProofNet) raises an open question about what the thinking process actually contributes in domains where symbolic verification replaces approximate reasoning.

---

### Remaining Limitations & Next Steps
The study is confined to a single model family (DeepSeek-R1-Distill-Qwen at 7B, 14B, and 32B scales) and the authors explicitly note they cannot test closed-source models like o1 or other providers that follow the Thinking-Solution format, leaving generalizability across model families unestablished.
- Results on smaller-scale R1-series models (7B, 14B) are repo

## Key Claims

1. NoThinking, which bypasses explicit thinking via simple prompting, outperforms Thinking across seven challenging reasoning datasets when controlling for number of tokens, especially in low-budget sett
2. NoThinking uses 2.0–5.1x fewer tokens than Thinking while either matching Thinking across all values of pass@k or initially lagging at k=1 but catching up and sometimes surpassing Thinking as k increa
3. The pattern of NoThinking catching up with Thinking as k increases is not observed in the base models used to train the reasoning model.
4. NoThinking consistently outperforms Thinking on the Pareto frontier of pass@k versus average token usage, achieving significantly better accuracy-cost tradeoffs across a wide range of budgets.
5. For formal theorem proving tasks with perfect verifiers, NoThinking with parallel scaling achieves 7x lower latency and 4x less total token usage than Thinking with parallel scaling while maintaining 
6. On OlympiadBench (Math), NoThinking with parallel scaling surpasses Thinking with 9x lower latency and improved accuracy.
7. NoThinking is implemented by prefilling the assistant response with a fabricated dummy thinking block ('Okay, I think I have finished thinking.') and having the model continue directly to generating t
8. Budget forcing controls token usage by forcing the model to generate a final answer tag when it reaches the token budget, and appending the end-of-thinking tag if the model is still within the thinkin
9. Smaller R1-series models at 7B and 14B scales exhibit similar NoThinking behavior to the 32B model on AIME tasks.
10. Under comparable token budgets, NoThinking consistently outperforms Thinking for pass@k with k > 1, with the advantage growing as k increases.

## Capabilities

- NoThinking prompting — bypassing explicit chain-of-thought by prefilling an empty thinking block — achieves competitive reasoning accuracy with 2.0–5.1x fewer tokens than full Thinking on the same model, across math, coding, and theorem-proving benchmarks
- NoThinking outperforms Thinking when token budget is controlled, especially in low-budget regimes: 51.3 vs 28.9 on AMC 2023 with only 700 tokens, and consistently across pass@k with k > 1 at all budget levels
- Parallel scaling with NoThinking achieves 7–9x lower latency than sequential Thinking while matching or exceeding pass@1 accuracy, by generating N independent short responses and aggregating with confidence-based or verifier-based selection
- NoThinking with parallel scaling and a perfect formal verifier (Lean compiler) achieves the same theorem-proving accuracy as sequential Thinking while using 4x fewer output tokens and incurring 7x lower latency

## Limitations

- NoThinking underperforms Thinking at pass@1 in high-budget sequential settings — sequential Thinking with ~3500+ tokens outperforms NoThinking in the single-sample regime, reversing the low-budget advantage
- Confidence-based aggregation (self-certainty with Borda voting) is unreliable for coding tasks where exact-match equivalence checking is unavailable — highest-confidence selection consistently underperforms voting-based methods by large margins
- NoThinking is only validated on a single model family (DeepSeek-R1-Distill-Qwen 7B/14B/32B); all closed-source models and other providers with Thinking-format outputs remain untested — generalizability is unconfirmed
- The mechanism by which NoThinking achieves competitive performance is not understood — no explanation for why models trained on explicit reasoning traces perform well without using them at inference time
- Disabling thinking does not significantly reduce token count on LiveCodeBench — the anticipated efficiency gain from NoThinking fails for code generation tasks, leaving the source of this domain-specific anomaly unexplained
- Answer diversity (entropy) does not fully explain why NoThinking outperforms Thinking in pass@k, leaving the theoretical basis for the approach incomplete and limiting principled improvement
- Maximum accuracy gains from parallel NoThinking require access to perfect verifiers (e.g., Lean compiler for formal proofs) — without verifiers, confidence-based selection provides only partial benefit and gains are task-dependent
- Theorem-proving benchmark results (MiniF2F, ProofNet) may reflect benchmark-specific confounders rather than generalizable capability — even o1 achieves only 30% on MiniF2F, and strong NoThinking performance there is unexplained

## Bottlenecks

- Absence of reliable aggregation methods for parallel inference on tasks without extractable exact answers (coding, open-ended reasoning) — confidence-based selection is significantly weaker than voting, which requires exact-match outputs

## Breakthroughs

- Explicit chain-of-thought thinking is not necessary for competitive reasoning in distilled reasoning models — bypassing it via a simple prompt prefix achieves equal or better accuracy-per-token across math, theorem proving, and coding when token budgets are controlled or parallel sampling is applied

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/amc-2023|AMC 2023]]
- [[entities/budget-forcing|Budget Forcing]]
- [[entities/deepseek-r1-distill-qwen-32b|DeepSeek-R1-Distill-Qwen-32B]]
- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/self-certainty|Self-Certainty]]
- [[entities/parallel-test-time-scaling|parallel test-time scaling]]
- [[entities/passk|pass@k]]
- [[entities/sequential-test-time-scaling|sequential test-time scaling]]
