---
type: source
title: 'The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic
  Tree Search'
source_id: 01KJV0GSYV7W8GBHGVKRDNSWNC
source_type: paper
authors:
- Yutaro Yamada
- Robert Tjarko Lange
- Cong Lu
- Shengran Hu
- Chris Lu
- Jakob Foerster
- Jeff Clune
- David Ha
published_at: '2025-04-10 00:00:00'
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- reasoning_and_planning
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

**Authors:** Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, David Ha
**Published:** 2025-04-10 00:00:00
**Type:** paper

## Analysis

# The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search
2025-04-10 · paper · Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu et al. (8 total)
https://arxiv.org/pdf/2504.08066

---

### Motivation & Prior Limitations
What limitations, bottlenecks, or open problems does this paper address? What was the state of the art before this work, and why was it insufficient?

- The AI Scientist-v1 required human-authored code templates for each new topic area, severely constraining autonomy and out-of-the-box deployability across diverse machine learning domains.
  - Every new research area demanded manual effort to draft a baseline experiment outline in code, making the system effectively semi-automated rather than fully autonomous.
- The AI Scientist-v1 used a strictly linear hypothesis-testing routine, limiting exploration depth and preventing systematic investigation of complex research questions.
  - Linear execution meant each code refinement directly built on the immediately preceding experiment, producing short-sighted experimentation that could not backtrack, branch, or explore alternative directions in parallel.
- Prior fully automated scientific discovery systems had never produced a manuscript that successfully passed formal peer review, leaving the practical ceiling of such systems undemonstrated.
  - The AI Scientist-v1 did not submit any generated manuscripts to peer review, so no external validation of end-to-end scientific quality existed.
- The AI Scientist-v1 lacked Vision-Language Model (VLM) integration, meaning figure quality, caption accuracy, and visual clarity in generated manuscripts went unchecked during experimentation and writing.

---

### Proposed Approach
What does the paper propose, and how does it differ from prior work addressing the same problem? Describe the core technical contribution — the mechanism, architecture, algorithm, or method — not just the claim that it works.

- The AI Scientist-v2 replaces human-authored templates with a generalized idea generation phase that operates at a higher level of abstraction, prompting the system to formulate research directions akin to drafting a grant proposal before committing to implementation, with Semantic Scholar queried in the loop to assess novelty against existing literature.
  - Unlike v1's code-conditioned idea generation, v2 begins from open-ended research concepts and assesses feasibility before any code is written.
- The core technical contribution is a parallelized agentic tree search for experiment execution, managed by a dedicated Experiment Progress Manager agent that coordinates four explicitly staged phases: (1) Preliminary Investigation, (2) Hyperparameter Tuning, (3) Research Agenda Execution, and (4) Ablation Studies.
  - Each node in the tree encapsulates an experiment script, textual plan, error traces, runtime metrics, performance metrics, LLM feedback, visualization scripts, figure paths, VLM figure feedback, and a buggy/non-buggy status — a richer state representation than the scalar evaluation scores used in related work like AIDE (Jiang et al., 2025).
  - Node selection uses a best-first strategy guided by an LLM evaluator; buggy nodes are prioritized for debugging with a predefined probability, while non-buggy nodes are selected for refinement. New child nodes across all selected parents are executed concurrently in parallel, accelerating exploration significantly.
  - Specialized node variants handle distinct needs: hyperparameter nodes systematically probe configurations while tracking previously tested ones to avoid redundancy; ablation nodes evaluate component importance; replication nodes run different random seeds to compute mean/standard deviation statistics; aggregation nodes consolidate replication outputs into combined visualizations without running new experiments.
- VLMs are integrated at two stages: during tree-based experimentation to critique generated figures immediately (flagging unclear labels, missing legends, or misleading visualizations and marking nodes as buggy), and during manuscript reflection to verify figure-caption alignment and detect duplication between main text and appendix.
  - This contrasts with v1, which had no VLM integration and used an Aider-based incremental writing loop; v2 replaces that with a single-pass manuscript generation followed by a separate reflection stage powered by a reasoning model (OpenAI o1).
- Dataset acquisition is standardized by prompting the system to use Hugging Face Hub's `datasets.load_dataset` whenever possible, reducing ad-hoc dataset handling across diverse ML domains.

---

### Results & Capabilities
What does the approach achieve? Include specific numbers, benchmarks, comparisons, and qualitative capabilities. Distinguish between the paper's central claims and secondary findings.

- The AI Scientist-v2 produced the first fully AI-generated manuscript to successfully pass formal peer review: one of three submissions to the ICLR 2025 "I Can't Believe It's Not Better" (ICBINB) workshop received an average reviewer score of 6.33 out of 10 (individual scores: 6, 7, 6), placing it in roughly the top 45% of the 43 total workshop submissions and exceeding the acceptance threshold.
  - The accepted paper investigated compositional regularization for neural network generalization, reported a negative result (the regularization did not improve and sometimes harmed performance), and was praised by reviewers for clearly articulating why the approach failed — a finding the workshop's negative-results theme rewarded.
- The system operates without any human-authored code templates, generalizing across diverse ML domains from a single codebase, in contrast to v1 which required per-topic manual baseline code.
- The accepted manuscript was produced with minimal human intervention: humans provided the high-level workshop theme, selected which three of ~40 AI-generated ideas to run, execut

## Key Claims

1. The AI Scientist-v2 produced the first entirely AI-generated manuscript to successfully pass a peer-review process at a recognized machine learning workshop.
2. The AI Scientist-v1 used a strictly linear and shallow experimentation approach, preventing deeper exploration of scientific hypotheses.
3. AI Scientist-v2 eliminates the dependency on human-provided code templates, increasing the system's autonomy and enabling deployment across multiple machine learning domains.
4. The AI Scientist-v2 uses a novel progressive agentic tree-search algorithm managed by a dedicated experiment manager agent, enabling deeper and more systematic exploration of complex hypotheses.
5. One of the three AI-generated manuscripts submitted to the ICLR 2025 ICBINB workshop received an average reviewer score of 6.33, placing it in roughly the top 45% of submissions.
6. The accepted AI-generated paper investigated whether compositional regularization in neural network training can improve compositional generalization, finding that it does not yield significant improv
7. The Experiment Progress Manager coordinates four clearly defined stages: Preliminary Investigation, Hyperparameter Tuning, Research Agenda Execution, and Ablation Studies.
8. The agentic tree search uses a best-first search strategy guided by an LLM that evaluates candidate nodes based on performance metrics, training dynamics, and quality of generated plots.
9. In the tree search, buggy nodes (those with execution errors or failed VLM review) are selected with a predefined probability to prioritize error resolution and debugging over non-buggy refinement.
10. New child nodes in the tree search are all executed concurrently in parallel, significantly accelerating the exploration process.

## Capabilities

- End-to-end autonomous scientific paper generation without human-authored code templates — the system formulates hypotheses, generates experimental code from scratch via tree search, executes experiments, visualizes results, and authors complete manuscripts across diverse ML domains
- AI-generated scientific manuscripts can pass peer review at a recognised ML workshop — one of three fully autonomous submissions exceeded the acceptance threshold at an ICLR 2025 workshop with scores of 6, 6, 7 (avg 6.33)
- Parallelised agentic tree search for iterative scientific experimentation — multiple experimental nodes execute concurrently across four structured stages (feasibility → hyperparameter tuning → research agenda → ablations), enabling systematic recovery from failures and hypothesis-space exploration
- VLM-integrated iterative feedback loop for scientific figure quality — VLMs evaluate label clarity, caption alignment, legend completeness, and figure duplication during both live experiment execution and manuscript writing phases

## Limitations

- AI-generated science is inconsistently publishable even at low-bar venues — only 1 of 3 submissions was accepted at a workshop with a 60–80% typical acceptance rate, implying the system fails to reach that threshold the majority of the time
- Autonomous systems cannot reliably generate genuinely novel, high-impact scientific hypotheses or design truly innovative experimental methodologies — they produce incremental, interpolative ideas within the training distribution
- Autonomous research pipelines introduce citation hallucinations and literature omissions — the system both fabricates references and drops foundational citations (e.g., Hochreiter & Schmidhuber 1997 omitted), undermining scientific credibility
- Full autonomy claim requires non-trivial human meta-selection — humans select which AI-generated ideas to run, execute multiple seeds per idea, and hand-pick the best complete manuscript for submission, representing significant curation burden hidden from the autonomy framing
- Autonomous experimental code generation does not enforce statistical validity — the accepted paper had ~57% training/test dataset overlap undetected by the automated review loop, which could entirely invalidate its results
- VLM figure review catches visual quality issues but fails at semantic verification — the pipeline approved figures with captions that misinterpreted experimental outcomes, including a figure where the baseline outperformed the proposed method contradicting the written claims
- Autonomous scientific experimentation is implicitly constrained to ML domains with Hugging Face-compatible datasets — the system cannot reliably design experiments in domains requiring custom data pipelines, proprietary datasets, or specialised hardware
- Tree-search-based autonomous experimentation has high computational cost and scalability challenges — each branch requires full code generation, execution, and evaluation; the branching factor makes deep scientific exploration expensive
- Autonomous research systems test narrow experimental conditions without recognising need for architectural breadth — the accepted paper was criticised for testing only LSTMs without considering transformers, a comparison reviewers flagged as obvious and necessary
- Autonomous systems produce papers insufficiently rigorous for top-tier main-conference acceptance — lack of deep methodological justification, limited ablation scope, and insufficient theoretical grounding place outputs firmly below ICLR/NeurIPS/ICML main-track standards

## Bottlenecks

- Autonomous AI systems cannot reliably generate genuinely novel scientific hypotheses — they interpolate within the training distribution, producing incremental ideas and exploratory negative results rather than the paradigm-shifting contributions required for high-impact publication
- Automated scientific workflows lack principled experimental validity checking — dataset contamination, methodological confounds, incorrect statistical interpretations, and figure-claim mismatches pass through current automated review loops undetected

## Breakthroughs

- First fully AI-generated paper to successfully pass blind peer review at a recognised ML workshop — an end-to-end autonomous pipeline with no human editing of experimental content produced a manuscript accepted by independent expert review at an ICLR 2025 workshop
- Template-free autonomous scientific experimentation via agentic tree search — AI Scientist-v2 eliminates dependence on human-authored code templates, enabling domain-general autonomous scientific code generation managed by a structured multi-stage experiment manager agent

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/aider|Aider]]
- [[entities/reflexion|Reflexion]]
