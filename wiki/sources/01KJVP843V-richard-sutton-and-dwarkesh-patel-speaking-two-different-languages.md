---
type: source
title: Richard Sutton and Dwarkesh Patel – speaking two different languages
source_id: 01KJVP843VKX3S3CDY4PP7SC8P
source_type: video
authors: []
published_at: '2025-09-29 00:00:00'
theme_ids:
- generative_media
- pretraining_and_scaling
- reinforcement_learning
- rl_theory_and_dynamics
- scaling_laws
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Richard Sutton and Dwarkesh Patel – Speaking Two Different Languages

This source documents a viral podcast exchange between Richard Sutton — co-inventor of reinforcement learning and 2024 Turing Award recipient — and podcaster Dwarkesh Patel, revealing how the same words mask fundamentally incompatible conceptual frameworks, and articulating Sutton's case that LLMs are a detour from the path to genuine intelligence.

**Authors:** Richard Sutton, Dwarkesh Patel
**Published:** 2025-09-29
**Type:** video

---

## Why This Conversation Matters

The exchange caught fire on Twitter not because of a single disagreement, but because two people speaking the same words were operating in entirely different conceptual universes. Sutton comes from the tradition of Alan Turing and John McCarthy — where intelligence means acting in the world, having goals that change the world, and learning from consequences. Patel comes from the LLM era, where prediction means next-token generation, goals mean training objectives, and world models mean large language models.

The collision of these two vocabularies is the substance of the interview.

---

## The Vocabulary Gaps

### Prediction

Sutton's prediction is grounded in the world: *if I act, what happens next?* The model predicts, then receives ground truth through real consequences. Surprise — the gap between prediction and outcome — drives learning.

Patel's prediction is textual: *what is the next word?* LLMs predict token sequences, which can superficially resemble reasoning or planning. But there is no prediction in Sutton's sense — the network cannot predict what a human will do *after* receiving the model's output. The feedback loop is broken.

> "There is no actual prediction in the sense that the network cannot predict what you, as a human, will do after the network gave you this token-after-token reply."

### Goals

McCarthy's definition anchors Sutton: *intelligence is the computational part of the ability to achieve goals.* A goal, for Sutton, is a real-world outcome — something that changes the environment. When Patel argues that LLMs have goals (next-token prediction), Sutton rejects this: a training objective is not a goal. The system is not trying to change anything. It is sitting there predicting.

> "When Sutton says goal, he means a real-world outcome. When Dwarkesh says goal, he means an internal training objective. Very different."

### Imitation

Patel invokes imitation learning as a parallel to how children acquire skills — cultural transmission through repetition. Sutton's counter: children's imitation is never goalless. There is always a *why* behind what a child imitates. Mindless repetition does not describe what children do. The goalless-mimicry framing mischaracterizes the developmental process.

### World Models

When Patel describes LLMs as "the best world models we've made to date," Sutton pushes back directly. A world model, properly defined, enables prediction of what would happen *after an action the model takes*. LLMs do not model consequences of their own actions in open environments — only in controlled or simulated settings. Sutton went further: he asked Patel not to use the word *model* for LLMs at all, preferring *artificial neural networks* or simply *networks*.

---

## Sutton's Framework for Intelligence

Sutton offers a four-part decomposition of intelligence — what he calls the **experiential paradigm**:

1. **Policy** — in the situation I'm in, what should I do?
2. **Value Function** (from TD Learning) — how well is it going?
3. **Perception / State** — your sense of where you are.
4. **Transition Model of the World** — if you do this, what happens? The physics of consequences.

This is the framework LLMs are missing. They have no policy grounded in real-world outcomes, no value function tied to environmental feedback, and no transition model predicting action consequences. They are architecturally orthogonal to this decomposition.

---

## Sutton's Assessment of LLMs

Sutton did not declare LLMs dead. He expressed genuine surprise at how effective artificial neural networks have proven at language tasks. But effectiveness at language is not effectiveness at intelligence:

> "I expect there to be systems that can learn from experience which could perform much better and be more scalable. In which case it will be another instance of the Bitter Lesson — the things that used human knowledge were eventually superseded by things that just trained from experience and computation."

LLMs, in this view, are a capable but fundamentally limited artifact. The [[themes/scaling_laws|scaling laws]] that drive their improvement do not address the architectural absence of real-world grounding.

---

## Capabilities Identified

- [[themes/pretraining_and_scaling|LLM next-token prediction]] operates at broad production scale and maturity — the technology works as described.
- LLM outputs can superficially resemble [[themes/rl_theory_and_dynamics|reasoning and planning]] processes, even though the underlying mechanism is token-sequential generation.

---

## Limitations Identified

| Limitation | Severity | Trajectory |
|---|---|---|
| LLMs cannot predict real-world consequences of actions | **Blocking** | Stable |
| LLMs lack genuine goals that change the world | **Blocking** | Stable |
| LLMs are not true world models in non-controlled environments | Significant | Stable |
| Current AI does not learn from embodied physical experience | Significant | Stable |
| No consensus on whether LLMs are adequate scaffolding for AGI | Significant | Unclear |

The most important of these is the first two. They are not incidental gaps — they are structural absences from Sutton's definition of what intelligence *is*. An LLM that cannot predict real consequences and has no world-affecting goal is, in Sutton's framework, not a candidate for AGI regardless of scale.

---

## Open Bottlenecks

**Real-world grounding** — Current AI systems lack grounding in environmental consequences, preventing the development of truly agentic systems that learn from and predict the effects of their actions. Simulation helps but does not resolve the bottleneck. Horizon: unknown.

**Training objective / goal alignment** — The fundamental architectural gap between next-token prediction (training objective) and real-world goal-directedness blocks the development of agents that can genuinely modify their environment. Horizon: unknown.

**AGI path consensus** — There is active theoretical disagreement about whether LLM-based approaches plus additional mechanisms can reach AGI, or whether fundamentally different learning paradigms are required. Patel thinks LLMs may be the right scaffolding if they can generalize sufficiently. Sutton thinks the whole approach misses the target. Horizon: 5+ years.

See [[themes/video_and_world_models|video and world models]] and [[themes/reinforcement_learning|reinforcement learning]] for adjacent bottleneck tracking.

---

## Sutton's View on AI Succession

Sutton holds that AI succession — the transition of dominant intelligence from biological to digital or augmented forms — is inevitable, driven by four structural forces:

1. No unified human governance capable of stopping development.
2. The problem of intelligence will be solved.
3. Superintelligence will be reached.
4. The most intelligent entities will accrue power.

This succession, in his view, should be grounded in the experiential paradigm — systems that learn from actual interaction with the world, not from static text corpora.

---

## Connections

- [[themes/reinforcement_learning|Reinforcement Learning]] — Sutton's four-part intelligence framework is the conceptual core of RL, applied here as a lens to evaluate LLMs.
- [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]] — The TD Learning origin of the value function and the experiential paradigm connect directly to theoretical foundations.
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — The Bitter Lesson prediction positions LLMs as the current dominant paradigm but not the final one.
- [[themes/video_and_world_models|Video and World Models]] — The world model definitional dispute is a direct intervention in debates about what counts as a world model.
- [[themes/scaling_laws|Scaling Laws]] — Implicitly challenged: scaling LLMs may not address the structural limitations Sutton identifies.
- [[themes/generative_media|Generative Media]] — LLMs as generators of language outputs are effective at their task; the question is whether that task is intelligence.

---

## Editorial Note

This source is unusual in being as much about epistemology as about technical substance. The value is not just Sutton's claims but the diagnostic of how the field speaks past itself. The same words — prediction, goal, world model, imitation — carry incompatible meanings across the old and new schools of AI research. Any synthesis of this source with LLM-era literature should account for these definitional faultlines explicitly.

## Key Concepts

- [[entities/bitter-lesson|Bitter Lesson]]
- [[entities/imitation-learning|Imitation Learning]]
- [[entities/large-language-model|Large Language Model]]
- [[entities/reinforcement-learning|Reinforcement Learning]]
- [[entities/the-bitter-lesson|The Bitter Lesson]]
- [[entities/world-model|World Model]]
- [[entities/value-function|value function]]
