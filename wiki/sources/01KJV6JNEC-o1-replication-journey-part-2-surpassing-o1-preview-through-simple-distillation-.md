---
type: source
title: 'O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation,
  Big Progress or Bitter Lesson?'
source_id: 01KJV6JNEC6GFA7ADGS68H01C6
source_type: paper
authors:
- Zhen Huang
- Haoyang Zou
- Xuefeng Li
- Yixiu Liu
- Yuxiang Zheng
- Ethan Chern
- Shijie Xia
- Yiwei Qin
- Weizhe Yuan
- Pengfei Liu
published_at: '2024-11-25 00:00:00'
theme_ids:
- alignment_and_safety
- chain_of_thought
- finetuning_and_distillation
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# O1 Replication Journey — Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?

This paper delivers a deliberately transparent demonstration that simple knowledge distillation from O1's API — without novel algorithmic contribution — can surpass O1-preview on AIME2024, while simultaneously exposing a field-wide transparency crisis in O1 replication research and introducing a formal framework (TTI) for auditing methodological honesty.

**Authors:** Zhen Huang, Haoyang Zou, Xuefeng Li, Yixiu Liu, Yuxiang Zheng, Ethan Chern, Shijie Xia, Yiwei Qin, Weizhe Yuan, Pengfei Liu
**Published:** 2024-11-25
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

The post-O1 replication landscape suffers from a transparency crisis: numerous institutions claim to replicate O1-level reasoning while obscuring their actual methodology — specifically, the widespread but undisclosed use of knowledge distillation from O1's API. Without a standardized transparency framework, the research community cannot accurately assess claimed advances or build on them reproducibly. The opacity creates a distorted picture of the field's genuine technical progress, conflating prompt-engineering-level shortcuts with fundamental algorithmic innovation.

Synthesizing the long chains of thought required for O1-style reasoning (reflection, error correction, backtracking) is also technically hard: tree-search approaches like MCTS (used in Part 1's "journey learning") are computationally expensive, creating a high barrier for most research groups. Part 1's approach required tree-search plus LLM-driven reflection synthesis — costly and complex to replicate at scale.

### Proposed Approach

The core technical contribution is a deliberately transparent demonstration that **simple knowledge distillation from O1's API** — directly prompting O1 to generate long-thought reasoning chains, then applying two-stage SFT — can surpass O1-preview on AIME with minimal algorithmic complexity. This contrasts sharply with Part 1's journey learning (MCTS + LLM reflection synthesis) and positions distillation as the lowest-cost, highest-quality point on the data acquisition frontier.

The **two-stage SFT pipeline**:
1. Fine-tune Qwen2.5-Math-72B on reformatted Olympic-level math problems (rewritten by GPT-4o-mini into step-by-step, `\boxed`-format solutions) to acclimate the model to long-thought format
2. Fine-tune again on the O1-distilled dataset of long-form reasoning chains

Data curation filters Olympic-level problems from open-source and self-curated datasets, removing image-dependent, answer-less, and proof-based problems, retaining only numerically-answerable questions. A "reformatted technology" step standardizes solutions into lengthy, detailed step-by-step chains. The distilled dataset captures O1's reflection and self-correction patterns without accessing O1's internal chain-of-thought (API-restricted) — only the final long-form responses are used.

The paper also proposes the **Technical Transparency Index (TTI)**, a 100-point binary scoring framework across four dimensions — Data (14), Methodology (33), Evaluation (24), Open-Source (29) — to systematically benchmark transparency and reproducibility of O1 replication claims. Every checklist item is scored Yes/No; explicit acknowledgment that a technique was *not* used still earns full points, rewarding honest disclosure over implementation scope.

### Results & Capabilities

**Mathematical reasoning:** The distilled 72B model achieves 13/30 on AIME 2024 vs. O1-preview's 12/30, under comparable inference-time compute (8,016 vs. 9,083 average output tokens). It also reaches 87.2% on MATH500 vs. O1-preview's 85.5%. O1-mini remains substantially stronger (21/30 on AIME, 90.0% on MATH500), indicating a meaningful gap between distilling from O1-preview-level outputs and the full O1-mini capability tier.

**Cross-domain generalization:** Despite training exclusively on mathematical long-thought data, the model demonstrates substantial transfer to open-domain QA — Auto-J scores improve from 81.6% to 88.0% and LIMA scores from 77.2% to 87.2%. Case studies show transfer of mathematical systematic-thinking patterns to technical programming queries (Python asyncio debugging) and structured multi-perspective analysis.

**Sycophancy resistance:** The model becomes meaningfully less susceptible to sycophancy after SFT, with ChineseFactEval-Sycophancy scores improving from 89.70% to 92.65%. The self-reflection process forces the model to interrogate false assumptions in prompts rather than accepting them — e.g., the post-SFT model correctly identifies that China's second-longest river is the Yellow River, not the Pearl River as falsely asserted.

**Safety — mixed results:** Flames improves (91.0% → 92.5%) due to the dataset's emphasis on deep reflection scenarios aligned with long-thought training. But WildSafety degrades (92.0% → 86.5%), causing overall safety to drop from 94.3% to 93.0%. The Flames improvement is attributed to the model's enhanced ability to pause, reflect, and identify safety hazards before addressing surface requests.

**Factuality — no improvement:** On SimpleQA, ChineseSimpleQA, and ChineseFactEval-General, performance does not improve and slightly declines (e.g., CFE-General: 69.08% → 62.65%), because longer reasoning chains generate additional hallucinations via fabricated search engine interactions. Models in long-thought mode attempt to simulate web searches and confabulate plausible-but-false results.

---

## Key Claims

1. A base model fine-tuned on tens of thousands of O1-distilled long-thought chains can outperform O1-preview on AIME with minimal technical complexity.
2. The distilled 72B model achieves 87.2% on MATH500, surpassing O1-preview's 85.5%, under comparable inference cost.
3. Despite training only on mathematical problem-solving data, O1-distilled models demonstrate strong generalization to open-ended QA tasks.
4. Models fine-tuned on O1-distilled long-thought data become significantly less susceptible to sycophancy, improving from 89.70% to 92.65% on ChineseFactEval-Sycophancy.
5. Long-thought SFT does not improve factuality on short-form fact-seeking benchmarks — SimpleQA scores slightly decline (10.58% → 10.41%).
6. Longer reasoning chains in post-SFT models lead to additional hallucinations, specifically models fabricating search engine results.
7. Long-thought training improves safety on Flames (91% → 92.5%) but decreases WildSafety performance (92% → 86.5%), indicating systematic thinking alone is insufficient for comprehensive safety.
8. Widespread but undisclosed use of O1 knowledge distillation creates a distorted picture of technical progress in the field.
9. Distillation-trained models are inherently bounded by the teacher model's capabilities, creating a performance ceiling that prevents genuine advancement beyond O1.
10. Data quality exerts a more substantial influence on model performance than either model size or data volume.

---

## Capabilities

**Simple distillation surpasses O1-preview** *(maturity: demo)*
Knowledge distillation from O1's API combined with standard SFT allows a 72B base model to surpass O1-preview on AIME2024 (13/30 vs. 12/30) using only tens of thousands of distilled samples. This is reproducible without novel algorithmic contribution — the principal requirements are data access and compute for fine-tuning.

**Cross-domain transfer from math to open-domain QA** *(maturity: demo)*
Models fine-tuned exclusively on mathematical long-thought data demonstrate strong generalization: Auto-J improves 81.6→88%, LIMA 77.2→87.2%, with transfer to technical programming assistance and structured multi-perspective argumentation. The systematic thinking patterns of mathematical reasoning appear to be domain-general.

**Sycophancy resistance via self-reflection** *(maturity: demo)*
Long-thought self-reflection training enables models to detect and correct false assumptions embedded in prompts rather than accepting them. The model interrogates stated premises against its knowledge during extended reasoning, producing a behavioral resistance to manipulation that emerges as a byproduct of reasoning training rather than explicit alignment work.

**Safety-relevant systematic thinking** *(maturity: demo)*
Models trained on O1-like reflective data demonstrate improved ability to identify life-threatening risks (e.g., fire hazards from corridor charging) before addressing the user's surface-level request — an emergent safety-relevant behavior arising from comprehensive systematic analysis of situations.

---

## Limitations

**Hard capability ceiling from distillation** *(severity: blocking, trajectory: stable)*
Distillation-trained models are fundamentally bounded by the teacher model's capabilities. No matter how sophisticated the distillation process, improvements can never surpass the original model. The distilled 72B model already demonstrates this: 13/30 on AIME vs. O1-mini's 21/30. See also: [[themes/finetuning_and_distillation|Finetuning & Distillation]].

**Hallucination amplified by long reasoning chains** *(severity: significant, trajectory: improving)*
Extended thinking mode causes models to simulate search engine interactions and fabricate search results — multi-step reasoning chains built on confabulated evidence. Factuality benchmarks decline post-SFT precisely because longer chains create more opportunities for plausible-sounding fabrications. This is a qualitatively new failure mode: the model is not merely wrong, but *confidently wrong with apparent process*.

**Safety regression on diverse benchmarks** *(severity: significant, trajectory: unclear)*
Long-thought SFT without explicit safety alignment data causes WildSafety to degrade from 92% to 86.5%, despite improvements on reflection-focused safety benchmarks. Systematic thinking is insufficient for comprehensive safety — it helps with hazard identification but does not prevent other safety failures. See [[themes/alignment_and_safety|Alignment & Safety]].

**O1 API opacity blocks true mechanism replication** *(severity: blocking, trajectory: stable)*
O1's API restricts access to internal thought processes. Only the final visible outputs can be distilled — the actual reasoning mechanisms (search algorithms, optimization strategies, inference-time scaling) remain opaque. The most technically valuable component of O1 cannot be distilled or replicated through the API. This makes distillation a shortcut that does not advance understanding of what makes O1 work.

**ToS reproducibility gap** *(severity: significant, trajectory: stable)*
Per OpenAI's Terms of Use, the O1-distilled training data cannot be fully publicly disclosed. The paper demonstrates the approach works but the community cannot replicate it at scale without independently re-collecting distilled data — creating a structural reproducibility constraint that limits the scientific value of the demonstration.

**Research culture atrophy risk** *(severity: significant, trajectory: worsening)*
Distillation-based training cultivates prompt engineering and optimization skills rather than first-principles algorithm development. The paper argues this creates structural skill atrophy risk in the next generation of AI researchers — who learn to distill rather than to invent inference-time search, RL reward modeling, or novel optimization strategies.

**Field-wide transparency crisis** *(severity: significant, trajectory: worsening)*
Most O1 replication works score 0 on Data and Open-Source TTI dimensions. The lack of transparency makes it increasingly difficult to assess genuine technical progress, and creates incentive structures that reward undisclosed capability borrowing while claiming novel contribution. See [[themes/post_training_methods|Post-Training Methods]].

---

## Bottlenecks

**Transparency crisis in O1 replication research** *(horizon: 1–2 years)*
Widespread undisclosed use of distillation prevents accurate assessment of genuine technical progress, making the research literature an unreliable signal for actual algorithmic advances. The TTI framework proposed here is a necessary but not sufficient solution — adoption requires community norms or conference requirements that don't yet exist.
> *"Most works scored 0 on Data and Open-Source transparency dimensions...the lack of transparency in methodology reporting makes it increasingly difficult..."*

**Distillation capability ceiling** *(horizon: 3–5 years)*
Open-source models trained via distillation approach but cannot exceed the teacher. The key mechanisms — inference-time search, RL, reward modeling — remain locked inside closed systems. Independent advancement of inference-time scaling techniques requires research capacity and institutional incentives that distillation shortcuts actively undermine.

**Safety-reasoning tension** *(horizon: 1–2 years)*
Long-thought SFT that improves reasoning degrades safety on diverse benchmarks without explicit safety data. Combining the two training objectives without interference requires solutions that do not yet exist — separate pipelines risk capability dilution; joint training faces objective conflicts. See [[themes/alignment_and_safety|Alignment & Safety]].

---

## Breakthroughs

**Distillation achieves benchmark-surpassing performance without algorithmic novelty** *(significance: notable)*
The demonstration that impressive benchmark results can be achieved through pure distillation — with no novel contribution — is itself a significant result. It reframes the interpretation of prior claimed O1-replications and establishes a lower bound on what counts as genuine technical advance. The bitter lesson: the field cannot distinguish real progress from sophisticated imitation without transparency infrastructure.

**Cross-domain transfer from mathematical long-thought training** *(significance: notable)*
Models trained exclusively on math reasoning show substantial improvements in open-domain QA, structured argumentation, and sycophancy resistance. This suggests that long-thought reasoning training induces general cognitive behaviors — systematic analysis, assumption interrogation, structured decomposition — that transfer across domains independently of the training domain's content. See [[themes/chain_of_thought|Chain of Thought]] and [[themes/reasoning_and_planning|Reasoning & Planning]].

---

## Open Questions

- Can the cross-domain transfer benefits of long-thought training be obtained without the factuality regression caused by simulated search interactions?
- Does the safety regression on WildSafety represent a fundamental tension between reasoning depth and safety alignment, or an artifact of training data composition?
- What is the minimum TTI score that constitutes a genuine methodological contribution rather than distillation-with-extra-steps?
- Can inference-time scaling techniques (the opaque core of O1) be independently rediscovered, or does the distillation shortcut permanently redirect research attention?

---

## Themes

- [[themes/alignment_and_safety|Alignment & Safety]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/finetuning_and_distillation|Finetuning & Distillation]]
- [[themes/hallucination_and_reliability|Hallucination & Reliability]]
- [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/math500|MATH500]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/rejection-sampling|Rejection Sampling]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/passk|pass@k]]
