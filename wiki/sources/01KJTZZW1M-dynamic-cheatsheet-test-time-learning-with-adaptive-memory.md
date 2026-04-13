---
type: source
title: 'Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory'
source_id: 01KJTZZW1MNKKNZCX5GTN3Y8RR
source_type: paper
authors:
- Mirac Suzgun
- Mert Yuksekgonul
- Federico Bianchi
- Dan Jurafsky
- James Zou
published_at: '2025-04-10 00:00:00'
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory

**Authors:** Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, James Zou
**Published:** 2025-04-10 00:00:00
**Type:** paper

## Analysis

# Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory
2025-04-10 · paper · Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, James Zou
https://arxiv.org/pdf/2504.07952

---

### Motivation & Prior Limitations
- Deployed language models operate statelessly: each input query is processed independently, with no retention of insights, strategies, or errors from prior inferences, forcing models to repeatedly re-derive the same solutions and re-commit the same mistakes.
  - This stands in sharp contrast to human cognition, which is grounded in incremental, experience-driven learning that continuously internalizes new knowledge into a persistent mental model.
- Existing alternatives each carry significant trade-offs that DC is designed to avoid: fine-tuning (dynamic evaluation, domain adaptation) modifies model weights and is incompatible with black-box APIs; retrieval-augmented generation retrieves from large static corpora rather than adapting dynamically; and naive full-history appending bloats context, dilutes useful signal, and escalates inference costs without curating what is retained.
  - On AIME 2024, Claude 3.5 Sonnet's baseline accuracy was 23.3% and GPT-4o's was 20.0%, with majority voting providing zero improvement over single-shot inference — illustrating the ceiling of non-adaptive approaches.

---

### Proposed Approach
- Dynamic Cheatsheet (DC) is a lightweight, parameter-free framework that augments a black-box LLM with a persistent, self-curating external memory that evolves across sequential inference queries without any gradient-based updates.
  - Unlike RAG (which retrieves from a fixed external corpus) or fine-tuning (which modifies weights), DC dynamically curates a compact library of reusable strategies, code snippets, and solution heuristics drawn entirely from the model's own test-time experience.
  - The framework has two core modules: a **Generator** (`Gen(x_i, M_i)`) that conditions on both the current query and the current memory state, and a **Curator** (`Cur(M_i, x_i, ỹ_i)`) that updates memory after each query by assessing solution quality without access to ground-truth labels, pruning faulty heuristics, and consolidating entries for compactness and generalizability.
- Two primary variants are introduced: **DC-Cu (Cumulative)**, which curates memory after generation and uses the full accumulated cheatsheet in subsequent queries; and **DC-RS (Retrieval & Synthesis)**, which first retrieves the top-k most similar past input-output pairs (via cosine similarity over embeddings, k=3) before updating the memory and generating a response, enabling direct exemplar reuse alongside abstracted heuristics.
  - DC-RS addresses two weaknesses of DC-Cu: the inability to incorporate insights from the current query before responding, and the lack of direct access to historical input-output pairs — particularly valuable for diverse, domain-spanning benchmarks like GPQA-Diamond.
  - Memory is intentionally kept selective and succinct — storing transferable strategies rather than raw transcripts — to prevent context ballooning and maintain efficient retrieval.

---

### Results & Capabilities
- DC dramatically improves performance on tasks where a reusable computational strategy exists and can be discovered early in the test sequence: GPT-4o's accuracy on Game of 24 rose from 10% (baseline) to 99% under DC-RS, after the model discovered and stored a Python brute-force solver and subsequently retrieved it for all remaining instances.
  - The gap between DC-∅ (empty memory, 19%) and DC-RS (99%) on Game of 24 isolates memory curation and retrieval as the primary driver of this gain rather than structured prompting alone.
- On AIME math competition problems, Claude 3.5 Sonnet achieved its largest gains: AIME 2024 accuracy rose from 23.3% to 50.0% under DC-Cu (a 27% absolute gain), AIME 2025 from 6.7% to 36.7%, and AIME 2020–2024 from 6.7% to 40.6% under DC-RS — driven by the accumulation of algebraic, combinatorial, and geometric strategies across sequential questions.
- DC enables near-perfect performance on structured arithmetic tasks: both Claude 3.5 Sonnet and GPT-4o reached 97–100% accuracy on Math Equation Balancer (from baselines of 44.8% and 50.0% respectively) by learning and reusing code-based operator-insertion routines.
- On knowledge-intensive tasks, DC yields meaningful but more modest gains: Claude 3.5 Sonnet improved from 59.6% to 68.7% on GPQA-Diamond under DC-RS (+9.1%), and from 74.0% to 82.0% on MMLU-Pro Physics (+8%), by maintaining compact reference guides on domain principles.
  - GPT-4o showed little to no gain on GPQA-Diamond (57.1% baseline vs. 57.1% DC-RS, with a slight dip in some variants), suggesting retrieval can introduce confusion when examples are topically diverse and retrieval quality is inconsistent.
- DC's memory-based adaptation substantially outperforms majority voting (MV): on AIME 2024, MV yielded 23.3% (identical to baseline), while DC-Cu reached 50.0%; on AIME 2025, MV yielded 6.7% vs. DC-Cu's 36.7%.
- A secondary emergent capability is the spontaneous adoption of code generation as a problem-solving strategy: DC nudges capable models toward recognizing when Python scripts are more reliable than internal chain-of-thought arithmetic, encoding these tool-use patterns into memory for reuse.

---

### Implications
- DC demonstrates that persistent, self-curating external memory is a viable form of test-time learning that substantially closes the gap between isolated inference and cumulative experience-driven problem-solving, without requiring model access, fine-tuning infrastructure, or ground-truth supervision.
- The finding that memory curation outperforms both full-history appending and majority voting reframes how practitioners should think about inference-time compute allocation: structured, selective retention of insights is more valuable than either statistical aggregation or brute-force context accumulation.
- The s

## Key Claims

1. Current language models process each input query separately without retaining insights from previous attempts during inference.
2. Dynamic Cheatsheet enables test-time learning without requiring explicit ground-truth labels or human feedback.
3. Claude 3.5 Sonnet's accuracy on AIME math exams more than doubled after applying Dynamic Cheatsheet.
4. GPT-4o's success rate on the Game of 24 puzzle increased from approximately 10% to 99% after discovering and reusing a Python-based solution via Dynamic Cheatsheet.
5. Dynamic Cheatsheet enabled GPT-4o and Claude to reach near-perfect accuracy on arithmetic equation balancing tasks, whereas their baselines stagnated around 50%.
6. Dynamic Cheatsheet achieved a 9% improvement for Claude on GPQA-Diamond and an 8% boost on MMLU-Pro Engineering and Physics.
7. Dynamic Cheatsheet curates memory focusing on concise, transferable snippets rather than entire transcripts to facilitate meta-learning and avoid context ballooning.
8. Dynamic Cheatsheet does not modify underlying model parameters and is compatible with black-box LLM APIs.
9. Claude 3.5 Sonnet's AIME 2024 accuracy jumped from 23% to 50% under DC-Cu, more than doubling its baseline score.
10. Claude 3.5 Sonnet gained 30% accuracy on AIME 2025 using Dynamic Cheatsheet.

## Capabilities

- Persistent external memory augmentation (Dynamic Cheatsheet) enables black-box LLMs to accumulate and reuse strategies, code snippets, and heuristics across sequential queries at inference time without weight updates, dramatically improving performance on challenging reasoning tasks
- LLMs can spontaneously discover, encode, and reuse code-based solutions (e.g., Python brute-force scripts) through iterative inference, enabling near-perfect performance on algorithmic tasks previously solved with poor accuracy
- Self-curated memory synthesis outperforms full-context history appending for multi-step mathematical reasoning — DC-Cu achieves 50% on AIME 2024 vs 26.7% for full-history and 23.3% baseline for Claude 3.5 Sonnet; GPT-4o drops to 13.3% under full-history vs 40% under DC-RS
- Memory-based test-time adaptation outperforms majority voting for complex reasoning — DC-Cu achieves 50% on AIME 2024 vs 23.3% for majority voting (3 samples) for Claude 3.5 Sonnet

## Limitations

- DC is ineffective for smaller/weaker models (GPT-4o-mini, Claude 3.5 Haiku) because insufficient base capability means memory is populated with low-quality or incorrect strategies that reinforce rather than correct errors
- DC's sequential structure is incompatible with large-scale parallel or batch inference workloads, limiting production applicability
- LLMs struggle to generate long, well-organized outputs for memory curation, causing memory degradation over time through truncation or abbreviation of existing entries
- Poorly filtered retrieval in DC-RS can introduce confusion and degrade performance when queries are diverse or loosely related — GPT-4o's GPQA-Diamond performance occasionally dipped due to suboptimal retrieval choices
- DC effectiveness depends heavily on inter-task structural similarity — when test examples share reusable structure, gains are dramatic; on heterogeneous tasks DC provides limited or negative benefit
- Faulty heuristics that enter memory get amplified across subsequent queries, with error clustering in latent embedding space causing systematic propagation of wrong strategies to semantically similar problems
- Memory curator has no access to ground-truth labels and must self-assess solution correctness, making curation reliability fundamentally bounded by model self-evaluation accuracy — which is the same capability DC is trying to improve
- Significant token overhead as memory accumulates — DC-Cu increases average token usage approximately 5x over baseline (370 → 1831 tokens on AIME 2024), creating substantial inference cost scaling that grows with session length
- R1-style reasoning models (DeepSeek R1, o1) gain minimal benefit from DC because their verbose chain-of-thought outputs are too long to be compressed into compact, reusable heuristics
- DC success is model-specific even among frontier models — Claude 3.5 Sonnet failed to internalize a Python-based strategy for Game of 24 (14% under DC vs 99% for GPT-4o), revealing that DC amplifies model-specific behavioral tendencies rather than providing a universal capability boost
- DC is evaluated exclusively on sequential same-distribution benchmark tasks — real-world heterogeneous query streams, multi-user systems, and cross-domain deployments are absent from evaluation, leaving generalization to production conditions entirely unvalidated
- GPT-4o performance actively degraded under DC on MMLU-Pro Engineering tasks (53.2% baseline → 44.0% DC-Cu) and on AIME under full-history (20% → 13.3%), showing accumulated memory can actively harm performance when domain diversity exceeds memory quality

## Bottlenecks

- Inter-task semantic similarity is a prerequisite for DC-style memory reuse — when deployed on heterogeneous or non-stationary query distributions, stored strategies fail to transfer and memory-based test-time learning stalls or regresses
- Base model generative capability gates memory-augmented test-time learning — smaller models and verbosity-prone reasoning models (R1-style) cannot produce compact, reusable strategies, so memory seeding fails and DC provides no benefit or actively degrades performance
- Sequential memory update dependency blocks parallelization of DC-based inference, preventing scaling to batch workloads and high-throughput production deployments where queries must be processed independently
- LLM output generation quality asymmetry — models read long contexts well but cannot generate equivalently long, structured outputs — creates systematic memory curation degradation requiring external database infrastructure to work around

## Breakthroughs

- Inference-time tool discovery and persistent memory enables near-perfect (99%) accuracy on algorithmic tasks — a ~10x improvement from 10% baseline without any weight updates — demonstrating that inference-time strategy accumulation can functionally substitute for parametric knowledge in well-struct
- Persistent external memory more than doubles AIME mathematical competition performance (23% → 50% for Claude 3.5 Sonnet on AIME 2024) without parameter updates, demonstrating that inference-time knowledge accumulation can approach fine-tuning-level gains on high-difficulty mathematical reasoning

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/claude-35-haiku|Claude 3.5 Haiku]]
- [[entities/claude-35-sonnet|Claude 3.5 Sonnet]]
- [[entities/dynamic-cheatsheet|Dynamic Cheatsheet]]
- [[entities/gpt-4o|GPT-4o]]
- [[entities/game-of-24|Game of 24]]
