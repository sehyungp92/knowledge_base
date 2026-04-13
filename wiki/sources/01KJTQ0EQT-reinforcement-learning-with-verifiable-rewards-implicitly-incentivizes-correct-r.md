---
type: source
title: Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct
  Reasoning in Base LLMs
source_id: 01KJTQ0EQT3NPZSQAZ4D1D8SJA
source_type: paper
authors:
- Xumeng Wen
- Zihan Liu
- Shun Zheng
- Shengyu Ye
- Zhirong Wu
- Yang Wang
- Zhijian Xu
- Xiao Liang
- Junjie Li
- Ziming Miao
- Jiang Bian
- Mao Yang
published_at: '2025-06-17 00:00:00'
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs

**Authors:** Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang, Junjie Li, Ziming Miao, Jiang Bian, Mao Yang
**Published:** 2025-06-17 00:00:00
**Type:** paper

## Analysis

# Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
2025-06-17 · paper · Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu et al. (12 total)
https://arxiv.org/pdf/2506.14245

---

### Motivation & Prior Limitations
- A prominent hypothesis (Yue et al., 2025) emerged suggesting that RLVR does not genuinely expand reasoning capacity but merely improves sampling efficiency — specifically, that all correct reasoning paths already exist in the base model and RLVR only adjusts their sampling probabilities.
  - The key evidence was that Pass@K of the base LLM increases faster than its RLVR-tuned counterpart, eventually matching or surpassing the post-RLVR model at moderately large K, which appeared to imply RLVR reduces overall reasoning capacity while boosting Pass@1.
  - Contradictory findings from multiple groups (Liu et al., 2025a; Chen et al., 2025b; Shojaee et al., 2025) had gone unresolved, with no systematic framework able to reconcile them.
- The standard Pass@K metric is unreliable for evaluating math reasoning because base LLMs can produce incorrect chain-of-thought (CoT) reasoning yet coincidentally arrive at the correct numerical answer, particularly for hard problems with simple integer answers that are easy to guess with repeated sampling.
  - This metric conflation masked genuine differences in reasoning quality between base and post-RLVR models, causing the capability boundary expansion to go undetected in prior analyses.

---

### Proposed Approach
- The paper introduces CoT-Pass@K, a refined evaluation metric that counts a sample as successful only when both the final answer and the intermediate reasoning CoT are verified correct, separating genuine reasoning success from lucky guessing.
  - CoT correctness at scale is assessed using an LLM-as-a-CoT-Judge paradigm with DeepSeek-R1-0528-Qwen3-8B as a lightweight verifier, applied multiple times per CoT with three aggregation strategies: any-correct, all-correct, and majority-correct.
- The paper provides a formal theorem (Theorem 1) proving that GRPO implicitly incentivizes correct reasoning even when rewards are based solely on final answer correctness, requiring no explicit CoT supervision.
  - The proof rests on a "Logic Prior" assumption: that pre-trained LLMs assign higher conditional probability of a correct answer given a correct CoT than given an incorrect one (α > β), a condition satisfied once the model has internalized strong knowledge and logic priors from pre-training.
  - Under this assumption, the expected GRPO advantage is provably positive for correct CoTs and negative for incorrect CoTs, causing the probability of generating correct CoTs (p_c^θ) to increase monotonically across training steps.
- Training dynamics are analyzed by reproducing DAPO-style GRPO training on Qwen2.5-32B and tracking per-prompt indicators P(CA) (fraction of correct answers) and P(CC|CA) (fraction of correct CoTs among correct answers) throughout training.
- CoT quality is independently validated by using post-RLVR CoT data as SFT training signal: if supervised fine-tuning on that data produces better generalization, the CoTs are considered high quality — providing a model-learning perspective on CoT quality orthogonal to automated verification.

---

### Results & Capabilities
- Using CoT-Pass@K, DAPO-Qwen-32B (post-RLVR from Qwen2.5-32B base) shows a consistent and significant performance gap over the base model across all K values up to 1024 on AIME 2024 and AIME 2025, directly contradicting the sampling-efficiency-only hypothesis under standard Pass@K.
  - The gap is most pronounced on AIME 2025, which was released after the base model's training cutoff and is therefore free from data contamination, making it the cleanest signal of genuine extended reasoning capability.
- For competitive coding tasks, AceReason-Nemotron-7B (post-RLVR from DeepSeek-R1-Distill-Qwen-7B) shows clear Pass@K improvements over its distilled pre-RLVR counterpart across all six versions of LiveCodeBench (v1–v6), confirming that RLVR can extend reasoning boundaries even for models that already demonstrate strong reasoning via distillation.
  - Only medium and hard problems contribute to differentiation at large K, underscoring that benchmark difficulty is a prerequisite for detecting capability boundary effects.
- Training dynamics confirm that P(CC|CA) improves substantially during DAPO training even as P(CA) saturates toward 1.0, empirically validating that RLVR incentivizes correct CoTs implicitly and from the earliest training steps.
- SFT on DAPO CoT data nearly replicates the Pass@1 performance of the full DAPO-Qwen-32B model, demonstrating that the quality of incentivized CoTs is high enough that supervised distillation from them can replicate expensive RLVR training — and that such high-quality CoTs cannot be directly sampled from the base model without RLVR first having improved them.
- Even CoT data labeled as "incorrect" (containing verifiable reasoning errors) improves in quality over the course of RLVR training when measured by downstream SFT generalization, suggesting that overall CoT structure improves even when individual steps remain imperfect.

---

### Implications
- The paper resolves a high-profile debate in the RLVR community by demonstrating that the sampling-efficiency-only hypothesis is an artifact of using a metric (Pass@K on final answers) that is insensitive to reasoning quality, not a fundamental limitation of RLVR — this reframes what evaluation benchmarks and metrics are necessary for studying test-time compute scaling.
- The theoretical result that GRPO implicitly incentivizes correct reasoning without explicit CoT supervision suggests that answer-only verifiable rewards are sufficient to drive genuine reasoning improvement, with implications for reward model design and the scope of RLHF/RLVR for tasks where intermediate step verification is expensive or impossible.

## Key Claims

1. RLVR can extend the reasoning capability boundary for both mathematical and coding tasks, going beyond mere improvements in sampling efficiency.
2. The hypothesis that RLVR merely improves sampling efficiency without expanding reasoning capacity—because all correct reasoning paths are already present in the base model—is challenged by contradicto
3. Pass@K is an unreliable evaluation metric for math reasoning because base LLMs can produce incorrect chain-of-thought reasoning yet coincidentally arrive at the correct answer, especially for hard pro
4. CoT-Pass@K reveals a consistent and significant performance gap between DAPO-Qwen-32B and Qwen2.5-32B on AIME 2024 and AIME 2025 across all values of K up to 1024, which is not visible using standard 
5. On benchmarks such as MATH-500 and AMC23, RLVR effects are less pronounced because base LLMs can already solve these problems correctly with sufficient sampling attempts.
6. RLVR shows no improvement on the Minerva benchmark due to a train-test domain mismatch, as DAPO training data was restricted to math problems with integer answers while Minerva contains physics proble
7. For code reasoning, Pass@K is a reliable metric because code execution verification significantly reduces the likelihood of guessing, unlike math where answer tokens can be coincidentally correct.
8. AceReason-Nemotron-7B shows clear Pass@K improvements over its pre-RLVR counterpart DeepSeek-R1-Distill-Qwen-7B on most LiveCodeBench versions, demonstrating that RLVR can extend reasoning boundaries 
9. Only medium and hard problems in LiveCodeBench-v6 contribute to differentiation between post-RLVR and base models at large K values, underscoring the importance of selecting challenging benchmarks for
10. GRPO implicitly incentivizes correct reasoning: the expected GRPO advantage is positive for correct CoTs and negative for incorrect CoTs, causing the probability of generating correct CoTs to increase

## Capabilities

- RLVR (via GRPO/DAPO) genuinely extends the reasoning capability boundary for both math and competitive coding tasks beyond what Pass@K on answer correctness reveals — demonstrated by a persistent CoT-Pass@K gap that holds across all K values up to 1024 on AIME 2024 and 2025
- SFT on RLVR-generated reasoning CoTs can replicate the Pass@1 performance of a post-RLVR model without the heavy RL training compute cost — high-quality CoT data generated by RLVR serves as a transferable supervision signal
- LLM-as-a-CoT-Judge paradigm — using a specialized lightweight reasoning model (DeepSeek-R1-0528-Qwen3-8B) to verify intermediate reasoning chain correctness at scale for unstructured math problems
- RLVR training implicitly incentivizes correct reasoning from the very first training steps, with generalization improvements in both Pass@K and CoT-Pass@K observable at early checkpoints (step 30 onward)

## Limitations

- High compute cost of RLVR training restricts most research to models ≤32B parameters, leaving the regime of very large models essentially unexplored
- Standard Pass@K metric computed on answer correctness alone is systematically unreliable for evaluating RLVR's effect on mathematical reasoning — base LLMs can guess correct answers via incorrect CoTs, masking genuine reasoning capability differences
- RLVR provides no improvement on benchmarks with training-domain mismatch — DAPO-trained on integer-answer math problems shows zero improvement on Minerva (physics free-form answers)
- RLVR optimization reaches a ceiling where fully-optimized training questions can no longer provide valid GRPO gradient signal (all-correct groups), yet approximately 30% of generated CoTs remain incorrect — imperfect reasoning behaviors cannot be mitigated with answer-correctness reward alone
- RLVR can unintentionally reinforce incorrect reasoning chains and harmful biases when the Logic Prior assumption fails — model biases and knowledge errors from pre-training may be amplified rather than corrected
- RLVR's theoretical framework (Theorem 1) provides no formal generalization guarantee — the mechanism explaining why training improves is decoupled from any proof that improvements transfer to held-out problems
- Verifying CoT correctness at scale requires expensive LLM-based judgment — prohibitive cost of manual inspection forces reliance on an LLM verifier whose own reliability is uncertain and must be validated
- RLVR effects on simple or potentially contaminated benchmarks (MATH-500, AMC23) are undetectable — the method cannot distinguish whether base model performance is due to genuine capability or training data leakage
- LLM-based CoT verifiers have unknown and potentially variable reliability — the study notes a pressing need for benchmark design to assess verifier reliability, implying current verifiers are not yet trustworthy enough for unsupervised deployment

## Bottlenecks

- Standard outcome-only evaluation metrics (Pass@K on answer correctness) are structurally incapable of detecting genuine RLVR-induced reasoning improvements in math domains, creating a measurement bottleneck that has produced contradictory research findings and delayed scientific consensus
- RLVR training on a fixed dataset eventually exhausts learnable signal as questions become fully optimized (P(CA)→1), leaving residual imperfect CoTs that cannot be corrected through answer-correctness reward alone — creating a hard ceiling on CoT quality improvement via pure RLVR

## Breakthroughs

- First formal theoretical proof (Theorem 1) that GRPO implicitly incentivizes correct reasoning even when rewards are based solely on answer correctness — showing that pre-trained LLMs' logic priors cause the GRPO gradient to systematically increase correct CoT probability
- SFT on RLVR-generated CoT data can nearly replicate the Pass@1 performance of the full RLVR-trained model — demonstrating that RLVR's reasoning improvements are encodable in a static dataset and transferable via cheap supervised learning

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/cot-passk|CoT-Pass@k]]
- [[entities/deepseek-r1-distill-qwen-7b|DeepSeek-R1-Distill-Qwen-7B]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/minerva|Minerva]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
- [[entities/passk|pass@k]]
