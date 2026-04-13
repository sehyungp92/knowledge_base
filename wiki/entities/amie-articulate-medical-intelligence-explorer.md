---
type: entity
title: AMIE (Articulate Medical Intelligence Explorer)
entity_type: entity
theme_ids:
- agent_evaluation
- agent_systems
- evaluation_and_benchmarks
- medical_and_biology_ai
- multi_agent_coordination
- multimodal_models
- scientific_and_medical_ai
- software_engineering_agents
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0048175050541580606
staleness: 0.0
status: active
tags: []
---
# AMIE (Articulate Medical Intelligence Explorer)

**Type:** entity
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/vision_language_models|vision_language_models]]

## Overview

A Google Research LLM-based AI system for conversational diagnostic and management reasoning, comprising a Dialogue Agent and a Management Reasoning (Mx) Agent built on Gemini language models

## Key Findings

1. The OSCE study used 105 scenarios across three modality types (35 skin photos, 35 ECGs, 35 clinical documents), evaluated by 18 specialist physicians with each consultation reviewed by 3 independent s (from "2025-5-6")
2. The Dialogue Agent uses a chain-of-reasoning approach with three sequential steps: Plan Response, Generate Response, and Refine Response (from "Towards Conversational AI for Disease Management")
3. AMIE remains a research system not intended for clinical use and requires further real-world validation before clinical translation. (from "2025-5-6")
4. AMIE implements a three-phase state-aware dialogue framework: (1) History Taking, (2) Diagnosis & Management, and (3) Answer Follow-up Questions, with automatic phase transitions driven by intermediat (from "2025-5-6")
5. The Mx Agent's structured reasoning chain consists of three stages: Analyze Patient, Set Objectives, and Plan and Cite (from "Towards Conversational AI for Disease Management")
6. AMIE was evaluated against 19 board-certified PCPs with a median post-residency experience of 6 years (IQR 3.5–11.5 years) (from "2025-5-6")
7. The OSCE study evaluated AMIE against 21 PCPs with a median of 9 years post-residency experience across 100 multi-visit scenarios in 5 medical specialties (from "Towards Conversational AI for Disease Management")
8. RxQA is a multiple-choice medication reasoning benchmark derived from two national drug formularies (US and UK) and validated by board-certified pharmacists (from "Towards Conversational AI for Disease Management")
9. The clinical guideline corpus totals 10.5 million tokens across 627 documents, exceeding Gemini's two million context window and necessitating a preliminary retrieval step (from "Towards Conversational AI for Disease Management")
10. The codebase and specific prompts for multimodal AMIE are not being open-sourced due to safety implications associated with unmonitored deployment of AI systems in medical contexts. (from "2025-5-6")
11. Further research would be needed before real-world clinical translation of AMIE (from "Towards Conversational AI for Disease Management")
12. The Dialogue Agent was fine-tuned on Gemini 1.5 Flash, replacing the previously used PaLM-2 base model (from "Towards Conversational AI for Disease Management")
13. AMIE uses a dual-agent architecture inspired by dual-process theory, with a fast Dialogue Agent analogous to System 1 and a slower Mx Agent analogous to System 2 (from "Towards Conversational AI for Disease Management")
14. The Dialogue Agent uses RLHF/RLAIF following supervised fine-tuning, with reward models trained from both human and LLM-generated pairwise preferences (from "Towards Conversational AI for Disease Management")
15. The Mx Agent uses decoding constraints to enforce a predefined JSON schema, guaranteeing valid plan structure and citation format (from "Towards Conversational AI for Disease Management")

## Relationships

## Limitations and Open Questions

## Sources
