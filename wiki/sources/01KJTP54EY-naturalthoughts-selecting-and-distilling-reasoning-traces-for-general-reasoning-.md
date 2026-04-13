---
type: source
title: 'NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning
  Tasks'
source_id: 01KJTP54EYE9CBWV7A593AFAQP
source_type: paper
authors:
- Yang Li
- Youssef Emad
- Karthik Padthe
- Jack Lanchantin
- Weizhe Yuan
- Thao Nguyen
- Jason Weston
- Shang-Wen Li
- Dong Wang
- Ilia Kulikov
- Xian Li
published_at: '2025-07-02 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks

**Authors:** Yang Li, Youssef Emad, Karthik Padthe, Jack Lanchantin, Weizhe Yuan, Thao Nguyen, Jason Weston, Shang-Wen Li, Dong Wang, Ilia Kulikov, Xian Li
**Published:** 2025-07-02 00:00:00
**Type:** paper

## Analysis

# NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks
2025-07-02 · paper · Yang Li, Youssef Emad, Karthik Padthe, Jack Lanchantin, Weizhe Yuan et al. (11 total)
https://arxiv.org/pdf/2507.01921

---

### Motivation & Prior Limitations
- Prior work on reasoning distillation lacked a systematic study of *which* reasoning demonstrations from a teacher model most effectively transfer reasoning capabilities to a student model, leaving practitioners without principled data curation guidance.
  - LIMO and S1K showed that ~1,000 carefully hand-selected examples can dramatically improve performance, but this "Less is More" hypothesis was validated only on narrow math and coding domains and did not generalize reliably to broader reasoning tasks (Sun et al., 2025).
  - Existing distilled datasets like OpenThoughts and OpenR1 focused on collecting large volumes of teacher traces without studying quality dimensions such as difficulty, reasoning diversity, or verbosity — treating more data as uniformly better.
- State-of-the-art reasoning models exhibit sub-optimal reasoning patterns including "overthinking" and "underthinking," yet no prior distillation pipeline addressed the resulting inference-time inefficiency as a first-class objective alongside accuracy.
  - System-2-only distillation produced models averaging 8,740 tokens per response on GPQA-Diamond and could not be steered to reason concisely even when explicitly instructed.
- RL alone does not introduce new reasoning primitives into a student model's prior, making SFT distillation a necessary prerequisite step even before RL post-training (Yue et al., 2025).

---

### Proposed Approach
- The paper introduces NaturalThoughts (NT), a dataset and systematic curation pipeline built by generating DeepSeek-R1 reasoning traces over questions from NaturalReasoning (2.8M diverse multi-domain questions), then studying multiple data selection axes — scale, diversity, and difficulty — to identify what makes distillation most sample-efficient.
  - Unlike LIMO and S1K, which use manual question curation restricted to math/coding, NaturalThoughts draws from a broad multi-domain pool spanning 13 top-level domains (Engineering, Medicine, Law, History, etc.) and scales up to 500k examples.
  - Reasoning traces are annotated along three axes using Llama-3.1-70B-Instruct as an annotator: (1) domain/topic taxonomy, (2) meta-reasoning strategies present in each trace (self-verification, backtracking, exploration, etc.), and (3) verbosity scores (0–10).
- Three diversity-based selection strategies are compared: uniform topic sampling, semantic embedding clustering, and reasoning strategy diversity (selecting examples with 4–8 unique reasoning strategies and high reasoning density).
- Three difficulty-based selection strategies are compared: length-biased sampling (upweighting long traces via $p = (l/C)^\tau$), verbosity filtering, and model disagreement (using DeepSeek-R1 vs. Llama-3.3-70B answer agreement as a difficulty proxy).
- A mixed System-1/System-2 distillation method is proposed where training data contains either full CoT traces (System-2) or condensed final answers only (System-1), with two mixing strategies: random mixing at probability $p \in \{0.2, 0.4, 0.6\}$ and difficulty-based mixing (System-2 for disagreement examples, System-1 for easy ones). Inference-time prompts explicitly control which reasoning mode the model uses.

---

### Results & Capabilities
- Random selection from NaturalThoughts at 1k examples already matches or exceeds manually curated baselines: NT-Random-1k achieves 37.1% on GPQA-Diamond vs. 36.9% for S1K and 34.0% for LIMO, despite no manual curation.
  - This directly contradicts the "Less is More" hypothesis in a general-domain setting — the NaturalReasoning question pool appears sufficiently high-quality that random draws outperform curated narrow-domain sets.
- Scaling consistently improves performance without saturation up to 500k examples: NT-Random scales from 37.1% (1k) → 37.6% (10k) → 42.5% (100k) → 48.3% (500k) on GPQA-Diamond for Llama-3.1-8B-Instruct.
- Reasoning strategy diversity is the most sample-efficient selection criterion at 10k scale, outperforming topic diversity and semantic diversity; it also outperforms random selection at 100k (44.1% vs. 42.5% GPQA-Diamond) and 500k (48.6% vs. 48.3%).
  - This implies that diversity of *reasoning traces* matters more than diversity of *questions* — a novel finding relative to prior data curation literature.
- Model disagreement selection is the strongest single difficulty signal: at 100k examples it achieves 45.2% GPQA-Diamond vs. 42.5% for random, and at 500k it ties reasoning strategies (45.2% vs. 48.6%), with particularly strong gains on MATH-500 (70.2% vs. 67.5% at 100k).
- With 100k examples, NaturalThoughts-trained Llama-3.3-70B-Instruct surpasses DeepSeek-R1-Distill-Llama-70B (trained on 800k non-public examples) on GPQA-Diamond (67.6% vs. 65.2%), MMLU-Pro (78.9% vs. 78.5%), and SuperGPQA (50.6% vs. 49.4%).
- NT with 500k examples outperforms OpenThoughts3 trained on 1.2M examples on three of four benchmarks when using Qwen-2.5-7B-Instruct as the student model (48.6% vs. 46.9% GPQA-Diamond, 62.7% vs. 59.1% MMLU-Pro, 35.2% vs. 33.5% SuperGPQA).
- Difficulty-based mixed distillation achieves 38.9% on GPQA-Diamond in "Think" mode — a 1.3% improvement over pure System-2 distillation — while using only 36% System-2 responses in training, outperforming random mixing at 60% System-2 (37.5%).
  - Mixed training also enables all three inference modes (No-Think, Adaptive-Think, Think), whereas System-1-only and System-2-only models each lock into one behavior and cannot be steered to the other.
  - System-1-only distillation achieves responses 27x shorter than System-2 with only a 4.6% accuracy drop (34.0% vs. 37.6% GPQA-Diamond), but cannot leverage additional test-time compute when prompted to do so.

---

### Implications
- The findi

## Key Claims

1. Distilling reasoning traces from a larger teacher model via supervised finetuning outperforms reinforcement learning with the smaller student model alone.
2. Reinforcement learning alone does not increase the innate priors for reasoning in a student model, while SFT on reasoning traces from a teacher model can add new reasoning primitives.
3. Simply scaling up data size with random sampling is a strong baseline that yields steady performance gains for reasoning distillation.
4. Selecting difficult examples that require more diverse reasoning strategies is more sample-efficient for transferring teacher model reasoning skills to a student model.
5. The 'Less is More' hypothesis from LIMO and S1K does not hold when scaling reasoning distillation beyond 1,000 examples on diverse general-domain questions.
6. Using only 1,000 randomly selected examples from NaturalThoughts already outperforms LIMO and is on par with S1K, despite LIMO and S1K using rigorous manual curation.
7. Training on 500k NaturalThoughts examples outperforms training on 1.2 million OpenThoughts3 examples on three of the four evaluation benchmarks when using Qwen-2.5-7B-Instruct as the student model.
8. Training Llama-3.3-70B-Instruct with 100k NaturalThoughts examples outperforms DeepSeek-R1-Distill-Llama-70B (trained on 800k non-public data) on GPQA-D, MMLU-Pro, and SuperGPQA.
9. Reasoning strategy diversity is a more effective data selection criterion than topic-based or semantic embedding diversity.
10. Uniformly sampling across question topics reduces performance compared to random sampling, likely because question topic distribution is too concentrated among a small set of topics.

## Capabilities

- Small language models (7–8B parameters) can acquire strong general STEM reasoning capabilities by distilling reasoning traces from a larger teacher model via SFT, with 1,000 randomly selected examples outperforming manually curated datasets like LIMO and matching S1K
- Selecting distillation examples based on diversity of meta-reasoning strategies (backtracking, self-verification, exploration, etc.) is the most sample-efficient data selection axis for transferring reasoning capabilities from teacher to student — more effective than question-topic diversity or sema
- Mixed System-1 and System-2 distillation enables student models to dynamically adapt reasoning depth at inference time — flexibly switching between fast (direct answer) and slow (full chain-of-thought) modes based on explicit instruction or implicit question difficulty
- Difficulty-based mixed distillation — applying System-2 reasoning traces only to hard questions and System-1 responses to easy ones — achieves higher peak accuracy than pure System-2 distillation (38.9% vs 37.6% on GPQA-Diamond) while using only 36% System-2 responses in the training set
- Scaling high-quality diverse reasoning distillation data to 500k examples consistently improves student model performance without saturation — 500k NaturalThoughts examples outperforms 1.2M OpenThoughts3 examples on three of four benchmarks for Qwen-2.5-7B
- Training Llama-3.3-70B-Instruct on only 100k NaturalThoughts examples outperforms DeepSeek-R1-Distill-Llama-70B trained on 800k non-public data on GPQA-D, MMLU-Pro, and SuperGPQA, demonstrating high data efficiency in reasoning distillation for larger student models

## Limitations

- All findings about data selection, diversity, and difficulty are validated only in the off-policy distillation setting (SFT on teacher labels); whether the same conclusions hold for on-policy distillation (matching teacher logits given student-generated context) is entirely unverified
- NaturalThoughts training yields lagging improvements specifically on mathematical task evaluations — performance on MATH-500 lags general STEM benchmarks relative to expectations — because the NaturalReasoning source questions don't resemble standard math benchmark problems
- Models trained exclusively on System-2 (full chain-of-thought) demonstrations cannot reliably produce short answers even when explicitly instructed not to think — reducing average response length only from 8,740 to 5,134 tokens despite explicit 'no-think' instruction
- Models trained exclusively on System-1 (direct answer) demonstrations cannot leverage additional test-time compute even when explicitly prompted to reason, fundamentally capping their performance ceiling regardless of available inference budget
- RL training alone does not add new reasoning primitives to a student model — it can only amplify and refine existing priors — making SFT distillation a structural prerequisite for acquiring qualitatively new reasoning behaviors
- Topic-level question diversity as a selection criterion for reasoning distillation actively reduces performance compared to random sampling — topic distribution is too coarse and concentrated to serve as a meaningful diversity signal for reasoning capability
- Verbosity scores for reasoning traces — measuring rambling vs. efficiency — are not a reliable quality signal for distillation data selection because the distribution is too concentrated, with insufficient spread between low/medium/high verbosity subsets to produce consistent performance differences
- Selecting for easy-to-verify answers (short reference answer length as proxy) does not consistently improve reasoning distillation performance — benefits appear only for math tasks, not across general STEM domains
- SOTA teacher reasoning models systematically exhibit overthinking — generating excessive reasoning tokens beyond what problems require — contaminating distillation datasets with inefficient reasoning patterns that propagate to student models
- Reducing maximum training sequence length to control inference cost (from 16,384 to 8,192 tokens) causes severe accuracy degradation in System-2 distillation — truncation removes valid reasoning steps that complex problems genuinely require
- Curated small-scale distillation datasets from prior work (LIMO, S1K) focused narrowly on math and coding do not generalise to reasoning in other domains — gains are in-distribution only and don't transfer to broader STEM reasoning
- Implications of distillation data selection choices for subsequent RL post-training are entirely unexplored — it is unknown how the SFT data curation strategy interacts with RL fine-tuning in multi-stage training pipelines
- Training infrastructure requirements — 32 NVIDIA H200 GPUs with 400k-token dynamic batching for 500k-example SFT — places these experiments beyond the reach of most academic research groups and smaller labs

## Bottlenecks

- No principled, scalable method for selecting which reasoning traces to distill — existing strategies (topic diversity, verbosity) are weak signals; reasoning strategy diversity and model disagreement are promising but require expensive annotation pipelines at scale
- Overthinking in teacher reasoning models (R1, o1, o3) contaminates distillation datasets with sub-optimal, verbose reasoning patterns, requiring active filtering and curation to avoid propagating inference inefficiency to student models
- Interaction between SFT distillation data curation choices and subsequent RL post-training is unstudied — optimal multi-stage training pipelines (curated SFT → RL) cannot be designed without understanding how distillation data quality propagates through RL fine-tuning

## Breakthroughs

- Scaling high-quality diverse reasoning distillation data consistently improves student model performance up to 500k examples without saturation — directly contradicting and empirically disproving the 'Less is More' hypothesis from LIMO and S1K that claimed ~1,000 carefully curated examples were suff
- Difficulty-based mixed System-1/System-2 distillation simultaneously achieves higher peak accuracy than pure System-2 distillation and enables flexible inference-time compute control — surpassing the accuracy-efficiency frontier of both pure approaches and enabling a single model to operate across t

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]

## Key Concepts

- [[entities/overthinking|Overthinking]]
