---
type: source
title: DeepSeek-V3 Technical Report
source_id: 01KJV5S7TQ43GW6XHHXNQ6EFCD
source_type: paper
authors:
- DeepSeek-AI
- Aixin Liu
- Bei Feng
- Bing Xue
- Bingxuan Wang
- Bochao Wu
- Chengda Lu
- Chenggang Zhao
- Chengqi Deng
- Chenyu Zhang
- Chong Ruan
- Damai Dai
- Daya Guo
- Dejian Yang
- Deli Chen
- Dongjie Ji
- Erhang Li
- Fangyun Lin
- Fucong Dai
- Fuli Luo
- Guangbo Hao
- Guanting Chen
- Guowei Li
- H. Zhang
- Han Bao
- Hanwei Xu
- Haocheng Wang
- Haowei Zhang
- Honghui Ding
- Huajian Xin
- Huazuo Gao
- Hui Li
- Hui Qu
- J. L. Cai
- Jian Liang
- Jianzhong Guo
- Jiaqi Ni
- Jiashi Li
- Jiawei Wang
- Jin Chen
- Jingchang Chen
- Jingyang Yuan
- Junjie Qiu
- Junlong Li
- Junxiao Song
- Kai Dong
- Kai Hu
- Kaige Gao
- Kang Guan
- Kexin Huang
- Kuai Yu
- Lean Wang
- Lecong Zhang
- Lei Xu
- Leyi Xia
- Liang Zhao
- Litong Wang
- Liyue Zhang
- Meng Li
- Miaojun Wang
- Mingchuan Zhang
- Minghua Zhang
- Minghui Tang
- Mingming Li
- Ning Tian
- Panpan Huang
- Peiyi Wang
- Peng Zhang
- Qiancheng Wang
- Qihao Zhu
- Qinyu Chen
- Qiushi Du
- R. J. Chen
- R. L. Jin
- Ruiqi Ge
- Ruisong Zhang
- Ruizhe Pan
- Runji Wang
- Runxin Xu
- Ruoyu Zhang
- Ruyi Chen
- S. S. Li
- Shanghao Lu
- Shangyan Zhou
- Shanhuang Chen
- Shaoqing Wu
- Shengfeng Ye
- Shengfeng Ye
- Shirong Ma
- Shiyu Wang
- Shuang Zhou
- Shuiping Yu
- Shunfeng Zhou
- Shuting Pan
- T. Wang
- Tao Yun
- Tian Pei
- Tianyu Sun
- W. L. Xiao
- Wangding Zeng
- Wanjia Zhao
- Wei An
- Wen Liu
- Wenfeng Liang
- Wenjun Gao
- Wenqin Yu
- Wentao Zhang
- X. Q. Li
- Xiangyue Jin
- Xianzu Wang
- Xiao Bi
- Xiaodong Liu
- Xiaohan Wang
- Xiaojin Shen
- Xiaokang Chen
- Xiaokang Zhang
- Xiaosha Chen
- Xiaotao Nie
- Xiaowen Sun
- Xiaoxiang Wang
- Xin Cheng
- Xin Liu
- Xin Xie
- Xingchao Liu
- Xingkai Yu
- Xinnan Song
- Xinxia Shan
- Xinyi Zhou
- Xinyu Yang
- Xinyuan Li
- Xuecheng Su
- Xuheng Lin
- Y. K. Li
- Y. Q. Wang
- Y. X. Wei
- Y. X. Zhu
- Yang Zhang
- Yanhong Xu
- Yanhong Xu
- Yanping Huang
- Yao Li
- Yao Zhao
- Yaofeng Sun
- Yaohui Li
- Yaohui Wang
- Yi Yu
- Yi Zheng
- Yichao Zhang
- Yifan Shi
- Yiliang Xiong
- Ying He
- Ying Tang
- Yishi Piao
- Yisong Wang
- Yixuan Tan
- Yiyang Ma
- Yiyuan Liu
- Yongqiang Guo
- Yu Wu
- Yuan Ou
- Yuchen Zhu
- Yuduan Wang
- Yue Gong
- Yuheng Zou
- Yujia He
- Yukun Zha
- Yunfan Xiong
- Yunxian Ma
- Yuting Yan
- Yuxiang Luo
- Yuxiang You
- Yuxuan Liu
- Yuyang Zhou
- Z. F. Wu
- Z. Z. Ren
- Zehui Ren
- Zhangli Sha
- Zhe Fu
- Zhean Xu
- Zhen Huang
- Zhen Zhang
- Zhenda Xie
- Zhengyan Zhang
- Zhewen Hao
- Zhibin Gou
- Zhicheng Ma
- Zhigang Yan
- Zhihong Shao
- Zhipeng Xu
- Zhiyu Wu
- Zhongyu Zhang
- Zhuoshu Li
- Zihui Gu
- Zijia Zhu
- Zijun Liu
- Zilin Li
- Ziwei Xie
- Ziyang Song
- Ziyi Gao
- Zizheng Pan
published_at: '2024-12-27 00:00:00'
theme_ids:
- adaptive_computation
- ai_market_dynamics
- model_architecture
- model_commoditization_and_open_source
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DeepSeek-V3 Technical Report

DeepSeek-V3 is a 671B-parameter Mixture-of-Experts language model (37B activated per token) that achieves frontier-class performance across math, code, and reasoning benchmarks — matching GPT-4o and Claude-3.5-Sonnet on most tasks — while introducing three training innovations that collectively resolve longstanding MoE scaling barriers: auxiliary-loss-free load balancing, DualPipe pipeline parallelism, and fine-grained FP8 mixed-precision training validated at extreme scale for the first time.

**Authors:** DeepSeek-AI et al. (200 total)
**Published:** 2024-12-27
**Type:** Paper
**Themes:** [[themes/model_architecture|Model Architecture]] · [[themes/pretraining_and_scaling|Pretraining & Scaling]] · [[themes/scaling_laws|Scaling Laws]] · [[themes/adaptive_computation|Adaptive Computation]] · [[themes/model_commoditization_and_open_source|Model Commoditization & Open Source]] · [[themes/ai_market_dynamics|AI Market Dynamics]]

---

## Motivation

Prior to this work, the open-source frontier lagged substantially behind closed-source models on math, code, and reasoning. But more specifically, DeepSeek-V3 targets three structural problems that had blocked efficient MoE scaling:

**Load balancing without performance loss.** The conventional solution to expert routing collapse — auxiliary losses (GShard, Switch Transformer) — directly degrades model performance when the loss is too large, forcing an unresolvable trade-off. Sequence-wise auxiliary losses further suppress expert specialization by enforcing artificial balance at the sequence level.

**Cross-node communication bottlenecks.** Fine-grained expert parallelism across nodes over InfiniBand approaches a 1:1 compute-to-communication ratio, and existing pipeline methods (1F1B, ZeroBubble) cannot adequately hide this overhead.

**FP8 training at scale.** FP8 GEMM accumulation on H800 Tensor Cores is hardware-limited to ~14-bit precision, causing meaningful accuracy loss as inner dimension K grows. Prior FP8 frameworks relied on delayed, tensor-wise quantization that left precision on the table.

---

## Architecture

DeepSeek-V3 builds on the [[themes/model_architecture|MLA + DeepSeekMoE]] foundation from DeepSeek-V2, adding two novel training objectives.

**Multi-Head Latent Attention (MLA)** performs low-rank joint compression of attention keys and values, dramatically reducing KV cache during inference while maintaining performance comparable to standard Multi-Head Attention. This is a prerequisite for serving a 671B model economically.

**DeepSeekMoE** uses finer-grained experts than traditional architectures (GShard), isolating some experts as permanently shared while routing tokens across specialist experts. DeepSeek-V3 activates 37B of 671B parameters per token — a roughly 18:1 total-to-active ratio.

---

## Key Innovations

### Auxiliary-Loss-Free Load Balancing

Instead of penalizing imbalanced routing through a conflicting training objective, DeepSeek-V3 adds a **per-expert dynamic bias term** to affinity scores used *only* for routing decisions — not for gating weights. After each step, bias terms are adjusted based on observed expert load across the full batch.

This enforces **batch-wise** rather than sequence-wise balance, allowing experts to develop domain-specific routing patterns (specialization) while preventing collapse. A tiny complementary sequence-wise loss (α=0.0001) handles extreme within-sequence cases only.

> *"we pioneer an auxiliary-loss-free strategy for load balancing, which minimizes the performance degradation that arises from encouraging load balance"*

Ablations confirm: batch-wise balance achieves equivalent validation loss to the auxiliary-loss-free method (both 2.253 on 1B models), and both outperform sequence-wise auxiliary loss (2.258). The strategy is strictly superior across all model scales tested.

### Multi-Token Prediction (MTP)

DeepSeek-V3 predicts D=1 additional tokens beyond the next token using lightweight MTP modules that **share the main model's embedding and output head**, preserving the full causal chain at each prediction depth. Unlike Gloeckle et al. (2024)'s independent parallel heads, this sequential design maintains causal consistency and densifies the training signal.

At inference, MTP modules are repurposed for **speculative decoding** at no added cost: the second predicted token is accepted 85–90% of the time across generation topics, yielding **1.8× tokens per second**.

### DualPipe Pipeline Parallelism

DualPipe feeds micro-batches **bidirectionally** through the pipeline and decomposes each chunk into attention, dispatch, MLP, and combine sub-components that are manually interleaved, fully overlapping forward/backward computation with all-to-all communication.

- Reduces pipeline bubbles by ~half vs. 1F1B (bubble term scales as PP/2 − 1 rather than PP − 1)
- Cross-node all-to-all kernels route tokens over IB to same-index GPUs on target nodes, then NVLink intra-node — fully overlapping both fabrics
- Only **20 of 132 SMs** are required to saturate both IB and NVLink

> *"This overlap also ensures that, as the model further scales up, as long as we maintain a constant computation-to-communication ratio, we can still employ a larger cluster"*

The trade-off: DualPipe requires 2× model parameter copies and (1/PP + 1) activation overhead — acceptable at large EP sizes.

### FP8 Mixed Precision Training

DeepSeek-V3 validates FP8 training at 671B scale for the first time, achieving <0.25% relative loss error vs. BF16 baseline. Key departures from prior FP8 frameworks:

- **Fine-grained quantization**: 1×128 tile-wise for activations, 128×128 block-wise for weights (vs. tensor-wise)
- **Uniform E4M3** rather than E4M3/E5M2 split
- **Online (not delayed) quantization** with CUDA-Core FP32 promotion every NC=128 elements to counter hardware's ~14-bit accumulation limit
- Design explicitly aligned with NVIDIA Blackwell's microscaling format — forward-compatible

### Reasoning Capability Distillation

Post-training distills from DeepSeek-R1 (long-CoT) via a two-stage pipeline:
1. Train domain expert models using SFT+RL on R1-generated data with reflection/verification prompts
2. Rejection-sample from those experts to curate 1.5M SFT instances balancing accuracy with concise formatting

GRPO (Group Relative Policy Optimization) estimates the baseline from group scores rather than a separate critic, reducing memory/compute vs. PPO.

---

## Results

| Benchmark | DeepSeek-V3 | Claude-3.5-Sonnet | GPT-4o |
|---|---|---|---|
| MATH-500 | **90.2%** | 78.3% | 74.6% |
| AIME 2024 | **39.2%** | 16.0% | — |
| MMLU | **88.5** | — | — |
| MMLU-Pro | **75.9** | — | — |
| GPQA | **59.1** | — | — |
| SWE-bench Verified | 42.0% | **50.8%** | — |

- Outperforms all open-source models on a comprehensive benchmark suite
- Matches or approaches GPT-4o and Claude-3.5-Sonnet across most tasks
- Achieves state-of-the-art math performance **among non-long-CoT models**, including outperforming o1-preview on MATH-500
- Top-performing open-source model on coding competition benchmarks (LiveCodeBench)

**Training efficiency:** 2.788M H800 GPU hours total; 2.664M for pre-training on 14.8T tokens; completed in under two months. At $2/GPU-hour, estimated cost: **$5.576M**. Zero irrecoverable loss spikes or rollbacks during training.

---

## Limitations & Open Questions

### Performance Gaps

**English factual knowledge** remains a significant gap: DeepSeek-V3 trails GPT-4o and Claude-3.5-Sonnet on SimpleQA despite superiority on Chinese factual knowledge (C-SimpleQA). The source of this asymmetry is unexplained — whether it reflects pre-training data composition, tokenization, or post-training choices is unclear.

**Real-world software engineering** represents a persistent capability gap: SWE-bench Verified scores 42.0% vs. Claude-3.5-Sonnet's 50.8% — roughly 8.8 percentage points behind despite leading all other metrics. Agentic software engineering appears to require something beyond general coding ability that DeepSeek-V3 hasn't fully captured.

### Hardware & Infrastructure Constraints

**FP8 accumulation precision** on H800/Hopper Tensor Cores is hardware-limited to ~14-bit, causing up to ~2% maximum relative error. The software workaround (CUDA-Core promotion every 128 elements) requires reading BF16 activations from HBM, writing quantized FP8 back, then reading again — redundant memory transfers that cannot currently be fused. This bottleneck resolves only with next-generation hardware (Blackwell).

**Current GPUs lack native tile/block-wise quantization support.** Tensor Cores only support per-tensor scaling, forcing constant data movement between Tensor Cores and CUDA Cores for dequantization. Fine-grained quantization as a standard training primitive requires hardware support that doesn't yet exist on deployed clusters.

**SM allocation for MoE communication** dedicates 20 of 132 available SMs (~15%) to all-to-all routing, leaving Tensor Cores idle during communication phases. This represents a permanent throughput tax on current hardware that dedicated network co-processors or future chip designs would resolve.

**Deployment footprint is prohibitive for broad adoption.** The minimum inference deployment requires 40 nodes (320 H800 GPUs) for decoding alone. Even organizations with access to model weights face an infrastructure barrier that makes frontier-class MoE serving economically unviable outside hyperscalers. This is a [[themes/model_commoditization_and_open_source|fundamental democratization barrier]] that persists independent of model quality.

### Cost Transparency

The reported $5.576M training cost **explicitly excludes** prior R&D, failed runs, and ablation experiments. The true resource investment to reach this point — including DeepSeek-V2, failed MoE configurations, and infrastructure development — is substantially higher and undisclosed. This framing, while technically accurate, creates misleading comparisons with closed-source model training costs.

### DualPipe Memory Overhead

DualPipe requires maintaining **two full copies of model parameters** in GPU memory during training. Though manageable at large expert parallelism sizes (where model state is spread across many nodes), this doubles the parameter memory footprint and limits applicability to architectures where total parameter count is small relative to cluster memory.

---

## Connections & Implications

**Resolves the auxiliary loss dilemma in MoE.** The dynamic bias approach cleanly separates routing balance enforcement from the training objective, eliminating a conflict that has persisted since GShard. This should generalize beyond DeepSeek-V3 to any fine-grained MoE architecture. See [[themes/adaptive_computation|adaptive computation]] for broader context on dynamic routing.

**MTP + speculative decoding is a notable inference unlock.** The 1.8× decoding speedup with 85–90% acceptance rate comes essentially for free from the training objective — no separate speculative model required. This substantially improves the economics of serving a 671B model, partially offsetting the deployment footprint limitation.

**R1 → V3 distillation establishes a reusable pattern.** Transferring long-CoT reasoning capability into a standard autoregressive model without long-CoT inference overhead is a reproducible methodology: train experts on CoT data, rejection-sample into concise SFT. This likely becomes standard practice for future reasoning-capable base models. See [[themes/pretraining_and_scaling|pretraining and scaling]] for related capability transfer patterns.

**The cost efficiency claim reshapes [[themes/ai_market_dynamics|competitive dynamics]].** A frontier-class model trained for ~$5.576M — even understated — compresses the assumed cost differential between open and closed frontier development. Whether this reflects algorithmic efficiency (DualPipe, FP8) or infrastructure advantages (owned hardware, electricity costs) has significant implications for which organizations can realistically compete at the frontier.

**FP8 training at 671B scale paves a path to Blackwell.** The explicit alignment of fine-grained quantization tile sizes with NVIDIA's microscaling format suggests this is not an artifact of DeepSeek-V3's architecture but a forward-looking design decision. When native hardware support arrives, the software workarounds (CUDA-Core promotion, redundant HBM transfers) become unnecessary, yielding additional efficiency gains.

---

## Anticipations

- Native hardware support for tile/block-wise quantization (Blackwell microscaling) should eliminate the FP8 accumulation workaround, yielding additional efficiency gains measurable as reduced memory transfers per GEMM operation
- The auxiliary-loss-free dynamic bias approach should be adopted by other MoE training efforts given its clean theoretical motivation and demonstrated performance advantage
- Deployment footprint for 671B-class MoE will remain a practical barrier until inference serving infrastructure (disaggregated attention/MLP, speculative decoding at scale) matures sufficiently to reduce minimum viable GPU counts

## Key Concepts

- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/infiniband|InfiniBand]]
- [[entities/multi-head-latent-attention|Multi-Head Latent Attention]]
- [[entities/multi-token-prediction|Multi-Token Prediction]]
- [[entities/multi-token-prediction-mtp|Multi-Token Prediction (MTP)]]
- [[entities/nvlink|NVLink]]
- [[entities/speculative-decoding|Speculative Decoding]]
- [[entities/yarn|YARN]]
