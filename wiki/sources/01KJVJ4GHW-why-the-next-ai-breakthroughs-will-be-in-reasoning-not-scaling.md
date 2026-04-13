---
type: source
title: Why The Next AI Breakthroughs Will Be In Reasoning, Not Scaling
source_id: 01KJVJ4GHWQJ4E9T3EKKD6DZAG
source_type: video
authors: []
published_at: '2024-11-14 00:00:00'
theme_ids:
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why The Next AI Breakthroughs Will Be In Reasoning, Not Scaling

> This source argues that OpenAI's o1 model represents a step-function capability shift driven by test-time compute and chain-of-thought reasoning — an orthogonal scaling direction to pretraining — and illustrates this through concrete case studies in circuit design and aerodynamic engineering. It makes the case that the next competitive moat in AI products is proprietary domain-specific evaluation data, not model improvements alone.

**Authors:** (YouTube/podcast hosts, guests unnamed in transcript)
**Published:** 2024-11-14
**Type:** video
**Source:** https://www.youtube.com/watch?v=JiwiqYGw4iU&t=34s

---

## Core Argument

The central claim is that [[themes/test_time_compute_scaling|test-time compute scaling]] via chain-of-thought reasoning is an orthogonal research direction to pretraining scaling — and that this direction is responsible for o1's step-function capability gains over GPT-4o. Rather than simply training a larger model, o1 learns *how to think* by receiving process-level feedback on intermediate reasoning steps, not just final outputs. This is the critical distinction: prior models were trained on what answers to produce; o1 is trained on how to reason toward them.

Sam Altman's founding motivation for [[entities/openai|OpenAI]] anchors the framing: he believed AGI would be better at science than humans, accelerating all scientific progress. The reasoning capability gap — the inability to think through complex problems systematically — was what blocked that vision. o1 is presented as the first credible step toward closing it.

---

## Mechanism: How o1 Reasons Differently

o1's architecture draws on [[themes/reinforcement_learning|reinforcement learning]] techniques developed during OpenAI's Dota project, which used self-play and reward functions to achieve superhuman performance on a complex planning game. The same family of RL algorithms (rooted in Q-learning) underpins o1's chain-of-thought training.

The key innovations:

- **Process reward models**: Feedback is provided on each reasoning step, not just the final answer. This enables direct supervision of *thinking patterns*, not just output correctness.
- **Proprietary CoT dataset**: OpenAI built an expensive new dataset of chain-of-thought traces — a giant dataset of how to break complex problems into reasoning steps — at significant internal cost. This is not replicable cheaply.
- **Deliberate opacity**: o1's internal reasoning chain is hidden from users in ChatGPT. A simplified version is displayed. This is a deliberate choice to protect the training data advantage embedded in the CoT traces.

The result is that o1 can apply more compute at inference time to iteratively improve its reasoning — analogous to a human scientific organization working through a problem, but more consistently.

---

## Case Studies

### Diode Computers: Circuit Design

Diode Computers is building an AI designer for PCB/circuit design. PCB design involves four major steps: system design (architecture and component selection), schematic layout, component placement, and routing. Routing is an NP-complete problem; companies like Nvidia, Intel, and Apple employ large teams of electrical engineers specifically for it.

Up to GPT-4, Diode had automated significant portions of schematic design and simple routing. But **system design and component selection remained out of reach** — requiring expert knowledge to read datasheets and select appropriate components.

With o1, Diode demonstrated full system design from a natural language description. Given a specification like "build a wearable heart rate monitor with an accelerometer and a microcontroller," o1 reads the component database, selects the appropriate parts, and outputs the matched design.

Critically: **Diode had tried the same prompts with GPT-4o. It flat out didn't work.** Switching to o1 without any other changes made it work. This is the clearest evidence cited for a step-function capability unlock rather than incremental improvement.

The system uses a multi-model architecture: GPT-4o-mini extracts unstructured data from PDF datasheets into structured format, which o1 then reasons over. This pattern — smaller models for extraction, reasoning models for decision-making — is described as increasingly common across complex AI products. See [[themes/startup_and_investment|startup and investment]] context for competitive implications.

**Capability**: o1 can design circuits from natural language (maturity: narrow production)
**Limitation**: requires pre-structured data; PDF extraction is a prerequisite step

### Camfer: CAD Design

Camfer is described as "Devin for CAD" — a system that generates CAD designs from natural language. Normally this requires a mechanical engineer to run simulations and solve governing equations.

o1 was able to write and solve partial differential equations (Navier-Stokes) to design airfoils from natural language specifications, handling multiple simultaneous simulation constraints. Previously this required mechanical engineers running dedicated simulation software.

Camfer's implementation is notable: rather than a plugin to SolidWorks, it runs as a desktop executable that opens SolidWorks and controls the UI directly, simulating human interaction. This is an early example of computer-use patterns applied to engineering workflows.

The broader implication pointed to: if scaling laws hold, far more difficult engineering challenges — room temperature fusion, complex fluid mechanics — become tractable. This is presented as a directional indicator of where [[themes/test_time_compute_scaling|test-time compute scaling]] leads.

---

## Landscape Contributions

### Capabilities Demonstrated

- **Circuit system design from natural language** — full component selection and PCB layout from high-level specs (narrow production). See [[themes/reasoning_and_planning|reasoning and planning]].
- **PDE-based aerodynamic optimization** — writing and solving Navier-Stokes equations to optimize airfoil designs (narrow production).
- **Complex customer support edge case handling** — 70% error rate reduced to 5% using CoT + process reward models trained on evaluation data; accuracy on hardest cases went from 0% to 85% (narrow production).
- **Multi-model orchestration** — using GPT-4o-mini for extraction and o1 for reasoning as an emerging architectural best practice (broad production).
- **Process-level RL on CoT traces** — training on intermediate reasoning steps rather than only final outcomes (broad production). See [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

### Limitations and Open Questions

**Latency** (significant, improving): o1 inference is substantially slower than standard LLMs. Diode cached pre-generated system diagrams as a workaround. This blocks deployment in real-time interactive applications.

**Opacity and non-steerability** (significant, improving): o1's internal reasoning chain cannot be edited or redirected mid-generation. It is a deterministic black box from the user's perspective. The next unlock identified explicitly is the ability to edit each step of the chain of thought — enabling human-in-the-loop refinement and adversarial step-level training.

**Residual errors on hard cases** (significant, improving): Even at 85% accuracy on difficult cases, 15% still require human intervention. CAD designs require fine-tuning adjustments. The system does not eliminate expert review.

**Ground truth dependency** (significant, stable): o1's [[themes/reinforcement_learning|RL]] training requires verifiable ground truth. Tasks with ambiguous success criteria — open-ended customer support, subjective judgment calls — cannot benefit from the same training regime. Rules-based systems remain more reliable where objective criteria don't exist.

**Replication cost** (significant, stable): The proprietary CoT dataset was expensive to build and is not publicly available. The capability gains are partially locked behind training investments that competitors cannot easily replicate.

**GPT-4 hard failure** (blocking, improving): The complete failure of GPT-4o on tasks where o1 succeeds reveals an architectural ceiling — no amount of prompting or fine-tuning of transformer-only models without CoT training closes the gap. This is framed as evidence that reasoning is a qualitatively different capability, not a quantitative improvement.

### Bottlenecks Identified

| Bottleneck | Horizon |
|---|---|
| Latency of reasoning models in interactive applications | 1–2 years |
| Human-in-the-loop reasoning optimization / step-level editing | Months |
| Domain-specific evaluation data scarcity | 1–2 years |
| Ambiguous task ground truth for open-ended reasoning | 1–2 years |

### Breakthroughs

- **Step-function capability jump**: o1 enables previously impossible engineering tasks. The GPT-4o → o1 transition is not incremental. See [[themes/test_time_compute_scaling|test-time compute scaling]].
- **Test-time compute as orthogonal scaling axis**: Inference-time reasoning provides comparable gains to training-time scaling, with different cost/benefit trade-offs.
- **Process-level reward models on CoT**: Intermediate supervision enables step-by-step optimization and fine-grained credit assignment for multi-step reasoning.
- **Proprietary eval data as moat**: The competitive advantage in AI products is shifting from model capability to data access and curation quality. Teams with proprietary domain-specific test cases and workflows can build best-in-class versions; others cannot.

---

## Strategic and Investment Context

The source was recorded in the context of a YC hackathon of funded startups building real product features — not toy demos. This grounds the capability claims in commercial deployment rather than benchmark performance.

The investment thesis implied: the companies with durable advantages are those with proprietary evaluation datasets and domain-specific workflows not available online. The model itself is commoditizing; the moat is in the data that makes domain-specific fine-tuning and evaluation possible. See [[themes/startup_formation_and_gtm|startup formation and GTM]] for implications.

Sam Altman's compute ambition — scaling spend by four orders of magnitude to roughly one trillion dollars — frames the long arc: both pretraining scaling (GPT-5 series) and test-time compute scaling ([[themes/rl_for_llm_reasoning|RL for LLM reasoning]]) are being pursued in parallel. The source argues that o1-style reasoning advances may arrive faster and with more immediate commercial impact than the next pretraining step-up.

---

## Open Questions

- At what point does test-time compute scaling hit diminishing returns, and how does that horizon compare to pretraining scaling?
- Can process reward models be trained effectively on tasks without verifiable ground truth, or is the ambiguous-task limitation fundamental?
- As o1's chain-of-thought editing becomes possible, what new training data and adversarial refinement loops become accessible?
- How far does the circuit design and CAD capability generalize — does it transfer to novel hardware architectures, or is it still pattern-matching over seen design spaces?
- Will the proprietary eval data moat widen (incumbents accelerate) or narrow (synthetic data generation catches up)?

---

## Related Themes

- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]

## Key Concepts

- [[entities/scaling-laws|Scaling Laws]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
