---
type: source
title: 'ToRL: Scaling Tool-Integrated RL'
source_id: 01KJV1PA03Z4FFHSTXB56B2R02
source_type: paper
authors:
- Xuefeng Li
- Haoyang Zou
- Pengfei Liu
published_at: '2025-03-30 00:00:00'
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
# ToRL: Scaling Tool-Integrated RL

**Authors:** Xuefeng Li, Haoyang Zou, Pengfei Liu
**Published:** 2025-03-30 00:00:00
**Type:** paper

## Analysis

# ToRL: Scaling Tool-Integrated RL
2025-03-30 · paper · Xuefeng Li, Haoyang Zou, Pengfei Liu
https://arxiv.org/pdf/2503.23383

---

### Motivation & Prior Limitations
Existing Tool-Integrated Reasoning (TIR) approaches are constrained by their reliance on Supervised Fine-Tuning (SFT) on trajectories distilled from stronger models, which restricts models to predetermined tool usage patterns and limits exploration of optimal strategies.
- Pure Chain-of-Thought reasoning falters on complex calculations, equation solving, and tasks requiring precise computation — the very problems where tool integration would be most valuable.
  - This gap persists despite prior TIR work (ToRA, MathCoder, Qwen2.5-Math-Instruct-TIR), all of which rely on SFT or apply RL only on top of already-SFT-trained models.
- Applying RL post-SFT means the model begins exploration from a narrow, human-prescribed distribution of tool use patterns rather than discovering strategies from scratch.
  - Qwen-Math applies RL to SFT-trained models but with limited implementation transparency, obscuring understanding of tool integration dynamics within RL.

---

### Proposed Approach
TORL (Tool-Integrated Reinforcement Learning) trains models to autonomously discover tool utilization strategies by applying RL directly to base models — without any prior supervised fine-tuning — integrating a code interpreter into the RL environment's rollout loop.
- The TIR rollout framework intercepts a special code termination token (`'''output`) during generation, pauses text generation, executes the extracted code block in an isolated sandbox, injects the result as structured context, and then resumes generation — enabling iterative reasoning informed by real execution outputs.
  - This differs from SFT-based TIR by making the discovery of when and how to invoke tools entirely reward-driven rather than imitation-based.
- Four key engineering choices shape the framework: (1) a hyperparameter C capping tool calls per response to bound GPU idle time from interpreter latency; (2) Sandbox Fusion as the isolated execution environment (over qwen-agent's executor) to prevent segfaults from corrupting the training process; (3) stripping verbose tracebacks to the final error line to limit context bloat; (4) masking sandbox OBSERVATION outputs during loss computation to prevent the model from memorizing specific execution outputs rather than learning generalizable reasoning.
- The reward function uses a simple binary scheme: +1 for correct answers, −1 for incorrect, with an optional −0.5 penalty for non-executable code (though this penalty is omitted from the primary experiments after ablation showed it harms performance by incentivizing overly simple code).
- Training uses GRPO, rolls out 128 problems with 16 samples each, omits KL loss, and sets temperature to 1 to maximize exploration — all applied to Qwen2.5-Math base models at 1.5B and 7B scales.

---

### Results & Capabilities
TORL-7B achieves 43.3% accuracy on AIME24, surpassing RL-trained models without tool integration by ~10 percentage points and the best existing TIR model (Qwen2.5-Math-7B-Instruct-TIR at 26.7%) by ~16 points.
- Across five benchmarks (AIME24, AIME25, MATH500, OlympiadBench, AMC23), TORL-7B averages 62.1% — a 14.7% absolute improvement over the next best comparable model — and TORL-1.5B averages 48.5%, a 7.2% gain.
  - On AIME25, TORL-7B reaches 30.0% vs. 16.7% for the TIR baseline, showing the gains are not benchmark-specific.
  - TORL-7B at 7B parameters achieves accuracy comparable to some 32B RL-trained models.
- Training dynamics reveal three emergent cognitive behaviors that arise without explicit instruction, solely from reward signal: (1) strategic tool invocation — code usage in responses grows from ~40% to ~80% within the first 100 steps; (2) self-regulation of ineffective code — the model progressively reduces generation of code that is either never executed or generated only after the final answer; (3) dynamic cross-validation — the model detects inconsistencies between analytical and computational results and re-engages the interpreter to resolve them.
  - The correlation between code execution success and answer correctness strengthens over training: correct responses exhibit substantially higher code pass rates than incorrect ones.
- Increasing C from 1 to 2 (allowing two tool calls per response) yields approximately 2% additional average accuracy, confirming that more reasoning-tool cycles improve problem-solving depth.

---

### Implications
The finding that rich tool-use strategies emerge from base models via pure reward signal — without any SFT warm-up — strengthens the case that RL scaling from scratch is a viable and potentially superior pathway for acquiring complex cognitive skills, challenging the assumption that SFT bootstrapping is necessary.
- The emergent cross-validation behavior (using code to check natural language reasoning and vice versa) resembles a form of metacognition and suggests that multi-modal reasoning integration may be a natural attractor under reward-driven learning, not something requiring explicit architectural engineering.
- For the program synthesis and code generation themes, TORL demonstrates that correctness-only reward is sufficient to drive syntactic quality improvements — the model learns to write executable, semantically meaningful code as an instrumental goal, not a directly rewarded one.
- The efficiency–effectiveness trade-off revealed by varying C (doubling step time from 118s to 288s when going from C=0 to C=2) establishes a concrete scaling dimension for test-time compute in tool-augmented settings: more tool calls improve accuracy but at superlinear cost, making this a key variable for deployment-time compute allocation.

---

### Remaining Limitations & Next Steps
The evaluation is entirely restricted to mathematical problem-solving benchmarks (AIME, MATH500, OlympiadBench, AMC23), leaving open whether TORL's eme

## Key Claims

1. TORL-7B achieves 43.3% accuracy on AIME24, surpassing RL without tool integration by 14% and the best existing Tool-Integrated Reasoning model by 17%.
2. Traditional Chain-of-Thought reasoning methods fail on complex calculations, equation solving, or processes requiring precise computation.
3. Existing TIR approaches based on supervised fine-tuning restrict models to predetermined tool usage patterns and limit exploration of optimal strategies.
4. TORL enables RL training directly from base models without prior supervised fine-tuning, yielding qualitatively different behaviors than methods building upon predetermined patterns.
5. TORL-7B achieves 43.3% accuracy on AIME problems, comparable to some 32B models trained with reinforcement learning.
6. As TORL training progresses, the proportion of problems solved using code increases steadily, along with a growing percentage of syntactically correct and executable code.
7. Without explicit instruction, TORL-trained models learn to identify and reduce the generation of ineffective code patterns, suggesting an emerging form of metacognition about tool utility.
8. Increasing the maximum allowed tool calls per problem significantly enhances performance but introduces severe computational overhead.
9. The TORL training dataset consists of 28,740 high-quality verifiable mathematical questions derived from Olympic-level competition problems after filtering and difficulty balancing.
10. In TORL's TIR rollout, error messages from failed code execution are deliberately returned to the LLM to enhance its capacity to generate syntactically and semantically correct code in subsequent iter

## Capabilities

- Reinforcement learning directly from base models (without SFT) can train LLMs to autonomously discover and use computational tools (code interpreters) for mathematical reasoning, achieving 43.3% on AIME24 with a 7B model — surpassing SFT+RL and RL-only baselines
- LLMs trained with tool-integrated RL develop emergent metacognitive behaviors — self-regulating ineffective code generation and cross-validating computational outputs against analytical reasoning — without explicit instruction
- Tool-Integrated Reasoning (TIR) enables LLMs to iteratively generate code, execute it, and adjust reasoning based on execution outputs — correcting indexing errors, verifying intermediate results, and improving accuracy on numerical computation tasks
- RL-trained models spontaneously develop cross-checking behavior — solving problems analytically, verifying via code execution, detecting inconsistencies between the two, and correcting reasoning accordingly

## Limitations

- Tool call execution during RL rollouts introduces severe GPU idle time — rollout speed is inversely proportional to tool call frequency, with a single allowed tool call doubling per-step training time (118s → 237s on 8×A800)
- Increasing the tool call budget (C) improves accuracy but nearly doubles or more training step time — creating a hard efficiency-effectiveness trade-off that severely constrains practical scaling of tool call depth
- TORL is evaluated exclusively on mathematical benchmarks — no demonstration across other reasoning domains (coding, scientific reasoning, general QA), leaving generalizability entirely unaddressed
- RL from base models for tool-integrated reasoning requires verifiable, closed-form answers — proof-based problems and questions with ambiguous verification criteria are excluded, sharply limiting the training distribution
- Pure chain-of-thought reasoning systematically fails on tasks requiring precise computation, equation solving, or exhaustive enumeration — arithmetic errors accumulate through token-level pattern matching
- Adding a code executability penalty to the RLVR reward function does not improve performance — may actively harm it by incentivizing overly simplistic code that avoids errors but cannot solve hard problems
- Unsafe code interpreter implementations (without sandbox isolation) risk compromising entire training runs via segfaults and illegal memory access — requiring isolated sandboxed environments that add latency overhead
- When the per-response tool call budget C is exhausted mid-reasoning, the model is forced to switch to pure text reasoning — creating a hard performance cliff where problems requiring more than C computational steps degrade abruptly
- TORL experiments are limited to 1.5B and 7B parameter models — no evidence of tool-integrated RL scaling behavior at 32B+ scale, emergent behavior persistence, or whether the efficiency-effectiveness trade-off worsens at scale
- SFT-based tool integration restricts models to the distribution of trajectories distilled from stronger models, preventing discovery of tool-use strategies that differ qualitatively from human-designed patterns

## Bottlenecks

- Code execution latency during RL rollouts creates prohibitive training inefficiency — each tool call synchronization point doubles or more per-step training time, blocking scaling of tool-integrated RL to multi-call, long-horizon reasoning chains
- Verifiable reward requirement confines tool-integrated RL to closed-form mathematical domains — the absence of auto-verifiable rewards for open-ended tasks blocks generalization of TORL-style training beyond math benchmarks

## Breakthroughs

- Tool-integrated reasoning capabilities — strategic tool invocation, self-regulation of ineffective code, cross-validation between computational and analytical modes — can emerge from RL on base models without any supervised fine-tuning initialization

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/grpo|GRPO]]
- [[entities/math500|MATH500]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/tool-integrated-reasoning-tir|Tool-Integrated Reasoning (TIR)]]
- [[entities/verl|veRL]]
