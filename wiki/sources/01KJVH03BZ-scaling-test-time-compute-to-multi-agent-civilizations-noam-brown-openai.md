---
type: source
title: Scaling Test Time Compute to Multi-Agent Civilizations — Noam Brown, OpenAI
source_id: 01KJVH03BZQ19MPYYZFNY9E9QE
source_type: video
authors: []
published_at: '2025-06-19 00:00:00'
theme_ids:
- agent_systems
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Scaling Test Time Compute to Multi-Agent Civilizations — Noam Brown, OpenAI

**Authors:** 
**Published:** 2025-06-19 00:00:00
**Type:** video

## Analysis

Reasoning Models & Fast vs\. Slow Thinking Paradigm

- The thinking fast and slow \(System 1 and System 2\) analogy, while reasonably diffused, is imperfect when applied to AI scaling\. One underappreciated aspect is that the pre\-trained models need a certain level of capability in order to benefit from this extra thinking\.
	- This is why the reasoning paradigm emerged when it did –  trying to apply a reasoning paradigm on top of GPT\-2, for example, would yield almost anything\. Small models showed no benefit from CoT, but larger models began to demonstrate a lift\. 
		- There is a lot of debate about the extent to which this kind of behaviour is emergent, but clearly there is a difference\.
		- These are not 2 independent paradigms, they are related in the sense that you need a certain level of System 1 capability in your models in order to have to be able to benefit from System 2\.
- System 2 thinking does apply to visual reasoning, but its benefit depends on the specific question\.
	- For instance, GeoGuessr, where o3 has demonstrated impressive performance, is certainly one where you do benefit from System 2 thinking\. 
	- For simple image recognition, there is likely to be less benefit from System 2 thinking because you know it or you do not\.
		- This may be analogous to information retrieval: if you need a specific fact and do not have web access, you either know it or you don't\. 
	- For spatial reasoning tasks like Tic\-Tac\-Toe, where all information is present, while GPT\-4\.5 can make legal moves, it falls over and will make mistakes sometimes\. Although it may be possible for a much larger System 1 model in the future to play perfectly without explicit System 2 scaffolding, but right now, you would need a System 2 approach\. 
- The more System 1 capability \(intuition, implicit knowledge\) a model has, the faster it will be\.
	- This is similar to humans learning chess, where a very smart person might do well in a novel game by applying intense System 2 thinking for weeks, but building up System 1 intuition significantly increases speed and efficiency\.
- However, building harnesses \(external scaffolding or prompt engineering that guides the model\) for specific games or tasks may be similar to giving models crutches that they will eventually move beyond\. The ideal harness is no harness\.
	- The goal should be to improve the capabilities of the models so they can do well at everything without harnesses, which would then inherently lead to progress on more specific evaluations\.
- Sometimes System 2 capabilities are classified as test\-time compute, but there are times where that paradigm may not be directly applicable\. 
	- For instance, in robotics, if a robot takes some action in the world and it breaks something, you cannot simply undo that action\. 
		- If it were to simulate what would happen if the robot moves in a certain way, and decided not to do that action, as a result, that would be completely different\. 
- The question of whether a router \(to send requests between a fast System 1 model and a slower System 2 model\) needs to be smart or dumb is a complex one\. 
	- A dumb model could recognise a problem's difficulty and route it, but there is also the risk of a dumb model being fooled or overconfident\. There is a real trade\-off\.
- At the same time, many current development patterns, like harnesses and routers, will eventually be washed away by scale\. 
	- This is similar to how complex agentic systems built on non\-reasoning models became somewhat less relevant with the advent of reasoning models\. The complex behaviour, in many ways, makes it worse and it is better to just give the reasoning model the same question without any scaffolding
	- These current scaffolds will be replaced by models in general becoming more capable\. 
		- For instance, OpenAI's stated goal is a single unified model, which would render routers unnecessary for internal model routing\.
- Product developers face a difficult challenge in planning for models that are rapidly changing\. They need to avoid spending significant time building something that might be obsolete in a similar timeframe due to rapid model advancements\. 

Reinforcement Finetuning and Long\-Term Model Adaptability

- RFT is interesting and worth looking into for developers\. Its key benefit lies in specialising the models for custom data that is not baked into the raw model\.
	- Unlike harnesses that might be made obsolete by larger models, the data collected for RFT is going to be useful as the models improve as well\. This makes RFT a strategy that compliments the model scaling and becoming more capable rather than necessarily getting washed away by the scale\.
- In various game domains \(poker, Hanabi, Diplomacy\), having models think before acting resulted in orders of magnitude difference, equivalent to models 1,000\-100,000x bigger\.
	- At the same time, it was evident that simply scaling pre\-training alone would not lead to superintelligence in LLMs\. Just scaling pre\-training would hit economic feasibility limits before achieving superintelligence unless a reasoning paradigm was found\.
- RL went through a dark age but is now in a golden age, which is not just attributable to smarter base models and better data, but also to a gradual process of finding signs of life and then iterating\.
	- OpenAI recognised very conclusive signs of life around October 2023 and invested heavily in scaling it up, which ultimately what led to reasoning models arriving when they did\.
	- Initially, RL research at OpenAI was framed around data efficiency with concerns about hitting a data wall before compute limits\. However, it turned out RL also effectively provides the equivalent of scaling up compute also by a ton\.
- Even established AI researchers often question if reasoning models can succeed in domains where success is less well\-defined \(beyond easily verifiable areas like maths and coding\)\.
	- However, in some

## Key Claims

1. Cicero achieved top 10% of human players in Diplomacy when released in late 2022
2. Cicero was bottlenecked by the quality of available language models at the time of its development
3. Cicero would hallucinate and deny prior statements it had made in conversations, even when users could scroll up to verify
4. Humans who were not expecting a bot were inclined to rationalize bizarre bot behavior as tiredness, intoxication, or trolling
5. The ideal AI harness for game-playing is no harness — harnesses are a crutch that AI should eventually move beyond
6. O3 without any harness performs poorly at playing Pokémon
7. Building a better harness to improve eval scores is the wrong response to poor model performance; the correct response is improving underlying model capabilities
8. DeepSeek found that MCTS was not particularly useful in their system
9. Many engineers are currently spending large numbers of tokens on search techniques without commensurate benefit
10. There is a meaningful distinction between a tool call to verify move legality before acting versus making a move and receiving legality feedback as an environment signal

## Capabilities

- Deep research: AI generates high-quality research reports and analysis in open-ended domains with subjective success metrics, demonstrating reasoning works beyond easily-verifiable tasks
- O3 reasoning model operates as general-purpose problem-solver replacing search and enabling complex coding tasks through extended inference-time reasoning
- Extended test-time reasoning: models allocate variable compute at inference time (minutes to hours to days) for complex problem-solving across domains
- AI agents achieve world championship-level play in multi-player negotiation games with imperfect information (Diplomacy)
- Adaptive opponent modeling: agents learn to understand and adapt to individual opponent playstyles in multi-agent competitive/collaborative games

## Limitations

- Language models hallucinate about conversation context, failing to track prior statements or acknowledge content explicitly visible in chat history
- AI models require orders of magnitude more data than humans to achieve equivalent learning efficiency
- Scaling test-time compute incurs exponential cost increases, creating hard ceiling on inference-time reasoning budget per query
- Extended test-time reasoning breaks research iteration velocity: experiments requiring hours/days of thinking cannot be parallelized, forcing serial iteration
- Reasoning paradigm requires minimum pre-training capability threshold to be effective; fails to improve performance when applied to small models
- Reasoning models have high latency (hours per query), preventing use as real-time interactive pair programmers in coding workflows
- Self-play training converges only to minimax equilibrium in 2-player zero-sum games; inadequate for multi-player or non-zero-sum scenarios requiring collaboration
- Imperfect information enumeration (poker approach) breaks down as hidden state space scales; 40-piece games have ~40! possible states, making enumeration infeasible
- No perfect simulator of human biology and chemistry exists, blocking validation of AI-designed drugs without wet-lab testing
- Physical robotics research has fundamentally slower iteration cycles than software due to hardware constraints

## Bottlenecks

- Wall-clock time constraint on research iteration: as models require hours/days of reasoning, research iteration speed hits wall-clock time bottleneck rather than compute bottleneck
- Biological/chemical simulation fidelity gap: absence of accurate digital simulators of human biology prevents AI-assisted drug discovery from leveraging extended reasoning
- Self-play convergence limitation: minimax equilibrium convergence only valid for 2-player zero-sum games; blocks scaling self-play to multi-agent non-zero-sum domains

## Breakthroughs

- Reasoning paradigm (o1/o3): test-time inference-time compute with explicit reasoning chains achieves 1000-100,000x performance equivalent improvements
- Reasoning paradigm generalizes to non-verifiable domains: test-time reasoning works in domains with subjective success metrics (research, writing, analysis)
- Multi-agent negotiation games solved at world championship level: AI agent capability in Diplomacy reaches competitive world-championship level against top human players

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/bitter-lesson|Bitter Lesson]]
- [[entities/codex|Codex]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/system-1-system-2-thinking|System 1 / System 2 Thinking]]
- [[entities/windsurf|Windsurf]]
- [[entities/multi-agent-systems|multi-agent systems]]
- [[entities/o3|o3]]
