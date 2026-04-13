---
type: theme
title: Post-Training Methods
theme_id: post_training_methods
level: 1
parent_theme: meta_foundations
child_themes:
- finetuning_and_distillation
- synthetic_data_generation
- in_context_and_meta_learning
- test_time_learning
- reinforcement_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 118
sources_since_update: 0
update_count: 1
velocity: 0.043
staleness: 0.0
status: active
tags: []
---
# Post-Training Methods

> Post-training methods are navigating a fundamental tension between specialization and generality. The field has grown sophisticated enough to fine-tune foundation models for narrow domains, but not yet sophisticated enough to do so without eroding what made them general. The current trajectory is shifting away from weight-modification as the primary adaptation strategy, toward inference-time scaffolding as a forgetting-avoidance alternative, with momentum concentrated around state-aware reasoning frameworks that have shown clinically relevant gains in controlled settings. Whether this pivot constitutes a genuine paradigm shift or a temporary workaround remains the central open question.

**Parent:** [[themes/meta_foundations|meta_foundations]]
**Sub-themes:** [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/test_time_learning|test_time_learning]], [[themes/reinforcement_learning|reinforcement_learning]]

## Current State

The defining story of post-training methods as of mid-2025 is one of a paradigm running into its ceiling precisely when deployment pressure is highest.

Supervised fine-tuning of multimodal foundation models for targeted clinical tasks (ECG analysis being the concrete case on record) measurably degrades performance on adjacent consultation tasks, including management plan quality. This is catastrophic forgetting in a clinically consequential form, and what is notable about the current moment is not that the problem exists but that it remains classified as stable in trajectory: no clear resolution is emerging, and the estimated resolution horizon sits at one to two years. The standard fine-tuning paradigm has not found an algorithmic path to specialization that preserves generality.

The response visible in the evidence is a reorientation rather than a fix. Inference-time domain specialization via state-aware reasoning frameworks has demonstrated clinically relevant gains in multimodal medical settings without modifying model parameters at all. This approach is currently at research-only maturity: it works in controlled conditions but has not cleared the bar for deployment. The architectural implication is significant. Post-training is being reframed not as weight modification but as reasoning scaffolding, sidestepping the forgetting problem by not touching the weights that encode general knowledge in the first place.

A separate thread, neural trajectory co-training during post-training for humanoid robotics, shows consistent additive gains over real-data finetuning across simulation and physical tasks, currently at demo maturity. This suggests the post-training toolkit is expanding beyond language and vision into embodied domains, though the evidence base here is thin relative to the clinical thread.

Momentum is concentrated around inference-time adaptation as a forgetting-avoidance strategy. The field is watching whether state-aware reasoning frameworks move from research-only to reproducible demo status, whether any technique demonstrates specialization with preserved generality (which would resolve the core bottleneck), and whether the robotics co-training results replicate across more task distributions.

## Capabilities

- **Inference-time domain specialization** via state-aware reasoning frameworks can achieve strong multimodal medical performance without parameter modification. Maturity: research-only (controlled conditions; not yet deployment-ready).
- **Neural trajectory co-training** during post-training provides consistent additive gains over real-data-only finetuning in humanoid robotics, with reported improvements of +4 across simulation and physical tasks. Maturity: demo.

## Limitations

- **Catastrophic forgetting in domain-specific fine-tuning.** Supervised fine-tuning of multimodal foundation models for targeted clinical tasks (e.g., ECG analysis) measurably degrades performance on adjacent tasks (e.g., management plan quality). Severity: significant. Trajectory: stable (no resolution emerging). Type: implicit performance cliff, surfacing under deployment conditions rather than in narrow benchmarks.

## Bottlenecks

- **Specialization without generality loss.** Domain-specific fine-tuning causes catastrophic forgetting in multimodal medical models, and no established method exists to prevent it. This directly blocks the construction of specialized multimodal clinical AI that can excel at targeted diagnostics while maintaining broad consultation quality. Status: active. Resolution horizon: 1-2 years.

## Breakthroughs

No confirmed breakthroughs recorded for this theme yet. The inference-time domain specialization result is a capability advance at research-only maturity; it becomes a breakthrough if it demonstrates generalizable deployment-grade performance beyond the specific setups where it has been demonstrated.

## Anticipations

- If state-aware reasoning frameworks mature to reproducible demo status, they may establish inference-time adaptation as a viable alternative to fine-tuning across a broader range of domains, not just clinical AI.
- If any technique demonstrates specialization with preserved generality (i.e., solves the catastrophic forgetting bottleneck), it would shift the entire trajectory of this theme and unlock the next generation of domain-specific foundation model deployment.

## Cross-Theme Implications

- The catastrophic forgetting bottleneck has direct implications for [[themes/finetuning_and_distillation|finetuning_and_distillation]]: it constrains the conditions under which distillation and fine-tuning can be applied to multimodal models without degrading general capabilities.
- The inference-time specialization pivot connects to [[themes/test_time_learning|test_time_learning]]: both treat adaptation as a runtime phenomenon rather than a training-time one, and breakthroughs in either thread may transfer to the other.
- The neural trajectory co-training result in robotics links to [[themes/reinforcement_learning|reinforcement_learning]], where the question of how to combine real and synthetic experience during post-training is actively contested.
- [[themes/synthetic_data_generation|synthetic_data_generation]] is upstream of this theme: the quality and distribution of synthetic post-training data directly determines whether specialization gains come at the cost of generality.

## Contradictions

- The field is simultaneously pursuing two strategies whose underlying assumptions are in tension: (1) fine-tuning as the path to domain specialization, and (2) inference-time adaptation as the path to domain specialization without fine-tuning. If the second approach scales, it calls into question the investment in the first.
- The robotics co-training result (additive gains over real-data finetuning) sits alongside the clinical forgetting result (fine-tuning degrades adjacent performance). These are not necessarily contradictory (different domains, different architectures), but they suggest the costs and benefits of post-training weight modification are highly domain-dependent in ways that are not yet well-characterized.

## Research Opportunities

- Developing fine-tuning methods that explicitly preserve general performance while achieving targeted specialization, particularly for multimodal medical models. This would directly resolve the core bottleneck.
- Scaling and stress-testing state-aware inference-time frameworks beyond the clinical settings where they have been demonstrated, to determine whether the forgetting-avoidance benefit generalizes.
- Characterizing the conditions under which neural trajectory co-training provides additive gains, to assess whether the robotics results generalize to other embodied domains or to language and vision settings.
- Establishing a principled taxonomy of when inference-time adaptation is sufficient versus when weight modification is necessary, to guide practitioners choosing between approaches.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KKT4ZV99-dont-throw-the-baby-out-with-the-bathwater-how|DON’T THROW THE BABY OUT WITH THE BATHWATER: HOW]]: Deep learning with test-time fine-tuning achieves state-of-the-art performance on ARC-AGI, reaching 
- **2026-04-08** — [[sources/01KJS48D4H-context-engineering-for-ai-agents-lessons-from-building-manus|Context Engineering for AI Agents: Lessons from Building Manus]]: With Claude Sonnet, cached input tokens cost 0.30 USD/MTok versus 3 USD/MTok for uncached tokens, a 
- **2026-04-08** — Wiki page created. Theme has 118 sources.
- **2026-02-17** — [[sources/01KJT1CPWR-improving-interactive-in-context-learning-from-natural-language-feedback|Improving Interactive In-Context Learning from Natural Language Feedback]]: Current flagship LLMs struggle to integrate corrective feedback on hard reasoning tasks, revealing s
- **2026-01-28** — [[sources/01KJT1VZTM-reinforcement-learning-via-self-distillation|Reinforcement Learning via Self-Distillation]]: SDPO treats the current model conditioned on feedback as a self-teacher and distills its feedback-in
- **2026-01-22** — [[sources/01KJT1PH9D-learning-to-discover-at-test-time|Learning to Discover at Test Time]]: TTT-Discover performs reinforcement learning at test time, allowing the LLM to continue training wit
- **2025-12-29** — [[sources/01KJT2PY1B-end-to-end-test-time-training-for-long-context|End-to-End Test-Time Training for Long Context]]: TTT via next-token prediction has O(T) complexity for prefill and O(1) for decode.
- **2025-12-18** — [[sources/01KJT4G8AA-meta-rl-induces-exploration-in-language-agents|Meta-RL Induces Exploration in Language Agents]]: LAMER is evaluated using Qwen3-4B as the base model across all primary experiments.
- **2025-12-18** — [[sources/01KJT38XNY-adaptation-of-agentic-ai|Adaptation of Agentic AI]]: The T2 approach (s3) achieves 58.9% average accuracy with only 2,400 training samples by training a 
- **2025-12-15** — [[sources/01KJT4T78E-lets-not-just-put-things-in-context-test-time-training-for-long-context-llms|Let's (not) just put things in Context: Test-Time Training for Long-Context LLMs]]: qTTT's objective is the standard next-token prediction loss computed over a small randomly sampled c
- **2025-12-04** — [[sources/01KJT5MN24-the-universal-weight-subspace-hypothesis|The Universal Weight Subspace Hypothesis]]: Over 1100 models — including 500 Mistral-7B LoRAs, 500 Vision Transformers, and 50 LLaMA-8B models —
- **2025-12-04** — [[sources/01KJT62ZGZ-nex-n1-agentic-models-trained-via-a-unified-ecosystem-for-large-scale-environmen|Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment Construction]]: NexAU adopts a recursive, fractal architecture inspired by the ReAct paradigm, treating sub-agents, 
- **2025-12-02** — [[sources/01KJT6M5JK-deepseek-v32-pushing-the-frontier-of-open-large-language-models|DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models]]: DeepSeek-V3.2 introduces DeepSeek Sparse Attention (DSA), which reduces attention computational comp
- **2025-12-02** — [[sources/01KKT3NJ4Y-nested-learning-the-illusion-of-deep-learning-architecture|Nested Learning: The Illusion of Deep Learning Architecture]]: Delta Gradient Descent extends basic gradient descent with a more expressive L2 regression loss obje
- **2025-11-28** — [[sources/01KJT6RXNS-thetaevolve-test-time-learning-on-open-problems|ThetaEvolve: Test-time Learning on Open Problems]]: AlphaEvolve is a closed-source system.
- **2025-11-26** — [[sources/01KJT6V2CT-monet-reasoning-in-latent-visual-space-beyond-images-and-language|Monet: Reasoning in Latent Visual Space Beyond Images and Language]]: Monet introduces a three-stage distillation-based SFT pipeline that enables MLLMs to generate contin
- **2025-11-25** — [[sources/01KJT71V4Q-evo-memory-benchmarking-llm-agent-test-time-learning-with-self-evolving-memory|Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory]]: ReMem's performance improvement strongly correlates with within-dataset task similarity (Pearson r=0
- **2025-11-21** — [[sources/01KJT7H2D2-downscaling-intelligence-exploring-perception-and-reasoning-bottlenecks-in-small|Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models]]: Visual extraction tuning is a training paradigm in which the model explicitly learns to extract the 
- **2025-11-11** — [[sources/01KJT9Y5SJ-the-path-not-taken-rlvr-provably-learns-off-the-principals|The Path Not Taken: RLVR Provably Learns Off the Principals]]: RLVR update sparsity (fraction of unchanged parameters) ranges from 36% to 92% across models, while 
- **2025-11-09** — [[sources/01KJTA8224-tiny-model-big-logic-diversity-driven-optimization-elicits-large-model-reasoning|Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B]]: MGPO degrades to standard GRPO when the regularization coefficient λ=0, and increases focus on uncer
- **2025-11-06** — [[sources/01KJTAMFNJ-v-thinker-interactive-thinking-with-images|V-Thinker: Interactive Thinking with Images]]: V-Thinker treats reasoning as a code-driven visual interaction process where at each step the model 
- **2025-11-05** — [[sources/01KJTASF4S-scaling-agent-learning-via-experience-synthesis|Scaling Agent Learning via Experience Synthesis]]: RL training for LLM agents is challenging due to costly rollouts, limited task diversity, unreliable
- **2025-11-03** — [[sources/01KJTBNSX3-simulating-environments-with-reasoning-models-for-agent-training|Simulating Environments with Reasoning Models for Agent Training]]: A 32B model fine-tuned on Simia-simulated trajectories (based on Qwen2.5-32B-Instruct) surpasses GPT
- **2025-10-29** — [[sources/01KJTC6DXZ-supervised-reinforcement-learning-from-expert-trajectories-to-step-wise-reasonin|Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning]]: Directly applying SFT on the s1K challenging dataset leads to performance degradation compared to th
- **2025-10-22** — [[sources/01KJTCHAPG-loongrl-reinforcement-learning-for-advanced-reasoning-over-long-contexts|LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts]]: A two-way substring exact match reward verifier is used as a rule-based reward, where a trajectory r
- **2025-10-17** — [[sources/01KKT3SS8Q-deepseek-ocr-contexts-optical-compression|DeepSeek-OCR: Contexts Optical Compression]]: DeepSeek-OCR (Gundam mode, 795 tokens) achieves an overall OmniDocBench edit distance of 0.083, outp
- **2025-10-16** — [[sources/01KJTD7NB3-continual-learning-via-sparse-memory-finetuning|Continual Learning via Sparse Memory Finetuning]]: LoRA finetuning on new facts causes a 71% drop in NaturalQuestions F1 score
- **2025-10-16** — [[sources/01KJVERVWW-why-rl-won-kyle-corbitt-openpipe-acq-coreweave|Why RL Won — Kyle Corbitt, OpenPipe (acq. CoreWeave)]]: OpenPipe, a fine-tuning and task-specific RL platform, was acquired by CoreWeave approximately two y
- **2025-10-09** — [[sources/01KJTDMNGQ-agent-learning-via-early-experience|Agent Learning via Early Experience]]: Early experience is positioned as a practical bridge between imitation learning and fully experience
- **2025-10-08** — [[sources/01KJTE0Y5S-h1-bootstrapping-llms-to-reason-over-longer-horizons-via-reinforcement-learning|h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning]]: Curriculum RL training on composed GSM8K problems achieves a 2.06× improvement on AIME 2024 relative
- **2025-10-06** — [[sources/01KJTEBGCX-agentic-context-engineering-evolving-contexts-for-self-improving-language-models|Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models]]: ACE uses incremental delta updates—small sets of candidate bullets—rather than full context rewrites
- **2025-09-29** — [[sources/01KJTFKNRP-evolution-strategies-at-scale-llm-fine-tuning-beyond-reinforcement-learning|Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning]]: Evolution Strategies (ES) can successfully fine-tune LLMs at the billion-parameter scale through dir
- **2025-09-29** — [[sources/01KJT3ZXPZ-from-fx-and-gx-to-fgx-llms-learn-new-skills-in-rl-by-composing-old-ones|From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones]]: RL on Level-2 compositional problems improves held-out Level-3 accuracy from near-zero (~5%) to appr
- **2025-09-24** — [[sources/01KJVT4GRY-ai-talent-wars-xais-200b-valuation-googles-comeback|AI Talent Wars, xAI’s $200B Valuation, & Google’s Comeback]]: RL is highly effective in domains with clear, verifiable answers such as math and coding, which expl
- **2025-09-24** — [[sources/01KJTGT235-thinking-augmented-pre-training|Thinking Augmented Pre-training]]: Thinking Augmented Pre-Training (TPT) enhances the data efficiency of LLM pre-training by a factor o
- **2025-09-16** — [[sources/01KJTJ3WVG-towards-general-agentic-intelligence-via-environment-scaling|Towards General Agentic Intelligence via Environment Scaling]]: The AgentScaler framework collected more than 30,000 APIs from ToolBench, API-Gen, and an internal t
- **2025-09-11** — [[sources/01KJTJSM72-llm-jepa-large-language-models-meet-joint-embedding-predictive-architectures|LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures]]: For Llama-3.2-1B-Instruct on GSM8K fine-tuning, LLM-JEPA achieves 70.4% accuracy versus 56.0% for th
- **2025-09-04** — [[sources/01KJTKM1EW-rls-razor-why-online-reinforcement-learning-forgets-less|RL's Razor: Why Online Reinforcement Learning Forgets Less]]: Off-policy RL algorithms were not studied, leaving their forgetting behavior relative to on-policy m
- **2025-09-04** — [[sources/01KJTERZ79-arcmemo-abstract-reasoning-composition-with-lifelong-llm-memory|ArcMemo: Abstract Reasoning Composition with Lifelong LLM Memory]]: ArcMemo-PS achieves a 7.5% relative gain over a strong no-memory baseline on ARC-AGI-1, improving of
- **2025-08-06** — [[sources/01KJTMK79E-chain-of-agents-end-to-end-agent-foundation-models-via-multi-agent-distillation-|Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL]]: AFM achieves 59.8% on AIME2025 benchmark, an absolute improvement of over 10.5% compared to previous
- **2025-07-29** — [[sources/01KJTMV92B-persona-vectors-monitoring-and-controlling-character-traits-in-language-models|Persona Vectors: Monitoring and Controlling Character Traits in Language Models]]: Persona vectors are computed as the difference in mean activations between model responses that exhi
- **2025-07-25** — [[sources/01KJTMXXZG-gepa-reflective-prompt-evolution-can-outperform-reinforcement-learning|GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning]]: GEPA works off-the-shelf on closed-source models, achieving +12.19% aggregate improvement on GPT-4.1
- **2025-07-21** — [[sources/01KJTNBZH1-learning-without-training-the-implicit-dynamics-of-in-context-learning|Learning without training: The implicit dynamics of in-context learning]]: The implicit weight update formula for a contextual block is exact: the output of the contextual blo
- **2025-07-02** — [[sources/01KJTP54EY-naturalthoughts-selecting-and-distilling-reasoning-traces-for-general-reasoning-|NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks]]: Simply scaling up data size with random sampling is a strong baseline that yields steady performance
- **2025-07-01** — [[sources/01KJTP56NV-does-math-reasoning-improve-general-llm-capabilities-understanding-transferabili|Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning]]: UniReason-Qwen3-14B trained with RL on 47K math examples achieves 55.7% on AIME24, 87.8% on MATH500,
- **2025-06-30** — [[sources/01KJTNW0W4-thinking-with-images-for-multimodal-reasoning-foundations-methods-and-future-fro|Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers]]: The dominant multimodal reasoning paradigm ('Thinking about Images') treats the visual modality as a
- **2025-06-23** — [[sources/01KJTPFD62-omnigen2-exploration-to-advanced-multimodal-generation|OmniGen2: Exploration to Advanced Multimodal Generation]]: OmniGen2 achieves a GenEval overall score of 0.86 with an LLM rewriter, surpassing UniWorld-V1 (0.84
- **2025-06-12** — [[sources/01KJTQCH1T-self-adapting-language-models|Self-Adapting Language Models]]: Using base Qwen-2.5-7B synthetic data (without RL) for knowledge incorporation yields 39.7% accuracy
- **2025-06-12** — [[sources/01KJTQCEKY-the-diffusion-duality|The Diffusion Duality]]: Duo uses a 170M-parameter modified Diffusion Transformer (DiT) with rotary positional encoding, trai
- **2025-06-02** — [[sources/01KJTQRK41-small-language-models-are-the-future-of-agentic-ai|Small Language Models are the Future of Agentic AI]]: NVIDIA Nemotron-H hybrid Mamba-Transformer models (2/4.8/9bn) achieve instruction following and code
- **2025-05-30** — [[sources/01KJTQZ7NZ-continual-learning-in-vision-language-models-via-aligned-model-merging|Continual Learning in Vision-Language Models via Aligned Model Merging]]: PAM assumes that previous task data is not available when learning a new task and that task identity
- **2025-05-29** — [[sources/01KJTRVBMF-atlas-learning-to-optimally-memorize-the-context-at-test-time|ATLAS: Learning to Optimally Memorize the Context at Test Time]]: Most existing architectures use a surprise metric that updates memory based only on the current inpu
- **2025-05-29** — [[sources/01KJTRB1VP-test-time-training-done-right|Test-Time Training Done Right]]: Large Chunk Test-Time Training (LaCT) uses chunk sizes ranging from 2048 to 1 million tokens as the 
- **2025-05-21** — [[sources/01KJTTJRKW-the-unreasonable-effectiveness-of-entropy-minimization-in-llm-reasoning|The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning]]: Entropy minimization alone, without any labeled data, can substantially improve LLM performance on c
- **2025-05-17** — [[sources/01KJTT48H0-model-merging-in-pre-training-of-large-language-models|Model Merging in Pre-training of Large Language Models]]: Merging checkpoints from the stable (constant learning rate) training phase produces consistent and 
- **2025-05-14** — [[sources/01KJTVG7CE-qwen3-technical-report|Qwen3 Technical Report]]: Qwen3 uses YARN and Dual Chunk Attention during inference to achieve a four-fold increase in effecti
- **2025-05-06** — [[sources/01KJTWFMSP-absolute-zero-reinforced-self-play-reasoning-with-zero-data|Absolute Zero: Reinforced Self-play Reasoning with Zero Data]]: AZR uses three complementary reasoning modes—deduction, abduction, and induction—each corresponding 
- **2025-05-05** — [[sources/01KJTV56AP-rm-r1-reward-modeling-as-reasoning|RM-R1: Reward Modeling as Reasoning]]: RM-R1-DeepSeek-Distilled-Qwen-32B achieves the highest average score of 81.5 among all evaluated mod
- **2025-04-29** — [[sources/01KJTX3RQ3-x-fusion-introducing-new-modality-to-frozen-large-language-models|X-Fusion: Introducing New Modality to Frozen Large Language Models]]: Training on noisy images for I2T (understanding) tasks degrades image understanding performance, wit
- **2025-04-22** — [[sources/01KJTYN6R6-π-05-a-vision-language-action-model-with-open-world-generalization|$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization]]: Zero-shot prompting GPT-4 as the high-level policy achieves the worst performance among all baseline
- **2025-04-22** — [[sources/01KJTYK6PA-ttrl-test-time-reinforcement-learning|TTRL: Test-Time Reinforcement Learning]]: TTRL on Qwen2.5-Math-7B achieves an average gain of 76% across AIME 2024, AMC, MATH-500, and GPQA
- **2025-04-22** — [[sources/01KJTY7ADE-tina-tiny-reasoning-models-via-lora|Tina: Tiny Reasoning Models via LoRA]]: The total cost of reproducing all experiments in the Tina paper from scratch is $526 USD.
- **2025-04-17** — [[sources/01KJTZ9VS7-sleep-time-compute-beyond-inference-scaling-at-test-time|Sleep-time Compute: Beyond Inference Scaling at Test-time]]: Sleep-time compute is implemented by prompting a model to draw inferences and rewrite context in a w
- **2025-04-16** — [[sources/01KJTZV5JK-climbing-the-ladder-of-reasoning-what-llms-can-and-still-cant-solve-after-sft|Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?]]: Exh-level questions are not addressed by scaling SFT dataset size; all SFT models across all dataset
- **2025-04-14** — [[sources/01KJTZYPKZ-reasoning-models-can-be-effective-without-thinking|Reasoning Models Can Be Effective Without Thinking]]: Reasoning models such as DeepSeek-R1 approach complex tasks by generating long chains of thought as 
- **2025-04-10** — [[sources/01KJTZZW1M-dynamic-cheatsheet-test-time-learning-with-adaptive-memory|Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory]]: Claude 3.5 Sonnet's performance on AIME 2020–2024 surged from 6.7% to 40.6% under DC-RS.
- **2025-04-07** — [[sources/01KJV168T2-synthetic-data-generation-multi-step-rl-for-reasoning-tool-use|Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use]]: SWiRL does not require golden labels or human annotations, relying entirely on model-based judgments
- **2025-04-05** — [[sources/01KJSVB9E8-rl-backlog-openais-many-rls-clarifying-distillation-and-latent-reasoning|RL backlog: OpenAI's many RLs, clarifying distillation, and latent reasoning]]: OpenAI's Computer-Using Agent (CUA) is trained using reinforcement learning to interact with graphic
- **2025-04-03** — [[sources/01KJV181HF-inference-time-scaling-for-generalist-reward-modeling|Inference-Time Scaling for Generalist Reward Modeling]]: SPCT consists of two phases: rejective fine-tuning as a cold start and rule-based online RL that rei
- **2025-03-26** — [[sources/01KJV2A0J3-qwen25-omni-technical-report|Qwen2.5-Omni Technical Report]]: Qwen2.5-Omni is an end-to-end multimodal model that can perceive text, images, audio, and video whil
- **2025-03-24** — [[sources/01KKT4SWNY-reasoning-to-learn-from-latent-thoughts|Reasoning to Learn from Latent Thoughts]]: Augmenting pretraining data with GPT-4o-mini synthesized latent thoughts achieves 25.38% on MATH, si
- **2025-03-24** — [[sources/01KKT4WS4T-adaworld-learning-adaptable-world-models-with-latent-actions|AdaWorld: Learning Adaptable World Models with Latent Actions]]: In action transfer evaluation on LIBERO and SSv2, AdaWorld (continuous latent action) achieves FVD o
- **2025-03-18** — [[sources/01KKT532F3-2025-3-18|2025-3-18]]: New capability: Neural trajectory co-training during post-training provides consistent additive 
- **2025-03-11** — [[sources/01KJV2VB8A-proc4gem-foundation-models-for-physical-agency-through-procedural-generation|Proc4Gem: Foundation models for physical agency through procedural generation]]: Proc4Gem uses a hierarchical procedural generation pipeline to sample realistic indoor living-room s
- **2025-03-11** — [[sources/01KKT5AKA5-gemini-robotics-bringing-ai-into-the-physical|Gemini Robotics: Bringing AI into the Physical]]: Gemini Robotics excels at deformable object manipulation while baselines struggle with these tasks.
- **2025-03-09** — [[sources/01KJV2XQ8N-vision-r1-incentivizing-reasoning-capability-in-multimodal-large-language-models|Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models]]: Vision-R1-CI (cold-start only, no RL) on the Llama-3.2-11B base improves MathVista from 48.6% to 62.
- **2025-02-19** — [[sources/01KJV42M0K-qwen25-vl-technical-report|Qwen2.5-VL Technical Report]]: To handle varying image sizes during training, Qwen2.5-VL dynamically packs data samples based on in
- **2025-02-12** — [[sources/01KJV44APF-llm-pretraining-with-continuous-concepts|LLM Pretraining with Continuous Concepts]]: The attribution score in CoCoMix is computed as the element-wise product of the pre-activation conce
- **2025-02-05** — [[sources/01KJV4D5YX-demystifying-long-chain-of-thought-reasoning-in-llms|Demystifying Long Chain-of-Thought Reasoning in LLMs]]: A piecewise cosine reward function that incentivizes efficient use of inference compute stabilizes C
- **2025-01-31** — [[sources/01KJV4M1H3-s1-simple-test-time-scaling|s1: Simple test-time scaling]]: Supervised finetuning of Qwen2.5-32B-Instruct on s1K required only 26 minutes of training on 16 H100
- **2025-01-28** — [[sources/01KJVCSNWX-from-alphago-to-agi-ft-reflectionai-founder-ioannis-antonoglou|From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou]]: In-context learning is the ability of a model to learn a new task on the fly from a few examples, wi
- **2025-01-22** — [[sources/01KJV4YYAN-test-time-preference-optimization-on-the-fly-alignment-via-iterative-textual-fee|Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback]]: TPO-D2-N5 (10 total responses sampled) surpasses Best-of-N sampling with 30 and 60 samples, achievin
- **2025-01-09** — [[sources/01KJV56ZJP-transformer-squared-self-adaptive-llms|Transformer-Squared: Self-adaptive LLMs]]: SVF learns a vector z that scales the singular values of weight matrices, producing a new weight mat
- **2025-01-08** — [[sources/01KJV5D2Z7-rstar-math-small-llms-can-master-math-reasoning-with-self-evolved-deep-thinking|rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking]]: rStar-Math improves Qwen2.5-Math-7B from 58.8% to 90.0% on the MATH benchmark, surpassing o1-preview
- **2025-01-07** — [[sources/01KJV5GK45-cosmos-world-foundation-model-platform-for-physical-ai|Cosmos World Foundation Model Platform for Physical AI]]: Using an FP8-quantized TensorRT-LLM engine for VILA video captioning achieves a 10x speedup in throu
- **2024-12-31** — [[sources/01KJV5HWSH-titans-learning-to-memorize-at-test-time|Titans: Learning to Memorize at Test Time]]: The surprise metric with momentum is mathematically equivalent to gradient descent with momentum, wh
- **2024-12-24** — [[sources/01KJVGAVH2-best-of-2024-synthetic-data-smol-models-loubna-ben-allal-huggingface-ls-live-neu|Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace [LS Live! @ NeurIPS 2024]]]: Synthetic data is now used throughout the entire LLM pipeline, including both pre-training and post-
- **2024-12-19** — [[sources/01KJV5SBG0-lmfusion-adapting-pretrained-language-models-for-multimodal-generation|LMFusion: Adapting Pretrained Language Models for Multimodal Generation]]: Learning rate decoupling (ratio 0.1) reduces the language performance gap from 7% to 2% in dense mod
- **2024-12-18** — [[sources/01KJV5Z0M1-inference-aware-fine-tuning-for-best-of-n-sampling-in-large-language-models|Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models]]: BoN-aware fine-tuning improves Bo32 accuracy of Gemma 2B on Hendrycks MATH from 26.8% to 30.8%.
- **2024-12-06** — [[sources/01KJVJDB5G-reinforcement-fine-tuning12-days-of-openai-day-2|Reinforcement Fine-Tuning—12 Days of OpenAI: Day 2]]: The correct answer label in RFT training data is not shown to the model during training, but is used
- **2024-12-05** — [[sources/01KJV5E1EB-arc-prize-2024-technical-report|ARC Prize 2024: Technical Report]]: The ARC-AGI benchmark remains unbeaten as of December 5, 2024, five years after its creation.
- **2024-11-25** — [[sources/01KJV6JNEC-o1-replication-journey-part-2-surpassing-o1-preview-through-simple-distillation-|O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?]]: The distilled 72B model achieves 87.2% on MATH500, surpassing O1-preview's 85.5%, under comparable i
- **2024-11-22** — [[sources/01KJV6PJWC-tulu-3-pushing-frontiers-in-open-language-model-post-training|Tulu 3: Pushing Frontiers in Open Language Model Post-Training]]: No model in the top 50 on LMSYS ChatBot Arena (as of November 2024) has released its post-training d
- **2024-11-21** — [[sources/01KJVKPGFR-everything-you-wanted-to-know-about-llm-post-training-with-nathan-lambert-of-all|Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI]]: Tulu 3 uses a three-stage post-training pipeline: Supervised Fine-Tuning (SFT), Direct Preference Op
- **2024-11-15** — [[sources/01KJV6G030-llava-cot-let-vision-language-models-reason-step-by-step|LLaVA-CoT: Let Vision Language Models Reason Step-by-Step]]: LLaVA-CoT decomposes answer generation into four structured reasoning stages: summary, caption, reas
- **2024-11-11** — [[sources/01KKT4PNZT-the-surprising-effectiveness-of-test-time-training-for-few-shot-learning|The Surprising Effectiveness of Test-Time Training for Few-Shot Learning]]: TTT with an 8B-parameter LM achieves 61.9% accuracy on ARC when ensembled with program-synthesis met
- **2024-11-09** — [[sources/01KJVHWJNM-why-o1-is-a-big-deal|Why o1 is a BIG deal]]: Older LLMs do not use test-time compute; they generate answers instantaneously without spending ener
- **2024-11-04** — [[sources/01KJV6C0D1-combining-induction-and-transduction-for-abstract-reasoning|Combining Induction and Transduction for Abstract Reasoning]]: The data generation pipeline starts with 100-160 manually written Python seed programs and expands t
- **2024-10-30** — [[sources/01KJVKZAT6-training-zamba-a-hybrid-model-master-class-with-zyphras-quentin-anthony|Training Zamba: A Hybrid Model Master Class with Zyphra's Quentin Anthony]]: Mamba 2's SSD algorithm adds structure to the A matrix (which controls state transitions), enabling 
- **2024-10-15** — [[sources/01KJV7DD3S-latent-action-pretraining-from-videos|Latent Action Pretraining from Videos]]: LAPA uses a VQ-VAE-based objective to learn discrete latent actions between image frames in a fully 
- **2024-10-14** — [[sources/01KJV7N48D-thinking-llms-general-instruction-following-with-thought-generation|Thinking LLMs: General Instruction Following with Thought Generation]]: Thought Preference Optimization (TPO) achieves a 52.5% win rate on AlpacaEval (length-controlled) an
- **2024-10-10** — [[sources/01KJV4TENF-genarm-reward-guided-generation-with-autoregressive-reward-model-for-test-time-a|GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time Alignment]]: The Autoregressive Reward Model parametrizes the reward of a complete response as a log probability,
- **2024-10-07** — [[sources/01KJV7XNNN-differential-transformer|Differential Transformer]]: DIFF Transformer is substantially more robust to in-context learning order permutation than Transfor
- **2024-10-02** — [[sources/01KJV8790R-generative-reward-models|Generative Reward Models]]: GenRM replaces the Bradley-Terry reward modelling approach with a strictly more general preference m
- **2024-09-19** — [[sources/01KJV83GN1-training-language-models-to-self-correct-via-reinforcement-learning|Training Language Models to Self-Correct via Reinforcement Learning]]: SCoRe achieves a 15.6% absolute improvement in self-correction performance on MATH relative to the b
- **2024-09-10** — [[sources/01KJV8BD2M-kag-boosting-llms-in-professional-domains-via-knowledge-augmented-generation|KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation]]: KAG achieves a relative improvement of 19.6% on HotpotQA and 33.5% on 2wiki compared to state-of-the
- **2024-08-21** — [[sources/01KJV8WEM4-llm-pruning-and-distillation-in-practice-the-minitron-approach|LLM Pruning and Distillation in Practice: The Minitron Approach]]: Llama 3.1 8B was pretrained on 15 trillion tokens on a proprietary dataset.
- **2024-08-06** — [[sources/01KJSY403H-on-the-arc-agi-1-million-reasoning-challenge|On the “ARC-AGI” $1 Million Reasoning Challenge]]: Greenblatt's prompts are approximately 30,000 tokens long, comparable in length to a 50-page master'
- **2024-07-29** — [[sources/01KJVKZER8-llm-attention-that-expands-at-inference-test-time-training-explained|LLM Attention That Expands At Inference? Test Time Training Explained]]: TTT's compression is updated (trained) at every step, allowing the model to dynamically adapt to the
- **2024-07-12** — [[sources/01KJVM69GC-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states|Learning to (Learn at Test Time): RNNs with Expressive Hidden States]]: Standard softmax attention is quadratic in sequence length due to the QK^T matrix computation.
- **2024-06-13** — [[sources/01KJV8JK29-openvla-an-open-source-vision-language-action-model|OpenVLA: An Open-Source Vision-Language-Action Model]]: OpenVLA uses next-token prediction with cross-entropy loss evaluated only on predicted action tokens
- **2024-04-22** — [[sources/01KJVN9ZJX-robotics-research-update-with-keerthana-gopalakrishnan-and-ted-xiao-of-google-de|Robotics Research Update, with Keerthana Gopalakrishnan and Ted Xiao of Google DeepMind]]: PIVOT enables zero-shot robot guidance using vision-language models without any special fine-tuning 
- **2024-04-11** — [[sources/01KJVN834B-robotics-in-the-age-of-generative-ai-with-vincent-vanhoucke-google-deepmind-nvid|Robotics in the Age of Generative AI with Vincent Vanhoucke, Google DeepMind | NVIDIA GTC 2024]]: RT1 is an end-to-end transformer model that tokenizes language instructions and images and outputs e
- **2024-04-01** — [[sources/01KJVAT3JD-stream-of-search-sos-learning-to-search-in-language|Stream of Search (SoS): Learning to Search in Language]]: The SoS model achieves 51.27% accuracy on held-out inputs compared to 25.73% for the optimal path mo
- **2024-02-01** — [[sources/01KJV9HBN6-executable-code-actions-elicit-better-llm-agents|Executable Code Actions Elicit Better LLM Agents]]: There is a large performance gap between open-source and closed-source LLMs on CodeAct tasks: the be
- **2024-01-21** — [[sources/01KJVMD0J9-alphageometry-solving-olympiad-geometry-without-human-demonstrations-paper-expla|AlphaGeometry: Solving olympiad geometry without human demonstrations (Paper Explained)]]: AlphaGeometry's core inference loop alternates between a symbolic deduction engine attempting to clo
- **2023-09-01** — [[sources/01KJV8MTT2-rlaif-vs-rlhf-scaling-reinforcement-learning-from-human-feedback-with-ai-feedbac|RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback]]: RLAIF achieves comparable performance to RLHF across summarization, helpful dialogue generation, and
- **2023-05-25** — [[sources/01KJVC2MPT-voyager-an-open-ended-embodied-agent-with-large-language-models|Voyager: An Open-Ended Embodied Agent with Large Language Models]]: VOYAGER can consistently solve all four zero-shot generalization tasks (Diamond Pickaxe, Golden Swor
