---
type: source
title: Reinforcement Learning for Reasoning in Large Language Models with One Training
  Example
source_id: 01KJTSHBZTMDFZH6C79ZKEPGJ7
source_type: paper
authors:
- Yiping Wang
- Qing Yang
- Zhiyuan Zeng
- Liliang Ren
- Liyuan Liu
- Baolin Peng
- Hao Cheng
- Xuehai He
- Kuan Wang
- Jianfeng Gao
- Weizhu Chen
- Shuohang Wang
- Simon Shaolei Du
- Yelong Shen
published_at: '2025-04-29 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
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
# Reinforcement Learning for Reasoning in Large Language Models with One Training Example

**Authors:** Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu, Baolin Peng, Hao Cheng, Xuehai He, Kuan Wang, Jianfeng Gao, Weizhu Chen, Shuohang Wang, Simon Shaolei Du, Yelong Shen
**Published:** 2025-04-29 00:00:00
**Type:** paper

## Analysis

# Reinforcement Learning for Reasoning in Large Language Models with One Training Example
2025-04-29 · paper · Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu et al. (14 total)
https://arxiv.org/pdf/2504.20571

---

### Motivation & Prior Limitations
- The data-centric aspects of RLVR (Reinforcement Learning with Verifiable Reward) remain underexplored despite substantial investment in refining RL algorithms such as PPO and GRPO, leaving open the fundamental question of how much training data RLVR actually requires.
  - Prior work such as LIMR proposed Learning Impact Measurement (LIM) to reduce training set size by sixfold, but did not explore how aggressively the dataset could be reduced, leaving the lower bound of data requirements unknown.
  - Critical questions about the specific role of data quantity, quality, and the mechanisms behind observed empirical phenomena (self-reflection, robust generalization) had not been rigorously addressed.
- The prevailing assumption was that RLVR's strong performance on mathematical reasoning benchmarks was attributable to the diversity and scale of training data (e.g., 1.2k–7.5k examples), obscuring how much improvement might stem from training signal structure rather than data volume.

---

### Proposed Approach
- The paper introduces 1-shot RLVR: training an LLM with RLVR using a single example, selected via a simple Historical Variance Score that ranks training examples by the variance of their per-epoch accuracy during a short preliminary training run on the full dataset.
  - The variance score (vi = var(si,1, ..., si,E)) reflects the consistency of reward signal across epochs; high-variance examples provide more informative gradient signal during RL training.
  - The selected single example is duplicated to fill the required batch size (128), and standard GRPO or PPO training proceeds with binary outcome reward, KL divergence loss, and an entropy loss term that incentivizes diverse exploration of reasoning paths.
- The approach differs from prior data selection work (e.g., LIMR) by pushing to an extreme reduction (single example) rather than moderate pruning, and by emphasizing the role of exploration (entropy loss) over dataset curation as the operative mechanism for generalization.

---

### Results & Capabilities
- A single training example elevates Qwen2.5-Math-1.5B from 36.0% to 73.6% on MATH500, and from 17.6% to 35.7% average across six mathematical reasoning benchmarks (MATH500, AIME24, AMC23, Minerva Math, OlympiadBench, AIME25), matching the performance of RLVR trained on the full 1.2k DeepScaleR subset (73.6% / 35.9%).
  - Two training examples further slightly exceed the 1.2k subset performance (MATH500: 74.8%, average: 36.6%), and match full MATH training set performance (average: 36.7%).
- The phenomenon of **post-saturation generalization** is identified: training accuracy on the single example saturates before step 100, yet test performance continues improving for hundreds to thousands of additional steps (e.g., +9.9% average gain for π13 from step 500 to step 2000), without overfitting test performance even when the training response degenerates into multilingual gibberish.
- Cross-category generalization is consistently observed: training on a single Geometry example (π13) improves Algebra, Number Theory, and Precalculus performance, and training on a single Algebra example (π1) improves across all MATH500 subcategories, suggesting that the learned capability is not category-specific reasoning but a more general reasoning mode.
- The effectiveness generalizes across models and algorithms: Qwen2.5-Math-7B 1-shot RLVR achieves +17.8% average improvement (5.9% above format-reward baseline); Llama-3.2-3B-Instruct 2-shot RLVR matches or slightly exceeds full-set RLVR; PPO produces comparable results to GRPO on Qwen2.5-Math-1.5B; DeepSeek-R1-Distill-Qwen-1.5B shows improvements with few-shot RLVR, though the gap with full-set is larger.
- 1-shot RLVR on math examples also improves non-mathematical reasoning (ARC-Easy: 55.8% vs. 48.0% base; ARC-Challenge: 33.4% vs. 30.2% base), outperforming full-set RLVR on these tasks, suggesting the effect is a general reasoning enhancement rather than math-specific tuning.
- Ablation confirms that **policy gradient loss** is the primary driver of improvement, distinguishing 1-shot RLVR from "grokking" (which depends heavily on weight decay regularization). Entropy loss alone without outcome reward yields a measurable performance boost, though weaker than the format-reward baseline.

---

### Implications
- The extreme sample efficiency of 1-shot RLVR challenges the assumption that RLVR's effectiveness depends on dataset diversity and scale, suggesting instead that base models already possess latent reasoning capabilities that can be unlocked by even a single well-structured training signal.
- Post-saturation generalization reveals a qualitatively new learning dynamic in RL fine-tuning: continued policy gradient updates after training accuracy saturation still improve test performance, implying that RL training is not simply fitting to examples but shaping internal reasoning representations in a way that continues to transfer.
- The disproportionate role of entropy loss (exploration incentive) over data quantity shifts the design priority for RLVR systems toward exploration mechanisms, suggesting that future work should investigate entropy regularization, temperature scheduling, and diversity-promoting objectives as first-class concerns rather than data curation.
- For the test-time compute theme, the observation that 1-shot RLVR increases response length and self-reflection frequency on evaluation tasks implies that unlocking extended chain-of-thought reasoning may require less training data than previously assumed — the bottleneck may be exploration during training rather than coverage of reasoning patterns in data.
- These findings prompt a re-examination of what large RLVR data

## Key Claims

1. RLVR with a single training example can achieve performance comparable to using datasets with thousands of examples for mathematical reasoning
2. RLVR with two examples slightly exceeds the performance of using 1.2k examples and matches the performance of using 7.5k MATH training examples
3. 1-shot RLVR effectiveness has been confirmed across multiple base models including Qwen2.5-Math-1.5B, Qwen2.5-Math-7B, Llama3.2-3B-Instruct, and DeepSeek-R1-Distill-Qwen-1.5B
4. Post-saturation generalization occurs in 1-shot RLVR: training accuracy saturates near 100% rapidly but test performance continues improving for hundreds or thousands of additional steps
5. In 1-shot RLVR, even after overfitting (training responses become multilingual gibberish), test responses remain interpretable and maintain high accuracy
6. Overfitting in 1-shot RLVR occurs very late: the single training example is not overfitted until after millions of rollouts (π1 after 1400 steps, π13 after 1800 steps, with 1024 samples per step)
7. 1-shot RLVR enables cross-category generalization: training on a single example from one category (e.g., Geometry) often enhances performance in other categories (e.g., Algebra, Number Theory)
8. Test data belonging to the same category as the training example does not necessarily exhibit better improvement, suggesting stimulated reasoning capability cannot be predicted by superficial features
9. 1-shot RLVR on math examples can improve model performance on non-mathematical reasoning tasks (ARC-Easy and ARC-Challenge), even outperforming full-set RLVR
10. Self-reflection frequency (words like 'rethink', 'recheck', 'recalculate') increases in evaluation responses as 1-shot RLVR training progresses, especially after ~1250 steps

## Capabilities

- RLVR with a single training example (1-shot RLVR) achieves comparable mathematical reasoning performance to RLVR trained on thousands of examples — Qwen2.5-Math-1.5B improves from 36.0% to 73.6% on MATH500 with one example, matching the 1.2k-dataset result of 73.6%; 2-shot RLVR slightly exceeds full
- Single-example RLVR training generalizes across mathematical problem categories — training on a Geometry example can improve Algebra and Number Theory, with the training example's category not reliably predicting which downstream categories benefit most
- Post-saturation generalization: RLVR training with a single example continues improving held-out test performance for hundreds of additional gradient steps after training accuracy saturates at 100%, and persists even after the model catastrophically overfits and produces incoherent training outputs
- Entropy loss injection during RLVR training promotes diverse reasoning path exploration and yields measurable performance gains even when used as the sole training signal — without any outcome reward

## Limitations

- 1-shot RLVR completely fails on examples that are too difficult for the base model — when pass@k ≈ 0, the training produces zero or degraded learning signal and actively harms model performance below baseline
- Optimal example selection for 1-shot RLVR requires first training on the full dataset to compute historical variance scores — a circular dependency that negates much of the data-efficiency gain in practice
- 1-shot RLVR effectiveness degrades substantially for models already distilled from long chain-of-thought data — the gap between few-shot and full-set RLVR is considerably larger for DeepSeek-R1-Distill-Qwen-1.5B than for base models
- 1-shot RLVR requires the single training example to be solvable by the base model with non-trivial probability — the method is conditionally dependent on base model capability at that specific problem type, not universally applicable
- 1-shot RLVR shows training instability on general instruction-tuned models — Llama-3.2-3B-Instruct exhibits unstable RLVR training dynamics with smaller absolute gains than math-specialised models
- At late training stages in 1-shot RLVR, the model catastrophically overfits the single example — producing unintelligible multilingual gibberish mixed with correct calculations on the training input — indicating the training process becomes degenerate even if test performance is temporarily preserve
- 1-shot RLVR has only been validated on mathematical reasoning domains with verifiable ground-truth answers — the method's applicability to non-mathematical, open-ended, or creative tasks is untested beyond two ARC benchmarks
- The mechanism underlying 1-shot RLVR's effectiveness is not explained — why a single example suffices, what determines which examples work, and why cross-category generalisation occurs remain theoretically unresolved
- Training response length is bounded to 3072 tokens with 4096-token total context for 1.5B models — constraining the complexity of reasoning chains that can be explored during RLVR training

## Bottlenecks

- No scalable method exists to identify optimal 1-shot RLVR training examples without first running full-dataset training — the best available approach (historical variance score) requires the expensive process it is meant to replace, blocking practical deployment of ultra-data-efficient RLVR

## Breakthroughs

- A single training example suffices to match full-dataset RLVR performance — the data requirement for RLVR post-training is orders of magnitude smaller than previously assumed, providing strong empirical evidence that RLVR primarily elicits latent capabilities already encoded by pretraining rather th
- Post-saturation generalization: RLVR training continues producing meaningful test accuracy improvements for hundreds of steps after training accuracy reaches 100%, and persists even after the model catastrophically overfits the single training example — decoupling policy generalisation from per-exam

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/math500|MATH500]]
- [[entities/grokking|grokking]]
- [[entities/verl|veRL]]
