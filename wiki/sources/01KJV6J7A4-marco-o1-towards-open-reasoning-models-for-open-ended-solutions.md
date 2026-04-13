---
type: source
title: 'Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions'
source_id: 01KJV6J7A4PJ91RSCRYNM08706
source_type: paper
authors:
- Yu Zhao
- Huifeng Yin
- Bo Zeng
- Hao Wang
- Tianqi Shi
- Chenyang Lyu
- Longyue Wang
- Weihua Luo
- Kaifu Zhang
published_at: '2024-11-21 00:00:00'
theme_ids:
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions

Marco-o1 is an open attempt to replicate and extend OpenAI o1-style reasoning beyond closed-domain benchmarks, combining supervised fine-tuning on curated Chain-of-Thought data with Monte Carlo Tree Search (MCTS) at inference time. Rather than training a separate reward model, it uses token log-probability confidence scores as a heuristic reward signal, enabling inference-time search in domains — most notably machine translation — where ground-truth verifiers do not exist.

**Authors:** Yu Zhao, Huifeng Yin, Bo Zeng, Hao Wang, Tianqi Shi, Chenyang Lyu, Longyue Wang, Weihua Luo, Kaifu Zhang
**Published:** 2024-11-21
**Type:** Paper · [arxiv](https://arxiv.org/pdf/2411.14405)
**Themes:** [[themes/chain_of_thought|Chain of Thought]] · [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/reinforcement_learning|Reinforcement Learning]] · [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] · [[themes/search_and_tree_reasoning|Search & Tree Reasoning]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Motivation

OpenAI's o1 demonstrated exceptional reasoning on closed-domain benchmarks (AIME, CodeForces), but its technical roadmap remains opaque. The central question Marco-o1 investigates is whether large reasoning models (LRMs) can generalize to **open-ended domains** where correct answers are not uniquely defined and rewards are hard to quantify.

Two structural gaps motivated the work:

1. **RL-based reasoning is domain-restricted.** Existing approaches work well for math, physics, and coding because these have verifiable ground truth. Domains like translation or nuanced language understanding lack equivalent reward signals.
2. **Standard LLM inference is single-pass.** Models cannot recover from early reasoning errors or discover higher-confidence reasoning chains that exist but were not initially sampled. Coarse action granularity in tree search compounds this — full reasoning steps cause the model to miss sub-step reasoning pivots.

---

## Approach

### Base Model and Training Data

Marco-o1 fine-tunes **Qwen2-7B-Instruct** on ~60K samples:
- 45,125 samples from the filtered Open-O1 CoT dataset
- 10,000 MCTS-synthesized Marco-o1 CoT samples (synthetic, computationally expensive to generate)
- 5,141 Marco instruction-following samples

### MCTS at Inference Time

Each node in the MCTS tree represents a reasoning state; actions are LLM outputs representing potential next steps. The reward signal is derived entirely from the model's own output distribution — no external verifier or trained reward model is used.

For each token $t_i$, confidence is computed as:

$$c_i = \frac{\exp(p(t_i))}{\sum_{k=1}^{5} \exp(p(t_k))}$$

The rollout reward is the mean confidence across all tokens in the path — softmax-normalised log-probability of the chosen token against its top-5 alternatives.

Three action granularities are explored:
- **Full reasoning steps** — coarse; misses nuanced intermediate states
- **64-token mini-steps** — finer; expands solution space
- **32-token mini-steps** — finest practical granularity; best on MGSM-Zh

Token-level search is acknowledged as theoretically optimal but currently impractical due to exponential branching costs and the absence of a token-level reward design.

### Reflection Mechanism

After each thought, the prompt *"Wait! Maybe I made some mistakes! I need to rethink from scratch."* is appended, inducing self-critique without any external feedback signal. This recovers approximately 50% of problems the base model initially answers incorrectly.

---

## Results

| Model | MGSM-En (Test@1) | MGSM-Zh (Test@1) |
|---|---|---|
| Qwen2-7B-Instruct (base) | 84.00% | 76.80% |
| Marco-o1-CoT | ~84% | 71.20% ↓ |
| Marco-o1-MCTS (step) | **90.40%** | 80.00% |
| Marco-o1-MCTS (32-token) | ~88% | **82.40%** |

At Test@32, all MCTS variants reach 99.2–99.6% on MGSM-En versus 96.0% for the base model — quantifying the headroom that better search and reward modeling could unlock.

**Notable first:** Marco-o1 is the first LRM applied to machine translation, correctly rendering culturally-specific Chinese slang (e.g., "stepping-on-poop sensation" → "comfortable sole") where Google Translate fails. This is the paper's primary claim about open-ended generalisation.

---

## Capabilities

- **MCTS-guided reasoning** achieves +6.17%/+5.60% over base on MGSM-En/Zh using token confidence as a proxy reward *(maturity: research_only)*
- **Self-reflection prompt injection** recovers ~50% of initially-failed hard problems without any training or external feedback *(maturity: research_only)*
- **Mini-step MCTS (32–64 tokens)** expands reasoning solution space beyond coarse full-step actions *(maturity: research_only)*
- **LRM applied to translation** — inference-time scaling improves colloquial/slang translation quality over Google Translate *(maturity: demo)*

---

## Limitations

> Limitations are listed in descending severity. The most significant are structural, not incidental.

**Blocking:**
- **No trained reward model.** The system relies entirely on heuristic confidence scores. Authors identify training an ORM/PRM as future work — this gap directly caps reliability and blocks principled scaling. The confidence-score signal is noisier than a trained reward model and introduces substantial randomness into tree search results.
- **No scalable reward for open-ended tasks.** MCTS and RL-based inference-time scaling cannot reliably extend beyond math/coding to domains lacking ground truth. The paper poses this as an open question without resolution.

**Significant:**
- **Substantially underperforms OpenAI o1.** The paper concedes the model "primarily exhibits o1-like reasoning characteristics" and "falls short of a fully realized o1 model."
- **English-only CoT fine-tuning actively hurts multilingual reasoning.** Marco-o1-CoT scores 71.2% on MGSM-Zh versus 76.8% for the untuned base model. Fine-tuning on monolingual reasoning chains degrades cross-lingual transfer.
- **Token-level MCTS is computationally impractical.** The theoretically optimal search granularity cannot be used in practice, forcing coarser approximations.
- **No consistent best granularity.** Different action granularities win on different benchmarks (step for MGSM-En, 32-token for MGSM-Zh) — optimal search granularity is task- and language-dependent, with no principled selection method.
- **Synthetic training data is small and expensive.** ~10K MCTS CoT samples limit volume and diversity.
- **Unclear LRM technical roadmap.** The field lacks consensus on the correct training recipe — the paper explicitly cites this as its motivation.

**Minor:**
- **Incomplete reasoning traces.** MCTS chains can skip explicit logical steps even when producing correct answers (e.g., skipping the final letter 'y' in a word problem), suggesting the model shortcuts rather than fully reasons.

---

## Bottlenecks Addressed / Exposed

**Partially addresses:**
- [[themes/test_time_compute_scaling|Test-time compute scaling]] in non-math domains — demonstrates MCTS can improve translation quality, but without a reliable reward signal.

**Exposes / deepens:**
- **Reward model absence for MCTS reasoning** — token probability heuristics introduce randomness that caps performance. The confidence score reward is a workaround, not a solution. *(Horizon: 1–2 years)*
- **Token-level search compute wall** — exponential branching costs make fine-grained inference-time search infeasible at scale. *(Horizon: 1–2 years)*
- **Open-ended domain reward gap** — no scalable verification mechanism exists for creative, linguistic, or multi-criteria tasks, blocking generalisation of LRM training and inference-time scaling. *(Horizon: 3–5 years)*

---

## Breakthrough

**First application of LRM inference-time compute scaling to machine translation.** By extending MCTS-guided extended CoT to a domain with no verifiable ground truth, Marco-o1 demonstrates that the search-and-reflect paradigm is not intrinsically bound to formal domains — the model can self-evaluate plausibility in linguistic tasks even absent a formal correctness criterion. This is a notable expansion of where RLHF-free reasoning improvements are possible, though the evidence base is qualitative (case studies only, no systematic benchmark).

---

## Open Questions

1. Can the confidence-score reward be replaced by a trained process reward model (PRM) without requiring ground truth, enabling reliable MCTS scaling beyond math/code?
2. Does optimal MCTS action granularity systematically co-vary with task type, language, or reasoning depth — and can this be predicted without grid search?
3. How much of the Test@1 → Test@32 performance gap (~12pp on MGSM-En) is recoverable with a better reward signal versus fundamental limits of the base model?
4. Can LRM inference-time scaling generalise to domains with multi-criteria evaluation (e.g., creative writing, legal reasoning) where plausibility is evaluable but correctness is not?
5. Does multilingual reasoning require multilingual CoT fine-tuning data, or can cross-lingual transfer be preserved with mixed-language training?

---

## Related

- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] — the central scaling axis explored
- [[themes/search_and_tree_reasoning|Search & Tree Reasoning]] — MCTS as the inference-time mechanism
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — the broader paradigm Marco-o1 attempts to extend
- [[themes/chain_of_thought|Chain of Thought]] — the fine-tuning data format and reasoning representation

## Key Concepts

- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
- [[entities/large-reasoning-model-lrm|Large Reasoning Model (LRM)]]
