---
type: source
title: 'General-Reasoner: Advancing LLM Reasoning Across All Domains'
source_id: 01KJTQH6AARJQYQXWEP3E5GY52
source_type: paper
authors:
- Xueguang Ma
- Qian Liu
- Dongfu Jiang
- Ge Zhang
- Zejun Ma
- Wenhu Chen
published_at: '2025-05-20 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# General-Reasoner: Advancing LLM Reasoning Across All Domains

**Authors:** Xueguang Ma, Qian Liu, Dongfu Jiang, Ge Zhang, Zejun Ma, Wenhu Chen
**Published:** 2025-05-20 00:00:00
**Type:** paper

## Analysis

# General-Reasoner: Advancing LLM Reasoning Across All Domains
2025-05-20 · paper · Xueguang Ma, Qian Liu, Dongfu Jiang, Ge Zhang, Zejun Ma et al. (6 total)
https://arxiv.org/pdf/2505.14652

---

### Motivation & Prior Limitations
RL-based reasoning training for LLMs has been almost exclusively confined to mathematics and coding, creating models that fail to generalize to broader domains such as physics, chemistry, finance, and the humanities.
- Data scarcity outside mathematics makes it difficult to assemble large-scale training sets with reliably verifiable answers, since web sources lack the structured, competition-style Q&A density that mathematical domains enjoy.
- Rule-based verifiers — the standard reward mechanism in math RL pipelines — are fundamentally incompatible with diverse answer representations, enforcing rigid exact-match criteria that produce high false-negative rates on semantically correct but differently formatted answers (e.g., "4.9 N·m" vs. "4.9 J").
  - In a sample of 50k answer pairs that Gemini-2.0-Flash deemed correct, the rule-based verifier agreed only 22.2% of the time, demonstrating systemic reward signal corruption on non-math data.
- Narrow training induces cross-domain degradation: S1/S1.1, which focuses on mathematical reasoning, improves math scores but degrades MMLU-Pro performance by 4–6%, confirming that domain-specific RL overfits at the expense of general reasoning capability.

---

### Proposed Approach
General-Reasoner introduces two jointly designed components — a large-scale diverse-domain dataset (WebInstruct-verified) and a compact generative model-based verifier (General-Verifier) — enabling Zero RL training directly from base LLMs across all reasoning domains without a supervised fine-tuning stage.

- **WebInstruct-verified dataset**: Starting from ~5M web-crawled instructions in WebInstruct, the pipeline re-crawls original source pages to recover human-verified Q&A pairs, then uses Gemini-1.5-Pro to filter for questions with clearly verifiable short answers (~1M intermediate), and applies Gemini-2.0-Flash to annotate metadata (subject, difficulty, answer type) and generate 8 candidate solutions per question for quality control.
  - Questions where all 8 Gemini solutions fail (likely noise/unsolvable) and questions where all 8 succeed (trivially easy) are both excluded, producing ~230K high-quality questions spanning mathematics, physics, chemistry, finance, economics, history, and biology.
  - Easy undergraduate-level mathematics is explicitly filtered out to prevent domain imbalance, since math data is over-represented on the web.

- **General-Verifier (1.5B)**: A compact generative verifier initialized from Qwen2.5-Math-1.5B and fine-tuned on Gemini-2.0-generated candidate answers and verification annotations to predict answer equivalence via chain-of-thought reasoning followed by a binary true/false label.
  - The verifier conditions on the original question, ground-truth answer, and student answer simultaneously, enabling context-aware semantic comparison rather than surface-level string matching.
  - This replaces both traditional rule-based verifiers (brittle, format-sensitive) and large-LLM-as-judge approaches (computationally prohibitive at RL training scale).

- **GRPO training** is applied directly to base models (Qwen2.5 7B/14B, Qwen3 4B/14B) with a reward structure that returns −0.5 for failed answer extraction, +1 for verified correct answers with a length-based penalty (−0.05 × min(10, |len_answer − len_ground_truth|)) to discourage verbosity.

---

### Results & Capabilities
General-Reasoner consistently outperforms same-backbone base models, instruction-tuned models, and math-specialized RL baselines (SimpleRL, Open-Reasoner-Zero, Nemotron-CrossThink) across 12 general and mathematical reasoning benchmarks.

- On MMLU-Pro, General-Reasoner-7B achieves 58.9% vs. 47.7% for the base model and 57.0% for the instruction-tuned model; General-Reasoner-Qw2.5-14B reaches 66.6% vs. 62.7% for the instruction-tuned 14B, representing ~10% absolute gains on general benchmarks over math-only RL baselines.
- The best model, General-Reasoner-Qw3-14B, achieves 56.1% on GPQA-Diamond and 54.4% on TheoremQA, matching or exceeding GPT-4o (50.0% and 43.6% respectively) using only Zero RL — no SFT, no distillation from a larger teacher.
- Cross-domain training does not harm mathematical performance: General-Reasoner-Qw2.5-14B achieves 53.9% average on math benchmarks, outperforming SimpleRL-14B (50.7%) despite training on diverse rather than math-only data, demonstrating positive transfer from general domain reasoning to mathematics.
- Ablation confirms the contribution of domain diversity: restricting training to math-only data for the 14B backbone reduces MMLU-Pro from 66.6% to 64.8%, GPQA from 43.4% to 38.9%, and SuperGPQA from 39.5% to 35.6%, while providing only a marginal math gain.
- The model-based verifier directly improves training dynamics: using General-Verifier instead of rule-based verification on Qwen3-4B-Base for 120 steps yields +2 points on MMLU-Pro (60.1% vs. 58.1%), and critically, the rule-based verifier plateaus at step ~60 while the model-based verifier continues improving, indicating the rule-based verifier starves the RL signal on diverse data.
- General-Reasoner avoids the "overthinking" failure mode of long-chain reasoning models: average response length grows from ~700 to ~1,000 tokens during training, compared to DeepScaleR outputs that can reach ~32k tokens. On MMLU-Pro Computer Science, General-Reasoner-4B achieves 61% accuracy in 1.5 minutes vs. 35% accuracy in 18 minutes for DeepScaleR-1.5B-Preview on identical hardware.

---

### Implications
This work establishes that the data bottleneck limiting RL-based reasoning to mathematics is addressable through systematic web curation paired with an LLM-in-the-loop quality filter, opening Zero RL training to the full breadth of knowledge-intensive reasoning tasks.

- The

## Key Claims

1. Current RL-based LLM reasoning works primarily focus on mathematical and coding domains due to data abundance and ease of answer verification.
2. DeepSeek-R1-Zero demonstrated that training a base LLM directly via RL can unlock powerful reasoning capabilities without relying on a supervised fine-tuning step.
3. Training solely on mathematical data (S1/S1.1) degrades performance on MMLU-Pro by 4-6%, demonstrating negative transfer from math-only RL training to general reasoning.
4. Rule-based verifiers have a high false-negative rate, achieving only 22.2% agreement with Gemini-2.0-Flash on answers Gemini deems correct.
5. The General-Verifier (1.5B parameter model-based verifier) achieves 78.7% agreement with Gemini-2.0-Flash, substantially outperforming rule-based verifiers.
6. Rule-based verifiers fail to recognize semantically equivalent answers that differ in representation, such as '4 + 8t, 1 + 2t, 17 - t' versus 'x = 4 + 8t, y = 1 + 2t, z = 17 - t'.
7. The model-based verifier is particularly beneficial for non-math STEM fields like Physics and Engineering, where answer formats are diverse, while structured fields like Economics show smaller gaps be
8. Training with the model-based verifier causes continued improvement through 120 steps, while the rule-based verifier plateaus at around step 60 (~58% on MMLU-Pro).
9. General-Reasoner-Qw3-14B matches or beats GPT-4o on GPQA (56.1% vs 50.0%) and TheoremQA (54.4% vs 43.6%) using only Zero RL without supervised fine-tuning.
10. General-Reasoner trained on diverse domains boosts performance on general benchmarks like MMLU-Pro and SuperGPQA by approximately 10% compared to base models.

## Capabilities

- Zero RL training on diverse multi-domain data (physics, chemistry, finance, history, biology) produces a 14B model that matches or outperforms GPT-4o on GPQA (56.1% vs 50.0%) and TheoremQA (54.4% vs 43.6%) without any supervised fine-tuning stage
- A compact 1.5B generative verifier model trained on Gemini-2.0-generated labels can assess answer equivalence across diverse domains with 78.7% agreement with Gemini-2.0-Flash, versus only 22.2% for rule-based verification — enabling scalable RL reward signals beyond math/code
- Diverse-domain Zero RL training simultaneously improves both general reasoning (MMLU-Pro, GPQA, SuperGPQA up ~10%) and mathematical reasoning — cross-domain generalization provides additive benefit rather than trade-off with math specialization
- Length-penalty reward shaping during GRPO training suppresses overthinking — General-Reasoner produces ~1000-token responses while achieving better accuracy than models generating ~32K-token outputs (e.g., DeepScaleR), yielding 40x faster inference at higher accuracy
- Large-scale diverse verifiable reasoning dataset (230K questions spanning physics, chemistry, finance, economics, history, biology) constructed via web crawling + LLM filtering enables training beyond mathematics

## Limitations

- Rule-based verification fails catastrophically for diverse answer types outside mathematics, achieving only 22.2% agreement with correct answers confirmed by Gemini — a 77.8% false-negative rate that corrupts RL reward signals and blocks generalization training
- RL training exclusively on mathematical data causes generalization failure: math-only models degrade on MMLU-Pro by 4-6 percentage points compared to models trained on diverse data, revealing a performance cliff when domain distribution shifts
- The General-Verifier model itself has a ~21.3% disagreement rate with Gemini-2.0-Flash, meaning roughly 1 in 5 reward signals during RL training may be incorrect — introducing systematic noise into the training signal
- The entire General-Reasoner paradigm is restricted to tasks with verifiable short-form answers — open-ended tasks (writing, explanation, agentic planning, creative work) are entirely excluded from this training and reward framework
- Web-crawled reasoning data has high inherent noise — questions that all 8 candidate solutions fail (unsolvable/noisy) and questions all 8 solutions answer correctly (trivially easy) must be filtered, indicating that naive web data is unreliable for RL training without expensive LLM-based curation
- Generating training data for the diverse dataset requires running Gemini-2.0-Flash to produce 8 candidate solutions per question across ~1M intermediate questions — computationally expensive at scale and introduces dependency on closed proprietary models for dataset creation
- Zero RL performance is bounded by base model quality — improvements are larger on stronger Qwen3 backbones than Qwen2.5, and the Zero RL approach provides no way to escape the limits of the base model's implicit knowledge distribution
- Training costs remain substantial at frontier scale: 14B model training requires 32×H100 GPUs (4 nodes × 8) for ~4 days, limiting reproducibility and iteration speed outside well-resourced labs
- Despite explicit domain-balancing filters, the WebInstruct-verified dataset remains 33.9% mathematics — the most data-rich domain still dominates by a factor of ~3x over second-place physics (23.7%), indicating structural web data imbalance persists even after curation
- Performance gap vs closed-source or closed-data systems remains on some benchmarks — General-Reasoner-Qw3-14B underperforms DeepSeek-R1 (MMLU-Pro 70.3% vs 84.0%, GPQA 56.1% vs 71.5%) indicating open-data approaches have not closed the frontier gap

## Bottlenecks

- Lack of large-scale, high-quality verifiable reasoning data spanning diverse non-mathematical domains (physics, chemistry, finance, humanities) prevents RL training for general reasoning — current RL methods are confined to math/code due to data scarcity and verification difficulty outside these dom
- Traditional reward models require large parameter count to resist exploitation, while rule-based verifiers fail for diverse answer formats — creating a gap where compact, reliable, domain-general reward signals for RL training are unavailable

## Breakthroughs

- A compact 1.5B generative verifier trained on LLM-generated labels achieves 78.7% agreement with Gemini-2.0-Flash on diverse answer verification — demonstrating that scalable, cross-domain RL reward signals can be provided without large reward models or rule-based systems, enabling Zero RL training 

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/gpqa|GPQA]]
- [[entities/rule-based-verifier|Rule-based Verifier]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/webinstruct|WebInstruct]]
