---
type: source
title: 'Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language
  Models'
source_id: 01KJV2XQ8NBRP17VKK27RKV3JR
source_type: paper
authors:
- Wenxuan Huang
- Bohan Jia
- Zijie Zhai
- Shaosheng Cao
- Zheyu Ye
- Fei Zhao
- Zhe Xu
- Xu Tang
- Yao Hu
- Shaohui Lin
published_at: '2025-03-09 00:00:00'
theme_ids:
- chain_of_thought
- multimodal_models
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models

**Authors:** Wenxuan Huang, Bohan Jia, Zijie Zhai, Shaosheng Cao, Zheyu Ye, Fei Zhao, Zhe Xu, Xu Tang, Yao Hu, Shaohui Lin
**Published:** 2025-03-09 00:00:00
**Type:** paper

## Analysis

# Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models
2025-03-09 · paper · Wenxuan Huang, Bohan Jia, Zijie Zhai, Shaosheng Cao, Zheyu Ye et al. (10 total)
https://arxiv.org/pdf/2503.06749

---

### Motivation & Prior Limitations
- Multimodal Large Language Models (MLLMs) lack the complex, human-like Chain-of-Thought (CoT) reasoning that has emerged in text-only LLMs like DeepSeek-R1, limiting their performance on tasks requiring logical inference, questioning, and self-reflection.
  - Existing multimodal CoT datasets are constructed via human heuristics in a step-by-step form, yielding "Pseudo-CoT" that lacks natural cognitive processes such as questioning, reflection, and self-inspection — resulting in only shallow reasoning capability.
  - Methods like LLaVA-CoT-11B (54.8% MathVista) and Mulberry-7B (63.1% MathVista) represent the prior open-source reasoning MLLM ceiling, significantly below closed-source OpenAI O1 (73.9%).
- Directly applying the DeepSeek-R1-Zero paradigm — pure RL without initialization data — fails to incentivize complex reasoning in MLLMs due to the absence of large-scale, high-quality multimodal reasoning data and the high compute required for prolonged training.
  - Vision-R1-Zero, trained with direct RL on 10K multimodal math problems, achieves only 50.7% average accuracy and produces only short, low-complexity CoT chains (avg. 1,285 output tokens), failing to generalize from the limited data.
- Cold-start initialization alone introduces an "Overthinking Optimization Problem": after SFT on complex CoT data, the model engages in excessively long but incorrect reasoning chains, concentrating correct reasoning processes in shorter sequences and making subsequent RL optimization unstable.
  - Vision-R1-CI (cold-start initialized, no RL) achieves only 44.5% average accuracy despite producing much longer outputs (avg. 3,566 tokens), and directly applying RL to it (Vision-R1-Long) yields only 47.7%, showing optimization difficulty rather than improvement.

---

### Proposed Approach
- Vision-R1 combines two stages: (1) cold-start initialization via a novel **Modality Bridging** technique to construct 200K human-annotation-free multimodal CoT samples, followed by (2) RL training using **Progressive Thinking Suppression Training (PTST)** with Group Relative Policy Optimization (GRPO) to mitigate overthinking and incrementally develop complex reasoning.
  - Unlike prior multimodal CoT construction (human heuristics, step-by-step templates), Modality Bridging converts visual information into text by first prompting an MLLM to generate a Pseudo-CoT that explicitly exposes necessary visual details, then using that Pseudo-CoT alongside the original image-question to generate a richer textual description, which is finally passed to the text-only DeepSeek-R1 to produce high-quality, self-reflective CoT reasoning.
  - The resulting Vision-R1-cold dataset contains dramatically more self-reflective markers than prior datasets: "Wait" appears 585,719 times vs. 2,300 in LLaVA-CoT (100K) and 1,122 in Mulberry (260K), quantifying the qualitative difference in cognitive process fidelity.
- PTST addresses the Overthinking Optimization Problem by imposing a hard sequence-length constraint at early RL stages (4K tokens, 16 samples per group) to force the model to learn correct, compressed reasoning, then progressively relaxing the constraint in later stages (8K tokens, 8 samples per group) to allow the model to autonomously extend reasoning for harder problems.
  - Unlike standard GRPO with a soft formatting reward, PTST uses a **hard formatting result reward function (HFRRF)** where reward ri = 1 only when both format and answer correctness are simultaneously satisfied (binary reward), preventing the model from gaming partial credit with long, incorrect chains.
  - No system prompt is used during RL training because cold-start initialization already instills robust formatting capability; the length constraint in PTST acts as the sole structural regulator.
- The base model for all 7B experiments is Qwen2.5-VL-7B; larger variants (32B, 72B) use correspondingly scaled Qwen2.5-VL bases with additional RL training data beyond the core 10K dataset.

---

### Results & Capabilities
- Vision-R1-7B achieves 73.5% on MathVista, only 0.4% below OpenAI O1 (73.9%), while surpassing its 7B base model Qwen2.5-VL-7B by +5.4% and outperforming all other open-source reasoning MLLMs by a substantial margin.
  - On fine-grained MathVista sub-tasks, Vision-R1-7B scores 80.3% (GEO), 79.0% (ALG), and 83.2% (GPS), exceeding Qwen2.5-VL-7B by +13.4%, +10.3%, and +16.4% respectively — improvements concentrated in the hardest geometric and algebraic subtasks.
  - Vision-R1-7B achieves these results using only 10K multimodal math problems for RL training, demonstrating strong data efficiency.
- Scaling to larger models yields further gains: Vision-R1-32B scores 76.4% and Vision-R1-72B scores 78.2% on MathVista, with both improving over their respective Qwen2.5-VL bases by ~4.7% and achieving ~10% average accuracy gains across MathVista, MathVerse, and MM-Math.
  - Vision-R1-72B achieves 63.2% on MathVerse and 66.4% on MM-Math, representing +8.9% average improvement over Qwen2.5-VL-72B across all benchmarks.
- Vision-R1-7B generalizes beyond math: when the cold-start data is applied to Llama-3.2-11B-V, the resulting Vision-R1-LlamaV-CI-11B achieves state-of-the-art results across all tested general benchmarks (MMStar: 61.4, ChartQA: 83.9, MME: 2190, HallBench: 49.5) as well as math benchmarks, outperforming both LLaVA-CoT-11B and Mulberry-Llama-11B — demonstrating that the cold-start data quality transfers across base models and domains.
- The model qualitatively exhibits the "Aha moment" phenomenon — self-generated questioning, backtracking, and verification mid-reasoning — analogous to what DeepSeek-R1 demonstrated in text-only settings, representing a genuine emergence of structured c

## Key Claims

1. Direct RL training without cold-start initialization struggles to activate complex reasoning capabilities (questioning, reflection) in MLLMs due to the absence of large-scale, high-quality multimodal 
2. Vision-R1-7B achieves 73.5% accuracy on MathVista, only 0.4% lower than OpenAI O1, using only 10K multimodal math data during RL training.
3. Vision-R1-32B and Vision-R1-72B achieve 76.4% and 78.2% on MathVista respectively when scaling up RL training data.
4. Vision-R1-7B with only 7B parameters achieves performance comparable to state-of-the-art MLLMs with over 70B parameters on math reasoning tasks.
5. Manually constructed multimodal CoT datasets result in 'Pseudo-CoT' reasoning that lacks essential cognitive processes (questioning, reflection, inspecting), limiting effectiveness on complex vision r
6. Cold-start initialization with a 200K multimodal CoT dataset followed by RL training (GRPO) outperforms direct RL-only training on MLLMs.
7. After cold-start initialization, the MLLM exhibits an Overthinking Optimization Problem: correct reasoning processes tend to concentrate in shorter CoT sequences, while extended reasoning lengths do n
8. Progressive Thinking Suppression Training (PTST) resolves the overthinking optimization problem by initially constraining reasoning length and progressively relaxing it, enabling correct reasoning int
9. PTST uses a staged approach with sequence length limits of 4K, 8K, and 16K tokens per stage and group counts of 16, 8, and 4 respectively; Vision-R1 achieves competitive performance after only two sta
10. The Hard Formatting Result Reward Function (HFRRF) assigns reward=1 only when both format requirements and answer correctness are simultaneously satisfied, otherwise reward=0.

## Capabilities

- Cold-start initialization on automated high-quality multimodal CoT data combined with GRPO RL training (PTST) enables MLLMs to develop human-like complex reasoning with questioning and self-reflection, achieving performance comparable to models 10x larger
- Automated construction of large-scale (200K) high-quality multimodal CoT datasets without human annotations via modality bridging — converting visual information to text for a text-only reasoning LLM, then pairing the resulting complex CoT back with the original images
- Vision-R1-7B achieves 73.5% on MathVista — within 0.4% of OpenAI O1 — using only 7B parameters trained with 10K RL examples, demonstrating near-frontier multimodal math reasoning at modest scale
- Progressive Thinking Suppression Training (PTST) resolves the overthinking optimization problem in cold-started MLLMs by progressively relaxing reasoning length constraints (4K→8K tokens) during RL, guiding models to first learn correct short reasoning then extend to complex problems

## Limitations

- Direct RL training on MLLMs without cold-start initialization fails to activate complex reasoning (questioning, reflection, self-correction) — the DeepSeek-R1-Zero paradigm does not transfer to multimodal models
- Cold-started MLLMs exhibit an 'Overthinking Optimization Problem' — after learning verbose CoT from DeepSeek-R1, correct reasoning concentrates in short chains while longer chains contain mostly incorrect steps, creating an anti-correlation that destabilizes RL optimization
- Text-only reasoning LLMs (e.g., DeepSeek-R1) cannot directly process multimodal inputs, requiring indirect conversion pipelines that introduce irreducible information loss
- Vision-R1 is evaluated exclusively on mathematical reasoning benchmarks — generalization to general visual understanding, non-mathematical reasoning, or real-world multimodal tasks is entirely undemonstrated
- SFT on multimodal data without CoT reasoning processes before RL is actively harmful — reducing average accuracy to 39.8% vs 50.7% for RL-only, a severe 10.9% regression
- PTST provides negligible benefit without cold-start initialization (+1.1% over pure RL-only baseline), confirming the entire recipe is conditional on the cold-start data quality step
- Scaling Vision-R1 beyond 7B requires additional undisclosed training data during RL — the 10K dataset sufficient for 7B is not sufficient for 32B and 72B variants, indicating data requirements scale with model size
- Prior multimodal CoT datasets (LLaVA-CoT, Mulberry) systematically lack genuine cognitive processes — 'Wait' appears 585,719 times in Vision-R1-cold vs 2,300 in LLaVA-CoT (100K samples) — indicating the field has been training on 'Pseudo-CoT' without awareness of the quality gap
- Vision-R1 training was terminated at Stage 2 of PTST rather than completing Stage 3 (16K context) — the full potential of extending reasoning to very long chains is uncharacterized

## Bottlenecks

- Absence of high-quality multimodal CoT data with genuine cognitive processes (questioning, reflection, self-correction) prevents direct RL from incentivizing complex reasoning in MLLMs — the DeepSeek-R1-Zero paradigm requires a multimodal equivalent of this data to function
- The Overthinking Optimization Problem — cold-started MLLMs concentrate correct reasoning in short chains while RL pressure to extend length fills longer chains with incorrect steps — creates an anti-correlation that makes standard GRPO training unstable and ineffective without specialized length man

## Breakthroughs

- Vision-R1 demonstrates that RL can successfully incentivize human-like complex reasoning in MLLMs — achieving near-OpenAI-O1 multimodal math performance with a 7B model — by combining automated high-quality CoT cold-start with Progressive Thinking Suppression Training

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/cold-start-initialization|Cold-Start Initialization]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
