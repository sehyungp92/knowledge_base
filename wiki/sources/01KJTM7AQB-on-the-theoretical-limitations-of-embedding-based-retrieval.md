---
type: source
title: On the Theoretical Limitations of Embedding-Based Retrieval
source_id: 01KJTM7AQBVQ8DCDMHH6B4J318
source_type: paper
authors:
- Orion Weller
- Michael Boratko
- Iftekhar Naim
- Jinhyuk Lee
published_at: '2025-08-28 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- knowledge_and_memory
- model_architecture
- representation_learning
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# On the Theoretical Limitations of Embedding-Based Retrieval

**Authors:** Orion Weller, Michael Boratko, Iftekhar Naim, Jinhyuk Lee
**Published:** 2025-08-28 00:00:00
**Type:** paper

## Analysis

# On the Theoretical Limitations of Embedding-Based Retrieval
2025-08-28 00:00:00 · paper · Orion Weller, Michael Boratko, Iftekhar Naim, Jinhyuk Lee
https://arxiv.org/pdf/2508.21038

---

### Motivation & Prior Limitations
- Vector embedding models (dense retrievers) have been increasingly tasked with instruction-following, reasoning, and coding retrieval, yet a common assumption holds that any failures stem from unrealistic queries or insufficient training data rather than fundamental architectural constraints.
  - Prior empirical work (e.g., Reimers & Gurevych 2020) observed that smaller-dimension embeddings produce more false positives at scale, but without a theoretical grounding connecting embedding dimension to representational capacity.
  - Benchmarks like BEIR, QUEST, and BRIGHT probe empirical limits but cover only an infinitesimally small fraction of possible top-k query-document combinations—QUEST's 3,357 queries against 325k documents represent a negligible sample of the ≈7.1×10⁹¹ possible top-20 document subsets—masking the true structural limits of single-vector retrieval.
- The rise of instruction-based retrieval (logical operators, multi-condition queries, reasoning over corpora) continuously increases the number of distinct top-k document subsets that must be representable, pushing models toward a regime where their geometric representational capacity is theoretically bounded.

---

### Proposed Approach
- The paper provides a formal theoretical connection between communication complexity theory (specifically, the sign-rank of the query-relevance matrix) and the minimum embedding dimension required to represent all top-k retrieval objectives, proving that for any fixed dimension d there exist retrieval tasks that cannot be solved by any single-vector embedding model.
  - The core result (Proposition 2) shows that the row-wise-order-preserving rank of a binary relevance matrix A is bounded below by rank±(2A − 1) − 1 and above by rank±(2A − 1), linking retrieval capacity directly to the sign-rank of the ±1 version of the qrel matrix—a quantity known to grow arbitrarily large.
  - A "free embedding" empirical protocol is introduced: query and document vectors are directly optimized via gradient descent (Adam, InfoNCE loss, full-batch) over the target qrel matrix without any natural-language constraints, yielding the best-case upper bound on what any embedding model could possibly achieve for a given dimension.
- The LIMIT dataset is constructed as a realistic natural-language instantiation of the theoretical hard case: 50k documents (people with random liked attributes), 1,000 queries of the form "who likes X?", k=2 relevant documents per query, with the qrel matrix chosen to maximize combinatorial coverage (46 documents, C(46,2)=1,035 combinations, the densest pattern that fits within 1,000 queries).
  - Dataset design deliberately uses trivially simple queries and documents to isolate the combinatorial-geometric bottleneck from confounding factors like query complexity or domain mismatch.

---

### Results & Capabilities
- Free-embedding optimization reveals a critical-n curve well-fit by a degree-3 polynomial (y = −10.53 + 4.03d + 0.052d² + 0.0037d³, r²=0.999), extrapolating critical document counts of ~500k at d=512, ~1.7M at d=768, ~4M at d=1024, and ~250M at d=4096—all insufficient for web-scale corpora even under ideal test-set optimization conditions.
  - At k=2, directly optimizing free embeddings fails once the number of documents exceeds these critical-n thresholds, confirming the theoretical bound holds empirically in its strongest possible form.
- State-of-the-art single-vector models (Gemini Embeddings, Qwen3 Embeddings, GritLM 7B, E5-Mistral 7B, Promptriever, Snowflake Arctic Embed L) all score below 20% Recall@100 on the full LIMIT dataset despite the trivial query form.
  - Even in the small 46-document variant, no single-vector model solves the task at Recall@20, and the best Recall@2 scores remain below 60%.
  - Performance correlates strongly with embedding dimension: larger dimensions consistently yield higher scores across all tested models.
- Fine-tuning on an in-domain training split (same attribute format, non-overlapping attributes) yields only marginal improvement (up to 2.8 Recall@10), confirming the failure is not domain shift but a structural geometric limitation; fine-tuning on the test set enables overfitting (solving the task), consistent with free-embedding results.
- The dense qrel pattern (all C(46,2) combinations) is dramatically harder than other patterns: switching GritLM from a random or disjoint qrel pattern to the dense pattern drops Recall@100 by ~50 absolute points; E5-Mistral suffers a ~10× reduction (40.4 → 4.8 Recall@100).
- Alternative architectures escape the single-vector bottleneck to varying degrees: BM25 achieves near-perfect scores (treating vocabulary as an implicitly very high-dimensional sparse space); GTE-ModernColBERT (multi-vector, MaxSim) substantially outperforms single-vector models; Gemini-2.5-Pro used as a long-context reranker over all 46 documents solves 100% of 1,000 queries in a single forward pass.
- LIMIT performance shows no meaningful correlation with BEIR scores, indicating that MTEB/BEIR rankings do not predict which models approach or avoid this geometric limitation.

---

### Implications
- The single-vector embedding paradigm has a hard geometric ceiling: as instruction-following and agent-driven retrieval proliferate (with logical operators, multi-condition filters, and hyper-specific queries), the combinatorial diversity of top-k subsets demanded will inevitably exceed what any realistically-dimensioned dense embedding can represent, regardless of training scale or data quality.
- Current retrieval benchmarks systematically underestimate this limitation because they sample only a negligible fraction of possible query-document combination space; benchmark designers should deliberately stress-tes

## Key Claims

1. The number of top-k subsets of documents capable of being returned as the result of some query is limited by the dimension of the embedding.
2. State-of-the-art embedding models fail on the LIMIT dataset despite the simple nature of the task, with recall@100 below 20%.
3. For any fixed embedding dimension d, there exists a binary relevance matrix which cannot be captured via d-dimensional embeddings.
4. The minimum embedding dimension required to represent a retrieval task is bounded by the sign-rank of the query-relevance matrix.
5. The critical-n (maximum number of documents representable) as a function of embedding dimension d fits a 3rd-degree polynomial: y = -10.5322 + 4.0309d + 0.0520d^2 + 0.0037d^3.
6. For web-scale search, even the largest embedding dimensions with ideal test-set optimization are insufficient to model all document combinations.
7. Poor performance of embedding models on LIMIT is not due to domain shift, as training on in-domain data provides negligible improvement.
8. Models can overfit to the LIMIT test set, indicating the task is solvable in principle but is fundamentally limited by embedding dimension.
9. Real-world embedding models are multiple times more limited than free-embedding best-case optimization, exacerbating dimensional constraints.
10. Denser qrel patterns (maximizing document combinations tested) make retrieval tasks significantly harder for embedding models.

## Capabilities

- Cross-encoder/reranker models (e.g., Gemini-2.5-Pro) can solve complex combination retrieval tasks that defeat single-vector embedding models, achieving 100% recall on tasks where SOTA embeddings score below 60% recall@2
- Multi-vector retrieval models (ColBERT-style, e.g. GTE-ModernColBERT) significantly outperform single-vector models on combination-heavy retrieval tasks by using multiple vectors per sequence with MaxSim scoring
- BM25 sparse retrieval achieves near-perfect scores on combination-dense retrieval tasks due to its effectively very high-dimensional implicit vector space
- Free embedding optimization (directly optimizing query/document vectors over the test set qrel matrix) can solve retrieval tasks that defeat real models, providing a tight empirical upper bound on the theoretical sign-rank limit
- Instruction-diverse embedding model training (e.g., Promptriever) utilizes embedding dimensions more fully than MRL-trained models, yielding better performance on combination-heavy retrieval tasks

## Limitations

- Single-vector embedding models have a provably hard combinatorial ceiling: for any fixed embedding dimension d, there exist retrieval tasks whose top-k document combinations cannot be represented by any query vector, regardless of training data or model scale
- SOTA single-vector embedding models (GritLM, Qwen3, Gemini Embeddings, E5-Mistral) score below 20% recall@100 on LIMIT, a dataset with trivially simple natural-language queries ('who likes Apples?') over 50k documents
- Even under ideal best-case conditions (free embedding optimization directly on the test qrel matrix), practical embedding dimensions (512–4096) cannot represent all top-k document combinations at web-scale corpus sizes
- Real-world embedding models are multiple times more dimensionally limited than the theoretical free-embedding bound, meaning practical retrieval capability degrades substantially faster than theory predicts
- Fine-tuning single-vector embedding models on in-domain training data produces essentially no improvement on combination-dense retrieval (less than 3 absolute recall@10 gain on LIMIT), confirming the failure is architectural not a data distribution problem
- Existing retrieval evaluation benchmarks (BEIR/MTEB) test an infinitesimally small fraction of the possible query-document combination space, systematically concealing embedding model failures that appear in real agentic usage
- MTEB/BEIR benchmark scores show no correlation with performance on combination-dense retrieval (LIMIT), meaning high MTEB rankings do not predict whether a model can handle agentic or instruction-following queries
- Multi-vector models (ColBERT-style) are not deployed for instruction-following or reasoning-based retrieval, leaving the critical question of whether their expressiveness advantage transfers to the most demanding retrieval scenarios entirely open
- Cross-encoder rerankers solve the embedding combination limitation in principle but are computationally prohibitive for first-stage retrieval at scale, creating a hard expressiveness-efficiency tradeoff with no current solution
- Sparse and lexical retrieval models cannot generalize to instruction-following or reasoning-based queries where there is no lexical or paraphrase overlap between query and relevant documents
- The theoretical framework cannot identify a priori which specific retrieval tasks will fail for a given embedding model — only that some subset provably will — leaving practitioners unable to predict failures without empirical testing
- The theoretical limitations proven for single-vector embeddings do not extend to multi-vector models; their theoretical capacity bounds remain uncharacterized, making it unknown how far they can push against the ceiling

## Bottlenecks

- Single-vector embedding dimension is a provably hard ceiling on retrieval combination capacity: for web-scale corpora with dense instruction-following queries, no practical embedding dimension can represent all required top-k combinations
- No retrieval architecture currently combines the ANN-scalability of single-vector embeddings, the combinatorial expressiveness of cross-encoders, and the instruction-following generalization needed for agentic search
- Standard retrieval evaluation benchmarks (MTEB/BEIR) systematically hide embedding model combination failures by sampling a vanishingly small fraction of the qrel combination space, blocking the community from understanding true model limits

## Breakthroughs

- Mathematical proof (via sign-rank theory from communication complexity) that single-vector embedding models have a fundamental, dimension-bounded combinatorial capacity limit that cannot be overcome by better training data, larger models, or any amount of fine-tuning

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/model_architecture|model_architecture]]
- [[themes/representation_learning|representation_learning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]

## Key Concepts

- [[entities/bm25|BM25]]
