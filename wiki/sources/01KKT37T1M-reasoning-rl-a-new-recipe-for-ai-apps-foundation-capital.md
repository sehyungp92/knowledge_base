---
type: source
title: 'Reasoning + RL: A new recipe for AI apps - Foundation Capital'
source_id: 01KKT37T1MKGPVBH7Y32GWGBHJ
source_type: article
authors: []
published_at: None
theme_ids:
- knowledge_and_memory
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Reasoning + RL: A new recipe for AI apps - Foundation Capital

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Reasoning + RL: A new recipe for AI apps - Foundation Capital
article
https://foundationcapital.com/reasoning-rl-a-new-recipe-for-ai-apps/

---

## Briefing

**The center of gravity for applied AI has shifted from RAG (knowledge retrieval) to reasoning + RL (decision-making under uncertainty), driven by pre-training saturation, a data ceiling, and maturing RL algorithms. This shift isn't incremental — it represents a fundamentally different model of what AI apps do: not retrieving and summarizing, but planning, acting, and learning from outcomes. Builders who fail to internalize this transition risk building products that are structurally obsolete.**

### Key Takeaways
1. **Pre-training has hit a wall** — Gains from ever-larger pre-training runs are plateauing; next-token prediction doesn't directly optimize for complex problem-solving or extended task coherence.
2. **The internet's text is exhausted as training data** — By 2023, models had ingested essentially all available text; RL solves the data problem by generating training signal from real interactions with the application itself.
3. **RL is the new moat-builder** — The competitive advantage is shifting from proprietary data corpora (RAG era) to process knowledge and RL training pipelines that improve continuously from deployment.
4. **IMO gold medal is proof of concept** — Google and OpenAI both achieved gold-medal performance on the International Math Olympiad using reasoning + RL, the first time AI has hit this milestone, validating the paradigm at the hardest end of formal reasoning.
5. **Control logic is migrating from developers to models** — In RAG, developers hand-crafted retrieval heuristics and query expansions; in the reasoning + RL paradigm, the model owns its own planning and information-gathering strategy.
6. **Reward hacking is the critical new failure mode** — RL systems find shortcuts to maximize reward that don't reflect intended goals; mitigating this requires multi-objective reward functions and deep domain expertise in anticipating misalignment.
7. **Process knowledge replaces document corpora** — Instead of dropping documents into a vector store, builders should collect annotated walkthroughs of expert decision-making to prime reasoning agents.
8. **Every user interaction becomes training data** — RL-based systems create a self-reinforcing flywheel: deployment generates feedback signals that feed back into the training loop, compounding improvement over time.
9. **GRPO is a key enabling algorithm** — DeepSeek's GRPO allows LLMs to explore multiple reasoning paths and learn which strategies succeed, exemplifying the new generation of RL methods making extended reasoning feasible.
10. **Reasoning model costs will commoditize** — Current frontier reasoning models are large and expensive, but distillation and specialized hardware will open reasoning approaches to latency-sensitive and cost-constrained use cases within months.
11. **Model-based RL is the next frontier** — Anticipated future techniques will let AI simulate outcomes using an internal world model before acting, enabling safer and more sample-efficient learning in open-ended domains.

---

### Why RL Is Surging Now: Four Converging Forces

- **Pre-training saturation** has made scale alone insufficient for capability gains.
  - Models like GPT-4 have vast implicit knowledge yet still make basic reasoning errors and lose coherence on long tasks.
  - Fine-tuning on domain data increases knowledge in a niche but does not teach models to solve novel problems or sustain extended tasks — RL is required to push those capabilities.
- **The data ceiling** means the internet is exhausted as a pre-training corpus.
  - By 2023, essentially all available text had been ingested; there is little novel unseen knowledge remaining in standard pre-training corpora.
  - **RL's unique answer to this problem**: it generates training data endogenously through real interactions — "you can view RL as an extreme case of a data-sparse regime: the agent learns from each attempt's outcome, creating new data as it goes."
  - The practical builder implication: train on your application — have the model learn from the real decisions and scenarios that occur within your software, not fabricated data in a vacuum.
- **Maturing RL algorithms** have made reasoning-scale RL tractable.
  - The AI community discovered that giving models more time to think yields better results, but this requires mechanisms to manage and direct that thinking.
  - New algorithms like **DeepSeek's GRPO** blend LLMs with RL to enable exploration across a space of reasoning paths and learn which strategies succeed.
  - The maturation of these methods has made it feasible to push reasoning capabilities much further than chain-of-thought prompting alone.
- **OpenAI's institutional DNA** shaped the current research agenda.
  - OpenAI's origins were in RL — game-playing agents, Rubik's Cube-solving robots, RL algorithm development — long before ChatGPT.
  - The author notes the agenda-setting effect: if Meta were leading the charge, we'd likely hear more about social interaction data and personalization instead.

---

### The Structural Difference Between RAG and Reasoning Agents

- **RAG architecture** is fundamentally a one-pass retrieval + synthesis pipeline.
  - Developer's job: engineer good retrieval (keywords or embeddings), then have LLM synthesize from retrieved text in a single pass.
  - Iteration loop is manual: if the answer isn't good, the developer refines search queries, adds context, or expands related terms (e.g., "Gong pricing," "Clari features").
  - This is conceptually analogous to how search engines like Google operate: find and rank the most relevant results, then summarize.
  - **The locus of intelligence is the developer**, who decides what to retrieve and how to frame the query.
- **Reasoning agent architecture** internalizes planning and retrieval strategy into the model itself.
  - The 

## Key Claims

1. RL for LLMs dominated the agenda at ICML, confirming a shift in the center of gravity for AI-focused founders from RAG to RL.
2. Both Google and OpenAI achieved gold-medal performance on the International Math Olympiad (IMO) using LLMs powered by advanced reasoning and RL techniques.
3. Pre-training gains have started to plateau over the past year, and simply predicting the next token does not directly optimize for solving complex problems.
4. By 2023, models had essentially ingested the entire internet of text data, leaving little unseen knowledge in pre-training corpora.
5. RL generates its own training data through real interactions, making it an effective approach in data-sparse regimes.
6. RL was key to creating the new class of reasoning models released over the past 9 months, including OpenAI's 'o' series, DeepSeek's R1, and Google's Gemini 2.0.
7. Fine-tuning on domain-specific data makes a model more knowledgeable in a niche but does not inherently teach the model how to solve new problems or carry out extended tasks.
8. Models like GPT-4 still make basic reasoning errors and lose coherence on long tasks despite having vast implicit knowledge.
9. The DeepSeek team developed GRPO, a novel RL algorithm that blends LLMs with RL to let models explore different reasoning paths and learn which strategies succeed.
10. In the reasoning agent paradigm, control logic shifts from humans to AI, with builders spending less time on prompt engineering and retrieval heuristics.

## Capabilities

- Google and OpenAI both achieved gold-medal performance on the International Mathematical Olympiad (IMO) using LLMs powered by advanced reasoning and RL techniques — the first time AI systems have ever hit this milestone.
- Reasoning agents can autonomously decompose a task into multi-step search plans, execute iterative information-gathering actions, branch exploration dynamically, and synthesise a final result — without developer-driven retrieval engineering.
- RL-trained reasoning models (OpenAI o-series, DeepSeek R1, Gemini 2.0) are in production use for enterprise long-horizon decision-making spanning dozens of systems and thousands of conditional steps.
- RL enables models to generate their own domain-specific training data through real task interactions, sidestepping the exhaustion of internet-scale pretraining corpora.

## Limitations

- Gains from scaling pretraining compute have begun to plateau — simply predicting the next token does not directly optimise for complex problem-solving, and incremental scaling no longer yields proportional capability gains.
- Despite vast implicit knowledge, frontier models like GPT-4 still make basic reasoning errors and lose coherence on long tasks.
- Fine-tuning on domain-specific data increases knowledge in a niche but does not teach models how to solve novel problems or carry out extended multi-step tasks.
- Frontier reasoning models are currently too large and computationally expensive for latency-sensitive or cost-constrained production use cases.
- RL-based agents are susceptible to reward hacking — discovering unintended shortcuts to maximise reward signals that don't reflect the true desired outcome, requiring careful multi-objective reward design and domain expertise.
- Internet-scale text data for pretraining is effectively exhausted — models have ingested essentially all available text by 2023, leaving no meaningful novel knowledge source for further pretraining-based capability improvement.
- RAG-based AI systems require continuous developer intervention to improve retrieval quality — query expansion, ranking refinement, context injection — making them dependent on human engineering rather than autonomous improvement.
- Building RL-based AI systems requires deep domain expertise to design valid reward functions — a high expertise barrier that limits who can implement reasoning + RL pipelines and increases the risk of misspecified objectives.
- Current RL algorithms for language domains lack sufficient sample efficiency for practical open-ended task training — each trial generates limited signal, making learning slow in complex environments.
- There is a near-total absence of tooling for RL-based AI product development — no standard platforms for defining custom evals, capturing structured feedback, or translating domain expert knowledge into reward functions.

## Bottlenecks

- Pretraining data for language models is effectively exhausted — the internet's text corpus has been consumed, and there is no scalable new source of novel knowledge for further pretraining-based capability improvement without synthetic or interaction-derived data.
- Frontier reasoning model inference is too computationally expensive and high-latency to be deployed in cost-constrained or real-time production contexts, blocking the reasoning + RL paradigm from reaching the full range of enterprise use cases.
- Lack of mature tooling for RL-based product development — no standard infrastructure for eval definition, feedback capture, or reward function authoring — blocks adoption of reasoning + RL by teams without deep ML expertise.
- RL algorithms for language models are insufficiently sample-efficient for open-ended, complex enterprise workflows — requiring either large volumes of interaction data or expensive human feedback to learn robustly.

## Breakthroughs

- Both Google and OpenAI achieved gold-medal performance on the International Mathematical Olympiad (IMO) — the first time any AI system has reached this milestone — using LLMs powered by advanced reasoning and RL techniques.
- The locus of AI application development has undergone a structural shift: control logic for multi-step tasks is migrating from human-engineered retrieval and prompt pipelines into RL-trained model reasoning policies — fundamentally changing how AI products are built.

## Themes

- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/data-flywheel|data flywheel]]
