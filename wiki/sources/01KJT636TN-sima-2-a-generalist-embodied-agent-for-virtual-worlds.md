---
type: source
title: 'SIMA 2: A Generalist Embodied Agent for Virtual Worlds'
source_id: 01KJT636TN4PH9BH7MEJZ86AVM
source_type: paper
authors:
- SIMA team
- Adrian Bolton
- Alexander Lerchner
- Alexandra Cordell
- Alexandre Moufarek
- Andrew Bolt
- Andrew Lampinen
- Anna Mitenkova
- Arne Olav Hallingstad
- Bojan Vujatovic
- Bonnie Li
- Cong Lu
- Daan Wierstra
- Daniel P. Sawyer
- Daniel Slater
- David Reichert
- Davide Vercelli
- Demis Hassabis
- Drew A. Hudson
- Duncan Williams
- Ed Hirst
- Fabio Pardo
- Felix Hill
- Frederic Besse
- Hannah Openshaw
- Harris Chan
- Hubert Soyer
- Jane X. Wang
- Jeff Clune
- John Agapiou
- John Reid
- Joseph Marino
- Junkyung Kim
- Karol Gregor
- Kaustubh Sridhar
- Kay McKinney
- Laura Kampis
- Lei M. Zhang
- Loic Matthey
- Luyu Wang
- Maria Abi Raad
- Maria Loks-Thompson
- Martin Engelcke
- Matija Kecman
- Matthew Jackson
- Maxime Gazeau
- Ollie Purkiss
- Oscar Knagg
- Peter Stys
- Piermaria Mendolicchio
- Raia Hadsell
- Rosemary Ke
- Ryan Faulkner
- Sarah Chakera
- Satinder Singh Baveja
- Shane Legg
- Sheleem Kashem
- Tayfun Terzi
- Thomas Keck
- Tim Harley
- Tim Scholtes
- Tyson Roberts
- Volodymyr Mnih
- Yulan Liu
- Zhengdong Wang
- Zoubin Ghahramani
published_at: '2025-12-04 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- robotics_and_embodied_ai
- spatial_and_3d_intelligence
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# SIMA 2: A Generalist Embodied Agent for Virtual Worlds

**Authors:** SIMA team, Adrian Bolton, Alexander Lerchner, Alexandra Cordell, Alexandre Moufarek, Andrew Bolt, Andrew Lampinen, Anna Mitenkova, Arne Olav Hallingstad, Bojan Vujatovic, Bonnie Li, Cong Lu, Daan Wierstra, Daniel P. Sawyer, Daniel Slater, David Reichert, Davide Vercelli, Demis Hassabis, Drew A. Hudson, Duncan Williams, Ed Hirst, Fabio Pardo, Felix Hill, Frederic Besse, Hannah Openshaw, Harris Chan, Hubert Soyer, Jane X. Wang, Jeff Clune, John Agapiou, John Reid, Joseph Marino, Junkyung Kim, Karol Gregor, Kaustubh Sridhar, Kay McKinney, Laura Kampis, Lei M. Zhang, Loic Matthey, Luyu Wang, Maria Abi Raad, Maria Loks-Thompson, Martin Engelcke, Matija Kecman, Matthew Jackson, Maxime Gazeau, Ollie Purkiss, Oscar Knagg, Peter Stys, Piermaria Mendolicchio, Raia Hadsell, Rosemary Ke, Ryan Faulkner, Sarah Chakera, Satinder Singh Baveja, Shane Legg, Sheleem Kashem, Tayfun Terzi, Thomas Keck, Tim Harley, Tim Scholtes, Tyson Roberts, Volodymyr Mnih, Yulan Liu, Zhengdong Wang, Zoubin Ghahramani
**Published:** 2025-12-04 00:00:00
**Type:** paper

## Analysis

# SIMA 2: A Generalist Embodied Agent for Virtual Worlds
2025-12-04 · paper · SIMA team, Adrian Bolton, Alexander Lerchner, Alexandra Cordell, Alexandre Moufarek et al. (66 total)
https://arxiv.org/pdf/2512.04797v1

---

### Motivation & Prior Limitations
Foundation models trained on static internet-scale data produce fundamentally disembodied intelligence — they are passive and lack the low-level sensorimotor capabilities needed to act in 3D worlds, a modern instantiation of Moravec's Paradox where chess-playing proves easier than clearing a dinner table.
- SIMA 1, the direct predecessor, was limited to short, direct natural language commands (e.g., "Go to the campfire"), could not produce text output, reason internally, process multi-modal inputs, or generalize robustly to novel environments or instructions.
  - SIMA 1 trained language encoding from scratch, constraining instruction-following to the vocabulary of annotated gameplay data and making it brittle outside training distributions.
- Baseline frontier models (Gemini Flash-Lite and Pro, without embodied finetuning) achieve only 3.2% and 7.0% success on embodied tasks, demonstrating that embodied competence is not an emergent property of large-scale vision-language pretraining — it must be explicitly trained.
- Existing VLA agents are trained on fixed demonstration datasets and do not possess a mechanism for autonomous skill acquisition; they represent a trained artifact rather than a learning process, leaving the questions of how to define open-ended tasks and compute rewards in novel environments largely unresolved.

---

### Proposed Approach
SIMA 2 is a Vision-Language-Action (VLA) agent built on a Gemini Flash-Lite foundation model, finetuned on a mixture of human gameplay demonstrations and synthetically-generated "bridge data," with a subsequent reinforcement learning stage on verifiable tasks, enabling unified perception, reasoning, dialogue, and keyboard-and-mouse action within a single token stream.
- The architecture unifies vision, language, and action as a single structured text output that is deterministically parsed into low-level keyboard and mouse commands, internal reasoning, and dialogue — eliminating the strict input/output constraints of SIMA 1 and enabling emergent multi-modal interaction.
  - The agent receives 720p RGB video frames and a natural language/image instruction; it outputs chunks of actions alongside optional internal reasoning and dialogue tokens, with the agent itself specifying which output modalities to generate at each step.
- "Bridge data" is a key training innovation: a small set of high-quality gameplay trajectories is annotated by Gemini Pro with causally-consistent internal reasoning and dialogue interleaved with low-level actions, bridging the gap between embodied motor control and high-level language understanding.
  - Bridge data includes error-correcting behavior, instruction chaining, visual question answering, memory-dependent behavior, and no-ops to signal task completion — capabilities absent from raw human gameplay recordings.
- A supervised finetuning (SFT) stage is followed by online reinforcement learning from verifiable rewards on curated (initial state, instruction, verification function) triples, with shaped rewards to improve instruction-following controllability.
- For open-ended self-improvement, three Gemini instances are composed: a Task Setter that proposes achievable instructions from the current environment state, the SIMA 2 agent that executes them, and a Gemini-based reward model that scores trajectories (0–100 rubric, calibrated against human preference pairs) to generate a training signal without access to ground-truth game state.
  - This three-component loop is deployed inside a running game instance with no privileged state access — the reward model operates purely on pixels and natural language goals, directly addressing the long-standing challenge of defining universal reward functions in open-world settings.

---

### Results & Capabilities
SIMA 2 effectively doubles SIMA 1's average success rate on training environments, approaching human-level performance across both human-evaluated (65% SIMA 2 vs. 33% SIMA 1 vs. 66% human) and automatically-evaluated (86% SIMA 2 vs. 30% SIMA 1 vs. 78% human) task suites.
- Per-environment improvements range from +18% to +57% absolute success rate on human evaluations and +5% to +57% on automatic evaluations, with the largest gains in complex commercial video game environments requiring menu navigation and diverse game dynamics.
- On entirely held-out environments (ASKA and MineDojo), SIMA 2 outperforms SIMA 1 by over 12–13% absolute, completing tasks in 26 out of 50 MineDojo task categories, while SIMA 1 could only complete 2 task types — demonstrating qualitatively stronger generalization.
  - Naive human baselines (no prior game experience) achieved ~19% on MineDojo and ~32% on ASKA, placing SIMA 2's held-out generalization in the same order of magnitude as a first-time human player.
- SIMA 2 acquires qualitatively new capabilities absent in SIMA 1: embodied dialogue (including embodied question-answering requiring navigation to gather information), internal chain-of-thought reasoning that modifies behavior, complex multi-step instruction following, multilingual instruction following (French, German, Mandarin), emoji-based instruction parsing, and multi-modal prompting via sketches or diagrams.
- Despite extensive finetuning on low-level action data, SIMA 2 retains strong general reasoning with modest benchmark regressions: –4.0% on LiveCodeBench (code), –15.4% on AIME (math), and –19.5% on GPQA Diamond (STEM) relative to baseline Gemini, with RL training causing no significant additional regression over SFT alone.
- The self-improvement process on a fixed task set in ASKA drives average Gemini-scored performance above the human reference trajectory score and lifts initial task success from below 25% of tasks to ab

## Key Claims

1. SIMA 2 is built upon a Gemini Flash-Lite foundation model and trained using supervised finetuning on a mixture of gameplay and Gemini pretraining (non-gameplay) data.
2. SIMA 1 was limited to short and direct instructions, could not respond in language or reason about its actions, and often displayed brittleness in generalizing to new situations or instructions.
3. SIMA 1's language encoding was trained from scratch, constraining instruction-following capabilities to the vocabulary of annotated gameplay on which it was trained.
4. SIMA 1 was incapable of outputting text such as internal reasoning or dialogue, and incapable of receiving multi-modal instruction prompts.
5. Foundation models trained primarily on static internet-scale datasets result in intelligence that is fundamentally disembodied and passive, leading to deficits in embodied performance.
6. Foundation models face a modern instantiation of Moravec's Paradox, where high-level cognitive tasks have proven easier to achieve than low-level sensorimotor skills.
7. SIMA 2 substantially closes the gap with human performance across a diverse portfolio of games.
8. SIMA 2 demonstrates robust generalization to previously unseen environments including photorealistic worlds generated on-the-fly by Genie 3.
9. SIMA 2 is capable of open-ended self-improvement by leveraging Gemini to generate tasks and provide rewards, enabling autonomous skill learning from scratch in new environments.
10. The self-improvement process uses three foundation models (task setter, agent, reward model) together with a general world model to autonomously acquire new skills in new environments.

## Capabilities

- Generalist embodied agent achieves near-human performance across diverse 3D virtual game environments, effectively doubling its predecessor's success rate and closing the gap with human players across navigation, tool use, menu interaction, crafting, and construction
- Embodied agents can simultaneously act, reason internally, and engage in natural language dialogue while operating in 3D virtual worlds — including embodied question-answering where the agent takes physical actions to discover information before reporting back
- Embodied agent generalizes zero-shot to entirely unseen 3D virtual environments including new game mechanics, visual styles, and menus — approaching naive human performance on first exposure
- Open-ended self-improvement: a VLA agent can autonomously acquire new skills in previously unseen environments using a foundation model as both task generator and reward function, without any human demonstrations
- Foundation model (Gemini) used as universal reward function for embodied 3D tasks — scores video trajectories against natural language goals using a calibrated rubric without any game-state information
- Embodied agent trained purely in virtual game environments can navigate photorealistic real-world-style environments generated by a world model — proof-of-concept for sim-to-real transfer of embodied intelligence
- Vision-language-action model accepts image sketches and diagrams as instruction modalities — users can annotate screenshots or draw objects to specify tasks rather than describing them in text
- Embodied agent follows instructions in French, German, Mandarin Chinese, and even emoji despite being trained only on English gameplay data — zero-shot multilingual transfer from the foundation model backbone
- Hierarchical multi-model composition for embodied agents: a slow, more capable Gemini Pro model orchestrates a fast SIMA action model by issuing natural language instructions every k steps, with a text-based recurrent memory enabling long-horizon context beyond the immediate context window
- Finetuning a large foundation model on embodied keyboard-and-mouse action data using mixed gameplay + pretraining data retains most of the base model's reasoning capabilities, with only minor regression on coding, math, and STEM benchmarks

## Limitations

- Competent embodied interaction is not an emergent property of large-scale language/vision pretraining — frontier models (Gemini Flash-Lite: 3.2%, Pro: 7%) perform near-chance on embodied tasks without specialized action finetuning
- Combat tasks in 3D environments remain significantly below human performance — requiring fine motor control, split-second decisions, and spatial tracking that current discretized keyboard/mouse agents cannot handle reliably
- RL training phase is strictly limited to training environments — reinforcement learning cannot improve performance in held-out environments, creating a hard ceiling on zero-shot generalization gains from RL
- Finetuning on embodied action data causes 15-25% regression on advanced math reasoning (AIME) and 16-19% regression on STEM (GPQA Diamond) — trading off general intelligence for embodied competence even with mixed training
- Agents fail in held-out environments primarily due to suboptimal exploration strategies rather than time constraints — a qualitatively different failure mode from humans that suggests agents lack efficient exploration heuristics in novel environments
- Self-improvement has only been validated in a single held-out environment (ASKA) — generality of the open-ended self-improvement loop across diverse environments with different mechanics and visual styles is unproven
- Physical-world deployment of embodied agents trained in virtual environments is entirely undemonstrated — the paper only shows navigation in photorealistic virtual environments generated by a world model, not real robotic control
- The open-ended self-improvement loop requires three separate foundation model calls per episode step (task setter, agent, reward model) plus a world model — making it computationally prohibitive to scale without significant inference cost reduction
- Training requires licensed commercial video game environments — data collection depends on proprietary licensing agreements with game developers, limiting community reproducibility and independent scaling research
- Human gameplay demonstrations remain the primary and irreplaceable training signal for low-level motor control in 3D environments — the majority of training data by volume requires expensive human collection
- The agent receives only every 10th frame (effective 3fps from a 30fps stream), severely limiting temporal resolution for fast-moving tasks such as combat and precision motor actions
- Automatic evaluations for commercial games are restricted to outcomes detectable via screen OCR, pixel heuristics, and agent action patterns — a large class of semantically complex tasks cannot be automatically evaluated at scale
- The Gemini-based reward model is calibrated against a small dataset of human preference pairs — reward signal quality and potential hacking vulnerabilities at scale are not assessed

## Bottlenecks

- Sim-to-real transfer for embodied agents trained in virtual 3D environments: no validated method exists for deploying keyboard-and-mouse-based embodied intelligence to physical robotic systems with continuous action spaces and real-world sensor noise
- Scalable embodied training data: human gameplay demonstrations are the irreplaceable primary signal for low-level motor control in 3D environments — this data bottleneck limits scale, reproducibility, and participation beyond well-resourced labs
- Open-ended embodied task evaluation: no scalable method exists for automatically assessing task completion across arbitrary 3D environments; current approaches require manually-engineered detection functions or expensive human raters, blocking reliable evaluation of generalist capabilities

## Breakthroughs

- Near-human embodied task performance achieved across diverse 3D virtual environments using a single generalist agent built on a foundation model — demonstrating that Moravec's Paradox is substantially bridgeable with the right training approach
- Demonstrated open-ended self-improvement of a VLA agent in a previously unseen 3D environment using a foundation model as both task generator and reward function — no human demonstrations required for new skill acquisition
- Foundation model capabilities (reasoning, language, vision) are substantially preserved after embodied action finetuning using mixed pretraining + gameplay data, disproving the prior belief that action finetuning necessarily erodes conversational and reasoning ability

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/vision_language_action_models|vision_language_action_models]]

## Key Concepts

- [[entities/genie-3|Genie 3]]
- [[entities/minedojo|MineDojo]]
- [[entities/moravecs-paradox|Moravec's Paradox]]
- [[entities/reinforcement-learning-from-verifiable-rewards|Reinforcement Learning from Verifiable Rewards]]
- [[entities/spatial-intelligence|Spatial Intelligence]]
