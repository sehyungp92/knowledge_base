---
type: source
title: Investing in AI for Hard Tech, with Eric Vishria of Benchmark and Sergiy Nesterenko
  of Quilter
source_id: 01KJVRC3JX821XQE4V2NJEHFN1
source_type: video
authors: []
published_at: '2024-06-12 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- reasoning_and_planning
- scientific_and_medical_ai
- search_and_tree_reasoning
- startup_and_investment
- startup_formation_and_gtm
- vc_and_startup_ecosystem
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Investing in AI for Hard Tech, with Eric Vishria of Benchmark and Sergiy Nesterenko of Quilter

This source examines why reinforcement learning — not generative AI — is the right approach for autonomous circuit board design, using Quilter as a case study in applying domain-specific AI to physical engineering problems. It also surfaces a broader investment thesis: that vertical hard-tech AI applications may generate faster and more durable returns than foundation model companies.

**Authors:** Eric Vishria (Benchmark), Sergiy Nesterenko (Quilter)
**Published:** 2024-06-12
**Type:** Video — [YouTube](https://www.youtube.com/watch?v=64iPS9AXrcc)

---

## Why Circuit Board Layout Is an AI Problem — Not a Copilot Problem

The conventional response to a complex knowledge-work problem is to build a copilot: keep the human in the loop, automate the easy parts, let the expert handle the rest. Quilter's founding insight is that circuit board layout is structurally incompatible with this model.

If a co-pilot successfully handles 90% of a board layout, the remaining 10% involves routing thin traces across an already-dense board without violating any of the constraints already established. A human cannot meaningfully perform this task — the interdependencies are too fine-grained, the error surface too large. The conclusion is that layout must be done entirely by AI, or not at all. There is no stable intermediate.

This sets up the core product framing: a compiler for electronics. Users specify their optimization target — cost, performance, power density, board size — and the system returns a range of valid solutions. The human makes architectural decisions; the AI handles physical instantiation.

The market context reinforces the opportunity. Electronics now permeate product categories that were purely mechanical a decade ago. The number of companies needing PCB design has expanded far faster than the supply of skilled layout engineers. SpaceX, despite having an internal board design team, could not serve demand from other internal teams — a signal of how broadly underserved this market is.

---

## Why Reinforcement Learning, Not LLMs

The data situation makes supervised learning untenable on two grounds.

First, there is almost no usable open-source circuit board data. The best designs are proprietary — locked inside Apple, Google, and similar companies. Even the open-source boards that exist are largely unreliable: approximately three out of four boards submitted to manufacturers are manufacturable in a physical sense but fail because the underlying physics does not work. The manufacturer receives a mask set showing copper etching patterns and component placement — not the signal flow or electromagnetic behavior needed to validate correctness. Any training dataset assembled from historical boards would be majority-corrupted, and cleaning it requires running physics simulations anyway.

Second, even with clean, complete data, supervised learning would produce roughly human-level performance. If the model learns to predict what humans would design, it learns the distribution of human decisions — including all the systematic errors that make human board design slow, expensive, and suboptimal.

Reinforcement learning sidesteps both problems. The reward signal comes from physics simulation, not human judgment. Humans are poor at evaluating whether a board will work; Maxwell's equations are not. This makes the reward signal unusually reliable compared to RLHF in language models, where sycophancy and reward hacking are known failure modes. The RL approach also creates a path to superhuman performance — optimizing against physics directly, rather than approximating what humans would do.

The user-facing interface exposes the optimization objective as a control surface: dense and expensive vs. cheap and large, performance vs. power efficiency. The AI searches the Pareto frontier; the engineer chooses a point on it.

---

## The Sparse Reward Problem and How Quilter Addresses It

The central technical challenge in applying RL to circuit board design is reward sparsity. A complete board design is validated by physics simulation at the end of the process. If the final reward (does this board work?) is the only signal, the agent must explore randomly through an enormous space before ever finding a positive example — and may never find one at all.

Quilter's approach is hierarchical reward shaping: decompose the design process into stages, and define dense intermediate rewards that correlate with the ultimate sparse reward.

- **Placement stage**: components are positioned; reward checks manufacturability, collision avoidance, and heuristic signals about routing feasibility.
- **Routing stage**: traces are laid; reward checks connectivity and approximate signal integrity constraints.
- **Validation**: approximated physics models (conservative quasi-static solvers) are used for continuous feedback; full-wave Maxwell solvers are reserved for final validation runs.

The physics approximations are deliberately conservative: they sacrifice some theoretical optimality to ensure that anything passing the approximation check will also pass full simulation. This allows the agent to learn against a reliable but computationally tractable signal.

The long-term goal is to collapse this into a single end-to-end sparse reward function — the agent winning only when the full physics check passes. That would enable performance to substantially exceed human capability, but it requires solving the sparse reward problem at scale.

**Open constraints:**
- Full-wave simulation (FDTD/FEM) for high-speed digital and RF designs takes approximately 20 minutes per evaluation. Millions of evaluations per training run make this computationally prohibitive at current scales.
- The team estimates that small boards are 3–5 years from superhuman performance; motherboard-class designs are 5+ years out, with high uncertainty.

---

## Capability and Limitation Profile

### What Quilter Can Do Now

- Autonomous layout and routing for low-complexity boards (low-speed digital, up to 4A current), optimizing against user-specified objectives
- Physics-validated outputs using conservative approximations of Maxwell equations — manufacturable and reliably functional
- Multi-objective optimization exposing cost/performance/density tradeoffs as a user-controlled parameter

### What It Cannot Yet Do

- **Complex boards**: high-speed digital, mixed-signal, RF, and high-power designs require expensive full-wave solvers that are computationally infeasible at current training scale
- **Data reuse**: historical board repositories are largely unusable without physics validation — the corruption rate is too high
- **Short-horizon training**: the sparse reward problem remains partially unsolved; intermediate reward shaping is hand-crafted from domain heuristics, not learned end-to-end

### Talent as a Hard Constraint

The bottleneck Quilter identifies as most binding is not compute or data — it is personnel. The problem requires simultaneous expertise across neural networks, cutting-edge RL, systems programming (C++/CUDA), and electromagnetics. This combination is rare enough that it constitutes a structural constraint on development speed.

---

## The Generative AI Boundary

A recurring theme in this conversation is a distinction between interpolation and extrapolation. Generative models — LLMs, diffusion models — are characterized as sophisticated interpolators: they produce outputs within the convex hull of their training data, synthesizing and recombining what humans have already created.

This is genuinely powerful for many tasks. It is structurally limited for circuit board design for two reasons: the training data is corrupted and sparse (as above), and the performance ceiling is roughly human-level by construction — the model can only learn to approximate what humans have done.

Reinforcement learning against physics is the alternative: it can discover solutions that no human has designed, optimize against constraints humans cannot track manually, and improve beyond the human performance frontier. The claim is that for problems where (a) the reward signal is grounded in computable physics and (b) the design space substantially exceeds human cognitive reach, RL offers a qualitatively different capability profile than generative approaches.

This maps to a broader observation about where generative AI has structural limits: any domain where the best known solutions are produced by humans and the evaluation signal is noisy human preference will tend to cap generative model performance near the human distribution.

---

## Investment Thesis: Vertical AI vs. Foundation Models

[[entities/benchmark|Benchmark]] has not invested in any foundation model company. The stated reasoning is that foundation models combine two unfavorable properties:

1. **Extreme capital intensity**: training runs cost hundreds of millions of dollars.
2. **Rapid depreciation**: a model built for $150M becomes reproducible for $5M within six months. The assets created are among the most rapidly depreciating in venture capital history.

The defensibility question for foundation model companies is therefore structural: if the model itself is a commodity within 6–12 months, value must accrue elsewhere (distribution, data, workflow integration). The investment calculus is difficult.

By contrast, vertical AI applications — Quilter being the example — are characterized by:

- Domain-specific data that cannot be easily replicated (proprietary board designs, physics simulation outputs)
- Reward signals that don't depend on human preference (physics is the judge)
- A performance ceiling that is superhuman, not human-level
- A market where the problem is genuinely unsolved (not just underserved by software)

The observation that vertical AI companies have shown faster revenue traction than infrastructure or foundation model plays is noted as a data point that challenges the assumption that general-purpose AI captures the most value in the current wave.

---

## Connections

- [[themes/startup_and_investment|Startup & Investment]] — The Benchmark investment framework (what's changing in the world, idea maze, founder profile) and the foundation model depreciation thesis
- [[themes/vc_and_startup_ecosystem|VC & Startup Ecosystem]] — Vertical AI vs. foundation model returns; the "sugar high" framing for early revenue traction
- [[themes/startup_formation_and_gtm|Startup Formation & GTM]] — Disruptive entry at the low end of the PCB market, expanding the bottom of the market
- [[themes/reasoning_and_planning|Reasoning & Planning]] — Hierarchical reward shaping for long-horizon planning tasks; sparse vs. dense reward structures
- [[themes/search_and_tree_reasoning|Search & Tree Reasoning]] — RL-based search through design space; physics-grounded evaluation
- [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]] — Physics simulation as a reliable oracle; RL outperforming human design in constrained optimization
- [[themes/scientific_and_medical_ai|Scientific & Medical AI]] — Generalization of the physics-grounded reward signal pattern to other hard-science domains

---

## Open Questions

- At what complexity threshold does the physics simulation cost become prohibitive, and what approximation schemes are viable at that boundary?
- Can the intermediate reward shaping be learned rather than hand-crafted — and if so, what does the sample efficiency look like?
- Does the interpolation/extrapolation distinction hold as a general claim about generative models, or is it specific to domains where training data is corrupted or sparse?
- How much of the vertical AI revenue traction is durable vs. early adopter enthusiasm — and what metrics distinguish the two?
- If foundation model costs continue to drop exponentially, does the vertical AI thesis strengthen (cheaper substrate) or weaken (less differentiation from fine-tuning)?

## Key Concepts

- [[entities/benchmark|Benchmark]]
- [[entities/diffusion-model|Diffusion Model]]
- [[entities/foundation-model|Foundation Model]]
- [[entities/github-copilot|GitHub Copilot]]
- [[entities/idea-maze|Idea Maze]]
- [[entities/reinforcement-learning|Reinforcement Learning]]
- [[entities/supervised-learning|Supervised Learning]]
