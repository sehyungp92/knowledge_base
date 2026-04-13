---
type: source
title: Welcome to the Era of Experience
source_id: 01KKT2RD0VB7YHASW6CG1Y7GAX
source_type: article
authors: []
published_at: '2025-04-10 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Welcome to the Era of Experience

Silver and Sutton's 2025 manifesto argues that the era of human data is hitting a structural ceiling — the best human-generated training data has been largely consumed, and supervised imitation cannot produce superhuman intelligence. The paper defines a concrete post-pretraining roadmap: "the era of experience," in which agents learn continually from grounded interaction with the world via reinforcement learning, generating experiential data that dwarfs human data in both scale and quality. It reframes classic RL concepts (value functions, exploration, world models, temporal abstraction) as prematurely abandoned tools now ready for revival.

**Authors:** David Silver, Richard S. Sutton
**Published:** 2025-04-10
**Type:** Article

---

## Core Argument

The paper diagnoses the current moment as a transition between two paradigms. The era of human data produced remarkable generality in LLMs — a single model writing poetry, solving physics problems, diagnosing medical issues, and summarising legal documents — but is approaching a fundamental limit. In mathematics, coding, and science, the extractable knowledge from human corpora is **rapidly approaching saturation**. More importantly, genuinely new insights — new theorems, technologies, scientific breakthroughs — lie beyond the current boundaries of human understanding and therefore *cannot exist* in any human-generated dataset.

The proposed solution is not incremental: agents must learn from their own interaction with the world, generating experience that scales without a human ceiling.

> "valuable new insights, such as new theorems, technologies or scientific breakthroughs, lie beyond the current boundaries of human understanding and cannot be captured in any human data"

The transition is framed as already underway. AlphaProof bootstrapped ~100K human proofs into 100 million RL-generated proofs to achieve IMO medal performance. DeepSeek's RLVR work demonstrated that models given the right incentives — rather than explicit reasoning supervision — autonomously develop advanced problem-solving strategies.

---

## Four Dimensions of the Experiential Break

### 1. Streams Over Episodes

Current LLMs operate in short, stateless interaction episodes with no cross-episode memory or adaptation. Experiential agents maintain **continuous streams** persisting over months or years, enabling long-horizon goal pursuit.

A health agent connected to wearables could track sleep, activity, and diet across many months, adjusting recommendations based on long-term trends. A science agent could pursue multi-year goals like discovering new materials or reducing CO₂, running simulations, proposing experiments, and iterating across an extended timeline. Individual steps may offer no immediate benefit — value accumulates in aggregate toward distant goals.

### 2. Grounded Actions and Observations

LLMs interact primarily through text I/O. Experiential agents interact through rich sensorimotor channels: computer interfaces, robotic embodiment, sensor streams, experimental apparatus. A new wave of prototype agents have already crossed a threshold from text-privileged communication to genuinely general computer use via visual GUI interfaces.

### 3. Grounded Rewards

This is the pivotal dimension. Human-prejudged reward creates an impenetrable ceiling: **agents cannot discover strategies that are better than what human raters can appreciate**. Grounded rewards arise from the environment itself — exam results, health metrics, empirical measurements, formal proof verification — enabling agents to discover strategies humans would not have anticipated or valued.

> "Relying on human prejudgement in this manner usually leads to an impenetrable ceiling on the agent's performance: the agent cannot discover better strategies than those already known and appreciated by the human raters"

The paper proposes a bi-level resolution: a neural reward function grounded in environment signals but steerable by user feedback, allowing grounded autonomy without sacrificing human directability.

### 4. Grounded Reasoning

Human chain-of-thought is one instance of a universal computer, not the optimal one. Experiential agents can discover symbolic, distributed, or differentiable reasoning modes better suited to their tasks. Agents trained to imitate human thoughts may inherit **fallacious methods of thought** — flawed assumptions, biases, outdated frameworks — with no mechanism to correct them without real-world feedback.

---

## Landscape Contributions

### Capabilities Established

| Capability | Maturity | Notes |
|---|---|---|
| LLM generality across diverse tasks | broad_production | Writing, physics, medicine, law from a single model |
| AlphaProof IMO medal performance | narrow_production | RL + formal verification; 100M proofs generated |
| RLVR autonomous strategy development | narrow_production | DeepSeek R1-style; no explicit reasoning supervision |
| LLM chain-of-thought reasoning | broad_production | Token-appending as universal computer |
| GUI-based computer control agents | demo | Visual interface interaction, not just API calls |
| RL execution-feedback tool use | narrow_production | Increasingly built on running code and observing results |
| AlphaZero-style simulation scaling | narrow_production | Potentially unlimited scaling with network size, experience, and thinking time |

See [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/pretraining_and_scaling|Pretraining and Scaling]].

### Limitations Identified

**Blocking — structural ceiling on imitation:**
- Supervised learning on human data cannot produce superhuman intelligence; performance is approaching a ceiling set by the limits of human knowledge itself
- Insights representing genuinely new knowledge cannot be captured or learned from existing human data — this is not a data shortage problem, it is an architectural one
- Human-prejudged rewards impose an impenetrable ceiling on what agents can discover
- Agents without world grounding become an echo chamber of existing human knowledge, unable to validate genuinely new understanding

**Significant — current system architecture:**
- LLMs operate in short episodes with no carryover between sessions — long-term adaptation and goal-pursuit are structurally precluded
- Current systems cannot measure or optimise future consequences of their actions — immediate response orientation only
- RLHF bypassed core RL capabilities (value functions, exploration, world models, temporal abstraction), leaving current systems structurally incapable of deep autonomous learning
- Human language is likely not the optimal reasoning substrate; more efficient mechanisms exist but are unexplored

**Significant — emerging risks:**
- Autonomous experiential agents over long time horizons provide fewer natural intervention points for human oversight — misalignment risk increases
- Moving away from human data and human reasoning will make future AI systems **progressively harder to interpret**
- Value function estimation from long, incomplete experience streams is an unsolved problem, blocking long-horizon credit assignment
- Principled real-world exploration methods that discover behaviours radically different from human priors do not yet exist

---

## Bottlenecks

| Bottleneck | What It Blocks | Horizon |
|---|---|---|
| Exhaustion of high-quality pretraining data | Further capability improvement via data scaling | 1–2 years |
| Human-derived reward ceiling | Superhuman performance and autonomous knowledge discovery | 1–2 years |
| Absence of long-stream RL infrastructure | Lifelong experiential agents with continuous learning | 1–2 years |
| Absence of real-world world models | Grounded long-horizon planning | 3–5 years |
| Undeveloped temporal abstraction methods | Goals spanning months or years in continuous streams | 3–5 years |

The first two bottlenecks are framed as already beginning to resolve — AlphaProof and DeepSeek as evidence. The latter three remain open research problems. See [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]].

---

## Breakthroughs Cited

**AlphaProof IMO medal** *(major)* — First AI system to achieve medal-level performance at the International Mathematical Olympiad. Demonstrates that RL-based experiential learning can surpass human-centric approaches in formal mathematical reasoning, and that 100K human examples can be bootstrapped into 100M RL-generated proofs — illustrating the multiplicative leverage of experiential learning.

**DeepSeek RLVR** *(notable)* — LLMs trained with RL and verifiable rewards autonomously develop advanced problem-solving strategies without explicit human reasoning supervision. Validates the core claim that the right incentive structure, not imitation, is sufficient.

**Visual GUI agents** *(notable)* — A new wave of prototype agents cross from text-privileged to genuinely general computer use via the same visual interfaces humans use — a threshold event in action grounding.

---

## Open Questions and Tensions

**The alignment tension.** Experiential agents pursuing long-horizon goals with fewer intervention points represent a qualitatively different alignment challenge. The paper's proposed resolution — a bi-level neural reward function steerable by user feedback — is described at a high level but remains unimplemented at scale. The claim that adaptive reward functions could self-correct misalignment before catastrophic outcomes is plausible but unverified.

**Interpretability regression.** Moving away from human data and human reasoning modes will make future systems harder to interpret. The paper acknowledges this as a worsening trajectory but offers no concrete mitigation strategy — it is treated as a cost to be managed rather than a problem to be solved.

**Generalisation from simulation.** Simulation-era RL agents failed to generalise from closed simulation environments to open-ended real-world problems. The paper argues the era of experience resolves this by operating directly in grounded reality — but the mechanism by which open-ended real-world rewards avoid the reward misspecification problems that plagued simulation is not fully worked out.

**The single-reward hypothesis.** The claim that "even a single grounded reward signal, optimised with great effectiveness, may be sufficient to induce broadly capable intelligence" is provocative and underspecified. It echoes the reward hypothesis from classical RL theory but its applicability to open-ended real-world domains remains an open empirical question.

**Physical-world pacing as a safety mechanism.** The observation that drug trials and real-world experiments cannot be compressed beyond physical time is presented as a natural brake on runaway self-improvement — but this only applies to capabilities that require physical experiments. Digital domains (mathematics, software, language) face no such constraint.

---

## Connections

- [[themes/agent_self_evolution|Agent Self-Evolution]] — Core thesis: self-improving experience generation as the post-pretraining paradigm
- [[themes/agent_systems|Agent Systems]] — Architectural requirements for continuous-stream lifelong agents
- [[themes/reinforcement_learning|Reinforcement Learning]] — Revival of classical RL concepts (value functions, exploration, world models) sidelined by RLHF era
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — RLVR and AlphaProof as early instantiations of the experiential paradigm
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — Data exhaustion thesis; experiential data as the next scaling axis
- [[themes/scaling_laws|Scaling Laws]] — AlphaZero-style unlimited scaling generalised to open-ended domains

## Key Concepts

- [[entities/alphaproof|AlphaProof]]
- [[entities/chain-of-thought-reasoning|Chain of Thought Reasoning]]
- [[entities/era-of-experience|Era of Experience]]
- [[entities/rlhf|RLHF]]
- [[entities/world-model|World Model]]
