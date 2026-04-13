---
type: source
title: 'Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term
  Memory'
source_id: 01KJTG8SPD68P8TGVR8248H9R4
source_type: paper
authors:
- Lin Long
- Yichen He
- Wentao Ye
- Yiyuan Pan
- Yuan Lin
- Hang Li
- Junbo Zhao
- Wei Li
published_at: '2025-08-13 00:00:00'
theme_ids:
- agent_evaluation
- agent_memory_systems
- evaluation_and_benchmarks
- knowledge_and_memory
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory

**Authors:** Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, Wei Li
**Published:** 2025-08-13 00:00:00
**Type:** paper

## Analysis

# Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory
2025-08-13 · paper · Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin et al. (8 total)
https://arxiv.org/pdf/2508.09736

---

### Motivation & Prior Limitations
- Existing long video understanding methods cannot process arbitrarily long, continuous multimodal streams online, a fundamental requirement for real-world agent deployment.
  - Context-extension and visual-token-compression approaches still process finite, offline videos and are computationally prohibitive when reprocessing full video history per instruction.
  - Memory-based online video methods (MovieChat, MA-LMM, Flash-VStream) store only encoded visual features, which cannot maintain coherent entity identity or evolving event state across long time spans.
- Language-based memory approaches (Socratic Models) describe entities with textual phrases like "a man with a beard," which are inherently ambiguous and accumulate inconsistencies over time, degrading long-term coherence.
- Existing LVQA benchmarks focus primarily on low-level visual perception (action recognition, spatial/temporal localization) and do not evaluate higher-order cognitive abilities — person understanding, general knowledge extraction, cross-modal reasoning — that are essential for agent applications.
  - Benchmarks such as EgoSchema, LongVideoBench, HourVideo, and Video-MME lack agent-perspective videos and do not include cross-modal, person, or knowledge QA categories.

---

### Proposed Approach
- M3-Agent is a multimodal agent framework with an entity-centric, multimodal long-term memory graph, operating via two parallel processes: continuous memorization from live video/audio streams, and multi-turn reasoning-based control over stored memory.
  - Unlike single-turn RAG systems, the control process employs reinforcement learning to learn iterative memory retrieval: at each round the agent either issues a `[Search]` call (using `search_node` for entity queries or `search_clip` for event queries) or emits a `[Answer]`, running for up to H=5 rounds.
  - Memory is stored as a multimodal graph whose nodes hold text, face images, or voice audio alongside embeddings and confidence weights; conflicting entries are resolved through weight-based voting so correct associations accumulate dominance over time.
- Consistent entity representation is achieved by running external facial recognition and speaker diarization tools to assign persistent `face_id` and `voice_id` identifiers, replacing fragile natural-language descriptions with stable multimodal node references across arbitrarily long streams.
  - Cross-modal identity linking (face↔voice equivalence) is performed during semantic memory generation, with a novel algorithm that mines "meta-clips" — short monologue segments containing exactly one face and one voice — to build a reliable global face-voice correspondence map.
- Two separate policy models are trained to optimal specialization: Qwen2.5-Omni-7B (visual+audio) for memorization via supervised imitation learning on GPT-4o/Gemini-1.5-Pro-synthesized demonstrations, and Qwen3-32B for control via DAPO reinforcement learning with binary correctness rewards evaluated by GPT-4o.
  - The memorization training uses a three-stage synthetic pipeline: episodic memory via hybrid GPT-4o/Gemini-1.5-Pro annotation, identity equivalence detection via meta-clip mining, and semantic memory synthesis via structured prompt templates; total training set is 26,943 clips from 500 long videos.

---

### Results & Capabilities
- M3-Agent outperforms the strongest baseline (Gemini-GPT4o-Hybrid) by 6.7%, 7.7%, and 5.3% absolute accuracy on M3-Bench-robot, M3-Bench-web, and VideoMME-long, respectively.
  - On M3-Bench-robot the strongest prior method was MA-LMM (24.4%); M3-Agent achieves 30.7%, a 6.3-point gain despite MA-LMM being a purpose-built online video architecture.
  - On VideoMME-long the Gemini-GPT4o-Hybrid prompted system scores 56.5%; M3-Agent (a trained 7B+32B open-source stack) reaches 61.8%, demonstrating that RL-trained open models can surpass prompted frontier models on long-video understanding.
- Semantic memory is the single most impactful component: ablating it reduces accuracy by 17.1%, 19.2%, and 13.1% on the three benchmarks respectively, with the largest drop on M3-Bench-web.
- DAPO reinforcement learning for control contributes 10.0%, 8.0%, and 9.3% accuracy gains over the prompted baseline (control-32b-prompt) across the three benchmarks, and scales consistently with model size from 8B to 32B parameters.
  - DAPO outperforms GRPO on all three benchmarks (e.g., 30.7% vs. 30.0% on M3-Bench-robot), though the margin is modest at the 32B scale.
- Inter-turn instruction (re-prompting the model with the original question at each retrieval round) is critical: removing it causes 10.5%, 5.8%, and 5.9% drops, indicating it prevents goal drift across multi-turn retrieval chains.
- M3-Agent shows the largest relative gains on person understanding (+15.5% over Gemini-GPT4o-Hybrid on M3-Bench-web) and cross-modal reasoning (+6.7%), the two categories most dependent on persistent, cross-modal entity identity.

---

### Implications
- The entity-centric multimodal graph architecture directly addresses the consistency problem that plagues language-only memory systems, suggesting that grounding memory in stable perceptual identifiers (face/voice embeddings) rather than natural language descriptions is a necessary design principle for long-horizon multimodal agents.
- The success of RL-trained open-source models (Qwen3-32B) over prompted frontier models (GPT-4o, Gemini-1.5-Pro) on multi-turn memory retrieval suggests that task-specific RL fine-tuning on agentic retrieval behavior is a more effective path than prompt engineering for RAG-based reasoning — a finding with direct implications for personal assistant and robotics system design.
- M3-Bench establishes a new evaluation standa

## Key Claims

1. M3-Agent outperforms the strongest baseline (Gemini-GPT4o-Hybrid) by 6.7%, 7.7%, and 5.3% on M3-Bench-robot, M3-Bench-web, and VideoMME-long respectively.
2. Removing semantic memory from M3-Agent reduces accuracy by 17.1%, 19.2%, and 13.1% on M3-Bench-robot, M3-Bench-web, and VideoMME-long respectively, demonstrating semantic memory is the most impactful 
3. Reinforcement learning training improves M3-Agent accuracy by 10.0%, 8.0%, and 9.3% on M3-Bench-robot, M3-Bench-web, and VideoMME-long respectively compared to non-RL training.
4. Removing inter-turn instructions from M3-Agent's control process decreases accuracy by 10.5%, 5.8%, and 5.9% on M3-Bench-robot, M3-Bench-web, and VideoMME-long respectively.
5. Disabling reasoning mode in M3-Agent leads to accuracy declines of 11.7%, 8.8%, and 9.5% on M3-Bench-robot, M3-Bench-web, and VideoMME-long respectively.
6. GPT-4o achieves 96% agreement with human judges when used as an automatic evaluator for open-ended video QA.
7. Existing memory-based video understanding methods that store only visual features struggle to maintain coherent long-term tracking of entities such as human identities over time.
8. Extending the context window in multimodal models or compressing visual tokens does not scale effectively for infinitely long video streams.
9. Reprocessing entire video history for each new instruction is computationally prohibitive in interactive agent scenarios.
10. Traditional video description methods focus on low-level visual details while overlooking high-level world knowledge such as character identity and entity attributes, leading to ambiguity in long-term

## Capabilities

- Multimodal agent (M3-Agent) can continuously process arbitrarily long real-time video and audio streams online, building both episodic and semantic memories incrementally without reprocessing prior history
- Entity-centric multimodal memory graph that links face, voice, and textual knowledge for the same person — enabling persistent identity tracking across arbitrarily long video streams via facial recognition and speaker diarization tools
- RL-trained (DAPO) multi-turn reasoning control policy that autonomously issues iterative memory searches and integrates retrieved evidence across up to 5 rounds, outperforming prompted frontier models on memory-based reasoning tasks
- Cross-modal reasoning to infer and link face-voice identity equivalences — automatically mining high-confidence monologue clips to establish a global face-voice correspondence that propagates across all subclips
- Weight-based voting mechanism for robust memory conflict resolution — frequently activated memory entries accumulate higher weights and override conflicting lower-weight entries, allowing the system to self-correct over time even when individual clips produce errors
- Semantic memory extraction from video observations — proactively generating world knowledge (character identities, preferences, relationships, environmental rules) from raw episodic observations rather than storing only low-level event descriptions

## Limitations

- Retaining all fine-grained episodic details in long-term memory is impractical — agents cannot selectively memorize task-relevant details without dedicated attention mechanisms, causing cognitive overload or information loss
- Text/language-based memory is fundamentally inadequate for spatial reasoning — verbal descriptions cannot retain spatial layout information as effectively as visual memory (snapshots), causing failure on tasks involving object location and spatial configuration
- Optimal multimodal agent performance requires two separate specialized policy models — one for memorization (multimodal understanding) and one for control (reasoning) — creating significant engineering overhead, inference cost, and deployment complexity
- Training data is extremely limited at 500 long videos and 2,736 QA pairs — generalization to diverse real-world deployment scenarios is unvalidated at this data scale
- Robot benchmark videos are filmed by human actors wearing head-mounted cameras rather than actual robots — genuine robot deployment gaps (hardware constraints, different sensory profiles, embodiment dynamics) are entirely untested
- Training requires 16 GPUs with 80GB memory each — infrastructure requirements are substantial and limit accessibility for most academic and small-scale research groups
- Feature-based online video understanding methods (MovieChat, MA-LMM, Flash-VStream) fail to maintain long-term entity consistency — storing only visual feature vectors cannot track evolving identity and event coherence over time
- GPT-4o cannot process audio natively — in multimodal agent evaluations requiring cross-modal audio-visual reasoning, GPT-4o must rely on ASR transcripts as a lossy audio substitute, losing prosody, speaker identity, and non-verbal cues
- Benchmark evaluation uses pre-recorded long videos simulating agent perceptual streams rather than actual real-time continuous agent operation — true online performance in live deployments remains unvalidated
- General knowledge extraction significantly underperforms relative to other question types — M3-Agent achieves 19.1% on GK vs 43.3% on person understanding on M3-Bench-robot, revealing a sharp performance cliff for inductive world-knowledge generalization
- Language-based character descriptions ('a man with a beard', 'a woman in a red dress') are inherently ambiguous and accumulate inconsistencies over extended time spans — a fundamental limitation of text-only memory for dynamic agent scenarios with many characters
- Control reasoning process is capped at a fixed maximum of 5 rounds — tasks requiring deeper evidence synthesis chains or broader memory search cannot exceed this limit, creating a hard performance ceiling for complex queries
- Single-turn RAG is insufficient for memory-based reasoning in long-context agent scenarios — retrieving all relevant memory in one shot fails for tasks requiring iterative narrowing and multi-hop evidence synthesis

## Bottlenecks

- No principled selective memorization mechanism exists — agents lack the ability to focus memory resources on task-relevant details and ignore irrelevant ones during continuous observation, causing cognitive overload at scale
- Text-centric memory architectures cannot represent spatial information adequately — incorporating visual snapshots or geometric representations for spatial memory is necessary but significantly increases storage and retrieval cost
- Real robot video data collection is prohibitively expensive and logistically complex — hardware costs, operational constraints, and deployment complexity prevent large-scale robot-perspective dataset creation for training and evaluation
- Long-term entity identity consistency in multimodal streams is unsolved by existing approaches — feature-based methods fail, language descriptions are ambiguous, and hybrid architectures require expensive facial recognition and speaker diarization pipelines

## Breakthroughs

- RL-trained open-source multimodal agent (7B memorization + 32B control) consistently surpasses prompted frontier model combinations (Gemini-1.5-Pro + GPT-4o hybrid) on long-term memory-based reasoning — demonstrating that task-specific RL training dominates scale for memory tasks
- Semantic memory (abstract world knowledge extracted from observations) contributes 17–19% accuracy improvement over episodic-only memory — empirically establishing semantic abstraction as the dominant component of effective long-term agent memory

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/vision_language_models|vision_language_models]]
