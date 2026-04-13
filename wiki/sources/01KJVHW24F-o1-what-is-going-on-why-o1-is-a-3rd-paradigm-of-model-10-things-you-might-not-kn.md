---
type: source
title: o1 - What is Going On? Why o1 is a 3rd Paradigm of Model + 10 Things You Might
  Not Know
source_id: 01KJVHW24FPVBK88X2RSRAMY6V
source_type: video
authors: []
published_at: '2024-09-18 00:00:00'
theme_ids:
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# o1 - What is Going On? Why o1 is a 3rd Paradigm of Model + 10 Things You Might Not Know

**Authors:** 
**Published:** 2024-09-18 00:00:00
**Type:** video

## Analysis

How o1 Works

- The foundational original objective of language models is to model language and to predict the next word\. This was the first paradigm, which in itself if interesting but not overly useful\. So another objective was brought in for the second paradigm\. We wanted models to be honest, <a id="_Hlk188985268"></a>harmless and helpful, so a reward would be given to the model when it produced outputs that met those objectives – enter ChatGPT\. 
- o1 represents the third paradigm, where we want to reward answers that <a id="_Hlk188985415"></a>are objectively correct\. The original objectives have not been forgotten but another one has been layered on top\. 
- When it comes to training a model for reasoning, one thing that immediately jumps to mind is have humans write out their thought process and train on that\. However, feeding the model thousands of examples of human step\-by\-step reasoning is not really optimal as it does not scale well\. 
- However, if the model is trained using RL to generate and hone its own chain of thoughts, it would represent a scalable way of exploring models reasoning that could work even better than having humans write chains of thought for it\.
- If the temperature of the model is set to 1 so that it gets creative generates lots of diverse chains of thought, then some of those outputs are going to be good, especially with more time spent thinking longer chains of thought\. 
	- If there is a way of automatically grading those outputs, it doesn't matter how low a proportion of the outputs are correct as long as there at least one or a few correct ones\. 
	- Then only the outputs that produce the correct answer in mathematics, science, coding with correct reasoning steps can be taken to finetune the model\. 
		- As only the correct outputs with correct reasoning steps are being used for finetuning or further training, this reinforcement learning process can be highly data efficient\.
- This can be seen as a marriage of train time compute \(i\.e\., the finetuning or training of a model\), and test time compute \(i\.e\., when the model is actually outputting something\)\. 
	- We already knew that giving the models the time to produce serial calculations one after another before producing their final output boost results, especially in technical domains\. But then marry that with train time compute, training on those correct generations results in the two scaling graphs in the OpenAI blog, where neither graph looks like they are levelling off\.
		- For the mathematics competition, more time to think equals better results, but then train or finetune the model or generator on correct outputs and reasoning steps, that also produces a noticeable increase\. 
- Given that the chains of thoughts are the key ingredient to the model’s success, the chains of thought that led to the output are hidden when using o1\.
	- OpenAI admits that part of the reason for that is their own competitive advantage, since rival labs could train using the successful chains of thought that were outputted by the o1 series\. 
- In summary, o1 represents a paradigm shift from memorising the answers to memorising the reasoning\. Given that it was trained on the reasoning steps that ended up leading to a correct answer, it is starting to get better at recognising which kinds of reasoning lead to correct answers in which domain\. 
	- But again if those reasoning steps or facts are not in the training data, it will still fail\. o1 is still not a departure from the broader paradigm of fitting a curve to a distribution to boost performance by making everything in\-distribution\. New ideas may still be needed for AGI\. 
	- Another way of putting this is that there does not exist a foundation model for the physical world\. There still isn’t a huge dataset of correct answers for real world tasks\. 

Is This Reasoning?

- A broader question to all of this may be whether this is reasoning and whether it counts as human\-like intelligence\. The answer is that it definitely is not human\-like, but it might not ultimately matter\. 
- A useful analogy may be to think of it as a librarian who you go up to because you have a question you want answered\. The library books represent the model's training data and the original ChatGPT was a very friendly librarian but it would often bring you the wrong book, or maybe it would bring you the right book that could answer your question but point to the wrong paragraph within that book\. 
	- ChatGPT was decent as a librarian, but had no idea what it was handing to you\. It was pretty easy if you wanted to demonstrate that it wasn't actually intelligent\. 
	- The o1 series of models are much better librarians\. They've been taking notes on what books successfully answered the questions and which ones didn't, down to the level not just of the book but the chapter, the paragraph and the line\. 
- There is still the question of whether or not the librarian actually understands what it’s presenting, but this may not ultimately matter, especially when we do not even understand how the human brain works\. 
- <a id="_Hlk184120345"></a>With the chains of thought, the models are clearly much more capable at serial calculations\. The ability to break down long or confusing questions into a series of small computational steps is why o1 preview is more likely to get the more complicated reasoning questions correct\. 
	- As always, it's worth remembering that exam style knowledge benchmarks in particular, rather than true reasoning benchmarks, does not equal real world capabilities\. 
- <a id="_Hlk184120347"></a>However, if you ask a question about something that's not in the model's training data, then the librarian will still screw up and is unlikely to say it does not know and instead will bring an irrelevant book\. That weakness is still present in o1 preview\. 
- <a id="_Hlk184120351"></a>Also, for domains that have plenty of training data but no clearly correct or inco

## Key Claims

1. Training a model using RL to generate its own chains of thought produces better results than training on human-written chains of thought.
2. High-temperature sampling (temperature=1) is used during training to generate diverse chains of thought as candidates for fine-tuning.
3. Only chains of thought that produce correct answers are used to fine-tune the model, making the process highly data-efficient.
4. O1 represents a marriage of test-time compute (thinking time at inference) and train-time compute (fine-tuning on correct generations), both of which independently scale performance.
5. Both test-time compute scaling and train-time compute scaling graphs for difficult mathematics competition problems do not appear to be leveling off.
6. O1's internal chains of thought are hidden from users, partly for competitive advantage, as rival labs could train on successful chains of thought.
7. O1 shows large performance boosts over GPT-4o in domains with objectively correct or incorrect answers, but shows regression in domains like personal writing.
8. O1 represents a paradigm shift from 'memorize the answers' to 'memorize the reasoning', learning which types of reasoning steps lead to correct answers.
9. Process reward models that verify individual reasoning steps produce more dramatic results than outcome-based reward models that only evaluate final answers.
10. Process reward models can identify correct solutions even when the generator (GPT-4) only produced the correct solution one time in a thousand.

## Capabilities

- o1 achieves substantially improved performance on mathematical, scientific, and coding reasoning tasks compared to GPT-4, through extended test-time compute via chain-of-thought reasoning
- Models can decompose complex multi-step reasoning problems into serial computational steps, breaking down confusing questions into manageable parts
- Reinforcement learning on model-generated chains of thought produces better reasoning performance than training on human-written chain-of-thought examples
- Process reward models can verify and score intermediate reasoning steps (not just final answers) in mathematical and scientific reasoning, enabling fine-tuning on high-quality reasoning paths
- Process reward models trained on mathematical domains generalize to evaluate reasoning in other technical domains (chemistry, physics) without retraining
- Combining test-time compute (longer inference-time reasoning) with train-time compute (RL fine-tuning on correct reasoning) shows continued performance scaling without plateau
- Models can learn to recognize which reasoning patterns and step sequences lead to correct answers, independent of explicit memorization of facts
- Models can learn to generate chains of thought in non-human-interpretable formats (translated languages, synthesized notation) while still solving problems correctly

## Limitations

- o1 reasoning capabilities are restricted to domains with verifiable correct/incorrect answers; performance regresses or stagnates in domains with ambiguous or open-ended correctness (personal writing, creative tasks)
- o1 fails when required reasoning steps or facts are absent from its training data; cannot retrieve information from a non-existent knowledge library regardless of reasoning capability
- o1 continues to exhibit persistent hallucination and refuses to admit uncertainty; will confidently present irrelevant information rather than acknowledging lack of knowledge
- Domains with abundant training data but no clearly correct/incorrect ground truth cannot leverage process reward model training; no automatic way to sift and score reasoning chains
- Process reward model training requires high-temperature sampling for diversity but temperature cannot be adjusted in o1 API, limiting user control over reasoning-exploration trade-off
- Spatial reasoning and physical world understanding remain significant weaknesses; o1 cannot solve problems requiring detailed spatial or physical intuition
- No amount of prompt engineering (chain-of-thought prompting) on base GPT-4 can match o1's reasoning performance; the training paradigm shift cannot be replicated via inference-time techniques alone
- Automated reward models for step-by-step verification cannot perfectly distinguish correct vs incorrect reasoning paths; false positives occur where models reach correct answers via flawed reasoning
- Reinforcement learning on reasoning generates creative solutions that are sometimes unpredictable and difficult to interpret, posing safety challenges in long-horizon or real-world settings

## Bottlenecks

- Absence of ground-truth verifiable answers for real-world tasks blocks scaling of process reward model training; cannot automatically sift correct reasoning chains for fine-tuning when correctness is ambiguous or unmeasurable
- Open-ended domains without clearly defined correctness criteria cannot leverage automated verification; reward models cannot be trained or applied where no ground truth exists (writing, creative tasks, subjective reasoning)
- Reinforcement learning on long-horizon reasoning in real-world settings produces unpredictable creative solutions that may violate intended objectives; current approaches lack mechanisms to constrain creative exploration toward safe outcomes
- Foundation model for physical world does not exist; lack of learned world model blocks spatial reasoning, physical intuition, and real-world task decomposition even with improved reasoning architectures

## Breakthroughs

- Marrying test-time compute (extended inference-time reasoning chains) with train-time compute (RL fine-tuning on correct reasoning paths) creates a paradigm shift enabling systematic reasoning scaling across quantitative domains
- Process reward models trained to verify intermediate reasoning steps (not just final answers) enable higher-precision training signals and generate significant performance improvements over outcome-only rewards
- Model-generated chains of thought via reinforcement learning outperform human-written chain-of-thought examples, enabling scalable self-generated reasoning data without human annotation bottleneck
- Models learn to generate novel reasoning patterns (potentially illegible to humans, in translated languages or synthesized notation) while solving hard problems correctly, paralleling Stockfish's transition from handcrafted evaluation to learned reasoning
- Test-time compute scaling in reasoning shows continued improvement trajectory without evidence of plateau, suggesting compute-optimal inference can scale indefinitely within verification bounds

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/chain-of-thought-cot|Chain of Thought (CoT)]]
- [[entities/expert-iteration|Expert Iteration]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/outcome-reward-model-orm|Outcome Reward Model (ORM)]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/reinforcement-learning-for-reasoning|Reinforcement Learning for Reasoning]]
- [[entities/self-taught-reasoner-star|Self-Taught Reasoner (STaR)]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
