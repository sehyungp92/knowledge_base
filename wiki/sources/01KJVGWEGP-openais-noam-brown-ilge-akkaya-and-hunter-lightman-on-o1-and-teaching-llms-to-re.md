---
type: source
title: OpenAI's Noam Brown, Ilge Akkaya and Hunter Lightman on o1 and Teaching LLMs
  to Reason Better
source_id: 01KJVGWEGPG3S8AK3KEBP7MQJT
source_type: video
authors:
- Noam Brown
- Ilge Akkaya
- Hunter Lightman
published_at: '2024-10-02 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# OpenAI's Noam Brown, Ilge Akkaya and Hunter Lightman on o1 and Teaching LLMs to Reason Better

This source documents a Sequoia Capital interview with three OpenAI researchers behind o1, establishing the conceptual framework, research history, and empirical findings behind inference-time compute scaling — and making the case that this represents a new, largely untapped axis of AI improvement orthogonal to pre-training.

**Authors:** Noam Brown, Ilge Akkaya, Hunter Lightman
**Published:** 2024-10-02
**Type:** video · Sequoia Capital
**Source:** https://www.youtube.com/watch?v=jPluSXJpdrA

---

## Expert Analysis

### The Central Argument

o1 is not primarily a product announcement — it is a proof that the ceiling on AI capability is far higher than pre-training saturation concerns had suggested. The researchers are explicit: the trend line matters more than the current benchmark numbers. What o1 preview establishes is that allocating more compute at inference time predictably improves output quality along a new scaling law, and this axis is far from exhausted.

The conceptual engine is the **generator-verifier gap**: problems where generating a correct answer is hard but verifying one is easy. Sudoku, mathematical proofs, competitive programming — these are exactly the domains where extended thinking time compounds into large gains. Problems at the opposite end of the spectrum (factual trivia, creative writing, open-ended judgment) either have no verifiable ground truth or offer no benefit from additional deliberation.

### Research History and the Path to Conviction

None of the three researchers held strong prior conviction that this direction would work. Conviction built empirically. One originally joined OpenAI to work on robotics and embodied AI before pivoting after ChatGPT demonstrated a different paradigm. Another spent years building bespoke math systems before seeing o1 outscore them all.

The critical backstory runs through [[themes/agent_systems|AlphaGo]]: a system that thought for ~30 seconds per move via Monte Carlo Tree Search and was noticeably weaker without that time budget. AlphaGo's dependence on a large pre-training step from human data was later underappreciated by the deep RL community — a mistake that caused researchers to over-conclude from AlphaZero's self-play success. When GPT-3 demonstrated massive capability without deep RL, talent flooded away from RL research. o1 is the corrective: **RL becomes genuinely powerful when combined with a strong general pre-trained base** rather than applied from scratch to narrow domains.

### Emergent Backtracking: The Aha Moment

The decisive empirical observation was that RL training caused models to spontaneously develop backtracking — without this behavior being explicitly engineered. When stuck, the model would produce text like *"wait, this is wrong — let me take a step back"* and restart its reasoning path. This emergent behavior shifted researcher conviction.

The [[themes/chain_of_thought|chain of thought]] produced is human-interpretable: researchers can read, inspect, and debug how the model reasons through problems. This is structurally different from opaque intermediate activations. When solving geometry problems, o1 produces verbal visualization strategies ("let's put the points at...") that mirror how a human would contextualize spatial information.

### What o1 Can and Cannot Do

**Demonstrated capabilities:**

- Backtracking and self-correction during reasoning — recognizing dead ends and restarting
- Passes OpenAI's research engineer interview at high pass rates
- Outperforms PhD students on GPQA (science question answering)
- Solving mathematical proofs previously demonstrated only by humans
- Authoring pull requests in production repositories
- Serving as scientific brainstorming partner — cancer biology and gene therapy researchers use it to surface novel research directions (an unanticipated use case the team found meaningful)
- At the IOI programming competition, solved a problem via an unusual method that puzzled competitive programmers — not a stroke of genius, but evidence the model navigates solution space differently than humans

**Structural limitations:**

- Performance lift is concentrated in STEM and reasoning-heavy tasks; minimal or no advantage on non-reasoning tasks
- Scores below 40 on creative writing benchmarks
- Better than humans at math, but not yet as effective at the full software engineering job
- Cannot leverage longer reasoning time on tasks where solution quality is hard to define or verify — the RL training paradigm structurally requires verifiable ground truth
- No proven transfer to humanities, philosophy, or domains requiring subjective judgment
- Unknown scaling ceiling — o1 hasn't existed long enough to test extended thinking times; it's unclear whether longer reasoning eventually solves arbitrary hard problems or hits fundamental limits

The benchmark gap is important to hold carefully: o1 outperforms PhD students on GPQA, but is not smarter than a PhD in every dimension. Benchmark scores are proxies calibrated for humans and mean something different when AI takes them.

---

## Landscape Contributions

### Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| Learned backtracking and self-correction | narrow_production | Emergent from RL training, not explicitly engineered |
| Coding assistance (PRs, multi-step reasoning) | narrow_production | Authoring PRs in production repos |
| Research engineer-level technical problem solving | narrow_production | High pass rates on internal interview |
| Novel mathematical proof solving | narrow_production | Problems previously solved by humans only |
| Inference-time scaling law | demo | Performance improves predictably with thinking time |
| Human-interpretable reasoning chains | narrow_production | Inspectable, debuggable chain of thought |

### Limitations

- **Reasoning requires verifiable structure** (severity: blocking) — the RL training paradigm cannot be applied to tasks without ground-truth verification. This is not a calibration issue but a structural constraint on what the approach can address.
- **STEM specificity** (severity: significant) — the performance gap vs. prior models is concentrated in domains with large generator-verifier gaps. Whether improvements propagate to humanities and open-ended domains is explicitly held as an open question.
- **Engineering scaling burden** (severity: significant, trajectory: improving) — the conceptual idea is simple; the implementation challenges in scaling to production are substantial.
- **Inference cost and latency** (severity: significant, trajectory: improving) — longer thinking improves accuracy but creates tension with real-time and cost-sensitive deployments.
- **Evaluation gap outside STEM** (severity: significant) — benchmarks for assessing reasoning in non-verifiable domains don't yet exist in standardized form.
- **Unknown scaling ceiling** (severity: significant, trajectory: unclear) — no empirical data yet on long-horizon thinking limits.

### Bottlenecks

- **[[themes/test_time_compute_scaling|Inference-time compute]] cost/latency tradeoff** — blocking practical deployment in real-time systems; horizon: 1–2 years
- **Engineering infrastructure for scaled reasoning** — systems-level work required before the approach can be pushed further; horizon: months
- **Benchmarks for non-STEM reasoning** — cannot plan interventions in humanities/creative domains without evals; horizon: 1–2 years
- **Extending RL-based reasoning to non-verifiable domains** — structural challenge; current training requires ground truth; horizon: 3–5 years

### Breakthroughs

- **Inference-time compute scaling laws** (significance: paradigm_shifting) — a new, orthogonal axis of improvement established alongside pre-training scaling laws
- **General-purpose reasoning via RL on language models** (significance: major) — unified RL training produces reasoning across diverse domains rather than narrow task-specific systems

---

## Key Claims

1. o1 is trained with reinforcement learning to develop reasoning — the model learns to think, not just recall.
2. Reasoning capability is a property of problem types, not a binary model attribute — specifically, problems where longer thinking yields better answers (System 2 analogy).
3. The generator-verifier gap is the structural engine: hard-to-generate, easy-to-verify problems are where extended inference compute pays off most.
4. AlphaGo's dependence on pre-training from human data was underappreciated — a historical error the deep RL community overcorrected from.
5. RL produces emergent backtracking without explicit engineering — the key empirical observation that shifted researcher conviction.
6. Inference-time scaling follows a law analogous to pre-training scaling — performance improves predictably with thinking time.
7. Engineering, not research, is the primary bottleneck — scaling novel algorithms to production is predominantly an infrastructure challenge.
8. o1's chain of thought is hidden for competitive reasons, not safety ones — the same logic as not releasing model weights.
9. The path to AGI runs through reasoning — navigating obstacles is the core of economically valuable work.

---

## Open Questions

- Will reasoning improvements transfer to humanities and open-ended creative tasks, or is the generator-verifier framework a hard ceiling for those domains?
- What is the scaling ceiling for inference-time compute — does longer thinking eventually solve arbitrary hard problems, or does it hit fundamental limits?
- Can the RL + verifiable reward mechanism be extended to tasks without clear ground truth?
- Does [[themes/reasoning_and_planning|reasoning]] capability developed in STEM domains generalize structurally, or does each domain require domain-specific scaffolding?

---

## Related

- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/agent_systems|Agent Systems]]
- [[themes/software_engineering_agents|Software Engineering Agents]]

## Key Concepts

- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/gpqa|GPQA]]
- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
- [[entities/pre-training-scaling-laws|Pre-training Scaling Laws]]
- [[entities/reinforcement-learning-for-reasoning|Reinforcement Learning for Reasoning]]
- [[entities/system-1-system-2-thinking|System 1 / System 2 Thinking]]
- [[entities/generator-verifier-gap|generator-verifier gap]]
- [[entities/o1|o1]]
