---
type: theme
title: Vision-Language-Action Models
theme_id: vision_language_action_models
level: 2
parent_theme: robotics_and_embodied_ai
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 25
sources_since_update: 0
update_count: 1
velocity: 0.34
staleness: 0.0
status: active
tags: []
---
- **Capabilities** rendered as a table for scannability rather than a flat list
- **Limitations** grouped thematically (performance cliffs, architectural constraints, reasoning-action integration, etc.) rather than listed individually, since many are interrelated
- **Contradictions** section surfaced three genuine tensions in the data: aggregate vs. subset success metrics, the reasoning-dexterity fine-tuning trade-off, and the open-source-inference vs. closed-training distinction
- **Research Opportunities** derived from the bottleneck and limitation data, each tied to a specific finding rather than generic suggestions
- Em dashes minimized throughout per writing style preferences

## Current State

## Capabilities

## Limitations

## Bottlenecks

## Breakthroughs

## Anticipations

## Cross-Theme Implications

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-03-10** — [[sources/01KM247D7R-can-world-models-unlock-general-purpose-robotics|Can world models unlock general purpose robotics?]]: V-JEPA 2 takes approximately 16 seconds per action, which is roughly 100x too slow for real-time rob
- **2025-12-06** — [[sources/01KJVMEPM5-world-models-general-intuition-khoslas-largest-bet-since-llms-openai|World Models & General Intuition: Khosla's largest bet since LLMs & OpenAI]]: General Intuition raised a $134 million seed round led by Ka Ventures (Vinod Khosla), described as K
- **2025-12-04** — [[sources/01KJT636TN-sima-2-a-generalist-embodied-agent-for-virtual-worlds|SIMA 2: A Generalist Embodied Agent for Virtual Worlds]]: SIMA 1 was limited to short and direct instructions, could not respond in language or reason about i
- **2025-12-02** — [[sources/01KJSZ22MD-vision-native-ai-opportunities-a-precursor-to-intelligent-robotics|Vision-native AI opportunities: a precursor to intelligent robotics]]: Hybrid VLA architectures are becoming the standard, with large VLMs handling cloud-side planning and
- **2025-11-18** — [[sources/01KJT838Q9-π-06-a-vla-that-learns-from-experience|$π^{*}_{0.6}$: a VLA That Learns From Experience]]: RECAP pre-trains on tens of thousands of hours of demonstrations from numerous tasks and a variety o
- **2025-11-12** — [[sources/01KJT9K4DJ-wmpo-world-model-based-policy-optimization-for-vision-language-action-models|WMPO: World Model-based Policy Optimization for Vision-Language-Action Models]]: WMPO enables on-policy GRPO for VLA models without any interaction with the real environment by usin
- **2025-09-12** — [[sources/01KJVN12YG-fully-autonomous-robots-are-much-closer-than-you-think-sergey-levine|Fully autonomous robots are much closer than you think – Sergey Levine]]: Physical Intelligence aims to build general-purpose robotic foundation models capable of controlling
- **2025-09-01** — [[sources/01KJTK2Z9A-robix-a-unified-model-for-robot-interaction-reasoning-and-planning|Robix: A Unified Model for Robot Interaction, Reasoning and Planning]]: Robix introduces novel capabilities including proactive dialogue, real-time interruption handling, a
- **2025-07-08** — [[sources/01KJVN4FS2-2-robotics-pioneers-unpack-the-path-to-generalist-robots|2 Robotics Pioneers Unpack the Path to Generalist Robots]]: Current robotics foundation models are demo-ready but not deployment-ready, as they still fail frequ
- **2025-06-26** — [[sources/01KJTPB47Q-worldvla-towards-autoregressive-action-world-model|WorldVLA: Towards Autoregressive Action World Model]]: WorldVLA is initialized from Chameleon, a unified model for image understanding and generation.
- **2025-06-24** — [[sources/01KJTPGRRA-unified-vision-language-action-model|Unified Vision-Language-Action Model]]: UniVLA achieves an average sequence length of 4.41 on the CALVIN ABC→D benchmark, exceeding the prio
- **2025-04-22** — [[sources/01KJTYN6R6-π-05-a-vision-language-action-model-with-open-world-generalization|$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization]]: π0.5 has limitations including susceptibility to unfamiliar drawer handles, difficulty with partial 
- **2025-03-27** — [[sources/01KJV26GZX-cot-vla-visual-chain-of-thought-reasoning-for-vision-language-action-models|CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models]]: CoT-VLA generates subgoal images as intermediate visual reasoning steps before generating action seq
- **2025-03-18** — [[sources/01KKT532F3-2025-3-18|2025-3-18]]: Breakthrough: GR00T N1: First open-source generalist VLA foundation model for humanoid robots 
- **2025-03-18** — [[sources/01KKT56P61-2025-3-18|2025-3-18]]: New capability: Multimodal LLMs can reason about physical common sense (space, time, fundamental
- **2025-03-11** — [[sources/01KKT5AKA5-gemini-robotics-bringing-ai-into-the-physical|Gemini Robotics: Bringing AI into the Physical]]: Breakthrough: A single foundation VLM (Gemini 2.0 / Gemini Robotics-ER) now unifies all robot 
- **2025-03-11** — [[sources/01KJV2VB8A-proc4gem-foundation-models-for-physical-agency-through-procedural-generation|Proc4Gem: Foundation models for physical agency through procedural generation]]: On an out-of-distribution target (toy giraffe), the SPOC baseline achieves 0% success while Gemini a
- **2025-02-26** — [[sources/01KJVN5D5F-self-driving-expert-unpacks-the-biggest-breakthroughs-and-bottlenecks|Self-Driving Expert Unpacks the Biggest Breakthroughs and Bottlenecks]]: Waymo uses cameras, lidars, and radars as complementary sensors whose strengths and weaknesses are o
- **2025-02-20** — [[sources/01KJSWHZY2-helix-a-vision-language-action-model-for-generalist-humanoid-control|Helix: A Vision-Language-Action Model for Generalist Humanoid Control]]: Helix's System 2 is an internet-pretrained VLM operating at 7-9 Hz for scene understanding and langu
- **2024-10-15** — [[sources/01KJV7DD3S-latent-action-pretraining-from-videos|Latent Action Pretraining from Videos]]: LAPA uses a VQ-VAE-based objective to learn discrete latent actions between image frames in a fully 
- **2024-09-17** — [[sources/01KJVMZ5JN-jim-fan-on-nvidias-embodied-ai-lab-and-jensen-huangs-prediction-that-all-robots-|Jim Fan on Nvidia’s Embodied AI Lab and Jensen Huang’s Prediction that All Robots will be Autonomous]]: Internet-scale data lacks motor control signals and cannot provide the action data required to train
- **2024-06-13** — [[sources/01KJV8JK29-openvla-an-open-source-vision-language-action-model|OpenVLA: An Open-Source Vision-Language-Action Model]]: VLAs that directly fine-tune VLMs for action prediction take a more end-to-end approach than prior g
- **2024-05-10** — [[sources/01KJVNEG9Q-the-future-of-robotics|The future of robotics]]: Research-grade robot arms cost between $40,000 and $70,000.
- **2024-04-22** — [[sources/01KJVN9ZJX-robotics-research-update-with-keerthana-gopalakrishnan-and-ted-xiao-of-google-de|Robotics Research Update, with Keerthana Gopalakrishnan and Ted Xiao of Google DeepMind]]: PIVOT enables zero-shot robot guidance using vision-language models without any special fine-tuning 
- **2024-04-11** — [[sources/01KJVN834B-robotics-in-the-age-of-generative-ai-with-vincent-vanhoucke-google-deepmind-nvid|Robotics in the Age of Generative AI with Vincent Vanhoucke, Google DeepMind | NVIDIA GTC 2024]]: RT2 treats robot actions as just another language in a multilingual VLM, outputting action tokens al
