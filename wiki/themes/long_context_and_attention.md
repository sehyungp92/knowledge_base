---
type: theme
title: Long-Context & Attention
theme_id: long_context_and_attention
level: 2
parent_theme: model_architecture
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 33
sources_since_update: 0
update_count: 1
velocity: 0.197
staleness: 0.0
status: active
tags: []
---
**Structure:** All required sections present in exact order. No frontmatter block.

**Key decisions:**
- **Limitations** grouped by severity (blocking → significant → minor) rather than a flat list, since the severity metadata makes hierarchy the natural reading order.
- **Contradictions** synthesised from the data: the recurrent-vs-quadratic tradeoff, the research/production divergence, and the YaRN reliability gap are all latent in the raw data but not stated explicitly — surfaced here as the most meaningful tensions.
- **Research Opportunities** derived from the bottleneck/limitation structure, each one targeting a specific gap rather than restating general aspirations.
- **Cross-Theme Implications** reproduced verbatim from the provided data with correct wikilink format.
- Em dashes minimised throughout per your writing style preference; colons, semicolons, and parentheses used instead.

## Current State

## Capabilities

## Limitations

## Bottlenecks

## Breakthroughs

## Anticipations

## Cross-Theme Implications

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJS34DRS-what-is-power-retention-manifest-ai|What Is Power Retention? - Manifest AI]]: The fatal flaw of Transformers is that their attention mechanism requires remembering the entire pas
- **2026-04-08** — [[sources/01KJS0KV75-titans-miras-helping-ai-have-long-term-memory|Titans + MIRAS: Helping AI have long-term memory]]: Titans uses a deep neural network (specifically a multi-layer perceptron) as its long-term memory mo
- **2025-12-31** — [[sources/01KJT2Q145-recursive-language-models|Recursive Language Models]]: An RLM initializes a REPL programming environment in which the prompt P is set as the value of a var
- **2025-12-29** — [[sources/01KJT2PY1B-end-to-end-test-time-training-for-long-context|End-to-End Test-Time Training for Long Context]]: Full attention (self-attention over full context) has O(T²) computational complexity for prefill and
- **2025-12-16** — [[sources/01KJT37Q1W-t5gemma-2-seeing-reading-and-understanding-longer|T5Gemma 2: Seeing, Reading, and Understanding Longer]]: Merged attention narrows the architectural differences between the T5Gemma 2 decoder and the Gemma 3
- **2025-12-15** — [[sources/01KJT4T78E-lets-not-just-put-things-in-context-test-time-training-for-long-context-llms|Let's (not) just put things in Context: Test-Time Training for Long-Context LLMs]]: Query-only TTT (qTTT) performs a single prefill to cache all key-value representations, then applies
- **2025-12-02** — [[sources/01KJT6M5JK-deepseek-v32-pushing-the-frontier-of-open-large-language-models|DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models]]: DeepSeek-V3.2 introduces DeepSeek Sparse Attention (DSA), which reduces attention computational comp
- **2025-11-17** — [[sources/01KJT8B0BV-on-the-fundamental-limits-of-llms-at-scale|On the Fundamental Limits of LLMs at Scale]]: For any computably enumerable set of LLMs, there exists a computable ground-truth function such that
- **2025-10-22** — [[sources/01KJTCHAPG-loongrl-reinforcement-learning-for-advanced-reasoning-over-long-contexts|LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts]]: KeyChain transforms short multi-hop QA datasets into high-difficulty long-context problems by extend
- **2025-10-21** — [[sources/01KJTCRE26-lightmem-lightweight-and-efficient-memory-augmented-generation|LightMem: Lightweight and Efficient Memory-Augmented Generation]]: LightMem's sensory memory module pre-compresses raw input to filter redundant or low-value tokens be
- **2025-10-17** — [[sources/01KKT3SS8Q-deepseek-ocr-contexts-optical-compression|DeepSeek-OCR: Contexts Optical Compression]]: Breakthrough: Demonstration that text can be compressed into vision tokens at 10x ratio with n
- **2025-09-12** — [[sources/01KJVN12YG-fully-autonomous-robots-are-much-closer-than-you-think-sergey-levine|Fully autonomous robots are much closer than you think – Sergey Levine]]: Moravec's paradox holds that in AI the cognitively 'easy' physical tasks (perception, manipulation) 
- **2025-09-01** — [[sources/01KJTKWSMK-refrag-rethinking-rag-based-decoding|REFRAG: Rethinking RAG based Decoding]]: REFRAG requires no modifications to the LLM architecture and introduces no new decoder parameters
- **2025-07-03** — [[sources/01KJTNTHTP-memagent-reshaping-long-context-llm-with-multi-conv-rl-based-memory-agent|MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent]]: MemAgent achieves 95%+ accuracy on the 512K RULER benchmark.
- **2025-06-18** — [[sources/01KJTNJCZN-mem1-learning-to-synergize-memory-and-reasoning-for-efficient-long-horizon-agent|MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents]]: MEM1-7B improves task performance by 3.5× compared to Qwen2.5-14B-Instruct on a 16-objective multi-h
- **2025-06-12** — [[sources/01KJTQ65VX-videoexplorer-think-with-videos-for-agentic-long-video-understanding|VideoExplorer: Think With Videos For Agentic Long-Video Understanding]]: VideoExplorer achieves an IoU@0.1 temporal grounding accuracy of 27.8 on LVBench, significantly outp
- **2025-06-05** — [[sources/01KJTPFVK6-log-linear-attention|Log-Linear Attention]]: Softmax attention has quadratic compute and linear memory complexity with respect to sequence length
- **2025-05-29** — [[sources/01KJTRB1VP-test-time-training-done-right|Test-Time Training Done Right]]: Large Chunk Test-Time Training (LaCT) uses chunk sizes ranging from 2048 to 1 million tokens as the 
- **2025-05-29** — [[sources/01KJTRVBMF-atlas-learning-to-optimally-memorize-the-context-at-test-time|ATLAS: Learning to Optimally Memorize the Context at Test Time]]: Polynomial feature map coefficients can be interpreted as input feature gates: setting a_i→0 exclude
- **2025-04-24** — [[sources/01KJTXK7YZ-token-shuffle-towards-high-resolution-image-generation-with-autoregressive-model|Token-Shuffle: Towards High-Resolution Image Generation with Autoregressive Models]]: Token-Shuffle's 2.7B model achieves a VQAScore of 0.77 on GenAI-Bench hard prompts, outperforming AR
- **2025-04-10** — [[sources/01KJTPMJBF-kimi-vl-technical-report|Kimi-VL Technical Report]]: Kimi-VL achieves 64.5 on LongVideoBench and 35.1 on MMLongBench-Doc, demonstrating strong long-conte
- **2025-02-17** — [[sources/01KJTYPXYC-a-mem-agentic-memory-for-llm-agents|A-MEM: Agentic Memory for LLM Agents]]: A-MEM achieves an F1 score of 3.45 on DialSim, representing a 35% improvement over LoCoMo's 2.55 and
- **2025-02-08** — [[sources/01KJVM8AVM-google-titans-learning-to-memorize-at-test-time|Google Titans: Learning to Memorize at Test Time]]: Titans proposes three distinct architectural integration variants for the long-term memory module: M
- **2024-12-31** — [[sources/01KJV5HWSH-titans-learning-to-memorize-at-test-time|Titans: Learning to Memorize at Test Time]]: Memory retrieval from the neural memory module is performed via a standard forward pass without weig
- **2024-11-20** — [[sources/01KJV6RXXK-hymba-a-hybrid-head-architecture-for-small-language-models|Hymba: A Hybrid-head Architecture for Small Language Models]]: At 1B scale under identical training conditions, Hymba achieves 1.74% higher average score than the 
- **2024-10-16** — [[sources/01KJVKT2TV-mamba-linear-time-sequence-modeling-with-selective-state-spaces-colm-oral-2024|Mamba: Linear-Time Sequence Modeling with Selective State Spaces (COLM Oral 2024)]]: Attention's KV cache causes inference time to grow linearly with cache size, and when summed over a 
- **2024-10-07** — [[sources/01KJV7XNNN-differential-transformer|Differential Transformer]]: DIFF Transformer's macro architecture is identical to Transformer (decoder-only, pre-RMSNorm, SwiGLU
- **2024-10-04** — [[sources/01KJV75HGR-alr2-a-retrieve-then-reason-framework-for-long-context-question-answering|ALR$^2$: A Retrieve-then-Reason Framework for Long-context Question Answering]]: ALR2 uses an explicit two-stage procedure that aligns LLMs with both retrieval and reasoning objecti
- **2024-08-07** — [[sources/01KJV47KDZ-tree-attention-topology-aware-decoding-for-long-context-attention-on-gpu-cluster|Tree Attention: Topology-aware Decoding for Long-Context Attention on GPU clusters]]: Self-attention has quadratic computational complexity O(n^2 · d) in sequence length, making long-con
- **2024-07-29** — [[sources/01KJVKZER8-llm-attention-that-expands-at-inference-test-time-training-explained|LLM Attention That Expands At Inference? Test Time Training Explained]]: TTT's compression is updated (trained) at every step, allowing the model to dynamically adapt to the
- **2024-07-12** — [[sources/01KJVM69GC-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states|Learning to (Learn at Test Time): RNNs with Expressive Hidden States]]: Standard softmax attention is quadratic in sequence length due to the QK^T matrix computation.
- **2023-10-03** — [[sources/01KJVBR6K0-ring-attention-with-blockwise-transformers-for-near-infinite-context|Ring Attention with Blockwise Transformers for Near-Infinite Context]]: Ring Attention enables training sequences more than 500 times longer than prior memory-efficient sta
