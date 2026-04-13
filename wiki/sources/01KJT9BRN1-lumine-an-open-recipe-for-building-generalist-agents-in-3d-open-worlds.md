---
type: source
title: 'Lumine: An Open Recipe for Building Generalist Agents in 3D Open Worlds'
source_id: 01KJT9BRN1WKE1FYCKA8E10VVF
source_type: paper
authors:
- Weihao Tan
- Xiangyang Li
- Yunhao Fang
- Heyuan Yao
- Shi Yan
- Hao Luo
- Tenglong Ao
- Huihui Li
- Hongbin Ren
- Bairen Yi
- Yujia Qin
- Bo An
- Libin Liu
- Guang Shi
published_at: '2025-11-12 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- computer_use_and_gui_agents
- multimodal_models
- reasoning_and_planning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Lumine: An Open Recipe for Building Generalist Agents in 3D Open Worlds

Lumine presents the first end-to-end vision-language-action model capable of completing multi-hour missions in real-time within complex 3D open-world commercial games, demonstrating zero-shot cross-game generalization and establishing an open recipe — data curation, action tokenization, hybrid reasoning, and inference optimization — for building generalist agents that operate at human-level efficiency without environment-specific reward engineering or architectural modification.

**Authors:** Weihao Tan, Xiangyang Li, Yunhao Fang, Heyuan Yao, Shi Yan, Hao Luo, Tenglong Ao, Huihui Li, Hongbin Ren, Bairen Yi, Yujia Qin, Bo An, Libin Liu, Guang Shi
**Published:** 2025-11-12
**Type:** Paper
**Arxiv:** https://arxiv.org/abs/2511.08892

---

## What This Breaks

Prior game-playing agents — DRL systems like DQN, AlphaStar, OpenAI Five — achieve mastery only in closed environments with explicit reward shaping. They exhibit brittle intelligence: no language grounding, no transfer, no ability to handle the textual and symbolic complexity of modern interactive games. The longest continuous task horizon achieved before Lumine was roughly one hour (Cradle on Red Dead Redemption 2), and that agent required pausing the game during inference — making real-time operation impossible.

VLM-based approaches (SIMA, JAVIS-VLA) are capped at short horizons of seconds to minutes. They excel at high-level reasoning but fail at generating precise low-level actions and recognizing fine-grained visual patterns at the speed interactive environments demand. Hierarchical architectures that decouple slow high-level planners from fast low-level controllers are difficult to optimize jointly due to non-stationarity.

A more subtle but consequential failure: GUI and game agents universally oversimplify input modeling. Most teleport the cursor to absolute coordinates and treat keys as coarse press/release events. This fails categorically in 3D environments where relative mouse movement controls the camera and holding versus tapping a key (sprinting, charging, skill sequences) triggers entirely different mechanics.

---

## Architecture

Lumine is a 7B-parameter [[themes/vision_language_models|VLM]] built on Qwen2-VL-7B-Base, processing raw pixels at 5 Hz and autoregressively generating keyboard-mouse actions at 30 Hz. The key design decisions are:

**Action tokenization in language space.** Rather than adding separate action heads or redefining the vocabulary, Lumine represents all keyboard and mouse operations within the existing token space. Each action step specifies relative mouse displacement (ΔX, ΔY ∈ (−1000, 1000)) and scroll (ΔZ ∈ [−5, 5]), followed by six consecutive 33ms action chunks specifying which keys (0–4 per chunk) are held or released. This achieves 30 Hz effective control from a 5 Hz inference loop.

**Hybrid thinking strategy.** Rather than reasoning at every step (computationally prohibitive) or never reasoning (insufficient for long-horizon coherence), Lumine selectively emits inner-monologue traces enclosed by `<|thought_start|>` / `<|thought_end|>` tokens only at critical transitions — task completions, sudden environmental changes invalidating prior plans, and novel goal emergence. This is the key mechanism enabling [[themes/chain_of_thought|adaptive chain-of-thought]] without the latency cost of reasoning at every step.

**Context-as-memory.** Short-term memory is a FIFO sliding window of up to 20 recent image-action pairs. Long-term memory is the most recent reasoning trace. At each reasoning event, context is flushed and re-accumulated with the new reasoning as its compressed summary. This is lightweight but structurally lossy — events further than 20 frames back and more than one reasoning cycle ago are irrecoverable without external memory.

---

## Training Curriculum

Three stages build capabilities in sequence:

1. **Pre-training** on 1,731 hours of filtered human gameplay (image-action pairs, no labels) to develop action primitives. Deliberately avoids large-scale instruction annotation, instead exposing the model to raw gameplay diversity — including suboptimal and irregular behaviors — to improve robustness. ~20% multimodal web data is retained throughout to preserve general VLM capabilities.

2. **Instruction-following fine-tuning** on 200 hours of GPT-4.1-captioned transition snippets to ground control in language. This stage corrects the behavioral bias introduced by pre-training, where players frequently pass NPCs without engaging — causing impaired goal-directed interaction in the base model.

3. **Reasoning fine-tuning** on 15 hours of 15K human-annotated inner-monologue traces (average 37.4 tokens per trace, 3.2s interval) to enable adaptive long-horizon [[themes/reasoning_and_planning|planning]].

An emergent capability sequence was observed during pre-training without explicit supervision: object interaction emerges first, then combat and GUI manipulation, then game mechanics — suggesting structured visuomotor competence can arise from large-scale imitation alone.

---

## Inference Optimization

Real-time 7B-model inference under 200ms required extensive engineering:

- **StreamingLLM** for KV-cache reuse across steps
- **4-GPU tensor parallelism** (one KV head per H20)
- **W8A8 quantization**
- **Draft-model-less speculative decoding** exploiting fixed action delimiters
- **CUDA graph fusion** and GPU-side image preprocessing

Combined, these yield a **25.3× end-to-end latency reduction**, bringing first-action-chunk latency (without reasoning) to 113.9ms — within the 200ms control cycle. This engineering contribution is independently significant: it demonstrates sub-200ms closed-loop control for a 7B-parameter [[themes/multimodal_models|multimodal model]] without architectural compromise.

---

## Results

On the 141-task benchmark spanning Collection, Combat, NPC Interaction, and Puzzle across Genshin Impact:

- **Lumine-Instruct** achieves >80% success on all simple-task categories
- **Lumine-Thinking (history)** completes the five-hour Mondstadt main storyline in 56 minutes — faster than fresh human players (78 min average) and matching expert players (53 min average)
- **Reasoning ablation:** Lumine-Thinking achieves 93.4% success on the five-act in-domain mission vs. 66.8% for Lumine-Instruct and 6.6% for Lumine-Instruct-NonHistory. Thinking models stay on-objective despite distractions; instruct models wander and fail to recover.

**Zero-shot cross-game generalization** (no fine-tuning): 100-minute missions in Wuthering Waves, full five-hour first chapter of Honkai: Star Rail. These games share visual similarity with Genshin Impact but differ in mechanics, UI layout, and quest structure.

---

## Limitations and Open Questions

### Hard Failures

**Aerial and precision combat** is currently intractable. The agent achieves zero success rate against the Eye of the Storm — a flying enemy that lands only briefly. It correctly identifies the required ranged character but cannot coordinate aiming precision, timing, and evasion under time pressure. This reflects a fundamental gap between the agent's visuomotor resolution and the demands of high-frequency reactive combat.

**Puzzle tasks** show the largest performance drop across all categories, requiring simultaneous mastery of spatial reasoning, fine-grained control, game-mechanic understanding, and logical deduction. Game mechanic understanding is particularly hard to acquire because relevant scenarios are sparse in raw gameplay data, making emergent learning slow and unreliable.

**Unseen visual objects** cannot be reliably recognized from a distance. The agent must physically approach and read on-screen name labels to confirm identity — zero-shot visual recognition of novel game entities fails at range.

### Structural Constraints

**Reasoning data is the ceiling.** Long-horizon autonomy rests on 15 hours of manually annotated data — a dataset that is both small and expensive to scale. Automated VLM labeling of reasoning traces is unreliable. This makes manual annotation the rate-limiting bottleneck for improving reasoning capability, and blocks RL-style self-improvement loops.

**RL is structurally inaccessible** in commercial game environments: no API access to internal state or rewards, GPU rendering requirements prevent the thousands of parallel rollouts that make RL practical. This is not a Lumine-specific limitation but a field-wide bottleneck for improving agents in realistic software environments.

**Infrastructure cost.** Real-time inference requires four NVIDIA H20 GPUs. This is not consumer-deployable. StreamingLLM's KV-cache eviction causes measurable performance degradation on long-horizon tasks, requiring the context-flush workaround that itself limits temporal coherence.

**The 2B model hits a capacity wall.** Below 1200 hours of training, 2B and 7B models track similarly. Beyond 1200 hours, the 2B model's benchmark performance degrades even as training loss continues to fall — demonstrating a hard capacity limitation for absorbing open-world complexity at smaller scale.

**Persistent 200ms perceptual lag.** The agent always acts on slightly stale observations. In highly time-sensitive scenarios — rapid-reaction combat, narrow timing windows — this introduces structural errors that cannot be engineered away without fundamentally faster inference.

**Context window truncation.** With only 20 recent frames and one reasoning trace retained, events from earlier in a long mission are irrecoverable. Tasks requiring recall of decisions made more than a few minutes prior have no mechanism for retrieval.

---

## Implications

Lumine's architecture challenges the assumption that [[themes/agent_systems|agent systems]] require hierarchical decomposition — separate slow-planner and fast-controller modules — to handle the gap between reasoning timescales and control timescales. The hybrid thinking strategy demonstrates that a single model can navigate this gap adaptively, reserving deliberation for moments where it is actually necessary.

The action tokenization approach has implications beyond games. The failure mode Lumine addresses — absolute cursor teleportation and coarse key press/release — affects any [[themes/computer_use_and_gui_agents|computer use agent]] operating in environments requiring continuous relative motion: creative tools, CAD software, any interface where the journey of the cursor matters, not just the destination.

The emergent visuomotor skill hierarchy from pre-training without explicit supervision is a data point for the thesis that structured competence can arise from large-scale behavioral imitation — relevant to debates about whether goal-directed behavior requires explicit goal supervision or can emerge from trajectory diversity alone.

The RL inaccessibility bottleneck is the deepest open question. Lumine demonstrates that imitation learning can reach human-level efficiency on a five-hour mission. But it cannot improve beyond the behavioral ceiling of its training data. Self-improvement — the mechanism that enabled AlphaGo to exceed human performance — remains structurally blocked in commercial interactive environments.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/vision_language_models|Vision-Language Models]]

## Key Concepts

- [[entities/action-chunking|Action Chunking]]
- [[entities/tensor-parallelism|Tensor Parallelism]]
