---
type: source
title: Deep Researcher with Test-Time Diffusion
source_id: 01KJTNBKSKJ6ZDQDWY9WHGNQTP
source_type: paper
authors:
- Rujun Han
- Yanfei Chen
- Zoey CuiZhu
- Lesly Miculicich
- Guan Sun
- Yuanjun Bi
- Weiming Wen
- Hui Wan
- Chunfeng Wen
- Solène Maître
- George Lee
- Vishy Tirumalashetty
- Emily Xue
- Zizhao Zhang
- Salem Haykal
- Burak Gokturk
- Tomas Pfister
- Chen-Yu Lee
published_at: '2025-07-21 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Deep Researcher with Test-Time Diffusion

**Authors:** Rujun Han, Yanfei Chen, Zoey CuiZhu, Lesly Miculicich, Guan Sun, Yuanjun Bi, Weiming Wen, Hui Wan, Chunfeng Wen, Solène Maître, George Lee, Vishy Tirumalashetty, Emily Xue, Zizhao Zhang, Salem Haykal, Burak Gokturk, Tomas Pfister, Chen-Yu Lee
**Published:** 2025-07-21 00:00:00
**Type:** paper

## Analysis

# Deep Researcher with Test-Time Diffusion
2025-07-21 00:00:00 · paper · Rujun Han, Yanfei Chen, Zoey CuiZhu, Lesly Miculicich, Guan Sun et al. (18 total)
https://arxiv.org/pdf/2507.16075

---

### Motivation & Prior Limitations
Performance of deep research agents using generic test-time scaling algorithms (CoT, best-of-n, MCTS, debate, self-refinement) plateaus when generating complex, long-form research reports, because these algorithms are assembled without deliberate design grounded in human cognitive writing behavior.
- Existing open-source DR agents (Huggingface Open DR, GPT Researcher, Open Deep Research) use linear or parallelized plan→search→generate pipelines that lose global context, miss critical cross-section dependencies, and accumulate information loss over long agentic trajectories.
  - GPT Researcher runs search queries in parallel before synthesis, losing coherence across sections; Open Deep Research researches each section independently, severing global dependencies.
- Current state-of-the-art LLMs cannot fully address search- and reasoning-intensive queries using internal knowledge or conventional single-step search tools, motivating a multi-iteration retrieval-augmented agent architecture.
- No principled draft-and-feedback mechanism analogous to how human researchers actually write — establishing a plan, producing a draft, iteratively seeking literature, revising — existed in prior open DR agent work.

---

### Proposed Approach
TTD-DR (Test-Time Diffusion Deep Researcher) reframes research report generation as a diffusion process: an initial noisy draft is iteratively "denoised" toward a high-quality final report through retrieval-augmented revision cycles, directly mirroring the human writing loop of plan → draft → search → revise.
- The analogy to diffusion models is precise: the LLM generates a preliminary draft from internal knowledge (the "noisy sample"), and each denoising step incorporates externally retrieved information to refine it, paralleling retrieval-augmented diffusion sampling.
  - Unlike Open Deep Research, TTD-DR avoids siloed per-section searches; the evolving draft plus a global research plan jointly direct all downstream retrieval, preserving cross-section coherence.
- The backbone agent has three stages: (1) Research Plan Generation produces a structured scaffold; (2) Iterative Search and Synthesis loops — Stage 2a generates targeted search questions conditioned on the plan and prior Q&A history, Stage 2b retrieves documents and produces a synthesized RAG answer rather than storing raw documents; (3) Final Report Generation synthesizes the plan and all Q&A pairs into the report.
- A Component-wise Self-Evolution algorithm is applied independently to each stage agent: multiple output variants are sampled with varied parameters (temperature, top_k), each variant receives LLM-as-judge fitness scores and textual critiques, undergoes iterative revision, and all evolved variants are merged via a crossover step — providing higher-quality context at every stage of the diffusion process.
  - Self-evolution addresses information loss within individual unit agents during long agentic trajectories, not just at the report level.

---

### Results & Capabilities
TTD-DR achieves state-of-the-art results across a wide array of benchmarks requiring intensive multi-hop search and reasoning, significantly outperforming existing open-source and comparable proprietary deep research agents.
- The system handles diverse industry domains — finance, biomedical, recreation, and technology — targeting the same query class as commercial products (OpenAI Deep Research, Perplexity, Grok) but using only standard search tools accessible to most agentic systems.
- Comprehensive evaluation used both long-form report quality metrics (assessed by expert evaluators) and concise-answer multi-hop reasoning benchmarks, with the framework outperforming on both task types simultaneously.
- Ablation studies confirm that both the draft-centric denoising mechanism and the self-evolutionary component-wise optimization contribute independently to the performance gains, and their synergistic combination produces the best outcomes.

---

### Implications
Conceptualizing test-time compute for agentic systems as a diffusion process over a mutable draft — rather than as search tree expansion or repeated sampling — provides a new design axis for long-horizon research agents that natively models coherence and revision.
- The draft as a persistent, updatable state object that guides retrieval at each step is a meaningful architectural departure from both linear pipelines and parallel section-level agents; this pattern could generalize to any long-document generation task requiring iterative grounding.
- Applying self-evolutionary optimization at the component level (plan, question, answer, report) rather than only at the output level suggests that information quality throughout the agentic trajectory — not just final generation — is a critical bottleneck for scaling deep research agents.
- The framing bridges test-time compute (scaling inference), RAG (retrieval-augmented generation), and agentic self-refinement into a single coherent framework, potentially unifying previously disconnected research threads in the autonomous agents and reasoning-and-planning domains.
- Demonstrating competitive performance using only widely available search tools (no proprietary multimodal or browser tools) lowers the barrier for deploying capable research agents and benchmarks proprietary systems on accessible infrastructure.

---

### Remaining Limitations & Next Steps
The paper restricts evaluation to search-tool-only setups, explicitly excluding multimodal and web-browsing tools that proprietary agents like OpenAI Deep Research use, which may underestimate the performance ceiling of the TTD-DR architecture when richer tools are available.
- This design choice is framed as a strength (broader accessibility) but 

## Key Claims

1. Deep research agents powered by LLMs often plateau in performance when generating complex, long-form research reports using generic test-time scaling algorithms.
2. Human writers of complex topics do not follow a linear progression but instead establish a high-level plan, draft, and then engage in multiple revision cycles.
3. During revision, human writers seek out literature or search tools to gather supplementary information that refines and strengthens their arguments.
4. Existing deep research agents primarily leverage test-time scaling approaches such as Chain-of-Thought, best-of-n sampling, Monte Carlo Tree Search, debate mechanisms, and self-refinement loops.
5. There is a striking resemblance between human iterative writing and the sampling process in a diffusion model augmented by retrieval.
6. Vanilla diffusion sampling can be ineffective for generating high quality outputs for complex research tasks.
7. TTD-DR achieves state-of-the-art results on benchmarks requiring intensive search and multi-hop reasoning, significantly outperforming existing deep research agents.
8. A draft-centric design makes the report writing process more timely and coherent while reducing information loss during the iterative search process.
9. Linear or parallelized planning-search-generation pipelines in DR agents can lead to loss of global context and miss critical dependencies during the research process.
10. Open Deep Research conducts separated searches for each section individually before combining them, which loses global context.

## Capabilities

- Test-time diffusion deep research (TTD-DR) achieves state-of-the-art on benchmarks requiring intensive multi-hop search and reasoning by framing report generation as an iterative draft-denoising process augmented with retrieval at each step
- Self-evolutionary algorithm applied to each component of an agentic research workflow — plan generation, search question generation, answer synthesis, report generation — using fitness scoring, textual critique, iterative revision, and multi-variant crossover to improve output quality at each stage
- RAG-based answer synthesis within deep research pipelines — retrieved documents are summarised into precise answers rather than stored as raw chunks — reducing context noise and information loss across long agentic research trajectories
- LLM-as-judge auto-raters can provide both fitness scores and actionable textual critiques on agentic workflow outputs (helpfulness, comprehensiveness), enabling targeted iterative self-improvement within a single agentic pipeline without human feedback

## Limitations

- Generic test-time scaling algorithms (CoT, best-of-N, MCTS, debate, self-refinement) plateau in performance when applied to complex long-form research report generation without task-specific architectural design grounded in human cognitive research behaviour
- Existing public deep research agents use linear or parallelised search-then-generate pipelines that lose global context and miss critical cross-section dependencies, limiting coherence in the final report
- Per-section isolated search (as used by Open Deep Research) prevents cross-section coherence and misses multi-hop dependencies that span multiple sections of a research report
- Long agentic research trajectories suffer from cumulative information loss at each stage — critical context from early search steps fails to propagate to final report generation as agents process sequential question-answer chains without a persistent evolving representation
- Proprietary deep research systems (OpenAI, Perplexity, Grok) are black boxes, preventing the research community from studying, reproducing, or systematically improving upon their methods
- Current state-of-the-art LLMs cannot fully address search-and-reasoning-intensive queries using only internal parametric knowledge or conventional single-hop search tools; multi-hop external retrieval with synthesis is required
- Most public deep research agents are designed without grounding in human cognitive research behaviour — they compose existing tools ad hoc rather than implementing principled plan-draft-search-revise cycles, producing structurally incoherent results
- Vanilla diffusion sampling without retrieval augmentation and component-wise self-evolution is insufficient for high-quality research outputs on complex tasks — the naive application of the diffusion analogy fails without both mechanisms working in synergy
- TTD-DR's self-evolutionary algorithm multiplies inference compute substantially by requiring multiple LLM calls per component (N variants × M revision iterations × K stages), creating significant cost barriers for production deployment at scale
- TTD-DR deliberately excludes multimodal and web browsing capabilities, meaning it cannot process figures, tables, images, or interactive web content found in real research papers and documents — limiting its real-world research utility

## Bottlenecks

- Deep research agents lack a principled iterative refinement mechanism analogous to human plan-draft-revise cycles; generic test-time scaling algorithms plateau without task-specific architectures that maintain global coherence across multi-hop search and synthesis
- Information loss across long agentic research trajectories — critical context from early search steps fails to propagate through sequential pipelines to final synthesis stages, degrading output quality in proportion to trajectory length
- Absence of rigorous evaluation methodology for deep research agents — existing benchmarks and metrics are insufficient to assess long-form research quality, multi-hop reasoning, and information synthesis quality across diverse industry domains

## Breakthroughs

- TTD-DR establishes that research report generation can be formally modelled as an iterative denoising diffusion process — with an evolving draft as the persistent latent representation, retrieval-augmented denoising as the refinement signal, and component-wise self-evolution optimising each workflow

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/test-time-scaling|Test-time Scaling]]
