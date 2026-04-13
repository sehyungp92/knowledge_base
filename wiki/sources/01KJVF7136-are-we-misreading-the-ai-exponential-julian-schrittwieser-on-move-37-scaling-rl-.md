---
type: source
title: Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling
  RL (Anthropic)
source_id: 01KJVF7136PS8KW9RF0ZC6BW55
source_type: video
authors: []
published_at: '2025-10-23 00:00:00'
theme_ids:
- agent_systems
- generative_media
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)

Julian Schrittwieser — a core architect of AlphaGo Zero, AlphaZero, and MuZero — argues that public discourse on AI is systematically underestimating frontier progress due to the unintuitive nature of exponential trends, and traces the intellectual lineage from AlphaGo's Move 37 to the modern pre-training + RL paradigm that underlies current agent capabilities.

**Authors:** Julian Schrittwieser
**Published:** 2025-10-23
**Type:** video

---

## Extrapolating the Exponential

The central claim is both simple and disorienting: autonomous task-completion length has been doubling every 3–4 months for several years without visible slowdown. This isn't extrapolated from a handful of data points — it reflects a consistent empirical trend across benchmarks, most notably METR's evaluations, which deliberately construct tasks with real-world messiness calibrated to specific time horizons.

The trajectory implied by this trend:

| Horizon | Projected Capability |
|---|---|
| Mid-2026 | Full-day autonomous task completion (implement a feature, produce a research report) |
| Late 2026 | At least one model matches industry expert performance across many occupations |
| 2027 | Models frequently outperform experts; Nobel Prize-equivalent discoveries plausible |

Schrittwieser is careful to note this doesn't mean all AI companies are on solid footing. A bifurcation is plausible: frontier labs (Anthropic, OpenAI, Google) accumulating real revenue while a broader ecosystem of AI-adjacent companies carries valuations unsupported by fundamentals. This would be an unusual market structure — bubble and non-bubble coexisting in the same sector.

**Why task length specifically?** Because it determines delegation capacity. A model that requires constant feedback limits what you can hand off. A model that can operate autonomously for hours becomes a manageable team member. The critical precondition is that the agent is smart enough to detect its own errors and self-correct — without this, long-horizon tasks just accumulate failures.

---

## From Move 37 to Modern RL

### The AlphaGo Lineage

Move 37 in the 2016 match against Lee Sedol was more than a famous moment — it was the first widely legible demonstration that AI could produce genuinely unexpected, creative outputs, not just optimal execution of encoded strategies. This matters for the contemporary debate about whether LLMs do "truly novel" things.

The technical progression that followed:

- **AlphaGo**: Supervised learning on amateur human games → deep network predicting move probabilities → combined with [[themes/reinforcement_learning|Monte Carlo Tree Search]] for planning and evaluation
- **AlphaGo Zero**: Human game data removed entirely. The network learned from self-play from scratch, receiving only win/loss signals from game outcomes. Rules were not encoded into the network — they were used only to score game results. All Go knowledge rediscovered autonomously.
- **AlphaZero**: Go-specific components stripped out. A single algorithm generalized across Go, chess, and Shogi with no game-specific knowledge.
- **[[themes/video_and_world_models|MuZero]]**: Motivated by a practical constraint — real-world tasks rarely come with a perfect simulator. MuZero learns a world model from interaction rather than assuming access to a perfect environment model.

Each step moved further from hand-coded knowledge and closer to pure self-directed learning from experience.

---

## The Pre-training + RL Synthesis

Schrittwieser identifies the dominant theme of 2025 as making [[themes/pretraining_and_scaling|pre-training]] and [[themes/reinforcement_learning|reinforcement learning]] work together. The logic is straightforward:

- Pre-training on large text corpora implicitly builds a world model and rich semantic representations
- This gives RL a massive head start — rather than exploring from scratch, the agent begins with a compressed model of how the world works
- RL then fine-tunes this representation through interaction, generating training data from the model's own behavior distribution

The virtuous cycle is critical: as models become smarter, the RL data they generate becomes more interesting and informative. The data quality scales with model capability.

**What pre-training cannot provide** is equally important. Internet text captures knowledge, not actions. It contains no examples of an agent failing, detecting the failure, and recovering. RL fills this gap — agents learn from their own error distributions in ways that pre-training data structurally cannot supply.

### The Prior Problem

Pre-training creates a powerful prior, but priors can restrict exploration. If the training distribution strongly weights against certain action sequences — even if those sequences are correct — the agent may never explore them. This is a known failure mode with no clean solution: [[themes/reinforcement_learning|strong priors accelerate learning in-distribution but can prevent discovery of out-of-distribution optima]].

---

## Novelty, Evaluation, and the Move 37 Equivalent for LLMs

The question of whether LLMs do genuinely novel things is, Schrittwieser argues, mostly settled: models sample from probability distributions over token sequences, making novel output structurally guaranteed. The harder question is whether novel outputs are *useful and interesting*.

This maps directly to why AlphaGo Zero's self-play worked: it required both the ability to generate diverse candidate moves *and* the ability to evaluate them accurately through MCTS. Neither alone is sufficient. The same constraint applies to modern [[themes/agent_systems|agent systems]] attempting open-ended scientific discovery — generation is easy; evaluation is the bottleneck.

The "Move 37 equivalent" for modern models requires:
1. A task sufficiently difficult and interesting that human solutions are not obviously optimal
2. A model capable of generating diverse candidates
3. A reliable evaluation mechanism that can distinguish useful novelty from noise

---

## Evaluation Infrastructure as a Binding Constraint

Evaluation is identified as a structural bottleneck with an irreducible trilemma:

> *Cheap · Reliable · Accurate — pick two.*

- **GDPval** (OpenAI): Authentic tasks from domain experts, compared against human expert performance. Accurate and unbiased, but extremely expensive.
- **METR autonomous task horizon**: Measures how long models can operate independently. Naturally incorporates real-world messiness because long tasks cannot be artificially sanitized.
- Public benchmarks: Cheap and fast, but subject to Goodhart's Law — once they become optimization targets, they stop measuring what they were designed to measure.

The deeper problem is that benchmark saturation is not a sign of success. It signals that the benchmark has been captured by the optimization process and that the actual capability measurement has migrated elsewhere.

---

## Capabilities

- **Autonomous task execution doubling every 3–4 months** — consistent empirical trend across years of benchmarks, not a projection from a short series ([[themes/scaling_laws|scaling_laws]])
- **Pre-training + RL as a working paradigm** — the combination forms the current production architecture for capable [[themes/agent_systems|agent systems]]; neither alone is sufficient
- **RL from self-generated data** — agents can improve by interacting with environments and training directly on the resulting trajectories; data quality scales with model capability
- **Flexible reward signal composition** — human feedback, win/loss signals, automated verification, and constitutional rules can be combined without algorithm changes ([[themes/reinforcement_learning|reinforcement_learning]])
- **Genuine novelty from sampling** — models structurally generate outputs not present in training data; the constraint is useful novelty, not novelty per se

---

## Limitations and Open Questions

**Structural limitations of pre-trained agents**
Raw pre-trained models are weak agents. Internet corpora are rich in information but devoid of action sequences, failure examples, and recovery trajectories. The gap between "knows about X" and "can do X autonomously" remains significant, and RL is the current best answer — not a complete one. (severity: significant, trajectory: improving)

**RL debugging complexity**
RL training pipelines have feedback cycles that make failure attribution unclear: is the problem in the reward signal, the data generation, the network update, or their interaction? This is substantially harder than supervised learning debugging and remains a practical bottleneck for scaling. (severity: significant, trajectory: improving)

**The prior restriction problem**
Pre-training priors can prevent exploration of correct but unconventional solutions. The tension between fast in-distribution learning and out-of-distribution generalization is unresolved. For scientific discovery applications, this is a significant concern. (severity: significant, trajectory: unclear)

**Exponential research difficulty**
Easy problems are found first. As a field matures, productivity gains must outpace exponentially increasing difficulty to maintain linear visible progress. Whether AI-assisted research can sustain this balance is the key uncertainty for claims about scientific breakthroughs by 2027. (severity: significant, trajectory: worsening)

**The evaluation trilemma**
No evaluation approach simultaneously achieves low cost, high reliability, and accuracy. As public benchmarks saturate, the burden shifts to expensive human-expert evaluations, which limits how frequently meaningful capability measurements can be taken. (severity: significant, trajectory: unclear)

**AI vs. human intelligence character mismatch**
AI systems that excel at quantitative and linguistic tasks often struggle with embodied, intuitive, and perceptual tasks. This is not a temporary gap — it reflects a fundamental difference in the structure of artificial vs. human intelligence. The economic implications depend heavily on which task types matter most. (severity: minor, trajectory: stable)

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/video_and_world_models|Video and World Models]]
- [[themes/generative_media|Generative Media]]

## Key Concepts

- [[entities/agentic-ai|Agentic AI]]
- [[entities/constitutional-ai|Constitutional AI]]
- [[entities/expert-iteration|Expert Iteration]]
- [[entities/goodharts-law|Goodhart's Law]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-verifiable-rewards|Reinforcement Learning from Verifiable Rewards]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/world-model|World Model]]
- [[entities/self-play|self-play]]
