---
type: source
title: 'START: Self-taught Reasoner with Tools'
source_id: 01KJV3G6RYWC5JM8X47AK9AAGE
source_type: paper
authors:
- Chengpeng Li
- Mingfeng Xue
- Zhenru Zhang
- Jiaxi Yang
- Beichen Zhang
- Xiang Wang
- Bowen Yu
- Binyuan Hui
- Junyang Lin
- Dayiheng Liu
published_at: '2025-03-06 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# START: Self-taught Reasoner with Tools

**Authors:** Chengpeng Li, Mingfeng Xue, Zhenru Zhang, Jiaxi Yang, Beichen Zhang, Xiang Wang, Bowen Yu, Binyuan Hui, Junyang Lin, Dayiheng Liu
**Published:** 2025-03-06 00:00:00
**Type:** paper

## Analysis

# START: Self-taught Reasoner with Tools
2025-03-06 · paper · Chengpeng Li, Mingfeng Xue, Zhenru Zhang, Jiaxi Yang, Beichen Zhang et al. (10 total)
https://arxiv.org/pdf/2503.04625

---

### Motivation & Prior Limitations
- Large reasoning models (LRMs) like OpenAI-o1 and DeepSeek-R1 achieve strong performance through long Chain-of-Thought (CoT), but suffer from hallucinations and computational inaccuracies because they rely exclusively on internal reasoning with no access to external verification or execution.
  - On hard LiveCodeBench problems, QwQ-32B-Preview hallucinates during complex test case analysis, producing flawed solutions that a code interpreter would immediately catch.
  - QwQ-RFT (training on the same data without tools) achieves performance nearly identical to QwQ-32B-Preview, confirming that the performance ceiling is a structural limitation of pure CoT, not a data insufficiency.
- Naïve approaches to combining long CoT with tool-integrated reasoning (TIR) fail entirely: direct prompting, well-designed system prompts, and in-context examples all fail to induce QwQ-32B-Preview or DeepSeek-R1 to invoke a Python interpreter during long CoT inference.
  - The likely cause is that LRMs trained for complex reasoning lose general instruction-following ability, making prompt-based tool activation ineffective.
- Synthesis of high-quality training trajectories containing Python interpreter calls within long CoT reasoning chains was an unsolved data-generation problem prior to this work.

---

### Proposed Approach
- The paper introduces START (Self-Taught Reasoner with Tools), a two-phase self-learning framework — Hint-RFT followed by RFT — that fine-tunes QwQ-32B-Preview to autonomously invoke a Python code interpreter within long CoT reasoning without requiring any human-demonstration data.
- **Hint-infer** circumvents the prompt-following failure of LRMs by injecting short, pre-designed natural-language hints directly into the model's generation stream at critical junctures — after high-frequency introspective conjunctions like "Alternatively" and "Wait," or immediately before the stop token — which activates latent tool-use capabilities the model already possesses but cannot self-trigger.
  - A Hint-Library provides domain-specific hints: for math, these cover complex calculations, self-reflection, logic checks, and alternative methods; for code, a "Debug hint" with a code template prompts the model to run candidate code against test cases before finalizing answers.
  - Inserting hints before the stop token repeatedly creates a sequential test-time scaling effect: each additional hint-inference round extends thinking time and raises solve rates on competition math benchmarks.
- **Hint-RFT** uses Hint-infer as a data-synthesis engine: greedy and hint-augmented inference are run on all training problems, and trajectories where Hint-infer succeeds but greedy inference fails are retained as seed data (Dseed: 10K math + 2K code problems), filtered for repetition, and used to fine-tune QwQ-32B-Preview into START-0.
  - This constitutes an active-learning selection strategy — only problems at the boundary of the model's capability (unsolvable without tools, solvable with them) are included, maximizing training signal per example.
- **RFT phase**: START-0 is then used to run 16 rounds of temperature-0.6/top-p-0.95 sampling across all 50K training problems, producing a larger, more diverse dataset DSTART (40K math + 10K code) for a final fine-tuning pass that yields START.
  - This self-distillation loop diversifies tool-use patterns without any external data source.

---

### Results & Capabilities
- START achieves state-of-the-art performance among open-weight 32B models across all evaluated benchmarks, matching or exceeding models distilled from much larger systems.
  - GPQA (PhD-level science QA): 63.6%, a +5.5pp absolute gain over QwQ-32B-Preview and matching Search-o1-32B; strongest on Physics (+6.2pp over QwQ), where computation dominates over knowledge recall.
  - AMC23: 95.0% (+15.0pp over QwQ-32B-Preview), AIME24: 66.7% (+16.7pp), AIME25: 47.1% (+7.1pp), MATH500: 94.4% (+3.8pp) — comparable to R1-Distill-Qwen-32B, which is distilled from the 671B DeepSeek-R1.
  - LiveCodeBench: 47.3% (+5.9pp), with the largest gain on medium-difficulty problems (46.0% → 84.6%), confirming that tool-assisted self-debugging is most impactful in the regime where the model can generate plausible but buggy code.
- The ablation (QwQ-RFT vs. START) isolates tool invocation as the primary driver of gains: QwQ-RFT improves only marginally over QwQ-32B-Preview (e.g., AIME24: 53.3% vs. 50.0%), while START reaches 66.7%, demonstrating that the tool capability — not additional training data — is responsible for the bulk of improvement.
- Hint-infer alone (without fine-tuning) also improves QwQ-32B-Preview across all benchmarks, functioning as a zero-shot test-time scaling method, though gains are substantially smaller than after Hint-RFT fine-tuning.
- START outperforms o1-preview on math benchmarks (AIME24: 66.7% vs. 44.6%; AMC23: 95.0% vs. 81.8%) while remaining below o1 and o3-mini on most tasks.

---

### Implications
- Hint-infer demonstrates that LRMs already contain latent tool-use capabilities that standard prompting cannot access — structured inference-time interventions can unlock these capabilities without any labeled data, suggesting that capability elicitation at inference time is a tractable alternative to full fine-tuning.
- The self-taught loop (Hint-infer → seed data → SFT → RFT) establishes a viable template for bootstrapping tool-integrated reasoning from a pure-CoT LRM using only outcome-verified trajectories, with no human demonstrations — directly relevant to scalable self-improvement and expert iteration in reasoning domains.
- The strong separation between Physics (computation-heavy, benefits from Python) and Biology (knowledge-heavy, benefits from search) in GPQA results suggests

## Key Claims

1. Large reasoning models like OpenAI-o1 and DeepSeek-R1 suffer from hallucinations and inefficiencies due to their reliance solely on internal reasoning processes.
2. Inserting artificially designed hints (e.g., 'Wait, maybe using Python here is a good idea.') during inference of a LRM effectively stimulates its ability to utilize external tools without requiring a
3. Hint-infer can serve as a simple and effective sequential test-time scaling method for large reasoning models.
4. Direct prompting, well-designed prompting, and in-context prompting all failed to get QwQ-32B-Preview and DeepSeek-R1 to invoke Python tools during long CoT on AIME24 and LiveCodeBench.
5. For mathematical tasks, inserting basic hints with Python identifiers enables the LLM to write appropriate code, while coding generation tasks require carefully designed hints and code templates to ac
6. When hints are inserted before the stop token of long CoT, the model exhibits a sequential test-time scaling effect where increased thinking time correlates with higher problem-solving success rate.
7. Hints are strategically inserted after specific high-frequency conjunction tokens such as 'Alternatively' and 'Wait', as these tokens typically indicate the model is questioning its own reasoning or c
8. START achieves 63.6% on GPQA (PhD-level science QA), representing a +5.5% absolute improvement over QwQ-32B-Preview.
9. START achieves 95.0% on AMC23, a +15.0% absolute improvement over QwQ-32B-Preview.
10. START achieves 66.7% on AIME24, a +16.7% absolute improvement over QwQ-32B-Preview.

## Capabilities

- Tool-integrated long chain-of-thought reasoning (Long TIR): a 32B open-weight LRM can synergize extended CoT with Python code execution, enabling complex computation verification, iterative self-debugging, and multi-method exploration during a single reasoning chain
- Hint-infer enables sequential test-time scaling for LRMs: inserting hints before the stop token repeatedly extends thinking time and monotonically improves problem-solving accuracy on competition-level math benchmarks without weight updates
- Self-training via Hint-RFT enables a large reasoning model to bootstrap tool-use capabilities using only self-generated trajectories — no human demonstration data required — through hint injection at inference followed by rejection sampling fine-tuning
- Iterative code interpreter integration during long CoT enables detect-debug-correct loops, resolving complex test-case analysis failures where pure internal reasoning consistently hallucinates
- Fine-tuned 32B open-weight LRM achieves 95.0% on AMC23, 66.7% on AIME24, and 47.1% on AIME25 — matching models distilled from 671B DeepSeek-R1 and surpassing o1-preview on math benchmarks, at 32B parameter scale

## Limitations

- LRMs trained via RL for complex reasoning lose generalized instruction-following — standard prompting, in-context examples, and structured prompt strategies all fail to activate tool use during long CoT, even on QwQ-32B-Preview and DeepSeek-R1
- Tool-integrated reasoning is domain-selective: biology and knowledge-retrieval tasks see negligible benefit from Python tool integration, while computation-heavy domains (physics, math) benefit strongly — revealing a structural gap for non-computational reasoning
- Hard coding problems remain largely unsolvable even with iterative tool-integrated debugging: START achieves only 12.2% on LiveCodeBench hard (up from 10.2% for base QwQ) — a near-flat ceiling that limited tool invocations cannot overcome
- Sequential test-time scaling via hint injection degrades on fine-tuned models — Hint-infer works substantially less effectively on START than on base QwQ-32B-Preview because fine-tuning internalizes hint patterns, collapsing the information gain from added hints
- START is restricted to a single external tool (Python interpreter); no search engines, knowledge bases, or specialized domain APIs are integrated, limiting reasoning assistance for non-computational tasks
- Manual hint library design is brittle — optimal hint type and placement varies by task and context; poorly positioned hints disrupt the model's original reasoning flow and there are no principled selection criteria
- Generalizability of START beyond math, code, and GPQA benchmarks is entirely unestablished — performance on broader or more diverse task distributions is unknown
- Training data covers only math and code domains (50K problems total); no coverage of biology, general science, social reasoning, or open-ended tasks — systematic domain bias baked into the model
- Tool invocations are hard-capped at 6 per inference, creating a hard ceiling on iterative debugging depth achievable during a single reasoning chain
- No real-world deployment, latency, cost, or safety evaluation is reported — all results are benchmark-only with no assessment of operational viability or adversarial robustness in production settings
- Adding more CoT training data without tool invocation (QwQ-RFT) yields negligible performance gains — pure self-training on reasoning chains hits a data wall and cannot overcome hallucination on complex computations

## Bottlenecks

- RL-trained LRMs systematically lose instruction-following generalization — standard prompting and in-context learning consistently fail to activate tool use during long CoT, blocking tool-integrated reasoning without special hint-injection or fine-tuning interventions
- Synthesizing training data containing tool invocations embedded inside long CoT is fundamentally hard — direct prompting, in-context learning, and structured prompt strategies all fail to elicit tool use in existing LRMs, creating a data bootstrap problem that requires special apparatus to break

## Breakthroughs

- Hint-RFT: a self-training framework that bootstraps tool-use in LRMs entirely from self-generated trajectories via inference-time hint injection — without any human demonstration data, curated tool-use examples, or modified training objectives
- Code execution grounded in long CoT eliminates a class of computational hallucinations in LRMs that pure self-training cannot address — verified interpreter output replaces unreliable internal simulation at any reasoning step

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/gpqa|GPQA]]
- [[entities/math500|MATH500]]
- [[entities/pass1|Pass@1]]
- [[entities/qwq-32b-preview|QwQ-32B-Preview]]
- [[entities/tool-integrated-reasoning-tir|Tool-Integrated Reasoning (TIR)]]
- [[entities/sequential-test-time-scaling|sequential test-time scaling]]
