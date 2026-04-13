---
type: source
title: 'Thinking LLMs: General Instruction Following with Thought Generation'
source_id: 01KJV7N48DXDR5PVV35ZAP2N82
source_type: paper
authors:
- Tianhao Wu
- Janice Lan
- Weizhe Yuan
- Jiantao Jiao
- Jason Weston
- Sainbayar Sukhbaatar
published_at: '2024-10-14 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinking LLMs: General Instruction Following with Thought Generation

This paper introduces Thought Preference Optimization (TPO), an iterative RLAIF method that trains LLMs to generate internal natural-language thoughts before responding — without any human-annotated reasoning data. By evaluating only the response (not the thought) with a standard judge model, TPO implicitly teaches the model which thought styles produce better outputs. The result is a general-purpose thinking capability that improves performance across diverse instruction categories, not just math and logic, while exposing fundamental open problems around thought evaluation, compute controllability, and catastrophic forgetting.

**Authors:** Tianhao Wu, Janice Lan, Weizhe Yuan, Jiantao Jiao, Jason Weston, Sainbayar Sukhbaatar
**Published:** 2024-10-14
**Type:** paper
**Source:** https://arxiv.org/pdf/2410.10630

---

## Motivation

Standard instruction-tuned LLMs allocate fixed compute per token regardless of task complexity, with no mechanism for explicit pre-response planning. [[themes/chain_of_thought|Chain-of-Thought]] prompting exists, but a meta-analysis by Sprague et al. (2024) found it unhelpful on tasks outside math and logic — leaving a gap for general instruction following. Prior "training to think" methods (STaR, Quiet-STaR, IRPO, Self-Notes) were all narrowly scoped to math or coding with access to ground-truth answers.

The core obstacle: no supervised data exists for thought processes. Post-training datasets contain responses or preferences over responses, but no information about internal reasoning. Collecting human thought traces is costly and of uncertain utility; existing reward models cannot evaluate thought quality at all.

---

## Method: Thought Preference Optimization

TPO is an iterative preference optimization loop:

1. **Prompt the model** to produce two-part outputs: a hidden `<thought>` section and a visible response, using either a *generic* open-ended thought prompt or a *specific* prompt requiring a draft response followed by self-evaluation.
2. **Sample K=8 outputs** per instruction at temperature 0.8.
3. **Evaluate responses only** with a judge model (ArmoRM 8B or STE 70B LLM-as-a-judge) — the judge never sees the thought. The best and worst response outputs form chosen/rejected pairs for [[themes/policy_optimization|DPO]] training.
4. **Include both thought and response** in the preference pairs, so the model implicitly learns which thought styles led to better responses without direct thought supervision.
5. **Apply length control** by subtracting a normalized length score (scaled by ρ) from the reward, counteracting the judge's systematic bias toward longer outputs.
6. **Iterate** for up to 4 rounds, generating 5,000 fresh instructions per iteration and discarding prior-iteration data.

This sidesteps the need for any judge capable of evaluating thought quality directly — a capability that does not currently exist.

---

## Results

| Benchmark | Direct Baseline | TPO |
|---|---|---|
| AlpacaEval 2 (LC win rate) | ~48.4% | **52.5%** (+4.1%) |
| Arena-Hard | ~33.0% | **37.3%** (+4.3%) |

At 8B parameters, TPO places 3rd on the AlpacaEval leaderboard (as of Sep. 2024, behind GPT-4 Omni and GPT-4 Turbo) and achieves Arena-Hard scores comparable to GPT-4 (06/13, 37.9%) and Mistral Large (37.7%).

**Thinking helps beyond reasoning tasks.** Fine-grained evaluation across 20 categories on 200 held-out UltraFeedback instructions shows gains in language and translation, marketing, health and wellness, and general knowledge — directly contradicting the Sprague et al. finding that CoT is only useful for math and logic.

**Thought compression emerges without supervision.** Thought length shrinks by 61% (generic prompt) and 30% (specific prompt) across 4 training iterations, suggesting the model self-organizes toward more efficient internal reasoning rather than verbose scratchpads.

**Prompting alone is harmful.** Before TPO training, adding a thought prompt *degrades* AlpacaEval win rate from 24.9% to 17.3%. The benefit comes entirely from optimization, not from prompting.

---

## Capabilities

- **General thinking via response-only reward signal** — iterative RLAIF on thought-response preference pairs trains latent reasoning behavior without annotated thought traces or specialized thought-evaluating judges. [[themes/reinforcement_learning|Reinforcement learning]] from response quality alone is sufficient to bootstrap a qualitatively new capability. *(maturity: research_only)*

- **Non-reasoning gains from thinking** — improvements extend to language translation, marketing, health, and general knowledge, broadening the viable design space for [[themes/post_training_methods|post-training methods]] beyond math and coding. *(maturity: demo)*

- **Competitive small-model performance** — an 8B Thinking LLM via TPO matches the Arena-Hard performance of much larger proprietary models, suggesting thinking partially offsets scale disadvantages. *(maturity: demo)*

- **Spontaneous thought efficiency** — thought length decreases across iterations without direct supervision, consistent with models learning to internalize and compress reasoning strategies. *(maturity: research_only)*

---

## Limitations & Open Problems

**No judge for thought quality.** The absence of a model capable of directly evaluating internal thoughts is the foundational constraint. Thought quality is assessed only through its downstream effect on responses, limiting training signal precision and making it impossible to steer the model toward specific reasoning strategies.

> *"There is a lack of a judge model that is capable of evaluating internal thoughts. Building such a judge is inherently challenging because it is hard to define what makes a thought good."*

**Catastrophic forgetting of math.** TPO training on diverse general instructions causes GSM8K accuracy to drop from 79.2% (seed model) to below 51.3%. No effective multi-objective strategy exists for adding general thinking while preserving domain-specific capabilities — a concrete blocker for unified thinking models.

**Uncontrolled compute per query.** Thought lengths are entirely self-determined. There is no mechanism to allocate thinking depth proportionally to task complexity, making per-query cost unpredictable and blocking cost-efficient deployment of thinking LLMs at scale.

**Scale unknown.** All experiments use 8B parameter models. Whether thinking benefits grow, shrink, or interact differently with model scale is entirely unvalidated.

**Architecture constraint on continuous thinking.** The Transformer architecture's hidden states do not feed back as inputs to future tokens, making natural language the only viable medium for explicit intermediate computation at inference time. Continuous vector-space thinking is structurally inaccessible without architectural changes.

**Fixed thought prompt type.** Training on a single thought prompt locks in suboptimal thinking patterns — different tasks likely benefit from different thought structures, but the model cannot dynamically select between thinking strategies at inference time.

**Judge length bias requires active mitigation.** Without length control, judge models' preference for longer responses causes response length to grow ~15% per training iteration, requiring a length-control mechanism that adds a hyperparameter and potential noise to the training signal.

---

## Bottlenecks Addressed & Created

| Bottleneck | Status | Horizon |
|---|---|---|
| Direct supervision of LLM thought processes | Partially sidestepped by response-only reward; fundamental gap remains | 1–2 years |
| Catastrophic forgetting when adding thinking to general models | Identified but unsolved | months |
| Adaptive test-time compute allocation for thinking LLMs | Identified but unsolved | months |

---

## Connections

- **[[themes/chain_of_thought|Chain-of-Thought]]** — TPO extends CoT-style thinking beyond math/logic, challenging the domain specificity assumption from Sprague et al. (2024).
- **[[themes/policy_optimization|Policy Optimization]]** — DPO is used as the core preference optimization algorithm; IRPO (adding NLL loss on chosen samples) produces negligible differences in this setting.
- **[[themes/finetuning_and_distillation|Finetuning & Distillation]]** — iterative self-improvement loop without distillation from a stronger model; improvement comes from preference signal within the model's own generation distribution.
- **[[themes/reasoning_and_planning|Reasoning & Planning]]** — qualitative analysis shows the specific thought prompt elicits interpretable draft-then-evaluate behavior; generic prompt enables structural planning for creative tasks without those steps appearing in output.
- **[[themes/post_training_methods|Post-Training Methods]]** — TPO is a post-training procedure applied to an existing instruction-tuned LLM, requiring no changes to pretraining or architecture.
- **[[themes/reinforcement_learning|Reinforcement Learning]]** — the iterative RLAIF loop is the core training mechanism; the paper is directly adjacent to ongoing work on RL-based reasoning (DeepSeek-R1, o1).

---

## Key Claims

1. Standard alignment frameworks produce LLMs that lack the ability to think explicitly before answering.
2. CoT prompting alone (without training) actively *hurts* general instruction following — thought prompts degrade AlpacaEval win rate from 24.9% to 17.3% before TPO training.
3. TPO achieves 52.5% LC win rate on AlpacaEval and 37.3% on Arena-Hard with an 8B model, outperforming direct-response baselines by +4.1% and +4.3%.
4. Response-quality reward alone is sufficient to train implicit thought quality — no thought-evaluating judge is required.
5. Thought compression (61%/30% reduction) emerges across training iterations without direct supervision.
6. Length control is mandatory: without it, judge length bias inflates response verbosity uncontrollably across iterations.
7. TPO causes catastrophic forgetting on GSM8K (79.2% → <51.3%), confirming that general instruction-following training conflicts with math-specific capability.
8. Natural language is the only viable medium for intermediate computation in standard Transformers — continuous vector thinking is architecturally blocked.
9. Thinking benefits extend to non-reasoning categories including language translation, marketing, health, and general knowledge.
10. Preference pairs must include both thought and response parts for the model to implicitly learn which thought styles produce better outcomes.

## Key Concepts

- [[entities/alpacaeval|AlpacaEval]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/gsm8k|GSM8K]]
- [[entities/quiet-star|Quiet-STaR]]
- [[entities/star|STaR]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/ultrafeedback|UltraFeedback]]
