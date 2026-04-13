---
type: source
title: Small Language Models are the Future of Agentic AI
source_id: 01KJTQRK4149XWRK6QFSAHABQX
source_type: paper
authors:
- Peter Belcak
- Greg Heinrich
- Shizhe Diao
- Yonggan Fu
- Xin Dong
- Saurav Muralidharan
- Yingyan Celine Lin
- Pavlo Molchanov
published_at: '2025-06-02 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- finetuning_and_distillation
- multi_agent_coordination
- post_training_methods
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Small Language Models are the Future of Agentic AI

This position paper argues that the dominant singleton-LLM paradigm for agentic AI is structurally misaligned with the actual distribution of agentic subtasks — most of which are repetitive, scoped, and non-conversational — and that sub-10B specialized SLMs are already capable enough, operationally more suitable, and orders of magnitude cheaper for the vast majority of agent invocations. The paper synthesizes capability evidence from existing SLMs, outlines a concrete six-step LLM-to-SLM conversion algorithm, and advocates for heterogeneous agentic architectures where SLMs serve as the default execution layer.

**Authors:** Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, Pavlo Molchanov
**Published:** 2025-06-02
**Type:** Position paper

---

## Motivation

The paper opens with a structural critique of the current agentic AI deployment model. As of writing, more than half of large IT enterprises are actively using AI agents (21% having adopted within the last year), and the sector — valued at USD 5.2bn — is projected to grow to nearly USD 200bn by 2034. Yet the entire paradigm routes agent subtasks through generalist LLMs backed by an estimated USD 57bn in centralized cloud inference infrastructure.

The core misalignment: **LLMs are engineered for open-domain breadth, but the majority of agentic subtasks are repetitive, scoped, and non-conversational**. Routing all invocations through a 70–175B generalist model is economically inefficient (10–30× the latency, energy, and FLOPs of a comparable SLM call) and environmentally unsustainable at scale. The scale is additionally structurally wasteful: in narrow agentic calls, LLM embeddings engage only a fraction of their parameters (high sparsity), meaning the additional capacity is idle but not free.

A secondary problem is behavioral: agentic systems require precise output formatting, reliable tool-call schemas, and zero tolerance for format hallucinations. Generalist LLMs are not optimized for this. Fine-tuned SLMs can be.

---

## The SLM-First Position

The paper defines SLMs as models that fit on a consumer device with practically low single-user inference latency — roughly sub-10B parameters as of 2025. The central claim is not merely that SLMs are cheaper, but that **they are already capable enough** for the vast majority of agentic invocations.

The proposed architecture is **heterogeneous agentic systems**: SLMs as the default execution layer for specialized, repetitive subtasks; LLMs invoked selectively only where genuine open-domain generality is required. This is a "Lego-like" composition of small specialized experts — scaling out instead of scaling up — enabling cheaper debugging, faster deployment, and better alignment with the operational diversity of real-world agentic tasks.

---

## Capability Evidence

The paper synthesizes benchmark results from existing SLMs rather than presenting new experiments:

| Model | Size | Capability demonstrated |
|---|---|---|
| Phi-2 | 2.7B | Commonsense reasoning and code generation on par with 30B models; ~15× faster |
| Phi-3 Small | 7B | Language understanding and reasoning on par with 70B models (same generation) |
| Nemotron-H | 2/4.8/9B | Instruction following and code generation comparable to dense 30B LLMs at order-of-magnitude fewer inference FLOPs |
| Hymba | 1.5B | 3.5× token throughput vs. comparably-sized transformers; outperforms 13B models on instruction following |
| xLAM-2 | 8B | State-of-the-art tool calling, surpassing GPT-4o and Claude 3.5 Sonnet |
| DeepSeek-R1-Distill-Qwen | 7B | Outperforms Claude-3.5-Sonnet-1022 and GPT-4o-0513 on reasoning tasks |
| SmolLM2 | 125M–1.7B | Matches 70B models from two years prior on language understanding, tool calling, and instruction following |
| RETRO | 7.5B | Language modeling performance comparable to GPT-3 (175B) via retrieval augmentation |
| Toolformer | 6.7B | Outperforms GPT-3 (175B) on various tasks via tool/API use |

The underlying trend: **the scaling curve between model size and capability is steepening**. Each generation of SLMs substantially closes the gap with the prior generation's LLMs.

See also: [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/agent_systems|Agent Systems]]

---

## The Conversion Algorithm

The paper proposes a concrete six-step LLM-to-SLM conversion workflow:

1. **Instrument** — log all non-HCI agent calls at the tool/model call interface
2. **Curate** — collect and anonymize 10k–100k task-specific examples; filter by overall workflow success
3. **Cluster** — identify recurring task patterns from prompt distributions
4. **Select** — choose candidate SLMs per task cluster
5. **Specialize** — fine-tune using PEFT (LoRA, QLoRA) or knowledge distillation from the incumbent LLM
6. **Route iteratively** — retrain and update routing as the distribution shifts

A key insight from step 5: the LLM being replaced can serve as a teacher signal via knowledge distillation, making SLM specialization a natural byproduct of existing LLM deployment. Agentic interaction logs filtered by task success are a high-quality organic training set — the pipeline generates its own specialization data.

See also: [[themes/post_training_methods|Post-Training Methods]]

---

## Limitations and Open Questions

The paper is candid about the limitations of its own position:

**On SLM capability:**
- SLMs have weaker general language understanding than same-generation LLMs of equivalent training regime — scaling laws remain operative across broad NLP tasks (translation, open-ended generation, general reasoning)
- SLMs may lack the "semantic hub" mechanism hypothesized in LLMs that enables cross-modal and cross-lingual abstraction; this capacity appears to require scale
- SLM capability claims are benchmark-specific and not validated for real agentic deployments; not all benchmarked capabilities translate to agentic utility

**On deployment:**
- Load balancing for specialized SLM inference endpoints is substantially harder than for generalist LLMs — narrow models have uneven demand patterns, degrading GPU utilization and per-token economics
- The $57B in centralized LLM inference infrastructure creates systemic inertia: tooling, APIs, developer skills, and optimization work all target generalist endpoints
- Infrastructure setup and engineering talent costs for self-hosted SLM inference are systematically omitted from per-token cost comparisons — the real total cost of SLM deployment is substantially higher than headline figures suggest
- SLMs remain insufficient for open-domain dialogue and complex general reasoning; full LLM elimination is infeasible

**On data:**
- SLM specialization requires 10k–100k task-specific examples plus data curation, PII removal, and anonymization pipelines — a non-trivial engineering burden
- The agentic data flywheel operates under the assumption that no confidential data is being processed — an assumption violated in most enterprise deployments, severely limiting organic data collection

**On measurement:**
- SLM development and evaluation is overwhelmingly driven by generalist benchmarks rather than agentic-specific metrics — a systematic measurement gap where models are optimized for the wrong objective

**The paper's own verdict:** "We acknowledge that alternative view AV2 is a valid view, with the exact economical considerations being highly case-specific. We believe that the jury is still out."

---

## Bottlenecks Identified

This paper surfaces three active bottlenecks in the transition to SLM-first agentic architectures:

**Infrastructure inertia** — The $57B capital commitment to centralized LLM inference creates adoption drag that pure technical arguments cannot overcome. Tooling, APIs, and optimization work are exclusively built for generalist endpoints. Horizon: 1–2 years.

**Absent agentic benchmarks** — SLMs are selected and developed on generalist metrics that don't reflect agentic task performance. Without agentic-specific evaluation, practitioners default to generalist LLMs that dominate generalist leaderboards. Horizon: months.

**Load balancing complexity** — Heterogeneous specialized SLM endpoints have uneven, narrower demand patterns than generalist endpoints, making GPU utilization harder to maintain. If utilization is low, per-token costs for SLMs may not undercut LLM API costs. Horizon: months.

The deeper structural bottleneck: **the LLM-centric paradigm itself** — singleton generalist models handling all invocations despite engaging only a fraction of their parameters for any narrow agentic subtask. This is the economic sustainability constraint the paper argues must be resolved for AI agent deployment to scale.

---

## Breakthroughs Noted

Two capability thresholds the paper treats as having been crossed:

- **SLM capability parity on agentic tasks** — Sub-10B specialized SLMs now match or exceed frontier LLMs on tool calling, instruction following, and structured reasoning. The capability gap that justified LLM deployment for these tasks has closed. xLAM-2-8B and DeepSeek-R1-Distill-Qwen-7B are the clearest demonstrations.

- **Hybrid architecture inference efficiency** — Mamba-Transformer architectures (Nemotron-H, Hymba) achieve order-of-magnitude inference FLOP reductions while matching dense LLMs 3–15× their size. This breaks the prior assumption that architecture must scale proportionally with capability.

---

## Connections

- [[themes/agent_systems|Agent Systems]] — the primary domain; the paper directly challenges the singleton-LLM agentic architecture that has become default
- [[themes/ai_business_and_economics|AI Business and Economics]] — the economic argument is central: 10–30× cost reduction per invocation, $57B in infrastructure inertia, total cost of deployment vs. headline per-token pricing
- [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]] — the paper argues the true cost comparison between SLM self-hosting and LLM API usage is systematically misrepresented
- [[themes/finetuning_and_distillation|Finetuning and Distillation]] — the conversion algorithm depends heavily on PEFT and knowledge distillation; the data flywheel from agentic logs is a novel framing of distillation pipelines
- [[themes/multi_agent_coordination|Multi-Agent Coordination]] — heterogeneous SLM/LLM systems require routing, task decomposition, and load balancing that multi-agent coordination frameworks must accommodate
- [[themes/post_training_methods|Post-Training Methods]] — LoRA, QLoRA, DoRA, and distillation from production logs are the enabling techniques for the proposed conversion pipeline

## Key Concepts

- [[entities/deepseek-r1-distill|DeepSeek-R1-Distill]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/lora|LoRA]]
- [[entities/qlora|QLoRA]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
