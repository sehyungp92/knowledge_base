---
type: source
title: 'The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning'
source_id: 01KJTDQZXFNEBRFPV0XD36EEWE
source_type: paper
authors:
- Milad Aghajohari
- Kamran Chitsaz
- Amirhossein Kazemnejad
- Sarath Chandar
- Alessandro Sordoni
- Aaron Courville
- Siva Reddy
published_at: '2025-10-08 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning

**Authors:** Milad Aghajohari, Kamran Chitsaz, Amirhossein Kazemnejad, Sarath Chandar, Alessandro Sordoni, Aaron Courville, Siva Reddy
**Published:** 2025-10-08 00:00:00
**Type:** paper

## Analysis

# The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning
2025-10-08 · paper · Milad Aghajohari, Kamran Chitsaz, Amirhossein Kazemnejad, Sarath Chandar, Alessandro Sordoni et al. (7 total)
https://arxiv.org/pdf/2510.06557

---

### Motivation & Prior Limitations
The standard RL "thinking environment" for reasoning LLMs is structured as an ever-growing context where the state equals the prompt concatenated with all prior reasoning tokens, making the state unbounded and forcing attention-based policies to pay quadratic compute cost as chains of thought lengthen.
- Existing mitigation strategies — length-regularized objectives, multi-stage training, early-exit pruning, token pruning — all operate within the LongCoT paradigm and therefore remain asymptotically quadratic; Zeng et al. (2025) shows multi-stage RL training even hurts final performance.
- The KV cache for a 1M-token trace on a small 1.5B model alone fills an entire H100 GPU, making very long reasoning traces physically impractical without expensive sequence-parallelism across GPUs.
- LongCoT-RL exhibits a hard test-time scaling ceiling: models trained with a fixed token budget plateau at that limit and cannot improve by allocating more compute at inference, strangling sequential test-time scaling as a lever.

---

### Proposed Approach
The paper introduces **Markovian Thinking**, a paradigm in which the policy conditions on a constant-size state regardless of total thinking length, decoupling "how long the model thinks" from "how much context it must process" and converting quadratic compute into linear compute with constant memory.
- The core insight is to redesign the MDP environment itself rather than constrain how much thinking occurs within the existing environment: by bounding the effective state, longer thinking becomes linear in FLOPs and constant in peak memory rather than quadratic.
- **Delethink** is the concrete instantiation: reasoning is organized into fixed-size chunks of C tokens; at each chunk boundary, the environment resets the context to a fresh prompt containing the original query plus the last m tokens of the previous chunk (the "textual Markovian state"), and all preceding reasoning tokens are deleted (hence "De-lete-think").
- The policy is trained via RL (PPO/GRPO family) to write a sufficient textual state near the end of each chunk so that reasoning can continue seamlessly after reset; the policy gradient is re-derived under the Delethink MDP, summing per-chunk objectives weighted by total trace length, making it a drop-in replacement for existing RL infrastructure.
- The environment is architecture-agnostic — it modifies only the sampling dynamics and imposes no constraints on model weights or attention — and Delethink can be applied zero-shot to off-the-shelf reasoning LLMs via "Delethink Tracing" without any fine-tuning.

---

### Results & Capabilities
An R1-Distill 1.5B model trained with Delethink using 8K-token chunks and a 24K total budget matches and surpasses LongCoT-RL trained with the same 24K budget on AIME'24, AIME'25, and HMMT'25 while consuming substantially less compute per RL step.
- Delethink's rollout throughput stays constant as thinking length increases (sustaining ~8,500 tokens/second/H100), whereas LongCoT-RL throughput declines steadily; at 96K average thinking length, LongCoT-RL costs an estimated 27 H100-months vs. 7 H100-months for Delethink — a ~4× wall-clock efficiency gain.
- Test-time scaling beyond training budget is qualitatively different for the two paradigms: LongCoT-RL 24K and 8K both plateau at their respective training limits, whereas Delethink continues to improve when given 100K+ additional tokens at inference — some AIME'25 problems are only solved with up to 140K thinking tokens despite the model being trained on 24K.
- Scaling to 96K training budget (I=23 chunks, C=8K) with only 150 additional RL steps starting from the 24K checkpoint reaches 49% on AIME'24 with average trace lengths of 36K–42K, demonstrating that the linear cost makes very long reasoning budgets practically feasible.
- Large SOTA reasoning models — GPT-OSS 120B and Qwen3-30B-A3B — exhibit robust Markovian Thinking zero-shot under Delethink Tracing across math competitions, PhD-level GPQA-Diamond, and coding tasks, with Qwen3 Delethink curves nearly coinciding with LongCoT curves; this confirms strong latent Markovian behavior in frontier models and signals scalability.
- Entropy remains roughly flat and non-collapsing throughout Delethink RL training, indicating stable learning comparable to LongCoT-RL.

---

### Implications
Redesigning the RL thinking environment rather than constraining thinking length is a qualitatively different lever — and potentially more powerful — than post-hoc efficiency techniques, suggesting that environment design deserves first-class attention in reasoning LLM research.
- Linear compute with constant memory opens a credible path toward reasoning models that think for millions of tokens, a regime that is physically infeasible for attention-based LongCoT regardless of hardware scaling.
- The demonstration that effective reasoning can proceed Markovian-style provides direct empirical support for adopting non-quadratic architectures (Mamba, linear attention, sparse/sliding-window attention) specifically for reasoning, resolving a long-standing uncertainty about whether these architectures can handle complex multi-step reasoning tasks — since thinking is shown to be structurally Markovian, sub-quadratic models should be able to leverage this directly without modification.
- The finding that SOTA models already exhibit latent Markovian traces zero-shot suggests that human reasoning itself may be approximately Markovian (carrying forward only necessary conclusions in spelled-out text), which has implications for how pretraining data shapes reasoning structure and how future training curricula might be designed.
- Delethink provides a natural interface

## Key Claims

1. The standard RL reasoning environment makes the state unbounded, growing with longer thoughts, and forces attention-based policies to pay quadratic compute as thoughts lengthen.
2. Markovian Thinking is a paradigm in which the policy advances reasoning while conditioning on a constant-size state, decoupling thinking length from context size, yielding linear compute with constant
3. Delethink is an RL environment that structures reasoning into fixed-size chunks; at chunk boundaries the context is reset and the prompt is reinitialized with a short carryover from the previous chunk
4. An R1-Distill 1.5B model trained with Delethink reasons in 8K-token chunks yet thinks up to 24K tokens, matching or surpassing LongCoT-RL trained with a 24K budget.
5. With test-time scaling, Delethink continues to improve where LongCoT-RL plateaus.
6. At 96K average thinking length, LongCoT-RL costs approximately 27 H100-months of compute versus 7 H100-months for Delethink.
7. The R1-Distill family (1.5B–14B) already samples Markovian traces zero-shot without additional training or prompting, recovering most of standard LongCoT performance.
8. GPT-OSS 120B exhibits robust Markovian Thinking zero-shot across PhD-level questions, coding tasks, math competitions, and crossword puzzles.
9. R1-Distill 1.5B trained with Delethink to think up to 96K tokens reaches 49% on AIME'24 with solutions averaging 36K tokens after only a few additional training steps.
10. Markovian Thinking could in principle let next-generation reasoning models think for millions of tokens by decoupling thinking length from context size.

## Capabilities

- Markovian Thinking (Delethink) enables RL training of reasoning LLMs with linear compute and constant memory by forcing the policy to reason in fixed-size context chunks with a short textual carryover — decoupling thinking length from context size and reducing training cost ~4x at 96K thinking token
- Delethink-trained R1-Distill 1.5B can reason up to 96K tokens (trained at 24K), reaching 49% on AIME'24 with solutions averaging 36K tokens — enabled by linear compute cost that makes extended RL training with very long thinking budgets feasible
- Delethink-trained models continue improving test-time accuracy far beyond their training-time thinking budget — scaling from 24K to 128K+ tokens at inference while LongCoT models plateau at training limits, with some AIME'25 problems only solved at 140K thinking tokens
- State-of-the-art reasoning LLMs (GPT-OSS 120B, Qwen3 30B-A3B, R1-Distill 1.5B–14B) exhibit latent Markovian Thinking zero-shot without any training or prompting — recovering most LongCoT performance in chunked inference across diverse benchmarks including PhD-level questions, math competitions, and 

## Limitations

- LongCoT RL training incurs quadratic compute costs blocking very long thinking budgets — training with average 96K thinking requires 27 H100-months under standard LongCoT, making large-scale long-thinking RL research economically inaccessible without alternative paradigms
- LongCoT models plateau at test-time when reasoning attempts to exceed training-time thinking budget — test-time scaling is hard-bounded by the training context limit and cannot generalise to longer reasoning chains
- Markovian Thinking is structurally incompatible with long-context retrieval tasks where the model depends on information distributed across a full context — RAG, long-document QA, and any task requiring backward references to earlier tokens cannot use Delethink
- Tasks requiring persistent live state larger than the Markovian carryover capacity — crossword grids, tiling puzzles, or any problem where the working state accumulates and cannot be compressed into m tokens — show meaningful performance degradation relative to LongCoT
- Chunk sizes ≤2K tokens significantly degrade Markovian reasoning quality — with only 1K tokens of Markovian state, the model loses the thread of reasoning across chunks, producing much lower accuracy at RL initialization and throughout training
- At sequence lengths below 32K tokens, Delethink incurs higher per-step compute than LongCoT — constant-factor overheads from chunk-boundary KV cache re-encoding and non-attention blocks dominate, with the efficiency crossover only occurring beyond 32K thinking tokens
- Delethink improvements on out-of-distribution tasks (GPQA-Diamond, LiveCodeBench) are modest — the gains observed on in-distribution math benchmarks do not transfer strongly to OOD domains, suggesting the approach's training benefits are domain-specific in its current form
- RL training of Delethink has only been validated at 1.5B parameter scale — evidence for SOTA models (up to 120B) is zero-shot only without RL fine-tuning; whether full-scale Delethink RL reproduces the training improvements at larger model sizes is unverified
- GPT-OSS 120B zero-shot Delethink with 8K chunk size lags behind LongCoT in test-time scaling — the 8K carryover is insufficient for SOTA 120B models zero-shot, requiring either larger chunk sizes (16K) or explicit RL fine-tuning to recover competitive performance
- All state-of-the-art frontier models — including hybrid architectures — still depend on quadratic self-attention; no production system uses truly linear architectures, making Delethink an environment-level workaround rather than an architectural solution to the quadratic scaling problem
- The mechanism explaining why Delethink outperforms LongCoT (rather than merely matching it) is speculative and unverified — hypotheses about short-context pretraining advantages, human Markovian reasoning patterns, and abstract representation pressure are offered without empirical validation

## Bottlenecks

- Quadratic compute and memory growth in standard LongCoT RL training blocks scaling to very long thinking budgets — the O(n²) attention cost makes RL training with >50K average thinking tokens economically infeasible for most research groups
- LongCoT test-time scaling is hard-bounded by training-time context length — models cannot leverage additional sequential inference compute beyond the thinking budgets they were trained on, preventing reasoning from saturating harder problems that require longer chains

## Breakthroughs

- The Markovian Thinking paradigm (Delethink) demonstrates that reasoning LLMs can be trained for arbitrarily long thinking chains with linear compute and constant memory — by restructuring the RL environment to use fixed-size chunks with learned textual state carryover, the quadratic attention bottle
- Delethink models trained at a modest 24K thinking budget continue improving accuracy when allowed to reason with 128K+ tokens at inference — demonstrating that the training thinking budget is not an intrinsic capability ceiling but an artifact of the LongCoT training environment that prevents genera

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/deepscaler-dataset|DeepScaleR Dataset]]
- [[entities/grpo|GRPO]]
- [[entities/kv-cache|KV Cache]]
- [[entities/ppo|PPO]]
- [[entities/rlvr|RLVR]]
- [[entities/sglang|SGLang]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/verl|verl]]
