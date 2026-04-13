---
type: theme
title: Reward Modeling & Verification
theme_id: reward_modeling
level: 2
parent_theme: reinforcement_learning
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 64
sources_since_update: 0
update_count: 1
velocity: 0.2
staleness: 0.0
status: active
tags: []
---
# Reward Modeling & Verification

> Reward modeling is in active transition — moving from a regime of brittle, hand-crafted reward functions toward general-purpose, data-free alternatives, but still blocked at the ceiling imposed by human evaluative capacity. Two structural breakthroughs (RULER's relative trajectory ranking and universal verifier architectures) have shifted what was an infrastructure problem into a configuration problem, but both sit at demo maturity, and the deepest bottleneck — human-derived reward ceilings blocking superhuman strategies — remains entirely unaddressed by any current approach.

**Parent:** [[themes/reinforcement_learning|reinforcement_learning]]

## Current State

For years, the central bottleneck in reward modeling was practical: constructing reliable reward signals for new agent task domains required labeled data, domain expertise, and careful engineering — prerequisites that made RL fine-tuning inaccessible to most teams. That bottleneck is now under direct attack.

RULER's relative within-group trajectory ranking sidesteps the hard problem of absolute LLM-as-judge calibration by exploiting GRPO's score normalization property — asking only for relative rankings within a trajectory batch rather than globally calibrated absolute scores. The result is a reward signal that outperforms hand-crafted alternatives on most tested tasks without any labeled data or human feedback. What was an infrastructure problem is becoming a configuration problem, and the 1–2 year horizon on broad RL adoption now looks achievable — provided the rubric brittleness problem resolves, which remains genuinely unclear. The finding that expert-specified rubrics frequently *degrade* RULER's performance relative to its generic default is a significant warning sign: reward specification is not yet a transparent engineering task.

Parallel progress on the verification side addresses a different bottleneck — the absence of ground-truth evaluators for subjective domains. The universal verifier architecture (one model grading another's outputs step-by-step against sources) opens RL training to creative work, advanced mathematics, and other tasks previously considered unscorable. Both breakthroughs are honest about their maturity: these are proof-of-concept results, not deployed infrastructure.

The deeper bottleneck — human-derived reward ceilings blocking superhuman strategies — remains entirely stuck. No current approach has a credible path around it. As long as reward signals derive from what humans can evaluate, agents are bounded by human judgment. The most structurally interesting development is the convergence between evaluation frameworks and training reward generators: if evaluation methodology and reward design are increasingly the same problem, benchmark construction becomes a direct lever on what agents can learn.

## Capabilities

- **Universal step-by-step verification** — A universal verifier model can grade another model's outputs step-by-step, cross-checking facts and logic against source material, enabling automatic scoring of domains previously requiring human evaluation. *(maturity: demo)*
- **General-purpose LLM-as-judge reward (RULER)** — Trains RL agents using relative trajectory ranking with no labeled data and no hand-crafted reward functions, outperforming task-specific alternatives on most tested domains. *(maturity: demo)*
- **Relative within-group trajectory ranking** — Sidesteps LLM-as-judge score calibration problems entirely, enabling reliable GRPO reward signals from imperfect judges. *(maturity: demo)*

## Limitations

- **Human evaluation ceiling** — Rewards derived from human pre-judgment impose an impenetrable ceiling: agents cannot discover strategies that are better than what humans can recognize as better. *(severity: blocking, trajectory: stable, type: explicit)*
- **Fuzzy-domain reward construction** — In domains where ground truth is fuzzy or subjective, frontier labs struggle to construct effective RL training signals, blocking capable agents in high-value areas like creative work, legal analysis, and strategic decision-making. *(severity: significant, trajectory: improving, type: explicit)*
- **RULER untested at inference time** — RULER has only been validated as a training-time reward signal; its proposed use as a test-time compute mechanism for improving agent performance at inference time remains unvalidated. *(severity: significant, trajectory: improving, type: explicit)*
- **Rubric brittleness** — Adding task-specific rubric customization to RULER frequently degrades performance relative to the default generic rubric, suggesting reward specification is not yet a principled engineering task. *(severity: significant, trajectory: unclear, type: implicit_performance_cliff)*
- **Judge quality dependency** — RULER's reward quality is entirely dependent on the capability of the configurable LLM-as-judge; a weak or misaligned judge produces unreliable reward signals, limiting applicability to settings where capable judges are available. *(severity: significant, trajectory: improving, type: implicit_controlled_conditions)*

## Bottlenecks

- **Subjective-domain evaluators** — Absence of standardized ground-truth evaluators for subjective and ambiguous domains prevents effective RL training outside narrow verifiable tasks, blocking highly capable agents in sales effectiveness, legal analysis, creative work, and strategic decision-making. *(status: active, horizon: 1–2 years)*
- **Labeled-data dependency for reward construction** — Constructing reliable reward signals for agentic RL without labeled data or hand-crafted functions blocks practical adoption of RL fine-tuning for diverse agentic task types by teams without ML infrastructure expertise. *(status: active, horizon: 1–2 years)*
- **Human-derived reward ceiling** — Human-derived reward signals impose an impenetrable ceiling on agent performance, blocking discovery of superhuman strategies and autonomous generation of novel knowledge in open-ended domains. *(status: active, horizon: long; no credible path currently exists)*

## Breakthroughs

- **RULER: relative within-group LLM trajectory ranking** — Enables reliable, general-purpose RL reward signals without labeled data or hand-crafted functions by exploiting GRPO's normalization property. Prior belief was that LLM-as-judge scores were too poorly calibrated in isolation to serve as RL rewards without task-specific rubrics or human data, making hand-crafted reward functions a practical necessity. *(significance: notable)*
- **Universal verifier architecture** — Using one AI model to grade another's outputs step-by-step against sources enables automatic scoring of advanced mathematics, creative writing, and other previously unscorable tasks, opening RL training to subjective domains. Prior belief was that such tasks required human evaluation and could not be automatically scored with sufficient reliability to drive RL training. *(significance: notable)*

## Anticipations

- Whether RULER's trajectory ranking transfers to test-time compute: the coupling to inference-time search is explicitly proposed but entirely unvalidated — a key open question for the field.
- Whether the rubric brittleness finding leads to principled methods for reward specification, or reveals a more fundamental limit on how much expert knowledge can be injected into LLM-as-judge systems.

## Cross-Theme Implications

- **→ [[themes/reinforcement_learning|reinforcement_learning]]** — GRPO's within-group score normalization removes the need for globally calibrated reward signals, making relative LLM-as-judge ranking viable as a reward — a structural coupling that makes general-purpose reward functions tractable.
- **→ [[themes/reinforcement_learning|reinforcement_learning]]** — Relative trajectory ranking, a technique from evaluation methodology, proves more effective than absolute scoring for reward signals; this convergence between evaluation and reward design suggests evaluation frameworks can increasingly double as training reward generators.
- **→ [[themes/test_time_compute_scaling|test_time_compute_scaling]]** — RULER's LLM-as-judge trajectory ranking, originally designed for training rewards, is explicitly proposed as a test-time compute mechanism — blurring the boundary between training-time reward signal and inference-time search.
- **→ [[themes/agent_self_evolution|agent_self_evolution]]** — RULER's elimination of labeled data and hand-crafted reward requirements directly enables continuous online RL for deployed agents; agents can self-improve from their own trajectories as they operate, making agent self-evolution practically accessible without curated datasets.
- **→ [[themes/continual_learning|continual_learning]]** — A reward function requiring no labeled data and scoring trajectories from live agent runs creates a practical path to continual learning where production traffic itself becomes the training signal, without manual annotation loops.
- **→ [[themes/software_engineering_agents|software_engineering_agents]]** — Removing labeled golden data requirements for RL reward functions directly unblocks RL fine-tuning for software engineering agents, where ground-truth correctness oracles are expensive or incomplete — enabling RL improvement on tasks beyond unit-test-verifiable code.
- **→ [[themes/alignment_methods|alignment_methods]]** — General-purpose LLM-as-judge reward functions that outperform hand-crafted rewards reduce reliance on human feedback in alignment pipelines, raising questions about whether RLHF-style human annotation remains necessary when automated relative ranking achieves superior results.
- **→ [[themes/benchmark_design|benchmark_design]]** — RULER's finding that a generic default rubric often outperforms task-specific expert rubrics challenges the assumption that evaluation quality requires domain-specific criteria, with implications for how benchmarks are designed and whether general rubrics can substitute for hand-crafted metrics.

## Contradictions

- RULER's rubric brittleness finding is in tension with the general expectation that more domain-specific information improves task performance: here, expert knowledge injected via rubrics frequently makes the reward signal *worse*, not better. The mechanism is not understood.
- The convergence between evaluation methodology and reward design is both a capability (reuse evaluation frameworks as reward generators) and a risk (benchmark construction choices now directly constrain what agents can learn, concentrating influence in benchmark designers).

## Research Opportunities

- **Principled rubric design** — Understanding why generic rubrics outperform expert-specified ones in RULER is a prerequisite for making reward specification a reliable engineering task rather than a trial-and-error process.
- **RULER at test-time** — Validating whether relative trajectory ranking transfers from training-time reward signal to inference-time search would establish a unified mechanism across the training/inference boundary.
- **Judge quality thresholds** — Characterizing the minimum capability level an LLM-as-judge must meet for RULER to remain reliable would make the approach's applicability envelope explicit.
- **Beyond human evaluation** — No credible approach currently exists for reward signals that transcend human evaluative capacity; this is the longest-horizon open problem and likely requires rethinking the nature of reward rather than improving existing methods.
- **Evaluation-reward convergence** — If evaluation frameworks and training reward generators are increasingly the same problem, there is an opportunity to build unified frameworks that serve both functions, with benchmark construction as a first-class lever on agent learning.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KKTEGC13-openpipe-rl-for-agents|OpenPipe | RL For Agents]]: Breakthrough: Relative within-group LLM trajectory ranking (RULER) enables reliable, general-p
- **2026-04-08** — [[sources/01KJSVF89A-how-hugging-face-is-using-e2b-to-replicate-deepseek-r1-e2b-blog|How Hugging Face Is Using E2B to Replicate DeepSeek-R1 — E2B Blog]]: Executing LLM-generated code locally poses serious security risks, including potential corruption of
- **2026-04-08** — Wiki page created. Theme has 64 sources.
- **2025-12-15** — [[sources/01KJVEVAZF-edwin-chen-why-frontier-labs-are-diverging-rl-environments-developing-model-tast|Edwin Chen: Why Frontier Labs Are Diverging, RL Environments & Developing Model Taste]]: LM Arena (Chatbot Arena) users spend approximately 1-2 seconds reviewing responses before voting, wi
- **2025-11-18** — [[sources/01KJT838Q9-π-06-a-vla-that-learns-from-experience|$π^{*}_{0.6}$: a VLA That Learns From Experience]]: π0.6 generates action chunks at 50 Hz consisting of joint angles and gripper commands
- **2025-11-10** — [[sources/01KJT9Y980-rlve-scaling-up-reinforcement-learning-for-language-models-with-adaptive-verifia|RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments]]: Expanding the collection of training environments consistently leads to better performance on held-o
- **2025-11-04** — [[sources/01KJTBFGVH-training-proactive-and-personalized-llm-agents|Training Proactive and Personalized LLM Agents]]: The proactivity reward adds +0.05 if all queries are low-effort, penalizes -0.1 per medium-effort qu
- **2025-10-08** — [[sources/01KJTD0659-hybrid-reinforcement-when-reward-is-sparse-its-better-to-be-dense|Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense]]: HERO (Hybrid Ensemble Reward Optimization) integrates sparse verifier signals with dense reward mode
- **2025-09-25** — [[sources/01KJTGJW0T-trustjudge-inconsistencies-of-llm-as-a-judge-and-how-to-alleviate-them|TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them]]: Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Pairwise Transitivity Inconsistency by 10.
- **2025-09-24** — [[sources/01KJTGWJGM-language-models-that-think-chat-better|Language Models that Think, Chat Better]]: RLMT uses 7.5K prompts from the WildChat-IF subset of the Tulu 3 SFT mixture, which prioritizes conv
- **2025-09-23** — [[sources/01KJTGTVN3-reinforcement-learning-on-pre-training-data|Reinforcement Learning on Pre-Training Data]]: RLPT uses two tasks: Autoregressive Segment Reasoning (ASR), which predicts the next sentence from p
- **2025-09-17** — [[sources/01KJTHM1GB-compute-as-teacher-turning-inference-compute-into-reference-free-supervision|Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision]]: The CaT framework has two components: reference estimation that aggregates rollouts into a pseudo-re
- **2025-09-08** — [[sources/01KJTK49M5-the-majority-is-not-always-right-rl-training-for-solution-aggregation|The Majority is not always right: RL training for solution aggregation]]: AggLM-1.7B generalizes to candidate set sizes k both smaller and larger than the k=8 used during tra
- **2025-08-18** — [[sources/01KJTMAX0G-reinforcement-learning-with-rubric-anchors|Reinforcement Learning with Rubric Anchors]]: Rubicon-preview (30B-A3B) outperforms DeepSeek-V3-671B by +2.4% on open-ended humanities benchmarks 
- **2025-07-24** — [[sources/01KJTN36CP-checklists-are-better-than-reward-models-for-aligning-language-models|Checklists Are Better Than Reward Models For Aligning Language Models]]: RLCF is the only alignment method that improves performance on every benchmark tested, including con
- **2025-07-23** — [[sources/01KJTN3N0M-rubrics-as-rewards-reinforcement-learning-beyond-verifiable-domains|Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains]]: RaR achieves relative improvements of up to 7% on GPQA-Diamond over LLM-as-judge baselines using Lik
- **2025-07-22** — [[sources/01KJTN6GH7-beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty|Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty]]: RLCR matches the task accuracy of RLVR while substantially improving calibration, reducing expected 
- **2025-07-21** — [[sources/01KJTN04YC-winning-gold-at-imo-2025-with-a-model-agnostic-verification-and-refinement-pipel|Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline]]: A model-agnostic verification-and-refinement pipeline equipped with any of Gemini 2.5 Pro, Grok-4, o
- **2025-07-03** — [[sources/01KJTNPY47-optimas-optimizing-compound-ai-systems-with-globally-aligned-local-rewards|Optimas: Optimizing Compound AI Systems with Globally Aligned Local Rewards]]: OPTIMAS maintains one Local Reward Function (LRF) per component, where each LRF satisfies a local-gl
- **2025-06-23** — [[sources/01KJTPV81Q-rlpr-extrapolating-rlvr-to-general-domains-without-verifiers|RLPR: Extrapolating RLVR to General Domains without Verifiers]]: RLPR surpasses General-Reasoner (which uses a trained 1.5B-parameter verifier model) by 1.6 average 
- **2025-06-17** — [[sources/01KJTQ0XQR-revisiting-reinforcement-learning-for-llm-reasoning-from-a-cross-domain-perspect|Revisiting Reinforcement Learning for LLM Reasoning from A Cross-Domain Perspective]]: GURU uses binary rewards (0 or 1) across all domains with three verification methods: rule-based mat
- **2025-06-16** — [[sources/01KJTQ0YV3-direct-reasoning-optimization-constrained-rl-with-token-level-dense-reward-and-r|Direct Reasoning Optimization: Constrained RL with Token-Level Dense Reward and Rubric-Gated Constraints for Open-ended Tasks]]: R3 identifies reasoning-reflective tokens as those whose likelihoods exhibit high variability across
- **2025-06-09** — [[sources/01KJSSZ2RA-what-comes-next-with-reinforcement-learning|What comes next with reinforcement learning]]: Current RLVR training generates 10K-100K tokens per answer for math or code problems during training
- **2025-05-30** — [[sources/01KJTR8Z78-writing-zero-bridge-the-gap-between-non-verifiable-tasks-and-verifiable-rewards|Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards]]: Writing-R1, based on an in-house SFT thinking model fine-tuned with BRPO, achieves 8.68 on WritingBe
- **2025-05-27** — [[sources/01KJTS8HZG-reinforcing-general-reasoning-without-verifiers|Reinforcing General Reasoning without Verifiers]]: In RLVR, a rule-based program assigns a reward of 1 if the final answer is correct and 0 otherwise.
- **2025-05-26** — [[sources/01KJTSAGB6-learning-to-reason-without-external-rewards|Learning to Reason without External Rewards]]: INTUITOR replaces external rewards in GRPO with self-certainty scores, enabling fully unsupervised r
- **2025-05-21** — [[sources/01KJTTA22M-gui-g1-understanding-r1-zero-like-training-for-visual-grounding-in-gui-agents|GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents]]: The DeepSeek-R1-Zero paradigm applies RL directly to base LLMs without relying on supervised fine-tu
- **2025-05-20** — [[sources/01KJTQH6AA-general-reasoner-advancing-llm-reasoning-across-all-domains|General-Reasoner: Advancing LLM Reasoning Across All Domains]]: The General-Verifier (1.5B parameter model-based verifier) achieves 78.7% agreement with Gemini-2.0-
- **2025-05-05** — [[sources/01KJTV56AP-rm-r1-reward-modeling-as-reasoning|RM-R1: Reward Modeling as Reasoning]]: RM-R1-DeepSeek-Distilled-Qwen-32B achieves the highest average score of 81.5 among all evaluated mod
- **2025-04-29** — [[sources/01KJTSHBZT-reinforcement-learning-for-reasoning-in-large-language-models-with-one-training-|Reinforcement Learning for Reasoning in Large Language Models with One Training Example]]: Post-saturation generalization occurs in 1-shot RLVR: training accuracy saturates near 100% rapidly 
- **2025-04-23** — [[sources/01KJTY5P1V-process-reward-models-that-think|Process Reward Models That Think]]: THINKPRM outperforms discriminative PRMs trained on full PRM800K by 8% on GPQA-Diamond and 4.5% on L
- **2025-04-19** — [[sources/01KJSTSTMC-openais-o3-over-optimization-is-back-and-weirder-than-ever|OpenAI's o3: Over-optimization is back and weirder than ever]]: Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the prima
- **2025-04-03** — [[sources/01KJV181HF-inference-time-scaling-for-generalist-reward-modeling|Inference-Time Scaling for Generalist Reward Modeling]]: SPCT consists of two phases: rejective fine-tuning as a cold start and rule-based online RL that rei
- **2025-03-31** — [[sources/01KJV1DNKJ-crossing-the-reward-bridge-expanding-rl-with-verifiable-rewards-across-diverse-d|Crossing the Reward Bridge: Expanding RL with Verifiable Rewards Across Diverse Domains]]: Strong open-source models including Qwen2.5-72B-Instruct and DeepSeek-R1-Distill-Qwen-32B perform po
- **2025-03-11** — [[sources/01KJV31KSH-gtr-guided-thought-reinforcement-prevents-thought-collapse-in-rl-based-vlm-agent|GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM Agent Training]]: GTR achieves a 17.5% success rate on Points24, compared to GPT-4o+Tool at 13.5%, SFT-only at 11.0%, 
- **2025-03-10** — [[sources/01KJV3AME5-optimizing-test-time-compute-via-meta-reinforcement-fine-tuning|Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning]]: The problem of optimizing test-time compute can be formalized as a meta-reinforcement learning (RL) 
- **2025-03-03** — [[sources/01KJV3M3CC-visual-rft-visual-reinforcement-fine-tuning|Visual-RFT: Visual Reinforcement Fine-Tuning]]: Visual-RFT improves accuracy by 24.3% over the baseline in one-shot fine-grained image classificatio
- **2025-02-10** — [[sources/01KJV47G2K-can-1b-llm-surpass-405b-llm-rethinking-compute-optimal-test-time-scaling|Can 1B LLM Surpass 405B LLM? Rethinking Compute-Optimal Test-Time Scaling]]: TTS approaches can be divided into Internal TTS (training LLMs with long CoT) and External TTS (samp
- **2025-02-04** — [[sources/01KJV4HRBK-qlass-boosting-language-agent-inference-via-q-guided-stepwise-search|QLASS: Boosting Language Agent Inference via Q-Guided Stepwise Search]]: QLASS is evaluated on WebShop, ALFWorld, and SciWorld — three environments that only provide a singl
- **2025-02-03** — [[sources/01KJV4KX85-process-reinforcement-through-implicit-rewards|Process Reinforcement through Implicit Rewards]]: PRIME achieves a 15.1% average improvement across key reasoning benchmarks over the SFT model starti
- **2025-02-03** — [[sources/01KJV3X90H-sample-scrutinize-and-scale-effective-inference-time-search-by-scaling-verificat|Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification]]: Verification@200 with Gemini v1.5 Pro achieves 8/15 on AIME 2024, 467/500 on MATH, 135/200 on LiveBe
- **2025-01-31** — [[sources/01KJV4M1H3-s1-simple-test-time-scaling|s1: Simple test-time scaling]]: Supervised finetuning of Qwen2.5-32B-Instruct on s1K required only 26 minutes of training on 16 H100
- **2025-01-22** — [[sources/01KJV50FH1-deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learnin|DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning]]: DeepSeek-R1-Zero suffers from poor readability and language mixing, occasionally combining English a
- **2025-01-22** — [[sources/01KJV4YYAN-test-time-preference-optimization-on-the-fly-alignment-via-iterative-textual-fee|Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback]]: TPO is an on-policy learning paradigm where the policy model continuously interacts with the reward 
- **2025-01-08** — [[sources/01KJV5D2Z7-rstar-math-small-llms-can-master-math-reasoning-with-self-evolved-deep-thinking|rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking]]: Terminal nodes in MCTS are scored as +1 for correct answers and -1 for incorrect answers, with Q-val
- **2024-12-18** — [[sources/01KJV5Z471-scaling-of-search-and-learning-a-roadmap-to-reproduce-o1-from-reinforcement-lear|Scaling of Search and Learning: A Roadmap to Reproduce o1 from Reinforcement Learning Perspective]]: o1's performance consistently improves with increasing computation of both reinforcement learning tr
- **2024-12-12** — [[sources/01KJVCZDP7-gemini-20-and-the-evolution-of-agentic-ai-oriol-vinyals|Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals]]: Model weights are frozen after training; all users receive the same fixed checkpoint and no further 
- **2024-12-06** — [[sources/01KJVJDB5G-reinforcement-fine-tuning12-days-of-openai-day-2|Reinforcement Fine-Tuning—12 Days of OpenAI: Day 2]]: RFT graders score model outputs on a continuous scale from 0 to 1 and can assign partial credit.
- **2024-12-04** — [[sources/01KJSXKC7D-openais-o1-using-search-was-a-psyop|OpenAI's o1 using "search" was a PSYOP]]: 80% of Llama 3.1 preference data consists of general chat, illustrating the weak signal in standard 
- **2024-12-03** — [[sources/01KJVHDMY1-inference-time-compute|Inference Time Compute]]: Chain of Thought prompting improves language model reasoning by having the model generate step-by-st
- **2024-10-10** — [[sources/01KJV4TENF-genarm-reward-guided-generation-with-autoregressive-reward-model-for-test-time-a|GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time Alignment]]: The Autoregressive Reward Model parametrizes the reward of a complete response as a log probability,
- **2024-10-04** — [[sources/01KJV75D18-system-2-reasoning-capabilities-are-nigh|System 2 Reasoning Capabilities Are Nigh]]: The majority of gains seen when using chain-of-thought prompting can be matched by prompting with a 
- **2024-10-02** — [[sources/01KJV84KVS-vineppo-refining-credit-assignment-in-rl-training-of-llms|VinePPO: Refining Credit Assignment in RL Training of LLMs]]: Auxiliary rollouts in VinePPO are used exclusively for value estimation and do not contribute direct
- **2024-10-02** — [[sources/01KJV8790R-generative-reward-models|Generative Reward Models]]: GenRM replaces the Bradley-Terry reward modelling approach with a strictly more general preference m
- **2024-09-28** — [[sources/01KJVHZDJP-openai-o1-the-biggest-black-box-of-all-lets-break-it-open|OpenAI o1 - the biggest black box of all. Let’s break it open.]]: o1's post-training includes the same three steps as GPT-4 plus an additional reinforcement learning 
- **2024-09-17** — [[sources/01KJVMZ5JN-jim-fan-on-nvidias-embodied-ai-lab-and-jensen-huangs-prediction-that-all-robots-|Jim Fan on Nvidia’s Embodied AI Lab and Jensen Huang’s Prediction that All Robots will be Autonomous]]: The Eureka system uses an LLM to automatically generate reward functions via code in the simulator A
- **2024-08-27** — [[sources/01KJSY2CEB-scaling-test-time-compute-a-new-paradigm-in-llm-performance|Scaling Test-Time Compute: A New Paradigm in LLM Performance]]: The study evaluates two key strategies for enhancing LLM performance at test-time: dense verifier re
- **2024-08-27** — [[sources/01KJV7NM6A-generative-verifiers-reward-modeling-as-next-token-prediction|Generative Verifiers: Reward Modeling as Next-Token Prediction]]: GenRM-CoT achieves 93.4% on GSM8K (Best-of-16) compared to 73% for LLM-as-a-Judge, surpassing GPT-4 
- **2024-08-21** — [[sources/01KJV8YY98-critique-out-loud-reward-models|Critique-out-Loud Reward Models]]: CLoud reward models are trained with a joint loss combining a reward modeling loss and a critique SF
- **2024-08-06** — [[sources/01KJV8ZDJ2-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model|Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters]]: The effectiveness of different approaches to scaling test-time compute critically varies depending o
- **2024-06-20** — [[sources/01KJV943BV-q-improving-multi-step-reasoning-for-llms-with-deliberative-planning|Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning]]: On the MATH dataset, DeepSeek-Math-7b enhanced with Q* achieves 55.4% accuracy, surpassing Gemini Ul
- **2024-06-04** — [[sources/01KJVA6TAA-dreureka-language-model-guided-sim-to-real-transfer|DrEureka: Language Model Guided Sim-To-Real Transfer]]: DrEureka uses GPT-4 as the backbone LLM and samples 16 domain randomization configurations, training
- **2023-12-14** — [[sources/01KJVB9Y21-math-shepherd-verify-and-reinforce-llms-step-by-step-without-human-annotations|Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations]]: MATH-SHEPHERD generalizes out-of-distribution: on the Hungarian national exam, LLemma-34B-PRM outper
- **2023-10-19** — [[sources/01KJVAT1TP-eureka-human-level-reward-design-via-coding-large-language-models|Eureka: Human-Level Reward Design via Coding Large Language Models]]: EUREKA's in-context evolutionary search iteratively refines the best reward from the previous iterat
- **2023-09-01** — [[sources/01KJV8MTT2-rlaif-vs-rlhf-scaling-reinforcement-learning-from-human-feedback-with-ai-feedbac|RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback]]: For harmless dialogue generation, RLAIF outperforms RLHF, with harmless rates of 88%, 76%, and 64% f
