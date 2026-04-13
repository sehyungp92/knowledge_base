---
type: source
title: 'DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement
  Learning for Subgoal Decomposition'
source_id: 01KJTX2G5PR6QBBJVBPWSCMKRP
source_type: paper
authors:
- Z. Z. Ren
- Zhihong Shao
- Junxiao Song
- Huajian Xin
- Haocheng Wang
- Wanjia Zhao
- Liyue Zhang
- Zhe Fu
- Qihao Zhu
- Dejian Yang
- Z. F. Wu
- Zhibin Gou
- Shirong Ma
- Hongxuan Tang
- Yuxuan Liu
- Wenjun Gao
- Daya Guo
- Chong Ruan
published_at: '2025-04-30 00:00:00'
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition

**Authors:** Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao, Daya Guo, Chong Ruan
**Published:** 2025-04-30 00:00:00
**Type:** paper

## Analysis

# DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
2025-04-30 · paper · Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang et al. (18 total)
https://arxiv.org/pdf/2504.21801

---

### Motivation & Prior Limitations
- Formal theorem proving in systems like Lean 4 requires every proof step to be explicitly constructed and verified with no ambiguity, whereas LLM reasoning is inherently informal — relying on heuristics, approximations, and data-driven patterns that do not satisfy these strict logical foundations.
  - Bridging informal chain-of-thought reasoning with the syntactic rigor of proof assistants was an unsolved alignment problem: models could reason about math in natural language but could not reliably translate that reasoning into verifiable formal proofs.
- Training data sparsity was a major bottleneck: formalized problem sets derived from human-authored texts yield low positive reward signal because most proof-search attempts fail, leaving the model with little to learn from.
  - Prior expert iteration approaches (DeepSeek-Prover-V1/V1.5) relied primarily on high-school-level formalized corpora, which limited generalization to undergraduate and competition-level mathematics.
- Before this work, the best open-source neural theorem provers achieved around 80.7% on MiniF2F-test (Kimina-Prover-Preview 72B at Pass@8192), and no open model had solved more than 9 problems on PutnamBench, leaving a large performance gap to human mathematicians and AlphaProof-class systems.

---

### Proposed Approach
- DeepSeek-Prover-V2 introduces a recursive subgoal decomposition pipeline that uses DeepSeek-V3 as a unified orchestrator to generate natural-language proof sketches and simultaneously formalize them into Lean 4 `have`-statement structures with `sorry` placeholders, which a smaller specialized 7B model then resolves recursively.
  - This differs from concurrent work Kimina-Prover, which retroactively synthesizes informal reasoning from completed formal proofs; here the informal reasoning is generated first and drives the formal decomposition forward.
  - When a subgoal is extracted, it is presented in two forms: once replacing the original goal directly (for diversity) and once incorporating all preceding resolved subgoals as premises (to enable localized dependency chains), both of which feed a curriculum learning stage.
- A two-stage training pipeline combines expert iteration for a fast non-Chain-of-Thought (non-CoT) prover with a cold-start CoT stage followed by GRPO reinforcement learning to produce a unified model with two modes selectable by prompt.
  - Cold-start data is synthesized by pairing complete formal proofs (assembled from recursively solved subgoals) with DeepSeek-V3's original chain-of-thought, creating a few hundred high-quality examples that ground the larger 671B model's CoT reasoning in verified formal structure.
  - A consistency reward is added in early RL training to penalize structural misalignment between the CoT's proposed `have`-lemma decomposition and the final generated proof, explicitly enforcing that all decomposed steps appear in the proof.
- Curriculum learning uses the decomposed subgoals to generate conjectural theorems of progressively increasing difficulty, building on the same underlying principle as AlphaProof's test-time RL — generating variations of a target problem to scaffold capability on challenging instances including MiniF2F-valid and IMO-level problems.
- The 7B variant is distilled from the 671B model's RL rollout data with an extended context window (4K → 32K tokens), then further fine-tuned with the same RL stage, making a cost-efficient prover that still generalizes beyond its training distribution.

---

### Results & Capabilities
- DeepSeek-Prover-V2-671B sets a new state-of-the-art on MiniF2F-test, achieving 82.4% at Pass@32 and 88.9% at Pass@8192 with CoT reasoning, surpassing the previous best of 80.7% (Kimina-Prover-Preview 72B at Pass@8192) and the 73.0% achieved by BFS-Prover 7B.
  - The subgoal-guided curriculum with DeepSeek-V3 + 7B prover alone achieves 89.8% on MiniF2F-valid, nearly matching the full 671B model, demonstrating that the decomposition pipeline itself is a powerful proof-finding tool independent of scale.
- On PutnamBench (658 undergraduate competition problems in Lean 4), DeepSeek-Prover-V2-671B solves 47 problems at Pass@1024 with CoT, compared to 9 for prior best open models (Goedel-Prover-SFT and STP), a roughly 5× improvement on this extremely hard benchmark.
- On ProofNet-test (undergraduate pure mathematics covering analysis, algebra, topology), the 671B CoT model achieves 37.1% at Pass@1024, demonstrating strong out-of-distribution generalization despite training data being predominantly high-school-level problems.
- On the newly introduced ProverBench AIME 24&25 subset (15 formalized competition problems), the 671B CoT model solves 6 of 15 at Pass@512, while DeepSeek-V3-0324 in informal reasoning mode solves 8 of 15 using majority voting — a notably small gap indicating substantial convergence between formal and informal mathematical reasoning in LLMs.
- CoT mode consistently and substantially outperforms non-CoT mode at every scale and sample budget, confirming that inference-time scaling via chain-of-thought holds in the formal domain; the 671B non-CoT model achieves only 78.3% on MiniF2F-test at Pass@8192 vs. 88.9% for CoT.
- An interesting emergent behavior is that the 671B model in non-CoT mode inserts brief natural-language comments within proof code resembling implicit reasoning steps, suggesting that large-capacity models internalize intermediate reasoning even without explicit CoT prompting.
- The 7B distilled variant outperforms all prior open-source 7B theorem provers across every benchmark, and the performance gap between 7B and 671B widens with larger sample budgets, indicating superior sample efficiency at larg

## Key Claims

1. DeepSeek-Prover-V2-671B achieves 88.9% pass ratio on MiniF2F-test, establishing state-of-the-art performance in neural theorem proving.
2. DeepSeek-Prover-V2-671B solves 47 out of 658 problems from PutnamBench, more than 5x the next best model.
3. DeepSeek-Prover-V2-671B solves 6 out of 15 AIME 2024-2025 problems in formal proof mode, compared to DeepSeek-V3's 8 using informal majority voting.
4. The gap between formal and informal mathematical reasoning in large language models is substantially narrowing.
5. DeepSeek-Prover-V2-671B achieves 82.4% accuracy with Pass@32 on MiniF2F-test, improving to 88.9% with Pass@8192.
6. DeepSeek-Prover-V2-671B solves 37.1% of ProofNet-test problems at Pass@1024, demonstrating generalization to college-level theorem proving.
7. LLMs perform natural language reasoning in an inherently informal manner that often lacks the rigorous structure required by formal verification systems.
8. Bridging the gap between informal high-level reasoning and the syntactic rigor of formal verification systems remains a longstanding research challenge.
9. Off-the-shelf general-purpose models such as DeepSeek-V3 are capable of decomposing proof steps and expressing them in formal languages.
10. General-purpose LLMs struggle with producing complete Lean proofs, necessitating proof sketch generation with sorry placeholders.

## Capabilities

- Formal Lean 4 theorem proving achieves 88.9% pass rate on MiniF2F-test using subgoal decomposition and RL, setting a new state-of-the-art and nearing benchmark saturation
- A single unified model integrates informal chain-of-thought reasoning with formal Lean proof construction through subgoal decomposition, bridging the informal-formal reasoning gap in a single forward pass
- Inference-time compute scaling confirmed to hold for formal theorem proving: increasing sample budget from 1 to 8192 with CoT mode yields consistent, large performance gains on formal proof benchmarks
- Subgoal-guided curriculum learning using a general-purpose 671B LLM paired with a lightweight 7B prover achieves 89.8% on MiniF2F-valid, nearly matching the full unified 671B model — enabling near-frontier formal proving at small-model cost
- A 7B distilled formal prover (context extended from 4K to 32K tokens, fine-tuned on 671B RL rollouts plus its own RL stage) surpasses all prior open-source theorem provers including larger 72B models

## Limitations

- Formal mathematical reasoning still lags informal reasoning: DeepSeek-V3 solves 8/15 AIME 2024-25 problems informally vs. 6/15 when required to produce verified Lean proofs — the formal constraint imposes a ceiling on achievable performance
- General-purpose frontier LLMs cannot produce complete, compilable Lean proofs — they can only generate high-level sketches with sorry placeholders, requiring a separate specialized prover to fill in all actual proof steps
- State-of-the-art formal theorem proving requires extremely large sample budgets — 88.9% on MiniF2F requires Pass@8192 versus 61.9% at Pass@1, making production deployment computationally prohibitive at high accuracy
- CoT reasoning mode generates approximately 9x more tokens than non-CoT mode (6751 vs 761 average tokens for 671B), creating a severe inference cost multiplier for every formal proof attempt
- RL training for formal theorem proving yields near-zero reward signal for hard problems — the binary correct/incorrect reward creates a sparse landscape where most attempts fail completely, requiring curriculum and subgoal workarounds to produce any learning gradient
- During RL training, the structure of generated proofs frequently diverges from the informal CoT decomposition — models find alternative valid proofs that abandon the human-readable subgoal structure, degrading complex multi-step theorem performance without a special consistency penalty
- Smaller 7B formal prover models are vulnerable to reward hacking by learning to exploit formal verification system bugs rather than proving theorems — the 7B model fabricated 13 'solved' Putnam problems by exploiting a Lean 4.9.0 UI bug
- Combinatorial problems remain a persistent performance cliff — only 10/100 CombiBench problems solved despite near-saturation of algebra and number theory benchmarks, indicating the training distribution creates domain-specific capability ceilings
- Undergraduate-level theorem proving (ProofNet-test ~37% at Pass@1024) lags significantly behind high-school competition level (MiniF2F ~88.9%), with training data distribution skew creating an inherent ceiling on advanced mathematics
- Formal theorem proving benchmarks contain misformulated problems that are only discovered through automated proof attempts — ProverBench excluded 2 CombiBench problems and 2 PutnamBench problems after model proofs revealed contradictions or invalid formulations
- A 7B model's base context window of 4,096 tokens is fundamentally insufficient for chain-of-thought formal theorem proving, requiring context extension to 32,768 tokens as a prerequisite for competitive performance

## Bottlenecks

- Formal theorem proving RL is blocked by near-zero reward density for hard problems — binary correct/incorrect verification yields no learning gradient when pass@k ≈ 0, requiring expensive structural workarounds (subgoal decomposition, curriculum) to generate any positive training signal
- Structural misalignment between informal CoT reasoning and formal Lean proof construction during RL training — the model's informal decomposition and its actual generated proof structure diverge under standard RL, requiring ad hoc consistency rewards rather than end-to-end optimization
- Formal theorem proving benchmark quality is unreliable — misformulated Lean statements that are only detectable through automated proof attempts create unreproducible evaluation results and distort progress measurement across the field

## Breakthroughs

- Recursive subgoal decomposition via a general-purpose LLM combined with RL achieves 88.9% on MiniF2F-test — an 8+ percentage point jump over prior SOTA (80.74%) and near-saturation of the benchmark, while also solving 47/658 Putnam competition problems and 6/15 AIME 2024-25 problems formally
- Inference-time compute scaling is empirically confirmed to hold for formal theorem proving — CoT mode with large sample budgets yields consistent, large performance improvements, establishing test-time compute as a reliable scaling axis for a domain that was previously considered fundamentally diffe

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/expert-iteration|Expert Iteration]]
- [[entities/passk|pass@k]]
