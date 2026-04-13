---
type: source
title: 'ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration'
source_id: 01KJT6ZBSZZGS2P7B02HS6CNP3
source_type: paper
authors:
- Hongjin Su
- Shizhe Diao
- Ximing Lu
- Mingjie Liu
- Jiacheng Xu
- Xin Dong
- Yonggan Fu
- Peter Belcak
- Hanrong Ye
- Hongxu Yin
- Yi Dong
- Evelina Bakhturina
- Tao Yu
- Yejin Choi
- Jan Kautz
- Pavlo Molchanov
published_at: '2025-11-26 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- policy_optimization
- reinforcement_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration

**Authors:** Hongjin Su, Shizhe Diao, Ximing Lu, Mingjie Liu, Jiacheng Xu, Xin Dong, Yonggan Fu, Peter Belcak, Hanrong Ye, Hongxu Yin, Yi Dong, Evelina Bakhturina, Tao Yu, Yejin Choi, Jan Kautz, Pavlo Molchanov
**Published:** 2025-11-26 00:00:00
**Type:** paper

## Analysis

# ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration
2025-11-26 · paper · Hongjin Su, Shizhe Diao, Ximing Lu, Mingjie Liu, Jiacheng Xu et al. (16 total)
https://arxiv.org/pdf/2511.21689

---

### Motivation & Prior Limitations
Prior tool-use agent research has been dominated by the single-model paradigm: equipping one powerful LLM with utility tools such as web search or calculators, which the authors argue fundamentally underutilizes the potential of tool-augmented reasoning.
- This monolithic approach fails to mirror how humans reason, namely by delegating sub-problems to domain experts and specialized systems rather than relying on a single generalist.
- Attempting to implement orchestration naively by prompting off-the-shelf models introduces systematic biases: GPT-5 delegated 73% of model calls to GPT-5-mini (self-enhancement bias), while Qwen3-8B deferred to GPT-5 in 66% of calls (defaulting to the strongest tool regardless of cost or utility).
- Controllability in tool-use agents along the dimensions of cost-efficiency and user preferences has remained largely unexplored, leaving no principled mechanism for aligning agent behavior with user-specified cost constraints.

---

### Proposed Approach
ToolOrchestra trains a small (8B-parameter) language model, Orchestrator, as the centralized "brain" of a heterogeneous multi-agent system, using end-to-end reinforcement learning with a multi-objective reward that jointly optimizes for task correctness, cost-latency efficiency, and alignment with user tool preferences.
- Unlike prior work that restricts tools to deterministic utilities, ToolOrchestra broadens the toolset to include domain-specialized LLMs (e.g., Qwen2.5-Math-7B, Codestral-22B) and powerful generalist LLMs (e.g., GPT-5, Claude Opus 4.1), all exposed through a single unified JSON-based interface — enabling the orchestrator to treat other models as callable tools with varying cost and capability.
- The agentic task is formalized as an MDP incorporating user action preferences, per-action costs, latency, and a binary correctness reward; the rollout follows a reasoning–action–observation loop for up to 50 turns, allowing multi-hop tool chaining across heterogeneous resources.
- To bootstrap RL training, the authors build an automatic data synthesis pipeline producing thousands of verifiable multi-turn tool-use examples across 10 domains (the ToolScale dataset), which will be publicly released.

---

### Results & Capabilities
Orchestrator-8B achieves 37.1% on HLE, outperforming GPT-5 (35.1%), Claude Opus 4.1 (34.6%), and Qwen3-235B-A22B (32.8%) while being 2.5x more computationally efficient than GPT-5.
- On τ2-Bench, Orchestrator scores 80.2% versus GPT-5's 77.7%, and does so by calling GPT-5 in only ~40% of reasoning steps—using cheaper models and tools for the remainder—while still exceeding a full-GPT-5 agent, demonstrating intelligent cost-aware routing.
- On FRAMES, Orchestrator achieves 76.3% against GPT-5's 74.0% and Qwen3-235B-A22B's 74.2%, using approximately 30% of GPT-5's cost across both FRAMES and τ2-Bench.
- The RL-trained Orchestrator generalizes robustly to unseen tasks and tools despite significant differences between training and evaluation distributions, indicating that the learned orchestration policy captures general reasoning patterns rather than task-specific heuristics.
- The RL-trained Orchestrator exhibits a balanced tool-calling distribution (33% GPT-5, 27% Qwen3-32B, 16% GPT-5-mini, 6% Qwen2.5-Coder-32B) compared to the pathological distributions of prompted models, confirming that training resolves self-enhancement and strength-defaulting biases.

---

### Implications
The central finding — that an 8B orchestrator outperforms frontier models of 235B+ parameters on hard reasoning benchmarks — provides strong empirical evidence that intelligence in complex tasks is better achieved through compositional, cost-aware delegation than through scaling a single monolithic model.
- This shifts the design question for agentic AI systems from "how large should the model be?" toward "how should a lightweight controller allocate sub-problems across a heterogeneous tool ecosystem?", with direct implications for cost-efficient deployment of AI in production settings.
- The multi-objective RL reward framework — incorporating user preference signals alongside correctness and efficiency — advances the practical controllability of autonomous agents, a dimension relevant to both safety/alignment (ensuring agent behavior respects user intent) and commercial deployment.
- The release of ToolScale provides a training resource for the multi-agent systems community that may lower the barrier to training orchestration models across diverse task domains.

---

### Remaining Limitations & Next Steps
The source text is a partial excerpt; the full methods section (Section 3 onward) is truncated, meaning key details about the RL algorithm, reward shaping specifics, and the complete tool catalog are not available for evaluation.
- The evaluation is limited to three benchmarks (HLE, τ2-Bench, FRAMES); while these are challenging and diverse, it is unclear how the approach performs on domains not covered by training or on tasks requiring persistent memory or long-horizon planning beyond 50 turns.
- The paper acknowledges that prompting-based orchestration is brittle but does not fully characterize the failure modes of the RL-trained Orchestrator, leaving its robustness under adversarial or distribution-shifted tool availability unaddressed in the excerpt.
- Cost comparisons rely on the specific tool pricing structure used in evaluation; the efficiency advantage could vary significantly depending on the cost ratio between the orchestrator and the tools it calls, which the paper does not fully analyze in sensitivity.

## Key Claims

1. Orchestrator-8B achieves 37.1% on Humanity's Last Exam (HLE), outperforming GPT-5 which scores 35.1%.
2. Orchestrator-8B is 2.5x more computationally efficient than GPT-5 on the HLE benchmark.
3. On τ2-Bench and FRAMES, Orchestrator surpasses GPT-5 while using only approximately 30% of GPT-5's cost.
4. Orchestrator-8B achieves 80.2% on τ2-Bench, compared to GPT-5's 77.7%, Claude Opus 4.1's 76.8%, and Qwen3-235B-A22B's 75.6%.
5. Orchestrator-8B achieves 76.3% on FRAMES, compared to GPT-5's 74.0%, Qwen3-235B-A22B's 74.2%, and Claude Opus 4.1's 72.8%.
6. Prior tool-use agent research has primarily focused on equipping a single powerful model with utility tools such as web search or calculators, which underutilizes the potential of tools.
7. Relying on straightforward model prompting for orchestration is brittle and introduces systemic biases, including self-enhancement bias and defaulting to the strongest available tool.
8. GPT-5 disproportionately delegates tasks to GPT-5-mini in 73% of model calls when used as a prompted orchestrator.
9. Qwen3-8B, when used as a prompted orchestrator, defers to GPT-5 in 66% of model calls.
10. ToolOrchestra uses end-to-end reinforcement learning with three reward objectives: correctness of outcome, efficiency in resource usage, and alignment with user preferences.

## Capabilities

- An RL-trained 8B orchestrator model achieves higher accuracy than frontier models (37.1% vs GPT-5's 35.1% on HLE) at 2.5x lower cost by dynamically routing subtasks to appropriate tools and models
- Small language models (8B parameters) trained end-to-end with RL can serve as effective orchestrators of heterogeneous tool ecosystems — coordinating web search, code interpreters, specialised domain models, and generalist frontier LLMs through a unified tool-calling interface
- RL-trained orchestrators generalise robustly to unseen tools and task domains not present during training, adapting their tool-use policy to new challenges without degradation
- Multi-objective RL training for agentic tool orchestration — jointly optimising for task correctness, cost efficiency, and user preference alignment — yields controllable and cost-effective tool-use policies
- A trained orchestrator can selectively invoke expensive frontier models for only ~40% of reasoning steps while still exceeding the performance of an agent that uses the large model for every step

## Limitations

- Prompting-based orchestration with off-the-shelf models exhibits self-enhancement bias — models disproportionately delegate to developmentally-related variants of themselves (GPT-5 calls GPT-5-mini in 73% of delegations)
- Off-the-shelf models used as orchestrators via prompting default to the strongest available tool regardless of cost or relative utility, making cost-efficient orchestration impossible without dedicated training
- Even the best tool-augmented agents achieve only ~37% on HLE — complex cross-domain reasoning tasks remain largely unsolved even with full access to a diverse toolkit of frontier models
- Controllability of tool-use agents along cost-efficiency and user-preference axes is a largely unexplored design dimension — prior research has focused exclusively on accuracy
- RL training for orchestrators is constrained to verifiable domains — the data synthesis pipeline requires automatically checkable outcomes, blocking extension to open-ended or unverifiable tasks
- Tool description generation for LLMs-as-tools requires a multi-step empirical sampling process (sample tasks → collect trajectories → auto-generate descriptions), making tool registration for new models semi-manual and hard to scale
- Multi-turn rollout is capped at 50 turns, imposing a hard limit on the complexity of problems the orchestrator can address and potentially causing truncated solutions on the hardest tasks
- All evaluations are on structured benchmarks (HLE, τ2-Bench, FRAMES) with no real-world or production deployment validation — system behaviour under open-domain, adversarial, or ambiguous conditions is unknown

## Bottlenecks

- Naive prompting of frontier models as orchestrators produces systematically biased tool-selection policies — self-enhancement and cost-agnostic defaulting prevent reliable orchestration without dedicated RL training
- Verifiable reward signal scarcity limits RL-trained orchestrators to a narrow set of structured domains — extending RL orchestration training to open-ended tool-use settings requires solving the outcome verification problem first

## Breakthroughs

- A small 8B model trained via RL to orchestrate diverse tools — including stronger frontier models — outperforms those frontier models on hard reasoning benchmarks at significantly lower cost, demonstrating that system-level intelligence can exceed the capability of any individual component

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/humanitys-last-exam|Humanity's Last Exam]]
- [[entities/markov-decision-process|Markov Decision Process]]
- [[entities/τ2-bench|τ2-bench]]
