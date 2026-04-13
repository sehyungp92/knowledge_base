---
type: source
title: 'Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment
  Construction'
source_id: 01KJT62ZGZMRE59Q4GV3Q450G8
source_type: paper
authors:
- Nex-AGI Team
- ':'
- Yuxuan Cai
- Lu Chen
- Qiaoling Chen
- Yuyang Ding
- Liwen Fan
- Wenjie Fu
- Yufei Gao
- Honglin Guo
- Pinxue Guo
- Zhenhua Han
- Zhengfu He
- Hanglei Hu
- Kai Hu
- Shengjia Hua
- Tianyu Huai
- Baodai Huang
- Li Ji
- Zhen Jiang
- Zhikai Lei
- Bufan Li
- Jiahang Lin
- Lizhi Lin
- Jinxiu Liu
- Shichun Liu
- Ziming Liu
- Yuchen Ni
- Pengfang Qian
- Yujiong Shen
- Qingyun Shi
- Wentao Shu
- Peng Sun
- Yiran Suo
- Tian Tang
- Boyu Tian
- Guoteng Wang
- Junzhe Wang
- Peixin Wang
- Zhiheng Xi
- Hang Yan
- Jie Yang
- Zhixiong Yang
- Tianchu Yao
- Guangze Ye
- Qianxi Yu
- Shuo Zhang
- Xinyue Zhang
- Yiqi Zhang
- Jiarong Zhao
- Miao Zheng
- Rui Zheng
- Enyu Zhou
- Jiazheng Zhou
- Maosen Zhou
- Yuhao Zhou
- Tao Gui
- Yining Zheng
- Xinchi Chen
- Jie Zhou
- Siyuan Feng
- Qin Chen
- Liang He
- Qi Zhang
- Xuanjing Huang
- Xipeng Qiu
published_at: '2025-12-04 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- post_training_methods
- software_engineering_agents
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment Construction

**Authors:** Nex-AGI Team, :, Yuxuan Cai, Lu Chen, Qiaoling Chen, Yuyang Ding, Liwen Fan, Wenjie Fu, Yufei Gao, Honglin Guo, Pinxue Guo, Zhenhua Han, Zhengfu He, Hanglei Hu, Kai Hu, Shengjia Hua, Tianyu Huai, Baodai Huang, Li Ji, Zhen Jiang, Zhikai Lei, Bufan Li, Jiahang Lin, Lizhi Lin, Jinxiu Liu, Shichun Liu, Ziming Liu, Yuchen Ni, Pengfang Qian, Yujiong Shen, Qingyun Shi, Wentao Shu, Peng Sun, Yiran Suo, Tian Tang, Boyu Tian, Guoteng Wang, Junzhe Wang, Peixin Wang, Zhiheng Xi, Hang Yan, Jie Yang, Zhixiong Yang, Tianchu Yao, Guangze Ye, Qianxi Yu, Shuo Zhang, Xinyue Zhang, Yiqi Zhang, Jiarong Zhao, Miao Zheng, Rui Zheng, Enyu Zhou, Jiazheng Zhou, Maosen Zhou, Yuhao Zhou, Tao Gui, Yining Zheng, Xinchi Chen, Jie Zhou, Siyuan Feng, Qin Chen, Liang He, Qi Zhang, Xuanjing Huang, Xipeng Qiu
**Published:** 2025-12-04 00:00:00
**Type:** paper

## Analysis

# Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment Construction
2025-12-04 · paper · Nex-AGI Team, :, Yuxuan Cai, Lu Chen, Qiaoling Chen et al. (66 total)
https://arxiv.org/pdf/2512.04987

---

### Motivation & Prior Limitations
- LLMs trained on static text corpora operate as "System 1" responders, lacking the long-horizon, goal-oriented reasoning required for agentic tasks, because the next-token prediction objective is fundamentally misaligned with sequential decision-making under environmental feedback.
  - Models trained this way fall into probability traps and myopic decision-making, failing to perform robust error recovery when actions fail in real-world tool-use scenarios.
- Constructing diverse, reliable interactive environments for agentic training is prohibitively expensive and has not scaled: existing approaches rely on limited or rigid frameworks that constrain the behavioral distribution available for policy learning.
  - Most open-source agent frameworks were designed for small-scale experiments, not large-scale reproducible trajectory generation, and collectively cover only a narrow range of tasks, tools, and interaction patterns.
- Agents trained on purely synthetic or static data exhibit a disconnect between reasoning and action, leading to hallucinations in tool usage such as invoking APIs based on outdated assumptions, because they have no exposure to the latency, stochasticity, and feedback loops of real-world execution.

---

### Proposed Approach
- The paper introduces a three-component unified ecosystem — NexAU, NexA4A, and NexGAP — that transforms environment construction from manual engineering into automated synthesis, enabling the generation of diverse, grounded agentic training trajectories at scale.
- **NexAU (Nex Agent Universe)** is a lightweight runtime that decouples agent definition from execution via declarative YAML configurations, implementing a recursive, fractal ReAct architecture where sub-agents are treated as interchangeable tools with isolated reasoning states, preventing context pollution in long-horizon tasks.
  - Unlike graph-based orchestration systems, NexAU's recursive delegation model allows a parent agent to instantiate child execution contexts with their own system prompts and toolsets, enabling simulation of hierarchies as deep as a "CTO" agent delegating to a "Software Engineer" agent without context overflow.
  - NexAU integrates Model Context Protocol (MCP) for live external services, supports Skill injection for procedural knowledge retrieval, and provides a thread-safe GlobalStorage mechanism for stateful cross-agent interactions.
- **NexA4A (Agent for Agent)** is a generative system that produces complete agent frameworks — including system prompts, sub-agent graphs, tool selections, and MCP integrations — from natural-language specifications alone, using a MetaAgent that chooses workflow patterns, decomposes tasks hierarchically, and assembles multi-agent systems typically one to three layers deep.
  - This approach treats agent environments as generative language specifications rather than static code, breaking the dependency on human-designed environments and enabling programmatic synthesis of new interaction topologies without writing executable framework code.
- **NexGAP (General Agent-data Pipeline)** generates end-to-end agentic trajectories by seeding framework construction with real MCP tools, synthesizing tasks via a hierarchical Problem Type Tree with inverse-frequency weighted sampling, executing agents through NexAU, and normalizing trajectories into seven distinct tool-call formats including OpenAI format and XML variants.
  - To mitigate hallucination and temporal knowledge gaps, NexGAP incorporates web search augmentation into query synthesis and employs a Quality Assessment Agent that iteratively processes trajectory batches and identifies issues such as reward hacking (e.g., fabricating test results using nonexistent test files), placeholder tool outputs, and excessive tool-return verbosity.

---

### Results & Capabilities
- Nex-N1 consistently outperforms open-source models of comparable size across six agentic benchmarks and achieves competitive performance with frontier proprietary models; the largest Nex-N1 variant surpasses GPT-5 on the BFCL v4 tool-use benchmark.
  - On τ²-bench (constraint-satisfaction in dual-control environments), DeepSeek-V3.1 fine-tuned with Nex-N1 reaches 80.2 vs. 42.8 for the base model; on SWE-bench Verified, it reaches 70.6 vs. 66.0 for the base; on BFCL v4, it reaches 65.3 vs. 56.3.
  - Smaller models also benefit substantially: Qwen3-32B fine-tuned with Nex-N1 improves from 41.5 to 72.1 on τ²-bench and from 12.9 to 50.5 on SWE-bench.
- Nex-N1 demonstrates strong cross-framework robustness on SWE-bench Verified evaluated across Terminus-2 XML, Claude Code, and OpenHands scaffolds, scoring 51.2, 62.0, and 63.5 respectively on a 100-instance subset, unlike models such as MiniMax M2 which score 0 under OpenHands.
- In human evaluation on agentic coding (43 test samples, 13 scenarios run inside Claude Code), Nex-N1 wins or ties against claude-sonnet-4.5 in 64.5% of scenarios and against MiniMax-M2 in 92.9% of scenarios, assessed on success rate, code accuracy, execution efficiency, readability, and scenario adaptability.
- A deep research agent built on NexAU and Nex-N1 scores 47.0% on the public Deep Research Benchmark, supporting multi-step planning, webpage inspection, iterative reflection, and — distinctively from competitors — visualized report and slide generation via dedicated sub-agents for image retrieval and visual design.
- The infrastructure produced over 200 agent frameworks and environments with agent graphs ranging from 1 to 34 nodes, spanning standard ReAct agents, multi-layer multi-agent systems, and fixed workflow pipelines across seven tool-call formats.

---

### Implications
- By demonstrating that agent environments can be gen

## Key Claims

1. Constructing interactive environments that are both broad in scope and reliable in structure is prohibitively expensive, and current approaches rely on limited environments or rigid frameworks.
2. NexAU adopts a recursive, fractal architecture inspired by the ReAct paradigm, treating sub-agents, tools, and external services as interchangeable functional units.
3. In NexAU, a sub-agent is exposed to its parent as simply a tool with a defined input schema, and the recursive structure ensures that reasoning states are isolated so a sub-agent's thought trace does 
4. NexAU uses declarative YAML configurations to define agents, decoupling the logical topology of an agent system from its imperative implementation, which allows programmatic synthesis of new agent arc
5. NexAU integrates Model Context Protocol (MCP) to connect agents to live external servers via a standardized protocol, ensuring the data synthesis pipeline respects the latency, error modes, and statef
6. NexA4A can automatically generate full multi-agent frameworks by constructing a declarative configuration defining nodes and interaction structure, using a MetaAgent that interprets high-level descrip
7. NexGAP constructs over 200 agent frameworks and environments, with agent and sub-agent graphs ranging from 1 to 34 nodes, spanning standard ReAct agents, multi-layer multi-agent systems, and fixed wor
8. Custom tools generated by NexA4A are often simple code snippets with limited interaction with outer systems; to address this, NexGAP incorporates over one hundred high-quality, production-ready real M
9. The query synthesis framework uses a Problem Type Tree—a hierarchical, bilingually annotated taxonomy—with an inverse-frequency weighted sampling strategy to mitigate sampling bias for underrepresente
10. Converting visual feedback from continuous scoring to binary judgments (e.g., whether a scene is too dark or whether a page is complete) improves reliability by turning subjective aesthetics into obje

## Capabilities

- Automated generation of diverse multi-agent frameworks and environments from natural language specifications, enabling training environment construction without manual engineering
- Agentic model training that generalises across heterogeneous agent frameworks — a single model achieves stable performance on SWE-bench across OpenHands, Claude Code, and Terminus-2 without framework-specific fine-tuning
- Deep research agents autonomously executing full research pipelines (task planning, web search, content extraction, iterative reflection, visualised report generation) achieving 47.0% on the Deep Research Benchmark
- Hierarchical multi-agent execution with isolated sub-agent contexts, enabling long-horizon task decomposition without context overflow via recursive ReAct delegation
- Large-scale automated agentic trajectory generation covering 200+ agent frameworks with 1–34 node agent graphs, spanning 7 distinct tool-call formats, used as training data
- Open-source agentic model (DeepSeek-V3.1-Nex-N1) surpassing GPT-5 on tool-use benchmarks (BFCL v4: 65.3 vs 61.6) while being competitive across general agentic and coding tasks

## Limitations

- Reward hacking is widespread in trained coding agents: agents fabricate test results using nonexistent test files rather than actually solving the underlying task, undermining RL-based agentic training
- Agentic model performance is highly framework-dependent: the same model (MiniMax M2) scores 64.5% on Claude Code but 0% on OpenHands on the same benchmark, with most models showing large gaps between reported scores and cross-framework scores
- Agentic benchmark results are highly sensitive to which specific tool implementation is used: swapping DuckDuckGo for Google Search caused a ~20-point swing for GPT-5 on BFCL, making benchmark scores non-reproducible without exact tool specification
- LLMs trained on static corpora systematically fail as agents: they act as 'System 1' responders susceptible to probability traps and myopic decision-making, unable to perform the long-horizon goal-oriented reasoning agentic tasks require
- Agents trained on static or purely synthetic data fail at real-world execution: hallucinate tool calls based on outdated API assumptions, and cannot perform robust error recovery when actions fail
- Visual feedback mechanisms for agentic code repair are unreliable — continuous quality scoring is too noisy to direct repair, requiring discretisation into binary judgments as a workaround
- Context overflow is a fundamental constraint for long-horizon agentic tasks: without explicit sub-agent isolation, parent agent context accumulates and degrades multi-step task performance
- Automated tool generation by LLMs produces shallow placeholder implementations with limited real system interaction, requiring manual curation of real MCP tools to achieve authentic training environments
- Agentic training trajectory quality assessment is significantly harder and more expensive than single-turn post-training data: length and scenario diversity make automated filtering error-prone, requiring multi-taxonomy agent judges
- Initial code generated for complex multi-component or interactive scenes is frequently unusable and requires iterative self-repair, which itself fails for sufficiently complex outputs (e.g. 3D scenes, interactive web pages)
- Cost of running full agentic evaluations forces sub-sampling that limits statistical validity: cross-framework comparisons in this paper use only 100 SWE-bench instances, making results potentially unrepresentative
- Existing open-source agent frameworks were designed as small-scale research prototypes, not production-grade trajectory generation infrastructure — they are fragile at scale with narrow task and tool coverage

## Bottlenecks

- Constructing diverse, high-quality interactive environments for agentic training is prohibitively expensive and manual, limiting the behavioral diversity available for training agents to generalise
- Simulation-reality gap in agentic training data: agents trained on synthetic environments cannot bridge to real-world execution because real APIs have latency, stochasticity, and statefulness that simulation cannot faithfully capture
- Objectively verifiable reward signals for complex agentic tasks are unavailable or gameable: binary success is too sparse, test execution can be fabricated, and intermediate process rewards require manual design

## Breakthroughs

- NexA4A: fully automated synthesis of complete multi-agent frameworks from natural language, generating 200+ environments spanning 1–34 node graphs and 7 tool-call formats without manual engineering
- Framework-agnostic agentic model: training on diverse framework topologies produces a model that maintains stable SWE-bench performance across OpenHands, Claude Code, and Terminus-2, solving a previously hidden framework-brittleness problem

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/react|ReAct]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/τ2-bench|τ2-bench]]
