---
type: source
title: 'GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents'
source_id: 01KJTTA22M7HXZZVMKH0533GGG
source_type: paper
authors:
- Yuqi Zhou
- Sunhao Dai
- Shuai Wang
- Kaiwen Zhou
- Qinglin Jia
- Jun Xu
published_at: '2025-05-21 00:00:00'
theme_ids:
- agent_systems
- computer_use_and_gui_agents
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents

**Authors:** Yuqi Zhou, Sunhao Dai, Shuai Wang, Kaiwen Zhou, Qinglin Jia, Jun Xu
**Published:** 2025-05-21 00:00:00
**Type:** paper

## Analysis

# GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents
2025-05-21 · paper · Yuqi Zhou, Sunhao Dai, Shuai Wang, Kaiwen Zhou, Qinglin Jia et al. (6 total)
https://arxiv.org/pdf/2505.15810

---

### Motivation & Prior Limitations
- The R1-Zero paradigm (online RL + chain-of-thought prior to action) has been adopted for GUI agents without critical analysis of whether its design choices transfer to grounding tasks, making it unclear whether performance gains stem from the RL algorithm itself or from confounding factors like backbone architecture, data scale, and training protocols.
  - Existing R1-style GUI agents (UI-R1, GUI-R1, InfiGUI-R1) differ across multiple axes simultaneously, preventing isolation of the RL contribution.
  - SFT-trained GUI agents require large-scale labeled datasets and generalize poorly to out-of-distribution scenarios, motivating RL-based alternatives.

- Standard GUI grounding reward functions (RHit and RIoU) individually cause opposite forms of reward hacking, undermining localization quality despite improving their respective metrics.
  - Optimizing RHit alone improves point accuracy but causes IoU to drop as training progresses; optimizing RIoU alone improves overlap but reduces accuracy, because GRPO's sample selection interacts with each reward to systematically shrink or expand predicted bounding boxes.

- The standard GRPO objective introduces two compounding biases that are particularly damaging for grounding: a response-level length bias that rewards longer incorrect outputs and shorter correct ones, and a question-level difficulty bias that causes the model to over-optimize easy samples.
  - In grounding tasks these biases are especially harmful because longer outputs empirically degrade grounding accuracy (Section 3.1), so the length bias directly amplifies grounding errors while simultaneously deprioritizing the hard examples where learning is most valuable.

- Prior R1-style GUI agents assume that chain-of-thought reasoning improves grounding, but this assumption conflicts with the visual-search nature of the task.
  - InfiGUI-R1 uses a "Slow Thinking Template" that encourages deliberative reasoning, yet grounding accuracy on ScreenSpot consistently decreases as the number of reasoning tokens increases, and models with higher text-to-image token ratios perform strictly worse across both text and icon subtasks.

---

### Proposed Approach
- GUI-G1 decomposes the R1-Zero training pipeline into three independently analyzed and corrected components — input design, output evaluation, and policy update — then proposes a targeted fix for each.

- For input design, a **Fast Thinking Template** eliminates the explicit `<think></think>` chain-of-thought scaffold entirely, prompting the model to produce the bounding box answer directly, on the empirical basis that visual grounding is a "System 1" perceptual task better served by fast intuition than slow deliberative reasoning.
  - This contrasts with InfiGUI-R1's Slow Thinking Template and is motivated by Kahneman's distinction between fast/intuitive and slow/effortful cognition applied to vision grounding.

- For output evaluation, a composite reward **RHit + αRIoU + βRBox** is introduced, where RBox is a novel size-regularization term that penalizes deviation of each predicted box coordinate from its ground-truth counterpart, constraining box size independently of hit accuracy or overlap.
  - RBox cannot be used alone (it assigns non-zero reward to poorly grounded predictions, destabilizing training), but when combined with RHit and RIoU it breaks the size-exploitation equilibrium and pushes predicted box sizes toward ground-truth dimensions (α=0.25, β=0.125).

- For policy update, two modifications to the GRPO objective are applied: (1) length normalization by |o_i| is replaced with a constant Max_Tokens, removing the per-token gradient amplification that drives length bias; (2) the objective is weighted by a per-query difficulty coefficient w_q derived from the relative bounding box size of the target, so smaller (harder) targets receive larger gradients.
  - The relative box size as a difficulty proxy is empirically grounded in ScreenSpot-Pro's own analysis showing that smaller targets are harder to localize.

- The full model, GUI-G1-3B, is built on Qwen2.5-VL-3B-Instruct and trained for one epoch on a 17K-sample dataset spanning Mobile (UI-BERT), Web (OS-Atlas), and Desktop (OS-Atlas) using the VLM-R1 framework on 4 × H800 GPUs; no KL divergence regularization is applied.
  - Training samples with consistently all-correct or all-incorrect responses across 8 rollouts are discarded to focus training signal on genuinely uncertain examples.

---

### Results & Capabilities
- GUI-G1-3B achieves 90.3% average accuracy on ScreenSpot, surpassing all prior 3B-class models and outperforming larger models including OS-Atlas-7B (82.5%) and the proprietary Gemini 2.0 Project Mariner (84.0%).
  - It also surpasses the best prior R1-style model InfiGUI-R1-3B (87.5%) while using roughly half the training data (17K vs. 32K samples), no intermediate SFT stage, and fewer output tokens at inference.

- On the harder ScreenSpot-Pro benchmark (high-resolution desktop scenarios), GUI-G1-3B scores 37.1%, outperforming the larger UI-TARS-7B (35.7%) and matching InfiGUI-R1-3B (35.7%) which it surpasses by 1.4 absolute points.
  - Strong performance is consistent across Office (59.1%), Scientific (48.0%), and CAD (32.2%) categories for text targets, though icon grounding remains significantly weaker across all models.

- Ablations on the GRPO objective improvements show additive gains: replacing length normalization raises ScreenSpot average from 82.3% to 83.2%, and adding difficulty reweighting raises it further to 83.3%, with the full GUI-G1 system reaching 90.3% when all three components (template, reward, objective) are combined.

- The Fast Thinking Template directly reduces inference token count, as 

## Key Claims

1. GUI grounding performance benefits more from scaled image tokens than from scaled text reasoning tokens.
2. Hit-based reward functions (RHit) cause reward hacking by encouraging models to predict smaller bounding boxes, improving point accuracy while degrading IoU.
3. IoU-based reward functions (RIoU) cause reward hacking by encouraging models to predict larger bounding boxes, improving IoU while reducing point accuracy.
4. RHit and RIoU induce opposing reward hacking behaviors when optimized in isolation, capturing complementary yet competing aspects of grounding quality.
5. A box-size constraint reward (RBox) mitigates reward hacking from RHit and RIoU by regularizing predicted box sizes toward ground truth dimensions.
6. RBox cannot be used as a standalone reward because it assigns non-zero rewards to poorly grounded predictions, causing the model to fail at generating correctly formatted outputs.
7. The GRPO objective introduces a response-level length bias that favors longer incorrect responses and shorter correct responses due to per-token gradient amplification.
8. GRPO's length bias is particularly harmful for GUI grounding because longer outputs are shown to degrade grounding accuracy.
9. GRPO exhibits a question-level difficulty bias that causes the model to focus disproportionately on easier samples rather than harder ones.
10. Relative bounding box size serves as a reliable proxy for task difficulty in GUI grounding, with smaller target boxes indicating harder instances.

## Capabilities

- GUI visual grounding with a 3B model achieves 90.3% accuracy on ScreenSpot and 37.1% on ScreenSpot-Pro using only 17K training samples and no intermediate chain-of-thought reasoning, surpassing larger models including UI-TARS-7B
- Difficulty-aware GRPO training — weighting policy gradient loss by inverse box size as a task difficulty proxy — improves RL optimization on hard GUI grounding samples without requiring additional data or training stages
- Combined Hit + IoU + box-size constraint reward function eliminates the opposing reward hacking behaviors that emerge when Hit and IoU objectives are optimised separately in GUI grounding RL
- R1-Zero-like RL training applied to GUI grounding outperforms SFT-trained models while requiring dramatically fewer training samples — 17K vs 13M (OS-Atlas) or 10M (UGround) — by unlocking latent capabilities through reward signal rather than imitation

## Limitations

- Longer chain-of-thought reasoning consistently degrades GUI visual grounding accuracy — more text tokens proportionally reduce grounding performance, especially for text-element targets where the degradation is steepest
- Hit-based reward functions in GUI grounding RL cause reward hacking toward smaller predicted boxes (improving accuracy, degrading IoU); IoU-based rewards cause the opposite — larger boxes (improving IoU, degrading accuracy). They cannot be optimised in isolation
- GRPO's length normalisation introduces a structural length bias: longer incorrect responses and shorter correct responses are systematically encouraged, compounding with grounding's already high sensitivity to text token count
- Standard GRPO treats all training samples with equal objective weight, causing models to over-optimise on easy grounding instances (large bounding boxes) and under-optimise on difficult ones (small targets, icons), reducing generalisation to real-world challenging GUI elements
- Icon grounding is substantially harder than text grounding across all model architectures and sizes — a persistent 10–30+ percentage point gap exists on ScreenSpot; on ScreenSpot-Pro icon accuracy remains below 20% for almost all models including the best
- GUI-G1-3B's ScreenSpot-Pro gains appear to come from activating pretrained knowledge rather than learning task-specific grounding — evidenced by underperformance on the OS subset vs OS-Atlas-7B (16.1% vs 16.8%) despite identical training data
- Box-size-only reward (RBox) fails to produce correct output format when used alone — non-zero rewards on poorly grounded predictions prevent the model from learning valid output structure; it must be combined with Hit and IoU signals
- SFT-based GUI agent training requires 1M–13M high-quality labeled samples and exhibits poor out-of-distribution generalisation, creating a steep data cost barrier for grounding model development
- High-resolution desktop GUI grounding (ScreenSpot-Pro) remains far from solved — best average performance is ~37–39% with professional application domains (CAD: 32%, Scientific: 48%) presenting particularly steep challenges
- All evaluation is on curated benchmarks (ScreenSpot, ScreenSpot-Pro) with no real-world deployment testing or user studies — real-world generalisation beyond benchmark scenarios is unverified
- The paper addresses only the grounding sub-task (locating UI elements); the full GUI agent pipeline — planning, multi-step action sequencing, error recovery — is explicitly out of scope and remains unaddressed
- Performance gains across R1-style GUI agents are confounded by simultaneous differences in backbone architectures, data sources, and training protocols — isolating the specific contribution of RL vs. other factors remains methodologically difficult

## Bottlenecks

- Opposing reward hacking from Hit-based and IoU-based grounding reward functions blocks reliable GUI agent RL training — optimising either metric individually causes box size drift in opposite directions, preventing simultaneous optimisation of both localization accuracy and overlap quality
- GRPO's length normalisation and equal-weight sample treatment structurally disadvantage GUI grounding RL — combined with grounding's high sensitivity to text token count, these biases reduce model performance on hard instances (small targets, icon elements)
- Icon grounding accuracy is far below text grounding across all model sizes and training paradigms — the persistent 15–30 point gap on standard benchmarks and sub-20% icon accuracy on ScreenSpot-Pro represents an unsolved visual-semantic alignment problem blocking reliable GUI automation on icon-heav

## Breakthroughs

- Empirical demonstration that fast thinking (no chain-of-thought) consistently outperforms slow thinking (explicit reasoning chains) for GUI visual grounding — more text reasoning tokens directly and monotonically degrade localization accuracy because image tokens, not text, carry the primary groundi

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/screenspot|ScreenSpot]]
