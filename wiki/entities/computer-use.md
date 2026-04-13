---
type: entity
title: Computer Use
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- chain_of_thought
- computer_use_and_gui_agents
- interpretability
- mechanistic_interpretability
- model_commoditization_and_open_source
- multi_agent_coordination
- reasoning_and_planning
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0027363716954648953
staleness: 0.0
status: active
tags: []
---
# Computer Use

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/interpretability|interpretability]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

A capability allowing Claude to observe a user's computer screen and issue virtual mouse clicks and keyboard presses to perform tasks on the user's behalf.

## Key Findings

1. In CBRN-related controlled studies, model-assisted participants showed uplift over non-assisted ones, but all attempts contained critical failures preventing end-to-end success. (from "Claude's extended thinking")
2. Prompt injection defenses for computer use improved from preventing 74% to 88% of attacks, with a 0.5% false-positive rate. (from "Claude's extended thinking")
3. Claude was given basic memory, screen pixel input, and function calls to sustain Pokémon gameplay through tens of thousands of interactions beyond its usual context limits. (from "Claude's extended thinking")
4. The visible thought process was not subjected to Claude's standard character training, resulting in thinking that is more detached and less personal than default outputs. (from "Claude's extended thinking")
5. Parallel test-time compute scaling is not available in the deployed Claude 3.7 Sonnet model and remains a research direction. (from "Claude's extended thinking")
6. Claude 3.7 Sonnet can allocate more turns, time, and computational power to computer use tasks than its predecessor. (from "Claude's extended thinking")
7. Prompt injection defenses combine new training, a system prompt instructing the model to ignore such attacks, and a classifier that triggers on potential injections. (from "Claude's extended thinking")
8. The visible thought process in Claude 3.7 Sonnet is intended as a research preview only. (from "Claude's extended thinking")
9. Developers can set a 'thinking budget' to control precisely how long Claude spends on a problem. (from "Claude's extended thinking")
10. Using 256 independent samples, a learned scoring model, and a maximum 64k-token thinking budget, Claude 3.7 Sonnet achieved 84.8% on GPQA. (from "Claude's extended thinking")
11. Claude 3.7 Sonnet's 'action scaling' allows it to iteratively call functions, respond to environmental changes, and continue until an open-ended task is complete. (from "Claude's extended thinking")
12. Claude 3.7 Sonnet successfully defeated three Pokémon Gym Leaders and won their Badges in Pokémon Red. (from "Claude's extended thinking")
13. Parallel test-time compute works by sampling multiple independent thought processes and selecting the best one without knowing the true answer ahead of time. (from "Claude's extended thinking")
14. Expert red-teamers found that the frequency of critical failures in CBRN task attempts was too high for successful end-to-end task completion. (from "Claude's extended thinking")
15. Extended thinking mode does not switch to a different model; it allows the same model to spend more time and effort on a problem. (from "Claude's extended thinking")

## Known Limitations

- Computer use on full OS environments is unreliable — 38.1% OSWorld success rate means ~62% task failure; human oversight explicitly required (severity: significant, trajectory: improving)
- Substantial performance cliff between web-based and full OS computer use — 87% WebVoyager vs 38.1% OSWorld reveals models are far more reliable in structured browser environments than general OS conte (severity: significant, trajectory: unclear)
- Computer use tool susceptible to prompt injection attacks even after mitigations — adversarial content in the environment can hijack agent actions (severity: significant, trajectory: improving)
- Computer use tool access gated to usage tiers 3-5 — the most capable agent tool is not broadly accessible, signaling safety and reliability concerns that limit real-world adoption (severity: minor, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
