---
type: source
title: 'Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to
  Deliberation'
source_id: 01KJTB00NQ3EFGQ5Q960ZK7RE1
source_type: paper
authors:
- Zhiwei Zhang
- Xiaomin Li
- Yudi Lin
- Hui Liu
- Ramraj Chandradevan
- Linlin Wu
- Minhua Lin
- Fali Wang
- Xianfeng Tang
- Qi He
- Suhang Wang
published_at: '2025-11-04 00:00:00'
theme_ids:
- agent_systems
- mathematical_and_formal_reasoning
- multi_agent_coordination
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation

**Authors:** Zhiwei Zhang, Xiaomin Li, Yudi Lin, Hui Liu, Ramraj Chandradevan, Linlin Wu, Minhua Lin, Fali Wang, Xianfeng Tang, Qi He, Suhang Wang
**Published:** 2025-11-04 00:00:00
**Type:** paper

## Analysis

# Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation
2025-11-04 · paper · Zhiwei Zhang, Xiaomin Li, Yudi Lin, Hui Liu, Ramraj Chandradevan et al. (11 total)
https://arxiv.org/pdf/2511.02303

---

### Motivation & Prior Limitations
Multi-agent LLM reasoning frameworks trained with reinforcement learning suffer from a critical "lazy agent" problem in which one agent dominates while the other contributes only trivially, effectively collapsing the multi-agent system into a single agent and negating the theoretical benefits of collaboration.
- The ReMA framework (Wan et al., 2025), which pairs a meta-thinking agent (task decomposition, goal-setting) with a reasoning agent (step-by-step execution) via multi-turn GRPO, exhibits clear lazy agent behavior: the reasoning agent often outputs blanks or simply copies the meta-thinking agent's responses, leaving the meta-thinking agent to carry nearly the entire reasoning burden.
  - Causal influence measurements show that the reasoning agent's influence diminishes markedly as ReMA training progresses, and performance actually drops from 75.0 to 74.4 on MATH500 relative to an untrained baseline despite training.
- The root cause is a structural bias in the multi-turn GRPO objective: the 1/T normalization term, designed to prevent bias toward longer rollouts, instead implicitly incentivizes agents to complete reasoning in fewer turns. Theorem 1 in the paper proves that unless the aggregated contribution of a longer trajectory is at least T_L/T_S times larger than a shorter one's, gradient updates favor the shorter trajectory — and lazy behaviors (empty outputs, summarization) naturally produce shorter trajectories, receiving preferential reinforcement.
- Prompt engineering to discourage trivial responses partially closes the causal-influence gap (improving MATH500 from 74.4 to 75.6) but does not resolve the underlying optimization bias, and the gains reflect shortcut exploitation rather than genuine collaborative reasoning.
- A secondary limitation surfaces as lazy behavior is reduced: longer multi-turn interactions cause the reasoning agent to "get lost" in dialogue, overcommitting to noisy or incomplete early context, a pattern documented by Laban et al. (2025) in general multi-turn LLM settings and confirmed empirically here.

---

### Proposed Approach
The paper introduces Dr. MAMR (Multi-Agent Meta-Reasoning Done Right), a three-component framework that addresses lazy agents through objective correction, causal credit assignment, and a deliberation mechanism for multi-turn recovery.

- **Objective correction**: The 1/T_i turn-count normalization is removed from the multi-turn GRPO loss, directly eliminating the structural bias toward shorter trajectories identified in Theorem 1. This alone alleviates but does not fully resolve lazy behavior, motivating the additional components.

- **Shapley-inspired causal influence (CI)**: Each trajectory is flattened into a sequence of meta-thinking and reasoning steps, and each step's causal influence is measured by computing the KL divergence between the model's next-step distribution with and without that step's tokens (via attention suppression). To address the instability of single-trajectory estimates — which are vulnerable to phrasing bias and limited coverage of possible continuations — steps are grouped by semantic similarity across rollouts, and influence scores are averaged within each group, analogous to Shapley value averaging over coalitions. This avoids the prohibitive cost of explicit resampling during online RL while producing stable, phrasing-robust contribution estimates.
  - The Shapley analogy is explicit: just as Shapley values average marginal contributions across all coalitions, this method averages influence across semantically similar steps across rollouts, approximating the expected causal contribution of an idea rather than a specific phrasing.

- **Verifiable reward for restart**: A special control token `<restart>` is introduced, instructing the reasoning agent to mask all prior reasoning outputs, consolidate meta-thinking instructions, and begin a fresh attempt. Whether a restart was beneficial is verified post-hoc: if masking prior reasoning outputs increases the model's log-probability of the correct final answer (Δℓ > 0) and the answer is correct (z = +1), or decreases it when the answer is wrong (z = −1), the restart receives reward +1; misaligned cases receive −1. This provides a verifiable, outcome-grounded training signal without requiring a learned critic.
  - The verifiable restart reward is combined with the outcome-based advantage and the normalized causal influence signal into an aggregated step-level advantage (Eq. 8), with tunable weights α and β.

---

### Results & Capabilities
Dr. MAMR substantially improves over ReMA and single-agent GRPO baselines across a diverse suite of mathematical reasoning benchmarks at 3B, 7B, and 14B scales on the Qwen2.5 family.
- On MATH500, Dr. MAMR achieves 78.4 Pass@1 compared to 74.4 for ReMA and 75.0 for the untrained baseline, a gain of 4 points over the trained multi-agent baseline.
- Enabling restart via prompt engineering alone at inference time (ReMA+) yields gains of approximately 8% on AMC23 and OlympiadBench under Pass@1, and approximately 7% on AIME24 and AIME25 under Pass@16, relative to standard ReMA — validating the deliberation hypothesis before full training.
  - ReMA+ outperforms ReMA on 6 of 8 benchmarks even under Pass@16 (which gives both methods many attempts), demonstrating that restart capacity addresses a systematic rather than incidental failure mode.
- Performance gaps between Dr. MAMR and baselines widen as benchmark difficulty and average number of turns increase, confirming that the gains are specifically attributable to more effective multi-turn collaboration rather than improved single-step reasoning.
- Causal influence distributions under Dr. MAMR (Fig. 2d) show sub

## Key Claims

1. In the ReMA framework, reasoning agents often contribute only trivially by summarizing or copying the meta-thinking agent's responses without genuine questioning or reflection, leaving the meta-thinki
2. The reasoning agent's causal influence diminishes markedly as ReMA training progresses, even though both agents initially contribute substantially when initialized from the base model.
3. Standard ReMA training causes a performance drop from 75.0 to 74.4 on MATH500 despite training, coinciding with the emergence of lazy agent imbalance.
4. Prompt engineering to discourage trivial responses in ReMA can partially mitigate the lazy agent issue (improving MATH500 from 74.4 to 75.6) but does not fully resolve it and still leaves the reasonin
5. The 1/Ti normalization term in multi-turn GRPO introduces a structural bias that causes the model to favor actions leading to fewer turns, which is the root cause of lazy agent behavior.
6. Theorem 1 formally proves that unless the aggregated gradient contribution of a longer trajectory is at least TL/TS times larger than a shorter one, the gradient update will favor the trajectory with 
7. Reasoning processes with lazy-agent behavior (e.g., producing empty outputs or simply summarizing) consistently involve fewer turns than those without lazy agents at initial training stages, which are
8. The turn-level bias from the 1/Ti normalization is substantially more pronounced than the token-level normalization bias analyzed in Dr.GRPO, because the number of turns T is far smaller than the numb
9. Longer multi-turn interactions can degrade LLM performance because LLMs overcommit to underspecified early context and struggle to recover from initial errors.
10. Allowing the reasoning agent to adaptively discard prior outputs via a system prompt (ReMA+) consistently matches or outperforms standard ReMA at inference time, with gains of about 8% on AMC23 and Ol

## Capabilities

- Multi-agent LLM reasoning framework with specialized meta-thinking and reasoning agent roles can solve complex mathematical reasoning through sequential turn-alternating collaboration, with meta-thinking agent decomposing tasks and reasoning agent executing step-by-step computation
- Dr. MAMR framework mitigates lazy agent collapse in sequential multi-agent LLM reasoning through Shapley-inspired causal influence measurement and verifiable restart rewards, achieving 78.4 on MATH500 versus 74.4 for baseline ReMA
- Shapley-inspired causal influence estimation groups semantically similar steps across rollouts and averages their one-step masked-attention divergences, producing robust per-step contribution scores during online RL without computationally prohibitive resampling
- Verifiable restart reward mechanism assigns credit to deliberation actions in multi-turn reasoning by measuring whether discarding prior history (via a <restart> control token) increases the model's probability of generating the correct final answer
- Multi-turn GRPO with turn-level importance ratios enables end-to-end reinforcement learning of multi-turn multi-agent LLM systems, providing finer-grained credit assignment than trajectory-level advantage methods

## Limitations

- In sequential multi-agent LLM reasoning, one agent consistently dominates while the other contributes trivially — reasoning agents frequently output blanks or merely copy the meta-thinking agent's response, collapsing the effective system to single-agent behavior
- Multi-turn GRPO normalization term (1/T_i) introduces a structural training bias: models systematically favor actions that reduce turn count even when longer trajectories achieve equal final reward, making the objective incompatible with genuine multi-turn collaboration
- Multi-agent RL training with naive ReMA actually degrades performance below the untrained base model on MATH500 (74.4 vs 75.0), demonstrating that multi-agent RL training can regress baseline performance when lazy agent dynamics take hold
- LLMs in multi-turn settings overcommit to incomplete early context — once a reasoning agent anchors on an early erroneous assumption, consistent performance drops occur in multi-turn vs single-turn conditions
- Online RL causal influence estimation is fundamentally limited to a single trajectory per step, making reliable Shapley-style attribution across diverse continuations computationally prohibitive without approximation
- Prompt engineering only partially mitigates lazy agent behavior — it narrows but does not close the causal contribution gap between agents, yielding only 0.6 MATH500 points vs the 4-point gain from structured training
- The Dr. MAMR approach and lazy agent analysis are evaluated exclusively on mathematical reasoning — the verifiable reward and causal influence mechanisms have no demonstrated generalizability to open-ended or non-verifiable domains
- Performance degradation in multi-agent interaction worsens with benchmark difficulty and turn count — the hardest benchmarks show the largest performance gaps, suggesting multi-agent reliability degrades superlinearly with task complexity
- Both meta-thinking and reasoning agents share the same model weights differentiated only by system prompts — this architectural coupling may cap the degree of genuine cognitive specialization achievable between roles
- Deliberation-via-restart behavior is latent but not reliably activated without explicit prompting or training — LLMs possess this capacity but require intervention to engage it consistently across benchmarks

## Bottlenecks

- Turn-count normalization in multi-turn GRPO structurally biases training toward fewer-turn trajectories, causing sequential multi-agent LLM systems to collapse into single-agent behavior and blocking effective collaborative reasoning training
- Error propagation in extended multi-turn multi-agent interactions — standard RL training provides no mechanism for a reasoning agent to escape commitment to early noisy context, capping the benefit of deeper inter-agent collaboration on hard tasks

## Breakthroughs

- First theoretical proof that multi-turn GRPO's turn-count normalization term (1/T) is the structural cause of lazy agent behavior — showing that equal-reward trajectories receive gradient updates biased toward fewer turns, explaining why multi-agent LLM reasoning collapses to single-agent behavior d

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/grpo|GRPO]]
- [[entities/large-reasoning-models|Large Reasoning Models]]
- [[entities/math500|MATH500]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/passk|pass@k]]
