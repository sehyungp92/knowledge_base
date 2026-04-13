---
type: source
title: 'World Models & General Intuition: Khosla''s largest bet since LLMs & OpenAI'
source_id: 01KJVMEPM5HBXF8TY2HZMMX64W
source_type: video
authors: []
published_at: '2025-12-06 00:00:00'
theme_ids:
- agent_systems
- generative_media
- multi_agent_coordination
- robotics_and_embodied_ai
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# World Models & General Intuition: Khosla's Largest Bet Since LLMs & OpenAI

General Intuition (GI) is a world model lab spun out of Medal, a decade-old game-clipping platform with 3.8 billion accumulated clips of peak human gameplay. This source documents GI's founding thesis — that predicting action tokens on interactivity data is to world models what predicting text tokens on internet data was to LLMs — and presents live demos of their vision-based gaming agents and interactive world model generation. It also captures the key limitations and open questions that define the current frontier of game-trained world models.

**Authors:** Pim de Witte (CEO, General Intuition / Medal); host unnamed
**Published:** 2025-12-06
**Type:** video

---

## Context & Origin

General Intuition is a spinout of Medal, a 10-year-old native game recorder with 12 million users — larger by active user count than Twitch's 7 million monthly active streamers. Medal's core product is retroactive clipping: software running silently in the background lets players capture the last 30 seconds after an interesting moment, similar to Tesla's bug-report model for self-driving. The result is a dataset of 3.8 billion clips specifically filtered for highlights — peak human behavior — with ground-truth controller overlays (keyboard/mouse positions, button presses, analog stick angles) attached to every frame.

This data asset attracted significant external interest. OpenAI offered $500 million for the clip archive. GI's founder turned it down to build an independent lab. Khosla Ventures led a $134 million seed round — Vinod Khosla's largest single seed bet since OpenAI — to pursue the world model thesis independently.

The broader context is active: DeepMind has published Genie 1, 2, and 3 and SIMA 1 and 2; [[entities/world-labs|World Labs]] (Fei-Fei Li) focuses on spatial intelligence; Yann LeCun's departure from Meta renewed debate about world models as a post-LLM frontier.

---

## Core Thesis

> *"LLMs were trained on predicting text tokens on words on the internet. What if we predict action tokens on interactivity data?"*

The analogy is precise: internet text → LLMs :: game interactivity data → world models. Video games provide a uniquely clean training signal because the player's hands *are* the optical dynamics — there is no pose estimation step, no inverse dynamics approximation, no gap between observation and action label. The controller overlay is ground truth.

This contrasts sharply with real-world video (YouTube), where recovering actions requires solving three stacked estimation problems: pose estimation → inverse dynamics → optical center tracking. Each step introduces noise; the pipeline is currently intractable at scale.

---

## What World Models Are (and Aren't)

GI draws a sharp distinction between **video models** and **world models**:

- A **video model** predicts the next likely or most entertaining frame in a sequence.
- A **world model** must understand the *full range of possibilities* from the current state and generate the next state conditioned on a *specific action taken*.

The action-conditioning requirement is what makes world models harder and more structurally different from generative video. See [[themes/video_and_world_models|Video & World Models]] for broader landscape context.

---

## Demos & Capabilities

### Vision-Based Gaming Agents

The agent receives raw pixels and predicts actions directly — no game state, no symbolic input, pure imitation learning. Key observations from the demo:

- **Behavioral fidelity:** early versions exhibited human-like habits such as periodically checking the scoreboard, driven entirely from imitation rather than explicit programming.
- **Self-recovery:** a 4-second working memory window is sufficient for the agent to occasionally unstick itself from dead ends.
- **Superhuman moments:** because the training data is highlights by construction, the baseline is peak human performance. The agent sometimes executes actions a typical human would not.
- **No RL, no fine-tuning:** the demonstrated models are pure imitation learning throughout.

The agent architecture transfers across environments: trained on less realistic games, transferred to more realistic games, then transferred to real-world video — entirely from pixels, with no handcrafted state or action labels required. This makes the recipe potentially general to any environment with appropriate data.

### Interactive World Model Generation

World models were pre-trained from scratch. Open-source video models were also fine-tuned to study physical transfer. Observed capabilities:

| Capability | Notes |
|---|---|
| Camera shake from explosions | Emergent — game engine does not implement shake; model inherits real-world physics prior |
| Smoke / partial observability | Model maintains position and orientation where other models break down |
| Zoom / scoped views | Spatial consistency preserved across different zoom levels and perspectives |
| Mouse sensitivity | Rapid camera movements supported; absent from other world models |
| Reload/hiding behavior | Agent predicts opponent reload state and selects appropriate cover positions |
| Generation length | ~20 seconds of coherent generation from 1 second of video context |

**Model distillation** produces very small variants that run in real time but exhibit visible capability degradation — more collisions, suboptimal routing — relative to the full models.

**Context window scaling** was identified as a surprising lever: behavior changes more dramatically with context length than initially expected.

---

## Limitations & Open Questions

These are among the most analytically important signals from this source.

**Blocking limitations:**

- **Sim-to-real gap for world models** — game-trained models do not transfer to real-world video without solving pose estimation, inverse dynamics, and optical dynamics (three compounding information-loss layers). No scalable pipeline exists. Relevant to [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]].
- **Robotics actuator mismatch** — GI's explicit thesis is *not* that models transfer to high-DOF robots. The bet is keyboard/mouse/joystick-compatible interfaces only. Continuous actuator spaces are out of scope.
- **No text-conditional generation** — current models cannot be steered via natural language. Integration with LLM-based planning ([[themes/agent_systems|Agent Systems]]) is future work.

**Significant limitations:**

- **4-second temporal memory** — long-horizon generation and multi-step planning are blocked by the short context window.
- **Action labels required** — passive video without ground-truth controller overlays is not trainable. YouTube footage is unusable without solving the labeling problem.
- **Highlight bias** — Medal's dataset is filtered for exciting moments. Routine, low-intensity behavior is underrepresented. This distorts what "average" looks like in the learned prior.
- **Inherited incorrect physics** — the world model reproduces camera shake from explosions that the actual game engine does not generate. Physics priors from the training data propagate into the model, including wrong ones.
- **First-person only** — third-person perspectives not yet demonstrated; may matter for multi-object or multi-agent tasks.
- **VR environment diversity** — VR platforms have hundreds of environments; PC gaming has tens of thousands. Platform diversity shapes transfer range.

---

## Breakthroughs

**Retroactive action-labeling at scale** shifts the world model training bottleneck from data scarcity to data abundance. 3.8 billion observation-action pairs with ground-truth labels is a qualitatively different starting point than any prior dataset in this space.

**Real-time interactive generation** with camera dynamics, occlusion reasoning, and adversarial state handling — camera shake inheritance, smoke traversal, zoom consistency — demonstrates that game-trained world models have already crossed a minimum viability threshold for immersive simulation.

---

## Connections to the Landscape

**Confirms** the DeepMind SIMA finding that approximately 100 actions common across games also exist in the real world. SIMA's 9-to-1 holdout (train on 9 games, test on 10th) shows meaningful cross-environment generalization — a prerequisite for GI's transfer thesis.

**Challenges** the assumption that internet video is the right pre-training substrate for embodied AI. GI's framing inverts this: game data may be *better* than YouTube footage precisely because it eliminates the labeling problem.

**Opens** a question for [[themes/vision_language_action_models|Vision-Language-Action Models]]: if world models can be pre-trained on game data and fine-tuned toward physical domains, what is the minimum viable bridge between game interactivity and real-world robot control?

**Relevant themes:** [[themes/agent_systems|Agent Systems]], [[themes/video_and_world_models|Video & World Models]], [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]], [[themes/vision_language_action_models|Vision-Language-Action Models]], [[themes/generative_media|Generative Media]], [[themes/multi_agent_coordination|Multi-Agent Coordination]]

## Key Concepts

- [[entities/genie|Genie]]
- [[entities/world-model|World Model]]
