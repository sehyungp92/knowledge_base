---
type: source
title: 'On Path to Multimodal Generalist: General-Level and General-Bench'
source_id: 01KJTWFJBZ1R2CNXHP7QK26YT4
source_type: paper
authors:
- Hao Fei
- Yuan Zhou
- Juncheng Li
- Xiangtai Li
- Qingshan Xu
- Bobo Li
- Shengqiong Wu
- Yaoting Wang
- Junbao Zhou
- Jiahao Meng
- Qingyu Shi
- Zhiyuan Zhou
- Liangtao Shi
- Minghe Gao
- Daoan Zhang
- Zhiqi Ge
- Weiming Wu
- Siliang Tang
- Kaihang Pan
- Yaobo Ye
- Haobo Yuan
- Tao Zhang
- Tianjie Ju
- Zixiang Meng
- Shilin Xu
- Liyu Jia
- Wentao Hu
- Meng Luo
- Jiebo Luo
- Tat-Seng Chua
- Shuicheng Yan
- Hanwang Zhang
published_at: '2025-05-07 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- multimodal_models
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# On Path to Multimodal Generalist: General-Level and General-Bench

This paper argues that the field's standard MLLM evaluation methodology is fundamentally broken — equating aggregate benchmark performance with generalist capability and AGI proximity — and proposes a corrective framework. It introduces **General-Level**, a five-tier synergy-based taxonomy for classifying multimodal generalists, and **General-Bench**, the most comprehensive multimodal evaluation benchmark to date (702 tasks, 325,800 instances across image, video, audio, 3D, and language). The central finding: no current model qualifies as a true multimodal generalist under rigorous synergy criteria, and the gap between "high benchmark scores" and genuine cross-modal intelligence is far larger than the field acknowledges.

**Authors:** Hao Fei, Yuan Zhou, Juncheng Li, Xiangtai Li, Qingshan Xu et al. (32 total)
**Published:** 2025-05-07
**Type:** Paper
**Themes:** [[themes/benchmark_design|Benchmark Design]] · [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] · [[themes/multimodal_models|Multimodal Models]] · [[themes/unified_multimodal_models|Unified Multimodal Models]]

---

## The Core Problem: What Benchmarks Actually Measure

The paper's diagnosis of current MLLM evaluation is pointed and specific. The prevailing paradigm has three structural failures:

**Format collapse.** Existing benchmarks (MME, MMMU, SEED-Bench, MMT-Bench, MEGA-Bench) convert all tasks into multiple-choice QA format. This means they can only assess comprehension — generation, editing, and native-format task prediction capabilities are entirely invisible to current leaderboards.

**Modality narrowness.** The majority of current benchmarks focus almost exclusively on image. Video, audio, 3D, and cross-modal combinations are severely underrepresented or absent, making leaderboard rankings systematically misleading about actual multimodal breadth.

**The super-agent loophole.** A pipeline assembling all SoTA specialist models into a routing agent would dominate every existing benchmark while possessing no genuine cross-modal intelligence. This exposes the core flaw: task-aggregate performance cannot distinguish true generalists from specialist ensembles.

> "it's effortless to assemble a 'super agent' from all singleton state-of-the-art (SoTA) specialists to achieve the above goal, while such a simplistic approach cannot achieve genuine AGI."

The practical consequence: GPT-4V and GPT-4o, which dominate existing leaderboards, support only 65.1% of image comprehension tasks in General-Bench and score **zero** on generation — meaning prior benchmarks have been masking serious coverage gaps.

---

## The General-Level Framework

General-Level defines **Synergy** as its organizing concept: the 1+1>2 effect where joint multimodal learning produces capabilities exceeding those of specialized models trained on individual tasks. This is operationalized practically — a generalist "demonstrates synergy" on a task if it surpasses the corresponding SoTA specialist, under the assumption that outperformance implies cross-task knowledge transfer.

The five levels, inspired by SAE's autonomous driving taxonomy:

| Level | Criterion | Current Status |
|-------|-----------|----------------|
| L1 | SoTA specialist performance | All specialists |
| L2 | Unified comprehension and/or generation with broad task coverage | Unified-io-2-XXL, AnyGPT lead |
| L3 | Cross-task synergy: generalist exceeds SoTA specialist on individual tasks | Sa2VA-26B, LLaVA-OneVision-72B, Qwen2-VL-72B |
| L4 | Synergy across both comprehension and generation (harmonic mean scored) | Only Mini-Gemini, Vitron-V1, Emu2-37B — all image-only |
| L5 | Total synergy including bidirectional language↔multimodal enhancement | **None found yet** |

The scoring system has proven mathematical properties: monotonic score decline across levels (S5 ≤ S4 ≤ S3 ≤ S2), anchoring only to specialist baselines (not peer generalists), and explicit incentives for both modality breadth and comprehension-generation balance.

---

## General-Bench

The benchmark dataset supporting General-Level evaluation:

- **702 tasks**, 145 skills, **325,800 instances**
- Modalities: image, video, audio, 3D, language
- 29 domains, both comprehension and generation tasks
- **58 distinct evaluation metrics** (not collapsed to accuracy)
- Original task formats preserved — not reformatted to MC-QA

This is the largest and most comprehensive MLLM benchmark to date, and the first to evaluate generation and comprehension within the same framework.

---

## Key Findings

### Coverage is far lower than assumed

Even frontier models support only a fraction of General-Bench tasks:

- GPT-4V and GPT-4o: 177 of 271 image comprehension tasks (65.1%), zero video/audio/3D coverage
- Sa2VA-8B (a top video model): 72.2% of video comprehension tasks
- Most models: near-zero support for audio and 3D

### Synergy is rare

The rate at which MLLMs outperform SoTA specialists is low across the board:

- Best closed-source win rates on image comprehension: GPT-4o, Gemini-1.5, Claude-3.5 at ~30%+
- Best open-source: Qwen2-VL-72B at 36.4%
- Level-4 achieved by only three models, all image-only
- Level-5: zero models

### Ranking inversions reveal what's being hidden

At Level-2 (which rewards modality breadth), Unified-io-2-XXL and AnyGPT outrank GPT-4o — because GPT-4o supports only image comprehension. The models that dominate existing leaderboards are systematically penalized once breadth and generation are required.

### Synergy patterns

Where synergy exists, it clusters among closely related tasks. Generation tasks show stronger synergy effects than comprehension within a modality. Cross-modal synergy is predominantly **unidirectional** — language enhances other modalities, not the reverse.

---

## Limitations and Open Problems

### Architectural ceiling: the pseudo-intelligence problem

The most structurally significant limitation: current MLLM architectures extend language reasoning to process other modalities rather than building native multimodal intelligence.

> "such an architectural setup merely simulates 'pseudo' multimodal intelligence, as it still fundamentally relies on the language intelligence of LLMs"

This means non-language modalities are permanently in service of language intelligence under current paradigms. The reverse direction — non-language modalities enhancing NLP task performance — has never been demonstrated in any model evaluated.

### The Level-5 barrier

Achieving Level-5 requires abductive cross-modal reasoning and modality-agnostic context consistency during inference. No current architectural approach provides this; the theoretical basis for how to achieve reverse cross-modal synergy remains unclear. This is assessed as a **blocking** limitation with a 3–5 year resolution horizon.

### Comprehension-generation optimization conflict

Joint training for unified comprehension and generation produces optimization conflicts — generation learning degrades comprehension performance. This is why Level-4 models are so rare and why all three that qualify (Mini-Gemini, Vitron-V1, Emu2-37B) achieve it only in the image modality.

### Pipeline architecture is structurally capped

Agent-based pipelines (LLM as scheduler invoking specialist modules) are bounded at specialist-level performance by construction — no feature sharing, no gradient propagation, no mechanism for cross-task transfer. They also suffer compounding error propagation with no correction mechanism.

### Evaluation blind spots

- **Modality imbalance in benchmark data:** image tasks vastly outnumber video/audio/3D, systematically biasing aggregate scores toward image-capable models
- **Computational prohibitiveness of video:** video tasks demand substantially more GPU memory and have far slower inference speeds, creating practical barriers to comprehensive evaluation
- **Benchmark saturation masked coverage gaps:** prior leaderboards obscured how little of multimodal space was actually being tested

---

## Implications for [[themes/benchmark_design|Benchmark Design]]

The paper makes an empirical case that the field's standard evaluation methodology has been misdirecting research investment. By rewarding narrow comprehension performance, existing benchmarks have:

1. Made specialist-aggregating pipelines look competitive with true generalists
2. Hidden the near-total absence of generation capability in frontier models
3. Created false confidence about progress toward multimodal AGI

The General-Level framework shifts the target from "highest score on fixed tasks" to "does this model actually transfer knowledge across modalities and tasks?" — a fundamentally different optimization objective with different architectural implications.

---

## Connections

- The "super agent" critique connects to broader debates about whether capability aggregation is meaningful progress — a pipeline that routes to specialists is not a generalist, regardless of aggregate performance
- The Level-5 barrier (language cannot yet be enhanced by multimodal learning) connects to [[themes/multimodal_models|multimodal model]] architecture debates about whether LLM-backbone designs are a fundamental constraint
- The comprehension-generation optimization conflict appears in unified model research broadly — see related work on Morph-Tokens and similar approaches attempting to bridge this gap
- The synergy operationalization (exceed specialist = demonstrate transfer) is a pragmatic approximation with known limitations: it cannot detect synergy in tasks where no specialist exists, and it conflates "outperformance" with "knowledge transfer" structurally

---

## Status Summary

The central contribution is the reframing: **the AGI proximity question for multimodal models cannot be answered by existing benchmarks**. Under rigorous synergy criteria, the frontier is at Level-3 (some cross-task transfer within a modality), with Level-4 (comprehension-generation parity) barely begun and Level-5 (bidirectional language-multimodal enhancement) entirely unachieved. The field is further from multimodal generalism than current leaderboard positions suggest.
