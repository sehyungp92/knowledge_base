---
type: source
title: 'Voyager: An Open-Ended Embodied Agent with Large Language Models'
source_id: 01KJVC2MPTYVFVV0HAC2N00NNW
source_type: paper
authors:
- Guanzhi Wang
- Yuqi Xie
- Yunfan Jiang
- Ajay Mandlekar
- Chaowei Xiao
- Yuke Zhu
- Linxi Fan
- Anima Anandkumar
published_at: '2023-05-25 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- in_context_and_meta_learning
- post_training_methods
- robotics_and_embodied_ai
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Voyager: An Open-Ended Embodied Agent with Large Language Models

Voyager introduces the first LLM-powered embodied lifelong learning agent in Minecraft, demonstrating that open-ended skill acquisition, compositional knowledge accumulation, and zero-shot generalization to novel tasks are achievable through pure prompting — no gradient updates, no parameter fine-tuning — via three tightly integrated components: an automatic curriculum, a growing code-based skill library, and an iterative self-verification loop.

**Authors:** Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar
**Published:** 2023-05-25
**Type:** paper

---

## Motivation

Prior embodied agents built on reinforcement learning and imitation learning operate on primitive actions, making them structurally ill-suited for systematic exploration, interpretability, and generalization in open-ended environments. They are not lifelong learners — they cannot progressively acquire, update, accumulate, and transfer knowledge over extended time spans.

LLM-based predecessors (ReAct, Reflexion, AutoGPT) fail in open-ended exploration for distinct reasons:
- **ReAct and Reflexion** lack a curriculum to sequence tasks by difficulty, preventing meaningful progress in Minecraft.
- **AutoGPT** can decompose goals into subgoals but lacks a persistent skill library, so it cannot accumulate reusable behaviors across episodes.
- All prior LLM agents treat the model as a one-shot planner rather than a component in a feedback-driven refinement loop — generated code cannot be iteratively improved against execution failures.

Catastrophic forgetting is a structural failure mode in continual learning systems that don't externalize knowledge into persistent, compositional stores.

---

## Approach

Voyager operates via blackbox GPT-4 queries with three integrated components:

### Automatic Curriculum
GPT-4 proposes a stream of progressively harder tasks conditioned on the agent's current inventory, biome, health, completed/failed task history, and a self-generated Q&A context (produced by GPT-3.5). The curriculum's explicit objective is "discover as many diverse things as possible" — a form of in-context novelty search that adapts to exploration progress without hand-engineered task sequences. GPT-3.5 handles cheaper auxiliary NLP subtasks; GPT-4 handles curriculum generation and code synthesis.

### Skill Library
Every successfully verified action program is stored as an executable JavaScript code snippet, indexed by the GPT-3.5 embedding of its natural language description — a vector database of reusable behaviors. Retrieval combines a self-generated task plan with environment feedback to find the top-5 most relevant prior skills, injected as in-context examples.

Complex skills are compositional: they call simpler previously learned skills (e.g., `craftStoneShovel()` calling `makeCraftingTable()`). This compounds capability rapidly and eliminates catastrophic forgetting by externalizing memory as code rather than parameters.

### Iterative Prompting Mechanism
A three-way feedback loop closes the skill acquisition cycle:
1. **Environment feedback** — intermediate progress messages from inside control APIs
2. **Execution errors** — from the JavaScript interpreter
3. **Self-verification** — a separate GPT-4 critic instance checks task success and generates corrective critique

Code generation repeats until self-verification confirms success or a 4-round limit is reached, at which point the curriculum proposes a new task. Self-verification replaces manually coded success checkers, making the mechanism applicable to arbitrary curriculum-proposed tasks.

---

## Results

Within 160 prompting iterations:
- **3.3× more unique items** discovered vs. prior SOTA
- **2.3× longer map traversal distances**
- **Tech tree milestones up to 15.3× faster** (wooden tools: ~6 vs. ~92 iterations; iron: ~21 vs. ~135)
- **Only agent to unlock diamond tool level** (1/3 runs); AutoGPT reaches iron but never diamond; ReAct and Reflexion fail to unlock any tech tree level

**Zero-shot generalization:** In a freshly instantiated world with four novel tasks (Diamond Pickaxe, Golden Sword, Lava Bucket, Compass), Voyager solves all four with 100% success rate in 18–21 iterations. ReAct, Reflexion, and vanilla AutoGPT solve none within 50 iterations. When AutoGPT is given Voyager's pre-built skill library, it achieves partial success — demonstrating the skill library is a plug-and-play transferable asset.

**Ablation contributions:**
- Removing automatic curriculum → 93% drop in discovered items
- Removing skill library → performance plateaus in later stages
- Removing self-verification → 73% drop in discovered items
- GPT-4 vs. GPT-3.5 → 5.7× more unique items, confirming a hard frontier model dependency

---

## Capabilities

| Capability | Maturity |
|---|---|
| LLM-driven adaptive curriculum for curiosity-driven exploration | `research_only` |
| Code-based compositional skill library with lifelong accumulation, no parameter updates | `demo` |
| Iterative prompting with environment feedback + LLM self-verification | `research_only` |
| Zero-shot generalization to novel tasks via skill retrieval and composition | `research_only` |
| GPT-4 as qualitative capability threshold for code-based embodied control (5.7× over GPT-3.5) | `narrow_production` |

See: [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]

---

## Limitations

**Blocking:**
- **Open-source LLM inadequacy.** GPT-3.5 and all open-source LLMs are categorically insufficient for the approach. The entire paradigm is locked to expensive closed-source frontier APIs, blocking reproducibility and democratic access. This is the single most structurally constraining limitation.
  > *"GPT-4 significantly outperforms GPT-3.5 in code generation and obtains 5.7× more unique items, as GPT-4 exhibits a quantum leap in coding abilities."*

**Significant:**
- **GPT-4 API cost.** At 15× the cost of GPT-3.5, lifelong learning agents that require frontier models face a hard accessibility barrier for research and deployment at scale.
- **LLM hallucinations.** The curriculum occasionally proposes unachievable tasks (e.g., "craft a copper sword" — a non-existent item), and code synthesis calls undefined API functions. These errors require robust downstream handling.
- **Self-verification failures.** The LLM critic produces incorrect task-completion signals — e.g., failing to recognize spider string as proof of killing a spider — causing agents to re-attempt already-solved tasks. The failure mode is opaque and non-systematic.
- **No visual/multimodal perception.** Voyager operates entirely on structured text state readouts and cannot observe the 3D environment directly. Spatial construction tasks require a human-in-the-loop visual critic. This was a GPT-4 API limitation at time of writing but is structurally significant.
- **Reliability degrades at maximum complexity.** Diamond-level tech tree (highest planning horizon) was unlocked in only 1 of 3 trials, revealing compounding failure probability at long skill chains.
- **No skill quality management.** The library has no pruning, conflict resolution, or quality degradation mechanism. Incorrect or low-quality skills committed before self-verification catches failures persist indefinitely and may corrupt future retrieval.
- **Simulation-only evaluation.** The entire evaluation is confined to Minecraft with a high-level Mineflayer API that abstracts away all low-level perception and motor control. No validation in real-world or physical robot domains exists.

**Minor:**
- **Hard 4-round cap creates abandonment without failure learning.** When the agent cannot solve a skill within 4 iterations, the attempt is discarded rather than the failure experience being stored and reasoned over.
- **GPT-3.5 substitution in auxiliary tasks.** Cost forces lower-quality context into curriculum generation and retrieval pipelines, introducing a quality-cost tradeoff embedded in the architecture itself.

---

## Bottlenecks Addressed / Surfaced

**Surfaced:**
- **Closed-source frontier model dependency** blocks reproducible and democratized lifelong learning agents. GPT-4 is necessary but cost-prohibitive and API-locked. *Horizon: 1–2 years.* See [[themes/agent_systems|Agent Systems]].
- **Absence of multimodal grounding** limits embodied agents to structured text environments. Without visual perception, autonomous operation in visually complex real-world or 3D spaces is impossible. *Horizon: months (partially resolved by subsequent GPT-4V release).*
- **Sim-to-real transfer gap** blocks deployment of LLM-based lifelong learning paradigms to physical robotics. Game APIs abstract away perception, motor control, and physical dynamics entirely. *Horizon: 3–5 years.* See [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]].

---

## Breakthrough

Voyager represents the first demonstration that LLM-powered lifelong learning with continuous skill acquisition, composition, and transfer is achievable in an open-ended environment with **no gradient-based training and no parameter modification**. This challenges the assumption that continual skill acquisition requires updating model weights, and establishes code as a viable, interpretable, non-parametric memory substrate for [[themes/agent_self_evolution|agent self-evolution]].

The externalization of learned behaviors as executable code — rather than as weight updates or latent representations — is the architectural insight that simultaneously solves catastrophic forgetting, enables compositionality, and preserves interpretability.

---

## Implications

- **For [[themes/in_context_and_meta_learning|in-context learning]]:** Voyager shows that a static frozen LLM can exhibit lifelong learning behavior when paired with external memory (code library) and structured feedback loops. The locus of learning shifts from parameters to the scaffolding around the model.
- **For [[themes/agent_self_evolution|agent self-evolution]]:** The automatic curriculum + skill library loop is a prototype of an agent that designs its own training signal. The system decides what to learn next based on what it already knows — a form of autonomous curriculum design.
- **For [[themes/tool_use_and_agent_protocols|tool use and agent protocols]]:** Code as the action space generalizes naturally to tool use — programs can call APIs, compose operations, and abstract over low-level interfaces in ways that natural language or motor commands cannot.
- **For [[themes/robotics_and_embodied_ai|robotics and embodied AI]]:** The Minecraft setting is a high-level proxy for physical embodiment. The framework's applicability to real robots remains the primary open question, gated by sim-to-real transfer and low-level sensorimotor control.
- **Open question:** Can skill libraries learned in simulation transfer zero-shot to physical domains, or does the abstraction provided by game APIs make the gap unbridgeable without domain adaptation?

---

## Related Themes

- [[themes/agent_self_evolution|Agent Self-Evolution]]
- [[themes/agent_systems|Agent Systems]]
- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Key Concepts

- [[entities/autogpt|AutoGPT]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gpt-35|GPT-3.5]]
- [[entities/gpt-4|GPT-4]]
- [[entities/minedojo|MineDojo]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/self-verification|Self-Verification]]
- [[entities/skill-library|Skill Library]]
- [[entities/voyager|Voyager]]
