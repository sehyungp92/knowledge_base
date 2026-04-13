---
type: source
title: On the Fundamental Limits of LLMs at Scale
source_id: 01KJT8B0BV5TFR1NRT0CJN30CV
source_type: paper
authors:
- Muhammad Ahmed Mohsin
- Muhammad Umer
- Ahsan Bilal
- Zeeshan Memon
- Muhammad Ibtsaam Qadir
- Sagnik Bhattacharya
- Hassan Rizwan
- Abhiram R. Gorle
- Maahe Zehra Kazmi
- Nukhba Amir
- Ali Subhan
- Muhammad Usman Rafique
- Zihao He
- Pulkit Mehta
- Muhammad Ali Jamshed
- John M. Cioffi
published_at: '2025-11-17 00:00:00'
theme_ids:
- alignment_and_safety
- hallucination_and_reliability
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# On the Fundamental Limits of LLMs at Scale

This paper presents a unified, proof-informed theoretical framework that formally derives hard performance ceilings for five persistent LLM failure modes — hallucination, context compression, reasoning degradation, retrieval fragility, and multimodal misalignment — grounding each in computability theory, information theory, and statistical learning. By pairing impossibility theorems with empirical corroboration, it shifts the field's framing from "engineering obstacles solvable by scale" to "intrinsic limits that scale cannot overcome," providing a principled basis for architecture-aware, theoretically guided LLM design.

**Authors:** Muhammad Ahmed Mohsin, Muhammad Umer, Ahsan Bilal, Zeeshan Memon, Muhammad Ibtsaam Qadir, Sagnik Bhattacharya, Hassan Rizwan, Abhiram R. Gorle, Maahe Zehra Kazmi, Nukhba Amir, Ali Subhan, Muhammad Usman Rafique, Zihao He, Pulkit Mehta, Muhammad Ali Jamshed, John M. Cioffi
**Published:** 2025-11-17
**Type:** Paper
**Source:** https://arxiv.org/pdf/2511.12869

---

## Motivation

Existing surveys on LLM reliability document empirical failure modes — hallucination, context degradation, reasoning brittleness, retrieval fragility, multimodal misalignment — without connecting them to the mathematical foundations of computation and learning. This leaves practitioners without a principled account of which failures are reducible and which are not.

The observation that GPT-4 achieved a 16-point MMLU gain and a 35-point GSM-8K gain over GPT-3.5 sustained the belief that scale alone can indefinitely extend intelligence. Yet larger models also fail more confidently and systematically. Without formal theory, benchmark scores are interpreted as progress toward elimination of failure, rather than as movement within provably bounded spaces.

---

## Framework

The paper formally derives theoretical ceilings for each of the five failure modes via a common theoretical vocabulary: diagonalization, Kolmogorov complexity, PAC sample-complexity bounds, and information-theoretic rate arguments.

### 1. Hallucination

Hallucination is proved inevitable through a three-tier theoretical hierarchy:

- **Diagonalization** (Theorems 1–2): For any computably enumerable model family, adversarial inputs on which every model fails are guaranteed — not just one, but infinitely many — independent of architecture, training procedure, or scale.
- **Undecidability** (Theorem 3): Problems like the Halting Problem force infinite failure sets for any computable predictor.
- **Finite capacity** (Lemma 1, Theorem 4): Kolmogorov complexity and PAC sample-complexity bounds establish that learning *m* independent binary facts simultaneously requires Ω(m/ε² · log(m/δ)) training examples — prohibitive for long-tail knowledge.

Empirical anchor: GPT-4 factual precision drops below 40% for individuals with fewer than 10 Wikipedia page views per day, compared to >90% for popular entities, directly corroborating the long-tail sample complexity bound.

### 2. Long-Context Compression

Three degradation laws are formalised:

- **Positional undertraining** (Lemma 2): Expected parameter updates for distant token pairs scale as O(p(j)), where p(j) → 0 as position j approaches the training length limit, leaving far-position attention near-initialization. In SlimPajama with a 2048-token window, fewer than 20% of training pairs involve distances in the upper half and fewer than 5% at the extreme end.
- **Sinusoidal encoding attenuation** (Lemma 3): Normalised dot products between positional encodings decay as |1/m Σcos(ωₖΔ)| ≤ 2/(ΩΔ), vanishing as separation Δ → ∞. Vanilla RoPE exhibits analogous long-range damping; extending maximum position without rescaling leads to steep perplexity increases beyond the original training range.
- **Softmax crowding** (Lemma 4, Corollary 1): Maintaining constant attention probability on a relevant token among N distractors requires a score margin that grows as Θ(ln N) — a pressure generic training cannot reliably provide.

Empirical anchor: Llama 3.1 70B, trained to a 128K context window, effectively leverages only ~64K tokens; GPT-3.5-Turbo-16k struggles on LongBench inputs averaging 6.7K words.

### 3. Reasoning Degradation

The reasoning limitation is traced to an objective mismatch between likelihood maximisation and logical entailment:

- The likelihood objective marginalises over chain-of-thought traces (Equation 28), making intermediate reasoning steps causally disposable — empirical mediation analysis finds the indirect effect of CoT traces on final answers is approximately zero on many tasks.
- Outcome-only RL reinforces this misalignment: training to optimise R(Y, Ŷ) = I[Ŷ = Y] imposes no requirement that intermediate steps be causally valid.
- Models favor pattern completion over true inference — likelihood training rewards local coherence, not logical entailment, producing syntactic rather than semantic generalization.

Empirical anchor: PAL (Program-Aided Language Models) achieves ~72% on GSM8K versus 55–65% for chain-of-thought, illustrating that offloading execution to formal symbolic systems partially sidesteps the reasoning gap.

### 4. Retrieval Fragility

RAG is formalised as a constrained optimisation under finite token budget B:

- The relevance–coverage dilemma forces a trade-off between precision-oriented and recall-oriented retrieval that cannot be simultaneously optimised under a fixed context window.
- Information-theoretically, mutual information between retrieved evidence and the target fact decays as retrieval set size grows, and semantic drift under bounded budget induces ranking noise and weak coupling between retrieved and generated text.
- Adversarial corpus poisoning (PoisonedRAG) achieves ~90% attack success rates by inserting only five orthogonally augmented documents per query in million-scale knowledge bases, exploiting the shared embedding manifold.
- Combined failure probability is lower-bounded as: Pr[failure] ≥ 1 − Pr[d* ∈ Dr] · Pr[LLM attends to d*].

### 5. Multimodal Misalignment

Multimodal failure is characterised by architectural colonisation by language:

- Language gradient channels dominate visual gradients by orders of magnitude (VideoLLaMA-7B attends to text tokens 157× more than visual tokens per token).
- CLIP-trained encoders exhibit semantic drift bounded below by √DKL(p_true||p_data) · σc.
- Cross-modal scaling laws are fractured: the effective scaling exponent αeff is bounded within [min(αtext, αvision), max(αtext, αvision)], so the slower-scaling modality constrains aggregate gain.
- MLLMs learn spurious spatial associations based on dataset co-occurrence frequencies rather than encoding actual geometric constraints: ψ(S) ≈ Σ wij · 1[co-occur(oi, oj)].
- Performance degradation scales with the KL divergence between training and test distributions of object-relation co-occurrences.
- Adding visual tokens to language models simply expands the space of spurious correlations without imposing compositional structure — a failure that persists even when models are trained with RL.

---

## Limitations Identified

The paper catalogs an extensive set of theoretical and empirical limitations, distinguished by whether they are engineering obstacles or fundamental ceilings.

**Fundamental/Irreducible:**
- Hallucination is provably inevitable for any computable LLM — diagonalization guarantees infinitely many failure inputs, undecidable problems force infinite failure sets, and finite capacity imposes a non-zero floor ([[themes/hallucination_and_reliability|Hallucination & Reliability]])
- An irreducible noise floor of ~2–3% demonstrably false factual claims in common web scrapes imposes a non-zero hallucination lower bound that persists even with infinite model size ([[themes/pretraining_and_scaling|Pretraining & Scaling]])
- Next-token likelihood training systematically misaligns model learning with logical reasoning — the objective cannot be repaired by scale ([[themes/reasoning_and_planning|Reasoning & Planning]])
- Creativity and factuality are provably in tension: A(θ) + α·C(θ) = κ, so improving one necessitates reducing the other ([[themes/alignment_and_safety|Alignment & Safety]])
- Softmax attention requires O(log N) score margins for relevant tokens as context grows — generic training may not produce these margins ([[themes/long_context_and_attention|Long Context & Attention]])

**Significant but Potentially Tractable:**
- Effective context utilization is substantially shorter than nominal window length — positional undertraining is an artifact of corpus statistics, not a mathematical necessity ([[themes/long_context_and_attention|Long Context & Attention]])
- Sinusoidal and RoPE positional encodings attenuate to near-zero for large separations; architectural alternatives may mitigate this ([[themes/model_architecture|Model Architecture]])
- Multimodal misalignment worsens with modality imbalance — bottleneck regularization to reduce text dominance is proposed as a tractable intervention ([[themes/model_architecture|Model Architecture]])
- Binary evaluation grading in all major benchmarks (MMLU-Pro, GPQA, MATH, SWE-bench, BBH, HLE, Omni-MATH) creates a rational incentive to always guess rather than abstain, distorting the research landscape ([[themes/alignment_and_safety|Alignment & Safety]])

**Systemic/Worsening:**
- Benchmark contamination inflates observed performance by an unquantified margin; models that have seen test examples memorize rather than generalize ([[themes/pretraining_and_scaling|Pretraining & Scaling]])
- Model collapse: LLM-generated data contaminating training corpora for subsequent models causes hallucination errors to become entrenched ground truth, amplifying errors across generations ([[themes/pretraining_and_scaling|Pretraining & Scaling]])
- RLHF/DPO training incentivizes confident, fluent fabrication over honest uncertainty — human annotators systematically prefer confident-sounding responses, embedding this bias in the reward model ([[themes/alignment_and_safety|Alignment & Safety]])
- LLMs cannot distinguish epistemic from aleatoric uncertainty, preventing adaptive sampling strategies; they are systematically overconfident — P[correct | 90% self-assessed confidence] ≪ 0.9 ([[themes/hallucination_and_reliability|Hallucination & Reliability]])

---

## Capabilities Noted

- Scaling produces predictable, large benchmark gains: GPT-4 achieved a 16-point MMLU and 35-point GSM-8K gain over GPT-3.5 — scaling works, within its bounded regime ([[themes/scaling_laws|Scaling Laws]])
- LLMs support context windows of up to 128K tokens, enabling book summarization, multi-document QA, and long conversation memory in broad production use ([[themes/long_context_and_attention|Long Context & Attention]])
- Retrieval-augmented generation reduces hallucination in specific domains by grounding generation in retrieved evidence, even though it cannot eliminate hallucination universally ([[themes/hallucination_and_reliability|Hallucination & Reliability]])
- Capacity-aware diagnostic frameworks can characterize where scaling helps, where it saturates, and where it fundamentally fails — providing principled guidance for LLM design decisions (research stage)

---

## Bottlenecks & Open Questions

The paper identifies several research-blocking constraints:

1. **Absence of formal theoretical frameworks** connecting observed LLM failures to fundamental computational limits blocks principled improvement — researchers cannot distinguish fixable from inherent constraints. Horizon: 1–2 years. ([[themes/scaling_laws|Scaling Laws]], [[themes/hallucination_and_reliability|Hallucination & Reliability]])

2. **Irreducible hallucination floor** from provable theoretical impossibility: finite model capacity and computability limits guarantee non-zero failure rates that no scaling, data curation, or alignment procedure can eliminate. Horizon: possibly fundamental. ([[themes/hallucination_and_reliability|Hallucination & Reliability]])

3. **Left-skewed position frequency distribution** leaves long-range attention parameters near initialization — models are systematically undertrained on late-context token interactions regardless of nominal window size. Horizon: 1–2 years. ([[themes/long_context_and_attention|Long Context & Attention]])

4. **Positional encoding saturation and long-range attenuation** (sinusoidal cancellation, RoPE phase misalignment) fundamentally limits long-range position discrimination. Horizon: 1–2 years. ([[themes/model_architecture|Model Architecture]])

5. **Next-token likelihood training objective** systematically misaligns model learning with logical reasoning — producing pattern completion rather than entailment. Horizon: 3–5 years. ([[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]])

6. **Binary evaluation grading** rewards confident guessing over calibrated abstention, blocking development of uncertainty-aware AI systems and distorting research incentives. Horizon: 1–2 years. ([[themes/alignment_and_safety|Alignment & Safety]])

---

## Key Claims

| Claim | Evidence |
|---|---|
| MLLMs learn spurious spatial co-occurrence associations, not geometric constraints | ψ(S) ≈ Σ wij · 1[co-occur(oi, oj)] |
| Performance degradation scales with KL divergence between training and test co-occurrence distributions | Formal derivation in paper |
| Compositional generalization failures arise from exponential combination space vs. finite training coverage | Multi-way combinations grow exponentially |
| RL training does not resolve compositional gaps with visual inputs | Empirical evidence cited |
| Ambiguous visual inputs trigger textual hallucinations; strong linguistic priors bias visual interpretation | Bidirectional contamination analysis |
| Contrastive decoding only marginally reduces language prior over-reliance | Empirical evaluation |
| Multimodal scaling laws are fundamentally fragmented — power laws break down at modality combination | αeff ∈ [min(αtext, αvision), max(αtext, αvision)] |
| At smaller scales language dominates; at larger scales vision scales slower, creating interference | Non-linear scaling analysis |

---

## Breakthroughs Claimed

- **Formal unification** of five persistent LLM failure modes under a single theoretical framework — establishing these as intrinsic limits rather than engineering artifacts. This is presented as a paradigm-shifting reframing of the reliability problem. (Significance: notable)
- **Unified proof-informed theoretical derivation** of fundamental limits via computability theory, information theory, and statistical learning — the first synthesis connecting all five failure modes to formal impossibility results simultaneously. (Significance: notable)

---

## Themes

- [[themes/alignment_and_safety|Alignment & Safety]]
- [[themes/hallucination_and_reliability|Hallucination & Reliability]]
- [[themes/long_context_and_attention|Long Context & Attention]]
- [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/pretraining_and_scaling|Pretraining & Scaling]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/scaling_laws|Scaling Laws]]

## Key Concepts

- [[entities/alpacaeval|AlpacaEval]]
- [[entities/benchmark-contamination|Benchmark Contamination]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/cot-passk|CoT-Pass@k]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/flashattention|FlashAttention]]
- [[entities/gpqa|GPQA]]
- [[entities/livebench|LiveBench]]
- [[entities/longbench|LongBench]]
- [[entities/mmlu|MMLU]]
- [[entities/model-collapse|Model Collapse]]
- [[entities/position-bias|Position Bias]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/rotary-position-embedding|Rotary Position Embedding]]
