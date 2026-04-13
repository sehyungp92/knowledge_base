---
type: source
title: 'TokenFormer: Rethinking Transformer Scaling with Tokenized Model Parameters'
source_id: 01KJV749E6WKMFMYWCX4C8G0XN
source_type: paper
authors:
- Haiyang Wang
- Yue Fan
- Muhammad Ferjad Naeem
- Yongqin Xian
- Jan Eric Lenssen
- Liwei Wang
- Federico Tombari
- Bernt Schiele
published_at: '2024-10-30 00:00:00'
theme_ids:
- model_architecture
- pretraining_and_scaling
- representation_learning
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# TokenFormer: Rethinking Transformer Scaling with Tokenized Model Parameters

TokenFormer proposes replacing all linear projections in Transformers with a cross-attention mechanism called Pattention, where model parameters are treated as learnable tokens. This architectural shift decouples parameter count from channel dimension width, enabling progressive model scaling by appending new key-value parameter pairs to existing checkpoints — achieving ~10x per-stage compute reduction and competitive performance with from-scratch baselines up to 1.4B parameters.

**Authors:** Haiyang Wang, Yue Fan, Muhammad Ferjad Naeem, Yongqin Xian, Jan Eric Lenssen, Liwei Wang, Federico Tombari, Bernt Schiele
**Published:** 2024-10-30
**Type:** paper
**Themes:** [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/scaling_laws|Scaling Laws]], [[themes/transformer_alternatives|Transformer Alternatives]], [[themes/representation_learning|Representation Learning]]

---

## Expert Analysis

### Motivation & Prior Limitations

Standard Transformer scaling is bottlenecked by its fixed linear projections: model capacity is bound to architectural hyperparameters like channel dimension, so any capacity increase forces full retraining from scratch at substantial compute cost. Each new model size in the standard paradigm (GPT series, Pythia) requires an entirely fresh training run — cumulative costs grow unsustainably as target model sizes increase.

Prior model reuse methods partially address this but introduce their own problems. Weight duplication (Net2Net), stacking, and combining approaches disturb the pre-established distribution of the smaller model, risking knowledge loss and slow convergence from the disrupted initialization. Scaling channel dimensions also worsens long-context efficiency independently: token-token attention scales quadratically with sequence length and linearly with model width, so larger models are disproportionately expensive for long sequences.

### The Pattention Layer

TokenFormer replaces every linear projection with a **token-Parameter attention (Pattention)** layer. Input tokens serve as queries; a set of learnable parameter tokens serve as keys and values. This cross-attention computes what was previously a fixed matrix multiply — but over a variable-length parameter set, making parameter count independent of channel dimension.

The standard softmax causes gradient instability in this setting. The authors replace it with a modified variant: **L2 normalization** (replacing L1) combined with **GeLU activation** (replacing the exponential). Ablations show this yields +2.1 points on ImageNet from the GeLU substitution and a further +1.2 points from L2 normalization. Layer normalization is made non-parametric (learnable scale/bias removed) to allow independently trained parameter token sets to be merged cleanly in future multi-modal settings.

### Progressive Scaling

Scaling proceeds by appending new key-value parameter token pairs to each Pattention layer, concatenated with existing pre-trained tokens along the token dimension. All other computations and channel dimensions remain unchanged. New key parameters are initialized to **zero**, new value parameters to **random values** — analogous to LoRA initialization — preserving the output distribution at the start of each scaling step and enabling fast convergence from prior training.

This decouples the parameter count axis from the channel dimension axis. Increasing model size via the parameter-token axis keeps `d_token` constant, which means token-token attention costs do not grow with model scale — a compounding advantage at longer sequence lengths.

### Results

**Language modeling (Pile, 300B tokens):**

| Model | Params | Perplexity | Training cost |
|---|---|---|---|
| Transformer (scratch) | 1.4B | 11.63 | Full 300B tokens |
| TokenFormer (progressive) | 1.4B | 11.77 | ~3× lower cumulative |
| Transformer (30B budget) | 1.4B | 13.34 | 30B tokens |
| TokenFormer (30B budget) | 1.4B | **11.77** | 30B tokens |

Each incremental scaling step required only ~30B additional tokens versus ~300B for a from-scratch baseline — roughly one-tenth the per-stage compute. Under matched 30B-token compute, progressively scaled TokenFormer substantially outperforms a same-size Transformer trained from scratch.

**Zero-shot benchmarks (LAMBADA, HellaSwag, PIQA, Arc-E, Arc-C, WinoGrande):**
TokenFormer-1.5B achieves 59.3% average accuracy versus Pythia-1.3B at 55.2%, OPT-1.3B at 55.0%, and GPT-Neo 1.3B at 52.4% — all trained on equivalent data.

**Vision (ImageNet-1K, MAE-style):**
TokenFormer-B/16 reaches 82.5% top-1 (vs. ViT-B/16 MAE at 82.3%); TokenFormer-L/16 reaches 83.1% (vs. ViT-L/16 MAE at 82.6%). This confirms expressiveness parity with standard ViT despite architectural differences, at the cost of ~27% parameter overhead (109M vs. 86M for B/16).

**Scaling baseline comparison:**
Against Net2Net-based scaling (both expanded from 354M to 757M on enwik8), TokenFormer converges faster and reaches lower final loss — attributed to the distribution-preserving zero initialization of new key tokens.

---

## Capabilities

- **Incremental parameter scaling** from 124M to 1.4B by appending key-value parameter token pairs to existing checkpoints, without retraining from scratch *(research only)*
- **~10x per-stage compute reduction** for each scaling step versus full from-scratch baselines, with comparable final perplexity *(research only)*
- **Decoupled long-context scaling**: holding `d_token` constant as model grows means token-token attention costs do not increase with model size, yielding increasingly favorable FLOPs at long sequence lengths *(research only)*
- **Distribution-preserving expansion**: zero-initialized new key tokens preserve existing output distribution, enabling fast convergence when incorporating new data *(research only)*
- **Competitive performance** on both language (zero-shot NLP benchmarks) and vision (ImageNet classification) tasks versus same-scale baselines *(research only)*

---

## Limitations & Open Questions

**Scale ceiling unknown.** All experiments top out at 1.4B parameters. Whether incremental scaling holds at frontier scale (10B–100B+) is entirely untested. The architecture's claims depend on this extrapolation being valid.

**First run still full cost.** The initial base model must be trained from scratch on the full pretraining corpus (~300B tokens). No savings accrue on the first training run — the efficiency gains only compound across subsequent scaling stages.

**Quadratic attention unchanged.** Token-token self-attention remains O(T²) in compute and memory. TokenFormer decouples *parameter scaling* from sequence cost but does not reduce the quadratic bottleneck itself. This is a separate, unsolved problem.

**Modified softmax as ecosystem friction.** Standard softmax causes gradient instability in Pattention, requiring the custom L2 + GeLU variant. This non-trivial departure from standard attention may complicate integration with existing frameworks and inference kernels.

**Vision-language integration unimplemented.** Merging visual and language Pattention parameter token sets is explicitly listed as future work. The theoretical path exists (non-parametric layer norms enable clean merging), but no experiments validate it.

**Benchmark scope.** All evaluations use standard academic benchmarks at 1024-token context. No real-world deployment, production stress testing, or long-context evaluation beyond training length is reported.

**Parameter overhead.** TokenFormer carries ~27% more parameters than equivalent-dimension ViT models. This is minor but relevant when comparing parameter counts directly.

**MoE efficiency unrealized.** The authors interpret Pattention as an extreme MoE instantiation (each key-value pair as an expert), suggesting sparsity techniques could reduce token-parameter interaction costs. This is not implemented or benchmarked.

**Interpretability claim unverified.** Theoretical interpretability benefits of parameter-as-token design are asserted but no mechanistic analysis or attention-pattern visualizations over parameter tokens are provided.

---

## Implications & Connections

**Foundation model growth model.** TokenFormer opens a qualitatively different scaling axis — additive and non-destructive — suggesting a paradigm where foundation models are grown continuously rather than retrained discretely. This has direct implications for the economics of [[themes/pretraining_and_scaling|pretraining]]: if checkpoints can be reused across scale steps, the effective cost curve for reaching frontier scale changes significantly.

**Modular multi-modal architectures.** Non-parametric layer norms plus mergeable parameter token sets suggest a principled mechanism for building vision-language models from independently trained unimodal components, followed by alignment tuning. This is structurally distinct from current approaches (joint pretraining or adapter fusion).

**Relationship to MoE.** The Pattention layer is interpretable as an MoE with dense routing over all key-value "experts." This suggests MoE sparsity techniques (top-k gating, load balancing) could be directly applied to reduce token-parameter interaction costs in future work — connecting this architecture to the [[themes/model_architecture|sparse architecture]] literature.

**Relationship to LoRA.** The zero/random initialization scheme for new parameter tokens is structurally analogous to LoRA-style delta initialization. This suggests TokenFormer progressive scaling could be viewed as a continual learning analog of parameter-efficient fine-tuning, with implications for how [[themes/pretraining_and_scaling|checkpoint reuse]] is theorized more broadly.

---

## Key Claims

1. Standard Transformer scaling requires full retraining from scratch when architectural components like channel dimensions are modified — costs scale unsustainably.
2. Pattention replaces all linear projections with cross-attention over learnable parameter tokens, decoupling parameter count from channel dimension.
3. Progressive scaling appends new key-value parameter pairs to existing checkpoints, requiring only ~30B tokens per stage versus ~300B for from-scratch baselines.
4. Under matched 30B-token compute, TokenFormer (11.77 perplexity) substantially outperforms a same-size from-scratch Transformer (13.34 perplexity).
5. Cumulative training cost for scaling 124M → 1.4B is reduced by more than 3× versus training each size from scratch.
6. Modified softmax (L2 normalization + GeLU) is necessary for gradient stability in Pattention; standard softmax causes diminished gradients.
7. Net2Net-style scaling disturbs the pre-trained distribution; TokenFormer's zero-initialization of new key tokens preserves it, yielding faster convergence.
8. TokenFormer-1.5B achieves 59.3% average zero-shot accuracy versus Pythia-1.3B at 55.2% on equivalent training data.
9. `d_token` held constant during scaling means token-token attention cost does not grow with model size, providing long-context efficiency advantages.
10. Vision-language integration via parameter token merging is theoretically enabled by non-parametric layer norms but remains unimplemented.

## Key Concepts

- [[entities/imagenet-1k|ImageNet-1K]]
- [[entities/lora|LoRA]]
- [[entities/perplexity|Perplexity]]
