---
type: source
title: No Priors Ep. 116 | With Sarah and Elad
source_id: 01KJVS9B1Y2BJXB5XD37Y2HSQT
source_type: video
authors: []
published_at: '2025-05-29 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- frontier_lab_competition
- model_commoditization_and_open_source
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# No Priors Ep. 116 | With Sarah and Elad

This episode offers a practitioner-level read on the current state of AI market structure, surfacing which verticals are consolidating and which remain open, while grounding that commercial view in a frank technical analysis of why autonomous agents remain brittle — tracing the root causes to unsolved problems in reward design, world modeling, and training diversity.

**Authors:** Sarah Guo, Elad Gil
**Published:** 2025-05-29
**Type:** video

---

## AI Market Consolidation

The AI application layer is entering a new phase: after two to three years of intense uncertainty and rapid iteration, a subset of verticals is now showing clear signs of convergence around dominant players.

**Verticals showing consolidation:**
- **Medical scribing / healthcare workflows** — winners such as Abridge and Open Evidence are visible. The product approach has been validated.
- **AI coding** — consolidating into two to three players: Cursor, Windsurf/Codeium, Cognition, and Microsoft Copilot. The category is further complicated by an unresolved architectural debate (see #Coding Architecture: Sync vs. Async below).
- **Customer success** — Sierra and Decagon are emerging as the likely dominant players.

**Verticals still wide open:**
- **Sales productivity tooling** — highly fragmented; no clear winner or even a clear dominant product approach.
- **Finance and accounting** — expected to produce dominant players given heavy document-driven workflows, but consolidation has not yet occurred.
- **Pharma and document-driven industries** — companies like BlueDot are doing interesting work, but the open question is whether the delay reflects a product problem (no one has landed on the right approach) or a model capability problem (models are not yet good enough).

The working hypothesis is that the market dynamics are now better understood: it is a race to identify verticals of relevance, develop a working product, secure proprietary data sources, and build distribution. The open question for late-arriving verticals is whether they are pre-consolidation or fundamentally harder.

---

## Coding Architecture: Sync vs. Async

[[entities/openai|OpenAI]]'s trajectory in the coding market illustrates the unresolved tension between IDE-integrated (synchronous) and cloud-based agent (asynchronous) workflows. OpenAI initially bet on async with [[entities/codex|Codex]], then acquired [[entities/windsurf|Windsurf]], an IDE-first tool. Microsoft open-sourced Copilot under competitive pressure from [[entities/cursor|Cursor]]. This sequence suggests the market has not yet settled on which workflow paradigm will dominate.

---

## Consolidation Strategy: The Case for Startup Mergers

A recurring argument in this episode is that competing startups in the same vertical should consider merging rather than fighting each other — the real competitive threat is the three to four large incumbents, not fellow startups.

Historical precedents cited:
- **Against merging too late:** Uber and Lyft's prolonged competition was arguably damaging to both.
- **For merging:** PayPal's merger with X.com allowed focused competition against incumbent financial infrastructure.

Common objections to merging and their rebuttals:

| Objection | Rebuttal |
|---|---|
| Ego / leadership concerns | Leadership structure matters less than the larger victory |
| Integration complexity | Cultural mismatches don't require full integration; exit packages can facilitate transitions |
| Relative valuation difficulty | Simple objective metrics (users, revenue) can determine ownership ratios without overthinking |

The thesis: merging enlarges the total pie, reduces pricing pressure from head-to-head competition, and concentrates firepower against incumbents. Note that this logic does not apply universally — large markets like payments can sustain multiple durable players.

M&A as a consolidation vector is already underway: OpenAI's acquisition of Windsurf/Codeium is identified as the first major step in this trend.

---

## Technical Bottlenecks in Agent Development

The episode contains a substantive technical discussion of why autonomous agents remain limited, structured around three interlocking problems.

### Behavior Cloning Is Brittle

Labs have invested heavily in collecting traces of humans performing sophisticated tasks, training agents via behavior cloning. The fundamental limitation: **this approach is brittle the moment the agent encounters a state not represented in the training distribution.** When a user or environment introduces an unexpected action, the agent fails rather than adapting. This is a structural limitation of the approach, not a data volume problem.

> *"It tends to be really brittle when you go off the path with the cloning techniques — model all monkey presses some button that like all the humans never pressed."*

### Reward Function Design for Real-World Tasks

Reinforcement learning sidesteps the brittleness of behavior cloning by training agents against a reward signal rather than demonstrations. But for real-world tasks, **designing an appropriate reward function is significantly harder than for well-defined games like chess or Go**, where outcomes are unambiguous. The gap between what a reward function incentivizes and what actually constitutes task success in the real world is a blocking limitation.

> *"It's very hard to design rewards and then you have a gap from reality."*

### World Model Environments: The Richness-Efficiency Trade-off

A research direction gaining traction is training agents inside learned world models — simulated environments that can be run cheaply and at scale. The core unsolved tension:

- The environment must be **rich enough** to teach genuinely useful problem-solving behavior.
- The environment must be **computationally cheap enough** to run at the scale needed for RL to work.
- Without sufficient **diversity** in the training environment, agents memorize a fixed path through their training distribution rather than developing generalizable strategies.

> *"You need diversity or you're just memorizing a path through your game, even if that game is like the game of doing research work."*

These three problems are deeply interrelated. Progress on world models could reduce dependence on behavior cloning; progress on reward design could make RL viable beyond narrow domains; diversity at training time is required for either approach to generalize.

---

## Landscape Signals

### Capabilities

- **Foundation LLMs as knowledge substrate** — Scaling model size and training data has produced a powerful foundation of knowledge and pattern recognition that serves as the basis for downstream specialization. (maturity: broad production)
- **Narrow code agents in production** — IDE-integrated and async/cloud-based code generation tools are in production use for real software engineering workflows. (maturity: narrow production)
- **Capable small and open models** — Open and smaller models are demonstrating meaningful code generation capability, expanding the competitive surface beyond frontier labs. (maturity: demo)

### Limitations

- **Behavior cloning brittleness** — Agents trained via behavior cloning fail completely when encountering out-of-distribution states. This is a blocking limitation for production-grade autonomous agents. (severity: blocking, trajectory: stable)
- **Async code agents not yet at sufficient quality** — Cloud-based software engineering agents do not yet work at the quality required for general deployment. (severity: blocking, trajectory: improving)
- **RL reward design for real-world tasks** — No generalizable approach to reward specification for open-ended real-world tasks. (severity: blocking, trajectory: unclear)
- **RL overfitting / path memorization** — Without training diversity, RL agents memorize solution paths rather than generalizing. (severity: significant, trajectory: unclear)
- **World model tractability** — Creating environments rich enough to teach useful behavior while remaining computationally tractable is an unsolved problem. (severity: significant, trajectory: unclear)

---

## Biotech Sidebar

The episode briefly covers two biotech areas with potentially significant implications:

- **Reproductive technology** — Research in Japan has demonstrated reprogramming of somatic cells into gametes, with successful mouse offspring produced from two male parents. The implication is that reproductive constraints tied to biological sex or age could be partially overcome.
- **Aging treatments beyond cosmetics** — The $40B market built around Botox highlights enormous demand for youth-related treatments, raising the question of why equivalent investment has not flowed into treatments for biological aging (skin aging, hair loss, vision, hearing, tooth regrowth). The hypothesis is that basic science gaps remain, but the market opportunity is large.

---

## Related Themes

- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/frontier_lab_competition|Frontier Lab Competition]]
- [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/behavior-cloning|Behavior Cloning]]
- [[entities/cognition|Cognition]]
- [[entities/cursor|Cursor]]
- [[entities/decagon|Decagon]]
- [[entities/harvey|Harvey]]
- [[entities/perplexity|Perplexity]]
- [[entities/reinforcement-learning|Reinforcement Learning]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/sierra|Sierra]]
- [[entities/windsurf|Windsurf]]
- [[entities/world-model|World Model]]
- [[entities/world-models|World Models]]
- [[entities/reinforcement-learning-rl|reinforcement learning (RL)]]
