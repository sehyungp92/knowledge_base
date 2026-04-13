---
type: source
title: Why o1 is a BIG deal
source_id: 01KJVHWJNMSKRJGJF4T97SY0Y4
source_type: video
authors: []
published_at: '2024-11-09 00:00:00'
theme_ids:
- ai_market_dynamics
- chain_of_thought
- frontier_lab_competition
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why o1 is a BIG deal

**Authors:** 
**Published:** 2024-11-09 00:00:00
**Type:** video

## Analysis

- One of the fundamental roadblocks to AGI was reasoning, and OpenAI believes it has been solved\. 
- If the model functions similar to humans, it may be easier to predict that it will be as good as humans\. And for most people, it does not feel intuitive that o1 is similar to human reasoning, but it may be\.
	- The older models are similar to System 1, while o1 fills in the gap of the System 2 reasoner\. 
- If you want to compare humans to AI under the same kind of constraints where they both do not think, performance wise, models obliterate humans on System 1\. GPT\-4 intuitively is very good and there are not a lot of tasks humans are better at\. 
	- Of course they have architectural differences\. They are able to take in the input data in parallel, just like how humans take in vision in parallel\. So we do not have to look at an image pixel by pixel sequentially and so can speak about an image within a second\. LLMs can do this with text\. 
- For creativity, it is better to ask GPT\-4 than o1, specifically asking GPT\-4 not give a chain of thought, but to just give the answer immediately and respond intuitively\. 
- <a id="_Hlk184907356"></a>With System 1 thinking, it is quite reasonable to assume they do not generalise well outside of distribution\. When you give them a novel problem that is truly novel, they will not be able to solve it\.
	- This is also similar to humans, where our intuition is still limited to the data we've been trained on, our experiences\. <a id="_Hlk184907376"></a>When something's truly novel, we need System 2 thinking and reasoning\. 
- <a id="_Hlk184898084"></a>o1 represents a different paradigm because what they are doing is reasoning, which can be defined as when sequences of data are generated in order to build a bridge from what we know to what we do not know\. That's exactly what these models are doing, generating chains of thought, to get to what they know to what they do not know\. 
	- In other words, they are able to simulate data around a problem that's outside of distribution\. And by simulating data around it, they make it in distribution, in a sense\. 
	- This is similar to what humans do\. When humans get something out of distribution, when they see a physics problem they haven't encountered before, they have to think about it\. They have to think, generate data, make a simulation around this data, and then they are able to solve it\. 
- The older models are not allowed to use the generation of data to solve a problem in real time\. Even if they are instructed to do chain of thought, it may improve the accuracy of the model, but it is not trained to use chain of thought effectively\. 
	- Humans, on the other hand, are trained to use chain of thought effectively\. When we make a mistake, we can look at why we made that mistake, look at the steps involved that caused us to make this mistake\. 
- o1 utilises what they already know to generate chains of thoughts and then have the model evaluate these chains of thoughts, see which ones are correct, which ones are logical, and when the answer produced from this chain of thoughts is incorrect, it is able to reflect on it and see what they did wrong and learn from that\. 
	- This is exactly what humans do, we generate data to go from what we don't know to what we want to know, and so we make out of distribution problems in distribution\. 
	- These models were not able to do this because they were not able to utilise the test time compute to go from the problem to the answer, but now they are able to and now they are trained to utilise this well\. This is the paradigm shift\. 
- Performance wise, they are going to get better\. They are comparing o1 to GPT\-2\. There may be another breakthrough and another way of thinking about things, but this is viewed as key to reaching AGI\. 
- One may point at other differences, such as our ability to actively learn\. But this may be more of a design choice than an architectural limitation as OpenAI wants to keep training controlled, so they train it on specific runs instead of continuously\. 
	- This can easily solved by finetuning models\.

---

OpenAI o1 \- the biggest black box of all\. Let’s break it open

## Key Claims

1. Reasoning has been identified as a fundamental roadblock to AGI, and OpenAI claims o1 has solved it.
2. OpenAI defines five levels of AI progression: chatbots (level 1), reasoners (level 2), agents (level 3), and beyond.
3. Sam Altman believes the path to AGI is now clear, with no unknown breakthroughs required beyond the reasoning paradigm established by o1.
4. ASI (artificial superintelligence) is estimated by OpenAI to be thousands of days away.
5. Pre-o1 large language models operate analogously to System 1 (fast, intuitive) thinking, not System 2 (slow, deliberate) thinking.
6. Older LLMs do not use test-time compute; they generate answers instantaneously without spending energy reasoning during inference.
7. GPT-4 outperforms humans on System 1 tasks, with few tasks where humans perform better.
8. Older LLMs can generalize to unseen data distributions (System 1 generalization) but fail on truly novel, out-of-distribution problems requiring reasoning.
9. Reasoning is defined as the sequential generation of data (chain of thought) to build a bridge from known information to unknown conclusions, transforming out-of-distribution problems into in-distribu
10. Older LLMs were not trained to use Chain of Thought effectively at test time, limiting their ability to reason about novel problems.

## Capabilities

- o1 solves novel, out-of-distribution problems through System 2 reasoning by generating intermediate chain-of-thought steps at test time
- Models can perform System 2 reasoning by generating intermediate data (chains of thought) to simulate out-of-distribution problems and map them to in-distribution solutions

## Limitations

- Legacy language models (pre-o1) lack effective test-time reasoning training and cannot utilize generated intermediate data (chain-of-thought) to solve problems at inference time
- System 1 models (standard autoregressive LLMs) generalize poorly to out-of-distribution problems and cannot handle genuinely novel scenarios encountered beyond training data
- RLHF training provides only binary feedback signals (correct/incorrect) rather than step-level reasoning feedback, preventing models from learning which specific reasoning steps caused failures
- Models are constrained to text-based reasoning and cannot directly visualize or spatially simulate scenarios (unlike humans), limiting certain forms of intuitive problem-solving
- Production deployments intentionally disable continuous online learning to prevent models from absorbing low-quality or contradictory user data

## Breakthroughs

- o1 achieves System 2 reasoning through test-time compute, enabling models to solve out-of-distribution and novel problems by generating intermediate reasoning chains that simulate solution trajectories

## Themes

- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/system-1-thinking|System 1 thinking]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/o1|o1]]
