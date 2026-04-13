---
type: source
title: The future of robotics
source_id: 01KJVNEG9Q5ACG8Q4DVQCMHBBT
source_type: video
authors: []
published_at: '2024-05-10 00:00:00'
theme_ids:
- robotics_and_embodied_ai
- robot_learning
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Future of Robotics

> A wide-ranging expert discussion on the current state and near-term trajectory of robotics, covering the transformative but incomplete role of LLMs in robot reasoning, the severe data and hardware bottlenecks blocking progress, and a pragmatic case for targeted augmentation over general-purpose robots. The source is candid about how far the field remains from its popular imagination.

**Authors:** 
**Published:** 2024-05-10
**Type:** video

---

## What This Source Contributes

This source offers a grounded, practitioner-level assessment of robotics as of mid-2024. Its most valuable contribution is the explicit framing of LLMs as a partial solution — genuinely useful for high-level task planning, but structurally incapable of generating low-level motor commands. It also quantifies the data gap precisely (a factor of millions between robotics and NLP/vision), and argues that the path to practical deployment runs through narrow, well-scoped applications rather than general-purpose humanoids.

---

## LLMs as a Partial Unlock

The arrival of large language models has meaningfully changed what is possible in [[themes/robotics_and_embodied_ai|robotics]]. For the first time, robots can engage in open-ended multi-step task planning — decomposing a goal like "make dinner" into a structured sequence of sub-tasks — using the common-sense world knowledge embedded in models like GPT-4. The interface between humans and robots has become dramatically more natural as a result.

LLMs also encode useful semantic constraints for manipulation: that glass is fragile, that a hammer should be grasped by the handle, that pressure should be modulated based on object properties. These are not derived from robot-collected data but from the general language corpus, and they transfer usefully into grasp planning and motion parameterisation.

> "These language models, they have this common sense knowledge baked in them, and now we can use that in robotics to do these task plans... it's not always correct, but the good thing is that they open up these doors for task planning to be done in an open-ended way."

This constitutes a genuine [[themes/vision_language_action_models|breakthrough]] at the symbolic planning layer. But it is bounded.

---

## The Hard Ceiling: Motor Control

LLMs cannot generate continuous motion trajectories. The action a robot needs — where exactly to move its hand every 10–100 milliseconds — is not a natural language output. It requires training on actual recorded robot arm motion, a fundamentally different data modality.

This creates a sharp two-layer architecture problem: LLMs handle the "what to do" layer, but the "how to move" layer requires separate learned models trained on robot-collected demonstrations. The gap between these layers is one of the central [[themes/robot_learning|open problems]] in the field.

> "They still cannot directly generate an action. The action that a robot needs to compute cannot be done by these models. To do that, actual motion of the robot arm needs to be given to these models."

---

## The Data Bottleneck

The magnitude of the data gap is striking. NLP and computer vision models have been trained on trillions of tokens and billions of images. Robotics has approximately hundreds of thousands of data points — a difference of roughly a million times.

Collecting robot motion data is expensive by construction: it must be gathered via teleoperation, joystick control, or physical demonstration, on physical hardware, in real time. This is painstakingly slow compared to scraping the internet.

One proposed path around this bottleneck is **learning from human video** — leveraging the vast corpus of YouTube demonstrations in the same way humans learn by watching. This is an active research question but remains unsolved. The core obstacle is **morphological mismatch**: a robot observing a human hand manipulating an object must translate those actions to a gripper with a completely different structure, degrees of freedom, and physical capabilities. The human hand has approximately 27 degrees of freedom and can modulate between stiff and compliant; most robot end-effectors are simple two-finger grippers.

> "If a robot looks at a video of a person, it needs to somehow understand how it maps to its own body — a translation of whatever was happening in the video to their world."

Breaking this translation problem would unlock an enormous source of training signal. It has not been broken.

---

## Hardware: Reliability and Cost

Hardware is identified as one of the most significant systemic constraints. The field bifurcates sharply:

**Industrial robots** (factory automation) are highly reliable, repeatable, and proven at scale. But they are rigid, dangerous, and must be physically separated from humans by cages. They cannot operate in unstructured human-shared environments.

**Research robots** are designed for versatility and compliance — the kind needed in homes and hospitals — but are expensive ($40,000–$70,000 per arm), fragile, and require constant repair. They are one-of-a-kind custom platforms, making it difficult to validate algorithms across labs or iterate quickly.

> "I'm constantly talking to my students and they're constantly repairing whatever new thing is broken again with our robots. I spent so much money from my lab on buying $40,000 robot arms or $70,000 robot arms."

This creates a compounding problem: the platforms most useful for real-world research are the least scalable and reliable, and the reliable platforms are unsuitable for the target deployment environments. Low-cost, durable, compliant mobile manipulation platforms are an active development goal, but are not yet available.

---

## The 90% Problem

A recurring theme across robotics (and [[themes/robotics_and_embodied_ai|autonomous systems]] generally) is the difficulty of the final 10%. Reaching 90% task completion in controlled conditions is achievable. The remaining edge cases — the unusual door, the unexpected obstacle, the atypical object — are what block real-world deployment.

> "You can probably bring it up, similar to autonomous driving, to maybe 90%. But then the rest of it is all these corner cases and edge cases, and that's really what requires a lot more work."

This asymmetry has direct implications for deployment timelines and economic viability. A robot that fails 10% of the time in a home context is not deployable. At $80,000–$100,000, it would need to be reliably useful to justify the cost — and current systems are not.

---

## Practical Deployment: The Augmentation Approach

The source argues that waiting for general-purpose robots is the wrong frame. A more productive strategy is identifying high-value, narrowly-scoped tasks that are achievable with current technology and where the cost of failure is manageable.

The Diligent Robotics case is offered as a model. Rather than building a patient-care robot, the company studied nurses' actual time use and found that supply shuttling — not patient interaction — consumed a disproportionate amount of their time. A robot capable of navigating a hospital corridor and pushing elevator buttons solves a real problem without requiring general-purpose capability.

This framing — **augmentation over automation, narrow over general** — recurs throughout the source. Exoskeletons supporting heavy lifting, prosthetics, specialised logistics robots: these are achievable and useful now, without waiting for breakthroughs in dexterity or robustness.

---

## Open Questions and Landscape Connections

| Question | Status |
|---|---|
| Can human video data be cross-morphology translated for robot training? | Open research problem |
| When will low-cost, durable, compliant platforms be available? | Unknown horizon |
| Can LLM hallucination be made safe enough for robot task planning? | Partially mitigated, not resolved |
| Will general-purpose humanoid robots reach practical deployment? | Unclear; may be sub-optimal form factor |

**Related themes:**
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]
- [[themes/robot_learning|Robot Learning]]
- [[themes/vision_language_action_models|Vision-Language-Action Models]]

**Key bottlenecks flagged:**
- Robot motion training data scarcity (blocking; 3–5 year horizon)
- High-level to low-level control gap (blocking; unknown horizon)
- Cross-morphology video transfer (blocking; 3–5 year horizon)
- Hardware reliability and cost for unstructured environments (blocking; 3–5 year horizon)
- Edge-case robustness for production deployment (blocking; 5+ year horizon)

## Key Concepts

- [[entities/teleoperation|teleoperation]]
