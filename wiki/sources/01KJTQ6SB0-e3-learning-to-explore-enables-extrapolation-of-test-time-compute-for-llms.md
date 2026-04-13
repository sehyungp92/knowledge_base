---
type: source
title: 'e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs'
source_id: 01KJTQ6SB0CMGZ7EKYGMYAWPGD
source_type: paper
authors:
- Amrith Setlur
- Matthew Y. R. Yang
- Charlie Snell
- Jeremy Greer
- Ian Wu
- Virginia Smith
- Max Simchowitz
- Aviral Kumar
published_at: '2025-06-10 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs

**Authors:** Amrith Setlur, Matthew Y. R. Yang, Charlie Snell, Jeremy Greer, Ian Wu, Virginia Smith, Max Simchowitz, Aviral Kumar
**Published:** 2025-06-10 00:00:00
**Type:** paper

## Analysis

# e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs
2025-06-10 · paper · Amrith Setlur, Matthew Y. R. Yang, Charlie Snell, Jeremy Greer, Ian Wu et al. (8 total)
https://arxiv.org/pdf/2506.09026

---

### Motivation & Prior Limitations
- Most existing reasoning models fail to extrapolate: when given test-time compute budgets beyond their training budget, they show negligible performance improvement rather than the continued gains the test-time scaling paradigm promises.
  - Empirically, multiple open-source models (R1-1.5B, OpenThinker-7B, DeepScaleR, STILL-3, II-Thought, Open-RS1) trained with both RL and SFT recipes show near-zero accuracy gain from 16k to 32k tokens on AIME 2025, despite pretraining context windows being 2–4× larger than the post-training budget.
  - Standard RL and SFT recipes do not teach models to implement algorithmic procedures (generate-verify-revise, search, backtracking) within their chain of thought; instead they tend to exploit short-cut solutions that terminate at training-budget length.
- SFT-based approaches are structurally incapable of producing extrapolating models because they only apply positive gradients on correct traces, reinforcing the model to terminate within the length of training examples and suppressing the diversity needed for exploration.
- Prompting-based budget extension (e.g., appending "Wait" tokens as in s1) is insufficient: it forces more tokens but does not teach the model to use them productively for structured search.

---

### Proposed Approach
- The paper introduces e3 (exploration enables extrapolation), a post-training recipe with three coupled ingredients that train a model to perform in-context exploration — structured search within a single forward pass by chaining generation, verification, and refinement operations.
- **Ingredient 1 — Chaining asymmetric capabilities**: The recipe exploits the verification-generation (VG) gap, where the base LLM is more reliable at verifying answers than generating them. By training the model to chain verification after generation (and iterating), in-context search emerges naturally without external tools. The formal definition (Definition 3.1) characterizes chaining as the policy benefiting from the composition q(p(·)) even though the optimal policy never needs to call q.
  - This differs from prior work that observed VG gaps empirically; e3 formalizes their necessity and designs the entire training recipe around exploiting them.
- **Ingredient 2 — Leveraging negative gradients in RL**: The negative gradient (the policy gradient term from incorrect traces, present in REINFORCE, PPO, and GRPO) reduces the probability mass on short incorrect responses including their EOS tokens, redistributing it onto longer traces that chain additional asymmetries (e.g., "Wait, let me verify…" instead of terminating). This is shown to increase token entropy, response diversity, and the number of chained verification steps.
  - This is mechanistically distinct from SFT (pure positive gradient) and from GRPOMask (RL with negative gradient zeroed out), both of which fail to increase response length or enable extrapolation. A formal theorem (Thm. 5.1) proves that a negative gradient step increases entropy proportional to (π(a₁|s) − π(a₂|s))² when the correct action is unlikely.
  - The paper introduces the didactic pₖ-model — a bigram MDP where the LLM makes k sequential attempts with perfect verification — to formally distinguish two RL phases: in-context exploration (negative gradient lowers p(stop), increasing k) versus sharpening (positive gradient improves p, the per-attempt success rate).
- **Ingredient 3 — Coupled curriculum over data difficulty and token budget**: Rather than fixing a single dataset and budget, e3 stages training by jointly increasing task difficulty and the training budget. A criterion (Eq. 6.1) selects the smallest budget B*_tr such that doubling to 2B yields less than κ=1.2× improvement, ensuring the budget is large enough for chaining but small enough for stable optimization.
  - Training at too-short budgets penalizes long exploratory traces by rewarding them negatively (they overrun the budget before finding the answer). Training at too-long budgets causes high-variance long-horizon RL instability. The coupled curriculum is the key insight: varying only data or only budget is shown empirically to be insufficient.
  - Applied to Qwen3-1.7B: Stage 1 trains on easy DMath problems at B_tr=8k; Stage 2 trains on medium+hard DMath at B_tr=16k.

---

### Results & Capabilities
- e3-1.7B achieves state-of-the-art performance among all models under 2B parameters on AIME 2025 and HMMT 2025, outperforming the next-best <2B model by more than 8% absolute on AIME 2025 peak performance.
  - pass@1 on AIME 2025: e3-1.7B scores 43.8% vs. Qwen3-1.7B (35.5%), R1-distill-Qwen-1.5B (23.1%), Nemotron-Reasoning-1.5B (33.6%).
  - pass@1 on HMMT 2025: e3-1.7B scores 24.7% vs. Qwen3-1.7B (22.2%) and Nemotron-Reasoning-1.5B (17.4%).
- The model trained at a maximum budget of 16k extrapolates consistently to 32k tokens (2× training budget), while all baseline open-source models plateau before 16k.
  - At 32k tokens, e3-1.7B outperforms s1.1-32B and OpenThinker-7B on AIME 2025, despite being 19–19× smaller in parameter count.
- Unlike the prevailing trend where RL training improves pass@1 at the cost of pass@k (i.e., sharpening), e3 improves pass@k for all k up to 32 over the Qwen3-1.7B base model, indicating it discovers genuinely new solutions rather than collapsing diversity.
  - pass@32 on AIME 2025: e3-1.7B at 67.2% vs. Qwen3-1.7B at 65.2%; on HMMT 2025: 56.1% vs. 54.9%.
- The VG-gap experiments on Countdown (Cdown) and n-digit multiplication (Mult) confirm the causal role of asymmetries: RL training on Cdown (high VG gap) yields steady length increases and extrapolation to 8–16× training budget, while Mult (low VG gap) shows negligible extrapolation improvement despite identica

## Key Claims

1. Most existing reasoning models do not extrapolate well when test-time compute is scaled beyond the maximum token budget they were trained on.
2. Performance gains from test-time scaling diminish for open-source reasoning models as the test-time budget increases, with virtually no gains from 16k to 32k tokens.
3. Training LLMs to perform in-context exploration — chaining operations such as generation, verification, and refinement — enables extrapolation of test-time compute beyond the training token budget.
4. The verification-generation (VG) gap — where models are more capable of verifying answers than generating correct ones — is a prerequisite asymmetry for enabling in-context exploration via RL.
5. RL training on problem domains with a VG gap encourages chaining of asymmetric skills, enabling in-context exploration that can discover new solutions and extrapolate to larger budgets.
6. A base model without VG asymmetry improves accuracy by at most 2% despite 16x test-time compute scaling, while a base model with VG asymmetry can still extrapolate well.
7. Models with greater VG gap exhibit less KL divergence from the base model, potentially implying better generalization.
8. The negative gradient in RL — gradients from incorrect traces with negative advantage — is a key enabler of in-context exploration when the base model presents asymmetries.
9. Negative gradients promote diverse responses during RL training by preventing entropy collapse over the next-token distribution.
10. The negative gradient moves probability mass from the EOS token in incorrect responses, repurposing it to increase the probability of chaining new asymmetric skills, resulting in greater response leng

## Capabilities

- The e3 recipe trains a 1.7B model to reliably extrapolate test-time compute to 2x its training token budget (16k→32k), achieving SOTA performance at <2B scale on AIME'25 (43.8% pass@1) and HMMT'25 (24.7% pass@1), outperforming some 7B and 32B models at large inference budgets
- LLMs can be trained to implement in-context search by chaining verification (easy) with generation (hard) within a single autoregressive trace, discovering correct answers through sequential self-verification that improves monotonically with more test-time compute
- The negative gradient component of RL training (gradients from incorrect traces) provably increases token distribution entropy and drives exploration by redistributing probability mass from short failed responses toward longer asymmetry-chaining sequences, enabling better test-time extrapolation
- A coupled curriculum over both problem difficulty and token budget, designed so each stage chooses the smallest budget that still rewards chaining asymmetries, enables stable long-horizon RL training that develops genuine in-context exploration, outperforming budget-only or data-only curriculum vari

## Limitations

- Virtually all existing open-source reasoning models trained with current RL/SFT recipes show near-zero performance gains when test budget exceeds training budget by 1.5–2x — test-time compute scaling saturates hard at the training-budget boundary
- SFT post-training cannot enable test-time compute extrapolation: it only reinforces correct traces at fixed lengths, strengthening early-stopping behavior rather than exploration, and cannot amplify the number of sequential attempts (k) needed for extrapolation
- When the base model lacks a verification-generation gap, RL post-training cannot develop in-context exploration — 16× more test-time compute yields ≤2% accuracy improvement, making extrapolation essentially impossible regardless of training recipe
- Autoregressive repetition bias creates a hard practical ceiling on in-context exploration chain length — base models begin repeating previously generated segments beyond certain output lengths, blocking further exploration regardless of nominal budget
- Long-horizon RL training at very large token budgets (≥16k) suffers from high gradient variance, producing models that perform worse at their own training budget than a model trained at 8k and extrapolated — directly training at very long budgets is not feasible
- Masking negative gradients in RL (as in online SFT/STaR) causes token distribution entropy collapse, producing responses that degenerate into repeating token streams when tested at budgets beyond training — making these methods structurally unable to extrapolate
- Training on hard problems at token budgets shorter than typical base model response lengths penalizes in-context exploration from the outset, producing models committed to terse answers that fail to generalize out-of-distribution and cannot extrapolate
- Budget-forcing extrapolation via prompting ('Wait') is substantially weaker than trained in-context exploration — prompting forces token generation but cannot direct it toward useful verification-chaining behavior, making it an ineffective substitute for exploration-trained models
- The e3 recipe has only been validated at 1.7B parameter scale and on mathematical reasoning domains — generalizability to larger model scales and non-mathematical reasoning is explicitly unverified

## Bottlenecks

- Absence of verification-generation asymmetry in base models blocks test-time compute extrapolation — without a competence gap where verification is easier than generation, RL post-training cannot develop the in-context exploration chains needed to productively use compute beyond the training budget
- Autoregressive repetition bias creates a hard ceiling on productive in-context exploration chain length — base models begin repeating previously generated segments beyond certain output lengths, preventing exploration chains from extending further regardless of nominal budget increase
- Long-horizon RL optimization instability constrains the maximum token budget at which stable RL training is feasible — policy gradient variance grows with horizon length, causing models trained at very long budgets to converge worse than models trained shorter and extrapolated, requiring curriculum 

## Breakthroughs

- e3 demonstrates a systematic, reproducible recipe for genuine test-time compute extrapolation in small LLMs: a 1.7B model trained with e3 reliably improves from 4k to 32k tokens (2x training budget), outperforming models up to 32B parameters at large inference budgets
- Theorem 5.1 formally proves that negative gradient RL steps increase token distribution entropy when the correct action is unlikely, providing the first theoretical grounding for why outcome-reward RL (not SFT) enables in-context exploration and predicting entropy collapse when negative gradients ar

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/budget-forcing|Budget Forcing]]
- [[entities/deepscaler-dataset|DeepScaleR Dataset]]
- [[entities/grpo|GRPO]]
- [[entities/passk|pass@k]]
