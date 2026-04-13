---
type: source
title: How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek
source_id: 01KJVF0TDNJTX98GKVNDR444RS
source_type: video
authors: []
published_at: '2025-10-16 00:00:00'
theme_ids:
- ai_market_dynamics
- chain_of_thought
- frontier_lab_competition
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek

**Authors:** 
**Published:** 2025-10-16 00:00:00
**Type:** video

## Analysis

Briefing

- Jerry Tworek, a key figure behind OpenAI's reasoning models, makes the case that the combination of large\-scale pre\-training and scaled RL is not merely a current technique but the foundational DNA of OpenAI since 2019\. 
- The conversation traces the full arc from DQN and Dota through RLHF and GPT\-4 to o1 and GPT\-5, with Tworek arguing that each step was necessary and neither component can succeed without the other\. 
- The central unresolved question – when a model can improve itself without human intervention – is identified as the true threshold that makes AGI predictions genuinely murky\.

Key Takeaways

- OpenAI's research plan in 2019 was identical to what they are executing today: "train a large generative model on all the data we can, then do RL on it"; the algorithms and architectures have changed but the core program has not\.
- o1 was a technology demonstration, not a polished product – it was "really mostly good at solving puzzles"; o3 was the first reasoning model Tworek personally found meaningfully useful and began using exclusively\.
- GPT\-4 was internally underwhelming before RLHF – the raw pre\-trained model seemed "pretty dumb" on long\-form generation despite strong single\-token evaluation scores; RLHF was what delivered the GPT moment the world experienced\.
- Pre\-training and RL are mutually dependent\. RL would not work without pre\-training, and pre\-trained models have limitations very hard to resolve without something that looks like RL\.
- RL is dramatically harder to scale than pre\-training – pre\-training is simple mathematically; RL has many more moving pieces, more failure modes, and more delicate tuning requirements at scale\.
- DeepSeek's GRPO release accelerated the entire US AI ecosystem – o1 caught most US labs by surprise; DeepSeek's adjacent RL work, open\-sourced shortly after, gave labs a roadmap that would otherwise have taken much longer to discover independently\.
- Reward hacking is a structural problem in RL analogous to bad incentive design in policy\-making\. What you reward is not always what you want; the whack\-a\-mole between reward shaping and model behaviour is ongoing and fundamental\.
- Online RL from live user interaction is theoretically possible but currently avoided – Cursor is reportedly experimenting with it; OpenAI is not, citing insufficient safeguards around what gets reinforced in a loop at ChatGPT's scale\.
- Alignment is partly an RL problem and partly a pure AI problem – steering behaviour is RL; but the model must also deeply understand consequences to choose correctly, which cannot be achieved by telling the model a few good things to do\.
- The self\-improvement threshold is the real AGI question – when is the moment that the model can improve itself without humans working on it and fixing it?
	- The path to AGI will feel like accumulation, not revolution\. It will feel less like completely turning around and more like keeping on adding more things, and maybe dissolving some old elements\.
- GPT\-5 is characterised as "o3\.1", an iteration of the same concept; the next significant jump the team is pursuing involves models thinking longer, interacting with more systems, and operating even more autonomously\.

What Reasoning Actually Is

- Reasoning is the process of getting to an answer you don't yet know, as distinct from answering a question where you already know the answer\. The longer spent getting there, by whatever means necessary, the better the result tends to be\.
- Language models are fundamentally next\-token prediction machines, but CoT externalises their thinking process in human words and concepts\. The capability emerges from training on vast amounts of human\-generated text in which humans already demonstrate step\-by\-step thinking\.
	- Classic demonstration: asking a model "what is 2\+3×4?" fails if it tries to answer in one token; asking it to "solve step by step" works because the intermediate tokens carry partial computation\.
	- CoT is basically a process of thinking encoded in words, how humans would solve a problem on a piece of paper\.
- How models decide how long to think \(auto mode in GPT\-5\):
	- Fundamentally a user experience trade\-off: longer thinking = better results, but users dislike waiting\.
	- The same underlying model is used for high\- and low\-reasoning modes; a parameter controls desired thinking length\.
	- Heuristics are encoded for when better answers are worth the wait, but it is ultimately about guessing the anticipation of the users\. High\- and low\-reasoning modes are exposed explicitly to allow users to make that trade\-off themselves\.

The Evolution of Reasoning Models

- The reasoning programme was a series of scale\-up runs that were progressively more ambitious\.
- o1: Released to demonstrate that reasoning models exist and work\.
	- The model was really mostly good at solving puzzles and a few thinking problems\. It was almost more of a technology demonstration than an actually really polished product\.
	- It caught most AI labs by surprise\.
- o3: The tectonic shift: a model that is meaningfully useful\.
	- Key capabilities: tool use, leveraging contextual information from multiple sources, persevering toward answers\.
- GPT\-5: Characterised as "o3\.1" – an iteration of the same concept and methods, not a paradigm shift from o3\.
	- Downstream products built on o3 technology: Codex, ChatGPT Agent, Deep Research\. Coding agents are at the moment the first really successful agentic products built on top of AI\.

Reinforcement Learning: From Basics to Modern Scale

RL 101

- Dog training analogy: give a treat for good behaviour, withhold attention for bad behaviour; over time the dog learns what you want\. The good way to do RL is if you balance those things – give cookies half of the time and punish the other half\.
- RL is fundamentally different from next\-token prediction\. It is a completely different gradient, a completely different se

## Key Claims

1. Reasoning is the process of getting to an answer you do not yet know, and the longer time spent on that process, the better the result.
2. Chain of thought is the thinking process of language models verbalized using human words and human concepts.
3. Language models learn to think like humans by training on human-generated text, which contains human thinking processes.
4. o1 was primarily a technology demonstration rather than a polished or broadly useful product, being mostly good at solving puzzles.
5. o3 represented a tectonic shift in the trajectory of AI, being a meaningfully useful model capable of using tools, leveraging contextual information from multiple sources, and persevering toward answe
6. GPT-5 can be considered o3.1 — an iteration of the same concept and approach as o3, not a fundamentally new paradigm.
7. Modern language models are first pre-trained, then undergo reinforcement learning; neither phase works well in isolation.
8. OpenAI's core research plan since early 2019 has been to train large generative models on all available data and then apply reinforcement learning — and this is exactly what is being executed today.
9. GPT-4 was underwhelming internally before RLHF was applied, appearing not much better than GPT-3 for long-form generation despite showing intelligence on single-token evaluation tasks.
10. RLHF was the key technique that transformed the raw GPT-4 pre-trained model into a successful product, making the 'ChatGPT moment' possible.

## Capabilities

- O3 model demonstrates meaningful practical utility with tool use, multi-step planning, and ability to leverage contextual information from various sources to solve complex problems
- Models can allocate extended thinking time to reason through problems, with demonstrated capability to think for 30 minutes, hours, or longer on certain task types before producing output
- Frontier reasoning models achieving competitive programming performance: solved 12 complex algorithmic problems in 5-hour time limit at ICPC, equivalent to first place; also competed in IOI and other programming contests
- O1 model demonstrated inference-time reasoning capability through extended chain-of-thought, enabling problem-solving on complex puzzles and thinking-oriented tasks via 'stop and think' mechanism
- Agentic coding agents (Codex-based) represent the first materially successful agentic products built on large language models, achieving practical automation of software development tasks
- Scientists actively using frontier reasoning models to solve real technical problems: reported credible instances of scientists using reasoning models for calculations and complex technical problem-solving, moving beyond competition metrics to practical research applications

## Limitations

- O1 model exhibited limited practical utility despite reasoning capability; good at puzzles but not broadly useful; product-level polish insufficient for deployment beyond technology demonstration
- Early GPT-4 (pre-RLHF) exhibited severe coherence breakdown on longer-form generation despite appearing smart in single-token responses; could not sustain logical reasoning across multi-turn outputs
- Reward hacking is endemic in RL training: models reliably discover adversarial loopholes in reward functions, optimizing for the literal reward signal rather than the spirit of the intended objective
- No principled, scalable reward function mechanism exists for open-ended language and agentic tasks; ground truth for task completion is either subjective, undefined, or prohibitively expensive to verify at scale
- RL training complexity far exceeds pre-training: many more moving pieces, error modes, bottlenecks, and failure modes that scale with system size; much harder to control and predict than pre-training
- Extended thinking capabilities (30min-2hr reasoning budgets) exist but lack proven product deployment model; no established user-facing interface or UX pattern for consuming long inference times
- Models show dramatically asymmetric capability across domains: excel at programming/math/puzzles with clear ground truth, but fail to match human performance on subjective/open-ended tasks and real-world knowledge work
- Human data labeling is both essential and continuously displaced: data labeling industry must constantly reinvent itself as models improve, because tasks models cannot yet solve become tasks models can solve, eliminating labeling opportunities

## Bottlenecks

- No scalable reward function mechanism for open-ended language and agentic tasks; cannot verify or reward task completion in domains without clear ground truth or where verification is expensive
- RL training has exponentially more failure modes and complexity than pre-training; many moving pieces including reward design, policy gradient computation, entropy management, exploration-exploitation balance all creating interdependent failure modes at scale
- No established product pattern or user interface for consuming models with long inference-time thinking budgets (30min-2hr); unclear how to deliver value in latency-sensitive applications or real-time interactive systems
- Fundamental asymmetry in model capability across domains: RL with verifiable rewards works well for programming/math but cannot be extended to subjective, open-ended, or knowledge-intensive domains where humans disagree or ground truth is undefined

## Breakthroughs

- RLHF (Reinforcement Learning from Human Feedback) unlocked high-quality language model outputs by optimizing post-training using human preferences; transformed GPT-4 from internally disappointing to world-class through preference-based reward optimization
- Inference-time reasoning scaling via extended chain-of-thought (O1 model): models can allocate additional compute at test time to 'think through' problems before generating answers, enabling step-by-step reasoning without increasing training compute
- Large-scale reinforcement learning on pre-trained language models validated OpenAI's 2019 core research hypothesis: pre-train on all available data then apply large-scale RL to create capable reasoning models

## Themes

- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/agentic-ai|Agentic AI]]
- [[entities/chain-of-thought-cot|Chain of Thought (CoT)]]
- [[entities/gpt-4|GPT-4]]
- [[entities/gpt-5|GPT-5]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/o1|o1]]
- [[entities/o3|o3]]
