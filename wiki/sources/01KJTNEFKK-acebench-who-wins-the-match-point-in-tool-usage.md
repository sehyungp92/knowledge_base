---
type: source
title: 'ACEBench: Who Wins the Match Point in Tool Usage?'
source_id: 01KJTNEFKKKGT5BEWNG2W426MV
source_type: paper
authors:
- Chen Chen
- Xinlong Hao
- Weiwen Liu
- Xu Huang
- Xingshan Zeng
- Shuai Yu
- Dexun Li
- Shuai Wang
- Weinan Gan
- Yuefeng Huang
- Wulong Liu
- Xinzhi Wang
- Defu Lian
- Baoqun Yin
- Yasheng Wang
- Wu Liu
published_at: '2025-01-22 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- benchmark_design
- evaluation_and_benchmarks
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ACEBench: Who Wins the Match Point in Tool Usage?

**Authors:** Chen Chen, Xinlong Hao, Weiwen Liu, Xu Huang, Xingshan Zeng, Shuai Yu, Dexun Li, Shuai Wang, Weinan Gan, Yuefeng Huang, Wulong Liu, Xinzhi Wang, Defu Lian, Baoqun Yin, Yasheng Wang, Wu Liu
**Published:** 2025-01-22 00:00:00
**Type:** paper

## Analysis

# ACEBench: Who Wins the Match Point in Tool Usage?
2025-01-22 00:00:00 · paper · Chen Chen, Xinlong Hao, Weiwen Liu, Xu Huang, Xingshan Zeng et al. (16 total)
https://arxiv.org/pdf/2501.12851

---

### Motivation & Prior Limitations
- Existing tool-use benchmarks lack evaluation of real multi-turn dialogue contexts, relying instead on predefined fixed content combinations that fail to capture dynamic, adaptive real-world interactions.
  - BFCL and HammerBench both construct multi-turn dialogues by concatenating pre-defined content, not simulating genuine conversational dynamics.
  - τ-Bench covers only two narrow scenarios, limiting generalizability.
- Current benchmarks provide insufficient fine-grained evaluation dimensions, omitting assessment of imperfect or incomplete user instructions despite these being common in real-world tool use.
  - Most benchmarks (ToolBench, API-Bank, Stable ToolBench) ignore special cases such as missing parameters, malformed inputs, or task-function mismatches entirely.
- Evaluation costs are high because many benchmarks rely on advanced LLMs or live API calls for scoring, introducing overhead and instability.
  - Stable ToolBench employs a virtual API server but still depends on large models for evaluation, creating cost and scalability challenges.

---

### Proposed Approach
- ACEBench introduces a comprehensive, LLM-free, automated tool-use benchmark with three evaluation categories — Normal, Special, and Agent — covering the full spectrum from basic single-turn calls to dynamic multi-turn agent interactions.
  - Normal data covers single-turn, multi-turn, similar-API disambiguation, personalization, and atomic-level capability subcategories, evaluated via AST parsing against ground truth without LLM judges.
  - Special data explicitly tests robustness to imperfect instructions: incomplete parameters, incorrectly formatted parameters, and task-function mismatches, scored by whether the model correctly identifies the defect.
  - Agent data uses expert-constructed sandbox environments with standardized functional interfaces, dynamic state management, and execution monitoring to simulate real-world multi-step, multi-turn interactions; GPT-4o serves as a user simulator during evaluation.
- The dataset construction pipeline combines LLM-based self-evolving API synthesis (a hierarchical API context tree covering 8 major domains and 4,538 APIs in Chinese and English) with multi-stage human and automated quality verification across 2,000 annotated entries.
  - Normal and Special data are auto-generated using graph-based sampling and multi-agent dialogue pipelines; Agent data is hand-crafted by domain experts to ensure scenario fidelity.

---

### Results & Capabilities
- Closed-source models dominate overall performance, with GPT-4o achieving the highest overall score of 85.4%, followed by GPT-4-Turbo at 84.5%, while open-source models like Qwen2.5-Coder-32B-Instruct (79.6%) and DeepSeek-V3 (74.8%) are narrowing the gap.
  - The performance gap between top open-source and closed-source models is shrinking, driven by advances in model architecture and training.
- Tool-learning fine-tuned models (Watt-Tool-8B, xLAM-7B-r, Hammer2.1-7B) show significant generalization loss on Special data despite strong Normal performance, with xLAM-7B-r scoring only 1–4% across the three Special subcategories.
  - This reveals a critical trade-off: fine-tuning on specific tool-use datasets improves narrow task performance but degrades robustness to imperfect or novel instructions.
- Agent tasks expose a hard ceiling for all models: most achieve end-to-end accuracy below 50% on multi-turn Agent tasks, with GPT-4-Turbo leading at 50.0% end accuracy and 66.0% process accuracy for multi-turn, and 85.0%/89.5% for multi-step.
  - Multi-turn performance is substantially harder than multi-step, as it requires maintaining consistency over dynamic user interactions rather than sequential tool chaining.
- The dominant error type on Normal data is parameter value error (~59–66% of errors across model families), followed by output format error (~8–20%), while function name and parameter type errors are rare, indicating models handle function matching well but struggle with value generation.
- Scaling improves performance substantially but with diminishing returns: performance gains slow between 32B and 72B in the Qwen2.5-Instruct series, suggesting marginal benefits decrease at larger scales.
- Prompt standardization positively correlates with accuracy: standard prompts outperform condensed and minimal prompts across all tested Qwen2.5-Instruct sizes, with the gap widening at smaller model scales.

---

### Implications
- The generalization failure of fine-tuned tool-use models on Special data challenges the prevailing assumption that task-specific fine-tuning is straightforwardly beneficial, suggesting that robustness to imperfect real-world instructions requires deliberate training data design, not just more tool-use examples.
- The near-universal sub-50% end-to-end accuracy on multi-turn Agent tasks signals that dynamic multi-turn tool orchestration remains a fundamental unsolved capability for current LLMs, constituting a meaningful bottleneck for autonomous agent deployment.
- The LLM-free, sandbox-based evaluation methodology demonstrates that comprehensive tool-use assessment can be made cost-efficient and scalable without sacrificing evaluation depth, pointing toward a viable design pattern for future agentic benchmarks.
- The benchmark's explicit coverage of robustness to imperfect instructions (Special category) highlights a gap in how the field measures dialogue and assistant quality — real users rarely issue perfect, complete commands, yet most benchmarks assume they do.

---

### Remaining Limitations & Next Steps
- The Normal and Special evaluation data is synthetically generated by LLMs, and despite quality verification measures, a gap remains compared to data sourced from rea

## Key Claims

1. Existing tool-use benchmarks lack multi-turn dialogue evaluation in real-world scenarios, with multi-turn dialogues in BFCL and HammerBench composed of predefined fixed content combinations rather tha
2. Current tool-use benchmarks lack fine-grained evaluation and personalized data assessment of how LLMs use tools.
3. Existing tool-use benchmarks ignore the assessment of special cases with imperfect user instructions, or use simplistic evaluation methods, despite real-world user instructions frequently being imperf
4. Relying on LLMs for evaluation of tool-use benchmarks introduces significant overhead and high costs.
5. Stable ToolBench's dependence on large models for evaluation results in high costs and scalability challenges.
6. τ-Bench's narrow focus on just two scenarios limits its generalizability across diverse tasks.
7. ACEBench comprises 2,000 annotated entries in two linguistically parallel versions (Chinese and English) with equal distribution of data types between them.
8. ACEBench covers 8 major domains and 68 sub-domains with a collection of 4,538 APIs in both Chinese and English.
9. ACEBench dialogue turns range from 1 to 8, covering most real-world scenarios.
10. ACEBench's Normal data evaluation uses AST parsing to compare model function call output with ground truth, enabling LLM-free evaluation.

## Capabilities

- Top frontier LLMs (GPT-4o, GPT-4-Turbo) achieve 84–85% accuracy on standard single-turn and atomic tool invocation tasks across diverse API domains
- Open-source models (Qwen2.5-Coder-32B, DeepSeek-V3) achieve competitive tool-use performance approaching closed-source frontier models, within ~6–10 percentage points overall
- LLMs achieve 85–89% process accuracy on scripted multi-step tool invocation tasks when the execution sequence is well-defined and fixed
- Tool-use performance scales clearly with model parameter count, with each significant step up in scale delivering measurable accuracy gains on complex multi-turn scenarios

## Limitations

- Dynamic multi-turn agent interactions where users participate in dialogue remain practically unsolved — end-to-end accuracy falls below 50% for nearly all models including frontier ones (GPT-4-Turbo 50%, Claude-3.5-Sonnet 21.5%, most others <32%)
- Fine-tuning LLMs on tool-use datasets causes severe generalization collapse — fine-tuned models (Watt-Tool-8B, xLAM-7B, Hammer2.1) score near 0% on imperfect/ambiguous instructions where comparably-sized base models score 26–79%
- Parameter value generation is the dominant failure mode (~60% of all errors across all model families) — models struggle to produce correct specific numerical values and contextually appropriate parameter content even when function selection succeeds
- LLMs almost universally detect imperfect instructions but fail to correctly specify what is wrong — error correction accuracy is near 0% for fine-tuned models (xLAM: 1 correct correction out of 196 attempts, Hammer2.1-3B: 0 out of 197)
- Models cannot reliably maintain and propagate contextual state across multi-turn interactions — information mismanagement (failure to record and correctly use earlier context) is a primary failure mode in agent tasks
- Models systematically violate predefined scene rules in complex agent tasks — skipping required procedural steps and breaking task logic even when constraints are provided in context
- Dramatic performance cliff between scripted multi-step and dynamic multi-turn agent tasks: GPT-4-Turbo drops from 85% to 50% EA, Claude-3.5-Sonnet drops from 57.5% to 21.5% EA — dynamic user participation halves or worse the performance of every tested model
- Scaling returns diminish sharply between 32B and 72B parameters on tool-use tasks — simple parameter scaling is unlikely to resolve the core multi-turn and ambiguous-instruction failures
- ACEBench and comparable tool-use benchmarks rely on LLM-generated synthetic APIs rather than real-world APIs, creating a systematic validity gap that may cause overestimation of production readiness
- No security or adversarial robustness evaluation exists in any current tool-use benchmark including ACEBench — prompt injection, tool misuse, and malicious API exploitation are entirely absent from evaluation frameworks
- Agent evaluation scenario diversity is bottlenecked by manual expert construction — agent benchmark coverage cannot scale without proportional expert labour investment
- No evaluation of inference latency, API call overhead, or cost in tool-use benchmarks — all existing benchmarks including ACEBench measure accuracy only, leaving production deployment economics entirely uncharacterised

## Bottlenecks

- Dynamic multi-turn tool use with real user participation remains practically unsolved: all frontier models fail to reliably complete tasks when user instructions evolve dynamically, blocking deployment of conversational AI agents in real-world settings
- The generalization-specialization tradeoff in tool-use fine-tuning is unresolved: no training approach known to reliably improve tool-use accuracy without catastrophically degrading performance on imperfect, ambiguous, or novel instructions
- Tool-use evaluation benchmarks built on synthetic LLM-generated APIs create a systematic real-world validity gap, preventing confident assessment of whether tool-use models are production-ready

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/τ-bench|τ-Bench]]
