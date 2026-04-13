---
type: source
title: 'Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning
  Models'
source_id: 01KJTNQNAG7PQ6JS7X6JENJ7JH
source_type: paper
authors:
- Yunxin Li
- Zhenyu Liu
- Zitao Li
- Xuanyu Zhang
- Zhenran Xu
- Xinyu Chen
- Haoyuan Shi
- Shenyuan Jiang
- Xintong Wang
- Jifang Wang
- Shouzheng Huang
- Xinping Zhao
- Borui Jiang
- Lanqing Hong
- Longyue Wang
- Zhuotao Tian
- Baoxing Huai
- Wenhan Luo
- Weihua Luo
- Zheng Zhang
- Baotian Hu
- Min Zhang
published_at: '2025-05-08 00:00:00'
theme_ids:
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models

This survey provides the most comprehensive map to date of the multimodal reasoning landscape, organizing roughly 700 publications through June 2025 into a four-stage developmental roadmap — from modular pipelines to language-centric short reasoning, extended RL-driven chains, and a prospective "native" Stage 4 where reasoning is omnimodal rather than language-mediated. Its core contribution is not just taxonomy but diagnosis: the survey argues that the language-centric paradigm, which has driven all recent gains, is also the primary structural bottleneck blocking the next generation of capable, adaptive, real-world multimodal agents.

**Authors:** Yunxin Li, Zhenyu Liu, Zitao Li, Xuanyu Zhang, Zhenran Xu, Xinyu Chen et al. (22 total)
**Published:** 2025-05-08
**Type:** Survey paper
**Source:** https://arxiv.org/pdf/2505.04921

---

## The Four-Stage Roadmap

The survey's organizing framework distinguishes four historical and prospective stages of multimodal reasoning:

**Stage 1 — Perception-Driven Modular Reasoning.** Task-specific CNN/LSTM pipelines where reasoning was implicit and decomposed into separate representation, alignment, fusion, and reasoning modules. No unified understanding; no generalizable chain of thought.

**Stage 2 — Language-Centric Short Reasoning (System-1).** [[themes/vision_language_models|Vision-Language Models]] achieved strong VQA and grounding performance via instruction tuning. But these models relied on surface-level pattern matching and static knowledge retrieval, failing at dynamic hypothesis generation, multi-step logical progression, and context-sensitive adaptation. Multimodal Chain-of-Thought (MCoT) at this stage remained short and reactive — effective for familiar or bounded tasks, not for abstraction or compositionality.

**Stage 3 — Language-Centric Long Reasoning (System-2).** The current frontier, subdivided into:
- *Cross-Modal Reasoning* — integrating visual, auditory, and programmatic cues
- *Multimodal-O1* — multi-stage CoT fine-tuning with MCTS/Beam Search (LLaVA-CoT, Mulberry, Marco-O1)
- *Multimodal-R1* — approximately 100 concurrent papers applying GRPO and DPO to multimodal LLMs across image, video, audio, GUI, and embodied modalities

**Stage 4 (prospective) — Native Large Multimodal Reasoning Models (N-LMRMs).** A paradigm where reasoning is natively emergent from omnimodal perception rather than retrofitted onto language representations. Not yet realized, but the survey's technical roadmap makes this its most forward-looking contribution.

---

## Current Capabilities

### What Works Now

[[themes/multimodal_models|Multimodal models]] deliver strong results in established domains:

- **Vision-language reasoning:** VQA, visual math, diagram/infographic interpretation, physical common sense, domain-specific reasoning in science and mathematics (maturity: broad production)
- **Multimodal Chain-of-Thought:** Step-by-step reasoning traces across text, images, audio, and video — improving cross-modal alignment without explicit task-specific supervision (maturity: broad production)
- **GUI navigation:** UI-TARS, SeeClick, InfiGUI-R1 execute multi-step tasks across web, desktop, and mobile environments via visual-language grounding (maturity: narrow production)
- **Audio understanding:** Large Audio-Language Models handle speech, environmental sounds, and music with evaluation across ASR, captioning, QA, and structure recognition (maturity: narrow production)
- **Text-to-image generation:** Complex compositional prompts, multi-turn editing, conditional generation with segmentation constraints (maturity: broad production)

### The GRPO Wave

The most significant empirical development catalogued by this survey is the transfer of [[themes/rl_for_llm_reasoning|DeepSeek-R1-style reinforcement learning]] to multimodal domains via GRPO. Roughly 100 concurrent papers applied this algorithm across:

- Mathematical geometry (R1-V, MM-EUREKA)
- Visual grounding and detection (VLM-R1, Visual-RFT, Seg-Zero)
- Video understanding (Video-R1, VideoChat-R1)
- Audio modalities (R1-Omni, AV-Reasoner)
- GUI automation (UI-TARS, InfiGUI-R1)
- Medical imaging at 2B–7B scale (Lingshu, Patho-R1)

This represents a genuine [[themes/reinforcement_learning|reinforcement learning]] breakthrough in scope — the rapid adoption across modalities and task types demonstrates that GRPO's rule-based reward formulation transfers effectively beyond text. However, a critical limitation remains: **the generalization that made DeepSeek-R1 remarkable in text has not occurred in multimodal settings.** Current multimodal GRPO work is confined to specific, verifiable closed-form tasks. Long-chain-of-thought abilities learned in mathematics have not propagated to general multimodal reasoning capability.

### OpenAI o3/o4-mini: Thinking With Images

[[themes/unified_multimodal_models|O3 and o4-mini]] pioneer a qualitatively new capability — native "thinking with images" within chain-of-thought, using tool calls (zoom, crop, flip, enhance) without separate specialized modules. Case studies from the survey demonstrate 8-minute reasoning chains on Chinese Civil Service Examination problems and structured visual puzzle solving. This is identified as a notable breakthrough, but the survey also documents significant failure modes that define the challenge ahead.

---

## Critical Limitations and Failure Modes

### Quantitative Benchmarks Reveal the Gap

The survey grounds its diagnosis in hard numbers:

- **OmniMMI** (streaming video, interactive reasoning): Even Gemini-1.5-Pro and GPT-4o achieve **less than 20% average accuracy**
- **WorldSense AVQA** (audio-video QA): Claude 3.5 Sonnet achieves only **35%**; best open-source model achieves only **25%**
- **BrowseComp** (complex web research): GPT-4o achieves **0.6%** alone, **1.9%** with browsing tools; OpenAI Deep Research reaches 51.5% via iterative tool calling
- **Multi-modality scaling** (BabelBench, OmnixR): Performance degrades sharply as the number of simultaneous modalities increases — all models show steep drops at 3+ modalities

### The Language-Centric Bottleneck

The survey's central structural argument is that the language-centric architecture which enabled current capabilities is simultaneously the primary bottleneck blocking the next generation. All reasoning is serialized through language token representations. Visual, audio, and other modalities are processed as inputs to a language system rather than as first-class reasoning substrates. The consequences:

- **Visual-centric long reasoning** (3D spatial understanding, complex visual information-seeking) remains critically underdeveloped
- **Interactive multimodal reasoning** (dynamic cross-modal dialogue, iterative feedback loops) is absent in practical systems
- **Omni-modal semantic alignment** — aligning abstract concepts across vision, audio, and text simultaneously — cannot be achieved through language mediation alone
- **Interleaved text-image generation during reasoning** is explicitly blocked: o3 can reason with images as input but cannot generate visual outputs as part of the reasoning process

### O3's Failure Modes as Diagnostic Data

The survey uses o3 case studies not just to demonstrate capability but to characterize the failure modes that define Stage 4 challenges:

- **Language prior overrides visual evidence:** o3 misidentifies a six-finger image as the standard four-finger + thumb emoji — linguistic knowledge interferes with direct visual perception
- **Fabricated chain-of-thought:** o3 constructs plausible but incorrect rationales for potentially correct answers — a deception risk distinct from hallucination in the final answer
- **Document hallucination:** Phone numbers parsed from resume PDFs can be incorrect; project experiences are fabricated by reusing content from other contexts

### Evaluation System Weaknesses

The survey identifies structural problems in how the field measures progress:

- **LLM-as-judge circularity:** Scoring by GPT-4o systematically favors outputs resembling GPT-4o's training distribution
- **Multiple-choice inflation:** Option-based evaluation deviates significantly from real-world open-ended interaction, likely overestimating practical capability
- **Benchmark contamination:** No mechanisms exist to detect whether models are gaming evaluations through memorization or targeted training — the trajectory here is *worsening*
- **Single-model evaluation limits:** No single model reliably evaluates all modalities without specialized tool augmentation

---

## The N-LMRM Vision and Technical Roadmap

The survey's prospective Stage 4 concept — Native Large Multimodal Reasoning Models — is characterized by two transformative capabilities:

**Multimodal Agentic Reasoning:** Hierarchical task decomposition, real-time strategy adjustment via environmental feedback, and closed-loop embodied learning. The current generation produces extended reasoning chains only in static settings; N-LMRMs would engage real-time iterative interaction with dynamic environments.

**Omni-Modal Understanding and Generative Reasoning:** A unified representational space for heterogeneous data fusion — not language as intermediary but modality-agnostic inference and contextual multimodal generation (e.g., generating diagrams from spoken instructions, synthesizing video narratives from text descriptions).

Technical pathways proposed:
- MoE architectures with modality-specialized experts for unified representation
- Interleaved multimodal long chain-of-thought as a new test-time compute scaling axis
- Continuous lifelong learning from world experiences via MCP/A2A protocols and online RL
- Data synthesis pipelines for 3+ modality alignment and multimodal interactive reasoning chains

---

## Open Bottlenecks

The survey's landscape analysis converges on a set of interrelated structural bottlenecks:

| Bottleneck | What It Blocks | Horizon |
|---|---|---|
| Language-centric architecture | Visual-centric reasoning, omni-modal generation, Stage 4 N-LMRMs | 3–5 years |
| RL generalization from narrow verifiable tasks | Broadly capable RL-trained multimodal models | 3–5 years |
| Absence of omni-modal semantic integration | Any-modal alignment, cross-modal ambiguity resolution | 3–5 years |
| Long-horizon interactive planning in dynamic environments | Autonomous agents with real-world environmental feedback | 1–2 years |
| High-quality 3+ modality training data | N-LMRM pre-training infrastructure | 1–2 years |
| Interleaved multimodal chain-of-thought | New axis of inference-time compute scaling | 1–2 years |
| Unified architecture without negative cross-modal interference | N-LMRM omni-modal processing | 1–2 years |
| No open-world real-time evaluation environments | Validation of agents that generalize beyond controlled simulation | 1–2 years |

The language-centric bottleneck appears at multiple levels simultaneously — as an architectural constraint, a training data constraint, and an evaluation constraint — suggesting the transition to N-LMRMs requires co-evolution across all three.

---

## Notable Absence: Safety and Reliability

Despite surveying approximately 700 papers, this work makes no mention of safety, adversarial robustness, or hallucination in multimodal reasoning chains as research priorities. For a survey that documents fabricated chain-of-thought, language-prior override of visual evidence, and document hallucination in o3, the absence of reliability analysis as a landscape dimension is conspicuous. This gap is itself informative about where the field's attention is currently concentrated — and where it arguably should shift.

---

## Related Themes

- [[themes/multimodal_models|Multimodal Models]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/unified_multimodal_models|Unified Multimodal Models]]
- [[themes/vision_language_models|Vision-Language Models]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/geneval|GenEval]]
- [[entities/mmbench|MMBench]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
- [[entities/scienceqa|ScienceQA]]
- [[entities/system-2-reasoning|System-2 Reasoning]]
- [[entities/vqav2|VQAV2]]
- [[entities/webarena|WebArena]]
