---
type: source
title: 'The "think" tool: Enabling Claude to stop and think'
source_id: 01KJSVPQDAAMA1FB974CP0RW2P
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# The "think" tool: Enabling Claude to stop and think

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# The "think" tool: Enabling Claude to stop and think
article
https://www.anthropic.com/engineering/claude-think-tool

---

## Briefing

**Anthropic's "think" tool is a lightweight, stateless mid-response scratchpad that dramatically improves Claude's performance in agentic tool-use scenarios — particularly policy-heavy and sequential decision-making tasks — by giving it a structured pause point to reason about newly acquired information. Distinct from extended thinking (which operates pre-response), the "think" tool is most valuable when the model's knowledge state changes during execution via tool call results. As of December 2025, extended thinking supersedes the dedicated think tool for most use cases, but the underlying insight — that mid-execution reasoning space yields compounding reliability gains — remains highly relevant for autonomous agent design.**

### Key Takeaways
1. **Think tool vs. extended thinking: fundamentally different timing** — Extended thinking runs before Claude generates a response; the "think" tool fires mid-response when Claude has received new external information from tool calls that must be reasoned over.
2. **54% relative improvement on hard policy tasks** — The "think" tool with an optimized prompt achieved 0.570 on τ-Bench airline pass^1 versus 0.370 baseline, the largest gain of any configuration tested.
3. **Simpler domains self-organize** — In the retail domain, the unprompted "think" tool alone achieved 0.812 vs 0.783 baseline, suggesting the model independently uses the scratchpad productively when policy complexity is lower.
4. **Extended thinking ≈ unprompted think tool in agentic settings** — In the airline domain, extended thinking (0.412) and the unprompted "think" tool (0.404) performed nearly identically at k=1, suggesting the real unlock is the combination of think tool + structured prompting.
5. **Consistency is the key gain, not just peak performance** — The think+prompt advantage compounds at higher k: pass^5 is 0.340 vs 0.100 for both unprompted-think and baseline, a 3.4x improvement in sustained reliability.
6. **SWE-bench: 1.6% isolated improvement with strong statistical power** — Controlled experiments (n=30 vs n=144) confirmed the think tool's contribution to Claude 3.7 Sonnet's SOTA 0.623 SWE-bench score (p < .001, d = 1.47).
7. **Domain-specific examples in the system prompt are the highest-leverage implementation choice** — The think tool's full benefit requires showing the model concrete reasoning patterns for your domain; the tool definition alone is insufficient for hard tasks.
8. **Zero downside risk on irrelevant tasks** — The tool doesn't change external behavior unless Claude autonomously invokes it, making it safe to add to any agentic setup.
9. **Non-sequential and simple tasks gain nothing** — Single tool calls, parallel calls, or low-constraint instruction following see no improvement, so the benefit is strictly conditional on decision chain complexity.
10. **Generalizes across Claude model generations** — Claude 3.5 Sonnet (New) achieves equivalent gains with the same configuration, indicating architectural generality of the technique.

---

### What the "Think" Tool Is and How It Differs from Extended Thinking

- The "think" tool is a special tool definition given to Claude that creates a designated scratchpad for mid-response reasoning.
  - It takes a single string input ("thought") and has no external effects — it does not fetch data, modify any database, or return information back to the model.
  - Mechanically, it simply appends the thought to the conversation log, making the reasoning transparent and auditable.
- **The critical distinction from extended thinking is temporal**: extended thinking occurs before Claude begins generating any response, allowing deep upfront planning; the "think" tool fires during response generation, after Claude has already received tool outputs.
  - Extended thinking: deep pre-action deliberation, best when all information is available from the query.
  - Think tool: reactive mid-execution reasoning, best when information is incrementally revealed by tool results.
- The think tool's reasoning is intentionally scoped — **"less comprehensive than extended thinking, and more focused on new information that the model discovers"** during execution.
- This makes the think tool uniquely suited to the information-acquisition structure of agentic loops, where the model's knowledge state materially changes with each tool invocation.

### When the "Think" Tool Provides the Most Value

- **Tool output analysis**: When Claude must carefully interpret the results of previous tool calls before deciding the next action, especially if backtracking may be needed.
  - Example: receiving a user's membership status and dynamically recalculating baggage fees before confirming a booking.
- **Policy-heavy environments**: When the model must navigate detailed rule sets, verify compliance, and cross-check multiple constraints simultaneously.
  - The airline benchmark is the canonical example — complex cancellation rules, fare classes, payment restrictions, segment states.
  - Simply having access to think improved airline performance, but the combination with structured prompting produced the largest gains, "likely due to the high complexity of the airline policy part of the benchmark."
- **Sequential decision making**: When each action in a chain depends on previous actions and errors are costly or hard to reverse.
  - In such settings, a mistake in step 3 may invalidate all subsequent steps, making mid-chain verification critical.
- The think tool does **not** help for:
  - Non-sequential tool calls (single calls or parallel calls with no interdependency).
  - Simple instruction following with minimal constraints.

### Benchmark Results: τ-Bench Airline Domain

- τ-Bench is a comprehensive benchmark simulating realistic customer service agent tasks, evaluating policy adherence, tool use, and multi-turn u

## Key Claims

1. The 'think' tool creates dedicated space for structured thinking during complex tasks and is distinct from extended thinking capability.
2. The 'think' tool is particularly suited for long chains of tool calls where Claude needs to process external information from tool call results that was not available in the original query.
3. The reasoning Claude performs with the 'think' tool is less comprehensive than extended thinking and more focused on newly discovered information.
4. On the τ-Bench airline domain, the 'think' tool with an optimized prompt achieved a 54% relative improvement over baseline on the pass^1 metric (0.570 vs 0.370).
5. On the τ-Bench retail domain, the 'think' tool alone (without additional prompting) achieved pass^1 of 0.812 versus 0.783 for the baseline.
6. In the airline domain of τ-Bench, extended thinking alone showed similar performance to the unprompted 'think' tool (0.412 vs 0.404 at k=1).
7. The 'think' tool contributed to Claude 3.7 Sonnet achieving a state-of-the-art SWE-bench score of 0.623.
8. On SWE-bench, the isolated effect of including the 'think' tool improved performance by 1.6% on average with high statistical significance.
9. Pairing the 'think' tool with optimized domain-specific prompting yields dramatically better results in difficult domains compared to the tool alone.
10. The improvements from using the 'think' tool are maintained across all pass^k levels up to k=5, indicating improved consistency and robustness to edge cases.

## Capabilities

- A lightweight 'think' tool — a no-op tool call that creates dedicated scratchpad space mid-response — improves Claude 3.7 Sonnet's policy adherence and sequential decision-making in agentic tool-use chains by up to 54% relative on complex domains without model retraining
- Claude 3.7 Sonnet achieves state-of-the-art 0.623 on SWE-bench, with the 'think' tool as a contributing technique (isolated effect: +1.6%, p < .001, d = 1.47)
- The 'think' tool benefit generalises across Claude model generations — Claude 3.5 Sonnet (New) achieves performance gains with the same think-tool configuration as Claude 3.7 Sonnet

## Limitations

- The 'think' tool provides zero measurable improvement for non-sequential or parallel tool calls — the structured reasoning space is only useful when building on accumulated context across a chain
- Think-tool reasoning is shallower and less comprehensive than extended thinking — it is focused only on processing newly discovered external information rather than deep pre-response deliberation
- Adding the 'think' tool increases prompt length and output token count, raising inference cost for every call regardless of whether the thinking step was necessary
- Agent reliability degrades sharply across repeated independent trials even with the best configuration: the top airline-domain setup drops from pass^1 = 0.584 to pass^5 = 0.340 — a 42% collapse in consistency — revealing persistent stochastic failure modes the think tool does not eliminate
- The think tool's benefits on complex domains are substantially gated behind domain-specific prompt engineering: without tailored examples of reasoning structure, gains are modest; the tool does not self-organize effective thinking without external guidance
- Extended thinking mode alone offers no advantage over the unprompted 'think' tool in sequential agentic scenarios — suggesting extended thinking does not effectively carry over into tool-call chain reasoning without additional scaffolding
- Even the best agentic configuration (think + optimised prompt) leaves ~43% of airline-domain tasks failing on first attempt — policy-heavy agentic scenarios remain substantially unsolved

## Bottlenecks

- Realising structured in-context reasoning benefits requires non-trivial domain-specific prompt engineering — models cannot self-direct effective reasoning patterns in novel policy environments without externally supplied examples, creating a per-deployment engineering burden that limits scalable age

## Breakthroughs

- A zero-architecture-change prompting intervention — a no-op 'think' tool with domain-specific examples — produces a 54% relative improvement in complex agentic task performance and contributes to SWE-bench SOTA (0.623), demonstrating that structured mid-generation reasoning scaffolding is a high-lev

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/extended-thinking|extended thinking]]
- [[entities/passk-metric|pass@k metric]]
- [[entities/passk-metric|pass^k metric]]
- [[entities/τ-bench|τ-Bench]]
