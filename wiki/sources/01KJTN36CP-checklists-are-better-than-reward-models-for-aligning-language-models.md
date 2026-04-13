---
type: source
title: Checklists Are Better Than Reward Models For Aligning Language Models
source_id: 01KJTN36CP4M8VZYW8BNS2TYDM
source_type: paper
authors:
- Vijay Viswanathan
- Yanchao Sun
- Shuang Ma
- Xiang Kong
- Meng Cao
- Graham Neubig
- Tongshuang Wu
published_at: '2025-07-24 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Checklists Are Better Than Reward Models For Aligning Language Models

**Authors:** Vijay Viswanathan, Yanchao Sun, Shuang Ma, Xiang Kong, Meng Cao, Graham Neubig, Tongshuang Wu
**Published:** 2025-07-24 00:00:00
**Type:** paper

## Analysis

# Checklists Are Better Than Reward Models For Aligning Language Models
2025-07-24 00:00:00 · paper · Vijay Viswanathan, Yanchao Sun, Shuang Ma, Xiang Kong, Meng Cao et al. (7 total)
https://arxiv.org/pdf/2507.18624

---

### Motivation & Prior Limitations
- Reinforcement learning for language model alignment has relied on reward signals that are either too narrow (verifiable-only tasks), too arbitrary (fixed reward models prone to hacking), or insufficiently comprehensive (prompted AI judges inferring grading dimensions on their own).
  - Reward models trained on human preferences show "reward hacking" because their notion of reward can be arbitrary and poorly correlated with actual instruction satisfaction — RewardBench accuracy correlates poorly with RLHF efficacy, as demonstrated in prior work (Malik et al., 2025; Razin et al., 2025).
  - Methods like UltraFeedback evaluate responses along only four global principles (instruction following, helpfulness, truthfulness, honesty), which fail to capture the full space of requirements in rich, multi-step user instructions.
  - Restricting RL to verifiable tasks (e.g., math, code) excludes large swaths of subjective open-ended behavior such as topicality, style, and content constraints.
- Existing RL methods applied to instruction following show inconsistent benchmark performance: Skywork-guided DPO improves AlpacaEval and InFoBench but causes notable regressions on IFEval and FollowBench; ArmoRM-guided DPO similarly degrades IFEval while helping elsewhere.

---

### Proposed Approach
- The paper proposes Reinforcement Learning from Checklist Feedback (RLCF), which replaces fixed reward models with dynamically generated, instruction-specific checklists as the source of reward signal for RL training.
  - Unlike reward models that apply the same learned scoring function to all instructions, RLCF extracts a unique set of yes/no requirements per instruction, making the evaluation criteria explicit and tailored to the actual constraints expressed in each query.
  - Checklists are generated via a "candidate-based" two-stage method: (1) produce responses of varying quality from models of different sizes (Qwen2.5-0.5B through 7B), then (2) prompt Qwen2.5-72B-Instruct to write a checklist covering all possible failure modes of those candidates, with importance weights per item. This outperforms "direct" prompting (which simply asks an LLM to extract a checklist from the instruction alone) on objectiveness, atomicity, and downstream RL performance.
  - Scoring each response combines a prompted LM judge (Qwen2.5-72B-Instruct, averaging 25 sampled scores per criterion) with an automatically generated verifier program for hard discrete constraints (e.g., character counts, presence of specific words), balancing the strengths of each — the judge handles qualitative criteria while the program handles exact formal constraints.
  - Two universal requirements covering conciseness and tone-matching are appended to all checklists to prevent reward hacking artifacts such as verbose preamble overviews.
  - The resulting scored response pairs are filtered to the 40% with the greatest per-criterion score difference, then used for DPO preference training. RLCF is conceptualized as an extreme mixture-of-evaluators: an unbounded set of prompted evaluators where a unique subset is chosen per instruction, generalizing over prior approaches from classic AI judges (1 evaluator) to ArmoRM (19 experts) to Constitutional AI (16 fixed criteria).
- The WildChecklists dataset of 130,000 instructions with corresponding synthetically generated checklists is released alongside models and code.

---

### Results & Capabilities
- RLCF is the only evaluated alignment method to produce improvements over Qwen2.5-7B-Instruct across all five benchmarks simultaneously (IFEval, InFoBench, FollowBench, AlpacaEval, Arena-Hard); all alternative automatic feedback sources produce mixed results.
  - On FollowBench, RLCF achieves a 5.5% absolute increase in average Hard Satisfaction Rate (71.4 → 75.3) and an 8.2% increase in Constraint Satisfaction Level (3.05 → 3.30), versus regressions for Skywork-DPO (69.5 HSR) and ArmoRM-DPO (70.4 HSR).
  - On InFoBench, RLCF improves overall requirement following ratio by 6.9% relative (78.1 → 84.1), roughly matching the best reward model baselines on this benchmark specifically.
  - On Arena-Hard, RLCF achieves a 6.4% relative improvement in win rate (51.3 → 54.6 vanilla), with consistent gains on style-controlled evaluation (42.8 → 48.4).
- RLCF transfers off-policy: using preference data collected from Qwen2.5-7B-Instruct scored by Qwen2.5-72B-Instruct, Llama 3.1 8B Instruct improves strongly on InFoBench and FollowBench, and OLMo 2 7B Instruct improves strongly on IFEval, with no regressions for either model.
- Checklist feedback is especially effective for "content" constraints on FollowBench — qualifiers that restrict the valid answer space (e.g., "consider how inflation affects the Fed's decision") — improving content Hard Satisfaction Rate from 60.0 to 66.4, suggesting the method incentivizes models to attend to the full instruction rather than salient spans.
- Candidate-based checklist generation is crucial: it produces checklists that are 90% atomic vs. 68% for direct generation, and translates to 2–3 point gains on IFEval and FollowBench in downstream RL training.
- Checklist-based scoring on RewardBench achieves 90.0 on Chat and 80.7 on Chat Hard, competitive with but below Skywork-27B (96.1/89.9) and ArmoRM (96.9/76.8), confirming that checklist rewards are reasonably well-correlated with human preferences while being better supervisors for RL than dedicated reward models.

---

### Implications
- The finding that reward model accuracy on RewardBench is a poor predictor of RL training efficacy challenges the standard proxy for evaluating alignment feedback quality and suggests the field needs training-time evaluations rather than static prefere

## Key Claims

1. RLCF is the only alignment method that improves performance on every benchmark tested, including constrained instruction following and general conversational assistance.
2. Off-the-shelf reward models yield mixed results across instruction following benchmarks, improving on some while causing regressions on others.
3. Reward model benchmark accuracy is poorly correlated with efficacy when used to supervise reinforcement learning.
4. Candidate-based checklist generation produces better checklists for RL training than directly prompting a model to extract a checklist.
5. Checklist feedback is most beneficial for 'content' constraints — open-ended qualifiers that restrict the valid answer space — suggesting it incentivizes models to attend to full instructions.
6. RLCF can be applied off-policy to improve models from other families, suggesting checklists capture universal criteria not tied to a specific model.
7. Optimizing for checklist completion without regularization leads to reward hacking, manifesting as responses beginning with long preamble overviews.
8. False positive rewards in reinforcement learning are more detrimental than false negative rewards, motivating the use of objective and atomic checklist criteria.
9. RLCF modestly reduces performance on out-of-distribution tasks including math reasoning and hallucination prevention, suggesting a need for more diverse training prompts.
10. Checklist-based reward scores are well-correlated with human preference judgments on RewardBench, particularly for Chat and Chat Hard categories, but underperform specialized reward models on Safety.

## Capabilities

- Reinforcement Learning from Checklist Feedback (RLCF): using dynamic, instruction-specific checklists as reward signals consistently improves instruction-following models across all tested benchmarks, where every other automatic feedback method gives mixed results
- Candidate-based automated checklist generation from instructions: produce diverse-quality candidate responses then prompt an LM to enumerate all failure modes, yielding checklists superior in objectivity, atomicity, and overall quality to direct prompting
- Hybrid LM-judge plus verifier program scoring for instruction evaluation: combining AI judge numerical scores (averaged over 25 samples) with code-based verification programs for hard discrete criteria produces more robust reward signals than either approach alone
- Off-policy checklist-based RL generalization: checklists generated from one model family (Qwen2.5) can improve instruction-following in different model families (Llama 3.1, OLMo 2) off-policy without regressions on any benchmark

## Limitations

- RLCF checklist scoring is computationally prohibitive for most practitioners: grading 130k instruction pairs with a 72B judge takes approximately 4 days on 8xH100 GPUs, with the AI judge being the explicit bottleneck
- RLCF requires a large teacher model as judge (strong-to-weak generalization dependency): a 72B model is used to supervise a 7B student, limiting applicability where large models are unavailable or too costly
- RLCF degrades safety alignment: reduces true refusals for genuinely unsafe prompts (Unsafe accuracy drops from 83.0 to 81.0 on XSTest) and is explicitly not a substitute for safety alignment
- RLCF causes 1-1.5% degradation on domains underrepresented in training data: GSM8K math accuracy and TruthfulQA hallucination prevention both decline because WildChat skews heavily toward daily assistance (75.5%) with only 12% math and factual content
- Standard reward models are unreliable RL supervisors despite high RewardBench benchmark accuracy: top-ranked models (Skywork-27B at #4, ArmoRM at #24 on RewardBench) cause regressions on multiple instruction-following benchmarks
- Single-rubric AI judges are insensitive to major instruction-specific quality differences: the same 100-point score is assigned to a correct Spanish translation and one with incoherent phrases, revealing fundamental discrimination failure at fine-grained instruction criteria
- Checklist generation quality is a critical performance gate: directly-generated checklists underperform candidate-based ones by 2-3% on FollowBench and 2% on IFEval, revealing sensitivity to upstream generation methodology
- Reducing judge sample count degrades RLCF on difficult, ambiguous instruction categories: cutting from 25 to 3-5 samples hurts 'content' and 'situation' constraint categories specifically, with FollowBench HSR declining by several points
- RLCF does not outperform supervised finetuning (SFT) when starting from a non-instruction-tuned base model: on FollowBench, SFT on WildChat outperforms DPO (RLCF) from the base Qwen2.5-7B
- Checklist-based reward is substantially weaker at safety evaluation than specialized reward models: 71.4% on RewardBench Safety vs 93.0% for Skywork-27B, indicating RLCF cannot replace safety-specific feedback mechanisms
- Reward hacking via preamble generation emerges when optimizing for checklist completion without global quality regularization: models learn to produce verbose, off-topic preamble overviews that satisfy individual checklist items superficially
- RLCF has only been explored with preference-based RL (DPO); policy gradient methods (GRPO, PPO) and online RL remain untested, leaving the question of whether checklist feedback can power stronger RL paradigms open
- LLMs cannot reliably evaluate hard discrete criteria and must defer to verifier programs which themselves cannot be synthesized for subjective or ambiguous requirements, creating a partial coverage gap in automated checklist scoring

## Bottlenecks

- LM judge inference cost for checklist scoring is computationally prohibitive at practitioner scale: averaging 25 scores per checklist item for 130k instructions requires 4 days on 8xH100 GPUs, blocking broad adoption of RLCF beyond well-resourced labs
- Reward model benchmark accuracy (RewardBench) is structurally decoupled from RL training efficacy: no principled basis exists for selecting reward sources that will reliably improve models under RL, forcing empirical per-benchmark validation

## Breakthroughs

- First automatic feedback method to consistently improve instruction-following models across all evaluated benchmarks spanning both constrained and open-ended instruction types — resolving the mixed-results failure mode that characterized all prior automatic RL alignment approaches

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/alignment_methods|alignment_methods]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/alpacaeval|AlpacaEval]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/ifeval|IFEval]]
- [[entities/qwen25-7b-instruct|Qwen2.5-7B-Instruct]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/ultrafeedback|UltraFeedback]]
- [[entities/wildchat|WildChat]]
- [[entities/generator-verifier-gap|generator-verifier gap]]
