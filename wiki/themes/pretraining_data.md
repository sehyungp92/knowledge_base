---
type: theme
title: Pretraining Data
theme_id: pretraining_data
level: 2
parent_theme: pretraining_and_scaling
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 18
sources_since_update: 0
update_count: 1
velocity: 0.0
staleness: 0.0
status: active
tags: []
---
```markdown
# Pretraining Data

> Pretraining data has moved from an abundant resource into the field's most intractable structural constraint, and the community is now visibly pivoting from scaling raw volume to extracting more signal from what already exists. The bottleneck is no longer treated as a fundamental ceiling but as a 3–5 year engineering problem, contingent on synthetic and interaction-derived alternatives proving out — yet underneath the engineering challenges lies a harder epistemological constraint: synthetic data inherits the ceiling of human knowledge as its reference distribution.

**Parent:** [[themes/pretraining_and_scaling|pretraining_and_scaling]]

## Current State

The arc of pretraining data research began with a simple assumption: more internet text produces better models. That assumption held until roughly 2023, when frontier labs effectively exhausted the available corpus — not in the sense of running out of bytes, but in the sense that all meaningful novel knowledge had been ingested. The bottleneck classification has since shifted from "possibly fundamental" to a 3–5 year resolution horizon, a subtle but telling change. The field no longer treats this as an unsolvable wall but as an engineering problem with a finite resolution window, contingent on synthetic and interaction-derived alternatives proving out. What once felt like a ceiling is being reframed as a forcing function.

Two research directions have emerged in response, at different maturity levels. The earlier insight — that code pretraining boosts abstract reasoning more than general NLP training, because code demands hierarchical structure rather than pattern memorization — pointed toward quality and data composition rather than volume as the primary lever. By early 2025, this intuition crystallized into BoLT: training jointly on raw text and inferred latent reasoning traces, so each token teaches the model more than it would in isolation. Results at 1.1B scale are striking — synthetic thought augmentation outperforms an equivalent volume of unique raw tokens — but the technique carries significant caveats: unvalidated at frontier scale, degrading general STEM knowledge when applied to math-heavy corpora, and computationally expensive due to the distributed heterogeneous cluster required for latent generation.

By September 2025, a narrower but more production-ready approach reached the field: rephrasing pipelines that generate ten variants of the same wiki passage, achieving 28.94 SimpleQA accuracy against 23.76 for naive repetition. This technique is in narrow production, meaning it works but only within validated domains. Momentum is building around token efficiency as the new primary scaling coefficient, but it is fragile momentum. The April 2025 observation that imitation of human data cannot achieve superhuman intelligence introduces a harder constraint underneath the engineering ones: the data wall forces synthetic augmentation, but synthetic augmentation inherits the ceiling of human knowledge as its reference distribution.

The key open questions are whether BoLT-style techniques validate at 70B+ parameter scales, and whether rephrasing pipelines extend cleanly to scientific and technical domains without quality degradation. Those two results would determine whether the 3–5 year resolution horizon is achievable or whether the field needs to route around pretraining itself via RL-generated and interaction-derived corpora.

## Capabilities

- **Code pretraining for abstract reasoning** — Code pre-training boosts LLM performance on abstract perceptual reasoning tasks (e.g., ARC) more than general NLP multi-task training, because code demands hierarchical structure rather than pattern memorization. *(maturity: research only)*

- **Synthetic latent thought augmentation (BoLT)** — Training jointly on raw text and inferred latent reasoning traces (Bootstrapped Latent Thoughts) outperforms training on an equivalent volume of unique raw tokens at 1.1B scale. Each token carries more signal when paired with structured latent reasoning. *(maturity: research only)*

- **Synthetic rephrasing pipelines** — A synthetic data rephrasing pipeline generating 10 rephrasings of wiki-text passages achieves 28.94 SimpleQA accuracy, compared to 23.76 for naive repetition, demonstrating that diversity of surface form improves knowledge token utility. *(maturity: narrow production)*

## Limitations

**Structural / data supply:**

- Human pretraining data is a finite, near-exhausted resource growing slower than compute, creating a hard ceiling on data-driven capability gains. *(severity: blocking, trajectory: worsening, type: implicit hedging)*
- Internet-scale text data for pretraining is effectively exhausted; models have ingested essentially all available text, removing naive volume scaling as a viable path. *(severity: blocking, trajectory: stable, type: explicit)*
- High-quality human pretraining data is increasingly scarce, making token efficiency rather than raw data volume the critical scaling coefficient. *(severity: significant, trajectory: worsening, type: implicit scale/cost)*
- Insights representing genuinely new knowledge — new theorems, technologies, scientific breakthroughs — cannot be captured from historical text corpora. *(severity: blocking, trajectory: stable, type: explicit)*
- Imitation of human data cannot achieve superhuman intelligence; performance on key domains is approaching a ceiling set by the quality and coverage of human-generated training data. *(severity: blocking, trajectory: worsening, type: explicit)*
- Static historical data stockpiles, previously considered a decisive moat for incumbents, are becoming less decisive as real-time and interaction-derived data sources grow in importance. *(severity: significant, trajectory: worsening, type: implicit performance cliff)*

**BoLT / synthetic augmentation:**

- The entire BoLT experimental validation is confined to a 1.1B parameter model under academic compute budget, making it unclear whether the approach holds at frontier scale. *(severity: significant, trajectory: unclear, type: explicit)*
- Reasoning-to-learn is only demonstrated on math-heavy reasoning data (FineMath corpus); transfer to general-domain pretraining corpora is unvalidated. *(severity: significant, trajectory: unclear, type: explicit)*
- MMLU-STEM performance across BoLT iterations fell within noise floor (< 28%), revealing that extended math-focused pretraining with latent augmentation degrades general STEM knowledge. *(severity: significant, trajectory: worsening, type: implicit performance cliff)*
- Latent generation at scale requires a distributed heterogeneous GPU cluster (H100/200, A100/6000/5000/40, L40, RTX3090), imposing significant infrastructure cost. *(severity: significant, trajectory: unclear, type: implicit scale/cost)*
- Continual bootstrapping risks catastrophic forgetting during iterative pretraining; special warmup-cool schedules are required. *(severity: significant, trajectory: unclear, type: implicit controlled conditions)*

**Rephrasing pipelines:**

- Scaling synthetic data rephrasing to diverse domains without introducing hallucinations and unintended toxicity remains unsolved. *(severity: significant, trajectory: unclear, type: explicit)*

**Domain-specific (genomics):**

- Eukaryotic training data required aggressive filtering (removing short contigs < 10kb, contigs > 5% ambiguous nucleotides), constraining the usable corpus. *(severity: minor, trajectory: stable, type: implicit controlled conditions)*
- Repeat element information (encoded via lowercase nucleotides) is discarded after the first 3T pretraining tokens, permanently excluding a biologically significant signal class. *(severity: minor, trajectory: stable, type: explicit)*
- Evo 2 trains on only one human genome (reference genome) with no population-scale human variant data, causing the model to underperform on population-specific variant prediction. *(severity: significant, trajectory: improving, type: implicit conspicuous absence)*
- Naive long-context training on raw eukaryotic reference genomes (predominantly noncoding repetitive sequence) degraded model performance; specialized data handling was required. *(severity: significant, trajectory: stable, type: implicit controlled conditions)*

**Agentic / workflow data:**

- Frontier labs lack visibility into inter-product workflows — the decisions, hand-offs, and multi-tool processes that occur across software products — because this data is proprietary to enterprise vendors. *(severity: significant, trajectory: stable, type: implicit conspicuous absence)*

## Bottlenecks

- **Language model pretraining data exhaustion** — The internet's text corpus has been effectively consumed by frontier models, forcing reliance on RL-generated data and synthetic corpora for continued capability gains. *(status: active, horizon: 3–5 years)*

- **High-quality data scarcity and token efficiency** — The exhaustion of high-quality human-written web text forces a costly pivot from data volume to token efficiency techniques and synthetic augmentation strategies. *(status: active, horizon: 3–5 years)*

- **Compute/data growth mismatch** — Pretraining compute scaling has outpaced the growth of high-quality human-written text on the web, creating a data-constrained regime for continued capability improvement at frontier model sizes. *(status: active, horizon: 1–2 years)*

- **Supervised pretraining scaling ceiling** — High-quality human pretraining data is being exhausted, blocking further capability improvement via supervised pretraining and scaling at frontier labs. *(status: active, horizon: 1–2 years)*

- **Population-scale genomic data absence** — Population-scale human genomic variation is absent from genomic foundation model training, blocking accurate prediction of rare and population-specific human variant pathogenicity. *(status: active, horizon: 1–2 years)*

- **Proprietary cross-product workflow data** — Real end-to-end workflow data (decisions, hand-offs, multi-tool processes) is structurally inaccessible to frontier labs, blocking agents that generalize to complete real-world work processes rather than siloed single-product tasks. *(status: active, horizon: 3–5 years)*

- **CUDA backward kernel patterns absent from pretraining data** — Absence of backward CUDA kernel optimization patterns in LLM pre-training data prevents effective LLM-driven optimization of full training pipelines, limiting automatic CUDA optimization to inference rather than training workloads. *(status: active, horizon: 1–2 years)*

## Breakthroughs

- **BoLT (Bootstrapped Latent Thoughts)** — Demonstrated that training jointly on raw text and inferred latent reasoning traces outperforms training on an equivalent volume of unique raw tokens at 1.1B scale. Reframes data efficiency as a function of per-token information content rather than corpus size. Results remain confined to academic compute budgets and the FineMath corpus.

- **Synthetic rephrasing pipeline** — Demonstrated that generating 10 surface-form rephrasings of the same wiki passage yields 28.94 SimpleQA accuracy vs. 23.76 for naive repetition, establishing diversity of form (not just volume) as a meaningful lever for knowledge acquisition. Reached narrow production status as of September 2025.

- **Code pretraining for abstract reasoning** — Established that code-heavy pretraining transfers to abstract perceptual reasoning (ARC benchmarks) more effectively than general NLP multi-task training, shifting research intuition toward data composition as a first-class design variable.

## Anticipations

- **BoLT validation at frontier scale (70B+)** — Whether latent thought augmentation maintains its advantage over raw token volume at parameter counts used by frontier labs is the key open question. Positive results would accelerate the pivot toward synthetic augmentation and establish a new scaling law coefficient around per-token information density.

- **Rephrasing pipeline domain extension** — Whether rephrasing-based synthetic augmentation extends cleanly to scientific and technical domains without quality degradation or hallucination amplification will determine the technique's applicability beyond narrow validated domains.

- **RL-generated and interaction-derived corpora as pretraining bypass** — If synthetic augmentation cannot overcome the human knowledge ceiling, the field may route around pretraining via RL-generated experience and proprietary interaction data. Evidence of this trajectory is already visible in the shift of frontier labs toward post-training and RLHF-derived capabilities.

- **Token efficiency as the new primary scaling law** — Momentum is building around token efficiency as the new scaling coefficient, replacing raw data volume. Whether this holds across model sizes, domains, and architectures remains unverified.

## Cross-Theme Implications

- **→ [[themes/audio_and_speech_models|Audio and Speech Models]]:** The bottleneck in audio generation was dataset quality and scale, not architecture: VGGSound (550 hours) and AudioSet (5K hours) are non-cinematic, small-scale datasets that systematically prevented audio models from learning professional production patterns. Internet-scale cinematic data unlocks synchronized diegetic/non-diegetic audio mixing, a qualitative capability the field had not previously achieved. This implies the audio research community has been solving the wrong problem: architectural innovation on inadequate data cannot substitute for proper data curation at scale. The same forcing function operating on language pretraining (data exhaustion driving qualitative reassessment of what data is) is operating on audio at an earlier stage.

- **→ [[themes/pretraining_and_scaling|Pretraining and Scaling]]:** The data exhaustion bottleneck directly destabilizes the compute-data-parameters scaling law regime. As high-quality data becomes the binding constraint rather than compute, the Chinchilla-style optimal allocation framework requires revision. Token efficiency techniques (BoLT, rephrasing) introduce a new per-token information density variable that existing scaling laws do not model.

- **→ [[themes/reinforcement_learning|Reinforcement Learning]]:** The imitation ceiling (synthetic data inheriting human knowledge as reference distribution) creates a structural demand for RL-generated experience as a source of non-imitative signal. RL becomes not just a post-training alignment technique but a potential pretraining data generator for superhuman capability domains.

- **→ Genomic and Biological Models:** Domain-specific pretraining data limitations (reference genome monoculture, aggressive filtering requirements, repeat element discarding, long-context degradation on repetitive noncoding sequence) parallel the general language data quality problem, but with higher stakes: errors propagate into clinical variant prediction rather than factual inaccuracy.

## Contradictions

- **Volume vs. quality as the scaling lever:** Early scaling research treated data volume as the primary variable (more tokens = better models). BoLT and rephrasing pipeline results suggest per-token information content is at least as important, if not more so, at current scales. These perspectives are not fully reconciled: BoLT's advantage may diminish as the baseline corpus quality improves, or it may compound.

- **Synthetic data as solution vs. synthetic data as ceiling:** Synthetic augmentation is simultaneously positioned as the response to the human data wall and subject to the constraint that it inherits human knowledge as its reference distribution. The community holds both views simultaneously, which may reflect an unresolved tension rather than a settled consensus.

- **Static data moats vs. dynamic data advantage:** The observation that static historical data stockpiles are becoming less decisive as real-time and interaction-derived data sources grow contradicts the long-held assumption that incumbent data hoarding is a durable competitive moat. This has not been formally tested against a frontier model trained predominantly on interaction-derived data.

## Research Opportunities

- **BoLT at frontier scale:** Validating latent thought augmentation at 70B+ parameters under realistic compute budgets is the highest-leverage experiment in the subfield. Negative results would be as valuable as positive, narrowing the viable solution space.

- **Cross-domain rephrasing quality metrics:** Rephrasing pipelines lack robust quality metrics beyond downstream benchmark accuracy. Developing hallucination-sensitive quality signals that generalize across domains would accelerate safe deployment beyond narrow validated settings.

- **Non-imitative pretraining signal sources:** If imitation of human data cannot achieve superhuman intelligence, what data sources can? Formalizing the taxonomy of non-imitative signal (RL rollouts, tool-use traces, multi-agent debate transcripts, structured self-play) and measuring their per-token contribution to capability is an open research program.

- **Population-scale genomic pretraining:** Training genomic foundation models on population-scale human variant data (rather than a single reference genome) is a near-term tractable improvement with direct clinical impact. The data exists (UK Biobank, gnomAD, population cohorts); the bottleneck is infrastructure and curation, not fundamental data absence.

- **Interaction-derived workflow corpora:** Constructing pretraining corpora from real multi-product workflow data (with appropriate privacy and consent frameworks) would address the proprietary cross-product data bottleneck. This is partly an institutional and legal problem, not only a technical one.

- **Backward CUDA kernel pattern corpus construction:** Systematically curating and synthesizing backward CUDA kernel optimization patterns as a pretraining data supplement could unlock LLM-driven end-to-end training pipeline optimization, currently blocked by pattern absence in existing corpora.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 18 sources.
- **2025-12-16** — [[sources/01KJT37Q1W-t5gemma-2-seeing-reading-and-understanding-longer|T5Gemma 2: Seeing, Reading, and Understanding Longer]]: EmbeddingGemma leverages T5Gemma 2 checkpoints to achieve state-of-the-art performance on text retri
- **2025-11-05** — [[sources/01KJTAPFA4-diffusion-language-models-are-super-data-learners|Diffusion Language Models are Super Data Learners]]: Diffusion language models consistently surpass autoregressive models when unique data is limited, ac
- **2025-10-21** — [[sources/01KJVP8YZR-andrej-karpathy-and-dwarkesh-patel-popping-the-agi-bubble-building-the-ai-aristo|Andrej Karpathy and Dwarkesh Patel – Popping the AGI Bubble, Building the AI Aristocracy]]: Karpathy defines AGI as a system that can perform any economically valuable task at human performanc
- **2025-09-29** — [[sources/01KJTF5EP6-mobilellm-r1-exploring-the-limits-of-sub-billion-language-model-reasoners-with-o|MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes]]: MobileLLM-R1-950M achieves an AIME score of 15.5, dramatically outperforming OLMo-2-1.48B (0.6) and 
- **2025-09-24** — [[sources/01KJTGT235-thinking-augmented-pre-training|Thinking Augmented Pre-training]]: Thinking Augmented Pre-Training (TPT) enhances the data efficiency of LLM pre-training by a factor o
- **2025-09-24** — [[sources/01KJVT4GRY-ai-talent-wars-xais-200b-valuation-googles-comeback|AI Talent Wars, xAI’s $200B Valuation, & Google’s Comeback]]: Invasive BCI requires skull surgery to implant a computer chip in the brain, enabling granular neura
- **2025-07-21** — [[sources/01KJTMX34E-diffusion-beats-autoregressive-in-data-constrained-settings|Diffusion Beats Autoregressive in Data-Constrained Settings]]: Masked diffusion language models train by randomly masking a fraction of tokens drawn from U(0,1) an
- **2025-07-08** — [[sources/01KJVN4FS2-2-robotics-pioneers-unpack-the-path-to-generalist-robots|2 Robotics Pioneers Unpack the Path to Generalist Robots]]: Physical Intelligence has raised over $400 million in funding.
- **2025-06-17** — [[sources/01KJTPVV11-from-bytes-to-ideas-language-modeling-with-autoregressive-u-nets|From Bytes to Ideas: Language Modeling with Autoregressive U-Nets]]: AU-Net applies a contracting path that pools bytes into words, then word pairs, then up to four-word
- **2025-06-04** — [[sources/01KJVTQQ0E-mercor-ceo-evals-will-replace-knowledge-work-ai-x-hiring-today-the-future-of-dat|Mercor CEO: Evals Will Replace Knowledge Work, AI x Hiring Today & the Future of Data Labeling]]: Before raising outside funding, Meror bootstrapped to a $1 million annual revenue run rate and $80,0
- **2025-05-30** — [[sources/01KJTQRXBY-how-much-do-language-models-memorize|How much do language models memorize?]]: GPT-style language models have an approximate memorization capacity of 3.6 bits per parameter
- **2025-05-20** — [[sources/01KJTT03GZ-emerging-properties-in-unified-multimodal-pretraining|Emerging Properties in Unified Multimodal Pretraining]]: BAGEL uses QK-Norm in each attention block to stabilize the training process, following common pract
- **2025-03-24** — [[sources/01KKT4SWNY-reasoning-to-learn-from-latent-thoughts|Reasoning to Learn from Latent Thoughts]]: New capability: Synthetic latent thought augmentation (training jointly on raw text and inferred
- **2025-02-19** — [[sources/01KKT5HWA5-genome-modeling-and-design|Genome modeling and design]]: Limitation identified: Evo 2 trains on only one human genome (reference genome) — no population-scale h
- **2024-12-24** — [[sources/01KJVGAVH2-best-of-2024-synthetic-data-smol-models-loubna-ben-allal-huggingface-ls-live-neu|Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace [LS Live! @ NeurIPS 2024]]]: FineWeb-Edu was created by using Llama 3 to rate educational quality of web pages 0–5, training a BE
- **2024-11-22** — [[sources/01KJV6RRM0-the-zamba2-suite-technical-report|The Zamba2 Suite: Technical Report]]: 4-bit quantization of Zamba2-2.7B reduces its memory footprint from 5.38 GB to 1.55 GB; adding 4-bit
- **2024-10-29** — [[sources/01KJVTXQWN-deepl-ceo-on-specialized-vs-general-models-beating-google-and-a-synchronous-tran|DeepL CEO on Specialized vs. General Models, Beating Google and a Synchronous Translation Future]]: DeepL most recently raised at a $2 billion valuation
- **2024-10-03** — [[sources/01KJV7V9DK-intelligence-at-the-edge-of-chaos|Intelligence at the Edge of Chaos]]: Downstream task evaluation freezes all pretrained GPT-2 layers and trains only the input and output 
```
