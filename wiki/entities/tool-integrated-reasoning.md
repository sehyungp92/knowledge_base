---
type: entity
title: Tool-Integrated Reasoning
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- mathematical_and_formal_reasoning
- multi_agent_coordination
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0008367699314797665
staleness: 0.0
status: active
tags: []
---
# Tool-Integrated Reasoning

Tool-Integrated Reasoning (TIR) is a paradigm for enhancing LLM reasoning by weaving external tools (primarily code interpreters) directly into the generation process, allowing models to delegate computation, verify intermediate steps programmatically, and iterate mid-chain rather than treating tool calls as discrete post-reasoning actions. It has emerged as one of the most consequential methodological shifts in the RL-for-reasoning literature, with systems like ReTool and Agent0 demonstrating that training models to reason *through* tools rather than *after* reasoning produces substantially faster convergence and higher final accuracy than text-only RL baselines.

**Type:** method
**Themes:** [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

TIR reframes the role of tools in LLM reasoning: rather than calling a calculator or code executor only after completing a reasoning trace, a TIR model interleaves tool invocations throughout its chain of thought, using execution feedback to steer subsequent thinking. This programmatic grounding addresses a fundamental weakness of pure text-based reasoning, namely that internal consistency does not guarantee correctness, whereas a code interpreter that returns a wrong answer cannot be argued with.

The paradigm gained traction as RL training methods (GRPO, PPO, and variants) proved capable of teaching models *when* to invoke tools and how to interpret their outputs. The key insight from systems like ReTool is that tool use need not be hand-coded: given a verifiable reward signal and sufficient training, models discover strategic tool use on their own, and they do so faster than text-only RL (400 training steps versus 1000+ for comparable performance).

## Key Findings

### Empirical Gains Are Large and Fast

The quantitative case for TIR is now substantial. ReTool, built on a DeepSeek-R1-Distill-Qwen-32B backbone, reaches 72.5% accuracy on AIME 2024 in extended settings, outperforming OpenAI o1-preview by 27.9 percentage points. The Qwen2.5-32B-Instruct variant hits 67.0% on AIME 2024 and 49.3% on AIME 2025 with only 400 training steps, whereas the text-only RL baseline requires more than 1,000 steps to reach 40.0%. This efficiency advantage suggests TIR is not just stronger but structurally better suited to the RL training loop: tool outputs provide dense, unambiguous feedback that shortens the credit assignment problem.

AGENTFLOW extends TIR gains to broader agentic settings, showing that a 7B-scale backbone trained under TIR principles achieves average accuracy gains of 14.9% on knowledge-intensive search tasks, 14.0% on broader agentic tasks, 14.5% on mathematical reasoning, and 4.1% on scientific reasoning relative to top-performing baselines. The gains on mathematical reasoning are consistent with ReTool's findings; the gains on search and agentic tasks reveal that the paradigm generalises beyond arithmetic and symbolic computation.

### Self-Evolving Curricula Amplify TIR

Agent0 pushes TIR into a self-supervised regime. It initialises two agents from the same base LLM (a curriculum agent and an executor agent) and co-evolves them through symbiotic competition, with no human-labeled training data. The curriculum agent learns to generate progressively harder tasks by maximising an uncertainty reward calibrated to the executor's self-consistency: the reward is maximised when the executor's pass rate is near 0.5, penalising tasks that are either trivially easy or impossibly hard. Evidence of successful curriculum learning is visible both in performance (Qwen3-8B-Base math score rises from 55.1 at iteration 1 to 58.2 at iteration 3) and in the curriculum itself (executor pass rate on generated tasks falls from 64.0% to 51.0% across iterations, confirming difficulty is increasing).

Crucially, the curriculum agent is also shaped to generate tool-reliant problems: an explicit tool reward causes average tool calls per generated task to rise from 1.65 to 2.60 across iterations. Ablations confirm this is not incidental; removing the tool reward causes a 7.2% performance drop, and removing the curriculum agent's training entirely causes a 9.3% drop.

### Training Dynamics and Implementation Details

ReTool sets the KL coefficient to 0.0 during RL training, indicating the team found standard KL regularisation unhelpful or counterproductive when tool outputs anchor the reward signal more strongly than the reference policy. Agent0 uses an Adaptive DPO (ADPO) variant that dynamically relaxes the upper clipping bound for high-ambiguity tasks, allowing larger gradient steps on low-probability but correct solutions, a sensible adjustment given that tool-integrated trajectories with correct outcomes may be sparse early in training. The tool reward scaling for Agent0's curriculum agent is set to λ_tool = 0.6 with a cap of C = 4, suggesting the tool signal is strong but not allowed to overwhelm the primary task reward.

### Historical Parallel and Conceptual Grounding

The appeal to AlphaGo and AlphaZero is instructive: those systems demonstrated that reward-only self-play could surpass world champions across Go, chess, shogi, and Stratego without human demonstrations. TIR occupies an analogous position in LLM reasoning: the tool (code interpreter, search engine, calculator) plays the role of the game engine, providing unambiguous outcome signal that RL can exploit without supervised labels. The analogy is imperfect (language tasks are open-ended where games are closed), but it explains why TIR enables the kind of sample efficiency gains that text-only RL cannot match.

## Limitations and Open Questions

The gains reported for TIR are concentrated in domains with clean, verifiable outputs: mathematical olympiad problems, code execution, structured search. How the paradigm transfers to tasks where tool output is noisy, ambiguous, or requires interpretation remains underexplored. AGENTFLOW's 4.1% gain on scientific reasoning (versus 14.5% on math) hints at a difficulty gradient correlated with output verifiability.

The KL=0.0 setting in ReTool raises a question about training stability: without KL regularisation, what prevents the policy from collapsing or mode-hopping? The paper does not fully address the conditions under which this is safe. Agent0's curriculum mechanism depends on the executor's self-consistency as a proxy for task difficulty, but self-consistency is itself a learned behaviour that may not track true difficulty monotonically across all task types.

The maturity classification of `narrow_production` reflects the current state: TIR works reliably in mathematical and code-execution settings, and some agentic search tasks, but has not demonstrated robust generalisation to the full breadth of reasoning challenges. The self-evolving curriculum (Agent0) remains limited to domains where automated verification is tractable; extending it to open-ended generation or multi-step scientific reasoning requires either learned verifiers or human feedback, reintroducing the annotation cost the paradigm sought to eliminate.

## Relationships

TIR sits at the intersection of [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] and [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], but its self-evolving variants (Agent0) are equally relevant to [[themes/agent_self_evolution|Agent Self-Evolution]] and [[themes/multi_agent_coordination|Multi-Agent Coordination]], since curriculum-executor co-evolution is a form of two-agent mutual shaping. The ADPO training variant connects to [[themes/policy_optimization|Policy Optimization]] research on trust region methods. The AlphaGo parallel links conceptually to [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], specifically the question of when self-play or environment-feedback alone is sufficient to exceed human-curated training data.

## Sources
