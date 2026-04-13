---
type: source
title: State of Startups and AI 2025 - Sarah Guo, Conviction
source_id: 01KJVSCDADQB46AAJ2EKGY7QJE
source_type: video
authors: []
published_at: '2025-08-02 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- software_engineering_agents
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# State of Startups and AI 2025 - Sarah Guo, Conviction

> A practitioner's-eye view of the AI application layer as of mid-2025, documenting which bets are paying off (coding agents, voice, vertical software), which structural forces are reshaping the model market (commoditization, multi-model competition), and what the "Cursor for X" thesis means for builders entering every domain. Grounded in ARR figures, acquisition prices, and grant application data from Conviction's portfolio, it is one of the more data-dense public assessments of where startup value is actually accreting.

**Authors:** Sarah Guo (Conviction)
**Published:** 2025-08-02
**Type:** video

---

## What's Working in the Market

### Reasoning as a New Scaling Vector

[[themes/agent_systems|Agent Systems]] entered a new phase with the emergence of test-time compute (reasoning) as a distinct scaling axis. Rather than relying solely on larger pre-training runs, labs now invest compute at inference time, enabling models to plan, backtrack, and search systematically — capabilities that were previously inaccessible regardless of model size.

This unlocks a specific class of use cases: transparent high-stakes decisions (where showing the chain of reasoning matters), sequential problem-solving, and systematic search over large hypothesis spaces. The tradeoff is real — reasoning costs more and introduces latency — but the capability unlock is qualitatively different from simply scaling parameters.

> "Reasoning is a new vector for scaling intelligence with more compute."

**Limitation:** Models require test-time compute investment for reasoning, creating a cost/latency tradeoff that currently blocks scalable deployment in real-time or cost-sensitive domains. Resolution horizon: 1–2 years.

### The Model Market Is Commoditizing

[[themes/ai_business_and_economics|AI Business and Economics]] saw a structural shift that Guo frames as permanently altering how application builders should think about foundation models:

- GPT-4 pricing dropped from **$30 per million tokens to $2 in ~18 months**
- Distilled versions now sit at **~10 cents per million tokens**
- Claude and [[entities/gemini|Gemini]] took significant market share from OpenAI on OpenRouter
- [[entities/deepseek|DeepSeek]] released base and reasoning models at a claimed fraction of typical training cost
- New credible entrants: SSI, Thinking Machines

Sam Altman's own framing: *"Last year's model is a commodity."* Guo's prescription for builders: plan for a multi-model world and expect the market to compete for your business. The model layer is not where durable startup value accumulates.

---

## The Application Layer: "Cursor for X"

### Why Code Was First

The [[themes/software_engineering_agents|Software Engineering Agents]] space produced the first breakout applications, and the reasons are structural:

1. **Code is logical, structured language** — closer to formal systems than natural language, reducing ambiguity
2. **Deterministic validation** — code can be compiled, tested, and executed; correctness is objectively verifiable
3. **Research priority** — labs treated code as a key AGI benchmark, making it a training and data collection focus

The result: a historically rapid S-curve. [[entities/cursor|Cursor]] grew from $1M to $100M ARR in 12 months with half a million developers and zero salespeople. [[entities/cognition|Cognition]] became the top committer in many companies' codebases. [[entities/windsurf|Windsurf]] was acquired by OpenAI for $3 billion. Lovable and Bolt each hit $30M ARR in weeks serving non-engineers.

**The deeper lesson** is not that code is special — it's that engineers built tools for engineers with deep workflow understanding. The same recipe is portable.

### The Recipe for Vertical AI

For builders entering other domains, Guo distills a three-part framework:

1. **Domain knowledge as bootstrap** — don't make users explain their context. Build products that arrive informed. Workflow-specific knowledge, not just AI capability, is the differentiator.

2. **Orchestration over prompting** — automatically collect and package context (including non-language data), route to the right models at the right time, deliver outputs in usable form. The generic text box is the wrong interface. *"The prompt is a bug, not a feature."*

3. **Seamless, familiar UX** — the goal is mind-reading, not assistant-querying. Workflow integration matters more than raw model capability.

> "These applications are a nice, thick wrapper around the underlying models. The value isn't just in the model itself but in the company that provides the entire workflow, context, and user experience."

**Limitation:** Domain knowledge and workflow context are not learnable from internet-scale data. Each vertical requires custom curation and context engineering — this bottleneck has no clear resolution horizon.

### Where the Opportunities Are

| Category | Logic | Examples |
|---|---|---|
| Text-heavy professional domains | High leverage for language models | Law ([[entities/harvey|Harvey]]: >$70M ARR) |
| Machine-interrogates-human | AI enables infinite patient conversations at scale | Customer root-cause, medical intake |
| Answer-not-in-common-crawl | Reasoning on novel domains with physical interaction | Robotics, biology, materials, physics |

The pattern in conservative, low-tech industries is notable: they adopt AI fastest because they know their customers and are solving real problems with measurable outcomes.

---

## Multimodality: Voice First, Then Video

[[themes/vertical_ai_and_saas_disruption|Vertical AI]] is being pulled by multimodal capability maturation:

- **Voice** is the first business modality because it maps to existing workflows — medical consults, lead generation, customer service. Companies like [[entities/elevenlabs|ElevenLabs]] surpassed $50M ARR scaling interactions that were previously human-rate-limited.
- **Video** ([[entities/heygen|HeyGen]], [[entities/midjourney|Midjourney]]) crossed into production with emotional expression, gesture control, and synthetic clones. $50M+ ARR.
- **Enterprise data gap:** Most enterprises lack structured voice, video, and image data today. As multimodal AI makes this data actionable, the incentive to capture it increases — a self-reinforcing dynamic that hasn't yet closed the loop.

**Limitation:** Enterprise lack of structured multimodal data currently limits deployment of multimodal AI applications beyond narrow verticals. Trajectory: improving (1–2 year horizon).

---

## Co-pilots vs. Agents: What's Actually Driving Revenue

A recurring theme in [[themes/agent_systems|Agent Systems]] is the gap between aspiration and revenue reality:

- **Co-pilots are underrated** — augmenting human decision-making (the Iron Man suit model) is where most current ARR lives
- **Agents are the direction** — but full automation remains unreliable, particularly as task latency increases
- **Human tolerance for failure collapses with latency** — a hallucination in a quick query is tolerable; one in a 30-minute agentic task is a support ticket and churn risk

> "Human tolerance for failure or hallucinations or lack of reliability, it just reduces dramatically as latency increases."

This creates a practical tension: the endgame (full autonomy) is what excites investors, but co-pilots are what generate defensible revenue today. The agent startups seeing real-world success are operating in this middle band — planning, hypothesis testing, backtracking — but with human checkpoints.

**Bottleneck:** Hallucination and reliability failures block full autonomy in customer-facing and high-stakes workflows. Resolution horizon: 1–2 years.

---

## Defensibility and the Hard Problems

Guo's framing of defensibility in [[themes/startup_and_investment|Startup and Investment]] resists the "moats are dead" narrative:

- **Workflow lock-in** is real when the product is deeply embedded in how a team operates
- **Data flywheels** matter in domains where usage generates proprietary training signal
- **Domain expertise** is the thing models can't replicate from internet data

The hardest problems — and potentially the highest-value ones — sit in domains where **the answers aren't in Common Crawl**: robotics, biology, materials science, physics. Here, AI must interact with atoms, not bits. The same reasoning capabilities that solve IMO mathematics appear transferable to molecular space and biological systems, but the data collection challenge is fundamentally different.

**Bottleneck:** AI capabilities in hard science and simulation domains require interaction with the physical world; no solution path analogous to LLM scaling exists. Resolution horizon: 3–5 years.

---

## Key Claims

| # | Claim | Evidence |
|---|---|---|
| 1 | Reasoning is a new vector for scaling intelligence with more compute | "reasoning is a new vector for scaling intelligence with more compute. The labs are really excited ab" |
| 2 | Agent startup applications to Embed grew 50% year-over-year | "the number of agent startups has gone up 50% over the last year and a lot of them are working like w" |
| 3 | HeyGen, ElevenLabs, Midjourney surpassed $50M ARR | "companies like Hey Genen and 11 and Midjourney that are rocketing past 50 million of AR" |
| 4 | GPT-4 dropped from $30 to $2 per million tokens in ~18 months | "GPT4 went from $30 per million tokens to $2 in about 18 months" |
| 5 | Distilled GPT-4 variants now ~10 cents per million tokens | "The distilled versions of that are like now 10 cents" |
| 6 | Claude and Gemini took significant OpenRouter market share from OpenAI | "you really saw Claude cut into OpenAI's market share and Google come roaring back with Gemini" |
| 7 | Cursor: $1M → $100M ARR in 12 months, 500K devs, zero salespeople | "a million to 100 million of AR in 12 months and half a million developers...zero salespeople" |
| 8 | Cognition is the top committer in many companies' codebases | "cognition which started with more autonomy is already the top committer in many companies" |
| 9 | Windsurf acquired by OpenAI for $3 billion | "Windsurf...being acquired by OpenAI for $3 billion" |
| 10 | Lovable and Bolt each hit $30M ARR in weeks | "lovable and bolt hit 30 million of AR each in a handful of weeks" |
| 11 | Harvey reached >$70M ARR; AI is now essential to legal competitiveness | "Harvey is you know two years in well over 70 million of ARR. It's AI is essential now to being competitive" |
| 12 | Sam Altman: "Last year's model is a commodity" | "Sam Alman himself, I think, said it best. Last year's model is a commodity" |

---

## Open Questions and Limitations

- **Data wall debate:** Widespread concern about training data scarcity; Guo is skeptical but acknowledges the debate is live and unresolved
- **Agent reliability threshold:** At what reliability level does human tolerance for agentic failures become commercially acceptable? No clear answer
- **Multimodal enterprise data gap:** Will enterprises invest in capturing voice/video/image data because AI makes it actionable, or does the value have to be demonstrated first? Chicken-and-egg dynamic
- **Vertical defensibility:** Domain-specific context is the moat, but context engineering per vertical is expensive — how does this scale across industries?
- **Hard science timeline:** The transfer of reasoning capabilities from math benchmarks to biological/physical domains is promising but empirically thin as of this source

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/software_engineering_agents|Software Engineering Agents]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/ai-agent|AI Agent]]
- [[entities/cognition|Cognition]]
- [[entities/cursor|Cursor]]
- [[entities/deepseek|DeepSeek]]
- [[entities/distillation|Distillation]]
- [[entities/elevenlabs|ElevenLabs]]
- [[entities/gemini|Gemini]]
- [[entities/harvey|Harvey]]
- [[entities/heygen|HeyGen]]
- [[entities/jasper|Jasper]]
- [[entities/midjourney|Midjourney]]
- [[entities/mistral|Mistral]]
- [[entities/sierra|Sierra]]
- [[entities/windsurf|Windsurf]]
