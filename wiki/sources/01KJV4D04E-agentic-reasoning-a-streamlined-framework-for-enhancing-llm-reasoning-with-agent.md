---
type: source
title: 'Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with
  Agentic Tools'
source_id: 01KJV4D04E2B7T3FE86HZTW793
source_type: paper
authors:
- Junde Wu
- Jiayuan Zhu
- Yuyuan Liu
- Min Xu
- Yueming Jin
published_at: '2025-02-07 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools

**Authors:** Junde Wu, Jiayuan Zhu, Yuyuan Liu, Min Xu, Yueming Jin
**Published:** 2025-02-07 00:00:00
**Type:** paper

## Analysis

# Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools
2025-02-07 · paper · Junde Wu, Jiayuan Zhu, Yuyuan Liu, Min Xu, Yueming Jin
https://arxiv.org/pdf/2502.04644

---

### Motivation & Prior Limitations
Current large reasoning models (DeepSeek-R1, o1, QwQ) excel in structured domains like math and code but fail on knowledge-intensive, open-ended tasks that require factual verification, complex logical relationships, and multi-step research across unstructured domains.
- Applying math- or coding-style formal reasoning to fields like social sciences, ethics, or law produces flawed or overly rigid results, because these domains rely on conventional wisdom, abstract concepts, and factual grounding rather than verifiable symbolic outcomes.
- Prior search-augmented and RAG-integrated reasoning approaches (RAgent, Search-O1) narrowly focus on single-agent retrieval enhancements and do not systematically explore optimal combinations of agentic tools, leaving a substantial performance gap versus proprietary systems like OpenAI Deep Research.
- Long reasoning chains with heavy tool usage degrade LLM coherence: models deviate from original queries, redundantly repeat tool calls, or revisit prior errors, with no structured mechanism to maintain context across extended multi-step reasoning.
- Existing open-source tool-augmented frameworks (AutoGPT, LangChain Agents) lack optimized task delegation and structured integration, reducing their effectiveness precisely where long-chain reasoning is needed most.

---

### Proposed Approach
Agentic Reasoning is a framework that enhances LLM reasoning by integrating three external LLM-based agents — a Web-Search agent, a Code agent, and a Mind-Map agent — as callable tools embedded directly into the reasoning chain via specialized tokens.
- The reasoning LLM dynamically decides when to invoke each agent by emitting categorized tokens (web-search, coding, or Mind-Map calling tokens) alongside a query; the reasoning process halts, dispatches the query plus current reasoning context to the relevant agent, receives results, and resumes — enabling iterative retrieval-and-reasoning cycles.
- The Mind-Map agent is the key architectural innovation: it transforms the running reasoning chain into a structured knowledge graph using entity extraction and semantic relationship identification (following GraphRAG), applies community clustering to group and summarize reasoning context, and supports RAG-style queries over the graph so the model can retrieve prior context on demand. This directly addresses coherence loss in long reasoning chains.
- The Web-Search agent improves over prior search-in-reasoning approaches through a four-stage pipeline: query breakdown (decomposing vague queries into specific search-optimized sub-queries using Mind-Map reasoning context), retrieval via Bing (top 20 pages), Cohere Rerank 3.5 re-ranking with iterative query refinement if average relevance of top-10 falls below 0.7, and RAG synthesis over high-relevance pages.
- The Code agent delegates quantitative and computational tasks to a specialized coding LLM (claude-3.5-sonnet), keeping the primary reasoning model free of coding disruptions; the coding LLM receives context from the Mind-Map and returns results in natural language for seamless reintegration.
- A key design finding is that tool quality dominates tool quantity: adding more tools (e.g., HuggingFace's 7-tool or LangChain's 109-tool defaults) degrades performance, because many capabilities are already embedded in the reasoning model and incorrect external outputs pollute the reasoning chain.

---

### Results & Capabilities
On Humanity's Last Exam, Agentic Reasoning with DeepSeek-R1 achieves 23.8% accuracy, a 14.4 percentage point improvement over the base DeepSeek-R1 (9.4%), placing it above Perplexity Deep Research (21.1%) and within 2.8% of the proprietary OpenAI Deep Research (26.6%), which uses a stronger internal reasoning model.
- On GPQA (PhD-level science QA), the framework achieves 81.2% overall with DeepSeek-R1, surpassing o3-mini-high (79.7%, the best prior proprietary model) and outperforming Search-O1 with DeepSeek-R1 (74.6%) by approximately 6.6 percentage points; gains are consistent across Physics (94.5%), Chemistry (73.7%), and Biology (80.5%).
- On GAIA (multi-ability agent benchmark combining reasoning, web browsing, and tool use), Agentic Reasoning achieves 66.13% average, surpassing OpenAI Deep Research on Level 1 (74.36% vs. 74.29%) and Level 2 (69.21% vs. 69.06%) tasks, narrowing the gap to 2.26% on Level 3.
- On the FreshWiki deep research benchmark, Agentic Reasoning achieves ROUGE-1 of 54.10, ROUGE-L of 19.62, and Entity Recall of 18.77, outperforming STORM (47.93 / 17.42 / 15.43) — a more complex multi-agent workflow — across all metrics.
- In human expert evaluation of deep research articles (56 questions from PhD-level finance, medicine, and law experts), Agentic Reasoning scores 3.7 on interest, 4.6 on organization, 4.2 on relevance, and 4.1 on coverage (1–5 scale), substantially outperforming Gemini Deep Research (2.7 / 2.5 / 2.3 / 3.0) on all dimensions.
- The Mind-Map agent proves critical for strategic deductive reasoning: in Werewolf (social deduction game) against seven experienced players, the model achieved a 72% win rate with Mind-Map versus 36% without, by tracking logical relationships between players' claims and anticipating deceptive behaviors.
- Ablation confirms synergistic effects: combining web search + Mind-Map + coding outperforms any single-tool or two-tool combination, and the three-tool configuration delivers greater gains than the sum of individual contributions.

---

### Implications
This work demonstrates a viable open-source path to near-parity with proprietary deep research systems (OpenAI Deep Research, Gemini Deep Research) by composing existing strong open models (DeepSeek-R1, DeepSeek-V3) with well-designed agentic scaffolding rath

## Key Claims

1. Agentic Reasoning narrows the performance gap between open-source and proprietary deep research models to 2.8% on Humanity's Last Exam.
2. Current LLM reasoning methods excel in structured domains like math and code but fail to generalize to knowledge-intensive or less structured tasks.
3. Applying math- or coding-style reasoning to fields like social sciences or ethics often produces flawed or overly rigid results.
4. Rule-based outcome rewards during training can yield reasoning capabilities equaling o1-level math and coding performance.
5. The Mind-Map agent constructs a knowledge graph from the reasoning chain to store and structure real-time reasoning context.
6. The Mind-Map agent uses community clustering on the knowledge graph and LLM-generated summaries to cluster and summarize reasoning context.
7. The Mind-Map agent enables the reasoning model to query its reasoning history as external memory to recover coherence in extended reasoning chains.
8. The Web-Search agent performs iterative query refinement: if the average relevance score of top-10 reranked pages falls below 0.7, it regenerates the search query up to three times.
9. Using 109 LangChain tools or Hugging Face's 7-tool default agent toolbox degrades GPQA performance compared to the curated 3-tool combination.
10. Agentic Reasoning with DeepSeek-R1 achieves 81.2% overall accuracy on GPQA, surpassing o3-mini-high (79.7%) and improving over DeepSeek-R1 base (71.5%) by nearly 10%.

## Capabilities

- Tool-augmented reasoning framework (web search + code execution + Mind-Map) achieves 23.8% on Humanity's Last Exam with DeepSeek-R1, a 14.4% improvement over the base model, and 81.2% on GPQA surpassing all prior public and proprietary methods including o3-mini-high
- Knowledge-graph-based Mind-Map agent constructs structured reasoning context in real time, maintaining coherence across long multi-tool reasoning chains and enabling correct resolution of logic-relationship traps that fool GPT, Gemini, and DeepSeek-R1 alone
- Multi-stage context-aware web search with query breakdown, reranking against Mind-Map reasoning context, and iterative refinement outperforms all prior RAG and search-in-reasoning approaches on GPQA, GAIA, and FreshWiki
- Open-source agentic reasoning system surpasses OpenAI Deep Research on GAIA Level 1 (74.36% vs 74.29%) and Level 2 (69.21% vs 69.06%), narrowing Level 3 gap to 2.26% — highest GAIA scores among all publicly available methods
- Structured knowledge-graph memory enables strategic social deduction reasoning — 72% win rate against experienced human Werewolf players (5+ years experience) versus 36% without Mind-Map, near-doubling performance

## Limitations

- Sequential invocation of multiple external agents significantly increases inference latency and computational cost, blocking real-time interactive use of agentic reasoning
- Agentic web search has no built-in source credibility verification — system is susceptible to misinformation and biased content injected via high-relevance-score but unreliable web pages
- Hallucinations in the reasoning LLM can derail entire multi-step agentic processes — compounding risk is especially dangerous in high-stakes domains (medical, legal) where minor inaccuracies cause significant consequences
- Accuracy systematically degrades as reasoning chain length and number of tool calls increase — harder questions inherently require more steps, creating an inverse correlation between task difficulty and task completion
- Even the best open-source agentic framework achieves only 23.8% on Humanity's Last Exam — over 76% of expert-level cross-domain questions remain unanswerable, revealing a deep ceiling on current AI knowledge integration
- RL-trained reasoning methods that excel in math and code fail on unstructured knowledge-intensive domains — social sciences, ethics, and moral reasoning — producing 'flawed or overly rigid results' when formal reasoning is imposed
- Adding more agentic tools beyond a minimal well-chosen set degrades reasoning performance — 7-tool (Hugging Face) and 109-tool (LangChain) configurations underperform the 3-tool setup due to inappropriate tool selection
- Code execution agent generates and runs arbitrary code (via Claude 3.5 Sonnet + Python 3.11) with no security analysis, sandboxing documentation, or injection risk assessment presented
- Web search agent injects arbitrary web page content into the LLM reasoning chain with no analysis of prompt injection vulnerabilities from adversarially crafted web pages
- System orchestrates at least 3 separate large LLMs per reasoning cycle (DeepSeek-R1 as reasoner, DeepSeek-V3 for search/RAG/Mind-Map, Claude 3.5 Sonnet for code) with no quantified per-query cost, token consumption, or latency figures
- Human evaluation of deep research quality uses only 56 questions from PhD experts in 3 domains (finance, medicine, law) — generalizability claims to 'diverse domains' are unsupported by the evaluation breadth

## Bottlenecks

- LLMs lose coherence in long agentic reasoning chains with many tool calls — deviating from queries, repeating identical tool calls, or revisiting prior errors — blocking reliable long-horizon multi-tool reasoning
- Sequential multi-agent invocation creates a latency wall for real-time agentic reasoning — each external tool call (web search, code execution, Mind-Map query) adds full round-trip latency to an already-long reasoning chain
- RL-based reasoning training has no effective reward signal for unverifiable knowledge domains (social sciences, ethics, moral reasoning), blocking extension of o1/R1-style reasoning to the majority of real-world knowledge-intensive tasks

## Breakthroughs

- Open-source agentic framework (DeepSeek-R1 + Agentic Reasoning) achieves within 2.8% of OpenAI Deep Research on Humanity's Last Exam (23.8% vs 26.6%) and surpasses it on GAIA Level 1 and Level 2 — closing the open-source/proprietary deep research gap through tool design rather than model scale
- Real-time knowledge graph construction from LLM reasoning chains (Mind-Map) approximately doubles agentic performance in strategic and long-chain tasks — from 36% to 72% in Werewolf game play, with consistent gains across GPQA and deep research benchmarks

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/gaia|GAIA]]
- [[entities/gpqa|GPQA]]
- [[entities/graphrag|GraphRAG]]
- [[entities/humanitys-last-exam|Humanity's Last Exam]]
- [[entities/qwq-32b|QwQ-32B]]
- [[entities/agentic-rag|agentic RAG]]
