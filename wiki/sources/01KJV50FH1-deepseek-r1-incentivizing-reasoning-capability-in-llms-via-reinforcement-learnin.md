---
type: source
title: 'DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement
  Learning'
source_id: 01KJV50FH1MQXMHQ5PN1HY1V5H
source_type: paper
authors:
- DeepSeek-AI
- Daya Guo
- Dejian Yang
- Haowei Zhang
- Junxiao Song
- Peiyi Wang
- Qihao Zhu
- Runxin Xu
- Ruoyu Zhang
- Shirong Ma
- Xiao Bi
- Xiaokang Zhang
- Xingkai Yu
- Yu Wu
- Z. F. Wu
- Zhibin Gou
- Zhihong Shao
- Zhuoshu Li
- Ziyi Gao
- Aixin Liu
- Bing Xue
- Bingxuan Wang
- Bochao Wu
- Bei Feng
- Chengda Lu
- Chenggang Zhao
- Chengqi Deng
- Chenyu Zhang
- Chong Ruan
- Damai Dai
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
- Honghui Ding
- Huajian Xin
- Huazuo Gao
- Hui Qu
- Hui Li
- Jianzhong Guo
- Jiashi Li
- Jiawei Wang
- Jingchang Chen
- Jingyang Yuan
- Junjie Qiu
- Junlong Li
- J. L. Cai
- Jiaqi Ni
- Jian Liang
- Jin Chen
- Kai Dong
- Kai Hu
- Kaige Gao
- Kang Guan
- Kexin Huang
- Kuai Yu
- Lean Wang
- Lecong Zhang
- Liang Zhao
- Litong Wang
- Liyue Zhang
- Lei Xu
- Leyi Xia
- Mingchuan Zhang
- Minghua Zhang
- Minghui Tang
- Meng Li
- Miaojun Wang
- Mingming Li
- Ning Tian
- Panpan Huang
- Peng Zhang
- Qiancheng Wang
- Qinyu Chen
- Qiushi Du
- Ruiqi Ge
- Ruisong Zhang
- Ruizhe Pan
- Runji Wang
- R. J. Chen
- R. L. Jin
- Ruyi Chen
- Shanghao Lu
- Shangyan Zhou
- Shanhuang Chen
- Shengfeng Ye
- Shiyu Wang
- Shuiping Yu
- Shunfeng Zhou
- Shuting Pan
- S. S. Li
- Shuang Zhou
- Shaoqing Wu
- Shengfeng Ye
- Tao Yun
- Tian Pei
- Tianyu Sun
- T. Wang
- Wangding Zeng
- Wanjia Zhao
- Wen Liu
- Wenfeng Liang
- Wenjun Gao
- Wenqin Yu
- Wentao Zhang
- W. L. Xiao
- Wei An
- Xiaodong Liu
- Xiaohan Wang
- Xiaokang Chen
- Xiaotao Nie
- Xin Cheng
- Xin Liu
- Xin Xie
- Xingchao Liu
- Xinyu Yang
- Xinyuan Li
- Xuecheng Su
- Xuheng Lin
- X. Q. Li
- Xiangyue Jin
- Xiaojin Shen
- Xiaosha Chen
- Xiaowen Sun
- Xiaoxiang Wang
- Xinnan Song
- Xinyi Zhou
- Xianzu Wang
- Xinxia Shan
- Y. K. Li
- Y. Q. Wang
- Y. X. Wei
- Yang Zhang
- Yanhong Xu
- Yao Li
- Yao Zhao
- Yaofeng Sun
- Yaohui Wang
- Yi Yu
- Yichao Zhang
- Yifan Shi
- Yiliang Xiong
- Ying He
- Yishi Piao
- Yisong Wang
- Yixuan Tan
- Yiyang Ma
- Yiyuan Liu
- Yongqiang Guo
- Yuan Ou
- Yuduan Wang
- Yue Gong
- Yuheng Zou
- Yujia He
- Yunfan Xiong
- Yuxiang Luo
- Yuxiang You
- Yuxuan Liu
- Yuyang Zhou
- Y. X. Zhu
- Yanhong Xu
- Yanping Huang
- Yaohui Li
- Yi Zheng
- Yuchen Zhu
- Yunxian Ma
- Ying Tang
- Yukun Zha
- Yuting Yan
- Z. Z. Ren
- Zehui Ren
- Zhangli Sha
- Zhe Fu
- Zhean Xu
- Zhenda Xie
- Zhengyan Zhang
- Zhewen Hao
- Zhicheng Ma
- Zhigang Yan
- Zhiyu Wu
- Zihui Gu
- Zijia Zhu
- Zijun Liu
- Zilin Li
- Ziwei Xie
- Ziyang Song
- Zizheng Pan
- Zhen Huang
- Zhipeng Xu
- Zhongyu Zhang
- Zhen Zhang
published_at: '2025-01-22 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

**Authors:** DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, Zhen Zhang
**Published:** 2025-01-22 00:00:00
**Type:** paper

## Analysis

# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
2025-01-22 · paper · DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song et al. (200 total)
https://arxiv.org/pdf/2501.12948

---

### Motivation & Prior Limitations
- Existing approaches to LLM reasoning rely heavily on human-annotated chain-of-thought demonstrations, which introduces scalability bottlenecks and cognitive biases that cap model performance at human-level reasoning quality.
  - SFT on human reasoning traces constrains models to replicate human thought patterns, preventing exploration of superior non-human-like reasoning pathways.
  - Human-annotated CoT trajectories often omit critical reasoning components like explicit reflection and verification steps, making them suboptimal training targets.
- Neural reward models used in RLHF-style training are susceptible to reward hacking at large scale and require expensive retraining, adding pipeline complexity.
  - The authors observed that outcome-based and process-based neural RMs are unreliable under large-scale RL, motivating a rule-based alternative for verifiable domains.
- Prior test-time scaling methods (majority voting, MCTS) lack dynamic allocation of compute per problem complexity, leading to inefficient token usage across tasks of varying difficulty.

---

### Proposed Approach
- DeepSeek-R1-Zero trains reasoning capabilities via pure reinforcement learning (GRPO) on top of DeepSeek-V3-Base, with no supervised fine-tuning phase, using only correctness-based rule rewards on verifiable tasks (math, code, logic).
  - This bypasses human-annotated reasoning traces entirely; the reward signal is solely based on final answer correctness against ground truth, plus a format reward enforcing `<think>...</think>` tags.
  - GRPO (Group Relative Policy Optimization) replaces PPO's value model by sampling a group of G outputs per question and computing advantages via within-group reward normalization, reducing resource consumption while maintaining stable optimization.
- DeepSeek-R1 extends R1-Zero through a four-stage multi-stage pipeline: (1) cold-start SFT on thousands of human-aligned long-CoT examples, (2) first RL stage with rule-based rewards and a language consistency reward, (3) rejection sampling + SFT on both reasoning and non-reasoning data, (4) second RL stage combining rule-based rewards, learned helpfulness/safety reward models, and language consistency rewards.
  - The cold-start data addresses R1-Zero's readability and language-mixing failures before RL amplifies those behaviors further.
  - The final RL stage limits model-based preference reward training to the last 400 of 1,700 steps, because extended preference reward training was observed to cause reward hacking (documented in Supplementary B.5).
- Distilled smaller models (multiple sizes) are trained via SFT on long-CoT trajectories sampled from DeepSeek-R1, enabling capability transfer without requiring the full RL pipeline.
  - The distillation approach demonstrates that reasoning patterns discovered through large-scale RL can bootstrap smaller models to outperform their original instruction-tuned counterparts.

---

### Results & Capabilities
- DeepSeek-R1-Zero, trained with pure RL and no SFT, raises AIME 2024 pass@1 from 15.6% to 77.9%, reaching 86.7% with self-consistency (cons@16), surpassing average human competitor performance.
  - This gain emerges purely from RL without any human reasoning demonstrations, and is accompanied by spontaneous development of self-reflection, verification, and exploration of alternative solution strategies.
  - An "aha moment" is observed mid-training where the model abruptly increases use of reflective language (e.g., "wait"), marking a discrete phase transition in reasoning behavior.
- DeepSeek-R1 achieves a Codeforces rating of 2029 (96.3rd percentile), 49.2% on SWE-Bench Verified, 65.9% on LiveCodeBench, and 97.3% on MATH-500.
  - On AlpacaEval 2.0 (LC win-rate), DeepSeek-R1 reaches 87.6%, and 92.3% on ArenaHard — improvements of ~25% and ~17% respectively over Dev3, attributable to the final mixed RL stage.
- The model spontaneously learns to allocate longer thinking chains to harder problems, with average response length on training problems growing steadily throughout RL from hundreds to tens of thousands of tokens, driven purely by intrinsic adaptation.
- The multi-stage pipeline shows measurable capability tradeoffs at each stage: Dev1 improves instruction-following (IF-Eval 71.7% vs. R1-Zero 46.6%) but degrades AIME performance (59.0% vs. 77.9%) due to limited cold-start data; Dev2 recovers reasoning with strong GPQA Diamond and coding gains; Dev3 and the final RL stage close the gap on general-purpose benchmarks.

---

### Implications
- Pure RL on verifiable tasks can elicit advanced reasoning behaviors (self-reflection, verification, dynamic strategy adaptation) without human-authored reasoning demonstrations, suggesting that the bottleneck for reasoning capability is reward signal quality and compute — not human annotation bandwidth.
- The "aha moment" phenomenon — where qualitatively new reasoning patterns emerge discontinuously during RL — is empirically documented for the first time at scale, providing evidence that emergent cognitive-like behaviors can arise from outcome-only optimization pressure.
- Rule-based reward design (correctness verifiers, compiler test cases) appears sufficient for verifiable reasoning domains and avoids reward hacking that plagues neural RMs, pointing toward verifiability as the key axis along which RL-based capability development can reliably scale.
- Distillation from RL-trained long-CoT models to smaller models establishes a viable pathway for democratizing frontier reasoning capabilities, with the distilled models outperforming their direct instruction-tuned counterparts — implying that RL-discovered reasoning traces are higher quality training signal than human demonstrations.

## Key Claims

1. Reasoning abilities of LLMs can be incentivized through pure reinforcement learning without human-labeled reasoning trajectories
2. Pure RL training facilitates emergent development of advanced reasoning patterns including self-reflection, verification, and dynamic strategy adaptation
3. Models trained via RL on verifiable tasks surpass counterparts trained via conventional supervised learning on human demonstrations
4. Emergent reasoning patterns from large-scale RL models can be systematically distilled to enhance reasoning capabilities of smaller models
5. Conventional SFT approaches to reasoning constrain models to human thought processes, inherently capping performance and preventing exploration of superior non-human reasoning pathways
6. DeepSeek-R1-Zero uses GRPO with rewards based solely on correctness of final predictions, without constraints on the reasoning process itself
7. DeepSeek-R1-Zero bypasses conventional SFT before RL training, based on the hypothesis that human-defined reasoning patterns may limit model exploration
8. DeepSeek-R1-Zero's AIME 2024 pass@1 score improved from 15.6% to 77.9% through RL training alone
9. DeepSeek-R1-Zero achieves 86.7% on AIME 2024 with self-consistency decoding (cons@16), significantly surpassing average human competitor performance
10. DeepSeek-R1-Zero naturally increases its thinking time (response length) throughout training via intrinsic adaptation, without external modifications

## Capabilities

- Pure reinforcement learning without any SFT phase induces emergent sophisticated reasoning behaviors in LLMs — self-reflection, verification, and dynamic strategy adaptation — starting from a base checkpoint alone
- Multi-stage RL + SFT pipeline achieves frontier-level reasoning performance: 79.8% pass@1 on AIME 2024, 97.3% on MATH-500, Codeforces 2029 rating (96.3 percentile), 49.2% on SWE-Bench Verified, 92.3 on ArenaHard
- Rule-based reward systems (accuracy + format rewards) enable reliable large-scale RL training for mathematical and coding tasks without neural reward model exploitation
- LLM reasoning capabilities can be effectively distilled from large RL-trained models into smaller models, producing reasoning abilities that surpass those models' original instruction-tuned counterparts
- RL-trained reasoning models naturally develop dynamic compute allocation at inference — allocating fewer tokens to simple problems and more tokens to complex ones without explicit programming
- GRPO (Group Relative Policy Optimization) enables scalable LLM RL training by eliminating the separate value model required by PPO, significantly reducing resource consumption
- Self-consistency decoding with 16 samples improves reasoning performance significantly: DeepSeek-R1-Zero improves from 77.9% to 86.7% pass rate on AIME 2024, surpassing average human competitors
- Cold-start SFT followed by RL enables models to develop both human-readable, aligned reasoning chains AND strong reasoning capability simultaneously — resolving the readability vs. capability tradeoff of pure RL

## Limitations

- Pure RL training (without SFT) produces models with poor readability and language mixing — combining English and Chinese within a single chain-of-thought response
- Pure RL training (R1-Zero) has limited performance on non-reasoning generative tasks — writing, open-domain QA — due to narrow focus on verifiable rule-based reward domains
- DeepSeek-R1 structural output capabilities are suboptimal and the model cannot leverage external tools such as search engines and calculators to improve output
- DeepSeek-R1 exhibits overthinking on simple questions — excessive reasoning tokens allocated to tasks not requiring them, reducing token efficiency
- DeepSeek-R1 is optimized only for Chinese and English; queries in other languages cause language mixing — the model may reason and respond in English even when the query is in another language
- DeepSeek-R1 is highly sensitive to prompt engineering — few-shot prompting consistently degrades performance compared to zero-shot
- Large-scale RL has not been applied to software engineering tasks — long evaluation cycles make RL training impractical, limiting SWE improvement to supervised approaches
- Neural reward models are susceptible to reward hacking at scale — as RL training progresses, policy models discover adversarial shortcuts to exploit imperfect neural reward functions
- Pure RL methods cannot scale to tasks without reliable verifiers — writing, creative, and complex agentic tasks lack ground-truth reward mechanisms that resist hacking
- DeepSeek-R1 has only moderate inherent safety — vulnerable to jailbreak attacks where enhanced reasoning capabilities produce more operationally feasible dangerous content (e.g., manufacturing instructions)
- Open-source model weights are vulnerable to downstream fine-tuning that strips safety alignment — releasing weights enables actors to remove safety protections
- Language consistency reward causes a small but measurable degradation in raw reasoning performance — human preference alignment trades off against capability
- Model-based preference reward leads to reward hacking with extended training — the second RL stage limits general preference rewards to only the final 400 of 1700 steps to control exploitation
- SFT on human demonstrations impedes exploration of optimal reasoning strategies — human-provided responses omit critical reasoning components like explicit reflection and verification steps, capping model reasoning at human-level patterns
- DeepSeek-R1 achieves only 30.1% on SimpleQA — strong reasoning performance does not transfer to factual recall accuracy, suggesting reasoning and grounding are largely orthogonal capabilities
- Limited cold-start data causes a reasoning performance regression in early pipeline stages — Dev1 shows degradation versus R1-Zero on AIME, suggesting insufficient high-quality cold-start data disrupts previously developed capabilities
- Pre-training data contamination with AI-generated text — web crawl data contains significant volumes of OpenAI model-generated answers, introducing invisible indirect knowledge distillation from proprietary models into ostensibly independent training
- RL training shows discontinuous performance jumps at specific checkpoints tied to hyperparameter changes — non-monotonic training dynamics indicate training stability is sensitive to maximum response length and other hyperparameters

## Bottlenecks

- Long evaluation cycles for software engineering tasks make RL training impractical — running test suites to grade code correctness is too slow to fit within RL rollout loops, blocking RL-based improvement of software engineering agents beyond supervised baselines
- Absence of reliable verifiers for open-ended generative tasks (writing, creative, multi-step agentic) is the fundamental barrier preventing pure RL scaling beyond verifiable math and code domains
- Neural reward models become exploitable within hundreds of RL training steps at scale — policy models discover adversarial shortcuts faster than reward models can be retrained, imposing hard practical limits on RL training duration for preference-based objectives

## Breakthroughs

- Pure RL from a base LLM checkpoint (with no SFT phase) induces emergent advanced reasoning behaviors — including spontaneous self-reflection, verification, and dynamic strategy switching — enabling AIME 2024 performance that surpasses average human competitors
- Open-source multi-stage RL pipeline achieves performance on par with OpenAI o1 across major reasoning benchmarks — 79.8% AIME 2024, 97.3% MATH-500, Codeforces 2029 rating — breaking the implicit monopoly of closed labs on frontier reasoning capability
- Reasoning capabilities from large RL-trained models can be effectively distilled into small models via supervised distillation, producing small models that surpass original instruction-tuned counterparts — demonstrating that reasoning need not be re-discovered from scratch at smaller scale

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/arenahard|ArenaHard]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/long-chain-of-thought|Long Chain-of-Thought]]
- [[entities/multi-head-latent-attention|Multi-Head Latent Attention]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/overthinking|Overthinking]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/rejection-sampling|Rejection Sampling]]
- [[entities/rejection-sampling-fine-tuning|Rejection Sampling Fine-Tuning]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/self-consistency-decoding|Self-Consistency Decoding]]
