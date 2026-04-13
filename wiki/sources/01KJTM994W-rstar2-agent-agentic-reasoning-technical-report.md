---
type: source
title: 'rStar2-Agent: Agentic Reasoning Technical Report'
source_id: 01KJTM994WR8NQRXJYD7Z74EHT
source_type: paper
authors:
- Ning Shang
- Yifei Liu
- Yi Zhu
- Li Lyna Zhang
- Weijiang Xu
- Xinyu Guan
- Buze Zhang
- Bingcheng Dong
- Xudong Zhou
- Bowen Zhang
- Ying Xin
- Ziming Miao
- Scarlett Li
- Fan Yang
- Mao Yang
published_at: '2025-08-28 00:00:00'
theme_ids:
- agent_systems
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# rStar2-Agent: Agentic Reasoning Technical Report

**Authors:** Ning Shang, Yifei Liu, Yi Zhu, Li Lyna Zhang, Weijiang Xu, Xinyu Guan, Buze Zhang, Bingcheng Dong, Xudong Zhou, Bowen Zhang, Ying Xin, Ziming Miao, Scarlett Li, Fan Yang, Mao Yang
**Published:** 2025-08-28 00:00:00
**Type:** paper

## Analysis

# rStar2-Agent: Agentic Reasoning Technical Report
2025-08-28 00:00:00 · paper · Ning Shang, Yifei Liu, Yi Zhu, Li Lyna Zhang, Weijiang Xu et al. (15 total)
https://arxiv.org/pdf/2508.20722

---

### Motivation & Prior Limitations
- Long Chain-of-Thought (CoT) reasoning — "thinking longer" — is fundamentally insufficient for hard problems requiring subtle intermediate verification or creative reasoning shifts, because models rely on internal self-reflection which frequently fails to detect or correct mistakes.
  - Models using pure CoT cannot reliably self-correct when an initial approach is flawed; they lack mechanisms to validate intermediate steps externally.
  - Scaling test-time compute via long CoT alone (as in o-series, DeepSeek-R1, Gemini-2.5) has driven recent gains but hits a ceiling on problems where intermediate errors compound.
- Agentic RL with coding tools introduces severe environment noise: models generating incorrect code receive environment error messages unrelated to the reasoning task, causing them to waste tokens fixing tool errors rather than advancing reasoning.
  - Under naive GRPO with outcome-only rewards, trajectories with failed intermediate tool calls still receive positive reward if the final answer is correct, reinforcing the model to treat tool errors as acceptable; error rates plateau at ~15% for Qwen2.5-32B and ~10% for Qwen3-14B.
- Large-scale agentic RL imposes infrastructure bottlenecks that prior systems did not address: a single training batch can trigger tens of thousands of concurrent tool calls, and multi-turn rollouts with variable lengths cause severe GPU idle time and KV cache overflow under static allocation.

---

### Proposed Approach
- rStar2-Agent introduces three coordinated innovations to make agentic RL effective at scale: a high-throughput isolated code execution infrastructure, the GRPO-RoC algorithm, and a compute-efficient multi-stage training recipe that avoids reasoning-heavy SFT.
- **GRPO-RoC (Group Relative Policy Optimization with Resampling on Correct)** addresses environment noise under outcome-only rewards through asymmetric trajectory sampling: it oversamples 2G rollouts, then downsamples to G by uniformly subsampling negative trajectories (preserving failure diversity) while filtering positive trajectories to retain only those with minimal tool errors and format violations.
  - Each positive trajectory is scored by tool error ratio (num_error_calls / num_all_calls; trajectories with no tool calls assigned perr=0.5 to encourage tool use) and a format penalty for structural violations (e.g., redundant answer blocks), then sampled inversely proportional to total penalty.
  - Unlike step-level rewards or explicit tool-error penalties (used by Kimi, Li et al.), GRPO-RoC maintains a minimal answer-only outcome reward, avoiding reward hacking and preserving exploration during early training when reasoning is still developing.
  - Additional GRPO modifications include: removing the KL divergence penalty to allow free exploration of tool-augmented reasoning patterns, applying Clip-Higher (εhigh=0.28 vs standard 0.2) to better explore high-entropy forking tokens, and removing entropy loss to prevent training collapse.
- **Reliable High-Throughput Code Environment** is a distributed service across CPU cores of 64 AMD MI300X GPUs capable of handling 45K concurrent tool calls per step with mean latency of 0.3 seconds, isolated from the main training process via a master-node task queue with 32 send workers and worker nodes each running 1024 execution workers.
  - Answer correctness verification (Math-Verifier) is offloaded asynchronously to this service to prevent CPU-intensive rule-based checks from blocking GPU rollouts.
- **Load-Balanced Rollout Scheduler** dynamically assigns rollout requests based on available KV cache capacity per GPU rather than static even distribution, dispatches tool calls asynchronously upon generation, and reassigns new requests in real time as GPUs free cache — eliminating the compounding idle time and KV cache overflow/recomputation that plague static allocation in multi-turn settings.
- **Training Recipe** begins with a non-reasoning SFT stage (165K function-call data + 30K instruction-following + 27K chat) to instill only tool formatting and instruction compliance without enhancing reasoning, then runs three GRPO-RoC RL stages with progressively increasing max lengths (8K→12K→12K) and difficulty, totaling only 510 RL steps on 64 MI300X GPUs completed in one week.
  - Stage 1 (300 steps, 8K max): trains on full 42K curated math problems; Stage 2 (85 steps, 12K max): extends length once clipping ratio stabilizes; Stage 3 (125 steps, 12K max): offline-filters to 17.3K harder problems (those not solved by all 8 rollouts from the Stage 2 final policy).
  - Data curation enforces integer-only answers to avoid verifier failures on algebraically equivalent expressions, sourcing 100K candidates from DAPO training set, AoPS via OpenMathReasoning, and Project Euler, cleaned to 42K high-quality pairs.

---

### Results & Capabilities
- rStar2-Agent-14B achieves 80.6% pass@1 on AIME24, 69.8% on AIME25, and 52.7% on HMMT Feb. 2025, surpassing DeepSeek-R1 (671B) at 79.8%/70.0%/44.4% and outperforming o3-mini (medium), Claude Opus 4.0 (Think), and QWQ-32B on AIME24 by 1.0%, 3.6%, and 1.1% respectively — using a 14B model trained in 510 RL steps.
  - This is achieved without reasoning-specific SFT; starting from near-zero on AIME (3.3% after non-reasoning SFT), GRPO-RoC alone drives performance to frontier level.
- rStar2-Agent-14B produces significantly shorter responses than comparable models: 9,340 tokens on AIME24 and 10,943 on AIME25, versus DeepSeek-R1-Zero (671B) at 14,247/17,133, Qwen3-14B at 14,748/17,522, and QWQ-32B at 11,868/15,865.
- Despite being trained exclusively on math data, rStar2-Agent-14B generalizes: it achieves 60.9% on GPQA-Diamond (science reasoning), surpassing DeepSeek-V3 (59.1%); 60.8% on 

## Key Claims

1. rStar2-Agent-14B achieves 80.6% pass@1 on AIME24, surpassing DeepSeek-R1 (671B), o3-mini (medium), and Claude Opus 4.0 (thinking)
2. Long Chain-of-Thought reasoning is fundamentally limited for hard problems because internal self-reflection often fails to detect mistakes or self-correct when the initial approach is flawed
3. Agentic RL with Python coding tools enables models to verify intermediate steps and explore alternative solutions, complementing internal self-reflection when long CoT alone is insufficient
4. Under outcome-only reward schemes, trajectories with incorrect intermediate tool calls can still receive positive reward if the final answer is correct, causing the model to treat tool errors as accep
5. GRPO-RoC significantly reduces tool-call errors in positively rewarded trajectories compared to naive GRPO, which plateaus at ~10-15% error rate
6. GRPO-RoC uses asymmetric sampling: oversampling 2G rollouts, filtering positive trajectories for quality while uniformly downsampling negative trajectories to preserve failure diversity
7. The agentic RL infrastructure handles up to 45K concurrent tool calls per training step with average latency of 0.3 seconds per call
8. Static rollout allocation in agentic RL causes GPU idle time, synchronization delays, and KV cache overflow due to high variability in multi-turn rollout lengths
9. A dynamic load-balanced rollout scheduler that assigns requests based on available KV cache capacity eliminates GPU idle time and prevents KV cache overflow
10. Multi-stage RL training with progressively increasing response length (8K→12K→12K tokens) achieves frontier-level math reasoning in only 510 total RL steps

## Capabilities

- A 14B model (rStar2-Agent-14B) achieves frontier-level math reasoning via agentic RL, surpassing the 671B DeepSeek-R1 on AIME24 (80.6% vs 79.8%) and matching it on AIME25 (69.8% vs 70.0%), while producing significantly shorter responses (9,339 vs 17,132 tokens on average)
- Agentic RL with Python code tools enables 'smarter' reasoning — models learn to invoke tools at the right reasoning step, reflect on execution feedback, verify intermediate results, and self-correct by generating alternative code, going beyond merely 'thinking longer'
- Frontier-level math reasoning achievable with only 510 RL training steps on 64 AMD MI300X GPUs completed in one week — roughly 10–100x fewer steps than competing methods (DeepSeek-R1-Zero: >9K steps; DAPO: >5K steps; MiMo: 175K steps)
- GRPO-RoC (Resample-on-Correct) algorithm addresses environment noise in agentic RL without reward hacking — asymmetric oversampling filters noisy tool-error trajectories from the positive set while preserving failure diversity in negatives, continuously reducing tool errors (unlike naive GRPO which 
- High-throughput isolated code execution environment supports up to 45,000 concurrent tool calls per training step with 0.3-second average end-to-end latency, removing code execution as a training bottleneck for large-scale agentic RL
- Math-only agentic RL generalizes to science reasoning without any science training data — rStar2-Agent-14B achieves 60.9% on GPQA-Diamond, surpassing DeepSeek-V3 (59.1%) despite zero science data in training
- Agentic RL induces an emergent 'reflection token' behavior: upon receiving tool execution feedback, the model generates dense high-entropy token sequences to diagnose errors, explore alternatives, and refine reasoning — a qualitatively distinct cognitive pattern absent from pure CoT models
- Non-reasoning cold-start SFT (tool formatting and instruction following only, no reasoning data) followed by RL achieves stronger final reasoning than reasoning-heavy SFT warmup, by avoiding SFT overfitting and keeping initial responses short for efficient RL exploration

## Limitations

- RL training collapses irreversibly once the model reaches its pretraining capacity ceiling — after peak accuracy, continued training causes both policy and reward signals to collapse, and no known fix (temperature increase, length extension, more tool turns, higher clip ratio, optimizer reset) recov
- Long chain-of-thought reasoning fundamentally fails on hard problems with subtle intermediate errors or requiring creative reasoning shifts — internal self-reflection does not detect mistakes and cannot self-correct when the initial approach is flawed
- Under naive outcome-only GRPO, tool error rates in positively-rewarded trajectories plateau at ~15% (Qwen2.5-32B) and ~10% (Qwen3-14B) — the training signal actively reinforces incorrect tool use if the final answer happens to be correct
- Rule-based math verifiers (e.g., Prime, math verifier) fail to recognize algebraically equivalent answer expressions — cannot confirm that (a+b)(b+c)(c+a) and (a+c)(c+b)(b+a) are equal — forcing training data to be restricted to integer-answer problems only
- Agentic RL training demonstrated only on math problems with Python coding tools — generalization of the approach (including the reflection token behavior and GRPO-RoC) to other domains or non-coding tools is explicitly unresolved
- Math-only agentic RL provides zero improvement on non-reasoning tasks such as general tool-use (BFCL v3) and instruction following (IFEval) — performance on these remains frozen at the SFT baseline
- N-gram repetition heuristics incorrectly filter legitimate verification behaviors (e.g., running two similar tool calls with different inputs to double-check a result) — simple pattern matching cannot distinguish undesirable repetition from purposeful self-verification
- Overly complex or fine-grained intermediate reward signals (step-level rewards, tool-error penalties) introduce bias that hinders effective RL exploration — the model is penalized for genuinely useful behaviors during early training when capabilities are still developing
- Static rollout allocation in standard RL infrastructure causes severe GPU idle time and KV cache overflow in multi-turn agentic settings — variable turn counts and token lengths create compounding imbalances that waste a significant fraction of compute
- Overlong rollout filtering (discarding truncated rollouts without reward, as proposed by DAPO) backfires in practice — it increases the proportion of overlong rollouts rather than decreasing them by removing the negative feedback signal that discourages repetitive length inflation
- Python code tokens are implicitly low-entropy (model is highly confident) because of extensive pretraining on code corpora — the model's coding tool effectiveness is partly a function of pretrained Python familiarity, not purely the agentic RL training signal
- Training data restricted to integer-answer problems only — over 60K candidate problems reduced to 42K after removing problems with non-integer, unverifiable, or complex-format answers — excluding a large fraction of real mathematical problems from RL training
- 32B scale experiments limited to only the first two of three RL stages due to compute constraints — the strongest training configuration (Stage 3 on hard problems) was not evaluated at 32B scale, making the full comparison incomplete

## Bottlenecks

- Pretraining capacity is a hard ceiling for RL-based reasoning improvement — RL cannot extend a model's reasoning capabilities beyond what was latent in pretraining, and attempting to push past this ceiling causes irreversible training collapse that no current hyperparameter or scheduling fix can rec
- Verifiable reward signals exist only for domains with symbolic or integer ground truth — outside of competitive math and formal program execution, there is no reliable automatic verifier, blocking agentic RL from being applied to most real-world reasoning tasks
- Tool-induced environment noise in agentic RL corrupts training quality — code errors in intermediate steps mislead the model into generating long, low-quality trajectories, and standard outcome-only rewards reinforce this by rewarding any trajectory that reaches a correct final answer regardless of 

## Breakthroughs

- A 14B model trained with agentic RL surpasses the 671B DeepSeek-R1 on competitive math benchmarks (AIME24: 80.6% vs 79.8%) while using 47x fewer parameters and producing 45% shorter responses — demonstrating that algorithmic efficiency via agentic tool use can substitute for raw scale
- GRPO-RoC (Resample-on-Correct) demonstrates that environment noise in agentic RL can be addressed through asymmetric trajectory sampling rather than reward engineering — filtering noisy positive trajectories while preserving failure diversity, without introducing new reward hacking vectors

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/sglang|SGLang]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/verl|verl]]
