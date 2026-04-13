---
type: source
title: Robotics Research Update, with Keerthana Gopalakrishnan and Ted Xiao of Google
  DeepMind
source_id: 01KJVN9ZJX206MA7GP8WJWM6DT
source_type: video
authors: []
published_at: '2024-04-22 00:00:00'
theme_ids:
- in_context_and_meta_learning
- post_training_methods
- pretraining_and_scaling
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Robotics Research Update, with Keerthana Gopalakrishnan and Ted Xiao of Google DeepMind

> A wide-ranging conversation with two Google DeepMind researchers covering six papers published in 2023–2024 that mark a step-change in robot learning: RT-2, RT-X, RT-Trajectory, AutoRT, Learning to Learn Faster, and PIVOT. Together these works demonstrate that the same foundation model architectures and scaling techniques driving progress in language and vision can be applied to robotics—but also surface the field's most stubborn bottlenecks around data, motion representation, and safety.

**Authors:** Keerthana Gopalakrishnan, Ted Xiao (Google DeepMind)
**Published:** 2024-04-22
**Type:** video

---

## The Inflection Point Framing

A year prior, robotics was characterized as sitting between GPT-2 and GPT-3—capable but brittle, starved of internet-scale data. By the time of this conversation, the characterization had shifted: we are closer to GPT-3 era robotics. The explanation is less about any single breakthrough and more about a compounding systems effect:

> "Things that used to work maybe 20–30% of the time are now working 60–70% of the time."

In a complex engineered system where many components must work together, a uniform reliability improvement across every subsystem—research iteration, engineering scaling, data collection—accelerates progress nonlinearly. This framing sets the context for all six papers discussed.

---

## Papers Covered

### RT-2: Internet Knowledge Meets Robot Control

[[themes/vision_language_action_models|Vision-Language-Action Models]]

RT-2 is the direct successor to RT-1. Where RT-1 demonstrated that sufficient in-domain data yields high in-domain performance, RT-2 addresses the harder problem of generalization. The key insight: express robot actions as language tokens, so a single end-to-end model handles both semantic understanding and motor commands without a separate action head.

**Co-training** is the mechanism that makes this work. Each training batch contains both image-language pairs from the internet and robot trajectory data from Google's in-house collection (~130,000 teleoperated demonstrations on ~17 object categories in office/kitchen settings). This prevents catastrophic forgetting—the model retains internet concepts while learning to act.

The result: robots can manipulate objects never seen in training by stitching internet concepts onto in-domain motor patterns.

**Critical limitation:** motion generalization is bounded by the training corpus. The model can transfer internet semantic knowledge to *known* movements, but cannot generate *novel* movements. This is structural: physics, contact dynamics, and manipulation trajectories do not exist at scale on the internet, so there is no corresponding pre-training signal to transfer.

> "Movement data or even the physics of how to grab different objects does not quite exist on the internet—so where would that knowledge come from?"

See: [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/robot_learning|Robot Learning]]

---

### RT-X: The Embodiment Generalization Problem

[[themes/scaling_laws|Scaling Laws]] | [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]

RT-X is a multi-lab collaboration establishing a shared dataset and demonstrating cross-embodiment transfer. The headline result: a single generalist model trained across diverse robot morphologies—from small Widow-X tabletop arms to mobile manipulators to dexterous hands—outperforms specialist models trained for individual robots *on their own setups*.

This is conceptually significant. Prior to RT-X, the field had no common benchmark: each lab used different robots and different data, making results incomparable. The dataset revealed a secondary finding: massive redundancy, with most labs independently collecting pick-and-place data rather than complementary task coverage.

**On embodiment identification:** RT-X does not receive an explicit embodiment token. It infers which robot it is operating through visual observations alone. This works—remarkably—but imposes a hard constraint:

> "There's no possibility of zero-shotting to a completely unseen robot embodiment with a different action space or observation space."

The analogy that emerged post-RT-X: different robot embodiments are like different human languages—conceptually similar with differing surface expression. This reframing opened the door to cross-embodiment transfer as a principled research direction rather than an engineering impossibility.

**Remaining bottleneck:** implicit embodiment inference from pixels alone is brittle at the margins. No explicit robot API or action space specification capability exists, limiting zero-shot transfer to morphologies meaningfully different from those in training.

---

### RT-Trajectory: Bridging Planning and Learning

[[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]

RT-Trajectory addresses a longstanding tension in robotics: classical search-and-planning methods offer interpretable, long-horizon behavior but require explicit state representations; end-to-end learned policies are flexible but opaque and short-horizon. RT-Trajectory proposes a bridge: represent a planned trajectory as a simple line drawing overlaid on the camera image, then condition the policy on this sketch.

The result is granular behavioral control through visual prompting:

> "Under the same initial conditions, just change the prompt a little bit—do some prompt engineering—and you can get qualitatively different behavior."

A single human demonstration, reduced to a line sketch, enables in-context skill acquisition. This is [[themes/in_context_and_meta_learning|in-context learning]] applied to physical tasks, without retraining.

The limitation is representation fidelity: line sketches capture path geometry but not contact forces, timing, or gripper state. Tasks requiring dense contact specification cannot be fully represented this way.

---

### AutoRT: Scaling Human Oversight

[[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]

AutoRT tackles the operational scaling problem: how do you supervise 50+ robots operating in previously unseen real-world environments without proportional growth in human oversight? The system uses an LLM to generate candidate tasks appropriate to the current environment, then filters proposed actions through a *robot constitution*—a rules-based safety framework analogous in spirit to Constitutional AI.

The robot constitution provides first-line ethical and safety checks, allowing robots to reject tasks that violate defined constraints before attempting them. This is the field's most direct engagement with [[themes/robotics_and_embodied_ai|robot safety and alignment]] at deployment scale.

**Critical caveat:** safety and alignment for robotics remains in its infancy. Language-based specification of safety constraints is preliminary. The gap between 50 supervised robots and confident deployment in human homes involves unsolved problems in semantic safety specification, real-world edge case coverage, and business/integration challenges that are not purely technical.

---

### Learning to Learn Faster: Human Feedback Loops

[[themes/post_training_methods|Post-Training Methods]] | [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]

This work introduces a day/night learning cycle. During the day, a frozen policy interacts with users who provide natural language corrective feedback; the model updates in-context. Overnight, the accumulated feedback is used to retrain the underlying policy. This combines the immediacy of in-context adaptation with the permanence of gradient-based learning.

The architecture points toward a broader research direction: self-improvement through human interaction, without requiring new teleoperated demonstrations. The bottleneck it targets—linear scaling of data collection with human operators—is not solved but meaningfully softened.

---

### PIVOT: Zero-Shot VLM-Guided Robot Control

[[themes/vision_language_action_models|Vision-Language-Action Models]]

PIVOT asks whether a vision-language model, with no robot-specific fine-tuning, can guide robot actions. The answer is: yes, weakly, and the weakness is instructive. An optimization-based approach extracts implicit physical reasoning from VLM outputs—reasoning the models were never explicitly trained to produce.

Performance is far below fine-tuned policies. But the demonstration is conceptually significant:

> "The fact that it even kind of shows very promising behavior is itself surprising."

This establishes a lower bound on what general-purpose VLMs implicitly know about physical reasoning, and identifies the gap that robot-specific pre-training must close.

**Known gap:** VLMs trained on internet data lack dense contact spatial reasoning—left/right/up/down relationships, contact interactions, force estimation. This knowledge does not exist at scale in image-text corpora and cannot be transferred through prompting alone.

---

## Limitations and Open Questions

### Data

The most fundamental bottleneck: high-quality robot demonstrations require human teleoperation. Dataset sizes scale linearly with deployed human operators and robots—not logarithmically with compute, as in language. The RT-1 dataset of 130,000 demonstrations represents a ceiling achievable only through sustained, expensive human effort.

Paths forward mentioned: (1) improving data efficiency of policies so fewer demonstrations suffice, (2) self-improvement and autonomous data collection, (3) better leveraging of foundation model world knowledge to reduce the volume of robot-specific data required.

### Motion and Contact

Internet pre-training provides semantic generalization but zero motion generalization. The physics of grasping, contact dynamics, and manipulation trajectories are absent from web-scale corpora. This is not a scaling problem—it is a data distribution problem. Even a much larger internet crawl would not close this gap.

Current action tokenization is further inadequate for dextrous manipulation: it has no representational vocabulary for multi-point contact, contact forces, or complex state changes like deformable object manipulation.

### Scope Constraints

All six papers operate within a narrow morphological envelope: single-arm manipulators with two-fingered grippers and single cameras. Dextrous manipulation (multi-finger hands), mobile whole-body control, and interactions with fragile objects, liquids, or deformable materials remain largely outside current capabilities.

### Safety and Deployment

The robot constitution in AutoRT is a first step, not a solution. Reliable, safe home robots are described as "still some time away"—not primarily because of capability gaps but because of unsolved problems in semantic safety specification, business model viability, integration complexity, and real-world edge case coverage.

### Zero-Shot Transfer

Despite RT-X's cross-embodiment results, zero-shot transfer to genuinely novel morphologies (different action spaces, observation spaces) is not possible. The model's embodiment inference is implicit and fragile at distribution boundaries.

---

## Research Trajectory

Three identified directions for near-term focus:

1. **Data scale and efficiency** — either acquire more diverse demonstrations or reduce the volume required per skill
2. **Self-improvement** — autonomous data collection and policy improvement without continuous human supervision
3. **Foundation model leverage** — better interfaces between internet-scale pre-training and robot control, reducing the gap between PIVOT-style zero-shot and fine-tuned performance

The broader arc: robotics is not yet at GPT-4 equivalent capability, but the core architectural bet—that the same scaling paradigm that worked in language and vision will work in robotics—is gaining empirical support. The barriers are increasingly identified as data distribution problems and representation problems rather than fundamental architectural limits.

---

## Related Themes

- [[themes/vision_language_action_models|Vision-Language-Action Models]] — RT-2 and PIVOT directly instantiate this paradigm
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]] — primary theme across all six papers
- [[themes/robot_learning|Robot Learning]] — cross-embodiment transfer, in-context skill acquisition
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — co-training strategy, scaling bottlenecks
- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]] — RT-Trajectory, Learning to Learn Faster
- [[themes/post_training_methods|Post-Training Methods]] — human feedback integration, overnight retraining cycles
- [[themes/scaling_laws|Scaling Laws]] — generalist vs. specialist tradeoffs, data scaling constraints

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/imitation-learning|Imitation Learning]]
- [[entities/rt2|RT2]]
