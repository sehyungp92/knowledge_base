---
type: source
title: 'SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning'
source_id: 01KJT1G6YCBG5BYZZQAB57E7D7
source_type: paper
authors:
- Peng Xia
- Jianwen Chen
- Hanyang Wang
- Jiaqi Liu
- Kaide Zeng
- Yu Wang
- Siwei Han
- Yiyang Zhou
- Xujiang Zhao
- Haifeng Chen
- Zeyu Zheng
- Cihang Xie
- Huaxiu Yao
published_at: '2026-02-09 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning

**Authors:** Peng Xia, Jianwen Chen, Hanyang Wang, Jiaqi Liu, Kaide Zeng, Yu Wang, Siwei Han, Yiyang Zhou, Xujiang Zhao, Haifeng Chen, Zeyu Zheng, Cihang Xie, Huaxiu Yao
**Published:** 2026-02-09 00:00:00
**Type:** paper

## Analysis

# SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
2026-02-09 · paper · Peng Xia, Jianwen Chen, Hanyang Wang, Jiaqi Liu, Kaide Zeng et al. (13 total)
https://arxiv.org/pdf/2602.08234

---

### Motivation & Prior Limitations
LLM agents operate episodically and fail to accumulate reusable knowledge across tasks, treating each interaction in isolation despite having access to rich interaction histories.
- Existing memory-based methods store raw trajectories in external databases, but these trajectories are verbose, redundant, and noise-heavy, making it difficult for agents to extract critical behavioral patterns.
  - Raw trajectory memory approaches (Reflexion, ExpeL, Mem0) struggle with the information density vs. noise trade-off, and empirically show performance degradation as shown by their low ALFWorld success rates (28.8–46.3%) compared to RL baselines.
  - More recent compressed-memory and online-training approaches (MemRL, EvolveR, MemP) improve efficiency but still mimic past solutions rather than distilling core transferable principles, and fail to adapt the agent's internal policy — MemRL achieves only 21.4% on ALFWorld despite using RL to update its memory bank.
- The key missing insight is abstraction: effective experience transfer requires extracting compact, reusable behavioral strategies rather than compressing or replaying trajectories, and requires a co-evolving knowledge store rather than a static one.

---

### Proposed Approach
SKILLRL is a three-component framework that transforms raw interaction trajectories into a hierarchical skill library (SKILLBANK) and co-evolves that library with the agent's RL-trained policy through recursive failure analysis.

- **Experience-based skill distillation** uses a teacher model (OpenAI o3) to apply differential processing to collected trajectories: successful episodes are abstracted into generalizable strategic patterns, while failed trajectories are synthesized into concise counterfactual failure lessons rather than discarded or stored verbatim.
  - This distillation achieves 10–20× token compression compared to raw trajectories, encoding both what to do and why failures occur.

- **SKILLBANK** organizes distilled knowledge into two levels: general skills (Sg) capturing universal strategic principles applicable across all task types (e.g., systematic exploration, precondition verification), and task-specific skills (Sk) encoding domain-specific action sequences and failure modes per task category.
  - At inference, general skills are always included in context while task-specific skills are retrieved via semantic similarity over task description embeddings with a TopK threshold, giving the policy a skill-augmented context: πθ(at | o≤t, d, Sg, Sret).

- **Recursive skill evolution** treats SKILLBANK as a dynamic component during RL training rather than a static knowledge base, triggering skill library updates after each validation epoch for task categories with success rate below a threshold (δ = 0.4).
  - The teacher model analyzes failed validation trajectories sampled via diversity-aware stratified sampling, identifies gaps not addressed by current skills, proposes new skills, and refines ineffective existing ones — creating a virtuous cycle where policy improvement exposes new failure modes that drive library expansion.
  - A cold-start SFT phase precedes RL training, fine-tuning the base model on teacher-generated skill-augmented reasoning traces so it learns to retrieve, interpret, and apply skills before entering the RL stage; skipping this drops performance by ~20%.

- Policy optimization uses GRPO with importance ratios computed over the full skill-augmented context, with KL regularization anchored to the post-SFT reference policy to preserve learned skill utilization while improving task performance.

---

### Results & Capabilities
SKILLRL achieves state-of-the-art performance across nine benchmarks, outperforming all baselines by 15.3% on average, with a 7B open-source model surpassing much larger closed-source systems.

- On ALFWorld, SKILLRL achieves 89.9% overall success rate, a 12.3% absolute improvement over the GRPO baseline it builds on, and a 35.2% absolute gap over the best memory-augmented RL baseline (Mem0+GRPO at 54.7%).
  - The largest per-task gains are on the most complex subtasks: PickTwo (+23% over GRPO), Cool (+22%), and Heat (+15%), where multi-step planning and state tracking are critical and task-specific skills provide the most leverage.
  - Qwen2.5-7B with SKILLRL outperforms GPT-4o by 41.9% and Gemini-2.5-Pro by 29.6% on ALFWorld, demonstrating that structured skill learning can compensate for model scale.

- On WebShop, SKILLRL achieves 72.7% success rate vs. 66.1% for GRPO and 46.9% for SimpleMem+GRPO, with an average score of 85.2.

- On seven search-augmented QA benchmarks (single-hop: NQ, TriviaQA, PopQA; multi-hop: HotpotQA, 2Wiki, MuSiQue, Bamboogle), SKILLRL achieves a state-of-the-art average of 47.1%, surpassing Search-R1 (38.5%) and EvolveR (43.1%).
  - Performance is especially strong on complex multi-hop tasks: Bamboogle at 73.8% (+19.4% over EvolveR), suggesting hierarchical skills are particularly valuable for multi-step information synthesis.
  - Despite training only on NQ and HotpotQA, SKILLRL maintains competitive out-of-domain performance on TriviaQA, PopQA, and 2Wiki, indicating distilled search strategies generalize across task types.

- The skill library grows from 55 skills (12 general, 43 task-specific) to 100 skills by the end of training, with growth predominantly in task-specific skills (43→80), showing balanced expansion across task categories.

- SKILLRL maintains a context length averaging under 1,300 tokens vs. ~1,450 tokens for raw memory retrieval, a 10.3% reduction despite achieving substantially higher performance — demonstrating that abstraction resolves rather than exacerbates the context-bloat problem.

- Convergence is significant

## Key Claims

1. Existing memory-based methods store raw trajectories that are often lengthy, redundant, and noise-heavy, preventing extraction of high-level reusable behavioral patterns.
2. Memory-based methods that compress trajectories and update memory banks via online training merely mimic past solutions and fail to distill core principles or adapt the agent's internal policy.
3. SKILLRL achieves state-of-the-art performance on ALFWorld, WebShop, and seven search-augmented benchmarks, outperforming strong baselines by over 15.3%.
4. SKILLRL achieves an 89.9% success rate on ALFWorld and 72.7% on WebShop.
5. SKILLRL with Qwen2.5-7B-Instruct outperforms GPT-4o by 41.9% and Gemini-2.5-Pro by 29.6% on ALFWorld, demonstrating that effective skill learning can compensate for model scale.
6. SKILLRL achieves a 12.3% absolute improvement over vanilla GRPO on ALFWorld (77.6% to 89.9%), directly attributable to the skill-augmentation mechanism.
7. MemRL, which uses RL solely to update its memory bank while keeping the policy frozen, fails to adapt to complex environments, yielding only 21.4% on ALFWorld.
8. SKILLRL achieves a state-of-the-art average score of 47.1% on search-augmented QA tasks, outperforming Search-R1 (38.5%) and EvolveR (43.1%).
9. On Bamboogle, SKILLRL surpasses EvolveR by 19.4%, demonstrating that hierarchical skills effectively guide multi-step information synthesis.
10. Despite being trained on limited datasets (NQ, HotpotQA), SKILLRL maintains competitive performance on out-of-distribution tasks like TriviaQA and 2Wiki, confirming that distilled search strategies ar

## Capabilities

- LLM agents can automatically distill diverse interaction trajectories into compact, hierarchical skill libraries, achieving 10–20× token compression versus raw trajectories while improving rather than degrading reasoning utility
- Recursive skill evolution enables an agent's knowledge library to co-evolve with its RL-trained policy, continuously discovering and addressing emergent failure modes across training without catastrophic forgetting of prior skills
- A 7B open-source model fine-tuned with skill-augmented RL achieves 89.9% on ALFWorld, outperforming GPT-4o by 41.9% and Gemini-2.5-Pro by 29.6%, demonstrating that structured experiential knowledge can compensate for model scale on complex agent tasks
- Agents trained on skill-abstracted knowledge generalise across out-of-domain search QA datasets: SKILLRL trained only on NQ and HotpotQA maintains competitive performance on TriviaQA, 2Wiki, Bamboogle and other OOD tasks, confirming that distilled search strategies are task-agnostic
- Failure trajectory synthesis into counterfactual lessons — concise structured analyses identifying the failure point, flawed reasoning, correct alternative, and general principle — enables agents to learn from failures without exposing the full noisy trajectory in context

## Limitations

- Current LLM agents treat every task execution as episodic and stateless — each run starts from scratch with no accumulated knowledge from past successes or failures, fundamentally blocking experience-driven improvement
- Raw trajectory memory approaches suffer performance degradation at scale — verbose trajectories with redundancy and noise lead to sub-optimal performance or outright regression compared to no-memory baselines, as evidenced by MemRL achieving only 21.4% on ALFWorld
- Skill-augmented RL requires a state-of-the-art proprietary teacher model (OpenAI o3) for both skill distillation and SFT data generation — the entire pipeline quality is gated on access to a frontier closed-source model as an external dependency
- Cold-start supervised fine-tuning is a hard prerequisite — without an SFT phase demonstrating skill retrieval and utilisation, the base model cannot leverage the skill library during RL, causing approximately 20 percentage-point performance drop
- All evaluations are in text-based simulated environments (ALFWorld text-game, WebShop simulator, search QA) — no evidence of transfer to real GUI environments, physical systems, or production deployments with perceptual noise and unstructured feedback
- Skill evolution is only triggered for task categories below a success threshold — categories that already pass the threshold accumulate subtle failure modes that are never analysed, creating a systematic blind spot in continuous improvement
- RL training uses only binary (0/1) task success rewards — no dense reward signal exists for partial progress, making learning critically dependent on the skill library generating enough successful trajectories to provide any gradient at all
- Context length remains a hard ceiling on agent policy even after skill abstraction — the optimisation problem is explicitly formulated with a binding context constraint |c| ≤ Lmax, and as skill libraries grow the constraint is re-approached
- Memory-augmented RL that decouples policy training from memory bank updates fails severely — updating only the memory while keeping the policy frozen yields 21.4% vs 89.9% for joint co-evolution, showing policy adaptation and memory are not independently optimisable

## Bottlenecks

- The absence of principled abstraction mechanisms means agents cannot extract high-level reusable strategies from raw experience — trajectory-based memory is too noisy and verbose to enable skill transfer, blocking generalisation across tasks and long-horizon learning
- Sparse binary rewards and long action horizons in agentic RL create a circular dependency — the skill library must bootstrap enough early successes to provide training signal, while the policy must be capable enough to exploit skills, making joint initialisation a critical and fragile requirement

## Breakthroughs

- SKILLRL demonstrates that hierarchical skill abstraction combined with recursive co-evolution during RL enables a 7B open-source model to substantially outperform GPT-4o (+41.9%) and Gemini-2.5-Pro (+29.6%) on ALFWorld, overturning the assumption that large model scale is the primary driver of agent

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/bamboogle|Bamboogle]]
- [[entities/cold-start-sft|Cold-Start SFT]]
- [[entities/expel|ExpeL]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/mem0|Mem0]]
- [[entities/musique|MuSiQue]]
- [[entities/qwen25-7b-instruct|Qwen2.5-7B-Instruct]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/webshop|WebShop]]
