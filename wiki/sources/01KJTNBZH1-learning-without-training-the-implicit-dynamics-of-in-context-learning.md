---
type: source
title: 'Learning without training: The implicit dynamics of in-context learning'
source_id: 01KJTNBZH14TEKXP19FT16W8TY
source_type: paper
authors:
- Benoit Dherin
- Michael Munn
- Hanna Mazzawi
- Michael Wunder
- Javier Gonzalvo
published_at: '2025-07-21 00:00:00'
theme_ids:
- in_context_and_meta_learning
- interpretability
- mechanistic_interpretability
- model_architecture
- post_training_methods
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Learning without training: The implicit dynamics of in-context learning

**Authors:** Benoit Dherin, Michael Munn, Hanna Mazzawi, Michael Wunder, Javier Gonzalvo
**Published:** 2025-07-21 00:00:00
**Type:** paper

## Analysis

# Learning without training: The implicit dynamics of in-context learning
2025-07-21 00:00:00 · paper · Benoit Dherin, Michael Munn, Hanna Mazzawi, Michael Wunder, Javier Gonzalvo
https://arxiv.org/pdf/2507.16003

---

### Motivation & Prior Limitations
The mechanisms enabling in-context learning (ICL) in LLMs remain largely unknown, despite ICL being one of the most striking emergent properties of large language models — the ability to adapt to new patterns at inference time without any weight updates.
- Prior theoretical work explaining ICL as implicit gradient descent was limited to simplified transformer blocks trained on toy linear regression datasets, leaving open whether this intuition generalises to realistic architectures and general contexts.
  - Works such as Akyürek et al. and Von Oswald et al. demonstrated implicit gradient descent only for linear attention on linear regression setups, not for general transformer blocks with nonlinear MLPs.
- A separate result (cited as [6]) showed it is theoretically impossible to compress a prompt exactly into implicit weight updates of attention layer matrices without modifying the model architecture (requiring new attention biases), leaving the MLP layer's role underexplored.
  - This created a gap in understanding which component of the transformer block is the natural locus of context absorption.

---

### Proposed Approach
The paper introduces the notion of a **contextual block** — a generalisation of a transformer block consisting of a contextual layer (e.g., self-attention) composed with a standard MLP — and proves that the context acts as an exact, implicit **rank-1 weight update** of the MLP's first fully-connected layer.
- The core result (Theorem 2.2) is exact, not approximate: the output of a contextual block with full context `T_W(C, x)` is provably identical to the output with reduced context and an explicitly modified weight matrix `T_{W+ΔW}(C\Y, x)`, where the update formula is derived in closed form.
  - The implicit update is `ΔxW(Y) = (W δAx(Y)) A(C\Y, x)^T / ‖A(C\Y, x)‖²`, a rank-1 matrix formed as an outer product of a column vector and a row vector.
  - The framework generalises beyond self-attention to any contextual layer (RNNs, local-attention recurrents), enabling comparison of different architectures through the lens of the update structure they induce.
- By iteratively applying the theorem as each context token is consumed, the paper derives an implicit gradient descent dynamics over the MLP weights, with the learning rate equal to `1/‖A(x)‖²` and a per-step loss whose gradient vanishes when a new token has no marginal effect on the attention output.

---

### Results & Capabilities
The paper establishes that the implicit weight update formula connects three previously disparate phenomena — ICL, factual knowledge editing (rank-1 matrix edits as in ROME/MEMIT), and activation steering vectors — within a single mechanistic account.
- The low-rank matrix component of the implicit update (from the skip-connection case in Appendix B) is structurally identical to the rank-1 edits used in factual knowledge editing methods, suggesting these are manifestations of the same underlying mechanism.
- The vector component of the implicit update (also from the skip-connection case) has the same structural form as steering vectors used in representation engineering and activation patching, directly linking steering to the transformer's natural inference mechanics.
- Experimental verification (Section 4 and Figure 3) confirms that the implicit gradient updates vanish as the full context is consumed — i.e., once all tokens are processed and the MLP weights have absorbed the context, marginal weight changes go to zero, consistent with convergence of the implicit learning dynamics.
- The paper also shows that, unlike the attention layer, the MLP layer is *naturally predisposed* to absorb context as exact weight updates without any architectural modification, explaining why the MLP (not attention) is the primary site of contextual adaptation.

---

### Implications
This work provides the first exact, architecture-agnostic theoretical account of how context transforms into implicit parameter updates in realistic transformer blocks, potentially reframing ICL as a well-defined form of dynamic, query-dependent low-rank finetuning.
- The connection to rank-1 factual edits (ROME, MEMIT) implies that targeted knowledge editing methods are not ad-hoc interventions but are exploiting the same rank-1 update structure the transformer uses internally during every forward pass — with implications for how we understand and design editing methods.
- The connection to steering vectors implies that interpretability techniques based on linear representation patching have a grounding in the model's native inference mechanics, potentially validating and extending their theoretical basis.
- The result that MLP layers (not attention layers) are the natural absorbers of contextual weight updates has architectural implications: it suggests MLP capacity, not attention capacity, may be the binding constraint for ICL quality, and it motivates evaluation of contextual layers (RNN vs. attention) through the lens of what implicit weight updates they generate.
- The framework's generalisation to any contextual layer opens a mechanistic basis for comparing transformer and non-transformer architectures (e.g., state-space models, RNNs) on their ICL capability, grounded in the structure of their implicit updates rather than empirical benchmarks alone.

---

### Remaining Limitations & Next Steps
The implicit weight updates derived in the paper are **query-dependent** (they vary with the input query token `x`), meaning they cannot serve as static context compression — the "finetuned" weights must be recomputed for each new query.
- This is an explicit tradeoff acknowledged by the authors: exact implicit updates are dynamic, preventing their use as a static cache or KV-

## Key Claims

1. The stacking of a self-attention layer with an MLP allows the transformer block to implicitly modify the weights of the MLP layer according to the context at inference time.
2. A transformer block implicitly transforms a context into a rank-1 weight update of its MLP layer, providing an exact formula for this implicit update.
3. The implicit rank-1 weight update mechanism from context may be the reason why LLMs can learn in-context without weight updates during training.
4. In-context learning allows LLMs to adapt based on information provided in the input prompt without any changes to the model's underlying weights.
5. The mechanisms behind in-context learning in LLMs are still largely unknown at the time of writing.
6. Prior work has shown that simplified transformer blocks trained on linear regression datasets perform implicit weight updates corresponding to gradient descent optimization.
7. In-context learning can be understood as a form of implicit finetuning of the original pretrained model.
8. The implicit weight update formula for a contextual block is exact: the output of the contextual block with full context is precisely equivalent to the output with reduced context and modified weights
9. The implicit weight update ∆xW(Y) is a rank-1 matrix, as WδAx(Y) is a column vector and A(C\Y,x)^T is a row vector.
10. The low-rank matrix part of the implicit update is reminiscent of rank-1 updates used in factual knowledge editing of LLMs.

## Capabilities

- In-context learning can be characterized as implicit stochastic gradient descent over MLP weights as prompt tokens are consumed sequentially, with an explicit closed-form learning rate (1/‖A(x)‖²) and per-step loss derivable from first principles — providing a quantitative dynamics model of ICL at i
- Steering vectors and low-rank matrix edits (factual knowledge editing) can be derived as two components of the same underlying implicit weight-update formula in transformer blocks — unifying mechanistic interpretability tools under a single theoretical framework

## Limitations

- The implicit MLP weight updates produced by context are query-dependent and dynamic — they cannot be precomputed as static context compression because the update formula depends on the specific input query token at inference time
- Attention layers are fundamentally incapable of absorbing context as exact implicit weight updates without architectural modifications — a theoretical performance cliff that does not affect MLP layers
- The theoretical framework is validated only in simple toy experiments — no demonstration that the rank-1 implicit update formula accurately characterizes or predicts ICL behavior in production-scale LLMs
- Prior theoretical justification for ICL-as-gradient-descent only holds for simplified transformer blocks trained on toy linear regression tasks — the generalization to arbitrary natural language tasks and real architectures was unproven before this work and remains partially so
- Extension of the single-block rank-1 update theorem to full stacked transformer networks requires iterative application per block; no closed-form characterization of the full network's implicit update exists
- The implicit rank-1 weight update is not unique due to overparameterization — infinitely many weight matrices produce the same output, limiting the interpretive specificity of the mechanistic account
- The implicit gradient descent interpretation does not characterize whether implicit updates are task-optimal or aligned with any useful learning objective — the loss function is derived post-hoc from the update formula, not from task performance
- No investigation of whether different contextual layer types (RNN, SSM, local attention) produce qualitatively different or inferior implicit weight updates — the theoretical framework admits alternatives but their comparative properties are unexplored

## Bottlenecks

- Absence of theoretical understanding of ICL mechanisms has blocked principled architectural and training decisions — which layers are responsible, what kind of update they perform, and why more context helps has been empirically observable but mechanistically opaque

## Breakthroughs

- First exact theoretical derivation showing that transformer blocks perform precise rank-1 MLP weight updates from context, providing a closed-form formula and unifying in-context learning, factual knowledge editing, and steering vectors under a single mechanistic account

## Themes

- [[themes/in_context_and_meta_learning|in_context_and_meta_learning]]
- [[themes/interpretability|interpretability]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]

## Key Concepts

- [[entities/in-context-learning-icl|in-context learning (ICL)]]
