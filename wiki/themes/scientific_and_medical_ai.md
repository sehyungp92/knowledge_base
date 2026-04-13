---
type: theme
title: Scientific & Medical AI
theme_id: scientific_and_medical_ai
level: 1
parent_theme: reasoning_and_planning
child_themes:
- ai_for_scientific_discovery
- medical_and_biology_ai
created: '2026-04-08'
updated: '2026-04-08'
source_count: 28
sources_since_update: 0
update_count: 1
velocity: 0.107
staleness: 0.0
status: active
tags: []
---
# Scientific & Medical AI

> Scientific & Medical AI has moved decisively past its first act — proving that deep learning can match human experts on narrow diagnostic tasks — and is now grappling with the harder, more consequential problem of designing biological systems from scratch. The field's trajectory bends toward generative biology, but is currently blocked by a methodological gap: there is no established way to trade inference-time compute for higher-quality biological designs, the same lever that made language models transformative. Until that gap closes, the most ambitious applications — epigenomic control, multi-gene circuit design, cell-type-specific regulatory engineering — remain pre-paradigmatic, even as discriminative capabilities (classification, structure prediction) continue to mature rapidly.

**Parent:** [[themes/reasoning_and_planning|Reasoning & Planning]]
**Sub-themes:** [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]], [[themes/medical_and_biology_ai|Medical & Biology AI]]

## Current State

The current moment in Scientific & Medical AI is best understood as an asymmetry: discriminative AI has largely delivered on its early promises, while generative AI for biology is accumulating capability claims faster than validated methodology.

The discriminative half of the curve — classifying diseases, predicting protein structures, flagging anomalies in medical imaging — saw its landmark consolidation with AlphaFold-class results, which demonstrated that seemingly intractable biological prediction problems could yield to scale and architecture. That success raised the field's ambitions and, critically, raised its expectations for the design direction. If prediction was solvable, design should follow. But prediction and design are asymmetric problems. Predicting the structure of a given sequence is a constrained inference task; designing a sequence with specified multi-property behavior is an open-ended search over a combinatorial space with sparse, delayed feedback.

By early 2025, this asymmetry had crystallized into a concrete methodological bottleneck: the field knows how to train foundation models on biological sequences, but it does not know how to systematically improve design quality by allocating more compute at inference time. In language models, techniques like chain-of-thought reasoning, beam search, and RLHF gave practitioners a handle on quality — a way to steer outputs without retraining. Biology lacks an equivalent. The result is that biological design models can produce outputs, but practitioners have limited levers to improve them on demand.

The research frontier is now actively probing whether beam search, diffusion guidance, or iterative refinement can serve as biological analogs to chain-of-thought. The first validated demonstration that a design task — particularly multi-property regulatory sequence engineering — shows consistent quality improvement with increased inference compute would likely trigger rapid methodology consolidation, analogous to what RLHF did for language alignment: not a new capability, but a new handle on an existing one that makes the whole system steerable.

## Capabilities

*(Coverage in the source library is currently thin for this section — the field's documented advances are concentrated in discriminative tasks. Generative design capabilities are claimed but methodologically unvalidated at scale.)*

The established capability tier includes narrow diagnostic matching (medical imaging classification, pathology detection), biological sequence prediction (structure, function annotation), and single-property sequence generation under constrained conditions. AlphaFold-class models represent the ceiling of what discriminative AI has achieved: near-human or superhuman accuracy on well-defined prediction benchmarks, trained on large curated datasets with clear ground truth.

Generative capabilities — designing sequences with specified properties — exist as demonstrated proofs of concept but have not yet shown reliable multi-property control or consistent quality improvement with additional compute.

## Limitations

The most structurally significant limitation is the absence of inference-time scaling methodology for biological sequence design. Unlike language models, where practitioners can trade compute for quality through techniques like chain-of-thought prompting or beam search, biological design models offer no equivalent handle. This is not a training data problem or a model architecture problem in isolation — it is a methodology problem: the field lacks validated protocols for systematically improving design outputs without full retraining.

Secondary limitations follow from this:

- **Multi-property control**: Designing sequences that simultaneously satisfy multiple biological constraints (e.g., expression level, cell-type specificity, chromatin accessibility) remains unsolved at scale.
- **Feedback sparsity**: Biological validation is slow and expensive, which limits the iterative refinement loops that make AI systems steerable.
- **Distribution shift**: Models trained on known biological sequences may not generalize reliably to novel design regimes that fall outside evolutionary precedent.
- **Validated vs. claimed**: The gap between what models claim to design and what wet-lab validation confirms is poorly characterized across the field.

## Bottlenecks

**No established methodology for inference-time scaling in biological sequence design** — *Active, blocking, 1–2 year resolution horizon*

The field has no validated approach for trading inference-time compute for improved biological design quality. This is structurally analogous to the pre-RLHF state of language model alignment: models could generate outputs, but practitioners lacked systematic levers to steer them toward higher quality without retraining.

This bottleneck is directly blocking the most consequential generative applications:
- **Epigenomic control**: Designing sequences that predictably reshape the epigenetic landscape of a cell
- **Multi-gene circuit design**: Engineering regulatory logic across multiple interacting genes
- **Cell-type-specific regulatory sequence engineering**: Designing enhancers or promoters that activate in a specified cell type and not others

These targets represent the difference between reading biology and writing it. Resolution will likely require adapting techniques from the LLM scaling playbook — beam search, diffusion guidance, iterative refinement with biological reward signals — to the sequence design setting, with experimental validation demonstrating reliable quality-compute tradeoffs.

## Breakthroughs

*(No breakthroughs recorded in current source coverage. AlphaFold-class results, while paradigm-shifting for protein structure prediction, predate the current snapshot's primary coverage window. Watch this section for updates as the inference-time scaling question resolves.)*

## Anticipations

- **First validated inference-time scaling result for biological design**: A demonstration that a design task — particularly multi-property regulatory sequence engineering — shows consistent, measurable quality improvement as inference compute increases. This result would likely trigger rapid methodology consolidation across the field.
- **Methodology consolidation analogous to RLHF**: Once an inference-time scaling handle exists for biological design, expect fast convergence on a small set of dominant protocols, narrowing the current fragmentation of approaches.
- **Capability inversion**: As generative methodology matures, the field's center of gravity may shift from discriminative (classifying known biology) to generative (specifying new biology), changing which benchmarks and evaluation frameworks matter.

## Cross-Theme Implications

- **[[themes/reasoning_and_planning|Reasoning & Planning]]**: The inference-time scaling bottleneck in biological design is a domain-specific instance of a general problem — how to make AI systems reason more effectively with more compute. Advances in chain-of-thought, process reward models, and search-guided generation in the LLM context are directly relevant to biological design. The relationship is bidirectional: biological design may surface novel evaluation regimes for reasoning quality where ground truth is expensive, sparse, and delayed.
- **[[themes/ai_for_scientific_discovery|AI for Scientific Discovery]]**: The discriminative-to-generative transition in biology is a leading indicator for AI-driven discovery more broadly. The methodology gaps that have appeared here — multi-property optimization, feedback sparsity, validation lag — will recur in chemistry, materials science, and drug design as those fields reach the same inflection point.
- **[[themes/medical_and_biology_ai|Medical & Biology AI]]**: Clinical applications remain predominantly discriminative (diagnostics, triage, risk stratification), insulated from the generative bottleneck in the near term. But the long arc of the field converges: the most impactful medical AI applications (personalized therapeutics, gene therapy design, synthetic biology for treatment) depend on solving the design problem.

## Contradictions

- **Capability claims vs. validated methodology**: The field produces frequent reports of generative design successes, but the absence of established inference-time scaling methodology suggests many of these results are single-instance demonstrations rather than evidence of reliable, generalizable design capability. The gap between claimed and validated performance is poorly characterized.
- **AlphaFold expectations vs. design asymmetry**: AlphaFold's success created a narrative that biological AI is solving its hardest problems. But prediction and design are not symmetric — and the current bottleneck suggests the design half of the curve may be structurally harder, not just further behind on the same trajectory.

## Research Opportunities

- **Biological analogs to chain-of-thought**: Systematic investigation of whether beam search, diffusion guidance, or iterative refinement with biological reward signals can produce reliable quality-compute tradeoffs in sequence design. The highest-value experiment is one that demonstrates consistent improvement across multiple design targets, not a single showcase result.
- **Process reward models for biology**: In LLMs, process reward models that score intermediate reasoning steps enabled better search. Biology needs analogous intermediate signals — partial sequence evaluations, predicted folding checkpoints, simulated expression proxies — that can guide generation without full wet-lab validation.
- **Multi-property benchmark construction**: The field lacks agreed-upon benchmarks for multi-property biological design. Building these — with clear ground truth, measurable properties, and scalable validation — would allow the inference-time scaling question to be answered rigorously.
- **Feedback loop compression**: Reducing the time and cost of biological validation (through organoids, high-throughput assays, or computational proxies) directly expands the design iteration budget, which is the underlying resource constraint that makes inference-time scaling matter.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 28 sources.
- **2026-02-14** — [[sources/01KJVPHM2Z-the-100x-ai-breakthrough-no-one-is-talking-about|The 100x AI Breakthrough No One is Talking About]]: Google DeepMind explicitly states that its results should not be interpreted as AI being able to con
- **2026-02-11** — [[sources/01KJRZT83A-gemini-deep-think-redefining-the-future-of-scientific-research|Gemini Deep Think: Redefining the Future of Scientific Research]]: Google built a math research agent internally codenamed Aletheia, powered by Gemini Deep Think mode,
- **2026-01-22** — [[sources/01KJT1PH9D-learning-to-discover-at-test-time|Learning to Discover at Test Time]]: All TTT-Discover results are achieved with an open model (OpenAI gpt-oss-120b), in contrast to previ
- **2025-10-15** — [[sources/01KJS27HS4-how-a-gemma-model-helped-discover-a-new-potential-cancer-therapy-pathway|How a Gemma model helped discover a new potential cancer therapy pathway]]: Inhibiting CK2 via silmitasertib had not previously been reported in the literature to explicitly en
- **2025-09-17** — [[sources/01KJTHM1GB-compute-as-teacher-turning-inference-compute-into-reference-free-supervision|Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision]]: The CaT framework has two components: reference estimation that aggregates rollouts into a pseudo-re
- **2025-07-24** — [[sources/01KJVJ6D0C-math-olympiad-gold-medalist-explains-openai-and-google-deepmind-imo-gold-perform|⚡️Math Olympiad gold medalist explains OpenAI and Google DeepMind IMO Gold Performances]]: Neither DeepMind nor OpenAI used Lean or other formal verification languages for the 2025 IMO; both 
- **2025-07-23** — [[sources/01KJTN3N0M-rubrics-as-rewards-reinforcement-learning-beyond-verifiable-domains|Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains]]: RaR achieves relative improvements of up to 7% on GPQA-Diamond over LLM-as-judge baselines using Lik
- **2025-06-27** — [[sources/01KJTP7WMB-the-automated-llm-speedrunning-benchmark-reproducing-nanogpt-improvements|The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements]]: Recent reasoning LLMs combined with state-of-the-art scaffolds struggle to reimplement already-known
- **2025-06-17** — [[sources/01KKT490MT-alphaevolve-a-coding-agent-for-scientific-and|AlphaEvolve: A coding agent for scientific and]]: AlphaEvolve discovered open mathematical problems were suggested by external mathematicians Terence 
- **2025-05-13** — [[sources/01KKT4EFFY-healthbench-evaluating-large-language-models|HealthBench: Evaluating Large Language Models]]: HealthBench has low overall score variability across repeated runs, with a standard deviation of app
- **2025-05-06** — [[sources/01KKT4FGMX-2025-5-6|2025-5-6]]: AMIE was evaluated against 19 board-certified PCPs with a median post-residency experience of 6 year
- **2025-04-29** — [[sources/01KJVP1SYG-the-quest-to-solve-all-diseases-with-ai-isomorphic-labs-max-jaderberg|The Quest to ‘Solve All Diseases’ with AI: Isomorphic Labs’ Max Jaderberg]]: Isomorphic Labs aims to build a general drug design engine applicable to any target or disease area,
- **2025-04-15** — [[sources/01KJVNVKAH-arc-institutes-patrick-hsu-on-building-an-app-store-for-biology-with-ai|Arc Institute's Patrick Hsu on Building an App Store for Biology with AI]]: EVO2 is an auto-regressive multiconvolutional hybrid model trained on genomic sequences
- **2025-04-10** — [[sources/01KJV0GSYV-the-ai-scientist-v2-workshop-level-automated-scientific-discovery-via-agentic-tr|The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search]]: The AI Scientist-v2 produced the first entirely AI-generated manuscript to successfully pass a peer-
- **2025-04-10** — [[sources/01KJVFZ54E-new-in-nature-google-agents-beat-human-doctors-make-scientific-discoveries-with-|New in Nature: Google Agents Beat Human Doctors, Make Scientific Discoveries – With Vivek and Anil]]: Co-scientist's top hypothesis for the mechanism of bacterial drug resistance exactly matched an expe
- **2025-03-08** — [[sources/01KJVBPHHT-towards-conversational-ai-for-disease-management|Towards Conversational AI for Disease Management]]: The clinical guideline corpus totals 10.5 million tokens across 627 documents, exceeding Gemini's tw
- **2025-02-25** — [[sources/01KJVNYSCT-no-priors-ep-103-with-vevo-therapeutics-and-the-arc-institute|No Priors Ep. 103 | With Vevo Therapeutics and the Arc Institute]]: Vivo's Mosaic platform enables simultaneous drug screening across cells pooled from many cancer pati
- **2025-02-19** — [[sources/01KKT5HWA5-genome-modeling-and-design|Genome modeling and design]]: A novel needle-in-haystack evaluation for DNA language models was developed, using categorical Jacob
- **2024-10-07** — [[sources/01KJV8271T-kgarevion-an-ai-agent-for-knowledge-intensive-biomedical-qa|KGARevion: An AI Agent for Knowledge-Intensive Biomedical QA]]: KGAREVION fine-tunes the LLM on a KG completion task using TransE structural embeddings as prefix to
- **2024-10-03** — [[sources/01KJVNQNBD-ai-at-the-intersection-of-bio-vijay-pande-surya-ganguli-bowen-liu|AI at the Intersection of Bio | Vijay Pande, Surya Ganguli & Bowen Liu]]: ChatGPT demonstrated capabilities that were entirely unpredicted, marking a qualitative shift in AI
- **2024-09-05** — [[sources/01KJVNKY66-implementation-data-impact-of-healthcare-ai-with-julie-and-vijay|Implementation, Data, Impact of Healthcare AI with Julie and Vijay]]: Lung cancer is not a single disease but seven distinct types with different genomic signatures that 
- **2024-08-23** — [[sources/01KJVQ9TRD-josh-wolfe-lux-capital-predictions-on-emerging-technologies-ai-and-the-future-of|Josh Wolfe (Lux Capital): Predictions on Emerging Technologies, AI, and the Future of VC]]: Lux Capital has no aspiration to go public.
- **2024-08-12** — [[sources/01KJV8RNT6-the-ai-scientist-towards-fully-automated-open-ended-scientific-discovery|The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery]]: The AI Scientist produces each paper at a cost of less than $15.
- **2024-08-01** — [[sources/01KJVNQMNS-ai-in-pharmaceutical-rd-with-kim-branson|AI in Pharmaceutical R&D with Kim Branson]]: GSK uses machine learning methods in production to predict the directionality of genetic variants (w
- **2024-06-28** — [[sources/01KJVNGK3M-grand-challenges-in-healthcare-ai-with-vijay-pande-and-julie-yoo|Grand Challenges in Healthcare AI with Vijay Pande and Julie Yoo]]: The healthcare industry is currently experiencing a labor crisis with shortages of highly specialize
- **2024-06-12** — [[sources/01KJVRC3JX-investing-in-ai-for-hard-tech-with-eric-vishria-of-benchmark-and-sergiy-nesteren|Investing in AI for Hard Tech, with Eric Vishria of Benchmark and Sergiy Nesterenko of Quilter]]: Benchmark has not invested in any foundation model companies.
- **2024-04-30** — [[sources/01KJV95THR-kan-kolmogorov-arnold-networks|KAN: Kolmogorov-Arnold Networks]]: The original Kolmogorov-Arnold representation theorem corresponds to a 2-layer KAN with shape [n, 2n
- **2024-01-21** — [[sources/01KJVMD0J9-alphageometry-solving-olympiad-geometry-without-human-demonstrations-paper-expla|AlphaGeometry: Solving olympiad geometry without human demonstrations (Paper Explained)]]: AlphaGeometry is a neuro-symbolic system that combines trained language models with symbolic solvers
