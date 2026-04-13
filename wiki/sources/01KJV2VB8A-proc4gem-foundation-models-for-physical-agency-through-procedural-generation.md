---
type: source
title: 'Proc4Gem: Foundation models for physical agency through procedural generation'
source_id: 01KJV2VB8ASRWNCSSZGH80M3TN
source_type: paper
authors:
- Yixin Lin
- Jan Humplik
- Sandy H. Huang
- Leonard Hasenclever
- Francesco Romano
- Stefano Saliceti
- Daniel Zheng
- Jose Enrique Chen
- Catarina Barros
- Adrian Collister
- Matt Young
- Adil Dostmohamed
- Ben Moran
- Ken Caluwaerts
- Marissa Giustina
- Joss Moore
- Kieran Connell
- Francesco Nori
- Nicolas Heess
- Steven Bohez
- Arunkumar Byravan
published_at: '2025-03-11 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- robotics_and_embodied_ai
- robot_learning
- synthetic_data_generation
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Proc4Gem: Foundation models for physical agency through procedural generation

**Authors:** Yixin Lin, Jan Humplik, Sandy H. Huang, Leonard Hasenclever, Francesco Romano, Stefano Saliceti, Daniel Zheng, Jose Enrique Chen, Catarina Barros, Adrian Collister, Matt Young, Adil Dostmohamed, Ben Moran, Ken Caluwaerts, Marissa Giustina, Joss Moore, Kieran Connell, Francesco Nori, Nicolas Heess, Steven Bohez, Arunkumar Byravan
**Published:** 2025-03-11 00:00:00
**Type:** paper

## Analysis

# Proc4Gem: Foundation models for physical agency through procedural generation
2025-03-11 · paper · Yixin Lin, Jan Humplik, Sandy H. Huang, Leonard Hasenclever, Francesco Romano et al. (21 total)
https://arxiv.org/pdf/2503.08593

---

### Motivation & Prior Limitations
- Robot learning has historically been split between two incompatible regimes: tasks with rich contact physics (locomotion, dexterous manipulation) that ignore semantic diversity, and tasks with semantic/linguistic grounding (embodied navigation, pick-and-place) that use simplified or abstracted physics.
  - High-fidelity physics simulators like MuJoCo and PyBullet bridge the sim-to-real gap for specific control tasks but lack photorealism and semantic diversity, making them unsuitable for generating large-scale diverse data.
  - Embodied AI simulators like Habitat, ProcTHOR, and Gibson achieve semantic diversity but sacrifice physical realism, limiting transfer to kinematic or motion-planner-based manipulation primitives rather than contact-rich whole-body control.
- Robot data is orders of magnitude scarcer than Internet-scale text and image data, and scaling real-world data collection is insufficient to match the trillions of tokens used to train frontier language models.
  - Prior work combining realism and diversity (e.g., RoboCasa) required mixing real data with simulation data for effective transfer; purely simulation-trained policies with direct real-world transfer had not been demonstrated for contact-rich, semantically grounded tasks.
- No prior work had shown that a single end-to-end policy could simultaneously handle whole-body contact dynamics and open-vocabulary semantic navigation, precluding modular solutions that chain separate navigation and manipulation policies.

---

### Proposed Approach
- Proc4Gem is a multi-step pipeline that combines procedural scene generation, high-fidelity MuJoCo physics, photorealistic Unity rendering, privileged expert RL training, and behavioral cloning distillation into Gemini to produce a language-conditioned whole-body control policy trained entirely on synthetic data.
  - Scene generation uses a VLM-captioned asset database of thousands of furniture objects and a heuristic hierarchical placement recipe to sample semantically meaningful living-room configurations; Gemini generates five natural language descriptions per asset at increasing verbosity levels to serve as language commands.
  - Physics simulation runs in MuJoCo for accurate contact dynamics while rendering is offloaded to Unity for photorealistic RGB images, combining the strengths of both engines in a single pipeline — a deliberate departure from prior work that used either one or the other.
- A privileged RL expert policy is trained on ground-truth simulation state (no rendering required), then hundreds of thousands of successful rollouts are collected across procedurally generated scenes and used to fine-tune Gemini via behavioral cloning with next-token prediction loss.
  - The expert uses domain randomization across episodes to improve robustness; the student (fine-tuned Gemini) takes only RGB images from two onboard cameras and natural language target descriptions as input, with no access to privileged state.
  - The target task — pushing a white trolley with the robot's body toward a language-specified object in a varied room layout — was deliberately chosen to require fusing low-level physical reasoning (momentum, force application) with high-level semantic understanding, ruling out simple modular solutions.
- Deployment uses a distributed asynchronous hierarchical control system where robot hardware remotely queries the fine-tuned Gemini model at 2 Hz, with action caching to handle network latency and jitter; a separate low-level velocity controller (trained with massively parallel TPU-accelerated MJX) maps 3D planar velocity commands to robot motion.

---

### Results & Capabilities
- In procedurally generated simulation scenes, both the fine-tuned Gemini policy and the SPOC transformer baseline recover much of the privileged expert's 68.9% success rate, with strong generalization to out-of-distribution text descriptions and to Italian-language instructions despite training exclusively on English.
  - The multilingual zero-shot capability is attributed to the broad pretraining of SigLIP (trained on WebLI across 109 languages) and Gemini's intrinsic multilingual competence, not any explicit multilingual training signal.
- In the fixed simulation scene replicating the real-world test environment (constructed via 3D scanning), Gemini achieves 70.0% ± 0.46% success when trained with 3D-scanned assets, compared to the baseline's 62.1% ± 0.49%, while the privileged expert achieves 85.4%.
- On real-world hardware, Gemini significantly outperforms the SPOC baseline on difficult settings: the baseline drops ~40% on average in hard configurations compared to Gemini, and achieves 0% success on the highly out-of-distribution "Giraffe" target (a 1.5-meter toy giraffe described only as "Giraffe") while Gemini achieves 70%.
  - Gemini also demonstrates qualitative generalization to humans as targets, a blue-and-white robot dog (a copy of its own hardware), and physically perturbed conditions with 10 kg of added trolley weight — none of which appeared in training data.
  - Cumulative success rate curves show the baseline succeeds faster in easy episodes but Gemini recovers more robustly over time, indicating more cautious but more reliable behavior in the real world.
- The simulation-only training pipeline achieves direct zero-shot real-world transfer with no real robot data, demonstrating that photorealistic rendering combined with physics domain randomization is sufficient to close the visual and dynamic sim-to-real gap for this class of tasks.

---

### Implications
- Proc4Gem provides a concrete existence proof that the dichotomy between contact-rich control and semantic diversity in simulation is not fundamenta

## Key Claims

1. A foundation model (Gemini) fine-tuned solely on simulation data can control a quadruped robot to push an object to unseen targets in unseen real-world environments.
2. Robotics as a data modality is many orders of magnitude below the scale of frontier language model training data.
3. High-fidelity physics simulators lack photorealism and semantic diversity, preventing them from serving as a large-scale diverse data source.
4. Embodied AI simulators achieve large-scale semantic diversity by trading off physical realism.
5. Effective transfer of policies trained purely in simulation to mobile manipulation tasks in the real world had not been demonstrated prior to this work.
6. Proc4Gem uses a hierarchical procedural generation pipeline to sample realistic indoor living-room scenes from a VLM-captioned asset dataset.
7. Gemini is used to generate five natural language descriptions per asset with increasing levels of detail, which serve as language commands for the agent.
8. The privileged expert policy is trained using model-free off-policy RL on state information, then distilled into a student that uses only RGB images and language.
9. Domain randomization is applied across episodes to robustify the expert policy.
10. Gemini is fine-tuned for robot control using behavioral cloning with next-token prediction loss on trajectory data.

## Capabilities

- Gemini foundation model fine-tuned solely on simulation data directly controls a real-world quadruped robot for language-conditioned whole-body manipulation — pushing a trolley to semantically-specified targets in unseen real-world environments
- Simulation-trained robot policies generalize zero-shot to Italian language instructions despite being trained exclusively on English — with effectively no performance drop
- Gemini-based robot policy achieves 70% success rate on a completely novel object category (toy giraffe) never seen in training, while a strong transformer baseline achieves 0%
- Procedural scene generation combining MuJoCo physics simulation with Unity photorealistic rendering generates large-scale, semantically diverse robot training data that transfers to the real world without any real robot data collection
- Foundation model robot policy shows robustness to large physics distribution shifts — successfully manipulating a trolley loaded with 10 kilograms of added weight despite training only on unloaded configurations

## Limitations

- Robot interaction data is many orders of magnitude below language model training scale, with no scalable path to comparable data volumes via real-world collection alone
- Large multimodal model inference speed limits robot control frequency to 2 Hz, constraining the difficulty of dynamic manipulation tasks that require faster reactive control
- Deploying large multimodal models remotely for robot control introduces meaningful network latency and jitter, requiring caching mechanisms that reduce responsiveness
- Prior sim-to-real transfer for embodied AI has been restricted to non-interactive or kinematic manipulation tasks — contact-rich whole-body control was previously not achievable purely from simulation
- High-fidelity physics simulators lack photorealism and semantic diversity, preventing them from serving as unlimited sources of large-scale diverse robot training data
- Simulation asset placement cannot model stacked objects, creating a visual domain gap where the real-world evaluation environment contains objects the training distribution structurally excludes
- Real-world evaluation is confined to a single mock living room with only three target objects and three difficulty configurations — generalization to truly arbitrary real-world environments remains undemonstrated
- Full context length of frontier multimodal models is not exploited for robotics — only 8-step context is used, and effective long-context utilization for long-horizon navigation and manipulation remains an open problem
- Direct reinforcement learning of large foundation models within simulation is not yet demonstrated — the pipeline relies on behavior cloning from privileged RL experts, which caps performance below what end-to-end RL could achieve
- Expert distillation pipeline requires training a privileged RL expert then collecting hundreds of thousands of simulation episodes before student training begins — a substantial compute investment that scales poorly with task diversity
- Gemini policy is significantly more cautious than the transformer baseline — higher success rate is achieved by slower, more conservative behaviour rather than faster convergence, suggesting incomplete internalization of physical dynamics

## Bottlenecks

- Inference latency of frontier multimodal models limits robot control to low frequencies (2 Hz), blocking deployment of large foundation models for dexterous or dynamic manipulation requiring sub-100ms reaction times
- Multi-stage expert distillation pipeline (privileged RL expert → large-scale episode collection → student BC training) creates a per-task engineering bottleneck that prevents rapid scaling to diverse robot tasks

## Breakthroughs

- First demonstration of pure simulation-to-real-world transfer for contact-rich, whole-body robot manipulation grounded in open-vocabulary semantic understanding — no real robot data used

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/vision_language_action_models|vision_language_action_models]]

## Key Concepts

- [[entities/gemini|Gemini]]
- [[entities/siglip|SigLIP]]
- [[entities/behavioral-cloning|behavioral cloning]]
- [[entities/domain-randomization|domain randomization]]
- [[entities/sim-to-real-gap|sim-to-real gap]]
