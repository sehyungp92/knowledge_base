---
type: entity
title: Claude Opus 4.1
entity_type: entity
theme_ids:
- agent_evaluation
- ai_business_and_economics
- ai_market_dynamics
- benchmark_design
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- frontier_lab_competition
- interpretability
- model_behavior_analysis
- pretraining_and_scaling
- scaling_laws
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012085590220268166
staleness: 0.0
status: active
tags: []
---
# Claude Opus 4.1

> Claude Opus 4.1 is Anthropic's flagship large language model that, as of mid-2025, achieved a notable milestone by outperforming OpenAI's own models on OpenAI's GDPval benchmark — a rigorous evaluation of AI performance across 44 occupations spanning nine major industries. Its near-parity with human industry experts on substantive, multi-hour professional tasks has made it a central reference point in debates about AI's readiness for economic automation.

**Type:** entity
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/interpretability|interpretability]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/scaling_laws|scaling_laws]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Claude Opus 4.1 is notable not just for its benchmark performance but for the circumstances under which that performance became public: OpenAI chose to publish GDPval results that showed a competitor's model outperforming their own. This transparency, widely noted in commentary, lends the findings unusual credibility. GDPval itself is methodologically serious — tasks were sourced from industry professionals averaging 14 years of experience, each task requiring roughly 7 hours of expert work, and graded via blinded comparison allowing both clear preferences and ties. Across 1,320 tasks covering 44 occupations, Claude Opus 4.1 came closest to industry expert performance among all evaluated models, including OpenAI's offerings.

This result positions Opus 4.1 as a significant signal in the [[themes/frontier_lab_competition|frontier lab competition]] narrative: Anthropic's model leading on an OpenAI-designed benchmark is evidence that the frontier is genuinely contested rather than consolidated around any single lab. It also anchors ongoing discussions in [[themes/ai_business_and_economics|AI business and economics]] about the pace at which models are approaching economic substitutability for knowledge workers.

## Key Findings

The GDPval results show Claude Opus 4.1 achieving near-parity with human experts across predominantly digital, economically significant occupations. The benchmark's scope was deliberately constrained to sectors contributing at least 5% of US GDP, with five occupations per sector weighted by salary — a design choice that makes results more economically legible but also narrows what conclusions can be drawn about the broader workforce.

Several structural features of the benchmark temper the significance of Opus 4.1's lead. Tasks were one-shot: models received a problem and produced a solution without the iterative clarification that characterises real professional work. Human expert evaluators themselves agreed only 70% of the time on which answer — model or human — was better, revealing substantial subjectivity baked into the grading signal. And the benchmark explicitly excludes occupations whose tasks are not predominantly digital, meaning large segments of the labour market fall entirely outside its scope.

These caveats matter for interpreting what Opus 4.1's performance actually means. Strong performance on a well-designed but structurally bounded benchmark is evidence of advancing capability, not a proof of general professional readiness. The benchmark also does not capture the asymmetric cost of catastrophic errors — a limitation particularly salient in high-stakes domains like medicine, law, or infrastructure, where a single failure can outweigh many successes.

Separately, Opus 4.1 was observed hallucinating specific credit and pricing values in at least one documented interaction, then acknowledging the fabrication when challenged. This is a concrete example of a failure mode that GDPval-style benchmarks are poorly positioned to surface: confident confabulation on factual specifics that a human expert would simply know or look up.

## Known Limitations

- **Hallucination of factual specifics**: Opus 4.1 fabricated pricing values in at least one documented case, admitting the error only when challenged — a limitation not captured by task-level benchmark grading. *(severity: significant, trajectory: improving)*
- **One-shot task ceiling**: Production code correctness on full-stack tasks required multiple follow-ups, indicating that even frontier models outside GPT-5 struggle with end-to-end correctness in realistic software development workflows. *(severity: significant, trajectory: improving)*
- **Benchmark-reality gap**: Strong GDPval performance was achieved under conditions (one-shot, digital-only, no clarification loops) that abstract away key features of professional work, leaving open how performance translates to deployed settings.

## Relationships

Claude Opus 4.1's primary evaluative context is [[themes/evaluation_and_benchmarks|GDPval]], OpenAI's 44-occupation benchmark, where it outperformed GPT-5 and other OpenAI models — an outcome discussed at length in OpenAI Tests if GPT-5 Can Automate Your Job - 4 Unexpected Findings and Failing to Understand the Exponential, Again. Its performance on coding tasks connects it to broader questions in [[themes/code_generation|code generation]] and [[themes/code_and_software_ai|code and software AI]], while its hallucination behaviour surfaces tensions in [[themes/model_behavior_analysis|model behavior analysis]]. The competitive dynamics — an Anthropic model leading on an OpenAI benchmark — make it a live data point in [[themes/frontier_lab_competition|frontier lab competition]] and [[themes/ai_market_dynamics|AI market dynamics]]. Its proximity to expert-level performance on economically weighted tasks feeds directly into [[themes/vertical_ai_and_saas_disruption|vertical AI and SaaS disruption]] discussions about what near-parity actually implies for labour substitution timelines.

## Limitations and Open Questions

## Sources
