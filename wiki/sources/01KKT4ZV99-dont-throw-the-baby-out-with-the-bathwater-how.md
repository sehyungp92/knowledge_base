---
type: source
title: 'DON’T THROW THE BABY OUT WITH THE BATHWATER: HOW'
source_id: 01KKT4ZV99Z4F5KXE800DY9DDE
source_type: paper
authors: []
published_at: None
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DON’T THROW THE BABY OUT WITH THE BATHWATER: HOW

**Authors:** 
**Published:** None
**Type:** paper

## Analysis

# DON'T THROW THE BABY OUT WITH THE BATHWATER: HOW
paper
https://github.com/MohamedOsman1998/deep-learning-for-arc/blob/main/deep_learning_for_arc.pdf

---

### Motivation & Prior Limitations
The ARC-AGI benchmark was designed to test genuine in-context learning rather than memorization, exposing a fundamental gap in standard deep learning evaluation: models are tested on in-distribution data, measuring existing skills rather than the efficiency of the learning process itself.
- Large foundation models (LLMs and vision models) perform poorly on ARC out of the box, with GPT-4 achieving only 10.6% on the combined dataset and 6.75% on the public test set, because ARC requires dynamically acquiring new transformations rather than reusing pretrained knowledge.
  - The research community held significant uncertainty about whether neural networks could ever be trained to perform well on ARC-like tasks.

Prior approaches framed ARC as a symbolic or program-synthesis problem, but this misclassification led to architectural choices ill-suited to the benchmark's perceptual nature.
- Neuro-symbolic and code-generation methods (e.g., CodeIt at 14.8%, GPAR at 50% on a restricted subset) hit a ceiling because they require explicitly encoding transformation rules in formal languages, which is more difficult than directly predicting output grids and fails on tasks with near-infinite possible transformations.
  - Shallow architectures like Proto-Net process grid-pairs in isolation and average embeddings, inadvertently destroying the cross-pair interaction information needed to infer transformation rules.

Benchmark evaluation practices in related work are unreliable: many studies report scores on the public evaluation set (potentially seen during pretraining) and omit computational cost, making fair comparison impossible.

---

### Proposed Approach
The paper proposes treating ARC as a perceptual reasoning problem and committing fully to the deep learning paradigm by placing both the neural network and the optimizer inside the inference loop, rather than relying solely on a frozen pretrained model.

**Architecture and pretraining (ICL emphasis):** The authors base their system on LongT5, an encoder-decoder model chosen for its non-causal (bidirectional) attention in the encoder, which allows all tokens — including those from different grid-pairs — to attend to each other simultaneously, enabling the cross-pair associative learning that ARC demands.
- The full riddle (all training grid-pairs and the test input) is serialized into a single flat text sequence so the model processes all examples jointly in one forward pass, directly contrasting with architectures that embed grid-pairs independently.
- Multi-task training on diverse NLP and coding datasets is used alongside ARC data; code pretraining in particular is emphasized because code datasets demand precise, hierarchical, non-memorizable reasoning and are "more logical and less ambiguous" than natural language.
- Synthetic riddle generators using Domain Specific Languages (DSLs) expand training data; a dual-prediction objective (predict both the output grid and the underlying DSL function names) improves robustness over training on either target alone. Riddles are deliberately overspecified to prevent the model from encoding ambiguities into weights.

**Test-Time Fine-Tuning (TTFT):** During evaluation on each test riddle, the authors generate synthetic training data by treating held-out demonstration examples as new test cases (where the answer is known), augmenting them via color permutation, spatial transformations from the dihedral group D4, and example shuffling, then running a brief full-parameter fine-tuning pass before generating predictions.
- The motivation is "iterative reframing": a model locked into an incorrect initial interpretation of a riddle cannot self-correct via the forward pass alone; TTFT provides a gradient-based mechanism to re-process the riddle from scratch under a corrected framing.
- Full parameter updates are chosen over LoRA or chain-of-thought prompting for their simplicity and guaranteed expressive power when generating novel abstractions is required.

**AIRV (Augment, Inference, Reverse-Augmentation, Vote):** A test-time augmentation strategy that applies spatial transformations to the riddle, runs inference, reverses the augmentation on the predicted output, and aggregates predictions across multiple augmentations via majority voting.
- Because each ARC riddle has exactly one correct answer, voting strongly amplifies consistent correct predictions while suppressing diverse incorrect ones — analogous to the clustering step in AlphaCode.
- Beam search is used for autoregressive decoding to maintain multiple candidate output trajectories, mitigating the brittleness of greedy decoding where a single wrong token produces an unrecoverable trajectory.

---

### Results & Capabilities
AIRV alone yields up to a 260% accuracy boost over zero-shot baseline on the ARC private test set; combining TTFT with AIRV yields a further 300% boost, with the fully trained base LongT5 going from 5 correct (zero-shot) → 13 (AIRV only) → 39 (TTFT + AIRV) tasks on the private test set.
- These results are evaluated on the fully held-out private test set under competition constraints: 2 hours on a single P100 GPU (16 GB VRAM), with top-2 attempt scoring.

The combined approach achieved first place in the 2023 ARCathon competition and reached 58% accuracy on the ARC-AGI private test set in the 2024 Kaggle competition, representing the highest known score at the time of writing.

Model size scaling behaves differently depending on test-time technique: zero-shot and AIRV-only performance scales with model size (larger models form more associations in the forward pass), but TTFT performance does not scale with model size in the same way — the fully-trained base model achieves a 300% TTFT boost versus only 140% and 240% for the partially-trained large

## Key Claims

1. Deep learning with test-time fine-tuning achieves state-of-the-art performance on ARC-AGI, reaching 58% on the private test set in 2024.
2. AIRV (Augment Inference Reverse-Augmentation and Vote) produces up to a 260% boost in accuracy over baseline ARC pre-training on the private test set.
3. Test-Time Fine-Tuning (TTFT) adds a further 300% boost over the AIRV-only baseline on ARC private test set.
4. ARC problems are more perceptual and qualitative in nature than quantitative, making deep learning an appropriate paradigm for solving them.
5. Large-scale foundation models do not perform well on ARC out of the box when prompted with these problems.
6. The ARC dataset reliably tests the efficiency of the learning process itself rather than pre-trained knowledge, because little pre-training knowledge can be leveraged to solve its riddles.
7. Current benchmarks like ImageNet have become saturated, with models progressing by exploiting labeler biases rather than genuine understanding.
8. Shallow architectures that independently embed grid-pairs and combine them via averaging are ill-suited for ARC because they cannot capture cross-grid-pair interactions.
9. High-performing methods on vision meta-learning and NLP datasets rely more on pretraining knowledge than genuine meta-learning, causing a memorization problem.
10. LLMs can identify and utilize Probabilistic Context-Free Grammars, suggesting they perform associative learning that is useful for ARC tasks.

## Capabilities

- Test-Time Fine-Tuning (TTFT) combined with AIRV achieves 58% accuracy on the ARC-AGI private test set — the highest score recorded during the 2024 ARC Kaggle competition — using only a single P100 GPU under a 2-hour compute budget.
- Augment Inference Reverse-Augmentation and Vote (AIRV) — applying spatial transformations to input riddles, generating predictions, reversing augmentations, and voting — boosts ARC accuracy by up to 260% over a zero-shot baseline.
- Test-Time Fine-Tuning (TTFT) — briefly fine-tuning a pretrained model on augmented versions of the current test riddle's demonstration examples before inference — delivers an additional ~300% performance gain on ARC over AIRV-only, consistent across model sizes and training regimes.
- LLMs (LongT5 encoder-decoder) trained with multi-task and code pre-training can acquire contextual, associative reasoning sufficient for novel abstract visual transformation tasks (ARC), via non-causal attention across all grid-pair tokens presented simultaneously.
- Code pre-training boosts LLM performance on abstract perceptual reasoning (ARC) more than general NLP multi-task training, because code demands hierarchical reasoning, precise context tracking, and low reliance on memorized associations.
- Dual-prediction training — simultaneously predicting the output grid and the underlying DSL function names — improves model robustness on ARC over training on either target alone.
- Synthetic ARC riddle generation via Domain Specific Language (DSL) sampling of function names and parameters enables large-scale, overspecified training data that reduces memorization artifacts and improves contextual reasoning.

## Limitations

- Frozen pretrained LLMs (GPT-4, GPT-3.5, GPT-4V) achieve only 6–20% accuracy on ARC without task-specific training, demonstrating that scale and general pretraining alone are insufficient for abstract visual reasoning.
- Causal (masked) decoder-only architectures substantially underperform encoder-decoder models on ARC because early tokens in a causal sequence cannot attend to later context, preventing full bidirectional cross-grid-pair reasoning from the outset.
- Larger pretrained models perform worse under TTFT (the Large variant scores lower TTFT accuracy than the smaller Base model), despite outperforming in zero-shot and AIRV-only settings — indicating that TTFT efficiency is not correlated with model size.
- Code-based intermediate output generation for ARC consistently underperformed direct grid-output generation in initial trials, because producing syntactically valid, general-purpose transformation programs is harder than directly predicting the output grid.
- Even when the correct transformation rule is identified, limited model depth and capacity cause pixel-level execution errors (off-by-one or off-by-two pixels), requiring TTFT to patch fine-grained execution accuracy.
- The method is practically constrained by competition compute limits (2 hours, single P100 GPU, 16GB VRAM), and the 58% score was achieved with additional optimizations beyond what the constrained environment allows — implying the approach is not yet feasible at high throughput or low cost.
- Program synthesis approaches for ARC require extensive manual engineering — humans must explicitly encode pair-association heuristics, transformation search logic, and confirmation checks — and still fail on perceptual tasks with near-infinite transformation spaces.
- Object-centric neural approaches fail to generalize when the task-relevant 'object' is ambiguous or highly context-dependent — their fixed segmentation priors become incorrect assumptions that hurt performance on the full ARC distribution.
- State-of-the-art deep learning achieves only 58% on the ARC private test set — a task designed for easy human solution — indicating a large and poorly characterized gap between current AI abstract reasoning and human-level fluid intelligence.
- Shallow cross-grid interaction architectures (Proto-Net-style, CodeIt, pure embedding-averaging) destroy cross-example information by processing grid-pairs independently, making them fundamentally incapable of tasks that require joint reasoning across multiple input-output pairs.
- Training data ambiguity — where generated riddles leave aspects of transformations underspecified — causes models to encode ambiguities into weights via memorization rather than learning to reason contextually, degrading generalization.
- ARC evaluation on the public dataset is unreliable due to potential pretraining contamination — several related-work papers evaluate only on public data that may have been included in LLM pretraining corpora, inflating apparent performance.

## Bottlenecks

- Per-task TTFT gradient computation at inference time — requiring a full fine-tuning pass over augmented riddle data before each prediction — imposes compute overhead that makes the approach impractical outside of batch/competition settings.
- Generating sufficiently large, diverse, and correctly specified ARC training data is a fundamental bottleneck: real ARC tasks are scarce (400 training riddles), and synthetic generators must avoid underspecification artifacts or models learn to memorize rather than reason.
- The ARC private test set — only 100 tasks, sequestered and competition-mediated — is too small and inaccessible to enable reliable, frequent evaluation of progress toward human-level abstract reasoning, creating a measurement bottleneck.
- The space of ARC transformations is combinatorially near-infinite even with simple priors, making symbolic/search-based approaches fundamentally bottlenecked by enumeration complexity — there is no performant quantitative approach to searching this space.

## Breakthroughs

- First successful demonstration that the deep learning paradigm — treating both the neural network and the optimizer as integral components of inference via Test-Time Fine-Tuning — can achieve state-of-the-art performance on ARC, reaching 58% on the private test set in 2024.
- AIRV (Augment Inference Reverse-Augmentation and Vote) establishes that geometric test-time augmentation with voting is highly effective for single-answer abstract reasoning tasks — producing up to 260% accuracy gains by exploiting the fact that correct solutions are unique while errors are diverse.

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/in-context-learning-icl|in-context learning (ICL)]]
