---
type: source
title: ⚡️Math Olympiad gold medalist explains OpenAI and Google DeepMind IMO Gold
  Performances
source_id: 01KJVJ6D0CCF5T2WR30GJ4N3ZC
source_type: video
authors: []
published_at: '2025-07-24 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- ai_market_dynamics
- benchmark_design
- compute_and_hardware
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- reasoning_and_planning
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Math Olympiad Gold Medalist Explains OpenAI and Google DeepMind IMO Gold Performances

> A math olympiad gold medalist analyzes the 2025 IMO results where both DeepMind and OpenAI independently achieved gold medal performance using natural language reasoning — without formal verification tools — contextualizing what this means for AI's mathematical maturity, where the hard limits remain, and what a more rigorous benchmark for mathematical AI would actually look like.

**Authors:** (unnamed IMO gold medalist)
**Published:** 2025-07-24
**Type:** video

---

## What Happened at IMO 2025

Both DeepMind (Gemini) and [[entities/openai|OpenAI]] independently achieved gold medal-level performance at IMO 2025 using models that reason entirely in natural language — no internet access, no external tools, no formal verification languages. DeepMind's result was officially verified and submitted to IMO; OpenAI's was not officially submitted but was reviewed and validated by three former IMO medalists.

This marks a decisive shift from 2024, when DeepMind's AlphaProof/AlphaGeometry system required a human to first translate natural language problem statements into Lean before the AI could engage with them — and even then, some solutions took 60 hours or more, far exceeding the 4.5-hour limit for human competitors.

In 2025, Lean is gone entirely. The wall clock time dropped from ~60 hours to under 400 seconds — an order-of-magnitude improvement that the author argues cannot be explained by hardware scaling alone and reflects a qualitative change in how these models reason.

A second Gemini model was also submitted with no in-context learning (no curated example solutions provided), achieving the same gold-medal result — countering claims that the model had simply memorized or been primed with competition-style solutions.

---

## How the Models Work

DeepMind's system uses **parallel thinking**: the model runs multiple solution paths simultaneously, then a judge model selects the best result. This is paired with new [[themes/reasoning_and_planning|reinforcement learning techniques]] specifically developed to leverage multi-step reasoning — an area where LLMs have historically struggled. Training explicitly for multi-step processes, combined with RL that exploits this structure, is what the author identifies as the core technical advance.

The broader pattern, however, is continuity rather than revolution: most underlying ideas are not new. What changed is systematic application, scale of compute, and data availability.

---

## What the IMO Does and Does Not Test

The author is careful to contextualize what this milestone actually demonstrates. IMO problems do not require deep knowledge of advanced mathematics — they reward:
- Sharp observation and pattern recognition
- Techniques like contradiction and counterexample
- Logical persistence and rigor

What IMO problems do **not** test:
- Research creativity and conjecture generation
- Ability to learn and apply new advanced concepts
- Abstraction, generalization, or cross-domain transfer
- The capacity to invent new methods or identify non-obvious structural relationships

The IMO is, in the author's framing, "one stepping stone" — a test of problem-solving ability, not mathematical maturity.

---

## The Remaining Hard Limit: Problem 6

No AI system solved IMO 2025 Problem 6 — the hardest problem on the paper, and one that required **combinatorial creativity**: constructing novel examples, exploring a solution space experimentally, and proving that constructed examples represent minimal or extremal bounds. This is precisely the class of problem where AI currently fails: not step-by-step textbook derivations, but hypothesis-driven exploration where there is no clear path and the solver must invent the path itself.

This is not merely a capability gap — it points to a **structural bottleneck** in how current models reason. AI systems perform well when a problem decomposes into sequential steps with verifiable intermediate states. They struggle when the problem requires:
- Generating and evaluating novel conjectures
- Running "experiments" on small examples to build intuition
- Inferring general structure from sparse data

See [[themes/mathematical_and_formal_reasoning|mathematical and formal reasoning]] and [[themes/reasoning_and_planning|reasoning and planning]] for related landscape context.

---

## The Benchmark Problem

Current AI math benchmarks — AMC, AMY, IMO, USA competition math — assess only a narrow slice of what professional mathematicians actually do. The author proposes a richer decomposition of mathematical skill into three broad categories:

**1. Mathematical knowledge and understanding**
Knowing definitions, theorems, and lemmas; understanding why they are true; fluency in calculation and analytical technique; connecting theory to application.

**2. Problem-solving and communication**
Navigating problems via contradiction, decomposition, analogy, and logical reasoning. Equally, structuring arguments clearly and communicating proofs in ways others can follow.

**3. Learning, meta-skills, and creativity**
This is what separates problem-solvers from mathematicians: learning new knowledge, abstracting across domains (e.g., probabilistic methods in combinatorics), translating real-world scenarios into formal models, generalizing from examples to theorems. At the highest level: inventing new methods, seeing non-obvious relationships, generating genuinely novel ideas.

Current benchmarks capture category 2. They largely ignore categories 1 and 3. A more holistic benchmark would need to be co-designed by mathematicians and AI researchers — neither group alone has the full picture.

See [[themes/evaluation_and_benchmarks|evaluation and benchmarks]] and [[themes/benchmark_design|benchmark design]].

---

## Paths Forward

**Logical reasoning and formal verification:** The most tractable near-term path. Lean (and other proof assistants) can serve as a verifier, giving RL a clear correctness signal. The bottleneck is data: current Lean corpora contain roughly 1 million tokens; estimates suggest ~1 trillion tokens would be needed for effective training. Scaling this corpus is an active effort among mathematicians (notably Kevin Buzzard and collaborators), but it is multi-year work.

**Creativity:** Much harder. There is currently no reward function that can capture originality or the quality of a conjecture. Defining such a function requires deep domain knowledge — and building it requires collaboration between mathematicians who understand what makes creativity mathematically valuable and AI researchers who can translate that into training objectives. This collaboration is nascent but increasing.

---

## Landscape Contributions

### Capabilities
- IMO gold medal performance via natural language reasoning, without formal languages or internet access ([[themes/mathematical_and_formal_reasoning|mathematical and formal reasoning]], maturity: *narrow_production*)
- Parallel multi-step reasoning: exploring multiple solution paths simultaneously with a judge model selecting best results ([[themes/reasoning_and_planning|reasoning and planning]], maturity: *demo*)
- Order-of-magnitude improvement in inference speed for olympiad-level math (~60 hours → ~400 seconds)

### Limitations
- **Creative combinatorics remains blocked:** AI cannot solve problems requiring novel example construction and extremal reasoning (severity: *blocking*)
- **No verifiable conjecture generation:** No reward function exists for evaluating mathematical creativity; training for this is currently undefined (severity: *blocking*)
- **Lean data scarcity:** ~1M tokens available vs. ~1T tokens estimated as needed for effective formal math training (severity: *significant*)
- **Natural language proof verification:** Without formal languages, solution checking requires expert human review rather than automated verification (severity: *significant*)
- **Benchmark coverage gap:** Existing benchmarks assess problem-solving only; research creativity and knowledge application are unmeasured (severity: *significant*)

### Breakthroughs
- Elimination of the Lean translation requirement for olympiad-level AI math (significance: *major*) — see [[themes/mathematical_and_formal_reasoning|mathematical and formal reasoning]]
- Independent gold medal achievement by two separate labs using different approaches (significance: *notable*)
- Wall clock time reduction from 60 hours to under 400 seconds — likely reflecting qualitative reasoning improvements beyond hardware scaling (significance: *major*)

---

## Open Questions

- What does a rigorous, holistic benchmark for mathematical AI actually look like, and who is positioned to build it?
- Is the wall clock improvement purely a reasoning advance, or partially an artifact of problem selection / difficulty distribution at IMO 2025?
- How quickly can Lean corpora be scaled, and does the formal/informal trade-off fundamentally limit one path over the other?
- Can creativity in mathematics ever be captured by a reward function, or does it require a fundamentally different training paradigm?

---

*Themes: [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]] · [[themes/reasoning_and_planning|Reasoning and Planning]] · [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]] · [[themes/benchmark_design|Benchmark Design]] · [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]] · [[themes/compute_and_hardware|Compute and Hardware]] · [[themes/ai_market_dynamics|AI Market Dynamics]]*

## Key Concepts

- [[entities/alphaproof|AlphaProof]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
