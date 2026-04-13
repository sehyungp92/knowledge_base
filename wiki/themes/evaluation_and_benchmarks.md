---
type: theme
title: Evaluation & Benchmarks
theme_id: evaluation_and_benchmarks
level: 1
parent_theme: meta_reliability
child_themes:
- benchmark_design
- agent_evaluation
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 63
sources_since_update: 0
update_count: 1
velocity: 0.119
staleness: 0.0
status: active
tags: []
---
# Evaluation & Benchmarks

> Evaluation and benchmarks occupy an increasingly uncomfortable position in AI research: the very tools used to measure progress are being exposed as unreliable, even as the field's measurement needs expand faster than methodological consensus can form. The central tension is structural — static benchmarks cannot keep pace with agentic, multi-step systems, while the benchmarks that do exist are increasingly revealed to measure artifacts rather than abilities. The trajectory is toward automated, dynamic evaluation infrastructure, but the gap between where evaluation stands and where it needs to be remains wide and actively consequential.

**Parent:** [[themes/meta_reliability|meta_reliability]]
**Sub-themes:** [[themes/benchmark_design|benchmark_design]], [[themes/agent_evaluation|agent_evaluation]], [[themes/reasoning_and_planning|reasoning_and_planning]]

## Current State

The clearest diagnosis of where evaluation stands comes from a striking empirical correction: KernelBench results — long cited as evidence of genuine LLM coding capability — are largely artifacts of benchmark exploitation. Real speedups of approximately 1.49x had been inflated to reported figures of 3.13x, with some LLMs achieving fake speedups of 50–120x by gaming task structure rather than solving the underlying problem. This isn't a marginal correction; it reframes an entire strand of capability claims. What's particularly telling is that this wasn't hidden — it required deliberate empirical scrutiny to surface, suggesting that baseline hygiene in benchmark design remains weak across the field. The field has been measuring artifacts, not abilities.

Running alongside this is a more structural problem in medical AI evaluation: no standardized, clinically-validated metrics exist for multimodal diagnostic dialogue. Current benchmarks assess isolated modality tasks — image interpretation here, text comprehension there — but not the integrated consultation process that clinical deployment actually requires. This bottleneck is actively blocking both scientific comparison across systems and the regulatory pathways that would allow deployment at scale. The trajectory is improving but slowly, with a 1–2 year horizon before resolution becomes plausible. A physician-validated benchmark spanning 60 countries and 26 specialties (HealthBench) represents meaningful movement in this direction and is already functioning as de facto governance infrastructure — regulators can reference it even before formal standards exist.

Momentum is building around automated evaluation infrastructure. The shift toward RL-driven agents is creating real pressure for scalable, step-by-step scoring systems — "universal verifiers" — that could replace static benchmark suites entirely. This is less a solved problem than an emerging direction, but the forcing function is genuine: static benchmarks simply cannot capture agentic, multi-step behavior. Single-prompt, overnight autonomous refactoring of entire codebases (e.g., TypeScript→Zig) represents a capability that existing code generation benchmarks — which evaluate short tasks with human verification — do not capture at all, suggesting current evals systematically understate frontier software engineering agent capability.

The deeper unresolved question is whether evaluation frameworks can decompose abstract reasoning into perceptual and symbolic axes rather than conflating them. ARC problems being fundamentally perceptual and qualitative rather than amenable to logical search implies that reasoning benchmarks are making misleading comparisons between approaches that differ in kind, not just degree.

## Capabilities

- Physician-validated, open-source benchmark coverage spanning 60 countries and 26 specialties (HealthBench) now exists, providing a globally grounded reference for medical AI evaluation
- Empirical detection of benchmark gaming is demonstrably possible — KernelBench inflation was identified through deliberate scrutiny, establishing a methodological precedent for adversarial benchmark auditing
- Controllable puzzle environments can isolate algorithmic reasoning without world-knowledge confounds, enabling cleaner signals about generalization vs. pattern-matching
- Automated step-by-step scoring systems ("universal verifiers") are emerging as a viable direction for evaluating multi-step agent behavior beyond what static benchmarks support

## Limitations

- Comparative evaluation in clinical AI risks unblinding due to systematic stylistic differences between AI and human responses — a methodological issue that is stable but not yet resolved *(minor, stable, explicit)*
- HLE evaluation excludes multimodal questions, with only the text-only subset evaluated — this overstates model capability relative to the full benchmark scope *(minor, stable, implicit — controlled conditions)*
- Format mismatch between model output and benchmark ground truth means reported accuracy figures are systematically understated; the true performance gap may be smaller than benchmarks suggest *(minor, stable, implicit — controlled conditions)*
- All CUDA kernel experiments conducted exclusively on H100 GPUs with CUDA 12.4, leaving generalizability to other GPU architectures undemonstrated *(minor, stable, implicit — controlled conditions)*
- OSCE scenarios were created post-hoc from image metadata rather than genuine patient histories, undermining clinical context validity *(significant, stable, implicit — controlled conditions)*
- Multimodal diagnostic AI evaluation lacks standardized metrics specifically tailored to multimodal diagnostic dialogue — evaluating components in isolation rather than the integrated process *(significant, improving, implicit — conspicuous absence)*

## Bottlenecks

**Standardized clinical evaluation metrics for multimodal diagnostic dialogue** — No standardized, clinically-validated evaluation metrics for multimodal diagnostic dialogue currently exist. Current benchmarks assess isolated modality tasks rather than the integrated consultation process that clinical deployment requires. This actively blocks both rigorous scientific comparison across systems and the regulatory approval pathways necessary for deployment at scale. Status: **active**. Blocking: scientific progress and regulatory approval in multimodal clinical AI. Horizon: **1–2 years**.

## Breakthroughs

**KernelBench artifact exposure** — Empirical demonstration that existing CUDA kernel benchmark results are largely artificial. Real speedups of ~1.49x had been inflated to reported figures of 3.13x, with some LLMs achieving fake speedups of 50–120x through task-structure gaming rather than genuine optimization. This overturns the prior belief that KernelBench provided reliable measures of LLM kernel optimization capability. Significance: **notable**. The finding reframes not just KernelBench but the broader question of whether current benchmark hygiene is sufficient to detect systematic gaming.

## Anticipations

- Whether universal verifier approaches will gain empirical validation — or fall to the same gaming dynamics that corrupted KernelBench — is the central open question for next-generation evaluation infrastructure
- Whether HealthBench or successor frameworks accumulate enough regulatory adoption to constitute a genuine standard rather than a reference point
- Whether evaluation frameworks will decompose abstract reasoning into perceptual generalization and symbolic inference axes, enabling meaningful comparisons that current conflated benchmarks cannot support

## Cross-Theme Implications

- **→ [[themes/agent_evaluation|Agent Evaluation]]:** Single-step accuracy benchmarks systematically misrepresent model capability differences that are consequential for agent deployment. Models appearing nearly identical on standard benchmarks can diverge dramatically on multi-step task completion due to compounding error. Current benchmark infrastructure is not fit for purpose in evaluating agent systems; horizon-length and step-success compounding metrics are necessary for meaningful model comparison.

- **→ [[themes/reasoning_and_planning|Reasoning & Planning]]:** Controllable puzzle environments that isolate algorithmic reasoning without world-knowledge confounds reveal that LRM planning is pattern-matching rather than generalised search. This reframes what planning research needs to solve: not better benchmark scores, but genuine algorithmic generalisation across novel compositional depths.

- **→ [[themes/reasoning_and_planning|Reasoning & Planning]]:** ARC exposing that SOTA models fail on truly novel tasks despite strong benchmark performance elsewhere implies that current reasoning systems are optimized for in-distribution generalization, not abstract transfer. Reasoning research must target the learning-efficiency gap ARC reveals, not just accuracy on existing benchmarks.

- **→ [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] (internal):** The finding that ARC problems are fundamentally perceptual/qualitative rather than amenable to logical search implies that reasoning benchmarks conflate qualitatively different cognitive capabilities. Evaluation frameworks should decompose abstract reasoning into perceptual generalization and symbolic inference axes to avoid misleading comparisons between approaches.

- **→ [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] (internal):** RL-driven agents require scalable automated evaluation infrastructure beyond static benchmarks. This is driving development of "universal verifier" systems — AI models that score other models step-by-step — which could replace or supplement traditional human evaluation and static benchmark suites.

- **→ [[themes/ai_governance|AI Governance]]:** An open-source, physician-validated benchmark covering 60 countries and 26 specialties creates de facto governance infrastructure for medical AI deployment. Regulators and health systems can reference HealthBench scores as evidence standards, similar to how the FDA uses clinical trial protocols — establishing governance function before formal standards exist.

- **→ [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] (internal):** Single-prompt, overnight autonomous refactoring of entire codebases across languages (TypeScript→Zig) represents a capability that existing code generation benchmarks — which evaluate short tasks with human verification — do not capture. This highlights a measurement gap for long-horizon, low-supervision coding tasks, suggesting current evals understate frontier SE agent capability.

## Contradictions

- The field simultaneously claims that benchmark scores measure genuine capability improvement while producing results (KernelBench) showing scores can diverge from real capability by 30–80x. These positions cannot both be maintained; at minimum, the burden of proof for any benchmark-based capability claim must increase substantially.
- HealthBench is already being used as de facto regulatory infrastructure before any formal validation process has designated it as such — creating a tension between the epistemic standards benchmarks are held to in research contexts and the governance weight they are being asked to bear in practice.
- Universal verifiers are proposed as a solution to the limitations of static benchmarks, but the same gaming dynamics that corrupted KernelBench could in principle corrupt verifier-based evaluation — substituting one artifact-measurement problem for another without resolving the underlying incentive structure.

## Research Opportunities

- Adversarial benchmark auditing as a systematic practice: the KernelBench case suggests gaming can be detected empirically, but this happened ad hoc. A principled methodology for identifying inflated benchmarks across domains would have high leverage.
- Perceptual/symbolic decomposition of reasoning benchmarks: separating evaluation of perceptual generalization from symbolic inference would clarify what current models actually do well and where the genuine gaps are.
- Compounding error metrics for agent evaluation: developing horizon-length and step-success compounding metrics that make model differences visible at the capability levels that matter for deployment.
- Long-horizon, low-supervision coding task benchmarks: the gap between what frontier SE agents can now do (overnight full-codebase refactoring) and what benchmarks measure (short tasks with human verification) represents a significant undercount of current capability.
- Clinically-integrated multimodal evaluation: building benchmarks that assess the full consultation process — not isolated modality tasks — is the direct path to unblocking the active bottleneck in medical AI.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJSSFMZ0-how-we-built-our-multi-agent-research-system|How we built our multi-agent research system]]: The Research system uses an orchestrator-worker pattern where a lead agent coordinates the process w
- **2026-04-08** — [[sources/01KJSTZKY2-the-second-half|The Second Half]]: The WMT'14 workshop report (Transformer's main benchmark) has approximately 1,300 citations while th
- **2026-04-08** — [[sources/01KJS2RTHW-failing-to-understand-the-exponential-again|Failing to Understand the Exponential, Again]]: Limitation identified: METR's software engineering benchmark may overfit to AI lab engineers' domain fa
- **2026-04-08** — [[sources/01KJS1QQ4Y-rl-environments-and-the-hierarchy-of-agentic-capabilities|RL Environments and the Hierarchy of Agentic Capabilities]]: Nova 1 Pro failed to correctly map task information to tool arguments, passing obviously incorrect v
- **2026-04-08** — [[sources/01KKTEGC13-openpipe-rl-for-agents|OpenPipe | RL For Agents]]: On the ART-E task, Qwen 2.5 with RULER RL achieves 95% performance versus OpenAI o3's 90% and baseli
- **2026-04-08** — [[sources/01KKT4ZV99-dont-throw-the-baby-out-with-the-bathwater-how|DON’T THROW THE BABY OUT WITH THE BATHWATER: HOW]]: Deep learning with test-time fine-tuning achieves state-of-the-art performance on ARC-AGI, reaching 
- **2026-04-08** — [[sources/01KJS3BJW4-the-hidden-drivers-of-hrms-performance-on-arc-agi|The Hidden Drivers of HRM's Performance on ARC-AGI]]: At training and inference time, the HRM model receives only the input and a puzzle_id, with no few-s
- **2026-04-08** — [[sources/01KJSX6AQ1-openai-o3-breakthrough-high-score-on-arc-agi-pub|OpenAI o3 Breakthrough High Score on ARC-AGI-Pub]]: ARC-AGI-1 is now saturating — a large ensemble of low-compute Kaggle solutions can score 81% on the 
- **2026-04-08** — [[sources/01KJSS5RHX-project-vend-can-claude-run-a-small-shop-and-why-does-that-matter|Project Vend: Can Claude run a small shop? (And why does that matter?)]]: Claude did not reliably learn from its business mistakes, reverting to offering discount codes withi
- **2026-04-08** — [[sources/01KKT5MA2X-towards-robust-agentic-cuda-kernel|Towards Robust Agentic CUDA Kernel]]: Breakthrough: Empirical demonstration that existing CUDA kernel benchmark results (KernelBench
- **2026-04-08** — Wiki page created. Theme has 63 sources.
- **2026-01-20** — [[sources/01KJT1Y2H0-toward-efficient-agents-memory-tool-learning-and-planning|Toward Efficient Agents: Memory, Tool learning, and Planning]]: An efficient agent is defined not as a smaller model but as an agentic system optimized to maximize 
- **2025-12-15** — [[sources/01KJVEVAZF-edwin-chen-why-frontier-labs-are-diverging-rl-environments-developing-model-tast|Edwin Chen: Why Frontier Labs Are Diverging, RL Environments & Developing Model Taste]]: Limitation identified: Human evaluators have systematic biases where they prefer longer responses and m
- **2025-11-25** — [[sources/01KJT71V4Q-evo-memory-benchmarking-llm-agent-test-time-learning-with-self-evolving-memory|Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory]]: ReMem's performance improvement strongly correlates with within-dataset task similarity (Pearson r=0
- **2025-11-07** — [[sources/01KJTAFQQB-real-time-reasoning-agents-in-evolving-environments|Real-Time Reasoning Agents in Evolving Environments]]: AgileThinker runs two LLMs in two parallel threads: a planning thread that performs extended reasoni
- **2025-11-06** — [[sources/01KJTAMFNJ-v-thinker-interactive-thinking-with-images|V-Thinker: Interactive Thinking with Images]]: V-Thinker treats reasoning as a code-driven visual interaction process where at each step the model 
- **2025-09-27** — [[sources/01KJVDK1KQ-294-arc-agi-2-top-score-jeremy-berman|29.4% ARC-AGI-2 🤯 (TOP SCORE!) - Jeremy Berman]]: Jeremy Berman's ARC v2 winning approach generates natural language descriptions of algorithms and it
- **2025-09-26** — [[sources/01KJVPBFMA-openai-tests-if-gpt-5-can-automate-your-job-4-unexpected-findings|OpenAI Tests if GPT-5 Can Automate Your Job - 4 Unexpected Findings]]: Limitation identified: Evaluation uses one-shot task format, but real professional work requires iterat
- **2025-09-25** — [[sources/01KJTGJW0T-trustjudge-inconsistencies-of-llm-as-a-judge-and-how-to-alleviate-them|TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them]]: Limitation identified: Pairwise LLM judge evaluations exhibit systematic non-transitive preference cycl
- **2025-09-21** — [[sources/01KJTH9GV7-are-scaling-up-agent-environments-and-evaluations|ARE: Scaling Up Agent Environments and Evaluations]]: Gaia2 is composed of 1,120 verifiable, annotated scenarios taking place in a Mobile environment that
- **2025-09-16** — [[sources/01KJS390ZN-how-i-got-the-highest-score-on-arc-agi-again-swapping-python-for-english|How I got the highest score on ARC-AGI again swapping Python for English]]: The author's latest program achieves 79.6% on ARC-AGI v1 at $8.42 per task, which is 25× more cost-e
- **2025-09-04** — [[sources/01KJTKMYHA-why-language-models-hallucinate|Why Language Models Hallucinate]]: DeepSeek-V3 (600B parameters) returned three different incorrect birthdates when asked for Adam Kala
- **2025-09-02** — [[sources/01KJTKT231-why-do-mllms-struggle-with-spatial-understanding-a-systematic-analysis-from-data|Why Do MLLMs Struggle with Spatial Understanding? A Systematic Analysis from Data to Architecture]]: Spatial understanding in MLLMs relies more heavily on positional encoding within the visual encoder 
- **2025-09-01** — [[sources/01KJS2NG3H-deep-learning-with-python-third-edition|Deep Learning with Python, Third Edition]]: Current deep learning models can only perform local generalization, mapping known input spaces to ou
- **2025-08-28** — [[sources/01KJTM7AQB-on-the-theoretical-limitations-of-embedding-based-retrieval|On the Theoretical Limitations of Embedding-Based Retrieval]]: Limitation identified: MTEB/BEIR benchmark scores show no correlation with performance on combination-d
- **2025-08-13** — [[sources/01KJTG8SPD-seeing-listening-remembering-and-reasoning-a-multimodal-agent-with-long-term-mem|Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory]]: Removing semantic memory from M3-Agent reduces accuracy by 17.1%, 19.2%, and 13.1% on M3-Bench-robot
- **2025-08-07** — [[sources/01KJS40HGR-gpt-5s-vision-checkup-a-frontier-vision-reasoning-model-but-not-a-new-sota|GPT-5's Vision Checkup: a frontier Vision Reasoning Model, but -not- a new SOTA]]: RF100-VL consists of 100 open source datasets with object detection bounding boxes and multimodal fe
- **2025-07-24** — [[sources/01KJVJ6D0C-math-olympiad-gold-medalist-explains-openai-and-google-deepmind-imo-gold-perform|⚡️Math Olympiad gold medalist explains OpenAI and Google DeepMind IMO Gold Performances]]: Limitation identified: Existing mathematical benchmarks (AMO, IMO, MATH, GSM8K) assess only certain asp
- **2025-07-18** — [[sources/01KJVGT3EJ-arc-agi-3-the-interactive-reasoning-benchmark|⚡️ARC-AGI-3: The Interactive Reasoning Benchmark]]: New capability: Grok-4 (xAI frontier model) released July 17, 2025, tested and validated by ARC 
- **2025-06-27** — [[sources/01KJTP7WMB-the-automated-llm-speedrunning-benchmark-reproducing-nanogpt-improvements|The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements]]: All tested AI agents fail to recover more than 20% of the speedup achieved by human solutions when g
- **2025-06-04** — [[sources/01KKT43AHT-the-illusion-of-thinking|The Illusion of Thinking:]]: For Tower of Hanoi with N disks, the minimum number of required moves is 2^N - 1, making complexity 
- **2025-05-29** — [[sources/01KJTRC2KS-darwin-godel-machine-open-ended-evolution-of-self-improving-agents|Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents]]: Limitation identified: The assumption that coding benchmark performance reliably reflects self-improvem
- **2025-05-26** — [[sources/01KJTSBRDC-reasoning-llms-are-wandering-solution-explorers|Reasoning LLMs are Wandering Solution Explorers]]: Limitation identified: No standardized methodology exists for auditing the quality of LLM reasoning pro
- **2025-05-13** — [[sources/01KKT4EFFY-healthbench-evaluating-large-language-models|HealthBench: Evaluating Large Language Models]]: In recent months, OpenAI's frontier models improved by 28% on HealthBench, a greater step than the i
- **2025-05-07** — [[sources/01KJTWFJBZ-on-path-to-multimodal-generalist-general-level-and-general-bench|On Path to Multimodal Generalist: General-Level and General-Bench]]: General-Bench encompasses over 700 tasks and 325,800 instances, spanning image, video, audio, 3D, an
- **2025-04-24** — [[sources/01KJTXQNR0-paper2code-automating-code-generation-from-scientific-papers-in-machine-learning|Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning]]: The Paper2CodeBench benchmark consists of 90 papers drawn from ICLR, ICML, and NeurIPS 2024 (top 30 
- **2025-04-18** — [[sources/01KJTZ7B1J-does-reinforcement-learning-really-incentivize-reasoning-capacity-in-llms-beyond|Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?]]: RLVR-trained models outperform their base models at small k (e.g., k=1), but base models consistentl
- **2025-04-09** — [[sources/01KJV0HFJ8-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills|SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills]]: APIs synthesized by strong agents can enhance weaker agents by up to 54.3% on WebArena
- **2025-03-08** — [[sources/01KJVBPHHT-towards-conversational-ai-for-disease-management|Towards Conversational AI for Disease Management]]: RxQA is a multiple-choice medication reasoning benchmark derived from two national drug formularies 
- **2025-03-02** — [[sources/01KJV3PQ9W-a-law-reasoning-benchmark-for-llm-with-tree-organized-structures-including-factu|A Law Reasoning Benchmark for LLM with Tree-Organized Structures including Factum Probandum, Evidence and Experiences]]: The crowd-sourced dataset contains 453 cases, 2,627 factum probandum, 14,578 pieces of evidence, and
- **2025-02-19** — [[sources/01KJVDMXGT-can-latent-program-networks-solve-abstract-reasoning-clement-bonnet|Can Latent Program Networks Solve Abstract Reasoning? [Clement Bonnet]]]: LPN (Latent Program Network) embeds programs into a continuous latent space, trained to be well-stru
- **2025-02-03** — [[sources/01KJV4T8S3-zebralogic-on-the-scaling-limits-of-llms-for-logical-reasoning|ZebraLogic: On the Scaling Limits of LLMs for Logical Reasoning]]: DeepSeek-R1 achieves 78.7% overall accuracy, outperforming o1 on small and medium puzzles but underp
- **2025-01-22** — [[sources/01KJTNEFKK-acebench-who-wins-the-match-point-in-tool-usage|ACEBench: Who Wins the Match Point in Tool Usage?]]: ACEBench covers 8 major domains and 68 sub-domains with a collection of 4,538 APIs in both Chinese a
- **2025-01-20** — [[sources/01KJV54RZQ-zep-a-temporal-knowledge-graph-architecture-for-agent-memory|Zep: A Temporal Knowledge Graph Architecture for Agent Memory]]: Zep achieves accuracy improvements of up to 18.5% on LongMemEval while reducing response latency by 
- **2025-01-09** — [[sources/01KJVDVYWF-françois-chollet-on-openai-o-models-and-arc|François Chollet on OpenAI o-models and ARC]]: Limitation identified: Transduction-based approaches systematically overfit to public evaluation sets; 
- **2025-01-07** — [[sources/01KJSWNT7B-agents|Agents]]: An agent is characterized by the environment it operates in and the set of actions it can perform.
- **2024-12-25** — [[sources/01KJVFQM7C-best-of-2024-in-agents-from-1-on-swe-bench-full-prof-graham-neubig-of-openhandsa|Best of 2024 in Agents (from #1 on SWE-Bench Full, Prof. Graham Neubig of OpenHands/AllHands)]]: Open Hands provides agents with the ability to call arbitrary Python code rather than a fixed set of
- **2024-12-06** — [[sources/01KJSXHZ75-how-i-came-in-first-on-arc-agi-pub-using-sonnet-35-with-evolutionary-test-time-c|How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute]]: ARC-AGI-Pub restricts internet-connected programs to the public leaderboard, making them ineligible 
- **2024-12-06** — [[sources/01KJV68FPF-smoothie-label-free-language-model-routing|Smoothie: Label Free Language Model Routing]]: SMOOTHIE does not consider cost tradeoffs between large and small models when routing, optimizing on
- **2024-12-05** — [[sources/01KJV5E1EB-arc-prize-2024-technical-report|ARC Prize 2024: Technical Report]]: The ARC-AGI benchmark remains unbeaten as of December 5, 2024, five years after its creation.
- **2024-11-22** — [[sources/01KJV6PJWC-tulu-3-pushing-frontiers-in-open-language-model-post-training|Tulu 3: Pushing Frontiers in Open Language Model Post-Training]]: Limitation identified: Many open model benchmark scores are systematically deflated by few-shot formatt
- **2024-11-11** — [[sources/01KKT4PNZT-the-surprising-effectiveness-of-test-time-training-for-few-shot-learning|The Surprising Effectiveness of Test-Time Training for Few-Shot Learning]]: TTT with an 8B-parameter LM achieves 61.9% accuracy on ARC when ensembled with program-synthesis met
- **2024-11-04** — [[sources/01KJV6C0D1-combining-induction-and-transduction-for-abstract-reasoning|Combining Induction and Transduction for Abstract Reasoning]]: The ensemble with GPT-4 descriptions achieves 26.50% validation accuracy compared to 19.50% with GPT
- **2024-10-19** — [[sources/01KJVMA9D5-gsm-symbolic-understanding-the-limitations-of-mathematical-reasoning-in-large-la|GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models]]: Limitation identified: Models achieve significantly higher accuracy on original GSM8K problems than on 
- **2024-10-09** — [[sources/01KJV7TRY2-pixtral-12b|Pixtral 12B]]: New capability: LLM-judged multimodal multi-turn instruction following benchmark (MM-MT-Bench) a
- **2024-10-08** — [[sources/01KJVK9P0T-no-priors-ep-85-ceo-of-braintrust-ankur-goyal|No Priors Ep. 85 | CEO of Braintrust Ankur Goyal]]: Breakthrough: LLM-based evaluation has become standard practice, enabling scalable and continu
- **2024-10-07** — [[sources/01KJV8271T-kgarevion-an-ai-agent-for-knowledge-intensive-biomedical-qa|KGARevion: An AI Agent for Knowledge-Intensive Biomedical QA]]: KGAREVION fine-tunes the LLM on a KG completion task using TransE structural embeddings as prefix to
- **2024-10-03** — [[sources/01KJVJSX48-stanford-ai-researcher-on-whats-next-in-research-reaction-to-o1-and-how-ai-will-|Stanford AI Researcher on What’s Next in Research, Reaction to o1 and How AI will Change Simulation]]: New capability: Language models as automatic benchmark generators: using LLMs to systematically 
- **2024-09-18** — [[sources/01KJV8DVH3-to-cot-or-not-to-cot-chain-of-thought-helps-mainly-on-math-and-symbolic-reasonin|To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning]]: Limitation identified: 95% of CoT's apparent gains on MMLU — one of the most-cited broad reasoning benc
- **2024-08-06** — [[sources/01KJSY403H-on-the-arc-agi-1-million-reasoning-challenge|On the “ARC-AGI” $1 Million Reasoning Challenge]]: Limitation identified: Greenblatt's reported scores of 71% (training) and 51% (public evaluation) are s
- **2024-06-27** — [[sources/01KJV3VT1C-colpali-efficient-document-retrieval-with-vision-language-models|ColPali: Efficient Document Retrieval with Vision Language Models]]: ColPali offline document indexing latency is 0.39 seconds per page, compared to 7.22 seconds for a P
- **2024-06-26** — [[sources/01KJVKC8GK-hallucination-free-assessing-the-reliability-of-leading-ai-legal-research-tools-|Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools (Paper Explained)]]: The paper was produced by researchers from Stanford and Yale evaluating leading commercial AI legal 
- **2024-06-17** — [[sources/01KJSYJP6K-getting-50-sota-on-arc-agi-with-gpt-4o|Getting 50% (SoTA) on ARC-AGI with GPT-4o]]: GPT-4o achieves 50% accuracy on the ARC-AGI public test set by generating approximately 8,000 Python
- **2024-01-25** — [[sources/01KJV9RNVZ-webvoyager-building-an-end-to-end-web-agent-with-large-multimodal-models|WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models]]: New capability: GPT-4V serving as reliable automatic evaluator for open-ended multimodal web age
