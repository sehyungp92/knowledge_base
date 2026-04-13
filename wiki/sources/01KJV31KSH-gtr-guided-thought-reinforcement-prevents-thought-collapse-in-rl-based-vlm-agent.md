---
type: source
title: 'GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM
  Agent Training'
source_id: 01KJV31KSHB04ZMJ4EYSDJBXJ8
source_type: paper
authors:
- Tong Wei
- Yijun Yang
- Junliang Xing
- Yuanchun Shi
- Zongqing Lu
- Deheng Ye
published_at: '2025-03-11 00:00:00'
theme_ids:
- chain_of_thought
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM Agent Training

**Authors:** Tong Wei, Yijun Yang, Junliang Xing, Yuanchun Shi, Zongqing Lu, Deheng Ye
**Published:** 2025-03-11 00:00:00
**Type:** paper

## Analysis

# GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM Agent Training
2025-03-11 · paper · Tong Wei, Yijun Yang, Junliang Xing, Yuanchun Shi, Zongqing Lu et al. (6 total)
https://arxiv.org/pdf/2503.08525

---

### Motivation & Prior Limitations
RLVR (RL with verifiable outcome rewards) has proven effective for scaling CoT reasoning in text-only LLMs, but its application to VLM agents in goal-directed visual environments remained largely unexplored and underperforming.
- Prior work (RL4VLM) demonstrated feasibility of PPO-based RL finetuning for VLM agents on simple tasks but showed limited gains on complex, long-horizon tasks like the 24 Points card game and ALFWorld embodied tasks.
  - In the 24 Points game, RL4VLM achieves only 2.5% task success rate — comparable to an untuned base model — despite extended training.
- When rewards are based solely on final action outcomes, the agent's chain-of-thought reasoning receives no direct supervision signal, which becomes catastrophic in tasks with long episodes, large state spaces, and multi-step dependencies.
  - The paper identifies and names this failure mode "thought collapse": a rapid loss of diversity in generated thoughts, producing state-irrelevant and templated reasoning that outputs near-identical thoughts regardless of the current visual state, followed by invalid actions and consistently negative rewards.
  - Thought collapse persists across model scales (7B and 13B LLaVA variants) and with extended training budgets (up to 30k steps), ruling out insufficient capacity or compute as the root cause.
- Existing process guidance alternatives are insufficient for this setting. Process Reward Models (PRMs) require expensive human annotations and cannot generalize to dynamic environments; VLM-as-a-judge approaches provide only numerical scores that are too coarse to prevent reward hacking; length-based rewards encourage longer thoughts but not coherent ones.
  - In ablation comparisons, both VLM-as-a-judge and length-reward variants fail to improve task success rate even when episode returns show marginal gains.

---

### Proposed Approach
The paper proposes Guided Thought Reinforcement (GTR), a framework that augments standard PPO-based RL finetuning of VLM agents with automated, step-level thought correction provided by an off-the-shelf VLM corrector model.
- At each RL training step, a corrector model (GPT-4o in experiments) evaluates the agent's generated thought for visual recognition accuracy and reasoning correctness, then produces a refined thought trajectory when errors are detected.
  - This differs from PRMs (which require human-labeled process data), VLM-as-a-judge (which only scores), and behavior cloning from expert demonstrations (which requires expert-level reference trajectories): the corrector need only be capable enough to produce better-than-random corrections, not optimal solutions, as verified by GTR surpassing the corrector model itself.
- GTR combines two simultaneous training objectives: PPO updates on action tokens (from environment rewards) and SFT cross-entropy updates on thought tokens (from corrected thought trajectories), tightly coupling reasoning process improvement with action policy improvement.
  - The action probability for policy gradient is computed over both CoT tokens and action tokens with a scaling factor λ to balance their differing lengths (Eq. 2).
- To address distribution shift between the corrector's reference thoughts and the agent's evolving on-policy outputs, GTR adopts DAgger (Dataset Aggregation): all historical corrected thought samples are accumulated into a growing dataset used for SFT updates, preventing catastrophic forgetting as the policy changes.
- Additional stabilization mechanisms include a token-level repetition penalty during generation, a format reward for structurally valid outputs integrated into the corrector's judgment, and tool-use augmentation of the corrector (e.g., invoking Python code to enumerate valid 24-point equations), which provides task-specific grounding that general-purpose VLMs otherwise lack.
- Crucially, GTR clones only thought tokens via SFT, not full responses. Cloning actions alongside thoughts was found to amplify corrector hallucinations and interfere with the agent's ability to adjust based on environmental feedback.

---

### Results & Capabilities
GTR achieves a 17.5% task success rate on the 24 Points game with a 7B LLaVA model, representing a 3–5× improvement over all prior methods including GPT-4o (2.5%), Qwen2-VL-72B (4.5%), and RL4VLM (2.5%), while using a notably smaller model.
- GTR also surpasses GPT-4o with tool-use augmentation (13.5% success rate), demonstrating that RL exploration guided by correction enables the agent to discover strategies beyond what imitation of the corrector alone can achieve.
- When applied to the stronger Qwen2.5-VL-7B backbone, GTR reaches success rates comparable to OpenAI o3 on the 24 Points task within a short training period, while RL4VLM on the same backbone degrades with additional training.
- On simpler gym cards tasks (Numberline, EZPoints, Blackjack) where thought collapse is less prominent, GTR still improves over RL4VLM and matches or exceeds Qwen2-VL-72B (10× larger), achieving 100% success on Numberline and EZPoints.
- On ALFWorld embodied tasks (evaluated without text observation descriptions, a harder setting than prior work), GTR achieves a 0.18 average success rate versus 0.04 for RL4VLM, with particular strength on Cool & Place (0.33) and Look in Light (0.23) subtasks.
  - RL4VLM exhibits thought collapse in ALFWorld as well — both success rate and episode returns decline during training — while GTR shows steady improvement across all task categories.
- Ablations confirm that: (1) thought weight annealing (gradually removing process guidance) causes regression to thought collapse; (2) removing tool-use from the corrector eliminates performance gains; (3) removing DAgge

## Key Claims

1. Reinforcement learning with verifiable outcome rewards (RLVR) has effectively scaled up chain-of-thought reasoning in large language models.
2. When rewards are based solely on action outcomes, RL fails to incentivize chain-of-thought reasoning in VLMs.
3. Thought collapse is characterized by rapid loss of diversity in the agent's thoughts, state-irrelevant and incomplete reasoning, and subsequent invalid actions resulting in negative rewards.
4. GTR achieves 3 to 5 times higher task success rates compared to state-of-the-art models despite using notably smaller model sizes.
5. Thought collapse persists across both LLaVA-7B and LLaVA-13B model scales and is not resolved by extending training from 15k to 30k steps.
6. Thought collapse arises from RL training in which rewards are determined entirely by final actions, leaving the intermediate thought process unevaluated and unsupervised.
7. Thought collapse is especially pronounced in tasks with longer episodes, larger state spaces, and greater complexity.
8. The VLM-as-a-judge approach using numerical scores does not improve task success rates and is insufficient for effective RL training in complex tasks.
9. Length-based rewards fail to incentivize meaningful reasoning in VLM agents.
10. GTR achieves a 17.5% success rate on Points24, compared to GPT-4o+Tool at 13.5%, SFT-only at 11.0%, and RL4VLM at 2.5%.

## Capabilities

- Process-guided RL (GTR) enables a 7B VLM agent to reach o3-level performance on the 24-points card game — a complex multi-step visual reasoning task — outperforming GPT-4o, Qwen2-VL-72B, and Gemini at 3-5x smaller model size
- Automated VLM corrector provides scalable per-step process supervision for RL training of vision-language agents without human annotations — correcting reasoning trajectories on-the-fly and outperforming the corrector model itself
- GTR-trained LLaVA-7B achieves competitive success rates on ALFWorld embodied household tasks using visual-only observations (no text scene descriptions), approximating the performance of models trained with textual scaffolding
- DAgger-based thought dataset aggregation enables continual improvement of VLM agents under iterative PPO updates by mitigating distribution shift between evolving policy and historical correction data

## Limitations

- Outcome-only reward RL causes 'thought collapse' in VLM agents on complex tasks: rapid, irreversible loss of reasoning diversity resulting in state-irrelevant, templated outputs and invalid actions — model continues generating text but has lost meaningful reasoning ability
- Thought collapse is scale-invariant and training-budget-invariant: occurs identically in 7B and 13B models, and is not mitigated by doubling training steps from 15k to 30k — larger models and longer training do not escape the failure mode
- VLM-as-judge numerical scoring is insufficient as process reward for complex RL tasks: episodic returns increase but task success rates fail to improve, due to reward hacking and lack of positive incentives in hard problems
- Length-based reasoning rewards (designed to encourage longer thoughts) also fail to improve task success rates in complex RL settings — they are equally insufficient as process guidance
- GTR's effectiveness is hard-bounded by the corrector model's capability: removing tool use from GPT-4o corrector eliminates all performance improvement — the corrector must possess sufficient task-specific analytical ability
- Corrector model hallucinations actively degrade performance when applied to full response cloning (thoughts + actions) — thought-action mismatches from corrector errors are reinforced, overriding environmental feedback
- Thought collapse only manifests in long-horizon, large-state-space tasks (>10 steps, complex action space) — simpler tasks with short episodes are unaffected by outcome-only reward RL, masking the limitation in typical benchmarks
- GTR has only been validated at 7B-scale models due to resource constraints — whether process-guided RL confers comparable advantages to larger-scale VLMs remains untested
- GTR training requires ~30 hours on a single 40GB GPU with LoRA — the corrector model (GPT-4o) must be called at every RL step, creating latency and API cost overhead throughout training
- Process guidance must be maintained throughout the entire training process — cosine annealing to reduce thought cloning weight late in training causes relapse into thought collapse, demonstrating no stable regime without continuous supervision
- Promoting o1-style long chain-of-thought for sequential action reasoning in VLM agents remains unexplored — GTR focuses on fast-thinking single-step reasoning, not extended deliberation across action sequences
- VLM agents trained in multimodal environments tend to rely on text descriptions when both modalities are available, neglecting visual input — visual-only evaluation reveals substantially weaker performance than text-augmented settings

## Bottlenecks

- Outcome-only RLVR cannot sustain coherent reasoning in VLM agents for complex long-horizon visual tasks — the absence of per-step thought supervision causes irreversible reasoning collapse, creating a hard dependency on external process guidance infrastructure
- Scalable GTR requires a frontier-level external corrector (GPT-4o with tool use) — the framework's effectiveness ceiling is set by the corrector's task-specific reasoning quality, creating an infrastructure dependency that prevents democratization

## Breakthroughs

- Identification of 'thought collapse' as a distinct, systematic failure mode in RLVR training of VLM agents — and demonstration that it is caused by structural absence of thought supervision, not model capacity or training budget
- GTR enables a 7B VLM (Qwen2.5-VL-7B with GTR) to reach o3-level performance on 24-points card game — a complex multi-step visual reasoning benchmark — while outperforming GPT-4o, Qwen2-VL-72B, and Gemini at 10x smaller model size

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/qwen25-vl-7b|Qwen2.5-VL-7B]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/task-success-rate|Task Success Rate]]
