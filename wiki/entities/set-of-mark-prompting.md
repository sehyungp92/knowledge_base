---
type: entity
title: Set-of-Mark Prompting
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_systems
- chain_of_thought
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- finetuning_and_distillation
- knowledge_and_memory
- multi_agent_coordination
- multimodal_models
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0009457185370341676
staleness: 0.0
status: active
tags: []
---
# Set-of-Mark Prompting

Set-of-Mark (SoM) Prompting is a visual annotation technique that overlays bounding boxes and numerical labels directly onto screenshots of interactive interfaces, enabling vision-language models to ground their actions in specific UI elements rather than relying on abstract spatial reasoning. It has become a foundational building block for web and GUI agents, offering a lightweight, interpretable bridge between visual perception and action selection without requiring specialized object detection models.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/multimodal_models|Multimodal Models]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/vision_language_models|Vision-Language Models]]

---

## Overview

Set-of-Mark Prompting addresses a core challenge in GUI and web agents: given a screenshot, how does a model know *which element* to interact with? The technique annotates the visual input with explicit labels — bounding boxes and numeric markers — on interactive elements, allowing the model to reference them by ID rather than guessing coordinates or element descriptions. This sidesteps the need for precise spatial grounding from the model itself, trading that burden for a reliable pre-processing step.

The most prominent deployment of this approach is in WebVoyager, where the labeling is implemented not through a learned object detector but through a rule-based JavaScript tool (GPT-4V-Act) that programmatically identifies interactive DOM elements and renders their bounding boxes onto the screenshot. This design choice is deliberate: it avoids the brittleness of detection models on the highly variable visual landscape of live websites, while still providing the structured visual grounding that large multimodal models need to act reliably.

---

## Role in WebVoyager

WebVoyager demonstrates the practical value of SoM-style prompting in a particularly demanding setting: open-web navigation on real websites via Selenium, not sanitized local mirrors. The agent faces floating ads, pop-up windows, and constantly evolving page layouts — conditions that stress-test both visual grounding and planning. By overlaying numbered labels on interactive elements, WebVoyager gives GPT-4V a structured visual vocabulary for referring to page components, which the model then combines with [[themes/chain_of_thought|ReAct-style reasoning]] — generating a natural language thought before producing action code.

The results are striking. WebVoyager achieves a **59.1% task success rate** on its 643-task benchmark (spanning 15 popular websites), substantially outperforming both text-only WebVoyager at 40.1% and GPT-4 (All Tools) at 30.8%. All three multimodal backbones tested — GPT-4V, Claude-3-Opus, and GPT-4o — significantly outperform the text-only baseline, confirming that the visual grounding enabled by SoM labeling is doing real work, not just providing cosmetic structure. On the SeeAct online test set, WebVoyager's 30% success rate also edges out the best SeeAct autonomous agent's 26%.

---

## Limitations and Open Questions

Despite its advantages, SoM prompting does not fully solve visual grounding — it relocates the problem rather than eliminating it. In WebVoyager's failure analysis, **visual grounding issues account for 24.8% of failures**, suggesting that even with bounding box overlays, models struggle to correctly interpret and act on the annotated elements in complex layouts. Hallucination accounts for a further 21.8% of failures, and navigation becoming stuck (exhausting the step budget) is the single largest failure mode at 44.4%.

A structural limitation lies in the resolution requirements of web navigation. SoM labeling is only as useful as the model's ability to read the annotated page content; most open-source LMMs reduce images to 224×224 or 336×336 pixels, making smaller fonts unrecognizable and rendering fine-grained web navigation essentially infeasible. This creates a hard dependency on high-resolution capable frontier models, constraining the technique's accessibility.

The rule-based JavaScript implementation also raises questions about generalizability. DOM-based element extraction works well for standard HTML interactive elements but may fail on canvas-rendered UIs, custom components, or heavily JavaScript-modified pages — exactly the kind of edge cases that proliferate on live websites. A deeper integration with learned detection, or hybrid approaches combining DOM signals with visual saliency, remains an open direction.

---

## Connections

SoM Prompting sits at the intersection of several active research threads. It is closely related to work on [[themes/computer_use_and_gui_agents|computer use agents]] more broadly, where the challenge of translating visual perception into precise UI actions is central. The technique complements [[themes/chain_of_thought|chain-of-thought and ReAct prompting]] by structuring the *perceptual* side of reasoning, giving models unambiguous referents for their action plans. It also connects to [[themes/vision_language_models|vision-language model]] capabilities research, since the effectiveness of SoM labeling is gated by the model's resolution handling and fine-grained visual comprehension — as explored in works like Thinking with Images for Multimodal Reasoning.

The Agent S framework extends the broader paradigm of visually-grounded GUI agents, building on foundations that SoM Prompting helped establish. As evaluation of web agents matures — WebVoyager's GPT-4V-based automatic evaluator achieves 85.3% agreement with human judgment (kappa ≈ 0.70, matching inter-human agreement) — the field gains better tools for understanding where SoM-style approaches succeed and where they break down.

## Key Findings

## Relationships

## Sources
