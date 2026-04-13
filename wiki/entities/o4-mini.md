---
type: entity
title: o4-mini
entity_type: entity
theme_ids:
- agent_memory_systems
- agent_systems
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- continual_learning
- evaluation_and_benchmarks
- knowledge_and_memory
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
- test_time_compute_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0008291661177154636
staleness: 0.0
status: active
tags: []
---
# o4-mini

OpenAI's o4-mini is a reasoning-optimized language model that has emerged as a key reference point across multiple research frontiers in 2025, particularly in abstract reasoning, agentic code generation, and mathematical problem-solving. Its position on the cost-performance Pareto frontier — ranking second only to Grok 4 on ARC-AGI-1 while remaining substantially cheaper than o3 — makes it the default workhorse model in studies where inference budget matters.

**Type:** entity
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]]

---

## Overview

o4-mini is OpenAI's compact reasoning model, positioned as the cost-efficient counterpart to o3. It is trained with reinforcement learning to produce extended chain-of-thought reasoning traces and, notably, integrates visual reasoning directly into its thinking process — manipulating images dynamically mid-reasoning in ways its predecessors could not. By mid-2025 it had become the de facto benchmark model across a range of research papers studying memory augmentation, agentic CUDA kernel optimization, and abstract reasoning, precisely because it sits at the frontier of what is achievable without incurring the compute cost of o3.

---

## Key Findings

### Abstract Reasoning and Memory Augmentation

The ArcMemo paper uses o4-mini as its primary problem-solving model and reveals a fundamental limitation of all current reasoning models: inference-time insights are discarded the moment the context window resets. The patterns uncovered during a long reasoning trace simply do not carry forward to the next query. ArcMemo addresses this by maintaining a persistent external memory of abstract concepts in a parameterized, typed, higher-order-function-capable format (the PS format), and the results are striking. With two retries, ArcMemo-PS achieves an Oracle@2 score of 70.83 on ARC-AGI-1 against a no-memory baseline of 55.17. Without the oracle, the official score improves from 55.17 to 59.33 — a 7.5% relative gain. Crucially, the abstract concept-level memory formulation is the only design that consistently outperforms the no-memory baseline at *all* tested inference compute scales, suggesting that the abstraction level of stored knowledge, not just its presence, is what drives robustness across compute budgets.

### Agentic CUDA Kernel Optimization

In Towards Robust Agentic CUDA Kernel, o4-mini serves as the base LLM for an evolutionary optimization pipeline targeting GPU kernel performance — configured with temperature 1.0, high reasoning effort, and 16,384 max tokens. The results challenge the assumption that larger or slower models are necessary for low-level systems work. The evolutionary approach built around o4-mini achieves 3.40x speedup on MNIST ConvReluPool forward pass, against 1.91x, 2.17x, and 2.20x for Kevin-32B, Qwen3-32B, and Claude-3-7-Sonnet best-of-40 respectively. On MNIST Linear ReLU forward pass, the advantage is even more pronounced: 2.65x versus 0.34x (Kevin-32B), 0.72x (Qwen3-32B), and 0.39x (Claude-3-7-Sonnet). Correctness is evaluated by passing all tests across input sizes, initialization settings, and random seeds with floating point tolerance of 1e-5, and runtimes are measured over 2,000 runs on H100 GPUs after 25 warmup runs — a rigorous setup that makes the performance gaps credible. The pipeline also supports Claude-3-7-Sonnet, Gemini-2.5-Pro, GPT-4.1, and o3 as drop-in alternatives, positioning o4-mini as one option within a broader multi-LLM optimization framework rather than an irreplaceable component.

### Mathematical Reasoning

On AIME 2025 with Python interpreter access, o4-mini achieves 99.5% pass@1 (100% consensus@8), ranking as the best-performing benchmarked model on both AIME 2024 and 2025. The RLAD paper provides relevant context here: it demonstrates that training a separate abstraction generator alongside a solution generator via two-player RL achieves an average 44% improvement over DAPO on AIME 2025, suggesting that o4-mini's strong AIME performance may itself partly reflect training dynamics that reward abstraction discovery — a hypothesis worth tracking as more is revealed about its post-training recipe.

---

## Capabilities

- **Multimodal chain-of-thought reasoning**: o4-mini integrates images directly into its thinking process, including dynamic manipulation (rotating, zooming, transforming), a qualitative departure from earlier reasoning models that treat vision as a separate preprocessing step. (maturity: narrow_production)
- **AIME 2025 mathematical reasoning**: 99.5% pass@1 with Python access — best-performing benchmarked model on both AIME 2024 and 2025. (maturity: narrow_production)
- **Complex web research**: Web browsing agent achieving 26.4% on BrowseComp (o4-mini-high: 28.3%, Claude-4-Opus: 18.8%), demonstrating multi-step research capability on questions requiring precise short answers. (maturity: narrow_production)
- **Cost-performance frontier**: o4-mini strictly outperforms o3-mini while costing less, maintaining a Pareto-improving cost-performance relationship relative to its predecessor. (maturity: broad_production)
- **Terminal coding agent**: Codex CLI combines o4-mini reasoning with local codebase access and multimodal inputs including screenshots and low-fidelity sketches. (maturity: demo)

---

## Known Limitations

o4-mini's limitations are less about capability ceiling and more about evaluation context and throughput:

**Evaluation comparability.** SWE-bench evaluations of o4-mini use 256k context length and exclude 23 non-runnable samples, improving solve rate by approximately 3% relative to standard-context evaluations. This makes direct comparison with prior results difficult and suggests published SWE-bench numbers may be optimistic relative to realistic deployment conditions.

**Throughput unchanged.** Despite the capability step-change from o3-mini, rate limits for o4-mini remain identical to predecessor models. High-volume research or production pipelines face the same throughput ceiling regardless of which reasoning model they use — a constraint that becomes load-bearing when running large benchmark evaluations or agentic pipelines with many parallel rollouts.

**Context window amnesia.** The ArcMemo finding is perhaps the most structurally important limitation: all reasoning models, o4-mini included, discard everything learned during inference once the context window resets. This is not a failure of reasoning quality but a fundamental architectural property. Memory augmentation systems like ArcMemo partially address it, but they introduce their own failure modes (memory retrieval noise, abstraction mismatch) and do not close the gap entirely.

---

## Relationships

o4-mini is positioned in direct comparison with **o3** (its expensive counterpart), **o3-mini** (its predecessor), **Claude-3-7-Sonnet**, **Gemini-2.5-Pro**, **GPT-4.1**, **Kevin-32B**, and **Qwen3-32B** across the papers surveyed. The [[themes/test_time_compute_scaling|test-time compute scaling]] theme is central: much of what makes o4-mini interesting is how it trades off cost against reasoning depth at inference time, a dynamic that is directly manipulated in ArcMemo's inference compute scaling experiments. Its connection to [[themes/agent_memory_systems|agent memory systems]] is newly foregrounded by ArcMemo — the paper is fundamentally about what o4-mini *cannot* do natively (retain cross-query learning) and how external memory patches that gap. The CUDA kernel work connects it to [[themes/software_engineering_agents|software engineering agents]] in a domain — low-level GPU programming — where LLM-based agents were not previously competitive. The RLAD connection to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] is more speculative but suggestive: if abstraction discovery during RL training is what drives strong mathematical reasoning, o4-mini's training methodology may be closer to RLAD's two-player paradigm than its public description indicates.

## Limitations and Open Questions

## Sources
