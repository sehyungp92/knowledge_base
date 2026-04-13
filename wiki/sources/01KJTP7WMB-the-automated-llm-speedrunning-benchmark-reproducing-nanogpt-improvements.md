---
type: source
title: 'The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements'
source_id: 01KJTP7WMBW5WAB4NJAB1ESNTJ
source_type: paper
authors:
- Bingchen Zhao
- Despoina Magka
- Minqi Jiang
- Xian Li
- Roberta Raileanu
- Tatiana Shavrina
- Jean-Christophe Gagnon-Audet
- Kelvin Niu
- Shagun Sodhani
- Michael Shvartsman
- Andrei Lupu
- Alisia Lupidi
- Edan Toledo
- Karen Hambardzumyan
- Martin Josifoski
- Thomas Foster
- Lucia Cipolina-Kun
- Abhishek Charnalia
- Derek Dunfield
- Alexander H. Miller
- Oisin Mac Aodha
- Jakob Foerster
- Yoram Bachrach
published_at: '2025-06-27 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- ai_for_scientific_discovery
- benchmark_design
- evaluation_and_benchmarks
- scientific_and_medical_ai
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements

**Authors:** Bingchen Zhao, Despoina Magka, Minqi Jiang, Xian Li, Roberta Raileanu, Tatiana Shavrina, Jean-Christophe Gagnon-Audet, Kelvin Niu, Shagun Sodhani, Michael Shvartsman, Andrei Lupu, Alisia Lupidi, Edan Toledo, Karen Hambardzumyan, Martin Josifoski, Thomas Foster, Lucia Cipolina-Kun, Abhishek Charnalia, Derek Dunfield, Alexander H. Miller, Oisin Mac Aodha, Jakob Foerster, Yoram Bachrach
**Published:** 2025-06-27 00:00:00
**Type:** paper

## Analysis

# The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements
2025-06-27 · paper · Bingchen Zhao, Despoina Magka, Minqi Jiang, Xian Li, Roberta Raileanu et al. (23 total)
https://arxiv.org/pdf/2506.22419

---

### Motivation & Prior Limitations
- Automated scientific reproducibility — the ability of an AI agent to reimplement an experiment from a description such that it reproduces previously reported outcomes — is a necessary precondition for autonomous AI research agents, yet no benchmark existed that evaluated this capability across a cumulative chain of research innovations in a single domain with a unified success metric.
  - Prior reproducibility benchmarks such as PaperBench, CORE-Bench, Papers2Code, and SciReplicate evaluate agents on wide sets of unrelated papers, making cross-task comparison difficult and precluding evaluation of whether an agent can track compounding innovations over time.
  - No prior ML reproducibility benchmark simultaneously satisfied all four properties: requiring actual reproducibility (not just optimization), covering a sequential chain of results, focusing on LLM research specifically, and providing a baseline agent scaffold — the Automated LLM Speedrunning Benchmark is the first to meet all four criteria.
- Early LLM-based research agents, while capable of some code-level optimization, frequently fail to execute experiments that faithfully reflect their intended goals, meaning that the gap between hypothesis generation and reliable implementation remains a critical bottleneck.

---

### Proposed Approach
- The paper introduces the Automated LLM Speedrunning Benchmark, which tasks AI research agents with reproducing each of 19 successive wall-time records from the NanoGPT Speedrun — a community competition to train GPT-2 to a target cross-entropy loss of 3.28 on FineWeb in the shortest time on a single 8×H100 node.
  - Each task gives the agent the previous record's training script (train_gpt2.py) and optionally one or more hint formats: Level 1 (pseudocode), Level 2 (natural-language text description), or Level 3 (mini-paper); hints were drafted by DeepSeek-R1, manually verified, and corrected where needed.
  - Performance is measured by the Fraction of Speedup Recovered (FSR), defined as (t_i − t'_{i+1}) / (t_i − t_{i+1}), where t'_{i+1} is the agent's achieved training time; this gives a normalized, cross-task-comparable metric grounded in real hardware execution on a fixed cluster.
  - The benchmark improvements span a diverse range of code-level changes, from high-level algorithmic advances (e.g., the Muon optimizer, later validated at larger scale) to hardware-aware optimizations (e.g., FlexAttention, mixed precision), making the task realistic for the frontier problem of LLM training improvement.
- The authors also release a flexible search scaffold that extends AIDE into a general tree-search parameterization, with variants including Flat (best-of-M), Tree, Forest, AIDE, and Multi-AIDE, all receiving a fixed budget of M=20 search steps; each step involves code implementation via Aider (diff-based edits), execution on 8xH100, and LLM-generated analysis of results.

---

### Results & Capabilities
- Even the best-performing agents struggle severely: o3-mini with Multi-AIDE and all three hint levels combined achieves a mean FSR of only ~0.46, meaning it recovers less than half the speedup attained by the corresponding human solutions, and all agents fail to recover more than 20% of speedup on average when given no hints.
  - o3-mini generally achieves equal or better FSR than other models; pseudocode (Level 1) is the single most useful hint format, enabling ~40% FSR for o3-mini; combining all three hint levels with Multi-AIDE raises this to ~46%.
  - Flat search (best-of-M) generally matches or outperforms iterative search scaffolds for individual hint levels, and explicit debug steps (AIDE vs. Tree/Forest) do not provide significant additional benefit, suggesting that iterative improvement without dedicated debugging is sufficient at current capability levels.
- DeepSeek-R1 exhibits a surprising failure mode: its FSR actually worsens when individual hints are provided compared to the no-hint baseline, because attempting to implement complex hint-described changes results in buggy code; combining all three hint levels does recover some performance for R1 (up to ~0.41 with Multi-AIDE+Forest).
  - R1 produces more buggy nodes under AIDE and Multi-AIDE than o3-mini, suggesting weaker self-debugging; Gemini-2.5-Pro produces fewer buggy nodes than all other models yet lags on FSR, indicating it produces more conservative, robust but insufficiently performant code.
  - Claude-3.7-Sonnet generates an increasing fraction of buggy nodes as search progresses, gradually overtaking the fraction of working nodes; its mean FSR is comparable to o3-mini in some configurations but its IQM is substantially lower, revealing that its improvements are high-variance with many failures.
- Adding FlexAttention documentation (a module potentially outside training cut-off) as an additional hint for Record 12 actually degrades FSR for both R1 (0.09→0.07) and o3-mini (0.10→0.06), indicating that current models struggle to exploit in-context external knowledge not present in their training corpus when applied to complex implementation tasks.
- In the cumulative experiment — where agents build each record on their own prior solution rather than the ground-truth script — o3-mini with Multi-AIDE and all hints recovers ~60% of the speedup for Record 2 but drops to ~20% for Record 3 and essentially 0% for Record 4, showing rapid error compounding when starting from imperfect prior solutions.
- Code embedding similarity (using SFR-Embedding-Code 2B) correlates modestly with FSR, with stronger correlations emerging at richer hint levels (R²=0.17–0.27 for Level 3 and Level 1+2+3 for some models), and an LLM-judge (R1) scoring reproduced code changes shows clear positiv

## Key Claims

1. Recent reasoning LLMs combined with state-of-the-art scaffolds struggle to reimplement already-known scientific innovations even when given detailed hints.
2. All tested AI agents fail to recover more than 20% of the speedup achieved by human solutions when given no hints.
3. The NanoGPT Speedrun community effort reduced GPT-2 training time from 45 minutes to below 3 minutes between June 2024 and May 2025.
4. o3-mini generally achieves equal or better Fraction of Speedup Recovered than other models for all hint levels.
5. Flat search (best-of-M) generally matches or outperforms iterated search scaffolds across individual hint levels.
6. Pseudocode hints are the most effective individual hint format, enabling o3-mini to recover approximately 40% of the human speedup.
7. DeepSeek-R1 agents perform worse with individual hints than without them, producing buggy code when trying to implement complex described changes.
8. Combining multiple hints (pseudocode + text) substantially degrades performance for o3-mini but benefits DeepSeek-R1.
9. Gemini-2.5-Pro and Claude-3.7-Sonnet achieve the lowest IQM performance among tested models, lagging behind even the open-weights DeepSeek-R1.
10. Claude-3.7-Sonnet generates significantly more buggy nodes than other models, with buggy node fraction gradually overtaking working nodes in the search tree.

## Capabilities

- AI research agents (o3-mini + multi-AIDE scaffold) with all hint levels can recover approximately 46% of NanoGPT speedrun wall-time improvements — the best demonstrated performance on scientific reproduction of LLM training optimisations
- Muon optimizer, invented during the NanoGPT community speedrun, generalises beyond GPT-2 scale and demonstrates training efficiency benefits for much larger modern LLMs
- Community-driven algorithmic optimisations (Muon optimizer, mixed precision, FlexAttention variants) reduced GPT-2 training time from 45 minutes to under 3 minutes on a single 8xH100 node — a 15x improvement in training wall time
- Multi-AIDE iterative tree-search scaffold outperforms flat best-of-M sampling for scientific code reproduction tasks, demonstrating that structured search with branching and parent selection benefits complex implementation tasks

## Limitations

- Frontier AI research agents with state-of-the-art scaffolds recover less than 20% of speedrun improvements without hints, demonstrating that autonomous scientific reproduction without guidance remains effectively unsolved
- Even with detailed mini-paper hints, the best agent combination only recovers ~46% of speedrun improvements, leaving more than half of documented human innovations beyond reliable automated reproduction
- DeepSeek-R1's performance degrades when given individual hint descriptions compared to no-hint baseline — attempting to implement the specified changes results in buggy code that performs worse than making no changes at all
- Claude 3.7 Sonnet generates an increasing proportion of buggy nodes in iterative search trees, with errors eventually overtaking working solutions — the model is fundamentally unable to self-correct and improve code under iterative scaffolding
- Cumulative sequential reproduction fails catastrophically after only 2-3 steps — agents building on their own prior solutions rather than ground-truth records see performance collapse to zero improvement by the fourth record
- Injecting external technical documentation about post-training-cutoff APIs (FlexAttention, released August 2024) into model context actually worsens performance, suggesting models cannot productively exploit knowledge not internalised during pretraining
- Combining richer hint formats (text + pseudocode, mini-paper + pseudocode) substantially degrades o3-mini performance compared to pseudocode alone, revealing a failure to integrate longer and more heterogeneous context for code implementation tasks
- Explicit debugging steps in agent scaffolds provide no measurable benefit over simple iterative improvement — AIDE-based scaffolds with debug logic match performance of tree/forest methods without debugging, indicating agents cannot meaningfully self-diagnose code errors
- Gemini-2.5-Pro generates working code reliably but systematically fails to implement the more efficient target solutions — it optimises for code correctness at the cost of performance improvement, suggesting it cannot reason about hardware-level optimisation trade-offs
- Reproducibility benchmark performance degrades monotonically as task complexity increases — later records (higher index) are consistently harder for all agent models, suggesting agents cannot handle the cumulative algorithmic complexity of advanced training optimisations
- Current reproducibility benchmarks cannot disentangle memorisation from genuine generalisation — models may have seen ground-truth speedrun solutions during pretraining, making it impossible to determine whether performance reflects true code synthesis capability
- Current AI research agents are evaluated only on code-level reproduction of single-script training optimisations — multi-file codebases, distributed training considerations, and optimising for properties beyond wall-time (held-out task performance, memory footprint) are entirely out of scope

## Bottlenecks

- Automated scientific reproduction remains effectively unsolved: frontier reasoning agents with search scaffolds and detailed hints recover less than half of known human innovations in LLM training, blocking reliable autonomous research agents
- Compounding error propagation in sequential agent code generation blocks reliable multi-step scientific reproduction — errors in earlier outputs corrupt the starting point for subsequent tasks, causing performance to collapse after 2-3 steps
- Knowledge cutoff creates a hard boundary on agent ability to exploit recently released APIs and libraries — in-context injection of external documentation about post-cutoff modules worsens rather than improves performance, blocking agents from using the frontier technical stack

## Breakthroughs

- Community-driven NanoGPT speedrun achieved a 15x reduction in GPT-2 training wall time (45 minutes to under 3 minutes on 8xH100) through a succession of algorithmic and hardware-aware innovations including the Muon optimizer, mixed precision, and FlexAttention
- Muon optimizer, discovered in the context of a community speedrun competition, demonstrated generalisation beyond the GPT-2 training regime to provide training efficiency benefits for much larger modern LLMs — elevating a competition artefact to a broadly applicable training technique

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/aider|Aider]]
- [[entities/fineweb|FineWeb]]
- [[entities/flexattention|FlexAttention]]
- [[entities/muon-optimizer|Muon Optimizer]]
