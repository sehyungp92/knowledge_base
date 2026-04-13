---
type: source
title: 'LLM Pruning and Distillation in Practice: The Minitron Approach'
source_id: 01KJV8WEM4N2QDRN4NSWYE8XX1
source_type: paper
authors:
- Sharath Turuvekere Sreenivas
- Saurav Muralidharan
- Raviraj Joshi
- Marcin Chochowski
- Ameya Sunil Mahabaleshwarkar
- Gerald Shen
- Jiaqi Zeng
- Zijia Chen
- Yoshi Suhara
- Shizhe Diao
- Chenhan Yu
- Wei-Chun Chen
- Hayley Ross
- Oluwatobi Olabiyi
- Ashwath Aithal
- Oleksii Kuchaiev
- Daniel Korzekwa
- Pavlo Molchanov
- Mostofa Patwary
- Mohammad Shoeybi
- Jan Kautz
- Bryan Catanzaro
published_at: '2024-08-21 00:00:00'
theme_ids:
- finetuning_and_distillation
- model_architecture
- post_training_methods
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# LLM Pruning and Distillation in Practice: The Minitron Approach

This paper adapts and extends NVIDIA's Minitron compression pipeline to handle a critical real-world constraint: the absence of original pretraining data. By introducing a *teacher correction* phase and a downstream-task-based depth-pruning criterion, it demonstrates that structured pruning + knowledge distillation can produce state-of-the-art models at target scales using up to 150× fewer training tokens than training from scratch — and that this is now achievable without proprietary data access.

**Authors:** Sharath Turuvekere Sreenivas, Saurav Muralidharan, Raviraj Joshi, Marcin Chochowski, Ameya Sunil Mahabaleshwarkar, Gerald Shen, Jiaqi Zeng, Zijia Chen, Yoshi Suhara, Shizhe Diao, Chenhan Yu, Wei-Chun Chen, Hayley Ross, Oluwatobi Olabiyi, Ashwath Aithal, Oleksii Kuchaiev, Daniel Korzekwa, Pavlo Molchanov, Mostofa Patwary, Mohammad Shoeybi, Jan Kautz, Bryan Catanzaro
**Published:** 2024-08-21
**Type:** paper
**Source:** https://arxiv.org/pdf/2408.11796

---

## Motivation

Training entire LLM families from scratch at each deployment size is time-, data-, and resource-intensive. Compression via pruning + distillation offers a shortcut, but the standard recipe assumes access to the original pretraining dataset for distillation — an assumption that increasingly fails as frontier models (Llama 3.1, Mistral NeMo) are trained on private corpora.

Without adaptation, applying distillation on a different dataset causes *distribution shift in sub-word token statistics* between the teacher's training data and the distillation data, degrading the quality of the teacher's guidance. A second independent problem: the standard depth-pruning saliency criterion — LM validation loss — turns out to be a poor proxy for downstream task performance.

---

## The Minitron Approach

### Teacher Correction

The central innovation. Before or during distillation, the unpruned teacher model is lightly fine-tuned (~100B tokens) on the target distillation dataset using a low learning rate (one-fifth the original peak LR) with cosine decay. This adapts the teacher's token distribution to the new data without significantly shifting its downstream accuracy.

Effects:
- Reduces LM validation loss of the trained student by **over 6%** compared to distilling from the uncorrected teacher
- Can be performed *concurrently* with distillation (continuously correcting the teacher as the student trains), achieving parity with the sequential approach and enabling further parallelism
- Has minor and inconsistent per-task accuracy effects on the teacher itself — some benchmarks improve, some degrade — meaning it is not a uniform quality booster

The cost is non-trivial: ~100B tokens of fine-tuning compute. Open questions remain about whether LoRA, layer-norm-only tuning, or fewer tokens could achieve equivalent correction.

### Structured Pruning

Activation-based importance estimation is used across all axes simultaneously — depth, neuron, attention head, and embedding channel — using only 1024 calibration samples and forward passes only (no backpropagation). Neural Architecture Search is skipped in favour of manually configured architectures informed by prior NAS findings.

Two pruning strategies are compared at the same 4B parameter budget from Llama 3.1 8B:

| Strategy | What is removed | Depth-pruning criterion |
|---|---|---|
| **Width pruning** | Hidden dim + MLP intermediate dim (attention heads retained) | N/A |
| **Depth pruning** | Contiguous block of middle layers (16–31) | Winogrande accuracy |

The depth-pruning criterion is a direct response to a discovered failure mode: importance-based *non-contiguous* layer removal achieves lower LM validation loss but collapses Winogrande to 0.5 (random chance). Contiguous removal guided by downstream task accuracy scores 0.595.

### Distillation and Alignment

Distillation uses **forward KL divergence on logits only** — no cross-entropy LM loss — with the corrected teacher providing supervision. Post-distillation, alignment proceeds via NeMo-Aligner: math/code SFT → instruction SFT → two rounds of Reward-aware Preference Optimization (RPO).

---

## Results

### Compression Efficiency

| Model | Compressed from | Training tokens | Tokens vs. from-scratch |
|---|---|---|---|
| MN-Minitron-8B | Mistral NeMo 12B | 380B | 40× fewer (vs. Llama 3.1 8B: 15T) |
| Llama 3.1-Minitron-4B | Llama 3.1 8B | 94B | 150× fewer |

### Accuracy: Width vs. Depth Pruning (4B base models)

| Benchmark | Width-pruned | Depth-pruned |
|---|---|---|
| MMLU | 60.5% | 58.7% |
| GSM8K | 41.2% | **16.8%** |
| Winogrande | — | 59.5% |

Width pruning consistently outperforms depth pruning, and the gap is severe for multi-step reasoning in base models. After instruction tuning, the gap narrows substantially — but depth pruning still underperforms.

### Inference Throughput (single H100 80GB, TensorRT-LLM, FP8)

- Depth-pruned 4B: **2.7× speedup** vs. Llama 3.1 8B (larger batch size from reduced memory footprint drives additional gains)
- Width-pruned 4B: **1.8× speedup** vs. Llama 3.1 8B
- FP8 vs. BF16 alone: **1.4× speedup**

### Student Surpassing Teacher

MN-Minitron-8B, compressed from Mistral NeMo 12B, *exceeds its teacher* on two benchmarks after distillation:

| Benchmark | Teacher (12B) | Student (8B) |
|---|---|---|
| GSM8K | 55.7% | **58.5%** |
| HumanEval | 23.8% | **36.2%** |

Attributed to the curated composition of the distillation dataset rather than a compression artefact. This is an important nuance: the distillation dataset shapes not just sample efficiency but final capability profile.

---

## Limitations and Open Questions

**Perplexity ≠ task performance for depth pruning.** LM validation loss is a structurally unreliable saliency criterion. Non-contiguous layer removal that minimises validation loss produces random-chance Winogrande scores — a stark dissociation that should raise caution about using PPL-based metrics for any architectural compression decision. See [[themes/scaling_laws|Scaling Laws]] for related questions about what loss predicts.

**Depth pruning damages reasoning.** The 16.8% vs. 41.2% GSM8K gap for base 4B models is not a marginal accuracy difference — it is a near-collapse of multi-step reasoning capability. Depth-pruned models may require substantially more instruction tuning to recover this capability, and the recovery mechanism is not explained. See [[themes/finetuning_and_distillation|Finetuning and Distillation]].

**Coding capability resists compression.** Aligned compressed models underperform on HumanEval and MBPP relative to similarly-sized competitors, and the depth-pruned 4B base model has no HumanEval result reported at all — a conspicuous absence suggesting the capability collapsed below reportable thresholds.

**Teacher correction cost is unsolved.** ~100B tokens is non-trivial. Whether LoRA, layer-norm-only fine-tuning, or fewer tokens can achieve equivalent distribution alignment is explicitly flagged as future work. Until cheaper correction methods are validated, the pipeline's accessibility is limited.

**Industrial-scale hardware requirement.** The distillation pipeline uses 32 NVIDIA DGX H100 nodes — hardware inaccessible to most researchers. Despite open-sourcing model weights, the *process* of producing them is practically restricted to well-resourced labs. This creates an asymmetry between open weights and reproducible methodology.

**No safety evaluation.** Compressed and re-aligned models are open-sourced with permissive licenses, but no safety, adversarial robustness, or alignment evaluation is reported. Compression and RPO alignment may alter safety properties relative to the teacher in undercharacterised ways.

**NAS skipped.** Manual architecture configuration was used. The paper notes this likely means reported accuracy results underrepresent the achievable ceiling.

---

## Bottleneck Implications

### Proprietary pretraining data blocking distillation

Teacher correction is a direct engineering response to an accelerating bottleneck: frontier models increasingly trained on private corpora are blocking standard distillation pipelines. The technique decouples compression from data provenance, making it applicable to *any* open-weight model regardless of training data accessibility. This partially dissolves a bottleneck that was on a worsening trajectory — but 100B tokens of correction compute remains a meaningful barrier. See [[themes/pretraining_and_scaling|Pretraining and Scaling]].

### Absence of reliable proxy metrics for pruning decisions

The failure of LM validation loss as a saliency criterion for depth pruning is a concrete instance of the broader problem: there is no cheap, reliable proxy that predicts downstream task accuracy for structural pruning choices. The paper's solution — using Winogrande accuracy directly — is expensive and task-specific. This bottleneck remains open and blocks automated, compute-efficient pruning pipelines.

---

## Key Methodological Findings

1. **Teacher correction is necessary, not optional.** Without it, distillation on a different dataset is sub-optimal due to sub-word token distribution shift. The 6%+ validation loss reduction from correction is not marginal.

2. **Concurrency is viable.** Teacher correction and distillation can run in parallel without accuracy cost, enabling more efficient pipeline scheduling.

3. **Contiguous > non-contiguous for depth pruning.** Middle layers (16–31 in Llama 3.1 8B) are the least important. Beginning and end layers are most critical for LM validation loss. Non-contiguous importance-based selection that appears better by PPL is actually worse on tasks.

4. **Width pruning preserves reasoning better than depth pruning.** Retain attention heads; prune MLP intermediate dimension and embedding channels instead of removing layers when accuracy is the priority.

5. **Logit-only KD with forward KL is optimal.** No cross-entropy LM loss component is needed.

---

## Connections

- [[themes/finetuning_and_distillation|Finetuning and Distillation]] — teacher correction as a new phase in the distillation pipeline; logit-only KD design choices
- [[themes/model_architecture|Model Architecture]] — width vs. depth pruning tradeoffs; transformer layer importance distribution
- [[themes/post_training_methods|Post-Training Methods]] — RPO alignment of compressed models; instruction tuning recovery of pruned capabilities
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — the 40–150× token efficiency gain reframes the cost structure of maintaining model families at scale
- [[themes/scaling_laws|Scaling Laws]] — the perplexity/task-accuracy dissociation challenges the assumption that LM loss is a universal quality proxy

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/ifeval|IFEval]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/lora|LoRA]]
- [[entities/mmlu|MMLU]]
- [[entities/mt-bench|MT-Bench]]
