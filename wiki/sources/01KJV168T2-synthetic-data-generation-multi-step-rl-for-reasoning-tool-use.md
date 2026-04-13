---
type: source
title: Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use
source_id: 01KJV168T2NY322WPC7HYVR7C9
source_type: paper
authors:
- Anna Goldie
- Azalia Mirhoseini
- Hao Zhou
- Irene Cai
- Christopher D. Manning
published_at: '2025-04-07 00:00:00'
theme_ids:
- agent_systems
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use

**Authors:** Anna Goldie, Azalia Mirhoseini, Hao Zhou, Irene Cai, Christopher D. Manning
**Published:** 2025-04-07 00:00:00
**Type:** paper

## Analysis

# Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use
2025-04-07 · paper · Anna Goldie, Azalia Mirhoseini, Hao Zhou, Irene Cai, Christopher D. Manning
https://arxiv.org/pdf/2504.04736

---

### Motivation & Prior Limitations
- Traditional RL approaches for LLMs (RLHF, RLAIF, RLEF) treat the problem as single-step, optimizing only at the end of an episode, which leaves multi-step reasoning and tool use tasks largely unaddressed.
  - Methods like RLHF and RLAIF compute reward only at the final response, creating a credit assignment problem when multiple interleaved reasoning steps and tool calls are required before an answer.
  - Existing multi-step RL alternatives have significant practical drawbacks: DQO operates at the token level (shown to be less effective than step-level), and OREO requires training and co-optimizing a separate value network and policy, making it prohibitively expensive for large models.
- LLMs struggle with multi-hop question answering, mathematical problem-solving, and agentic tasks precisely because incorrect intermediate steps compound into incorrect final results, and the model must learn when to stop searching, how to formulate queries, and how to synthesize findings — capabilities not targeted by single-step optimization.
- Prior synthetic data approaches (STaR, RFT, ReSTEM) rely on golden labels to filter trajectories for correct outcomes, which restricts data volume and may not generalize; ReSTEM in particular plateaus after a few iterations, presumably due to overfitting when trained only on correct traces.

---

### Proposed Approach
- SWiRL (Step-Wise Reinforcement Learning) is a two-stage offline methodology: Stage 1 generates and filters multi-step synthetic trajectories using an LLM augmented with tools (search engine or calculator), and Stage 2 applies step-wise RL by decomposing each trajectory into sub-trajectories and optimizing per-step reward using a generative reward model.
  - Unlike DeepSeek-R1 and Llama-3 RL finetuning which optimize only for final performance using golden labels, SWiRL optimizes the reasonableness of each intermediate step given its prior context, with no golden labels anywhere in the pipeline.
  - The step-wise decomposition converts each trajectory of k actions into k sub-trajectories; the reward model (Gemini 1.5 Pro) scores each action given its full preceding context, and the policy gradient objective maximizes the expected sum of these step-wise rewards.
- For synthetic data generation, the base model (Gemma 2) iteratively generates chain-of-thought plus tool calls; tool responses are executed and injected into context; trajectories are then filtered by process quality (each step judged reasonable by Gemini 1.5 Pro Thinking) rather than by outcome correctness.
  - Process-only filtering retains trajectories where every step is sound regardless of whether the final answer is correct, deliberately including both positive and negative outcome examples to expose the RL optimizer to a mixture of trajectories.
  - The offline design allows parallel trajectory generation to avoid training bottlenecks from slow tool execution, and produces a fixed, reproducible dataset.

---

### Results & Capabilities
- SWiRL outperforms the base Gemma-2-27b model by substantial relative margins: 21.5% on GSM8K, 12.3% on HotPotQA, 14.8% on CofCA, 11.1% on MuSiQue, and 15.3% on BeerQA, averaging approximately 15% relative improvement across benchmarks.
  - SWiRL-finetuned Gemma-2-27b scores 67.8 on HotPotQA, 39.3 on CofCA, and 43.6 on MuSiQue (partial match), competitive with or surpassing GPT-4 (74.8 / 51.9 / 63.9) on some datasets and substantially ahead of all open-source 7b-class baselines.
- SWiRL exhibits strong cross-task generalization: training only on HotPotQA (text QA with search) improves GSM8K (math with calculator) by a relative 16.9%, and training only on GSM8K improves HotPotQA by 9.2%.
  - This cross-domain transfer — different tool, different task type — suggests SWiRL improves a general multi-step reasoning capability rather than task-specific patterns.
- Process-only filtering consistently yields the best downstream accuracy; outcome-filtered data underperforms unfiltered data on most benchmarks (except MuSiQue), and the combination of process+outcome filtering is never the best strategy for SWiRL.
  - This directly contradicts the assumption inherited from SFT-based distillation (e.g., DeepSeek-R1) that filtering for correct outcomes is necessary or beneficial.
- SWiRL outperforms its own reward model (Gemini 1.5 Pro) on out-of-distribution benchmarks CofCA and BeerQA, ruling out the explanation that gains are merely from distilling a stronger teacher.
- The mechanism underlying performance gains is verified empirically: after SWiRL training, mean process label accuracy rises from 82.5% to 91.0% on HotPotQA (in-distribution) and from 87.5% to 91.6% on GSM8K (out-of-distribution), confirming that downstream accuracy gains are driven by improved per-step reasoning quality rather than superficial pattern matching.
- Even without tool access at inference time, SWiRL-trained models show meaningful improvement over base models, indicating that training improves internal problem decomposition independently of tool scaffolding.
- Significant gains are achievable with as few as 1,000 training trajectories; scaling to 10,000 continues to improve performance, and cross-domain improvement on GSM8K scales with HotPotQA dataset size.

---

### Implications
- The finding that process-filtered (but outcome-agnostic) data enables better RL learning than outcome-filtered data challenges the prevailing assumption in the synthetic data literature that correctness of final answers is the primary signal worth filtering for; this has direct implications for how reward models and data pipelines should be designed for agentic training.
- The cross-task and cross-tool generalization results suggest that multi-step reasoning is a tran

## Key Claims

1. SWiRL outperforms baseline approaches by 21.5%, 12.3%, 14.8%, 11.1%, and 15.3% in relative accuracy on GSM8K, HotPotQA, CofCA, MuSiQue, and BeerQA respectively.
2. Training SWiRL only on HotPotQA (multi-hop question-answering) improves zero-shot performance on GSM8K (mathematics) by a relative 16.9%, demonstrating cross-task generalization.
3. Training SWiRL on GSM8K (mathematics) improves performance on HotPotQA (multi-hop question-answering) by 9.2%, demonstrating bidirectional cross-task generalization.
4. Traditional RL approaches for LLMs (RLHF, RLAIF, RLEF) focus on single-step optimization, leaving multi-step task challenges unaddressed.
5. Process-only filtering (without outcome filtering) consistently yields the highest downstream accuracy for SWiRL, outperforming no filtering, outcome filtering, and combined process+outcome filtering.
6. Outcome-based filtering of training data usually harms SWiRL performance relative to process-only filtering, because SWiRL benefits from a mixture of correct and incorrect trajectory outcomes.
7. SWiRL can learn effectively from trajectories with incorrect final answers, unlike supervised fine-tuning which requires correct-outcome data.
8. SWiRL does not require golden labels or human annotations, relying entirely on model-based judgments for data generation, filtering, and RL optimization.
9. Supervised fine-tuning (SFT) degrades reasoning performance compared to the base model when applied to multi-step reasoning and tool use tasks.
10. SFT benefits from process+outcome filtered data (requiring correct final answers), whereas SWiRL benefits from process-only filtered data — the two methods have opposite data filtering requirements.

## Capabilities

- Step-Wise RL (SWiRL) trains LLMs for multi-step reasoning and tool use using only process-filtered synthetic data — no golden labels or human annotations required — achieving 15%+ relative accuracy gains over baselines on multi-hop QA and mathematical reasoning.
- Multi-step RL training on one task type (multi-hop QA) generalizes zero-shot to a structurally different task and tool (mathematical reasoning with calculator), improving GSM8K performance by 16.9% — and vice versa.
- Generative reward models (Gemini 1.5 Pro) can provide step-level process feedback for multi-step RL optimization without access to ground-truth answers, enabling scalable offline training pipelines.
- Parallel offline generation of large-scale multi-step synthetic trajectories with tool use (search, calculator) enabling fast training data collection decoupled from slow environment execution.
- SWiRL improves multi-step reasoning even without access to a tool at inference time, indicating that step-wise RL internalizes problem decomposition skills beyond tool-calling mechanics.
- Significant multi-step RL gains are achievable with as few as 1,000 synthetic trajectories, enabling low-cost adaptation to new domains without requiring large-scale annotation pipelines.

## Limitations

- Traditional RL methods (RLHF, RLAIF, RLEF, PPO, DPO, GRPO) are designed for single-step optimization only — reward is calculated at episode end — making them structurally inadequate for multi-step agentic tasks requiring sequences of reasoning and tool calls.
- Smaller models (2B and 9B parameters) show in-domain improvements from SWiRL but fail to exhibit cross-task generalization — a hard capability threshold exists at scale that smaller models cannot cross.
- Supervised finetuning (SFT) on multi-step synthetic data degrades base model performance — the memorization tendency of SFT conflicts with the generalization requirements of multi-step agentic tasks.
- SWiRL performance collapses with only 100 training trajectories — a practical minimum threshold of ~1,000 trajectories is required before meaningful generalization emerges.
- Outcome-filtering of synthetic training data (selecting only trajectories with correct final answers) is counterproductive for multi-step RL — it removes negative examples the model needs to learn recovery and error correction.
- Hard step-count ceilings (5 steps for QA, 10 for math) are imposed at both training and inference time — the system cannot handle tasks requiring longer chains, and the ceiling's impact on difficulty ceiling is unevaluated.
- Model-based evaluation using LLM judges introduces stochasticity and potential judge bias — different judge models (GPT-4o vs Gemma-2-27b vs Gemini 1.5 Pro) are used across experiments, complicating cross-experiment comparability.
- SWiRL uses Gemini 1.5 Pro as its generative reward model — a computationally expensive frontier model — making the approach inaccessible for resource-constrained settings, despite being framed as open-source.
- SWiRL is evaluated only on multi-hop QA and grade-school math — no evaluation on coding, desktop automation, web navigation, or real agentic tasks despite framing the paper around the 'explosion of agentic applications'.
- Iterative ReSTEM-style synthetic data loops plateau after a few training iterations — a known ceiling on self-improvement via synthetic data that SWiRL has not been evaluated against over multiple iterations.
- SWiRL's offline training uses a static synthetic dataset — the model cannot adapt to environment drift, changing tool APIs, or novel query distributions encountered after deployment.
- No evaluation of safety properties — a tool-use agent trained to maximize step-wise rewards with a search engine is never assessed for misuse potential, prompt injection via retrieved content, or adversarial tool responses.

## Bottlenecks

- Long-horizon credit assignment in multi-step tool-use RL — existing single-step RL methods cannot attribute trajectory-level outcomes to intermediate reasoning and tool-call steps, blocking training on multi-step agentic tasks.
- Requirement for golden labels (correct final answers) in synthetic data pipelines restricts RL training to tasks with verifiable outcomes, excluding open-ended agentic tasks where ground truth is unavailable.
- Compounding error propagation in multi-step reasoning — each incorrect intermediate step increases the probability of trajectory-level failure, and prior single-step RL methods have no mechanism to correct mid-trajectory mistakes.
- Scale threshold for cross-task generalization — multi-step RL generalization requires models above ~27B parameters; smaller models remain domain-confined, making the approach inaccessible for edge deployment.

## Breakthroughs

- Process-only filtering of synthetic training trajectories (judging step quality without requiring correct final answers) outperforms outcome-filtered data for multi-step RL — reversing the prevailing assumption that correct-outcome filtering is necessary or beneficial.
- Multi-step RL training demonstrates strong cross-task and cross-tool generalization — training on multi-hop QA with a search engine improves mathematical reasoning with a calculator by 16.9% zero-shot, and vice versa — suggesting that step-wise RL learns a domain-general reasoning substrate.

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/grpo|GRPO]]
- [[entities/gsm8k|GSM8K]]
- [[entities/generative-reward-model|Generative Reward Model]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/musique|MuSiQue]]
- [[entities/prime|PRIME]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/restem|ReSTEM]]
- [[entities/reinforcement-learning-from-ai-feedback-rlaif|Reinforcement Learning from AI Feedback (RLAIF)]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/star-self-taught-reasoner|STaR (Self-Taught Reasoner)]]
