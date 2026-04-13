---
type: source
title: Why RL Won — Kyle Corbitt, OpenPipe (acq. CoreWeave)
source_id: 01KJVERVWWKQ1EY0CX0E9RG165
source_type: video
authors: []
published_at: '2025-10-16 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- startup_and_investment
- startup_formation_and_gtm
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why RL Won — Kyle Corbitt, OpenPipe (acq. CoreWeave)

**Authors:** 
**Published:** 2025-10-16 00:00:00
**Type:** video

## Analysis

Finetuning and Market Dynamics

- In early 2023 we were looking at different ideas, and immediately after the GPT\-4 launch, we saw an opportunity in the market at the time as GPT\-4 was extremely powerful but insanely expensive\. So there was an opportunity to distil specific workflows from GPT\-4 down to much smaller, much cheaper models\. 
	- There was a very clear value proposition there\. Given how expensive GPT\-4 was, it was hard to deploy in production, but you could take those abilities and deploy them much more cheaply\. 
		- At the time, while the prices were too high on the closed models, you couldn't just drop in an open model and replace them, because the quality was quite bad, especially when moving to smaller model sizes\. Larger open models were not even available at that time\.
	- While the initial traction was super strong, there was a slow march of the frontier model token prices dropping by 3\-5x over and over again, which ate away at the value proposition over time\.
		- Competition never really materialised from the NeoClouds or the GPU providers\. Everybody had an offering in finetuning, but nobody used them because they were hard to use, which is perhaps not so surprising given that it was not their primary focus\.
- Mistral and Mixtral with their 7B models marked the start of a golden period of finetuning startups as they were the first credible open\-source models, better than Llama 2 that they were effectively replacing, with a fully open Apache 2 license\.
- <a id="_Hlk212465900"></a>LoRAs have some very attractive properties compared to doing a full finetune\. 
	- During training, using a LoRA helps a bit because it reduces memory requirements\. 
	- But where they really shine is at inference time\. With LoRAs, you can multiplex – essentially stack or swap – an arbitrarily large number of LoRAs on the same GPU deployment, which provides a lot of flexibility and makes scaling and serving much more efficient\.
- LoRAs may have gone out of fashion for a while, largely because finetuning itself wasn’t in vogue, but now that finetuning is coming back in a big way, LoRAs are once again the right solution in many cases\. 
	- They are a smart, efficient, and flexible way to adapt large models without the overhead of retraining them from scratch\. As a relatively lightweight customisation of an existing model for a specific task, there is really no downside to using a LoRA, while there are lots of upsides from an infrastructure simplicity point of view\. 
	- The research from Thinking Machines showed that everyone doing post\-training work inside these big labs tends to use LoRAs – not for the full\-scale production runs, but for experimentation\. When they are testing new methods or running smaller\-scale experiments, they’ll just apply LoRAs on top of a base model, and it works perfectly well for that purpose\.

When to Finetune

- <a id="_Hlk212466073"></a>It is still the case that you do not always need finetuning, and should only do so when cost, latency, or quality consistency are the primary factors\.
	- The biggest case where finetuning really makes sense today – which applies both to classical SFT and the RL\-based methods – is when you have to move to a smaller model, typically for latency reasons\. If you’re constrained to a smaller model for deployment, then finetuning often becomes essential to get acceptable performance\. 
		- This is especially common in real\-time voice applications, where response time is critical\. 
		- It is also common with customers who have strict latency or hardware constraints, say, they need to deploy on a single GPU or within their own cloud infrastructure\. 
	- Outside of those scenarios, though – probably 90% of cases – finetuning still isn’t a great return on investment\. If you’re not constrained by latency or model size, it’s generally better to stick with the base model rather than invest in finetuning at this stage\.
- There are two parts on the cost side, and then there are multiple parts on the benefit side\. 
	- On the cost side, the main things you have to think about are the upfront effort required to get an actual training system set up for your task\. 
		- That can be quite variable, but at a minimum, you are going to have to dedicate a couple of weeks of a fairly competent engineer's time\. If you have a very complex system and you are doing RL and you need to set up a whole environment, it could be a couple of months of time\. That's a fixed cost\. 
	- There's also an ongoing carrying cost where once you've committed to doing finetuning, it does make other parts of your stack less flexible, less nimble, because whenever you're updating your prompt or you're adding new context, now you have to spend a few hours training a model, and that's just going to slow down your iterations, which is a real cost\. And in many cases, that's the larger cost\. So you only want to do that if the benefits are large enough\.
	- The dollar cost is almost never a factor\. It's just so much less than the time, the amount you're spending this engineer to do the work\. Each of these runs is a couple hundred dollars, and you don't have to do that many of them\.

The Transition to Reinforcement Learning

- The switch to RL was triggered by the release of o1 preview when it became clear that someone had figured out how to make RL actually work with LLMs\. The goal was to figure out whether it works for tasks specifically and tease out different parts of the market\. 
	- Now, there is a very strong consensus that on the frontier, general\-purpose model side, investments in RL are paying off, especially when taking on the more agentic tasks\. The big labs are paying ridiculous amounts of money for these environments, but they are actually getting good results, both on the coding model side and in other contexts as well\. 
- When it was clear that RL was going to work in that context, then the question was whether it could be applied for 

## Key Claims

1. Fine-tuning requires a minimum of a couple weeks of a competent engineer's time as upfront fixed cost.
2. Complex RL fine-tuning setups requiring custom environments can take a couple of months of engineering time.
3. Fine-tuning imposes an ongoing carrying cost by making the stack less nimble, as prompt or context updates require retraining.
4. The dollar cost of individual fine-tuning training runs is negligible, typically between $5 and a few hundred dollars per run.
5. RL training is especially effective for coding models and agentic use cases.
6. GRPO with LLM-as-judge reward assignment works far better than expected for task-specific RL fine-tuning.
7. The reward assignment problem for task-specific RL is largely solved via LLM-as-judge.
8. Even a relatively weak judge model (Qwen 2.5 32B) enables a fine-tuned smaller model (Qwen 2.5 14B) to surpass all frontier models on a specific task.
9. LLM-as-judge works robustly because the model only needs to produce relative rankings, not absolute quality scores.
10. Environment setup is the remaining unsolved bottleneck for task-specific RL, requiring significant manual work per task.

## Capabilities

- GRPO-based RL training with relative LLM judgment (no need for absolute ground truth) achieves state-of-the-art agent performance; even weak open-source judge models (e.g., Qwen 2.5 32B) enable agents to outperform frontier models on task-specific domains
- Ruler library (Relative Universal LLM Elicited Rewards): LLM-as-judge framework for GRPO that replaces need for absolute ground-truth reward functions with relative comparisons; works reliably with any LLM judge and requires no specialized judge models
- Task-specific RL training (Ruler + GRPO) on small open-source models achieves performance competitive with or better than frontier models on specific agentic tasks without requiring frontier model APIs
- PPO-based RL training can operate directly on real production traces without requiring simulated or sandboxed environments, unlike GRPO which requires reproducible parallel rollouts
- Serverless reinforcement learning service: managed RL infrastructure that handles GPU allocation, crash recovery, auto-scaling, and cluster management, enabling enterprises to run RL without infrastructure expertise
- RL post-training for agentic reasoning and coding tasks is now consensus best practice among frontier labs; o1 and subsequent releases prove RL produces major capability improvements over SFT

## Limitations

- GRPO requires fully reproducible, sandboxed environments for parallel rollout generation; nearly impossible to implement for real-world applications due to non-determinism, failure modes, and system complexity
- Sandboxed training environments must replicate production failure modes and bugs; agents trained without exposure to realistic failure modes fail catastrophically in production
- Simulated user behavior in agentic RL training lacks diversity and breadth of real user responses; LLM-based user simulators cannot adequately capture unpredictable human variations, causing distribution shift
- RL training setup has high fixed engineering cost; minimum 2-3 weeks of senior engineer time, scaling to 2-3 months for complex agentic tasks with custom environments
- Iteration velocity penalty after committing to RL: prompt changes require retraining cycles (hours to days) instead of instant deployment, reducing nimbleness in production iteration
- Fine-tuning business model faces existential pressure from two sides: frontier labs releasing increasingly capable and cheaper distilled models, and GPU providers bundling fine-tuning as commodity service
- Market viability for task-specific training depends on frontier labs NOT eventually training on every possible task; if labs scale RL to all domains, independent task customization becomes unnecessary
- GRPO-style RL is likely a dead end for real-world agentic tasks due to fundamental requirement for reproducible parallel rollouts being incompatible with production system complexity
- Prompt optimization tools (e.g., Jeppa) fail to provide meaningful improvements over baseline prompts; performance gains are marginal (50% → 56%) compared to RL (50% → 96%), making investment unjustified
- Open-source model adoption suppressed by frontier lab pricing subsidies; despite better cost and privacy economics, enterprises default to subsidized proprietary APIs making open-source uncompetitive
- RL fine-tuning ROI unclear for many tasks; benefits must justify 2-3 month engineering cost, but quantification is difficult and many tasks may not benefit enough to justify the investment
- Infrastructure libraries for RL built by PhD students lack production-grade reliability and usability; pervasive quality issues force companies to rebuild core tooling

## Bottlenecks

- Reproducible training environment construction for GRPO is the critical path blocker; building exact copies of production systems with identical failure modes, non-determinism handling, and user simulation is essentially impossible at scale
- User behavior diversity gap in simulated agentic RL environments; LLM user simulators cannot generate the breadth and unpredictability of real human interactions, causing trained agents to fail on distribution shift
- Task-specific RL adoption blocked by high fixed setup cost (2-3 months engineering) relative to marginal gains for many use cases; ROI calculation is opaque and prevents wider enterprise adoption
- Frontier labs' strategic choice to scale RL across all task domains creates existential uncertainty about the value of task-specific fine-tuning; if labs can train on every task, independent customization becomes commodity or obsolete
- Frontier model pricing subsidies suppress open-source adoption; even with cost and privacy advantages, enterprises default to subsidized proprietary APIs, creating structural headwind for open-source deployment and RL-based customization

## Breakthroughs

- Ruler library and GRPO relative-comparison framework solve reward specification bottleneck: relative LLM judgment (comparing multiple outputs) is far more robust than absolute ground-truth assignment; even weak open-source models (Qwen 2.5 32B) work reliably as judges without requiring frontier mode
- Task-specific RL training validated to achieve frontier-level performance on enterprise tasks: weak open-source models (Qwen 14B) with RL training outperform top frontier models on agentic domains without requiring frontier model APIs or enormous compute
- o1 and subsequent models prove that RL post-training is the standard approach for reasoning and agentic capabilities at frontier labs; consensus has shifted from speculation to established practice, with all major labs investing heavily in RL infrastructure

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/startup_formation_and_gtm|startup_formation_and_gtm]]

## Key Concepts

- [[entities/coreweave|CoreWeave]]
- [[entities/grpo|GRPO]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
- [[entities/o1|o1]]
