---
type: theme
title: AI for Scientific Discovery
theme_id: ai_for_scientific_discovery
level: 2
parent_theme: scientific_and_medical_ai
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 16
sources_since_update: 0
update_count: 1
velocity: 0.388
staleness: 0.0
status: active
tags: []
---
# AI for Scientific Discovery

> AI for Scientific Discovery is bifurcating into two structurally distinct trajectories: a genomics branch demonstrating remarkable generative capability — encoding arbitrary regulatory patterns into DNA via inference-time search — but blocked at the wet-lab validation wall, and a computational optimization branch (exemplified by AlphaEvolve) that has crossed into narrow production but remains confined to domains with automated scoring functions. Momentum is building in silicon-native substrates while stalling at the interface between computational and experimental science, and the keystone bottleneck is the absence of machine-executable evaluation oracles for wet domains.

**Parent:** [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]

## Current State

The field moved in two waves. Early 2025 brought the more conceptually radical shift: Evo 2 demonstrated that genomic foundation models could cross from sequence *prediction* to sequence *design with intent*. The breakthrough was not the model itself but the combination of inference-time beam search guided by Enformer/Borzoi epigenomic oracle ensembles — a pipeline that encodes arbitrary regulatory patterns (square waves, Morse code chromatin peaks) into DNA sequence. This constituted generative epigenomics as a new discipline, not an incremental improvement on prior gradient-based or screening-based approaches.

The wall it immediately encountered was physical, not computational. No established wet-lab pipeline exists for validating AI-designed sequences at whole-chromosome or synthetic-genome scale. The scoring oracle — Enformer and Borzoi predictions — has unknown reliability for sequences far outside its training distribution, meaning the most striking demonstrations rest on unvalidated computational proxies. The gap between what can be generated and what can be confirmed is the defining constraint of this branch.

Mid-2025 brought a different kind of result with AlphaEvolve: LLM-guided evolution reducing expert kernel engineering time from months to days and outperforming expert-designed tiling heuristics by 23%. This was a genuine narrow-production deployment rather than a research demonstration — but its architecture made the ceiling explicit. AlphaEvolve requires automated evaluation metrics; biology, chemistry, and most of natural science remain structurally out of reach not because the generative capability is insufficient, but because the evaluation infrastructure does not exist. You cannot evolve solutions to experiments you cannot score.

The result is a bifurcated momentum profile. Computational substrates — hardware design, algorithm optimization, mathematical reasoning — are iterating rapidly under AlphaEvolve-style systems. Experimental natural science is structurally stalled. The resolution pathway is visible: simulation environments (molecular dynamics pipelines, protein folding sandboxes, synthetic biology platforms) maturing into reliable automated evaluation oracles. Whether that happens on a 1-2 year or 3-5 year horizon is the open empirical question that will determine when evolutionary AI discovery enters wet science.

## Capabilities

- **Whole-genome sequence generation** — Evo 2 can generate novel whole-genome sequences for organisms including mitochondrial genomes. *(maturity: research_only)*
- **Programmable epigenomic design** — Inference-time beam search guided by Enformer/Borzoi epigenomic predictors enables Evo 2 to generate DNA sequences with targeted chromatin accessibility profiles, including encoding arbitrary spatial patterns (square waves, Morse code peaks) at base-pair resolution. *(maturity: research_only)*
- **LLM-guided hardware kernel optimization** — Evolutionary coding agents reduce expert kernel engineering time from months to days for hardware-accelerator tiling heuristics, outperforming expert-designed solutions by 23%. *(maturity: narrow_production)*
- **Hardware RTL design simplification** — Evolutionary agents apply to RTL design, finding simplifications in Verilog circuit implementations. *(maturity: demo)*

## Limitations

- **Automated evaluation requirement** — AlphaEvolve is fundamentally limited to problems with automated evaluation metrics; it cannot address domains where experiments require physical execution or expert judgment. *(severity: significant, trajectory: improving)*
- **Unvalidated epigenomic predictions** — Epigenomic design validation relies entirely on Enformer/Borzoi model predictions rather than experimental chromatin accessibility assays; the reliability of these oracles for sequences far outside training distribution is unknown. *(severity: significant, trajectory: unclear)*
- **Compute cost of beam search** — Generative epigenomics beam search requires running Enformer (196,608 bp input) and a 4-replicate Borzoi ensemble (524,288 bp input) at each step; this is prohibitive for long sequences or production workflows. *(severity: significant, trajectory: improving)*
- **Evaluation cost ceiling** — AlphaEvolve evaluation costs can reach ~100 compute-hours per solution, limiting throughput and making the system infeasible for applications requiring rapid iteration. *(severity: significant, trajectory: stable)*
- **Abstraction-level sensitivity** — The choice of abstraction level (evolving solution directly vs. constructor function vs. search algorithm) significantly affects results; this is an implicit design parameter with no automated selection mechanism. *(severity: significant, trajectory: stable)*
- **LLM quality evaluation immaturity** — LLM-provided evaluation of solution quality for non-computable properties (e.g., simplicity) is a secondary mechanism not yet optimized. *(severity: significant, trajectory: improving)*
- **Natural language hypothesis scope gap** — AlphaEvolve's applicability to natural language–described scientific hypotheses rather than code is unexplored and out of scope for current deployments. *(severity: significant, trajectory: improving)*
- **Preprint status** — Evo 2 results are from a preprint not yet certified by peer review; all benchmarks and zero-shot capability claims are provisional. *(severity: minor, trajectory: improving)*

## Bottlenecks

- **Wet-lab validation pipeline** — No established pipeline exists for validating AI-designed large-scale genomic sequences (whole chromosomes, synthetic genomes) in the laboratory. Blocking: therapeutic and research applications of generative genomics; synthetic biology at the chromosome scale. *(status: active, horizon: 1-2 years)*
- **Automated evaluation oracles for experimental science** — The absence of machine-executable evaluation functions for natural science domains (chemistry, biology, physics) is the structural barrier preventing AlphaEvolve-style systems from entering wet science. Blocking: AI-driven scientific discovery expanding from mathematics and computer science into experimental natural sciences. *(status: active, horizon: 3-5 years)*
- **Inference-time compute scaling** — Compute cost of beam search for genomic sequence design is prohibitive for long sequences or iterative laboratory workflows. Blocking: deploying generative genomic design at practical scales (whole chromosomes, large regulatory regions). *(status: active, horizon: 1-2 years)*

## Breakthroughs

- **Programmable epigenome design via beam search** — Evo 2 with inference-time beam search guidance demonstrates the ability to encode arbitrary spatial chromatin accessibility patterns into DNA sequence. *Prior belief: designing DNA sequences to produce precise, programmable chromatin accessibility patterns was an unsolved challenge — no system could reliably encode arbitrary patterns (e.g., alternating open/closed regions at bp resolution) into DNA sequence.* *(significance: major)*
- **Generative epigenomics pipeline** — Beam search guided by Evo 2 + Enformer/Borzoi ensemble enables end-to-end LLM-guided design of regulatory sequences. *Prior belief: designing synthetic DNA sequences with targeted epigenomic properties required either expert-designed rules, high-throughput experimental screening (SELEX, MPRA), or gradient-based methods on non-generative models.* *(significance: notable)*

## Anticipations

- Whether simulation environments (molecular dynamics, protein folding pipelines, synthetic biology sandboxes) mature into reliable automated evaluation oracles within 1-2 years is the keystone signal: it would unlock evolutionary AI discovery in experimental natural science a full cycle earlier than the 3-5 year structural estimate.
- Resolution of the Evo 2 preprint through peer review will either confirm or qualify the zero-shot generative claims that currently anchor the genomics trajectory.

## Cross-Theme Implications

- ← **reasoning_and_cognitive_architectures**: External expert validation that frontier reasoning models (e.g., o3) can generate and critically evaluate novel hypotheses in biology, math, and engineering — rather than just retrieving or summarizing — raises the possibility of AI as a genuine collaborative thought partner in research. This accelerates timelines for AI-assisted hypothesis generation workflows and strengthens the case that the bottleneck in scientific AI is evaluation infrastructure, not hypothesis generation.
- → **hardware_and_compute**: AlphaEvolve's narrow-production results in kernel engineering and RTL design demonstrate that AI-driven optimization of the compute stack itself is viable today — creating a potential feedback loop where AI-optimized hardware accelerates the AI systems doing the optimizing.
- → **synthetic_biology**: Generative epigenomics, if wet-lab validation pipelines mature, would transform synthetic biology from a combinatorial screening discipline into a design discipline — fundamentally altering how regulatory circuits are constructed.

## Contradictions

- AlphaEvolve is presented as a scientific discovery system, yet its hard architectural requirement for automated evaluation metrics structurally excludes most of natural science. The framing as "AI for science" sits in tension with a deployment reality confined to algorithm and hardware domains — areas better characterized as engineering optimization than scientific discovery.
- The most dramatic Evo 2 results (programmable chromatin accessibility patterns) are validated entirely by the same class of model used to guide generation (Enformer/Borzoi). This circularity — oracle-guided design evaluated by oracle prediction — means the claimed breakthrough is currently unfalsifiable within the computational pipeline alone.

## Research Opportunities

- Developing lightweight, fast epigenomic proxy models suitable for iterative beam search at chromosome scale — reducing the per-step cost from hundreds of compute-hours to something compatible with exploratory design workflows.
- Building standardized wet-lab assay pipelines (ATAC-seq, Hi-C, synthetic genome assembly) specifically designed to validate AI-generated sequence designs, creating a feedback loop between computational generation and experimental confirmation.
- Investigating whether AlphaEvolve-style evolutionary agents can operate over molecular simulation outputs (e.g., MD trajectories, docking scores) as automated evaluation proxies — the bridging experiment that would test whether simulation fidelity is sufficient to substitute for physical evaluation.
- Exploring abstraction-level selection strategies for evolutionary agents: whether meta-learning or automated curriculum methods can remove the implicit design parameter that currently requires human judgment.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 16 sources.
- **2026-02-14** — [[sources/01KJVPHM2Z-the-100x-ai-breakthrough-no-one-is-talking-about|The 100x AI Breakthrough No One is Talking About]]: Deep Think is not a separate model but a reasoning mode within Gemini 3 that allocates additional co
- **2026-02-11** — [[sources/01KJRZT83A-gemini-deep-think-redefining-the-future-of-scientific-research|Gemini Deep Think: Redefining the Future of Scientific Research]]: Aletheia performed a semi-autonomous evaluation of 700 open problems on Bloom's Erdős Conjectures da
- **2026-01-22** — [[sources/01KJT1PH9D-learning-to-discover-at-test-time|Learning to Discover at Test Time]]: TTT-Discover achieves a score of 567,062 on the AtCoder Heuristic Contest 39, slightly surpassing th
- **2025-10-15** — [[sources/01KJS27HS4-how-a-gemma-model-helped-discover-a-new-potential-cancer-therapy-pathway|How a Gemma model helped discover a new potential cancer therapy pathway]]: Biological foundation models follow clear scaling laws analogous to natural language models — larger
- **2025-07-24** — [[sources/01KJVJ6D0C-math-olympiad-gold-medalist-explains-openai-and-google-deepmind-imo-gold-perform|⚡️Math Olympiad gold medalist explains OpenAI and Google DeepMind IMO Gold Performances]]: Neither DeepMind nor OpenAI used Lean or other formal verification languages for the 2025 IMO; both 
- **2025-06-27** — [[sources/01KJTP7WMB-the-automated-llm-speedrunning-benchmark-reproducing-nanogpt-improvements|The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements]]: All tested AI agents fail to recover more than 20% of the speedup achieved by human solutions when g
- **2025-06-17** — [[sources/01KKT490MT-alphaevolve-a-coding-agent-for-scientific-and|AlphaEvolve: A coding agent for scientific and]]: New capability: LLM-guided evolution reduces expert kernel engineering time from months to days 
- **2025-04-29** — [[sources/01KJVP1SYG-the-quest-to-solve-all-diseases-with-ai-isomorphic-labs-max-jaderberg|The Quest to ‘Solve All Diseases’ with AI: Isomorphic Labs’ Max Jaderberg]]: Reinforcement learning differs from supervised learning in that it does not require knowing the corr
- **2025-04-15** — [[sources/01KJVNVKAH-arc-institutes-patrick-hsu-on-building-an-app-store-for-biology-with-ai|Arc Institute's Patrick Hsu on Building an App Store for Biology with AI]]: EVO2 is an auto-regressive multiconvolutional hybrid model trained on genomic sequences
- **2025-04-10** — [[sources/01KJV0GSYV-the-ai-scientist-v2-workshop-level-automated-scientific-discovery-via-agentic-tr|The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search]]: The AI Scientist-v2 produced the first entirely AI-generated manuscript to successfully pass a peer-
- **2025-02-25** — [[sources/01KJVNYSCT-no-priors-ep-103-with-vevo-therapeutics-and-the-arc-institute|No Priors Ep. 103 | With Vevo Therapeutics and the Arc Institute]]: There is currently no accepted benchmark for evaluating virtual cell model quality.
- **2024-08-12** — [[sources/01KJV8RNT6-the-ai-scientist-towards-fully-automated-open-ended-scientific-discovery|The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery]]: The AI Scientist can produce a full research paper at a cost of less than $15 per paper.
- **2024-08-01** — [[sources/01KJVNQMNS-ai-in-pharmaceutical-rd-with-kim-branson|AI in Pharmaceutical R&D with Kim Branson]]: GSK uses machine learning on clinical imaging to derive continuous quantitative traits (e.g., degree
- **2024-06-12** — [[sources/01KJVRC3JX-investing-in-ai-for-hard-tech-with-eric-vishria-of-benchmark-and-sergiy-nesteren|Investing in AI for Hard Tech, with Eric Vishria of Benchmark and Sergiy Nesterenko of Quilter]]: Benchmark has not invested in any foundation model companies.
- **2024-04-30** — [[sources/01KJV95THR-kan-kolmogorov-arnold-networks|KAN: Kolmogorov-Arnold Networks]]: KANs can be made increasingly more accurate via grid extension — fitting a fine-grained spline to th
- **2024-01-21** — [[sources/01KJVMD0J9-alphageometry-solving-olympiad-geometry-without-human-demonstrations-paper-expla|AlphaGeometry: Solving olympiad geometry without human demonstrations (Paper Explained)]]: AlphaGeometry is trained entirely without human demonstrations as training data, relying instead on
