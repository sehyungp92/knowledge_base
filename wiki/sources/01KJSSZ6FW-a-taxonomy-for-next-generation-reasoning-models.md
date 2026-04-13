---
type: source
title: A taxonomy for next-generation reasoning models
source_id: 01KJSSZ6FW6S8SCHDWRGJ6G103
source_type: article
authors: []
published_at: '2025-06-04 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# A taxonomy for next-generation reasoning models

**Authors:** 
**Published:** 2025-06-04 00:00:00
**Type:** article

## Analysis

# A taxonomy for next-generation reasoning models
2025-06-04 · article
https://www.interconnects.ai/p/next-gen-reasoners

---

## Briefing

**Reasoning models are entering a second generation where the bottleneck shifts from skill acquisition (solving hard self-contained problems via RLVR) to planning — specifically the abilities of strategy and abstraction needed to operate effectively as autonomous agents over long time horizons. This matters because the path from 1-hour to 4+-hour autonomous task completion in 2026 requires deliberate, supervised seeding of planning behaviors through cold-start data and eventual end-to-end RL on long-horizon, sparse reward tasks — neither of which will emerge automatically from current training pipelines.**

### Key Takeaways
1. **Four-tier capability taxonomy** — Skills → Calibration → Strategy → Abstraction defines the development order for reasoning models, where the first two are native single-pass abilities and the latter two are prerequisites for effective agency.
2. **RLVR unlocked skills; planning must be explicitly trained** — DeepSeek R1 proved training-time RL compute translates to performance, but planning abilities require deliberate cold-start SFT data seeding before RL can refine them.
3. **Overthinking is a structural side-effect of RL training** — The coupling between RL and inference-time scaling caused models to overthink easy problems; calibration is currently patched by users via model selectors and thinking budgets, not by the model itself.
4. **Parallel compute and linear chain-of-thought scaling are fundamentally different** — Parallel sampling (o1-pro, Claude 4's internal scorer) adds robustness and consistency, not new skills, and suppresses rare tokens as a side effect.
5. **Strategy failure is hard to recover from** — In autoregressive generation, an early wrong directional choice is often irreversible; agents improve this marginally by editing plans but remain heavily susceptible.
6. **Abstraction requires multi-scale task decomposition** — Future agents must break multi-day tasks into 1-2 minute inference steps (10-100K tokens), a granularity challenge that barely exists at current task horizons but becomes critical as horizons extend.
7. **o3 leads on skills, Claude 4 leads on software planning** — o3 excels at niche search (a skill, not planning) but fails at broad synthesis; Claude Code's planning advantage may simply be training to iteratively revise its plan.
8. **Academic research is misaligned with deployment needs** — Research heavily targets skill benchmarks (math, code) and calibration, but the planning subsets critical for agents are underrepresented and hard to evaluate outside costly full-system contexts.
9. **Planning is output-focused, not behavior-focused** — Unlike reasoning chains, which required novel behavioral initialization, planning is about results and should partially transfer from existing hard math/code behaviors, making cold-start seeding tractable.
10. **The real race is usable systems, not frontier benchmarks** — Pushing models toward nearly-impossible math or top competitive programming has diminishing value; the priority should be systems people actually deploy on real-world tasks.
11. **Context management is an underappreciated planning sub-skill** — An agent's ability to maintain a running state summary — skipping completed tasks, recovering from failed approaches — is foundational to generalized planning.
12. **Quality/rare-token anti-correlation is a structural cost of parallel compute** — Majority voting and reward-model-based selection systematically suppress novel outputs because reward models have never scored rare tokens before.

---

### The Four-Tier Taxonomy: What Each Level Means

- **Skills** are the ability to solve self-contained problems and are the foundation everything else builds on.
  - Measured by frontier evaluations: Humanity's Last Exam, MATH, AIME, LiveCodeBench, Aider Polyglot.
  - All major AI labs have launched or will launch reasoning models in the current cycle, explicitly because of skills gains.
  - Skills are the direct output of RLVR training and the mechanism by which RL compute translates to benchmark performance.

- **Calibration** is the ability to match compute spend to problem difficulty without user assistance.
  - Currently, calibration is a **user-level problem**, not a model-level one: model selectors, reasoning toggles, thinking budget forcing, and effort selectors all offload this judgment.
  - Thinking budget forcing is mechanically implemented by suppressing the `</think>` token and appending "wait" to force longer reasoning.
  - RL loss functions can enforce length control more precisely than instruction tuning or preference tuning — a structural advantage that should eventually enable model-native calibration.
  - Reasoning models already better express confidence, which should translate into overthinking mitigations.
  - **Calibration is commercially important** (faster, cheaper, more profitable outputs) but is not the critical path to new agentic use-cases.

- **Strategy** is the ability to choose the right high-level plan before committing to a generation path.
  - **The core problem**: in autoregressive generation, the first few tokens determine the entire trajectory, and wrong directions are often unrecoverable.
  - Agents can edit their plans, which provides some recovery capability, but they remain heavily susceptible to early strategic errors.
  - Current models do very light or implicit planning — only a priori planning in agentic workflows will substantially narrow the search space.

- **Abstraction** is the ability to decompose strategy into sub-problems of appropriate granularity.
  - Too-hard sub-tasks: no progress is made. Too-small sub-tasks: the model times out.
  - The current time horizon is short enough that abstraction is a minor problem, but as horizons extend to multi-day tasks, models must decompose into **individual 

## Key Claims

1. The first generation of reasoning models brought inference-time scaling; the second generation will bring new types of agentic language modeling applications.
2. The four key capabilities of reasoning models — Skills, Calibration, Strategy, and Abstraction — must be developed in that sequence for progressively more complete reasoning on complex tasks.
3. Skills and Calibration are native single-inference-pass abilities, while Strategy and Abstraction are needed specifically to build effective agents.
4. Scaling RLVR (Reinforcement Learning with Verifiable Rewards) enables models to learn useful skills for solving downstream tasks, first confirmed publicly by DeepSeek R1.
5. Models will generate more tokens per response as they discover new skills, and all four taxonomy abilities can be further tuned by increasing token spend per component.
6. The rush for skill acquisition has caused a second-order problem of models overthinking even easy problems, due to the deep coupling of RL training and the unlock of inference-time scaling.
7. The ideal goal for calibration is that models scale inference-time compute proportionally to actual problem difficulty on their own, without user intervention.
8. Currently, calibration is offloaded to users via model selectors, reasoning on/off buttons, thinking budget forcing, and reasoning effort selectors.
9. RL loss functions are flexible enough to enable precise length control in a way that instruction or preference tuning loss functions cannot.
10. Parallel test-time compute does something fundamentally different from scaling underlying RL training — it adds robustness and answer quality rather than unlocking new skills.

## Capabilities

- All major AI laboratories have deployed reasoning models with step-change performance on frontier evaluations (Humanity's Last Exam, MATH, AIME, LiveCodeBench, Aider Polyglot) via RLVR skill acquisition
- Parallel test-time compute via sampling multiple sequences and selecting the best via an internal scoring model is in confirmed production use at frontier labs (Claude 4, o1-pro)
- o3 demonstrates leading cross-domain skill acquisition spanning math, code, and search, with planning-adjacent capabilities exemplified by Deep Research for niche information retrieval
- Claude Code (Claude 4) demonstrates stronger planning for software engineering agentic tasks compared to OpenAI's Codex, representing differentiated planning maturity across labs
- RLVR-trained reasoning models express calibrated confidence better than instruction-tuned models, laying groundwork for automated overthinking mitigation
- RL loss functions enable precise token-length control that instruction tuning and preference tuning cannot achieve — demonstrated in research settings
- Thinking budget manipulation via end-of-thinking token suppression and 'wait' injection allows forcing extended reasoning depth in deployed reasoning models

## Limitations

- Frontier reasoning models do very little planning on hard problems unless explicitly prompted — planning is not an emergent default behavior from RLVR training
- o3 fails at synthesis tasks requiring comparison across broad information categories — can find niche facts but cannot plan the structured gathering and analysis of many diverse sources
- Calibration of reasoning effort to problem difficulty is not intrinsic to current models — it is entirely offloaded to users via model selectors, on/off toggles, and thinking budget controls
- Reasoning models systematically overthink trivially easy problems as a direct side-effect of RLVR training coupling token spend with skill acquisition
- Planning capabilities (Strategy and Abstraction) required for agentic tasks are not present by default in current generation reasoning models — prompting provides only partial mitigation
- Wrong initial strategy direction in a single autoregressive pass is not recoverable — the stream of tokens locks in a plan that cannot be revised mid-generation without explicit edit mechanisms
- Parallel inference-time scaling systematically suppresses rare and novel tokens — majority voting and reward models consistently downweight outputs not represented in their training distribution
- Deep Research and Codex exhibit high output variance — oscillating between masterpiece and dud results — revealing that current planning capabilities are brittle and unreliable across runs
- No academic benchmarks adequately capture the strategy and abstraction components of planning needed for effective agentic systems — research community is over-indexed on math skills
- Models cannot reliably decompose multi-day agentic tasks into appropriately-sized sub-problems solvable in 1-2 minute inference steps (10-100K tokens) — abstraction at this granularity is currently unsolved
- Agentic context management — tracking completed tasks, avoiding revisiting finished work, recovering from failed strategies across long episodes — is not reliably implemented in current models
- Planning capability development requires expensive manual annotation of training traces encoding both high-level strategy and sub-task abstraction before RL training can be applied
- Planning and agentic capabilities can only be meaningfully evaluated in full system context with substantial inference costs — isolated benchmark evaluation is insufficient and systematically misleading
- Agent time horizons are saturating at approximately 1 hour with current models — the Skills improvement from RLVR is exhausted and further gains require planning capabilities not yet trained in
- Parallel compute scaling (sampling + scoring) does not unlock new model skills — it adds robustness and quality assurance on existing capabilities only; it is qualitatively different from training-time RL compute

## Bottlenecks

- Planning capabilities (Strategy + Abstraction) are the critical missing training objective blocking agent time horizon expansion from ~1 hour to 4+ hours — RLVR has not produced these behaviors and no scalable training approach exists yet
- Cold-start training data for planning behaviors requires expensive manual annotation of high-quality strategy and abstraction traces — no automated pipeline exists to bootstrap this data at scale
- Intrinsic difficulty-proportional compute allocation is unsolved in training — models cannot autonomously scale inference compute in proportion to task hardness, forcing user-side workarounds
- End-to-end RL training on long-horizon sparse agentic tasks is not yet feasible — planning capabilities must first be bootstrapped via SFT before RL can provide useful learning signal on multi-hour tasks

## Breakthroughs

- Parallel test-time compute with internal scoring model transitions from research prototype to confirmed production deployment at frontier labs, establishing it as a standard component of frontier model serving

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/deep-research|Deep Research]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/parallel-test-time-compute|Parallel Test-Time Compute]]
- [[entities/rlvr|RLVR]]
- [[entities/o3|o3]]
