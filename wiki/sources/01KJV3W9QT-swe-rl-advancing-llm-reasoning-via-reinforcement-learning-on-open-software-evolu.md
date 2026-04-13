---
type: source
title: 'SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software
  Evolution'
source_id: 01KJV3W9QTWHPKY0X75EST48R9
source_type: paper
authors:
- Yuxiang Wei
- Olivier Duchenne
- Jade Copet
- Quentin Carbonneaux
- Lingming Zhang
- Daniel Fried
- Gabriel Synnaeve
- Rishabh Singh
- Sida I. Wang
published_at: '2025-02-25 00:00:00'
theme_ids:
- agent_systems
- ai_software_engineering
- code_and_software_ai
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution

**Authors:** Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin Carbonneaux, Lingming Zhang, Daniel Fried, Gabriel Synnaeve, Rishabh Singh, Sida I. Wang
**Published:** 2025-02-25 00:00:00
**Type:** paper

## Analysis

# SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution
2025-02-25 · paper · Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin Carbonneaux, Lingming Zhang et al. (9 total)
https://arxiv.org/pdf/2502.18449

---

### Motivation & Prior Limitations
- Prior RL work for coding (DeepSeek-R1, follow-ups) was confined to competitive programming and mathematics, leaving real-world software engineering tasks largely unaddressed by RL-based training.
  - Competitive coding rewards rely on execution feedback against self-contained programs; real-world SE tasks lack easily executable environments and incur high execution costs, making this reward regime inapplicable.
  - Existing open-model SE approaches (Lingma-SWE-GPT, SWE-Gym, SWE-Fixer) all depend on distilled outputs from proprietary models (GPT-4o or Claude-3.5-Sonnet) and use supervised finetuning (SFT), which steers models toward a narrow task distribution and degrades performance on out-of-domain tasks.
- Most high-performing SWE-bench systems relied on powerful proprietary LLMs, with advances driven by prompting strategies rather than improvements to the underlying model.
  - Among medium-sized open models (<100B parameters), the prior best on SWE-bench Verified was SWE-Gym-32B at 32.0% and SWE-Fixer-72B at 32.8%, both trained with proprietary data distillation.

---

### Proposed Approach
- SWE-RL applies reinforcement learning directly to real-world software engineering using software evolution data — the full record of GitHub development lifecycles including code snapshots, pull requests, issues, and code changes — with a lightweight rule-based reward requiring no proprietary model in the loop.
  - Unlike SFT baselines that require synthetic chain-of-thought generation from a teacher model plus carefully curated data mixes, SWE-RL needs only a seed PR dataset and the RL loop itself to self-improve.
  - The reward function is a continuous sequence similarity score (via Python's `difflib.SequenceMatcher`, yielding 0–1) between the predicted patch and the oracle patch merged by the PR; responses with incorrect format receive a reward of −1. A continuous reward is used rather than discrete exact-match, because real-world patches are highly diverse and rarely match exactly — the continuous signal captures partial correctness and allows learning of incremental improvements.
- The policy is trained with GRPO (Group Relative Policy Optimization) on 273k curated GitHub PR seeds, each containing an issue description, code context (full file contents of changed and relevant files), and an oracle patch.
  - Providing complete file contents in the prompt implicitly forces the model to reason about precise fault locations before generating repair edits, teaching bug diagnosis and repair generation jointly without explicit supervision on localization.
- A simplified pipeline scaffold, Agentless Mini, is built on top of Agentless, reducing localization to file-level only and delegating fine-grained reasoning to the repair step, which aligns with the RL training signal and allows the model to generalize to other pipeline steps (test generation, reranking) through out-of-domain transfer.

---

### Results & Capabilities
- Llama3-SWE-RL-70B achieves 41.0% on SWE-bench Verified, the best reported result among medium-sized models (<100B parameters) and comparable to GPT-4o (38.8% with Agentless) and o1-preview (41.3%).
  - This is achieved without any proprietary model in the training pipeline, trained exclusively on publicly available GitHub data.
  - The SFT baseline (Llama3-SWE-SFT-70B) with the same seed data reaches only 36.2%, and the base Llama-3.3-70B-Instruct with majority voting reaches only 16.6% in oracle repair conditions.
- In oracle repair conditions (greedy decoding, oracle-localized files provided), Llama3-SWE-RL-70B scores 34.8 vs. 29.6 for the SFT model and 16.6 for the base model with majority voting; format accuracy is 95.6% vs. 96.2% (SFT) and 44.6% (base with voting).
- Performance scales meaningfully with compute at inference: increasing repair samples from 20 to 160 raises the score from 33.6 to 40.0, with diminishing returns beyond 160; increasing reproduction test samples from 1 to 20 raises the score from 38.8 to 41.0, saturating at 20–30 tests.
- Despite training exclusively on issue-solving, Llama3-SWE-RL-70B improves over its base model on five out-of-domain benchmarks: HumanEval+ (76.2→79.9), CRUXEval-I (60.5→71.6), CRUXEval-O (61.9→75.5), MATH (63.2→73.7 strict), and MMLU (86.49→86.82), whereas the SFT baseline degrades on average across these same tasks.
  - The paper identifies "aha moment" emergent reasoning behaviors — self-reflection, alternative exploration, and divide-and-conquer strategies — appearing in both in-domain (issue solving) and out-of-domain (function implementation, mathematics) outputs, consistent with DeepSeek-R1's findings but demonstrated here for real-world SE tasks for the first time.
- Continuous rewards substantially outperform discrete (exact-match) rewards: discrete training achieves only 29.0 repair score vs. 34.8 for continuous, with discrete rewards growing slower and remaining near zero throughout training, confirming that exact-match is too sparse a signal for real-world patch diversity.

---

### Implications
- SWE-RL demonstrates that RL on real-world software artifacts — not synthetic tasks or competition problems — is a viable and superior path to general reasoning capability improvement, suggesting that the richness and diversity of authentic software evolution data may be a better reasoning training signal than curated math or competition benchmarks.
- The result that SFT consistently degrades out-of-domain performance while RL improves it, even on a single task distribution, has significant implications for training strategy: SFT may be fundamentally limited in producing generalizable reasoning, whereas RL's exploratory incentive structure induces tran

## Key Claims

1. RL applied solely to software engineering issue-solving causes generalized reasoning skills to emerge that transfer to out-of-domain tasks including mathematics, function coding, library use, code rea
2. Supervised fine-tuning (SFT) on issue-solving data leads to average performance degradation on out-of-domain tasks, even with carefully curated data mixes, whereas RL does not.
3. SWE-RL uses a lightweight rule-based reward defined as the sequence similarity between the LLM-generated patch and the oracle patch, computed via Python's difflib.SequenceMatcher.
4. If the LLM response is incorrectly formatted, the reward assigned is -1; otherwise it is the sequence similarity score between predicted and oracle patch.
5. SWE-RL curates 273,000 high-quality PR seeds from GitHub as the seed RL dataset, filtered by heuristics requiring at least one linked issue describing a bug fix and code changes involving programming 
6. SWE-RL uses Group Relative Policy Optimization (GRPO) for policy optimization.
7. Training SWE-RL conditions the model on complete file contents, implicitly teaching it to identify precise fault locations before generating repair edits.
8. Llama3-SWE-RL-70B was trained for 1,600 steps with a 16k context window, global batch size of 512, sampling 16 rollouts from each of 32 problems per batch, on 512 NVIDIA H100 GPUs taking approximately
9. SWE-RL training causes emergent 'aha moments'—self-reflection, exploration of alternative approaches, and divide-and-conquer reasoning—in a real-world software engineering context, confirming similar 
10. Llama3-SWE-RL-70B generalizes to pipeline subtasks (file-level localization, reproduction test generation, regression test selection) despite being trained only on the repair subtask.

## Capabilities

- RL training on real-world GitHub PR data (without proprietary teacher models) enables a 70B open LLM to achieve 41.0% on SWE-bench Verified — best among medium-sized (<100B) models and comparable to GPT-4o
- Sequence similarity (non-execution) rule-based reward enables RL for real-world software issue solving, sidestepping the need for executable environments or proprietary teacher models
- RL training on a single domain (software issue solving) induces generalized reasoning skills that transfer to unrelated domains: function coding, mathematics, code reasoning, library use, and general language understanding
- RL on real-world SE tasks induces 'aha moment' emergent behaviors — self-reflection, exploring alternative approaches, divide-and-conquer — in large LLMs on software engineering tasks
- Test-time compute scaling via sampling multiple repair patches and reproduction tests improves SE agent performance on SWE-bench, with score rising from 33.6% (20 samples) to 41.0% (500 samples)

## Limitations

- Sequence similarity reward measures textual overlap with oracle patches but not semantic equivalence — the model cannot discover functionally correct but textually different solutions
- Execution-based RL reward signals are impractical for real-world software engineering due to execution cost and absence of executable environments
- Pipeline-based scaffold (Agentless Mini) divides solving into discrete inference stages, preventing the model from learning through interaction feedback or considering the problem holistically
- Test-time compute scaling for SE agents hits a performance plateau beyond ~160 repair samples — marginal gains diminish sharply (40.0% at 160 samples → only 41.0% at 500 samples)
- RL training for a 70B model requires 512 H100 GPUs for 32 wall-time hours — inaccessible to most researchers and organizations
- Supervised fine-tuning on domain-specific data degrades out-of-domain performance even with carefully curated mixed training data — RL is required to avoid capability regression
- Even best-in-class open SE agents (41% SWE-bench Verified) still fail on 59% of real-world GitHub issues — a large unsolved gap relative to what would be needed for autonomous deployment
- Base LLMs without RL/SFT produce correctly formatted SE patches only 12.2% of the time under greedy decoding — format adherence is a fundamental prerequisite not met by instruction-tuned models
- Discrete binary reward (exact patch match) fails entirely for real-world SE — reward remains near zero throughout training because real patches are too diverse to match exactly
- RL training is limited to a 16k context window — real-world repositories with large files or spanning many modules may be truncated, constraining applicability to larger codebases
- Localization is simplified to file-level only — the model is not trained to pinpoint function-level or line-level fault locations, requiring complete file contents as workaround
- Proprietary large models still substantially outperform best open SE agents: Claude-3.5-Sonnet+OpenHands=53%, DeepSeek-R1=49.2% vs Llama3-SWE-RL=41.0% — a 12-point ceiling gap persists

## Bottlenecks

- Absence of practical execution-based reward signals for real-world SE tasks forces RL to rely on approximate text similarity metrics, limiting the quality of the reward signal and blocking more capable SE agents
- Sequence similarity rewards cannot distinguish functionally equivalent code patches from wrong ones — semantic code equivalence checking at RL training scale remains unsolved
- Pipeline-based scaffolding forces SE RL training into isolated single-step subtasks, preventing the model from learning end-to-end from multi-step interaction feedback across the full development cycle

## Breakthroughs

- First successful RL training approach for real-world software engineering using only raw open-source GitHub PR data and lightweight rule-based rewards — no proprietary teacher models, no execution environments — achieving SOTA for open medium-sized LLMs (41% SWE-bench Verified)
- RL training on a single domain-specific task (software issue solving) induces generalized reasoning capabilities that transfer and improve performance on unrelated domains — first demonstration that SE data can function as a general reasoning curriculum

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_software_engineering|ai_software_engineering]]
- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/pass1|Pass@1]]
- [[entities/swe-rl|SWE-RL]]
