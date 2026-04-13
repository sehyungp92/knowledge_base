# Knowledge Base

A personal knowledge engine that transforms passive reading into a constantly evolving, structured understanding of the current state of AI — organised by themes and subthemes that overlap and connect deeply to one another. Ingest sources (papers, articles, videos, podcasts), extract claims with evidence, surface limitations that are often only implicit in the original material, trace the implications of breakthroughs across domains, anticipate what those breakthroughs may enable, and identify where the next ones will come from based on the technological bottlenecks that remain. The goal is a living model of current capabilities, hidden limitations, and emerging trajectories — queryable, auditable, and sharpened by everything you read.

## How It Works

The system operates across four layers:

**Knowledge Graph** — what sources say. Claims extracted with verbatim evidence, concepts linked by typed semantic edges (`builds_on`, `contrasts_with`, `enables`, `alternative_to`, `specializes`, `component_of`), and weighted relationships between sources. Graph algorithms (betweenness centrality, PageRank, Louvain community detection) identify structurally important concepts, bridge nodes between themes, and cluster boundaries.

**Landscape Model** — what is true about AI right now. A temporal, evidence-traced representation organized by themes (as a DAG), tracking capabilities (with maturity), limitations (with type and trajectory), bottlenecks (with resolution horizons), breakthroughs (with implication cascades), anticipations (trackable predictions), and cross-theme implications.

**Belief System** — what you think about what is true. Tracked positions with confidence levels, supporting/opposing evidence, and history. The system surfaces conflicts and challenges stale positions.

**Wiki** — compiled reasoning, human-readable. Over 1,200 markdown pages (themes, entities, sources, syntheses, questions, beliefs) that compile raw graph and landscape data into navigable, interlinked narratives. The wiki is the primary context surface for LLM reasoning — handlers read wiki pages first, falling back to database queries only when pages are stale or missing. Pages are filed automatically after every `/save`, `/reflect`, `/challenge`, and `/implications`, and maintained by a deterministic index that tracks cross-references, staleness, and structural health without LLM calls.

## Architecture

Local-first. No cloud dependencies.

```
Adapters (Telegram, Discord, Web, Heartbeat, YouTube, News)
    │
    ▼
  Gateway ─── SQLite Job Queue
    │
    ▼
Skills Registry ─── 25+ commands
    │
    ▼
Agent Executor ─── Multi-provider (Claude, Codex, Z.AI, OpenRouter)
    │
    ▼
PostgreSQL + pgvector + FTS ─── File Library (library/{source_id}/)
```

- **Database:** PostgreSQL 16 with pgvector for embeddings and pg_trgm for full-text search
- **Embeddings:** Ollama (local, 768-dim vectors)
- **Agent brain:** Claude Code CLI (Max subscription), with fallback to OpenRouter
- **Job queue:** SQLite with session management and retry logic
- **Frontend:** FastAPI backend + Next.js/React web UI

## Setup

### Prerequisites

- Python 3.11+
- Docker (for PostgreSQL)
- [Ollama](https://ollama.ai) running locally
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (or alternative provider)
- Node.js 18+ (for the web UI)

### Install

```bash
# Clone and enter the project
cd knowledge_base

# Start PostgreSQL with pgvector
docker compose -f docker/docker-compose.yml up -d

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials (Telegram token, API keys, etc.)

# Initialize the database
python db/migrate.py

# Seed the theme taxonomy
python db/seed_themes.py
```

### Run

```bash
# Start the gateway (main entry point)
python gateway/main.py
```

This starts the job queue, adapter listeners, and the web API server. Connect via Telegram, Discord, or the web UI at `http://localhost:8000`.

For the web frontend:

```bash
cd webapp/web
npm install
npm run dev
```

## Commands

### Core Ingestion

| Command | Description |
|---------|-------------|
| `/save <url>` | Ingest a source — extracts claims, landscape signals, implications |
| `/summarise <url>` | Preview a source summary before committing to save |
| `/delete <source>` | Remove a source and all dependent data |

> `/save https://arxiv.org/abs/2401.04088` — fetches the paper, classifies it under relevant themes, extracts 15–30 claims with verbatim evidence, writes a structured deep summary, detects two new capabilities and a limitation, links it to an open bottleneck on inference cost, and files everything under `library/01KJ…/`. 

### Knowledge Exploration

| Command | Description |
|---------|-------------|
| `/ask <question>` | Grounded Q&A over your library |
| `/map <concept>` | Show a concept's neighborhood in the knowledge graph |
| `/path <source> <source>` | Explain the connection path between two sources |
| `/contradictions [topic]` | Surface conflicting claims |
| `/synthesis <topic>` | Multi-source consolidated report |

> `/ask "What evidence exists that chain-of-thought hurts performance?"` — retrieves the 8 most relevant sources via hybrid search, synthesizes an answer citing specific claims with evidence snippets, and flags where your sources disagree.
>
> `/synthesis "test-time compute"` — pulls every source touching test-time compute, groups claims by sub-topic, identifies where authors agree, where they contradict, and what the open questions are. Not a summary of summaries — a structured argument map grounded in your actual library.
>
> `/path "Scaling Monosemanticity" "Constitutional AI"` — traces the shortest connection through shared concepts, co-cited claims, and thematic overlap, explaining *why* two seemingly unrelated papers are linked in your knowledge graph.

### Landscape Model

| Command | Description |
|---------|-------------|
| `/landscape [theme]` | View current state of AI for a theme or full overview |
| `/bottlenecks [theme]` | Bottleneck analysis with resolution horizons |
| `/anticipate [query]` | Generate, review, or calibrate predictions |
| `/implications <source> [thesis]` | Deep cross-theme impact analysis |
| `/changelog [period]` | View how the landscape model changed over time |
| `/gaps [theme]` | Identify coverage gaps and suggest reading |
| `/themes` | Review and approve proposed new themes |

> `/landscape robotics` — returns a temporal narrative: where robotics stood 3 months ago, what shifted (sim-to-real transfer breakthroughs, new manipulation benchmarks), which bottlenecks are easing, which anticipations gained evidence. Not a Wikipedia summary — a trajectory derived from sources you've actually read.
>
> `/bottlenecks reasoning` — lists every bottleneck tagged under reasoning, each with its current status, linked breakthroughs that might resolve it, estimated resolution horizon, and the specific sources that established the bottleneck. You see "long-horizon planning reliability" is *shifting* because three recent papers provided partial evidence.
>
> `/implications "GPT-4o system card" "multimodal models will compress the traditional NLP-CV pipeline boundary"` — takes your thesis and traces its cross-theme consequences: what it means for tooling, for evaluation benchmarks, for startups building on modality-specific APIs. Each implication is grounded in claims from your library.
>
> `/gaps multimodal_models` — shows you have 12 sources on vision-language models but nothing on audio-language integration, suggests 3 recent papers that would fill the gap, and ranks them by how many open questions they'd address.

### Human Enrichment

| Command | Description |
|---------|-------------|
| `/enrich <source>` | Correct, supplement, or reinterpret extractions |
| `/challenge <entity> <id>` | Challenge a landscape entity or belief |
| `/beliefs [query]` | View and update tracked positions |

> `/enrich "Attention Is All You Need"` — you noticed the system missed an implicit limitation: the paper's efficiency claims only hold for sequence lengths under 512. You add this, the system classifies it as a "controlled conditions" limitation, links it to the context-length bottleneck, and marks it as human-contributed so it's never overwritten by re-extraction.
>
> `/challenge bottleneck 42` — you think the "data quality for RLHF" bottleneck is overstated. You submit your reasoning, the system retrieves evidence for and against from your library, records the challenge with resolution, and adjusts the bottleneck's confidence. Your disagreement becomes part of the model.

### Idea Generation

| Command | Description |
|---------|-------------|
| `/reflect <source> [query]` | Generate ideas via multi-agent tournament |
| `/ideas [query]` | List, rate, develop, and track generated ideas |

> `/reflect "Scaling Monosemanticity" "applications beyond interpretability"` — retrieves neighboring sources, generates 12 candidate ideas across synthesis/transfer/contradiction/extension strategies, kills 4 that are too similar to things already in your library, runs a critique-debate tournament on the survivors, and returns 3 ranked ideas — each citing specific claims from specific papers, with a novelty score and development path.

### Utilities

| Command | Description |
|---------|-------------|
| `/next [query]` | Prioritized reading recommendations |
| `/status [job_id]` | Check status of a running job |
| `/provider [name]` | Show or switch the active LLM provider |
| `/model [tier]` | Show or switch the global model tier |

> `/next "I want to understand why RL is making a comeback"` — ranks unread sources by relevance to your query, weighted by how many open bottlenecks and anticipations they'd inform, and how many knowledge graph edges they'd create. The top recommendation isn't just topically relevant — it's the paper that would most improve your model's coverage.

## Ingestion Pipeline

When you `/save` a URL:

```
URL
 ├─ Fetch & parse (article, arXiv, YouTube, podcast, PDF)
 │   └─ Audio/video: domain-aware Whisper transcription (corpus concepts as initial prompt)
 ├─ Theme classification
 │
 ├─ Phase 1 (parallel):
 │   ├─ Claims + evidence extraction
 │   ├─ Deep theme-aware summary
 │   ├─ Landscape signals: capabilities, limitations, bottlenecks, breakthroughs
 │   └─ Cross-theme implications
 │
 ├─ Phase 2 (conditional):
 │   ├─ Match against open anticipations
 │   ├─ Propagate breakthrough effects to bottlenecks
 │   ├─ Check against tracked beliefs
 │   └─ File wiki pages (source, entity, synthesis)
 │
 └─ Phase 3 — Post-processing (5-step pipeline):
     ├─ Source edges: compute weighted connections to existing sources
     ├─ Concept edges: classify typed semantic relationships (builds_on, contrasts_with, etc.)
     ├─ Graph metrics: incremental betweenness centrality for affected neighborhoods
     ├─ State summaries: regenerate landscape narratives for impacted themes
     └─ Anticipation matching: review open predictions against new evidence
```

## Idea Generation Pipeline

When you `/reflect` on a source:

```
Source
 ├─ Retrieve neighbors (hybrid search + graph traversal)
 ├─ Generate candidates across 6 strategies:
 │   synthesis, transfer, contradiction, extension, bottleneck, implications
 ├─ Novelty gate (embedding similarity + Jaccard fallback)
 ├─ Critique (individual agent review)
 ├─ Debate (two-tier: deep panel for top 40%, single-turn for rest)
 ├─ Evolve weak candidates
 └─ Rank (landscape context + belief weighting)
```

Every idea must cite specific claims from specific sources. No idea passes without demonstrating it isn't a restatement of something already in the library.

## Graph Intelligence

Every handler that reasons over the knowledge base can inject structured graph context alongside wiki narratives. The shared `query_graph_context()` function assembles a compact block containing:

- **Bridge concepts** — high-betweenness nodes that connect otherwise distant themes, surfacing non-obvious structural relationships in the corpus
- **Concept edges** — typed semantic relationships between concepts (`builds_on`, `contrasts_with`, `enables`, `alternative_to`, `specializes`, `component_of`), classified by LLM during post-processing for high-confidence co-occurring concept pairs
- **Cross-theme implications** — how a development in one theme affects another, with provenance and confidence
- **Contradictions** — conflicting claims between sources, detected via claim-level analysis
- **Suggested questions** — graph-topology-driven inquiry ("Why does X bridge themes Y and Z?", "High-centrality concepts lacking wiki pages")

Graph context is budget-aware — each handler specifies a character budget, and the formatter prioritizes the most structurally informative signals. This unified composition replaces the previous fragmentation where some handlers had graph access, others had wiki access, and none combined both coherently.

### Epistemic Status Vocabulary

Every claim and landscape entity carries a human-readable confidence tier derived from its provenance and scoring:

| Tier | Meaning |
|------|---------|
| `ESTABLISHED` | Multiple corroborating sources, high confidence |
| `EXTRACTED` | Directly stated in a single source |
| `INFERRED` | Derived from evidence patterns, not explicitly stated |
| `AMBIGUOUS` | Conflicting evidence or unclear provenance |
| `SPECULATIVE` | Low confidence, limited evidence |

## Wiki as Compiled Reasoning

The wiki is not documentation — it is the system's primary compiled reasoning surface. Raw database rows (claims, edges, metrics) are compiled into navigable markdown pages that LLM handlers read as context before generating responses.

**Page types and their role:**

| Type | Count | Purpose |
|------|-------|---------|
| Themes | 82 | Temporal narratives of how each AI theme evolved, with state summaries |
| Entities | 504 | Concept-level pages compiling all claims, edges, and landscape signals for a single concept |
| Sources | 614 | Per-source pages with extracted claims, summary, and cross-references |
| Syntheses | — | Multi-source consolidated analyses filed after `/reflect` topic mode |
| Questions | — | Open questions generated from graph topology and coverage gaps |
| Beliefs | — | Tracked positions with evidence for/against and challenge history |

**Context assembly:** When a handler like `/ask` or `/reflect` needs context, it calls `gather_wiki_context()` which reads theme narratives, entity pages for relevant concepts, source pages for cited sources, and any synthesis/belief/question pages matching the query scope. This wiki-first retrieval replaces direct database queries for most reasoning paths, providing richer, pre-compiled context with cross-references already resolved.

**Automatic maintenance:** A deterministic wiki index tracks every page's cross-references, staleness, and structural integrity without LLM calls. Pages are filed automatically after ingestion and analysis. Stale pages are flagged and regenerated during heartbeat cycles.

## Project Structure

```
knowledge_base/
├── adapters/          # Channel integrations (Telegram, Discord, Heartbeat, YouTube, News)
├── agents/            # Executor, tournament, debate, critique, novelty gate
├── db/                # Schema, migrations, seed data
├── docker/            # Docker Compose for PostgreSQL
├── gateway/           # Dispatcher, job queue, skill handlers
├── ingest/            # Source parsers, extractors, post-processors
├── library/           # File-based source storage (library/{source_id}/)
├── memory/            # Markdown memory files (human-auditable)
├── notify/            # Notification emitters
├── prompts/           # Claude instruction prompts for each skill
├── reading_app/       # Core runtime: config, DB pool, embeddings, scheduler
├── retrieval/         # Hybrid search, graph context, wiki retrieval, landscape queries
│   ├── graph_context.py   # Shared graph intelligence (bridge concepts, concept edges, questions)
│   ├── wiki_retrieval.py  # Wiki-first context assembly (themes, entities, sources, syntheses)
│   ├── wiki_writer.py     # Wiki page generation and filing (6 page types)
│   ├── wiki_index.py      # Deterministic wiki health and cross-reference maintenance
│   └── ...                # hybrid.py, graph.py, graph_algorithms.py, lenses.py, landscape.py
├── scripts/           # Bulk ingestion, reprocessing, edge computation
├── skills/            # Skills registry (YAML)
├── tests/             # Pytest test suite
├── webapp/
│   ├── api/           # FastAPI backend (landscape, search, graph, beliefs, etc.)
│   └── web/           # Next.js frontend
├── wiki/              # Compiled reasoning pages (1,200+ markdown files)
│   ├── themes/        # Theme narratives with state summaries
│   ├── entities/      # Concept-level pages with claims, edges, signals
│   ├── sources/       # Per-source pages with extractions and cross-references
│   ├── syntheses/     # Multi-source consolidated analyses
│   ├── questions/     # Open questions from graph topology and gaps
│   └── beliefs/       # Tracked positions with evidence and challenges
└── .env.example       # Environment configuration template
```

## Lineage: What This Owes to OpenClaw

Knowledge Base's architecture is directly descended from [OpenClaw](https://github.com/openclaw/openclaw), the open-source personal AI agent system. Not as a dependency — nothing is imported — but as a structural blueprint. The patterns that matter most are the ones OpenClaw got right about how a personal agent should relate to its operator.

**The gateway-adapter-skills-executor pipeline.** OpenClaw demonstrated that a personal agent doesn't need a framework hierarchy. It needs a tight core loop: messages arrive through adapters, a dispatcher routes them to skills by pattern match, skills invoke an executor, results flow back. Knowledge Base adopts this verbatim — `gateway/main.py` → `adapters/` → `skills/` → `agents/executor.py` — because for a system that must stay comprehensible to one person, a linear pipeline beats a graph of microservices. Every message has one path through the system.

**Heartbeat as a first-class adapter, not a cron job.** OpenClaw's most counterintuitive design choice was treating proactive background work the same as user messages — another adapter that emits events into the same queue. Knowledge Base inherits this directly. The `HeartbeatAdapter` fires scheduled events (with quiet-hour awareness) that enter the exact same dispatch path as a Telegram message. This means the system can autonomously check for stale anticipations, regenerate landscape summaries, or compute new edges without any separate scheduling infrastructure. One path, whether the trigger is human or temporal.

**Markdown memory as the human-audit interface.** OpenClaw's `SOUL.md` and `AGENTS.md` established that agent state should be version-controlled, diffable, readable prose — not opaque database rows. Knowledge Base extends this into its core identity: the `library/{source_id}/` file tree (deep summaries, claim extractions, metadata as YAML) is designed so that a human can open any source folder and understand what the system extracted, verify it, and correct it. The landscape model lives in the database for queryability, but the evidence chain is always traceable to human-readable files.

**Provider-aware execution with cost visibility.** OpenClaw's multi-backend executor — supporting various model providers through a common interface — directly informed Knowledge Base's `ClaudeExecutor`, which wraps Claude CLI, OpenRouter, Codex, and Z.AI behind a unified `ExecutionResult` that tracks tokens and cost. For a system that makes hundreds of LLM calls per ingestion cycle across different model tiers, cost observability isn't optional.

**The deeper inheritance is philosophical.** OpenClaw's `VISION.md` argues that a personal agent should be local-first, observable, pluggable at boundaries but opinionated in its core loop, and designed so the operator can always see what happened and why. Knowledge Base takes this further: every claim has a verbatim evidence snippet, every landscape entity has provenance, every human enrichment is attributed separately from automated extraction. The system is not just observable — it is *auditable at the epistemic level*. That insistence on transparency traces directly back to OpenClaw's conviction that personal agents must be legible to the people who depend on them.

## Lineage: What This Owes to Hermes

Where OpenClaw provided the structural blueprint, [Hermes](https://github.com/plastic-labs/hermes) provided the insight that a knowledge system must learn from its own operation — that the critical gap isn't ingestion or extraction but *meta-learning*: the ability to learn not just about AI, but about how well it learns about AI, and to use that self-knowledge to improve future outputs. Hermes is an autonomous agent with active memory — it doesn't just store information, it watches how that information is used, corrected, and valued, then feeds those signals back into future behavior. Knowledge Base had sophisticated ingestion and extraction pipelines but no such feedback loops. It could extract capabilities and limitations from a paper, but it couldn't learn from a user correcting a missed limitation to extract similar ones better next time. It could score state summaries for quality, but it discarded those scores immediately — never tracking whether summaries were improving or degrading over time. Hermes showed what was missing: the closed loops that turn a static pipeline into a system that gets better with use.

**Correction pairs as few-shot calibration.** When a user corrects an extraction via `/enrich` or `/challenge`, that correction is the highest-signal feedback the system can receive. Hermes demonstrated that storing correction pairs (what the system produced vs. what the user wanted) and injecting them as few-shot examples into future prompts creates a closed learning loop. Knowledge Base now persists every correction — missed entities, spurious extractions, reclassifications — in `correction_examples` and injects the most relevant ones into `LANDSCAPE_EXTRACTION_PROMPT`. The extraction pipeline gets better with use, calibrated by the operator's actual standards rather than generic instructions.

**Active memory that populates itself.** Hermes's memory system doesn't wait to be told what to remember — it watches interactions and extracts signals about user preferences, research focus, and working patterns. Knowledge Base adapts this via `memory_signals.py`: after every substantive interaction (`/save`, `/enrich`, `/ask`, `/challenge`), a lightweight Haiku call extracts memory-worthy signals and writes them to `memory/memory.md` with bounded sections and duplicate detection. The system learns that you care about robotics embodiment, prefer concise responses, and always want limitation trajectories — without being told explicitly.

**Quality metrics as the substrate for self-improvement.** Hermes tracks its own performance persistently, enabling trend analysis over time. Knowledge Base now does the same: state summary quality scores (temporal language, specificity, narrative flow), source extraction completeness, and tournament strategy effectiveness are all persisted to `quality_metrics`. This turns "did the system get better?" from a subjective impression into a queryable trend. When a weekly heartbeat runs, it can report whether extraction quality is improving, which tournament strategies produce the best ideas, and which themes have thin coverage.

**Entity staleness as epistemic hygiene.** A landscape model that never forgets is a landscape model that lies. Capabilities described in a 2023 paper may have been superseded; bottlenecks may have been resolved. Hermes's approach to memory lifecycle — where information decays without reinforcement — inspired the staleness decay system. Every capability, limitation, and bottleneck now has an exponentially decaying `staleness_score` based on time since last corroboration. Entities that are re-confirmed during `/save` get refreshed; those that aren't gradually fade, ensuring the landscape model reflects current understanding rather than accumulated history.

**The deeper lesson is that a knowledge system that doesn't learn from corrections is just a pipeline.** OpenClaw gave Knowledge Base its skeleton — the gateway, the adapters, the dispatch loop. Hermes gave it proprioception: the ability to sense its own performance, remember what its operator values, and improve its extractions based on feedback rather than just instructions. The combination — a linear, auditable pipeline that also closes learning loops — is what makes the system genuinely useful over months of accumulated sources rather than merely functional.

## Lineage: What This Owes to Graphify

[Graphify](https://github.com/sehnryr/graphify) is a code-understanding tool that builds knowledge graphs from codebases — analyzing structure, detecting clusters, identifying bridge nodes, and generating navigable reports. Knowledge Base adapted several of its most effective patterns for a fundamentally different domain: epistemically uncertain, temporally evolving knowledge about AI.

**Shared graph context as a composable primitive.** Graphify's core insight was that graph intelligence shouldn't be scattered across individual features — it should be a single, queryable context block that any analysis can consume. Knowledge Base adopted this directly: `query_graph_context()` assembles bridge concepts, concept edges, cross-theme implications, contradictions, and suggested questions into a compact `GraphContext` dataclass that any handler can inject into its LLM prompt alongside wiki narratives. Before this, graph intelligence was fragmented — some handlers queried the graph directly, others used analytical lenses, and none composed both coherently.

**Typed concept-level edges.** Graphify models explicit relationships between code entities (calls, imports, inherits). Knowledge Base adapted this into typed semantic edges between concepts — `builds_on`, `contrasts_with`, `enables`, `alternative_to`, `specializes`, `component_of` — classified by LLM during post-processing for high-confidence co-occurring concept pairs. These relationships are structurally different from claim-level embedding similarity: "RLHF contrasts_with DPO" captures a relationship that vector proximity alone cannot express.

**Bridge concepts and structural surprise.** Graphify uses betweenness centrality to find "bridge nodes" that connect otherwise isolated clusters. Knowledge Base applies the same algorithm to its concept graph, surfacing concepts that structurally connect distant themes. These bridge concepts drive suggested questions ("Why does concept X connect themes Y and Z?") and enrich the graph context block with non-obvious cross-domain connections.

**Incremental recomputation.** Graphify's watch mode recomputes only affected neighborhoods when files change. Knowledge Base adapted this for post-ingestion: after `/save`, betweenness centrality is recomputed only for the 2-hop neighborhood of newly connected concepts, with periodic full recomputation to prevent drift.

**The translation cost was real.** Graphify operates on precise structural relationships (function calls, imports) where "bridge node" has an unambiguous meaning. In a knowledge graph with epistemically uncertain, temporally evolving relationships, "bridge" and "surprising connection" require domain-aware interpretation. The adaptation preserved the structural algorithms but added confidence tiers, temporal awareness, and provenance tracking that Graphify's domain doesn't require.

## Design Principles

- **Evidence-traced.** Every claim links back to a verbatim snippet. Every edge has evidence from both sides. Nothing is asserted without provenance.
- **Temporally aware.** State summaries describe how themes evolved, what shifted and why, where momentum is building or stalling.
- **Human-enriched.** Automated extraction handles what's explicit; the highest-value insights come from user interpretation via `/enrich`, `/implications`, and `/challenge`.
- **Limitations are the most valuable signal.** The system extracts implicit limitations (performance cliffs, controlled conditions, hedging language, buried scale/cost) alongside explicit ones, classifies them by type and severity, and links them to bottlenecks.
- **Ideas must be novel and grounded.** The multi-agent tournament enforces a hard novelty gate — no idea passes without demonstrating it isn't already in the library.

## License

Private project. Not licensed for redistribution.
