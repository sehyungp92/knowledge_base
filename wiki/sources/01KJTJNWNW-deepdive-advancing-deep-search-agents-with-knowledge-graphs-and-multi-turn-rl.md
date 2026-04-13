---
type: source
title: 'DeepDive: Advancing Deep Search Agents with Knowledge Graphs and Multi-Turn
  RL'
source_id: 01KJTJNWNWQRBPG1F3AXSTPPMJ
source_type: paper
authors:
- Rui Lu
- Zhenyu Hou
- Zihan Wang
- Hanchen Zhang
- Xiao Liu
- Yujiang Li
- Shi Feng
- Jie Tang
- Yuxiao Dong
published_at: '2025-09-12 00:00:00'
theme_ids:
- agent_systems
- knowledge_and_memory
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DeepDive: Advancing Deep Search Agents with Knowledge Graphs and Multi-Turn RL

DeepDive addresses the structural gap between open-source and proprietary deep search agents by introducing two complementary contributions: an automated knowledge-graph-based pipeline for synthesizing hard, ambiguous multi-hop training questions, and an end-to-end multi-turn GRPO reinforcement learning framework with a novel redundancy penalty — together lifting open-source 32B models from near-zero to 15.3% accuracy on BrowseComp, with semi-automated i.i.d. data pushing this further to 22.2%.

**Authors:** Rui Lu, Zhenyu Hou, Zihan Wang, Hanchen Zhang, Xiao Liu, Yujiang Li, Shi Feng, Jie Tang, Yuxiao Dong
**Published:** 2025-09-12
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

The central problem is a structural gap: on BrowseComp, most open-source models score under 10%, while OpenAI DeepResearch reaches 51.5%. The authors attribute this to two compounding failures.

First, **data scarcity at the right difficulty level**. Existing QA benchmarks (HotpotQA, 2WikiMultiHopQA, MuSiQue) feature predictable multi-hop steps over clear entities — questions solvable with a few direct searches. Real deep research requires iterative, ambiguity-resolving search over "blurry entities" (dates generalized to ranges, names replaced with descriptors), and such questions do not appear organically on the internet. Manual annotation is prohibitively expensive and hard to scale.

Second, **absent multi-turn RL integration**. Even strong reasoning models like DeepSeek-R1 make only shallow tool calls and suffer from hallucinations when equipped with browsing — they were trained for reasoning, not for combining long-horizon reasoning with multi-turn web interaction. Standard RL-for-reasoning training does not naturally produce deep search behavior.

### Proposed Approach

**KG-based data synthesis.** Random walks of length k ∈ [5, 9] over public knowledge graphs (KILT, AMiner) extract attribute-rich multi-hop paths. An LLM (Gemini-2.5-Pro) then obfuscates key attributes — generalizing dates to ranges, replacing names with descriptors — creating blurry entities that prevent shortcut retrieval. Node selection is constrained by out-degree range [4, 8] to avoid overly popular or dead-end nodes, and LLM-guided node selection enforces path coherence.

Each synthetic question is validated by attempting to solve it four times with GPT-4o; any question solved in at least one attempt is discarded. This contrasts with prior work that generated QA from model knowledge alone or simple graph traversals — KG grounding provides verifiable factual triples, controllable reasoning depth, and selective attribute obfuscation unavailable in purely model-generated data.

**Multi-turn RL with redundancy penalty.** The agent operates in a ReAct loop (reason → tool call → observe) with three browsing actions (search, click, open), trained with GRPO on trajectories sampled from a live web environment. The reward combines a strict binary correctness signal — a trajectory receives +1 *only* when every step is correctly formatted AND the final answer matches ground truth as verified by an LLM judge — with a redundancy penalty:

> r′(T) = r(T) − λ·S(T)

where S(T) is the mean pairwise Jaccard similarity across all search queries in the trajectory and λ = 0.1. KL penalty is set to β = 0 to promote exploration. A cold-start SFT phase uses reject-sampled traces from Claude-4-Sonnet-Thinking.

**Semi-automated i.i.d. synthesis.** Human annotators use o3 with search to explore domains, select verifiable entities, construct multi-hop questions, and discard samples the model cannot answer correctly — yielding 2,997 English and 275 Chinese QA pairs in-distribution with BrowseComp's difficulty profile.

### Results & Capabilities

**BrowseComp performance.** DeepDive-32B achieves 15.3% on BrowseComp, surpassing WebSailor-32B (10.5%), Search-o1-32B (2.8%), and WebDancer-32B (3.8%). With i.i.d. training data, this rises to 22.2% — a 40% relative improvement over the prior open-source best. OpenAI DeepResearch (51.5%) remains the target, with a persistent 29–36 point gap.

**RL is the primary driver.** The SFT-only DeepDive-32B scores 9.5% on BrowseComp; RL training raises it to 15.3%. Across four benchmarks, multi-turn RL adds +5.8%, +6.7%, +1.6%, and +3.3% over SFT-only. Evaluation accuracy and tool call counts rise in tandem throughout training — evidence of progressively deeper search strategies, not memorization.

**Test-time scaling along two axes:**
- *Tool-call budget scaling*: Performance improves monotonically from 8 to 128 max tool calls; RL-trained models clearly outperform SFT-only at budgets ≥ 16.
- *Parallel sampling*: Selecting the answer with fewest tool calls across 8 parallel samples achieves 24.8% on BrowseComp-266, versus 18.8% for majority voting and 12.0% for single attempts — approaching the pass@8 upper bound of 37.6%. The "fewest tool calls" heuristic works because early stopping correlates with model confidence.

**Ablation findings.** Removing the format reward eliminates learning progress. The redundancy penalty reduces tool call counts by ~14% in later training while improving accuracy by ~20%, demonstrating that pruning redundant search does not sacrifice effectiveness.

---

## Key Claims

1. Open LLMs perform poorly as deep search agents due to limited long-horizon reasoning capacity with browsing tools and the lack of sufficiently difficult supervised data.
2. Most existing QA datasets feature relatively simple questions that do not reflect true hard-to-find cases; HotpotQA questions can often be solved by searching for a few clear entities.
3. Deep search questions such as those in BrowseComp involve multiple blurry entities, requiring long-horizon reasoning and iterative deep search to reach the correct answer.
4. Even strong reasoning models such as DeepSeek-R1 make only shallow tool calls and often suffer from hallucinations in deep search settings — multi-turn deep search is not naturally emergent from standard RL-for-reasoning training.
5. Knowledge graphs are well-suited for generating deep search training data because they provide verifiability via factual entity-relation triples, multi-hop structure controllable via random walks, and selective attribute obfuscation.
6. Questions generated solely from node sequences of KG random walks tend to be too simple (similar to HotpotQA) because answers can be found by direct search; entity obfuscation is necessary to create genuine difficulty.
7. Nodes with excessively high out-degree are overly popular (answers too predictable); nodes with low out-degree hinder effective path expansion — out-degree filtering [4, 8] is essential.
8. DeepDive uses a strict binary reward where a trajectory receives +1 only when every step is correctly formatted and the final answer matches ground truth as verified by an LLM judge.
9. The redundancy penalty discourages repeated similar queries by computing mean pairwise Jaccard similarity across all search queries in a trajectory and subtracting a weighted similarity score.
10. DeepDive-32B achieves 15.3% on BrowseComp, surpassing all listed open-source agents and establishing a new open-source competitive result.
11. Multi-turn RL consistently enhances DeepDive-32B across all four benchmarks (+5.8%, +6.7%, +1.6%, +3.3% over SFT-only baseline).
12. The SFT-only model scores 9.5% on BrowseComp; RL training raises it to 15.3%.
13. RL gains are less pronounced for the 9B model — suggesting a minimum reasoning capacity threshold below which specialized RL training fails to transfer.
14. During RL training, evaluation accuracy on BrowseComp-266 consistently improves alongside rising tool call counts — the model progressively adopts deeper search strategies.
15. When tool call limit reaches 16 or more, RL-trained DeepDive-32B clearly outperforms its SFT-only counterpart, demonstrating RL's advantage in tool-call budget scaling.

---

## Landscape Contributions

### Capabilities

**Multi-turn RL for deep search** *(research_only)*
End-to-end GRPO training with redundancy penalty on KG-synthesized data improves open-source 32B models to 15.3% on BrowseComp — and 22.2% with semi-automated i.i.d. data — outperforming all prior open-source deep search agents. See [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] and [[themes/agent_systems|Agent Systems]].

**KG-grounded hard training data synthesis** *(research_only)*
Automated synthesis of ambiguous multi-hop QA pairs via knowledge graph random walks and LLM-based entity attribute obfuscation, producing training data that forces iterative deep search behavior without manual annotation. Connects to [[themes/knowledge_and_memory|Knowledge and Memory]] and [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]].

**Tool-call budget scaling** *(research_only)*
Deep search performance improves steadily and log-linearly as maximum tool calls grow from 8 to 128; RL-trained models outperform SFT-only at all budgets ≥ 16 — a concrete test-time scaling axis for [[themes/agent_systems|agentic systems]].

**Fewest-tool-calls selection heuristic** *(research_only)*
Selecting the answer requiring fewest tool calls from 8 parallel samples achieves 24.8% on BrowseComp-266 versus 18.8% majority voting — exploiting an inverse correlation between search depth and answer confidence as a cheap inference-time signal.

**Redundancy penalty via Jaccard similarity** *(research_only)*
A within-trajectory query similarity penalty reduces tool call counts by ~14% in later RL training while improving accuracy by ~20%, enabling more efficient deep search without sacrificing coverage. Relevant to [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]].

---

### Limitations

**Persistent open-source/proprietary gap** *(significant, improving)*
DeepDive-32B reaches 15.3% on BrowseComp; OpenAI DeepResearch reaches 51.5% — a 36-point gap that persists even after RL training on i.i.d. data (22.2%). The proprietary system's training data, scale, and methodology remain undisclosed.

**Synthetic data difficulty ceiling** *(significant, unclear)*
The upper difficulty limit of KG-synthesized questions remains significantly lower than expert-curated BrowseComp questions. The automated pipeline cannot reproduce the level of complexity that requires hours of expert research — creating a systematic training-evaluation distribution mismatch.

**Over-search pathology from hard-data RL** *(significant, unclear)*
Training on hard data induces an "over-search" phenomenon: agents make excessive tool calls even when the correct answer could be reached with fewer steps. This reflects misalignment between training incentives (maximize correctness on hard questions) and deployment efficiency. Optimal training steps and reward mechanisms remain unresolved.

**Minimum reasoning capacity threshold for RL** *(significant, unclear)*
The 9B model gains minimal benefit from multi-turn RL training — suggesting that below a certain base reasoning capacity, specialized RL training for deep search fails to transfer. The threshold is not characterized.

**SEAL-0 benchmark resistance** *(significant, stable)*
Performance on SEAL-0 does not improve with i.i.d. training — the benchmark requires discriminating among competing plausible search results, a skill orthogonal to the generative search strategy that KG and i.i.d. synthesis train.

**Sparse binary reward signal** *(significant, stable)*
The strict format-and-correctness requirement creates extremely sparse gradients for long multi-turn trajectories. A single formatting error anywhere in the trajectory zeroes the reward regardless of search quality, making learning brittle for edge cases.

**Context length cap during RL training** *(significant, improving)*
The 51,200-token context limit during RL training bounds how many browsing steps can be learned in a single trajectory, while SFT training used longer contexts. This caps the complexity of multi-turn strategies that can be reinforced.

**GPT-4o filtering bias** *(minor, unclear)*
The difficulty filter retains only questions GPT-4o fails in all four attempts, implicitly shaping the training distribution around GPT-4o's blind spots. Questions that require capabilities absent in GPT-4o but present in other systems may be systematically excluded.

**No security evaluation** *(significant, unclear)*
Agents browse arbitrary real web pages including open URLs with no evaluation of robustness against prompt injection, misleading content, or adversarial manipulation — a meaningful gap for any deployment scenario. Connects to [[themes/agent_systems|agent safety]] considerations.

**Missing inference cost reporting** *(significant, unclear)*
Scaling to 128 tool calls per query is analyzed for accuracy only; no discussion of API cost, latency, or practical deployment feasibility accompanies the scaling curves.

---

### Bottlenecks

**Automated data synthesis below expert-benchmark difficulty** *(1–2 years)*
KG-based methods produce systematically easier questions than BrowseComp, blocking purely automated scalable pipelines for training frontier-quality deep search agents without expensive human annotation. See [[themes/reinforcement_learning|Reinforcement Learning]] and [[themes/retrieval_augmented_generation|RAG]].

**Unstable RL training dynamics for multi-turn deep search** *(1–2 years)*
Over-search pathology emerges as a failure mode; optimal training steps, reward mechanisms, and difficulty curricula remain unclear — blocking stable, efficient RL training that generalizes to deployment without pathological behaviors.

**Structural gap between open-source and proprietary deep research agents** *(1–2 years)*
The 36-point accuracy gap on BrowseComp reflects training data quality/scale advantages and likely undisclosed proprietary techniques — blocking open-source deep research agents from replacing proprietary systems for complex information retrieval tasks.

---

### Breakthroughs

**Multi-turn GRPO with KG synthesis** *(notable)*
The combination of knowledge-graph-synthesized hard training data and Jaccard-similarity redundancy penalty in multi-turn GRPO lifts open-source 32B models to 15.3% on BrowseComp (22.2% with i.i.d. data). The techniques were adopted in the open GLM-4.5 and GLM-4.6 models, contributing to their strong deep search performance.

**Inverse correlation between tool calls and answer correctness** *(notable)*
The discovery that fewest-tool-calls selection outperforms majority voting in parallel sampling reveals a previously uncharacterized signal: early stopping correlates with model confidence and answer quality, while additional calls tend to reflect uncertainty. This finding has implications for inference-time compute allocation across [[themes/agent_systems|agentic systems]] broadly.

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/knowledge_and_memory|Knowledge and Memory]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

---

## Open Questions

- What is the minimum base reasoning capacity required for multi-turn RL to transfer effectively in deep search settings — and can it be characterized as a scaling threshold?
- Can the over-search pathology be resolved through curriculum design (easy → hard data ordering) or does it require fundamentally different reward shaping?
- Does the "fewest tool calls" heuristic generalize beyond BrowseComp-style questions, or is it specific to benchmarks where answer confidence covaries with search depth?
- How much of the 36-point proprietary/open-source gap is attributable to training data versus model scale versus undisclosed architectural choices?
- Can KG-based synthesis be extended to match expert-curated benchmark difficulty — or does BrowseComp-level complexity require human annotator judgment that is structurally irreplaceable?

## Key Concepts

- [[entities/cold-start-phase|Cold-Start Phase]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/react|ReAct]]
