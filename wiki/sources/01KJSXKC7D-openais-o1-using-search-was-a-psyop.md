---
type: source
title: OpenAI's o1 using "search" was a PSYOP
source_id: 01KJSXKC7DMMZZZK0SK94SYJNJ
source_type: article
authors: []
published_at: '2024-12-04 00:00:00'
theme_ids:
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# OpenAI's o1 using "search" was a PSYOP

**Authors:** 
**Published:** 2024-12-04 00:00:00
**Type:** article

## Analysis

# OpenAI's o1 using "search" was a PSYOP
2024-12-04 · article
https://www.interconnects.ai/p/openais-o1-using-search-was-a-psyop

---

## Briefing

**The apparent "search" capability in OpenAI's o1 is likely an illusion: o1 is best understood as a single language model trained with large-scale outcome-based RL on verifiable tasks, with search emerging implicitly from RL's internal optimization rather than from any explicit tree structure or process reward supervision at test time. The test-time compute scaling plot — widely taken as evidence of controllable search — can be fully explained by sampling multiple completions and bucketing by token count, requiring no search at all.**

### Key Takeaways
1. **o1's "search" is probably just RL** — All apparent search behavior is internal to the RL training process, not an explicit MCTS or tree-expansion mechanism applied at test or train time.
2. **The test-time compute plot may be a sampling artifact** — Plotting win rate vs. tokens used across multiple sampled completions (bucketed post-hoc) produces an inference scaling curve without any search engine.
3. **Standard RLHF is mostly style control** — 80% of Llama 3.1 preference data is "general chat," illustrating how weak its performance signal is compared to o1's verifiable-outcome training.
4. **Verifiable rewards are the key data ingredient** — o1 is trained on problems with checkable answers (math, code, constrained tasks), producing a strong, dense reward signal that enables data efficiency.
5. **Continuations replace process rewards** — LLM-as-a-judge generates corrective next steps when reasoning chains go wrong; unlike PRMs, this supervision is sparse (only on failure) rather than per-step.
6. **RL on reasoning beats human-written CoT** — OpenAI's "Aha!" moment was discovering that RL-trained chain-of-thought outperforms training on human demonstrations of reasoning.
7. **MCTS for language is impractical** — Reliable step-by-step branching requires clean state boundaries that language generation fundamentally lacks, making AlphaZero-style approaches ill-suited.
8. **Emergent self-checking is real and observable** — Tulu 3's RLVR training (pure outcome rewards) spontaneously produced "wait, let me check that" loops in CoT when training ran long, confirming RL induces reasoning behaviors without explicit supervision.
9. **This aligns with the Bitter Lesson** — Constraining the problem domain tightly (verifiable tasks) enabled unbounded compute scaling on RL without degradation, exactly as Sutton's lesson predicts.
10. **Scaling RL training alone may be the bigger story** — Even without controllable test-time compute, the left half of the scaling plot (more RL training → better performance) is potentially a paradigm shift in LM training.
11. **OpenAI likely uses both strong regularization and diverse data** — The ability to run RL longer without degradation implies unusual training stability that ordinary setups don't achieve.
12. **Process rewards may have bootstrapped early training** — The author speculates PRMs could have seeded initial high-quality examples, but does not expect them to be the primary scaled mechanism.

---

### What the Public Narrative Got Wrong

- OpenAI's communications around o1 were shaped to imply the use of explicit search mechanisms, drawing on accumulated hype around Q*, Noam Brown's search team, and AlphaZero-adjacent framing.
  - **This was framing, not disclosure** — no details confirming MCTS or tree search were ever actually provided; the implication was manufactured through selective association.
  - The author's own earlier hypothesis treated o1 as using process rewards at training plus depth-1 search at test time with a step-level verifier — this article argues that hypothesis is wrong.
- The test-time compute scaling plot was the primary piece of "evidence" for controllable search, but its interpretation is ambiguous.
  - The x-axis framing pairs training-time compute (genuinely controllable) with test-time compute in a way that implies symmetrical controllability.
  - **The plot could be entirely synthetic**: sample many completions per prompt, bucket by token length, score each bucket, sort — and you have a scaling curve with zero search.
  - OpenAI would still want to develop actual generation-length control eventually, but this is separate from search.

### The Simpler Hypothesis: Pure RL with Verifiable Rewards

- Professor Sasha Rush's "Speculations on Test-Time Scaling" frames four candidate mechanisms: Guess+Check, Process Rewards, Search/AlphaZero, and Learning to Correct.
  - The author's revised view eliminates Search/AlphaZero and Process Rewards, leaving only **Guess+Check** and **Learning to Correct** as the active mechanisms.
  - These are the two simplest candidates — no tree structure, no per-step supervision infrastructure.
- The core claim: o1 is trained entirely with **outcome-based RL on verifiable tasks**, with LLM-generated corrections providing sparse intermediate guidance when needed.
  - "Verifiable" means: math problems (exact answer), code (unit tests), constrained instructions (rule-checking), and similar domains.
  - The author suspects a large proportion of o1's training data falls in these verifiable categories, which explains the "data-efficient" framing in OpenAI's blog post.
  - OpenAI keeps re-training on prompts; when the model succeeds, it learns from that; when it fails, **continuations** provide a corrective scaffold.

### Continuations vs. Process Rewards

- Continuations are LLM-generated next steps inserted into a reasoning chain at the point of failure, allowing the model to recover and proceed to a correct answer.
  - A judge LLM identifies where the chain went wrong and generates a plausible continuation — effectively acting as a sparse process reward that only fires on failure.
  - **Key distinction from PRMs**: supervision is not required at every step; it only occurs when the final answer is wrong, m

## Key Claims

1. OpenAI's o1 launch was deliberately communicated to suggest the model uses explicit search (beyond naive reinforcement learning) at both training and test time, but this may be misleading.
2. o1-like systems can plausibly be built using exclusively large-scale reinforcement learning with no process/intermediate rewards and no tree-expansion search.
3. The test-time compute scaling plot shown by OpenAI may be an artifact of sampling multiple completions and bucketing by token count, rather than evidence of controllable test-time search.
4. An inference scaling law can be constructed from sampling and bucketing, without using any search.
5. The test-time compute plot implies that compute can be controlled as a generation parameter, which nudges observers toward assuming controllable test-time search.
6. Controllable generation length via prompting is a plausible alternative to branching search for test-time compute control, and was enabled by long-context advancements.
7. Standard RLHF (as in InstructGPT and Llama 3.1) primarily controls style while only marginally improving performance on a few capabilities.
8. 80% of Llama 3.1 preference data consists of general chat, illustrating the weak signal in standard RLHF.
9. o1 is trained primarily on prompts with verifiable answers (math, code, constrained instructions), and this verifiability is the source of its data efficiency.
10. LLM-as-a-judge feedback on intermediate reasoning chains is used to generate continuations — next steps to steer the model back on track when it goes wrong.

## Capabilities

- Large-scale RL training with outcome-based verifiable rewards enables data-efficient reasoning model training without process rewards or explicit test-time search
- LLM-as-judge can identify where a chain-of-thought goes wrong and generate corrective continuations, providing intermediate supervision without formal per-step process rewards
- RL-generated chain-of-thought reasoning outperforms human-written reasoning chains as training data, enabling fully synthetic self-improving reasoning data loops
- Extended RLVR training produces emergent self-correction behaviours (e.g. 'wait, let me check that') in chain-of-thought without explicit step-level supervision

## Limitations

- AlphaZero-style MCTS is structurally impractical for open-ended language generation — a language model cannot reliably generate one reasoning step at a time while branching and verifying at step boundaries
- Standard RLHF primarily controls output style rather than improving core reasoning capabilities — its training signal is fundamentally weak
- Extended RLVR training produces incoherent or degenerate behaviours outside the narrow training domain — task-level generalisation is not maintained past the useful training horizon
- Verifiable reward signals for RL training are confined to narrow constrained domains (math, code with unit tests, instruction-following with constraints) — open-ended tasks have no ground-truth verifier
- OpenAI's approach to verifying open-ended reasoning beyond math and code is entirely opaque — the architecture and scope of their generalised verifiers is unknown and unreplicable
- Process rewards (per-step supervision) are not scalable as a sustained training signal — likely limited to bootstrapping early training data
- RL training stability for reasoning models requires either strong regularisation (which impedes learning) or a large, highly diverse training corpus — both are difficult to achieve simultaneously
- The test-time compute scaling curve for o1 may not represent genuinely controllable inference — it could be an artefact of sampling variance in standard autoregressive decoding rather than active compute allocation

## Bottlenecks

- Maintaining coherent RL reasoning behaviours across a wide variety of tasks during extended RLVR training — without domain-specific overfitting or degenerate outputs emerging
- Verifiable reward signals exist only for narrow constrained domains, limiting the breadth of topics on which o1-style RL reasoning training can be applied

## Breakthroughs

- RL-generated chain-of-thought reasoning surpasses human-written reasoning chains as training data for reasoning models, eliminating the need for expensive expert annotation of thought processes

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/rlhf|RLHF]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/the-bitter-lesson|The Bitter Lesson]]
