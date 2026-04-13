---
type: entity
title: GPT-5
entity_type: entity
theme_ids:
- agent_evaluation
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- frontier_lab_competition
- interpretability
- mathematical_and_formal_reasoning
- model_behavior_analysis
- multimodal_models
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- scaling_laws
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0024400334125880252
staleness: 0.0
status: active
tags: []
---
# GPT-5

> GPT-5 is OpenAI's frontier reasoning model, positioned as a consumer-facing general intelligence capable of long-horizon agentic tasks and competitive-level mathematical reasoning. Its release marked a significant step in the [[themes/test_time_compute_scaling|test-time compute]] paradigm, yet its deliberate consumer orientation introduced meaningful regressions in writing quality and prompted a fundamental rethinking of how models should be prompted and deployed.

**Type:** entity
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/interpretability|interpretability]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

GPT-5 sits at an interesting position in the frontier model landscape: it is described as close to human performance on GDPval, yet its consumer-focused orientation means its headline benchmark results can appear to plateau relative to more capability-maximizing research models. This tension between commercial positioning and raw capability defines most of the interesting open questions around GPT-5. The model excels in long-horizon agentic settings with the right tooling but degrades noticeably when prompted in the old single-turn paradigm, and its vision capabilities, while frontier-class, do not establish a new state of the art in detection-heavy multimodal evaluation.

## Key Findings

### Mathematical Reasoning: Latent Strength, Pipeline-Gated

GPT-5's most striking quantified result comes from the IMO 2025 evaluation. On its own, using best-of-32 candidate selection, GPT-5 achieved 38.1% accuracy on the six IMO 2025 problems, the strongest baseline among the three frontier models tested (versus 31.6% for Gemini 2.5 Pro and 21.4% for Grok-4). Yet all three models, when fed through a model-agnostic [[themes/test_time_compute_scaling|verification-and-refinement pipeline]], converged to the same outcome: 5 out of 6 problems solved (~85.7% accuracy), a result equivalent to an IMO gold medal.

This finding is structurally important. GPT-5's baseline advantage did not translate into a pipeline advantage; the ceiling was the same across models. The implication is that current frontier models, including GPT-5, already possess substantial latent [[themes/mathematical_and_formal_reasoning|mathematical reasoning]] capability, but single-pass generation systematically fails to extract it. The pipeline overcomes finite reasoning budgets and first-draft errors through iterative refinement, and it accepted a solution only when the verifier confirmed correctness five consecutive times without issue. The one consistent failure across all models was IMO 2025 Problem 6, pointing to a residual limitation in complex combinatorial reasoning that no amount of refinement resolved.

A secondary implication: the path to advanced AI reasoning runs through both stronger base models and better methodologies for harnessing them. GPT-5's performance on this evaluation is simultaneously a proof of its capability and a reminder that raw model strength is not sufficient on its own.

### Vision: Frontier-Class but Not SOTA

GPT-5's vision capabilities were assessed against [[themes/vision_language_models|vision-language]] benchmarks via RF100-VL, a suite of 100 object detection datasets requiring multimodal few-shot instruction across novel image domains. Gemini 2.5 Pro holds the current zero-shot mAP50:95 record at 13.3 on this benchmark. GPT-5 is described as a frontier vision reasoning model but does not surpass this mark, placing it in a competitive but not leading position on detection-oriented tasks. This aligns with the general picture of GPT-5 as a strong generalist rather than a specialist in any single modality.

### Agentic Capability: High Ceiling, Tool-Dependent

In long-horizon agentic settings, GPT-5 with an explicit reasoning trace can execute over 2,100 sequential steps with approximately 80% success rate. This places it in research-only maturity territory: the capability is real but requires deliberate scaffolding. Critically, the model's [[themes/agent_systems|agentic]] potential only manifests with high-quality, open-ended tools. Atomic API-style tools significantly underutilize it, and the entire prompting paradigm must shift from context pre-loading to compass-style orientation. This is a fundamental design constraint, not a minor tuning issue.

## Known Limitations

GPT-5 carries a cluster of limitations that collectively define the gap between its theoretical capability ceiling and its practical utility.

The most immediately visible regression is in **writing quality**. GPT-5 is significantly worse than GPT-4.5 and GPT-4o at natural language generation, producing responses described as "LinkedIn-slop" style output that fails to preserve the user's tone. This is a surprising and significant step backward for a model positioned as a general-purpose consumer assistant, and its trajectory remains unclear.

The **prompting paradigm shift** is perhaps the more structurally important limitation. Prompting GPT-5 as a stateless model rather than as an agent degrades output quality significantly. The model was designed to be oriented, not briefed; given compass-style instructions rather than dense context pre-loads. Users and products built around prior GPT interaction patterns will systematically underperform until they adapt.

Compounding this is the **tooling access gap**: non-developers cannot currently reach GPT-5's capabilities without product integrations that do not yet exist at scale. The model's value is gated behind appropriate UI abstractions, which means its real-world impact curve lags its technical capability curve. This trajectory is improving but remains a near-term bottleneck.

GPT-5 also has **no persistent memory across sessions**, requiring full re-onboarding to codebases, standards, and domain context on every invocation. For professional and developer use cases, this is a significant friction cost that limits the compounding value of repeated use.

Finally, a more subtle constraint: the **single-model paradigm** in current agentic pipelines (where one LLM serves as both solver and verifier) is a known limitation flagged explicitly in the IMO 2025 work. Separating solver and verifier into distinct models is the natural next step, and GPT-5's current architecture has not yet been evaluated in that configuration.

## Open Questions

The consumer-focused positioning of GPT-5 raises a structural question that the available evidence cannot resolve: is the apparent performance plateau relative to capability-focused models a genuine capability gap, or a deliberate product trade-off? If the latter, a capability-maximizing variant of the same underlying model may already exist internally at OpenAI. The GDPval proximity to human performance is a strong signal that the base capability is there; what remains unclear is how much the consumer orientation cost in benchmark terms versus how much is simply not being measured by current evaluations.

The writing quality regression also raises an unresolved question about [[themes/rl_for_llm_reasoning|RL for reasoning]]: does training heavily on reasoning traces and verification tasks degrade stylistic and tonal modeling? If so, this represents a meaningful capability-quality trade-off that future training pipelines will need to explicitly address.

## Relationships

GPT-5 is one of three models evaluated together in the IMO 2025 pipeline paper, alongside [[themes/frontier_lab_competition|frontier competitors]] Gemini 2.5 Pro and Grok-4. Its baseline mathematical reasoning performance exceeds both, but all three converge to the same pipeline-assisted ceiling, suggesting the bottleneck has shifted from model capability to verification and refinement methodology.

On the vision side, GPT-5 sits behind Gemini 2.5 Pro on RF100-VL, reinforcing a pattern where Google's multimodal stack maintains an edge in structured detection tasks while OpenAI leads in reasoning-heavy domains.

The sources most directly bearing on GPT-5's character are "How GPT-5 Thinks" (OpenAI VP of Research Jerry Tworek), "GPT-5 Hands-On: Welcome to the Stone Age", and "OpenAI Tests if GPT-5 Can Automate Your Job", which collectively surface the agentic potential, the writing regression, the prompting paradigm shift, and the tooling access gap documented above.

## Limitations and Open Questions

## Sources
