---
type: source
title: Expert AI Researcher Reacts to o1 and Shares What's Next in Reasoning and Post-Training
source_id: 01KJVJPTJY48JVQAX88MX39NQS
source_type: video
authors: []
published_at: '2024-09-18 00:00:00'
theme_ids:
- ai_business_and_economics
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Expert AI Researcher Reacts to o1 and Shares What's Next in Reasoning and Post-Training

**Authors:** 
**Published:** 2024-09-18 00:00:00
**Type:** video

## Analysis

Exploring the Impact of Systems Thinking in AI  

- <a id="_Hlk181803555"></a>The release of the latest o1 model is exciting\. It is a sign of the OpenAI going in the direction of thinking about systems rather than models\. Essentially o1 is compressing a lot of the chain of thought ideas into the model using RLHF, ideas which have been around for a while, and turning that model into a more complicated system\. It's encouraging to see that this works so well for reasoning specifically\.
	- It is possible that some of the ideas that are in o1 were already in other models, without making it explicit, so the idea may not be super new, but as usual with OpenAI, you have to give them credit for how they execute it on it\. 
	- Contextual has been working on similar ideas, but on the retrieval side, so how to compress a lot of this system level thinking into models, or at least make sure to address the entire system\. 
- <a id="_Hlk181803042"></a>We should not necessarily expect most future models to follow this approach, especially when it comes to deployment with the impact on latency\. 
	- Latency will go up when you have to do a lot of thinking during test time, so it's not always the best thing to do\. There are different trade\-offs that has to be made when it comes to AI deployment\. 
- It will be interesting to see what UIs are built around the fact that you might have to wait, especially if you have very long context and there's a lot of complicated reasoning that has to be done, which will increase the thinking time as is the case for humans\. 

Overview of Contextual AI

- Contextual was started because of the frustration in enterprises where everybody was super excited about GenAI, but at the same time, it just wasn't ready for prime time, especially in enterprises\. 
	- Having come up with RAG, knew that it would be one of the solutions to a lot of these problems, but also knew that it would be possible to do much better than RAG\. 
		- RAG was an old idea and the original vision was actually much more ambitious than what ended up in the paper\. And so Contextual was founded with that more ambitious vision\. 
		- The company’s mission is to change the way the world works through AI and believes work is the most obvious place where this technology is going to have a major impact\.
- Believes that they are different from the likes of OpenAI or Anthropic on 2 core principles:
	- <a id="_Hlk181803571"></a>One is the emphasis on systems over models\. A model should represent ~10\-20% of a much larger system tasked with solving the problem\. And what an enterprise wants to acquire is the system rather than the model\. 
		- It is encouraging that OpenAI is also thinking about systems, but they are still looking to compress all of that into a model\.
	- <a id="_Hlk181803856"></a>The other thing is not having AGI as the goal\. AGI is a great idea, but it is fundamentally a consumer product\. Given that you do not know what the consumer really wants, generalist intelligence is needed to satisfy their needs\. In contrast, an enterprise often knows exactly what it wants and so you often do not want it to be a generalist, but specialised for a particular use case\. The right way to think about enterprise AI may be through specialisation, rather than generalisation\. 
		- For instance, for regulated industries like banks, at deployment a generalist AI may need to be constrained back again\. <a id="_Hlk177600832"></a>
- <a id="_Hlk181803967"></a>When you have an integrated systems approach with specialisation components, it is possible to say all the parts together have been end\-to\-end specialised\. 
	- The company specifically focuses on high\-value knowledge\-intensive use cases where it is worth being extra integrated and extra specialised\. 
- There is a lot of common ground between customers, and it’s all the same system:
	- You need to extract information from the data at very large scale and not fail\.
	- Then you need to put that in some retrieval mechanism, and it's not just one retriever anymore, in modern deployment, a mixture of retrievers approach is used\.
	- Then based on top of that, you contextualise the language model with that information\. Then you do a lot of things on top of the language model\. 
		- There's still a lot to gain from making the components themselves more specialised and then tuning the knobs to make everything more optimal\. 
- On the enterprise side, providing an end\-to\-end solution is one of the Contextual’s strengths, but it has also been challenging\. There's a lot of things that needs to happen to build a generalisable system\. 
	- For instance, had hoped to use off\-the\-shelf extraction systems\. Most language models are good as long as you give them the right context, which in turn requires the right retrieval and things like re\-ranking, and the retrieval can only be done properly if the extraction is done correctly\. 
		- It turns out that extracting information from a PDF is very hard, and there just isn't anything good out there in the open\. 
	- On the other end, <a id="_Hlk181804305"></a>evaluation and understanding the risk of the deployment and the real accuracy of the system is hugely important, especially for enterprises\. But there still isn't a set way to evaluate systems that enterprises can rely on\. That remains a very underexplored area\. 
		- People have claimed that part of building a good product is specifying upfront what you want it to do, which implies creating your own bespoke evaluation set\. At the same time, there are plenty of companies trying to productise this\. 
		- One of the real problems is that a lot of people don't understand what they want\. So arguably one of the ways to do this is engaging with the customers to figure out what success looks like, and hill climb together to achieve that success in a prototype setting, and then productionise it\. 
		- Some people are still not taking evaluation seriously enough 

## Key Claims

1. OpenAI's o1 model compresses Chain of Thought reasoning into a model using reinforcement learning, turning the model into a more complex system.
2. Test-time compute increases latency, making it unsuitable for all deployment scenarios.
3. o1 is much more powerful on math and law benchmarks, but older models do better on other tasks and are significantly faster.
4. Future models may require hours of wait time for responses when handling complex reasoning with very long context.
5. The model is only approximately 10–20% of the full system required to solve enterprise AI problems; the surrounding system is far more important.
6. Enterprise AI deployments benefit from specialization rather than general-purpose intelligence.
7. Directly exposing high-value AI use cases to end customers is risky; keeping humans in the loop is the safer approach.
8. RLHF was the secret sauce that made ChatGPT work by capturing human preferences at the full sequence level rather than the next-token level.
9. RLHF has two major problems: the cost of training and discarding a reward model, and the need for slow and expensive preference data annotation.
10. DPO eliminates the dependency on a separate reward model for alignment, making the process more efficient.

## Capabilities

- o1-style test-time reasoning models achieve frontier performance on mathematical and logical reasoning through compressed chain-of-thought reasoning via RLHF
- Direct preference learning from deployment feedback without separate reward models using DPO, KTO, CLAIR, and APO methods
- Contrastive revision pairs (CLAIR) enable preference data to capture causal structure of improvements rather than unstructured ranking
- Anchored Preference Optimization (APO) learns from preference data while accounting for the quality relationship between the model being trained and the data it learns from
- Mixture of retrievers approach combining multiple different retrieval mechanisms instead of single vector database
- End-to-end integrated system for enterprise AI combining extraction, retrieval, language model, and verification
- Specialized enterprise AI models outperform generalist models by focusing on domain-specific tasks without irrelevant capabilities

## Limitations

- Test-time reasoning models have significant latency costs; reasoning quality-latency tradeoff prevents broad real-time deployment
- Direct exposure of AI outputs to customers is unsafe for high-stakes use cases; safety risk increases with business value
- Standard RLHF requires training expensive, high-quality reward models that are discarded after training
- RLHF requires manual preference data annotation which is slow, expensive, and becomes prohibitively costly for specialized use cases
- Preference ranking data does not capture causal structure of why one output is better, resulting in underspecified training signals
- Model quality can exceed preference data quality, causing models to learn incorrect signals from training data that is worse than their own current capability
- PDF extraction (OCR, layout detection, metadata extraction) remains unsolved; no open-source systems provide reliable document information extraction
- Enterprise AI system evaluation lacks standardized methods; most enterprises use ad-hoc spreadsheets with 50 examples and high variance
- High-stakes decision-making tasks (investment decisions, hiring, performance reviews) cannot be automated; companies dramatically underestimate the complexity and risk
- Transformer architecture success stems from GPU hardware optimization compatibility, not fundamental algorithmic superiority; reveals path-dependency in architecture adoption
- Enterprise underestimates AI system integration complexity; companies expect plug-and-play deployment but require end-to-end system engineering across extraction, retrieval, model, and verification
- High-end research clusters have severe reliability issues; hardware failures and GPU failures require frequent swaps and repair cycles
- Synthetic data quality depends on base model capability; weak models generate weak data, creating a capability ceiling that depends on upstream model improvements
- Generalist models are inefficient for enterprise use; requiring fine-grained constraint engineering to comply with regulations and use-case-specific requirements
- Engineering and systems contributions (e.g., chain-of-thought prompting) were historically undervalued by ML academic community as not representing 'real' algorithmic contributions

## Bottlenecks

- Preference data collection is expensive and slow at scale; manual annotation of preference pairs blocks rapid RL iteration for specialized enterprise use cases
- Model quality can exceed training data quality, causing standard preference optimization methods (RLHF, DPO, KTO) to learn from suboptimal examples rather than improving
- No standardized enterprise evaluation framework exists; companies cannot reliably assess production AI system safety, accuracy, or regulatory compliance
- Direct AI output exposure to customers is unsafe for any economically material decision; safety and reliability barriers prevent autonomous decision-making in high-stakes domains

## Breakthroughs

- Direct preference optimization from feedback without separate reward models (DPO/KTO) eliminates expensive reward model training and enables real-time learning from production feedback
- CLAIR (contrastive revision pairs) captures causal structure of improvements, enabling preference data to encode 'why' one output is better rather than unstructured ranking
- APO (Anchored Preference Optimization) learns from preferences while accounting for the quality relationship between model and training data, preventing learning from suboptimal examples
- Systems-first architecture for enterprise AI treating integrated extraction, retrieval, language model, and verification as single optimization target rather than pluggable components

## Themes

- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/post-training|Post-training]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/multi-agent-systems|multi-agent systems]]
