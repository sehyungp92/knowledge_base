---
type: source
title: 29.4% ARC-AGI-2 🤯 (TOP SCORE!) - Jeremy Berman
source_id: 01KJVDK1KQBWP92KBFJF97NG36
source_type: video
authors: []
published_at: '2025-09-27 00:00:00'
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- model_architecture
- reasoning_and_planning
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# 29.4% ARC-AGI-2 (TOP SCORE!) - Jeremy Berman

Jeremy Berman details his top-scoring approach to ARC-AGI-2, tracing the evolution from Python-based iterative program synthesis to natural language algorithm description with evolutionary refinement — revealing why expressivity beats precision when benchmarks outpace what code can cleanly capture, and surfacing deep structural limitations in how current models reason.

**Authors:** Jeremy Berman
**Published:** 2025-09-27
**Type:** video

---

## The ARC Challenge and What Makes v2 Different

The ARC benchmark functions as an IQ test for machines: given a few input-output grid pairs sharing a common transformation rule, infer the rule and apply it to a novel test grid. Humans average ~75% accuracy on ARC v1; at launch, frontier models like GPT-4 and Claude Sonnet 3.5 scored ~5%. ARC v2 raises the difficulty substantially — its tasks are **compositional**, requiring multiple transformation rules applied in sequence, making them far harder to capture in deterministic code.

The top score on the ARC v2 public leaderboard sits at approximately 30%, meaning the benchmark remains largely unsolved despite representing tasks trivially easy for humans.

---

## From Python Programs to Natural Language

### The v1 Approach

Berman's starting point was inspired by Ryan Greenblatt's method: generate Python programs encoding the transformation rule, verify them against training examples, and iteratively refine failures. The key insight was a **revision loop** — feeding Sonnet 3.5 the specific cells it got wrong and asking it to improve its program, repeated up to ten times or until accuracy thresholds were met. This worked well for v1 tasks, costing roughly $8 per task compared to OpenAI's o3 approach of ~$200 per task (likely pure sampling without specialized search).

### Why Python Broke Down on v2

Python programs are **brittle** for ARC v2. The grid transformations in v2 are compositional in ways that resist clean algorithmic expression — the overwhelming majority are very hard to describe concisely in code. The deeper issue is theoretical: Python occupies a narrow region of program space, whereas the task distribution of v2 sprawls beyond it.

The realization that led to the switch: every single ARC v2 task can be fully described in **10 bullet points of plain English**, most in 5. This is not just a pragmatic observation — it may reflect something true about how humans solve these tasks, mentally composing natural language rules and checking them against examples.

> *"In some ways, this actually gets to the heart of ARC; everything is quite simple. This may also be how we do it too."*

### The Natural Language Architecture

The v2 solution generates **natural language descriptions of algorithms** rather than code, and refines them evolutionarily — keeping high-performing descriptions, discarding weak ones, and iterating. This exploits two properties of language models:

1. **Inductive bias**: LLMs are trained inductively on natural language, developing priors that express themselves most fully in that medium. Switching to natural language lets this bias operate without constraint.
2. **Expressivity**: Natural language covers more of the solution space. There are more degrees of freedom, meaning the search can reach solutions that Python would never find.

The trade-off is **verifiability**. Python programs can be run; natural language descriptions cannot. Checking whether a natural language description correctly transforms a grid requires the model itself to simulate execution — inductively, per training example, at the cost of multiple inference calls. This made the checker the bottleneck: it needed to be stronger than the instruction generator.

---

## Depth vs. Breadth: The Shifting Trade-off

For v1 tasks, depth — many revision iterations on a small set of candidates — was productive. For v2, **breadth dominates**: generating a wide diversity of candidate descriptions outperforms deep refinement of fewer candidates.

The reason is structural: modern [[themes/reasoning_and_planning|reasoning models]] trained with RL have **in-built revision loops**. The deep step-by-step refinement that previously required external scaffolding now happens inside the model's thinking block. An external revision loop adds diminishing value on top of this; increasing entropy and exploring the space broadly is more efficient.

This means the optimal architecture has shifted:

| ARC v1 | ARC v2 |
|--------|--------|
| Narrow breadth, deep revision loop | Wide breadth, shallow external loop |
| Python programs (deterministic, verifiable) | Natural language descriptions (expressive, inductive) |
| Revision loop compensates for weak thinking | Thinking model handles deep revision internally |
| ~$8/task | ~$30/task |

---

## Model Choice and Domain Spikiness

A significant finding is that model capabilities are **extremely domain-specific** ("spiky"). No single model generalizes equally across reasoning problem types. For ARC v1 — which required generating and reasoning about Python code — Sonnet 3.5's code-generation strengths made it the right choice. For natural language-based v2 approaches, models with different training distributions may hold advantages (Grok was noted as potentially having special capability from similar shape-task exposure).

This has a practical implication: architectural choice is benchmark-dependent in non-obvious ways, and the strongest general model is not always the strongest for a specific task distribution.

---

## Landscape Contributions

### Capabilities

- **Evolutionary NL refinement for abstract reasoning**: Generating natural language algorithm descriptions and iteratively refining them with verifiable feedback achieves state-of-the-art on ARC v2 (29.4%, top leaderboard). [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] · maturity: *narrow production*

- **RL reasoning models with emergent revision loops**: [[themes/chain_of_thought|chain-of-thought]] reasoning models trained with RL internalize iterative refinement, performing deep autonomous reasoning without external scaffolding. maturity: *broad production*

- **10x cost efficiency over sampling baselines**: Structured evolutionary search reduces ARC solution cost from ~$200/task (o3 sampling) to ~$30/task. maturity: *narrow production*

### Limitations

- **No synthesis outside training distribution** (severity: blocking): Models can only retrieve and recombine memorized patterns. They cannot think outside the box of their pretraining data. [[themes/representation_learning|Representation Learning]]

- **Lack of grounded world understanding** (severity: significant): Models operate on statistical patterns without deep causal or abstract understanding comparable to human cognition, requiring human supervision for non-trivial generalization.

- **Catastrophic forgetting under fine-tuning** (severity: blocking, trajectory: improving): Weight updates for new tasks degrade prior performance. Fine-tuning is expensive precisely because continual learning remains unsolved.

- **SGD finds shortcuts, not Turing-complete structures** (severity: significant, trajectory: unclear): Gradient descent reliably finds good-hearting shortcuts rather than general symbolic reasoning circuits. [[themes/model_architecture|Model Architecture]]

- **Fragmented domain-specific reasoning circuits** (severity: significant): Models do math-thinking and code-thinking, but these are separate circuits without a unified reasoning substrate. Cross-domain transfer remains weak.

- **Natural language outputs are high-entropy and unverifiable** (severity: significant, trajectory: stable): The expressivity advantage of natural language comes with an irreducible verifiability cost — outputs cannot be executed, only inductively checked.

- **No circuitry of invention** (severity: blocking): Models lack the capacity to generate genuinely novel hypotheses outside their training distribution, blocking scientific discovery applications.

### Bottlenecks

| Bottleneck | Blocks | Horizon |
|-----------|--------|---------|
| No out-of-distribution synthesis | Novel scientific discovery, creative reasoning | 3–5 years |
| Catastrophic forgetting | Continual learning, multi-task fine-tuning | 1–2 years |
| SGD shortcut bias | General symbolic reasoning, Turing-complete induction | 5+ years |
| No grounded world model | Fully autonomous reasoning, causal understanding | 3–5 years |
| Fragmented reasoning circuits | Cross-domain transfer, unified reasoning | 3–5 years |

### Breakthroughs

- **Emergent in-built revision loops** (significance: major): RL training produces models that iterate internally, eliminating the need for external scaffolding to achieve deep reasoning. This retroactively explains why v1-style revision loops worked — they were emulating what RL training now does natively.

- **Natural language beats code for expressive reasoning** (significance: major): Switching from Python to English as the program representation achieves higher coverage of the ARC v2 solution space, demonstrating a general principle about representation medium and search efficiency.

- **10-20x cost reduction via structured search** (significance: notable): Algorithmic efficiency, not raw compute, accounts for the gap between $200/task sampling and $30/task evolutionary refinement.

---

## Open Questions

**Verification as the bottleneck.** The checker needed to be stronger than the generator — meaning the hard part of natural language programs is not writing them but validating them. What does this imply for program synthesis at scale? Is there a hybrid representation (natural language + lightweight formal constraints) that captures expressivity while recovering some verifiability?

**Library transfer.** Berman notes a version that saved traces from training and reused them at test time improved efficiency. This is analogous to in-context few-shot library construction. How far does this generalize, and does it interact with the catastrophic forgetting bottleneck?

**What does 30% mean?** The top score on a benchmark "easy for humans" remaining at 30% with frontier models and specialized search suggests something structurally difficult. Is the gap explained by the compositional nature of v2 tasks, by training distribution gaps, or by a deeper architectural limitation?

**The spikiness problem.** If capabilities are highly domain-specific, does scaling smooth them out or does spikiness persist? The observation that different models may have "special capability" in narrow domains due to training distribution suggests the latter — with implications for how we should think about general reasoning progress.

---

## Themes

- [[themes/benchmark_design|Benchmark Design]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/representation_learning|Representation Learning]]

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
