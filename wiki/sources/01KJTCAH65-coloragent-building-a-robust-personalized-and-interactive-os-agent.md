---
type: source
title: 'ColorAgent: Building A Robust, Personalized, and Interactive OS Agent'
source_id: 01KJTCAH651RC7BMGMDJ344JGJ
source_type: paper
authors:
- Ning Li
- Qiqiang Lin
- Zheng Wu
- Xiaoyun Mo
- Weiming Zhang
- Yin Zhao
- Xiangmou Qu
- Jiamu Zhou
- Jun Wang
- Congmin Zheng
- Yuanyi Song
- Hongjiang Chen
- Heyuan Huang
- Jihong Wang
- Jiaxin Yin
- Jingwei Yu
- Junwei Liao
- Qiuying Peng
- Xingyu Lou
- Jun Wang
- Weiwen Liu
- Zhuosheng Zhang
- Weinan Zhang
published_at: '2025-10-22 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- multi_agent_coordination
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ColorAgent: Building A Robust, Personalized, and Interactive OS Agent

**Authors:** Ning Li, Qiqiang Lin, Zheng Wu, Xiaoyun Mo, Weiming Zhang, Yin Zhao, Xiangmou Qu, Jiamu Zhou, Jun Wang, Congmin Zheng, Yuanyi Song, Hongjiang Chen, Heyuan Huang, Jihong Wang, Jiaxin Yin, Jingwei Yu, Junwei Liao, Qiuying Peng, Xingyu Lou, Jun Wang, Weiwen Liu, Zhuosheng Zhang, Weinan Zhang
**Published:** 2025-10-22 00:00:00
**Type:** paper

## Analysis

# ColorAgent: Building A Robust, Personalized, and Interactive OS Agent
2025-10-22 · paper · Ning Li, Qiqiang Lin, Zheng Wu, Xiaoyun Mo, Weiming Zhang et al. (23 total)
https://arxiv.org/pdf/2510.19386

---

### Motivation & Prior Limitations
- Existing GUI/OS agents are predominantly passive "task executors" that fail to engage with users as collaborative partners, leaving unresolved the dual challenge of robust long-horizon environment interaction and personalized human intent alignment.
  - Single-agent paradigms suffer from three diagnosed failure modes on AndroidWorld: limited generalization (inability to adapt to minor UI variations or reuse prior experience), inconsistency and lack of memory across long-horizon compositional tasks, and poor error recovery — collectively accounting for over half of observed failures.
- Prior agentic frameworks rely on static, manually annotated datasets, creating a data bottleneck that constrains continuous model improvement and generalization to out-of-domain environments.
  - Single-action annotation paradigms implicitly penalize valid alternative action paths (e.g., tapping "Back" vs. calling `system_button("Back")`), misaligning training with real-world GUI interaction where multiple paths achieve the same goal.
- State-of-the-art agents before this work — including UI-TARS-1.5 (64.2%), MobileRL (75.8% on AndroidWorld), and MobileUse (62.9%) — either lacked open-model reproducibility or did not integrate personalized user interaction, leaving a gap between benchmark automation and real-world usability.

---

### Proposed Approach
- ColorAgent introduces a two-stage progressive training paradigm combined with a four-module multi-agent framework, targeting both the intrinsic reasoning capability of the GUI model and the systemic robustness of task execution.
  - **Stage I: Step-Wise Reinforcement Learning** decomposes offline GUI trajectories into per-step training samples `{I, h_{t-1}, s_t, a_t}` and applies Group Relative Policy Optimization (GRPO) with rule-based rewards covering format correctness and action accuracy (coordinate proximity, semantic text similarity, swipe direction); multi-path augmentation expands annotations to all verified valid actions with equal reward weight; difficulty-based filtering discards trivially easy (c=8) and trivially hard (c=0) samples from eight inference runs per instance.
  - **Stage II: Self-Evolving Training** creates an iterative loop — query generation via human seed experts augmented by DeepSeek-R1 expansion, trajectory rollout on dual environments (Android virtual + ColorOS physical devices), multi-discriminator filtering (task completion, action validity, path relevance, reasoning coherence), human correction of failed trajectories, and supervised fine-tuning — enabling the model to generate its own progressively higher-quality training data.
- The multi-agent framework adds three specialized modules around a central execution module: a **Knowledge Retrieval** module performing RAG over a knowledge database to inject task-specific priors; a **Task Orchestration** module that classifies composite vs. atomic tasks, decomposes them at a high level preserving user intent structure, and uses a memory transfer mechanism (task extractor + task rewriter) to propagate critical context across subtasks; and a **Hierarchical Reflection** module with three granularities — Action Reflector (per-step screenshot-diff monitoring), Trajectory Reflector (last 3–5 steps coherence check), and Global Reflector (end-of-task completion verification).
- For human intent alignment, two plug-and-play modules are explored: **Personalized User Intent Recognition** builds explicit (query-level SOP) and implicit (user profile) knowledge bases from historical trajectories and rewrites queries into personalized SOPs at deployment time via RAG; **Proactive Engagement** trains an "ask agent" via interleaved samples that decouple the judgment of when-to-ask from action-generation-given-answer, enabling the agent to autonomously decide between autonomous execution and clarifying dialogue.

---

### Results & Capabilities
- ColorAgent achieves state-of-the-art success rates of **77.2% on AndroidWorld** and **50.7% on AndroidLab**, surpassing all prior open models and frameworks, including MobileRL (75.8% / 46.8%) and Mobile-Agent-v3 (73.3% on AndroidWorld).
  - The training paradigm alone (applied to GUI-Owl-32B) yields 65.1% on AndroidWorld; adding the agent framework provides a further +12.1 points, confirming the complementary nature of model-level and framework-level contributions.
  - Applying step-wise RL to Qwen2.5-VL-72B-Instruct raises its AndroidWorld score from 35.0% to 58.3% (+23.3 pp); adding self-evolving training reaches 64.7% (+6.4 pp), demonstrating consistent gains across model scales.
- The ablation on AndroidWorld quantifies individual module contributions from the GUI-Owl-32B trained baseline (65.1%): Hierarchical Reflection → 70.3%, Task Orchestration → 72.8%, Knowledge Retrieval → 77.2%, confirming knowledge augmentation as the single largest framework-level gain.
- On human-agent interaction benchmarks, the personalized intent and proactive engagement modules achieve **58.66% IAR on MobileIAR** and **68.98% SR on VeriOS-Bench**, outperforming Qwen2.5-VL-72B-Instruct (53.75% / 54.01%) and all other baselines including UI-TARS-1.5-7B and GPT-4o.
- A notable generalization finding: despite higher training reward, the fine-tuned 72B model underperforms the fine-tuned 32B model on downstream benchmarks, suggesting larger models are more prone to overfitting the training distribution in GUI contexts.

---

### Implications
- The decomposition of OS agent failure into generalization, consistency, and error-recovery deficits — each addressed by a targeted module — provides a diagnostic framework that could guide multi-agent system design beyond mobile GUIs, particularly for any long-horizon agentic task requiring environ

## Key Claims

1. ColorAgent achieves a 77.2% success rate on AndroidWorld and 50.7% on AndroidLab, establishing new state-of-the-art results on both benchmarks.
2. More than half of single GUI agent failures stem from a lack of three core capabilities: generalization, reflection, and consistency.
3. Single GUI agents optimized on large-scale training datasets can achieve strong in-domain performance but easily fail in out-of-domain environments or tasks.
4. Single GUI agents are unable to learn from past trajectories to reuse prior experiences or avoid past mistakes, constituting a fundamental flaw.
5. Single agents are inherently incapable of handling compositional, long-horizon tasks without dedicated mechanisms for task decomposition, progress tracking, and cross-step memory management.
6. Step-wise reinforcement learning uses GRPO to optimize single-step decision-making in GUI agents, eliminating the need for a separate critic model.
7. Self-evolving training establishes a reinforcing cycle of data generation, model optimization, and higher-quality data generation, reducing reliance on manual annotation.
8. Traditional single-action annotation in GUI interaction frameworks implicitly penalizes valid alternative actions, failing to align with real-world GUI interaction characteristics where multiple disti
9. Multi-path augmentation boosts generalization in real-world scenarios at the cost of slightly compromising performance on static benchmarks that accept only one canonical action.
10. Difficulty-based filtering discards samples with perfect predictions (c=8) or complete failures (c=0) per 8 inference runs, yielding a more balanced and informative training dataset.

## Capabilities

- Mobile OS agent combining step-wise GRPO reinforcement learning and self-evolving training achieves 77.2% success rate on AndroidWorld and 50.7% on AndroidLab, establishing new SOTA among open models and frameworks for mobile GUI task completion
- Multi-agent framework with task orchestration, knowledge retrieval, and three-level hierarchical reflection enables consistent long-horizon task execution on mobile devices — decomposing composite goals, maintaining cross-step memory, and recovering from errors at action, trajectory, and global leve
- Self-evolving training pipeline for GUI agents creates a self-sustaining data generation loop (rollout → multi-discriminator filter → fine-tune), reducing reliance on manual annotation while continuously improving trajectory quality through iterative cycles
- Personalized OS agent extracts explicit SOPs and implicit user preferences from historical interaction trajectories, then rewrites queries and generates personalised standard operating procedures — achieving 58.66% intention alignment rate on MobileIAR
- Proactive ask agent autonomously determines when to execute tasks versus seek user clarification based on scenario trustworthiness assessment, achieving 68.98% step-wise success rate on VeriOS-Bench — substantially outperforming all baselines including GPT-4o (40.64%) and UI-TARS-7B-DPO (49.73%)
- Step-wise GRPO reinforcement learning applied to offline GUI trajectory data improves a 72B base model's mobile task success rate by 29.3 percentage points (35.0% → 64.7%) without a separate critic model, using rule-based format and action accuracy rewards

## Limitations

- Current mobile agent benchmarks are inadequate for OS agent evaluation: dominated by simple tasks, limited app coverage, no unpredictable or exceptional situations, and narrowly focused on task success rate while ignoring intent recognition accuracy, self-evolution, and user experience quality
- Single GUI agents fail in over 50% of real-world cases due to three structural deficiencies: (1) minor UI variations (e.g., double-click activation) cause repetitive unproductive loops; (2) cross-step memory loss causes information loss in compositional long-horizon tasks; (3) error recovery is limi
- Larger GUI models (72B) overfit training data more severely than smaller models (32B): the 72B achieves higher training reward but worse real-world benchmark performance — model scale does not reliably improve GUI agent generalisation
- OS agent security is entirely preliminary: the only mechanism is proactive human clarification in detected untrustworthy scenarios — no sandbox containment, no fine-grained permission boundaries, and no robust handling of adversarial inputs or abnormal conditions for a system with broad device acces
- Mobile OS agents remain unstable, unreliable, and untrustworthy for real-world deployment despite achieving SOTA benchmark performance — benchmark success rates do not predict reliable operation in the face of unpredictable real-world conditions
- Single GUI agents cannot adapt to new UI variations or learn from past errors during deployment — they have no mechanism to incorporate external knowledge or update strategy based on failure experience between tasks
- Multi-path annotation that improves real-world generalisation slightly degrades performance on static benchmarks that accept only a single 'canonical' action — creating a fundamental tension between benchmark optimisation and practical real-world usability
- Multi-agent collaboration for OS tasks introduces coordination overhead and efficiency bottlenecks — the design space for multi-agent OS architectures is largely unexplored and the scaling properties (latency, accuracy, communication cost) as agent pool size increases are unknown
- Full-parameter RL training of a 32B–72B GUI agent requires 64 A800 GPUs across multiple epochs — compute requirements that are inaccessible to most research groups and make rapid iterative training cycles prohibitive
- ColorAgent achieves only 50.7% success rate on AndroidLab — nearly half of tasks fail on a benchmark acknowledged to be simpler than real-world scenarios, revealing significant capability gaps in cross-application generalisation at the current SOTA

## Bottlenecks

- Inadequate OS agent evaluation paradigms distort research direction — benchmarks use simple tasks, narrow app coverage, single success-rate metrics, and ignore unpredictable real-world conditions, preventing reliable measurement of whether improvements transfer to deployment
- High-quality GUI interaction trajectory data requires expensive human annotation at scale — each trajectory requires real device interaction and step-level validation, limiting the volume and diversity of training data for GUI agents
- Absence of safe, controllable sandbox environments for OS agents blocks real-world deployment — agents with broad device access require principled containment and fine-grained permission control that does not yet exist at production grade
- Model scale does not reliably improve GUI agent generalisation — larger models overfit training distributions while smaller models underperform in-domain, leaving no clear scaling path for improving real-world OS agent capability

## Breakthroughs

- Step-wise GRPO reinforcement learning applied to decomposed offline GUI trajectories delivers a 29.3 percentage point success rate improvement (35.0% → 64.7% on AndroidWorld) for a 72B base VLM — establishing RL as a high-leverage, critic-free training signal for GUI agents using existing offline da
- Self-evolving training loop — iterative rollout on virtual and physical devices, multi-discriminator trajectory filtering, and fine-tuning with human-corrected failures — partially resolves the GUI training data bottleneck by creating a self-sustaining high-quality data generation cycle

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
