---
type: source
title: 'Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains'
source_id: 01KJTN3N0MX4CM4A1ME57J3ME0
source_type: paper
authors:
- Anisha Gunjal
- Anthony Wang
- Elaine Lau
- Vaskar Nath
- Yunzhong He
- Bing Liu
- Sean Hendryx
published_at: '2025-07-23 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- medical_and_biology_ai
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains

**Authors:** Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Yunzhong He, Bing Liu, Sean Hendryx
**Published:** 2025-07-23 00:00:00
**Type:** paper

## Analysis

# Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains
2025-07-23 00:00:00 · paper · Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Yunzhong He et al. (7 total)
https://arxiv.org/pdf/2507.17746

---

### Motivation & Prior Limitations
Reinforcement Learning with Verifiable Rewards (RLVR) has proven effective in domains like math and code — where correctness is binary and automatable — but fails to extend to real-world reasoning tasks that require nuanced, multi-criteria judgment rather than a single ground-truth answer.
- Preference-based reward models, the common fallback for unverifiable tasks, are known to overfit superficial artifacts such as response length, formatting quirks, and annotator biases, and require large volumes of pairwise comparison data to function reliably.
- Instance-specific rubrics had recently emerged as an evaluation tool in expert domains (e.g., HealthBench), but their potential as on-policy training signals — rather than just evaluation instruments — remained largely unexplored prior to this work.
- Generative reward models that produce interpretable scores exist in prior literature, but a general-purpose method for specifying reliable reward signals in tasks without a single ground truth — combining both subjective and objective criteria — had not been established.

---

### Proposed Approach
The paper introduces Rubrics as Rewards (RaR), an on-policy reinforcement learning framework that uses instance-specific, structured rubrics as the core reward mechanism, positioning them as a middle ground between binary verifiable rewards and coarse preference rankings.
- Rather than applying rubrics only at evaluation time, RaR treats them as checklist-style supervision: each rubric decomposes "what makes a good response" into modular, human-interpretable subgoals that generate automatable feedback signals aligned with expert intent.
- Rubrics are generated with input from both LLMs and human experts, and are evaluated for properties including expert grounding, coverage, self-containedness, and importance — ensuring they capture meaningful, domain-relevant criteria rather than surface-level proxies.
- The framework evaluates multiple strategies for aggregating rubric-level feedback into scalar rewards, enabling systematic comparison of aggregation choices in both medical (HealthBench) and science (GPQA-Diamond) domains.

---

### Results & Capabilities
The best RaR variant achieves a relative improvement of up to 31% on HealthBench and 7% on GPQA-Diamond compared to popular LLM-as-judge baselines that rely on direct Likert-scale rewards.
- RaR-trained policies generalize well across evaluation formats, performing strongly on both rubric-based assessments and multiple-choice tasks — suggesting the learned policy does not overfit to the specific reward signal structure used during training.
- Using rubrics as structured reward signals yields better alignment for smaller judge models and reduces performance variance across judge scales, indicating that RaR is more robust to judge capacity than Likert-based alternatives.

---

### Implications
RaR extends the applicability of RLVR-style post-training to expert domains — such as medicine and scientific reasoning — where correctness cannot be automatically verified, potentially unlocking on-policy RL for a much broader class of real-world tasks.
- The framing of rubrics as reusable, instance-specific reward functions suggests a path toward scalable reward specification that is interpretable by humans and auditable, which is directly relevant to safety and alignment research seeking reward models that don't obscure their decision criteria.
- The finding that rubric-based rewards reduce judge-scale variance is significant for RLHF research: it implies structured decomposition of reward signals can partially compensate for weaker judge models, reducing dependence on frontier-scale evaluators during training.
- For medical AI specifically, the HealthBench results suggest that rubric-grounded RL could be a viable path toward models that internalize expert clinical reasoning criteria rather than optimizing for superficial stylistic preferences.

---

### Remaining Limitations & Next Steps
The paper evaluates RaR in only two domains (medical and science), and the generalizability of rubric-based rewards to other expert domains — such as law, education, or policy analysis — is not demonstrated.
- The rubric generation process involves both LLM and human expert input, which introduces a construction bottleneck: the quality of the reward signal is upstream-dependent on rubric quality, and the cost and scalability of expert-grounded rubric creation at scale is not addressed.
- The paper compares RaR against LLM-as-judge baselines using Likert scoring, but does not benchmark against other structured reward approaches (e.g., process reward models or constitutional AI variants), leaving the full landscape of alternatives uncharted.
- The source text excerpt does not include detailed discussion of failure modes, edge cases where rubric decomposition breaks down, or how the method handles rubrics that are ambiguous, contradictory, or poorly calibrated — these represent implicit open questions.

## Key Claims

1. RLVR is effective for complex reasoning tasks with clear correctness signals such as math and coding, but extending it to real-world reasoning tasks is challenging due to nuanced, multi-criteria judgm
2. RaR achieves relative improvements of up to 31% on HealthBench over popular LLM-as-judge baselines that rely on direct Likert-based rewards.
3. RaR achieves relative improvements of up to 7% on GPQA-Diamond over LLM-as-judge baselines using Likert-based rewards.
4. RaR-trained policies adapt well to diverse evaluation formats, performing strongly on both rubric-based and multiple-choice tasks.
5. Using rubrics as structured reward signals yields better alignment for smaller judges compared to Likert-based reward approaches.
6. Rubric-based reward signals reduce performance variance across judge scales compared to coarser reward methods.
7. Preference-based reward models tend to overfit superficial artifacts such as response length, formatting quirks, and annotator biases.
8. Preference-based reward models require large volumes of pairwise comparisons, adding operational overhead.
9. RLVR in math and coding domains succeeds because reward models can be replaced by scoring functions or test cases that automatically verify correctness.
10. A general-purpose approach for specifying reliable reward signals in tasks without a single ground truth remains elusive.

## Capabilities

- On-policy RL training (RaR) extends RLVR to unstructured medical and science domains using rubric-based reward signals, achieving up to 31% relative improvement on HealthBench and 7% on GPQA-Diamond over LLM-as-judge baselines
- Rubric-based structured reward signals improve alignment consistency for smaller LLM judges and reduce performance variance across judge model scales compared to coarse Likert-based rewards
- RaR-trained policies generalise across evaluation format types, performing strongly on both rubric-based and multiple-choice tasks without format-specific specialisation

## Limitations

- RLVR is structurally restricted to tasks with clear verifiable correctness signals (math, code) and cannot directly extend to unstructured real-world reasoning without significant modifications to the reward mechanism
- Preference-based reward models overfit superficial artifacts — response length, formatting quirks, annotator biases — corrupting the reward signal and causing reward hacking
- Preference-based RLHF requires large volumes of pairwise comparison data, creating prohibitive data collection overhead when extending RL to new expert domains
- No general-purpose approach for specifying reliable reward signals exists for tasks without a single ground truth, where both subjective and objective criteria must be jointly satisfied
- RaR's rubric generation pipeline requires joint LLM and human expert input, meaning it is not fully automated — human expert involvement creates a scalability bottleneck when extending to new domains
- Performance gains from RaR are asymmetric across domains (31% on HealthBench vs only 7% on GPQA-Diamond), suggesting rubric-based rewards have uneven effectiveness and may not generalise uniformly across expert fields
- RaR is validated exclusively on benchmark evaluations; real-world deployment validity, safety properties, and clinical generalisability are entirely absent from the analysis

## Bottlenecks

- Absence of structured, automatable reward signals for expert domains (medical, scientific) is the core bottleneck preventing RL post-training from extending beyond STEM to unstructured real-world reasoning tasks

## Breakthroughs

- Rubrics as Rewards (RaR) provides a practical on-policy RL training framework for expert domains lacking verifiable ground truth, using instance-specific rubric checklists as structured, automatable reward signals in place of binary correctness checks or preference rankings

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/alignment_methods|alignment_methods]]
- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]

## Key Concepts

- [[entities/generative-reward-model|Generative Reward Model]]
- [[entities/healthbench|HealthBench]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
