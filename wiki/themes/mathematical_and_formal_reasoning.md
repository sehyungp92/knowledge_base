---
type: theme
title: Mathematical & Formal Reasoning
theme_id: mathematical_and_formal_reasoning
level: 2
parent_theme: reasoning_and_planning
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 55
sources_since_update: 0
update_count: 1
velocity: 0.419
staleness: 0.0
status: active
tags: []
---
# Mathematical & Formal Reasoning

> Mathematical and formal reasoning has crossed a threshold: AI systems have moved from showing promise on structured problems to achieving gold-medal performance at the International Mathematical Olympiad — the hardest benchmark in competitive human mathematics — and are now beginning to surpass human-discovered results on open problems. The trajectory is unusually sharp, driven by a methodological shift from human-curated training data to reinforcement learning against formal verification oracles. The core capability is now rated narrow_production for olympiad-level and verifiable-domain tasks, though whether this wave extends to genuinely novel mathematical structure remains an open and honest question.

**Parent:** [[themes/reasoning_and_planning|reasoning_and_planning]]

## Current State

Until recently, the central bottleneck in mathematical AI was whether systems could operate reliably within formal verification environments rather than merely producing plausible-looking mathematics. AlphaProof broke this open by generating 100 million proofs through direct interaction with a formal proving environment, demonstrating that reinforcement learning against a verifiable oracle — not human judgment — could drive capability well beyond narrow practice problems. The feedback signal shifted from human evaluation to formal correctness: stricter, and infinitely scalable.

The IMO gold medal followed, achieved independently by both Google and OpenAI by mid-2025. That independence matters: it signals a genuine capability threshold the field has crossed, not an artifact of a single architecture. AlphaEvolve pushed further still — an LLM-guided evolutionary agent discovered provably correct algorithms surpassing decades-old state-of-the-art results, including improving Strassen's 1969 matrix multiplication algorithm, a result that had resisted 56 years of human effort.

The critical limitation that remains is structural rather than performance-based. Even AlphaEvolve has not resolved the minimum rank for 3×3 matrix multiplication — a fundamental open question. Current systems operate better as search-and-verification engines over known solution spaces than as generators of genuinely novel mathematical structure. That trajectory is rated unclear, which is honest: it is not obviously closing.

What to watch next is not another benchmark. If RL-over-formal-systems continues scaling, and if the algorithm-discovery results generalize beyond combinatorial optimization to deeper structural mathematics, the next inflection point is likely a published mathematical result attributed to an AI system in a research journal.

## Capabilities

- **IMO medal-level formal reasoning via RL** — AlphaProof achieved IMO medal-level performance in formal mathematics through reinforcement learning, generating 100 million proofs via interaction with a formal proving environment. *(maturity: narrow_production)*
- **Reliable performance on verifiable domains** — AI systems achieving consistent performance on coding, math, and accounting tasks sufficient for production automation in constrained, well-defined contexts. *(maturity: narrow_production)*
- **Dual IMO gold medal** — Google and OpenAI both achieved gold-medal performance on the International Mathematical Olympiad using LLMs, independently confirming the capability threshold. *(maturity: narrow_production)*
- **State-of-the-art math reasoning (non-thinking models)** — AIME 2024 69.6 Avg@64, AIME 2025 49.5 Avg@64, MATH-500 97.4%, demonstrating that even non-thinking-mode models have reached high competitive mathematics performance. *(maturity: narrow_production)*
- **Olympiad-level performance competitive with o3** — AIME24 91.0% (Avg@32), competitive with o3 (90.3%) and ahead of Gemini 2.5 Pro (88.7%). *(maturity: narrow_production)*
- **Near-perfect AIME 2025 performance with tool access** — o4-mini achieves 99.5% pass@1 (100% consensus@8) on AIME 2025 with Python interpreter access, ranking as best-performing on competition mathematics with tool augmentation. *(maturity: narrow_production)*
- **AI gold medal at IMO** — AI achieves gold medal performance at the International Mathematical Olympiad in a demonstration context. *(maturity: demo)*
- **Algorithm discovery beyond human state-of-the-art** — LLM-guided evolutionary coding agent discovers provably correct algorithms surpassing decades-old state-of-the-art mathematical results. *(maturity: demo)*

## Limitations

- **Fundamental open problems remain unresolved** — Even with AlphaEvolve's combinatorial search capacity, the minimum rank for 3×3 matrix multiplication — a foundational open question — has not been resolved. This suggests the current capability wave operates better as a search and verification engine over known solution spaces than as a generator of genuinely novel mathematical structure. *(severity: significant, trajectory: unclear, type: implicit_conspicuous_absence)*

## Bottlenecks

The primary bottleneck — reliable operation within formal verification systems rather than informal mathematical mimicry — has been substantively broken by AlphaProof's RL-over-formal-systems approach. The remaining structural bottleneck is whether that feedback loop can be extended to domains without clean formal oracles, and whether algorithm-discovery results generalize from combinatorial optimization to deeper structural mathematics where correctness is harder to verify automatically.

## Breakthroughs

- **AlphaEvolve: first improvement to 4×4 matrix multiplication in 56 years** — AlphaEvolve discovers a rank-48 algorithm for multiplying two 4×4 complex-valued matrices — the first improvement over Strassen's recursive bound of 49 scalar multiplications since 1969. *(significance: major — prior belief: For 56 years, no algorithm with fewer than 49 scalar multiplications existed for 4×4 matrix multiplication over fields with characteristic 0; applying Strassen recursively gave 49 and was the known bound)*
- **AI achieves IMO gold medal (first instance)** — AI achieves gold medal performance at the International Mathematical Olympiad — the first time AI has reached the top tier of competitive human mathematics, requiring creative insight, multi-step proof construction, and reasoning under open-ended problem formulations. *(significance: major — prior belief: Olympiad-level mathematics was beyond current AI capability)*
- **IMO gold confirmed by two independent systems** — Both Google and OpenAI achieved gold-medal performance on the IMO independently — the first time AI systems have achieved this at the top competitive tier, confirming the result is a genuine capability threshold rather than a system-specific artifact. *(significance: major — prior belief: AI systems had never achieved gold-medal IMO performance; medal-level via AlphaProof had been demonstrated but gold remained out of reach)*
- **AlphaProof: first AI IMO medal via formal RL** — AlphaProof became the first AI system to achieve a medal at the International Mathematical Olympiad, demonstrating that RL from experience in a formal proving environment was sufficient for open-ended mathematical discovery at this level. *(significance: major — prior belief: Frontier olympiad performance was considered the exclusive domain of human-centric AI or human mathematicians; RL from experience was thought insufficient)*

## Anticipations

The most consequential near-term anticipation: a published mathematical result attributed to an AI system in a peer-reviewed research journal, driven by the continued scaling of RL-over-formal-systems and extension of the AlphaEvolve algorithm-discovery paradigm. Secondary anticipation: formal reasoning benchmarks will need explicit controls for tool access (particularly Python interpreter access) to remain meaningful signals of unaided mathematical reasoning capability, given that tool-augmented systems have effectively saturated current competition benchmarks.

## Cross-Theme Implications

- → [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]: Near-perfect AIME performance with a Python interpreter shows that tool-augmented reasoning effectively closes the gap on competition mathematics benchmarks. This implies formal reasoning benchmarks must now explicitly control for tool access to remain meaningful signals of unaided mathematical reasoning capability — a methodological challenge for the field's evaluation infrastructure.

## Contradictions

The field's benchmark narrative and its structural reality are in tension. Benchmark saturation (near-perfect AIME scores, IMO gold) suggests the capability is mature and general. But the failure to resolve the minimum rank for 3×3 matrix multiplication — a small, well-posed combinatorial problem — suggests the systems are highly capable search engines over tractable solution spaces, not general mathematical reasoners. These two characterizations are not obviously compatible, and the gap between them is where the most important open questions live.

## Research Opportunities

- **Extending formal-verification RL to oracle-free domains** — AlphaProof's approach requires a clean formal verifier. Most important mathematical and scientific domains lack one. Developing techniques to apply similar RL feedback in domains with partial, noisy, or expensive oracles would substantially expand scope.
- **Separating search capability from structural novelty** — Current systems excel at searching known solution spaces. Understanding the architectural or training conditions under which genuinely novel mathematical structure can emerge (not just be found) is the central open research question this theme raises.
- **Benchmark methodology for tool-augmented reasoning** — With o4-mini achieving near-perfect AIME scores under tool access, the community needs new benchmark designs that cleanly separate unaided reasoning from tool-augmented performance, and competitive-style problems from research-style open-endedness.
- **Generalization of algorithm discovery** — AlphaEvolve's results are on combinatorial optimization (matrix multiplication algorithms). Whether the paradigm generalizes to structural mathematics — topology, number theory, algebraic geometry — is open and high-stakes.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KKT37T1M-reasoning-rl-a-new-recipe-for-ai-apps-foundation-capital|Reasoning + RL: A new recipe for AI apps - Foundation Capital]]: Breakthrough: Both Google and OpenAI achieved gold-medal performance on the International Math
- **2026-04-08** — Wiki page created. Theme has 55 sources.
- **2026-02-11** — [[sources/01KJRZT83A-gemini-deep-think-redefining-the-future-of-scientific-research|Gemini Deep Think: Redefining the Future of Scientific Research]]: Gemini Deep Think scored up to 90% on the IMO-ProofBench Advanced test as inference-time compute sca
- **2025-12-18** — [[sources/01KJT4HR3T-justrl-scaling-a-15b-llm-with-a-simple-rl-recipe|JustRL: Scaling a 1.5B LLM with a Simple RL Recipe]]: JustRL trains on two 1.5B models using 32 A800-80GB GPUs for approximately 15 days each.
- **2025-12-16** — [[sources/01KJT367PQ-universal-reasoning-model|Universal Reasoning Model]]: URM achieves 16.0% pass@1 on ARC-AGI 2, nearly tripling HRM (5.4%) and more than doubling TRM (4.6%)
- **2025-11-28** — [[sources/01KJT6RXNS-thetaevolve-test-time-learning-on-open-problems|ThetaEvolve: Test-time Learning on Open Problems]]: AlphaEvolve is a closed-source system.
- **2025-11-17** — [[sources/01KJT8B0BV-on-the-fundamental-limits-of-llms-at-scale|On the Fundamental Limits of LLMs at Scale]]: LLMs have five fundamental limitations that persist even under scaling: hallucination, context compr
- **2025-11-09** — [[sources/01KJTA8224-tiny-model-big-logic-diversity-driven-optimization-elicits-large-model-reasoning|Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B]]: MGPO degrades to standard GRPO when the regularization coefficient λ=0, and increases focus on uncer
- **2025-11-04** — [[sources/01KJTB00NQ-unlocking-the-power-of-multi-agent-llm-for-reasoning-from-lazy-agents-to-deliber|Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation]]: The Shapley-inspired causal influence method groups semantically similar steps across rollouts and a
- **2025-10-29** — [[sources/01KJTBPFB9-scaling-latent-reasoning-via-looped-language-models|Scaling Latent Reasoning via Looped Language Models]]: Ouro 1.4B and 2.6B LoopLM models match the performance of models up to 12B parameters across a wide 
- **2025-10-08** — [[sources/01KJTD0659-hybrid-reinforcement-when-reward-is-sparse-its-better-to-be-dense|Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense]]: HERO (Hybrid Ensemble Reward Optimization) integrates sparse verifier signals with dense reward mode
- **2025-10-08** — [[sources/01KJTE0Y5S-h1-bootstrapping-llms-to-reason-over-longer-horizons-via-reinforcement-learning|h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning]]: Curriculum RL training on composed GSM8K problems achieves a 2.06× improvement on AIME 2024 relative
- **2025-10-02** — [[sources/01KJTF2CYX-rlad-training-llms-to-discover-abstractions-for-solving-reasoning-problems|RLAD: Training LLMs to Discover Abstractions for Solving Reasoning Problems]]: Reasoning abstractions improve pass@k and coverage (max@k) on ARC-AGI across multiple sample counts,
- **2025-09-10** — [[sources/01KJTHH7D3-a-survey-of-reinforcement-learning-for-large-reasoning-models|A Survey of Reinforcement Learning for Large Reasoning Models]]: AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world c
- **2025-09-08** — [[sources/01KJTK49M5-the-majority-is-not-always-right-rl-training-for-solution-aggregation|The Majority is not always right: RL training for solution aggregation]]: AggLM-1.7B generalizes to candidate set sizes k both smaller and larger than the k=8 used during tra
- **2025-08-28** — [[sources/01KJTM994W-rstar2-agent-agentic-reasoning-technical-report|rStar2-Agent: Agentic Reasoning Technical Report]]: rStar2-Agent-14B achieves 80.6% pass@1 on AIME24, surpassing DeepSeek-R1 (671B), o3-mini (medium), a
- **2025-07-31** — [[sources/01KJTMRHHG-seed-prover-deep-and-broad-reasoning-for-automated-theorem-proving|Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving]]: Seed-Prover's performance is strongest on algebra (72/85) and weakest on combinatorics (7/14) among 
- **2025-07-24** — [[sources/01KJVJ6D0C-math-olympiad-gold-medalist-explains-openai-and-google-deepmind-imo-gold-perform|⚡️Math Olympiad gold medalist explains OpenAI and Google DeepMind IMO Gold Performances]]: Both DeepMind and OpenAI independently achieved gold medal level performance at IMO 2025, reasoning 
- **2025-07-21** — [[sources/01KJTN04YC-winning-gold-at-imo-2025-with-a-model-agnostic-verification-and-refinement-pipel|Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline]]: The pipeline applied to Gemini 2.5 Pro achieved 94.5% accuracy on IMC 2025, ranking #3 among 434 hum
- **2025-07-20** — [[sources/01KJTNH60K-the-invisible-leash-why-rlvr-may-or-may-not-escape-its-origin|The Invisible Leash: Why RLVR May or May Not Escape Its Origin]]: On AIME2024, the base model achieves pass@8192 = 93.3% while ProRL-1.5B only achieves 83.3%, demonst
- **2025-07-01** — [[sources/01KJTP56NV-does-math-reasoning-improve-general-llm-capabilities-understanding-transferabili|Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning]]: RL models show markedly smaller average token-rank shifts than SFT models; UniReason-Qwen3-14B-RL av
- **2025-06-23** — [[sources/01KJTPV81Q-rlpr-extrapolating-rlvr-to-general-domains-without-verifiers|RLPR: Extrapolating RLVR to General Domains without Verifiers]]: RLVR success remains largely confined to mathematical and code domains due to heavy reliance on doma
- **2025-06-17** — [[sources/01KJTQ0EQT-reinforcement-learning-with-verifiable-rewards-implicitly-incentivizes-correct-r|Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs]]: RLVR can extend the reasoning capability boundary for both mathematical and coding tasks, going beyo
- **2025-06-17** — [[sources/01KKT490MT-alphaevolve-a-coding-agent-for-scientific-and|AlphaEvolve: A coding agent for scientific and]]: Breakthrough: AlphaEvolve discovers a rank-48 algorithm for multiplying two 4×4 complex-valued
- **2025-06-12** — [[sources/01KJTQ74E7-spurious-rewards-rethinking-training-signals-in-rlvr|Spurious Rewards: Rethinking Training Signals in RLVR]]: A Python reward (rewarding any response containing the string 'python') causes Qwen2.5-Math-7B to ge
- **2025-06-02** — [[sources/01KJTQSWGF-beyond-the-8020-rule-high-entropy-minority-tokens-drive-effective-reinforcement-|Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning]]: Training RLVR using only the top 20% highest-entropy (forking) tokens in the policy gradient loss ac
- **2025-05-27** — [[sources/01KJSTGBK2-reinforcement-learning-with-random-rewards-actually-works-with-qwen-25|Reinforcement learning with random rewards actually works with Qwen 2.5]]: Standard RLVR with ground truth rewards improves Qwen 2.5 Math 7B MATH-500 score by +24.6 points.
- **2025-05-26** — [[sources/01KJTSAGB6-learning-to-reason-without-external-rewards|Learning to Reason without External Rewards]]: INTUITOR replaces external rewards in GRPO with self-certainty scores, enabling fully unsupervised r
- **2025-05-21** — [[sources/01KJTTJRKW-the-unreasonable-effectiveness-of-entropy-minimization-in-llm-reasoning|The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning]]: EM-INF treats output logits as free parameters and uses gradient descent to minimize entropy at each
- **2025-05-20** — [[sources/01KJTQH6AA-general-reasoner-advancing-llm-reasoning-across-all-domains|General-Reasoner: Advancing LLM Reasoning Across All Domains]]: The General-Verifier (1.5B parameter model-based verifier) achieves 78.7% agreement with Gemini-2.0-
- **2025-05-06** — [[sources/01KJTWFMSP-absolute-zero-reinforced-self-play-reasoning-with-zero-data|Absolute Zero: Reinforced Self-play Reasoning with Zero Data]]: AZR uses three complementary reasoning modes—deduction, abduction, and induction—each corresponding 
- **2025-04-30** — [[sources/01KJTX2G5P-deepseek-prover-v2-advancing-formal-mathematical-reasoning-via-reinforcement-lea|DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition]]: DeepSeek-Prover-V2-671B achieves 88.9% pass ratio on MiniF2F-test, establishing state-of-the-art per
- **2025-04-29** — [[sources/01KJTSHBZT-reinforcement-learning-for-reasoning-in-large-language-models-with-one-training-|Reinforcement Learning for Reasoning in Large Language Models with One Training Example]]: Post-saturation generalization occurs in 1-shot RLVR: training accuracy saturates near 100% rapidly 
- **2025-04-23** — [[sources/01KJTY5P1V-process-reward-models-that-think|Process Reward Models That Think]]: THINKPRM outperforms discriminative PRMs trained on full PRM800K by 8% on GPQA-Diamond and 4.5% on L
- **2025-04-16** — [[sources/01KJTZV5JK-climbing-the-ladder-of-reasoning-what-llms-can-and-still-cant-solve-after-sft|Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?]]: Exh-level questions are not addressed by scaling SFT dataset size; all SFT models across all dataset
- **2025-04-15** — [[sources/01KJTZD9X5-retool-reinforcement-learning-for-strategic-tool-use-in-llms|ReTool: Reinforcement Learning for Strategic Tool Use in LLMs]]: ReTool (DeepSeek-R1-Distill-Qwen-32B backbone) achieves 72.5% accuracy on AIME 2024, surpassing Open
- **2025-04-14** — [[sources/01KJTZYPKZ-reasoning-models-can-be-effective-without-thinking|Reasoning Models Can Be Effective Without Thinking]]: Reasoning models such as DeepSeek-R1 approach complex tasks by generating long chains of thought as 
- **2025-04-10** — [[sources/01KJTZZW1M-dynamic-cheatsheet-test-time-learning-with-adaptive-memory|Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory]]: Claude 3.5 Sonnet's AIME 2024 accuracy jumped from 23% to 50% under DC-Cu, more than doubling its ba
- **2025-03-30** — [[sources/01KJV1PA03-torl-scaling-tool-integrated-rl|ToRL: Scaling Tool-Integrated RL]]: TORL uses a rule-based reward function: correct answers receive +1, incorrect answers receive -1, an
- **2025-03-02** — [[sources/01KJV3PQ9W-a-law-reasoning-benchmark-for-llm-with-tree-organized-structures-including-factu|A Law Reasoning Benchmark for LLM with Tree-Organized Structures including Factum Probandum, Evidence and Experiences]]: The crowd-sourced dataset contains 453 cases, 2,627 factum probandum, 14,578 pieces of evidence, and
- **2025-02-10** — [[sources/01KJV47G2K-can-1b-llm-surpass-405b-llm-rethinking-compute-optimal-test-time-scaling|Can 1B LLM Surpass 405B LLM? Rethinking Compute-Optimal Test-Time Scaling]]: TTS approaches can be divided into Internal TTS (training LLMs with long CoT) and External TTS (samp
- **2025-02-03** — [[sources/01KJV3X90H-sample-scrutinize-and-scale-effective-inference-time-search-by-scaling-verificat|Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification]]: On AIME 2024 Problem 11, only 1 out of 200 generated responses reached the correct answer (601), whi
- **2025-02-03** — [[sources/01KJV4T8S3-zebralogic-on-the-scaling-limits-of-llms-for-logical-reasoning|ZebraLogic: On the Scaling Limits of LLMs for Logical Reasoning]]: The solution space of a ZebraLogic N×M puzzle is (N!)^M, increasing factorially with grid size
- **2025-01-31** — [[sources/01KJV4M1H3-s1-simple-test-time-scaling|s1: Simple test-time scaling]]: DeepSeek r1-distill achieves stronger performance than s1-32B on AIME24 (72.6% vs 56.7%) while using
- **2025-01-09** — [[sources/01KJVDVYWF-françois-chollet-on-openai-o-models-and-arc|François Chollet on OpenAI o-models and ARC]]: ARC is intended as a research tool and compass toward AGI, not a binary indicator of whether AGI has
- **2025-01-08** — [[sources/01KJV5D2Z7-rstar-math-small-llms-can-master-math-reasoning-with-self-evolved-deep-thinking|rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking]]: Terminal nodes in MCTS are scored as +1 for correct answers and -1 for incorrect answers, with Q-val
- **2024-12-05** — [[sources/01KJV5E1EB-arc-prize-2024-technical-report|ARC Prize 2024: Technical Report]]: Deep learning-guided program synthesis does not currently decisively beat DSL-based brute-force prog
- **2024-11-25** — [[sources/01KJV6JNEC-o1-replication-journey-part-2-surpassing-o1-preview-through-simple-distillation-|O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?]]: O1-preview achieves 85.5% on MATH500 with an average of 1501 output tokens, while the distilled 72B 
- **2024-11-04** — [[sources/01KJV6C0D1-combining-induction-and-transduction-for-abstract-reasoning|Combining Induction and Transduction for Abstract Reasoning]]: The scaled-down BARC model (for Kaggle's private test set with limited compute) scores 19% on the pr
- **2024-10-19** — [[sources/01KJVMA9D5-gsm-symbolic-understanding-the-limitations-of-mathematical-reasoning-in-large-la|GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models]]: GSM-Symbolic is constructed from 100 GSM 8K templates, each generating 50 samples, yielding 5,000 to
- **2024-09-18** — [[sources/01KJV8DVH3-to-cot-or-not-to-cot-chain-of-thought-helps-mainly-on-math-and-symbolic-reasonin|To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning]]: In the meta-analysis, symbolic reasoning, math, and logical reasoning categories had average CoT imp
- **2024-08-27** — [[sources/01KJSY2CEB-scaling-test-time-compute-a-new-paradigm-in-llm-performance|Scaling Test-Time Compute: A New Paradigm in LLM Performance]]: The study evaluates two key strategies for enhancing LLM performance at test-time: dense verifier re
- **2024-08-27** — [[sources/01KJV7NM6A-generative-verifiers-reward-modeling-as-next-token-prediction|Generative Verifiers: Reward Modeling as Next-Token Prediction]]: GenRM-CoT can leverage majority voting over multiple sampled CoT rationales at test time to improve 
- **2024-06-20** — [[sources/01KJV943BV-q-improving-multi-step-reasoning-for-llms-with-deliberative-planning|Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning]]: On the MATH dataset, DeepSeek-Math-7b enhanced with Q* achieves 55.4% accuracy, surpassing Gemini Ul
- **2024-01-21** — [[sources/01KJVMD0J9-alphageometry-solving-olympiad-geometry-without-human-demonstrations-paper-expla|AlphaGeometry: Solving olympiad geometry without human demonstrations (Paper Explained)]]: AlphaGeometry is a neuro-symbolic system that combines trained language models with symbolic solvers
- **2023-12-14** — [[sources/01KJVB9Y21-math-shepherd-verify-and-reinforce-llms-step-by-step-without-human-annotations|Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations]]: Hard Estimation (HE) labels a step as good if any one of N completion paths reaches the correct answ
