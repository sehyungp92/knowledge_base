---
type: source
title: 'Superintelligence, Bubbles And Big Bets: AI Investing in 2024 | Matt Turck
  & Aman Kabeer, FirstMark'
source_id: 01KJVSSWSXZKBS0FR7T256NE0Q
source_type: video
authors: []
published_at: '2024-11-08 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- compute_and_hardware
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Superintelligence, Bubbles And Big Bets: AI Investing in 2024 | Matt Turck & Aman Kabeer, FirstMark

FirstMark's Matt Turck and Aman Kabeer survey the AI landscape at the close of 2024, mapping the unprecedented capital flows and valuations reshaping the industry against a more sobering picture of enterprise adoption, stochastic reliability limits, and unresolved questions about whether current investment trajectories can ever be justified by actual business output.

**Authors:** Matt Turck, Aman Kabeer (FirstMark)
**Published:** 2024-11-08
**Type:** video

---

## Overview

This is a capital markets and adoption audit of AI at the two-year mark of the ChatGPT era. The central tension throughout: the private and public markets are pricing in extraordinary future outcomes, while the operational reality for enterprises — slow adoption, underwhelming impact, compounding errors in multi-agent systems — suggests those bets are far from certain. The discussion is most valuable as a structured account of where money is flowing and why, alongside an honest accounting of the gaps between AI's demonstrated capabilities and its actual business penetration.

---

## The Year of Unprecedented Scale

2024 is defined by size. The largest venture capital round in history went to [[entities/openai|OpenAI]] — $6.6 billion at a $157 billion post-money valuation. The largest seed round went to Safe Superintelligence, co-founded by former OpenAI chief scientist Ilya Sutskever, raising ~$1 billion at a $5 billion valuation with no product. The largest acqui-hire ever was Google's $2.7 billion acquisition of the Character AI founders.

The infrastructure commitments are proportionally staggering. Meta, Google, and Amazon are collectively on track to invest $200 billion in AI infrastructure in 2024 alone. SoftBank CEO Masayoshi Son estimated the cumulative capex required to reach superintelligence at approximately $9 trillion. [[entities/xai|xAI]]'s Colossus supercomputer — built in 122 days with a team described as unusually small — came online with 100,000 Nvidia GPUs, with announced plans to scale to 200,000 and eventually 300,000 Blackwell GPUs.

These infrastructure bets carry real-world consequences. The energy and water requirements of new data centers are vast; Colossus alone consumes the annual energy equivalent of 100,000 homes. This has directly accelerated a revival of nuclear power interest in the US, with Microsoft (Three Mile Island), Google, and Amazon all signing nuclear energy deals. See [[themes/compute_and_hardware|Compute and Hardware]] for the broader infrastructure picture.

---

## Market Dynamics and Valuation

### Public Markets

NVIDIA is the central object of market attention — a $96 billion revenue company generating $53 billion in net income, trading at approximately 65x price-to-earnings against a typical mature-company multiple of ~20x. That gap represents an enormous embedded expectation of continued dominance.

Palantir trades at ~30x next-twelve-month revenue with ARR of $2.7 billion and growth in the 20-22% range — the most richly valued software company in the public markets, justified primarily by new logo growth exceeding 40% and specific business segment momentum.

The broader SaaS market tells a different story: median public software valuations sit at 5-6x NTM revenue, below the historical median of ~10x. The top 10 names trade at 14-15x. AI-adjacent names are priced on a completely different logic than the rest of software.

### Private Markets

Private AI valuations are similarly detached from conventional metrics. Sierra, co-founded by Brett Taylor (former Salesforce co-CEO and current OpenAI chairman), is reportedly quadrupling its valuation to $4.5 billion on approximately $20 million ARR — roughly 225x current ARR. This pattern recurs across the private AI landscape.

The divergence between AI and non-AI software markets is structurally notable: the same $3 billion valuation might represent a late-stage SaaS company with $375 million in expected NTM revenue, or an early-stage AI company with a vision and no shipped product. The two populations are priced as if they belong to different universes. Whether AI companies grow into these valuations or public markets rationalize back to conventional metrics is the defining open question in [[themes/ai_business_and_economics|AI Business and Economics]].

### IPO Pipeline

After one of the worst IPO periods in recent memory, AI compute companies are moving toward public markets. Cerebras has filed, though its relationship with G42 is under CFIUS review, potentially delaying the offering. CoreWeave is viewed as a natural candidate. If this cohort of AI hardware companies successfully goes public, it could reopen the IPO window and provide a valuation reference point for the broader sector. See [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]].

---

## Capabilities

### What Is Working

**Token price compression** is the clearest, most consequential development of the past year. The cost per token for GPT-4-class models dropped approximately 90%, dramatically expanding the viable application surface for AI inference. This is one of the few unambiguous positive developments with direct economic implications.

**Inference-time reasoning** has emerged as a distinct capability axis. OpenAI's o1 introduced test-time compute allocation as a mechanism for improving performance on mathematical and logical reasoning — representing a new lever beyond pretraining scale.

**Enterprise-adjacent adoption** is real in narrow domains: more than a quarter of code written at Google is AI-generated before engineer review; Microsoft's AI business is on track to exceed $10 billion in annual revenue run rate; Gemini API calls grew more than 14x in six months. Synthesia represents the commercial viability of AI video generation for enterprise use cases.

**Bottom-up adoption** is broad: 39% of Americans report using ChatGPT, including 28% who use it at work. This is genuine, widespread behavioral change — though it has not yet translated proportionally into business output.

---

## Limitations and Open Questions

### The Stochastic Problem

The most structurally important limitation is that AI model outputs are stochastic, not deterministic. Models do not produce the same answer to the same prompt, and they do not guarantee correctness. For automation at scale, this is not a minor inconvenience — it is a fundamental constraint on deployment in any high-consequence, high-reliability context.

This limitation compounds badly in multi-agent systems: when multiple autonomous agents are chained together, error rates compound rather than cancel. The result is that complex, multi-step autonomous workflows — the promised land of agentic AI — remain difficult to deploy reliably outside narrow, forgiving contexts.

### The Adoption-Impact Gap

The gap between adoption and impact is striking. A FirstMark survey found that 64% of CTOs had adopted AI in some form in the past 12 months — and 62% of those adopters reported being underwhelmed by the actual impact on their organization. A US Census Bureau statistic reinforces this: only 5% of American businesses report using AI to actually produce goods or services.

This is not a signal that AI is failing; it is a signal that the translation from tool adoption to business output is harder and slower than the investment narrative implies. The bottleneck appears to be the difficulty of applying AI to industry-specific complex problems beyond search and basic automation. Broad-deployment success in one domain (customer service chatbots, code completion) does not generalize automatically to the next. See [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]].

### The Scaling Law Question

No one knows whether the exponential performance improvements from increased compute and data will continue. This is explicitly acknowledged as the defining uncertainty: everyone has an opinion, but the empirical question is genuinely open. Given that the entire infrastructure investment thesis depends on continued scaling, this uncertainty underpins every valuation discussed above.

### Competitive Sustainability

Frontier model releases are occurring so frequently that competitive advantages are difficult to establish or measure. Individual models are best-in-class for weeks before being surpassed. For companies whose business models depend on differentiated model capability, this creates a structurally difficult environment. Specialized tooling and frameworks face a related problem: frameworks popular one year become unpopular the next, creating adoption risk throughout the stack.

### Vector Database Commoditization

General-purpose databases have added vector search capabilities to the point where they are "good enough for most use cases," eroding the differentiated value proposition of specialized vector databases. This is a case study in infrastructure commoditization under competitive pressure — likely to repeat in other specialized AI tooling categories.

---

## Landscape Contributions

### Key Bottlenecks

| Bottleneck | Horizon | Blocking |
|---|---|---|
| Scaling law trajectory uncertainty | Unknown | Long-term investment viability |
| Supply-demand timing mismatch in compute | 1-2 years | Infrastructure ROI |
| Enterprise AI value capture | 1-2 years | Sustained enterprise spending |
| Multi-agent error compounding | 1-2 years | Agentic system deployment |
| Complex enterprise workflow integration | 1-2 years | Beyond low-hanging fruit |
| Frontier model competitive sustainability | 1-2 years | Durable competitive advantage |

### Key Breakthroughs

- **90% token price reduction for frontier models** — structural cost compression enabling economically viable inference at scale (significance: major)
- **Inference-time reasoning** — test-time compute as a distinct axis of capability improvement, separate from pretraining scale (significance: notable)

---

## Connections

- [[themes/ai_business_and_economics|AI Business and Economics]] — primary frame for interpreting valuation divergences and adoption gaps
- [[themes/ai_market_dynamics|AI Market Dynamics]] — competitive dynamics among frontier model providers
- [[themes/compute_and_hardware|Compute and Hardware]] — infrastructure investment, energy constraints, and nuclear revival
- [[themes/startup_and_investment|Startup and Investment]] — record-setting rounds and the valuation logic of pre-product AI companies
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]] — IPO pipeline and private market dynamics
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]] — enterprise adoption challenges and the search for domain-specific AI impact

## Key Concepts

- [[entities/artificial-general-intelligence-agi|Artificial General Intelligence (AGI)]]
- [[entities/artificial-superintelligence-asi|Artificial Superintelligence (ASI)]]
- [[entities/gemini|Gemini]]
- [[entities/github-copilot|GitHub Copilot]]
- [[entities/inference-time-reasoning|Inference-Time Reasoning]]
- [[entities/mlops|MLOps]]
- [[entities/multi-agent-system|Multi-Agent System]]
- [[entities/scaling-laws|Scaling Laws]]
