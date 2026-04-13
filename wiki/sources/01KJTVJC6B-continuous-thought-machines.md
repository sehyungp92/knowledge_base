---
type: source
title: Continuous Thought Machines
source_id: 01KJTVJC6BWQXDBZ1WNG48GEC6
source_type: paper
authors:
- Luke Darlow
- Ciaran Regan
- Sebastian Risi
- Jeffrey Seely
- Llion Jones
published_at: '2025-05-08 00:00:00'
theme_ids:
- adaptive_computation
- latent_reasoning
- model_architecture
- reasoning_and_planning
- representation_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Continuous Thought Machines

The Continuous Thought Machine (CTM) is a recurrent neural architecture that reintroduces biological temporal dynamics as a first-class computational primitive, using per-neuron temporal integration (neuron-level models), neural synchronization as the primary latent representation, and an internal "thought" timeline decoupled from data dimensions — enabling emergent adaptive computation, spatial planning without positional encodings, and interpretable sequential attention, while remaining far from competitive scale and largely untested on language.

**Authors:** Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, Llion Jones
**Published:** 2025-05-08
**Type:** paper

---

## Motivation

Standard deep learning architectures deliberately abstract away the timing and interplay of individual neuron interactions. The authors argue this sacrifice, while enabling scale, has created a persistent gap between AI and human cognition — specifically the flexibility, efficiency, fluidity, generalization, and common sense that biological brains achieve through *temporal processing*.

Existing workarounds are insufficient:

- **Adaptive computation methods** (PonderNet, ACT, early-exit networks) treat variable compute as an explicit bolt-on module rather than an emergent architectural property.
- **Synchronization in prior work** (Reichert & Serre 2011; complex-valued networks) treats neural synchrony as a post-hoc emergent phenomenon for grouping or stabilization, not as an optimized latent representation.
- **Recurrence alone** is insufficient — the temporal *dynamics* that recurrence can unlock have been underexplored.

The CTM's central claim: neural dynamics and synchronization are not biological curiosities but computationally powerful mechanisms worth recovering.

---

## Architecture

### Internal Time Dimension

The CTM operates along a self-generated timeline of *internal ticks* (t = 1…T), entirely decoupled from data dimensions. Even a static image is processed iteratively — the model "thinks" across T steps before producing output. This contrasts with all feed-forward and standard sequential architectures, where computation depth is fixed to the data structure.

### Neuron-Level Models (NLMs)

Each of D neurons carries its own privately parameterized NLM — a depth-1 MLP that processes a history of M recent pre-activations (M ≈ 10–100) to produce that neuron's post-activation. This gives each neuron a unique temporal integration profile, inspired by the computational complexity of biological neurons while remaining fully differentiable.

Standard activation functions are shared and memoryless. NLMs are neither — and this per-neuron specialization is where temporal richness enters the model.

### Neural Synchronization as Latent Representation

The post-activation history matrix Z ∈ ℝ^(D×t) is used to compute a synchronization matrix S = ZZ^T ∈ ℝ^(D×D). Randomly sampled neuron pairs from S form low-dimensional projections used for:

- **Output predictions** (S_out)
- **Cross-attention queries** (S_action)

Learnable exponential decay factors per neuron pair allow the model to operate across multiple time scales. This is the CTM's central architectural innovation: synchronization is not observed after training — it is *optimized* as the primary representational mechanism.

"Snapshot" representations (projecting directly from post-activations z_t) were found to be too constraining, as they tie the representation directly to the downstream task and limit the types of dynamics the network can produce.

### Adaptive Computation Without a Halting Module

The loss function selects two ticks per forward pass:
- **t1**: tick of minimum loss (optimizes accuracy)
- **t2**: tick of maximum certainty (optimizes calibration)

Their cross-entropy losses are averaged. This natively implements adaptive computation: the model can halt early for simple inputs or continue for harder ones, without any dedicated halting component. Setting a certainty threshold of 0.8 allows halting for the majority of ImageNet instances after fewer than 10 of 50 internal ticks.

---

## Capabilities

### Spatial Planning and World Model Formation

[[themes/reasoning_and_planning|Reasoning & Planning]]

On 2D maze navigation (39×39 mazes, up to 100-step action sequences, *no positional encodings*), the CTM significantly outperforms feed-forward and 1–3 layer LSTM baselines. Without positional embeddings, the model must construct its cross-attention query by imagining the future state of the maze — a process the authors describe as analogous to *episodic future thinking* in humans.

Trained on 39×39 mazes, the CTM generalizes to 99×99 mazes via iterative re-application of the same learned policy, and continues exploring paths beyond its 100-step training horizon — suggesting it acquired a general spatial procedure rather than memorizing routes.

### Emergent Sequential Visual Attention

[[themes/representation_learning|Representation Learning]]

On ImageNet classification, the CTM learns to "look around" images — tracing complex multi-step attention paths across regions before predicting — entirely without any training signal directing this behavior. The attention strategy is an emergent consequence of the synchronization-based cross-attention mechanism.

### Native Adaptive Computation

[[themes/adaptive_computation|Adaptive Computation]]

Adaptive compute allocation emerges without any explicit halting mechanism. The certainty-based stopping criterion produces well-calibrated uncertainty estimates as a side effect: predicted probabilities align tightly with empirical accuracy across internal ticks without specialized calibration training.

### Sequential Reasoning on Parity

On cumulative parity over 64-length binary sequences, the CTM significantly outperforms parameter-matched LSTMs, with some runs achieving perfect accuracy at 75–100 internal ticks. Attention maps reveal interpretable left-to-right scanning strategies — individual heads learn sequential procedures visibly.

---

## Limitations & Open Questions

[[themes/transformer_alternatives|Transformer Alternatives]] | [[themes/model_architecture|Model Architecture]]

**Training cost scales with T.** Every forward pass requires T full iterations of synapse model and NLM computation. Training times are extended by a factor of T relative to single-pass architectures, currently restricting experiments to small-scale tasks.

**Quadratic synchronization scaling.** The synchronization matrix S ∈ ℝ^(D×D) scales O(D²) with neuron count. The current workaround — fixing randomly sampled neuron pairs at training initialization — prevents the model from adaptively discovering which synchronization patterns are most informative. This is a hard architectural bottleneck for scaling to large-width networks.

**ImageNet accuracy is far below state-of-the-art.** 72.47% top-1 with a ResNet-152 backbone reflects the absence of hyperparameter search and architectural optimization; the gap to competitive models is substantial and unaddressed.

**No language modeling experiments.** The CTM's entire innovation — neural synchronization as a temporal representation — has not been tested on discrete token sequences. Whether these mechanisms are viable for the dominant paradigm in AI remains entirely open.

**Seed sensitivity on parity.** Perfect accuracy on the parity task was achieved only in some random seeds. High variance across seeded runs suggests unstable convergence to qualitatively different solution strategies — a meaningful reliability concern.

**RL performance only matches LSTM baselines.** The architectural complexity of neural dynamics provides richer internal representations in partially observable environments, but does not translate to better task performance, suggesting the inductive biases are not universally beneficial.

**Temporal decay mechanism is task-inconsistent.** The learnable decay factors in synchronization are barely leveraged for ImageNet but more active for maze tasks, indicating the CTM requires task-specific tuning to extract value from multi-scale temporal processing.

**Limited baseline comparisons.** The paper explicitly favors breadth over depth in comparisons, omitting modern SSMs, Mamba, or well-tuned Transformers. The CTM's relative advantage over strong recurrent alternatives is unknown.

**No scaling evidence.** All experiments are at small model sizes. Whether neural dynamics and synchronization representations remain computationally useful or collapse at large scale is entirely undemonstrated.

---

## Breakthroughs

**Neural synchronization as an optimized latent representation.** Prior work used synchrony as a post-hoc phenomenon; the CTM explicitly trains temporal cross-correlations between neuron activity histories as the representational substrate driving attention and output. This is a conceptual reorientation, not just an architectural tweak.

**Emergent adaptive computation without a halting module.** The CTM's certainty-based early stopping arises from the loss formulation itself — no PonderNet-style halting component required. Adaptive behavior is an intrinsic property of how neural dynamics evolve, not an extrinsic add-on.

---

## Bottlenecks Identified

| Bottleneck | Blocks | Horizon |
|---|---|---|
| O(D²) synchronization matrix scaling | CTM deployment at large neuron counts; full exploitation of synchronization as a representational mechanism | 1–2 years |
| T-multiplied training compute | Training at scale needed to compete with state-of-the-art on NLP/vision benchmarks | 1–2 years |
| No language modeling application | Determining whether biologically-inspired temporal dynamics are viable for discrete sequence modeling | Months |

---

## Connections

- [[themes/adaptive_computation|Adaptive Computation]] — CTM's most mature demonstrated capability; emergent halting without a dedicated module is the headline result
- [[themes/latent_reasoning|Latent Reasoning]] — internal ticks as a "thought" timeline positions the CTM as an architecture for extended computation before commitment
- [[themes/representation_learning|Representation Learning]] — synchronization as a representation is the core theoretical bet
- [[themes/reasoning_and_planning|Reasoning & Planning]] — maze generalization is the strongest empirical demonstration of the architecture's value
- [[themes/model_architecture|Model Architecture]] — NLMs and the synapse model are the structural innovations
- [[themes/transformer_alternatives|Transformer Alternatives]] — the CTM is positioned as a biologically-grounded alternative path, though it has not yet competed at transformer scale

## Key Concepts

- [[entities/imagenet-1k|ImageNet-1K]]
- [[entities/quiet-star|Quiet-STaR]]
- [[entities/umap|UMAP]]
