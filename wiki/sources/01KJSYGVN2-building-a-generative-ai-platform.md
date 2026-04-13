---
type: source
title: Building A Generative AI Platform
source_id: 01KJSYGVN2S8CWYQXE7KNT7QRC
source_type: article
authors: []
published_at: '2024-07-25 00:00:00'
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Building A Generative AI Platform

**Authors:** 
**Published:** 2024-07-25 00:00:00
**Type:** article

## Analysis

# Building A Generative AI Platform
2024-07-25 · article
https://huyenchip.com/2024/07/25/genai-platform.html

---

## Briefing

**A production generative AI platform is not a single model call — it is a layered system of context construction, guardrails, routing, caching, and observability that must be assembled incrementally. The article argues that context construction (especially RAG) is the analogue of feature engineering in classical ML, and that caching is the most underrated component for cost and latency reduction. Understanding which components to add and when is the core engineering challenge separating toy demos from production deployments.**

### Key Takeaways
1. **Context construction is feature engineering** — Giving a model relevant external information at inference time is functionally equivalent to feature engineering in classical ML: it determines how well the model can process an input and directly reduces hallucinations.
2. **Hybrid search outperforms either retrieval method alone** — Production retrieval systems combine term-based (BM25/Elasticsearch) and embedding-based (vector search) retrieval sequentially or as an ensemble, with reranking as the bridge between cheap recall and precise precision.
3. **Prompt caching can eliminate billions of redundant token computations** — A 1,000-token system prompt reused across 1 million daily API calls wastes ~1 billion tokens per day without prompt cache; Google's context cache offers a 75% discount on cached tokens, signalling this will become standard.
4. **Agentic RAG extends read-only retrieval to write actions** — Web search, SQL execution, and document retrieval are all model-callable functions; adding write actions (email sending, database updates) makes systems vastly more capable but introduces prompt injection and data integrity risks.
5. **Query rewriting is a non-trivial prerequisite for accurate retrieval** — Conversational follow-up queries like "How about Emily Doe?" are semantically incomplete; without rewriting them into self-contained queries, retrieval returns irrelevant results and the entire RAG pipeline degrades.
6. **Model routers enable cost arbitrage across a heterogeneous model fleet** — Intent classifiers route simple queries to cheap models and complex ones to capable models; specialized routers are typically small, fast classification models that add minimal latency.
7. **Semantic cache is high-risk, high-reward** — It requires reliable embeddings, vector search, and a well-tuned similarity threshold; a miscalibrated threshold returns wrong cached answers, making it unsuitable unless cache hit rates are demonstrably high.
8. **Output guardrails and streaming are architecturally incompatible** — Stream completion exposes tokens to users before guardrails can evaluate the full response; teams must choose between latency (streaming) and safety (blocking evaluation).
9. **Observability must be built in from day one, not retrofitted** — Traces, metrics (TTFT, TBT, TPS, TPOT), and logs are the only way to understand pipeline failures; without them, debugging multi-step agentic flows is nearly impossible.
10. **Orchestration tools abstract too much too early** — Starting without LangChain/LlamaIndex forces explicit understanding of data flow and failure modes; orchestrators become valuable only once complexity justifies the abstraction cost.
11. **The Lost in the Middle effect changes context reranking priorities** — Unlike search ranking where position is critical, context reranking prioritises inclusion over exact order, though documents at the beginning and end of context are processed better by models.
12. **PII handling requires reversible masking, not deletion** — Sensitive data in prompts should be replaced with typed placeholders (e.g., `[PHONE NUMBER]`) and unmasked post-generation via a PII dictionary, preserving utility while preventing leakage to third-party APIs.

---

### RAG Architecture: From Simple Retrieval to Agentic Pipelines

- **The fundamental RAG pattern pairs a retriever with a generator**, where the retriever fetches relevant chunks from external memory sources and the generator produces a response conditioned on both the query and retrieved context.
  - External memory sources are typically unstructured documents (memos, contracts, news) that must be chunked before indexing because naively retrieving whole documents creates arbitrarily long contexts.
  - Chunk size is constrained by the model's maximum context length and application latency requirements — no single optimal chunk size exists across use cases.

- **Term-based retrieval (BM25, Elasticsearch) is the correct default starting point** before investing in embedding-based retrieval.
  - It is faster, cheaper, and works out of the box; both BM25 and Elasticsearch are described as "formidable baselines."
  - Term-based retrieval extends to images and videos via text metadata (titles, tags, captions).

- **Embedding-based retrieval uses ANN algorithms** (FAISS, ScaNN, ANNOY, hnswlib) to find nearest neighbours in vector space.
  - ANN-benchmarks evaluates algorithms on four metrics: recall, QPS, build time, and index size — each representing a different production tradeoff.
  - **Embedding-based retrieval is computationally expensive but can be significantly improved over time**, potentially outperforming term-based retrieval with investment.
  - Works across modalities: text, images, videos, audio, code, and even summaries of SQL tables and dataframes.

- **Hybrid search is the production standard**, typically implemented as a sequential pipeline: cheap term-based retrieval for candidate recall, followed by expensive vector search for reranking.
  - The ensemble pattern runs multiple retrievers in parallel and combines their relevance score rankings into a final ranking.
  - **Context reranking differs from search reranking**: exact position matters less than inclusion, because of the Lost in the Middle effect (Liu et a

## Key Claims

1. Having access to relevant information in the context can help the model generate more detailed responses while reducing hallucinations.
2. Context construction for foundation models is equivalent to feature engineering for classical ML models, serving the same purpose of giving the model the necessary information to process an input.
3. In-context learning enables a model to incorporate new information continually to make decisions, preventing it from becoming outdated.
4. RAG consists of two components: a generator (e.g. a language model) and a retriever.
5. In context reranking, models better understand documents placed at the beginning and end of the context, as opposed to the middle.
6. Context reranking differs from traditional search reranking in that the exact position of items is less critical than whether a document is included at all.
7. Ensemble retrieval combines multiple retrievers' rankings to generate a final ranking, improving retrieval quality.
8. Text-to-SQL RAG requires an intermediate step to predict which tables to use when many available tables cannot all fit in the model context.
9. Query rewriting is typically done using AI models to make ambiguous follow-up queries self-contained and resolve coreference in multi-turn conversations.
10. Samsung employees leaked proprietary company information to ChatGPT, leading Samsung to ban ChatGPT in May 2023.

## Capabilities

- Prompt caching allows overlapping prompt segments (e.g., system prompts, long documents) to be stored and reused, reducing both inference latency and cost significantly — implemented in major model APIs by mid-2024
- RAG pipelines demonstrably reduce hallucinations and enable models to answer queries beyond their training cutoff by injecting retrieved context, and are in broad production deployment
- Agentic RAG systems can autonomously invoke web search, term-based retrieval, embedding-based retrieval, and SQL execution as tool calls to dynamically augment context for each query
- Text-to-SQL pipelines translate natural language queries into executable SQL for structured data retrieval, with intermediate table-selection steps when schema size exceeds context limits
- Intent-based model routers classify query type and direct traffic to specialised models or pipelines (e.g., cheaper models for simple queries, specialist models for complex tasks), reducing cost and improving quality
- LLM-powered query rewriting resolves anaphora and conversational ellipsis in multi-turn dialogues, producing standalone queries suitable for retrieval, in production deployment
- Semantic caching for inference stores responses keyed by embedding similarity, enabling cache hits for paraphrased or near-duplicate queries rather than only exact matches
- Automated PII detection and reversible masking pipelines allow AI applications to sanitise inputs before sending to third-party model APIs and restore original values in outputs, in broad production use
- Write-action agentic workflows can automate complex end-to-end business processes (customer outreach, database updates, email sending) by chaining read and write tool calls

## Limitations

- Output guardrails are fundamentally incompatible with streaming completion mode — partial responses are streamed to users before the guardrail system can evaluate them, so unsafe content may be displayed before being caught
- There is no airtight mechanism to prevent employees or users from leaking private or proprietary information to third-party model APIs when using external model providers
- Guardrails add latency overhead significant enough that a minority of production teams choose to omit them entirely — revealing a real tension between safety coverage and response speed
- Prompt injection is an unresolved attack vector that uniquely threatens AI systems with tool access — attackers can manipulate model behaviour via crafted inputs in ways that have no close analogue in traditional software security
- Models exhibit 'lost in the middle' degradation — relevant documents placed in the middle of a long context are processed less reliably than those at the start or end, undermining RAG precision at scale
- Text-to-SQL breaks down when the number of available table schemas exceeds model context capacity, requiring an additional (and error-prone) intermediate table-selection step
- Agentic systems with write access require mandatory human approval gates for destructive operations, substantially reducing autonomy and throughput compared to read-only workflows
- Model internal knowledge is inherently unreliable for queries about information after the training cutoff — without external augmentation, models either hallucinate or refuse, with no reliable self-awareness of the gap
- Query rewriting fails when resolving references requires information the system does not possess — the model risks hallucinating identities (names, relationships) rather than acknowledging the query is unanswerable
- Prompt cache storage incurs significant ongoing cost and engineering complexity, including large memory footprints and cache invalidation challenges, offsetting some of the token-cost savings
- Open-source inference runtimes (e.g., llama.cpp) implement prompt caching with severe restrictions — only whole-prompt caching within the same session, providing little benefit for cross-session or cross-user reuse
- Sensitive data detection tools rely on AI classifiers and heuristics that cannot provide guaranteed coverage — attacker-crafted or novel PII formats may evade automated scanners
- Production observability for AI pipelines is significantly harder than traditional software — metric granularity, log volumes, and trace complexity are all substantially elevated, requiring dedicated tooling investment

## Bottlenecks

- Unresolved prompt injection vulnerability blocks broad autonomous deployment of write-action AI agents — organisations cannot safely give models write access to production systems without human approval gates that negate autonomy
- Guardrail latency overhead creates a forced tradeoff between safety coverage and response speed, blocking deployment of comprehensive guardrails in latency-sensitive real-time applications
- 'Lost in the middle' context position sensitivity constrains effective retrieval window size for RAG — retrieving more documents does not linearly improve answer quality because middle-context documents are systematically under-used
- Lack of standardised evaluation frameworks for AI platform components (retrieval quality, guardrail accuracy, cache hit rates, routing precision) blocks systematic optimisation — teams must build bespoke eval pipelines per application

## Breakthroughs

- Prompt caching — reusing computed KV states for shared prompt prefixes across API calls — entered production model APIs, enabling up to ~75% cost reduction and significant latency improvement for applications with long system prompts or repeated document context

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/agentic-workflow|Agentic Workflow]]
- [[entities/kv-cache|KV Cache]]
- [[entities/prompt-injection|Prompt Injection]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
