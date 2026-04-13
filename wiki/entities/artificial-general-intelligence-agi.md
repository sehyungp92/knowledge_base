---
type: entity
title: Artificial General Intelligence (AGI)
entity_type: theory
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- compute_and_hardware
- evaluation_and_benchmarks
- frontier_lab_competition
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- startup_and_investment
- test_time_learning
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00048348581493389063
staleness: 0.0
status: active
tags: []
---
# Artificial General Intelligence (AGI)

> Artificial General Intelligence refers to a hypothetical system capable of exhibiting the full range of cognitive capabilities that humans possess: robust generalization to novel tasks, efficient acquisition of new skills, and the capacity for scientific invention — analogous to a Turing machine's universality across computation. It remains one of the most contested and consequential targets in AI research, simultaneously serving as a benchmark design challenge, an investment thesis, a governance flashpoint, and a long-run capability goal for every major frontier lab.

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/startup_and_investment|startup_and_investment]], [[themes/test_time_learning|test_time_learning]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

---

## Overview

The working definition that has gained the most traction in the benchmarking community frames AGI as a system capable of *efficiently acquiring new skills and solving novel problems for which it was neither explicitly designed nor trained*. This formulation deliberately sidesteps raw performance on known tasks and instead focuses on generalization under novelty. It distinguishes AGI from narrow AI not by capability level but by the topology of what can be learned and when.

ARC-AGI — the Abstraction and Reasoning Corpus — was designed to operationalize this definition. Tasks require only "Core Knowledge" priors: basic objectness, elementary topology, and integer arithmetic. They assume no specialized world knowledge, no language, and no memorizable patterns. They are explicitly constructed so that preparation and memorization provide no advantage, targeting the generalization signal directly.

---

## Measurement: ARC-AGI as a Proxy

The history of ARC-AGI scores tells a stark story about the gap between current AI and the AGI target. In the first Kaggle competition in 2020, no deep-learning approach scored above 1%, and the top overall score was 20%. Over the following four years, with the field producing GPT-4, instruction tuning, and chain-of-thought reasoning, that number crept only to 33% by early 2024. The original GPT-3 scored 0% under direct prompting.

Yet humans find the benchmark trivially easy. Two testers scored 97% and 98% respectively, together covering all 100 private evaluation tasks. A Mechanical Turk study found 99% of public evaluation tasks solved by at least one worker. The human-AI gap on a benchmark explicitly designed to require nothing beyond basic priors is both a practical measurement and a conceptual argument: whatever current LLMs are doing at scale, it is not the kind of generalization the AGI definition requires.

---

## The 2024 Inflection

ARC Prize 2024 disrupted the stagnation. The private evaluation score jumped from 33% to 55.5%, driven by the emergence of test-time training (TTT) as a credible frontier technique. MindsAI, with Jack Cole and Mohamed Osman as early practitioners beginning in 2023, achieved the highest competition score of 55.5% on the private set, though they were ineligible for prizes because they did not open-source their solution.

A structurally distinct approach from Ryan Greenblatt reached 42% on ARC-AGI-Pub through LLM-guided program synthesis, searching thousands of Python programs per task using GPT-4o. This demonstrated that multiple independent strategies, one adapting model weights at test time and one using the model as a search heuristic over programs, could both breach previously stable performance ceilings.

The two approaches reflect a deeper tension in how the field conceptualizes progress toward AGI: is it about deeper generalization of learned representations, or about better search over structured program spaces? Both moved the needle; neither solved the problem.

---

## Open Questions and Limitations

Despite the 2024 gains, the benchmark remained unbeaten as of December 5, 2024, five years after its creation. The jump from 33% to 55.5% is significant, but 55.5% on a task that humans solve at 99% is not a narrow gap. The tasks that remain unsolved are not a random residual; they likely concentrate the hardest generalization failures.

The public leaderboard (ARC-AGI-Pub) offered approximately 1,000 times more compute than the Kaggle leaderboard (up to $10,000 in API credits versus a $10 equivalent), which means the improved scores come with a non-trivial compute premium. Whether the gains represent genuine generalization or more powerful search under greater compute remains an open empirical question.

More broadly, AGI as a concept carries definitional instability. The operational definition used by ARC-AGI is specific and narrow; other researchers, investors, and lab leaders use the term to mean substantially different things. This ambiguity makes AGI simultaneously a rigorous benchmark target, an investment narrative, and a governance trigger, with different communities talking past each other using the same word.

---

## Relationships

The measurement of AGI is tightly coupled with [[themes/benchmark_design|benchmark design]] and [[themes/evaluation_and_benchmarks|evaluation methodology]]; the specific techniques that drove 2024 gains, particularly test-time training, are detailed under [[themes/test_time_learning|test-time learning]] and [[themes/post_training_methods|post-training methods]]. The governance implications of AGI proximity are central to [[themes/alignment_and_safety|alignment and safety]] and [[themes/ai_governance|AI governance]]. Investment and competitive dynamics around AGI timelines are covered under [[themes/frontier_lab_competition|frontier lab competition]], [[themes/startup_and_investment|startup and investment]], and [[themes/vc_and_startup_ecosystem|VC and startup ecosystem]].

Primary sources: ARC Prize 2024: Technical Report, Google DeepMind CEO Demis Hassabis: The Path To AGI, Superintelligence, Bubbles And Big Bets: AI Investing in 2024.

## Key Findings

## Limitations and Open Questions

## Sources
