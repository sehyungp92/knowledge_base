---
type: source
title: LLM Pretraining with Continuous Concepts
source_id: 01KJV44APF5CB8BG6AH8428PA3
source_type: paper
authors:
- Jihoon Tack
- Jack Lanchantin
- Jane Yu
- Andrew Cohen
- Ilia Kulikov
- Janice Lan
- Shibo Hao
- Yuandong Tian
- Jason Weston
- Xian Li
published_at: '2025-02-12 00:00:00'
theme_ids:
- finetuning_and_distillation
- interpretability
- mechanistic_interpretability
- model_architecture
- post_training_methods
- pretraining_and_scaling
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# LLM Pretraining with Continuous Concepts

**Authors:** Jihoon Tack, Jack Lanchantin, Jane Yu, Andrew Cohen, Ilia Kulikov, Janice Lan, Shibo Hao, Yuandong Tian, Jason Weston, Xian Li
**Published:** 2025-02-12 00:00:00
**Type:** paper

## Analysis

# LLM Pretraining with Continuous Concepts
2025-02-12 · paper · Jihoon Tack, Jack Lanchantin, Jane Yu, Andrew Cohen, Ilia Kulikov et al. (10 total)
https://arxiv.org/pdf/2502.08524

---

### Motivation & Prior Limitations
Standard next token prediction (NTP) forces models to learn high-level representations incidentally, as a byproduct of minimizing token-level perplexity over superficial tokens like function words, which creates a poor inductive bias for abstract reasoning and long-horizon planning.
- Natural language tokens are semantically shallow — function words like "the" or "a" contribute little signal for conceptual reasoning, requiring massive training compute to acquire high-level understanding through token co-occurrence alone.
  - LeCun (2022) and Bachmann & Nagarajan (2024) identify this token-level granularity as a fundamental obstacle to planning and long-horizon reasoning.
- Knowledge distillation (KD) at pretraining scale is constrained to naive token-level probability matching because generating synthetic datasets requires producing billions of tokens, making richer teacher signals prohibitively expensive.
  - In weak-to-strong regimes — where a smaller teacher supervises a larger student — KD degrades mid-training as the student surpasses the teacher and begins inheriting noisy or suboptimal distributions.
- Pause tokens (Goyal et al., 2024) and self-generated thought tokens increase inference-time compute but inject no structured semantic content into the model's hidden state, offering compute without signal.

---

### Proposed Approach
CoCoMix (Continuous Concept Mixing) augments NTP by predicting sparse, semantically grounded concepts extracted from a pretrained Sparse Autoencoder (SAE) and interleaving the compressed concept vectors directly into the transformer's hidden state sequence alongside token embeddings.
- Concepts are extracted from a pretrained model's hidden state using a TopK SAE, which decomposes activations into a high-dimensional sparse basis where each active dimension corresponds to a semantically interpretable feature; this is the first application of SAEs to LLM pretraining rather than post-hoc analysis.
  - Rather than using all active SAE concepts, CoCoMix selects the top-K most influential ones via an attribution score defined as the element-wise product of the pre-activation concept vector and the loss gradient with respect to the concept — capturing both which concepts are active and which causally influence the next-token prediction.
  - The model learns a concept prediction head that maps its own hidden state to a cross-entropy loss over the selected concept indices (treated as discrete labels), then compresses the predicted sparse logit through a learnable linear projection into a single continuous concept vector $\hat{c}_t \in \mathbb{R}^d$.
- The continuous concept vector is interleaved into the hidden state sequence as $(h_1, \hat{c}_1, \ldots, h_t, \hat{c}_t)$, processed by remaining transformer blocks — explicitly distinct from intervention-style approaches (Zou et al., 2023; Wu et al., 2024) that additively modify the hidden state, because interleaving allows the model to treat the concept as an independent unit of information with its own positional context.
- The joint training objective sums the standard NTP loss (now conditioned on both token and concept history) and a weighted concept prediction loss $\lambda \mathcal{L}_{\text{concept}}$, trained end-to-end.

---

### Results & Capabilities
CoCoMix consistently outperforms NTP across all tested model scales (69M, 386M, 1.38B parameters) and all eight evaluation benchmarks after 200B training tokens on OpenWebText, demonstrating that augmenting pretraining with continuous concepts improves both language modeling and downstream commonsense reasoning.
- At 1.38B parameters, CoCoMix reaches NTP's final validation perplexity using 21.5% fewer training tokens, a direct sample efficiency gain attributable to the richer per-token training signal.
- CoCoMix outperforms knowledge distillation in all three evaluated regimes: standard teacher-to-student, weak-to-strong (124M teacher → 386M student), and distribution shift (teacher trained on OpenWebText, student trained on OpenWebMath); the weak-to-strong gap is particularly large, with CoCoMix improving average perplexity by 2.8 over KD on the 386M model while KD degrades below NTP mid-training.
  - The compression layer weight analysis reveals that 5.8% of concept weights in a 386M model have $\ell_2$ norm below $10^{-2}$, indicating the model learns to selectively suppress uninformative concepts from the weak teacher — explaining why CoCoMix handles weak-to-strong scenarios where KD cannot.
- CoCoMix enables direct concept steering: amplifying or suppressing specific predicted concept logits $z_t$ at inference time steers generation toward the corresponding semantic domain, confirmed by cross-referencing against the pretrained GPT-2 SAE's concept space, demonstrating that the model has learned SAE-aligned representations.
- Attribution-based concept selection improves sample efficiency by 17.5% over activation-value-based selection, and concept prediction over SAE-discretized targets substantially outperforms direct hidden state prediction under $\ell_1$, $\ell_2$, and cosine loss — validating that the SAE's semantic decomposition provides a cleaner training target than raw hidden states.
- Component ablations show that both concept prediction loss and concept interleaving are necessary: concept prediction alone yields modest perplexity reduction, interleaving alone yields near-zero improvement over NTP at matched parameter count, but combining both produces the full gains.

---

### Implications
CoCoMix establishes a practical pathway for grounding LLM representations in semantically interpretable dimensions during pretraining — not post-hoc — linking mechanistic interpretability research (SAE feature extraction) directly to training

## Key Claims

1. CoCoMix achieves comparable performance to next token prediction while using 21.5% fewer training tokens on a 1.38B parameter model, demonstrating higher sample efficiency.
2. CoCoMix consistently outperforms standard next token prediction, knowledge distillation, and pause token insertion across multiple model sizes (69M, 386M, 1.38B) on language modeling and downstream re
3. Using attribution scores (gradient times activation) to select concepts significantly outperforms using raw activation values, improving sample efficiency by 17.5%.
4. Direct hidden state prediction (without SAE concept decomposition) leads to worse performance than concept-level prediction, suggesting that SAE decomposition filters out noisy components.
5. Both concept prediction loss and concept interleaving are individually necessary; neither alone achieves the full performance benefit of CoCoMix.
6. CoCoMix outperforms knowledge distillation in weak-to-strong supervision settings where a smaller model's concepts guide a larger model's training, while KD degrades when the student surpasses the tea
7. Knowledge distillation performance degrades mid-training when the student model surpasses the teacher's capability, particularly in distribution shift scenarios.
8. CoCoMix's compression layer learns to assign near-zero weights to approximately 5.8% of concepts, indicating the model learns to ignore uninformative or noisy concepts from the teacher.
9. Interleaving (inserting) the continuous concept vector as a separate token outperforms directly adding the concept vector to the existing hidden state.
10. Natural language tokens are often superficial, necessitating substantial training for models to acquire high-level reasoning and conceptual understanding, and hindering long-horizon planning.

## Capabilities

- Sparse autoencoder concepts extracted from a small reference model (124M parameters) can guide pretraining of models 10x larger (1.38B), achieving superior performance to standard knowledge distillation in weak-to-strong supervision scenarios
- LLM generation can be steered at inference time by amplifying or suppressing specific predicted concept logits in a CoCoMix-trained model, providing a transparent and inspectable mechanism for controlling model output
- Attribution scores (gradient × pre-activation) select SAE concepts that causally influence next-token prediction, yielding 17.5% additional sample efficiency improvement over activation-magnitude-based concept selection

## Limitations

- CoCoMix requires a pretrained sparse autoencoder as a prerequisite, creating a bootstrapping dependency: a reference pretrained LLM must exist, an SAE must be trained on its hidden states, and only then can CoCoMix pretraining begin — meaning the technique cannot be applied from scratch
- CoCoMix is validated only up to 1.38B parameters — applicability to frontier-scale models (70B+) is entirely undemonstrated, and the FLOPs overhead from concept interleaving may compound poorly with scale
- All CoCoMix experiments use a context length of only 1024 tokens — performance on long-context tasks (multi-document reasoning, extended planning) is completely unknown, and interleaving doubles token count making long contexts doubly expensive
- CoCoMix incurs higher FLOPs per training step than standard next-token prediction, partially offsetting sample efficiency gains — total compute savings depend on the efficiency-FLOPs tradeoff which is not analysed rigorously
- SAE concepts used in CoCoMix are bounded by the representational capacity of a small reference model (124M GPT-2); concepts absent from the teacher's latent space cannot be acquired by the student regardless of its larger capacity
- SAE concepts are distribution-specific: the SAE is trained on OpenWebText (GPT-2's pretraining distribution), and concept quality degrades when the target training corpus diverges from the SAE training distribution
- Standard knowledge distillation for LLM pretraining degrades performance when the student surpasses the teacher mid-training: the student is penalised for moving toward better solutions that diverge from the teacher's suboptimal distribution
- Next-token prediction is an inherently low-information training signal dominated by syntactic function words: models require substantially more training data than necessary for concept-level reasoning because most prediction targets carry negligible semantic content
- CoCoMix concept steering is only qualitatively demonstrated for simple, surface-form concepts; steering reliability for abstract, compositional, or multi-step reasoning concepts is entirely unvalidated
- Applying KD to LLM pretraining at scale is limited by massive token counts (billions to trillions), forcing all current methods to resort to naive token-level probability matching rather than more structured knowledge transfer

## Bottlenecks

- Token-level next-token prediction provides an inherently low-information training signal dominated by syntactic function words, causing models to require far more training data than necessary to acquire conceptual and reasoning capabilities — pretraining efficiency is bottlenecked by the mismatch be
- Knowledge distillation for LLM pretraining is bottlenecked by the teacher capability ceiling: token-level probability matching forces KD toward the teacher's distribution ceiling, and weak-teacher scenarios cause active degradation when students surpass teachers — blocking principled weak-to-strong 

## Breakthroughs

- First demonstrated use of sparse autoencoders as a pretraining objective component: SAE-extracted concepts from a pretrained model serve as intermediate training targets during pretraining of a new model, bridging the historically separate tracks of mechanistic interpretability tools and training ef

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/interpretability|interpretability]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/representation_learning|representation_learning]]

## Key Concepts

- [[entities/hellaswag|HellaSwag]]
- [[entities/openwebmath|OpenWebMath]]
- [[entities/sample-efficiency|Sample Efficiency]]
