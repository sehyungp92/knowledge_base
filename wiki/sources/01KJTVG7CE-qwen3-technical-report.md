---
type: source
title: Qwen3 Technical Report
source_id: 01KJTVG7CET7J5XXHBCER2A9J8
source_type: paper
authors:
- An Yang
- Anfeng Li
- Baosong Yang
- Beichen Zhang
- Binyuan Hui
- Bo Zheng
- Bowen Yu
- Chang Gao
- Chengen Huang
- Chenxu Lv
- Chujie Zheng
- Dayiheng Liu
- Fan Zhou
- Fei Huang
- Feng Hu
- Hao Ge
- Haoran Wei
- Huan Lin
- Jialong Tang
- Jian Yang
- Jianhong Tu
- Jianwei Zhang
- Jianxin Yang
- Jiaxi Yang
- Jing Zhou
- Jingren Zhou
- Junyang Lin
- Kai Dang
- Keqin Bao
- Kexin Yang
- Le Yu
- Lianghao Deng
- Mei Li
- Mingfeng Xue
- Mingze Li
- Pei Zhang
- Peng Wang
- Qin Zhu
- Rui Men
- Ruize Gao
- Shixuan Liu
- Shuang Luo
- Tianhao Li
- Tianyi Tang
- Wenbiao Yin
- Xingzhang Ren
- Xinyu Wang
- Xinyu Zhang
- Xuancheng Ren
- Yang Fan
- Yang Su
- Yichang Zhang
- Yinger Zhang
- Yu Wan
- Yuqiong Liu
- Zekun Wang
- Zeyu Cui
- Zhenru Zhang
- Zhipeng Zhou
- Zihan Qiu
published_at: '2025-05-14 00:00:00'
theme_ids:
- adaptive_computation
- finetuning_and_distillation
- model_architecture
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Qwen3 Technical Report

**Authors:** An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, Zihan Qiu
**Published:** 2025-05-14 00:00:00
**Type:** paper

## Analysis

# Qwen3 Technical Report
2025-05-14 · paper · An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui et al. (60 total)
https://arxiv.org/pdf/2505.09388

---

### Motivation & Prior Limitations

- Existing model ecosystems forced users to choose between distinct chat-optimized models (e.g., GPT-4o) and dedicated reasoning models (e.g., QwQ-32B), creating deployment friction and preventing dynamic adaptation to task complexity within a single system.
  - Switching between models requires separate infrastructure, increases operational cost, and prevents fine-grained control over reasoning depth per query.

- Prior open-source multilingual models had severely constrained language coverage: Qwen2.5 supported only 29 languages, leaving the majority of the world's languages without competitive model support.
  - This limited global deployment potential and cross-lingual transfer, particularly for low-resource languages where high-quality training data is scarce.

- Inference-time compute scaling ("test-time compute") lacked a practical user-facing control mechanism: models either performed full chain-of-thought reasoning or none, with no mechanism to allocate a specific token budget to balance latency vs. accuracy.
  - Existing reasoning models like o3 and DeepSeek-R1 demonstrated inference-time scaling benefits but did not expose fine-grained budget control to users.

- Training smaller reasoning-capable models from scratch via reinforcement learning was prohibitively expensive, limiting the democratization of reasoning capabilities to large-scale model deployments.
  - There was no established efficient pathway for distilling unified thinking/non-thinking capability into sub-14B models without full four-stage training.

---

### Proposed Approach

- Qwen3 unifies thinking mode (long chain-of-thought reasoning) and non-thinking mode (direct response) within a single model via a four-stage post-training pipeline: (1) Long-CoT Cold Start, (2) Reasoning RL, (3) Thinking Mode Fusion, (4) General RL.
  - Thinking mode is activated by a `/think` flag in the chat template; non-thinking mode by `/no think`; the model defaults to thinking mode and handles multi-turn dialogues with mixed flags by following the last flag encountered.
  - The thinking budget mechanism works by interrupting the thinking process at a user-defined token threshold and injecting the stop-thinking instruction `"Considering the limited time by the user, I have to give the solution based on the thinking directly now.\n</think>.\n\n"` — this capability emerges from Thinking Mode Fusion without being explicitly trained.

- Pre-training uses a three-stage curriculum on 36 trillion tokens across 119 languages: a general stage (30T tokens, 4K context), a reasoning-intensive STEM/code stage (~5T higher-quality tokens), and a long-context stage (hundreds of billions of tokens at 32K context with YARN + Dual Chunk Attention for 4× inference length extrapolation).
  - Data expansion leverages Qwen2.5-VL to extract text from PDF documents, then Qwen2.5 to refine it, generating trillions of additional tokens; domain-specific synthesis uses Qwen2.5-Math and Qwen2.5-Coder.
  - Instance-level data mixture optimization (via ablation on proxy models with fine-grained labels) replaces coarser domain-level mixing used in prior work.

- The Reasoning RL stage (Stage 2) uses GRPO on 3,995 carefully filtered query-verifier pairs satisfying four criteria: not used in cold-start, learnable by the cold-start model, maximally challenging, and domain-diverse.
  - Training stability is achieved by controlling model entropy to increase steadily or remain stable, enabling consistent reward improvements over 170 RL steps without manual hyperparameter intervention (e.g., Qwen3-235B-A22B's AIME'24 score rises from 70.1 to 85.1 across this run).

- Strong-to-Weak Distillation replaces full four-stage training for lightweight models (0.6B–14B dense; 30B-A3B MoE), combining off-policy distillation (teacher outputs in both modes) followed by on-policy distillation (KL divergence minimization between student logits and teacher logits from Qwen3-32B or Qwen3-235B-A22B).
  - This achieves the same capability profile as full RL training at approximately 1/10 the GPU hours (1,800 vs. 17,920 GPU hours for the 8B model), with higher Pass@1 and notably improved Pass@64 — indicating broader exploration capacity, not just exploitation.

- General RL (Stage 4) employs a reward system covering 20+ tasks with three reward types: rule-based (for instruction following and format adherence), model-based with reference (Qwen2.5-72B-Instruct as judge), and model-based without reference (trained reward model from human preference data).
  - Agent capability is trained via multi-turn RL rollouts with real environment execution feedback, targeting long-horizon decision-making stability.

---

### Results & Capabilities

- The flagship Qwen3-235B-A22B (Thinking) achieves state-of-the-art open-source performance, outperforming DeepSeek-R1 on 17/23 benchmarks with only 60% of its activated parameters (22B vs. 37B) and 35% of total parameters (235B vs. 671B).
  - Key scores: AIME'24 85.7, AIME'25 81.5, LiveCodeBench v5 70.7, CodeForces 2056 (98.2th percentile), BFCL v3 70.8, AutoLogi 89.0 — competitive with or exceeding closed-source Gemini 2.5 Pro and OpenAI-o1 on most reasoning-demanding tasks.

- The thinking budget mechanism produces smooth, monotonic performance scaling: increasing allocated thinking tokens yields consistent improvements across mathematics, coding, and STEM benchmarks, and the paper notes further gains are expected if output length is extended beyond 32K (left as future work).
  - This is the first open-source demonstration of user-controllable inference-time compute scaling in a unified thinking/non-thinking model.

- Qwen3-32B (Thinking) surpasses QwQ-32B (the prior SOTA 32B reasoning model) on 17/23 benchmarks, including AIME'24 (81.4 vs. 79.5), AIME'25 (72.9

## Key Claims

1. Qwen3 integrates thinking mode and non-thinking mode into a single unified model, eliminating the need to switch between separate chat and reasoning models.
2. Qwen3 introduces a thinking budget mechanism that allows users to allocate computational resources adaptively during inference, balancing latency and performance based on task complexity.
3. Qwen3 expands multilingual support from 29 to 119 languages and dialects compared to its predecessor Qwen2.5.
4. Qwen3 is pre-trained on approximately 36 trillion tokens covering 119 languages and dialects.
5. The flagship model Qwen3-235B-A22B achieves 85.7 on AIME'24, 81.5 on AIME'25, 70.7 on LiveCodeBench v5, and 70.8 on BFCL v3.
6. Increasing the thinking budget for thinking tokens leads to consistent improvement in model performance across various tasks.
7. Qwen3 removes QKV-bias used in Qwen2 and introduces QK-Norm to the attention mechanism to ensure stable training.
8. Qwen3 MoE models have 128 total experts with 8 activated experts per token and exclude shared experts, unlike Qwen2.5-MoE.
9. Qwen3 pre-training follows a three-stage process: a general stage on 30T tokens, a reasoning stage on 5T higher-quality tokens, and a long-context stage extending sequence length to 32,768 tokens.
10. Qwen3 optimizes data mixture at the instance level through ablation experiments on small proxy models, unlike prior work that optimizes at the data source or domain level.

## Capabilities

- Single model integrating both thinking (long-CoT reasoning) and non-thinking (fast response) modes with dynamic switching via chat template flags, eliminating need to maintain separate model families
- User-controllable thinking budget mechanism enabling adaptive inference compute allocation, with emergent graceful degradation when reasoning is interrupted mid-process — not explicitly trained, arising naturally from mode fusion
- Open-source LLM pre-trained natively on 119 languages and dialects (up from 29 in Qwen2.5), achieving competitive multilingual benchmarks (MGSM 83.53, MMMLU 86.70 for flagship)
- MoE architecture achieving performance parity with dense models at only 1/5 activated parameters — and parity with the prior-generation Qwen2.5 dense baseline at 1/10 activated parameters
- Strong-to-weak distillation (off-policy and on-policy logit transfer) produces reasoning capabilities in small models that surpass full four-stage RL training at 1/10 the GPU cost, with better Pass@1 and Pass@64
- Open-source model achieving 85.7 on AIME'24, 81.5 on AIME'25, 70.7 on LiveCodeBench v5, and 70.8 on BFCL v3 — competitive with frontier proprietary models (o1, o3-mini, DeepSeek-V3)
- GRPO-based reasoning RL achieving monotonically consistent improvement over 170 training steps without manual hyperparameter intervention — AIME'24 score rising from 70.1 to 85.1 in a single uninterrupted run
- Dense model generation-over-generation efficiency gain: Qwen3-32B matches or exceeds Qwen2.5-72B on 10/15 benchmarks — strong generation-over-generation gains achievable at less than half the parameter count
- Instance-level data mixture optimization using fine-grained labels (educational value, domain, safety) across 30+ trillion tokens, outperforming prior source/domain-level mixture strategies
- VLM-based PDF extraction pipeline generating trillions of additional high-quality pre-training tokens from document sources, scaling training corpora beyond web crawl limits

## Limitations

- Thinking budget enforcement is implemented via blunt external truncation — inserting a hardcoded stop-thinking instruction — not through model-native principled stopping; model must produce an answer based on incomplete reasoning
- Cold-start data pipeline retains a human-in-the-loop dependency: when the strongest available reasoning model (QwQ-32B) consistently fails, human annotators must assess response accuracy — frontier problems cannot be automated
- Current SOTA reasoning models (QwQ-32B) require extensive post-hoc output filtering to produce training-quality CoT data — they naturally and frequently generate repetition, thinking-summary inconsistencies, guesswork masquerading as reasoning, and cross-lingual stylistic shifts
- RL-based reasoning training is restricted to verifiable domains — the entire Reasoning RL stage used only 3,995 query-verifier pairs, all in math/coding, leaving open-ended and cross-domain reasoning untouched by RL signal
- Full four-stage RL post-training is computationally prohibitive for small/edge models — only flagship models receive RL treatment; all smaller models fall back to distillation, making RL-native reasoning inaccessible below a certain scale
- Small edge models (0.6B–1.7B) show severe multilingual capability degradation — MGSM drops to 31–51 vs 83+ for the flagship, and INCLUDE benchmark performance collapses — the 119-language coverage does not transfer to small model scale
- Long context window (128K tokens) relies on extrapolation via YARN + Dual Chunk Attention beyond the 32K training context — the extended window is an inference-time engineering workaround, not a natively trained capability
- Multi-turn dialog mode selection is heuristic — model follows the last /think or /no think flag encountered rather than autonomously detecting query complexity; no task-aware reasoning about which mode fits the actual question
- Thinking mode SFT data (Stage 3) is generated via rejection sampling from the Stage 2 model itself — creating a ceiling where the Stage 3 model can only learn reasoning styles already present in Stage 2 outputs, potentially locking in suboptimal CoT patterns
- General RL reward system covers only ~20 hand-crafted task categories — scientific reasoning, long-horizon planning, and creative problem-solving are conspicuously absent from the reward coverage, leaving these domains outside RL-driven improvement
- Synthetic pre-training data generation relies on earlier Qwen2.5 family models (Qwen2.5, Qwen2.5-Math, Qwen2.5-Coder) — synthetic data quality is bounded by teacher model capability, creating a potential quality ceiling as Qwen3 trains on Qwen2.5-generated data

## Bottlenecks

- Separate model deployment for reasoning vs. chat creates infrastructure overhead and integration complexity — developers must route requests across two model families, doubling serving costs and complicating context management
- Full RL post-training pipeline is compute-prohibitive below flagship scale — the four-stage process (cold start, reasoning RL, mode fusion, general RL) is inaccessible for models under ~30B, creating a structural gap in RL-quality reasoning for edge deployment
- Instance-level annotation of trillion-token multilingual training corpora requires specialised infrastructure and labelling capacity that is inaccessible to most of the research community — a prerequisite bottleneck for frontier multilingual model training

## Breakthroughs

- Open-source single unified model (0.6B–235B) with controllable thinking/non-thinking modes and thinking budget, confirmed at production scale — commoditising a capability previously exclusive to proprietary frontier models
- Strong-to-weak distillation demonstrated to outperform full RL training for small models at 1/10 GPU cost — establishing a scalable, economically viable pathway for distributing frontier reasoning capabilities across all model scales
- MoE architecture achieving performance parity with prior-generation dense baseline at 1/10 activated parameters — a 10× inference efficiency gain without quality loss, demonstrated at scale across multiple benchmark categories

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/grpo|GRPO]]
- [[entities/grouped-query-attention|Grouped Query Attention]]
- [[entities/qk-norm|QK-Norm]]
- [[entities/thinking-mode|Thinking Mode]]
- [[entities/yarn|YARN]]
