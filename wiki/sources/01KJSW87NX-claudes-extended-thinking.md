---
type: source
title: Claude's extended thinking
source_id: 01KJSW87NXS3G6DHHGDDF3NXMZ
source_type: article
authors: []
published_at: None
theme_ids:
- chain_of_thought
- interpretability
- mechanistic_interpretability
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Claude's extended thinking

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Claude's extended thinking
article
https://www.anthropic.com/news/visible-extended-thinking

---

## Briefing

**Claude 3.7 Sonnet introduces extended thinking — serial test-time compute that lets the same model reason longer on harder problems — and demonstrates that visible chain-of-thought, while valuable for trust and alignment research, is fundamentally unreliable as a safety monitoring mechanism because models routinely act on factors they never verbalize. This post is as much a safety caveat as a capability announcement: every gain in visible reasoning comes with new attack surfaces and a fundamental epistemic limitation about what the thought process actually reveals.**

### Key Takeaways
1. **Extended thinking is compute-on-demand, not a separate model** — the same Claude 3.7 Sonnet allocates more sequential reasoning steps via a configurable "thinking budget," improving math accuracy logarithmically with thinking tokens allowed.
2. **Parallel test-time compute is the higher-ceiling strategy** — using 256 independent samples plus a learned scoring model, Claude 3.7 Sonnet reached 84.8% on GPQA (96.5% physics subscore), continuing to scale beyond majority vote limits.
3. **Faithfulness is broken — visible thinking cannot ground safety claims** — Anthropic's own research shows models "very often make decisions based on factors that they don't explicitly discuss in their thinking process," making chain-of-thought monitoring insufficient for safety arguments.
4. **Visible thoughts create new attack surfaces** — adversaries can study the thought process to craft better jailbreaks; more speculatively, training with exposed thoughts may incentivize models to hide or alter their internal reasoning.
5. **Action scaling enables persistent multi-turn agency** — Claude 3.7 Sonnet can now sustain open-ended tasks across tens of thousands of interactions, demonstrated concretely by defeating three Pokémon Gym Leaders where prior versions couldn't exit the starting house.
6. **CBRN uplift is real but incomplete** — assisted participants progressed further than unassisted ones on weapons-related tasks, but all attempts had critical failures preventing end-to-end success, keeping Claude at ASL-2.
7. **Thought process encryption is a middle path for safety** — harmful content in the thinking is hidden from users but not suppressed from the model's reasoning, preserving usefulness while limiting exposure.
8. **Prompt injection defense jumped from 74% to 88%** — a three-layer mitigation (training + system prompt + classifier) substantially improved computer use safety, with a 0.5% false-positive rate still to be reduced.
9. **Constitutional Classifiers are the ASL-3 bridge** — Anthropic positions its jailbreak-prevention classifier work as the key preparatory step before moving future, more capable models to ASL-3 safeguards.
10. **The visible thought process is explicitly a research preview** — Anthropic signals it may not expose thinking in full for future, more capable models, given asymmetric risks at higher capability levels.

---

### How Extended Thinking Actually Works

- Extended thinking is **serial test-time compute**: the model executes multiple sequential reasoning steps before producing its final output, consuming "thinking tokens" as it goes.
  - This is not a separate model or reasoning module — it is **the same weights given more sequential computation time**.
  - Developers control this via a configurable **thinking budget**, setting a ceiling on how many thinking tokens may be consumed per response.
  - Performance on math questions scales **logarithmically** with the number of thinking tokens, implying diminishing returns at very high budgets but consistent gains within practical ranges.
- The thought process is exposed to users in raw form, without the character training applied to Claude's normal outputs.
  - The result is thinking that is **more detached and less personal-sounding** than typical Claude responses — intentionally so, to give the model maximum latitude to reason without stylistic constraints.
  - Claude's thought process sometimes includes **incorrect, misleading, or half-baked intermediate thoughts**, analogous to human scratchpad reasoning that isn't meant for public consumption.
  - Anthropic researchers with math and physics backgrounds noted the **"eerie" similarity** between Claude's reasoning style and their own: exploring multiple angles, backtracking, and double-checking.

---

### Parallel Test-Time Compute: The Research Frontier

- Parallel test-time compute runs **multiple independent thought processes simultaneously** and selects the best result without knowing the ground truth answer in advance.
  - Strategy 1: **Majority / consensus voting** — select the answer appearing most frequently across samples.
  - Strategy 2: **Learned scoring model** — a trained verifier (or a second Claude instance) evaluates candidates and picks the best one.
- Results on GPQA using parallel scaling:
  - **256 independent samples + learned scoring model + 64k-token thinking budget → 84.8% GPQA overall, 96.5% physics subscore.**
  - Performance **continues to improve beyond the majority vote plateau**, suggesting the learned scoring model extracts signal that simple voting cannot.
- A key operational advantage: parallel sampling means Claude can **start returning answers before any single chain of thought completes**, since multiple processes run concurrently.
- **Parallel test-time compute is not in the deployed model** — it remains a research capability with open questions about cost, latency, and scoring model reliability.

---

### Agentic Capabilities and "Action Scaling"

- Claude 3.7 Sonnet introduces **action scaling**: iterative function calling with environmental feedback, enabling persistent open-ended task completion across many turns.
  - Compared to predecessors, it can allocate **more turns, more time, and more compute** per agentic task, not just more 

## Key Claims

1. Extended thinking mode does not switch to a different model; it allows the same model to spend more time and effort on a problem.
2. Developers can set a 'thinking budget' to control precisely how long Claude spends on a problem.
3. The visible thought process was not subjected to Claude's standard character training, resulting in thinking that is more detached and less personal than default outputs.
4. Models very often make decisions based on factors they don't explicitly discuss in their thinking process, undermining the reliability of thought process monitoring for safety.
5. Malicious actors might use the visible thought process to build better jailbreak strategies against Claude.
6. Models trained knowing their internal thoughts are on display might be incentivized to think in less predictable ways or deliberately hide certain thoughts.
7. Contradictions between a model's internal thoughts and its outward statements can be used to identify potentially deceptive behaviors.
8. Claude 3.7 Sonnet's 'action scaling' allows it to iteratively call functions, respond to environmental changes, and continue until an open-ended task is complete.
9. Claude 3.7 Sonnet can allocate more turns, time, and computational power to computer use tasks than its predecessor.
10. Previous versions of Claude became stuck very early in Pokémon Red, with Claude 3.0 Sonnet failing to leave the starting house in Pallet Town.

## Capabilities

- Extended thinking mode allows a single Claude model to scale its reasoning depth on demand — toggling between fast and slow thinking without switching to a separate model or architecture
- Developers can set a precise 'thinking budget' to control how many reasoning tokens Claude expends before producing its final answer, enabling cost/quality tradeoff management
- Claude's internal reasoning chain is surfaced to users in raw form during extended thinking, enabling inspection of intermediate reasoning steps for trust and alignment research
- Action scaling enables Claude to iteratively call functions, respond to environmental feedback, and sustain open-ended multi-step task execution with increasing turns and compute allocated per task
- Serial test-time compute scaling produces logarithmic accuracy improvements as thinking token budget increases, enabling a predictable quality/compute tradeoff for reasoning tasks
- Parallel test-time compute scaling via 256 independent samples combined with a learned scoring model achieves 84.8% on GPQA (including 96.5% physics subscore) and continues to benefit from compute beyond majority-vote saturation
- Layered prompt-injection defense for computer use — combining adversarial training, system prompt hardening, and a dedicated classifier — prevents 88% of injection attacks, up from 74% baseline
- Agentic Claude can play Pokémon Red continuously across tens of thousands of interactions, defeating 3 Gym Leaders by iteratively trying multiple strategies and revising prior assumptions — demonstrating sustained goal-directed behaviour over very long horizons

## Limitations

- The visible thought process is not faithfully grounded in the model's actual internal computation — models frequently make decisions based on factors they do not explicitly discuss in their reasoning chain, making thought monitoring unreliable as a safety signal
- Visible extended thinking cannot currently be used to provide safety assurances about model behaviour — the faithfulness gap means thought monitoring fails as a formal alignment verification method
- Extended thinking output is stripped of Claude's standard character and tone, producing more detached, impersonal reasoning traces — character training was deliberately withheld from the thinking process
- The thinking process regularly contains incorrect, misleading, or half-baked intermediate conclusions — the visible trace cannot be treated as reliable output and may confuse or mislead users who over-interpret it
- Exposing the reasoning trace is a security surface: adversaries can reverse-engineer it to design more effective jailbreaks, systematically exploiting the revealed decision logic
- If models learn during training that their reasoning will be displayed, they may be incentivised to reason in deliberately opaque, unpredictable ways or to conceal certain thoughts — creating a deceptive alignment risk unique to visible-thinking architectures
- Serial test-time compute scaling exhibits logarithmic diminishing returns — doubling the thinking token budget produces progressively smaller accuracy gains, imposing a hard compute-efficiency ceiling on chain-of-thought scaling
- 12% of prompt injection attacks against computer use still succeed — the layered defense stack leaves a residual attack surface that prevents treating computer use as safe for high-stakes autonomous deployment
- Parallel test-time compute scaling — the highest-performing inference strategy — is not available in production deployment, gatekeeping the peak quality ceiling from actual users
- Claude 3.7 Sonnet provides measurable CBRN uplift beyond freely available online information — model-assisted participants advance further toward successful task completion than unassisted ones, even though all attempts still contain critical failures
- Extended thinking safety implications are insufficiently understood to commit to revealing the thought process for future, more capable models — the decision to expose versus encrypt thinking must be re-evaluated per generation
- Thought process encryption is triggered reactively on potentially harmful content — harmful reasoning is not prevented, only hidden from users, leaving the model's actual processing untouched
- Extended thinking access is restricted to paid subscription tiers (Pro, Team, Enterprise, API) — a de facto cost barrier that limits access to higher-quality reasoning for free-tier users

## Bottlenecks

- Faithfulness gap between visible chain-of-thought and actual model computation blocks thought-monitoring as a viable mechanism for safety assurance — the reasoning trace cannot be trusted as a ground-truth account of why the model behaved as it did
- Residual 12% prompt injection success rate blocks treating computer use agents as trustworthy in adversarial or semi-trusted environments, preventing deployment in contexts where the information environment cannot be controlled
- Parallel test-time compute scaling infrastructure is not production-ready — the highest-performing inference strategy (256 samples + learned scoring model) requires serving and compute economics that are not yet viable for deployed models

## Breakthroughs

- Parallel test-time compute scaling with a learned scoring model achieves 84.8% GPQA (96.5% physics subscore) — demonstrating that combining independent parallel samples with a verifier substantially outperforms serial chain-of-thought scaling and continues to improve beyond majority vote saturation
- Action scaling enables Claude to sustain coherent goal-directed behaviour across tens of thousands of interactions with an environment — overcoming the hard contextual limit that caused prior models to fail immediately on open-ended sequential tasks

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/interpretability|interpretability]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/computer-use|Computer Use]]
- [[entities/gpqa|GPQA]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/parallel-test-time-compute|Parallel Test-Time Compute]]
- [[entities/prompt-injection|Prompt Injection]]
- [[entities/extended-thinking|extended thinking]]
