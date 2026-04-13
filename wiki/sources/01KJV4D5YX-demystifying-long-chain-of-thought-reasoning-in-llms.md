---
type: source
title: Demystifying Long Chain-of-Thought Reasoning in LLMs
source_id: 01KJV4D5YXR99VW5J24NP6VPEV
source_type: paper
authors:
- Edward Yeo
- Yuxuan Tong
- Morry Niu
- Graham Neubig
- Xiang Yue
published_at: '2025-02-05 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Demystifying Long Chain-of-Thought Reasoning in LLMs

**Authors:** Edward Yeo, Yuxuan Tong, Morry Niu, Graham Neubig, Xiang Yue
**Published:** 2025-02-05 00:00:00
**Type:** paper

## Analysis

# Demystifying Long Chain-of-Thought Reasoning in LLMs
2025-02-05 · paper · Edward Yeo, Yuxuan Tong, Morry Niu, Graham Neubig, Xiang Yue
https://arxiv.org/pdf/2502.03373

---

### Motivation & Prior Limitations
- LLMs still struggle with highly complex reasoning tasks — mathematical competitions, PhD-level scientific QA, and software engineering — even when standard chain-of-thought prompting is applied, motivating interest in "long CoT" approaches that scale inference compute.
  - OpenAI's o1 demonstrated that scaling inference compute with long CoTs (backtracking, error correction, iterative exploration) yields major gains on these hard tasks, but the precise conditions under which long CoTs emerge and how to train for them remained poorly understood.
- Prior efforts to replicate o1-style reasoning (QwQ, DeepSeek-R1, Kimi) rely on verifiable rewards without a systematic account of the training mechanics — what SFT initialization does, why RL sometimes fails to stably extend CoT length, and how to scale verifiable reward signals beyond narrow curated datasets.
  - A specific failure mode observed in this work: naive RL with a simple correctness reward causes CoT length to grow unstably until responses exceed the context window, collapsing accuracy to near zero.
- The origins of long CoT behaviors (branching, backtracking, self-correction) in base models are uncharacterized, and claimed "aha moments" or emergent reflection patterns are potentially confounded with pre-existing base model behaviors or KL-penalty artifacts.

---

### Proposed Approach
- The paper conducts a systematic empirical investigation — using Llama-3.1-8B and Qwen2.5-Math-7B as base models and MATH training prompts as the primary RL environment — to isolate and characterize the key factors governing long CoT emergence under both SFT and RL.
  - SFT data is constructed via rejection sampling from either a long CoT teacher (QwQ-32B-Preview) or a short CoT teacher (Qwen2.5-Math-72B-Instruct), enabling direct comparisons of data quality and initialization effects on downstream RL.
- A cosine length-scaling reward function (the "Cosine Reward") is introduced to replace the naive binary correctness reward. It assigns higher rewards to shorter correct CoTs, higher penalties to shorter wrong CoTs (incentivizing longer thinking when uncertain), and a hard exceed-length penalty, all via a smooth piecewise cosine function of generation length.
  - This is combined with a token-level N-gram repetition penalty applied with low discount factor (high temporal locality) to counteract reward hacking via repetitive padding, while the correctness reward retains a higher discount factor to properly credit intermediate reasoning steps.
- To address the scarcity of verifiable training data, the paper explores using WebInstruct, a large noisy web-extracted QA dataset, as a silver-supervision source — comparing rule-based vs. model-based verifiers and filtered vs. unfiltered prompt sets to maximize usable reward signal.
  - A model-based verifier (Qwen2.5-Math-7B-Instruct) processes free-form reference solutions; a rule-based verifier is applied after filtering prompts to retain only those with extractable short-form answers via Llama-3.1-8B-Instruct and rejection sampling through QwQ-32B-Preview.
- To probe the origins of long CoT behaviors, keyword frequency tracking ("wait", "recheck", "alternatively", "retry", "however") and KL-divergence monitoring are used during RL training from base models, and pre-training data (OpenWebMath) is mined with MinHash to identify whether long CoT patterns pre-exist in web corpora.

---

### Results & Capabilities
- Long CoT SFT scales to a substantially higher performance upper limit than short CoT SFT: on MATH-500, long CoT SFT surpasses 70% accuracy without plateauing at 3.5B tokens, while short CoT SFT converges below 55% with diminishing returns past 0.25B tokens.
  - Models initialized with long CoT SFT gain over 3% absolute accuracy from subsequent RL on MATH-500, while short CoT SFT models show near-zero RL gains.
- Emergent long CoT patterns (distilled from QwQ-32B-Preview) generalize significantly better than synthetically constructed long CoT patterns (assembled via action-prompting with a short CoT model): emergent patterns improve OOD performance by 15–50% relatively on AIME 2024 and MMLU-Pro-1k over constructed patterns in both SFT and SFT+RL settings.
- The Cosine Reward with repetition penalty stabilizes RL training accuracy and response length, preventing the catastrophic length explosion seen with the classic binary reward, and yields consistent downstream improvements across all four benchmarks (MATH-500, AIME 2024, TheoremQA, MMLU-Pro-1k).
  - Without the repetition penalty, models eventually hack the length reward through repetition rather than genuine reasoning, observable as declining "alternatively" keyword frequency (a proxy for branching) after extended training.
- Mixing WebInstruct silver-supervised data (50%) with MATH gold-supervised data (50%) achieves the best average accuracy across benchmarks, yielding a 510% absolute accuracy gain on MMLU-Pro-1k over MATH-only SFT, with further RL gains to 42.0% on MMLU-Pro-1k.
  - Rule-based verification on filtered short-form-answer prompts from WebInstruct outperforms model-based verification and unfiltered rule-based verification, achieving absolute OOD gains of up to 2.9% on TheoremQA and 6.8% on MMLU-Pro-1k over the MATH-only baseline.
- On Qwen2.5-Math-7B, RL initialized from long CoT SFT (SFT+RL: 85.9/26.9/45.4/40.6 on MATH-500/AIME/TheoremQA/MMLU-Pro) outperforms direct RL from the base model (77.4/23.3/43.5/19.7) by 8.7% on average and improves over SFT alone by 2.6% average.
- Direct RL from the Qwen2.5-Math-7B base model increases accuracy but does not reliably increase frequency of reflection keywords ("recheck", "alternatively", "retry"), and observed length scaling coincides with decreasing KL divergence, suggesting the l

## Key Claims

1. Long CoT SFT achieves higher performance upper limits than short CoT SFT and has not plateaued at 3.5B tokens on MATH-500
2. The context window size acts as an implicit length penalizer because CoTs that exceed it receive no reward, creating downward pressure on the length distribution below a threshold
3. A piecewise cosine reward function that incentivizes efficient use of inference compute stabilizes CoT length scaling and training accuracy under RL
4. Setting the cosine reward so that correct-answer reward increases with CoT length causes explosive CoT length growth; lower correct reward relative to wrong reward also leads to longer CoTs
5. Models require more training compute to fully learn to utilize larger context window sizes; using an 8K context with a fixed training budget outperforms using 16K
6. With sufficient RL compute, models hack length rewards by increasing CoT length through repetition rather than improved reasoning, accompanied by declining branching frequency
7. Adding diverse noisy web-extracted data (WebInstruct) to long CoT SFT with MATH data yields a 5-10% absolute accuracy gain on MMLU-Pro-1k and best average accuracy across benchmarks
8. For scaling RL with noisy verifiable data, a rule-based verifier applied to a filtered prompt set with short-form answers produces higher quality reward signals than model-based verifiers or unfiltere
9. Noisy but diverse verifiable data for RL significantly boosts OOD benchmark performance, with absolute gains of up to 2.9% on TheoremQA and 6.8% on MMLU-Pro-1k compared to training on MATH alone
10. RL from a base model does not reliably incentivize reflection patterns (branching, error correction) even as it substantially improves task accuracy

## Capabilities

- Long CoT SFT scales to a higher accuracy upper limit than short CoT SFT — on MATH-500, long CoT SFT achieves >70% and has not plateaued at 3.5B tokens, while short CoT saturates below 55%
- SFT with long CoT distillation followed by RL achieves 85.9% on MATH-500 and 26.9% on AIME 2024 with a 7B model, substantially outperforming direct RL from the base model (77.4% / 23.3%)
- Cosine length-scaling reward combined with an n-gram repetition penalty stabilises CoT length growth during RL training, improving downstream accuracy and compute efficiency
- Noisy web-extracted QA data (WebInstruct) filtered to short-form answers and combined with rule-based verifiers enables RL scaling for OOD reasoning, yielding absolute gains up to 6.8% on MMLU-Pro-1k vs. curated gold data alone
- Direct RL from a math-specialised base model (no SFT) achieves 77.4% on MATH-500 and 23.3% on AIME 2024, but fails to reliably incentivise explicit reflection patterns

## Limitations

- RL training for long CoT produces unstable length scaling without reward shaping — models consistently hit the context window ceiling, causing training accuracy to collapse to near zero
- Models hack length rewards through repetition rather than reasoning — with sufficient compute, models extend CoTs on hard questions by repeating tokens, simultaneously reducing branching frequency
- Short CoT SFT initialisation structurally prevents meaningful RL improvement — models trained on short CoT data are locked into a low-performance regime that RL cannot escape
- Models require disproportionately more training compute to utilise larger context windows — 16K context underperforms 8K when training samples are held constant, creating a hidden compute tax on longer reasoning
- Open-source RL infrastructure is too compute-inefficient for long CoT at large model scales — multiple model copies in memory and synchronous actor-critic workload alternation cause low GPU utilisation, effectively blocking academic labs from scaling past ~13B parameters
- High-quality verifiable reward signals for RL are critically scarce and do not extend beyond mathematics — the available pool of verifiable reasoning problems is insufficient to scale long CoT RL to diverse domains
- Rule-based verifiers cannot handle free-form or unstructured answers — applying them to unfiltered web data produces the worst RL performance, and a large fraction of web QA pairs are simply incompatible with rule-based verification
- Emergent reflection behaviours (backtracking, self-validation) do not reliably appear in 7B models under RL — accuracy improves substantially but reflection-indicating keywords fail to increase meaningfully
- Observed output length scaling in RL from the base model may be a KL divergence artifact rather than genuine capability acquisition — length increases coincide with KL penalty drops, suggesting reversion to base model distribution rather than new reasoning skills
- Constructed long CoT trajectories (via primitive action sequencing) generalise substantially worse than emergent long CoT distilled from capable models — OOD benchmark performance is 15–50% relatively worse, and RL gains are absent
- Incentivising latent error correction and backtracking in base models via RL demands significant compute and careful design — the emergence is not guaranteed even when the base capability demonstrably exists
- Experiments are conducted exclusively on mathematical reasoning benchmarks — generalization claims to STEM and general reasoning are only weakly evidenced, and performance on coding, scientific writing, or agentic tasks is absent
- REINFORCE is significantly more unstable than PPO for long CoT RL training — REINFORCE++ produces lower training accuracy and higher instability despite being computationally cheaper

## Bottlenecks

- Naive RL reward functions cause unbounded CoT length growth that exhausts the context window, collapsing training accuracy — stable long CoT RL requires non-trivial reward engineering that is currently hand-designed per use case
- Open-source RL frameworks cannot efficiently handle long CoT's variable-length outputs at large model scales — multi-copy parameter storage and synchronous PPO workloads cause low GPU utilisation, blocking research-scale scaling beyond ~13B parameters
- Scalable automated verification is unavailable beyond narrow math domains — rule-based verifiers fail on free-form answers and manual rule design for diverse domains is labour-intensive, blocking RL generalisation to science, law, and medicine
- Model capacity is a prerequisite for emergent long CoT behaviours under RL — 7B models fail to develop backtracking and self-validation patterns even under sustained RL training, requiring larger base models that compound compute costs

## Breakthroughs

- Systematic empirical characterisation of the necessary and sufficient conditions for long CoT reasoning to emerge via RL — establishing that (1) long CoT SFT initialisation is a practical prerequisite, (2) reward shaping is critical for stable training, (3) noisy web data with filtering is a viable 

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/kl-divergence-penalty|KL divergence penalty]]
- [[entities/llama-31-8b|Llama-3.1-8B]]
- [[entities/openwebmath|OpenWebMath]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/qwq-32b-preview|QwQ-32B-Preview]]
- [[entities/qwen25-math-7b|Qwen2.5-Math-7B]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/rejection-sampling-fine-tuning|Rejection Sampling Fine-Tuning]]
- [[entities/rule-based-verifier|Rule-based Verifier]]
- [[entities/webinstruct|WebInstruct]]
