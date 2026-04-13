---
type: theme
title: Policy Optimization Algorithms
theme_id: policy_optimization
level: 2
parent_theme: reinforcement_learning
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 78
sources_since_update: 0
update_count: 1
velocity: 0.026
staleness: 0.0
status: active
tags: []
---
- **Empty sections** (Limitations, Bottlenecks, Anticipations, Breakthroughs, Contradictions) are present with explicit notes that they represent coverage gaps rather than true absences — this matches the state summary's analysis and avoids misleading omissions.
- **Research Opportunities** are grounded in the state summary's "watch for" signals, translated into actionable research framings.
- **Cross-Theme Implications** uses the exact confidence value (0.85) from the data and links to `[[themes/reward_modeling|reward_modeling]]` via Obsidian wikilink.
- Em dashes are avoided per your writing style preference; colons, semicolons, and parentheses are used instead.

## Current State

## Capabilities

## Limitations

## Bottlenecks

## Breakthroughs

## Anticipations

## Cross-Theme Implications

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KKTEGC13-openpipe-rl-for-agents|OpenPipe | RL For Agents]]: On the Voice Ordering task, Qwen 2.5 with RULER RL achieves 96% versus OpenAI o3's 95% and baseline 
- **2026-01-28** — [[sources/01KJT1VZTM-reinforcement-learning-via-self-distillation|Reinforcement Learning via Self-Distillation]]: SDPO treats the current model conditioned on feedback as a self-teacher and distills its feedback-in
- **2026-01-05** — [[sources/01KJT2BQDA-agentic-memory-learning-unified-long-term-and-short-term-memory-management-for-l|Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents]]: Adding LTM alone yields performance gains of +10.6%, +14.2%, and +7.4% on ALFWorld, SciWorld, and Ho
- **2025-12-18** — [[sources/01KJT4HR3T-justrl-scaling-a-15b-llm-with-a-simple-rl-recipe|JustRL: Scaling a 1.5B LLM with a Simple RL Recipe]]: JustRL's results are limited to mathematical reasoning at 1.5B scale; generalization to other domain
- **2025-12-08** — [[sources/01KJT4XPFE-on-the-interplay-of-pre-training-mid-training-and-rl-on-reasoning-language-model|On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models]]: Reasoning complexity is quantified by the number of arithmetic operations, defined as op(G) = |E| wh
- **2025-12-01** — [[sources/01KJT6H3QA-stabilizing-reinforcement-learning-with-llms-formulation-and-practices|Stabilizing Reinforcement Learning with LLMs: Formulation and Practices]]: Importance sampling correction for the training-inference discrepancy is an inherent component of th
- **2025-11-26** — [[sources/01KJT6ZBSZ-toolorchestra-elevating-intelligence-via-efficient-model-and-tool-orchestration|ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration]]: The agentic task in ToolOrchestra is formalized as a Markov Decision Process (MDP) incorporating use
- **2025-11-26** — [[sources/01KJT6V2CT-monet-reasoning-in-latent-visual-space-beyond-images-and-language|Monet: Reasoning in Latent Visual Space Beyond Images and Language]]: Monet introduces a three-stage distillation-based SFT pipeline that enables MLLMs to generate contin
- **2025-11-20** — [[sources/01KJT7VEK3-evolution-strategies-at-the-hyperscale|Evolution Strategies at the Hyperscale]]: Naive Evolution Strategies (ES) becomes prohibitively expensive at scale on GPUs due to low arithmet
- **2025-11-20** — [[sources/01KJT7RXXT-agent0-unleashing-self-evolving-agents-from-zero-data-via-tool-integrated-reason|Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning]]: Curriculum agent generates progressively harder tasks across iterations: executor pass rate decrease
- **2025-11-18** — [[sources/01KJT89YD6-agent-r1-training-powerful-llm-agents-with-end-to-end-reinforcement-learning|Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning]]: GRPO achieved the best overall RL performance (average EM 0.3877) on multi-hop QA, closely followed 
- **2025-11-18** — [[sources/01KJT838Q9-π-06-a-vla-that-learns-from-experience|$π^{*}_{0.6}$: a VLA That Learns From Experience]]: RECAP pre-trains on tens of thousands of hours of demonstrations from numerous tasks and a variety o
- **2025-11-13** — [[sources/01KJT9AAYD-agentevolver-towards-efficient-self-evolving-agent-system|AgentEvolver: Towards Efficient Self-Evolving Agent System]]: Current RL-driven agent development requires manually constructed task datasets and extensive random
- **2025-11-12** — [[sources/01KJT9K4DJ-wmpo-world-model-based-policy-optimization-for-vision-language-action-models|WMPO: World Model-based Policy Optimization for Vision-Language-Action Models]]: WMPO enables on-policy GRPO for VLA models without any interaction with the real environment by usin
- **2025-11-11** — [[sources/01KJT9Y5SJ-the-path-not-taken-rlvr-provably-learns-off-the-principals|The Path Not Taken: RLVR Provably Learns Off the Principals]]: RLVR update sparsity (fraction of unchanged parameters) ranges from 36% to 92% across models, while 
- **2025-11-10** — [[sources/01KJTA1YHZ-iterresearch-rethinking-long-horizon-agents-with-interaction-scaling|IterResearch: Rethinking Long-Horizon Agents with Interaction Scaling]]: IterResearch achieves an average improvement of 14.5 percentage points over existing open-source dee
- **2025-11-04** — [[sources/01KJTBFGVH-training-proactive-and-personalized-llm-agents|Training Proactive and Personalized LLM Agents]]: The proactivity reward adds +0.05 if all queries are low-effort, penalizes -0.1 per medium-effort qu
- **2025-11-04** — [[sources/01KJTBCNKD-memsearcher-training-llms-to-reason-search-and-manage-memory-via-end-to-end-rein|MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning]]: MemSearcher trained on Qwen2.5-3B-Instruct achieves +11% relative average improvement over strong ba
- **2025-10-22** — [[sources/01KJTCHAPG-loongrl-reinforcement-learning-for-advanced-reasoning-over-long-contexts|LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts]]: A two-way substring exact match reward verifier is used as a rule-based reward, where a trajectory r
- **2025-10-13** — [[sources/01KJTD9WCB-demystifying-reinforcement-learning-in-agentic-reasoning|Demystifying Reinforcement Learning in Agentic Reasoning]]: Real end-to-end tool-use trajectories for SFT initialization dramatically outperform synthetic stitc
- **2025-10-10** — [[sources/01KJTDB22B-mitigating-overthinking-through-reasoning-shaping|Mitigating Overthinking through Reasoning Shaping]]: GRSP assigns descending penalty weights from shorter to longer segment clusters, penalizing short se
- **2025-10-08** — [[sources/01KJTD0659-hybrid-reinforcement-when-reward-is-sparse-its-better-to-be-dense|Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense]]: HERO (Hybrid Ensemble Reward Optimization) integrates sparse verifier signals with dense reward mode
- **2025-10-08** — [[sources/01KJTDQZXF-the-markovian-thinker-architecture-agnostic-linear-scaling-of-reasoning|The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning]]: The standard RL reasoning environment makes the state unbounded, growing with longer thoughts, and f
- **2025-10-07** — [[sources/01KJTE6RW1-in-the-flow-agentic-system-optimization-for-effective-planning-and-tool-use|In-the-Flow Agentic System Optimization for Effective Planning and Tool Use]]: AGENTFLOW with a 7B-scale backbone outperforms top-performing baselines with average accuracy gains 
- **2025-10-06** — [[sources/01KJTEKYPY-multi-agent-tool-integrated-policy-optimization|Multi-Agent Tool-Integrated Policy Optimization]]: MATPO uses an LLM-as-judge reward function combining accuracy (0.9 weight) and format correctness (0
- **2025-09-29** — [[sources/01KJTFKNRP-evolution-strategies-at-scale-llm-fine-tuning-beyond-reinforcement-learning|Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning]]: Evolution Strategies (ES) can successfully fine-tune LLMs at the billion-parameter scale through dir
- **2025-09-29** — [[sources/01KJTG66GD-training-agents-inside-of-scalable-world-models|Training Agents Inside of Scalable World Models]]: Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, without envir
- **2025-09-29** — [[sources/01KJT3ZXPZ-from-fx-and-gx-to-fgx-llms-learn-new-skills-in-rl-by-composing-old-ones|From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones]]: RL on Level-2 compositional problems improves held-out Level-3 accuracy from near-zero (~5%) to appr
- **2025-09-24** — [[sources/01KJTGWJGM-language-models-that-think-chat-better|Language Models that Think, Chat Better]]: RLMT (RL with Model-rewarded Thinking) trains language models to generate long chain-of-thought reas
- **2025-09-18** — [[sources/01KJTF5CHP-flowrl-matching-reward-distributions-for-llm-reasoning|FlowRL: Matching Reward Distributions for LLM Reasoning]]: FlowRL transforms scalar rewards into a normalized target distribution using a learnable partition f
- **2025-09-10** — [[sources/01KJTHH7D3-a-survey-of-reinforcement-learning-for-large-reasoning-models|A Survey of Reinforcement Learning for Large Reasoning Models]]: AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world c
- **2025-09-10** — [[sources/01KJTK494K-agentgym-rl-training-llm-agents-for-long-horizon-decision-making-through-multi-t|AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning]]: ScalingInter-RL surpasses the base model by 30 points on the TextCraft benchmark, achieving state-of
- **2025-09-04** — [[sources/01KJTKM1EW-rls-razor-why-online-reinforcement-learning-forgets-less|RL's Razor: Why Online Reinforcement Learning Forgets Less]]: Off-policy RL algorithms were not studied, leaving their forgetting behavior relative to on-policy m
- **2025-09-03** — [[sources/01KJTKFTJ0-emergent-hierarchical-reasoning-in-llms-through-reinforcement-learning|Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning]]: HICRA amplifies the advantage for planning tokens in successful trajectories and dampens their penal
- **2025-08-28** — [[sources/01KJTM994W-rstar2-agent-agentic-reasoning-technical-report|rStar2-Agent: Agentic Reasoning Technical Report]]: rStar2-Agent training was completed in one week using only 64 AMD MI300X GPUs, completing frontier-l
- **2025-08-27** — [[sources/01KJTM4P7P-memory-r1-enhancing-large-language-model-agents-to-manage-and-utilize-memories-v|Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning]]: The Memory Manager's reward is outcome-driven: operations are judged by their effect on downstream Q
- **2025-08-18** — [[sources/01KJTMAX0G-reinforcement-learning-with-rubric-anchors|Reinforcement Learning with Rubric Anchors]]: Rubicon-preview (30B-A3B) outperforms DeepSeek-V3-671B by +2.4% on open-ended humanities benchmarks 
- **2025-07-24** — [[sources/01KJTN36CP-checklists-are-better-than-reward-models-for-aligning-language-models|Checklists Are Better Than Reward Models For Aligning Language Models]]: RLCF is the only alignment method that improves performance on every benchmark tested, including con
- **2025-07-20** — [[sources/01KJTNH60K-the-invisible-leash-why-rlvr-may-or-may-not-escape-its-origin|The Invisible Leash: Why RLVR May or May Not Escape Its Origin]]: RLVR achieves very high support retention rates (SRR ≈ 0.93–0.99) across all evaluated models and do
- **2025-07-03** — [[sources/01KJTNPY47-optimas-optimizing-compound-ai-systems-with-globally-aligned-local-rewards|Optimas: Optimizing Compound AI Systems with Globally Aligned Local Rewards]]: OPTIMAS models a compound AI system as a directed acyclic graph where components are nodes and data 
- **2025-06-25** — [[sources/01KJTPC0T7-diffucoder-understanding-and-improving-masked-diffusion-models-for-code-generati|DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation]]: coupled-GRPO improves DiffuCoder's performance on code generation benchmarks by +4.4% on EvalPlus us
- **2025-06-17** — [[sources/01KJTME7HT-reasoning-with-exploration-an-entropy-perspective|Reasoning with Exploration: An Entropy Perspective]]: The entropy-based advantage term is clipped to prevent it from dominating or reversing the sign of t
- **2025-06-16** — [[sources/01KJTQ0YV3-direct-reasoning-optimization-constrained-rl-with-token-level-dense-reward-and-r|Direct Reasoning Optimization: Constrained RL with Token-Level Dense Reward and Rubric-Gated Constraints for Open-ended Tasks]]: R3 identifies reasoning-reflective tokens as those whose likelihoods exhibit high variability across
- **2025-06-12** — [[sources/01KJTQ74E7-spurious-rewards-rethinking-training-signals-in-rlvr|Spurious Rewards: Rethinking Training Signals in RLVR]]: Code reasoning frequency in Qwen2.5-Math-7B increases from 65% to over 90% when trained with spuriou
- **2025-06-10** — [[sources/01KJTQ6SB0-e3-learning-to-explore-enables-extrapolation-of-test-time-compute-for-llms|e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs]]: Most existing reasoning models do not extrapolate well when test-time compute is scaled beyond the m
- **2025-06-09** — [[sources/01KJTQH85K-reinforcement-pre-training|Reinforcement Pre-Training]]: RPT significantly improves the accuracy of next-token prediction.
- **2025-05-30** — [[sources/01KJTR8Z78-writing-zero-bridge-the-gap-between-non-verifiable-tasks-and-verifiable-rewards|Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards]]: Writing-R1, based on an in-house SFT thinking model fine-tuned with BRPO, achieves 8.68 on WritingBe
- **2025-05-30** — [[sources/01KJTQXH92-reflect-retry-reward-self-improving-llms-via-reinforcement-learning|Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning]]: Training is performed only on a dataset of failures (queries the model already handles correctly are
- **2025-05-30** — [[sources/01KJTQXNA5-prorl-prolonged-reinforcement-learning-expands-reasoning-boundaries-in-large-lan|ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models]]: Nemotron-Research-Reasoning-Qwen-1.5B was trained on a diverse, verifiable dataset of 136K problems 
- **2025-05-28** — [[sources/01KJTRVD3A-the-entropy-mechanism-of-reinforcement-learning-for-reasoning-language-models|The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models]]: Without entropy intervention, the relationship between policy entropy H and downstream validation pe
- **2025-05-27** — [[sources/01KJSTGBK2-reinforcement-learning-with-random-rewards-actually-works-with-qwen-25|Reinforcement learning with random rewards actually works with Qwen 2.5]]: Random rewards (awarding 1 reward per rollout prompt with a fixed probability in GRPO) improve Qwen 
- **2025-05-27** — [[sources/01KJTS8HZG-reinforcing-general-reasoning-without-verifiers|Reinforcing General Reasoning without Verifiers]]: VeriFree bypasses answer verification and instead uses RL to directly maximize the probability of ge
- **2025-05-26** — [[sources/01KJTSAGB6-learning-to-reason-without-external-rewards|Learning to Reason without External Rewards]]: INTUITOR replaces external rewards in GRPO with self-certainty scores, enabling fully unsupervised r
- **2025-05-21** — [[sources/01KJTTA22M-gui-g1-understanding-r1-zero-like-training-for-visual-grounding-in-gui-agents|GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents]]: The DeepSeek-R1-Zero paradigm applies RL directly to base LLMs without relying on supervised fine-tu
- **2025-05-21** — [[sources/01KJTTRBRJ-mmada-multimodal-large-diffusion-language-models|MMaDA: Multimodal Large Diffusion Language Models]]: MMaDA-8B surpasses LLaMA-3-7B and Qwen2-7B in textual reasoning
- **2025-05-20** — [[sources/01KJTQH6AA-general-reasoner-advancing-llm-reasoning-across-all-domains|General-Reasoner: Advancing LLM Reasoning Across All Domains]]: The General-Verifier (1.5B parameter model-based verifier) achieves 78.7% agreement with Gemini-2.0-
- **2025-05-19** — [[sources/01KJTTZHX6-adaptthink-reasoning-models-can-learn-when-to-think|AdaptThink: Reasoning Models Can Learn When to Think]]: Training AdaptThink-1.5B requires approximately 32 hours on one 8×H800 node; the 7B model requires a
- **2025-05-19** — [[sources/01KJTV54QV-thinkless-llm-learns-when-to-think|Thinkless: LLM Learns When to Think]]: DeGRPO decomposes the hybrid reasoning objective into two components: a control token loss governing
- **2025-04-30** — [[sources/01KJTX2G5P-deepseek-prover-v2-advancing-formal-mathematical-reasoning-via-reinforcement-lea|DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition]]: DeepSeek-Prover-V2-671B achieves 82.4% accuracy with Pass@32 on MiniF2F-test, improving to 88.9% wit
- **2025-04-29** — [[sources/01KJTSHBZT-reinforcement-learning-for-reasoning-in-large-language-models-with-one-training-|Reinforcement Learning for Reasoning in Large Language Models with One Training Example]]: Post-saturation generalization occurs in 1-shot RLVR: training accuracy saturates near 100% rapidly 
- **2025-04-23** — [[sources/01KJTXS7VE-skywork-r1v2-multimodal-hybrid-reinforcement-learning-for-reasoning|Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning]]: Future versions of R1V2 will focus on enhancing general visual capabilities while preserving the str
- **2025-04-22** — [[sources/01KJTYK6PA-ttrl-test-time-reinforcement-learning|TTRL: Test-Time Reinforcement Learning]]: TTRL on Qwen2.5-Math-7B achieves an average gain of 76% across AIME 2024, AMC, MATH-500, and GPQA
- **2025-03-25** — [[sources/01KJV1PKTA-research-learning-to-reason-with-search-for-llms-via-reinforcement-learning|ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning]]: ReSearch is trained from scratch without any labeled data on reasoning chains.
- **2025-03-12** — [[sources/01KJTMKZPA-search-r1-training-llms-to-reason-and-leverage-search-engines-with-reinforcement|Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning]]: Search-R1 improves question-answering performance by 24% for Qwen2.5-7B and 20% for Qwen2.5-3B over 
- **2025-03-11** — [[sources/01KJV2JYHE-in-prospect-and-retrospect-reflective-memory-management-for-long-term-personaliz|In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents]]: Retrospective Reflection uses LLM attribution signals generated during response generation as unsupe
- **2025-03-10** — [[sources/01KJV3AME5-optimizing-test-time-compute-via-meta-reinforcement-fine-tuning|Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning]]: The progress dense reward bonus is quantified by the change in the likelihood of eventual success fo
- **2025-03-03** — [[sources/01KJV3M3CC-visual-rft-visual-reinforcement-fine-tuning|Visual-RFT: Visual Reinforcement Fine-Tuning]]: Visual-RFT exceeds the baseline by 21.9 mAP on COCO two-shot object detection and by 15.4 mAP on LVI
- **2025-02-03** — [[sources/01KJV4KX85-process-reinforcement-through-implicit-rewards|Process Reinforcement through Implicit Rewards]]: Eurus-2-7B-PRIME surpasses Qwen2.5-Math-7B-Instruct on seven reasoning benchmarks using only 10% of 
- **2025-01-22** — [[sources/01KJV50MCD-kimi-k15-scaling-reinforcement-learning-with-llms|Kimi k1.5: Scaling Reinforcement Learning with LLMs]]: From 1,000 online contest coding problems, approximately 614 did not require a special judge, and 32
- **2025-01-22** — [[sources/01KJV50FH1-deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learnin|DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning]]: DeepSeek-V3-Base has 671 billion total parameters with 37 billion activated per token and was pre-tr
- **2025-01-09** — [[sources/01KJV56ZJP-transformer-squared-self-adaptive-llms|Transformer-Squared: Self-adaptive LLMs]]: SVF learns a vector z that scales the singular values of weight matrices, producing a new weight mat
- **2024-12-18** — [[sources/01KJV5Z0M1-inference-aware-fine-tuning-for-best-of-n-sampling-in-large-language-models|Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models]]: BoN-RLBP significantly improves pass@16 on HumanEval from 61.6% to 67.1% for Gemma 2B.
- **2024-11-21** — [[sources/01KJVKPGFR-everything-you-wanted-to-know-about-llm-post-training-with-nathan-lambert-of-all|Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI]]: Tulu 3 uses a three-stage post-training pipeline: Supervised Fine-Tuning (SFT), Direct Preference Op
- **2024-10-14** — [[sources/01KJV7N48D-thinking-llms-general-instruction-following-with-thought-generation|Thinking LLMs: General Instruction Following with Thought Generation]]: TPO requires no additional human-annotated thought data; instead it bootstraps thought generation fr
- **2024-10-02** — [[sources/01KJV84KVS-vineppo-refining-credit-assignment-in-rl-training-of-llms|VinePPO: Refining Credit Assignment in RL Training of LLMs]]: VinePPO computes unbiased Monte Carlo-based value estimates for intermediate states by sampling auxi
- **2024-09-19** — [[sources/01KJV83GN1-training-language-models-to-self-correct-via-reinforcement-learning|Training Language Models to Self-Correct via Reinforcement Learning]]: SCoRe Stage II jointly optimizes both attempts using reward shaping that rewards self-correction pro
- **2023-12-14** — [[sources/01KJVB9Y21-math-shepherd-verify-and-reinforce-llms-step-by-step-without-human-annotations|Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations]]: A larger LLM completer generates higher quality process annotation datasets; the quality of training
- **2023-09-01** — [[sources/01KJV8MTT2-rlaif-vs-rlhf-scaling-reinforcement-learning-from-human-feedback-with-ai-feedbac|RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback]]: For harmless dialogue generation, RLAIF outperforms RLHF, with harmless rates of 88%, 76%, and 64% f
