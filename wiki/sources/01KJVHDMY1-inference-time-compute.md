---
type: source
title: Inference Time Compute
source_id: 01KJVHDMY177HGHEF0FQ6JZM59
source_type: video
authors: []
published_at: '2024-12-03 00:00:00'
theme_ids:
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Inference Time Compute

**Authors:** 
**Published:** 2024-12-03 00:00:00
**Type:** video

## Analysis

Key Features of o1 Style Models

- <a id="_Hlk187528364"></a>Taking a closer look at o1, it is possible to identify some key features:
	- The model goes through a long thinking process, where thinking is defined as a token string, before generating the final answer\. 
	- It undertakes step\-by\-step reasoning, so it follows some thoughts decomposition on the step\-by\-step decoding process to solve the problem\. 
	- There are many repeated self\-reflections in trial\-and\-error loops\. 

Enabling LLMs to Think

- <a id="_Hlk187528369"></a>Open AI says in their blog that o1 thinks before its answers – it can produce a long internal chain of thoughts before responding to the user, where the keywords are “long” and “chain of thoughts”\.
- Chain of thought prompting can be described as a technique where the model is taught to think by imitating human reasoning process\.
	- For example, in a QA setting where some in\-context samples are given as examples to familiarise the model with the format, chain of thought prompting works by manually adding some rational explanations of each example, which the model will learn to follow, generating some explanations at the beginning before producing the answer\. 
- There are a couple of theoretic works that try to explain why CoT is so powerful for an LLM\. 
	- Theoretically, CoT adds recurrence computation back to transformers, extending expressivity of transformer to solve inherently serial problems, which is an important problem class\. 
		- Inherently serial problems include evaluating some arithmetic expressions, doing some automata simulation, and composing some permutations\. Combined, they get extended capability for evaluating code, doing maths and performing better on reasoning tasks\. 
- However, there are also some problems that transformer even equipped with CoT cannot solve:
	- Graph connectivity problems \(NC\-Complete\), including any node connectivity problems\. 
	- Linear programming or linear equalities \(P\-Complete / P\-Hard\) 
	- In\-context context\-free recognition \(P\-Complete / P\-Hard\) 
	- Testing whether a number is a prime \(P\-Complete / P\-Hard\) 
- The model can learn to imitate the reasoning process to think with CoT\. However, CoT dataset is expensive to obtain and requiring a lot of human annotations\. So the question is can the model be used to help generate high\-quality rationales that can be later used to train a model to do reliable CoT\. 
- The STaR paper describes a bootstrapping approach to create a CoT dataset\. 
	- The process starts by asking an LLM to generate rationales to questions where the ground truth answer is known\. If the generated answer is correct, then we can pseudo label this rationale to be correct, and augment the original data set with this generated rationale\. 
	- But if the answer is incorrect, the model is given the ground truth answer to let it reason backward and re\-prompted to generate a better rationale and answer\. And if the model now provides the correct answer, this new rationale would be added to the original dataset\. 
	- This generated CoT dataset can be used to finetune the language model\. 

Enable Step\-by\-Step Reasoning via Process Reward Model

- <a id="_Hlk187529040"></a>In the above process, only the final outcomes were used to supervise the model and do not ask whether the generated rationales are logical, reasonable or faithful\. And it is challenging to ask the model to elaborate and plan ahead if supervision is only provided based on the final outcome\. 
	- Some research have found that even some non\-informative rationales \(e\.g\., random tokens\) can improve model performance\. So unlocking reasoning in inference\-time only is not robust\. 
- To provide more fine\-grained supervision for every reasoning step, much more effort is required to collect the necessary supervision dataset to train a process reward model \(PRM\)\. There are broadly 2 ways to collect this fine\-grained supervision data: 
	- For the necessary step\-wise annotation, OpenAI’s Let's Verify Step\-by\-Step paper or PRM800k uses high\-quality manual annotation from experts\. 
	- The Math\-Shepherd paper demonstrates a way to do automatic annotation, leveraging LLMs and some heuristics\. 
- These parts corresponding to this quote from o1 that says:
	- Through RL, o1 learns to hone its chain of thought and refine strategies it uses\. It learns to recognize and correct its mistakes\. It learns to break down tricky steps into simpler ways\. It learns to try a different approach when the current one isn't working\. This process dramatically improves the model’s ability to reason\.
- OpenAI’s method for collecting high\-quality fine\-grained data for step\-wise supervision involves a GPT\-4 model that undergoes some maths training to warm up as well as some format following training\.
	- The model is used to sample reasoning trajectories on some maths questions, and a human expert provides annotations, labelling every reasoning step generated by the language models as positive, neutral or negative\. These annotations are then used to train the PRM\. 
	- This trained process reward model is evaluated using a best\-of\-N paradigm, where a generator model is used to sample N outputs, and the chosen answer is the one with the highest score\. 
		- The score for a given step is the probability of the step being a positive one, where the scores for every step is then multiplied to give the overall score\. 
- OpenAI’s approach to collect human\-annotated step\-wise annotation is relatively expensive and the Math\-Shepherd paper presents a way to utilise some heuristics for automatic data collection\. 
	- Again, given some mathematical questions, starting at some intermediate step, roll out k steps ahead and see whether some of them can reach the good answer\. 
	- And the annotations can be done in 2 ways\. In the softer score, the proportion of obtaining correct answers among all the roll outs is computed

## Key Claims

1. Chain of Thought prompting improves language model reasoning by having the model generate step-by-step rationales before producing a final answer, yielding more correct responses than standard prompti
2. Chain of Thought prompting extends the expressivity of Transformers by adding recurrence-like computation, enabling them to solve inherently serial problems beyond the capability of vanilla Transforme
3. Transformers equipped with Chain of Thought can evaluate arithmetic expressions, simulate automata, and compose permutations, thereby gaining extended capability for evaluating code and mathematical r
4. Even Transformers equipped with Chain of Thought cannot solve graph connectivity problems, linear programming or linear equality problems, context-free recognition, or primality testing.
5. STaR bootstraps chain-of-thought training data by pseudo-labeling model-generated rationales as correct when the final answer is correct, and by reprompting with the ground-truth answer to elicit impr
6. Supervising only on final outcomes is insufficient to teach reliable chain-of-thought reasoning because non-informative rationales can still improve performance, showing that outcome reward alone does
7. Process Reward Models provide fine-grained stepwise supervision at every reasoning step rather than only at the final outcome, enabling more reliable and rigorous step-by-step reasoning.
8. OpenAI collected human-annotated stepwise supervision data using a 3-way classification interface: positive (step is correct and reasonable), neutral (step is potentially subtly misleading), and negat
9. In best-of-N evaluation with a Process Reward Model, PRM scoring outperforms both outcome reward model scoring and majority voting, with performance continuing to improve as more solutions are sampled
10. Math-Shepherd enables automatic stepwise annotation without human labelers by rolling out multiple completions from each intermediate reasoning step and using the proportion of correct final answers a

## Capabilities

- Language models can generate step-by-step reasoning explanations before providing final answers, improving performance on complex reasoning tasks
- Process reward models evaluate individual reasoning steps rather than just final outcomes, enabling more reliable step-by-step reasoning supervision and training
- Test-time compute scaling: models can achieve better performance by allocating more computational resources at inference time through longer reasoning chains, best-of-N sampling, and search algorithms
- Language models can be trained through reinforcement learning to recognize and correct their own mistakes through self-reflection and iterative refinement
- Automatic annotation for process reward models via leave-one-out supervision enables cost-effective collection of step-level training data without expensive human annotation
- Models can learn to perform backtracking and search algorithms (tree search, beam search, A* search) as part of their reasoning by linearizing search trees into token sequences and training via next-token prediction
- Pure reinforcement learning without any supervised fine-tuning phase can induce emergent sophisticated reasoning behaviors in large language models
- Open-source reproductions of o1-style test-time reasoning models (QwQ-32B, Skywork-o1) achieve performance parity with or exceeding closed-source frontier models

## Limitations

- Language models cannot perform reliable self-reflection and self-correction without external feedback; they require verifier feedback, compiler feedback, or calculator support
- Standard reinforcement learning training causes models to learn only small superficial edits rather than substantial improvements, resulting in slow or no progress toward correct solutions (behavior collapse)
- Distribution shift: mistakes encountered during deployment may differ significantly from those in training data, making supervised fine-tuning insufficient for robust self-correction
- Best-of-N sampling for test-time scaling incurs significant computational overhead; beam search offers better performance-to-cost tradeoff but search and lookahead methods are prohibitively expensive
- Human annotation for process reward models is expensive and labor-intensive, limiting scalability of step-wise reasoning supervision
- Transformers lack expressivity to solve inherently sequential problems even with chain-of-thought: cannot reliably solve graph connectivity checks, linear programming, linear equalities, context-free language recognition, or primality testing
- Noninformative or random rationales can improve chain-of-thought performance when labeled as reasoning, suggesting the capability may lack true robustness and may not require genuine understanding
- Models universally apply long chain-of-thought reasoning to all queries regardless of difficulty, creating unnecessary inference overhead and inefficiency on simple problems
- Automatic annotation for process reward models still requires golden (correct) final answers for all training problems, constraining scalability to problems where ground truth is verifiable

## Bottlenecks

- Unreliability of inference-time self-correction without verifiers: models cannot perform robust self-reflection and correction without external verification signals, but reliable verifiers don't exist for many open-ended task domains
- Data scarcity for high-quality training of reasoning models: collecting sufficient high-quality ground-truth annotated reasoning trajectories is expensive and limits scaling of reasoning model training
- Structural limitations of standard RL formulations: traditional RL training for reasoning suffers from behavior collapse, distribution shift, and insufficient incentive structure for substantial iterative improvements
- Expressivity limitations of standard Transformers: vanilla Transformers lack computational capacity to solve inherently sequential problems (graph connectivity, linear programming, context-free languages, primality) even with chain-of-thought
- Computational cost of inference-time scaling: extending test-time compute through longer reasoning chains, search, and sampling incurs significant overhead; practical tradeoffs between compute budget and performance gains are still being explored

## Breakthroughs

- Test-time compute scaling as a primary scaling lever: inference-time computation can be scaled independently from training to improve reasoning performance on complex tasks, establishing test-time compute as a fundamental scaling dimension previously overlooked
- Process reward models enable fine-grained supervision for reasoning: process reward models that evaluate individual reasoning steps rather than just final outcomes enable much more efficient and reliable training of models to perform step-by-step reasoning
- Automatic annotation via leave-one-out supervision: process reward models can be trained using automatic annotations derived from leave-one-out supervision and rollout-based scoring without expensive human expert annotation
- Learned backtracking and search in language models: language models can be taught to perform backtracking and sophisticated search procedures (tree search, beam search, A* search) as part of their reasoning through token-based linearization of search structures
- Open-source parity with frontier reasoning models: open-source community implementations achieve performance parity with or exceeding closed-source frontier models, democratizing access to advanced reasoning capabilities

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/chain-of-thought-prompting|Chain of Thought Prompting]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/prm800k|PRM800K]]
- [[entities/qwq-32b-preview|QwQ 32B Preview]]
- [[entities/reflexion|Reflexion]]
- [[entities/score|SCoRe]]
- [[entities/star|STaR]]
- [[entities/test-time-compute|test-time compute]]
