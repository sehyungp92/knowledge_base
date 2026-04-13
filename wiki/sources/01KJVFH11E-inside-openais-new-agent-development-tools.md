---
type: source
title: Inside OpenAI's New Agent Development Tools
source_id: 01KJVFH11EDGK6MD0FNRCGC572
source_type: video
authors: []
published_at: '2025-03-25 00:00:00'
theme_ids:
- agent_systems
- computer_use_and_gui_agents
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Inside OpenAI's New Agent Development Tools

**Authors:** 
**Published:** 2025-03-25 00:00:00
**Type:** video

## Analysis

OpenAI’s Vision for Consumer Interaction

- The most exciting thing about releasing models and APIs that are underlying these agentic products is that we are going to see them in more and more products across the web\. So Computer Use coming to a browser that you like to use or Operator automating a task that you do day to day at work and doing all the clicking and filling out forms and other research on your behalf\. 
	- It's just going to become more and more deeply embedded into products that you use day to day\. 
- One of the interesting things about working on the API platform is that you don't actually know what people are going to want to build\. 
	- In the API, users know their domains much better than the model providers, and so it will be interesting to see how these products and these model capabilities make their way into verticals\. 
- <a id="_Hlk195306545"></a>With regards to agents communicating or getting information from the web, there has already been a big change\. 
	- In 2024, an agent would do a single turn, decide whether it wants to search the web or not, get information from the web and synthesise a response\. 
	- In 2025, it is already about products like deep research where the model is getting information from the web, thinking about what it has got, reconsidering its stance, getting something else from the web, opening multiple web pages in parallel to try to save time etc\. 
		- This whole CoT and calling tools in the reasoning process is a significant shift in terms of how agents access information from the web\. 
		- It is all going to be seamlessly embedded in this CoT process where tool calling is just happening between the internet, your private data and your private agents\. 
- People are looking to create these multi\-agent systems to solve these business problems\. 
	- If you look at like a customer support automation problem, you have one agent that's looking after your refunds, another that's looking after billing and shipping information, something else that makes a decision on pulling the FAQ or escalating to a human\. 
	- Agents SDK makes it much easier for developers to build on multi\-agent architectures\. And it is going to be interesting when you start exposing these agents to the public internet for someone else to communicate with them, which will happen perhaps in the coming months\. 
- Previously, most of the data that a model sees is either your own data, chat history, or file search\. However, especially with these tools that are much more connected to the web, we'll see a lot more data going into the model that's actually from around the web and not just data that the users are providing\. 

Challenges and Innovations in AI Finetuning

- Taking a step back, <a id="_Hlk195315176"></a>what most agentic products looked like in 2024 was a very clearly defined workflow with less than 10 tools, very well\-orchestrated to go from A to B to C\.
	- This is how a lot of companies built a bunch of cool coding agents, customer support automation projects, deep research projects, etc\. 
- In 2025, we've gone to this model where everything is happening within this CoT, moving away from the whole deterministic workflow building process\. 
	- The model is smart enough to figure out in its reasoning process how it should call multiple tools, and also figure out that it's going down the wrong path, take a U\-turn and then try something else\. 
		- <a id="_Hlk195319976"></a>OpenAI has been working on tools like reinforcement finetuning to make this something that developers can use themselves\. 
	- Last year you had to put such specific guardrails and chain things so closely together because you couldn't let things go off the rails\. Now you're even more flexible in what you can allow, and then the dream going forward will involve providing hundreds of tools that the model can figure out how to use for every task\. 
- The next step after this is going to be getting rid of that 10\-15 tool constraint, exposing it to hundreds of tools, have it figure out which is the right one to call and make use of those tools\. That may be the next unlock, where the agent has all the superpower it needs, i\.e\., the compute, the way of reasoning about different tool trajectories and access to a lot of tools\. 
	- Removing the number of tools constraint is hard to make that work with today's models, but that may soon change\. 
- Also it may be important to just increase the available runtime that these models have to go off and do what they need to do\. 
	- If you're a human, you can go off and work on something for a day and use as many tools as you need to get the job done\. Now we've seen <a id="_Hlk195319376"></a>runtimes that for models that are in the minutes \(e\.g\., deep research\), but being able to get these things to go into the hours and into the days is going to yield some powerful results\. 
- It will be interesting to see how the next generation of models generalise to all of the use cases that developers are going to have\. 
- <a id="_Hlk195319440"></a>There is also reinforcement finetuning technique where you are creating these tasks and graders\. And it would be amazing if developers can create their own tasks and graders, and get the model to find the right tool calling path for solving a particular problem that is unique to that domain\. 
	- You are actually steering the model in its CoT, and teaching it how to think about your domain, potentially training a model to be like a legal scholar or a medical doctor, training the way that it thinks in the same way that 4 years of university would train you to think in a specific way\. 
		- Reinforcement finetuning may potentially enable interesting verticalisation of these models\. 
- Providing the right level of tooling at the infrastructure level in to finetune for domains like legal or healthcare is still a work in progress\. 
	- Right now, OpenAI gives developers the basic building blocks to build thei

## Key Claims

1. In 2024, most agentic products consisted of clearly defined workflows with fewer than 12 tools and deterministic step-by-step orchestration.
2. By 2025, agents moved away from deterministic workflow building toward chain-of-thought tool calling where the model reasons about tool use, self-corrects, and backtracks autonomously.
3. The next major unlock for agents is removing the 10-15 tool constraint so agents can access hundreds of tools and select the appropriate one dynamically.
4. Current agent runtimes for products like Deep Research are in the minutes range, but extending them to hours and days is expected to yield significantly more powerful results.
5. Multi-agent architectures for customer support automation typically decompose into specialized agents handling refunds, billing/shipping, FAQ retrieval, and human escalation decisions.
6. OpenAI released the Agents SDK to support multi-agent swarm architectures because developers were already building them to solve business problems.
7. Splitting tasks across multiple specialized agents reduces the blast radius of prompt changes and makes debugging significantly easier compared to prompting a single agent with many instructions.
8. Computer use models work best in browser environments because that is primarily what they were trained on.
9. Computer use is well-suited for legacy applications without APIs, particularly for automating manual multi-application workflows in domains like healthcare.
10. Computer use agents are being used for visual geospatial research tasks, such as navigating Google Maps Street View to verify real-world changes like EV charging network expansion.

## Capabilities

- Chain-of-thought tool calling enables models to reason through multi-step problems, dynamically selecting tools mid-reasoning, reconsidering decisions, and taking alternate paths without pre-defined workflows
- Multi-agent systems with specialized agents can be coordinated to solve complex tasks, with each agent focused on a single subtask and delegating appropriately
- Computer use agents can autonomously interact with graphical interfaces across diverse applications by perceiving screenshots and controlling mouse/keyboard to automate legacy systems and non-API-accessible workflows
- Reinforcement fine-tuning allows developers to create domain-specific task definitions and graders to steer model reasoning toward specialized problem-solving approaches without full retraining
- Agents SDK enables developers to build and orchestrate multi-agent systems with clear task separation, simpler debugging, and isolated prompt engineering per agent

## Limitations

- Computer use models are primarily trained on browser environments and degrade significantly when applied to non-browser interfaces like iOS and Android screens
- Models struggle to reliably handle tool selection and invocation when exposed to more than ~10-15 tools; scalability to hundreds of tools is unsolved
- Long-horizon autonomous task execution is constrained to minutes of reasoning/runtime; scaling to hours or days is not yet achievable with current models
- Models lack precise control over structured output generation, particularly for generating code diffs with correct line numbers that can be applied cleanly to source files
- Task grading and evaluation framework generation for domain-specific fine-tuning is unsolved; no productized solution exists that works across domains without heavy customization
- Models cannot reliably handle open-ended task decomposition without explicit workflow scaffolding; operator complexity scales with manual orchestration effort rather than model capability
- Integration complexity dominates agent deployment effort; acquiring programmatic access to internal tools and APIs requires 90% of implementation work, leaving only 10% for LLM logic
- Model instruction following on complex multi-tool reasoning tasks remains unreliable without task-specific fine-tuning; zero-shot generalization does not hold across domains

## Bottlenecks

- Task grading and evaluation framework is the critical missing piece for productizing domain-specific fine-tuning; no standard approach exists for building graders that capture domain-specific correctness across legal, medical, scientific, and technical domains
- Scaling agentic tool use to hundreds of tools is algorithmically unsolved; current models plateau in reliability above ~10-15 tools, requiring developers to either constrain tool sets or fallback to deterministic orchestration
- Long-horizon task execution is constrained by context and runtime limits; models can sustain reasoning for minutes, not hours/days, preventing multi-hour autonomous work
- Computer use environment fragmentation: models are optimized for web browsers but degrade on mobile OS interfaces, creating demand for environment-specific implementations (iOS VMs, Android containers) that don't yet exist at scale
- Structured output generation precision for code patches is insufficient; models cannot reliably generate diffs with correct line numbers, breaking automated code application workflows
- MCP ecosystem and tools registry standardization is incomplete; unclear how to integrate MCP with broader tool discovery, governance, and reliability systems

## Breakthroughs

- Reasoning models integrated with tool calling in the inference chain enables dynamic multi-step task planning without pre-defined workflows; models can call multiple tools, evaluate results, reconsider decisions, and take alternate paths within a single reasoning trace
- Computer use agents achieve practical automation of legacy systems and non-API-accessible workflows through GUI interaction; agents perceive screen state via screenshots and control applications through mouse/keyboard events
- Multi-agent specialization paradigm: splitting complex tasks across multiple specialized agents (each handling one subtask) improves reliability, debuggability, and task success compared to monolithic single-agent systems
- Reinforcement fine-tuning enables domain-specific agent reasoning patterns through task and grader definition; models can be steered to think like legal scholars, medical doctors, or domain experts without full retraining

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/startup_formation_and_gtm|startup_formation_and_gtm]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/deep-research|Deep Research]]
- [[entities/multi-agent-architecture|Multi-Agent Architecture]]
- [[entities/operator|Operator]]
- [[entities/reinforcement-fine-tuning|Reinforcement Fine-Tuning]]
