---
type: source
title: What it takes to build AI agents that actually work - Foundation Capital
source_id: 01KKTEX3N26BD8CQVH89PDRMXM
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- ai_business_and_economics
- multi_agent_coordination
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# What it takes to build AI agents that actually work - Foundation Capital

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# What it takes to build AI agents that actually work - Foundation Capital
article
https://foundationcapital.com/ideas/what-it-takes-to-build-ai-agents-that-actually-work/

---

## Briefing

**The gap between a working demo and a production-grade AI agent is an engineering problem, not a model problem — and closing it requires the same deep systems expertise that some claim AI has made obsolete. Reliability compounds exponentially: at 99% per-step accuracy a 100-step workflow fails 63% of the time, but at 99.9% it succeeds 90% of the time, meaning each additional "nine" unlocks disproportionately longer autonomous horizons. Founders who understand this math and build toward it create moats that are structurally difficult to replicate.**

### Key Takeaways
1. **The 80/20 reliability trap** — Getting an agent to work in a demo takes 20% of the effort; getting it to 99.9% reliability takes 100x more work, and the gap is where moats form.
2. **Compounding error math is brutal** — At 90% per-step accuracy a 10-step task succeeds only 35% of the time; at 99.9% that same 10-step task succeeds 99% of the time — a qualitatively different product.
3. **"99% step-length" as the key metric** — The longest sequence an agent can execute while maintaining 99% per-step reliability determines whether you are selling a productivity tool or a complete outcome replacement.
4. **Horizon length is doubling every 7 months** — METR research shows frontier coding agents' reliable horizon has been on this trajectory, implying 10,000-step (≈1 month of work) workflows by 2029.
5. **Self-conditioning is a hidden failure mode** — As agents accumulate errors, those errors enter the context and accelerate subsequent failures; explicit step-by-step reasoning effectively resets the context and dramatically extends reliable horizons.
6. **Multi-agent specialization beats monolithic models** — A network of narrow, expert agents with defined handoff points consistently outperforms a single generalist agent on long-horizon tasks, because specialization maximizes per-step accuracy.
7. **Forward-deployed engineers are not optional overhead** — For vertical AI in regulated domains, embedding engineers with clients to surface undocumented SOPs and edge cases before go-live is what separates audit-ready from demo-grade software.
8. **Process transparency is itself a reliability mechanism** — Showing users the agent's reasoning trace both catches errors before they compound and builds the adoption trust that makes 99.9% technical accuracy commercially meaningful.
9. **LLMs are commoditizing; orchestration is the durable asset** — The enduring value lies in the engineering layers built around models — verification, error recovery, long-horizon orchestration — not the models themselves.
10. **Deep domain + engineering is the defensible combination** — "OpenAI can't just enter this space" because ERP integration, institutional knowledge extraction, and sustained client relationships cannot be replicated from 30,000 feet.
11. **Illusion of diminishing returns on benchmarks** — Research from Cambridge/Stuttgart/Max Planck shows that per-step accuracy gains that look marginal on leaderboards compound hyperbolically on long-horizon tasks, especially above 90% per step.
12. **We are in the decade of agent engineering, not just agents** — The limiting resource is not model capability but the systems thinking required to make models reliable enough for production: error cascade design, orchestration, verification, and workflow instrumentation.

---

### The Reliability Math: Why Each Nine Matters Disproportionately

- **The compounding error problem makes intuitive accuracy targets dangerously misleading** for anyone building workflow automation.
  - At 90% per-step accuracy: a 10-step task succeeds 35% of the time (0.9^10); a 100-step task succeeds 0.003% of the time — effectively never.
  - At 99% per-step accuracy: 10 steps succeed 90% of the time; 100 steps succeed 37% of the time — still failing more than half the time.
  - At 99.9% per-step accuracy: 100 steps succeed 90% of the time — a qualitatively different product category.
- **The relationship between per-step accuracy and horizon length is hyperbolic, not linear.** Moving from 99% to 99.5% accuracy might double the number of steps an agent can handle before failing — a gain that looks trivial on a benchmark leaderboard.
- Research from the University of Cambridge, University of Stuttgart, and Max Planck Institute describes this as the **"illusion of diminishing returns"**: on short-task benchmarks, model accuracy appears to flatten at high levels, but for long-horizon execution those incremental gains compound sharply.
  - In their experiments, models that look nearly identical on single-step metrics perform very differently on multi-step tasks, especially once per-step accuracy exceeds 80-90%.
- The practical framing for founders: **if you're not explicitly chasing sustained reliability over long sequences, you are building a demo, not a product.**

---

### The Horizon Length Trajectory and What It Implies

- METR research group tracks **"horizon length"**: how long an AI agent can work reliably before breaking down, measured in sequential steps at 99% accuracy.
  - Current best systems: approximately 100 steps at 99% accuracy, equivalent to 1-2 days of focused analyst work (e.g., a competitive landscape analysis or multi-source research brief).
  - OpenAI's Deep Research is cited as an example of what is achievable at this level today.
  - **Horizon length for software/coding agents has been doubling every 7 months.**
- If this trajectory holds, **10,000-step workflows at 99% accuracy become feasible by 2029** — equivalent to roughly one month of continuous work.
  - At that scale: AI managing a complete product launch including competitive analysis, product specification, go-to-market strategy, and launch execution.
- Andrej Karpathy's framing — "this isn't the year of agen

## Key Claims

1. Building an AI agent that works in a demo is relatively straightforward, but building one reliable enough to run a business on remains extremely hard
2. Deep technical expertise — understanding edge cases, debugging complex systems, building robust error handling — is required to get from 80% to 99%+ reliability in production AI agents
3. The demo-to-reliability gap creates a competitive moat because what looks easy to replicate masks what is nearly impossible to replicate
4. In autonomous vehicles, climbing from 90% to 99.9% reliability proved exponentially harder than the initial climb from 0% to 90%, and AI agents are now beginning the same ascent
5. At 90% per-step accuracy, a 10-step task succeeds only 35% of the time; at 99%, those same 10 steps succeed 90% of the time
6. A 100-step workflow at 99% per-step reliability completes successfully only ~37% of the time, meaning it fails more often than it succeeds
7. At 99.9% per-step reliability, 100 steps succeed ~90% of the time, making long-horizon automation viable
8. The relationship between per-step accuracy improvement and additional reliable steps is hyperbolic: the closer you get to perfect reliability, the more additional steps each incremental improvement un
9. Research from Cambridge, Stuttgart, and Max Planck Institute identified an 'illusion of diminishing returns' on short-task benchmarks that obscures large compounding gains on long-horizon tasks
10. Moving from 99% to 99.5% per-step accuracy could double the number of steps an agent handles before failing

## Capabilities

- Best AI systems can reliably manage ~100 sequential steps at 99% per-step accuracy, equivalent to a day or two of focused analyst work (e.g., competitive landscape analysis, multi-source research brief)
- GPT-5 with explicit reasoning trace can execute over 2,100 sequential steps with approximately 80% success rate on long-horizon tasks
- Horizon length for software and coding AI agents has been doubling every 7 months, as measured by METR research group
- Specialized multi-agent systems with distinct expert agents per sub-task, clear handoff checkpoints, and human escalation paths achieve higher long-horizon reliability than monolithic generalist agents
- Audit-ready agentic automation for finance and accounting: specialized agents for invoice coding, reconciliations, cash forecasting, and revenue recognition with full step-by-step verification trails
- Hybrid orchestration combining LLMs, trained ML models, and deterministic software tools within a single workflow to optimize for both outcome accuracy and process auditability

## Limitations

- Compounding per-step error rates make long-horizon tasks fail at surprisingly high rates: at 99% per-step accuracy, a 100-step workflow succeeds only ~37% of the time; at 90%, a 10-step task succeeds only 35% of the time
- Self-conditioning error cascade: errors made by an agent in earlier steps become part of the context for subsequent steps, increasing the probability of further errors and snowballing toward complete task failure
- Without structured step-by-step reasoning, frontier models fail after only a handful of steps in long-horizon tasks — the unaugmented model cannot sustain reliable multi-step execution
- Short-task benchmarks create an 'illusion of diminishing returns' — small accuracy improvements (89→90→91%) appear to plateau on leaderboards but produce large compounding gains in long-horizon task completion that are invisible to standard evals
- Tacit institutional knowledge — undocumented SOPs, informal rules, implicit business logic — exists only in human memory and cannot be discovered autonomously by AI agents, requiring sustained human-AI collaborative surfacing before automation can go live
- Forward-deployed engineer model for achieving enterprise AI reliability is non-scalable: weeks of embedded human-AI work before and after deployment is required per client, destroying SaaS unit economics and creating a hard ceiling on growth rate
- Enterprise user trust is a hard adoption ceiling independent of technical accuracy: an agent with 99.9% technical accuracy will not be adopted if users cannot see and verify its reasoning process
- AI agents are currently limited to ~100 sequential steps at production-grade (99%) reliability — tasks requiring months of continuous work (10,000+ steps) remain out of reach until approximately 2029 if current scaling trends hold
- Large incumbent platforms (OpenAI, etc.) cannot replicate the deep ERP integration and client-embedded reliability required by vertical AI — their scale advantage does not transfer to last-mile enterprise reliability

## Bottlenecks

- Long-horizon agent reliability wall: the mathematical compounding of per-step error rates means that even at 99% per-step accuracy, 100-step workflows succeed only 37% of the time — blocking reliable automation of any task longer than a few dozen steps
- Self-conditioning error propagation in long-horizon agents: early mistakes corrupt the context window for subsequent steps, accelerating failure in a snowballing pattern that pure model quality improvements do not fully address
- Evaluation infrastructure gap: short-task benchmarks systematically fail to measure long-horizon reliability, creating a disconnect between leaderboard rankings and real-world production value — builders and researchers lack adequate signal to optimize for what matters

## Breakthroughs

- Empirical discovery that AI agent horizon length has been doubling every 7 months — establishing a Moore's Law-like scaling trajectory for agent autonomy that makes long-horizon capability milestones predictable and near-term
- Structured reasoning traces enable GPT-5 to execute 2,100+ sequential steps reliably (~80% success rate), demonstrating that the long-horizon reliability gap is partially a reasoning architecture problem solvable without fundamentally new models
- Academic research establishes the hyperbolic relationship between per-step accuracy and long-horizon task completion: once above ~80-90% per-step accuracy, tiny improvements compound sharply — moving from 99% to 99.5% can double the number of steps an agent completes before failing

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/startup_formation_and_gtm|startup_formation_and_gtm]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/metr|METR]]
