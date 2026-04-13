---
type: source
title: 'AlphaEvolve: A coding agent for scientific and'
source_id: 01KKT490MT6VD9NZN7SB085KZF
source_type: paper
authors: []
published_at: '2025-06-17 00:00:00'
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- mathematical_and_formal_reasoning
- reasoning_and_planning
- scientific_and_medical_ai
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AlphaEvolve: A coding agent for scientific and

**Authors:** 
**Published:** 2025-06-17 00:00:00
**Type:** paper

## Analysis

# AlphaEvolve: A coding agent for scientific and algorithmic discovery
2025-06-17 · paper
https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf

---

### Motivation & Prior Limitations
LLM-based pipelines had not reliably produced entirely new scientific or practical discoveries, despite strong benchmark performance and hypothesis-generation capabilities, because they lacked a grounded feedback mechanism capable of sustaining iterative improvement over many generations without accumulating hallucinations.
- Prior LLM-guided evolution systems like FunSearch were severely constrained in scope: they evolved only a single Python function of 10–20 lines, required fast evaluation (≤20 min on 1 CPU), used relatively small code-only LLMs, provided minimal prompt context, and optimized a single scalar metric, limiting them to narrow problem classes.
- Specialized algorithmic discovery systems such as AlphaTensor (deep RL for matrix multiplication) required heavy domain-specific engineering and could not generalize across problem types, while classical evolutionary/genetic programming required handwritten mutation operators that are hard to design and fail to capture domain nuance.
- For 56 years after Strassen (1969), no algorithm had been found to multiply two 4×4 complex-valued matrices using fewer than 49 scalar multiplications over any characteristic-0 field, illustrating the difficulty of the open problems AlphaEvolve targets.

---

### Proposed Approach
AlphaEvolve is an LLM-driven evolutionary coding agent that iteratively proposes, evaluates, and selects modifications to entire codebases (not just single functions) using automated execution feedback as the grounding signal, enabling it to evolve complex, multi-component algorithms across any programming language.
- The core loop samples a parent program and inspiration programs from an evolutionary database, assembles a rich prompt (including prior solutions with scores, problem context, literature, meta-prompt instructions), queries an ensemble of Gemini 2.0 Flash and Gemini 2.0 Pro to produce code diffs in a structured SEARCH/REPLACE format, applies those diffs to create a child program, evaluates the child automatically, and re-inserts it into the database — all asynchronously and at scale.
- The evolutionary database balances exploration and exploitation using an algorithm combining MAP-Elites and island-based population models, enabling diversity maintenance alongside hill-climbing on the best known solutions.
- Three critical design choices distinguish AlphaEvolve from FunSearch: (1) full-file evolution across entire codebases in any language rather than a single Python function; (2) multi-objective optimization, where optimizing auxiliary metrics improves single-target performance by inducing structural diversity in the program pool; (3) frontier LLMs (Gemini 2.0 Pro + Flash ensemble) with rich natural-language context, meta-prompt evolution, and evaluation cascade for efficient pruning of poor solutions.
- A key methodological innovation for mathematical problems is evolving heuristic search algorithms rather than solutions directly — each evolved heuristic is given a fixed time budget and the current best construction and tasked with finding something better, yielding multi-stage, adaptive search strategies that are difficult to replicate manually.
- Users interact through a minimal API: annotating evolution blocks with `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` comments in an existing codebase and providing an `evaluate` function returning a dictionary of scalar scores.

---

### Results & Capabilities
AlphaEvolve improved the state of the art for 14 matrix multiplication tensor decompositions, including the first-ever rank-48 algorithm for 4×4 complex-valued matrix multiplication, breaking a 56-year-old open problem; for all m,n,p ≤ 5 targets, it matched or surpassed the best known solutions.
- For open mathematical construction problems across analysis, combinatorics, number theory, and geometry (50+ problems), AlphaEvolve rediscovered the best known construction in ~75% of cases and surpassed the state of the art in ~20% of cases, including a new upper bound on Erdős's minimum overlap problem and a kissing number configuration of 593 spheres in 11 dimensions (previous record: 592).
- Applied to Google's Borg data center scheduler, AlphaEvolve discovered a simple, interpretable heuristic function that recovers an average of 0.7% of fleet-wide compute resources continuously after deployment — outperforming both the production heuristic and a deep reinforcement learning alternative, while also being easier to debug and certify.
- For Gemini's matrix multiplication Pallas kernel tiling heuristic, AlphaEvolve achieved a 23% average kernel speedup over the expert-designed heuristic and a 1% reduction in overall Gemini training time, while reducing kernel optimization time from several months to days.
- AlphaEvolve optimized compiler-generated XLA intermediate representations for FlashAttention: a 32% speedup of the attention kernel itself and a 15% speedup in pre/postprocessing, demonstrating the ability to edit code never intended for human editing.
- For TPU RTL circuit design in Verilog, AlphaEvolve found a functionally equivalent simplification that reduced area and power, validated by TPU designers; notably, the result was expressed directly in Verilog, enabling engineer trust and adoption.
- Ablations confirm that every major component contributes materially: removing evolution, context in prompts, meta-prompt evolution, full-file evolution, or the powerful LLM each causes significant performance degradation on both the matrix multiplication and kissing number tasks.
- AlphaEvolve acts as a test-time compute scaling agent: its evolutionary procedure substantially amplifies base LLM capability beyond what repeated sampling 

## Key Claims

1. AlphaEvolve discovered an algorithm using 48 scalar multiplications to multiply two 4×4 complex-valued matrices, the first improvement over Strassen's algorithm in this setting after 56 years.
2. AlphaEvolve improved the state of the art for 14 different matrix multiplication targets.
3. On over 50 open mathematical problems, AlphaEvolve matched the best known constructions on approximately 75% of cases and surpassed the state of the art on approximately 20% of cases.
4. AlphaEvolve's scheduling heuristic continuously recovers on average 0.7% of Google's fleet-wide compute resources that would otherwise be stranded.
5. AlphaEvolve discovered a tiling heuristic that yields an average 23% kernel speedup over expert-designed heuristics and a 1% reduction in Gemini's overall training time.
6. AlphaEvolve reduced kernel optimization time from several months of dedicated engineering effort to just days of automated experimentation.
7. AlphaEvolve sped up the FlashAttention kernel by 32% and achieved a 15% speedup in pre- and postprocessing by optimizing compiler-generated XLA intermediate representations.
8. AlphaEvolve improved the kissing number lower bound in 11 dimensions from 592 to 593.
9. AlphaEvolve is a substantial enhancement of FunSearch, evolving entire code files of hundreds of lines in any language, whereas FunSearch evolved single functions of 10-20 lines only in Python.
10. AlphaEvolve requires automated evaluation metrics, making tasks requiring manual experimentation outside its scope.

## Capabilities

- LLM-guided evolutionary coding agent discovers provably correct algorithms that surpass decades-old state-of-the-art mathematical results, including improving Strassen's 4x4 matrix multiplication after 56 years and surpassing SOTA on 20% of 50+ open mathematical problems
- Evolutionary coding agent discovers and deploys production-grade infrastructure optimizations autonomously: 0.7% Google fleet-wide compute recovery from scheduling heuristics, 23% kernel speedup for Gemini training, 32% FlashAttention kernel speedup
- AI coding agent evolves entire multi-function, multi-language codebases of hundreds of lines (vs prior systems limited to single functions of 10-20 lines), enabling substantially more complex algorithmic discovery
- AI agent can directly optimize compiler-generated intermediate representations (IRs) of production ML kernels, despite IRs being designed for debugging not editing — achieving 32% speedup on FlashAttention and 15% on pre/postprocessing
- AI system accelerates its own training infrastructure: AlphaEvolve discovered a tiling heuristic that reduces Gemini's overall training time by 1%, creating an early self-improvement feedback loop
- Test-time compute scaling via evolutionary search with LLM mutation sustains meaningful capability gains well beyond what repeated sampling achieves, reaching regimes of genuine scientific discovery
- LLM-guided evolution reduces expert kernel engineering time from months to days for hardware-accelerator tiling heuristic design, with discovered heuristic outperforming the expert-designed baseline by 23%
- Evolutionary coding agent applies to hardware RTL design, finding simplifications in Verilog circuit implementations of TPU arithmetic units that pass formal verification

## Limitations

- AlphaEvolve is fundamentally limited to problems with automated evaluation metrics — it cannot address domains where experiments require physical execution, manual judgment, or cannot be simulated
- Self-improvement feedback loops are on the order of months, not hours or days — gains from AlphaEvolve-discovered optimizations feeding back into next-generation AlphaEvolve are currently moderate and slow
- Performance degrades significantly when SOTA frontier LLMs are replaced with smaller base models — the system is tightly coupled to current frontier model capabilities and does not generalize to smaller/cheaper LLMs
- Removing full-file evolution (restricting to single-function evolution as in FunSearch) significantly degrades performance on complex tasks — the approach breaks down for simpler agent configurations
- Evaluation costs can reach ~100 compute-hours per solution, limiting throughput and making the system infeasible for applications without parallelizable evaluation
- The choice of abstraction level (evolving solution directly vs. constructor function vs. search algorithm) significantly affects results and requires problem-specific expert knowledge to configure correctly
- AlphaEvolve requires a human-provided initial program (even if rudimentary) and evaluation function — it is not fully autonomous from problem specification, requiring domain expertise to frame the problem correctly
- Even with AlphaEvolve, fundamental mathematical limits remain unresolved — the minimum rank for 3x3 matrix multiplication is still unknown after extensive search
- LLM-provided evaluation of solution quality (for properties like 'simplicity') is a secondary mechanism not yet optimized — the system is not designed for open-ended discovery in domains requiring subjective or natural-language evaluation
- Removing context from prompts substantially degrades performance — the system depends heavily on rich context injection (prior solutions, problem description, evaluation results) and degrades significantly in minimal-context regimes
- AlphaEvolve's applicability to natural language–described scientific hypotheses (rather than code) is unexplored and out of scope — precluding application to most biology, chemistry, and social science discovery workflows

## Bottlenecks

- The absence of automated, machine-executable evaluation functions for natural science domains (chemistry, biology, physics) prevents evolutionary AI discovery agents from operating in those fields — experiments require physical execution or expert judgment that cannot be encoded as a scoring functio
- Manual crafting of kernel tiling heuristics for new hardware accelerators requires months of dedicated engineering and deep knowledge of hardware internals — creating a recurring bottleneck whenever new hardware generations arrive
- Self-improvement feedback loops in AI systems (where AI outputs improve AI training) operate on month-scale cycles, limiting the pace at which recursive capability gains can compound

## Breakthroughs

- AlphaEvolve discovers a rank-48 algorithm for multiplying two 4×4 complex-valued matrices — the first improvement over Strassen's 1969 algorithm for characteristic-0 fields in 56 years
- LLM-guided evolutionary coding agent deployed in production at Google, recovering 0.7% of fleet-wide compute and reducing Gemini training time by 1% — demonstrating that AI agents can autonomously improve mission-critical infrastructure at scale
- First demonstrated instance of an AI system (Gemini/AlphaEvolve) directly improving its own training infrastructure through autonomous code evolution — an early concrete realization of an AI self-improvement feedback loop

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/flashattention|FlashAttention]]
- [[entities/tensor-processing-unit|Tensor Processing Unit]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
