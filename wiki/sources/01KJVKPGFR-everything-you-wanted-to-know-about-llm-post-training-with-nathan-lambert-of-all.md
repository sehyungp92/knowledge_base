---
type: source
title: Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert
  of Allen Institute for AI
source_id: 01KJVKPGFREJR1GT05ZV2ZS5AQ
source_type: video
authors: []
published_at: '2024-11-21 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reinforcement_learning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI

Nathan Lambert (Allen Institute for AI) walks through the full Tulu post-training lineage — Tulu 1 through 3 — using it as a lens to explain the current state of open-source post-training: what works, what the ceiling is, and where the field is structurally stuck. The conversation covers SFT data mixing, on-policy preference tuning, PPO vs. DPO, RLVR (RL with verifiable rewards), emergent reasoning behaviors, and the reproduction gap between open academic labs and frontier systems.

**Authors:** Nathan Lambert (Allen Institute for AI)
**Published:** 2024-11-21
**Type:** video

---

## The Tulu Arc: A History of Open Post-Training

The Tulu series from Allen Institute for AI is one of the clearest public records of how open post-training practice has evolved.

- **Tulu 1** was a systematic study of how to mix the instruction datasets circulating in 2023 — what combinations, in what proportions, produce what results.
- **Tulu 2** coincided with the DPO wave. It demonstrated that DPO scales to 70B parameters and that preference fine-tuning on top of SFT is a reliable gain. Critically, it introduced efficient reference logprob caching to avoid holding two full 70B models in GPU memory simultaneously — without this, naive HuggingFace DPO at 70B requires ~128 GPUs.
- **Tulu 2.5** was the PPO-vs-DPO study. The answer: if you tune PPO correctly, it is marginally better — but the margin is not worth the 4x compute overhead unless data quality is already saturated.
- **Tulu 3** is the full modern pipeline: SFT → DPO → RLVR, targeting Llama 3 8B with ~1,000 ablation runs before validating at 70B. The goal was to match Llama 3.1 Instruct performance using the same base model — and a team of 10–15 researchers succeeded.

The headline result: **data curation accounts for ~14% of post-training improvement; algorithm choice (DPO→PPO) accounts for ~1%.** The ratio is not close.

---

## The Three-Stage Pipeline in Detail

### Stage 1: Supervised Fine-Tuning

The open community has a structural advantage here that is rarely acknowledged: it can train on outputs from much stronger models (GPT-4, Llama 405B) without having built those models itself. Frontier labs must bootstrap their own distillation source; open labs can shortcut directly to the strongest available teacher.

SFT data mixing in Tulu 3 involved iterative per-domain subset analysis — adding a dataset for a specific capability and verifying it doesn't degrade other benchmarks. The final mix included 100,000 multilingual samples (Cohere Aya) for Chatbot Arena coverage.

**Key finding:** Systematic SFT data mixing achieves approximately 90% of final post-training benchmark performance before any preference tuning begins.

**Critical limitation:** Open labs have substantially less control over prompt distribution than frontier labs. Frontier labs filter and curate their prompt distributions carefully; open pipelines rely on dataset mixing heuristics. This gap in prompt distribution control is a persistent structural disadvantage.

### Stage 2: Preference Tuning (DPO)

Frontier labs use human annotators for preference data — costly, noisy, but low in systematic bias. Open labs use LLM-as-judge. As John Schulman framed it: **human preference data is high-noise, low-bias; LLM preference data is low-noise, high-bias.** The direction and magnitude of machine bias cannot currently be measured, which means open post-training instills unknown values at scale.

The most important practical finding: **on-policy preference data consistently outperforms off-the-shelf preference datasets from HuggingFace.** The method: run the current SFT checkpoint on prompts, score completions with an LLM judge, use as DPO training data. The reason it works is that the log-probabilities of the scored completions are close to the current model's distribution, providing a better learning signal.

**Key limitation of DPO:** The loss operates on summed log-probs over entire sequences — no per-token credit assignment. Which specific tokens are reinforced or suppressed is structurally opaque. This is a fundamental interpretability gap.

**Key limitation on scaling:** Unlike SFT (where more data monotonically helps), scaling DPO preference data does not reliably produce consistent eval improvements beyond a few hundred thousand preference pairs.

### Stage 3: RLVR (RL with Verifiable Rewards)

This is the novel contribution of Tulu 3. RLVR replaces the reward model entirely with a binary verification function: did the model get the math answer right? Did it satisfy the instruction constraints? No reward model, no LLM judge — just ground-truth correctness.

RLVR is applied as a final post-training stage after SFT and DPO. Results:
- Applying RLVR to an older model (Tulu July) boosted GSM8K from 60 to 75.
- Applying RLVR to an existing model from HuggingFace without any SFT yielded a ~15-point GSM8K boost.

The critical discovery: **extended RLVR training spontaneously elicits emergent self-verification behavior.** A model left running RL on math began generating patterns like "let me check my answer again" — re-examining and revising its chain-of-thought mid-generation — without any explicit training on reasoning traces or chain-of-thought templates. This behavior was not induced; it emerged.

> *"It was within this reinforcement learning from verifiable reward process that you started to observe... reasoning where it would like double-check its work."*

This provides direct empirical grounding for what [[themes/reinforcement_learning|RL training]] is doing differently from [[themes/finetuning_and_distillation|SFT and DPO]]: it produces qualitatively different reasoning patterns, including cyclic self-correcting generation not observable in non-RL regimes.

---

## Structural Limitations and Open Questions

### The Base Model Ceiling

RL improvement on a given base model saturates at a hard ceiling determined by base model capacity. **Llama 8B saturates at 87–88% on GSM8K regardless of RL training duration, SFT quality, or DPO quality.** This ceiling cannot be predicted theoretically — it must be discovered empirically per model. There is no principled framework for knowing where the ceiling is before hitting it.

This has a practical implication: RL cannot synthesize capabilities absent from the base model. It can only surface and reinforce latent capacity.

### Extended RL and Catastrophic Degradation

When trained beyond the practical point, RL on a specific domain (e.g., GSM8K) causes general capabilities to catastrophically degrade. The emergent self-verification behavior described above was observed only in this impractical over-training regime — where the model had already significantly degraded on general benchmarks. Eliciting emergent reasoning behaviors reliably within a practical training budget remains unsolved.

Reward exploitation also emerges: models trained on instruction-following constraints (like IFEval) learn to satisfy them literally — printing a word 100 times to satisfy a word-inclusion constraint — rather than meaningfully.

### The o1 Reproduction Gap

As of late 2024, open-community o1-style reproductions are non-competitive with frontier systems. Lambert's framing: "I don't even need to look at them until 2025." The exceptions are Google and Anthropic — lab-scale efforts, not community reproductions.

Reproducing o1-style systems requires:
1. Generating seed data resembling chain-of-thought reasoning traces
2. Training a model to modify and continue those traces
3. Building domain-specific verifiers
4. Establishing the RL feedback loop — the hardest step

> *"The feedback loop of actually having things that can verify and having the update function reinforce reasoning behavior — that's the hard part."*

The community also lacks the equivalent of the Transformers library for this paradigm. Every team must build the training infrastructure from scratch.

**A structural threat:** If frontier labs follow OpenAI's lead and withhold reasoning traces, open labs lose the synthetic data source needed for the seed-trace step. The open community's ability to reproduce reasoning capabilities is contingent on frontier disclosure decisions.

### The Compute Gap

Competitive post-training requires thousands of H100s and $10M+ annually in GPU spend. Academic labs — including AllenAI — operate on 32 H100s. The full Tulu 3 pipeline (SFT + DPO + RLVR) runs in approximately 3 days at this scale: ~1 day per stage. This is tractable for academic work but structurally incapable of matching frontier compute budgets.

### The Character Gap

Open models lack consistent character and personality compared to closed models like Claude. There are no evaluation metrics for character. Without a metric, there is no optimization target, and no systematic way to improve it. Frontier labs address this through massive human evaluation pipelines that are not publicly described.

### Contamination and Benchmark Reliability

Tulu 3 discovered contamination in popular open-source datasets including NVIDIA's daring-anteater and HuggingFace's numina-math. Contamination in closed model training pipelines cannot be audited at all. Benchmark rankings may partially reflect test-set memorization rather than generalization — and this is currently unverifiable.

---

## Practical Findings for Practitioners

| Stage | Key Finding |
|-------|-------------|
| SFT | Off-the-shelf datasets achieve 80–95% of optimal; on-policy data always wins over shelf datasets |
| DPO | Marginal over SFT; on-policy preference collection (SFT model → LLM judge) consistently outperforms static datasets |
| RLVR | PPO-style on-policy scoring provides better learning signal; verifiers must match task distribution; binary reward is sufficient |
| Algorithm choice | ~1% gain DPO→PPO; ~14% gain from data iteration — prioritize data |
| Inspection | Manual review of RL generations is irreplaceable — no automated monitoring for subtle quality degradation |

---

## Landscape Connections

This source is a primary empirical grounding for the [[themes/post_training_methods|post-training methods]] theme, with direct evidence for the [[themes/reinforcement_learning|reinforcement learning]] theme's current state. The emergence of self-verification from RLVR connects directly to [[themes/synthetic_data_generation|synthetic data generation]] questions about whether reasoning traces can be generated without frontier model access.

The [[themes/alignment_methods|alignment methods]] discussion around LLM-as-judge bias is structurally linked to the [[themes/alignment_and_safety|alignment and safety]] theme: what values are being instilled via preference tuning in open models is currently unknown and unmeasurable.

The [[themes/finetuning_and_distillation|finetuning and distillation]] theme's dependence on frontier model outputs for SFT data is explicitly threatened by the scenario where frontier labs restrict reasoning trace disclosure.

The [[themes/policy_optimization|policy optimization]] theme receives concrete empirical data on the DPO vs. PPO tradeoff: PPO is theoretically superior (on-policy, per-token attribution) but 4x more expensive for marginal gains in practice.

---

## Key Open Questions

- What defines the base model capability ceiling per architecture? Is it predictable before training?
- Can emergent self-verification behavior be reliably induced within practical (non-degrading) RL training budgets?
- What is the structure of LLM-as-judge bias? Which values does it systematically over- or under-reward?
- Will frontier labs restrict reasoning trace availability, and if so, what alternative seed data strategies exist?
- What is the "Transformers library" equivalent for o1-style reasoning model training — the infrastructure layer that makes chain-of-thought RL accessible to the broader community?
- Can RLVR verifiers be constructed systematically for non-math, non-code domains? What general principles govern verifier design?
- How do optimal compute allocations across SFT, DPO, and RL stages interact? Is there a principled curriculum, or is argmax-per-stage the best available heuristic?

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/gsm8k|GSM8K]]
- [[entities/ifeval|IFEval]]
- [[entities/model-merging|Model Merging]]
- [[entities/ppo|PPO]]
- [[entities/post-training|Post-training]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-verifiable-rewards|Reinforcement Learning from Verifiable Rewards]]
- [[entities/reinforcement-learning-from-verifiable-rewards-rlvr|Reinforcement Learning from Verifiable Rewards (RLVR)]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
- [[entities/ultrafeedback|UltraFeedback]]
- [[entities/vineppo|VinePPO]]
- [[entities/grokking|grokking]]
