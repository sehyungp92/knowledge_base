---
type: source
title: 'OpenVLA: An Open-Source Vision-Language-Action Model'
source_id: 01KJV8JK292KN8R7YPV9Y8P533
source_type: paper
authors:
- Moo Jin Kim
- Karl Pertsch
- Siddharth Karamcheti
- Ted Xiao
- Ashwin Balakrishna
- Suraj Nair
- Rafael Rafailov
- Ethan Foster
- Grace Lam
- Pannag Sanketi
- Quan Vuong
- Thomas Kollar
- Benjamin Burchfiel
- Russ Tedrake
- Dorsa Sadigh
- Sergey Levine
- Percy Liang
- Chelsea Finn
published_at: '2024-06-13 00:00:00'
theme_ids:
- finetuning_and_distillation
- multimodal_models
- post_training_methods
- robotics_and_embodied_ai
- robot_learning
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# OpenVLA: An Open-Source Vision-Language-Action Model

OpenVLA introduces a 7B-parameter open-source vision-language-action model trained end-to-end on 970k real-world robot demonstrations from the Open X-Embodiment dataset. By releasing model weights, training code, and fine-tuning notebooks, it breaks open the previously closed VLA research landscape — and demonstrates that a carefully trained 7B open model can outperform the closed 55B RT-2-X by 16.5% absolute success rate across 29 tasks, while enabling consumer-GPU fine-tuning via LoRA and quantized inference at 15GB memory footprint.

**Authors:** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, Chelsea Finn
**Published:** 2024-06-13
**Type:** paper
**Themes:** [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]] · [[themes/vision_language_action_models|Vision-Language-Action Models]] · [[themes/multimodal_models|Multimodal Models]] · [[themes/finetuning_and_distillation|Finetuning & Distillation]] · [[themes/post_training_methods|Post-Training Methods]]

---

## Motivation

Prior learned robot manipulation policies generalize poorly under distribution shift. They can extrapolate to new initial conditions — varied object positions, lighting — but break when the scene composition changes, novel objects appear, or task instructions fall outside the training distribution. Internet-scale VLMs do not share this brittleness, which motivates the VLA paradigm: fine-tune a pretrained VLM to predict robot actions.

The VLA paradigm had already been explored, most notably in RT-2, but **the entire leading VLA space was closed-source**. RT-2-X (55B parameters) offered no public weights, no training methodology, no data mixture details. This blocked reproducibility and locked community research out of the most promising direction in generalist robot learning. Meanwhile, prior generalist policies like Octo composed pretrained components with scratch-initialized modules, foregoing the full benefit of end-to-end VLM initialization — and no prior work investigated efficient fine-tuning strategies for adapting VLAs to new robots on consumer hardware.

A compounding structural problem: even the largest robot manipulation datasets contain only 100K–1M demonstrations, sitting 3–4 orders of magnitude below the internet-scale data that trained the VLM backbones. This imbalance creates both an opportunity (leverage existing foundation models) and a persistent bottleneck (robot data is a fundamental constraint on generalization ceiling).

---

## Approach

### Architecture

OpenVLA builds on Prismatic-7B, a visually-conditioned LLM with a **fused two-encoder visual backbone**: DINOv2 patch embeddings (spatial, low-level) and SigLIP patch embeddings (semantic, high-level) concatenated channel-wise, then projected into the Llama 2 7B input space via a 2-layer MLP. This fusion is critical — comparisons show that single-encoder approaches lose spatial reasoning quality that matters for visuomotor control. SigLIP alone was insufficient; the DINOv2 component provides the positional grounding that manipulation requires.

### Action Tokenization

Actions are represented as language tokens by discretizing each robot action dimension independently into 256 bins using **1st–99th percentile quantile bounds** — not min-max bounds, which are sensitive to outliers. The 256 bins are mapped to the 256 least-used tokens in the Llama tokenizer vocabulary, overwriting them. Training uses standard next-token prediction cross-entropy loss evaluated only on action tokens.

This design choice — treating robot actions as vocabulary tokens — makes the entire training pipeline identical to VLM fine-tuning, enabling direct reuse of LLM infrastructure and making the VLA a direct beneficiary of any future improvements in language model training.

### Training

The model is trained on Open X-Embodiment data using Octo's mixture weights, which heuristically up-weight datasets with higher task and scene diversity. One notable casualty of the training run: **the DROID dataset was removed** for the final training third after action token accuracy remained persistently low throughout training, suggesting DROID requires either a substantially larger model or a higher mixture weight than the current 7B scale can accommodate. This is a meaningful signal about where current VLA capacity actually sits.

A critical finding is that **the vision encoder must be fine-tuned end-to-end** — frozen pretrained features are insufficient for visuomotor control. This negates the compute savings of frozen encoder strategies that work well in VLM fine-tuning. It also implies that VLA training is qualitatively different from standard VLM fine-tuning: the model trained for 27 epochs until action token accuracy exceeded 95%, compared to the 1–2 epochs standard for VLM runs.

Final training: 64 A100 GPUs × 14 days = **21,500 A100-hours**. This is a significant but not prohibitive compute cost for an institution — and critically, the open release means the community can adapt the trained model without repeating it.

### Efficient Adaptation

OpenVLA demonstrates LoRA fine-tuning and quantized inference on consumer hardware for the first time in the VLA setting. Fine-tuning is feasible on a single consumer-grade GPU. Inference runs at 15GB memory in bfloat16 on an RTX 4090; quantization reduces this footprint without measurable real-world task success degradation. A remote inference server is also provided to decouple compute from the robot platform.

---

## Results

| Comparison | Result |
|---|---|
| OpenVLA (7B) vs. RT-2-X (55B) | +16.5% absolute success rate across 29 tasks |
| Fine-tuned OpenVLA vs. Diffusion Policy | +20.4% absolute on multi-task multi-object language grounding |
| Fine-tuned OpenVLA vs. fine-tuned Octo | Clear win across 7 evaluated manipulation tasks |
| Prismatic backbone vs. LLaVA backbone | ~+10% absolute on single-object and multi-object grounding |
| LLaVA backbone vs. IDEFICS-1 | +35% absolute on multi-object language grounding tasks |

The backbone selection result is striking: **VLM backbone quality has an enormous effect on language grounding**. The jump from IDEFICS-1 to LLaVA is 35 percentage points. This confirms that the language grounding capability inherited from VLM pretraining is not a fixed benefit — it scales with the quality of the underlying model, and the choice of VLM backbone is a first-order decision in VLA design.

The one category where OpenVLA loses to RT-2-X: **semantic generalization** (novel objects, unseen internet concepts, instructions outside the training distribution). RT-2-X, despite its scale disadvantage on most axes, retains an edge here — likely because 55B parameters more thoroughly encode internet-scale semantic knowledge.

---

## Capabilities

- **Generalist manipulation at 7B scale** — outperforms a 55B closed model across 29 tasks and multiple embodiments (maturity: *demo*)
- **Consumer-GPU fine-tuning via LoRA** — first demonstrated LoRA + quantization pipeline for VLAs; adaptation no longer requires server clusters (maturity: *demo*)
- **Quantized inference without performance loss** — 15GB → significantly reduced footprint; RTX 4090 sufficient for real-world deployment (maturity: *demo*)
- **Multi-embodiment control out of the box** — single policy controls multiple distinct robot embodiments without per-embodiment retraining (maturity: *demo*)
- **Language-conditioned multi-task manipulation** — strong grounding in multi-object environments; +20.4% over from-scratch Diffusion Policy (maturity: *demo*)

---

## Limitations & Open Questions

**Inference speed** is the most immediate deployment constraint. OpenVLA runs at ~6Hz on an RTX 4090 with no inference optimization applied (no speculative decoding, no compilation). This is structurally below the 30–50Hz threshold for reactive real-time control. The VLA paradigm as currently implemented is limited to slow-paced, quasi-static manipulation. Speculative decoding and model compilation are natural next steps, but their viability for action token sequences with strict temporal coupling has not been established.

**Semantic generalization gap** is an unresolved weakness. RT-2-X's residual advantage in this category suggests that parameter scale is not simply wasteful — it encodes internet-scale semantic knowledge that a 7B model cannot fully replicate. As VLA datasets remain narrow relative to VLM training data, this gap may persist.

**Dataset diversity at current scale** is a hard constraint. The DROID dataset — one of the highest-diversity robot datasets available — could not be integrated at 7B scale. Action token accuracy never converged. This is not a training procedure failure; it is a signal that model capacity and data diversity are mismatched. Scaling the model or the mixture weight is required before high-diversity datasets can be productively absorbed.

**Vision resolution provides no benefit** in the VLA setting. 384×384 input — which yields gains on VLM benchmarks — showed no improvement over 224×224 on robot tasks while taking 3x longer to train. This suggests VLA architectures are not yet capable of exploiting additional visual detail, possibly because the action token bottleneck or the dataset size makes fine-grained visual distinctions non-predictive of task success.

**Sensor and embodiment scope** is narrow by design. Training is restricted to single-arm end-effector control with at least one third-person camera. Bimanual manipulation, mobile robotics, proprioception, depth, and tactile inputs are all out of scope. The authors acknowledge this explicitly as future work.

**End-to-end encoder fine-tuning is required** — frozen encoder strategies do not work. This eliminates the standard compute-saving approach from VLM fine-tuning and means full VLA training is heavier than expected.

**Data efficiency is fundamentally lower** than VLM training. 27 epochs vs. 1–2 epochs standard for VLMs suggests that visuomotor action prediction from demonstrations is a harder signal to learn from, and that the robot data regime requires qualitatively different training assumptions.

---

## Significance

OpenVLA's primary contribution is not a single technical innovation but a **structural shift in who can do VLA research**. By open-sourcing a model that outperforms the prior closed state-of-the-art at 7x smaller scale, and by demonstrating consumer-GPU adaptation via LoRA, the paper removes two barriers simultaneously: the barrier to studying VLA behavior (no weights previously available) and the barrier to adapting VLAs to new tasks (previously required large-scale GPU infrastructure).

The VLA paradigm itself — actions as language tokens, end-to-end VLM fine-tuning — creates a **direct inheritance channel** from future VLM and LLM progress to robot control. Any improvement in language models, visual encoders, or VLM training procedures becomes automatically applicable to VLA policies without architectural redesign. This is a structural advantage that from-scratch robot learning approaches do not share.

The result that data quality and architecture quality can substitute for parameter scale (7B > 55B) is consistent with emerging patterns in LLM research, but the robotics context makes it particularly significant given the cost of acquiring robot demonstration data.

---

## Connections

- [[themes/vision_language_action_models|Vision-Language-Action Models]] — OpenVLA is the first open-source competitive entrant in this space, establishing the baseline the community will build on
- [[themes/finetuning_and_distillation|Finetuning & Distillation]] — LoRA adaptation for VLAs opens parameter-efficient fine-tuning as a standard robotics workflow
- [[themes/multimodal_models|Multimodal Models]] — the DINOv2 + SigLIP fusion finding has implications for visual encoder design beyond robotics
- [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]] — the data scale gap (100K–1M vs. trillions of tokens) frames the central open problem for the field
- [[themes/post_training_methods|Post-Training Methods]] — the 27-epoch finding challenges assumptions about data efficiency inherited from VLM fine-tuning practice

## Key Concepts

- [[entities/bridgedata-v2|BridgeData V2]]
- [[entities/diffusion-policy|Diffusion Policy]]
- [[entities/flashattention|FlashAttention]]
- [[entities/lora|LoRA]]
- [[entities/open-x-embodiment-dataset|Open X-Embodiment Dataset]]
- [[entities/siglip|SigLIP]]
