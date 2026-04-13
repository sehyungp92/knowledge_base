---
type: source
title: 'ReTool: Reinforcement Learning for Strategic Tool Use in LLMs'
source_id: 01KJTZD9X582STWH1FEVJY6HXF
source_type: paper
authors:
- Jiazhan Feng
- Shijue Huang
- Xingwei Qu
- Ge Zhang
- Yujia Qin
- Baoquan Zhong
- Chengquan Jiang
- Jinxin Chi
- Wanjun Zhong
published_at: '2025-04-15 00:00:00'
theme_ids:
- agent_systems
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ReTool: Reinforcement Learning for Strategic Tool Use in LLMs

**Authors:** Jiazhan Feng, Shijue Huang, Xingwei Qu, Ge Zhang, Yujia Qin, Baoquan Zhong, Chengquan Jiang, Jinxin Chi, Wanjun Zhong
**Published:** 2025-04-15 00:00:00
**Type:** paper

## Analysis

# ReTool: Reinforcement Learning for Strategic Tool Use in LLMs
2025-04-15 · paper · Jiazhan Feng, Shijue Huang, Xingwei Qu, Ge Zhang, Yujia Qin et al. (9 total)
https://arxiv.org/pdf/2504.11536

---

### Motivation & Prior Limitations
- Reasoning models trained with RL (e.g., DeepSeek R1, OpenAI o1) excel at textual chain-of-thought but systematically fail at tasks requiring precise symbolic manipulation, such as geometric reasoning, numerical computation, and complex equation solving.
  - Text-based RL on Qwen2.5-32B-Instruct achieves only 40% on AIME2024 after 1080 training steps, while the base model scores 26.7%, exposing a hard ceiling on purely internal reasoning for competition mathematics.
- Prior methods for equipping LLMs with tool use — prompting and supervised fine-tuning on curated tool-use demonstrations — are limited to imitating a fixed data distribution and cannot adaptively learn *when* or *how* to invoke tools across diverse problem settings.
  - These approaches lead to brittle heuristics and tool misuse outside seen patterns; they cannot self-correct from execution errors or discover novel invocation strategies.
- A concurrent RL-based tool-use work applied the paradigm only at the 1.5B and 7B scale on Qwen2.5-Math models, leaving the performance and emergent behavior at 32B+ unexplored.

---

### Proposed Approach
- ReTool is a two-stage framework — cold-start supervised fine-tuning followed by PPO-based reinforcement learning with interleaved real-time code interpreter (CI) execution — that trains a model to autonomously discover when and how to invoke a code sandbox as part of its long-chain reasoning process.
  - Unlike text-only RL rollouts, ReTool's rollout policy produces hybrid trajectories of the form `[t1 ⊕ c1 ⊕ f1 ⊕ ... ⊕ o]`, where natural language reasoning, code blocks, and sandboxed interpreter feedback (including error messages) are dynamically interleaved; generation pauses on a `</code>` trigger, dispatches to an async sandbox pool, and resumes with interpreter output wrapped in `<interpreter>` tags.
  - The reward is deliberately minimal: a binary ±1 accuracy reward on the final boxed answer only, with no code-executability reward, deliberately avoiding reward hacking while relying on outcome pressure alone to shape tool-use strategy.
- The cold-start dataset is constructed by transforming an existing text-reasoning corpus (seeded from OpenThoughts and filtered via DeepSeek-R1 evaluation) into code-augmented reasoning traces using a structured prompt template that replaces manual calculation steps with executable code snippets, followed by two-stage format and answer verification.
  - Interpreter feedback tokens are masked from the loss computation to prevent external sandbox output from corrupting the model's coherent reasoning gradient signal.
  - KV-cache reuse is applied at each `</code>` trigger to reduce memory overhead during rollout, and an asynchronous sandbox worker pool prevents slower execution threads from bottlenecking training throughput.

---

### Results & Capabilities
- ReTool (Qwen2.5-32B-Instruct) achieves 67.0% pass@1 on AIME2024 and 49.3% on AIME2025, surpassing the text-based RL baseline (40.0% / 36.7%) using 400 training steps versus over 1000 steps — a simultaneous gain in both accuracy and training efficiency.
  - ReTool (DeepSeek-R1-Distill-Qwen-32B) pushes further to 72.5% on AIME2024 and 54.3% on AIME2025, outperforming OpenAI o1-preview by 27.9% on AIME2024, QwQ-32B-Preview (50.0%), and s1-32B (56.7%).
- The cold-start SFT model alone (without RL) achieves 40.9% on AIME2024 — nearly matching the text-based RL ceiling — confirming the cold-start dataset itself captures meaningful tool-use patterns.
- Behavioral analysis reveals a suite of emergent cognitive patterns during RL training: average response length drops ~40% (from ~10k to ~6k tokens) as code displaces verbose arithmetic; code ratio rises to ~98% of all responses; code complexity (line count) increases ~5× by end of training; and code invocation timing shifts earlier in the response trajectory, indicating the model learns to front-load computational verification.
  - The model exhibits spontaneous *code self-correction* — upon receiving a `NameError` from the sandbox, it diagnoses the scope issue, reflects verbally ("Oops, the functions need to be defined in the same scope"), and rewrites corrected, executable code — despite no explicit self-correction training signal.
  - Code purpose diversity expands post-RL (from primarily calculation toward verification, enumeration, and search), reflecting metacognitive development of adaptive tool selection.
- CI-powered reasoning demonstrably avoids the compounding numerical errors seen in text-only reasoning: in the case study, text-based reasoning produces the wrong answer (629) through manual modular arithmetic, while CI-powered reasoning produces the correct answer (699) via programmatic search.

---

### Implications
- Outcome-driven RL can teach tool invocation strategy entirely from task-level feedback without any human-labeled tool-use demonstrations, suggesting that hybrid neuro-symbolic systems may be achievable through reward signal alone rather than requiring curated execution traces.
- The emergent code self-correction behavior — analogous to the "aha moment" of self-reflection in pure text RL models like DeepSeek-R1 — implies that metacognitive error-recovery capabilities can transfer from the textual reasoning domain to the executable code domain under the same RL pressure.
- The ~40% token reduction with CI-powered reasoning suggests a complementary path to inference efficiency: rather than compressing reasoning chains, offloading computation to tools may be a more structurally sound route to shorter, more accurate solutions, with implications for test-time compute scaling research.
- ReTool's architecture — interleaved tool calls within a reasoning loop, masked loss on external feedback, async sandbo

## Key Claims

1. Reasoning models trained with reinforcement learning excel in textual reasoning but struggle with structured problem-solving such as geometric reasoning, precise computation, or complex equation solvi
2. Code interpreters provide a formal and executable interface for enumeration, verification, and precise computation, reducing ambiguity and compounding errors common in textual reasoning.
3. Prompting and supervised fine-tuning approaches to tool use are limited to imitating curated data distributions and fail to generalize to adaptive decisions about when and how to invoke external tools
4. ReTool (Qwen2.5-32B-Instruct backbone) achieves 67.0% accuracy on AIME 2024 with only 400 training steps, outperforming the text-based RL baseline which achieves 40.0% with over 1000 training steps.
5. ReTool (DeepSeek-R1-Distill-Qwen-32B backbone) achieves 72.5% accuracy on AIME 2024, surpassing OpenAI o1-preview by 27.9 percentage points.
6. The cold-start model (SFT only, no RL) achieves 40.9% on AIME 2024, closely matching the text-based RL baseline (40.0%) and substantially surpassing the untrained base model (26.7%).
7. After RL training, average response length is reduced by approximately 40% (from ~10k to ~6k tokens), suggesting CI-powered reasoning improves token efficiency.
8. During RL training, the proportion of responses containing code increases to nearly 98% of all questions, indicating progressive development of strategic tool usage.
9. The average number of code lines in responses increases approximately fivefold during RL training, indicating the model learns more complex coding strategies.
10. Code invocation timing advances (shifts earlier in the response) during RL training, indicating the model learns to determine optimal timing for tool usage.

## Capabilities

- RL-trained tool-integrated reasoning (ReTool) achieves 67% accuracy on AIME 2024 in 400 training steps at 32B scale, and 72.5% with an advanced backbone — surpassing OpenAI o1-preview by 27.9% on competition mathematics
- LLMs trained with CI-powered RL autonomously develop emergent code self-correction — detecting interpreter error messages and rewriting code — without any explicit training examples for this behavior
- CI-powered RL reduces average reasoning response length by approximately 40% compared to text-based RL (10k to 6k tokens) while achieving higher accuracy — code offloading improves token efficiency
- RL training autonomously converges on optimal code invocation timing and selection strategy without human priors — code usage reaches ~98% coverage and invocation timing advances progressively through training

## Limitations

- Pure text-based reasoning LLMs systematically fail at precise numerical calculation and symbolic manipulation — compounding arithmetic errors accumulate across multi-step textual computation chains
- SFT-based tool-use training is constrained by data distribution and cannot generalize beyond demonstrated patterns — models misuse tools or fall back on brittle heuristics outside training conditions
- ReTool's tool-integrated RL is validated exclusively on competition mathematics (AIME) — generalization to non-mathematical domains, tool types beyond code interpreters, or open-ended real-world tasks is entirely undemonstrated
- CI-powered RL training requires specialised asynchronous sandboxed code execution infrastructure — a significant engineering overhead with no equivalent in standard text-based RL setups
- Code executability of incorrect reasoning trajectories deteriorates during RL training — code quality in failed responses consistently worsens while correct responses maintain near-100% pass rate, creating a bifurcated quality distribution
- CI-powered RL benefits are unclear below 32B scale — a concurrent work applying similar RL tool-use training at 1.5B and 7B 'remained suboptimal', suggesting a capability threshold that small models may not clear
- KV-cache memory overhead scales substantially with interleaved code execution during RL rollouts — special mitigation strategies are required to maintain training feasibility at standard sequence lengths
- Binary outcome reward design acknowledges reward hacking risk but only 'alleviates' rather than eliminates it — and the approach is structurally limited to domains with verifiable ground-truth answers
- RL training does not eliminate dependence on human-curated cold-start SFT data — dual-verification involving human expert curation is still required to produce the initialisation dataset before RL can proceed

## Bottlenecks

- Compounding numerical errors in pure text-based LLM reasoning block reliable multi-step mathematical computation — each manual arithmetic step introduces error that cascades through subsequent derivations
- Absence of standard infrastructure for integrating multi-turn external tool execution into RL rollout pipelines blocks broad adoption of tool-augmented RL training — each new tool type requires custom async sandbox engineering

## Breakthroughs

- RL training with interleaved code interpreter execution autonomously discovers optimal tool-use strategies — including when to invoke tools, what code to write, and how to correct failures — without human priors, achieving AIME accuracy exceeding o1-preview at 32B scale with 2.7× fewer training step
- Emergent code self-correction arises purely from RL training with interpreter feedback — models learn to detect, diagnose, and repair code errors mid-trajectory without any curated self-correction demonstrations in training data

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/retool|ReTool]]
- [[entities/tool-integrated-reasoning|Tool-Integrated Reasoning]]
- [[entities/verl|verl]]
