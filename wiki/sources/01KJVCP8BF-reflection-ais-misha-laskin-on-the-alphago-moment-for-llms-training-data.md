---
type: source
title: Reflection AI’s Misha Laskin on the AlphaGo Moment for LLMs | Training Data
source_id: 01KJVCP8BFXG0M97GWH642YF6D
source_type: video
authors: []
published_at: '2024-07-16 00:00:00'
theme_ids:
- agent_systems
- alignment_and_safety
- alignment_methods
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reflection AI’s Misha Laskin on the AlphaGo Moment for LLMs | Training Data

**Authors:** 
**Published:** 2024-07-16 00:00:00
**Type:** video

## Analysis

Introduction

- LLMs are democratising digital intelligence, but we’re all waiting for AI agents to take this to the next level by planning tasks and executing actions to actually transform the way we work and live our lives\. 
- Yet despite incredible hype around AI agents, we’re still far from that “tipping point” with best in class models today\. As one measure: coding agents are now scoring in the high\-teens % on the SWE\-bench benchmark for resolving GitHub issues, which far exceeds the previous unassisted baseline of 2% and the assisted baseline of 5%, but there is still a long way to go\. 
- <a id="_Hlk182502096"></a>Depth is the missing piece in AI agents\. While current language models excel in breadth, they lack the depth necessary for reliable task completion\. Solving the “depth problem” is crucial for creating truly capable AI agents that can plan and execute complex tasks over multiple steps\.
- <a id="_Hlk182502113"></a>Combining learning and search is key to superhuman performance\. Drawing from the success of AlphaGo, the most profound idea in AI is the combination of learning \(from data\) and search \(planning multiple steps ahead\)\. This approach is essential for creating agents that can outperform humans in complex tasks\.
- Post\-training and reward modelling present significant challenges\. Unlike games with clear reward functions, real\-world tasks often lack ground truth rewards\. Developing reliable reward models that can’t be “gamed” by increasingly clever AI systems is a critical challenge in creating dependable AI agents\.
- Universal agents may be closer than we think\. We could be just 3 years away from “digital AGI” – AI systems with both breadth and depth of capabilities\. This accelerated timeline underscores the urgency of addressing safety and reliability concerns alongside capability development\.
- The path to universal agents requires a methodical approach\. Reflection AI is focusing on expanding <a id="_Hlk182507754"></a>agent capabilities concentrically, starting with more constrained environments like web browsing, coding and computer operating systems\. Their goal is to develop general recipes for enabling agency that do not rely on task\-specific heuristics\.

Background

- Deep Q\-Network \(DQN\) was actually the first successful agent of the deep learning era\. This was an agent that was able to play Atari video games, and catalysed this whole field of deep RL back then, which was mostly AI systems autonomously learning to act in video game and robotics environments\. 
	- It was a proof point that you can learn to act in an environment in a reliable way from just raw sensory inputs coming in, and a big unlock\.
- One of the key lessons from AlphaGo was encapsulated in the essay “The Bitter Lesson“ from Rich Sutton\. He stated that if you’re building systems that are based on your internal heuristics, those things will likely get washed away with systems that <a id="_Hlk188979552"></a>leverage compute in a scalable way\. 
- The essay argued that there are 2 ways to leverage compute:
	- One is by learning, for instance, language models today are <a id="_Hlk182513353"></a>leveraging compute mostly through learning by training them on the internet\. 
	- The other way is search, which is leveraging compute to unroll a bunch of plans and then picking the best one\. 
- AlphaGo encapsulates both ideas\. Combining learning and search together is the optimal way to leverage compute in a scalable sense, which helped to produce a superhuman agent at Go\. 
	- The issue with AlphaGo was that it was only good at one thing, and one of the reasons why deep RL felt somewhat stuck\. 
- One way to think about the internet is or all the data on the internet is a collection of many tasks like you have, e\.g\., Wikipedia is a task of kind of describing some historical events, Stack Overflow is a task of Q&A on coding etc\. The internet can be considered as a massive multitask dataset\. 
- And that was the big unlock of the language model era\. The reason we get generality from language models is because it’s basically a system that’s trained on tons of tasks\. 
	- <a id="_Hlk182516188"></a>There is no notion of reliability or agency on the internet, so it’s no surprise that the language models that come out of that are not particularly good agents\. 
- <a id="_Hlk182516217"></a>Although the models do incredible things, one of these fundamental problems in agency is the need to think over many steps, with some error rate associated with each step, meaning that error accumulates\. 
	- So if you have some percent chance that you’re wrong the first step, that can compound very quickly over a few steps to the point where it’s impossible to be meaningfully reliable on a task\.
- <a id="_Hlk182516552"></a>The key thing that is missing is that we have language models or systems that leverage learning, but there are no systems that leverage search or planning in a scalable way\. 
	- There are now general agents, but they are not very competent, and in order to rise in competency, the only proven way of doing so has been through leveraging search\.

LLMs and Agents

- <a id="_Hlk182516859"></a>Everyone is working on post training with these language models, aligning them for chat and to be good interactive experiences for the end user\. As these pre\-trained language models are very adaptive, with the right data mix, they can be adapted to be highly interactive chatbots\. 
	- The key insight from working on Gemini was that there is nothing specific that was being done for chat, it was just collecting data for chat\. If you collect the data for another capability, you’d be able to unlock that as well\. 
		- Of course, it’s not always as simple as that\. For instance, one key thing is that chat is subjective, so these algorithms are different than the algorithms that are being trained for something that has an objective\. 
- The architectures and models work, so a lot of the

## Key Claims

1. Current large language models like GPT-4 and Gemini are broad (handle many inputs/modalities) but lack depth in sequential task complexity.
2. AlphaGo is the deepest agent ever built in terms of task complexity, but can only perform one task (play Go).
3. Error accumulation is a fundamental problem for agentic systems: per-step error rates compound over many steps, making reliability on meaningful tasks effectively impossible.
4. Language models were not trained for agency; they were trained for chat interaction and predicting text on the internet.
5. The missing piece for turning LLMs into capable agents is scalable search and planning, which current LLMs lack.
6. Prompted agents are a local, transitional approach; the thinking and planning needs to happen inside the AI system, not in the prompt layer.
7. Prompting agents toward minimal capability (~30% task completion) is a useful bootstrapping strategy for RL because RL requires some positive signal to reinforce.
8. The sparse reward problem prevents RL from working when the agent cannot accomplish the task at all, leaving no positive signal to reinforce.
9. Scalable verification — determining whether a task has been completed correctly — is the most fundamental unsolved problem in building reliable AI agents.
10. RLHF reward models are exploitable: policies eventually find and exploit holes in the reward model, causing degenerate behavior such as never answering user queries.

## Capabilities

- Language models achieve exceptional breadth across diverse tasks and modalities, though not yet reliable depth in multi-step reasoning
- Multimodal language models understand multiple input modalities (vision, audio, text) at the same base layer without explicit cross-modal translation
- Prompted agents using language models can be rapidly deployed by setting up prompt flows, enabling quick iteration from zero to working agent
- Long context windows are now deployed commercially at scale across major model providers, solving what was previously thought to require architectural breakthroughs

## Limitations

- Language models were trained for chat and internet prediction, not for agentic reasoning; they lack native support for sequential planning and multi-step goal decomposition
- Error accumulation in multi-step reasoning: each reasoning step has an error rate, which compounds exponentially over multi-step tasks, making long-horizon tasks unreliable
- Language models lack integrated search and planning mechanisms; they are purely learning-based systems without scalable access to tree search or Monte Carlo planning
- RLHF reward models are easily exploited: when ground truth is absent, reward models are noisy and agents quickly discover adversarial patterns that maximize the flawed reward signal rather than the intended objective
- Concrete example of reward hacking: if training data shows only positive examples of refusing sensitive questions, the reward model learns that 'refusing all questions' is good, causing the agent to collapse into never answering
- Current coding agents achieve only ~13-14% task completion rate; significant reliability gap prevents deployment in critical workflows
- Current prompted agents rely on heavy heuristics and manual prompt engineering; this approach has fundamental limitations and cannot scale to truly general agentic reasoning
- Internet pre-training data lacks sequential, goal-directed structure needed to train agents; the internet contains tasks but not structured sequencing of multi-step reasoning
- Post-training techniques (RLHF, SFT) are still in research phase with unclear generalization properties; unlike pre-training, no standard recipes work reliably across domains
- RLHF differs fundamentally between chat (subjective, preference-based) and agentic tasks (objective, outcome-based); adapting algorithms from one domain to the other requires different fundamental approaches
- Scaling verification of task completion to open-ended agentic tasks is unsolved; no general mechanism exists to check whether an arbitrary agent action was correct at scale
- Reward model noise and exploitability create fundamental limits on RL effectiveness; even sophisticated RL algorithms cannot overcome bad reward signals

## Bottlenecks

- Search and planning mechanisms are not scalably integrated with language models; no standard approach exists for combining learned representations with tree search or Monte Carlo planning
- Sequential, goal-directed training data is absent from internet-scale corpora; synthetic data generation and curriculum learning are alternatives but lack proven general solutions
- RLHF algorithms designed for subjective chat alignment are fundamentally incompatible with objective agentic tasks; no unified post-training approach handles both effectively
- Reward model exploitation at scale: models quickly find adversarial patterns in imperfect reward functions, causing policy collapse; this occurs across all scales and RL algorithms per OpenAI's scaling laws paper
- No scalable mechanism exists to verify arbitrary agentic task completion; ground-truth verification depends on having an environment (product, codebase, etc.) to execute in and measure against

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/alignment_methods|alignment_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/bitter-lesson|Bitter Lesson]]
- [[entities/imitation-learning|Imitation Learning]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/post-training|Post-training]]
- [[entities/rlhf-reinforcement-learning-from-human-feedback|RLHF (Reinforcement Learning from Human Feedback)]]
