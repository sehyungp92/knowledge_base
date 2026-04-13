---
type: source
title: Why I don’t think AGI is right around the corner
source_id: 01KJST86K2TE39NHYAC3QQDHAD
source_type: article
authors: []
published_at: '2025-06-02 00:00:00'
theme_ids:
- agent_systems
- computer_use_and_gui_agents
- continual_learning
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why I don’t think AGI is right around the corner

**Authors:** 
**Published:** 2025-06-02 00:00:00
**Type:** article

## Analysis

# Why I don't think AGI is right around the corner
2025-06-02 · article
https://www.dwarkesh.com/p/timelines-june-2025

---

## Briefing

**The core argument is that continual learning — not raw intelligence — is the binding constraint on AI's economic transformation, and its absence means current LLMs cannot function as real employees regardless of benchmark performance. Even if progress stalls today, fewer than 25% of white-collar jobs would be automated; but when online learning is solved, the result could be a "broadly deployed intelligence explosion" as AI copies amalgamate learning across every job in the world simultaneously.**

### Key Takeaways
1. **Continual learning is the hidden bottleneck** — LLMs cannot build up context over time the way human employees do, making them permanently 5/10 at even simple, language-in/language-out tasks despite high baseline intelligence.
2. **The saxophone analogy exposes why prompting can't substitute for learning** — Teaching via refined instructions to a fresh student each time is fundamentally different from iterative feedback on the same learner; no prompt optimization can replicate human on-the-job improvement.
3. **AI progress stalling today ≠ massive automation** — The author estimates <25% of white-collar employment would be displaced without further progress, contradicting guests Sholto Douglas and Trenton Bricken's claim that data collection alone would automate most white-collar work within five years.
4. **In-session learning is real but ephemeral** — LLMs demonstrably improve their outputs within a long session through feedback, but this understanding of preferences is entirely lost at session end, and compacted context summaries are too brittle to preserve tacit, non-textual learning.
5. **Computer use is in the GPT-2 era** — Agents lack a pretraining corpus of multimodal interaction data, face sparse rewards over long horizons, and operate with unfamiliar action primitives; the author's 50/50 date for tax-filing-level computer use is 2028, not 2026.
6. **Algorithmic innovations take much longer than they appear** — The seemingly simple R1/o1 RL procedure took two years of engineering from GPT-4's release to o1, suggesting computer use — a harder problem with sparser data — will take at least as long.
7. **Frontier reasoning models represent genuine, qualitative progress** — o3 and Gemini 2.5 traces exhibit real self-correction and problem decomposition; Claude Code zero-shotting a working application from a vague spec is described as "baby general intelligence" in action.
8. **Solving continual learning would trigger a discontinuity, not a gradual ramp** — Once models can learn on the job, one AI instance could amalgamate experience across every copy doing every job in the world, potentially achieving functional superintelligence without further algorithmic progress.
9. **AGI timelines are lognormal — this decade or effectively bust** — Scaling training compute beyond 2030 hits hard physical limits (chips, power, fraction of GDP); after that, progress depends on algorithmic advances where low-hanging fruit will have been picked.
10. **Early broken versions of continual learning will give advance warning** — Labs are incentivized to ship partial innovations quickly, so the author expects a visible degraded precursor to full online learning before the bottleneck is truly solved.
11. **The 50/50 bet for human-equivalent on-the-job learning is 2032** — Seven years is a long time (GPT-1 was seven years ago), but the author sees no obvious architectural path to slot online learning into current models today.
12. **Misaligned 2028 ASI remains a genuinely plausible tail** — Despite extended median timelines, probability distributions are wide enough that safety work targeting near-term catastrophic outcomes is still well-justified.

---

### The Continual Learning Gap: Why LLMs Can't Function as Employees

- **The fundamental problem is not raw capability but the inability to improve through practice** — human employees become valuable through iterative, self-directed refinement over months and years, not through their baseline intelligence at hire.
  - The author spent over 100 hours building LLM tools for podcast post-production (transcript rewriting, clip identification, co-writing), finding models consistently "5/10" at short-horizon, language-in/language-out tasks that should be squarely in their repertoire.
  - The issue is not that models fail catastrophically; it is that they plateau immediately at their out-of-the-box level, with no mechanism for improvement across sessions.

- **The saxophone teaching analogy crystallizes the architectural mismatch** — human learning requires a single continuous learner receiving feedback on their own attempts; LLM "teaching" sends each new query to a fresh student who has only read written notes about previous failures.
  - No matter how refined the prompt, reading instructions cannot substitute for the embodied, iterative feedback loop that produces genuine skill acquisition.
  - This is why Fortune 500 companies aren't replacing workflows — it is a genuine capability gap, not organizational conservatism.

- **RL fine-tuning is not a substitute for deliberate, adaptive learning** — bespoke RL environments for every subtask in a job are impractical; human editors improve by noticing small things themselves, thinking about audience resonance, and refining workflow organically.
  - A hypothetical where a smart model constructs its own RL loop from high-level feedback sounds promising but is speculated to be extremely hard to generalize across task types.

- **In-session learning demonstrates the capability exists but cannot be preserved** — when the author gives feedback mid-essay ("your shit sucked, here's what I wrote instead"), subsequent paragraphs genuinely improve, showing the model can update on rich contextual feedback.
  - **This capability is entirely lost at session end**, confirming

## Key Claims

1. The primary reason Fortune 500 companies are not using LLMs to transform workflows is not organizational resistance but genuine difficulty in obtaining normal humanlike labor from LLMs.
2. LLMs perform at approximately a 5/10 level on simple, self-contained, short-horizon language-in/language-out tasks such as rewriting transcripts, identifying clip highlights, or co-writing essays.
3. LLMs can develop useful in-session understanding of user preferences and style mid-conversation, but this tacit knowledge is entirely lost at the end of the session.
4. Rolling context window compaction via text summaries will be brittle in non-text-based domains, because rich tacit experience cannot be faithfully distilled into text summaries outside software engine
5. Even Claude Code with rolling context compaction will sometimes reverse hard-earned optimizations if the explanation for why they were made did not survive the compaction summary.
6. If AI progress stalls today without advances in continual learning, fewer than 25% of white-collar jobs will be automated, because AIs cannot build up sufficient working context to function as actual 
7. Solving continual learning will produce a large discontinuity in the economic value of AI models, potentially triggering a broadly deployed intelligence explosion even without further algorithmic prog
8. AI models capable of online learning could amalgamate learnings across all deployed copies simultaneously, functionally becoming a superintelligence rapidly without further algorithmic progress.
9. Early broken versions of continual learning or test-time training will be released before a system that truly learns like a human, providing advance warning before this bottleneck is resolved.
10. Reliable computer use agents capable of handling week-long, multi-step agentic tasks end-to-end (e.g., preparing taxes) do not yet exist as of 2025.

## Capabilities

- Frontier reasoning models (o3, Gemini 2.5) demonstrate genuine multi-step deliberation: breaking down problems, generating internal monologue, and self-correcting when pursuing unproductive directions during inference
- Agentic coding assistants (Claude Code) can zero-shot working applications from vague high-level specifications without step-by-step instructions, in roughly 10 minutes
- LLMs can adaptively improve within a session by learning from corrective feedback on previous outputs, enabling meaningful co-authorship on iterative tasks when corrections are provided in-context
- Rolling context window compaction systems (e.g. Claude Code's /compact) allow agents to maintain working memory across long sessions by summarising accumulated context periodically
- Computer use agents can perform basic GUI navigation (clicking, typing, scrolling in browsers and desktop environments), but operate at a primitive level comparable to the GPT-2 era for language

## Limitations

- LLMs fundamentally cannot improve on a task over time the way a human employee would — there is no mechanism for deliberate, adaptive on-the-job learning; capabilities are fixed at deployment and cannot be shaped by high-level feedback
- All in-session adaptive understanding of user preferences and style is lost at context boundary — models cannot persist tacit experiential knowledge across sessions
- RL fine-tuning is not a practical substitute for organic human-like adaptive learning — it requires bespoke reward environment construction per subtask and cannot replicate the subtle, self-directed improvement humans perform organically
- Even technically capable AI systems cannot displace human employees in practice for personalised iterative tasks — inability to build persistent context defeats the practical value proposition regardless of raw task capability
- Context window summarisation (e.g. /compact) is brittle for preserving tacit optimisations — hard-earned engineering decisions are frequently lost because the reasoning behind them cannot be fully articulated in text summaries
- Rolling context compaction degrades sharply outside of text-heavy domains like software engineering — non-textual skills (performance craft, interpersonal judgment, sensory refinement) cannot be adequately represented as text summaries
- LLMs perform at roughly 5/10 quality on simple, self-contained, language-in/language-out tasks (transcript editing, clip selection, co-writing) — below the threshold for reliable autonomous deployment as skilled worker replacements
- Computer use agents lack a large pretraining corpus of multimodal GUI interaction data — models entering this domain are as data-starved as text LLMs would have been trained on 1980s text corpora
- Long-horizon computer use tasks require multi-hour uninterrupted rollouts before any correctness signal can be observed, making RL training signal extremely sparse and compute cost per training example prohibitive
- No public evidence suggests computer use models have become less data-hungry despite operating in an inherently low-data domain — models appear substantially under-practiced relative to language tasks, with no demonstrated sample efficiency improvements
- Training compute scaling at 4x/year cannot continue beyond ~2030 — chip manufacturing limits, global power grid capacity, and the fraction of GDP that can be allocated to AI training all impose hard physical ceilings
- Algorithmic innovations for complex agentic tasks that appear conceptually simple take 2+ years to reliably productionise — suggesting computer use timelines are systematically underestimated by those who conflate conceptual insight with engineering delivery

## Bottlenecks

- Absence of online continual learning blocks AI from functioning as a genuine employee replacement — models cannot build up company-specific context, preferences, and procedural knowledge over time the way humans do; this single gap gates mass white-collar automation
- Absence of large-scale multimodal computer use pretraining data limits agent capability ceiling and sample efficiency — current agents begin GUI interaction with far less domain exposure than text LLMs had for language tasks, making production reliability unachievable near-term
- Training compute scaling approaches a hard physical ceiling by ~2030 — continued 4x/year scaling of frontier training runs is unsustainable due to chip, power, and GDP-fraction constraints, forcing a transition to algorithmic progress as the primary driver
- Sparse long-horizon reward signals for multi-step computer use tasks make RL training intractable at practical cost — 2-hour rollouts produce a single binary correctness signal, blocking the kind of dense feedback loops that drove rapid improvement in math/coding agents

## Breakthroughs

- Inference-time reasoning (o1/o3, Gemini 2.5 style) constitutes a qualitative shift in how models process problems — they now genuinely decompose tasks, sustain internal deliberation, and self-correct mid-generation rather than producing direct associative responses

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/continual_learning|continual_learning]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/claude-code|Claude Code]]
- [[entities/continual-learning|Continual learning]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/test-time-training|Test-Time Training]]
