---
type: source
title: Ilya Sutskever – We're moving from the age of scaling to the age of research
source_id: 01KJVEQ1YVKVV8HEEVNSR41YTY
source_type: video
authors: []
published_at: '2025-11-25 00:00:00'
theme_ids:
- ai_governance
- alignment_and_safety
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Ilya Sutskever – We're moving from the age of scaling to the age of research

> A wide-ranging reflection by Ilya Sutskever on why current AI models feel jagged — brilliant on benchmarks, brittle in practice — and what it reveals about the deeper unsolved problems of generalization, RL environment design, and value functions. The talk argues that the field is transitioning from a period dominated by scaling into one requiring genuine algorithmic and scientific research.

**Authors:** Ilya Sutskever
**Published:** 2025-11-25
**Type:** video

---

## The Core Puzzle: Model Jaggedness

The central mystery Sutskever frames is a striking disconnect: frontier models crush hard benchmarks yet produce economic impact that seems disproportionately small relative to their apparent capability. This is not a minor gap — it is "one of the very confusing things about the models right now."

He offers two explanations:

**1. RL makes models single-minded.** [[themes/reinforcement_learning|Reinforcement learning]] may sharpen models in the directions rewarded during training while paradoxically flattening their broader contextual awareness. A model becomes laser-focused on the immediate conversational thread but loses global coherence and self-consistency. It becomes "aware" in some ways while becoming less aware in others.

**2. Researchers reward-hack themselves.** The deeper problem may not be in the model at all. RL environment design involves enormous degrees of freedom — unlike pre-training, where the answer to "what data?" is always "everything," RL requires deliberate choices about tasks, prompts, reward schemes, and curricula. In practice, those choices are implicitly guided by existing evals. Teams build environments that resemble the benchmarks they want the model to score well on. The result is overfitting at the research level, not just the model level:

> *"The true reward hackers may not be the models but the researchers, optimising too hard for polished eval scores rather than broad, messy robustness."*

This creates a situation where excellent benchmark performance coexists with mediocre real-world reliability — not because the model is deceptive, but because the entire training pipeline was inadvertently tuned to the eval.

---

## The Student A vs. Student B Analogy

Sutskever uses a clarifying analogy. Imagine two students learning competitive programming:

- **Student A** dedicates 10,000 hours — solves every problem, memorises every trick, drills every proof pattern.
- **Student B** practices perhaps 100 hours, performs extremely well, but invests far less.

Student B almost always becomes the better long-term engineer. Student A has depth in a narrow band; Student B has intuition, taste, conceptual clarity, and flexible reasoning.

> *"Models today are built much more in the image of Student A — trained on every competitive programming problem ever — and unsurprisingly we get a brilliant competitive programmer and a brittle software engineer."*

This reframes the benchmark-vs-reality gap: it is not a measurement artifact. It reflects a genuine training regime problem. Expanding the set of RL environments (the natural remedy) only partially addresses it. If the underlying generalisation mechanism is absent, more environments will not restore it.

---

## Pre-training: What It Gives and What It Cannot

[[themes/pretraining_and_scaling|Pre-training]] provides two advantages that no subsequent training stage replicates: scale (far more signal than any human could absorb) and naturalness (the world as rendered in text). But it does not automatically yield robust generalisation, and it is theoretically opaque in a way that makes debugging nearly impossible:

> *"Pre-training is very difficult to reason about because it's so hard to understand the manner in which the model relies on pre-training data."*

When a model fails, it is often unclear whether the failure reflects an absent or undersupported pattern in training data, a reasoning failure, or a generalisation failure — three very different root causes with very different remedies.

Two tempting analogies for pre-training both break down:

- **Childhood as pre-training**: Children process a tiny fraction of an LLM's data yet achieve vastly deeper, more robust, more transferable understanding. Childhood is not passive self-supervised learning; it is interactive, hierarchical curriculum learning under constant reward pressure, partially orchestrated by evolution.
- **Evolution as pre-training**: Evolution is not a statistical learner — it is an infinite-horizon RL system with a binary reward function (survive or not). Its contributions to human cognition include hardcoded priors for vision, locomotion, and social behavior that have no counterpart in current training.

There is no human analogue to pre-training. This makes it fundamentally difficult to reason about what it accomplishes and what it cannot.

---

## Value Functions: The Missing Mechanism

Current RL training for reasoning models (o1, R1-style approaches) is done without value functions. The model produces an entire chain of thought and only receives a reward at the very end. This creates a structural problem for long-horizon tasks:

> *"That means that if you are doing something that goes for a long time — if you're training a task that takes a long time to solve — it will do no learning whatsoever until it has solved it for the first time."*

A value function would provide intermediate reward signals — probabilistic estimates of whether the current trajectory is heading toward success — allowing credit to be assigned before the end of a rollout. This is not merely an efficiency gain; it is the difference between a learnable and an unlearnable signal for complex tasks.

The [[themes/rl_for_llm_reasoning|DeepSeek R1 paper]] noted that trajectory diversity in domains like coding makes intermediate value learning difficult: when a model is mid-solution, there are many possible next states, and mapping from current state to eventual outcome is ambiguous. But Sutskever expects value functions will eventually be incorporated anyway — not because they enable qualitatively new behaviors (anything achievable with them can be done without, just more slowly), but because the efficiency gains are substantial.

---

## The Emotion-as-Value-Function Hypothesis

A neuroscience case study is invoked to illustrate what current ML value functions lack. A patient who suffered damage to the brain region responsible for emotional processing remained fully articulate, logical, and capable of solving cognitive puzzles — but became nearly incapable of making decisions. Without emotional circuitry, routine choices became paralysing.

Sutskever's interpretation: human emotions may function as an evolutionarily hardcoded value function — a compressed encoding of what is good and bad across vast domains of experience, encoded at the neural level through millions of years of selection pressure. This is not a romantic claim; it is a structural one. Current ML systems have learned value functions attached to specific tasks. Humans have something more like a domain-general prior over value that modulates all behavior.

> *"Evolution also has endowed us with all these social desires... it's a high-level concept that's represented in the brain. I don't know how evolution did it, but it did it."*

This has a direct implication for [[themes/alignment_and_safety|alignment]]: the difficulty of teaching AI systems desired behaviors may not be purely a specification problem. It may reflect the absence of a substrate — an emotionally-encoded, evolutionarily-prior value system — that makes humans easy to teach via observation and social context.

---

## The Age of Research

The talk's framing argument is that scaling, while transformative, has consumed all the oxygen in the room:

> *"One consequence of the age of scaling is that scaling sucked out all the air in the room. Because scaling sucked out all the air in the room, everyone scaled."*

Capital allocated to scaling infrastructure crowded out architectural and algorithmic research. The field optimized for what was known to work. Now, with [[themes/scaling_laws|scaling laws]] showing signs of diminishing returns on certain axes, the field needs to return to genuine scientific investigation — understanding why models generalize poorly, how value functions should be structured, what the right RL curriculum looks like, and potentially what alternatives to transformers might exist.

This does not mean scaling is over. It means that the next gains will come from understanding, not from compute alone.

---

## Key Limitations Identified

| Limitation | Severity | Trajectory |
|---|---|---|
| Models generalize dramatically worse than humans despite benchmark superiority | Blocking | Stable |
| Eval-benchmark gap; unclear whether gap reflects deployment issues or eval overfitting | Significant | Worsening |
| RL environment design lacks principled selection criteria; degrees of freedom too high | Significant | Stable |
| No value functions in current training; long-horizon RL produces no signal until completion | Blocking | Improving |
| Pre-training data dependencies are opaque; failures undiagnosable | Significant | Stable |
| Trajectory diversity makes intermediate value estimation difficult in coding/math | Significant | Improving |
| Models lack evolutionarily-hardcoded domain-general value priors | Significant | Stable |
| Models cannot absorb behavioral goals from social context without bespoke reward engineering | Significant | Stable |

---

## Open Questions

- Is the benchmark-reality gap primarily an eval-overfitting artifact, or does it reflect a deeper generalisation failure?
- Can value functions be learned effectively in domains with high trajectory diversity, or does this require architectural changes?
- Is there an analogue to evolutionary priors that can be introduced into training — or does this require a fundamentally different paradigm?
- What would it mean to train a model more like Student B — and what training objective produces that kind of flexible, taste-driven competence?
- When does expanding RL environments help, and when does it only deepen the eval-overfitting problem?

---

## Related Themes

- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/alignment_and_safety|Alignment and Safety]]
- [[themes/ai_governance|AI Governance]]

## Key Concepts

- [[entities/continual-learning|Continual learning]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/sample-efficiency|Sample Efficiency]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/value-function|Value Function]]
- [[entities/vibe-coding|Vibe Coding]]
