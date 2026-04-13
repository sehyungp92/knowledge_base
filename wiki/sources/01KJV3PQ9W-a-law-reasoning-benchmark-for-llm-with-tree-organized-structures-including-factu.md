---
type: source
title: A Law Reasoning Benchmark for LLM with Tree-Organized Structures including
  Factum Probandum, Evidence and Experiences
source_id: 01KJV3PQ9W8J5XF8VBCBBYZEF3
source_type: paper
authors:
- Jiaxin Shen
- Jinan Xu
- Huiqi Hu
- Luyi Lin
- Fei Zheng
- Guoyang Ma
- Fandong Meng
- Jie Zhou
- Wenjuan Han
published_at: '2025-03-02 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- reasoning_and_planning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 15
tags: []
---
# A Law Reasoning Benchmark for LLM with Tree-Organized Structures including Factum Probandum, Evidence and Experiences

**Authors:** Jiaxin Shen, Jinan Xu, Huiqi Hu, Luyi Lin, Fei Zheng, Guoyang Ma, Fandong Meng, Jie Zhou, Wenjuan Han
**Published:** 2025-03-02 00:00:00
**Type:** paper

## Analysis

# A Law Reasoning Benchmark for LLM with Tree-Organized Structures including Factum Probandum, Evidence and Experiences
2025-03-02 · paper · Jiaxin Shen, Jinan Xu, Huiqi Hu, Luyi Lin, Fei Zheng et al. (9 total)
https://arxiv.org/pdf/2503.00841

---

### Motivation & Prior Limitations
- Existing AI legal systems focus on post-fact legal procedures (judgment generation, document summarization, case retrieval) but leave the foundational fact-finding phase — determining ultimate criminal facts from evidentiary materials — largely unexplored.
  - Prior work on AI-assisted adjudication assumes criminal facts are already established and generates judgments from them, bypassing the evidence analysis and interim reasoning steps that determine whether those facts are correctly established in the first place.
  - The root cause of wrongful judgments is often the misuse of implicit human experience during evidence interpretation, and no existing system makes this reasoning process transparent or auditable.
- No benchmark or dataset existed for evaluating law reasoning as a structured, evidence-backed inference task, leaving the gap between evidence interpretation and judicial decision-making unmeasured and unaddressed.
  - Wigmore's (1937) diagram method and Anderson et al.'s (2005) enhancement remained at a theoretical level due to complexity, and no computational implementation or evaluation framework had been built on them.

---

### Proposed Approach
- The paper introduces Transparent Law Reasoning with Tree-Organized Structures (TL), a task that takes a textual case description as input and outputs a hierarchical tree structure — spanning evidence nodes, multi-level factum probandum, and implicit human experiences — that justifies the final judicial decision.
  - The schema formalizes the reasoning chain as a nested tree where leaf nodes are evidences (documentary, testimonial), intermediate nodes are interim probanda, and the root is the ultimate probandum; edges represent inferences of the form r: v → f under experience e, making every inferential step explicit and auditable.
  - The task is decomposed into three sub-tasks: (I) Factum Probandum Generation (extracting interim probanda and generating the ultimate probandum), (II) Evidence Reasoning (extracting evidence spans and linking them to interim probanda), and (III) Experience Generation (surfacing the implicit experiential warrant connecting evidence to fact).
- The accompanying Knowledge-enhanced Transparent Law Reasoning Agent (TL Agent) implements a ReAct-like strategy over a suite of specialized tools: a Fact Finding Head (fact/evidence extraction, linking), Knowledge Search (vector-database retrieval via ChromaDB with bge-large-zh-v1.5 embeddings), a MultiRole Checker (LLM role-play as lawyer/judge/police officer for adversarial quality voting), a Reflection tool (consistency enforcement after each knowledge-tool invocation), an Emotion Check (neutrality validation on generated facts), and a Finish tool.
  - The base model is GPT-4o-mini; the reflection tool is invoked after every 1–2 knowledge-tool calls to integrate retrieved knowledge and maintain output format consistency, a design choice that separates this agent from vanilla ReAct.
- A crowd-sourced dataset of 453 real Chinese criminal cases (from China Judgement Online) was constructed using a two-phase Wizard-of-Oz methodology: LLM-based automatic annotation followed by human refinement via Label Studio, yielding 2,627 factum probanda, 14,578 evidence pieces, 16,414 experiences, and over 40,000 instruction-tuning samples.

---

### Results & Capabilities
- TL Agent achieves the highest comprehensive score (Sc = 31.50) among all evaluated systems, outperforming GPT-4o (25.74), Deepseek-V3 (30.35), Qwen-max (30.94), and domain-fine-tuned 6B models, while using GPT-4o-mini as its base model.
  - On Factum Probandum Generation (Task I), TL Agent scores Rouge-L 28.75, surpassing GPT-4o (26.44) and matching or exceeding models with far greater parameter counts.
  - On Evidence Reasoning (Task II), TL Agent achieves recall of 40.73 — substantially higher than all baselines including GPT-4o (19.84) — though precision (10.38) remains low across all models, reflecting the inherent difficulty of evidence-to-fact linkage.
  - On Experience Generation (Task III), TL Agent (Rouge-L 24.81) performs comparably to Deepseek-V3 (25.53), suggesting that large-scale pretraining on commonsense knowledge is the primary driver of performance on this sub-task.
- Fine-tuning smaller models (6B parameters) on the TL instruction dataset yields competitive performance: Qwen-6B fine-tuned achieves Sc = 20.52 and Task I Rouge-L 27.54, approaching GPT-4o-mini (25.16) despite the order-of-magnitude parameter difference.
- All models — including TL Agent — show a systematic tendency to over-associate evidence with interim probanda regardless of inferential validity, resulting in low precision on Task II across the board; this failure mode is identified as a fundamental open challenge of the task.

---

### Implications
- Making implicit judicial experience explicit and traceable in a machine-readable tree structure offers a concrete computational mechanism for bias detection in court reasoning, with direct implications for AI-assisted adjudication systems requiring public accountability ("Intelligent Court" paradigm).
- The decomposition of law reasoning into sub-tasks with distinct skill requirements (extraction vs. generation vs. commonsense inference) has methodological implications for reasoning and planning research: it demonstrates that structured, tool-augmented agents can exceed frontier LLMs on complex multi-step structured output tasks even with smaller base models.
- The failure of all models on evidence-to-fact linkage precision suggests that identifying valid inferential relations in natural language — rather than surface co-occurrence — remains a hard open problem for LLM-based reasoning syste

## Key Claims

1. Law reasoning (evidence reasoning) remains underexplored in AI legal applications despite progress in other legal tasks such as document summarization, argument mining, and case retrieval.
2. Existing AI judges primarily address post-fact legal procedures rather than simulating the comprehensive fact-finding phases of court processes.
3. Wrongful legal judgments often arise due to the misuse of implicit human experience in the reasoning process.
4. The TL Agent, using GPT-4o-mini as its base model, surpasses GPT-4o on factum probandum generation through multi-step reasoning and tool utilization.
5. Fine-tuned 6B parameter models demonstrate capabilities comparable to or exceeding those of larger LLMs on factum probandum generation after task-specific fine-tuning.
6. Legal domain fine-tuning (without task-specific fine-tuning) improves factum probandum generation performance over models with no legal knowledge fine-tuning.
7. All evaluated models exhibit high recall but low precision in evidence-to-interim probandum linkage, redundantly associating evidence with interim probandum regardless of substantive inference relatio
8. Experience generation (Sub-task III) relies heavily on extensive commonsense knowledge embedded in large-scale LLMs, making fine-tuned small models unable to surpass large API-accessible LLMs on this 
9. The TL Agent achieves the highest comprehensive score (31.50) among all evaluated models, outperforming GPT-4o (25.74), Qwen-max (30.94), and DeepSeek-v3 (30.35).
10. The crowd-sourced dataset contains 453 cases, 2,627 factum probandum, 14,578 pieces of evidence, and 16,414 experiences totaling 6,234,443 tokens.

## Capabilities

- LLM-based agent framework generates transparent hierarchical law reasoning structures (evidence → interim probandum → ultimate probandum) from unstructured case text, outperforming GPT-4o despite using GPT-4o-mini as the base model
- Multi-agent role-playing checker enables quality control of legal analysis outputs by having LLMs simulate lawyers, judges, and police officers — analyzing problems from distinct perspectives and voting on output quality
- Fine-tuned 6B parameter models achieve performance comparable to or exceeding large frontier LLMs on specialized legal fact extraction tasks after training on domain-specific instruction datasets
- Tool-augmented ReAct-style agents with domain-specific toolkits (fact extraction, evidence retrieval, reflection, multi-role checking) consistently outperform raw frontier model calls on specialized structured reasoning tasks
- LLM-assisted automatic annotation followed by human refinement can construct large domain-specific structured reasoning datasets — producing 40K+ instruction samples from 453 raw cases with complex hierarchical labels

## Limitations

- All LLMs systematically fail at evidence-to-fact linkage — models associate evidence with interim probandum indiscriminately regardless of whether an actual inferential relationship exists, collapsing precision across the board
- Commonsense and social experience generation cannot be recovered by fine-tuning small models — this capability is scale-dependent and embedded in large pretrained models in ways that task-specific fine-tuning cannot replicate
- Transparent law reasoning pipelines require domain expertise to design schemas and prompts — the approach is not turnkey and the effort is time-intensive, limiting who can deploy or adapt these systems
- English-corpus frontier models (Claude-3.5, GPT-4o-mini, GPT-4o) exhibit dramatic performance collapse on Chinese legal evidence extraction — Claude-3.5 achieves evidence F1 of 3.64 vs TL Agent's 16.53, a 4.5x gap
- No hallucination or factual error analysis is performed — the system targets judicial use where fabricated evidence links or invented experiences would constitute serious failures, yet reliability under error conditions is uncharacterized
- Dataset scope is limited to 453 Chinese criminal cases from a single source — generalizability to civil law, international jurisdictions, common law systems, or adversarial legal contexts is entirely untested
- Mechanistic explanation for why the TL Agent succeeds is absent — the paper acknowledges results without understanding the contributing factors, making principled improvement or failure diagnosis impossible
- Overall model performance on law reasoning remains very low in absolute terms — best comprehensive score is 31.50 (TL Agent) and best ROUGE-L for fact generation is ~28.75, indicating law reasoning is largely unsolved

## Bottlenecks

- Absence of structured benchmarks for the law reasoning / judicial fact-finding process — prior AI legal work addressed post-fact judgment generation, leaving the evidence-to-fact inference step uncharacterized and unmeasurable
- LLMs cannot reliably determine whether an inferential relationship exists between a specific piece of evidence and a claimed fact — all current models over-associate evidence with facts, blocking precision-critical legal applications
- Implicit judicial experience — the unstated contextual knowledge practitioners use to connect evidence to conclusions — cannot be reliably specified, extracted, or validated by AI systems, blocking transparent reasoning in high-stakes adjudication

## Breakthroughs

- First crowdsourced benchmark and formal task definition for transparent law reasoning — requiring AI to generate full hierarchical evidence→interim fact→ultimate fact structures with explicit experiences, rather than just producing a verdict

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
