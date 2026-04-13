---
type: source
title: 'LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures'
source_id: 01KJTJSM72XD56VFSEYRBBZE46
source_type: paper
authors:
- Hai Huang
- Yann LeCun
- Randall Balestriero
published_at: '2025-09-11 00:00:00'
theme_ids:
- finetuning_and_distillation
- model_architecture
- post_training_methods
- pretraining_and_scaling
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures

**Authors:** Hai Huang, Yann LeCun, Randall Balestriero
**Published:** 2025-09-11 00:00:00
**Type:** paper

## Analysis

# LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures
2025-09-11 · paper · Hai Huang, Yann LeCun, Randall Balestriero
https://arxiv.org/pdf/2509.14252

---

### Motivation & Prior Limitations
- LLM pretraining and finetuning rely exclusively on input-space reconstruction (next-token prediction via cross-entropy), yet in vision, embedding-space objectives — specifically Joint Embedding Predictive Architectures (JEPAs) — have been shown to be provably superior to their input-space counterparts for perception and reasoning tasks.
  - Input-space reconstruction objectives are known to introduce biases not present in embedding-space alternatives, and prior work on vision (I-JEPA, V-JEPA) demonstrated measurable benefits for knowledge discovery that have no equivalent in language.
- The standard autoregressive training objective does not implicitly minimize a JEPA-style embedding alignment term: controlled experiments show that minimizing cross-entropy loss leaves the JEPA prediction loss (cosine distance between Text and Code embeddings) entirely unchanged, confirming the two objectives are orthogonal.
  - This means the representational structure that JEPA induces — alignment of semantically equivalent views in embedding space — is simply not a consequence of standard LLM training, leaving a structural gap in learned representations.
- Existing embedding-space regularizers for LLMs (e.g., SimCSE, hierarchical cluster-based constraints) either sacrifice generative capabilities entirely or impose structural priors that fall outside the JEPA framework.
  - SimCSE and related methods produce strong sentence embeddings but cannot be used for generation, limiting their applicability to the dominant evaluation paradigm where models are judged on generated output.

---

### Proposed Approach
- LLM-JEPA introduces a composite training objective that combines the standard autoregressive LLM loss with a JEPA term operating in embedding space: `L_LLM-JEPA = Σ L_LLM(Text_{1:ℓ-1}, Text_ℓ) + λ × d(Pred(Enc(Text)), Enc(Code))`, where the JEPA term pulls the predicted embedding of Text toward the actual embedding of Code without modifying the generative pathway.
  - The key insight is to treat (Text, Code) pairs — natural language to regex, NL to SQL, question to answer, issue to code diff — as two views of the same underlying knowledge, directly mirroring how vision JEPAs treat different augmentations of the same image.
  - The predictor is implemented via tied weights: a special `[PRED]` token (or k such tokens) is appended to the input, and the embedding of the last predictor token serves as `Pred(Enc(·))`, reusing the LLM's own self-attention without any additional parameters beyond the token itself.
- The encoder uses the hidden state of the last token from the last layer as the sequence embedding, and a custom block-causal attention mask ensures Text and Code embeddings are computed independently in a single additional forward pass — preventing cross-contamination between views while avoiding a full third forward pass.
  - The mask sets attention entries between the two view blocks to −∞, so each view attends only causally within itself; the implementation requires only one extra forward pass (two total) rather than three separate passes.
- The cosine similarity is used as the distance metric d, and the hyperparameter λ balances the generative and JEPA terms; k predictor tokens (k ∈ {0,1,2,3,4}) control predictor capacity.

---

### Results & Capabilities
- LLM-JEPA consistently outperforms standard next-token-prediction finetuning across four model families (Llama-3.2-1B-Instruct, gemma-2-2b-it, OpenELM-1.1B-Instruct, OLMo-2-0425-1B-Instruct), four datasets (NL-RX-SYNTH, NL-RX-TURK, GSM8K, Spider), and model sizes from 1B to 8B parameters.
  - Representative gains on NL-RX-SYNTH: Llama3 baseline 37.0% → LLM-JEPA 51.6%; gemma2 baseline 11.5% → 20.2%; OpenELM baseline 51.3% → 66.6%. On Spider (NL→SQL): Llama3 baseline 19.4% → 27.2%. On GSM8K: Llama3 baseline 56.0% → 70.4%.
- LLM-JEPA exhibits markedly lower overfitting than standard finetuning, maintaining accuracy improvements across all six measured training epochs while the baseline degrades after peak performance.
  - This resistance to overfitting holds in both full finetuning and LoRA settings across all tested LoRA ranks.
- The JEPA objective induces measurably structured representations: t-SNE plots show tight, well-separated Text/Code clusters after LLM-JEPA finetuning versus disordered overlap under standard finetuning, and SVD analysis of `Enc(Text) − Enc(Code)` shows singular values several orders of magnitude lower, confirming the view-to-view mapping is confined to a narrow near-linear subspace.
- LLM-JEPA extends beyond (Text, Code) pairs: statistically significant improvements are observed on NQ-Open (20.12% → 21.59%, p=2.44e-3) and HellaSwag (69.40% → 70.51%, p=0.0136), and on reasoning models Qwen3-1.7B (44.32% → 45.00%) and DeepSeek-R1-Distill-Qwen-1.5B (13.87% → 15.04%) on GSM8K.
- Loss dropout (LD) at rates of 0.5–0.75 reduces compute to 1.25–1.5× the baseline cost while preserving or exceeding the accuracy of full LLM-JEPA, with the empirical guideline `λ × (1 − α) ≈ constant` for co-tuning dropout rate and loss weight.
  - At LD=0.75 with λ=4, the model achieves 73.08% on NL-RX-SYNTH (vs. 63.96% for full LLM-JEPA at LD=0, λ=1, at the same PFLOP budget), suggesting aggressive dropout with compensated λ can outperform the standard JEPA objective.
- Preliminary pretraining experiments show LLM-JEPA also benefits from-scratch training: on NL-RX-SYNTH, pretraining accuracy improves from 54.38% ± 1.70 (NTP) to 60.59% ± 1.01 (LLM-JEPA), with p=2.94e-4. JEPA pretraining on paraphrases (cestwc/paraphrase) also yields statistically significant improvements on downstream Rotten Tomatoes and Yelp sentiment classification after standard finetuning without JEPA.

---

### Implications
- The paper establishes a proof of

## Key Claims

1. In vision, embedding-space training objectives (JEPAs) are far superior to their input-space counterparts for representation learning.
2. LLM-JEPA outperforms standard LLM fine-tuning across four model families (Llama3, Gemma2, OpenELM, OLMo) and four datasets (NL-RX-SYNTH, NL-RX-TURK, GSM8K, Spider).
3. LLM-JEPA is more resistant to overfitting than standard fine-tuning across six training epochs.
4. Minimizing the standard next-token prediction LLM loss does not implicitly minimize the JEPA prediction loss, indicating the JEPA term must be explicitly added during training.
5. Adding the JEPA term to LLM training does not degrade next-token prediction capability.
6. LLM-JEPA only adds structure to the LLM latent space without altering its generative capabilities.
7. LLM-JEPA constrains the mapping from Enc(Text) to Enc(Code) within a narrow subspace, producing significantly smaller singular values in the SVD decomposition of Enc(Text) − Enc(Code) compared to base
8. For Llama-3.2-1B-Instruct on NL-RX-SYNTH fine-tuning, LLM-JEPA achieves 51.6% accuracy versus 37.0% for the baseline.
9. For Llama-3.2-1B-Instruct on GSM8K fine-tuning, LLM-JEPA achieves 70.4% accuracy versus 56.0% for the baseline.
10. LLM-JEPA improves pretraining quality: on NL-RX-SYNTH pretraining from random initialization, LLM-JEPA achieves 60.59% ± 1.01 accuracy versus 54.38% ± 1.70 for the next-token prediction baseline.

## Capabilities

- JEPA-based fine-tuning objective for LLMs (LLM-JEPA) that operates in embedding space and significantly outperforms standard next-token prediction fine-tuning while maintaining full generative capabilities, validated across four model families (Llama3, Gemma2, OpenELM, OLMo) and four datasets
- LLM-JEPA induces a near-linear, low-rank transformation between text and code embedding spaces, measurably structuring the LLM's latent space without altering its generative output quality
- LLM fine-tuning with JEPA objective exhibits systematic resistance to overfitting across training epochs while standard fine-tuning degrades, demonstrated across multiple model families and dataset sizes
- Random JEPA-loss dropout (LD) during LLM-JEPA training reduces per-epoch compute to as low as 1.25× standard fine-tuning cost while maintaining or exceeding full LLM-JEPA accuracy at equal FLOP budgets
- LLM-JEPA fine-tuning improves accuracy of dedicated reasoning models (Qwen3-1.7B, DeepSeek-R1-Distill) on math benchmarks (GSM8K), demonstrating JEPA's benefits extend to models already optimised via RL-based reasoning pipelines
- LLM-JEPA adds zero inference-time overhead — the JEPA term requires only one extra forward pass during training and disappears entirely at inference

## Limitations

- LLM-JEPA requires datasets with natural two-view structures (e.g., text–code pairs); applying it to arbitrary datasets requires a view-generation mechanism analogous to data augmentation in vision, which does not yet exist
- LLM-JEPA training incurs a 2× compute cost relative to standard fine-tuning due to the extra forward pass required to obtain independent view embeddings
- LLM-JEPA introduces two additional hyperparameters (λ, k) with no principled tuning strategy; optimal values vary unpredictably across tasks and models, requiring expensive grid search
- LLM-JEPA pretraining at full scale remains unvalidated; all pretraining experiments use small, domain-limited datasets and authors explicitly plan future scaling work
- All experiments test models only up to 8B parameters; whether LLM-JEPA accuracy gains, compute-overhead trade-offs, and hyperparameter dynamics hold at 70B+ scale is entirely unexamined
- LLM-JEPA pretraining from random weights fails to learn robust generation termination on small datasets, requiring a relaxed evaluation criterion (prefix matching instead of exact match)
- LLM-JEPA performance gains are substantially smaller on open-domain QA tasks (NQ-Open: +1.5pp, HellaSwag: +1.1pp) compared to structured view-pair tasks (NL-RX: +14–20pp), suggesting gains degrade as the relationship between views becomes less semantically tight
- Replacing cosine similarity with InfoNCE loss causes catastrophic performance collapse (34.40% ± 6.10 vs. 71.46% ± 1.34 baseline accuracy) with greatly increased variance, revealing extreme sensitivity of LLM-JEPA to the choice of similarity metric
- The JEPA term contributes zero implicit regularisation under standard next-token prediction training — minimising the LLM loss does not reduce the JEPA prediction loss — confirming that embedding-space and token-space objectives are orthogonal and cannot substitute for each other
- LLM-JEPA has not been tested on multimodal inputs, temporal sequences, or non-English/non-code modalities; all evaluations are English text paired with code or structured language

## Bottlenecks

- Absence of a principled view-generation mechanism for language data blocks LLM-JEPA from being applied to arbitrary pretraining corpora — only datasets with inherent dual-view structure (code/text, NL/SQL) are currently usable
- 2× training compute cost of LLM-JEPA (extra masked forward pass per batch) blocks practical adoption for large-scale LLM pretraining, even though loss dropout partially mitigates this at fine-tuning scale
- Lack of principled or efficient hyperparameter search for LLM-JEPA's (λ, k) pair blocks reliable deployment — current approach requires full 2D grid search, multiplying fine-tuning cost significantly

## Breakthroughs

- First successful adaptation of JEPA (Joint Embedding Predictive Architecture) objectives to LLMs, demonstrating that embedding-space training — previously exclusive to vision — can be applied to language fine-tuning and pretraining with consistent, significant accuracy gains without sacrificing gene

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/representation_learning|representation_learning]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/gsm8k|GSM8K]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/lora|LoRA]]
