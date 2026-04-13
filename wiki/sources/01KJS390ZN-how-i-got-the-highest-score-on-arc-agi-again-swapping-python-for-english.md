---
type: source
title: How I got the highest score on ARC-AGI again swapping Python for English
source_id: 01KJS390ZNAK2Z84GR9TH47DN2
source_type: article
authors: []
published_at: '2025-09-16 00:00:00'
theme_ids:
- agent_systems
- benchmark_design
- evaluation_and_benchmarks
- multi_agent_coordination
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How I got the highest score on ARC-AGI again swapping Python for English

**Authors:** 
**Published:** 2025-09-16 00:00:00
**Type:** article

## Analysis

# How I got the highest score on ARC-AGI again swapping Python for English
2025-09-16 · article
https://jeremyberman.substack.com/p/how-i-got-the-highest-score-on-arc-agi-again

---

## Briefing

**A practitioner achieves new SoTA on both ARC-AGI v1 (79.6%) and v2 (29.4%) by replacing Python code generation with evolutionary natural language instruction search using Grok-4, at 25× lower cost than o3 — and argues the deeper lesson is that LLMs fail generalization not because they're distribution-bound, but because their reasoning circuits are fused to domains rather than universal, and RL is the corrective.**

### Key Takeaways
1. **Natural language beats code for complex spatial reasoning** — ARC-AGI v2 transformations are too nuanced to express elegantly in Python, so evolving plain-English instructions unlocks performance that code generation cannot.
2. **79.6% on ARC v1 at $8.42/task vs. o3's $200/task** — the same evolutionary architecture achieves near-o3-level scores at 25× lower cost by switching the representation from functions to instructions.
3. **29.4% on ARC v2 is a new SoTA** — the previous best was 25%, and the human ceiling is 100%, meaning a 4× human–AI gap persists on v2 even after this advance.
4. **Evolutionary test-time compute scales intelligently** — the 3-phase loop (30 initial → 5 individual revisions → 5 pooled revisions = 40 max attempts) balances exploration, focused refinement, and recombination within token budget constraints.
5. **More context in pooled revisions can hurt, not help** — thinking models lose focus and hit token limits when given more than two parent instructions, revealing a counterintuitive tradeoff in multi-agent synthesis.
6. **LLMs have "dead reasoning zones"** — on 100k+ traces, thinking models confidently produce logically false outputs on ARC tasks and cannot self-correct even when explicitly shown the error, a failure mode humans do not have.
7. **The Fused Circuit Problem** — LLMs learn math-logic, code-logic, and writing-logic as separate skills rather than a universal reasoning kernel, causing incomplete transfer to novel domains.
8. **RL over CoT is the structural fix** — reinforcement learning forces pre-trained weights toward logical consistency by optimizing for correctness, not plausible-sounding next tokens.
9. **The goal is not escaping the training distribution** — AGI requires bringing universal, domain-agnostic reasoning *into* the training distribution, not making models out-of-distribution robust by other means.
10. **ARC-AGI remains the sharpest generalization probe** — LLMs that win the math olympiad fail children's grid puzzles, making it the clearest diagnostic of the human–AI reasoning gap.

---

### ARC-AGI as a Benchmark: Why It Still Matters

- ARC-AGI is described as "an intelligence test designed to measure abstract pattern recognition, similar to an IQ test," uniquely probing generalization rather than memorization.
  - The test presents novel input/output grid transformation patterns through a few examples and requires the system to infer and apply an underlying rule it has never encountered.
  - **The defining characteristic is the human–AI gap**: humans readily solve tasks that defeat state-of-the-art LLMs, making it the clearest proxy for generalization ability currently available.
- ARC-AGI v1 and v2 represent different difficulty tiers.
  - v1 tasks are moderately hard; v2 tasks, released in early 2025, require substantially more multi-step reasoning.
  - On v2: smart humans achieve 100% on batches of 100 tasks; the best LLMs achieve only 16% — a 6× gap even before this work.
- The benchmark exposes a paradox that motivates the entire research agenda: **LLMs can win the math olympiad but fail simple puzzles**, signaling that high benchmark performance in trained domains does not imply general reasoning competence.

---

### The v1 Solution: Python Function Evolution

- The original approach used language models to generate Python functions as candidate solutions for each ARC task.
  - Key advantage: functions are **deterministic and testable**, allowing hundreds of candidates to be scored against training examples and ranked objectively.
  - This enabled a clean evolutionary loop: generate → score → evolve from top performers.
- The Python approach has a hard ceiling on ARC v2.
  - v2 transformations "require nuanced pattern recognition and contextual understanding that would result in unwieldy, brittle code."
  - Complex spatial rules that humans describe naturally in language cannot be captured elegantly in programmatic form, causing the strategy to hit a wall.

---

### The v2 Solution: Evolving Natural Language Instructions

- The architectural shift is conceptually minimal but practically transformative: **replace Python functions with plain-English instructions** as the evolving unit.
  - Everything else — the evolutionary loop, fitness scoring, revision strategies — is preserved from v1.
  - The switch exploits the fact that natural language can express nuanced, contextual pattern rules that code cannot.

#### The Core Evaluation Loop
- For each task, Grok-4 generates plain-English instructions describing the input-to-output transformation.
- A subagent model applies each instruction to the training examples as if they were test inputs and generates predicted outputs.
- A **fitness score** is computed as the fraction of training examples solved correctly, with partial credit awarded as the percentage of correct cells for near-misses.
- This produces a ranked population of instructions ready for evolutionary refinement.

#### Individual vs. Pooled Revisions
- **Individual revisions**: take the single best instruction, its model-generated outputs, the ground truth, and an ASCII diff of discrepancies; prompt the model to refine the instruction to fix its mistakes.
  - Focused, targeted refinement with minimal context overhead.
- **Pooled revisions**: combine multiple scored instructions in one promp

## Key Claims

1. The author's latest program achieves 79.6% on ARC-AGI v1 at $8.42 per task, which is 25× more cost-efficient than o3.
2. The author's system sets a new state-of-the-art of 29.4% on ARC-AGI v2, surpassing the previous best of 25%.
3. o3 preview achieved 75.7% on ARC-AGI v1 spending $200 per task.
4. The author previously achieved 53.6% on ARC-AGI v1, taking first place in December.
5. The evolutionary system generates up to 40 candidate instructions using 36 dynamic prompts per task.
6. ARC-AGI v2 was created in early 2025 and has much harder tasks requiring more multi-step reasoning than v1.
7. Smart humans can achieve 100% accuracy on a batch of 100 ARC-AGI v2 challenges, while the best LLMs get only 16%.
8. The author's v1 solution used Python functions to solve tasks due to their deterministic and testable nature.
9. The Python-function strategy fails on ARC v2 because transformations are too complex to express elegantly in code.
10. Each instruction is evaluated via a fitness score based on how many training examples it solves correctly, including partial credit by percentage of correct cells.

## Capabilities

- Evolutionary test-time compute with natural language (English) instructions achieves 79.6% on ARC-AGI v1 and 29.4% SoTA on ARC-AGI v2 at $8.42 per task — 25x more cost-efficient than o3's $200 per task
- Multi-agent evolutionary architecture generates and refines up to 40 natural language candidate solutions per task through individual revision (single-instruction feedback) and pooled revision (multi-instruction synthesis) phases with Grok-4
- Natural language (English) instructions serve as a more expressive and generalisable medium than Python code for specifying complex multi-step visual pattern transformations in AI reasoning pipelines

## Limitations

- LLMs fundamentally struggle to generalise to tasks outside their training distribution, failing at abstract pattern recognition that humans solve trivially
- LLMs have 'dead reasoning zones' — regions of the weight space where logical consistency collapses for out-of-distribution inputs, producing obviously false conclusions even after extended chain-of-thought that cannot be corrected by feedback
- LLM reasoning circuits are fragmented across domain-specific embeddings (math-logic, code-logic, writing-logic), preventing fully transferable logical deduction across novel domains
- Code-based program synthesis approaches hit a hard complexity ceiling on ARC-AGI v2 — transformations requiring nuanced contextual pattern recognition cannot be expressed cleanly as deterministic programs
- Best LLMs achieve only 16% on ARC-AGI v2 while humans achieve 100% — a 6x gap indicating a fundamental ceiling on LLM generalisation capability as of mid-2025
- Thinking models generate excessive reasoning tokens during extended chain-of-thought, causing context limit failures when multiple candidate instructions are pooled — directly limiting the effectiveness of multi-instruction revision strategies
- Thinking models can spend up to 20 minutes reasoning on an out-of-distribution task and still produce logically false conclusions with high confidence, with no self-correction even when the error is explicitly pointed out
- Providing multiple candidate instructions as context to thinking models can degrade rather than improve reasoning performance — additional context causes focus loss analogous to human cognitive overload
- The evolutionary test-time compute approach still costs $8.42 per task — over 400 LLM calls per problem — making it impractical for any real-world deployment beyond research benchmarks

## Bottlenecks

- LLMs lack a domain-independent reasoning substrate — logical inference is learned as fragmented domain-specific circuits fused with content, blocking robust generalisation to novel out-of-distribution abstract tasks
- Per-task cost of evolutionary test-time search remains high (~$8–$200 depending on model and strategy), blocking practical application of generalisation-capable AI systems beyond research benchmarks

## Breakthroughs

- Replacing Python code with natural language (English) instructions as the evolved artifact in evolutionary test-time compute achieves new SoTA on ARC-AGI v2 (29.4%, up from 25%) and surpasses o3 on ARC-AGI v1 at 25x lower cost — demonstrating that NL is a more expressive fitness substrate than forma

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/evolutionary-test-time-compute|Evolutionary Test-Time Compute]]
