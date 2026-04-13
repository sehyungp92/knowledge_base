---
type: source
title: Speculations on Test-Time Scaling (o1)
source_id: 01KJVH25VEQ7K2S2HC77QQX37H
source_type: video
authors: []
published_at: '2024-11-12 00:00:00'
theme_ids:
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Speculations on Test-Time Scaling (o1)

**Authors:** 
**Published:** 2024-11-12 00:00:00
**Type:** video

## Analysis

- Recently, OpenAI released a new graph, where on the LHS, it showed a familiar curve where more training time compute leads to consistently better accuracy on a hard task\. On the RHS of this graph, there was a new curve that looked similar in that compute was contrasted with the performance of the model, except for the fact the x\-axis had test time compute\. The graph showed that the performance on the task gets much better as more test time compute is added to the system\. 
	- This is new and has not been seen before in language modelling\.
- One essay that often comes up when discussing scaling challenges is <a id="_Hlk187503073"></a>The Bitter Lesson, which is based on the historical observations that AI researchers have often tried to build knowledge into their agents\. This always helps in the short term and is personally satisfying to the researcher\. But in the long run, it plateaus and even inhibits further progress\. And breakthrough progress eventually arrives by opposing approaches based on scaling computation by search and learning\. 
	- <a id="_Hlk187504707"></a>What we've seen for the last five years is increase in the learning capability of models\. What we might be seeing now is a move towards search\. In particular, a type of search that is facilitated by learning to allow us to scale on some of these more technical problems\. 
- <a id="_Hlk187504823"></a>Noam Brown has been a strong proponent of search algorithms, encouraging the field in general to think more about search\. 
- One papers he discusses is from 2021 that discusses scaling laws for board games\. In this setting, it's easy to move back and forth between more training and more test time search, and the paper describes how training and test time search relate to each other\. 
- When talking about similar techniques for language models, people often bring up a paper from OpenAI from 2021, where a learned verifier is trained\. 
	- To do this, they will use a generative model to produce hundreds of different solutions\. They'll then have experts look at these solutions and select which are right and which are wrong\. 
	- Using this information, they can then train a verifier\. This verifier will tell you if you're doing well on the problem and can be used at test time to try to improve your answers\. 
- One of the most important results is that searching against this learned verifier can lead to improvements even upon just training on the actual good answers themselves\. 
	- This is an argument for moving beyond the standard SFT and more to a system that utilises a learned verifier in order to inject new signal into the model\. This allows you to utilise that verifier to improve the model at test time\. 
	- This is not what OpenAI is doing for o1, but it gives a sense of how they were exploring early uses of test time compute in developing their systems\. 

The Clues

- There are 2 sentences in the blog post published with the release of o1 that give a sense of what might be happening\. They say:
	- <a id="_Hlk187505270"></a>Our large\-scale reinforcement learning algorithm teaches the model how to think productively using its chain of thought in a highly data\-efficient training process\. 
- <a id="_Hlk187505281"></a>This sentence provides 3 clues into what might be happening: 
	- Firstly, the system is using RL, which implies that some signal is required from a verifiable problem of some sort\. Assuming there is no supervised data, the signal needs to be acquired in other ways\. 
	- Secondly, the method uses chain of thought\. Specifically, it's using CoT as its method of increasing test time compute\. This means that there is no search being done during test time\. In fact, the system is just generating a very long output stream, and using that to make its final prediction\. 
	- Finally, the system is data\-efficient\. This means is that it's learned from a relatively small set of data examples\. This is not making any claim about compute efficiency or even parameter efficiency, just that the amount of actual problems it needs is relatively small\. 
- In addition to this sentence, there are several other assumptions that people seem to be making about these models\. 
	- Firstly, it is a single final language model that generates an extremely long and coherent CoT\. It's just a model that babbles to itself until it thinks it has good enough information to make a guess of the answer to the problem\. 
	- Secondly, it is assumed that the model is not following expert examples\. This is not to say there isn't a huge amount of human supervision, but that supervision is not given in the form of direct human answers to questions\. 
	- Finally, there's an assumption that the behaviours it exhibits are learned\. That means they come somehow from data or self\-play, but not from being given to the model explicitly\. 
- Of these assumptions, the most important one is this idea of chain of thought\. The informal definition is that the model is going to generate intermediate steps in the process of producing an answer\. These intermediate steps are not supervised, but are simply sampled from the language model as we go\. 
- In the same blog post, OpenAI highlights this use of chain of thought\. They say:
	- o1 learns to hone its chain of thought and refine the strategies it uses\. It learns to recognise and correct its mistakes\. It learns to break down tricky steps into simpler ones\. It learns to try a different approach when the current one isn't working\. 
- This highlights that chain of thought is where the action is happening\. Unlike other systems that build in complex search as part of their test time, this model is simply utilising the chain of thought to do these steps as it goes\. 
- In their blog post, OpenAI additionally included some examples of the chain of thought for the system\. 
	- In one example, the model is producing an outline of all the steps it would like to produce, including complex sub\-steps

## Key Claims

1. Increasing language model parameters leads to consistently better performance at zero-shot tasks.
2. Test-time compute scaling produces consistent performance improvements on hard reasoning tasks, analogous to training-time compute scaling.
3. The Bitter Lesson holds that AI approaches based on scaling computation consistently outperform approaches that encode human knowledge into agents over the long run.
4. The current shift in language modeling may represent a move from scaling learning toward scaling search, facilitated by learning.
5. Noam Brown and other researchers underestimated how much scaling search would improve performance in game-playing AI.
6. A 2021 paper on scaling laws for board games demonstrates a trade-off between training-time compute and test-time search, showing neither alone substitutes for the other.
7. OpenAI's o1 is assumed to be a single final language model that generates a long, coherent chain of thought rather than an externally structured search system.
8. o1 is assumed not to learn from expert demonstrations; human supervision is present but not in the form of direct human answers to questions.
9. o1's exhibited behaviors are assumed to emerge from data or self-play rather than being explicitly programmed into the model.
10. Chain of thought intermediate steps in o1 are not supervised but sampled freely from the language model during generation.

## Capabilities

- Language models can scale reasoning performance at test time (inference) by generating longer chain-of-thought sequences; more compute at inference yields better accuracy on hard reasoning tasks
- Models can learn structured reasoning with planning, backtracking, and self-evaluation within a single chain-of-thought, including proposing alternatives and stopping to reconsider
- Reinforcement learning can teach models to generate and refine their own chain-of-thought reasoning, with RL-trained models outperforming those trained on human demonstrations alone
- Data-efficient RL training: models can learn to reason effectively from relatively small numbers of problem examples with automatic or learned verification signals, without requiring large scale human annotation
- Process reward models (PRMs) learning intermediate verification signals outperform outcome-only reward models, enabling more efficient rejection sampling during RL training
- Rejection sampling for acquiring verified solutions: sampling multiple chain-of-thought candidates and filtering to those that pass verification enables training on correct reasoning trajectories
- Expert iteration enables distillation of search algorithms (like MCTS or beam search) into language model weights, allowing models to learn search-like behavior through iterative training and enabling efficient inference-time reasoning
- Generative process reward models can be implemented as language models that reason through intermediate verification using chain-of-thought, merging generator and verifier into a single stream
- Amortized learned verifiers trained during RL can be deployed at test time to guide inference-time search and rejection sampling without access to original automatic verifiers
- Learning-to-correct approach: models can improve reasoning by learning to correct failed trajectories, with on-policy training preventing distribution shift and enabling iterative refinement

## Limitations

- Rejection sampling fails dramatically on hard problems where the base model success rate is extremely low; exponentially many samples needed as difficulty increases
- Learned verifiers are vulnerable to accepting out-of-distribution incorrect solutions that fool the reward model, degrading performance
- Process reward models plateau and degrade in accuracy as sample collection continues; performance ceiling emerges before desired solution quality is reached
- Combinatorial explosion in chain-of-thought trajectory space makes exact optimization intractable; marginalizing over all verified paths is computationally impossible
- Simple guess-and-check (rejection sampling) cannot explain emergent planning behaviors observed in o1, such as sophisticated backtracking and option evaluation
- Self-correction training collapses to ignoring bad solutions or fails to generalize when correction examples don't match model's actual generation distribution
- MCTS for language modeling lacks strong empirical evidence of success in open research; simpler methods outperform despite theoretical appeal
- Learning-to-correct and plan approaches are complex with many failure modes; exact implementation details critical but poorly documented in literature
- Limited empirical evidence for stream-of-search and learning-to-correct methods on realistic problems; all demonstrated results are on relatively simple tasks
- Extreme compute requirements for RL training at scale (nuclear power plants being built to support training) restrict this research to well-capitalized organizations
- Lack of transparency from OpenAI about o1's exact mechanism prevents the field from converging on best approach; multiple competing hypotheses remain unfalsifiable
- Open-source community has not yet produced successful large-scale RL-based reasoning systems despite clear evidence of concept viability

## Bottlenecks

- Automatic verifiers are limited to domains with easily checkable outputs (math, code); extension to open-ended reasoning tasks requires learned verifiers, which remain brittle
- Learned verifiers suffer from compound errors where they accept out-of-distribution incorrect solutions; no principled way to ensure robust verification at inference time
- Binary or scalar outcome-based RL signals provide zero learning gradient on hard problems where the model never produces any verified solutions (pass@k ≈ 0)
- On-policy learning requirements for self-correction create distribution shift; models trained on synthetic corrections don't learn to correct their own generated mistakes
- Expert iteration and search-based distillation require enormous training-time compute for rollouts and search; scaling to very long reasoning horizons becomes prohibitively expensive
- No principled method for selecting between competing mechanisms (guess-and-check vs process rewards vs expert iteration vs learning-to-correct) without detailed access to training internals

## Breakthroughs

- Test-time compute scaling via chain-of-thought: language models can dramatically improve reasoning performance by generating longer intermediate reasoning sequences at inference, creating a new performance scaling curve independent of model size
- Reinforcement learning can teach reasoning: models trained with RL to generate and refine their own chain-of-thought outperform those trained on human demonstrations, enabling data-efficient learning without human reasoning examples
- Process reward models outperform outcome-only reward models: learning intermediate verification signals at each step provides richer learning gradients than binary final-answer verification, enabling more efficient reasoning RL
- Expert iteration enables scaling search into models: complex search algorithms (MCTS, beam search) can be distilled into language model weights through iterative training, enabling inference-time reasoning without explicit runtime search

## Themes

- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/alphaproof|AlphaProof]]
- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/expert-iteration|Expert Iteration]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/the-bitter-lesson|The Bitter Lesson]]
- [[entities/o1|o1]]
- [[entities/self-play|self-play]]
