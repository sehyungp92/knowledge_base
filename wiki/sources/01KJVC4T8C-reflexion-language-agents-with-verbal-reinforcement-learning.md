---
type: source
title: 'Reflexion: Language Agents with Verbal Reinforcement Learning'
source_id: 01KJVC4T8CE55S82GE0X2ZHAMB
source_type: paper
authors:
- Noah Shinn
- Federico Cassano
- Edward Berman
- Ashwin Gopinath
- Karthik Narasimhan
- Shunyu Yao
published_at: '2023-03-20 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reflexion: Language Agents with Verbal Reinforcement Learning

**Authors:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Published:** 2023-03-20 00:00:00
**Type:** paper

## Analysis

# Reflexion: Language Agents with Verbal Reinforcement Learning
2023-03-20 · paper · Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan et al. (6 total)
https://arxiv.org/pdf/2303.11366

---

### Motivation & Prior Limitations
- LLM-based agents interacting with external environments (games, compilers, APIs) cannot efficiently learn from trial-and-error because traditional RL requires extensive training samples and expensive model fine-tuning, making weight updates impractical for agents built on massive pretrained models.
  - Prior agents like ReAct, SayCan, Toolformer, and WebGPT are limited to in-context learning as their only adaptation mechanism — they have no mechanism to carry forward lessons from failures across episodes.
  - Scalar and vector rewards in traditional RL are difficult to perform accurate credit assignment with in semantic action spaces, and existing approaches like Self-Refine are limited to single-generation tasks without multi-step decision-making or persistent memory.
- Code generation approaches such as AlphaCode, Self-Debugging, and CodeRL rely on ground truth test cases (disqualifying pass@1 reporting) and do not use self-reflection to bridge error identification and implementation improvement; CodeT uses self-generated tests but lacks an iterative self-learning step.

---

### Proposed Approach
- Reflexion introduces verbal reinforcement learning: instead of updating model weights, it converts task feedback (binary, scalar, or free-form) into natural language reflections that are stored in an episodic memory buffer and injected as additional context in subsequent trials, acting as a "semantic gradient signal."
  - The framework is modular, comprising three LLM-based components: an **Actor** (generates actions/text via policy πθ), an **Evaluator** (scores trajectories to produce a reward signal), and a **Self-Reflection model** (transforms the reward + trajectory into a nuanced verbal summary of mistakes and corrective strategies).
  - Memory is split into **short-term** (the current trajectory) and **long-term** (accumulated self-reflections, bounded by a sliding window of 1–3 experiences to respect context limits), mirroring the human distinction between fine-grained recent recall and distilled experiential knowledge.
  - Evaluator variants are task-specific: exact-match grading for reasoning, hand-coded heuristics or LLM-as-judge for decision-making, and self-generated unit test suites (filtered via AST validation, capped at 6 tests) for programming — enabling pass@1-eligible evaluation without ground-truth tests.
  - For programming, Chain-of-Thought prompting generates diverse unit tests whose results gate whether the agent self-reflects or exits early, making false negatives (failing tests on correct code) preferable to false positives (passing tests on incorrect code).

---

### Results & Capabilities
- Reflexion achieves **91% pass@1 on HumanEval (Python)**, surpassing the prior state of the art of 80.1% (GPT-4) — an absolute improvement of ~11 percentage points — using GPT-4 as the base Actor with self-generated test suites and verbal self-reflection.
  - On HumanEval Rust (hardest 50 problems), Reflexion reaches 68% vs. GPT-4's 60% baseline; on MBPP Python it reaches 77.1% (slightly below GPT-4's 80.1% due to high false-positive test rates of 16.3% causing premature stopping on incorrect solutions); on Leetcode Hard Python it doubles GPT-4's performance from 7.5% to 15.0%.
- On sequential decision-making (AlfWorld, 134 tasks), ReAct + Reflexion with a simple heuristic evaluator completes 130/134 tasks, outperforming ReAct-only by 22% absolute over 12 iterative trials; ReAct-only converges and stalls between trials 6 and 7 with a persistent 22% hallucination rate.
  - Self-reflection eliminates almost all hallucination failure modes (where agents falsely believe they possess an item) by distilling long failed trajectories into actionable "self-hints" that prevent the same mistake in future trials.
- On knowledge-intensive reasoning (HotPotQA, 100 questions), Reflexion improves CoT and ReAct baselines by up to 20% absolute; baseline CoT-only, ReAct-only, and CoT (GT)-only agents fail to probabilistically improve any tasks across subsequent trials at temperature 0.7, while Reflexion systematically recovers from failures.
  - An ablation isolating the self-reflection step from mere episodic memory replay (including the last trajectory without verbal analysis) shows self-reflection contributes an additional 8% absolute accuracy gain, demonstrating that verbal first-person explanation — not just retry with prior context — is the key mechanism.
- An ablation on HumanEval Rust shows that omitting test generation drops performance to 52% (below 60% baseline), and omitting self-reflection (keeping tests) leaves performance at 60% baseline — both components are necessary, and neither alone is sufficient, refuting blind trial-and-error debugging approaches for complex tasks.

---

### Implications
- Reflexion demonstrates that **test-time compute spent on iterative linguistic self-correction** is a viable alternative to gradient-based learning for adapting LLM agents — the policy is effectively encoded in natural language memory rather than model weights, suggesting a new design axis for capable agents without fine-tuning infrastructure.
- The framework formalizes a **verbal RL paradigm** where the policy is parameterized as {LLM, memory encoding}, pointing toward future work integrating richer memory structures (vector databases, SQL), value learning in natural language, and off-policy exploration — bridging LLM agent design and formal RL theory.
- Reflexion's interpretability advantage over traditional RL is practically significant for alignment: self-reflections are human-readable, auditable artifacts that can be monitored for intent before tool use, offering a concrete path toward more diagnosable autonomous agents in high-stak

## Key Claims

1. Reflexion achieves 91% pass@1 accuracy on HumanEval, surpassing the previous state-of-the-art GPT-4 which achieves 80%.
2. Traditional reinforcement learning methods require extensive training samples and expensive model fine-tuning, limiting their use for language agents.
3. Reflexion reinforces language agents through linguistic feedback rather than weight updates, maintaining reflective text in an episodic memory buffer.
4. Reflexion converts binary or scalar environment feedback into verbal feedback (textual summary) that acts as a semantic gradient signal for the agent.
5. Reflexion improves AlfWorld decision-making performance by an absolute 22% over strong baseline approaches in 12 iterative learning steps.
6. Reflexion improves HotPotQA reasoning performance by 20% over baseline approaches.
7. Reflexion is lightweight and does not require fine-tuning the LLM, unlike traditional RL approaches.
8. Reflexion allows for more nuanced forms of feedback (targeted changes in actions) compared to scalar or vector rewards that are challenging for accurate credit assignment.
9. Reflexion provides a more explicit and interpretable form of episodic memory over prior experiences and more explicit hints for actions in future episodes.
10. Reflexion has the disadvantage of relying on the LLM's self-evaluation capabilities and lacks a formal guarantee for success.

## Capabilities

- LLM agents can iteratively improve task performance through verbal self-reflection stored in episodic memory, without any gradient updates or model fine-tuning — achieving rapid adaptation across decision-making, reasoning, and coding tasks in a handful of trials
- Reflexion-augmented LLM achieves 91% pass@1 on HumanEval — surpassing GPT-4's prior 80% SOTA without any weight updates, using self-generated unit tests and verbal self-reflection for iterative code improvement
- LLMs can generate and execute their own unit test suites to evaluate code correctness, enabling self-supervised evaluation and pass@1-eligible reinforcement loops without ground-truth test access
- Sparse binary environment rewards can be amplified into nuanced natural-language feedback that enables LLM agents to perform verbal credit assignment across long multi-step trajectories
- ReAct agents augmented with verbal self-reflection achieve near-perfect performance (130/134 tasks) on AlfWorld multi-step household environments — a 22% absolute improvement over non-reflective baselines across 12 iterative trials

## Limitations

- Verbal policy optimization can converge to non-optimal local minima — self-reflection does not guarantee escape from suboptimal strategies and provides no formal convergence proof
- Long-term memory is hard-bounded by context window capacity, limiting stored reflections to 1–3 experiences — the agent cannot accumulate knowledge across more trials than fit in a single context
- Self-evaluation quality is a hard prerequisite — Reflexion's effectiveness is entirely contingent on the LLM's ability to accurately identify its own errors; the system provides no formal guarantee for success
- False-positive test suites cause Reflexion to prematurely halt on incorrect code — when LLM-generated unit tests pass an incorrect implementation, the agent terminates without further improvement; this explains underperformance on MBPP Python (77.1% vs GPT-4 baseline 80.1%)
- Reflexion without grounded test execution degrades below baseline — omitting internal test generation drops HumanEval Rust pass@1 from 60% (baseline) to 52%, showing that verbal self-reflection without a reliable evaluation signal actively harms performance
- Test-driven self-evaluation is inapplicable to large classes of real-world programs — non-deterministic generators, API-dependent functions, hardware-specific outputs, and concurrent programs cannot be reliably tested by self-generated unit tests
- Autonomous code execution proceeds without any safety validation — generated code runs directly in environments without sandboxing, static analysis, or human review, creating a security attack surface
- Non-reflective LLM baselines (CoT, ReAct) show zero probabilistic improvement across repeated trials — without verbal self-reflection, repeated sampling at temperature 0.7 cannot solve tasks that failed in the first attempt
- ReAct agents without reflection converge at a stable 22% hallucination rate on AlfWorld with no long-term recovery — incorrect object possession beliefs compound in long trajectories and cannot be self-corrected across trials
- Verbal credit assignment across long multi-step trajectories is fundamentally challenging — identifying which specific action in a trajectory caused downstream failure requires causal reasoning that the LLM may fail to perform accurately
- Reflexion experiments are conducted exclusively in text-based and code execution environments — generalisation to visual, embodied, or continuous-state environments is entirely undemonstrated

## Bottlenecks

- Verbal credit assignment from sparse binary rewards across long trajectories remains unsolved — Reflexion provides a practical heuristic, but it relies on LLM judgment rather than principled attribution and degrades when the model's self-assessment of causal responsibility is wrong
- Agent episodic memory is hard-bounded by LLM context window size — Reflexion is limited to 1–3 stored experiences, preventing accumulation of knowledge across more than a small number of trial episodes
- Reliable automatic code correctness evaluation without ground-truth tests is unsolved — LLM-generated test suites have meaningful false positive rates (16.3% on MBPP Python) that can mislead agents into accepting incorrect solutions and terminating improvement early

## Breakthroughs

- Reflexion demonstrates that LLM agents can exceed gradient-trained and fine-tuned model performance through purely verbal reinforcement — iterative self-reflection stored in episodic memory constitutes gradient-free policy improvement, achieving new SOTA on HumanEval (91% vs GPT-4's 80%) without any

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/credit-assignment-problem|Credit Assignment Problem]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/pass1|Pass@1]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/self-refine|Self-Refine]]
