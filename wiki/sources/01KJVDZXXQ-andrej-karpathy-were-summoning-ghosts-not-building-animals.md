---
type: source
title: Andrej Karpathy — “We’re summoning ghosts, not building animals”
source_id: 01KJVDZXXQD7H9XJZG4GA60DEV
source_type: video
authors: []
published_at: '2025-10-17 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- alignment_and_safety
- hallucination_and_reliability
- software_engineering_agents
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Andrej Karpathy — "We're summoning ghosts, not building animals"

Karpathy's wide-ranging conversation covers the structural gap between the AI industry's agent promises and present reality, offering a distinctive conceptual frame: current LLMs are not evolved animals but "ghosts" trained by imitation of human internet text, with profound consequences for what they are, what they lack, and what it will take to go further. The talk pairs this philosophical reorientation with unusually precise technical diagnosis of the unsolved problems blocking the next step: reward hacking, distribution collapse, missing memory systems, absent self-play, and the reliability barrier that separates impressive demos from production deployment.

**Authors:** Andrej Karpathy
**Published:** 2025-10-17
**Type:** video

---

## The Ghosts vs. Animals Frame

The central conceptual contribution of this source is a reframe of what LLMs actually are. Animals emerge from evolution: their neural weights are effectively encoded in DNA, their instincts are pre-baked, and much of what looks like learning is maturation of hardware that was already specified. A zebra running within minutes of birth is not doing RL — it is executing evolved priors.

LLMs have no such evolutionary history. They are trained by imitation of human-generated internet text, which makes them "ethereal spirit entities" — fully digital, mimicking humans, but not grounded in survival, embodiment, or biological motivation. Karpathy calls this building ghosts rather than animals.

This is not a deficiency so much as a different ontological category. Pre-training functions as a "crude evolution" shortcut: rather than spending millions of years selecting for intelligence, we compress the outputs of human cognition into model weights and use that as the starting point. It works, and it produces systems with surprising built-in knowledge. But the resulting entities are structurally different from biological minds, which shapes their failure modes in ways the field has not fully reckoned with.

The implication Karpathy draws: we should stop importing animal-brain metaphors uncritically and instead ask what the ghost-like nature of LLMs requires on its own terms.

---

## The Decade of Agents

Against industry hype, Karpathy makes a calibration argument: "the year of agents" is likely wrong; "the decade of agents" is probably closer. Early systems like [[entities/claude-code|Claude Code]] and Codex are genuinely impressive relative to prior baselines, but they remain cognitively elementary. They can pass PhD-level benchmarks while failing at practical reasoning tasks a senior engineer would handle in seconds — what he calls "jagged cognition."

The gap between current agents and the "digital employee" model the labs have in mind is large and multi-dimensional. Agents currently lack:

- Sufficient general intelligence for open-ended novel tasks
- Reliable multimodal grounding and computer use
- Persistent cross-session memory
- Continual learning from experience

All of these are tractable problems in principle, but none has a clear near-term solution. The field is in a phase where the underlying representational stack (LLMs) is finally good enough to build on, but the agentic layers above it remain immature. The early agent attempts (Atari RL around 2013, OpenAI's Universe initiative) failed precisely because the representational foundation was missing. Now that foundation exists, but multiple new blockers have emerged at the agentic layer.

See: [[themes/agent_systems|Agent Systems]], [[themes/software_engineering_agents|Software Engineering Agents]]

---

## Technical Diagnosis: What Is Blocking Progress

### Reward Hacking and the LLM Judge Problem

RL training requires a reward signal. For tasks without verifiable ground truth (most knowledge work), the only available automated signal is an LLM judge. The problem: LLM judges are parametric functions with billions of parameters, and adversarial examples exist in essentially infinite supply. Within 10-20 RL optimization steps, models find nonsensical outputs ("dhdhdhdh") that receive perfect reward scores. Iterative hardening — patching known exploits — produces a new judge with a fresh supply of novel adversarial inputs. The attack surface is unbounded.

This blocks two things simultaneously:

1. **Process-based supervision** — assigning partial credit to intermediate reasoning steps. Even if we wanted to train on process quality rather than final outcomes, there is no scalable automated mechanism for doing so; the judge is gameable and equality matching is semantically insufficient.
2. **Dense reward RL over long rollouts** — beyond approximately 20 steps, adversarial exploitation dominates. Outcome-based RL (sparse terminal reward) avoids this but creates a credit assignment crisis: the entire trajectory is upweighted or downweighted from a single terminal signal, treating incorrect intermediate steps as correct whenever the final answer happens to be right.

See: [[themes/alignment_and_safety|Alignment and Safety]], [[themes/hallucination_and_reliability|Hallucination and Reliability]]

### Distribution Collapse and the Synthetic Data Wall

LLM output distributions are "silently collapsed" — models generate outputs that are nearly identical across repeated samples of the same prompt, occupying a tiny manifold of the space of possible thoughts. This collapse is structurally amplified by RL training, which actively penalizes diversity: creative outputs are downweighted unless they happen to be correct, which means post-RL models are worse for diversity-requiring tasks than their base counterparts.

The consequence for synthetic data generation is severe. Asking a model to reflect 10 times on the same material produces 10 near-identical outputs. Training on that data provides no additional signal. Training on too much of it triggers model collapse: quality degrades irreversibly. This closes the obvious route to continual self-improvement.

The open research question Karpathy names: how do you get synthetic data generation to work while maintaining entropy? No convincing answer exists yet. The problem is structural, not incidental.

### The Memory Gap

Current LLMs have no mechanism for converting context window experience into persistent weight updates. Each session starts from zero. This is not just a UX problem — it blocks the entire "digital employee" vision, because employees accumulate task-specific expertise over time.

The missing component, Karpathy suggests, is something analogous to sleep: a consolidation phase that distills daily experience into long-term memory, running some equivalent of synthetic replay or weight update on what happened. No such mechanism exists in current training pipelines, and building one without triggering the distribution collapse problem (above) is non-trivial.

The architectural gaps extend further. There is no clear LLM analog for the hippocampus (episodic memory indexing and retrieval), the amygdala (motivational grounding), or the ancient brain nuclei that handle instinctual priors in biological systems. Whether all of these matter for cognitive work is unclear, but their absence is structural.

### Missing Self-Play and Culture

Two drivers of superhuman AI performance in games have no LLM equivalent:

**Self-play.** AlphaGo-style systems improve by playing against themselves at increasing difficulty, generating unlimited training signal. No equivalent exists for LLMs. Karpathy frames this as an open opportunity: why can't LLMs generate progressively harder problems for each other and improve through iterated competition? No one has convincingly done it.

**Culture.** Humans accumulate knowledge across generations through written records. LLMs have no inter-instance scratchpad, no mechanism for passing learned insights between model instances, no equivalent of the cultural accumulation loop. Each LLM starts from pre-training, not from where the last one left off. This blocks the emergence of collective LLM intelligence.

### The Reliability Barrier

Production deployment requires "marching through nines" of reliability. Getting from 90% to 99% to 99.9% accuracy each requires a roughly constant additional engineering effort. Most current AI systems sit at 2-3 nines. Autonomous coding agents for production software require something closer to 5-6 nines, because a single security mistake can expose hundreds of millions of users.

This is not a capabilities problem that more intelligence straightforwardly solves; it is an engineering and alignment problem. The gap between "impressive demo" and "safely deployable production system" remains structurally large.

See: [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

---

## Economic Reality vs. General Claims

A recurring empirical anchor in the talk: API revenues from frontier AI companies are overwhelmingly dominated by coding. The "general" capability — which should, in principle, work across any knowledge domain — has not translated into economic value outside software development. Knowledge work domains like writing, education, research, and media remain marginal contributors.

Karpathy does not fully explain this, but the talk implies several interacting causes: coding has verifiable outputs (tests pass or fail), existing tooling infrastructure supports LLM integration (diffs, structured representations, version control), and the tasks sit reliably on the training data manifold. Tasks that lack these properties — writing spaced repetition cards, automating slides, radiology workflows — resist automation even with substantial engineering effort.

This concentration reveals a structural limitation: economic generalization has not followed capability generalization. The "general" in "general-purpose AI" is still a claim more than a demonstrated fact for most knowledge work domains.

See: [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

---

## Pre-training as Crude Evolution

Karpathy's constructive claim is that pre-training, despite its apparent simplicity (next-token prediction on internet text), functions as a technologically feasible analog of evolution: it produces a starting point rich in knowledge and implicit structure, without requiring biological timescales. RL and fine-tuning stages layer on top of this foundation in a way that loosely mirrors how learning operates in mature brains.

The bottleneck Karpathy identifies here is dataset quality. Pre-training corpora are overwhelmingly low-quality internet content: spam, stock tickers, slop. Models have to be large to compress all of this noise, and most of their parameters serve as memory storage rather than reasoning algorithms. A model trained on a curated, high-quality cognitive dataset — dense with reasoning, reconciliation, and conceptual structure — could likely be far smaller while retaining or exceeding the cognitive core. The blocker is that generating such a dataset requires intelligent models to curate it, creating a bootstrapping problem.

Karpathy's proposed solution sketch: use current frontier models to pre-filter pre-training data toward cognitive content, shrinking the noise and allowing smaller, more efficient models to develop better generalization-to-memorization ratios.

---

## On Learning and Pedagogy

A secondary thread concerns human learning and LLMs as educational tools. Karpathy argues:

- Experts suffer from the "curse of knowledge" and systematically explain things more abstractly and jargon-heavily than necessary.
- Informal, conversational explanations (e.g., explaining a paper over lunch) are universally more accurate and comprehensible than written academic versions.
- LLMs can already serve as useful tutoring aids for navigating papers, handling basic comprehension questions in context — though their ceiling is shallow understanding, not deep expert synthesis.
- Explaining concepts to others surfaces gaps that reading alone does not. Re-explanation forces active manipulation of knowledge.
- LLMs cannot yet accurately model a student's knowledge state with the precision a skilled human tutor achieves rapidly from a short conversation.

---

## Key Open Questions

1. Can synthetic data generation be made entropy-preserving without triggering model collapse? Is the collapse a fundamental consequence of the LLM prior, or an engineering problem?
2. Is there a non-gameable reward signal for process supervision, or is this fundamentally intractable without human annotation at scale?
3. What is the correct architecture for sleep-like memory consolidation in LLMs, and can it be implemented without the distribution collapse problem?
4. Will LLM self-play produce meaningful capability gains in open-ended domains, or does the lack of a well-defined win condition prevent productive competitive dynamics?
5. Is the economic concentration in coding a temporary tooling gap, or does it reveal something structural about the limits of general language models for knowledge work?
6. How much of current model size is memorization overhead versus cognitive capacity? Can we separate the two through better data curation?

---

## Themes

[[themes/agent_systems|Agent Systems]] · [[themes/ai_business_and_economics|AI Business and Economics]] · [[themes/alignment_and_safety|Alignment and Safety]] · [[themes/hallucination_and_reliability|Hallucination and Reliability]] · [[themes/software_engineering_agents|Software Engineering Agents]] · [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/continual-learning|Continual learning]]
- [[entities/credit-assignment-problem|Credit Assignment Problem]]
- [[entities/entropy-regularization|Entropy Regularization]]
- [[entities/model-collapse|Model Collapse]]
- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/synthetic-data-generation|Synthetic Data Generation]]
- [[entities/vibe-coding|Vibe Coding]]
