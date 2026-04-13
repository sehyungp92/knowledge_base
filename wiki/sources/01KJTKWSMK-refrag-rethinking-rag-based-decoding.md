---
type: source
title: 'REFRAG: Rethinking RAG based Decoding'
source_id: 01KJTKWSMKJ3SMNHSW8EDA0W5J
source_type: paper
authors:
- Xiaoqiang Lin
- Aritra Ghosh
- Bryan Kian Hsiang Low
- Anshumali Shrivastava
- Vijai Mohan
published_at: '2025-09-01 00:00:00'
theme_ids:
- context_engineering
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# REFRAG: Rethinking RAG based Decoding

**Authors:** Xiaoqiang Lin, Aritra Ghosh, Bryan Kian Hsiang Low, Anshumali Shrivastava, Vijai Mohan
**Published:** 2025-09-01 00:00:00
**Type:** paper

## Analysis

# REFRAG: Rethinking RAG based Decoding
2025-09-01 00:00:00 · paper · Xiaoqiang Lin, Aritra Ghosh, Bryan Kian Hsiang Low, Anshumali Shrivastava, Vijai Mohan
https://arxiv.org/pdf/2509.01092

---

### Motivation & Prior Limitations
- Long-context inputs in RAG systems impose severe latency and memory costs because TTFT scales quadratically and KV cache memory scales linearly with prompt length, creating a fundamental trade-off between knowledge enrichment and inference efficiency.
  - Prior work like CEPE achieves only 2.01× TTFT acceleration at 16K tokens and is limited to prefix-context applications, making it unsuitable for multi-turn RAG or summarization where context must be inserted at arbitrary positions.
- Existing long-context optimization methods treat RAG inference as a generic LLM problem, ignoring three structural properties unique to RAG: sparse informational density across retrieved passages, availability of pre-computed retrieval encodings that go unused during decoding, and block-diagonal attention patterns arising from low cross-passage semantic similarity due to diversity and deduplication during re-ranking.
  - These block-diagonal attention patterns mean that most cross-chunk attention computations during decoding are effectively zero, representing wasted computation that generic sparse attention methods do not exploit.
- Compressive transformer approaches (e.g., Chevalier et al. 2023) that use compressed embeddings require sequential compression, preventing pre-computation and caching of chunk embeddings, and restrict compression to the prefix position only.

---

### Proposed Approach
- REFRAG (REpresentation For RAG) is a decoding framework that replaces retrieved passage tokens in the decoder input with pre-computed, compressed chunk embeddings from a lightweight encoder (e.g., RoBERTa), reducing the decoder's effective input length by a factor of k (the chunk compression rate) while preserving the autoregressive structure.
  - A lightweight encoder processes context into per-chunk embeddings, which are projected into the decoder's token embedding space via a learned projection layer; the decoder then attends to these chunk embeddings alongside normal token embeddings for the query, enabling "compress anywhere" — compression at arbitrary positions in the prompt, not just the prefix.
  - Unlike CEPE, which uses cross-attention to full token sequences and disrupts causal structure, REFRAG feeds compressed embeddings directly into the standard decoder input stream, maintaining compatibility with multi-turn and agentic applications.
- Training follows a two-stage recipe: a reconstruction task (encoder + projection trained to reconstruct original tokens from chunk embeddings, with decoder frozen) followed by continual pre-training on next-paragraph prediction using chunk embeddings, both employing curriculum learning that incrementally increases the number of chunks reconstructed to address the exponential difficulty of compressing k tokens into a fixed-length vector.
  - Curriculum learning was found to be essential — direct CPT without it failed to reduce perplexity even on the reconstruction task.
- A lightweight RL policy trained with next-paragraph prediction perplexity as a negative reward performs selective compression at inference time, determining which chunks to expand back to full token representation and which to keep compressed, enabling adaptive compression rates without recomputing chunk embeddings.
  - The RL policy outperforms heuristic alternatives (perplexity-ascending, perplexity-descending, and random chunk selection) across all tested compression rates, and REFRAG16 with selective RL compression at effective rate 8 outperforms REFRAG8 with full compression, demonstrating that the policy adds value beyond what the base compression rate captures.

---

### Results & Capabilities
- REFRAG achieves 30.85× TTFT acceleration over LLaMA (3.75× over CEPE, the prior state of the art) at a compression rate of 32, with no loss in perplexity on held-out datasets including Arxiv, Book, PG19, and ProofPile.
  - At compression rate 16 with cached embeddings, TTFT acceleration reaches 16.53× over LLaMA and 2.01× over CEPE, with a 9.3% average log-perplexity improvement over CEPE across four datasets.
- REFRAG extends the effective context window of LLaMA-2-7B (native 4K) by 16×, enabling inference over 16K+ token contexts without positional encoding modifications, because attention complexity now scales quadratically with the number of chunks rather than the number of tokens.
  - At context lengths of 4096–16384, REFRAG8 and REFRAG16 consistently match or outperform LLaMA-32K (fine-tuned for extended context) on perplexity benchmarks.
- On RAG downstream tasks across 16 datasets (NQ, FEVER, TQA, MMLU, CommonsenseQA, BoolQ, and others), REFRAG8 with 8 passages achieves equivalent latency to LLaMAFT with 1 passage while matching or exceeding its accuracy; REFRAG16 and REFRAG32 achieve lower latency than LLaMAFT with 1 passage while still outperforming it on most tasks.
  - Under a weak retriever scenario at equal latency, REFRAG achieves a 1.93% average accuracy gain over LLaMA across 16 RAG tasks; the gains are attributed to REFRAG's ability to include more retrieved passages within the same latency budget.
- In multi-turn conversational RAG (ORConvQA, QReCC, TopiOCQA), REFRAG consistently outperforms LLaMAFT at ≥4 and ≥6 turns with 10 passages, because LLaMAFT's 4K context window requires truncating conversational history while REFRAG's compression accommodates it.
- Compression rate 64 was found to degrade performance significantly, suggesting a practical upper bound on the compression rate; compression rate 32 remains competitive while 64 is described as overly aggressive.
- Decoder scale dominates performance gains — scaling from LLaMA-2-7B to LLaMA-2-13B reduces loss substantially, while scaling the encoder from RoBERTa-Base to RoBERTa-Large yields only modes

## Key Claims

1. RAG contexts exhibit block-diagonal attention patterns because retrieved passages have low semantic similarity due to diversity or deduplication during re-ranking
2. Most computations over RAG context during decoding are unnecessary and can be eliminated with minimal impact on performance due to attention sparsity
3. REFRAG achieves 30.85x time-to-first-token acceleration over LLaMA, representing 3.75x improvement over the previous state-of-the-art (CEPE), without loss in perplexity
4. REFRAG can extend the effective context size of LLMs by 16x through its compression framework
5. KV cache memory scales linearly with prompt length, while time-to-first-token latency increases quadratically and time-to-iterative-token latency grows linearly
6. REFRAG requires no modifications to the LLM architecture and introduces no new decoder parameters
7. REFRAG uses pre-computed compressed chunk embeddings from a lightweight encoder to replace full token sequences from retrieved passages in the decoder input
8. REFRAG supports compression at arbitrary positions within the prompt (compress anywhere), unlike prior methods limited to prefix context
9. A lightweight RL policy in REFRAG selectively determines which chunks require full token input versus compressed embeddings, enabling adaptive compression rates at inference time
10. For short context lengths, REFRAG achieves up to k× acceleration in TTFT and throughput; for longer contexts, acceleration reaches up to k² for both metrics

## Capabilities

- RAG-specific decoding framework (REFRAG) achieves 30.85× TTFT acceleration over standard LLaMA by exploiting block-diagonal attention sparsity in retrieved passages, without loss in downstream accuracy or perplexity
- Chunk embedding compression enables 16× context window extension for LLMs in RAG settings without modifying positional encodings or base model architecture
- RL-trained selective compression policy dynamically determines which context chunks require full token representation versus compressed embeddings at inference time, enabling adaptive compression without recomputing chunk embeddings
- Pre-computable chunk embeddings in RAG enable reuse across multiple queries from a shared retrieval corpus, eliminating redundant context encoding during decoding
- Compressed chunk embeddings support arbitrary placement within LLM prompts (not restricted to prefix), enabling multi-turn RAG and long document summarization while preserving autoregressive decoding

## Limitations

- Chunk compression has a practical ceiling around 32×; compression rate of 64 causes significant performance degradation, suggesting a fundamental information-density limit on fixed-size chunk embeddings
- REFRAG requires a complex multi-stage training pipeline — reconstruction task with curriculum learning, then continual pre-training (20B tokens), then SFT, then RL for selective compression — making it substantially harder to adapt to new base models than standard fine-tuning
- Dramatic accuracy collapse on BoolQ (from ~30% for standard LLaMA to 1.99–5.87% for REFRAG variants in short-context same-latency settings), revealing that chunk-level compression loses information critical for certain fine-grained binary judgment tasks
- TTIT (time-to-iterative-token) acceleration is dramatically less than TTFT improvement — only 1.5–2.5× versus 30× — meaning total generation latency for long responses remains largely constrained even with REFRAG
- REFRAG's compression benefits are structurally specific to RAG contexts (block-diagonal attention arising from diversity/deduplication) and are not applicable as a general long-context solution for dense narrative text
- Training restricted to Books and ArXiv domains only; generalization to enterprise RAG over structured or domain-specific content (code, medical literature, legal documents) is unverified
- Larger encoder model (RoBERTa-Large vs RoBERTa-Base) provides diminishing returns and may hurt performance under limited training data, indicating the system is data-hungry and sensitive to encoder-decoder size pairing
- Code not publicly released at time of publication — research results cannot be reproduced, integrated into production pipelines, or independently validated
- Performance advantage under weak retrieval is modest at equal passage count (+0.71%), meaning REFRAG's primary benefit is latency-aware context reinvestment (fitting more passages within a budget) rather than intrinsically better information extraction from compressed representations

## Bottlenecks

- RAG inference bottlenecked by treating retrieved-passage contexts as generic long-context inputs, wasting quadratic attention computation on semantically independent (block-diagonal) passages that do not attend to each other during decoding
- KV cache memory scales linearly and TTFT scales quadratically with prompt length, creating a hard trade-off between context richness (more retrieved passages) and system latency in RAG — operators must choose between accuracy and responsiveness

## Breakthroughs

- REFRAG demonstrates that RAG contexts exhibit exploitable block-diagonal attention sparsity (retrieved passages are semantically independent due to diversity/deduplication in re-ranking), enabling 30.85× TTFT acceleration and 16× context extension via chunk-level compression without accuracy loss — 

## Themes

- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
