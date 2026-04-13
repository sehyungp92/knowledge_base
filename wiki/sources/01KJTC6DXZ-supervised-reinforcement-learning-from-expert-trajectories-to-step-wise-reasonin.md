---
type: source
title: 'Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning'
source_id: 01KJTC6DXZNAJ02MGPRGRHDWAW
source_type: paper
authors:
- Yihe Deng
- I-Hung Hsu
- Jun Yan
- Zifeng Wang
- Rujun Han
- Gufeng Zhang
- Yanfei Chen
- Wei Wang
- Tomas Pfister
- Chen-Yu Lee
published_at: '2025-10-29 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning

> This paper diagnoses a structural failure at the intersection of SFT and RLVR for small-scale LLMs on hard reasoning problems — SFT overfits, RLVR starves for signal — and proposes SRL (Supervised Reinforcement Learning), a method that decomposes expert trajectories into step-wise training instances and applies a dense sequence-similarity reward to each action. By treating reasoning as sequential decision-making with intermediate supervision, SRL enables 7B models to learn problems previously unlearnable by either paradigm, and generalises from competition-level math to agentic software engineering.

**Authors:** Yihe Deng, I-Hung Hsu, Jun Yan, Zifeng Wang, Rujun Han, Gufeng Zhang, Yanfei Chen, Wei Wang, Tomas Pfister, Chen-Yu Lee
**Published:** 2025-10-29
**Type:** paper
**Source:** https://arxiv.org/pdf/2510.25992

---

## Motivation: The Hard Problem Gap

Small-scale open-source LLMs (7B class) face a training dead-end on challenging multi-step reasoning. The two dominant post-training approaches each fail in a different, structurally distinct way:

**RLVR failure mode** — [[themes/reinforcement_learning|Reinforcement Learning]] with verifiable rewards (e.g., GRPO) collapses on what the paper calls D_hard: problems where the model's pass@k is effectively zero. No successful rollouts means no positive advantage estimates, and the policy gradient carries no information. Worse, naively penalising all incorrect outputs actively destabilises training. The hardest problems — the ones most worth learning from — are structurally excluded from the learning signal.

**SFT failure mode** — [[themes/finetuning_and_distillation|Supervised Fine-Tuning]] on expert demonstrations enforces rigid token-by-token imitation across long, complex traces. On the s1K-1.1 dataset, Qwen2.5-7B SFT achieves only 16.6% average on math benchmarks versus 24.6% for the base model — a concrete, measurable *degradation*. The next-token prediction objective causes the model to overfit surface patterns rather than internalise reasoning strategy.

The hybrid SFT→RLVR pipeline does not resolve this: SFT first degrades the base model's priors before RL attempts repairs, yielding 17.4% vs. 24.5% for RLVR alone. Prior approaches like R3 (reverse curriculum via demonstration decomposition) still rely on outcome rewards, inheriting RLVR's failure on problems where even guided exploration yields zero correct completions.

---

## The SRL Framework

[[themes/post_training_methods|SRL]] reformulates problem-solving as sequential decision-making over discrete *actions* — meaningful intermediate steps extracted from expert trajectories — and trains with a dense reward at each step.

### Core mechanics

A single expert solution with N steps is decomposed into N−1 training instances. Each instance presents a partial solution prefix as context and asks the model to predict the next action. The model first generates a free-form `<think>` monologue, then commits to the action. The reward is applied **only to the action output**, not the reasoning trace.

The reward function uses Python's `difflib.SequenceMatcher`:

```
R = 2M / (|S1| + |S2|) ∈ [0, 1]
```

where M is the number of matching characters. This continuous signal is non-zero whenever the model's action partially resembles the expert action — precisely the property RLVR lacks.

### Design choices and their rationale

| Choice | Rationale |
|--------|-----------|
| Reward on action only, not monologue | Decouples reasoning *style* from action *fidelity* — the model develops its own internal reasoning while staying aligned with expert strategy |
| Continuous similarity reward | Provides gradient signal even on imperfect matches; eliminates the zero-signal failure mode of outcome-based RL |
| Dynamic sampling filter | Discards batches where rollout reward standard deviation falls below threshold ε — analogous to DAPO's filtering, adapted to continuous rewards |
| SRL as curriculum precursor | SRL → RLVR pipeline: first teach step-wise reasoning structure, then optimise for final-answer correctness |

The deliberate choice to leave the `<think>` monologue unsupervised is theoretically significant: it allows emergent reasoning behaviour to develop without being constrained to imitate the teacher's specific thought patterns.

---

## Results

### Competition-level mathematics (Qwen2.5-7B-Instruct, s1K-1.1 dataset)

| Method | AMC23 | AIME24 | AIME25 | Minerva | Avg |
|--------|-------|--------|--------|---------|-----|
| Base model | — | 13.3% | — | — | 24.6% |
| SFT | — | — | — | — | 16.6% |
| SFT → RLVR | — | — | — | — | 17.4% |
| RLVR | — | 10.0% | — | — | 24.5% |
| SRL | — | — | — | — | 27.6% |
| **SRL → RLVR** | — | **20.0%** | — | — | **28.3%** |

SRL alone outperforms RLVR by 3.0 pp and exceeds the best SFT baseline by 11 pp. The SRL→RLVR curriculum is the strongest result among all open-source methods tested.

### Ablation: what drives the gain?

- **Step-wise vs. holistic reward:** applying sequence-similarity reward to the full solution in one step yields 25.9% average; multi-step SRL yields 27.6%. Fine-grained decomposition — not just the reward function — accounts for the gap.
- **Dynamic sampling:** removing it drops average greedy performance from 27.6% to 24.7%, a non-trivial contribution.

### Agentic software engineering (SWE-Bench-Verified)

Qwen2.5-Coder-7B-Instruct trained on 5,000 Claude-3.7-Sonnet expert trajectories (134K step instances after decomposition):

| Method | Oracle resolve rate | End-to-end resolve rate |
|--------|---------------------|------------------------|
| SWE-Gym-7B (SFT baseline) | 8.4% | 4.2% |
| **SRL** | **14.8%** | **8.6%** |

74% relative improvement in oracle, 2× end-to-end — a direct SFT-vs-SRL comparison on the same base model and data.

Data multiplication effect: 5k trajectories → 134k step-wise training instances. Single expert solution with N steps becomes N−1 training examples.

### Scale sensitivity

- 3B models: SRL→RLVR improves average from 16.4% to 19.5% (AMC23, Minerva), but **zero gain on AIME24/AIME25** — model capacity creates a hard floor on the hardest problems.
- Gains are consistent across 7B and 3B for easier benchmarks, confirming the method is not an artefact of model scale at the 7B level.

---

## Emergent Reasoning Behaviours

Models trained with SRL exhibit behaviours not present in SFT models and not explicitly trained for:

- **Structured planning before execution** — the model generates a strategic overview before committing to steps
- **Dynamic mid-solution trajectory adjustment** — the model revises its approach partway through a solution
- **Reflective self-verification** — the model backtracks to check earlier steps

These emerge from the unsupervised `<think>` monologue design. Without constraining the reasoning trace to imitate teacher output, the model develops its own verification loop. Critically, these behaviours appear without simply producing longer outputs — it is qualitatively different reasoning, not just more tokens.

This connects to the broader [[themes/chain_of_thought|chain-of-thought]] research question: whether reasoning quality can be improved structurally rather than just by scale.

---

## Limitations and Open Questions

### Structural limitations

**Expert trajectory dependency.** SRL requires high-quality, decomposable expert trajectories with well-defined action granularity. Domains with ambiguous step boundaries, sparse expert data, or tasks requiring holistic intuition (rather than sequential sub-goals) cannot be directly addressed. The step decomposition pipeline also depends on structured, formatted solutions — data not matching the numbered step format is excluded, creating coverage gaps.

**Teacher ceiling.** Distillation from a teacher model imposes a hard performance ceiling on the student. The student cannot surpass the quality of the teacher's reasoning demonstrations regardless of training method. This is not a bug in SRL — it is a property of any distillation-based approach — but it means SRL cannot bootstrap a model beyond the frontier it is trained to imitate.

**Student proficiency floor.** SRL requires baseline instruction-following capability. Without sufficient initial competence, rollout outputs are incoherent and sequence similarity rewards are uniformly near zero — recreating the same failure mode as RLVR, just shifted to a different threshold.

**Student-teacher gap and teacher hacking.** Students fail to learn from overly complex demonstrations, and risk overfitting to teacher-specific flaws and idiosyncrasies that do not generalise. The paper acknowledges this as an unresolved challenge.

### Evaluation limitations

**SWE-Bench conflation.** The end-to-end software engineering evaluation uses an external Agentless-mini scaffold for fault localisation. The SRL model's true patch generation capability cannot be isolated from the scaffold's file identification quality — the oracle and end-to-end numbers measure different things and the gap between them (14.8% → 8.6%) reflects localisation error, not model reasoning failure.

**Sequence similarity metric variance.** The choice of `difflib.SequenceMatcher` is acknowledged to have uncharacterised performance variance. The impact of alternative similarity metrics on model behaviour is noted but not studied.

### Infrastructure limitations

**Online RL for software engineering is practically infeasible at scale.** Long context windows (100k+), high-latency test execution feedback loops, and slow patch verification prevent stable, scalable end-to-end RL training for software agents. SRL's offline distillation approach is partly motivated by this bottleneck — but it means the software engineering results are bounded by the quality of the offline teacher data, with no path to self-improvement through online interaction.

---

## Connections to Landscape Themes

**Bottleneck addressed:** SRL directly targets the [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] bottleneck that outcome-based RL produces zero learning signal on hard problems where pass@k ≈ 0. By providing dense intermediate rewards, it makes the hardest training examples learnable. This does not eliminate the bottleneck for all settings — model capacity still creates a hard floor at 3B, and the method requires offline expert data — but it is a meaningful resolution path for 7B-class models in domains with available expert trajectories.

**Curriculum learning for [[themes/reasoning_and_planning|reasoning]]:** The SRL→RLVR pipeline is a concrete instantiation of curriculum learning applied to reasoning: teach reasoning *structure* first (SRL), then optimise for reasoning *correctness* (RLVR). This is a design pattern likely to generalise beyond the specific tasks studied here.

**Offline vs. online tradeoff:** The software engineering results highlight a persistent tension. Online RL allows self-improvement through interaction with the environment but is practically blocked by engineering constraints. Offline distillation from expert trajectories is tractable but bounded by teacher quality. SRL occupies a middle position — using offline expert data but applying an RL-style objective that avoids SFT's imitation failure mode. Whether this middle position is stable or whether online RL will eventually become tractable for software agents is an open question.

**Implications for small model capability:** SRL establishes a practical pathway for training small open-source models on hard reasoning problems that were previously unlearnable. The consistent 7B results across math and code suggest the method is not domain-specific, and the domain-agnostic action decomposition framing (tool calls, proof steps, database queries) implies further generalisations are plausible without architectural changes.

---

## Key Claims

1. RLVR fails on hard problems where pass@k ≈ 0 — the policy gradient carries no information and penalising all incorrect outputs degrades performance.
2. SFT on complex expert demonstrations causes performance *degradation* below the base model on competition-level math, due to rigid token-level imitation overfitting.
3. SRL enables 7B models to learn problems previously unlearnable by both SFT and RLVR, via dense step-wise sequence similarity rewards.
4. Step-wise granularity is the key driver — applying the same reward holistically to the full solution yields lower performance than step-level decomposition.
5. SRL→RLVR curriculum yields the strongest results: the curriculum teaches reasoning structure before optimising for final-answer correctness.
6. Emergent interleaved reasoning behaviours (planning, adjustment, verification) arise from the unsupervised monologue design without explicit training.
7. SRL generalises to agentic software engineering, achieving 74% relative improvement over SFT baseline on SWE-Bench-Verified oracle.
8. Distillation imposes a hard teacher-ceiling: the student cannot surpass teacher quality regardless of training method.
9. Model capacity creates a hard floor: 3B models show zero gain on AIME-class problems despite meaningful gains on easier benchmarks.
10. Online RL for software engineering agents is practically blocked by long context windows, slow test execution, and patch verification latency.

---

*Themes: [[themes/chain_of_thought|Chain of Thought]] · [[themes/finetuning_and_distillation|Finetuning & Distillation]] · [[themes/post_training_methods|Post-Training Methods]] · [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/reinforcement_learning|Reinforcement Learning]] · [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]*

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/qwen25-3b-instruct|Qwen2.5-3B-Instruct]]
- [[entities/qwen25-7b-instruct|Qwen2.5-7B-Instruct]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/dynamic-sampling|dynamic sampling]]
- [[entities/passk|pass@k]]
