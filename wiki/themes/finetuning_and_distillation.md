---
type: theme
title: Finetuning & Distillation
theme_id: finetuning_and_distillation
level: 2
parent_theme: post_training_methods
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 61
sources_since_update: 0
update_count: 1
velocity: 0.233
staleness: 0.0
status: active
tags: []
---
# Finetuning & Distillation

> Finetuning & Distillation has moved decisively from a research technique into a production discipline. The center of gravity has shifted from whether post-training methods can improve models to how compounding improvement loops get built into deployed systems — a recalibration that repositions organizations controlling post-training pipelines as meaningful competitive actors, independent of pretraining compute.

**Parent:** [[themes/post_training_methods|post_training_methods]]

## Current State

The foundational shift in this theme is conceptual: pretraining is now understood as a floor, not a ceiling. Post-training methods — fine-tuning, reinforcement learning, distillation — have been shown to yield capability uplift far beyond what was previously attributed to them, reframing the entire training stack. This wasn't a gradual drift; it was a recalibration of where the leverage actually sits.

On the production side, the most concrete movement is the emergence of continuous fine-tuning loops grounded in live operational feedback. The demonstrated pattern — nightly fine-tune jobs consuming human-override telemetry, driving recall from 92% to 98% within a month without service interruption — establishes that improvement can be a compounding property of deployment itself, not just of periodic retraining. This is still narrow in scope (specific recall tasks in enterprise settings), but the mechanism is real and the infrastructure pattern is replicable. Meanwhile, small domain-specialized models running inside enterprise infrastructure are showing frontier-beating performance on narrow tasks while satisfying data residency requirements, though this capability sits at demo maturity rather than broad production.

The persistent structural limitation is that fine-tuning on domain data deepens knowledge without teaching generalization — models become more accurate within a niche but don't develop stronger reasoning or multi-step planning from the process. This is architectural and stable, with no near-term fix on the horizon from fine-tuning alone.

The pressure this creates is being partially absorbed by adjacent themes: synthetic data pipelines lowering the cost of assembling post-training corpora, and adaptive computation research suggesting timescale-aware update mechanisms as a longer-horizon alternative to static weight adjustment. What to watch: whether the continuous fine-tuning loop pattern propagates from narrow recall tasks into broader agentic behaviors, and whether the infrastructure pressure it creates accelerates practical progress in continual learning.

## Capabilities

- **Production feedback loops** (narrow_production) — Continuous model improvement from labeled failures without service interruption, exemplified by nightly fine-tune jobs consuming human-override telemetry.
- **Specialized small models** (demo) — Small, customized models running inside enterprise infrastructure outperforming frontier models on domain-specific tasks while satisfying data residency constraints.
- **Post-training capability amplification** (broad_production) — Fine-tuning, RL, and distillation substantially amplify capabilities beyond what pretraining alone establishes, now recognized as a primary source of capability uplift across the training stack.

## Limitations

- **Generalization ceiling** (severity: significant, trajectory: stable) — Fine-tuning on domain-specific data increases knowledge in a niche but does not teach models how to solve novel problems or develop stronger multi-step reasoning. This is an architectural constraint with no near-term fix from fine-tuning alone.

## Bottlenecks

- **Catastrophic forgetting under continuous updates** — Production deployment patterns requiring frequent, non-disruptive model updates from live signals create direct pressure on continual learning infrastructure. The absence of robust forgetting avoidance mechanisms constrains how aggressively continuous fine-tuning loops can be applied.
- **Post-training corpus assembly cost** — The marginal cost of domain-specific fine-tuning corpora remains a rate-limiter for the small-specialized-model pattern, though this is declining as document digitization pipelines scale.

## Breakthroughs

- **Production-grounded continuous fine-tuning loops** (significance: notable) — AI systems in enterprise deployment can improve accuracy metrics measurably within weeks by fine-tuning on operational feedback signals (false negatives, human overrides, telemetry). This breaks the prior assumption that model improvement required offline retraining cycles disconnected from production; deployed systems were previously static until a new version was released.
- **Post-training methods revealed as primary capability drivers** (significance: notable) — Fine-tuning, RL, and distillation have been shown to yield far more capability uplift than previously understood. This overturns the prior belief that post-training was primarily a safety and alignment layer with modest capability effects, and that base model pretraining determined the capability ceiling.

## Anticipations

- The continuous fine-tuning loop pattern will propagate from narrow recall tasks into broader agentic behaviors as the infrastructure matures.
- As document digitization scales to commodity throughput, the marginal cost of domain-specific fine-tuning corpora approaches zero — potentially moving the small-specialized-model capability from demo to broad production.
- Infrastructure pressure from frequent non-disruptive update requirements will accelerate practical progress in continual learning.

## Cross-Theme Implications

- **→ [[themes/creative_content_generation|Creative Content Generation]]** — Identity-preserving personalization and instruction-guided video editing both emerge from post-training on a large base model with no architectural changes. This extends the pre-train/post-train paradigm into fine-grained creative control: the marginal cost of a new creative specialization drops from "train a new model" to "curate post-training data," restructuring build-vs-adapt economics for creative AI tooling.
- **→ [[themes/generative_media|Generative Media]]** — Using a distilled 8B LLaMA3 for inference-time prompt rewriting — combined with model averaging across SFT checkpoints trained with varied data, hyperparameters, and base checkpoints — shows that post-training methodology is as critical as pretraining scale for video generation quality and controllability.
- **→ [[themes/continual_learning|Continual Learning]]** — Production deployment of enterprise agents with continuous fine-tuning from operational feedback is an applied instantiation of continual learning, creating pressure for infrastructure that supports frequent, non-disruptive model updates from live production signals without catastrophic forgetting.
- **← Document Understanding** — A commodity OCR pipeline producing tens of millions of digitised pages per day substantially lowers the barrier to assembling large-scale document corpora for post-training and distillation, particularly for structured text extraction from PDFs, scans, and historical materials.
- **← [[themes/adaptive_computation|Adaptive Computation]]** — Multi-timescale update mechanisms — where different components update at different frequencies — suggest a principled alternative to static post-training fine-tuning: models could learn to adapt at the right timescale, potentially making RLHF and SFT more sample-efficient.

## Contradictions

- The post-training capability amplification breakthrough implies that organizations without large pretraining compute can close capability gaps via fine-tuning and distillation — yet the generalization ceiling limitation implies those gaps will persist on reasoning and novel problem-solving, which are precisely the capabilities that matter most for agentic use cases. The resolution space here (whether RL-based post-training can eventually close the reasoning gap) is an active open question.

## Research Opportunities

- **Continual learning infrastructure for production pipelines** — The continuous fine-tuning loop pattern is real but constrained by catastrophic forgetting. Practical forgetting avoidance mechanisms that operate under the non-disruptive update constraint (no service interruption, frequent cadence) would unlock this pattern for a much broader class of tasks.
- **Generalizing the feedback signal** — Current production loops consume structured telemetry (false negatives, human overrides). Extending to richer, less structured operational signals would broaden the class of behaviors that can be improved continuously.
- **Timescale-aware post-training** — Translating multi-timescale update mechanisms from neuroscience-inspired adaptive computation research into concrete SFT/RLHF improvements is a tractable near-term research direction with potentially high sample-efficiency payoff.
- **Corpus assembly automation** — As OCR pipelines scale, the question shifts from "can we get enough data" to "how do we filter and structure it for post-training quality." Automated corpus curation for domain-specific fine-tuning is an underexplored engineering-research boundary.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 61 sources.
- **2026-02-17** — [[sources/01KJT1CPWR-improving-interactive-in-context-learning-from-natural-language-feedback|Improving Interactive In-Context Learning from Natural Language Feedback]]: Current flagship LLMs struggle to integrate corrective feedback on hard reasoning tasks, revealing s
- **2026-01-28** — [[sources/01KJT1VZTM-reinforcement-learning-via-self-distillation|Reinforcement Learning via Self-Distillation]]: Limitation identified: Off-policy self-distillation (SFT on teacher-generated successes) substantially 
- **2025-12-18** — [[sources/01KJT38XNY-adaptation-of-agentic-ai|Adaptation of Agentic AI]]: New capability: LoRA performs equivalently to full fine-tuning in RL settings even at very small
- **2025-12-04** — [[sources/01KJT5MN24-the-universal-weight-subspace-hypothesis|The Universal Weight Subspace Hypothesis]]: Breakthrough: Universal subspace-based model merging analytically outperforms all SOTA gradien
- **2025-11-26** — [[sources/01KJT6V2CT-monet-reasoning-in-latent-visual-space-beyond-images-and-language|Monet: Reasoning in Latent Visual Space Beyond Images and Language]]: The Monet-SFT-125K dataset contains 125K image-text interleaved CoT samples from real-world, documen
- **2025-11-21** — [[sources/01KJT7H2D2-downscaling-intelligence-exploring-perception-and-reasoning-bottlenecks-in-small|Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models]]: Visual extraction tuning is a training paradigm in which the model explicitly learns to extract the 
- **2025-11-11** — [[sources/01KJT9Y5SJ-the-path-not-taken-rlvr-provably-learns-off-the-principals|The Path Not Taken: RLVR Provably Learns Off the Principals]]: New capability: Theory-guided sparse RL fine-tuning using a 'safe mask' of non-principal, low-ma
- **2025-11-09** — [[sources/01KJTA8224-tiny-model-big-logic-diversity-driven-optimization-elicits-large-model-reasoning|Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B]]: New capability: The Spectrum-to-Signal Principle (SSP) decouples SFT and RL into complementary o
- **2025-10-29** — [[sources/01KJTC6DXZ-supervised-reinforcement-learning-from-expert-trajectories-to-step-wise-reasonin|Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning]]: Directly applying SFT on the s1K challenging dataset leads to performance degradation compared to th
- **2025-10-16** — [[sources/01KJVERVWW-why-rl-won-kyle-corbitt-openpipe-acq-coreweave|Why RL Won — Kyle Corbitt, OpenPipe (acq. CoreWeave)]]: Breakthrough: Task-specific RL training validated to achieve frontier-level performance on ent
- **2025-10-16** — [[sources/01KJTD7NB3-continual-learning-via-sparse-memory-finetuning|Continual Learning via Sparse Memory Finetuning]]: Limitation identified: LoRA systematically learns less than full finetuning while achieving less catast
- **2025-10-09** — [[sources/01KJTDMNGQ-agent-learning-via-early-experience|Agent Learning via Early Experience]]: Most current language agents rely on supervised fine-tuning on expert data, which is challenging to 
- **2025-09-29** — [[sources/01KJT3ZXPZ-from-fx-and-gx-to-fgx-llms-learn-new-skills-in-rl-by-composing-old-ones|From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones]]: Limitation identified: RFT (rejection fine-tuning / supervised learning on correct trajectories) on com
- **2025-09-29** — [[sources/01KJTFKNRP-evolution-strategies-at-scale-llm-fine-tuning-beyond-reinforcement-learning|Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning]]: Breakthrough: First successful application of Evolution Strategies to full-parameter fine-tuni
- **2025-09-16** — [[sources/01KJTJ3WVG-towards-general-agentic-intelligence-via-environment-scaling|Towards General Agentic Intelligence via Environment Scaling]]: New capability: 30B MoE open-source agent (AgentScaler-30B-A3B) achieves function-calling perfor
- **2025-09-11** — [[sources/01KJTJSM72-llm-jepa-large-language-models-meet-joint-embedding-predictive-architectures|LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures]]: New capability: LLM fine-tuning with JEPA objective exhibits systematic resistance to overfittin
- **2025-09-04** — [[sources/01KJTKM1EW-rls-razor-why-online-reinforcement-learning-forgets-less|RL's Razor: Why Online Reinforcement Learning Forgets Less]]: Forward KL divergence (R²=0.96) outperforms all alternative metrics as a predictor of forgetting, in
- **2025-08-06** — [[sources/01KJTMK79E-chain-of-agents-end-to-end-agent-foundation-models-via-multi-agent-distillation-|Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL]]: Breakthrough: Multi-agent distillation: systematic method for transferring collaborative intel
- **2025-07-29** — [[sources/01KJTMV92B-persona-vectors-monitoring-and-controlling-character-traits-in-language-models|Persona Vectors: Monitoring and Controlling Character Traits in Language Models]]: Persona vectors are computed as the difference in mean activations between model responses that exhi
- **2025-07-02** — [[sources/01KJTP54EY-naturalthoughts-selecting-and-distilling-reasoning-traces-for-general-reasoning-|NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks]]: Breakthrough: Scaling high-quality diverse reasoning distillation data consistently improves s
- **2025-07-01** — [[sources/01KJTP56NV-does-math-reasoning-improve-general-llm-capabilities-understanding-transferabili|Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning]]: RL models show markedly smaller average token-rank shifts than SFT models; UniReason-Qwen3-14B-RL av
- **2025-06-30** — [[sources/01KJTNW0W4-thinking-with-images-for-multimodal-reasoning-foundations-methods-and-future-fro|Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers]]: The dominant multimodal reasoning paradigm ('Thinking about Images') treats the visual modality as a
- **2025-06-12** — [[sources/01KJTQCEKY-the-diffusion-duality|The Diffusion Duality]]: Duo uses a 170M-parameter modified Diffusion Transformer (DiT) with rotary positional encoding, trai
- **2025-06-02** — [[sources/01KJTQRK41-small-language-models-are-the-future-of-agentic-ai|Small Language Models are the Future of Agentic AI]]: New capability: Parameter-efficient fine-tuning (LoRA, DoRA) of SLMs requires only a few GPU-hou
- **2025-05-30** — [[sources/01KJTQZ7NZ-continual-learning-in-vision-language-models-via-aligned-model-merging|Continual Learning in Vision-Language Models via Aligned Model Merging]]: New capability: During-training parameter alignment for LoRA merging preserves plasticity while 
- **2025-05-21** — [[sources/01KJTTJRKW-the-unreasonable-effectiveness-of-entropy-minimization-in-llm-reasoning|The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning]]: New capability: Unsupervised finetuning via direct token-level entropy minimization (EM-FT) impr
- **2025-05-17** — [[sources/01KJTT48H0-model-merging-in-pre-training-of-large-language-models|Model Merging in Pre-training of Large Language Models]]: Merging checkpoints from the stable (constant learning rate) training phase produces consistent and 
- **2025-05-14** — [[sources/01KJTVG7CE-qwen3-technical-report|Qwen3 Technical Report]]: Breakthrough: Strong-to-weak distillation demonstrated to outperform full RL training for smal
- **2025-05-05** — [[sources/01KJTV56AP-rm-r1-reward-modeling-as-reasoning|RM-R1: Reward Modeling as Reasoning]]: Limitation identified: Distillation-only training for reward models causes overfitting to surface patte
- **2025-04-29** — [[sources/01KJTX3RQ3-x-fusion-introducing-new-modality-to-frozen-large-language-models|X-Fusion: Introducing New Modality to Frozen Large Language Models]]: New capability: Vision tower initialization from a pretrained text-to-image DiT model enables kn
- **2025-04-22** — [[sources/01KJTYN6R6-π-05-a-vision-language-action-model-with-open-world-generalization|$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization]]: 97.6% of training examples provided to π0.5 during the first training phase do not come from mobile 
- **2025-04-22** — [[sources/01KJTY7ADE-tina-tiny-reasoning-models-via-lora|Tina: Tiny Reasoning Models via LoRA]]: Breakthrough: LoRA-based RL post-training achieves reasoning performance competitive with or e
- **2025-04-16** — [[sources/01KJTZV5JK-climbing-the-ladder-of-reasoning-what-llms-can-and-still-cant-solve-after-sft|Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?]]: New capability: SFT on 500–1K R1-style trajectories enables 32B base models to reach ~90% accura
- **2025-04-14** — [[sources/01KJTZYPKZ-reasoning-models-can-be-effective-without-thinking|Reasoning Models Can Be Effective Without Thinking]]: NoThinking is implemented by prefilling the assistant response with a fabricated dummy thinking bloc
- **2025-04-05** — [[sources/01KJSVB9E8-rl-backlog-openais-many-rls-clarifying-distillation-and-latent-reasoning|RL backlog: OpenAI's many RLs, clarifying distillation, and latent reasoning]]: Limitation identified: SFT distillation narrows the behavioral distribution of a model, constraining th
- **2025-03-26** — [[sources/01KJV2A0J3-qwen25-omni-technical-report|Qwen2.5-Omni Technical Report]]: The vision encoder uses flash attention with an MLP layer that merges adjacent 2×2 tokens into a sin
- **2025-03-24** — [[sources/01KKT4WS4T-adaworld-learning-adaptable-world-models-with-latent-actions|AdaWorld: Learning Adaptable World Models with Latent Actions]]: The latent action autoencoder uses an information bottleneck design with a Transformer architecture 
- **2025-03-11** — [[sources/01KJV2VB8A-proc4gem-foundation-models-for-physical-agency-through-procedural-generation|Proc4Gem: Foundation models for physical agency through procedural generation]]: Proc4Gem uses a hierarchical procedural generation pipeline to sample realistic indoor living-room s
- **2025-03-11** — [[sources/01KKT5AKA5-gemini-robotics-bringing-ai-into-the-physical|Gemini Robotics: Bringing AI into the Physical]]: Gemini 2.0 cannot perform complex motion planning such as obstacle avoidance in trajectory predictio
- **2025-02-19** — [[sources/01KJV42M0K-qwen25-vl-technical-report|Qwen2.5-VL Technical Report]]: Qwen2.5-VL-72B achieves mIoU of 50.9 on Charades-STA for temporal video grounding, surpassing GPT-4o
- **2025-02-12** — [[sources/01KJV44APF-llm-pretraining-with-continuous-concepts|LLM Pretraining with Continuous Concepts]]: New capability: Sparse autoencoder concepts extracted from a small reference model (124M paramet
- **2025-02-05** — [[sources/01KJV4D5YX-demystifying-long-chain-of-thought-reasoning-in-llms|Demystifying Long Chain-of-Thought Reasoning in LLMs]]: Limitation identified: Short CoT SFT initialisation structurally prevents meaningful RL improvement — m
- **2025-01-31** — [[sources/01KJV4M1H3-s1-simple-test-time-scaling|s1: Simple test-time scaling]]: New capability: Combining difficulty, diversity, and quality in data curation produces a 1,000-s
- **2025-01-09** — [[sources/01KJV56ZJP-transformer-squared-self-adaptive-llms|Transformer-Squared: Self-adaptive LLMs]]: Breakthrough: SVF achieves full-rank parameter-efficient fine-tuning with orders-of-magnitude 
- **2024-12-24** — [[sources/01KJVGAVH2-best-of-2024-synthetic-data-smol-models-loubna-ben-allal-huggingface-ls-live-neu|Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace [LS Live! @ NeurIPS 2024]]]: FineWeb-Edu was created by using Llama 3 to rate educational quality of web pages 0–5, training a BE
- **2024-12-19** — [[sources/01KJV5SBG0-lmfusion-adapting-pretrained-language-models-for-multimodal-generation|LMFusion: Adapting Pretrained Language Models for Multimodal Generation]]: Learning rate decoupling (ratio 0.1) reduces the language performance gap from 7% to 2% in dense mod
- **2024-12-18** — [[sources/01KJV5Z0M1-inference-aware-fine-tuning-for-best-of-n-sampling-in-large-language-models|Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models]]: BoN-RL-S significantly improves pass@32 of Gemma 2B on MATH from 60.0% to 67.0%.
- **2024-12-06** — [[sources/01KJVJDB5G-reinforcement-fine-tuning12-days-of-openai-day-2|Reinforcement Fine-Tuning—12 Days of OpenAI: Day 2]]: Breakthrough: Fine-tuned smaller models now exceed larger base models on specialized reasoning
- **2024-11-25** — [[sources/01KJV6JNEC-o1-replication-journey-part-2-surpassing-o1-preview-through-simple-distillation-|O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?]]: Breakthrough: Simple knowledge distillation from O1's API plus standard SFT — requiring no nov
- **2024-11-22** — [[sources/01KJV6PJWC-tulu-3-pushing-frontiers-in-open-language-model-post-training|Tulu 3: Pushing Frontiers in Open Language Model Post-Training]]: Breakthrough: First fully open-source, reproducible post-training pipeline (SFT + DPO + RLVR) 
- **2024-11-21** — [[sources/01KJVKPGFR-everything-you-wanted-to-know-about-llm-post-training-with-nathan-lambert-of-all|Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI]]: New capability: Off-the-shelf SFT/DPO/RL fine-tuning datasets achieve 80–95% of optimal performa
- **2024-10-30** — [[sources/01KJVKZAT6-training-zamba-a-hybrid-model-master-class-with-zyphras-quentin-anthony|Training Zamba: A Hybrid Model Master Class with Zyphra's Quentin Anthony]]: New capability: LoRA adapters on shared MLP blocks within hybrid architectures provide per-depth
- **2024-10-15** — [[sources/01KJV7DD3S-latent-action-pretraining-from-videos|Latent Action Pretraining from Videos]]: LAPA uses a VQ-VAE-based objective to learn discrete latent actions between image frames in a fully 
- **2024-10-14** — [[sources/01KJV7N48D-thinking-llms-general-instruction-following-with-thought-generation|Thinking LLMs: General Instruction Following with Thought Generation]]: In the TPO setup, thoughts are hidden from the end user and only the response part is shown, differe
- **2024-09-19** — [[sources/01KJV83GN1-training-language-models-to-self-correct-via-reinforcement-learning|Training Language Models to Self-Correct via Reinforcement Learning]]: SCoRe achieves a 12.2% intrinsic self-correction delta on HumanEval, 9% higher than the base model, 
- **2024-09-10** — [[sources/01KJV8BD2M-kag-boosting-llms-in-professional-domains-via-knowledge-augmented-generation|KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation]]: New capability: KAG-Model fine-tuning with 20,000+ diverse NLU instructions improves NLU and NLI
- **2024-08-21** — [[sources/01KJV8WEM4-llm-pruning-and-distillation-in-practice-the-minitron-approach|LLM Pruning and Distillation in Practice: The Minitron Approach]]: Breakthrough: Teacher correction removes the hard dependency on original pretraining data for 
- **2024-06-13** — [[sources/01KJV8JK29-openvla-an-open-source-vision-language-action-model|OpenVLA: An Open-Source Vision-Language-Action Model]]: New capability: VLA models can be fine-tuned on consumer GPUs via LoRA without compromising down
- **2024-04-11** — [[sources/01KJVN834B-robotics-in-the-age-of-generative-ai-with-vincent-vanhoucke-google-deepmind-nvid|Robotics in the Age of Generative AI with Vincent Vanhoucke, Google DeepMind | NVIDIA GTC 2024]]: RT1 is an end-to-end transformer model that tokenizes language instructions and images and outputs e
- **2024-02-01** — [[sources/01KJV9HBN6-executable-code-actions-elicit-better-llm-agents|Executable Code Actions Elicit Better LLM Agents]]: New capability: 7B fine-tuned open-source agents (CodeActAgent on Mistral-7B) can use the full P
- **2023-09-01** — [[sources/01KJV8MTT2-rlaif-vs-rlhf-scaling-reinforcement-learning-from-human-feedback-with-ai-feedbac|RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback]]: For harmless dialogue generation, RLAIF outperforms RLHF, with harmless rates of 88%, 76%, and 64% f
