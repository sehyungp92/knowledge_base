---
type: source
title: The Second Half
source_id: 01KJSTZKY2KHG1YCR9025Q54QV
source_type: article
authors: []
published_at: None
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Second Half

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# The Second Half
article
https://ysymyth.github.io/The-Second-Half/

---

## Briefing

**AI has crossed a threshold where a general "recipe" — language pre-training as priors, scale, and reasoning-as-action — can hillclimb any benchmark without requiring novel methods, rendering the first-half game of method innovation obsolete. The critical implication is that the bottleneck has shifted from training to evaluation: closing the "utility problem" (AI surpasses humans on benchmarks but hasn't moved GDP) requires inventing evaluation setups that break the recipe's assumptions, not just creating harder benchmarks.**

### Key Takeaways
1. **RL finally generalizes** — a single recipe now handles software engineering, IMO math, creative writing, and computer use; one year ago most researchers would have called this impossible.
2. **The most impactful AI papers were methods, not benchmarks** — Transformer has >160K citations vs. WMT'14's ~1,300; ImageNet has <1/3 the citations of AlexNet.
3. **The missing piece in RL was priors, not algorithms** — decades of algorithm focus (DQN, PPO, TRPO) were the wrong priority; language pre-training turned out to matter more than any RL algorithm.
4. **Reasoning as action is theoretically terrible but practically magical** — infinite action space should make RL impossible, but language priors allow reasoning steps to generalize across all games seen during pre-training.
5. **Language generalizes through reasoning in agents** — the core abstract principle; once priors and environment are correct, the RL algorithm is the most trivial part.
6. **Novel methods are now outpaced by recipe scaling** — a specialized method improves a task by ~5%; the next o-series model improves it by ~30% without targeting it.
7. **The utility problem is the most important problem in AI** — superhuman performance on chess, Go, SAT, IMO has not moved economics or GDP; the root cause is broken evaluation assumptions.
8. **Standard evaluation makes two false assumptions** — (1) tasks are fully autonomous with no human in the loop; (2) tasks are i.i.d. rather than sequential with accumulating familiarity.
9. **The second half game is evaluation design, not method design** — only evaluation setups that create new assumptions which break the recipe will force genuinely novel research.
10. **Academia lacks the courage to question the i.i.d. assumption** — we have long-term memory methods but no benchmarks to justify them, because questioning the foundation of ML is institutionally hard.

---

### The First Half: Why Methods Won Over Benchmarks

- The defining pattern of the first half was: develop novel training methods or models that hillclimb benchmarks, then create harder benchmarks and repeat.
  - Winners of the first half — Transformer, AlexNet, GPT-3, backpropagation — are uniformly training methods or architectures, not benchmark definitions.
  - Citation asymmetry illustrates the hierarchy: Transformer >160K citations vs. WMT'14 ~1,300; AlexNet roughly 3× ImageNet.
- Methods dominated because they were genuinely harder to create than tasks.
  - Designing backpropagation, convolutional nets, or the Transformer required remarkable insight; defining tasks often just meant taking existing human activities and encoding them as benchmarks.
  - Methods were also more general: the Transformer powered progress in CV, NLP, RL, and beyond, far exceeding the impact of any single benchmark it first proved itself on.
- **The game worked for decades** — it sparked world-changing ideas and ever-increasing benchmark performance across domains.
  - The only reason to change it: the cumulation of those breakthroughs eventually created a qualitatively different situation — a working general recipe.

---

### The RL Recipe: Three Components, One Neglected

- RL has three key components: **algorithm**, **environment**, and **priors**.
  - The classical RL research tradition (Sutton & Barto) is almost entirely about algorithms: REINFORCE, DQN, TD-learning, actor-critic, PPO, TRPO.
  - Environments and priors were treated as fixed or minimal — all RL experiments essentially started from scratch.
- In the deep RL era it became clear that environments matter empirically: algorithm performance is often highly specific to the environment it was developed in.
  - OpenAI's response was logical: build gym (standard RL environments), then World of Bits / Universe (turning internet/computer into games).
  - The plan was sound in principle: standardize the environment, then solve it with smart algorithms → digital AGI.
- **The plan failed for a critical reason**: RL agents solving Dota or robotic hands did not transfer to computer use or web navigation; different domains required different specialized systems.
  - The missing component was not a better algorithm but **priors**.

---

### Language Pre-Training as the Missing Prior

- After GPT-2/GPT-3, the missing piece became clear: powerful language pre-training distills general commonsense and language knowledge that can be fine-tuned into agents.
  - WebGPT (web agent) and ChatGPT (chat agent) demonstrate the pattern: pre-training → fine-tuning → world-changing capability.
  - **The most important part of RL might not be the RL algorithm at all, but priors obtainable in a way totally unrelated to RL.**
- Language pre-training creates good priors for chat but weaker priors for computer control or video games because those domains are further from internet text distribution.
  - CALM (2019) — the first LLM-based RL agent — demonstrated the problem: required millions of RL steps to hillclimb a single text game, with zero transfer to new games.
  - This was a known RL property but contrasted sharply with human zero-shot generalization to new games.
- The insight that resolved the transfer problem: **humans generalize because we can choose to reason** rather than only take direct actions.
  - An agent limited to "go to cabinet 2" or "kill dungeon with sword" cannot

## Key Claims

1. A single recipe combining language pre-training, scale, and reasoning-as-action can now tackle software engineering, creative writing, IMO-level math, mouse-and-keyboard manipulation, and long-form qu
2. The most impactful AI papers from the first half are training methods or models, not benchmarks or tasks
3. ImageNet has fewer than one-third the citations of AlexNet, illustrating that methods outrank benchmarks in the first half of AI
4. The WMT'14 workshop report (Transformer's main benchmark) has approximately 1,300 citations while the Transformer paper has over 160,000
5. In the first half of AI, methods were harder and more valuable than task definitions because humans simply converted existing human tasks into benchmarks with little insight
6. Methods were more valuable than benchmarks because their generality allowed hillclimbing across many different domains beyond the single task where they first proved themselves
7. RL has three key components—algorithm, environment, and priors—but historically researchers focused almost exclusively on the algorithm
8. OpenAI's plan to turn the internet/computer into an RL environment (World of Bits, Universe) failed to generalize: RL agents never solved computer use or web navigation and did not transfer across dom
9. The missing piece in RL was not the algorithm or environment but priors: powerful language pre-training that distills general commonsense and language knowledge
10. CALM (2019) was the first agent in the world built via pre-trained language models

## Capabilities

- A single unified recipe (language pre-training + scale + reasoning as RL actions) enables AI to tackle diverse high-difficulty tasks including software engineering, creative writing, IMO-level math, computer use, and long-form question answering without domain-specific algorithmic innovations
- AI systems have reached gold medal level performance on both IMO (International Mathematical Olympiad) and IOI (International Olympiad in Informatics)
- AI systems surpass most humans on SAT and bar exams, and beat world champions at chess and Go
- Language models can be fine-tuned via SFT/RL into web navigation and conversational assistants by leveraging language pre-training priors
- Adding open-ended language reasoning as actions in RL environments enables agents to leverage language pre-training priors to generalize across tasks, while affording flexible test-time compute allocation per decision
- The general recipe (o-series class systems) achieves ~30% improvements on arbitrary benchmarks without task-specific targeting, industrializing benchmark hillclimbing

## Limitations

- AI evaluation setups require fully autonomous single-turn task completion, but real-world tasks require ongoing human engagement throughout — creating a fundamental mismatch between what benchmarks measure and what deployment demands
- AI agents evaluate tasks in i.i.d. isolation without accumulating cross-session familiarity, while human workers compound knowledge by repeatedly working in the same codebase or domain
- Despite superhuman benchmark performance across chess, Go, SAT, bar exams, IMO, and IOI, AI has not produced measurable impact on real-world economics or GDP — revealing a systematic gap between benchmark performance and real utility
- Harder benchmarks are solved with increasing speed — the time between benchmark creation and saturation is shrinking — making benchmark creation a treadmill that cannot sustain long-term research direction
- Incremental novel training methods now only achieve ~5% task improvements while the general recipe achieves ~30% gains without task-specific targeting — effectively crowding out independent academic research contributions
- Language pre-training priors are substantially weaker for computer control and video game domains compared to language tasks, because these modalities are far from the Internet text distribution
- Academia lacks benchmarks that properly measure the need for or quality of long-term memory in AI agents — preventing evidence-based research justification and incentive for memory methods
- Pre-recipe RL agents required millions of environment steps to learn a single task and failed to transfer skills between games or domains
- The AI field spent decades systematically under-investing in RL environment design and prior quality relative to algorithm development — an implicit signal that the research community's prioritisation instincts are unreliable
- Whether AI will solve the utility problem (gap between benchmark performance and real-world economic impact) — and on what timescale — is explicitly uncertain

## Bottlenecks

- The 'utility problem': a systematic gap between AI's superhuman benchmark performance and measurable real-world economic impact, rooted in evaluation setups that exclude the interactive, sequential, and context-dependent nature of genuinely valuable work
- The i.i.d. benchmark assumption — tasks evaluated independently, autonomously, without human-in-the-loop — blocks both training and evaluation of agents capable of real-world sequential, collaborative work
- Lack of evaluation infrastructure and field-wide incentives for measuring real-world utility (vs. benchmark scores) prevents the research community from identifying and fixing the root causes of the AI utility gap

## Breakthroughs

- Language pre-training as RL priors combined with reasoning as RL actions creates a general, transferable recipe that enables a single system to tackle diverse high-difficulty tasks without domain-specific algorithms — ending the era where methods had to be reinvented per domain
- Reasoning (open-ended language generation) as an RL action space resolves the core transfer failure of pre-LLM RL agents — counterintuitively, adding combinatorially infinite empty actions enables generalization rather than degrading expected value

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/benchmark-saturation|Benchmark Saturation]]
- [[entities/react|ReAct]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/tau-bench|tau-bench]]
