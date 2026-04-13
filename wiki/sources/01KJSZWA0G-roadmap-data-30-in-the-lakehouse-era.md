---
type: source
title: 'Roadmap: Data 3.0 in the Lakehouse Era'
source_id: 01KJSZWA0GH70T66PMRGVHAN4H
source_type: article
authors: []
published_at: '2025-03-25 00:00:00'
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
# Roadmap: Data 3.0 in the Lakehouse Era

**Authors:** 
**Published:** 2025-03-25 00:00:00
**Type:** article

## Analysis

# Roadmap: Data 3.0 in the Lakehouse Era
2025-03-25 · article
https://www.bvp.com/atlas/roadmap-data-3-0-in-the-lakehouse-era

---

## Briefing

**The data lakehouse architecture — combining the governance of cloud warehouses with the flexibility of data lakes via open table formats — represents a foundational architectural shift, not an incremental upgrade, that is breaking vendor lock-in and enabling the interoperability AI workloads demand. Legacy data stacks are structurally incompatible with AI-era requirements (unstructured data at scale, real-time multimodal pipelines, agentic workflows), creating a $350B+ market undergoing a generational replacement cycle. BVP argues the next wave of multi-billion-dollar data infrastructure companies will be built on lakehouse-native primitives rather than incrementally improved modern data stack tools.**

### Key Takeaways
1. **The lakehouse is a paradigm replacement, not an upgrade** — it rewires how enterprise data infrastructure operates by unifying warehouse governance with data lake flexibility in a single interoperable architecture, ending the costly pattern of copying data between systems.
2. **Open table formats (Delta Lake, Iceberg, Hudi) are the enabling layer** — ACID compliance, schema evolution, time travel, and scalable metadata management were the missing primitives that made the lakehouse viable; Iceberg had a breakout 2024 including Databricks' acquisition of Tabular.
3. **AI workloads expose structural limits in legacy architectures** — real-time, multimodal, and composable data processing requirements cannot be retrofitted onto batch-first warehouse or lake designs, making migration a necessity rather than a preference.
4. **Metadata is moving from "reflection of truth" to "source of truth"** — in the lakehouse era, the metadata/catalog layer is the governance control plane, and companies must now track lineage and access not just for employees but for AI agents.
5. **Vendor lock-in is the critical enterprise pain point** — high costs set during ZIRP pricing, slow AI adaptation from incumbents, and the interoperability unlocked by open formats are converging to make unbundling from Snowflake/Databricks commercially viable for the first time.
6. **Real-time and streaming will displace batch as the dominant pipeline paradigm** — "shift left" toward the time of action is driven by AI inference demands, with managed platforms like Chalk making real-time feature serving accessible without operational complexity.
7. **Anthropic's MCP is positioned as a standardization layer for AI-data integration** — by preserving context relationships across queries, transformations, and outputs with governance baked in, MCP could become infrastructure for agentic data workflows.
8. **The boundary between data engineering and software engineering is collapsing** — AI-stack developer is the fastest-growing job title globally; full-stack AI proficiency is now an organizational requirement, not a specialty.
9. **Open source in data has overtaken proprietary tooling in momentum** — contributions to data repositories grew at 37% CAGR since 2020 vs. 18% for general software; enterprises adopt open source partly because LLMs are better trained on it, creating a Copilot-assistance advantage.
10. **Enterprise data infrastructure spend has nearly doubled in five years** — $180B in 2019 to $350B in 2024, with hyperscalers pouring trillions into AI-optimized infrastructure, signaling both maturity and continued expansion.
11. **Code-native tooling is replacing drag-and-drop ETL** — brittle low-code pipelines cannot handle AI-era volume and complexity; code-native tools become composable building blocks for turning manual workflows into agentic ones.
12. **AI-generated content is itself a data infrastructure stress test** — ChatGPT's 100M monthly active users producing a "tsunami" of text and visual content is compounding the unstructured data volume challenge enterprises must now architect around.

---

### The Architectural Shift: From Modern Data Stack to Lakehouse

- **The modern data stack (Data 2.0) is being superseded by the lakehouse paradigm (Data 3.0)**, just as the on-premise warehouse was superseded by cloud-native architectures — this is the third generational transition in ~50 years.
  - Data 1.0: traditional on-premise data warehouses.
  - Data 2.0: cloud data warehouses (Snowflake, BigQuery, Redshift) and data lakes — powerful but siloed.
  - Data 3.0: the lakehouse, combining both paradigms into a unified, interoperable architecture.
- The core problem the lakehouse solves is **data redundancy from copying**: AI/ML workflows consume directly from the data lake, while analytics workflows consume from the warehouse — enterprises were maintaining duplicate data in two systems with separate governance regimes.
- **The lakehouse is not a product from a single vendor; it is an architectural paradigm** built on open standards — open table formats, open storage formats (Parquet, ORC), and open data access protocols (Arrow).
- The "deconstructured database" concept, discussed as early as the late 2010s, is now materializing as a practical enterprise reality rather than a theoretical unbundling thesis.

---

### Open Table Formats: The Enabling Primitive Layer

- **Delta Lake, Apache Iceberg, and Apache Hudi are the foundational abstraction** that makes the lakehouse viable — they present underlying files as a single queryable "table" accessible through a standard API.
- Key capabilities unlocked by open table formats:
  - **ACID compliance**: atomicity, consistency, isolation, and durability — the same guarantees enterprises expect from relational databases, now available over object storage.
  - **Unified batch and streaming pipeline support**: eliminates the need for separate processing architectures for historical vs. real-time data.
  - **Schema and partition evolution**: modify data structures without downtime, critical for fast-moving AI product 

## Key Claims

1. Enterprise investment in data infrastructure has nearly doubled in five years, growing from $180 billion in 2019 to $350 billion in 2024.
2. Databricks has reached profitability, signaling a mature yet rapidly evolving data infrastructure market.
3. Snowflake and Databricks each currently generate over $3 billion in annual revenue in the compute and query layer.
4. AI workloads require infrastructure that supports structured, semi-structured, and unstructured data with high performance, scalability, and governance — a requirement legacy architectures cannot meet
5. Unstructured data is being generated at unprecedented speed in the AI era, driven in part by AI-generated content from ChatGPT's 100 million monthly active users.
6. AI workloads require real-time, multimodal, and composable data processing which traditional data architectures are not purpose-built for.
7. Data redundancy from copying data between data lakes and data warehouses is an unnecessary expense enterprises are seeking to eliminate.
8. Most AI/ML workflows consume directly from the data lake, which unlike warehouses typically lacks baked-in governance.
9. Vendor lock-in concerns have intensified in the AI era due to high costs of existing services priced during the ZIRP years and slow adaptation of traditional providers to AI workloads.
10. Open table formats (Delta Lake, Iceberg, Hudi) enable ACID compliance, batch and streaming pipelines, schema evolution, time travel, and scalable metadata management.

## Capabilities

- Data lakehouse architecture unifying structured, semi-structured, and unstructured data processing with ACID compliance, streaming pipelines, schema evolution, time travel, and scalable metadata management in a single interoperable platform
- Open table formats (Delta Lake, Iceberg, Hudi) enabling ACID compliance, batch and streaming pipelines, schema/partition evolution, time travel, and scalable metadata on cloud object storage — decoupling compute from storage
- Model Context Protocol (MCP) providing a standardized framework for context-aware AI interactions with enterprise data infrastructure, preserving relationships between queries, transformations, and outputs while maintaining governance and security
- Code-native data pipeline orchestration tools enabling production-scale AI workflow automation with built-in scheduling, monitoring, and observability — serving as building blocks for agentic data workflows
- Unified data catalogs providing lineage tracking and governance visibility across both human and AI agent data access in hybrid lakehouse and traditional architectures
- Managed real-time inference platforms enabling instant, data-rich AI decision-making (e.g. credit approvals) by serving live features at low latency without requiring enterprises to manage streaming infrastructure directly

## Limitations

- Legacy cloud data warehouses and data lakes cannot support the scale, speed, and complexity of modern AI workloads — they are not purpose-built for real-time, multimodal, or composable data processing
- Most AI/ML workflows consuming directly from data lakes lack baked-in governance, creating compliance and oversight gaps as AI-driven products expand the scope of what data is accessed and how
- Traditional data infrastructure requires manual context management across queries and transformations — an approach that is impractical or impossible at AI workload scale
- Drag-and-drop ETL and low-code data pipeline tools are too brittle, expensive, and inefficient for the volume and complexity of AI-era data workflows — failing at the scale required for production AI applications
- Enterprise data governance frameworks were not designed for AI agent access patterns — lineage records, audit trails, and access controls must now cover autonomous agents, a use case current tooling does not address
- Apache Flink stream processing is too operationally complex for most enterprises to manage directly, blocking adoption of continuous model training and real-time inference pipelines without significant platform engineering investment
- Data redundancy from copying data between lakes and warehouses creates compounding cost and governance overhead — a structural inefficiency that worsens as data volumes and compliance requirements grow in the AI era
- Vendor lock-in in incumbent data infrastructure platforms is intensifying as AI-era demands outpace legacy provider adaptation, while services priced during zero-interest-rate years are now economically untenable
- Closed-source data technologies receive structurally weaker LLM coding assistance due to underrepresentation in model training data, creating an emergent productivity disadvantage in AI-first development workflows
- Metadata in legacy systems was updated indirectly and asynchronously — a passive 'reflection of truth' model that cannot support real-time governance, optimisation, or agentic orchestration required in AI workloads
- No interoperability standard existed between traditional data stack components and AI-specific tools like vector databases, creating integration friction that slows enterprise AI deployment
- AI application developers and ML engineers face high cognitive overhead in identifying best-fit infrastructure solutions amid a rapidly proliferating vendor landscape — discovery friction slows adoption of genuinely better tools

## Bottlenecks

- Enterprise data governance tooling not designed for AI agent access — organizations lack lineage, audit, and access control mechanisms needed to govern programmatic agent data consumption at scale
- Lack of interoperability between traditional data stack infrastructure and AI-native tools (vector databases, streaming engines) creates architectural fragmentation blocking unified support for both analytics and AI inference workloads
- Batch-oriented enterprise data architectures cannot deliver real-time, low-latency feature serving for AI inference — the gap between historical batch data and live signals is unresolved for most production AI deployments
- Passive, asynchronous metadata management in legacy systems blocks real-time governance enforcement, automated query optimisation, and agentic orchestration that AI workloads require

## Breakthroughs

- Open table formats (Apache Iceberg, Delta Lake, Hudi) have established a universally adopted open standard that decouples compute from storage, enabling any query engine to read any data without vendor-specific formats or migration
- Anthropic's Model Context Protocol (MCP) establishes a standardized interface between AI agents and enterprise data infrastructure, enabling context-preserving, governance-compliant AI interactions across heterogeneous data sources

## Themes

- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/compute_and_hardware|compute_and_hardware]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]
