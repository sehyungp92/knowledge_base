---
type: theme
title: Multimodal Models
theme_id: multimodal_models
level: 1
parent_theme: model_architecture
child_themes:
- vision_language_models
- unified_multimodal_models
- audio_and_speech_models
- robotics_and_embodied_ai
- generative_media
created: '2026-04-08'
updated: '2026-04-08'
source_count: 67
sources_since_update: 0
update_count: 1
velocity: 0.015
staleness: 0.0
status: active
tags: []
---
- **Current State** is a temporal narrative covering the 1D-sequence architectural constraint, the language-as-lossy-channel problem, the conspicuous absence of capabilities/breakthroughs (attributed to thin coverage rather than genuine stasis), and the watch signal for what to ingest next.
- **Limitations** expands both recorded entries with their severity, trajectory, and type labels.
- **Cross-Theme Implications** covers both provided signals: the generative media finding (flow-matching DiT tractability) and the self-evolving agent finding (compositional tool use as a substitute for native multimodal architecture).
- **Research Opportunities** synthesizes the limitations and cross-theme signals into four concrete research directions without adding speculative content beyond what the data supports.
- Empty sections are marked with a note rather than left blank, so the structure is explicit about what is missing.
- No em dashes used; no frontmatter included.

## Current State

## Capabilities

## Limitations

## Bottlenecks

## Breakthroughs

## Anticipations

## Cross-Theme Implications

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJSW6SGQ-crossing-the-uncanny-valley-of-conversational-voice|Crossing the uncanny valley of conversational voice]]: Three model sizes were trained: Tiny (1B backbone, 100M decoder), Small (3B backbone, 250M decoder),
- **2026-01-05** — [[sources/01KJT2D42H-nextflow-unified-sequential-modeling-activates-multimodal-understanding-and-gene|NextFlow: Unified Sequential Modeling Activates Multimodal Understanding and Generation]]: NextFlow retains next-token prediction for text generation but adopts next-scale prediction for visu
- **2025-12-16** — [[sources/01KJT37Q1W-t5gemma-2-seeing-reading-and-understanding-longer|T5Gemma 2: Seeing, Reading, and Understanding Longer]]: T5Gemma 2 adapts pretrained decoder-only Gemma 3 models into encoder-decoder models using the UL2 ob
- **2025-12-03** — [[sources/01KJT6CAK6-thinking-with-programming-vision-towards-a-unified-view-for-thinking-with-images|Thinking with Programming Vision: Towards a Unified View for Thinking with Images]]: State-of-the-art MLLMs are surprisingly brittle to simple orientation changes, with simple rotation/
- **2025-12-02** — [[sources/01KJSZ22MD-vision-native-ai-opportunities-a-precursor-to-intelligent-robotics|Vision-native AI opportunities: a precursor to intelligent robotics]]: Hybrid VLA architectures are becoming the standard, with large VLMs handling cloud-side planning and
- **2025-11-26** — [[sources/01KJT6V2CT-monet-reasoning-in-latent-visual-space-beyond-images-and-language|Monet: Reasoning in Latent Visual Space Beyond Images and Language]]: Monet introduces a three-stage distillation-based SFT pipeline that enables MLLMs to generate contin
- **2025-11-21** — [[sources/01KJT7H2D2-downscaling-intelligence-exploring-perception-and-reasoning-bottlenecks-in-small|Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models]]: Visual extraction tuning is a training paradigm in which the model explicitly learns to extract the 
- **2025-11-15** — [[sources/01KJT8TG9R-mixture-of-states-routing-token-level-dynamics-for-multimodal-generation|Mixture of States: Routing Token-Level Dynamics for Multimodal Generation]]: The MoS router contributes only 0.008 seconds per iteration on a single A100 GPU for a 3B generation
- **2025-11-12** — [[sources/01KJT9BRN1-lumine-an-open-recipe-for-building-generalist-agents-in-3d-open-worlds|Lumine: An Open Recipe for Building Generalist Agents in 3D Open Worlds]]: Lumine processes raw pixels at 5 Hz to produce precise 30 Hz keyboard-mouse actions via action chunk
- **2025-11-12** — [[sources/01KJT8GR21-pan-a-world-model-for-general-interactable-and-long-horizon-world-simulation|PAN: A World Model for General, Interactable, and Long-Horizon World Simulation]]: PAN employs the Generative Latent Prediction (GLP) architecture that combines an autoregressive LLM-
- **2025-11-06** — [[sources/01KJTAMFNJ-v-thinker-interactive-thinking-with-images|V-Thinker: Interactive Thinking with Images]]: V-Thinker treats reasoning as a code-driven visual interaction process where at each step the model 
- **2025-10-30** — [[sources/01KJTBCK7K-thinkmorph-emergent-properties-in-multimodal-interleaved-chain-of-thought-reason|ThinkMorph: Emergent Properties in Multimodal Interleaved Chain-of-Thought Reasoning]]: ThinkMorph is a unified model fine-tuned on approximately 24K high-quality interleaved reasoning tra
- **2025-10-23** — [[sources/01KJTCC049-open-o3-video-grounded-video-reasoning-with-explicit-spatio-temporal-evidence|Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence]]: Open-o3 Video achieves state-of-the-art performance on V-STAR, improving mAM by +14.4% and mLGM by +
- **2025-10-17** — [[sources/01KKT3SS8Q-deepseek-ocr-contexts-optical-compression|DeepSeek-OCR: Contexts Optical Compression]]: DeepEncoder uses a 2-layer convolutional module performing 16× downsampling between SAM and CLIP com
- **2025-09-24** — [[sources/01KJTG79VB-video-models-are-zero-shot-learners-and-reasoners|Video models are zero-shot learners and reasoners]]: Veo 3 was announced in May 2025 and released in July 2025; Veo 2 was announced December 2024 and rel
- **2025-09-17** — [[sources/01KJTHGA5B-atoken-a-unified-tokenizer-for-vision|AToken: A Unified Tokenizer for Vision]]: ATOKEN achieves 0.21 rFID with 82.2% ImageNet zero-shot accuracy for images, 3.01 rFVD with 40.2% MS
- **2025-09-02** — [[sources/01KJTKT231-why-do-mllms-struggle-with-spatial-understanding-a-systematic-analysis-from-data|Why Do MLLMs Struggle with Spatial Understanding? A Systematic Analysis from Data to Architecture]]: Spatial understanding in MLLMs relies more heavily on positional encoding within the visual encoder 
- **2025-08-13** — [[sources/01KJTG8SPD-seeing-listening-remembering-and-reasoning-a-multimodal-agent-with-long-term-mem|Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory]]: Removing semantic memory from M3-Agent reduces accuracy by 17.1%, 19.2%, and 13.1% on M3-Bench-robot
- **2025-08-07** — [[sources/01KJS40HGR-gpt-5s-vision-checkup-a-frontier-vision-reasoning-model-but-not-a-new-sota|GPT-5's Vision Checkup: a frontier Vision Reasoning Model, but -not- a new SOTA]]: Gemini 2.5 Pro is the current SOTA on RF100-VL with a zero-shot mAP50:95 of 13.3.
- **2025-06-30** — [[sources/01KJTNW0W4-thinking-with-images-for-multimodal-reasoning-foundations-methods-and-future-fro|Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers]]: The dominant multimodal reasoning paradigm ('Thinking about Images') treats the visual modality as a
- **2025-06-26** — [[sources/01KJTPB47Q-worldvla-towards-autoregressive-action-world-model|WorldVLA: Towards Autoregressive Action World Model]]: WorldVLA is initialized from Chameleon, a unified model for image understanding and generation.
- **2025-06-24** — [[sources/01KJTPGRRA-unified-vision-language-action-model|Unified Vision-Language-Action Model]]: UniVLA raises the SimplerEnv-WidowX average success rate from 42.7% (SpatialVLA) to 69.8%.
- **2025-06-23** — [[sources/01KJTPFD62-omnigen2-exploration-to-advanced-multimodal-generation|OmniGen2: Exploration to Advanced Multimodal Generation]]: OmniGen2 achieves a GenEval overall score of 0.86 with an LLM rewriter, surpassing UniWorld-V1 (0.84
- **2025-06-23** — [[sources/01KJTPP5WB-vision-as-a-dialect-unifying-visual-understanding-and-generation-via-text-aligne|Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations]]: The LLM token embeddings in TA-Tok's codebook are always frozen; only the projection matrix W is tra
- **2025-06-18** — [[sources/01KJTPVSWT-show-o2-improved-native-unified-multimodal-models|Show-o2: Improved Native Unified Multimodal Models]]: Native unified multimodal models natively combine multimodal understanding and generation objectives
- **2025-06-12** — [[sources/01KJTQ65VX-videoexplorer-think-with-videos-for-agentic-long-video-understanding|VideoExplorer: Think With Videos For Agentic Long-Video Understanding]]: VideoExplorer with a 7B planner and 7B VLM achieves 51.7% average accuracy across LVBench, MLVU, and
- **2025-05-30** — [[sources/01KJTQZ7NZ-continual-learning-in-vision-language-models-via-aligned-model-merging|Continual Learning in Vision-Language Models via Aligned Model Merging]]: PAM achieves an average accuracy of 49.89 ± 1.66 on the CoIN benchmark, compared to 43.36 ± 8.18 for
- **2025-05-29** — [[sources/01KJTRR26F-grounded-reinforcement-learning-for-visual-reasoning|Grounded Reinforcement Learning for Visual Reasoning]]: ViGoRL-7B achieves 91.0% on ScreenSpot-V2 and 33.1% on ScreenSpot-Pro, outperforming open-source VLM
- **2025-05-21** — [[sources/01KJTTRBRJ-mmada-multimodal-large-diffusion-language-models|MMaDA: Multimodal Large Diffusion Language Models]]: Prior multimodal approaches combining language models with diffusion models handled discrete and con
- **2025-05-20** — [[sources/01KJTT03GZ-emerging-properties-in-unified-multimodal-pretraining|Emerging Properties in Unified Multimodal Pretraining]]: BAGEL uses QK-Norm in each attention block to stabilize the training process, following common pract
- **2025-05-08** — [[sources/01KJTNQNAG-perception-reason-think-and-plan-a-survey-on-large-multimodal-reasoning-models|Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models]]: Early multimodal reasoning systems employed CNNs and LSTM networks within supervised learning framew
- **2025-05-07** — [[sources/01KJTWFJBZ-on-path-to-multimodal-generalist-general-level-and-general-bench|On Path to Multimodal Generalist: General-Level and General-Bench]]: General-Level evaluation framework defines 5 scaling levels of MLLM performance and generality, cent
- **2025-05-06** — [[sources/01KKT4FGMX-2025-5-6|2025-5-6]]: The OSCE study used 105 scenarios across three modality types (35 skin photos, 35 ECGs, 35 clinical 
- **2025-05-05** — [[sources/01KJTWJ62T-voila-voice-language-foundation-models-for-real-time-autonomous-interaction-and-|Voila: Voice-Language Foundation Models for Real-Time Autonomous Interaction and Voice Role-Play]]: The Voila Benchmark comprises 1,580 samples across 66 subjects drawn from MMLU, MATH, OpenAI HumanEv
- **2025-05-05** — [[sources/01KJTVQTFF-ming-lite-uni-advancements-in-unified-architecture-for-natural-multimodal-intera|Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction]]: Ming-Lite-Uni is in alpha stage at time of publication and will be further refined.
- **2025-04-29** — [[sources/01KJTX3RQ3-x-fusion-introducing-new-modality-to-frozen-large-language-models|X-Fusion: Introducing New Modality to Frozen Large Language Models]]: Training on noisy images for I2T (understanding) tasks degrades image understanding performance, wit
- **2025-04-24** — [[sources/01KJTXK7YZ-token-shuffle-towards-high-resolution-image-generation-with-autoregressive-model|Token-Shuffle: Towards High-Resolution Image Generation with Autoregressive Models]]: Token-Shuffle is the first method to push autoregressive text-to-image generation to a resolution of
- **2025-04-23** — [[sources/01KJTXS7VE-skywork-r1v2-multimodal-hybrid-reinforcement-learning-for-reasoning|Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning]]: Future versions of R1V2 will focus on enhancing general visual capabilities while preserving the str
- **2025-04-10** — [[sources/01KJTPMJBF-kimi-vl-technical-report|Kimi-VL Technical Report]]: Reasoning data for RL training is generated by sampling reasoning trajectories using Kimi k1.5 as th
- **2025-04-08** — [[sources/01KJV0MQH7-transfer-between-modalities-with-metaqueries|Transfer between Modalities with MetaQueries]]: The MetaQuery approach follows a token → [transformer] → [diffusion] → pixels paradigm that composes
- **2025-03-26** — [[sources/01KJV2A0J3-qwen25-omni-technical-report|Qwen2.5-Omni Technical Report]]: Each image in Qwen2.5-Omni is treated as two identical frames for consistency with video processing.
- **2025-03-18** — [[sources/01KJVVDA1F-why-ai-voice-feels-more-human-than-ever|Why AI Voice Feels More Human Than Ever]]: Latency has dropped dramatically: one year ago, 2–3 seconds was acceptable; now even 0.5–1 second of
- **2025-03-11** — [[sources/01KJV31KSH-gtr-guided-thought-reinforcement-prevents-thought-collapse-in-rl-based-vlm-agent|GTR: Guided Thought Reinforcement Prevents Thought Collapse in RL-based VLM Agent Training]]: GTR achieves a 17.5% success rate on Points24, compared to GPT-4o+Tool at 13.5%, SFT-only at 11.0%, 
- **2025-03-09** — [[sources/01KJV2XQ8N-vision-r1-incentivizing-reasoning-capability-in-multimodal-large-language-models|Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models]]: Vision-R1-CI (cold-start only, no RL) on the Llama-3.2-11B base improves MathVista from 48.6% to 62.
- **2025-03-03** — [[sources/01KJV3M3CC-visual-rft-visual-reinforcement-fine-tuning|Visual-RFT: Visual Reinforcement Fine-Tuning]]: Visual-RFT improves accuracy by 24.3% over the baseline in one-shot fine-grained image classificatio
- **2025-02-19** — [[sources/01KJV42M0K-qwen25-vl-technical-report|Qwen2.5-VL Technical Report]]: Qwen2.5-VL's MRoPE decomposes position embeddings into three components—temporal, height, and width—
- **2025-02-03** — [[sources/01KJV4QZ2D-omnihuman-1-rethinking-the-scaling-up-of-one-stage-conditioned-human-animation-m|OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models]]: OmniHuman was trained on 18.7K hours of in-house human-related data filtered based on aesthetics, im
- **2025-01-22** — [[sources/01KJV50MCD-kimi-k15-scaling-reinforcement-learning-with-llms|Kimi k1.5: Scaling Reinforcement Learning with LLMs]]: From 1,000 online contest coding problems, approximately 614 did not require a special judge, and 32
- **2024-12-19** — [[sources/01KJV5SBG0-lmfusion-adapting-pretrained-language-models-for-multimodal-generation|LMFusion: Adapting Pretrained Language Models for Multimodal Generation]]: Transfusion combines autoregressive language modeling with diffusion-based image generation in a sin
- **2024-11-19** — [[sources/01KJVTRDK8-a-deep-dive-into-the-future-of-voice-in-ai|A Deep Dive into the Future of Voice in AI]]: Traditional voice mode used a speech-to-text step to convert audio to text, which was then sent into
- **2024-11-15** — [[sources/01KJV6G030-llava-cot-let-vision-language-models-reason-step-by-step|LLaVA-CoT: Let Vision Language Models Reason Step-by-Step]]: InternLM-XComposer2.5-Reward was used as the reward model to judge generation quality during test-ti
- **2024-11-12** — [[sources/01KJV6X74J-janusflow-harmonizing-autoregression-and-rectified-flow-for-unified-multimodal-u|JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation]]: JanusFlow's generation encoder (g_enc) and decoder (g_dec) are lightweight, containing approximately
- **2024-10-17** — [[sources/01KJV79X7A-movie-gen-a-cast-of-media-foundation-models|Movie Gen: A Cast of Media Foundation Models]]: Movie Gen Video Bench is a publicly released benchmark of 1003 prompts covering human activity, anim
- **2024-10-17** — [[sources/01KJV7CCFG-janus-decoupling-visual-encoding-for-unified-multimodal-understanding-and-genera|Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation]]: Janus employs a three-stage training procedure: (1) training adaptors and image head with frozen enc
- **2024-10-15** — [[sources/01KJT0GCSN-part-ii-multimodal-capabilities-unlock-new-opportunities-in-vertical-ai|Part II: Multimodal capabilities unlock new opportunities in Vertical AI]]: Google's Gemini 1.5 Pro can understand both image and video input and retain contextual understandin
- **2024-10-10** — [[sources/01KJV7PXBQ-agent-s-an-open-agentic-framework-that-uses-computers-like-a-human|Agent S: An Open Agentic Framework that Uses Computers Like a Human]]: The Worker's Trajectory Reflector observes the entire episode in real time and provides reflective a
- **2024-10-09** — [[sources/01KJV7TRY2-pixtral-12b|Pixtral 12B]]: Pixtral's multimodal decoder uses a causal self-attention mechanism that enables multi-image convers
- **2024-10-03** — [[sources/01KJVNQNBD-ai-at-the-intersection-of-bio-vijay-pande-surya-ganguli-bowen-liu|AI at the Intersection of Bio | Vijay Pande, Surya Ganguli & Bowen Liu]]: ChatGPT demonstrated capabilities that were entirely unpredicted, marking a qualitative shift in AI
- **2024-09-20** — [[sources/01KJVMK38D-the-future-of-ai-is-here-fei-fei-li-unveils-the-next-frontier-of-ai|“The Future of AI is Here” — Fei-Fei Li Unveils the Next Frontier of AI]]: Limitation identified: Multimodal LLMs use 1D token sequence representation fundamentally unsuited for 
- **2024-09-17** — [[sources/01KJV89Q4X-moshi-a-speech-text-foundation-model-for-real-time-dialogue|Moshi: a speech-text foundation model for real-time dialogue]]: Moshi is trained in four stages: audio pre-training on unsupervised data, post-training with simulat
- **2024-09-09** — [[sources/01KJVMXKY9-lumas-dream-machine-and-reasoning-in-video-models|Luma's Dream Machine and Reasoning in Video Models]]: Dream Machine is a foundational video generative model supporting both text-to-video and image-to-vi
- **2024-06-27** — [[sources/01KJV3VT1C-colpali-efficient-document-retrieval-with-vision-language-models|ColPali: Efficient Document Retrieval with Vision Language Models]]: Contrastive VLMs (Jina-CLIP, Nomic-vision) perform far worse than text-based pipelines on visually r
- **2024-06-20** — [[sources/01KJVRCA1S-vertical-ai-shows-potential-to-dwarf-legacy-saas-state-of-the-cloud-2024|Vertical AI shows potential to dwarf legacy SaaS | State of the Cloud 2024]]: Bridge automates medical documentation by recording patient conversations, summarizing and transcrib
- **2024-06-13** — [[sources/01KJV8JK29-openvla-an-open-source-vision-language-action-model|OpenVLA: An Open-Source Vision-Language-Action Model]]: The Prismatic VLM backbone outperformed LLaVA by approximately 10% absolute success rate on both sim
- **2024-05-13** — [[sources/01KJV91QH9-the-platonic-representation-hypothesis|The Platonic Representation Hypothesis]]: Neural networks trained with different objectives on different data and modalities are converging to
- **2024-04-11** — [[sources/01KJVN834B-robotics-in-the-age-of-generative-ai-with-vincent-vanhoucke-google-deepmind-nvid|Robotics in the Age of Generative AI with Vincent Vanhoucke, Google DeepMind | NVIDIA GTC 2024]]: The SayCan system uses a large language model to propose solutions to complex planning problems, ran
- **2024-01-25** — [[sources/01KJV9RNVZ-webvoyager-building-an-end-to-end-web-agent-with-large-multimodal-models|WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models]]: Inter-human annotator Fleiss Kappa before discussion is 0.7, indicating substantial agreement on web
