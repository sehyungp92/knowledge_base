---
type: source
title: 'h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning'
source_id: 01KJTE0Y5SDE6VQ128WMXX8RMA
source_type: paper
authors:
- Sumeet Ramesh Motwani
- Alesia Ivanova
- Ziyang Cai
- Philip Torr
- Riashat Islam
- Shital Shah
- Christian Schroeder de Witt
- Charles London
published_at: '2025-10-08 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning

**Authors:** Sumeet Ramesh Motwani, Alesia Ivanova, Ziyang Cai, Philip Torr, Riashat Islam, Shital Shah, Christian Schroeder de Witt, Charles London
**Published:** 2025-10-08 00:00:00
**Type:** paper

## Analysis

# h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning
2025-10-08 · paper · Sumeet Ramesh Motwani, Alesia Ivanova, Ziyang Cai, Philip Torr, Riashat Islam et al. (8 total)
https://arxiv.org/pdf/2510.07312

---

### Motivation & Prior Limitations
- LLMs perform well on short-horizon reasoning tasks but experience severe accuracy degradation as the number of dependent reasoning steps increases, a problem the authors term long-horizon reasoning (LHR).
  - Observed accuracy on composed 6th-grade math problems (GSM8K) collapses from 82.79% at horizon-1 to 35.06% at horizon-2 and 3.57% at horizon-5, far below what independent-error compounding would predict (68.54% and 43.21% respectively), indicating that LHR failures stem from horizon-specific skill deficits — state tracking, intermediate value management — that cannot be explained by single-step accuracy alone.
  - Existing inference-time scaffolding and step-level supervision (process reward models) are costly and do not scale; obtaining genuine long-horizon training data is expensive and sample-inefficient.
- Standard RLVR on fixed datasets saturates quickly because data complexity is bounded: entropy collapses and no new reasoning difficulty is introduced, limiting the number of useful training steps.
  - Yue et al. (2025) established that RLVR on LLMs only improves sampling efficiency of capabilities already latent in the base model; at high pass@k, the RL-trained model's performance converges to and is bounded by the base model's ceiling, implying no genuinely new skills are learned under ordinary RLVR regimes.

---

### Proposed Approach
- h1 introduces a method of **serial compositional chaining**: short, self-contained atomic problems (e.g., individual GSM8K questions) are linked into explicit dependency chains of arbitrary length h, where each sub-problem's input is a deterministic transform of the previous answer, creating synthetic long-horizon data with no new human annotations or teacher-model labels.
  - Lightweight adapter functions φⱼ (identity, scaling, unit conversion) map answer yⱼ to input xⱼ₊₁, yielding a single prompt requiring correct stateful sequential reasoning supervised only by the final answer yₕ — enabling pure outcome-only RL with no per-step labels.
  - This differs fundamentally from approaches that use process reward models (PRMs), inference-time search, or step-level supervision; h1 requires no auxiliary models and trains the model to internalize LHR capabilities rather than scaffolding them at inference time.
- RL training proceeds through a **stagewise curriculum** over explicit horizons h = 1, 2, …, H_max using Dr. GRPO, with model parameters carried forward between stages, so each stage trains on problems at exactly the current capability frontier.
  - The curriculum contrasts sharply with three baselines — Only-L1 (train only on atomic problems), Uniform-Mix (random horizon sampling), and Only-Long (train only on the hardest chains) — all of which fail to produce long-horizon gains; Only-Long is especially ineffective due to vanishing gradient signal when success probability is near zero.
  - The theoretical framing models stepwise correctness as qⱼ = p(θ₀) · σⱼ(θⱼ), where p is atomic reliability and σⱼ is a horizon-depth-specific capability; the curriculum is designed to raise p in early stages and then independently improve each σⱼ in later stages, a decomposition that makes outcome-only RL tractable at longer horizons.

---

### Results & Capabilities
- Curriculum RL on composed GSM8K chains produces large in-domain accuracy gains: horizon-2 accuracy improves from 35.06% (instruct baseline) to 58.51% (+66.9%), horizon-4 from 6.70% to 18.77% (+180.1%), and horizon-5 from 3.57% to 9.82% (+175.1%), while preventing RL saturation by allowing training to scale 5× more steps than standard RLVR.
  - Ablations confirm that Only-L1 training shows negligible improvement at horizons ≥2, Uniform-Mix degrades performance, and Only-Long fails entirely, establishing that the specific stagewise curriculum structure is responsible for the gains.
- h1 demonstrates **genuinely new capability acquisition** beyond the base model, contradicting the Yue et al. (2025) finding for standard RLVR: at pass@128 on unseen horizons 6, 7, and 8, curriculum-trained models significantly outperform the instruct model and the Only-L1 RLVR baseline, which converge quickly to the base model's ceiling.
  - This is the paper's central theoretical-empirical claim: the σⱼ horizon-specific skills do not exist in the base model and are genuinely learned via compositional curriculum RL — not merely unlocked through better sampling.
- Training exclusively on composed 6th-grade math (GSM8K) generalizes to significantly harder implicit-horizon benchmarks: AIME 2024 improves from 5.10% to 10.52% (+106.3%), MATH-500 from 64.20% to 69.20% (+7.8%), GSM-Symbolic P2 from 43.08% to 52.00% (+20.7%), and MMLU Pro Math from 58.47% to 61.21%.
  - The transfer is cross-domain: ReasoningGym propositional logic improves from 22.90% to 47.10% (+2.06×), graph problems from 15.00% to 22.50%, and algorithmic sentence reordering from 9.60% to 18.80%, with only geometry and game-of-life showing minor regressions.
  - Long-context benchmarks also improve: LongBench-v2 from 35.00% to 37.90% and Hash-hop (ultra-long-context multi-hop variable tracing) from 15.98% to 18.73%, indicating that the state-tracking skill σⱼ transfers to input-side long-context tasks.
- Theoretically, curriculum RL achieves **polynomial sample complexity** in horizon length H rather than the exponential cost of direct full-horizon outcome training, and this scaling matches training with dense per-step rewards — providing a formal justification for why outcome-only curriculum RL is practical.
  - The SNR of the REINFORCE gradient estimator scales as Θ(N · sₕ), where sₕ is the cumulative success probability; at full horizon H, sₕ is exponentially small, requiring batc

## Key Claims

1. LLMs excel at short-horizon reasoning tasks but performance drops as reasoning horizon lengths increase
2. The lack of increasing problem difficulty and diversity in RL datasets causes improvements to saturate after very few training steps
3. h1 composes short-horizon problems into arbitrarily long chains of dependent reasoning steps to synthesize long-horizon training data without new annotations
4. Curriculum RL training on composed GSM8K problems achieves a 2.06× improvement on AIME 2024 relative to the instruct model baseline
5. Long-horizon accuracy depends on horizon-dependent skills such as intermediate value tracking and state management that cannot be learned solely from training on atomic problems
6. Observed long-horizon accuracy is much lower than what independent-error compounding would predict, indicating non-independent error sources
7. Even after standard RL training improving single-step accuracy, long-horizon performance remains far below the independent-error prediction
8. Standard RLVR on LLMs only improves the sample efficiency of reasoning capabilities already present in the base model and does not teach new capabilities
9. Curriculum RL training on compositional synthetic data teaches new capabilities that exceed the base model's performance even at pass@128
10. Curriculum RL with outcome rewards achieves an exponential improvement in sample complexity over full-horizon training, comparable to dense per-step supervision

## Capabilities

- Curriculum RL on synthetically composed short-horizon problems bootstraps long-horizon reasoning that transfers to significantly harder out-of-distribution benchmarks — 2.06x improvement on AIME 2024 and notable gains on MATH-500, ReasoningGym, and long-context benchmarks, trained only on composed 6
- Atomic problem composition via lightweight adapters creates arbitrarily long-horizon verifiable training chains from existing short-horizon data with no human annotation or teacher-model involvement
- Curriculum RL with outcome-only rewards teaches genuinely new long-horizon reasoning capabilities that exceed base model ability even at very high pass@128 — new reasoning paths are unlocked rather than merely latent capabilities surfaced
- Stagewise curriculum RL achieves polynomial sample complexity in horizon length H versus exponential complexity for direct full-horizon outcome-reward training — providing a training-efficient path to long-horizon RL without dense reward infrastructure

## Limitations

- LLMs exhibit severe non-multiplicative accuracy collapse on long-horizon tasks — actual performance degrades far faster than independent error compounding predicts, indicating the existence of horizon-specific capability deficits (state management, value tracking) that single-step accuracy improveme
- Standard RLVR training on fixed datasets saturates rapidly after a small number of training steps due to entropy collapse, preventing scaling to harder or longer-horizon problems
- Direct full-horizon RL training requires batch sizes exponential in horizon length H to achieve useful gradient signal — rendering it computationally infeasible for long chains without a curriculum
- H1's curriculum approach is confined to serial dependency chains — parallel, branching, or graph-structured compositional reasoning is not addressed, limiting coverage of real-world multi-step tasks
- Curriculum RL improvements are restricted to domains with verifiable ground-truth outcomes — the method is inapplicable to open-ended, subjective, or creative reasoning tasks lacking automated evaluation
- Long-horizon training produces selective OOD transfer — geometry and game-of-life performance degrades while other reasoning domains improve, indicating that horizon-dependent skills learned on math chain composition can interfere with or displace domain-specific skills
- Curriculum RL scaling properties are uncharacterised — the rate and ceiling of capability improvement with increased compute, model scale, and horizon length remain unknown
- H1 experiments are validated primarily on a 3B parameter model — applicability to frontier-scale models (70B+) that already possess strong long-horizon capabilities from RLHF/SFT is unverified
- Curriculum RL requires the base model to already solve atomic subtasks with non-trivial accuracy — the method fails when the model cannot reliably solve the simplest chain links, creating a minimum capability prerequisite
- Generalisation scope of the H1 approach is bounded by the domain of atomic task sources — current experiments rely solely on GSM8K math, leaving non-mathematical atomic skills unexplored and limiting transfer breadth

## Bottlenecks

- Long-horizon reasoning RL is blocked by exponentially vanishing gradient signal — composing problems into long chains means very few rollouts succeed, making gradient updates informationally useless without a curriculum to progressively raise the success rate
- Long-horizon verifiable training data is expensive and scarce — obtaining multi-step reasoning chains with verified intermediate and final answers requires expert labor or large-scale automated infrastructure, blocking RL scaling beyond simple benchmarks

## Breakthroughs

- Curriculum RL on synthetically composed short-horizon data teaches genuinely new long-horizon reasoning capabilities beyond base model limits at pass@128 — directly falsifying the prior finding that RLVR only surfaces latent base model capabilities
- Theoretical proof that curriculum RL achieves polynomial sample complexity in horizon length H while direct full-horizon outcome-reward training requires exponential sample complexity — with formal equivalence to dense per-step supervision established

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/grpo|GRPO]]
- [[entities/gsm-symbolic|GSM-Symbolic]]
- [[entities/gsm8k|GSM8K]]
- [[entities/rlvr|RLVR]]
- [[entities/passk|pass@k]]
