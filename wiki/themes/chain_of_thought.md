---
type: theme
title: Chain-of-Thought Mechanics
theme_id: chain_of_thought
level: 2
parent_theme: reasoning_and_planning
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 96
sources_since_update: 0
update_count: 1
velocity: 0.1
staleness: 0.0
status: active
tags: []
---
# Chain-of-Thought Mechanics

> Chain-of-Thought Mechanics has crossed from research technique to broad production deployment, but is now confronting a second wave of structural problems — overthinking, fixation, interpretability fragility — that are harder to resolve than the original capability gaps. The field has a principled theoretical foundation (LLMs as universal computers via CoT) but lacks understanding of whether human language is even the right substrate, and is now discovering that the optimization pressure used to improve CoT may simultaneously corrupt its value as a monitoring signal.

**Parent:** [[themes/reasoning_and_planning|reasoning_and_planning]]

## Current State

The story of Chain-of-Thought Mechanics has two distinct acts, and the field is now deep into the second.

The first act was rapid legitimization. Through 2024 into mid-2025, the basic CoT paradigm — appending tokens into context to execute arbitrary algorithms before producing a final answer — moved from research novelty to broad production maturity. This was not incremental progress; it was a threshold crossing. The theoretical framing of LLMs as universal computers via CoT gave practitioners a principled explanation for *why* the mechanism works, not just empirical evidence that it does. On the heels of this came large reasoning models (LRMs), which extended CoT with self-correction: the ability to explore multiple reasoning paths, catch errors mid-trace, and revise before committing to an answer. By mid-2025 these had entered narrow production, representing genuine progress on long-task coherence — a limitation that had previously made CoT unreliable for complex, multi-step problems.

The second act is a reckoning with problems that were invisible while CoT was still being proven. LRMs overthink: they find correct answers early and then continue exploring, wasting inference compute with no gain. In failure cases, they fixate — latching onto an early wrong answer and failing to escape it despite exhausting their token budget. Self-correction, the mechanism designed to address coherence failures, proves insufficient to break out of these attractor states. Neither problem has a clear resolution horizon.

The deeper uncertainty is substrate. Human language is almost certainly not the optimal medium for machine reasoning — symbolic, continuous, or differentiable alternatives likely exist — but they remain undiscovered. This is not an engineering gap; it is a conceptual one the field is not visibly closing.

Most consequentially, capability maturity has outrun interpretability. Strong RL optimization applied to CoT appears to corrupt it from a transparent reasoning trace into an obfuscated artifact. CoT's value as a monitoring and interpretability signal — already empirically unverified at the trace level — becomes actively fragile under the same optimization pressures being used to improve it. The next inflection point will likely come from empirical work on CoT faithfulness and trace-level supervision quality, or from the field acknowledging a fundamental tradeoff between performance and transparency.

## Capabilities

- **Broad production:** LLMs can reason through chain-of-thought, functioning as universal computers by appending tokens into their own context. This is no longer a research capability — it underpins deployed systems.
- **Narrow production:** Reasoning models can explore and self-correct reasoning traces, finding correct solutions after initial incorrect paths. The self-correction mechanism represents genuine progress on coherence over long tasks.
- **Research frontier:** GPT-5 with an explicit reasoning trace can execute over 2,100 sequential steps with approximately 80% success rate on long-horizon tasks — a result that challenged prior assumptions about where the ceiling lay (see #Breakthroughs).

## Limitations

- **Coherence collapse without structure** (blocking, improving): Without structured step-by-step reasoning, frontier models fail after only a handful of steps in long-horizon tasks. The limitation is architectural, not a matter of raw capability, and structured CoT is the current mitigation.
- **LRM overthinking** (significant, stable): LRMs exhibit overthinking on simple problems — finding the correct solution early but wastefully continuing to explore, burning inference compute for no gain. No resolution mechanism is established.
- **LRM fixation in failure cases** (significant, unclear): In failed cases, LRMs fixate on an early incorrect solution and waste the remaining token budget without escaping — active self-correction proves insufficient to break these attractor states.
- **Trace-level validity unmeasured** (minor, unclear): Quality of reasoning traces is not measured — only final answer accuracy is evaluated. The validity of chain-of-thought as a reasoning process, rather than a pattern-matching artifact, remains an open empirical question.
- **Suboptimal computational substrate** (significant, improving): Human language is likely not the optimal computational substrate for AI reasoning; more efficient non-human mechanisms probably exist but have not been discovered. This is a conceptual gap, not an engineering one.
- **Residual coherence loss** (significant, improving): Despite vast implicit knowledge, frontier models still make basic reasoning errors and lose coherence on long, complex problems — CoT mitigates but does not eliminate this.

## Bottlenecks

The central bottleneck is the **interpretability-optimization tradeoff**: the same RL optimization pressure that improves CoT performance appears to degrade CoT's value as a transparent reasoning trace, introducing a potential monitorability tax. Resolving this requires either new optimization objectives that preserve trace fidelity, or empirical methods to verify faithfulness under optimization pressure.

A secondary bottleneck is **substrate discovery**: identifying computational representations beyond natural language that are more efficient for reasoning. This bottleneck has no clear near-term resolution path — it requires conceptual breakthroughs rather than incremental engineering.

The **overthinking and fixation** problems in LRMs represent a third bottleneck: efficient inference budgeting and escape mechanisms for attractor states in reasoning traces. These are more tractable in principle but lack established solutions.

## Breakthroughs

- **Long-horizon execution via structured traces:** Structured reasoning traces enable GPT-5 to execute 2,100+ sequential steps reliably (~80% success rate), demonstrating that long-horizon reliability is achievable without fundamentally better base models. This was significant because the ceiling was previously assumed to be a raw capability limitation — the result reframed it as a structural/scaffolding problem.

## Anticipations

- Empirical work on CoT faithfulness — whether traces accurately reflect internal reasoning — will determine whether CoT can serve as a durable interpretability tool or must be treated as a gameable proxy.
- Resolution of the overthinking and fixation problems in LRMs likely requires new inference-time control mechanisms or training objectives; progress here would unlock reliable long-horizon reasoning in deployed systems.
- Discovery of non-linguistic reasoning substrates would be a paradigm shift; absence of progress here may eventually force the field to acknowledge a hard ceiling on CoT-based approaches.

## Cross-Theme Implications

- **→ [[themes/interpretability|Interpretability]]:** CoT reasoning traces are effective as a behavioral monitoring signal in current models, but this utility is fragile — optimization pressure can render them uninformative or actively misleading, posing a fundamental challenge for using CoT as an interpretability tool.
- **→ [[themes/mechanistic_interpretability|Mechanistic Interpretability]]:** CoT faithfulness — whether the chain-of-thought fully and accurately reflects the model's internal reasoning — is now a live empirical question. CoT may be a noisy or gameable proxy for true internal states, with direct implications for interpretability research methodology.
- **→ [[themes/mechanistic_interpretability|Mechanistic Interpretability]]:** Systematic analysis of LRM reasoning traces — tracking solution positions within thoughts, fixation patterns, and token budget utilisation — establishes a behavioral interpretability methodology that complements mechanistic approaches. Reasoning traces are a new observable layer that interpretability research can exploit to study planning and search behavior.
- **→ [[themes/scaling_laws|Scaling Laws]]:** Injecting chain-of-thought-style reasoning traces into pretraining data meaningfully changes the effective scaling curve. Models trained on thought-augmented data achieve performance levels that require substantially more raw tokens without augmentation, suggesting the scaling law literature should account for data enrichment quality, not just quantity.
- **→ [[themes/chain_of_thought|Chain-of-Thought]] (self-referential):** Strong RL optimization pressure applied directly to CoT can corrupt it from a transparent reasoning trace into an obfuscated artifact, suggesting a 'monitorability tax' is required — deliberately limiting optimization strength on CoT to preserve interpretability.

## Contradictions

- **Self-correction vs. fixation:** LRMs were introduced partly as a solution to coherence failures via self-correction, yet LRM failure cases show that self-correction is insufficient to escape fixation on early incorrect answers. The mechanism meant to address a key CoT limitation does not generalize to its most problematic failure mode.
- **Optimization vs. transparency:** The same RL optimization pressure that improves CoT reasoning quality appears to degrade CoT's value as a transparent, interpretable trace. Improving the capability and preserving the monitoring signal may be in direct tension.
- **Broad deployment vs. unmeasured trace validity:** CoT is in broad production, yet the quality of the reasoning traces themselves — as opposed to final answers — is not systematically measured. The field has deployed a mechanism whose internal validity remains unverified at the process level.

## Research Opportunities

- **Trace-level evaluation:** Developing metrics and benchmarks for CoT faithfulness — measuring whether traces reflect internal computation rather than post-hoc rationalization — is a high-leverage open problem with direct implications for both interpretability and safety.
- **Inference budget control:** Mechanisms to detect early correct solutions and terminate reasoning traces efficiently would directly address the overthinking problem in LRMs, reducing inference cost without sacrificing accuracy.
- **Fixation escape:** Understanding why LRMs get stuck in attractor states and designing training objectives or inference-time interventions to enable escape is an open problem with no established solution.
- **Non-linguistic reasoning substrates:** Exploring symbolic, continuous, or differentiable representations as alternatives or complements to natural language for intermediate reasoning steps is a long-horizon but potentially high-impact research direction.
- **Monitorability-preserving optimization:** Designing RL training objectives that improve CoT reasoning performance while preserving trace interpretability — rather than treating these as independent goals — could resolve the central interpretability-optimization tension.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJS1WVEB-interleaved-thinking-unlocks-reliable-minimax-m2-agentic-capability|Interleaved Thinking Unlocks Reliable MiniMax-M2 Agentic Capability]]: When prior reasoning state is dropped, cumulative understanding breaks down, state drift increases, 
- **2026-04-08** — [[sources/01KJSW87NX-claudes-extended-thinking|Claude's extended thinking]]: The visible thought process was not subjected to Claude's standard character training, resulting in 
- **2026-04-08** — [[sources/01KJSVFS87-tracing-the-thoughts-of-a-large-language-model|Tracing the thoughts of a large language model]]: Language models are not directly programmed but learn strategies through training that arrive inscru
- **2026-04-08** — [[sources/01KJSTZKY2-the-second-half|The Second Half]]: The WMT'14 workshop report (Transformer's main benchmark) has approximately 1,300 citations while th
- **2026-04-08** — [[sources/01KJSVPQDA-the-think-tool-enabling-claude-to-stop-and-think|The "think" tool: Enabling Claude to stop and think]]: The 'think' tool creates dedicated space for structured thinking during complex tasks and is distinc
- **2026-04-08** — Wiki page created. Theme has 96 sources.
- **2025-12-08** — [[sources/01KJT4XPFE-on-the-interplay-of-pre-training-mid-training-and-rl-on-reasoning-language-model|On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models]]: The experimental models are 100M parameter Qwen2.5-style decoder-only models trained on a 30B token 
- **2025-12-05** — [[sources/01KJT5XWMY-the-missing-layer-of-agi-from-pattern-alchemy-to-coordination-physics|The Missing Layer of AGI: From Pattern Alchemy to Coordination Physics]]: UCCT defines anchoring strength as S = ρd − dr − γ log k, where ρd is effective support, dr is repre
- **2025-11-12** — [[sources/01KJT9BRN1-lumine-an-open-recipe-for-building-generalist-agents-in-3d-open-worlds|Lumine: An Open Recipe for Building Generalist Agents in 3D Open Worlds]]: Lumine processes raw pixels at 5 Hz to produce precise 30 Hz keyboard-mouse actions via action chunk
- **2025-11-07** — [[sources/01KJTAFQQB-real-time-reasoning-agents-in-evolving-environments|Real-Time Reasoning Agents in Evolving Environments]]: AgileThinker runs two LLMs in two parallel threads: a planning thread that performs extended reasoni
- **2025-10-30** — [[sources/01KJTBCK7K-thinkmorph-emergent-properties-in-multimodal-interleaved-chain-of-thought-reason|ThinkMorph: Emergent Properties in Multimodal Interleaved Chain-of-Thought Reasoning]]: Applying a constraint that target object bounding boxes occupy 1%-30% of image area reduces the Visu
- **2025-10-29** — [[sources/01KJTC6DXZ-supervised-reinforcement-learning-from-expert-trajectories-to-step-wise-reasonin|Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning]]: SRL decomposes expert solution trajectories into sequences of step actions and trains the model to p
- **2025-10-29** — [[sources/01KJTBPFB9-scaling-latent-reasoning-via-looped-language-models|Scaling Latent Reasoning via Looped Language Models]]: Ouro 1.4B and 2.6B LoopLM models match the performance of models up to 12B parameters across a wide 
- **2025-10-23** — [[sources/01KJTCC049-open-o3-video-grounded-video-reasoning-with-explicit-spatio-temporal-evidence|Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence]]: Open-o3 Video achieves state-of-the-art performance on V-STAR, improving mAM by +14.4% and mLGM by +
- **2025-10-16** — [[sources/01KJVF0TDN-how-gpt-5-thinks-openai-vp-of-research-jerry-tworek|How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek]]: o1 was primarily a technology demonstration rather than a polished or broadly useful product, being 
- **2025-10-10** — [[sources/01KJTDB22B-mitigating-overthinking-through-reasoning-shaping|Mitigating Overthinking through Reasoning Shaping]]: GRSP produces an average of 21.07 reasoning segments versus 26.66 from models trained without penalt
- **2025-10-08** — [[sources/01KJTDQZXF-the-markovian-thinker-architecture-agnostic-linear-scaling-of-reasoning|The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning]]: The standard RL reasoning environment makes the state unbounded, growing with longer thoughts, and f
- **2025-10-08** — [[sources/01KJTE28KR-base-models-know-how-to-reason-thinking-models-learn-when|Base Models Know How to Reason, Thinking Models Learn When]]: Thinking models significantly outperform their base counterparts on challenging reasoning benchmarks
- **2025-10-02** — [[sources/01KJTF2CYX-rlad-training-llms-to-discover-abstractions-for-solving-reasoning-problems|RLAD: Training LLMs to Discover Abstractions for Solving Reasoning Problems]]: RLAD achieves an average 44% improvement over DAPO (state-of-the-art long chain-of-thought RL) on AI
- **2025-09-29** — [[sources/01KJTF5EP6-mobilellm-r1-exploring-the-limits-of-sub-billion-language-model-reasoners-with-o|MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes]]: MobileLLM-R1-950M achieves an AIME score of 15.5, dramatically outperforming OLMo-2-1.48B (0.6) and 
- **2025-09-27** — [[sources/01KJVDK1KQ-294-arc-agi-2-top-score-jeremy-berman|29.4% ARC-AGI-2 🤯 (TOP SCORE!) - Jeremy Berman]]: ARC v2 is fundamentally different from ARC v1 because its tasks are compositional, requiring multipl
- **2025-09-24** — [[sources/01KJTGWJGM-language-models-that-think-chat-better|Language Models that Think, Chat Better]]: RLMT (RL with Model-rewarded Thinking) trains language models to generate long chain-of-thought reas
- **2025-09-24** — [[sources/01KJTG79VB-video-models-are-zero-shot-learners-and-reasoners|Video models are zero-shot learners and reasoners]]: Veo 3 was announced in May 2025 and released in July 2025; Veo 2 was announced December 2024 and rel
- **2025-09-24** — [[sources/01KJTGT235-thinking-augmented-pre-training|Thinking Augmented Pre-training]]: The vanilla 8B model trained on 100B tokens scores only 19.2 on GSM8k and 9.1 on MATH, while the TPT
- **2025-09-23** — [[sources/01KJTH6DPN-what-characterizes-effective-reasoning-revisiting-length-review-and-structure-of|What Characterizes Effective Reasoning? Revisiting Length, Review, and Structure of CoT]]: Naive CoT lengthening is associated with lower accuracy in large reasoning models.
- **2025-09-23** — [[sources/01KJTGTVN3-reinforcement-learning-on-pre-training-data|Reinforcement Learning on Pre-Training Data]]: RLPT used as initialization for RLVR yields additional improvements of 2.3 and 1.3 in Pass@1, and 3.
- **2025-09-22** — [[sources/01KJS34J20-thinking-searching-and-acting|Thinking, Searching, and Acting]]: Modern reasoning models are built on three fundamental primitives: Thinking (reasoning traces enabli
- **2025-09-18** — [[sources/01KJTF5CHP-flowrl-matching-reward-distributions-for-llm-reasoning|FlowRL: Matching Reward Distributions for LLM Reasoning]]: FlowRL transforms scalar rewards into a normalized target distribution using a learnable partition f
- **2025-09-03** — [[sources/01KJTKFTJ0-emergent-hierarchical-reasoning-in-llms-through-reinforcement-learning|Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning]]: HICRA amplifies the advantage for planning tokens in successful trajectories and dampens their penal
- **2025-09-01** — [[sources/01KJTK2Z9A-robix-a-unified-model-for-robot-interaction-reasoning-and-planning|Robix: A Unified Model for Robot Interaction, Reasoning and Planning]]: In the continued pretraining stage 2 (instruction tuning), the vision encoder is frozen while all ot
- **2025-08-30** — [[sources/01KJTM1K7F-parathinker-native-parallel-thinking-as-a-new-paradigm-to-scale-llm-test-time-co|ParaThinker: Native Parallel Thinking as a New Paradigm to Scale LLM Test-time Compute]]: ParaThinker achieves 12.3% average accuracy improvement over sequential LLMs for 1.5B models with 8 
- **2025-07-31** — [[sources/01KJTMRHHG-seed-prover-deep-and-broad-reasoning-for-automated-theorem-proving|Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving]]: Seed-Geometry's dataset from 230 million unique geometry problems totaled 38 billion tokens after pr
- **2025-07-22** — [[sources/01KJTN6GH7-beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty|Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty]]: RLCR provably incentivizes both accuracy and calibration: the combined reward is maximized when the 
- **2025-07-02** — [[sources/01KJTP54EY-naturalthoughts-selecting-and-distilling-reasoning-traces-for-general-reasoning-|NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks]]: Simply scaling up data size with random sampling is a strong baseline that yields steady performance
- **2025-06-30** — [[sources/01KJTNW0W4-thinking-with-images-for-multimodal-reasoning-foundations-methods-and-future-fro|Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers]]: Stage 3 (Intrinsic Visual Imagination) achieves full cognitive autonomy by using a unified generativ
- **2025-06-26** — [[sources/01KJTMPYR9-hierarchical-reasoning-model|Hierarchical Reasoning Model]]: HRM executes sequential reasoning tasks in a single forward pass without explicit supervision of the
- **2025-06-17** — [[sources/01KJTME7HT-reasoning-with-exploration-an-entropy-perspective|Reasoning with Exploration: An Entropy Perspective]]: Removing the clip-higher technique from RL training causes entropy to collapse to 0.03, compared to 
- **2025-06-17** — [[sources/01KJTQ0EQT-reinforcement-learning-with-verifiable-rewards-implicitly-incentivizes-correct-r|Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs]]: RLVR can extend the reasoning capability boundary for both mathematical and coding tasks, going beyo
- **2025-06-16** — [[sources/01KJTQ0YV3-direct-reasoning-optimization-constrained-rl-with-token-level-dense-reward-and-r|Direct Reasoning Optimization: Constrained RL with Token-Level Dense Reward and Rubric-Gated Constraints for Open-ended Tasks]]: R3 identifies reasoning-reflective tokens as those whose likelihoods exhibit high variability across
- **2025-06-10** — [[sources/01KJTQ6SB0-e3-learning-to-explore-enables-extrapolation-of-test-time-compute-for-llms|e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs]]: Most existing reasoning models do not extrapolate well when test-time compute is scaled beyond the m
- **2025-06-09** — [[sources/01KJTQH85K-reinforcement-pre-training|Reinforcement Pre-Training]]: RPT provides a stronger pre-trained foundation for subsequent reinforcement fine-tuning, leading to 
- **2025-06-04** — [[sources/01KKT43AHT-the-illusion-of-thinking|The Illusion of Thinking:]]: New capability: Reasoning models can explore and self-correct reasoning traces, finding correct 
- **2025-06-04** — [[sources/01KJSSZ6FW-a-taxonomy-for-next-generation-reasoning-models|A taxonomy for next-generation reasoning models]]: The four key capabilities of reasoning models — Skills, Calibration, Strategy, and Abstraction — mus
- **2025-06-02** — [[sources/01KJTQSWGF-beyond-the-8020-rule-high-entropy-minority-tokens-drive-effective-reinforcement-|Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning]]: Training RLVR using only the top 20% highest-entropy (forking) tokens in the policy gradient loss ac
- **2025-05-30** — [[sources/01KJTQXH92-reflect-retry-reward-self-improving-llms-via-reinforcement-learning|Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning]]: The Llama-3.1-70B model on Countdown is outclassed by the Qwen-2.5-3B model, which is more than 20x 
- **2025-05-29** — [[sources/01KJTRR26F-grounded-reinforcement-learning-for-visual-reasoning|Grounded Reinforcement Learning for Visual Reasoning]]: ViGoRL-7B achieves 91.0% on ScreenSpot-V2 and 33.1% on ScreenSpot-Pro, outperforming open-source VLM
- **2025-05-27** — [[sources/01KJTS8HZG-reinforcing-general-reasoning-without-verifiers|Reinforcing General Reasoning without Verifiers]]: VeriFree bypasses answer verification and instead uses RL to directly maximize the probability of ge
- **2025-05-26** — [[sources/01KJTSBRDC-reasoning-llms-are-wandering-solution-explorers|Reasoning LLMs are Wandering Solution Explorers]]: Systematic exploration must satisfy three properties: validity (traces must follow reachability stru
- **2025-05-19** — [[sources/01KJTV54QV-thinkless-llm-learns-when-to-think|Thinkless: LLM Learns When to Think]]: Thinkless reduces the usage of long-form reasoning by 50%–90% on benchmarks such as Minerva Algebra,
- **2025-05-19** — [[sources/01KJTTZHX6-adaptthink-reasoning-models-can-learn-when-to-think|AdaptThink: Reasoning Models Can Learn When to Think]]: AdaptThink reduces average response length of DeepSeek-R1-Distill-Qwen-7B by 40.1% while improving a
- **2025-05-19** — [[sources/01KJTTV05K-beyond-semantics-the-unreasonable-effectiveness-of-reasonless-intermediate-token|Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate Tokens]]: The study uses a model-organism paradigm: 0.5B parameter Qwen2.5 models trained from scratch on form
- **2025-05-05** — [[sources/01KJTV56AP-rm-r1-reward-modeling-as-reasoning|RM-R1: Reward Modeling as Reasoning]]: The Chain-of-Rubrics mechanism has the model first classify each input as either Chat or Reasoning t
- **2025-04-30** — [[sources/01KJTX2G5P-deepseek-prover-v2-advancing-formal-mathematical-reasoning-via-reinforcement-lea|DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition]]: DeepSeek-Prover-V2-671B solves 47 out of 658 problems from PutnamBench, more than 5x the next best m
- **2025-04-23** — [[sources/01KJTY5P1V-process-reward-models-that-think|Process Reward Models That Think]]: THINKPRM outperforms discriminative PRMs trained on full PRM800K by 8% on GPQA-Diamond and 4.5% on L
- **2025-04-16** — [[sources/01KJTZV5JK-climbing-the-ladder-of-reasoning-what-llms-can-and-still-cant-solve-after-sft|Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?]]: Exh-level questions are not addressed by scaling SFT dataset size; all SFT models across all dataset
- **2025-04-14** — [[sources/01KJTZYPKZ-reasoning-models-can-be-effective-without-thinking|Reasoning Models Can Be Effective Without Thinking]]: Reasoning models such as DeepSeek-R1 approach complex tasks by generating long chains of thought as 
- **2025-04-05** — [[sources/01KJSVB9E8-rl-backlog-openais-many-rls-clarifying-distillation-and-latent-reasoning|RL backlog: OpenAI's many RLs, clarifying distillation, and latent reasoning]]: OpenAI's Computer-Using Agent (CUA) is trained using reinforcement learning to interact with graphic
- **2025-03-31** — [[sources/01KJV1DNKJ-crossing-the-reward-bridge-expanding-rl-with-verifiable-rewards-across-diverse-d|Crossing the Reward Bridge: Expanding RL with Verifiable Rewards Across Diverse Domains]]: Strong open-source models including Qwen2.5-72B-Instruct and DeepSeek-R1-Distill-Qwen-32B perform po
- **2025-03-27** — [[sources/01KJV26GZX-cot-vla-visual-chain-of-thought-reasoning-for-vision-language-action-models|CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models]]: CoT-VLA achieves 81.13% average success rate on the LIBERO benchmark, outperforming OpenVLA (76.5%),
- **2025-03-25** — [[sources/01KJV1PKTA-research-learning-to-reason-with-search-for-llms-via-reinforcement-learning|ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning]]: ReSearch is trained from scratch without any labeled data on reasoning chains.
- **2025-03-18** — [[sources/01KKT56P61-2025-3-18|2025-3-18]]: Limitation identified: Quality of reasoning traces (thinking process) is not measured — only final answ
- **2025-03-13** — [[sources/01KJSVYBCE-advances-in-generative-ai-latent-space-reasoning-comparing-continuous-chain-of-t|Advances in Generative AI Latent Space Reasoning: Comparing Continuous Chain of Thought and Recurrent Depth Models]]: The recurrent block in the Recurrent Depth Approach can be applied multiple times before generating 
- **2025-03-11** — [[sources/01KJV31KSH-gtr-guided-thought-reinforcement-prevents-thought-collapse-in-rl-based-vlm-agent|GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM Agent Training]]: GTR achieves a 17.5% success rate on Points24, compared to GPT-4o+Tool at 13.5%, SFT-only at 11.0%, 
- **2025-03-11** — [[sources/01KKT5EC5T-monitoring-reasoning-models-for-misbehavior-and-the-risks-of|Monitoring Reasoning Models for Misbehavior and the Risks of]]: CoT monitoring was conducted in real-time during frontier model training, enabling detection and pat
- **2025-03-09** — [[sources/01KJV2XQ8N-vision-r1-incentivizing-reasoning-capability-in-multimodal-large-language-models|Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models]]: Vision-R1-CI (cold-start only, no RL) on the Llama-3.2-11B base improves MathVista from 48.6% to 62.
- **2025-03-09** — [[sources/01KJV3DVFC-agent-models-internalizing-chain-of-action-generation-into-reasoning-models|Agent models: Internalizing Chain-of-Action Generation into Reasoning models]]: Traditional agentic workflows rely on external prompts to manage interactions with tools and the env
- **2025-03-06** — [[sources/01KJV3G6RY-start-self-taught-reasoner-with-tools|START: Self-taught Reasoner with Tools]]: START achieves 95.0% on AMC23, a +15.0% absolute improvement over QwQ-32B-Preview.
- **2025-02-25** — [[sources/01KJV3MZFW-chain-of-draft-thinking-faster-by-writing-less|Chain of Draft: Thinking Faster by Writing Less]]: On GSM8K zero-shot setting, GPT-4o CoT achieves 94.8% accuracy using 278.4 tokens vs CoD at 84.4% us
- **2025-02-05** — [[sources/01KJV4D5YX-demystifying-long-chain-of-thought-reasoning-in-llms|Demystifying Long Chain-of-Thought Reasoning in LLMs]]: Long CoT SFT achieves higher performance upper limits than short CoT SFT and has not plateaued at 3.
- **2025-02-03** — [[sources/01KJV3X90H-sample-scrutinize-and-scale-effective-inference-time-search-by-scaling-verificat|Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification]]: On AIME 2024 Problem 11, only 1 out of 200 generated responses reached the correct answer (601), whi
- **2025-01-25** — [[sources/01KJVHQGH8-emergency-pod-reinforcement-learning-works-reflecting-on-chinese-models-deepseek|Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5]]: DeepSeek R1-Zero is trained using pure reinforcement learning with no human preference data, no huma
- **2025-01-22** — [[sources/01KJV50FH1-deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learnin|DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning]]: DeepSeek-V3-Base has 671 billion total parameters with 37 billion activated per token using a Mixtur
- **2025-01-09** — [[sources/01KJV5B2QG-search-o1-agentic-search-enhanced-large-reasoning-models|Search-o1: Agentic Search-Enhanced Large Reasoning Models]]: Search-o1 integrates an agentic RAG mechanism and a Reason-in-Documents module into the LRM reasonin
- **2024-12-20** — [[sources/01KJV5VMCP-deliberative-alignment-reasoning-enables-safer-language-models|Deliberative Alignment: Reasoning Enables Safer Language Models]]: Safety-trained models reference the correct policy category in their CoT at much higher accuracy tha
- **2024-12-09** — [[sources/01KJV65FZD-training-large-language-models-to-reason-in-a-continuous-latent-space|Training Large Language Models to Reason in a Continuous Latent Space]]: Coconut uses the last hidden state of the LLM as a 'continuous thought' representation of the reason
- **2024-12-06** — [[sources/01KJSXHZ75-how-i-came-in-first-on-arc-agi-pub-using-sonnet-35-with-evolutionary-test-time-c|How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute]]: The author achieved 53.6% accuracy on ARC-AGI-Pub using Claude Sonnet 3.5, setting a new public reco
- **2024-12-04** — [[sources/01KJSXKC7D-openais-o1-using-search-was-a-psyop|OpenAI's o1 using "search" was a PSYOP]]: Reinforcement learning methods used during training are themselves a form of search — they explore t
- **2024-12-03** — [[sources/01KJVHDMY1-inference-time-compute|Inference Time Compute]]: Process Reward Models provide fine-grained stepwise supervision at every reasoning step rather than 
- **2024-11-25** — [[sources/01KJV6JNEC-o1-replication-journey-part-2-surpassing-o1-preview-through-simple-distillation-|O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?]]: O1-preview achieves 85.5% on MATH500 with an average of 1501 output tokens, while the distilled 72B 
- **2024-11-21** — [[sources/01KJV6J7A4-marco-o1-towards-open-reasoning-models-for-open-ended-solutions|Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions]]: MCTS in Marco-o1 uses confidence scores derived from softmax-applied log probabilities of the top-5 
- **2024-11-15** — [[sources/01KJV6G030-llava-cot-let-vision-language-models-reason-step-by-step|LLaVA-CoT: Let Vision Language Models Reason Step-by-Step]]: InternLM-XComposer2.5-Reward was used as the reward model to judge generation quality during test-ti
- **2024-11-09** — [[sources/01KJVHWJNM-why-o1-is-a-big-deal|Why o1 is a BIG deal]]: Older LLMs do not use test-time compute; they generate answers instantaneously without spending ener
- **2024-10-14** — [[sources/01KJV7N48D-thinking-llms-general-instruction-following-with-thought-generation|Thinking LLMs: General Instruction Following with Thought Generation]]: In the TPO setup, thoughts are hidden from the end user and only the response part is shown, differe
- **2024-10-14** — [[sources/01KJVJ4E39-openai-o1s-new-paradigm-test-time-compute-explained|OpenAI o1's New Paradigm: Test-Time Compute Explained]]: OpenAI does not expose the full Chain of Thought token stream to API users, only providing the final
- **2024-10-04** — [[sources/01KJV75D18-system-2-reasoning-capabilities-are-nigh|System 2 Reasoning Capabilities Are Nigh]]: Monte Carlo Tree Search at inference time, guided by model predictions, improves game-playing model 
- **2024-10-02** — [[sources/01KJVGWEGP-openais-noam-brown-ilge-akkaya-and-hunter-lightman-on-o1-and-teaching-llms-to-re|OpenAI's Noam Brown, Ilge Akkaya and Hunter Lightman on o1 and Teaching LLMs to Reason Better]]: O1 is OpenAI's first major foray into general inference-time compute and reasoning.
- **2024-09-19** — [[sources/01KJV83GN1-training-language-models-to-self-correct-via-reinforcement-learning|Training Language Models to Self-Correct via Reinforcement Learning]]: SCoRe Stage II jointly optimizes both attempts using reward shaping that rewards self-correction pro
- **2024-09-18** — [[sources/01KJVHW24F-o1-what-is-going-on-why-o1-is-a-3rd-paradigm-of-model-10-things-you-might-not-kn|o1 - What is Going On? Why o1 is a 3rd Paradigm of Model + 10 Things You Might Not Know]]: O1's extra layer of reinforcement learning cannot be replicated through prompt engineering on the ba
- **2024-09-18** — [[sources/01KJV8DVH3-to-cot-or-not-to-cot-chain-of-thought-helps-mainly-on-math-and-symbolic-reasonin|To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning]]: In the meta-analysis, symbolic reasoning, math, and logical reasoning categories had average CoT imp
- **2024-09-10** — [[sources/01KJV8BD2M-kag-boosting-llms-in-professional-domains-via-knowledge-augmented-generation|KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation]]: The KAG E-Health application contains more than 1.8 million entities, 400,000 term sets, 5 million r
- **2024-08-27** — [[sources/01KJV7NM6A-generative-verifiers-reward-modeling-as-next-token-prediction|Generative Verifiers: Reward Modeling as Next-Token Prediction]]: GenRM-CoT can leverage majority voting over multiple sampled CoT rationales at test time to improve 
- **2024-08-21** — [[sources/01KJV8YY98-critique-out-loud-reward-models|Critique-out-Loud Reward Models]]: CLoud reward models are trained with a joint loss combining a reward modeling loss and a critique SF
- **2024-04-01** — [[sources/01KJVAT3JD-stream-of-search-sos-learning-to-search-in-language|Stream of Search (SoS): Learning to Search in Language]]: The SoS model achieves 51.27% accuracy on held-out inputs compared to 25.73% for the optimal path mo
- **2024-03-14** — [[sources/01KJVAWHZ0-quiet-star-language-models-can-teach-themselves-to-think-before-speaking|Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking]]: Quiet-STaR results in a substantial computational overhead because it generates many thought tokens 
- **2024-02-15** — [[sources/01KJVAAKMA-chain-of-thought-reasoning-without-prompting|Chain-of-Thought Reasoning Without Prompting]]: CoT-decoding combined with zero-shot CoT prompting achieves 48.4% on GSM8K for Mistral-7B, surpassin
- **2023-10-06** — [[sources/01KJVA39KX-language-agent-tree-search-unifies-reasoning-acting-and-planning-in-language-mod|Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models]]: LATS achieves 83.8% pass@1 on HumanEval with GPT-3.5, outperforming Reflexion (68.1%), ToT (54.4%),
