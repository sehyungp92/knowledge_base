---
type: source
title: 'GPT-5''s Vision Checkup: a frontier Vision Reasoning Model, but -not- a new
  SOTA'
source_id: 01KJS40HGRR8XAXKWYQY9YE3T1
source_type: article
authors: []
published_at: '2025-08-07 00:00:00'
theme_ids:
- agent_systems
- ai_market_dynamics
- benchmark_design
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- frontier_lab_competition
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GPT-5's Vision Checkup: a frontier Vision Reasoning Model, but -not- a new SOTA

**Authors:** 
**Published:** 2025-08-07 00:00:00
**Type:** article

## Analysis

# GPT-5's Vision Checkup: a frontier Vision Reasoning Model, but not a new SOTA
2025-08-07 · article
https://www.latent.space/p/gpt5-vision

---

## Briefing

**GPT-5 advances vision-language reasoning enough to rank in the top 5 on general leaderboards, but completely fails at spatial grounding — scoring mAP50:95 of 1.5 vs. Gemini 2.5 Pro's 13.3 on RF100-VL — because OpenAI appears not to include object detection data in pretraining. The core finding is that comprehension and localization are fully decoupled capabilities, and reasoning alone cannot substitute for detection-specific training signal.**

### Key Takeaways
1. **GPT-5 is not a vision SOTA** — On both Vision Checkup and RF100-VL, GPT-5 matches or underperforms the best prior models rather than establishing a new frontier.
2. **Reasoning is now the primary lever for vision leaderboard performance** — All top models on Vision Checkup are reasoning models; the gains come from test-time compute applied to visual tokens, not vision-specific architectural advances.
3. **Comprehension ≠ localization** — GPT-5 correctly identifies objects in images but places bounding boxes wildly off-target, demonstrating these are separate capabilities that can be fully dissociated.
4. **OpenAI's pretraining gap is a likely root cause** — The suspected reason GPT-5 scores 1.5 vs. Gemini's 13.3 on object detection is that OpenAI simply excludes object detection supervision from pretraining data.
5. **Increasing reasoning effort doesn't fix detection** — Setting reasoning effort to "high" yields no improvement on RF100-VL, confirming that more chain-of-thought cannot compensate for absent spatial priors.
6. **Real-time vision with reasoning is still impractical** — 10+ second latency per image rules out autonomous robotics and real-time agentic workflows for any current reasoning-capable VLM.
7. **Nondeterminism undermines reliability** — OpenAI's reasoning mode can answer the same visual question correctly and incorrectly across two identical calls, making production deployment risky.
8. **RF100-VL exposes what "vibe check" benchmarks hide** — Even the best LLMs score below 10 mAP50:95 on novel real-world object categories, a stark contrast to their performance on saturated academic benchmarks.
9. **The model router explains GPT-5-Mini parity** — GPT-5-Mini achieving the same vision scores as GPT-5 is not a capability equivalence; it reflects intelligent routing dispatching simpler vision queries to sub-models.
10. **Object detection pretraining is a structural differentiator** — Gemini and Qwen outperform OpenAI models on grounding tasks specifically because they include detection data; this is an architectural/data choice, not a scaling artifact.

---

### The Two-Tier Vision Benchmark Reality

- **General comprehension tasks are largely solved** across all frontier models, including reading text, signs, receipts, CAPTCHAs, and color recognition — these represent the "easy" tier where models converge.
  - The remaining hard tier — counting, spatial understanding, object detection, document understanding — shows high variance, and this variance is where meaningful differentiation exists.
  - **The variance across task types makes aggregate comparisons misleading** without benchmark-level decomposition.

- Vision Checkup, Roboflow's open source leaderboard, tracks frontier performance on the harder tier, and its verdict is unambiguous: **reasoning capability is the dominant predictor of ranking**, not vision-specific design.
  - OpenAI holds the top positions, with GPT-5 placing in the top 5.
  - The editorial implication is that leaderboard success currently reflects general intelligence applied to images, not specialized visual understanding.

- **RF100-VL was specifically designed to escape benchmark saturation** and expose real-world grounding failures that standard leaderboards obscure.
  - Released at CVPR, it comprises 100 datasets from Roboflow Universe with bounding box annotations and multimodal few-shot instructions across novel image domains.
  - The benchmark question it operationalizes: "How well does your LLM understand the real world?" — framed as grounding, not comprehension.
  - **Even the best-performing model (Gemini 2.5 Pro) only reaches 13.3 mAP50:95 zero-shot**, and most top LLMs score below 10.

---

### GPT-5's Catastrophic Grounding Failure

- GPT-5 scored **mAP50:95 of 1.5** on RF100-VL — a roughly 9x gap below Gemini 2.5 Pro's 13.3, and well below the already-low field average.
  - This is not a marginal underperformance; it represents near-complete failure to localize objects with accurate bounding boxes.

- The volleyball dataset example makes the failure mode concrete: **GPT-5 correctly identifies the objects** (ball, two blockers, defenders) but generates bounding boxes that don't correspond to their actual positions or sizes.
  - The same pattern appears in a sheep dataset — semantic comprehension intact, spatial grounding broken.
  - UI element detection also shows no improvement over prior models, relevant to agentic workflows and computer-use applications.

- **The root hypothesis is pretraining data composition**: OpenAI models are suspected to exclude object detection supervision, while Gemini and Qwen include it.
  - This is a structural training decision, not a capacity or parameter count issue.
  - It means the gap cannot be closed by scaling reasoning — it requires retraining with detection-annotated data.

- Providing detailed textual instructions marginally helps GPT-5 on detection tasks, and it scores slightly above o3 — but **the improvement is incremental, not categorical**.
  - Raising reasoning effort to "high" produces no measurable gain on RF100-VL, further confirming that the bottleneck is not reasoning depth but spatial representation.

---

### Reasoning as Vision Accelerant — and Its Limits

- The dominant pattern in frontier VLM progress is **reasoning capability borrowed from LLM pretraining a

## Key Claims

1. GPT-5's vision performance is not a new state-of-the-art — it matches the best models available prior to its release.
2. GPT-5-Mini's vision scores the same as GPT-5's vision, which is attributed to a model router rather than equivalent base capability.
3. Most VLMs cannot correctly count 4 coins in a photo or locate where specific items are in an image.
4. Tasks like reading text, signs, receipts, CAPTCHAs, and understanding colors are generally solved by all frontier models.
5. Harder vision tasks such as counting, spatial understanding, object detection, and document understanding show high performance variability across models.
6. All top models on the Vision Checkup leaderboard are reasoning models.
7. OpenAI dominates vision capability leaderboards and GPT-5 places in the top 5 of Vision Checkup.
8. Strong vision leaderboard performance is primarily attributable to reasoning capabilities from pretraining and test-time compute, rather than vision-specific advances.
9. Reasoning mode in OpenAI models is nondeterministic — the same question asked twice can yield both correct and incorrect answers.
10. Visual reasoning with current frontier models takes over 10 seconds per image, making it impractical for real-time applications.

## Capabilities

- Reasoning capability transfers significantly to general vision tasks — reasoning models dominate top positions on vision leaderboards, outperforming non-reasoning counterparts on general visual understanding benchmarks
- Basic visual understanding tasks — reading text, signs, receipts, CAPTCHAs, and identifying colors — are broadly solved by all frontier VLMs
- GPT-5 achieves slight improvement over o3 on simple visual tasks, with detailed instructions further boosting scores

## Limitations

- GPT-5 scores only 1.5 mAP50:95 on RF100-VL object detection — 9x lower than Gemini 2.5 Pro's 13.3 SOTA — due to absence of object detection data in pretraining
- Frontier VLMs can comprehend scene content but cannot reliably localize or ground objects spatially — bounding box predictions miss correct positions and sizes even when scene semantics are correctly understood
- Reasoning-mode vision inference takes 10+ seconds per image — too slow for real-time use cases, creating a hard speed-accuracy tradeoff with no good middle ground
- Reasoning models exhibit significant nondeterminism on vision tasks — identical prompts yield correct answers on some runs and incorrect answers on others, making reliability-sensitive deployment difficult
- Increasing reasoning effort to 'high' does not improve object detection scores — test-time compute scaling fails to compensate for absent pretraining priors on spatial localization
- GPT-5 shows no improvement on UI element detection compared to prior OpenAI models — vision-powered computer use agents have not advanced for GUI grounding tasks
- Harder visual tasks (counting, spatial understanding, object detection, document understanding) show high performance variability across models — these capabilities are persistently inconsistent even at the frontier
- All top LLMs score below 10 mAP50:95 on RF100-VL for novel object identification in real-world contexts — even the best VLMs fail systematically on object classes from domains outside standard training distributions
- AI systems remain far from enabling autonomous robotics in uncontrolled environments — VLM-level visual understanding is insufficient for the counting, spatial understanding, and localization requirements of general manipulation
- GPT-5-Mini scores comparably to GPT-5 on vision tasks — vision capability does not scale with general model tier under OpenAI's routing architecture, decoupling vision performance from overall model investment

## Bottlenecks

- Absence of object detection pretraining data in frontier VLMs blocks spatial grounding and localization — a prerequisite for computer use agents and robot perception
- Reasoning-mode inference latency for vision (10+ seconds per image) blocks real-time visual applications despite superior accuracy on benchmarks
- Fundamental architectural gap between semantic scene comprehension and precise spatial object grounding in current VLMs — understanding scene content does not entail knowing where objects are
- Internet-scale pretraining corpora underrepresent specialized visual task types (counting, spatial reasoning, object detection, novel domains), creating persistent capability gaps that scaling alone cannot close

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/gpt-5|GPT-5]]
- [[entities/gemini-25-pro|Gemini 2.5 Pro]]
