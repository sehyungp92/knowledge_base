---
type: source
title: 'Spurious Rewards: Rethinking Training Signals in RLVR'
source_id: 01KJTQ74E7CE1V0S09YFQEF1Q3
source_type: paper
authors:
- Rulin Shao
- Shuyue Stella Li
- Rui Xin
- Scott Geng
- Yiping Wang
- Sewoong Oh
- Simon Shaolei Du
- Nathan Lambert
- Sewon Min
- Ranjay Krishna
- Yulia Tsvetkov
- Hannaneh Hajishirzi
- Pang Wei Koh
- Luke Zettlemoyer
published_at: '2025-06-12 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Spurious Rewards: Rethinking Training Signals in RLVR

**Authors:** Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du, Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei Koh, Luke Zettlemoyer
**Published:** 2025-06-12 00:00:00
**Type:** paper

## Analysis

# Spurious Rewards: Rethinking Training Signals in RLVR
2025-06-12 · paper · Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang et al. (14 total)
https://arxiv.org/pdf/2506.10947

---

### Motivation & Prior Limitations
- RLVR has become a dominant post-training paradigm for improving mathematical reasoning, but the mechanisms underlying its gains remain poorly understood, making it unclear what role the reward signal actually plays.
  - A large body of recent RLVR research draws conclusions almost exclusively from experiments on Qwen2.5-Math models, raising the risk that findings reflect model-specific artifacts rather than general principles about reinforcement learning for language models.
  - Prior work using noisy or limited ground-truth labels (majority voting, one-shot RL) had already hinted that RLVR may not require high-quality supervision, but no work had systematically probed whether rewards with zero or negative correlation to correctness could still produce gains.
- The GRPO training objective contains a clipping term whose effect on gradient dynamics under uninformative rewards had not been formally characterised, leaving a mechanistic gap in understanding why weak supervision can suffice.

---

### Proposed Approach
- The paper introduces a controlled experimental framework using a progression of increasingly spurious binary reward functions — majority-vote, format, random (γ = 0.5), and deliberately incorrect — to probe the minimum supervision needed for RLVR to improve math performance, and then mechanistically explains the observed gains via an analysis of GRPO's clipping term.
  - Unlike prior work that studied noisy-but-correlated rewards, this paper includes rewards that are strictly uncorrelated (random) or negatively correlated (incorrect labels from majority voting), making it the most extreme test of reward necessity to date.
  - The mechanistic analysis shows that GRPO's clipping function introduces a gradient bias that amplifies tokens already high-probability under the base policy, even when rewards carry no task information: tokens whose old policy probability is high enough that the upper clipping threshold (π_old · (1 + ε_c)) exceeds 1.0 can never be suppressed, receiving unconditionally non-negative gradient updates.
- A focused case study on "code reasoning" — the behaviour of Qwen2.5-Math models writing Python code in their chain-of-thought without any code interpreter — is used to trace how RLVR with spurious rewards amplifies pre-existing high-prior behaviours rather than teaching new skills.
  - The paper validates the causal role of code reasoning through two explicit interventions: prompt-forcing (prepending "Let's solve this using Python") and a Python-string reward, both of which replicate the performance gains without any correctness signal.

---

### Results & Capabilities
- RLVR with GRPO using completely random rewards improves Qwen2.5-Math-7B by 21.4 absolute points on MATH-500, reaching 73% of the 29.1-point gain achieved with ground-truth rewards, and achieves similar proportional gains on AMC and AIME 2024.
  - Even incorrect-label rewards — deliberately trained to match wrong answers — yield a 24.1% gain on MATH-500 for Qwen2.5-Math-7B, only 5 points below ground-truth supervision.
  - On AIME 2025 (questions post-dating all model knowledge cutoffs), ground-truth rewards show a clearer advantage, with spurious rewards producing only −0.4% to +4.5% gains, suggesting that genuine new-knowledge tasks expose the limits of spurious elicitation.
- Removing the clipping term from GRPO completely eliminates the gains from random rewards across three independent ablation designs (disabled clipping, large mini-batch, single-gradient rollout), directly validating the mechanistic hypothesis.
- Code reasoning frequency in Qwen2.5-Math-7B increases from 65% before RLVR to over 90% within 15 training steps under any spurious reward, and the rise in code frequency tracks accuracy gains closely; with ground-truth rewards, code frequency eventually declines as natural-language reasoning improves instead, indicating a qualitatively different learning dynamic.
- Spurious rewards consistently fail to generalise beyond the Qwen family: OLMo2-7B and Llama3.1-8B show flat or negative performance changes under random and incorrect rewards, and even Qwen2.5 general-purpose models (not math-specialised) benefit less than Qwen2.5-Math variants.
  - Two recent published RLVR methods — Test-Time Reinforcement Learning (TTRL) and one-shot RL — when replicated in the paper's framework, show the same Qwen-specific pattern: strong gains on Qwen matching ground-truth performance, but failure to transfer to other model families.

---

### Implications
- The dominant use of Qwen2.5-Math as the de facto evaluation model for RLVR research creates a systematic replication risk: reported gains may reflect the amplification of Qwen-specific pretraining priors rather than genuine algorithmic progress, and methods validated only on this family should be treated with caution until confirmed on Llama, OLMo, or other architecturally distinct models.
- The finding that RLVR at open-source post-training compute scales elicits latent capabilities rather than instilling new ones has direct implications for how the field should interpret benchmark improvements: a large MATH-500 gain does not necessarily indicate that a model has learned to reason better, only that it has been steered toward a pre-existing high-accuracy behaviour pattern.
- Spurious and format rewards should be adopted as standard dummy baselines in RLVR evaluation: any proposed reward signal that cannot outperform a random reward on diverse model families provides weaker evidence of genuine contribution than currently assumed.
- The clipping-bias mechanism identified here suggests that GRPO's standard implementation contains an inductive bias toward exploiting high-prior behaviours, which interacts with the pre

## Key Claims

1. GRPO exhibits a clipping bias arising from its clip term, which amplifies high-prior behaviors learned during pre-training even without informative rewards.
2. Spurious rewards effective for Qwen models often fail to produce gains for other model families such as Llama3 or OLMo2.
3. Code reasoning frequency in Qwen2.5-Math-7B increases from 65% to over 90% when trained with spurious rewards.
4. Training Qwen2.5-Math-7B with incorrect label rewards yields a 24.1% absolute improvement on MATH-500, compared to 29.1% from ground truth rewards.
5. All reward functions, including pathologically designed ones (random, incorrect), lead to significant improvements in Qwen2.5-Math math performance within the first 50 training steps.
6. Without the clipping term in GRPO, random rewards fail to yield consistent performance improvements.
7. GRPO's clipping bias asymmetrically suppresses low-probability tokens and reinforces high-probability ones, even when rewards are uninformative.
8. Qwen2.5-Math-7B generates Python code in 65.0% of reasoning responses on MATH-500 even without access to a code interpreter.
9. In Qwen2.5-Math-7B, responses containing code reasoning achieve 60.9% accuracy on MATH-500, compared to 28.0% for responses without code.
10. Under RLVR with spurious rewards, Qwen2.5-Math-7B code reasoning frequency rapidly increases to approximately 90% within 15 training steps.

## Capabilities

- RLVR training with GRPO can elicit substantial math reasoning improvements (21.4% on MATH-500) in Qwen2.5-Math models even with completely random or incorrect reward signals, by amplifying pre-existing high-prior reasoning behaviors from pretraining
- Qwen2.5-Math models possess a latent 'code reasoning' capability — generating structured Python reasoning chains without code execution — that achieves 60.9% accuracy on MATH-500 versus 28.0% for natural language reasoning on the same model
- Simple prompt-based elicitation of code reasoning ('Let's solve this using Python') improves MATH-500 accuracy by 15–24% on Qwen2.5-Math models without any training
- The GRPO clipping mechanism's training dynamics can be analytically characterised: it asymmetrically reinforces high-probability tokens (cannot exceed upper clip bound since probability ≤ 1) and suppresses low-probability ones, creating a reward-agnostic amplification signal

## Limitations

- RLVR training dynamics and gains are highly model-family dependent: spurious rewards reliably improve Qwen2.5 and Qwen2.5-Math models but yield flat or negative results for Llama3 and OLMo2 families
- At current open-source compute scales, RLVR does not teach models genuinely new reasoning capabilities but instead elicits latent capabilities already present in the base model from pretraining
- GRPO's clipping term creates a systematic prior-amplification training signal independent of reward quality, meaning that measured RLVR gains conflate genuine reward-guided learning with reward-agnostic prior amplification
- Spurious reward gains do not transfer to truly novel problems: on AIME2025 (post-knowledge-cutoff questions), ground truth rewards show a clear advantage over all spurious reward variants
- Qwen2.5-Math-7B evaluation performance is highly sensitive to prompt variations — a task-irrelevant 'spurious prompt' can sometimes produce anomalously high initial performance, undermining the reliability of benchmark measurements
- The RLVR research field has a systematic validation gap: conclusions are drawn primarily from Qwen models, and the same methods often fail to generalise to Llama or OLMo2 families
- Code reasoning elicitation is model-specific: forcing code reasoning in Llama3 and OLMo2 models actively degrades math performance by 21–29%, since these families lack effective code-reasoning pretraining priors
- Models already post-trained with RL see minimal gains under nearly all reward conditions, suggesting a saturation ceiling once pretraining priors have been fully amplified by an initial RL pass

## Bottlenecks

- RLVR research conclusions are systematically unvalidated across model families: the field's de facto reliance on Qwen2.5-Math as the primary evaluation platform means most published RLVR findings have unknown generalisability, and spurious baselines are absent from standard evaluation
- RLVR is fundamentally constrained by pretraining priors at current compute scales: the algorithm amplifies reasoning strategies the base model already possesses but cannot develop genuinely new capabilities absent from pretraining data

## Breakthroughs

- Demonstration that RLVR gains in Qwen2.5-Math arise substantially from GRPO clipping bias amplifying pretraining priors rather than from reward signal quality: random and incorrect rewards achieve 74–83% of ground-truth reward gains, with a mechanistic explanation via the clip term's asymmetric grad

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/amc|AMC]]
- [[entities/grpo|GRPO]]
- [[entities/pass1|Pass@1]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/test-time-reinforcement-learning-ttrl|Test-Time Reinforcement Learning (TTRL)]]
