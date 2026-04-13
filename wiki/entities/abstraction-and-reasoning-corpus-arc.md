---
type: entity
title: Abstraction and Reasoning Corpus (ARC)
entity_type: dataset
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- in_context_and_meta_learning
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 8.422255383608861e-05
staleness: 0.0
status: active
tags: []
---
# Abstraction and Reasoning Corpus (ARC)

> The Abstraction and Reasoning Corpus (ARC) is a benchmark of 1,000 visual analogy puzzles — each requiring a model to infer abstract grid-transformation rules from a handful of demonstrations — created by François Chollet to probe few-shot generalization and fluid intelligence. It has become a canonical stress test for AI reasoning systems, distinguishing approaches that truly abstract from those that merely pattern-match on training distributions, and has catalyzed a competitive research programme with prize money, novel inference-time techniques, and a hard open question about what it would mean for a machine to genuinely solve it.

**Type:** dataset
**Themes:** [[themes/benchmark_design|benchmark_design]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]]

## Overview

ARC consists of 1,000 tasks partitioned into 400 training tasks, 400 public evaluation tasks, and 200 unpublished private evaluation tasks — the last of which is the authoritative measure of progress. Each task presents a small set of input-output grid demonstrations and asks the model to infer the latent transformation rule well enough to apply it to a novel grid. The design deliberately resists memorisation: rules are novel compositions of primitive concepts (symmetry, tiling, colour logic, shape manipulation), and the few-shot structure means brute-force statistical pattern matching cannot substitute for rule induction.

Chollet framed ARC as a proxy for general fluid intelligence — the capacity to acquire new skills on the fly rather than recall pre-trained ones. The benchmark's difficulty for large language models, despite their broad competence on other tasks, made it a flashpoint for debate about what LLMs actually learn and whether scale alone can close the gap.

## Key Findings

Progress on ARC has been painfully slow relative to other benchmarks, and the methods that have moved the needle reveal as much about the benchmark's structure as about AI capabilities in general.

**The score trajectory is revealing.** The 2020 Kaggle competition's winning entry reached only ~21% on a 100-task private evaluation subset; an ensemble of the top two methods brought that to 31% — already requiring multi-model combination to squeeze out gains. By 2023, MindsAI held the lead at 34%, inching to 43% by the time of writing. The state-of-the-art before the ARC Prize announcement in 2024 sat at 34% on the private set. These numbers are striking not because they're low in absolute terms, but because progress has required increasingly sophisticated test-time machinery rather than straightforward capability improvements from better base models. (from On the "ARC-AGI" $1 Million Reasoning Challenge)

**The leading methods exploit test-time learning, not just inference.** MindsAI's approach converts few-shot tasks into effectively many-shot ones by automatically augmenting each task's demonstrations and performing additional fine-tuning on those augmented transformations at inference time — what they call "active inference." This is paired with synthetic task generation: starting from 100–160 manually written Python seed programs, a data generation pipeline uses LLM remixing to produce 400,000 new ARC-style problems paired with solutions, providing the training signal needed for the fine-tuning to be meaningful. (from On the "ARC-AGI" $1 Million Reasoning Challenge, Combining Induction and Transduction for Abstract Reasoning)

**Program synthesis at scale is the other viable direction.** Ryan Greenblatt's generate-test-revise approach prompts GPT-4o to generate approximately 5,000 Python programs per task, using prompts around 30,000 tokens long — comparable in length to a 50-page master's thesis. This achieved 51% on the public evaluation set (on a 100-task sample, standard error ~5%) and 71% on training tasks. However, the method is not competition-legal: it requires internet access to the GPT-4o API and exceeds the 12-hour runtime limit imposed by the ARC Prize rules. The meaningful number is 50% on the public evaluation set, not the private one — a distinction that matters significantly given that the public and private sets differ in difficulty. (from On the "ARC-AGI" $1 Million Reasoning Challenge)

**The ARC Prize raised the stakes sharply.** Announced in June 2024 by Chollet and Mike Knoop, the competition offers a $500,000 grand prize for any program scoring 85% or higher on 100 tasks from the private evaluation set, within a 12-hour runtime window and with no internet access. The gap between the current best legal score (~43%) and the prize threshold (85%) is wide enough that no incremental improvement is likely to close it — a new paradigm may be required.

## Open Questions and Limitations

The benchmark raises a genuine epistemological tension. The methods that perform best — test-time fine-tuning on augmented demonstrations, massive program synthesis — are computationally expensive in ways that scale poorly to real-world deployment. Whether these are genuine steps toward fluid intelligence or sophisticated forms of search within a fixed hypothesis class remains contested.

The distinction between public and private evaluation sets is under-appreciated in public discourse. Scores on the public set are optimistically biased: researchers can iterate against it, and the private set is harder by design. Greenblatt's 51% public figure, widely cited, is not directly comparable to the 43% MindsAI score on the private set — comparing them conflates two different problems.

The synthetic data generation pipeline that underlies the best-performing approaches (100–160 seed programs → 400k problems via LLM remixing) raises questions about coverage: does the remixed distribution actually cover the tail of rule compositions that appears in the private evaluation set, or does it systematically miss certain abstractions? This is largely unanswered. Similarly, the test-time learning approaches work by fine-tuning on augmented demonstrations — but the quality and diversity of those augmentations likely determines the ceiling, and failure modes are opaque.

At 85%, the prize threshold is itself arbitrary. Whether ARC-solving at that level would constitute evidence of general fluid intelligence, or merely demonstrate that a specific benchmark has been engineered around, is a question Chollet and the broader community have not resolved.

## Relationships

ARC sits at the intersection of [[themes/benchmark_design|benchmark_design]] and [[themes/test_time_learning|test_time learning]] in a productive tension: the benchmark was designed to resist the kinds of memorisation that make other benchmarks fragile, but the methods now approaching its frontier rely heavily on inference-time adaptation — which reintroduces a form of task-specific learning that Chollet's original framing was meant to exclude. This connects it to broader debates in [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]] about whether benchmarks inevitably get gamed by sufficiently flexible systems.

The synthetic data generation work (see Combining Induction and Transduction for Abstract Reasoning) ties ARC directly to [[themes/synthetic_data_generation|synthetic_data_generation]] methodology: the LLM-remixing pipeline is itself a demonstration that program synthesis and language models can serve as data factories for tasks where human annotation is intractable. The program synthesis direction (Greenblatt's approach) is an instantiation of [[themes/test_time_compute_scaling|test_time compute scaling]] — trading inference budget for accuracy in a domain where correctness is verifiable.

## Limitations and Open Questions

## Sources
