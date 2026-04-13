---
type: source
title: 'Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning'
source_id: 01KJTXS7VE3H4C50SP28CMVYP8
source_type: paper
authors:
- Peiyu Wang
- Yichen Wei
- Yi Peng
- Xiaokun Wang
- Weijie Qiu
- Wei Shen
- Tianyidan Xie
- Jiangbo Pei
- Jianhao Zhang
- Yunzhuo Hao
- Xuchen Song
- Yang Liu
- Yahui Zhou
published_at: '2025-04-23 00:00:00'
theme_ids:
- alignment_and_safety
- hallucination_and_reliability
- multimodal_models
- policy_optimization
- reinforcement_learning
- rl_for_llm_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning

**Authors:** Peiyu Wang, Yichen Wei, Yi Peng, Xiaokun Wang, Weijie Qiu, Wei Shen, Tianyidan Xie, Jiangbo Pei, Jianhao Zhang, Yunzhuo Hao, Xuchen Song, Yang Liu, Yahui Zhou
**Published:** 2025-04-23 00:00:00
**Type:** paper

## Analysis

# Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning
2025-04-23 · paper · Chris, Yichen Wei, Yi Peng, Xiaokun Wang, Weijie Qiu et al. (13 total)
https://arxiv.org/pdf/2504.16656

---

### Motivation & Prior Limitations
- Extending "slow-thinking" reinforcement learning strategies to multimodal domains degrades performance on general visual tasks even as it improves visual reasoning benchmarks, creating a fundamental specialization-generalization tension that prior work failed to resolve.
  - Models optimized for mathematical reasoning via RL show performance gains on MMMU and MathVision but concurrent degradation on general perception benchmarks like AI2D, accompanied by increased visual hallucination rates.
  - Standard SFT prior to RL inadvertently undermines subsequent reasoning development, yet removing it entirely leaves the visual-language alignment problem unsolved.
- GRPO, the dominant RL algorithm for reasoning, suffers from a "Vanishing Advantages" problem where candidate responses within a query group converge to uniform correctness or incorrectness, causing advantage signals to collapse and halting effective policy updates.
  - Effective training samples (those with non-zero advantages) drop from ~60% at training start to under 40% in later phases, severely degrading gradient density and training efficiency.
- Existing preference optimization techniques for multimodal models treat preference pairs as binary, failing to capture the nuanced progression of complex reasoning paths where multiple valid solution trajectories exist; reward models also predominantly evaluate textual quality in isolation, ignoring the visual-logical relationship central to multimodal reasoning.

---

### Proposed Approach
- Skywork R1V2 introduces a hybrid reinforcement learning paradigm that sequentially applies Mixed Preference Optimization (MPO) followed by GRPO with a hybrid reward signal, bypassing SFT entirely by using a modular adapter to bridge a frozen vision encoder (InternViT-6B) with a pretrained reasoning language model (QwQ-32B).
  - Rather than distilling from a teacher model or applying SFT, R1V2 connects components modularly: a lightweight MLP adapter fc maps frozen visual features fv(xv) into the language model's representation space, preserving the LLM's intrinsic reasoning capability while grounding it visually.
  - Adapter-only training (leaving both the vision encoder and LLM frozen) proved empirically superior to joint LLM+adapter or adapter+vision-encoder configurations, suggesting cross-modal alignment is the critical bottleneck rather than visual encoding quality.
- MPO unifies three loss terms — a DPO-style relative preference loss Lpreference, a BCO-style absolute quality loss Lquality (with a moving-average reward baseline δ for stability), and a generation NLL loss Lgeneration — guided by the Skywork-VL reward model to reduce hallucination and overthinking before RL begins.
  - MPO combines reward-model signals from Skywork-VL with hand-crafted rule-based constraints (format correctness, factual consistency, step-by-step completeness), producing a hybrid reward structure that aligns outputs across both stylistic and factual dimensions.
- GRPO is augmented with a hybrid reward function r(x, yi) = rrule + rθ + rformat, where rθ is the Skywork-VL preference reward introduced specifically to mitigate the "alignment tax" that pure rule-based RL imposes on reasoning ability.
- The Selective Sample Buffer (SSB) addresses vanishing advantages by caching high-value samples with non-zero advantage signals and reintroducing them during policy updates via weighted sampling proportional to absolute advantage magnitude, maintaining gradient density throughout training.
  - SSB is applied not only during policy updates but also at offline inference time to pre-filter the prompt pool, yielding over 10% improvement in training efficiency during the initial optimization phase.
  - Calibrated MPO reward thresholds are monitored throughout training to prevent excessive reinforcement signals from inducing visual hallucinations, with threshold 15 producing more stable dynamics than lower values.

---

### Results & Capabilities
- R1V2 (38B parameters) achieves state-of-the-art performance among open-source models across both text and multimodal reasoning benchmarks: 78.9% on AIME2024, 63.6% on LiveCodeBench, 73.2% on LiveBench, 82.9% on IFEVAL, 66.3% on BFCL, 73.6% on MMMU, 74.0% on MathVista, 62.6% on OlympiadBench, 49.0% on MathVision, and 52.0% on MMMU-Pro.
  - These results represent large gains over predecessor R1V1: +6.9pp on AIME24, +6.4pp on LiveCodeBench, +18.6pp on LiveBench, +10.4pp on IFEVAL, +12.8pp on BFCL.
- R1V2 outperforms models 2.9× its size: it surpasses Qwen2.5-VL-72B by 3.4pp on MMMU (73.6% vs. 70.2%) and by 22.2pp on OlympiadBench (62.6% vs. 40.4%), and surpasses QvQ-Preview-72B by 29.4pp on OlympiadBench (62.6% vs. 33.2%).
  - On AIME2024, R1V2 (78.9%) outperforms OpenAI-o1 (74.3%) and approaches DeepSeek-R1-671B (79.8%), a model with 17.6× more parameters.
- The MPO stage substantially reduces hallucination rates: standard SFT yields 18.4% hallucination, MPO alone reduces this to 8.7%, and the full MPO+GRPO hybrid settles at 9.1%, while SFT degrades mathematical reasoning (70.0% on AIME24) compared to MPO (79.0%) or the hybrid (78.9%).
- The SSB mechanism maintains effective training sample proportion above 60% versus below 40% without it, and its ablation shows a modest but consistent improvement on MMMU (73.6 vs. 73.4) while sustaining MathVision performance.
- Qualitative evaluation on Chinese Gaokao physics and mathematics problems demonstrates R1V2's ability to apply physical principles systematically (e.g., correctly identifying that AC frequency depends on rotational speed rather than coil turns), decompose 3D geometry problems into coordinate-system subproblems, and perform explicit self-verification of intermediate steps.
- On general vision 

## Key Claims

1. Excessive reinforcement signals can induce visual hallucinations in vision-language models.
2. Slow-thinking multimodal models demonstrate over 30% improvement on benchmarks like AIME24 and AMC23 compared to fast-thinking counterparts.
3. R1V2 acquires multimodal reasoning skills directly via reinforcement learning without teacher model distillation.
4. Models optimized heavily for mathematical reasoning often demonstrate degraded performance on everyday visual tasks, while general-purpose models struggle with complex analytical reasoning.
5. Applying preference optimization to complex multimodal reasoning remains relatively underexplored due to two critical limitations: binary preference pairs fail to capture complex reasoning paths, and 
6. R1V2 eliminates the supervised fine-tuning (SFT) stage, unlike its predecessor R1V1, because SFT can inadvertently undermine subsequent reinforcement learning and reasoning processes.
7. Cross-modal alignment rather than visual encoding represents the critical bottleneck in multimodal reasoning.
8. Capabilities in text and vision exhibit high transferability — improvements in one modality directly benefit the other.
9. MPO reduces repetitive chain-of-thought and overthinking artifacts in model outputs.
10. The GRPO vanishing advantages phenomenon arises when all responses within a query group converge toward uniform correctness or incorrectness, causing relative advantage signals to diminish and impedin

## Capabilities

- Open-source 38B multimodal reasoning model trained purely via RL without SFT achieves 78.9% on AIME2024, 73.6% on MMMU, and 62.6% on OlympiadBench — outperforming 72B+ open-source models and competitive with proprietary systems
- Mixed Preference Optimization (MPO) applied before GRPO reduces VLM hallucination from 18.4% (SFT baseline) to 8.7%, while simultaneously improving reasoning benchmark scores — functioning as both alignment and hallucination mitigation
- Selective Sample Buffer (SSB) mechanism maintains >60% effective (non-zero advantage) training samples throughout GRPO training versus <40% without it, yielding >10% training efficiency improvement by caching high-advantage examples
- Adapter-only training (MLP bridge between frozen vision encoder and frozen LLM) outperforms joint LLM+adapter and adapter+vision-encoder configurations for multimodal reasoning alignment — confirming cross-modal bridging as the primary lever
- Cross-modal reasoning transfer: RL improvements to text reasoning capabilities directly improve visual reasoning performance without modality-specific training, and vice versa

## Limitations

- Slow-thinking / extended reasoning applied to VLMs systematically degrades performance on general visual perception benchmarks (e.g., AI2D) even as it improves mathematical and scientific reasoning scores
- Aggressive RL reward signals for visual reasoning induce visual hallucinations — a direct and measurable trade-off between reasoning depth and factual grounding in VLMs
- GRPO training efficiency collapses in later training phases: effective (non-zero advantage) samples drop from ~60% to under 40% as responses converge, starving the gradient signal and blocking continued improvement
- SFT applied before RL training systematically undermines subsequent reasoning performance in VLMs — the two paradigms are antagonistic, forcing a binary choice between warm-up convenience and reasoning ceiling
- Removing SFT to preserve reasoning capability introduces a reduction in general visual understanding performance — the no-SFT design is a deliberate trade-off, not a free lunch
- MPO reward threshold sensitivity causes reward hacking and performance collapse at lower thresholds: MMMU accuracy peaks at 73.6% then degrades to 68.9% over continued training when threshold is too low
- Hybrid MPO+GRPO slightly increases hallucination rate versus MPO alone (9.1% vs 8.7%) — adding GRPO for reasoning introduces a small but measurable factual accuracy regression
- Training the vision encoder provides minimal additional benefit over adapter-only training — the vision encoder's representation quality is already saturated for downstream reasoning tasks, and its gradient updates may even interfere
- Open-source multimodal reasoning models still trail top proprietary systems significantly: OpenAI-o4-mini scores 81.6 vs 73.6 on MMMU and 93.4 vs 78.9 on AIME2024 — a ~8-15 point gap that pure RL innovations have not closed
- Video understanding performance is notably weak relative to the model's image and text reasoning strengths — VideoMME (60.2%) and MVBench (61.5%) scores are described only as 'acceptable', with no analysis of the gap
- No discussion of inference latency, computational cost, or deployment requirements despite the 38B parameter scale and 64K token generation length — practical serving constraints are a conspicuous absence
- Evaluation contamination risk is not discussed: the model trained extensively on AIME-style competition mathematics and olympiad problems, yet those same problem types constitute the primary evaluation benchmarks

## Bottlenecks

- Cross-modal alignment (not visual encoding) is the primary architectural bottleneck for multimodal reasoning — improving visual encoding produces negligible gains while improving the bridge adapter unlocks reasoning performance
- Reasoning-generalization trade-off in VLMs: no current training strategy simultaneously achieves state-of-the-art specialized reasoning and general visual perception — optimizing one degrades the other
- Vanishing advantages in GRPO training block sustained VLM RL optimization: effective training samples drop from ~60% to <40% as responses converge, creating a hard efficiency ceiling without explicit sample management
- Reward threshold calibration in iterative preference optimization for VLMs has no principled solution: thresholds that are too low cause reward hacking and performance collapse; thresholds too high slow convergence — manual search required per task

## Breakthroughs

- Hybrid MPO+GRPO+SSB training pipeline achieves a new Pareto frontier for open-source VLMs: a 38B model outperforms 72B+ open-source models on reasoning benchmarks while maintaining competitive general understanding — previously believed to require either much larger scale or inevitable capability tr
- Selective Sample Buffer (SSB) mechanism empirically resolves the vanishing advantages problem in GRPO by caching and reinjecting high-advantage samples, maintaining >60% effective training samples versus <40% baseline throughout training

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/pass1|Pass@1]]
- [[entities/qwq-32b|QwQ-32B]]
