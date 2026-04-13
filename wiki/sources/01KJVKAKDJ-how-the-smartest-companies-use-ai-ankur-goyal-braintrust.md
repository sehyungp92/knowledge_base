---
type: source
title: How the Smartest Companies Use AI | Ankur Goyal, Braintrust
source_id: 01KJVKAKDJCQKZ7MT9P788V9NE
source_type: video
authors: []
published_at: '2024-06-07 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- frontier_lab_competition
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How the Smartest Companies Use AI | Ankur Goyal, Braintrust

**Authors:** 
**Published:** 2024-06-07 00:00:00
**Type:** video

## Analysis

https://www.youtube.com/watch?v=9oKmZ2Oa-M0&t=1802s

Evaluations

- At the moment, every company, whether they are a software company or just have software in their company, is trying to figure out how their products, internal processes, core business change with AI. At every company, there's a group of product managers, engineers, designers getting together, prototyping things, shipping things into production. 
- And the way that people build software is changing right in front of our eyes. To an extent, it comes down to using evals as the core primitive around which to build AI software. 
	- If you engineer a good system for evals that allows you try out new ideas, incorporate user feedback, immediately take action when something go wrong with an AI in production and make sure it doesn't happen again, the velocity keeps on growing. 
- There are a variety of different things that can go wrong with AI because the technology is inherently non-deterministic. For instance, in the context of an agent, this could involve using the wrong tool, or in the space of data analysis, generating the wrong SQL query. And at times a marginal improvement in model performance may equate to gains for some use cases and losses for others. 
	- Evals can help to address these issues. 
- Evaluation describes a workflow and methodology around gathering test data that represents what you expect to happen with an AI system and then testing your AI system against the test data. 
	- In some ways, it is similar to unit testing or continuous integration with traditional software. The difference is that evals are never perfect. And so you can't just have 100% green or 100% red result with an eval. More detailed analysis is needed every time an eval is run to really understand what is happening and what the potential issues are. 
- Evals are not a new idea. What's challenging and interesting now is that the core persona driving a lot of the AI innovation is not just the ML scientist or a data scientist anymore, but a lot of product engineers are building really exciting things with AI. And evals are a very new idea for product engineers. 
	- Braintrust makes it easy for any engineer to get started with evals and immediately set up good developer loop to build good software. 
- Before the likes of Braintrust, most people would rely on vibe checks, which just involves seeking opinions to see if a group consensus can be reached about whether or not it is better. 
	- If you're just starting and prototyping something, that is the only thing you can do. And so that should be the step 0, but it should not be step 1 or 2 onwards. As soon as you pass the vibe check, you should immediately get your idea, feature or app out in front of some users to generate data as people are playing around with it, logged in a format that can be used to test later. 

Braintrust Overview

- Likes to think of Braintrust as the end-to-end developer platform for people to build the best AI products.
- At a high level, likes to think about the 3 big components of the old world of building software. There's the IDE, the CI/CD, and observability. And it is possible to do all 3 of those things in Braintrust
	- For instance, there is a prompt playground, which allows you to create and test prompts, and test models side by side. It's a powerful multiplayer collaborative IDE system that allows you to build the prompts that power your application. 
- To have the IDE, CI/DC and observability all in one place is significant because everything revolves around data. 
	- A classic example may be if you're building an app and you ship an internal version and your CEO tries it out and comments that a particular query was not good, then you can find that interaction in the logs, save it into a dataset so that every time someone runs an eval or someone is playing with prompts in the playground, that piece of data is under consideration for what they're doing. 
	- The fact that you are able to share these datasets that you curate and build up is very powerful.
- One exciting feature of BrainTrust is that it allows customers to deploy the infrastructure in their own cloud environment, while the UI that is being updating all the time is hosted in BrainTrust’s environment. That means as a customer who cares a lot about data security, all the data can be stored in their own cloud environment rather than having to send all of it to a third party. 
	- There are not many products that do that and it is not easy to build. However, once you architect and build a product that way, it allows you to have the best of both worlds between security at scale and rapid development. 
	- For instance, to reflect a piece of user feedback, you can actually work on the change on a branch and then send the customer a link to that preview, which means that they get to use software that's unreleased. And so you can actually work on fairly novel changes and get user feedback without necessarily shipping the change. And then once the feedback is vetted and the code is vetted via code review, then it can be landed much more safely. 

How AI is Changing Software Development

- There may be broadly 2 kinds of developer workflows that will matter, and both are giant areas of opportunity and innovation. 
	- The first category is about using AI to develop software. 
	- The second category is building good software that uses AI or has an AI component.
- If you’re building software as we know it today, e.g., software for ordering coffee from a coffee shop, the workflow around creating that kind of software is going to change dramatically, and it's already significantly easier to create that software for a variety of reasons. 
	- For instance, the likes of Vercel removes a lot of the friction that is associated with spinning up an application, hosting it with authentication etc., compared to what it used to be even 5 years ago. And if you add AI on top of that, that makes it even easier. 
	- There is g

## Key Claims

1. The smartest companies maintain two AI product roadmaps: one assuming incremental AI improvement without AGI, and one assuming transformative AI breakthroughs.
2. Products should be architected so that a 2x model improvement automatically makes the product better.
3. Most companies forecast at least 50% of engineering projects involving AI over the next one to two years, and close to 100% within five years.
4. The paradigm for building software has fundamentally shifted away from code in an IDE toward data from users and prompts that non-engineers can contribute to.
5. A majority of BrainTrust users use TypeScript SDKs rather than Python SDKs, suggesting TypeScript is emerging as the language of AI product development.
6. The primary persona driving AI innovation has shifted from ML scientists and data scientists to product engineers.
7. Without structured eval tooling, teams resort to 'vibe checks' — informal group consensus evaluations that are not reproducible or scalable.
8. Alternative LLM providers broadly use the same network protocol as OpenAI models, enabling a single protocol to target any major model.
9. Tool calling is valued primarily because it forces models to output data in a structured, code-consumable format, not merely because it enables external tool invocation.
10. Without structured output / tool calling support, the only viable product category an AI model can support is chat products.

## Capabilities

- Tool calling (function calling) is now fundamental to all production AI products, enabling models to generate structured data that matches specified formats for reliable integration with code
- Multiple LLM model abstraction layer enabling seamless switching between OpenAI, Google, Anthropic, Meta, and other providers through a unified API interface
- TypeScript and product engineering are now the dominant paradigm for AI product development, not Python and ML science
- Enterprise-scale AI agents deployed in production by multiple major SaaS companies (Zapier, Notion, Retool, Instacart, AirTable) showing viable commercial product models
- Shift from IDE-centric code development to data-and-prompt-driven software paradigm where product managers, users, and non-engineers can influence behavior

## Limitations

- Models without reliable tool calling cannot produce structured output reliably, forcing developers to only build chat products or custom parsing layers
- Fragmented multi-model landscape creates selection paralysis and cognitive overhead that delays product development decisions
- Pre-systematic evaluation, developers resort to informal 'vibe checks' (manual testing by committee) instead of data-driven model selection
- Uncertainty about AGI timeline forces enterprises to hedge bets across multiple incompatible product roadmaps, increasing planning complexity
- Non-chat AI products require specialized integration expertise (data pipelines, API abstraction, observability) that most product engineers lack
- Selling non-AI enterprise software is structurally difficult — attention and capital allocation have shifted entirely to AI-enabled products

## Bottlenecks

- Fragmented model ecosystem creates cognitive overhead preventing developers from efficiently finding cost-optimal models for their specific tasks
- Enterprise adoption of non-AI software is functionally blocked due to complete organizational pivot toward AI initiatives
- Emerging workflow disconnect between developer tooling (IDEs, git) and AI-native product development (data-driven, prompt-driven iteration)

## Breakthroughs

- Tool calling (function calling) has become universal and mandatory for all production AI products, fundamentally enabling non-chat agentic systems
- Shift from IDE/code-centric software development to data-and-prompt-driven paradigm where non-engineers (product managers, users) influence product behavior
- TypeScript and product engineering (not Python and ML science) have become the dominant paradigm for building production AI products

## Themes

- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/startup_formation_and_gtm|startup_formation_and_gtm]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/braintrust|BrainTrust]]
