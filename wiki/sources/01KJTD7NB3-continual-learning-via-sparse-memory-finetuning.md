---
type: source
title: Continual Learning via Sparse Memory Finetuning
source_id: 01KJTD7NB37K99263WJPFS4N31
source_type: paper
authors:
- Jessy Lin
- Luke Zettlemoyer
- Gargi Ghosh
- Wen-Tau Yih
- Aram Markosyan
- Vincent-Pierre Berges
- Barlas Oğuz
published_at: '2025-10-16 00:00:00'
theme_ids:
- agent_memory_systems
- continual_learning
- finetuning_and_distillation
- knowledge_and_memory
- post_training_methods
- pretraining_and_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Continual Learning via Sparse Memory Finetuning

> This paper proposes sparse memory finetuning, a method that exploits the architectural sparsity of memory layer models to enable post-deployment knowledge updates with dramatically reduced catastrophic forgetting. By selecting only the memory slots most specific to new input (ranked via TF-IDF against a background corpus) and applying gradient masks to freeze all other parameters, the approach achieves a Pareto-dominant learning-vs-forgetting tradeoff: matching full finetuning on new knowledge acquisition while reducing held-out performance degradation from 89% (full finetuning) and 71% (LoRA) to just 11% on NaturalQuestions F1.

**Authors:** Jessy Lin, Luke Zettlemoyer, Gargi Ghosh, Wen-Tau Yih, Aram Markosyan, Vincent-Pierre Berges, Barlas Oğuz
**Published:** 2025-10-16
**Type:** paper
**Source:** https://arxiv.org/pdf/2510.15103

---

## The Core Problem

Language models are static artifacts after deployment. They cannot accumulate new knowledge without overwriting what they already know — a failure called catastrophic forgetting that has persisted from classical neural networks into the LLM era.

The existing mitigations all have structural deficiencies:

- **Full finetuning** updates all shared parameters, so gradient updates for new data interfere destructively with pretraining representations. On NaturalQuestions F1, finetuning on 1K TriviaQA facts causes an 89% performance drop.
- **LoRA** adds a small low-rank adapter, limiting interference but also limiting capacity. Biderman et al. (2024) confirmed the tradeoff is intrinsic: LoRA achieves less forgetting but learns less, yielding a 71% F1 drop at equivalent knowledge acquisition. Parameter-efficient expansion cannot escape this ceiling.
- **Replay** requires rehearsing pretraining data alongside new data, but modern LLMs undergo multiple rounds of pretraining, post-training, and alignment, making it intractable to define what to replay or at what mixture ratio. Replay also grows more data-inefficient as models accumulate experience.
- **Elastic Weight Consolidation** reduces but does not eliminate interference, since it only penalizes rather than fully restricts parameter updates.

The common failure mode across all methods is that no mechanism isolates *which* parameters store *which* knowledge. Updates bleed across tasks.

---

## Method: Sparse Memory Finetuning

The paper's central observation is that [[themes/agent_memory_systems|memory layer]] architectures already provide the structural property needed for isolation, and that this property can be exploited deliberately during finetuning.

### Memory Layer Architecture

Memory layers (Berges et al., 2024) replace one feedforward network in the transformer with a lookup into a large pool of key-value slots (1M slots in main experiments). The lookup is sparse: each token accesses only k=32 slots per head per layer, activating roughly 0.0002–0.03% of total memory parameters per forward pass. This is orders of magnitude finer-grained than [[themes/pretraining_and_scaling|mixture-of-experts]] architectures, which typically activate 10–100 experts and access a much larger fraction of parameters per token.

The result is that different knowledge items naturally route to different memory addresses. General-purpose patterns (syntax, broad world knowledge) cluster in frequently-activated slots; specific facts activate rare, input-specific slots.

### Selecting What to Update

Naive sparse memory finetuning would update all activated slots, which still permits interference through shared "general-purpose" indices. The key contribution is a ranking step using TF-IDF:

1. Compute IDF scores for each memory slot from 1000 random batches of DCLM pretraining data (computed once, stored statically, zero per-step overhead).
2. For each training batch, compute TF scores: how often each slot is accessed for this specific batch.
3. Rank by TF-IDF: select only the top-t slots that are *frequent in the current batch but rare in pretraining*. These are the knowledge-specific slots.
4. Apply a gradient mask: only top-t slots receive gradient updates; all others are frozen via `.detach()`.

The TF-IDF framing directly mirrors document retrieval intuitions: high-IDF slots are rare signals specific to the current input, analogous to rare but informative query terms. Low-IDF slots, accessed constantly during pretraining, are treated as infrastructure and left untouched.

Ablations confirm this decomposition is critical: using raw TF counts without IDF achieves comparable learning but significantly more forgetting, especially at small t. The IDF component is what prevents overwriting general-purpose indices.

### Optimizer Choice

AdamW is discarded in favor of SGD for the sparse memory update step. Adaptive per-parameter step sizes, weight decay, and momentum in AdamW interact poorly with extreme sparsity in ways that are not yet theoretically understood. SGD's simplicity contributes measurably to reduced forgetting. The theoretical explanation is left as open work.

---

## Results

Across two tasks and a full hyperparameter sweep, sparse memory finetuning Pareto-dominates both full finetuning and LoRA:

| Method | NaturalQuestions F1 Drop | New Knowledge Acquisition |
|---|---|---|
| Full finetuning | 89% | High |
| LoRA | 71% | High |
| Sparse memory (t=500) | 11% | High (same) |

On the document QA task (1,824 Wikipedia paragraph chunks for 100 SimpleQA questions), sparse memory finetuning matches the best full finetuning and LoRA configurations on target task performance while exhibiting substantially less degradation on NaturalQuestions F1 and GSM8K NLL.

The gap widens with learning capacity: as t increases, sparse memory finetuning continues to learn more without proportionally increasing forgetting, while full finetuning and LoRA degrade monotonically.

Qualitative analysis of memory accesses shows that TF-IDF-selected trainable indices align with entity boundaries in text and with the specific indices accessed when answering target questions at test time. The method is identifying semantically meaningful memory addresses, not arbitrary ones.

---

## Implications for the Landscape

This result shifts the framing of [[themes/continual_learning|continual learning]] from a regularization or capacity problem to an **architectural** problem. Prior work treated continual learning as a matter of adding constraints or small adapters to existing architectures. Sparse memory finetuning demonstrates that the structural property of memory layers (per-token sparse access to a large pool) is itself a precondition for effective knowledge isolation.

The implications cascade through [[themes/finetuning_and_distillation|finetuning and post-training]] practice:

- LoRA's position as the near-optimal PEFT method for post-deployment updates is challenged. Its Pareto-dominated tradeoff means it is neither the best at learning nor the best at retention, only a compromise.
- Architectural sparsity may need to be treated as a first-class design target for deployable, updatable models rather than a performance optimization.
- The base memory-augmented model outperforms a standard transformer on held-out benchmarks at equivalent parameter count (consistent with Berges et al., 2024), suggesting memory layers improve [[themes/knowledge_and_memory|knowledge retention]] even without sparse finetuning.

---

## Open Problems and Limitations

The paper is clear about what it does not yet establish:

**Scope limitations.** Validation is limited to factual QA (TriviaQA, SimpleQA, NaturalQuestions) with a 1.3B model. Generalization to complex reasoning, coding, and procedural skill acquisition is explicitly deferred and mechanistically unclear. Factual recall may be uniquely well-suited to memory layer routing; it is not obvious that skills or reasoning patterns decompose the same way.

**Architectural dependency.** Sparse memory finetuning requires a memory layer to be present in the pretrained model. It cannot be retrofitted to standard transformers without retraining from scratch. This limits near-term applicability to the existing fleet of deployed models, almost none of which currently include memory layers. Adoption requires the [[themes/pretraining_and_scaling|pretraining]] community to treat memory layers as a standard architectural component.

**Background corpus sensitivity.** The choice of background corpus for TF-IDF ranking materially affects the tradeoff. Using the training domain itself (e.g., TriviaQA questions) as background leads to less retention and significantly more forgetting. The correct background must approximate the full breadth of pretraining, which is not always accessible or well-defined.

**Batch-level granularity.** The top-t selection is static and batch-level: a fixed number of slots per batch regardless of individual example complexity. Per-sequence or adaptive granularity is noted as a direction for future work.

**Memory lookup scalability.** At pool sizes of 1M–100M keys, the memory embedding lookup is a computational bottleneck requiring approximate product-key decomposition. This trades retrieval exactness for efficiency and may affect which slots get selected during finetuning.

**Continual skill learning remains unsolved.** For reasoning, coding, and tool use, it is not clear how to distill lessons from experience into parametric form. RAG is not a sufficient answer for tasks where retrieval is difficult. This broader problem, of agents that improve their problem-solving abilities through deployment experience, remains entirely open across all [[themes/post_training_methods|post-training methods]].

---

## Connections

- [[themes/agent_memory_systems|Agent Memory Systems]] — memory layers as infrastructure for knowledge-specific parameter routing in deployable agents
- [[themes/continual_learning|Continual Learning]] — Pareto-dominant tradeoff over full finetuning and LoRA; architectural sparsity as the key ingredient
- [[themes/finetuning_and_distillation|Finetuning and Distillation]] — LoRA's intrinsic learning-forgetting ceiling; SGD vs. AdamW interaction with sparse updates
- [[themes/knowledge_and_memory|Knowledge and Memory]] — memory layers as structured stores where knowledge items route to distinct, addressable locations
- [[themes/post_training_methods|Post-Training Methods]] — post-deployment knowledge updates as a distinct regime from alignment and instruction tuning
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — memory layers improving pretraining knowledge retention; architectural choices as prerequisites for continual learning

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/dclm|DCLM]]
- [[entities/elastic-weight-consolidation|Elastic Weight Consolidation]]
- [[entities/gsm8k|GSM8K]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/lora|LoRA]]
- [[entities/triviaqa|TriviaQA]]
- [[entities/continual-learning|continual learning]]
