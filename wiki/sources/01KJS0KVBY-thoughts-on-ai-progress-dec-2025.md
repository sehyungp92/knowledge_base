---
type: source
title: Thoughts on AI progress (Dec 2025)
source_id: 01KJS0KVBYCHNQZRE4RMASZH9R
source_type: article
authors: []
published_at: '2025-12-02 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- frontier_lab_competition
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thoughts on AI progress (Dec 2025)

**Authors:** 
**Published:** 2025-12-02 00:00:00
**Type:** article

## Analysis

# Thoughts on AI progress (Dec 2025)
2025-12-02 · article
https://www.dwarkesh.com/p/thoughts-on-ai-progress-dec-2025

---

## Briefing

**The author argues that current RL-on-LLMs (RLVR/mid-training) is fundamentally incompatible with near-AGI timelines — the very effort required to pre-bake skills reveals the absence of human-like learning, and "technology diffusion lag" is cope for missing capabilities evidenced by lab revenues being 4 orders of magnitude below what AGI-level AI would command. Long-term, actual AGI (billions of human-like intelligences sharing knowledge) is expected within one to two decades, driven not by a software singularity but by continual learning, which will emerge gradually like in-context learning rather than as a sudden breakthrough.**

### Key Takeaways
1. **The RL mid-training dilemma** — If models are near human-like learners, pre-baking skills is pointless; if pre-baking is necessary, AGI is not imminent — these positions cannot both be true simultaneously.
2. **Benchmark gains are largely purchased, not discovered** — Billions of dollars paid to PhD and MD experts writing curated question-answer pairs drives benchmark progress, making this a large-scale expert systems reprise rather than genuine generalisation.
3. **Robotics as the litmus test** — Robotics is fundamentally an algorithms problem: humans teleoperate existing hardware with minimal training, so the need for massive multi-home data collection reveals the absence of human-like learning.
4. **Human labor's value is its zero-training-pipeline cost** — The macrophage anecdote illustrates that human workers are economically valuable precisely because no custom training loop is needed for each lab-specific micro-task; true AI automation requires semantic-feedback generalisation.
5. **Diffusion lag is capability cope** — AI adoption outside coding is slow because models lack capabilities, not because technology diffuses slowly; true AGI would onboard faster than human employees and diffuse through firms almost instantly.
6. **The 4-orders-of-magnitude revenue gap is the real benchmark** — Knowledge workers earn tens of trillions in wages annually; current lab revenues being ~10,000x below that number reveals how far models are from human knowledge-worker performance.
7. **RL scaling prestige is borrowed from pretraining** — Pretraining scaling followed near-physical-law predictability; RLVR has no analogous well-fit public trend, and Toby Ord's analysis implies a 1,000,000x RL compute scale-up for one GPT-level boost.
8. **AI models are capability-uniform; humans are not** — Comparing AI to the median human overestimates AI's economic value because O-ring dynamics mean top-percentile humans generate disproportionate value; but matching top humans will make AI impact explosively large.
9. **Continual learning, not singularity, is the post-AGI growth engine** — Human capability development is domain-experience-driven; the main improvement driver after AGI will be agents learning from deployment and distilling learnings back to a central model.
10. **Continual learning will unfold like in-context learning** — It will not be one-and-done; initial breakthroughs will be quickly replicated by competitors, with human-level continual learning taking another 5–10 years after first demonstrations.
11. **Competition keeps compounding** — Previous flywheels (user engagement, synthetic data) have failed to produce runaway lab advantages; some force — talent poaching, reverse engineering, rumor mills — has repeatedly neutralised them.
12. **Goalpost shifting is epistemically warranted** — Repeatedly solving supposed sufficient AGI bottlenecks (general understanding, few-shot learning, reasoning) without economic AGI is evidence that intelligence and labor are more complex than previously modelled, not evidence of bad faith.

---

### The RL Mid-Training Contradiction

- **The current RLVR/mid-training paradigm is logically inconsistent with near-AGI timelines.** Either models will soon learn on the job (making all pre-baked skill training pointless), or they won't (meaning AGI is not near).
  - Labs are building an "entire supply chain of companies" constructing RL environments to teach models tool-specific skills: web browser navigation, Excel financial modelling, PowerPoint slide crafting.
  - Humans never undergo analogous pre-training — they don't rehearse every piece of software they might ever use before starting a job.

- **The "automated AI researcher" bootstrap argument is logically circular and empirically implausible.** The claim is that clunky current RL will eventually produce a superhuman AI researcher who solves the fundamental learning problem.
  - The analogy offered: "We're losing money on every sale, but we'll make it up in volume." A system without children-level learning is being asked to solve a century-old problem that has stumped humanity's best minds.
  - **Labs' own commercial decisions contradict this framing.** You don't need to pre-bake PowerPoint skills in order to automate an AI researcher — the fact that labs are doing so reveals an implicit bet that models will continue to fail at on-the-job generalisation.

- **The efficiency counterargument has limits.** It is genuinely more efficient to build common tool fluency (browsers, terminals) once in training rather than re-acquiring it per user.
  - But this argument underrates how much **company- and context-specific skill** most jobs require — and there is currently no robust mechanism for AI to acquire these.
  - One key future advantage of AGI will be sharing knowledge across instances; but that advantage only helps for knowledge that *can* be centralised, not for the long tail of contextual judgment.

- **Beren Millidge's framing:** frontier model improvements should be attributed not just to scale and ML cleverness, but to "billions of dollars spent paying PhDs, MDs, and other experts to write questions and provide example answe

## Key Claims

1. The current approach of RL-on-LLMs with verifiable outcomes is internally contradictory with short AGI timelines: if models are near human-like learners, pre-baking skills is pointless; if pre-baking 
2. Frontier model benchmark improvements are substantially driven by billions of dollars spent hiring expert humans (PhDs, MDs) to write questions and provide example answers, resembling the expert syste
3. The heavy reliance on expert-curated human trajectories for frontier models implies they lack the critical core of learning that a true AGI must possess.
4. Robotics is fundamentally an algorithms problem rather than a hardware or data problem; the fact that enormous data collection from many homes is required reveals the absence of human-like learning.
5. The argument that current clunky RL will produce a superhuman AI researcher capable of solving AGI is implausible because such a system would lack basic learning capabilities that children have.
6. Labs' actions of pre-baking domain-specific skills (e.g., PowerPoint) signal their own implicit belief that models will continue to fail at generalizing and on-the-job learning.
7. Human workers are economically valuable precisely because they do not require custom training pipelines to be built for every subtask or lab-specific micro-task.
8. It is not possible to automate even a single job by baking in a predefined set of skills, because jobs require hundreds of daily judgment calls that differ across people and from day to day.
9. The 'technology diffusion lag' explanation for slow AI adoption is cope that glosses over missing capabilities; true AGI-level models would diffuse far more rapidly than human employees.
10. If AI models were truly at AGI level, companies would be spending trillions of dollars per year on tokens; current lab revenues being 4 orders of magnitude below that figure reveals models are nowhere

## Capabilities

- Frontier models can be trained via RL on verifiable outcomes to acquire specific tool-use skills (browser navigation, spreadsheet automation, coding) through mid-training pipelines at production scale
- Large language models exhibit powerful in-context few-shot learning, adapting to new tasks at inference time without weight updates

## Limitations

- AI models cannot learn continuously from experience during deployment — there is no robust mechanism for on-the-job skill acquisition or generalisation from novel situations encountered in production
- Frontier model benchmark gains require billions of dollars in expert-curated reasoning trajectories (PhDs, MDs, domain experts), making improvements expensive, narrow, and potentially non-generalising — a large-scale reprise of the expert systems era
- Current AI cannot automate a complete knowledge work job because each job requires hundreds of daily context-specific judgment calls and on-the-job skill acquisition that cannot be pre-baked into model weights
- RL scaling (RLVR) has no well-characterised public scaling law, with preliminary evidence suggesting approximately 1,000,000x more RL compute is needed per unit capability gain versus pretraining scaling
- Benchmark improvements from RL training mask dependence on expert data pipelines rather than genuine learning capability — gains may not reflect the general intelligence required for AGI
- AI model capabilities are roughly uniformly distributed across instances, unlike the heavy-tailed distribution of human ability, causing systematic overestimation of economic value when benchmarked against median humans
- Robotic systems must collect training data across thousands of diverse real-world environments per task (e.g. different homes for dish-washing) because models lack the sample-efficient generalisation humans use when learning to teleoperate new hardware
- Each new task domain requiring AI automation needs its own custom training pipeline, making per-task ROI negative across the long tail of specialised narrow tasks
- Current AI lab revenues are approximately 4 orders of magnitude below what AGI-level knowledge worker replacement would command, revealing that models are nowhere near replacing human knowledge workers at scale outside of coding
- Models cannot generalise the RLVR capability gains to the core learning problem required for AGI — automated AI researchers trained via RLVR are being proposed to solve a generalisation problem the models themselves do not possess

## Bottlenecks

- Absence of robust continual / on-the-job learning prevents AI from acquiring the company-specific, context-specific, and role-specific skills required during deployment, blocking broad economic adoption of AI across knowledge work
- RLVR compute scaling is extremely inefficient — preliminary evidence suggests ~1,000,000x more RL compute is needed per capability gain equivalent to a pretraining scaling step — blocking this as a cost-feasible path to AGI-level capability
- Expert data curation for RLVR creates a supply-chain bottleneck — frontier capability gains depend on expensive, time-consuming construction of high-quality human expert reasoning trajectories, limiting the breadth and pace of skill acquisition

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/continual-learning|Continual learning]]
- [[entities/in-context-learning-icl|In-context learning (ICL)]]
- [[entities/mid-training|Mid-training]]
- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
