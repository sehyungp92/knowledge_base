---
type: source
title: Chain-of-Thought Reasoning Without Prompting
source_id: 01KJVAAKMAAG1EF225E4C6QT5A
source_type: paper
authors:
- Xuezhi Wang
- Denny Zhou
published_at: '2024-02-15 00:00:00'
theme_ids:
- chain_of_thought
- interpretability
- model_behavior_analysis
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Chain-of-Thought Reasoning Without Prompting

**Authors:** Xuezhi Wang, Denny Zhou
**Published:** 2024-02-15 00:00:00
**Type:** paper

## Analysis

# Chain-of-Thought Reasoning Without Prompting
2024-02-15 · paper · Xuezhi Wang, Denny Zhou
https://arxiv.org/pdf/2402.10200

---

### Motivation & Prior Limitations
Prior work on eliciting chain-of-thought reasoning from LLMs has relied almost exclusively on prompting — either few-shot demonstrations with intermediate steps or zero-shot instructions like "Let's think step by step" — which introduces substantial human priors and makes it difficult to distinguish genuine model reasoning ability from learned prompt-following behavior.
- Prompting techniques encode task-specific human knowledge, making it impossible to cleanly assess a model's *intrinsic* reasoning capabilities since improvements could reflect "human teaching" rather than latent model ability.
  - Few-shot CoT prompting is task-specific, requires manual engineering per task, and produces inconsistent performance across prompt variants; zero-shot CoT still requires deliberately crafted trigger phrases.
- Greedy decoding — the standard inference procedure — systematically suppresses CoT reasoning paths, leading to the widespread but incorrect conclusion that pre-trained LLMs cannot reason without prompting.
  - On GSM8K, greedy decoding achieves only 9.9% (Mistral-7B) and 34.8% (PaLM-2 L), and the year parity task (whether a celebrity was born in an even/odd year) remains at chance (~50%) for even state-of-the-art models under direct prompting.
- Model fine-tuning and instruction-tuning can elicit CoT behavior but require expensive supervised data with CoT annotations and large compute budgets, limiting accessibility.

---

### Proposed Approach
The paper proposes **CoT-decoding**: rather than relying on the top-1 greedy token at each step, the method examines the top-*k* alternative tokens at the *first* decoding step, then continues greedy decoding from each branch, revealing CoT reasoning paths that are latent in the model's probability distribution but suppressed by standard greedy selection.
- The key insight is that pre-trained LLMs have internalized reasoning capabilities during pre-training, but greedy decoding preferentially selects direct-answer tokens (e.g., "5") over reasoning-initiating tokens (e.g., "I", "We") because the pre-training distribution skews toward simpler question formats.
  - This differs from sampling-based methods (self-consistency, temperature sampling, nucleus sampling) which do not force diversity at the critical first token and thus fail to escape the model's strong direct-answer prior without a CoT prompt.
- CoT paths are identified using a confidence metric Δ: the mean probability gap between the top-1 and top-2 tokens across all answer tokens in a given decoding path, inspired by minimum-margin active learning.
  - Paths with an embedded CoT systematically exhibit much higher Δ than direct-answer paths, allowing reliable selection without any external verifier, additional model, or supervised signal.
  - A weighted aggregation variant sums Δ values across all paths that agree on an answer, further stabilizing results against logit sensitivity.
- The method is entirely unsupervised, requires no prompt engineering, no fine-tuning, no additional models, and works at inference time with O(*k*) compute relative to greedy decoding's O(1).

---

### Results & Capabilities
CoT-decoding is the only decoding strategy tested that substantially improves reasoning over greedy decoding; all other alternatives (top-*k* sampling, nucleus sampling, beam search, temperature sampling) either match or *hurt* greedy performance on Mistral-7B GSM8K.
- On GSM8K, CoT-decoding achieves 25.1% (Mistral-7B) and 63.2% (PaLM-2 L) versus greedy baselines of 9.9% and 34.8% — representing gains of +15.2 and +28.4 percentage points respectively, with self-consistency without CoT prompt achieving only 12.9% / 40.6%.
- On year parity, CoT-decoding lifts performance from ~57% (near-chance) to ~95% on PaLM-2 L, a task where greedy scaling shows zero improvement — performance stays flat across model sizes until CoT paths are recovered.
- CoT-decoding on the pre-trained PaLM-2 L (63.2% GSM8K) nearly matches the instruction-tuned version of the same model (67.8%), demonstrating that a substantial portion of instruction-tuning's reasoning gains can be recovered via decoding alone, without any supervised data.
- When combined with zero-shot CoT prompting, the aggregated CoT-decoding achieves 48.4% (Mistral-7B) and 87.0% (PaLM-2 L) on GSM8K, outperforming self-consistency with zero-shot CoT (39.4% / 85.3%) at the same compute budget.
- The method generalizes across PaLM-2 (XS through L), Mistral-7B, and Gemma-7B, and improves both pre-trained and instruction-tuned variants, suggesting the finding is model-family-agnostic.
- Manual analysis of the top-100 GSM8K questions found that 88% of the highest-confidence decoding path (by Δ) among the top-10 paths contained a CoT, confirming the reliability of the confidence-CoT correlation.

---

### Implications
CoT-decoding provides a cleaner empirical lens on LLMs' *intrinsic* reasoning abilities by eliminating prompting as a confounder, reframing much of the prior reasoning literature: the failure of direct-answer prompts is largely an artifact of greedy decoding, not a fundamental model limitation, and existing CoT prompts primarily serve to reorder latent reasoning paths toward the top of the distribution rather than inject new capability.
- This result challenges the test-time compute paradigm: significant reasoning gains are achievable by exploring a small branching factor (*k* = 10) at a single token position, without requiring the much heavier compute of iterative self-refinement, tree search, or verification networks.
- The finding that pre-training distribution heavily shapes which CoT paths exist (simple tasks have latent CoT paths; highly synthetic multi-step tasks do not) provides a mechanistic learning-dynamics hypothesis: instruction-tuning and few-shot prompting "promote" ex

## Key Claims

1. CoT reasoning paths can be elicited from pre-trained LLMs by simply altering the decoding process, without any prompting
2. Standard greedy decoding obscures inherent reasoning capabilities of LLMs
3. The belief that LLMs are inherently incapable of effective reasoning without prompting is an artifact of considering only the greedy decoding path
4. The presence of a CoT path in the decoding process correlates with higher model confidence in the final answer, measurable as a larger probability gap between top-1 and top-2 tokens in the answer span
5. 88% of highest-confidence decoding paths among the top-10 for GSM8K questions contain CoT paths
6. CoT-decoding is the only decoding strategy that effectively improves language model reasoning; other alternatives including temperature sampling, top-k sampling, nucleus sampling, and beam search eith
7. Self-consistency without CoT prompting fails to match CoT-decoding because the model has a strong tendency to provide direct answers, making the first token less diverse under sampling
8. CoT-decoding effectively elicits reasoning across multiple language model families including PaLM-2, Mistral, and Gemma, sometimes doubling or tripling performance over greedy decoding
9. CoT-decoding yields +10-30% absolute accuracy gains on GSM8K across PaLM-2 model scales
10. Under greedy decoding, year parity task performance remains flat across model scales, but CoT-decoding recovers the CoT paths and achieves near-perfect accuracy at larger scales

## Capabilities

- Pre-trained LLMs can produce chain-of-thought reasoning paths by exploring top-k alternative tokens at the first decoding step, without any CoT prompting, instruction tuning, or fine-tuning — achieving 72% on GSM8K (vs 44% greedy) and 95% on year parity (vs 57% greedy) using PaLM-2 Large
- The probability gap between the top-1 and top-2 decoded answer tokens (delta metric) reliably identifies CoT vs non-CoT decoding paths — 88% of top-delta paths among top-10 contain genuine CoT chains on GSM8K, significantly outperforming model log-probability and length-normalized log-probability as
- CoT-decoding enables a pre-trained model to approach instruction-tuned performance without any supervised data — pre-trained PaLM-2 Large reaches 63.2% on GSM8K vs 67.8% for the instruction-tuned version of the same scale
- CoT-decoding stacks additively on top of zero-shot CoT prompting, achieving 87.0% on GSM8K with aggregated paths (vs 85.3% for self-consistency with zero-shot CoT prompting) and 48.4% vs 39.4% on Mistral-7B

## Limitations

- LLMs lose track of intermediate states in multi-step symbolic tasks as complexity scales — on Coin Flip and Web-of-Lies, models produce CoT paths that simulate steps but accumulate state-tracking errors, revealing an intrinsic architectural vulnerability not fixed by CoT-decoding
- Correct CoT paths become inaccessible beyond 2-3 reasoning steps — models can generate valid CoT paths for tasks requiring 1-2 knowledge manipulation steps but fail systematically beyond that, with multi-step arithmetic at depth 2, length 4 reaching only 16% even with CoT-decoding
- LLMs systematically apply left-to-right calculation order in CoT paths even when correct mathematical precedence (operator order of operations) requires different sequencing — an intrinsic bias not corrected by CoT-decoding
- Standard greedy decoding deployment systematically suppresses model reasoning capabilities — benchmark results using greedy decoding do not reflect intrinsic LLM reasoning ability, meaning the field has been measuring an artifact of the decoding procedure rather than true capability
- For highly synthetic and novel reasoning tasks absent from pre-training distribution, CoT paths are rarely present in any of the top-k decoding paths — few-shot CoT prompting in these cases teaches genuinely new solution strategies rather than surfacing existing capabilities
- CoT-decoding requires white-box access to model token probabilities (logits) — it cannot be applied to commercial API-only models such as GPT-4 or Claude that do not expose full vocabulary distributions; this restriction is never discussed in the paper despite its significance for practical adoption
- Confidence-based path selection degrades for open-ended answers — the probability gap between top-2 tokens is less precise as an indicator of correctness when answers are not closed-form (numerical, categorical), blocking extension of CoT-decoding beyond structured reasoning tasks
- CoT-decoding requires k forward passes through the model (one per alternative decoding path), multiplying inference compute by k — creating a O(k) compute cost at deployment time that blocks low-latency production use
- Standard sampling strategies (temperature, top-k, nucleus) fail to elicit CoT reasoning without prompts — the model's strong bias toward direct first-answer tokens overwhelms sampling diversity, so self-consistency without CoT prompting achieves only 12.9% vs CoT-decoding's 25.1% on Mistral-7B GSM8K
- Branching at later decoding steps is severely constrained by previously committed tokens — early incorrect tokens dramatically reduce the probability of recovering correct reasoning paths mid-sequence, making mid-path correction practically infeasible at the first token
- Instruction-tuned models occasionally still produce direct answers without CoT even after fine-tuning on CoT data — CoT-decoding provides additional gains (+7% on GSM8K, +28.7% on MultiArith for Mistral-7B inst-tuned), indicating instruction tuning incompletely instills CoT generation

## Bottlenecks

- Standard greedy decoding deployment suppresses latent CoT reasoning capabilities in pre-trained LLMs — production systems default to greedy decoding, which systematically selects direct-answer tokens over reasoning paths that exist in lower-probability alternatives
- Absence of reliable open-ended answer confidence metrics blocks CoT-decoding from scaling beyond closed-form reasoning tasks — the probability-gap signal that enables CoT path selection degrades outside numerical/categorical answer spaces
- Pre-training distribution skew toward simple tasks creates a hard ceiling on intrinsic multi-step reasoning — correct CoT paths for tasks requiring 3+ reasoning steps are absent from the top-k decoding space regardless of k, and cannot be recovered without few-shot demonstrations that teach rather t

## Breakthroughs

- CoT reasoning capability is latent in pre-trained LLMs and was previously hidden by greedy decoding — a simple decoding modification (top-k first-token branching with confidence-based path selection) elicits near-instruction-tuned reasoning performance without any prompting or supervised data

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/interpretability|interpretability]]
- [[themes/model_behavior_analysis|model_behavior_analysis]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gsm8k|GSM8K]]
- [[entities/speculative-decoding|Speculative Decoding]]
- [[entities/instruction-tuning|instruction tuning]]
