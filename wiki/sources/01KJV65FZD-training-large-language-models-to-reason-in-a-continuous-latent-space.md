---
type: source
title: Training Large Language Models to Reason in a Continuous Latent Space
source_id: 01KJV65FZDWMAWMC6AV3HP5XFS
source_type: paper
authors:
- Shibo Hao
- Sainbayar Sukhbaatar
- DiJia Su
- Xian Li
- Zhiting Hu
- Jason Weston
- Yuandong Tian
published_at: '2024-12-09 00:00:00'
theme_ids:
- chain_of_thought
- latent_reasoning
- reasoning_and_planning
- search_and_tree_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Training Large Language Models to Reason in a Continuous Latent Space

Coconut (Chain of Continuous Thought) challenges the foundational assumption that LLM reasoning must occur in language space. By feeding the model's last hidden state back as the next input embedding — bypassing the language model head entirely — the approach enables reasoning in an unconstrained continuous latent space. This produces an emergent BFS-like search over candidate reasoning paths, achieves superior accuracy-efficiency trade-offs on planning-intensive benchmarks, and reveals that language is a bottleneck for cognition rather than a substrate for it. The work is currently limited to GPT-2-scale models on narrow benchmarks and faces fundamental training parallelism constraints that block scaling.

**Authors:** Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, Yuandong Tian
**Published:** 2024-12-09
**Type:** paper

---

## Motivation: Language as a Reasoning Bottleneck

Standard [[themes/chain_of_thought|Chain-of-Thought]] reasoning forces every intermediate step through the language model head, encoding it as discrete tokens. This design carries three structural costs:

1. **Uniform compute allocation.** Token generation distributes compute evenly across all positions. Most tokens exist for fluency and contribute negligibly to reasoning; a small fraction of "critical tokens" require disproportionate planning while receiving the same fixed compute budget.

2. **Premature commitment.** Autoregressive left-to-right generation forecloses alternatives the moment a token is emitted. CoT cannot backtrack or maintain parallel hypotheses.

3. **Language is optimized for communication, not cognition.** Neuroimaging evidence shows the brain's language network remains largely inactive during reasoning tasks — a dissociation that suggests natural language is not the optimal substrate for internal computation.

Prior partial fixes — succinct CoT prompting, learnable `<pause>` tokens, filler tokens (`...`) — remain confined to the language space. Pfau et al. (2024) explicitly noted that filler tokens work only for highly parallelizable problems and do not recover CoT-level expressivity gains.

---

## The Coconut Approach

### Continuous Thoughts

Coconut replaces decoded language tokens during intermediate reasoning steps with the model's own last hidden state `h_t`, fed directly back as the next input embedding `e(x_{t+1})`. This short-circuits the language bottleneck: reasoning steps never pass through the vocabulary projection or embedding lookup, making the entire reasoning process fully differentiable and end-to-end trainable by gradient descent.

Special `<bot>` and `<eot>` tokens mark boundaries between language mode and latent mode. The model alternates between standard autoregressive decoding and latent-mode recurrence based on position.

Critically, the training objective does **not** encourage continuous thoughts to reconstruct the removed language steps. The loss applies only to the language tokens that follow the latent segment, freeing the model to discover more efficient latent representations rather than compressing language reasoning.

### Multi-Stage Curriculum

Direct training on Q&A pairs with latent thoughts fails completely — models trained this way perform no better than the no-CoT baseline. The training scaffold is a multi-stage curriculum inspired by iCoT (Deng et al., 2024):

1. Train on full CoT data (language reasoning intact).
2. At each subsequent stage, replace the first `k` language reasoning steps with `k × c` continuous thoughts.
3. Continue until all language steps are internalized; select the best validation checkpoint across 50 total epochs.
4. Reset optimizer state at each stage transition.

This staged replacement lets language reasoning chains serve as a bootstrapping scaffold. Without them, latent reasoning cannot be learned.

---

## Results

| Benchmark | Coconut | CoT | No-CoT | Tokens (Coconut) | Tokens (CoT) |
|---|---|---|---|---|---|
| ProsQA | **97.0%** | 77.5% | — | **14.2** | 49.4 |
| ProntoQA | **99.8%** | 98.8% | — | **9.0** | 92.5 |
| GSM8k | 34.1% | **42.9%** | 16.5% | — | — |

On **ProsQA** (a new DAG-based logical reasoning benchmark requiring multi-hop path search), Coconut achieves a 19.5 percentage-point accuracy gain over CoT while generating 3.5× fewer tokens. CoT on ProsQA systematically hallucinates non-existent graph edges or commits to incorrect paths early; Coconut progressively narrows candidate paths across latent steps.

On **GSM8k**, Coconut outperforms iCoT (30.0%) but does not surpass full CoT (42.9%). The authors attribute this to GSM8k requiring contextual understanding rather than planning-heavy search — the regime where continuous latent reasoning offers the least advantage.

---

## Emergent BFS-Like Search

The most structurally interesting finding is that Coconut develops an implicit breadth-first search pattern without being trained or instructed to do so.

Probing the probability distributions over candidate nodes after continuous thoughts reveals:
- **Step 1:** Probability mass distributes broadly across multiple candidate next nodes — wide parallel exploration.
- **Step 2:** Mass consolidates toward higher-value nodes. The top-ranked node at step 2 often differs from step 1 — demonstrating non-greedy lookahead behavior.

The predicted probability of a candidate node following continuous thoughts functions as an **implicit value function** estimating each node's potential for reaching the correct answer. Nodes with lower "height" (closer to terminal/answer states in the DAG) receive reliably accurate evaluations; nodes far from terminal states produce ambiguous, unreliable estimates.

This emergent search pattern contrasts sharply with CoT's greedy single-path commitment. It arises from the unconstrained continuous space — continuous thoughts can encode multiple alternative next steps simultaneously in ways discrete tokens cannot.

See also: [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/reasoning_and_planning|Reasoning and Planning]]

---

## Limitations and Open Questions

### Fundamental Training Constraint
Training requires `n+1` sequential forward passes per step when `n` latent thoughts are scheduled. This is **incompatible with standard data-parallel distributed training** — the sequential dependency between forward passes blocks the parallelism that makes large-scale training feasible. This is the primary blocker for scaling Coconut beyond GPT-2.

### No Curriculum, No Learning
Without the multi-stage language CoT curriculum, training collapses entirely. This means Coconut **cannot be applied to tasks without step-by-step language reasoning annotations** — open-domain settings, multimodal inputs, or any domain lacking clean intermediate supervision are out of scope.

### GSM8k Ceiling
Coconut does not surpass CoT on math reasoning. Tasks requiring complex contextual understanding rather than planning-heavy search appear to be a fundamental mismatch for the current latent reasoning approach.

### Scale and Generalization
All experiments use GPT-2-scale models on three narrow structured benchmarks with deterministic ground truth. Scalability to large-scale pretraining and real-world tasks is entirely undemonstrated.

### Inference Inflexibility
Coconut has no mechanism for autonomously determining how many continuous thoughts a problem requires. Inference uses either a fixed pre-set thought count or a separately trained binary classifier — neither generalizes well to problems of varying difficulty.

### Value Function Degradation
The implicit value function degrades at high reasoning depths (nodes far from terminal states), precisely where exploration is most needed. This means the emergent BFS degrades on longer reasoning chains — the opposite of what would be desirable for scaling to harder problems.

### Training Cost Scaling
Training cost scales linearly with reasoning chain length: `N` stages, each running up to 50 epochs. For tasks with longer chains, training compute becomes prohibitive well before any pretraining-scale regime is reached.

---

## Relationship to Adjacent Work

- **iCoT (Deng et al., 2024):** Coconut adopts iCoT's multi-stage curriculum but replaces discrete internalized tokens with continuous hidden states, enabling genuine latent-space reasoning rather than compressed language reasoning.
- **Pause tokens / filler tokens:** Both approaches insert extra computation between question and answer but remain in language space, limiting expressivity. Coconut's latent space is unconstrained by the vocabulary.
- **MCTS/tree search:** Coconut's emergent BFS pattern is structurally similar to tree search methods but arises without any explicit search algorithm or reward model — it is learned implicitly from the training objective.

See also: [[themes/latent_reasoning|Latent Reasoning]]

---

## Significance

Coconut is a proof of concept that LLMs can learn to reason outside language space using existing language supervision as a scaffold. The emergent BFS behavior — arising without explicit training — suggests that the continuous space has structural properties that enable forms of reasoning that discrete token sequences cannot efficiently represent.

The work's primary contribution is demonstrating feasibility at small scale. Its primary limitation is that every path to scaling faces a structural blocker: sequential training compute, curriculum dependency on language annotations, and undemonstrated behavior at realistic model sizes. Whether these constraints are fundamental or engineering challenges remains an open question central to the future of [[themes/latent_reasoning|latent reasoning]] research.

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/gsm8k|GSM8K]]
