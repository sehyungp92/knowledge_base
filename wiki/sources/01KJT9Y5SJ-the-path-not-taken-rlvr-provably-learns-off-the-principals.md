---
type: source
title: 'The Path Not Taken: RLVR Provably Learns Off the Principals'
source_id: 01KJT9Y5SJX1HXPKBT1SMCE14Y
source_type: paper
authors:
- Hanqing Zhu
- Zhenyu Zhang
- Hanxian Huang
- DiJia Su
- Zechun Liu
- Jiawei Zhao
- Igor Fedorov
- Hamed Pirsiavash
- Zhizhou Sha
- Jinwon Lee
- David Z. Pan
- Zhangyang Wang
- Yuandong Tian
- Kai Sheng Tai
published_at: '2025-11-11 00:00:00'
theme_ids:
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Path Not Taken: RLVR Provably Learns Off the Principals

**Authors:** Hanqing Zhu, Zhenyu Zhang, Hanxian Huang, DiJia Su, Zechun Liu, Jiawei Zhao, Igor Fedorov, Hamed Pirsiavash, Zhizhou Sha, Jinwon Lee, David Z. Pan, Zhangyang Wang, Yuandong Tian, Kai Sheng Tai
**Published:** 2025-11-11 00:00:00
**Type:** paper

## Analysis

# The Path Not Taken: RLVR Provably Learns Off the Principals
2025-11-11 · paper · Hanqing Zhu, Zhenyu Zhang, Hanxian Huang, DiJia Su, Zechun Liu et al. (14 total)
https://arxiv.org/pdf/2511.08567

---

### Motivation & Prior Limitations
- Reinforcement Learning with Verifiable Rewards (RLVR) — the key driver behind Large Reasoning Models such as OpenAI-o3 and DeepSeek-R1 — paradoxically achieves high-gain reasoning improvements through surprisingly sparse parameter updates, yet the mechanism behind this sparsity was unknown and its interpretation contested.
  - Mukherjee et al. (2025) observed sparse updates empirically and attributed them to zero gradients, a conclusion this paper directly challenges as an artifact of imprecise measurement under bfloat16 storage.
  - Prior work lacked a parameter-level account of *where* RLVR updates land, not just *how many* parameters change, leaving the structural dynamics of RL fine-tuning a black box.
- SFT-era parameter-efficient fine-tuning (PEFT) methods, including principal-weight-targeted sparse fine-tuning (Liu et al., 2025c) and PiSSA (Meng et al., 2024a), were being naively carried over to RLVR without any principled justification that RL and SFT share a common optimization geometry.
  - The absence of a mechanistic theory meant practitioners had no geometric basis for choosing or designing PEFT methods suited to RL post-training, despite RL training consuming substantially more compute than SFT.

---

### Proposed Approach
- The paper proposes the **Three-Gate Theory** — a mechanistic framework explaining how RLVR updates are constrained (Gate I: KL Anchor), steered (Gate II: Model Geometry), and filtered (Gate III: Precision) to produce their characteristic sparse, off-principal update pattern.
  - **Gate I (KL Anchor)**: On-policy RL implicitly imposes a per-step KL leash on parameter movement. Proposition 3.2 proves that any one-step update satisfying a KL budget K is bounded in Fisher-metric norm by √(2K/μ), ensuring small per-step weight changes regardless of dataset or RL variant (including clip-only variants like DAPO with β=0, where ratio clipping provides an O(ε²) KL bound).
  - **Gate II (Model Geometry)**: A well-pretrained model's structured optimization landscape — specifically its singular value gaps — steers KL-constrained updates off high-curvature principal directions into low-curvature, spectrum-preserving subspaces. This is formalized via Wedin's sin-Θ theorem (Theorem 3.3) and Corollaries 3.4–3.5, which show that small-norm updates cannot substantially rotate top-k singular subspaces or shift singular values. Because this steering originates from the pretrained model's geometry rather than the dataset or RL algorithm, the bias is *model-conditioned*.
  - **Gate III (Precision)**: bfloat16 storage (7 mantissa bits) acts as a realization filter: micro-updates in non-preferred parameter regions fall below the unit-in-the-last-place (ULP) threshold and are not stored, making the off-principal bias *appear* as sparsity. This is a visibility amplifier, not a cause — optimizer states remain in float32.
- The paper also introduces a bf16-aware update sparsity probe (Definitions 2.1–2.2) using a relative tolerance η=10⁻³ that is equivalent to bitwise equality, correcting the unreliable fixed absolute-tolerance probe used in prior work.

---

### Results & Capabilities
- RLVR consistently yields update sparsity one order of magnitude higher than SFT across all tested model families and RL algorithms: RLVR sparsity ranges from 36.3% (Reinforcement++ on DS-Qwen-1.5B) to 91.7% (GRPO on Qwen3-30B-A3B), while SFT sparsity ranges from only 0.6% to 18.8%.
- RLVR updates exhibit a **persistent, model-conditioned routing bias**: across five independent runs from the same base model (DS-Qwen-1.5B) trained on disjoint datasets with different RL algorithms, the parameter-update masks share substantially higher Jaccard overlap (0.55–0.60 across attention and MLP layers) than the independent Bernoulli baseline (0.37–0.47), with consensus maps revealing contiguous stripe-like spatial patterns in Q/K/V/O projections that emerge early in training and are reinforced over time.
  - Causal evidence from geometry scrambling (orthogonal rotation and head permutation of specific layers in Qwen3-4B-Base) shows that disrupting the pretrained geometry collapses update-mask overlap to random levels in intervened layers while leaving untouched layers unaffected, establishing model geometry as the mechanistic cause of the bias.
- RLVR **preserves pretrained spectral structure** while SFT distorts it: on Qwen3-8B, DS-Qwen-1.5B, and Qwen3-14B-Base, RLVR shows consistently small principal-subspace rotation and near-identical singular-value profiles relative to the base model, whereas SFT induces substantially larger rotations and normalized spectral drift on all layers.
- RLVR **avoids principal weights** (the high-energy directions identified by rank-k SVD reconstruction), showing sub-random overlap with the principal mask, while exhibiting super-random overlap with low-magnitude weights; conversely, SFT targets principal weights. After excluding the intersection of principal and low-magnitude weights (Mprinc ∩ M_low^c), the residual overlap between RLVR updates and principal weights drops further.
- These off-principal, spectrum-preserving signatures **generalize beyond math/code RLVR** to agentic RL settings (AgentFlow, VERL-Agent, SkyRL, VERL-Tool on planning, WebSearch, DeepSearch, SWE tasks) and to RLHF (DPO, SimPO on instruction-following), indicating a common optimization bias within the KL-anchored RL post-training regime.
- For **sparse fine-tuning**, a fixed "safe mask" (Mlow ∪ M_princ^c) that freezes principal and large-magnitude weights while updating non-principal, low-magnitude ones most closely tracks the dense RLVR KL divergence curve and achieves comparable final accuracy using roughly 70% of parameters, whereas the principal-only mask (Mprin

## Key Claims

1. RLVR reliably improves large-language-model reasoning while apparently modifying only a small fraction of parameters, creating a paradox of high-cost, high-gain training with minimal weight modificati
2. The apparent sparsity of RLVR parameter updates is a surface artifact of a model-conditioned optimization bias, not a fundamental property of the training process.
3. RLVR update sparsity (fraction of unchanged parameters) ranges from 36% to 92% across models, while SFT sparsity is consistently low at 0.6%–18.8%.
4. For a fixed pretrained model, RLVR consistently concentrates visible updates into a narrow, stable subset of parameters that remain strikingly invariant across diverse algorithms and datasets.
5. RLVR update consensus maps reveal contiguous row/column stripe-like bands in attention projection matrices, indicating structured routing rather than random scatter.
6. Similar stripe-structured update footprints are observed on Llama and Mistral model families, suggesting the routing bias is generic to RLVR rather than model-family specific.
7. The apparent RLVR update sparsity largely disappears when the learning rate is increased to scale sub-ULP updates above the representable threshold in bfloat16.
8. RLVR update sparsity cannot be explained by precision limits alone; it requires a consistent optimization bias during RL that concentrates visible changes in specific parameter regions throughout trai
9. On-policy RL updates yield a per-step policy KL bound (Gate I, KL Anchor), which limits parameter movement during each RLVR update step.
10. Even when the explicit KL term is removed (e.g., in DAPO with β=0), the ratio clipping trick still imposes a KL bound O(ε²) in the small-step regime.

## Capabilities

- Three-Gate Theory provides the first parameter-level mechanistic characterisation of RLVR training dynamics: updates are KL-anchored (Gate I), steered off principal weight directions by pretrained model geometry (Gate II), and rendered visibly sparse by bfloat16 precision limits (Gate III)
- Theory-guided sparse RL fine-tuning using a 'safe mask' of non-principal, low-magnitude weights reproduces dense RLVR KL trajectory and final accuracy using approximately 70% of parameters, constructed entirely from the pretrained model without additional training
- Low-rank LoRA (even rank-1) can match full-parameter RL performance, with a geometric explanation: adapters approximate off-principal updates while frozen base weights regularise against principal-direction drift
- RLVR's model-conditioned optimization bias is invariant across datasets, RL algorithms (GRPO, DAPO, REINFORCE++), and multiple model families (Qwen, Llama, Mistral), and extends to agentic tasks and RLHF — indicating a universal structural property of RL post-training on pretrained LLMs

## Limitations

- SFT-era principal-targeted PEFT methods (PiSSA, sparse fine-tuning on principal weights) are fundamentally misaligned with RLVR's off-principal optimization regime — PiSSA provides no gain over standard LoRA and frequently collapses at higher learning rates required for competitive performance
- No RLVR-native geometry-aware PEFT methods exist; the paper identifies the design target but all demonstrated approaches use one-shot fixed masks without dynamic adaptation across training
- Direct quantification of optimisation landscape curvature in LRMs with long chain-of-thought reasoning is computationally prohibitive at scale, requiring indirect proxies (principal weights via rank-k SVD reconstruction)
- bfloat16 numerical format (7 mantissa bits) systematically masks micro-updates in non-preferred parameter regions, making RLVR's optimization dynamics appear sparser than they are — a precision-induced confound that invalidates naive update sparsity analyses
- RLVR achieves reasoning gains through selective modification of 8–64% of parameters despite substantial compute cost (RL substantially more expensive than SFT) — the effective parameter-space work done per compute dollar is far smaller than training costs imply
- RLVR's optimisation bias depends entirely on the pretrained model's weight geometry — function-preserving orthogonal rotations abolish the bias, meaning RLVR's favourable properties are contingent on preserving the specific pretrained spectral structure throughout the pipeline
- Prior published measurements of RLVR update sparsity (using fixed absolute-tolerance probes) are methodologically unreliable and may have over- or under-reported sparsity, undermining conclusions drawn from that literature

## Bottlenecks

- Absence of RL-native, geometry-aware PEFT methods designed for RLVR's off-principal optimization subspace — all existing parameter-efficient methods inherit SFT-era assumptions (principal weight targeting) that are structurally misaligned with how RL modifies models

## Breakthroughs

- Three-Gate Theory provides the first parameter-level mechanistic account of RLVR training dynamics, proving that update sparsity is a surface artefact of a model-conditioned geometric optimization bias — not a property of RL algorithms — and establishing a white-box foundation for RLVR-native algori
- Empirical and theoretical proof, with causal intervention evidence, that RLVR and SFT operate in disjoint optimization regimes in parameter space: RLVR systematically avoids high-curvature principal weight directions while SFT targets them, and disrupting pretrained geometry destroys the RLVR bias

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/grpo|GRPO]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/verl|veRL]]
