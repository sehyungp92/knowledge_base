---
type: source
title: 'From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing
  Old Ones'
source_id: 01KJT3ZXPZ651405J33E90HCG4
source_type: paper
authors:
- Lifan Yuan
- Weize Chen
- Yuchen Zhang
- Ganqu Cui
- Hanbin Wang
- Ziming You
- Ning Ding
- Zhiyuan Liu
- Maosong Sun
- Hao Peng
published_at: '2025-09-29 00:00:00'
theme_ids:
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones

**Authors:** Lifan Yuan, Weize Chen, Yuchen Zhang, Ganqu Cui, Hanbin Wang, Ziming You, Ning Ding, Zhiyuan Liu, Maosong Sun, Hao Peng
**Published:** 2025-09-29 00:00:00
**Type:** paper

## Analysis

# From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones
2025-09-29 · paper · Lifan Yuan, Weize Chen, Yuchen Zhang, Ganqu Cui, Hanbin Wang et al. (10 total)
https://arxiv.org/pdf/2509.25123

---

### Motivation & Prior Limitations
- A central open debate in LLM post-training is whether RL teaches genuinely new skills or merely reweights and reranks existing capabilities already present in the base model from pretraining.
  - Recent work (Yue et al., 2025; Wu et al., 2025a) observed that as the sampling budget k increases in pass@k evaluation, the performance gap between RL-trained and base models narrows, leading to the conclusion that RLVR only distills base-model pass@k into pass@1 rather than learning new abilities.
  - Other work (Gandhi et al., 2025; Liu et al., 2025b; Zhao et al., 2025) characterized "aha moments" in RL training as amplification of pre-existing cognitive behaviors, not emergent skill acquisition.
- Prior investigations into this question suffered from three confounding factors: data contamination (pretrained LLMs may have seen benchmark-adjacent data), coarse-grained aggregate metrics that conflate easy and hard problems, and mixed-difficulty benchmarks where improvements on a specific skill type are masked by bottlenecks in other skills.
  - Sun et al. (2025) concluded RL does not promote compositional generalization, but their training included no explicit compositional incentive, making their setup an inadequate test of the hypothesis.
- The entropy collapse phenomenon and the difficulty of distinguishing genuine learning from capability activation further impede clean analysis of RL's role in LLM post-training.

---

### Proposed Approach
- The paper introduces a controlled synthetic testbed based on string transformation prediction to cleanly isolate RL's capacity for compositional skill acquisition, free from data contamination and ambiguous skill boundaries.
  - 25 unique string transformation functions are constructed with meaningless identifiers (e.g., `func_16`) so that functionality cannot be inferred from names, and function definitions are hidden during both RL training and evaluation, making tasks unsolvable without prior atomic skill acquisition.
  - Compositional difficulty is precisely controlled via nesting depth: Level-n problems require n-function composition (e.g., Level-2: `func_16(func_15(x))`), enabling fine-grained evaluation across a difficulty spectrum rather than a single aggregate score.
- Training uses a two-stage protocol that separates atomic skill acquisition from compositional skill learning: Stage 1 uses rejection fine-tuning (RFT) to internalize each function's behavior independently (without definitions in prompt); Stage 2 trains either with online RL via GRPO (binary correctness reward, no reasoning demonstrations) or offline RFT on compositional problems, enabling a direct comparison.
  - This mirrors the cognitive skill acquisition model from Anderson (1982), where humans learn new cognitive skills by composing and then internalizing existing atomic ones.
  - The paper formalizes the **RL Compositionality Hypothesis**: once a model has acquired the necessary atomic skills via NTP training, RL with proper compositional incentivization can teach the model to compose those skills into genuinely new, more complex capabilities.
- Generalization is assessed along three axes: held-out evaluation (compositions of functions not seen in RL training), easy-to-hard transfer (evaluating on Level-3 through Level-6 after training only on Level-2), and cross-task transfer (testing whether compositional skill learned on the string task transfers to the Countdown arithmetic task).

---

### Results & Capabilities
- RL on Level-2 compositional problems teaches genuinely new skills that generalize to unseen, harder compositional problems: accuracy on Level-3 problems improves from ~5% to ~30%, and on Level-4 from ~1% to ~15%, despite the model never training on problems beyond Level-2.
  - This generalization trend continues to Level-5 and Level-6, indicating the model has internalized a general principle of compositional reasoning rather than memorizing specific compositions.
  - RL trained only on Level-1 atomic problems peaks at ~90% accuracy on Level-1 but remains near zero on Level-2 and above, demonstrating that atomic RL alone is insufficient to unlock compositional capability.
- RL decisively outperforms iterative RFT on the same compositional data: the RL Level-2 model achieves 64% on Level-2 and 27% on Level-3, while iterative RFT never surpasses 2.6% on Level-3 and only reaches 15% on Level-2 (the same difficulty it was trained on), failing to generalize even within the same difficulty tier.
- Compositional skills learned via RL transfer across task domains: a model trained on string compositional RL (Multi-Base + RL L1+2) achieves 35% accuracy on unseen Level-3 Countdown problems, outperforming the Multi-Base baseline by more than 18 percentage points, despite never receiving RL training on Countdown.
  - Critically, a model with compositional RL on strings but without Countdown atomic skills (String-Base + RL L1+2) fails completely on Countdown, confirming that target-domain atomic skills are a prerequisite for transfer — the compositional skill acts as a meta-skill that enhances use of existing atomic knowledge.
- The paper rebuts the "reranking illusion" with pass@k analysis: on easy problems (Levels 1-2) where the base model already solves some instances, the performance gap shrinks with larger k, consistent with the reranking narrative; but on hard compositional problems (Levels 3-6) where the base model's pass@k is near zero, the RL Level-1+2 model's gap over the RFT base *widens* with k — at Level-5, the gap grows from 4% at pass@1 to ~25% at pass@1024.
- Behavioral analysis using Gemini-2.5-Pro to classify failure modes reveals that RL Level-2 fundamentally transforms how models fail: RFT Base,

## Key Claims

1. RL enables LLMs to acquire genuinely new skills by composing existing atomic skills, mirroring the human cognitive skill acquisition mechanism described by Anderson (1982).
2. RL on Level-2 compositional problems improves held-out Level-3 accuracy from near-zero (~5%) to approximately 30%, and Level-4 from ~1% to 15%, demonstrating easy-to-hard generalization.
3. RL training on atomic-only (Level-1) problems is insufficient to produce compositional skills; accuracy on Level-2 remains below 25% and Levels 3–6 stay near zero.
4. Both RL and compositional training incentives are jointly necessary for learning generalizable compositional skills; either alone is insufficient.
5. Task-specific atomic skills are a prerequisite for cross-task compositional transfer; a model with compositional RL training but lacking the target task's atomic skills fails completely on the target 
6. The 'reranking illusion' describes how aggregate pass@k metrics on mixed-difficulty benchmarks mask genuine skill acquisition by conflating problems where the base model already succeeds with problems
7. On hard compositional problems (Levels 3–6) where the base model's pass@k is near zero, the RL Level 1+2 model's performance gap over the RFT base widens as k increases — the opposite of the 'rerankin
8. None of the compositional learning findings (generalization, transfer) are observed when training with next-token prediction (supervised fine-tuning) on the same data.
9. The 'aha moments' attributed to RL training may not be emergent but rather the result of amplifying existing cognitive behaviors already present in base models, according to recent critics.
10. RL exploration is impeded by entropy collapse, and performance gaps between base and RL-trained models diminish as k increases in pass@k evaluations — observations that have fueled pessimism about RL'

## Capabilities

- RL training on compositional tasks enables LLMs to learn genuinely new compositional skills — composing known atomic skills to solve previously unsolvable problems — with generalisation to unseen function compositions and higher nesting depths than seen in training
- Compositional reasoning skills acquired via RL on one task transfer to a structurally different target task as a domain-agnostic meta-skill, provided the model already possesses the target task's atomic skills
- RL genuinely expands pass@k performance ceilings on hard compositional problems — not merely reranking base model distributions — evidenced by a widening performance gap at higher sample budgets on problems where the base model has near-zero pass@k

## Limitations

- All compositional RL findings are demonstrated only in a synthetic string-transformation testbed — whether RL compositional learning generalises to natural reasoning domains (mathematics, code generation, scientific reasoning) remains undemonstrated
- RL on atomic tasks alone fails entirely to develop compositional skills — explicit compositional incentive (training on compositional problems) is a necessary prerequisite; without it, generalisation above training difficulty level remains near zero
- RFT (rejection fine-tuning / supervised learning on correct trajectories) on compositional data fundamentally fails to generalise even to held-out problems of the same difficulty — achieving less than 2.6% on Level 3 vs. RL's 27%, and only 15% on Level 2 training problems
- Compositional RL generalisation degrades sharply with nesting depth — accuracy at Level 5 is ~5-6%, Level 6 ~2%, Level 7 ~1%, Level 8 ~0.5% — revealing a steep performance cliff beyond Level 4 even for models explicitly trained on composition
- Cross-domain compositional skill transfer requires the target domain's atomic skills to be pre-acquired via supervised training — models with compositional RL but without target-domain atomic knowledge fail completely on transfer tasks
- Standard mixed-difficulty benchmarks create a 'reranking illusion' — aggregate pass@k metrics on easy-dominated benchmarks produce systematically false-negative conclusions about whether RL learns new skills, obscuring genuine capability gains on hard problems
- RL training provides little incentive to learn genuinely new skills when trained on tasks where the base model already has high pass@k — in this regime RL behaviour is constrained to reranking existing capabilities
- RL exploration is structurally impeded by entropy collapse — a known failure mode during training where the model's output distribution collapses, reducing the diversity of rollouts needed to discover novel compositional strategies
- The feasibility of acquiring both atomic and compositional skills simultaneously via RL without supervised scaffolding is an open question — all current findings depend on a two-stage pipeline with supervised pre-acquisition of atomic skills

## Bottlenecks

- RL requires explicit compositional training incentives to unlock compositional generalisation — without compositional problems in the training distribution, RL on atomic tasks cannot develop the meta-skill of composition regardless of reward quality
- Existing RL evaluation methodology — mixed-difficulty benchmarks with coarse aggregate pass@k metrics — systematically underestimates RL's genuine skill learning, blocking accurate understanding of what RL contributes and appropriate resource allocation between pretraining and post-training
- Bootstrapping RL-based compositional generalisation requires prior supervised acquisition of domain-specific atomic skills, creating a two-stage pipeline dependency that limits the autonomy and scalability of post-training and blocks end-to-end RL-only skill development

## Breakthroughs

- Controlled causal evidence that RL genuinely teaches LLMs new compositional skills — composing pre-existing atomic capabilities into novel ones that were unsolvable before RL — with cross-domain transfer, directly falsifying the dominant 'reranking-only' hypothesis

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/entropy-collapse|Entropy Collapse]]
- [[entities/rlvr|RLVR]]
- [[entities/passk|pass@k]]
