---
type: source
title: Reinforcement Learning via Self-Distillation
source_id: 01KJT1VZTM3QVQ1N93X3DQ5JBB
source_type: paper
authors:
- Jonas Hübotter
- Frederike Lübeck
- Lejs Behric
- Anton Baumann
- Marco Bagatella
- Daniel Marta
- Ido Hakimi
- Idan Shenfeld
- Thomas Kleine Buening
- Carlos Guestrin
- Andreas Krause
published_at: '2026-01-28 00:00:00'
theme_ids:
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement Learning via Self-Distillation

**Authors:** Jonas Hübotter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella, Daniel Marta, Ido Hakimi, Idan Shenfeld, Thomas Kleine Buening, Carlos Guestrin, Andreas Krause
**Published:** 2026-01-28 00:00:00
**Type:** paper

## Analysis

# Reinforcement Learning via Self-Distillation
2026-01-28 · paper · Jonas Hübotter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella et al. (11 total)
https://arxiv.org/pdf/2601.20802

---

### Motivation & Prior Limitations
- Current RLVR methods such as GRPO learn only from a scalar outcome reward per attempt, creating a severe credit-assignment bottleneck that masks rich environmental state information from the learning signal.
  - GRPO estimates advantages from sparse outcome rewards; when all rollouts in a group receive the same (often zero) reward, advantages collapse to zero and learning stalls entirely.
  - The scalar reward is a 1-bit feedback signal: it reveals whether a rollout was wrong but not *what* went wrong, losing information like runtime errors, failing unit tests, or judge evaluations that many verifiable environments already provide.
- Distillation from a strong external teacher provides dense token-level supervision but requires a stronger model than the student, making it inapplicable in online learning where the goal is to push capability beyond existing models.
  - Off-policy distillation also suffers from distribution shift between the teacher's generations and the student's own generation distribution.
- Process reward models (PRMs) improve credit assignment in RLVR by estimating per-step rewards, but they are a distinct model from the student, introducing significant memory overhead, and are still ultimately trained on scalar reward signals rather than rich tokenized feedback.

---

### Proposed Approach
- The paper formalizes **Reinforcement Learning with Rich Feedback (RLRF)**, a generalization of RLVR where the environment returns arbitrary tokenized feedback (runtime errors, unit test failures, LLM judge evaluations) rather than a scalar reward, and introduces **Self-Distillation Policy Optimization (SDPO)** to exploit this feedback without any external teacher.
  - SDPO uses the current policy in two roles simultaneously: as the "student" that generates the original attempt, and as the "self-teacher" — the same model re-prompted with the original question, the environment feedback, and (if available) a successful rollout from the same batch — to re-evaluate log-probabilities of the student's original response in hindsight.
  - The learning signal is a logit-level KL-divergence loss, `LSDPO(θ) = Σ_t KL(πθ(·|x,y<t) ∥ stopgrad(πθ(·|x,f,y<t)))`, which minimizes the divergence between the student's next-token distribution and the feedback-conditioned self-teacher's distribution; the stopgrad prevents the teacher from degenerating toward the student.
  - SDPO's gradient is formally a policy gradient where GRPO's constant per-rollout advantage is replaced by token-position-specific, vocabulary-wide logit-level advantages `A^SDPO_{i,t}(ŷ_{i,t}) = log πθ(ŷ_{i,t}|x,f_i,y_{i,<t}) / πθ(ŷ_{i,t}|x,y_{i,<t})`, enabling dense credit assignment of |y|·(K+1) unique advantages per sequence (top-K approximation with K=100).
- In standard RLVR environments without rich textual feedback, SDPO treats successful rollouts from the same batch as implicit feedback for failed attempts, allowing the self-teacher to identify specific mistakes by comparing the student's attempt to a working solution — unlike GRPO, which assigns the same negative advantage to every token in a failed rollout.
- Two stability improvements are employed: a regularized self-teacher via either exponential moving average (EMA) of parameters or trust-region interpolation with the initial teacher, and the symmetric Jensen-Shannon divergence in place of the KL divergence for the distillation loss.
- The computational overhead is minimal: log-probs for the self-teacher are computed over the existing rollout (no additional generation), adding only 5.8–17.1% wall-clock time per step versus GRPO; memory overhead is avoided via top-K distillation.

---

### Results & Capabilities
- On **LiveCodeBench v6** (competitive programming, 131 questions from Feb–May 2025), SDPO with Qwen3-8B achieves **48.8% final accuracy versus GRPO's 41.2%**, and reaches GRPO's final accuracy in **4× fewer generations**; SDPO also surpasses the strongest instruct models on the public LCBv6 leaderboard, including Claude Sonnet 4 (40.5%) and Claude Opus 4 (39.7%).
  - SDPO particularly improves over GRPO on medium and hard LCBv6 questions, and gains grow with model scale across the Qwen3 family (0.6B, 1.7B, 4B, 8B), consistent with the hypothesis that self-teaching is an emergent property of in-context learning ability.
- On **scientific reasoning and tool use** (RLVR setting without rich textual feedback), SDPO achieves **70.2% vs. 66.6% aggregate accuracy** over GRPO, and learns substantially faster — on Chemistry with Olmo3-7B-Instruct, SDPO achieves GRPO's 5-hour accuracy in **50 minutes of wall-clock training (6× speedup)** and exceeds it by more than 10 percentage points at 5 hours.
- SDPO consistently produces **3× shorter responses on average** than GRPO while achieving higher accuracy, with an extreme case of **11× reduction in response length** on Chemistry with Olmo3-7B-Instruct; qualitative analysis shows GRPO generates filler phrases ("Hmm", "Wait"), circular logical loops, and repeated calculations, while SDPO's generations remain direct.
  - A representative example shows GRPO producing 5,549 tokens with 25 instances of "Wait" and repeated identical calculations ("101.85 ≈ 69.3" appears four times), versus SDPO producing 764 tokens with no circular reasoning, to the same question.
- **Test-Time Self-Distillation** on very hard LCBv6 questions (pass@64 < 0.03 under base Qwen3-8B) achieves **discovery@k 3× faster** than both best-of-k sampling and multi-turn in-context reprompting; SDPO reaches 22% discovery probability with ~3× fewer generations, and solves 53.2% of very hard questions within 2,750 attempts versus 35.6% (multi-turn) and 41.5% (best-of-k).
  - SDPO uniquely solves one question (Q3) that neither best-

## Key Claims

1. Current RLVR methods create a severe credit-assignment bottleneck by learning only from a scalar outcome reward per attempt
2. Many verifiable environments provide rich tokenized feedback (runtime errors, failing unit tests, LLM judge evaluations) beyond scalar rewards that explain why an attempt failed
3. GRPO advantages collapse to zero when all rollouts in a group receive the same reward, causing learning to stall
4. SDPO treats the current model conditioned on feedback as a self-teacher and distills its feedback-informed next-token predictions back into the policy
5. SDPO achieves 48.8% final accuracy on LiveCodeBench v6 versus 41.2% for GRPO, while also outperforming Claude Sonnet 4 (40.5%) and Claude Opus 4 (39.7%)
6. SDPO reaches GRPO's final accuracy on LiveCodeBench v6 in 4× fewer generations
7. SDPO outperforms GRPO in aggregate accuracy on scientific reasoning and tool use tasks: 70.2% vs 66.6% final accuracy
8. SDPO produces responses more than 3× shorter on average across tasks compared to GRPO while achieving higher accuracy
9. SDPO achieves an 11× reduction in response length relative to GRPO on Chemistry with Olmo3-7B-Instruct while maintaining higher accuracy
10. GRPO frequently generates filler phrases like 'Hmm' and 'Wait' or enters circular logical loops, whereas SDPO generates concise responses that avoid these superficial patterns

## Capabilities

- SDPO (Self-Distillation Policy Optimization) enables dense logit-level credit assignment during RL post-training by using the current model conditioned on rich environment feedback as its own teacher, without any external teacher model or separately trained reward model
- SDPO-trained Qwen3-8B achieves 48.8% on LiveCodeBench v6 competitive programming, surpassing Claude Sonnet 4 (40.5%), Claude Opus 4 (39.7%), and the GRPO baseline (41.2%), with 4× fewer training generations to reach GRPO's final accuracy
- SDPO training produces reasoning chains up to 11× shorter than GRPO while achieving higher accuracy, by eliminating circular reasoning, repetition, and filler tokens induced by sparse-reward RL
- Test-time self-distillation (SDPO applied at inference to individual hard problems) compresses interaction history into model weights rather than context, solving problems that neither best-of-k sampling nor multi-turn in-context sampling can solve within the same generation budget — achieving 3× fe
- SDPO bootstraps a model beyond its initial self-teacher capability: during training the student's accuracy surpasses the original teacher's accuracy, demonstrating true capability amplification without an external performance ceiling
- SDPO integrates as a minimal drop-in modification to existing RLVR pipelines by replacing only the advantage estimates in GRPO, requiring no architectural changes and adding only 5.8–17.1% compute overhead
- On-policy self-distillation training avoids catastrophic forgetting better than both off-policy distillation (SFT on teacher outputs) and GRPO, achieving the best performance–forgetting tradeoff across holdout benchmarks (IFEval, ArenaHard-v2, MMLU-Pro)

## Limitations

- SDPO depends on the model's in-context learning ability and underperforms GRPO on weak models below approximately 1.5B parameters — the self-teacher's retrospection ability is an emergent property of scale
- SDPO learning breaks down when environment feedback is uninformative or misleading — the method has no fallback when feedback does not accurately characterise what went wrong
- RLVR methods (including SDPO without rich environment feedback) provide zero learning signal for binary-reward problems until the first solution is independently discovered — making them ineffective at the true capability frontier
- Scalar outcome rewards in standard RLVR mask information about why an attempt failed, creating a fundamental information bottleneck that limits credit assignment granularity across the entire generated sequence
- SDPO not yet validated on open-ended tasks without verifiable rewards — the retrospection mechanism's effectiveness for alignment, creative generation, or continuous-reward tasks is entirely unknown
- Multi-turn in-context sampling at test time hits the transformer context window after approximately 837–1007 steps for hard problems, causing performance to plateau and stall — a fundamental constraint of the attention mechanism
- GRPO and standard RLVR training systematically induces verbose, circular reasoning — with models generating repeated filler phrases ('Hmm', 'Wait'), loops, and redundant calculations — as an emergent training artifact
- SDPO has not been tested with frontier-scale models or at the scale of full multi-task RL training runs — the approach may not generalise at scale beyond Qwen3-8B and Olmo3-7B
- Test-time self-distillation still fails to find a solution within 2750 attempts for approximately 46.8% of very hard questions (pass@64 < 0.03), showing it does not fully solve the hard-problem discovery challenge
- SDPO's benefit over GRPO is significantly reduced or reversed for combined SDPO+GRPO hybrid training on stronger models — the scalar reward signal from GRPO may actively corrupt learning when the model is already a strong in-context learner
- Off-policy self-distillation (SFT on teacher-generated successes) substantially underperforms on-policy SDPO and leads to worse catastrophic forgetting, revealing that distribution shift between student and teacher is harmful unless corrected by on-policy training
- Including the student's original attempt in the self-teacher's reprompt context biases the teacher toward the student's approach, reducing exploration diversity and lowering the entropy of the output distribution

## Bottlenecks

- Binary/scalar rewards in RLVR create a cold-start problem at the capability frontier: learning is impossible on problems the model cannot yet solve even once, because zero reward provides zero gradient signal — blocking RL-driven capability amplification beyond current skill ceiling
- SDPO and similar self-distillation RL methods are gated by an emergent in-context learning threshold — below a model scale threshold (~1.5B), the self-teacher cannot accurately retrospect failures, blocking the approach from smaller/edge-deployed models
- Lack of rich tokenized environment feedback beyond scalar rewards in most RL training pipelines blocks adoption of RLRF methods — the RLRF paradigm requires environments that expose structured failure signals (runtime errors, test outputs), which most existing RL environments do not provide

## Breakthroughs

- Self-Distillation Policy Optimization (SDPO) demonstrates that a language model can use itself as its own dense credit-assignment teacher by conditioning on its failure feedback — eliminating the requirement for a stronger external teacher or separately trained process reward model to achieve token-
- Test-time self-distillation (SDPO applied per-question at inference) solves hard problems inaccessible to both best-of-k sampling and multi-turn in-context sampling, by compressing multi-turn interaction history into model weights rather than context — circumventing the transformer context window bo
- SDPO training demonstrates that verbosity and circular reasoning in RLVR-trained models is an artifact of sparse credit assignment, not a necessary property of deep reasoning — dense feedback produces reasoning chains up to 11× shorter with higher accuracy, directly contradicting the prevailing scal

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/qwen3|Qwen3]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/verl|verl]]
