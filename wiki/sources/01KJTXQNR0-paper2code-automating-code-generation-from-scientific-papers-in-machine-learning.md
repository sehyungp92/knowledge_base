---
type: source
title: 'Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning'
source_id: 01KJTXQNR0JHH7MB6RQNMB8EYC
source_type: paper
authors:
- Minju Seo
- Jinheon Baek
- Seongyun Lee
- Sung Ju Hwang
published_at: '2025-04-24 00:00:00'
theme_ids:
- agent_systems
- benchmark_design
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- multi_agent_coordination
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning

**Authors:** Minju Seo, Jinheon Baek, Seongyun Lee, Sung Ju Hwang
**Published:** 2025-04-24 00:00:00
**Type:** paper

## Analysis

# Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning
2025-04-24 · paper · Minju Seo, Jinheon Baek, Seongyun Lee, Sung Ju Hwang
https://arxiv.org/pdf/2504.17192

---

### Motivation & Prior Limitations
Only ~19.5% of papers accepted to top-tier ML conferences in 2024 (ICLR, ICML, NeurIPS) release code implementations, creating a severe reproducibility bottleneck that forces researchers to manually reverse-engineer methods from prose descriptions — a process that is both time-consuming and error-prone.
- Prior LLM-based scientific automation systems (e.g., AI Scientist, MLAgentBench) sidestep this problem entirely by assuming access to pre-existing implementations or partial code scaffolds, making them inapplicable when no code exists.
  - This assumption is structurally flawed for real-world use: the papers with the most novel contributions are precisely those least likely to have released code.
- Naively prompting an LLM to generate an entire repository from a paper in a single pass fails due to the inherent complexity of scientific documents, long-context limitations of current models, and the difficulty of maintaining coherent cross-file dependencies and global architectural structure.
  - Papers are written to persuade human readers, not to specify software: they contain high-level motivation, persuasive narrative, and loosely structured algorithmic detail that is ambiguous from a software engineering perspective.
- Existing repository-level code generation frameworks (ChatDev, MetaGPT) follow a bottom-up strategy that expands short natural-language requirements via role-playing or SOPs — a mismatch for the long-form, loosely structured input of a scientific paper.

---

### Proposed Approach
PaperCoder is a multi-agent, multi-stage LLM framework that decomposes paper-to-repository code generation into three sequential stages — Planning, Analysis, and Coding — each handled by specialized agents that accumulate and propagate structured context forward through the pipeline.
- The **Planning** stage transforms the unstructured paper into four structured artifacts: (1) an overall plan identifying core components (model, training, evaluation, data); (2) an architecture design producing a file list, class diagram, and sequence diagram; (3) a logic design that establishes a dependency-ordered file list and per-file logic specifications; and (4) a config.yaml capturing hyperparameters and runtime settings.
  - The explicit execution order in the logic design phase is critical: without it, code generation can produce file B before file A when B imports from A, causing build failures — an issue confirmed in ablation when architecture design is added without logic design (scores drop).
- The **Analysis** stage iterates over each file identified during planning and generates a detailed per-file specification: functional goals, input/output behavior, intra- and inter-file dependencies, and algorithmic constraints derived from the paper.
- The **Coding** stage generates files sequentially in dependency order, conditioning each file on the full paper, all planning artifacts, the file's analysis, and all previously generated files — ensuring that each generated file has complete awareness of its upstream context.
- This top-down decomposition contrasts with ChatDev and MetaGPT's bottom-up role-playing approach, and with single-pass generation; it is designed specifically to handle the mismatch between scientific prose and software specification.

---

### Results & Capabilities
PaperCoder consistently outperforms all baselines on Paper2CodeBench (90 papers from ICLR, ICML, NeurIPS 2024) across both reference-based and reference-free evaluation, achieving scores of 3.68–3.83 (reference-based) and 4.73–4.77 (reference-free) on a 5-point Likert scale, compared to the next-best baseline (the one-shot "Paper" method) at 3.08–3.28 and 4.08–4.30.
- Reference-free evaluation (used when no ground-truth repository exists) is a reliable proxy for reference-based evaluation, with a Pearson correlation of r = 0.79, validating its use as a standalone metric at scale.
- In human evaluations conducted by original paper authors, 88% of PaperCoder repositories were ranked first among all compared systems, and 92% of human judges rated the generated repositories as helpful for reproduction — with completeness, clean structure, and faithfulness to the paper as the top-cited reasons for preference.
- On PaperBench Code-Dev (20 ICML 2024 papers with human-annotated rubrics), PaperCoder achieves replication scores of 45.1% (o3-mini-high) and 51.1% (Claude 3.5 Sonnet), substantially outperforming BasicAgent (5.1% / 35.4%) and IterativeAgent (16.4% / 27.5%).
- Generated repositories are near-executable: manual execution tests on five papers show that only an average of 0.81% of total code lines require modification (e.g., fixing deprecated APIs, correcting data type mismatches) to achieve successful execution.
- Model backbone quality is a critical factor: o3-mini-high substantially outperforms open-source alternatives (DS-Coder, Qwen-Coder, DS-Distill-Qwen), and the gap is large enough that framework design alone cannot compensate for a weak backbone.
- Augmenting the pipeline with Self-Refine-style verification at the planning and analysis stages yields measurable downstream gains, with config file quality improving by +1.00 and architecture design by +0.76 points, and final code quality improving by +0.50.
- Papers accepted as oral/spotlight presentations generate slightly higher-quality implementations than poster papers (3.72–3.88 vs. 2.83–2.87 by model evaluation), suggesting that clearer scientific writing correlates with more faithful code generation.

---

### Implications
PaperCoder demonstrates that repository-level code generation from scientific prose is a tractable problem when approached with structured multi-agent decomposition, which has direct implications for accelerating the

## Key Claims

1. Only approximately 19.5% of papers accepted to top-tier machine learning conferences in 2024 provide their code implementations.
2. Generating a complete, modular, and faithful code repository in a single LLM pass is extremely challenging due to paper complexity, long-context limitations, and difficulty maintaining cross-file depe
3. PaperCoder uses a top-down approach (planning → analysis → coding) that outperforms bottom-up approaches used by prior multi-agent software development frameworks.
4. 88% of repositories generated by PaperCoder are rated as best over all baselines in human evaluation.
5. 92% of human judges report that PaperCoder-generated repositories are helpful for reproducing the original work.
6. PaperCoder-generated codebases can be executed with only minor modifications, averaging 0.81% of total code lines changed.
7. PaperCoder achieves a replication score of 45.14% (±0.3) on PaperBench Code-Dev with o3-mini-high, compared to 5.1% for BasicAgent and 16.4% for IterativeAgent.
8. Reference-free evaluation (using only the paper) is a reliable proxy for reference-based evaluation, with a Pearson correlation coefficient of r=0.79 between them.
9. Adding architecture design alone to the pipeline causes a performance drop because it does not specify execution order, leading to confusion during code generation; logic design resolves this.
10. Integrating all pipeline modules (overall plan, architecture design, logic design, configuration generation, and analysis) yields the highest performance, confirming the effectiveness of the fully str

## Capabilities

- Multi-agent LLM frameworks can automatically generate operational code repositories directly from ML research papers without any pre-existing code, skeleton implementations, or APIs — achieving 88% best-ranking rate and 92% expert helpfulness rating
- Structured planning→analysis→coding multi-agent decomposition enables repository-level code generation that is near-executable with only 0.81% of lines requiring minor modification for successful execution
- LLM-powered multi-agent pipelines can generate multi-file repositories with coherent architectural design, class/sequence diagrams, file dependency ordering, and configuration files from unstructured scientific text
- Self-refinement applied to intermediate planning and analysis outputs measurably improves downstream code generation quality — configuration file quality improves by +1.00 on a 5-point scale, architecture design by +0.76
- LLM-based reference-free evaluation of code repositories (without ground-truth implementations) achieves Pearson r=0.79 correlation with reference-based evaluation and r=0.78 rank correlation with human expert judgment

## Limitations

- Generated code repositories are dramatically less complete than author-released implementations — PaperCoder produces ~14K tokens, 7 files, 35 functions versus author releases averaging 32K tokens, 28 files, 122 functions
- Paper-to-code generation fails most on data processing components — papers systematically under-specify data formats, preprocessing steps, and loading procedures, making this the primary source of implementation errors
- Performance degrades sharply with weaker backbone models — open-source models score 1.47–2.05 on reference-based evaluation versus 3.66 for o3-mini-high, making the approach practically unusable without frontier-class reasoning models
- Even best-in-class paper-to-code generation achieves only 45–51% replication score on PaperBench — more than half of paper results cannot be fully replicated from generated code alone
- The system is constrained to papers with repositories under 70,000 tokens — large research codebases are excluded, biasing evaluation toward simpler implementations and limiting applicability to complex ML systems
- Architecture design planning alone (without execution ordering) actively degrades code generation quality — structural knowledge without sequencing information causes cross-file dependency confusion
- Single-pass (one-shot) code generation from full papers produces substantially worse results than structured multi-stage pipelines — confirming that LLMs cannot maintain global coherence across repository-scale generation in a single context
- Code quality correlates with paper presentation quality — oral/spotlight papers produce measurably better implementations than poster papers, meaning generated code inherits systematic quality gaps from underspecified research writing
- No safeguards exist for reproducing security-sensitive research (jailbreaking, exploitation techniques) — the ethics statement acknowledges the risk but defers mitigation to production deployment as future work
- The approach is only evaluated on ML papers from three top venues (ICLR, ICML, NeurIPS) — generalizability to other scientific domains (biology, physics, chemistry) with different writing conventions and code structures is entirely untested
- Only ~19.5% of accepted papers at top ML conferences in 2024 provide code implementations — the vast majority of published research remains inaccessible for direct reproduction

## Bottlenecks

- ML research reproducibility is blocked by a structural code availability gap — only ~19.5% of accepted top-tier ML papers release implementations, forcing researchers to manually reverse-engineer methods and slowing scientific velocity
- Single-pass LLM generation is insufficient for repository-level code — context limitations and global coherence requirements mean complex multi-file repositories cannot be generated without structured decomposition, blocking naive automation of paper-to-code workflows
- Scientific papers are written as human communication artifacts rather than engineering specifications — systematic under-specification of data processing, implementation details, and experimental configurations creates an irreducible information gap that blocks fully automated reproduction

## Breakthroughs

- Structured multi-stage multi-agent decomposition (planning→analysis→coding) makes faithful paper-to-code generation feasible for the first time — PaperCoder achieves 45–51% replication scores and 92% expert helpfulness rating where prior systems achieved 5–16%

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/self-refine|Self-Refine]]
