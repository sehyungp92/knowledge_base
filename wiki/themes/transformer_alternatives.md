---
type: theme
title: Transformer Alternatives
theme_id: transformer_alternatives
level: 2
parent_theme: model_architecture
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 34
sources_since_update: 0
update_count: 1
velocity: 0.2
staleness: 0.0
status: active
tags: []
---
# Transformer Alternatives

> The transformer alternatives field is in active ferment — moving from theoretical critique toward architectural proof-of-concept, with recurrent and hybrid models accumulating evidence that the transformer's dominance is contingent rather than fundamental. The core scalability bottleneck remains structurally intact, but the nature of the capability claim has shifted: hybrid architectures are demonstrating practical efficiency gains in real deployments, while pure attention-free models like Hope are now empirically confirming transformer limitations on tasks involving state tracking and formal language recognition — limitations that are not improving, and in some cases widening.

**Parent:** [[themes/model_architecture|model_architecture]]

## Current State

For years, the central bottleneck in transformer alternatives was not capability but credibility: recurrent architectures lacked validation at scales that matter. That bottleneck remains structurally intact. The Hope architecture (December 2025) and StripedHyena 2 (February 2025) both deliver compelling results, but at 1.3B parameters and 100B training tokens respectively — well short of frontier scale. The compute barrier blocking adoption in serious foundation model training sits at the same place it did before these results: no evidence above ~10B parameters. The field has gotten better at proving the concept without yet proving the scale.

What has shifted is the *nature* of the capability claim. Earlier hybrid work — including the Mamba-MLP-Transformer multimodal backbone (March 2025) — demonstrated practical efficiency gains for long video sequences, a demo-maturity result showing that hybrid architectures can reduce quadratic attention overhead in real deployments. StripedHyena 2 extended this with a multi-hybrid convolutional architecture achieving 3x training throughput over optimised transformer baselines, with a constant-memory footprint for genomic sequence generation. These are engineering wins.

Hope represents a qualitatively different advance. It doesn't just match transformers more efficiently — it *beats* them on tasks transformers structurally cannot solve. Perfect scores on non-star-free regular, counter, and parity language recognition tasks, where transformers score near zero, establish that the transformer's architectural limitation around state tracking and formal language recognition is real, empirically confirmed, and not improving. The limitation landscape is now bifurcated: attention-free models are closing the gap on in-context recall (previously a transformer stronghold), while the gap on non-parallelizable recurrence tasks is widening in the other direction, against transformers.

Momentum is building simultaneously on two fronts — hybrid architectures gaining practical traction for long-context efficiency, and pure attention-free models pushing the theoretical frontier. The cross-theme signal toward continual learning is particularly significant: if self-referential update mechanisms at inference time prove robust at scale, the transformer's continual learning limitations may be architectural rather than fundamental, and alternatives may leapfrog rather than merely catch up.

## Capabilities

- **Hope architecture** achieves state-of-the-art language modeling and common-sense reasoning among attention-free models, outperforming all attention-free baselines (RWKV-7, Comba, Titans, TTT, Miras, DLA) and closing the gap with transformers. *(maturity: research_only)*
- **Hope** outperforms all baselines including transformers on the MAD synthetic benchmark, covering compression and in-context recall tasks. *(maturity: research_only)*
- **Hope** achieves perfect scores on all formal language recognition tasks — including non-star-free regular, counter, and parity — where transformer baselines score near zero. *(maturity: research_only)*
- **Hope** outperforms all baselines on average across language modeling (perplexity) and common-sense reasoning benchmarks. *(maturity: research_only)*
- **StripedHyena 2**, a multi-hybrid convolutional SSM/attention architecture, achieves 3x training throughput over optimised transformer baselines while generating genomic sequences with a constant memory footprint. *(maturity: research_only)*
- **Hybrid Mamba-MLP-Transformer** architectures can serve as efficient LLM backbones for multimodal models, handling long video sequences with reduced quadratic attention overhead. *(maturity: demo)*

## Limitations

- **Mamba selective state spaces alone** are insufficient for capturing all detail in long sequences — requiring hybrid training designs to compensate. *(severity: minor, trajectory: improving, type: explicit)*
- **Transformers fundamentally fail** on non-parallelizable, recurrence-dependent tasks such as state tracking and formal language recognition. This limitation is now empirically confirmed and not improving. *(severity: significant, trajectory: stable, type: explicit)*
- **Hope's validation gap**: improvements are demonstrated only at 760M and 1.3B parameter scales on 30B–100B tokens; there is no evidence of behaviour at frontier scale. *(severity: significant, trajectory: unclear, type: implicit — conspicuous absence)*
- **In-context recall gap**: attention-free models still lag behind transformers on in-context recall tasks despite closing the gap; transformers remain dominant here. *(severity: significant, trajectory: improving, type: implicit — performance cliff)*

## Bottlenecks

- **Scalability of recurrent architectures to frontier training scales** remains unvalidated. The absence of evidence above ~10B parameters is the primary barrier blocking replacement or supplementation of transformers in frontier foundation model training. *(status: active, horizon: 1–2 years)*
- **Transformer architectural ceiling on state tracking and formal language tasks** blocks transformer-based systems from state tracking, formal language processing, and tasks requiring non-linear recurrent computation. This bottleneck is not on the transformer side to resolve — it defines where alternatives have a structural opening. *(status: active, horizon: 1–2 years)*

## Breakthroughs

- **Hope architecture** (December 2025), combining self-referential Titans with a Continuum Memory System, achieves new state-of-the-art among attention-free models on both standard language modeling and long-context tasks simultaneously. Prior belief held that no attention-free architecture had matched transformers on both dimensions at once, and that continual learning required external memory modules or regularisation methods like EWC. Hope challenges both assumptions. *(significance: notable)*
- **Hope on formal language recognition**: achieving perfect performance on all formal language recognition tasks — including non-star-free regular, counter, and parity — resolves a long-standing theoretical gap. Prior belief held that models with sufficient expressiveness for these tasks (non-linear recurrence, e.g., LSTM, SRWM) could not be trained in parallel and thus could not scale to the token volumes required for competitive language modeling. Hope demonstrates this trade-off is not absolute. *(significance: notable)*

## Anticipations

- Whether any group attempts Hope or a Hope-like architecture above 10B parameters — the result would either validate or deflate the 1–2 year scalability horizon.
- Whether the in-context recall gap continues closing as attention-free architectures mature — if so, transformers lose their last clear structural advantage outside of parallelism.
- Whether self-referential inference-time update mechanisms prove robust at scale, which would have direct implications for continual learning architectures.

## Cross-Theme Implications

- → [[themes/continual_learning|continual_learning]]: A self-modifying sequence model that learns its own update rule at inference time represents a class of transformer alternatives that natively supports online learning — suggesting that the transformer bottleneck for continual learning is architectural, not fundamental, and that alternatives can overcome it without external memory or regularisation hacks.
- → [[themes/transformer_alternatives|transformer_alternatives]]: The hybrid window-local + convolutional compression + global attention pattern validated in DeepEncoder provides an empirically grounded template for long-context architectures that avoids full quadratic attention, informing the design of transformer alternatives optimised for document-scale inputs.

## Contradictions

- The field simultaneously holds that (1) recurrent alternatives are not ready at scale, and (2) recurrent alternatives beat transformers on certain tasks. These are not contradictory — they operate at different scales and task types — but they create a tension in how the field is narrated. The "transformers are dominant" framing remains accurate for frontier training; the "transformers are limited" framing is now also empirically accurate for specific task classes. Both are true, at different points in the capability space.
- Hope's in-context recall results (matching or exceeding transformers on MAD) sit in tension with the stated limitation that attention-free models still lag on in-context recall. The MAD benchmark may not fully represent the in-context recall tasks where transformers dominate — this distinction warrants scrutiny as more benchmarks are applied.

## Research Opportunities

- **Scale testing for Hope-class architectures**: The most direct open question in the field. A Hope or Hope-like model trained above 10B parameters on 1T+ tokens would either confirm or falsify the scalability hypothesis. High value, high cost.
- **Formal language task benchmarking across architectures**: Hope's perfect scores on non-star-free tasks open a new evaluation axis. Systematic benchmarking of current frontier models on formal language recognition would establish how wide the transformer limitation actually is in practice.
- **Hybrid architecture search for long-context efficiency**: The StripedHyena 2 and Mamba-MLP-Transformer results suggest that the design space of hybrid architectures is underexplored. Principled architecture search in this space — varying the ratio, placement, and type of recurrent vs. attention layers — could yield practical gains without requiring full recurrent training.
- **Inference-time learning robustness**: Hope's self-referential update mechanism at inference time is theoretically significant for continual learning. Whether it is robust to distribution shift, adversarial inputs, and extended deployment conditions is an open empirical question with high downstream value.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJS0KV75-titans-miras-helping-ai-have-long-term-memory|Titans + MIRAS: Helping AI have long-term memory]]: Breakthrough: Titans introduces a deep MLP as a long-term memory module that learns and update
- **2026-04-08** — [[sources/01KJS34DRS-what-is-power-retention-manifest-ai|What Is Power Retention? - Manifest AI]]: Breakthrough: Discovery that retention derived from the symmetric power mathematical formulati
- **2026-04-08** — [[sources/01KJS3BJW4-the-hidden-drivers-of-hrms-performance-on-arc-agi|The Hidden Drivers of HRM's Performance on ARC-AGI]]: ARC Prize independently verified HRM at 32% on the ARC-AGI-1 Semi-Private evaluation set.
- **2026-04-08** — Wiki page created. Theme has 34 sources.
- **2025-12-16** — [[sources/01KJT367PQ-universal-reasoning-model|Universal Reasoning Model]]: URM achieves 16.0% pass@1 on ARC-AGI 2, nearly tripling HRM (5.4%) and more than doubling TRM (4.6%)
- **2025-11-23** — [[sources/01KJVDXNW6-he-co-invented-the-transformer-now-continuous-thought-machines-llion-jones-luke-|He Co-Invented the Transformer. Now: Continuous Thought Machines [Llion Jones / Luke Darlow]]]: SudokuBench uses handcrafted variant sudoku puzzles with diverse natural-language-described constrai
- **2025-11-20** — [[sources/01KJT7VEK3-evolution-strategies-at-the-hyperscale|Evolution Strategies at the Hyperscale]]: Breakthrough: Stable pretraining of a language model operating entirely in int8 integer dataty
- **2025-11-19** — [[sources/01KJS121AX-ai-101-what-is-lejepa-the-theory-upgrade-jepa-has-been-missing|AI 101: What is LeJEPA? The Theory Upgrade JEPA Has Been Missing]]: JEPA does not try to predict pixels or surface details — it predicts the abstract state of the world
- **2025-11-12** — [[sources/01KJT9KDWV-tidar-think-in-diffusion-talk-in-autoregression|TiDAR: Think in Diffusion, Talk in Autoregression]]: Breakthrough: TiDAR is the first architecture to simultaneously close the quality gap with AR 
- **2025-11-05** — [[sources/01KJTAPFA4-diffusion-language-models-are-super-data-learners|Diffusion Language Models are Super Data Learners]]: Breakthrough: Systematic empirical proof that diffusion language models extract 3x+ more signa
- **2025-10-31** — [[sources/01KJTC07QH-continuous-autoregressive-language-models|Continuous Autoregressive Language Models]]: Breakthrough: CALM establishes continuous next-vector prediction as a viable and superior perf
- **2025-07-21** — [[sources/01KJTMX34E-diffusion-beats-autoregressive-in-data-constrained-settings|Diffusion Beats Autoregressive in Data-Constrained Settings]]: Breakthrough: The widely-reported 16× compute disadvantage of masked diffusion language models
- **2025-07-14** — [[sources/01KJTN8HBD-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-token-level|Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation]]: Under equal training budget of 16.5e18 FLOPs, MoR with expert-choice routing and Nr=2 achieves lower
- **2025-07-02** — [[sources/01KJTNZS7X-energy-based-transformers-are-scalable-learners-and-thinkers|Energy-Based Transformers are Scalable Learners and Thinkers]]: Limitation identified: EBTs are incompatible with existing pretrained foundation models — the architect
- **2025-06-26** — [[sources/01KJTMPYR9-hierarchical-reasoning-model|Hierarchical Reasoning Model]]: HRM executes sequential reasoning tasks in a single forward pass without explicit supervision of the
- **2025-06-25** — [[sources/01KJTPC0T7-diffucoder-understanding-and-improving-masked-diffusion-models-for-code-generati|DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation]]: Breakthrough: Empirical discovery of the entropy sink phenomenon in masked diffusion LLMs: a s
- **2025-06-17** — [[sources/01KJTPVV11-from-bytes-to-ideas-language-modeling-with-autoregressive-u-nets|From Bytes to Ideas: Language Modeling with Autoregressive U-Nets]]: Breakthrough: AU-Net demonstrates that tokenisation can be fully internalised into a language 
- **2025-06-12** — [[sources/01KJTQCEKY-the-diffusion-duality|The Diffusion Duality]]: Breakthrough: Discrete Consistency Distillation (DCD) achieves 100–128× sampling acceleration 
- **2025-06-05** — [[sources/01KJTPFVK6-log-linear-attention|Log-Linear Attention]]: Breakthrough: Log-linear attention establishes a principled, implementable middle ground betwe
- **2025-05-29** — [[sources/01KJTRVBMF-atlas-learning-to-optimally-memorize-the-context-at-test-time|ATLAS: Learning to Optimally Memorize the Context at Test Time]]: Breakthrough: Omega rule enables parametric recurrent memory to optimize over a sliding contex
- **2025-05-29** — [[sources/01KJTRB1VP-test-time-training-done-right|Test-Time Training Done Right]]: Limitation identified: LaCT fast-weight components (SwiGLU-MLP and linear variants) lack rotation invar
- **2025-05-08** — [[sources/01KJTVJC6B-continuous-thought-machines|Continuous Thought Machines]]: The CTM uses an internal time dimension decoupled from data dimensions to enable iterative refinemen
- **2025-02-19** — [[sources/01KKT5HWA5-genome-modeling-and-design|Genome modeling and design]]: New capability: Multi-hybrid convolutional architecture (StripedHyena 2) achieving 3x training t
- **2025-02-08** — [[sources/01KJVM8AVM-google-titans-learning-to-memorize-at-test-time|Google Titans: Learning to Memorize at Test Time]]: Breakthrough: Titans architecture achieves breakthrough by combining Transformer expressivenes
- **2025-02-07** — [[sources/01KJV49W0K-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-approach|Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach]]: Limitation identified: Integration with modern efficiency architecture improvements (linear attention, 
- **2024-12-31** — [[sources/01KJV5HWSH-titans-learning-to-memorize-at-test-time|Titans: Learning to Memorize at Test Time]]: New capability: Titans are provably more expressive than Transformers and modern linear recurren
- **2024-12-13** — [[sources/01KJV64ZDF-byte-latent-transformer-patches-scale-better-than-tokens|Byte Latent Transformer: Patches Scale Better Than Tokens]]: Breakthrough: BLT is the first byte-level LLM to match tokenization-based model performance in
- **2024-11-22** — [[sources/01KJV6RRM0-the-zamba2-suite-technical-report|The Zamba2 Suite: Technical Report]]: Breakthrough: Open-source hybrid Mamba2-transformer models (Zamba2) simultaneously achieve SOT
- **2024-11-20** — [[sources/01KJV6RXXK-hymba-a-hybrid-head-architecture-for-small-language-models|Hymba: A Hybrid-head Architecture for Small Language Models]]: Breakthrough: Parallel SSM+attention hybrid-head fusion within the same layer (Hymba architect
- **2024-10-30** — [[sources/01KJV749E6-tokenformer-rethinking-transformer-scaling-with-tokenized-model-parameters|TokenFormer: Rethinking Transformer Scaling with Tokenized Model Parameters]]: Breakthrough: Tokenformer demonstrates that treating model parameters as learnable tokens and 
- **2024-10-30** — [[sources/01KJVKZAT6-training-zamba-a-hybrid-model-master-class-with-zyphras-quentin-anthony|Training Zamba: A Hybrid Model Master Class with Zyphra's Quentin Anthony]]: Breakthrough: Mamba 2 SSD (State Space Duality) algorithm restructures the SSM state matrix to
- **2024-10-16** — [[sources/01KJVKT2TV-mamba-linear-time-sequence-modeling-with-selective-state-spaces-colm-oral-2024|Mamba: Linear-Time Sequence Modeling with Selective State Spaces (COLM Oral 2024)]]: Breakthrough: State-space models with three key innovations (large state size via expansion fa
- **2024-07-29** — [[sources/01KJVKZER8-llm-attention-that-expands-at-inference-test-time-training-explained|LLM Attention That Expands At Inference? Test Time Training Explained]]: New capability: Mamba architecture achieves best-in-class performance at shorter context lengths
- **2024-07-12** — [[sources/01KJVM69GC-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states|Learning to (Learn at Test Time): RNNs with Expressive Hidden States]]: Breakthrough: Meta-learning framework for RNN hidden state updates achieves linear-complexity 
- **2024-04-30** — [[sources/01KJV95THR-kan-kolmogorov-arnold-networks|KAN: Kolmogorov-Arnold Networks]]: The original Kolmogorov-Arnold representation theorem corresponds to a 2-layer KAN with shape [n, 2n
