---
type: source
title: Thinking Augmented Pre-training
source_id: 01KJTGT235Z05NVQFQZSC32XBF
source_type: paper
authors:
- Liang Wang
- Nan Yang
- Shaohan Huang
- Li Dong
- Furu Wei
published_at: '2025-09-24 00:00:00'
theme_ids:
- chain_of_thought
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinking Augmented Pre-training

**Authors:** Liang Wang, Nan Yang, Shaohan Huang, Li Dong, Furu Wei
**Published:** 2025-09-24 00:00:00
**Type:** paper

## Analysis

# Thinking Augmented Pre-training
2025-09-24 · paper · Liang Wang, Nan Yang, Shaohan Huang, Li Dong, Furu Wei
https://arxiv.org/pdf/2509.20186

---

### Motivation & Prior Limitations

- The pool of high-quality human-authored web data is finite and has been largely exhausted by frontier models trained on 10T+ tokens, creating a hard ceiling on data-driven scaling even as compute continues to grow.
  - Models like LLaMA-3.1 (15T tokens) and Qwen2.5 represent the near-exhaustion regime; the community cannot simply acquire more organic human data at the scale needed for the next generation.

- A distinct but underexplored bottleneck is that certain high-quality tokens are exceptionally difficult to learn via single-step next-token prediction because they represent the compressed output of deep, multi-step human reasoning that a model of limited capacity cannot reconstruct from context alone.
  - The paper's motivating example: the answer token "890" requires fluent command of polynomial division, the Remainder Theorem, and divisor properties — none of which are deducible from surface pattern matching at fixed model capacity.

- Prior work addressing token learnability (data selection, rewriting, Reasoning CPT, BoLT) was either limited in scale (≤8B tokens, ≤1B parameters) or domain-specific, with no demonstration that thinking-augmented training generalizes across pre-training, mid-training, and fine-tuning at 100B-token scale.
  - Reasoning CPT scaled only to ~150M tokens under continual pre-training and evaluated only base models on MMLU; BoLT used GPT-4o-mini, covered only math, and required an iterative EM bootstrapping algorithm adding implementation complexity.

---

### Proposed Approach

- Thinking Augmented Pre-Training (TPT) augments each document in the pre-training corpus with an automatically generated thinking trajectory produced by an off-the-shelf open-source LLM (DeepSeek-R1-Distill-Qwen-7B by default), then trains on the concatenated sequence `[document; thinking_trajectory]` using standard next-token prediction loss over all tokens.
  - The generation prompt instructs the model to "simulate an expert's in-depth thought process" using the Feynman technique, deliberately skipping trivial details and focusing on complex, informative aspects — no task-specific prompting or human annotation is required.
  - Unlike RPT, which requires online rollouts and token-level RL, TPT is a purely offline, document-level data preprocessing step with no architectural changes, making it trivially scalable to arbitrary corpus sizes.

- TPT implements an implicit training-time analogue of test-time scaling: because thinking trajectory length correlates with document difficulty and reasoning intensity, harder samples naturally receive more training compute without any manual quality filtering or heuristic up-sampling.
  - Analysis of 20k stratified documents shows Math and Physics domains produce ~1800 and ~1600 average thinking tokens respectively, versus ~1000 for low-reasoning domains; "Advanced Reasoning" documents generate ~50% more tokens than "No Reasoning" documents.

- The method is universally applicable across training stages — pre-training from scratch, mid-training (continual pre-training) from existing checkpoints, and supervised fine-tuning — requiring only a capable open-source thinking generator and a standard LM training loop.

---

### Results & Capabilities

- TPT improves data efficiency of LLM pre-training by a factor of 3×: an 8B model trained with TPT on 100B tokens achieves performance comparable to LLaMA-3.1-8B trained on 15T tokens (average 43.9 vs. 46.8 across GSM8k, MATH, BoolQ, MMLU, MMLUPro).
  - The vanilla 8B baseline trained on the same 100B tokens scores only 26.2 average, while TPT-8B reaches 43.9 — a 67% relative improvement — with the performance gap widening throughout training and becoming pronounced after 20B tokens.

- On reasoning benchmarks after SFT, TPT-8B dramatically outperforms both its vanilla baseline and LLaMA-3.1-8B-Instruct across every evaluated task: AIME24 jumps from 1.0% to 35.2%, MATH-500 from 33.8% to 82.4%, LiveCodeBench from 1.9% to 23.4%, and GPQA from 27.7% to 45.2%.
  - The vanilla pre-training baseline fails almost completely on competition-level reasoning (AIME24: 1.0%, LCB: 1.9%), demonstrating that standard next-token prediction on the same corpus does not develop the latent reasoning capacity that TPT instills.

- Mid-training results across model families (Qwen2.5 and LLaMA-3, 1.5B–7B parameters) consistently show TPT outperforming OpenR1 baselines trained on the identical SFT dataset: TPT-LLaMA-3B achieves AIME24 of 18.6% versus 5.8% for OpenR1-LLaMA-3B, a 3× improvement, and TPT-Qwen2.5-7B reaches MATH-500 92.5% and AIME24 57.5%.
  - LLaMA models benefit more than Qwen2.5 models from thinking augmentation, likely because LLaMA's pre-training corpus contained less reasoning-intensive data, leaving more headroom for TPT to fill.

- A surprising ablation finding: using a smaller thinking generation model (DeepSeek-R1-Distill-Qwen-1.5B instead of 7B) yields better downstream performance across most benchmarks, suggesting the generator–trainee relationship is non-trivial and that smaller generators may produce trajectories better calibrated to downstream model learning.

- Under the constrained data regime (10B raw tokens, 40B training budget), TPT continues improving steadily through all training tokens while vanilla pre-training plateaus once the data is exhausted through repeated epochs, demonstrating that thinking trajectories extract substantially more signal from a fixed underlying dataset.

---

### Implications

- TPT provides a concrete and practical mechanism for the field to continue scaling model capabilities even after the exhaustion of high-quality human-authored web data, by amplifying the learning signal latent in already-collected corpora rather than requiring new data sources.

- The training-time/test-time s

## Key Claims

1. Thinking Augmented Pre-Training (TPT) enhances the data efficiency of LLM pre-training by a factor of 3.
2. For a 3B parameter model, TPT improves post-training performance by over 10% on several challenging reasoning benchmarks.
3. High-quality tokens are difficult to learn at fixed model capacity because the underlying rationale for a single token can be exceptionally complex and deep.
4. The pool of human-authored, organically generated data on the web is finite and has been largely exhausted by existing frontier models.
5. A TPT-trained 8B model on 100B tokens achieves performance comparable to LLaMA-3.1-8B trained on 150x more data (15T tokens).
6. TPT raises GSM8k accuracy from 19.2% to 50.1% and more than doubles MATH scores from 9.1% to 21.8% for an 8B model trained on 100B tokens.
7. After SFT, TPT-8B outperforms LLaMA-3.1-8B-Instruct on every evaluated benchmark despite being pre-trained on a fraction of the data.
8. Vanilla pre-training fails to develop strong reasoning capabilities, as evidenced by very low scores on AIME24 and LiveCodeBench.
9. Under constrained data, vanilla pre-training plateaus as unique tokens are exhausted, while TPT continues to improve steadily.
10. Mathematics and Physics domains produce notably longer thinking trajectories, consistent with these fields requiring deep reasoning.

## Capabilities

- Augmenting pre-training data with LLM-generated thinking trajectories (TPT) improves data efficiency by 3×, enabling an 8B model trained on 100B tokens to match LLaMA-3.1-8B trained on 15T tokens across math and reasoning benchmarks
- Thinking augmented mid-training dramatically improves small models (1.5B–7B parameters) on challenging reasoning benchmarks — LLaMA-3B achieves 18.6% on AIME24 (up from 5.8% baseline, a 3× increase); Qwen2.5-7B reaches 92.5% on MATH-500
- Models trained on thinking-augmented data can surpass the model used to generate their training trajectories — TPT-Qwen2.5-7B outperforms its 7B teacher (DS-Distill-Qwen-7B) on AIME24 (57.5 vs 53.2), AIME25 (39.4 vs 35.5), and JEEBench (73.6 vs 49.9)
- Thinking trajectory length naturally correlates with domain reasoning intensity, providing automatic compute-weighted up-sampling of high-value training content without manual heuristics — math documents receive ~70% more thinking tokens than no-reasoning documents
- Thinking augmented pre-training under constrained raw data (10B tokens) prevents the performance plateau that afflicts vanilla pre-training through repeated epochs, enabling continued improvement on reasoning tasks throughout training

## Limitations

- TPT requires running inference with a capable open-source model over the entire pre-training corpus — at trillion-token frontier scale, this inference cost would be enormous and is entirely unanalyzed in the paper
- The relationship between target model capacity and optimal thinking generator model size is theoretically unsolved — a 1.5B generator unexpectedly outperforms a 7B generator, making principled model selection for TPT impossible with current understanding
- TPT benefits are strongly concentrated in reasoning-intensive domains — performance gains on BoolQ (reading comprehension) are modest (66.5%→75.0%) compared to math (MATH: 9.1%→21.8%; GSM8k: 19.2%→50.1%), limiting utility for general language tasks
- SFT alone on 350k samples is fundamentally insufficient to develop strong reasoning — without thinking augmented mid-training, LLaMA-3B achieves near-zero AIME24 accuracy regardless of SFT duration, revealing a hard capability floor that post-training cannot overcome
- Expert-level documents receive shorter thinking trajectories than undergraduate-level documents, suggesting the 7B generator model cannot produce sufficiently deep analysis for highly specialized content — limiting TPT's utility at the frontier of scientific and technical knowledge
- Results are explicitly marked 'work in progress' and validated only up to 100B training tokens and 8B model parameters — generalization to frontier-scale training (1T+ tokens, 70B+ parameters) is entirely undemonstrated
- TPT in the abundant-data regime processes 3× fewer unique documents than vanilla pre-training within the same token budget — the breadth-depth tradeoff and potential factual coverage gaps are not analyzed
- Benchmark contamination through thinking trajectory generation is not discussed — the DeepSeek generator model's training distribution may overlap with evaluation benchmarks (AIME, MATH-500), and injecting its reasoning into pre-training data may constitute indirect contamination
- The training corpus used (MegaMath-Web-Pro-Max and FineWeb-Edu) is heavily skewed toward math and educational content — the 3× efficiency claim and reasoning gains may not generalize to pre-training on broader, more diverse web corpora
- A single generic prompt template is used for trajectory generation across all document types — domain-adaptive or automatically optimized prompts are unaddressed, leaving substantial quality improvements unrealized

## Bottlenecks

- Applying thinking trajectory augmentation at trillion-token frontier pre-training scale is blocked by the inference cost of running a capable generation model over the entire corpus — no cost analysis exists and the economics at 10T-token scale are unknown
- Principled selection of the thinking generation model for TPT is blocked by a lack of theoretical understanding of why smaller generators can outperform larger ones — empirical grid search is required for each new application

## Breakthroughs

- Thinking Augmented Pre-Training (TPT) achieves 3× data efficiency in LLM pre-training by augmenting text with automatically generated reasoning trajectories — an 8B model on 100B tokens matches LLaMA-3.1-8B on 15T tokens; post-SFT scores exceed LLaMA-3.1-8B-Instruct on every benchmark
- TPT-trained student models systematically exceed their teacher (the trajectory generation model) on multiple benchmarks — TPT-Qwen2.5-7B surpasses DS-Distill-Qwen-7B on 6 of 10 benchmarks including AIME24 (57.5 vs 53.2) and JEEBench (73.6 vs 49.9)

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/pretraining_data|pretraining_data]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-7b|DeepSeek-R1-Distill-Qwen-7B]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/gsm8k|GSM8K]]
- [[entities/mmlu|MMLU]]
- [[entities/mid-training|Mid-training]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
