---
type: source
title: The Bitter Lesson
source_id: 01KJSYMQZHTDFENE6S1N3E8Y7W
source_type: article
authors: []
published_at: None
theme_ids:
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# The Bitter Lesson

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# The Bitter Lesson
article
http://www.incompleteideas.net/IncIdeas/BitterLesson.html

---

## Briefing

**Rich Sutton argues that every major AI breakthrough — chess, Go, speech, vision — has followed the same pattern: human-knowledge-based approaches lose to general-purpose computation via search and learning, and the field has repeatedly failed to internalize this lesson.** The core claim is that search and learning are the only two techniques that scale arbitrarily with computation, making them the dominant long-run strategy, while encoding human domain knowledge is a short-term crutch that plateaus and ultimately inhibits progress. The implication for current AI research is as pointed as ever: stop building in what we know, and instead build the meta-methods that can discover it.

### Key Takeaways
1. **Search-first beat knowledge-first in chess (1997)** — Deep Blue's victory over Kasparov was won by massive tree search, not by encoding chess strategy, but human-knowledge researchers dismissed it as a non-general fluke.
2. **The same pattern recurred in Go, 20 years later** — All efforts to leverage human knowledge of Go's special structure proved irrelevant once search was applied effectively at scale, with self-play learning to acquire a value function as a critical addition.
3. **Self-play is computationally equivalent to search** — Learning by self-play, like search, is a mechanism for leveraging massive computation rather than encoding human priors, which is why both scale and both win.
4. **HMMs beat human phonology in the 1970s DARPA competition** — Statistical methods requiring more computation outperformed knowledge-engineered speech systems, catalyzing a decades-long shift toward statistics across all of NLP.
5. **Deep learning completes the trajectory in vision and speech** — By relying on convolution and learned invariances rather than edges, SIFT, or phonemes, deep learning moved even further from human knowledge and achieved dramatically better results.
6. **Human knowledge helps short-term, inhibits long-term** — The bitter lesson's core empirical pattern: knowledge-based methods provide quick early wins that are personally satisfying to researchers, but plateau and block the path to breakthrough.
7. **Search and learning are the only arbitrarily-scalable techniques** — These two classes of methods continue improving as computation grows without bound; no knowledge-encoding approach shares this property.
8. **Mind contents are irredeemably complex — stop trying to simplify them** — Space, objects, symmetries, multi-agent structure: all are part of the arbitrary external world and should not be hard-coded because their complexity is endless.
9. **Build meta-methods that discover, not systems that contain discoveries** — The correct architectural principle is to embed only the discovery process, not its outputs; encoding what we know makes it harder to learn how knowing works.
10. **The field keeps repeating the mistake** — As of the essay's writing, AI researchers continue to build in human structure, making the bitter lesson an ongoing failure of collective learning, not merely a historical one.

---

### The Recurring Historical Pattern Across Domains

- In computer chess, the dominant research program before 1997 focused on encoding human understanding of chess structure into evaluation functions and heuristics.
  - When Deep Blue won using massive, deep tree search with custom hardware, the human-knowledge community rejected the result as unrepresentative — "brute force" search was not general and not how humans played.
  - **This reaction is the archetype of the bitter lesson: dismissing an empirical defeat on the grounds that the winning method doesn't match researcher intuitions about intelligence.**

- Computer Go repeated the pattern with a roughly 20-year lag.
  - Enormous effort went into leveraging Go's special features (territory, influence, shape libraries) to avoid expensive search — exactly the strategy that had failed in chess.
  - **All of it proved irrelevant, or worse, once search was applied at scale** — the qualifier "or worse" implies that human-knowledge scaffolding can actively block scale-up.
  - The critical addition in Go was self-play learning to acquire a value function, enabling the system to evaluate positions without exhaustive rollouts.

- Speech recognition: the 1970s DARPA competition is the canonical NLP case.
  - Human-knowledge entrants modeled words, phonemes, and the physical structure of the vocal tract.
  - Hidden Markov Models — more statistical, more compute-hungry — won decisively.
  - The impact cascaded: the entire field of NLP shifted toward statistics and computation over subsequent decades.
  - **Deep learning is the most recent and most extreme step in this direction**: less human knowledge, more computation, larger training sets — and dramatically better outcomes.

- Computer vision followed an identical arc.
  - Early paradigms: edge detection, generalized cylinders, SIFT features — all representations derived from human theories of perception.
  - Today these are entirely discarded. Convolutional neural networks use only convolution and learned invariances, both of which are minimal structural assumptions, and perform vastly better.
  - **The progression is monotonic**: each generation moves further from human representation and closer to learned computation.

---

### Why Researchers Keep Making the Same Mistake

- **Short-term utility creates a trap.** Building human knowledge into a system produces immediate performance gains, which rewards the researcher and confirms their approach. This makes it genuinely rational to pursue in the short run even though it is disastrous in the long run.
- **Personal satisfaction reinforces the mistake.** Researchers who encode domain knowledge are expressing their understanding of the world — the work is intellectually engaging and feels meaningful. There is no comparable emoti

## Key Claims

1. The methods that defeated world chess champion Kasparov in 1997 were based on massive, deep search, not human-knowledge-based approaches.
2. Human-knowledge-based chess researchers dismissed search-based victories as non-general and non-human, despite empirical evidence to the contrary.
3. Computer Go showed the same pattern as chess — human-knowledge approaches eventually proved irrelevant once search and learning were applied at scale — but the transition was delayed by approximately 
4. Learning by self-play to learn a value function was an important component of the breakthrough in computer Go.
5. Search and learning are the two most important classes of techniques for utilizing massive amounts of computation in AI research.
6. Self-play learning, like search, enables massive computation to be brought to bear on a problem.
7. In the DARPA-sponsored speech recognition competition in the 1970s, statistical methods based on hidden Markov models outperformed methods that incorporated human knowledge of words, phonemes, and the
8. The victory of statistical methods over human-knowledge methods in speech recognition led to a major change in all of natural language processing, gradually shifting the field toward statistics and co
9. Deep learning methods rely even less on human knowledge than prior statistical methods, using more computation and huge training sets to produce dramatically better speech recognition systems.
10. Incorporating human knowledge into AI systems was ultimately counterproductive and a waste of research time once massive computation became available through Moore's Law.

## Capabilities

- Massive search-based approaches, without human chess knowledge encoding, can defeat world champion chess players
- Self-play learning combined with large-scale search achieves superhuman performance in complex games like Go without encoding human game knowledge
- Statistical and deep learning methods trained on large datasets produce dramatically better speech recognition than approaches encoding human phonological and linguistic knowledge
- Deep learning neural networks using convolution and learned invariances outperform all feature-engineered computer vision approaches (edges, SIFT features, generalized cylinders)
- Search and learning are general-purpose methods that scale arbitrarily with increased computation across all AI domains — no ceiling has been identified

## Limitations

- Human-knowledge-based AI approaches consistently plateau and ultimately inhibit further progress as computation scales — they help short-term but block long-term gains
- The AI field as a whole is still systematically repeating the mistake of building human knowledge into systems, despite consistent historical failure of this approach across domains
- The contents of minds are irreducibly complex — simple abstractions for space, objects, agents, and symmetries cannot capture the full complexity needed for general AI
- Neurosymbolic and human-knowledge-hybrid approaches provide short-term gains but create architectural debt — becoming irrelevant or actively harmful once search and learning are applied at scale
- AI systems that encode human discoveries cannot participate in the discovery process itself — they are locked into the boundary of what humans already know
- Human-knowledge approaches to speech recognition based on linguistic, phonetic, and vocal tract structure were entirely superseded by statistical computation — demonstrating catastrophic misallocation of research effort when the paradigm is wrong
- Short-term success of knowledge-engineering approaches creates institutional momentum and researcher attachment that delays adoption of superior computation-scaling approaches by decades

## Bottlenecks

- Persistent researcher bias toward encoding human knowledge in AI systems — rather than developing general meta-methods — misdirects field-wide effort and slows adoption of computation-scaling approaches by decades per domain
- Absence of general meta-methods that can discover and represent arbitrary world complexity without relying on human-specified structure or priors — the actual goal of AGI research as described

## Breakthroughs

- Search-based AI without human chess knowledge defeated world champion Kasparov in 1997, definitively demonstrating that computation scaling beats knowledge encoding even in domains thought to require deep human expertise
- Self-play learning combined with large-scale search achieved superhuman Go after decades of human-knowledge-based approaches failed — confirming the chess result was a universal principle, not a one-off
- Deep learning trained on massive datasets achieved dramatically superior speech recognition and then NLP broadly, displacing decades of linguistically-informed knowledge engineering across an entire research field

## Themes

- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/the-bitter-lesson|The Bitter Lesson]]
- [[entities/value-function|value function]]
