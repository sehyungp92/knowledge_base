---
type: source
title: 'Agentic Context Engineering: Evolving Contexts for Self-Improving Language
  Models'
source_id: 01KJTEBGCX5K0JDYWCFW466EAP
source_type: paper
authors:
- Qizheng Zhang
- Changran Hu
- Shubhangi Upasani
- Boyuan Ma
- Fenglu Hong
- Vamsidhar Kamanuru
- Jay Rainton
- Chen Wu
- Mengmeng Ji
- Hanchen Li
- Urmish Thakker
- James Zou
- Kunle Olukotun
published_at: '2025-10-06 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- knowledge_and_memory
- post_training_methods
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

**Authors:** Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun
**Published:** 2025-10-06 00:00:00
**Type:** paper

## Analysis

# Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
2025-10-06 · paper · Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong et al. (13 total)
https://arxiv.org/pdf/2510.04618

---

### Motivation & Prior Limitations
- Existing context adaptation methods suffer from **brevity bias**, a tendency to compress domain-specific knowledge into short, generic prompts that omit the heuristics, failure modes, and tool-use guidelines that agents and knowledge-intensive tasks actually require.
  - GEPA explicitly promotes brevity as a design goal; Gao et al. document that iterative prompt optimizers repeatedly converge to near-identical generic instructions (e.g., "Create unit tests to ensure methods behave as expected"), losing diversity and propagating recurring errors.
- A second failure mode, **context collapse**, occurs when an LLM is tasked with monolithically rewriting an accumulated context at each adaptation step: as context grows, the model compresses it into a shorter, less informative summary, abruptly erasing accumulated knowledge.
  - On AppWorld, a context of 18,282 tokens with 66.7% accuracy collapsed to 122 tokens at the next step, dropping accuracy to 57.1% — below the no-adaptation baseline of 63.7%.
- Prior methods treat contexts as static summaries or single optimized prompts rather than as evolving, cumulative knowledge stores, making them poorly suited to long-horizon agent tasks and domain-intensive reasoning where performance depends on retaining, not compressing, task-specific detail.
  - ICL fills a fixed context window with demonstrations; GEPA refines a monolithic prompt; Dynamic Cheatsheet accumulates memory but uses end-to-end rewriting that is vulnerable to collapse.

---

### Proposed Approach
- ACE (Agentic Context Engineering) treats contexts as **evolving playbooks** — structured, itemized collections of strategies, domain concepts, and failure modes — that grow and refine incrementally rather than being rewritten wholesale.
  - Builds on the agentic architecture of Dynamic Cheatsheet but adds a dedicated Reflector role and replaces monolithic rewrites with incremental delta updates, separating the responsibilities of trajectory generation, insight extraction, and context curation into three specialized components.
- The framework divides labor across three roles: the **Generator** produces reasoning trajectories for new queries; the **Reflector** critiques those trajectories to extract concrete lessons (optionally across multiple refinement rounds); the **Curator** synthesizes lessons into compact delta entries that are merged deterministically by lightweight non-LLM logic.
  - Because merging is non-LLM-based and itemized, multiple deltas can be merged in parallel, enabling batched adaptation; this is the primary source of ACE's dramatic latency and cost reduction relative to methods that require LLM-driven rewrites.
- Each context bullet carries metadata (unique identifier, helpful/harmful counters) and a small unit of content (reusable strategy, domain concept, or failure mode), enabling **localized updates**: only relevant bullets are modified, not the entire context.
- The **grow-and-refine** mechanism appends new bullets while updating existing ones in-place and periodically de-duplicates via semantic embeddings, controlling redundancy without sacrificing accumulated knowledge; refinement can be proactive (after each delta) or lazy (only when the context window is exceeded).
- ACE operates in both **offline** settings (system prompt optimization over a training split before deployment) and **online/test-time** settings (sequential context updates during inference), and can function without ground-truth labels by leveraging natural execution feedback such as code execution success or failure.

---

### Results & Capabilities
- ACE outperforms all evaluated baselines on agent tasks, achieving an average gain of **+10.6%** on the AppWorld benchmark and **+8.6%** on financial analysis benchmarks (FiNER and Formula) across offline and online settings.
  - On AppWorld offline adaptation: ReAct + ACE reaches 59.4% average accuracy versus 46.4% for ReAct + GEPA and 46.0% for ReAct + ICL, a margin of ~13 percentage points over the next-best method.
- On the AppWorld public leaderboard (as of September 20, 2025), ReAct + ACE (59.4% average) matches IBM CUGA (60.3%), a production-level GPT-4.1-based agent, while using the smaller open-source model DeepSeek-V3.1; in the online adaptation setting, ACE surpasses IBM CUGA on the harder test-challenge split by 8.4% TGC and 0.7% SGC.
- ACE achieves strong performance **without labeled supervision** by relying solely on execution feedback: in the no-label offline setting on AppWorld, ReAct + ACE still improves 14.8% over the ReAct baseline, demonstrating self-improvement without ground-truth annotation.
- ACE reduces adaptation overhead dramatically relative to prior methods: **86.9% lower adaptation latency on average**, with specific figures of 82.3% latency reduction and 75.1% fewer rollouts versus GEPA (offline AppWorld), and 91.5% latency reduction and 83.6% token cost reduction versus Dynamic Cheatsheet (online FiNER).
- Ablation studies confirm that the Reflector and multi-epoch adaptation each contribute independently: removing both reduces AppWorld average accuracy from 59.4% to 55.1%; removing only multi-epoch reduces it to 56.8%, isolating the value of iterative reflection and repeated passes over training data.
- On Formula (financial numerical reasoning), ACE in the offline+labeled setting achieves 85.5% accuracy versus the base LLM's 67.5% — an 18-point absolute gain — demonstrating that evolving playbooks are particularly effective for tasks requiring precise, structured domain knowledge (e.g., XBRL rules and financial computation patterns).

---

### Implications
- ACE shifts the locus of LLM adaptation from weight updates to **context engineering**, offering 

## Key Claims

1. Existing context adaptation methods suffer from brevity bias, where iterative optimization collapses toward short, generic prompts that omit domain-specific heuristics and tactics.
2. Context collapse occurs when an LLM is tasked with fully rewriting accumulated context, causing it to compress large, detailed contexts into much shorter, less informative summaries with sharp perform
3. Context collapse is a fundamental risk of end-to-end context rewriting with LLMs, not specific to any single method like Dynamic Cheatsheet.
4. LLMs are more effective when provided with long, detailed contexts and can distill relevance autonomously, unlike humans who benefit from concise generalization.
5. ACE outperforms strong baselines by an average of 10.6% on agent benchmarks and 8.6% on domain-specific benchmarks.
6. ACE can construct effective contexts without labeled supervision by leveraging natural execution feedback such as code execution success or failure.
7. ReAct + ACE on the AppWorld leaderboard matches the top-ranked production-level agent IBM CUGA (GPT-4.1) on average and surpasses it on the harder test-challenge split, despite using the smaller open-
8. ACE achieves 86.9% lower adaptation latency on average compared to existing adaptive methods.
9. ACE uses a three-role modular architecture: a Generator that produces reasoning trajectories, a Reflector that extracts insights from successes and errors, and a Curator that integrates insights into 
10. ACE uses incremental delta updates—small sets of candidate bullets—rather than full context rewrites, enabling localized edits that preserve past knowledge while adding new insights.

## Capabilities

- Agentic context engineering (ACE) enables smaller open-source LLMs to self-improve through structured context accumulation, matching production-level proprietary agents — DeepSeek-V3.1 + ACE matches GPT-4.1-based IBM CUGA on AppWorld with +17.1% over base
- Incremental delta context updates (non-LLM merge logic applied to itemized bullet entries) achieve 82–92% reduction in adaptation latency and token cost compared to monolithic context rewriting, while maintaining or exceeding performance gains
- LLM agents can construct effective context playbooks without labeled supervision by leveraging natural execution feedback (code success/failure, formula correctness), achieving +14.8% over base on complex agent tasks
- Structured context playbooks accumulating domain-specific XBRL strategies and heuristics across episodes improve financial analysis accuracy by +8.6–12.8% over strong prompt-optimization baselines (MIPROv2, GEPA)

## Limitations

- Context adaptation methods including ACE degrade below baseline when reliable execution signals or ground-truth labels are absent — context is actively polluted by spurious feedback (ACE online FiNER without GT: −3.4%; DC online without GT: −3.7%), meaning the technique is harmful in low-verifiabili
- LLMs have a fundamental architectural tendency toward brevity bias — iterative context optimization systematically converges toward short, generic instructions, dropping domain-specific heuristics, tool-use guidelines, and common failure modes that are critical for complex tasks
- Context collapse is a fundamental failure mode of end-to-end context rewriting by LLMs — an LLM instructed to fully rewrite an 18K-token accumulated context can collapse it to 122 tokens in a single step, dropping performance below the no-adaptation baseline (57.1 vs 63.7)
- ACE's effectiveness is demonstrated only on tasks with structured, verifiable feedback (API-based agent tasks, formula correctness) — applicability to open-ended analytical, creative, or subjective tasks with ambiguous feedback is entirely unevaluated
- Growing context playbooks add inference prefill cost and KV cache pressure; the paper treats this as an open engineering challenge requiring ongoing infrastructure investment rather than a solved problem
- Cross-task generalization of accumulated context playbooks is entirely absent from evaluation — whether domain-specific playbooks transfer across heterogeneous task types within a single deployment is not studied, suggesting task-domain specificity

## Bottlenecks

- Brevity bias in LLM-driven context optimization creates a systematic convergence failure — iterative methods compress away domain-specific knowledge toward generic instructions, blocking reliable adaptation in knowledge-intensive and multi-step agent tasks
- Absence of reliable execution feedback blocks inference-time context adaptation from operating in open-ended or subjective domains — without verifiable signals, self-improving context mechanisms degrade below baseline through spurious update accumulation

## Breakthroughs

- Accumulative context engineering — treating LLM contexts as growing playbooks rather than compressed summaries — consistently outperforms compression-based prompt optimization and enables a smaller open-source model to match a production-level proprietary agent purely through context design

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/appworld|AppWorld]]
- [[entities/dynamic-cheatsheet|Dynamic Cheatsheet]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/textgrad|TextGrad]]
