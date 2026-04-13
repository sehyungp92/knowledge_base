---
type: source
title: Some ideas for what comes next
source_id: 01KJSSCZFW7522G261CFV3N587
source_type: article
authors: []
published_at: '2025-06-23 00:00:00'
theme_ids:
- agent_systems
- ai_market_dynamics
- frontier_lab_competition
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Some ideas for what comes next

**Authors:** 
**Published:** 2025-06-23 00:00:00
**Type:** article

## Analysis

# Some ideas for what comes next
2025-06-23 · article
https://www.interconnects.ai/p/summertime-outlook-o3s-novelty-coming

---

## Briefing

**The AI field in mid-2025 is undergoing a structural shift: parameter scaling has lost its product differentiation power, progress is moving into post-training and inference-time compute, and agent reliability — not peak model capability — is becoming the primary competitive frontier. o3's unreplicated search behavior is the single clearest open question about whether OpenAI has a durable technical lead.**

### Key Takeaways
1. **o3's search is a genuinely novel capability** — multiple months post-launch, no other lab has replicated its "trained hunting dog" relentlessness at finding niche information, suggesting a real technical breakthrough rather than just a scaling increment.
2. **The RL tool-use training problem is unsolved in the open** — models in RL quickly unlearn to use tools that aren't rewarded, and constructing data pipelines that reliably incentivize search throughout training is a hard, largely unpublished challenge.
3. **Search infrastructure is a hidden moat** — OpenAI's Bing backend versus Anthropic's SEO-spam-plagued Brave API is an underappreciated quality gap in model search capability.
4. **Agent reliability improvements are discontinuous and rapid** — sub-task failure rates can drop from 50% to ~99% via targeted post-training data, creating sudden large perceived quality jumps without any change in peak model capability.
5. **Two distinct agent failure regimes exist** — the distinction between "can't do the task at all" versus "fails on rare sub-components" determines whether an agent can compound on product-market fit or is stuck waiting for a fundamental capability jump.
6. **Parameter scaling as product differentiation ended in 2024** — GPT-4.5 cost ~100x GPT-4's compute and delivered only marginal user-metric gains; the biggest training cluster now buys research pace, not product leadership.
7. **The industry has converged on stable model tier standards** — tiny/small/standard/big tiers with predictable price-latency-capability profiles signal a maturing market, not a frontier of unbounded scaling.
8. **Benchmarks will increasingly mislead about real progress** — as real-world gains decouple from benchmark gains (as in Claude 4), evaluation frameworks will appear flat while actual utility improves, creating a narrative opportunity for AI skeptics.
9. **Pretraining science still matters even as parameter growth stalls** — Gemini 2.5's training stability and optimization dynamics improvements produced significant out-of-pretraining performance gains, showing pretraining quality and pretraining scale are separable.
10. **GPT-5's "size" will come from inference-time scaling** — the era of "bigger model = smarter model" for consumer products is over; future capability increases route through test-time compute, not larger weights.

---

### o3's Search as an Unreplicated Breakthrough

- **The standard narrative about o3 — that it "scaled RL compute" — misses the most distinctive feature**: its qualitatively different search behavior, not just its reasoning depth.
  - For a normal query, o3 can examine tens of websites, described as a "trained hunting dog on the scent" — relentless, targeted, and distinct from anything else available.
  - **The absence of any comparable model from Google or Anthropic months after release is the real signal** — in a field where capabilities tend to mirror rapidly across labs, this gap is anomalous.

- If the gap persists through summer 2025, **it would confirm that OpenAI achieved a genuine technical breakthrough in search reliability within reasoning models**, not merely a compute advantage.

- The contrast with OpenAI's typical competitive landscape is striking: Gemini and Claude releases tend to shadow each other in capability, making o3's durable search advantage the most interesting open question in frontier AI.

### Why Replicating o3's Search Is Hard

- **The core RL challenge: models rapidly learn to abandon tools that don't provide clear training signal.**
  - In early RL experiments, prompting the model to search via system prompt works, but as training progresses, if search tool usage isn't tied to reward, the model stops using it — quickly.
  - This creates a data curation problem: you must find or construct tasks where search is intrinsically necessary for getting the reward, not just decoratively useful.

- **OpenAI's edge likely comes from accumulated RL training expertise**, particularly from Deep Research (itself built on o3), which provided feedback loops for refining tool-use reliability at scale.
  - A DeepSeek R1-style scaled RL paper showing consistent tool use rates across data subsets would be a significant open-science contribution.

- **Search index quality is a structural bottleneck**, not just a model quality issue.
  - OpenAI operates on a Bing backend — higher-quality, lower SEO spam.
  - Anthropic uses Brave's API, which suffers from SEO spam degrading result quality.
  - Academic replications using either API face moderate additive infrastructure costs beyond compute.

- Once open baselines exist, a productive research direction would be testing **generalization to unseen data stores** — critical for deploying search-augmented agents on private, sensitive data (healthcare, banking).

### Agent Progress: Fast but Discontinuous

- **LLM agents are architecturally different from chat models** — they involve many model calls, potentially multiple models, and multiple prompt configurations, managing real environments with complex memory requirements.
  - Chat models were designed for linear tasks with no environment; agents must handle broader task breadth continuously.

- **Two-class failure taxonomy for agents:**
  - Class 1: The model fundamentally cannot perform the target task (requires capability breakthrough).
  - Class 2: The model fails on small, specific sub-

## Key Claims

1. o3's core breakthrough includes scaling compute for reinforcement learning training with verifiable rewards (RLVR)
2. o3's search capability is qualitatively different from any other model available
3. Multiple months after o3's April 2025 release, no other leading lab has released a model with comparable search capability
4. In RL training, if a search tool is not useful the model will rapidly learn to stop using it
5. Finding RL data where the model is incentivized to search is the critical unsolved challenge in replicating o3's search capability
6. OpenAI's models use a Bing backend for search while Anthropic uses Brave's API
7. Anthropic's search quality is degraded by SEO spam in Brave's API results
8. OpenAI has accumulated significant expertise in RL training for consistent tool use, partly through Deep Research's training
9. Claude Code has exceptional product-market fit, especially with Claude 4
10. LLM-based agents involve many model calls, sometimes with multiple models and multiple prompt configurations

## Capabilities

- o3 can search tens of websites with relentless, targeted search behaviour, finding niche information in a qualitatively different way than prior models — described as a 'trained hunting dog on the scent'
- Rapid post-training iteration allows labs to identify specific agent failure modes in production, generate targeted training data, and fix sub-task reliability from ~50% to ~99% within short deployment cycles
- Claude Code with Claude 4 has achieved strong product-market fit for agentic coding, enabling even non-specialist users to build demos and standalone websites with high reliability
- Pretraining efficiency gains allow newer frontier models to match or exceed predecessor performance at the same or smaller parameter counts, holding API prices flat while improving capability

## Limitations

- During RL training for tool/search use, models rapidly learn to abandon tools if they do not reliably generate reward signal — making it extremely difficult to train stable, persistent search behaviour via RLVR
- Search-augmented reasoning models are fundamentally bottlenecked by the quality of their underlying search index — inferior indices with SEO spam (e.g., Brave API) significantly degrade search-based capabilities regardless of model quality
- Raw parameter scaling has hit sharply diminishing returns for user-facing capability — GPT-4.5 required approximately 100x the training compute of GPT-4 but delivered only marginal improvements on normal user metrics
- No competing lab has matched o3's search capability in the months since its April 2025 release — implying significant hidden technical barriers to replicating RL-trained reliable tool use at this quality level
- Open and academic communities lack the RL training data, search-incentivised environments, and infrastructure expertise required to train models with reliable tool-use comparable to o3
- Standard benchmarks are losing validity as measures of real-world agent capability — Claude 4 showed minor benchmark gains alongside major real-world improvements, making progress increasingly opaque to external observers
- New agentic platforms face high-variance, unpredictable success — unlike model capability scaling, reaching product-market fit depends on task-domain fit, product design, and timing that cannot be reliably forecast
- Future parameter scaling beyond current tiers is contingent on AI monetisation success — introducing business model risk as a hard ceiling on when the next generation of frontier pretraining becomes viable

## Bottlenecks

- Lack of RL training data and environments that reliably incentivise tool/search use blocks open research and smaller labs from training models with o3-quality search-augmented reasoning
- Inferior search index infrastructure outside top labs (SEO-spam-heavy APIs, high incremental cost for academic use) creates a practical ceiling on search-augmented model quality for all but the largest players
- Raw parameter scaling has become economically unviable as a primary capability differentiator, and the transition to inference-time and post-training approaches leaves an unclear path to the next qualitative capability tier

## Breakthroughs

- o3 achieved qualitatively distinct search-augmented reasoning via RLVR training on search-incentivised data — producing a model whose search behaviour is categorically better than any competitor months after release, suggesting a genuine technical moat rather than incremental improvement
- Post-training iteration cycles have become fast enough that labs can diagnose, fix, and deploy agent reliability improvements for specific failure modes within weeks — decoupling agent quality improvement from pretraining scale and investment

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/claude-4|Claude 4]]
- [[entities/claude-code|Claude Code]]
- [[entities/codex|Codex]]
- [[entities/deep-research|Deep Research]]
- [[entities/gpt-45|GPT-4.5]]
- [[entities/post-training|Post-training]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/o3|o3]]
