---
type: source
title: Grounded Reinforcement Learning for Visual Reasoning
source_id: 01KJTRR26FHKZWP1KG1G09HD39
source_type: paper
authors:
- Gabriel Sarch
- Snigdha Saha
- Naitik Khandelwal
- Ayush Jain
- Michael J. Tarr
- Aviral Kumar
- Katerina Fragkiadaki
published_at: '2025-05-29 00:00:00'
theme_ids:
- chain_of_thought
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Grounded Reinforcement Learning for Visual Reasoning

**Authors:** Gabriel Sarch, Snigdha Saha, Naitik Khandelwal, Ayush Jain, Michael J. Tarr, Aviral Kumar, Katerina Fragkiadaki
**Published:** 2025-05-29 00:00:00
**Type:** paper

## Analysis

# Grounded Reinforcement Learning for Visual Reasoning
2025-05-29 · paper · Gabriel Sarch, Snigdha Saha, Naitik Khandelwal, Ayush Jain, Michael J. Tarr et al. (7 total)
https://arxiv.org/pdf/2505.23678

---

### Motivation & Prior Limitations
- Most state-of-the-art VLMs operate end-to-end in a single forward pass, predicting answers without adapting their computational strategy to the task structure or exposing interpretable intermediate reasoning steps.
  - Prompt-based decomposition methods (ViperGPT, VisualProg, V*) generate fixed reasoning chains that do not adapt to the input scene and rely on frozen backbones and hand-crafted prompts.
- Applying standard RL directly to VLMs fails to induce useful visual reasoning behaviors and instead exacerbates ungrounded reasoning.
  - Behavioral analysis on Qwen2.5-VL-3B shows the base model examines only 1.44 regions per task, sets almost no visual subgoals (0.07), and never backtracks (0.00). Vanilla GRPO marginally increases region exploration (1.8) but eliminates visual subgoal setting entirely (0.00) and still shows no backtracking.
  - RL can only amplify behaviors already present in the base model's sampling distribution; because pretrained VLMs are biased toward abstract language-based strategies rather than region-level analysis, standard RL collapses onto reward-maximizing shortcuts at the expense of richer visual cognition.
- The cognitive behaviors that support generalization in text-based RL (subgoal setting, backtracking, verification) had not been identified or instantiated for visual reasoning tasks prior to this work.

---

### Proposed Approach
- ViGoRL (Visually Grounded Reinforcement Learning) redefines each reasoning step as a tuple ⟨st, (xt, yt)⟩ — a textual thought anchored to a specific image coordinate — forcing the model to explicitly reference spatial locations as evidence throughout its chain of thought.
  - Unlike vanilla GRPO or SFT baselines, grounding is baked into the reasoning trace format itself rather than treated as auxiliary supervision; the model autonomously learns to propose and use spatial coordinates without external grounding labels.
- The training pipeline is two-stage: (1) MCTS-based warm-start SFT that scaffolds grounded reasoning behaviors, followed by (2) GRPO reinforcement learning that refines these behaviors against task-correctness rewards.
  - MCTS uses a frozen Qwen2.5-VL-72B teacher to expand reasoning trees where each node is a ⟨thought, coordinate⟩ tuple; from 1,500 prompts it generates ~30k high-quality reasoning traces exhibiting wide region exploration, visual verification, and backtracking — behaviors impossible to obtain from linear teacher rollouts alone.
  - Linearized MCTS paths are converted into two trace types: direct successful chains and "corrected chains" where a failed branch triggers an explicit backtrack before reaching the correct answer.
  - The format reward during GRPO awards +1 only if all coordinate references are valid (in addition to checking ⟨think⟩/⟨answer⟩ tags), directly incentivizing maintained grounding throughout RL training.
- A novel multi-turn RL extension allows the model to dynamically request higher-resolution crops of predicted coordinates via tool calls, supplying fresh fine-grained visual evidence impossible to encode in the globally-resized input image.
  - The multi-turn reward includes a diversity bonus (+0.2 per sufficiently distinct crop coordinate, up to 4) to prevent the model from repeating the same region, and a strict grammar reward enforcing correct dialog structure across think/tool_call/observation turns.

---

### Results & Capabilities
- ViGoRL-3B achieves 62.9% accuracy on SAT-2, a +12.9 point improvement over Vanilla GRPO and +16.8 points over the base model, with consistent gains on out-of-distribution spatial benchmarks BLINK (48.5%) and RoboSpatial (67.1%).
  - ViGoRL-7B scales further to 67.5% on SAT-2, 54.1% on BLINK, and 76.4% on RoboSpatial, indicating the method generalizes across model sizes.
- Grounded reasoning dramatically amplifies measurable visual cognitive behaviors: ViGoRL explores 3.5 regions per task (vs. 1.44 base, 1.8 vanilla GRPO), sets 1.1 grounded subgoals per task (15× higher than base), increases visual verification (0.39 vs. 0.14), and uniquely develops visual backtracking (0.47 vs. 0.00 in all baselines).
  - These behavioral gains enable the 3B ViGoRL model to match the accuracy of zero-shot Qwen2.5-VL-72B on SAT-2 (0.64 vs. 0.65).
- On web grounding, ViGoRL-7B achieves 91.0% on ScreenSpot-V2 and 33.1% on ScreenSpot-Pro, outperforming OS-Atlas and UGround variants trained on orders of magnitude more GUI data (up to 13M samples).
- Multi-turn RL with zoomed-in visual feedback achieves 86.4% on V*Bench, surpassing GPT-4o (66.0%), Sketchpad-GPT-4o (80.3%), and IVM-Enhanced GPT-4V (81.2%).
- On VisualWebArena (vision-only, no HTML access), ViGoRL surpasses the prior state-of-the-art ICAL by 3.0% despite ICAL having access to textual set-of-marks derived from HTML.
- Human evaluation confirms spatial grounding is interpretable: 72.8% of predicted coordinates were judged as accurately referring to the described region, and correctly-grounded steps rated 3.81/5 for helpfulness versus 2.26/5 for incorrectly-grounded steps.

---

### Implications
- Spatial grounding may be a general-purpose cognitive scaffold for VLMs analogous to how human visual attention routines decompose complex reasoning into perceptually anchored steps, suggesting that architectural alignment with human cognition is not merely interpretive but functionally beneficial for generalization.
- The finding that standard RL collapses onto ungrounded shortcuts unless the initial policy is explicitly biased toward grounded behaviors has direct implications for RLHF and reward modeling in multimodal settings: outcome-only rewards are insufficient to steer models toward richer intermediate reasoning strategies in vision.
- MCTS as a data generatio

## Key Claims

1. Most state-of-the-art VLMs operate end-to-end, predicting answers in a single forward pass without adapting computational strategies to different tasks.
2. RL can only amplify or chain reasoning primitives already present in the base model's sampling distribution, not induce entirely new behaviors.
3. Current VLMs often fail to reference fine-grained image inputs; their reasoning is largely ungrounded, treating vision as static context rather than actively referenced input.
4. Qwen2.5-VL-3B examines only 1.44 regions per task with minimal visual verification (0.14) and no backtracking.
5. Standard RL optimization exacerbates ungrounded reasoning: RL-tuning with task-level rewards slightly increases region exploration to 1.8 but eliminates visual subgoal setting (0.00) and shows no back
6. Without grounding incentives, RL collapses onto reward-maximizing shortcuts at the expense of richer visual reasoning behaviors.
7. Even large models (Qwen2.5-VL-72B) deployed with standard prompting explore only 2–3 regions, set few subgoals, and never backtrack.
8. MCTS-based warm-start generates approximately 30k high-quality reasoning traces from 1,500 prompts using a teacher model.
9. Distillation from linear rollouts without MCTS leads to degraded generalization on out-of-distribution spatial tasks after GRPO training.
10. ViGoRL-3B achieves 62.9% accuracy on SAT-2, representing +16.8 points over the base model and +12.9 points over Vanilla GRPO.

## Capabilities

- VLMs can be trained via RL to explicitly anchor each reasoning step to spatial image coordinates (deictic grounding), producing interpretable reasoning traces that guide visual attention to task-relevant regions and induce emergent visual exploration behaviors
- Multi-turn RL with dynamic visual feedback (tool-call-triggered zooming into predicted coordinates) enables precise fine-grained small-element localization, achieving 86.4% on V*Bench and surpassing GPT-4o (66%) and all tool-using VLM pipelines
- A 3B-parameter VLM trained with visually grounded RL achieves spatial reasoning accuracy (64%) comparable to a 72B zero-shot baseline (65%), demonstrating extreme parameter efficiency through grounding-aware training
- MCTS-guided teacher distillation generates diverse visually-grounded reasoning traces exhibiting exploration, backtracking, and verification from only 1,500 prompts (~30k traces) — orders of magnitude smaller than typical SFT corpora
- VLMs trained with visually grounded RL develop emergent cognitive behaviors — visual backtracking (0.47/task), grounded subgoal setting (15× increase over base), visual verification (3× increase) — that are entirely absent in zero-shot 72B models and standard RL-tuned models

## Limitations

- Standard RL (GRPO) applied directly to VLMs without explicit grounding incentives collapses onto ungrounded shortcuts — it eliminates visual subgoal setting entirely (drops to 0.00 from 0.07 in the base model) and never induces backtracking, worsening reasoning quality despite improving answer-level
- RL cannot induce genuinely new reasoning behaviors from scratch — it can only amplify or chain primitives already present in the base model's sampling distribution; models lacking target behaviors must be bootstrapped via SFT before RL is effective
- Even 72B-parameter VLMs fail to spontaneously exhibit visual backtracking or systematic region exploration zero-shot — these behaviors never appear regardless of model scale, indicating they are absent from pretraining
- The ViGoRL training pipeline requires access to a 72B teacher model for MCTS-based grounded trace generation — a significant compute accessibility barrier that limits adoption to well-resourced labs
- Professional GUI element grounding (ScreenSpot-Pro) remains at only 33.1% accuracy with the best ViGoRL-7B model — professional-grade visual UI understanding is far from solved despite significant improvements over baselines
- Live multi-step web agent performance (VisualWebArena) remains extremely low even with ViGoRL-7B (11.2%) — multi-step real-world web navigation far exceeds current visual grounding capabilities
- Teacher distillation without MCTS (using linear rollouts) preserves in-distribution performance but degrades out-of-distribution generalization — MCTS-generated search diversity is specifically required for robust generalization
- Multi-turn visual feedback (zooming) yields only marginal gains (+1.2%) in standard-resolution settings — the dynamic zoom capability primarily benefits low-resolution or fine-grained element scenarios, not general visual reasoning
- Approximately 27% of spatial grounding coordinate predictions are spatially inaccurate (human evaluation), causing helpfulness to drop from 3.81 to 2.26 on incorrect grounding — coordinate precision remains a significant weak point
- Adaptive bounding-box cropping provides no accuracy benefit over fixed-size point cropping due to imprecise box predictions and inconsistent aspect ratios — VLMs cannot reliably predict precise spatial extents, only approximate centers

## Bottlenecks

- VLM pretraining distribution is heavily biased toward abstract, language-based reasoning rather than region-level visual analysis — standard RL amplifies this bias, making explicit bootstrapping via grounded SFT a prerequisite before any RL training on visual reasoning tasks
- High-resolution professional GUI grounding (ScreenSpot-Pro class tasks) remains fundamentally unsolved at ~33% even with explicit grounding, zooming, and large-scale web-finetuning — blocking reliable deployment of visual computer-use agents in professional environments

## Breakthroughs

- Spatially grounded RL training (ViGoRL) enables a 3B VLM to match the spatial reasoning accuracy of a 72B zero-shot model — demonstrating that training paradigm, not parameter count, is the primary bottleneck for visual reasoning capability
- Standard RL (GRPO) with correctness-only rewards systematically and completely eliminates visual reasoning sub-behaviors (subgoal setting drops to 0.00 from 0.07) — demonstrating that naive reward design actively degrades multimodal reasoning quality even while improving aggregate accuracy metrics

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/qwen25-vl|Qwen2.5-VL]]
- [[entities/screenspot|ScreenSpot]]
