---
type: source
title: Generative AI’s Act o1
source_id: 01KJT0NENFWGH8SKG9Z3X2YWYQ
source_type: article
authors: []
published_at: '2024-10-09 00:00:00'
theme_ids:
- agent_systems
- ai_market_dynamics
- frontier_lab_competition
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Generative AI’s Act o1

**Authors:** 
**Published:** 2024-10-09 00:00:00
**Type:** article

## Analysis

# Generative AI's Act o1
2024-10-09 · article
https://www.sequoiacap.com/article/generative-ais-act-o1/

---

## Briefing

**The AI field is undergoing a fundamental architectural shift from training-time compute ("System 1" pattern matching) to inference-time compute ("System 2" deliberate reasoning), exemplified by OpenAI's o1 — and this shift is not merely a model improvement but a new scaling law that unlocks a qualitatively different class of agentic applications. The implications cascade from research labs through the investment stack: reasoning R&D is "cool again" via deep RL, cognitive architectures are becoming the real moat at the application layer, and the addressable market is expanding from software seats to the multi-trillion-dollar services economy.**

### Key Takeaways
1. **A new scaling law has opened** — inference-time (test-time) compute now follows its own scaling curve: the more compute a model is given at inference, the better it reasons, independent of pre-training scale.
2. **o1 is the AlphaGo moment for LLMs** — like AlphaGo, o1 uses search/simulation across candidate reasoning chains at inference time, scored by a value function, rather than returning the first pattern-matched response.
3. **Deep RL is the enabling mechanism** — o1 is trained with reinforcement learning over chains of thought, and emergent behaviors (backtracking, novel problem-solving strategies) arise from scaling inference time.
4. **The value function is the hard part** — scoring reasoning quality is trivially easy for Go (simulate to end) or code (run tests), but unsolved for open-ended tasks like writing, which explains o1's domain skew toward math/science/coding.
5. **Cognitive architectures are the real application moat** — application-layer companies are not "wrappers"; they encode domain-specific reasoning workflows that general models cannot efficiently replicate.
6. **The business model shifts from seats to outcomes** — AI-native companies sell work ($ per resolution, $ per outcome), not software licenses, targeting the services profit pool measured in trillions, not the software market.
7. **Multi-agent systems are the next multiplier** — once individual agents can reliably do work, teams of agents can accomplish vastly more, modeling social learning and parallel reasoning processes.
8. **Incumbents face a deeper threat than appreciated** — the "AI-native" transition may be as disruptive as the on-prem-to-SaaS shift, requiring wholesale reinvention of EPD, GTM, and business models that most incumbents failed to execute historically.
9. **The copilot-to-autopilot arc is the deployment pattern** — companies earn trust by deploying human-in-the-loop first, using those reps to justify removing the human, as exemplified by GitHub Copilot.
10. **"Move 37" is the target state** — a general AI system producing superhuman, genuinely novel outputs is the horizon; this would not require "waking up" but would constitute AGI as the next technology phase, not a singular event.
11. **Foundation model layer is commoditizing** — GPT-4 price per token fell 98% since launch; the model layer is a knife-fight with no winner, making the application and reasoning layers the venture opportunity.
12. **Last-mile app providers hold domain data advantages** — real-world domain-specific data and cognitive architectures remain hard to encode in general models, giving application-layer companies a durable edge.

---

### The o1 Architecture: AlphaGo Applied to Language

- **o1 represents the first example of a general-purpose LLM with true inference-time reasoning**, achieving this not through architectural novelty in the transformer but through a training and inference regime borrowed conceptually from AlphaGo.
  - AlphaGo was pre-trained on ~30 million human Go moves, then at inference time ran Monte Carlo tree search across future scenarios, scoring each path and selecting the highest expected-value move.
  - **The key insight is that AlphaGo's performance scales with inference time**: with zero inference-time compute it cannot beat top humans; with more compute it surpasses them.
  - o1 applies this logic to language: rather than returning the first predicted token sequence, the model generates multiple reasoning chains, evaluates them, and returns the highest-scoring response.
- **The actual implementation of o1 is not publicly disclosed**, but analysis of its chain-of-thought outputs suggests RL training over reasoning traces.
  - The model uses reinforcement learning to reward chains of thought that lead to correct outcomes, teaching the model which reasoning patterns are productive.
  - **Emergent behaviors observed**: backtracking when stuck (not explicitly trained), spatial visualization for geometry problems, and novel solution strategies in programming competitions that differ from human approaches.
- **The value function problem is the central unsolved challenge for inference-time compute.**
  - For Go: simulate the game to completion, observe the winner, compute expected value — fully automated and dense signal.
  - For code: execute the output and check whether tests pass — automated, reasonably dense signal.
  - For open-ended tasks (essays, summaries, itineraries): no automated ground truth exists, making reward signal construction difficult and domain coverage uneven.
  - This is why **o1 is comparatively stronger on math, science, and coding** — domains with verifiable correct answers — and weaker on unstructured, subjective tasks.

---

### The New Scaling Law: Inference-Time Compute

- **Pre-training scaling laws are well understood**: more data and compute during training yields predictable capability improvements, following power-law curves (Chinchilla-style).
- **The o1 paper establishes a second, orthogonal scaling axis**: allocating more compute at inference time (test-time compute) independently improves reasoning quality.
  - This creates a two-dimensional scaling surface: model capab

## Key Claims

1. OpenAI's o1 is the first example of a model with true general reasoning capabilities, achieved through inference-time compute.
2. Inference-time compute involves asking the model to stop and think before giving a response, which requires more compute at inference time.
3. Pre-trained models rely on training-time compute, and basic reasoning emerges as a property of scale but remains very limited.
4. AlphaGo was first pre-trained on approximately 30 million moves from previous games and self-play to mimic human experts.
5. AlphaGo at inference time runs a search or simulation across a wide range of potential future scenarios, scores those scenarios, and responds with the highest expected value scenario.
6. AlphaGo's performance scales with inference-time compute: with zero inference-time compute it cannot beat the best human players, but as inference time scales it surpasses them.
7. The key difficulty in applying AlphaGo-style inference-time compute to LLMs is constructing the value function for scoring open-ended responses.
8. Scoring is relatively tractable for coding (test execution) and math, but difficult for open-ended tasks like essay writing or travel planning.
9. o1 is comparatively strong on domains proximate to logic such as coding, math, and the sciences, and weaker on open-ended and unstructured domains like writing.
10. o1's key implementation involves reinforcement learning applied to the chains of thought generated by the model.

## Capabilities

- OpenAI o1 performs inference-time reasoning via a 'stop and think' mechanism — generating candidate responses, scoring them, and selecting the highest-expected-value answer — with emergent backtracking, human-analogous visualization strategies, and novel problem-solving approaches as properties of s
- o1-class reasoning models achieve strong performance on verifiable structured domains — coding, mathematics, and sciences — significantly above prior-generation instinctual pre-trained models
- AI automated penetration testing (XBOW) matches the performance of the most highly skilled human pentesters, enabling continuous automated security testing at a fraction of the cost of human engagements
- Multi-step agentic software engineering — Factory's droid agents decompose complex software tasks (PR review, backend migration), propose changes, add unit tests, execute across files in dev environments, and merge code conditionally on test passage
- AI-native CRM generation (Day.ai) — with only email/calendar access and a one-page questionnaire, AI automatically generates and continuously maintains a fully tailored CRM with zero ongoing human input
- Agentic AI customer support (Sierra) performs complete issue resolution end-to-end with graceful human escalation, delivered as outcome-based pricing (per resolution) rather than per-seat software licensing

## Limitations

- o1-class reasoning models are structurally weaker on open-ended, unstructured domains (writing, creative tasks, subjective judgment) compared to verifiable domains — the performance asymmetry is fundamental, arising from the absence of a computable reward function
- No principled method exists for constructing reward/value functions for open-ended knowledge work — scoring essay drafts, travel itineraries, or document summaries in a way that enables inference-time search is an unsolved theoretical problem
- Foundation models have largely failed to become standalone breakout products — despite strong API capabilities, only ChatGPT has succeeded as a direct consumer product, indicating systematic difficulty converting raw model capability into end-user value
- Mainstream enterprise deployment of raw foundation models is blocked by hallucinations, black-box opacity, and clumsy workflow integration — the gap between API-level capability and enterprise-deployable reliability remains wide
- No evidence of continuous self-improvement through broad-domain self-play — the capability required for AI 'takeoff' has not been demonstrated despite significant investment, implying that the value function problem for general domains is unsolved at the self-play level too
- Domain-specific reasoning cannot be efficiently encoded in general-purpose models — the messy real world requires custom cognitive architectures that horizontal foundation models cannot substitute for
- Fully autonomous 'autopilot' AI deployment is not yet reliable enough for mainstream rollout — the systematic pattern of 'copilot first, autopilot later' reveals that unassisted operation has error rates too high to deploy without human fallback
- Inference-time compute scaling requires a wholesale infrastructure shift from pre-training clusters to dynamic 'inference clouds' — this capital-intensive transition has not yet occurred, creating a deployment bottleneck for o1-class capabilities at scale
- o1 implementation details are not publicly disclosed — actual mechanisms of inference-time RL training over chain-of-thought remain trade secrets, blocking independent replication and open research on inference-time scaling
- Gathering real-world domain data and encoding application-specific cognitive architectures remains hard for any given vertical — this systematically advantages last-mile application providers over general model labs
- Incumbent SaaS companies may be structurally unable to transition to AI-native architectures — the AI shift demands wholesale reinvention of EPD, GTM, and business models analogous to the SaaS-vs-on-prem transition, which most incumbents historically failed to navigate
- Consumer UX for AI is fundamentally unsolved — blank-prompt interfaces require users to know what to ask, creating an adoption barrier that prevents general-population engagement with AI capabilities

## Bottlenecks

- No principled method for constructing verifiable reward/value functions for open-ended knowledge work — blocks extension of inference-time compute scaling beyond coding, math, and science into writing, strategy, planning, and other unstructured task domains
- Inference cloud infrastructure for dynamic per-query compute scaling does not yet exist at production scale — the transition from pre-training batch compute to dynamic inference clouds required to deploy o1-class reasoning broadly is a major unsolved infrastructure problem
- Domain-specific real-world data scarcity combined with the engineering complexity of custom cognitive architectures prevents rapid AI deployment into new industry verticals — each new domain requires bespoke data pipelines and workflow engineering that cannot be short-circuited

## Breakthroughs

- OpenAI o1 establishes inference-time compute as a new, independent scaling law for AI reasoning — the first public demonstration that reasoning quality improves continuously and predictably with compute allocated at inference, orthogonal to pre-training scale
- Backtracking, human-analogous reasoning strategies, and genuinely novel problem-solving approaches emerge in o1 as spontaneous properties of scaling RL over chain-of-thought — without direct supervision for these specific behaviors

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/multi-agent-system|Multi-Agent System]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/system-1-thinking|System 1 thinking]]
- [[entities/value-function|value function]]
