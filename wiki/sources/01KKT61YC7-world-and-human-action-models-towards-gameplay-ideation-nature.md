---
type: source
title: World and Human Action Models towards gameplay ideation - Nature
source_id: 01KKT61YC7TVSYYSDYMBE0Z6R7
source_type: paper
authors: []
published_at: '2025-02-19 00:00:00'
theme_ids:
- creative_content_generation
- generative_media
- image_generation_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# World and Human Action Models towards gameplay ideation - Nature

**Authors:** 
**Published:** 2025-02-19 00:00:00
**Type:** paper

## Analysis

# World and Human Action Models towards gameplay ideation - Nature
2025-02-19 · paper
https://www.nature.com/articles/s41586-025-08600-3

---

### Motivation & Prior Limitations
State-of-the-art generative AI models fail to adequately support creative ideation in game development because they cannot combine consistent world-adherent outputs with meaningful diversity, and they do not persist user modifications across generated sequences.
- Creatives reported that current models cannot maintain contextual consistency (game physics, studio style, narrative coherence) while also producing diverse outputs, making generated material too incoherent to build on iteratively.
  - One VP of Experience described: "The AI still isn't very good at kind of keeping generating and then kind of following specific rules and mechanics, you know, because it's inconsistent."
- Existing creativity support tools required manually defining or extracting domain-specific structure, limiting them to narrow domains and preventing generalization across games or genres.
- Prior world modelling work (recurrent networks, RSSMs, transformers) had demonstrated potential in 2D video games and road traffic but had not been systematically evaluated for the specific capabilities — consistency, diversity, persistency — needed to support creative professionals in complex 3D games.
- Current generative AI models operate primarily through text-based prompts and do not support direct manipulation of generated content or adoption of user-proposed edits, blocking the iterative tweaking that is central to professional creative practice.

---

### Proposed Approach
The paper introduces WHAM (World and Human Action Model), a 1.6B-parameter transformer trained on ~500,000 anonymized human gameplay sessions from the 3D multiplayer game Bleeding Edge, designed to generate consistent and diverse gameplay sequences and to persist user modifications.
- WHAM frames gameplay as a sequence of discrete tokens, using a VQGAN image encoder (540 tokens per frame at native 300×180 resolution for the 1.6B model, 256 tokens at 128×128 for smaller variants) interleaved with discretized controller action tokens (buttons as 0/1, joystick axes discretized into 11 buckets), trained via a decoder-only causal transformer with next-token prediction.
  - This differs from prior world models by targeting creative support rather than task-automation, and by operating on a complex 3D multiplayer game rather than 2D Atari-style or simulated environments.
  - Persistency is enabled architecturally by allowing token-level modification during autoregressive generation: users can edit image tokens directly (e.g., inserting a game object into a frame), and the model conditions subsequent generation on those altered tokens.
- The evaluation methodology itself is a core contribution: three capability metrics (FVD-based consistency, Wasserstein distance on action distributions for diversity, human-annotated persistency rate) are derived directly from a user study of 27 game creatives across 8 studios, grounding ML evaluation in creative practitioner needs rather than generic task-completion benchmarks.
- Training data comprised approximately 7 years of continuous play (27.89 TiB; ~1.4B frames at 10 Hz for the 7 Maps dataset), with scaling analysis conducted across models ranging from 15M to 1.6B parameters to inform architecture selection under a compute budget of ~1×10²² FLOPS.

---

### Results & Capabilities
The 1.6B WHAM generates highly consistent gameplay sequences of up to 2 minutes, with FVD improving monotonically with compute (FLOPS) across model sizes, and with human annotators confirming that increasing training reduces structural, action, and interaction inconsistencies.
- FVD (Fréchet Video Distance) decreases with model scale and training compute; the 1.6B model using full-resolution 300×180 images achieves lower FVD than smaller models because the higher-resolution ceiling allows generated frames to more closely match ground truth.
  - A strong correlation of r = 0.77 was found between FVD and training loss, validating loss as a proxy for consistency quality.

WHAM's action diversity approaches the human-to-human baseline as measured by Wasserstein distance between generated and real action distributions across 1,024 held-out gameplay sequences.
- The 894M model achieves slightly better Wasserstein distance than the 1.6B model, attributed to the larger model's greater token vocabulary (16,384 vs. 4,096) and image token count (540 vs. 256) implicitly down-weighting action loss; training a second 1.6B model with 10× action loss weighting partially recovers this gap.
- Qualitatively, three gameplay futures generated from a single starting state by the 1.6B WHAM show distinct character trajectories, navigation paths across different Jumppads, and visual variations in character appearance (e.g., hoverboard skins).

Persistency of user-inserted game elements (Powercell, allied/opponent character, Vertical Jumppad) reaches 85% or higher across all element types when the model is conditioned on five edited input frames, compared to substantially lower rates with a single edited frame.
- Human annotation of 600 generated videos showed 90% inter-annotator agreement; only 7 of 600 videos were classified as "Unusable."
- Persistency gains diminish from 5 to 10 input frames (not statistically significant), indicating that 5 frames saturates context utility for this capability.

---

### Implications
WHAM demonstrates that large generative models trained on raw gameplay data can learn 3D game physics, mechanics, and temporal structure without any hand-engineered domain knowledge, suggesting that the approach is likely to generalize across existing games and ultimately to new games and genres.
- This removes the dominant bottleneck of prior creativity support tools — the need for manual domain modelling — opening the methodology to music, video, and other creative domain

## Key Claims

1. WHAM can generate consistent and diverse gameplay sequences and persist user modifications
2. Generative AI models can learn relevant structure from data without manually defining domain-specific structure, enabling broader applications than previous creativity support tools
3. Gaming is the entertainment industry's largest sector worldwide, reaching an audience of more than 3 billion people
4. Creatives in game development need diversity of divergent thinking contextualized into a consistent game world to achieve meaningful new experiences
5. Present generative AI models struggle to maintain consistency across extended generation sequences with specific rules and mechanics
6. Without contextual consistency, diversity in generated outputs risks being devoid of meaningful importance
7. Creative ideation with generative AI requires models that support direct manipulation of generated content beyond text-based prompts
8. WHAM is built on a transformer architecture using VQGAN image encoding with discrete tokens
9. WHAM was trained on approximately 500,000 anonymized gaming sessions from the game Bleeding Edge, totalling over 7 years of continuous play
10. The largest WHAM model uses 1.6 billion parameters with a 1-second context length, trained on the 7 Maps dataset

## Capabilities

- Generating consistent 3D gameplay sequences up to 2 minutes long using a 1.6B autoregressive transformer world model trained on human gameplay data
- Generating diverse alternative futures (multiple plausible continuations) from a single gameplay starting point, capturing the full distribution of human player behaviors and visual character appearances
- Persisting user-inserted game elements (objects, characters, map features) in world model video generation at 85%+ rate when conditioned on 5 edited input frames
- Learning 3D game world structure — including physics, game mechanics, and character behaviors — entirely from raw gameplay data without any domain-specific prior knowledge or handcrafted rules
- Predictable performance scaling for world models with compute — FVD (video consistency quality) reliably improves with model size and FLOPS, enabling accurate loss prediction via scaling law extrapolation
- Visual (non-language) prompting of world models using starting frames to condition generation, enabling direct image-based creative input rather than requiring text descriptions

## Limitations

- State-of-the-art generative AI models are insufficiently capable of supporting iterative tweaking and divergent thinking, creating a gap between what creative professionals need and what models can currently deliver
- WHAM context window limited to 1 second (10 frames), preventing it from considering the full game experience or maintaining coherence across longer temporal spans during generation
- Generative AI cannot reliably follow specific game rules and mechanics across extended generation, producing inconsistent outputs that break world coherence
- Scaling world models to 1.6B parameters with higher image token counts causes a degradation in action diversity relative to smaller 894M models, revealing a token budget trade-off between image fidelity and behavioral diversity
- Persistency fails or degrades significantly when only one edited input frame is provided — the model requires 5+ frames to reliably maintain user modifications, making single-shot editing unreliable
- Persistency evaluation was conducted only under artificially simplified conditions (minimal camera movement, no special effects, no complex NPC interactions, no-op controller actions), masking true performance in dynamic gameplay scenarios
- Persistency fails for small-sized edits, low-contrast insertions, or objects placed in unusual locations — reliability is highly dependent on visual salience of the modification
- WHAM cannot yet persist highly imaginative or out-of-distribution creative elements that deviate significantly from training data — only standard in-game objects and characters were successfully persisted
- Training requires a massive proprietary dataset (27.89 TiB, ~500,000 gameplay sessions, 7+ years of play) from a single commercial game under special data-sharing agreements — this is not replicable without equivalent industry partnerships
- The entire evaluation is conducted on a single 3D game (Bleeding Edge) by a single studio — cross-game, cross-genre, and cross-domain generalization of the approach is entirely unvalidated empirically
- Text-based prompting is fundamentally insufficient for supporting creative ideation in generative AI — creative workflows require direct manipulation, iterative modification, and non-linguistic control modalities
- Training compute for the 1.6B WHAM reached ~1×10²² FLOPS — this is substantial and not accessible to researchers without industrial-scale infrastructure, limiting reproducibility
- The FVD consistency metric was validated only via a preliminary correlation analysis on one model size (894M), and the link between FVD and human-perceived creative utility of generated content is not established

## Bottlenecks

- Generative AI models lack native support for iterative human manipulation workflows — models cannot accept direct visual edits, persist partial modifications across multi-step refinement, or support creative back-and-forth exploration at the granularity required by professional creatives
- Proprietary, large-scale action-labeled gameplay data is unavailable publicly — training world models for games requires exclusive partnerships with commercial studios, creating a structural access barrier that blocks replication and broader research
- Short context windows (currently ~1 second) prevent world models from maintaining awareness of global game state, narrative arc, and long-range mechanics — blocking use in full creative production pipelines where consistency across minutes or hours of content is required

## Breakthroughs

- Scaling laws confirmed for world models: world model performance (measured by FVD and training loss) reliably improves as a power law with compute and model size, analogous to scaling laws in language models — enabling principled compute allocation and loss prediction for world models
- WHAM demonstrates that autoregressive transformer world models can maintain visual and mechanical consistency across 2-minute 3D gameplay sequences — substantially extending previously demonstrated coherence horizons for complex interactive 3D environments

## Themes

- [[themes/creative_content_generation|creative_content_generation]]
- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/fréchet-video-distance-fvd|Fréchet Video Distance (FVD)]]
