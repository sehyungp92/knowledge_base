---
type: source
title: 'MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners
  with Open Training Recipes'
source_id: 01KJTF5EP64KXMVKZ4R7TDYVRY
source_type: paper
authors:
- Changsheng Zhao
- Ernie Chang
- Zechun Liu
- Chia-Jung Chang
- Wei Wen
- Chen Lai
- Sheng Cao
- Yuandong Tian
- Raghuraman Krishnamoorthi
- Yangyang Shi
- Vikas Chandra
published_at: '2025-09-29 00:00:00'
theme_ids:
- chain_of_thought
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes

**Authors:** Changsheng Zhao, Ernie Chang, Zechun Liu, Chia-Jung Chang, Wei Wen, Chen Lai, Sheng Cao, Yuandong Tian, Raghuraman Krishnamoorthi, Yangyang Shi, Vikas Chandra
**Published:** 2025-09-29 00:00:00
**Type:** paper

## Analysis

# MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes
2025-09-29 · paper · Changsheng Zhao, Ernie Chang, Zechun Liu, Chia-Jung Chang, Wei Wen et al. (11 total)
https://arxiv.org/pdf/2509.24945

---

### Motivation & Prior Limitations
- The prevailing assumption that chain-of-thought reasoning only emerges in sufficiently large models trained on massive corpora (>10T tokens) has driven enormous compute expenditure, leaving the question of whether this data scale is truly necessary largely unexamined.
  - State-of-the-art small reasoning models like Qwen3-0.6B rely on a proprietary 36T-token pretraining corpus, making them impossible to replicate or study with open data alone.
  - Fully open-source small models (OLMo-2-1.48B, SmolLM2-1.7B) score 0.6 and 0.3 respectively on AIME24, suggesting their pretraining distributions fail to install latent reasoning potential regardless of post-training effort.
- Small models face a qualitatively different challenge from large ones: limited neuron capacity forces overlapping knowledge encoding, making noise in training data disproportionately harmful through interference and superposition effects, so simply scaling down large-model recipes is insufficient.
  - Uniform dataset sampling, the standard baseline, ignores heterogeneous marginal utility across sources and wastes token budget on data that does not transfer to reasoning-relevant capabilities.

---

### Proposed Approach
- The paper introduces a data-centric framework with three interconnected innovations — capability-aware dataset selection via leave-one-out (LOO) NLL analysis, cross-capability influence-weighted data mixing, and a mid-training data–model co-evolution strategy — applied across a four-phase pipeline (two pretraining phases, two mid-training phases, two post-training stages) totaling 4.2T tokens.
  - **Dataset selection (Section 2.1):** A hierarchical rejection sampling pipeline builds compact capability-probing datasets (~10,000 examples per domain) by combining FineWeb-Edu classifier scores (>4 threshold), Ask-LLM binary scoring (top 10% per dataset), domain-specific prompts for code/math/knowledge, and semantic deduplication. LOO ablations then measure the NLL delta on these probing sets when each source is excluded, quantifying per-token cross-domain contribution without touching held-out benchmarks.
  - **Data mixing (Section 2.2):** Building on the AutoMixer framework, influence scores are computed at T=10 evenly spaced checkpoints using domain-specialized models, aggregated as a joint influence signal across code, math, and knowledge capabilities (with linearly increasing checkpoint weights), and converted into closed-form dataset-level sampling weights. This "benchmark-free, self-evolving" mixture is derived entirely from the training corpus without any held-out benchmark access.
  - **Mid-training co-evolution (Section 3):** Starting from the Dolmino corpus augmented with math and code data, the model iteratively rejects samples with negative influence scores, recomputes dataset-level mixing ratios, and retrains — terminating when influence distributions converge near zero, indicating information exhaustion. Two stages suffice in practice.
- Post-training follows an established two-stage procedure: general instruction alignment with Tülu-3-SFT (866k samples) followed by domain-specific reasoning SFT on OpenMathReasoning, OpenScienceReasoning-2, and OpenCodeReasoning-2 (3.2M samples combined). Decoupling these stages outperforms joint training.

---

### Results & Capabilities
- MobileLLM-R1-950M matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks while using only 4.2T pretraining tokens — 11.7% of Qwen3's proprietary 36T-token corpus — placing it on the Pareto frontier of accuracy vs. training-token efficiency.
  - On AIME24, MobileLLM-R1-950M scores 15.5 vs. 11.3 for Qwen3-0.6B, 0.6 for OLMo-2-1.48B, and 0.3 for SmolLM2-1.7B.
  - On HumanEval (base model), MobileLLM-R1-950M achieves 46.3%, the highest among all sub-1B models, compared to 30.5% for Qwen3-0.6B and 6.7% for OLMo-2-0425-1B.
  - On MATH, MobileLLM-R1-950M scores 74.0%, compared to 73.0% for Qwen3-0.6B and 19.2% for OLMo-2-1.48B.
- The influence-weighted data mixture outperforms uniform sampling on code, math, and knowledge benchmarks without any benchmark exposure during training or mixture construction, validating the benchmark-free self-optimization claim.
  - Figure 4 shows consistent perplexity reduction across all three capability domains when using the derived mixture vs. original uniform sampling.
- When all baselines are fine-tuned on the identical reasoning SFT corpus, MobileLLM-R1 models consistently outperform their open-source counterparts at every scale (140M, 360M, 950M), demonstrating that the gains originate in pretraining/mid-training rather than post-training data.
  - MobileLLM-R1-360M achieves 5.1 on LiveCodeBench-v6, surpassing SmolLM2-1.7B (4.4), Gemma3-1B (2.0), and LLaMA3.2-1B (4.1).
- An unexpected LOO finding: removing StarCoder degrades math performance more than removing OpenWebMath degrades code performance, reversing the commonly held assumption that mathematical data is the primary driver of coding ability.
- Training dynamics show that math pre-training transfers to coding: a sharp perplexity drop on GSM8K occurs during pretraining phase 2, and subsequently the same math-trained model exhibits a dramatic coding perplexity drop during mid-training phase 2, suggesting a directional knowledge transfer from math to code.

---

### Implications
- The work empirically dismantles the second major assumption in reasoning model development — that reasoning requires >10T token pretraining — suggesting that data quality, curation methodology, and token efficiency can substitute for raw scale, which has significant implications for research groups without access to proprietary data at Qwen or DeepSeek scale.
- The benchm

## Key Claims

1. Strong reasoning abilities can emerge with approximately 2T tokens of high-quality data, challenging the assumption that massive datasets (>10T tokens) are required for reasoning emergence.
2. MobileLLM-R1-950M achieves an AIME score of 15.5, dramatically outperforming OLMo-2-1.48B (0.6) and SmolLM-2-1.7B (0.3) despite having fewer parameters.
3. MobileLLM-R1-950M matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks despite being trained on only 11.7% of Qwen3's 36T pretraining tokens.
4. Small language models are far more sensitive to data noise than large models, making data quality and curation paramount for compact models.
5. As models shrink, neurons must encode more overlapping knowledge, increasing the risk of interference and conflicts, a phenomenon explained through superposition.
6. Removing FineWeb-Edu from pretraining causes the largest degradation across all capability domains (knowledge, math, and code), attributable to its broad web-based composition that connects diverse do
7. StarCoder benefits math performance more than OpenWebMath benefits code performance, reversing the commonly held assumption that mathematical data contributes disproportionately to coding ability.
8. Wikipedia contributes little to math or code performance compared to web or domain-specific data, but remains necessary as a structured and reliable source of factual knowledge.
9. Influence-score-weighted data mixing consistently outperforms uniform sampling on Code, Math, and Knowledge benchmarks, even when those benchmarks are not accessed during training or mixture construct
10. Two mid-training stages suffice to produce a well-compressed dataset that balances generality with targeted capability improvements.

## Capabilities

- Sub-billion parameter language models can achieve strong chain-of-thought reasoning through data-centric training alone — MobileLLM-R1-950M achieves AIME24 score of 15.5, matching or surpassing Qwen3-0.6B on multiple reasoning benchmarks with only 4.2T pretraining tokens versus Qwen3's 36T
- Benchmark-free, self-evolving data optimization via cross-capability influence scoring enables principled pretraining data mixture construction without any benchmark exposure during curation — resulting mixture generalises to held-out benchmarks across code, math, and knowledge domains
- Data-model co-evolution via iterative influence-based rejection sampling compresses mid-training data to maximally informative samples — converges when all samples reach near-zero influence, providing an automatic termination signal indicating dataset exhaustion
- Staged post-training — instruction alignment SFT first (Tulu-3), followed by domain-specific reasoning SFT — consistently outperforms joint training on math and general reasoning for small language models

## Limitations

- Small language models (sub-1B) are fundamentally more sensitive to training data noise than large models — noise easily overwhelms limited capacity, and neurons must encode overlapping knowledge, creating interference and conflict between knowledge representations
- Models below 400M parameters fail to produce reliable outputs on complex coding benchmarks — LiveCodeBench performance effectively collapses below this scale threshold regardless of training quality
- Introducing domain-specific reasoning data (math or code) into small model training degrades MMLU factual knowledge performance — a fundamental zero-sum capacity trade-off between reasoning specialization and general knowledge retention that is more severe at smaller scales
- Long-context chain-of-thought reasoning directly conflicts with on-device deployment — KV cache growth from extended reasoning traces sharply increases memory footprint, negating the benefits of small model size for edge deployment
- Sub-1B models trained via data-centric methods still fall significantly short of distilled larger models on hard reasoning — AIME24 score of 15.5 versus 29.1 for DeepSeek-R1-Distill-Qwen-1.5B, revealing a hard capability ceiling that data quality improvements cannot close
- Influence score computation requires training separate domain-specialized model checkpoints at ten evenly-spaced timesteps per domain — a computationally expensive prerequisite that limits practical accessibility of the data curation approach for resource-constrained researchers
- The paper's stated motivation is on-device deployment, but no actual on-device evaluation is performed — inference latency, memory usage under real device constraints, and energy consumption are conspicuously absent despite being the primary deployment rationale
- Smallest models (140M) achieve only 16.3% GSM8K and 15.9% HumanEval even after optimal data curation and post-training — absolute performance remains far below practical thresholds for real-world task delegation despite significant improvements over baselines

## Bottlenecks

- On-device deployment of reasoning models is blocked by KV cache memory explosion during long chain-of-thought generation — extended reasoning traces are fundamental to CoT capability but their memory footprint is incompatible with edge device constraints
- Small model parameter count creates a hard zero-sum trade-off between reasoning specialization and factual knowledge retention — every gain in domain-specific reasoning comes at cost to general knowledge, preventing small models from achieving broad general capability

## Breakthroughs

- Strong reasoning capabilities demonstrated in sub-1B parameter models trained on only ~4.2T tokens — 11.7% of Qwen3's data — falsifying the assumption that massive pretraining corpora (>10T tokens) are a prerequisite for reasoning emergence
- Leave-one-out influence analysis reveals that code training data (StarCoder) benefits mathematical reasoning more than mathematical data (OpenWebMath) benefits coding — reversing the canonical directionality of cross-domain transfer assumed in the pretraining literature

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/pretraining_data|pretraining_data]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/chain-of-thought-cot-reasoning|Chain-of-Thought (CoT) Reasoning]]
- [[entities/cosmopedia|Cosmopedia]]
- [[entities/finemath|FineMath]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/gsm8k|GSM8K]]
- [[entities/openwebmath|OpenWebMath]]
