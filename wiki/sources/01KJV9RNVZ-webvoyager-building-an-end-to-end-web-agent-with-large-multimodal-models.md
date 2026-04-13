---
type: source
title: 'WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models'
source_id: 01KJV9RNVZPC7HGR9C28BV0R0N
source_type: paper
authors:
- Hongliang He
- Wenlin Yao
- Kaixin Ma
- Wenhao Yu
- Yong Dai
- Hongming Zhang
- Zhenzhong Lan
- Dong Yu
published_at: '2024-01-25 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models

**Authors:** Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, Dong Yu
**Published:** 2024-01-25 00:00:00
**Type:** paper

## Analysis

# WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models
2024-01-25 · paper · Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai et al. (8 total)
https://arxiv.org/pdf/2401.13919

---

### Motivation & Prior Limitations
- Existing web agents were restricted to a single input modality (typically text/HTML) and evaluated only in simplified web simulators or static web snapshots, leaving a large gap to real-world applicability.
  - Approaches like WebGPT, WebAgent, and WebArena focused on processing raw HTML or accessibility trees, which produce overly verbose text representations and miss the visual structure that rendered webpages are explicitly designed to communicate.
  - Benchmarks such as Mind2Web relied on stepwise, offline evaluation against a single "golden" trajectory, penalizing valid alternative strategies and making fair comparison between methods difficult.
- Vision capability was underutilized despite being central to how browsers actually present information: rendered webpages encode UX-driven visual hierarchy that is more efficiently parsed visually than through DOM text representations.
  - While Pix2Struct and WebArena initiated screenshot-based navigation experiments, these were preliminary and did not represent deep exploration of multimodal decision-making in live web environments.

---

### Proposed Approach
- WebVoyager is an end-to-end multimodal web agent that takes screenshots and auxiliary text of interactive elements as joint observations, reasons via a ReAct-style thought-action loop, and executes actions on real live websites without any human intervention.
  - Unlike prior work that processed HTML directly or required a separately fine-tuned retrieval module (as in SeeAct), WebVoyager uses a rule-based JavaScript tool (GPT-4V-Act) to extract interactive elements from the DOM and overlay bounding boxes with numerical labels on screenshots — no object detection model required.
  - The observation space combines the labeled screenshot with auxiliary text per element (content, type, aria-label), while the action space covers Click, Input, Scroll, Wait, Back, Jump to Search Engine, and Answer — a minimal but sufficient set for generalist web browsing.
- Context management is handled by retaining only the three most recent webpage observations while keeping the full history of thoughts and actions, preventing the agent from being overwhelmed by stale visual content across long trajectories.
  - The backbone is GPT-4 Turbo with vision (gpt-4-vision-preview), with additional experiments using Claude 3 Opus and GPT-4o.
- A new benchmark of 643 tasks across 15 popular websites was constructed via self-instruct (GPT-4 Turbo seeded with human-written tasks) followed by manual verification, with annotations distinguishing "Golden" (stable, enumerable) from "Possible" (open-ended, real-time) answers.
- An automated evaluation protocol uses GPT-4V as a multimodal judge: it receives the task, the agent's final answer, and the last k screenshots of the navigation trajectory and returns a binary success judgment, replacing the infeasible golden-trajectory matching used in prior offline benchmarks.

---

### Results & Capabilities
- WebVoyager achieves a 59.1% Task Success Rate on the 643-task benchmark, substantially outperforming GPT-4 (All Tools) at 30.8% and the text-only WebVoyager variant at 40.1%.
  - The multimodal advantage is most pronounced on visually complex websites: Booking (43.2% vs. 2.3% text-only), Google Flights (59.5% vs. 7.1% text-only), and Google Map (70.7% vs. 61.0% text-only), where accessibility tree representations become verbose and unintuitive for calendar and map interactions.
- On the GAIA web browsing subset (90 Level 1–2 tasks), WebVoyager outperforms both GPT-4V (All Tools) and the text-only baseline across both difficulty levels.
- WebVoyager achieves 30% success on the SeeAct online test set versus 26% for the best autonomous SeeAct agent, while WebVoyager requires no additional fine-tuned cross-encoder module.
- The GPT-4V automatic evaluator reaches 85.3% agreement and a Cohen's κ of 0.70 with human judges when provided the full navigation trajectory, matching inter-annotator agreement among human evaluators (Fleiss κ = 0.70 before discussion).
  - Agreement degrades meaningfully with fewer screenshots: κ = 0.51 at k=1 vs. 0.70 at full trajectory, indicating that trajectory context is essential for reliable automated evaluation.
- GPT-4o as backbone scores 55.5% overall (auto-evaluated); Claude 3 Opus scores 52.8%, with both significantly above the text-only setting but trailing GPT-4V (57.1%) in auto-evaluation under GPT-4V as judge.
  - Cross-model evaluation reveals systematic self-preference bias: Claude-3-Opus rates its own outputs highest, while GPT-4o is more lenient overall and GPT-4V tends toward strictness; GPT-4o as judge yields κ = 0.72 with humans, slightly higher than GPT-4V's 0.70.

---

### Implications
- The strong performance gap between multimodal and text-only agents on visually structured tasks (calendars, maps, sorting UIs) establishes that visual grounding of rendered pages is a necessary capability for generalist web automation — not an optional enhancement.
- The GPT-4V-based automatic evaluation protocol addresses a core bottleneck in the field: evaluating open-ended, trajectory-based tasks at scale without requiring fixed golden answers, enabling future benchmark construction decoupled from predefined correct paths.
- The paper demonstrates that high-resolution, long-context vision-language models are a prerequisite for real-world computer use agents — open-source LMMs at 224×224 or 336×336 resolution with 4K context windows are architecturally insufficient for this task class, creating a near-term capability gap between open and closed models.
- Self-preference bias in LMM-as-judge evaluation (each model favoring its own outputs) is a latent validity threat that must be accounted for when

## Key Claims

1. WebVoyager achieves a 59.1% task success rate on the WebVoyager benchmark, significantly surpassing GPT-4 (All Tools) at 30.8% and text-only WebVoyager at 40.1%.
2. GPT-4V-based automatic evaluation achieves 85.3% agreement with human judgment, making it a reliable evaluator for open-ended web agents.
3. Rendering HTML into visual webpages is a critical functionality overlooked by existing text-based web agent approaches.
4. Visual analysis of rendered web pages is more effective than processing raw HTML representation for web navigation.
5. WebVoyager uses Set-of-Mark inspired numerical labeling of interactive web elements on screenshots to facilitate action decision-making, implemented via a rule-based JavaScript tool without any object
6. WebVoyager uses context clipping, retaining only the three most recent observations while keeping the full history of thoughts and actions, to prevent agent confusion from excessive web page observati
7. WebVoyager follows the ReAct prompting paradigm, generating a natural language thought process before producing action code.
8. Using a single black color for bounding box borders and label backgrounds yields higher task success rates than using multiple colors.
9. Stepwise offline evaluation on predefined golden trajectories, as used in Mind2Web, may not fully account for the variety of viable strategies and can lead to biased evaluation.
10. Navigation stuck (running out of steps) is the most common failure mode for WebVoyager, accounting for 44.4% of failures.

## Capabilities

- Multimodal web agent completing real-world end-to-end tasks across 15 popular websites using rendered screenshots and interactive element text, achieving 59.1% task success rate without human intervention or website-specific tuning
- GPT-4V serving as reliable automatic evaluator for open-ended multimodal web agent trajectories, achieving 85.3% agreement and kappa=0.70 with human judges — on par with inter-annotator agreement
- Rule-based interactive element extraction and Set-of-Mark numerical labeling on live web screenshots enabling precise element identification for agent action prediction, without requiring any object detection model

## Limitations

- Multimodal web agents underperform text-only agents on text-heavy websites — dense small-font text in screenshots is harder to parse than accessibility trees, creating a modality-dependent performance cliff
- Navigation stuck is the dominant failure mode (44.4% of failures) — agents exhaust step budgets through imprecise queries, incorrect scroll targeting, and repetitive loops rather than completing tasks
- Visual grounding failures account for 24.8% of errors — agents misidentify uncommon UI patterns, confuse adjacent elements, and cannot distinguish dense overlapping web elements
- Hallucination causes 21.8% of web agent failures — agents accept partially correct answers or execute plausible-but-wrong actions (e.g., typing into the wrong text box) with no error signal
- Context clipping to retain only 3 most recent observations causes agents to repeat previous mistakes — they cannot detect their own in-episode failure loops without full recent history
- Open-source LMMs are structurally unsuitable for web navigation — image resolution of 224×224 to 336×336 makes fine-grained web text unreadable, and 4096-token context length is insufficient for 15-step trajectories requiring 7000+ tokens
- LMMs used as automatic evaluators exhibit self-preference bias — each model rates its own generated outputs higher than competitors', undermining their use as neutral benchmarks
- Web agents cannot access websites requiring login or CAPTCHA, blocking coverage of the majority of commercially valuable services
- Task success rate degrades sharply as webpage interactive element density and trajectory length increase — complexity of web structure is a direct predictor of agent failure
- Model-specific cognitive biases emerge on structured UI tasks — GPT-4o systematically fails to select 'one way' for one-way flights; Claude-3-Opus consistently struggles with sequential form input on booking interfaces
- Drag interactions are entirely unsupported, blocking tasks requiring fine-grained positional manipulation (sliders, drag-and-drop reordering, drawing tools)
- Prompt misalignment causes 9% of failures — agents in longer trajectories fail to produce parseable action outputs or prematurely terminate tasks they have explicitly stated are incomplete
- Web agents face safety risks at deployment scope — unintentional malicious content downloads, private data leakage to public sites, and fake request generation — blocking production deployment without extensive safety infrastructure that does not yet exist

## Bottlenecks

- Visual grounding precision for fine-grained interactive web elements is insufficient for reliable web navigation — agents confuse adjacent elements, fail on uncommon UI patterns, and cannot read dense text in screenshots, accounting for 24.8% of all failures
- Long-trajectory web navigation is bottlenecked by a context management tradeoff — retaining full screenshot history is token-prohibitive, but clipping to 3 recent observations causes agents to loop on their own recent mistakes
- Open-source LMMs are excluded from practical web agent deployment by insufficient image resolution (224–336px) and context length (4096 tokens), creating a frontier model dependency that blocks open, reproducible, cost-effective development

## Breakthroughs

- Multimodal (vision + text) web agents substantially outperform both text-only accessibility-tree agents and tool-integrated agents on real-world websites, demonstrating that rendered visual context is a necessary ingredient for generalist web navigation

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/gaia|GAIA]]
- [[entities/mind2web|Mind2Web]]
- [[entities/set-of-mark-prompting|Set-of-Mark Prompting]]
- [[entities/task-success-rate|Task Success Rate]]
- [[entities/webarena|WebArena]]
