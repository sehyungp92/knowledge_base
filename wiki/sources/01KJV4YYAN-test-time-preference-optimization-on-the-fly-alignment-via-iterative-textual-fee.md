---
type: source
title: 'Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual
  Feedback'
source_id: 01KJV4YYANBM1GBBMZN5JZ41KC
source_type: paper
authors:
- Yafu Li
- Xuyang Hu
- Xiaoye Qu
- Linjie Li
- Yu Cheng
published_at: '2025-01-22 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- post_training_methods
- reinforcement_learning
- reward_modeling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback

This paper introduces Test-Time Preference Optimization (TPO), a framework that achieves RLHF/DPO-level alignment quality purely at inference time — without updating model parameters — by translating numerical reward signals into natural-language critiques that iteratively steer a model's own outputs, demonstrating that an unaligned SFT model can surpass its fully trained aligned counterpart in under two revision steps at less than 0.01% of training compute.

**Authors:** Yafu Li, Xuyang Hu, Xiaoye Qu, Linjie Li, Yu Cheng
**Published:** 2025-01-22
**Type:** paper

## Motivation

[[themes/alignment_methods|Alignment methods]] like RLHF and DPO fold preference signal directly into model weights via gradient-based updates over large datasets. Training Llama-3.1-70B-DPO on 64k examples at max length 2,048 requires approximately 72,840 PFLOPs — a cost that must be repeated every time preferences, safety requirements, or target distributions shift. This makes rapid adaptation expensive and operationally inflexible.

Prior inference-time alternatives — Best-of-N sampling, tree search (MCTS, TreeBoN), token-level reward guidance — treat the reward model as a passive scorer rather than an interactive environment. They scale in *sample count* but not in *response quality per sample*: they collect high-reward outputs without executing feedback-driven revision. No prior work had shown that an unaligned (SFT-only) model could match or exceed a strongly RLHF-aligned counterpart purely at inference time.

## Approach

TPO reframes gradient descent as a sequence of textual operations on the model's *outputs* rather than its *parameters*. The analogy is explicit: the generated response is treated as the "variable" being optimized, and numerical gradients are replaced by three prompt-driven LLM calls per iteration:

1. **Textual loss computation** — a prompt (P_loss) identifies strengths in the highest-reward candidate and weaknesses in the lowest-reward candidate from a maintained response cache.
2. **Textual gradient derivation** — specific, actionable improvement instructions are derived from the loss description.
3. **Variable update** — N new candidate responses are generated conditioned on the textual gradient.

Formally, TPO searches for an optimal *contextual parameter* ϕ that reshifts the output distribution p(y_w | ϕ; θ, x) with θ fixed — contrasting with DPO/RLHF which fold the reward signal into θ. The reward model functions strictly as an environment providing scalar feedback; all interpretation and generation is performed by the policy model itself, exploiting its instruction-following capability as an alignment resource.

The cache retains all responses across iterations. At each step, the globally highest- and lowest-scoring responses are selected as the next chosen/rejected pair, combining **parallel sampling** (width N) with **sequential revision** (depth D). This is implemented on the TextGrad framework with a custom preference-oriented loss prompt.

## Results

| Setting | AlpacaEval 2 LC | Arena-Hard WR |
|---|---|---|
| Llama-3.1-70B-Instruct (baseline) | 36.9% | 59.0% |
| Llama-3.1-70B-SFT + TPO D2-N5 | — | 70.5% |
| Llama-3.1-70B-SFT + TPO D5-N20 | 37.8% | 77.5% |
| Mistral-Small-Instruct-2409 (22B) + TPO | 53.4% | 72.2% |

Key quantitative findings:

- **Unaligned surpasses aligned:** After two TPO iterations, Llama-3.1-70B-SFT surpasses Llama-3.1-70B-Instruct on all metrics and exceeds Llama-3.1-405B-Instruct's Arena-Hard win rate.
- **Small model reach:** A 22B Mistral model with TPO reaches GPT-4-Turbo-comparable performance on AlpacaEval 2 (LC 53.4%).
- **Depth beats breadth:** TPO-D2-N5 (15 total samples) outperforms Best-of-N with 30 samples (65.2% avg win rate) and BoN-60 (57.5%), demonstrating that sequential revision is more compute-efficient than scaling sample count.
- **Inference stability:** Applying TPO to the unaligned SFT model reduces the standard deviation of reward scores across generations, making it more deterministic than the pre-TPO aligned Instruct model.
- **Compute:** Total inference cost is approximately 9.3 PFLOPs per query — less than 0.01% of the ~72,840 PFLOPs needed to train the DPO baseline.

## Capabilities

- **Inference-time alignment without weight updates.** [[themes/alignment_and_safety|Alignment]] quality matching or exceeding full RLHF/DPO training is achievable purely at runtime. This establishes alignment as a *runtime property* rather than a fixed training artifact. *(maturity: demo)*
- **Textual gradient descent.** LLMs can perform optimization in natural language space — interpreting numerical reward feedback, generating critique, and steering their own output distribution. Strong instruction-following capability is itself an alignment resource. *(maturity: demo)*
- **Complementary scaling axes.** [[themes/test_time_learning|Test-time compute scaling]] via depth (sequential revision) and width (parallel sampling) are complementary and jointly effective; depth outperforms width alone at equal sample budgets. *(maturity: demo)*

## Limitations & Open Questions

**Capability floor.** TPO fails on smaller models lacking sufficient instruction-following ability. Llama-3.1-8B-Instruct shows *decreasing* reward scores over successive TPO iterations rather than improving. The threshold of capability required is undetermined, blocking deployment on cost-efficient small models. *(severity: significant, trajectory: improving)*

**Reward model proxy ceiling.** TPO optimizes toward a reward model, not true human preferences. Any biases, exploitability, or distributional gaps in the [[themes/reward_modeling|reward model]] become both the ceiling and the primary distortion source for all aligned outputs. Benchmark evaluations rely entirely on reward model scores and GPT-4-as-judge, with no evaluation against actual human preferences. *(severity: significant, trajectory: stable)*

**Diminishing returns after step one.** The first revision yields the largest improvement; subsequent steps are comparatively marginal. This practically caps useful depth in most deployment settings. *(severity: minor, trajectory: stable)*

**Multiplicative inference cost.** TPO multiplies inference cost by N×D plus three additional LLM calls per iteration (loss, gradient, update). Despite being orders of magnitude cheaper than training, this is a non-trivial multiplier at deployment scale. *(severity: significant, trajectory: stable)*

**External reward model dependency.** TPO requires a capable reward model to be co-deployed at inference time — an infrastructure dependency that makes the approach inapplicable where no suitable reward model exists. *(severity: significant, trajectory: improving)*

**No TPO-specific training.** The policy models used were not trained for TPO subtasks (textual loss calculation, gradient computation). Performance is therefore a lower bound; specialized training may yield substantial further gains. *(severity: minor, trajectory: improving)*

**Safety claims are unverified under adversarial pressure.** BeaverTails and XSTest improvements are measured by classifiers with no adversarial testing. The same test-time mechanism that improves safety compliance could in principle be exploited to degrade it. *(severity: significant, trajectory: unclear)*

## Bottlenecks Addressed & Created

TPO contributes to [[themes/test_time_learning|test-time compute scaling]] by demonstrating that iterative textual revision is a productive search mechanism alongside purely sampling-based methods. However, it surfaces two new bottlenecks:

1. **Small-model capability floor** — blocking democratisation of inference-time alignment beyond large frontier models. *(horizon: 1–2 years)*
2. **Reward model quality as hard ceiling** — reliable test-time alignment that generalises to true human preferences requires reward models that are themselves unbiased and unexploitable. *(horizon: 1–2 years)*

## Implications

**For [[themes/alignment_methods|alignment research]]:** The decoupling of preference signal from the training pipeline implies that reward models should be designed as interactive environments, not static loss supervisors. Reward model interpretability and robustness become first-class concerns for inference-time alignment.

**For [[themes/post_training_methods|post-training methods]]:** TPO suggests that some portion of alignment work currently performed at training time could be deferred to inference — reducing the need for large preference datasets and enabling rapid re-targeting of deployed models as requirements evolve.

**For [[themes/reinforcement_learning|RL-based training]]:** The textual gradient mechanism is a plausible candidate for fine-tuning signal generation — particularly for tasks where differentiable reward functions are unavailable but language critiques can be generated.

**For safety and [[themes/alignment_and_safety|AI safety]]:** The ability to shift safety-relevant model behaviour post-deployment without weight updates is a double-edged finding. It suggests deployed safety properties may be adjustable at inference time — which is both a correction capability and a potential attack surface.

## Key Claims

- Training-time alignment (RLHF, DPO) requires iterative retraining that hinders adaptation to evolving distributions.
- TPO performs gradient descent in textual form: loss calculation, gradient computation, and variable update — all in natural language.
- TPO searches for an optimal *contextual parameter* ϕ rather than optimal model weights θ.
- The highest- and lowest-scoring responses among candidates serve as the chosen/rejected pair for textual loss computation.
- After two TPO steps, an unaligned SFT model can match or exceed fully aligned models trained on tens of thousands of samples.
- The first optimization step yields the largest improvement; subsequent steps are comparatively less impactful.
- TPO can be viewed as a synthesis of parallel sampling and sequential revision from the test-time scaling perspective.
- TPO-D2-N5 (15 samples total) surpasses BoN-30 and BoN-60 on average GPT-4 win rate.
- Increasing search width from 5 to 20 consistently boosts performance before plateauing; smaller width can be compensated by additional revision rounds.
- TPO fails on Llama-3.1-8B-Instruct — a foundational level of instruction-following proficiency is necessary for the approach to succeed.

## Related Themes

- [[themes/alignment_and_safety|Alignment & Safety]]
- [[themes/alignment_methods|Alignment Methods]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/test_time_learning|Test-Time Learning]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/length-controlled-win-rate|Length-Controlled Win Rate]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/textgrad|TextGrad]]
