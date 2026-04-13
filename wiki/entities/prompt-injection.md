---
type: entity
title: Prompt Injection
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- chain_of_thought
- frontier_lab_competition
- interpretability
- mechanistic_interpretability
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.006103796791276607
staleness: 0.0
status: active
tags: []
---
# Prompt Injection

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/chain_of_thought|chain_of_thought]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/interpretability|interpretability]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

A security attack where malicious text in user-controlled input attempts to override or hijack developer-written system prompt instructions (e.g., 'Ignore previous instructions...'). Argued here to be a symptom of broken prompt abstractions rather than a fundamental security problem.

## Key Findings

1. Parallel test-time compute works by sampling multiple independent thought processes and selecting the best one without knowing the true answer ahead of time. (from "Claude's extended thinking")
2. Prompt injection defenses for computer use improved from preventing 74% to 88% of attacks, with a 0.5% false-positive rate. (from "Claude's extended thinking")
3. Prompt injection defenses combine new training, a system prompt instructing the model to ignore such attacks, and a classifier that triggers on potential injections. (from "Claude's extended thinking")
4. Claude 3.7 Sonnet successfully defeated three Pokémon Gym Leaders and won their Badges in Pokémon Red. (from "Claude's extended thinking")
5. Claude 3.7 Sonnet's 'action scaling' allows it to iteratively call functions, respond to environmental changes, and continue until an open-ended task is complete. (from "Claude's extended thinking")
6. In CBRN-related controlled studies, model-assisted participants showed uplift over non-assisted ones, but all attempts contained critical failures preventing end-to-end success. (from "Claude's extended thinking")
7. Using 256 independent samples, a learned scoring model, and a maximum 64k-token thinking budget, Claude 3.7 Sonnet achieved 84.8% on GPQA. (from "Claude's extended thinking")
8. Claude was given basic memory, screen pixel input, and function calls to sustain Pokémon gameplay through tens of thousands of interactions beyond its usual context limits. (from "Claude's extended thinking")
9. Expert red-teamers found that the frequency of critical failures in CBRN task attempts was too high for successful end-to-end task completion. (from "Claude's extended thinking")
10. Parallel test-time compute scaling is not available in the deployed Claude 3.7 Sonnet model and remains a research direction. (from "Claude's extended thinking")
11. The visible thought process in Claude 3.7 Sonnet is intended as a research preview only. (from "Claude's extended thinking")
12. Claude 3.7 Sonnet can allocate more turns, time, and computational power to computer use tasks than its predecessor. (from "Claude's extended thinking")
13. The visible thought process was not subjected to Claude's standard character training, resulting in thinking that is more detached and less personal than default outputs. (from "Claude's extended thinking")
14. Developers can set a 'thinking budget' to control precisely how long Claude spends on a problem. (from "Claude's extended thinking")
15. Extended thinking mode does not switch to a different model; it allows the same model to spend more time and effort on a problem. (from "Claude's extended thinking")

## Known Limitations

- Prompt injection vulnerabilities allow attackers to exfiltrate sensitive enterprise data through AI agents connected to internal systems (severity: blocking, trajectory: unclear)
- Computer use tool susceptible to prompt injection attacks even after mitigations — adversarial content in the environment can hijack agent actions (severity: significant, trajectory: improving)
- No discussion of security, adversarial robustness, or prompt injection risks for agents interacting with external systems (web, CRMs, ERPs) — a conspicuous absence given the described attack surface (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
