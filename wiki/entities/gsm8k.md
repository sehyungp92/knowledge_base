---
type: entity
title: GSM8K
entity_type: metric
theme_ids:
- adaptive_computation
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- latent_reasoning
- model_architecture
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.0037006884085924612
staleness: 0.0
status: active
tags: []
---
# GSM8K

**Type:** metric
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Grade School Math 8K benchmark measuring exact match on mathematical word problems. Classified by the authors as requiring reasoning.

## Key Findings

1. The R3 framework bootstraps solely from the model's own outputs without relying on external LLMs. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
2. Qwen-2-7B Instruct after GRPO training outperforms vanilla Qwen-2-72B Instruct on function calling when both models are given two attempts. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
3. During inference, the Free Transformer samples Z from a uniform prior over one-hot vectors, with no encoder required at generation time. (from "The Free Transformer")
4. Smaller fine-tuned models (1.5B to 7B parameters) can outperform models in the same family that are 10 times larger. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
5. In the R3 framework, only the tokens generated during the self-reflection phase are rewarded, not the tokens of the correct answer. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
6. The Free Transformer uses a Binary Mapper to convert H=16 logits into a one-hot vector of dimension 2^H = 65,536 with gradient pass-through via sigmoid monotonicity. (from "The Free Transformer")
7. Decoder Transformers do not make explicit latent decisions about the stream of symbols to generate; their only decisions are the choices of the tokens themselves. (from "The Free Transformer")
8. OPTIMUS (2020) was a prior work combining a pre-trained BERT encoder with a GPT-2 decoder fine-tuned with a VAE-like loss, using a CLS token to compute the latent embedding. (from "The Free Transformer")
9. The Free Transformer extends the decoder Transformer by conditioning its generative process on random latent variables learned without supervision via a variational procedure. (from "The Free Transformer")
10. MobileLLM-R1-950M achieves an AIME score of 15.5, dramatically outperforming OLMo-2-1.48B (0.6) and SmolLM-2-1.7B (0.3) despite having fewer parameters. (from "MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes")
11. The Reflect, Retry, Reward framework achieves up to 34.7% improvement at math equation writing and 18.1% improvement at function calling. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
12. The R3 framework requires only a binary success/failure signal from a response verifier, making it suitable for tasks where success can be easily verified. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")
13. The Free Transformer injects the latent random state Z at the middle layer of the decoder, sharing the first half of Transformer blocks between encoder and decoder to minimize overhead. (from "The Free Transformer")
14. The Free Transformer requires only a single additional non-causal Transformer block and two linear layers for the encoder, resulting in 3.6% compute/memory overhead for the 1.5B model and 3.1% for the (from "The Free Transformer")
15. On Countdown math equation solving, GRPO-trained models improved performance by an average of 16.0% on the 15,000-sample test set. (from "Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning")

## Capabilities

- LMs augmented with synthetic latent thoughts achieve dramatically improved math reasoning data efficiency: a 1.1B TinyLlama reaches 25.4% on MATH and 33.6% on GSM8K with only 480M raw tokens, versus 5 (maturity: research_only)

## Known Limitations

- BoLT bootstrapping causes few-shot GSM8K performance to degrade across iterations even as MATH performance improves and finetuned GSM8K improves — indicating that extended optimization on math-heavy c (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
