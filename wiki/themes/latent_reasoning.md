---
type: theme
title: Latent & Continuous Reasoning
theme_id: latent_reasoning
level: 2
parent_theme: reasoning_and_planning
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 22
sources_since_update: 0
update_count: 1
velocity: 0.0
staleness: 0.0
status: active
tags: []
---
# Latent & Continuous Reasoning

> Latent & Continuous Reasoning is an early-stage research direction that has demonstrated proof-of-concept validity — showing that shifting chain-of-thought from observable text into a continuous latent space yields measurable gains on math benchmarks — but remains architecturally constrained by myopic, chunk-by-chunk generation. The trajectory points toward deeper integration of continuous representations into reasoning pipelines, with the central open question being whether non-myopic, hierarchical latent planning is an engineering problem or a deeper architectural mismatch.

**Parent:** [[themes/reasoning_and_planning|reasoning_and_planning]]

## Current State

The foundational move of this research direction was deceptively simple: instead of generating chain-of-thought reasoning in the observable text space X, let the model reason in a latent space Z. As of early 2025, this transition has been demonstrated to work. Latent thought models consistently outperform raw-text CoT on math benchmarks at inference time — a meaningful result because it implies that the constraint of reasoning in human-readable tokens is itself a bottleneck. Forcing a model to commit to discrete, interpretable steps appears to limit the quality of intermediate computation. "Thinking out loud" in text is a lossy projection of a richer underlying process, and working directly in that richer space yields measurable gains.

However, the architecture has not escaped its first serious wall. The current generation structure is myopic: latent thoughts are produced autoregressively chunk-by-chunk, with no mechanism for hierarchical planning across a long horizon. This matters because the tasks where reasoning matters most — writing a research paper, architecting a codebase, composing a novel — demand multi-level planning: outline before paragraph, algorithm before implementation, argument before evidence. The present approach cannot represent that structure.

No breakthroughs have landed recently and no active anticipations are being tracked, suggesting the field is in a consolidation phase, or that source coverage of this theme remains thin. Momentum is concentrated at the proof-of-concept layer — demonstrating that latent reasoning works — rather than at the scaling or application layer.

## Capabilities

- **Latent-space chain-of-thought** *(maturity: research only)* — Latent thought models can perform chain-of-thought reasoning in a latent space Z rather than the observed text space X, outperforming standard CoT on math benchmarks at inference time.

## Limitations

- **Myopic generation structure** *(severity: significant, trajectory: unclear, type: explicit)* — The current latent generation structure models latent thoughts autoregressively for each local text chunk, with no mechanism for holding abstract goal representations across a long generation horizon. This prevents the kind of hierarchical, multi-level planning required for complex, long-horizon tasks.

## Bottlenecks

- **Discrete token commitment in reasoning** — The requirement to reason in human-readable token sequences forces early commitment to interpretable intermediate steps, potentially constraining the quality of the underlying computation. Latent reasoning is a direct response to this bottleneck, but has not yet resolved it at scale or for general tasks.
- **Non-myopic latent planning** — No current architecture supports holding abstract goal representations across a full generation horizon before committing to local predictions. Whether this is a solvable engineering problem or a deeper architectural mismatch remains an open question with an unresolved trajectory.

## Breakthroughs

*No breakthroughs recorded for this theme as of the current coverage period.*

## Anticipations

*No active anticipations are currently being tracked for this theme. This may reflect a consolidation phase in the research or thin source coverage.*

## Cross-Theme Implications

- **Interpretability** — If latent thought spaces can be characterized — what kinds of representations they contain, how they differ from text-space reasoning traces — it would accelerate both trust in latent reasoning systems and architectural iteration. Interpretability work on these spaces is a near-term prerequisite for moving the field forward.
- **[[themes/reasoning_and_planning|Reasoning & Planning]]** — Latent reasoning reframes what "planning" means computationally. If successful, it suggests that planning quality is not just a function of search depth or prompting strategy, but of the representational space in which intermediate steps are computed.
- **Efficiency & Inference** — Reasoning in latent space rather than generating verbose text chains has potential implications for inference cost, though this connection is not yet well-characterized in the literature.

## Contradictions

- The core claim — that latent reasoning outperforms text-space CoT — sits in tension with the interpretability assumption embedded in most chain-of-thought research, which holds that human-readable intermediate steps are not just a UX convenience but a structural aid to reasoning. If the latent results hold, that assumption needs revision.

## Research Opportunities

- **Non-myopic latent planning** — Architectures that can maintain abstract goal representations across a full generation horizon before committing to local token predictions. If this gap closes, latent reasoning could move from a math-benchmark curiosity to a general-purpose reasoning substrate.
- **Characterizing latent thought spaces** — Interpretability research aimed at understanding what latent thought representations contain and how they relate to semantic structure. This is a prerequisite for both trust and architectural iteration.
- **Scaling latent reasoning** — Current results are proof-of-concept. It is unclear whether the performance advantages of latent-space CoT hold at scale, generalize beyond math benchmarks, or compound with other reasoning improvements.
- **Hybrid representations** — Exploring architectures where some reasoning steps are latent and others are text-grounded, potentially combining the computational richness of latent space with the verifiability of explicit reasoning traces.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 22 sources.
- **2025-12-16** — [[sources/01KJT367PQ-universal-reasoning-model|Universal Reasoning Model]]: URM achieves 16.0% pass@1 on ARC-AGI 2, nearly tripling HRM (5.4%) and more than doubling TRM (4.6%)
- **2025-11-26** — [[sources/01KJT6V2CT-monet-reasoning-in-latent-visual-space-beyond-images-and-language|Monet: Reasoning in Latent Visual Space Beyond Images and Language]]: The Monet-SFT-125K dataset contains 125K image-text interleaved CoT samples from real-world, documen
- **2025-11-25** — [[sources/01KJT7B6T7-latent-collaboration-in-multi-agent-systems|Latent Collaboration in Multi-Agent Systems]]: Only the final agent in LatentMAS decodes text output; all intermediate agents operate and communica
- **2025-11-23** — [[sources/01KJVDXNW6-he-co-invented-the-transformer-now-continuous-thought-machines-llion-jones-luke-|He Co-Invented the Transformer. Now: Continuous Thought Machines [Llion Jones / Luke Darlow]]]: SudokuBench uses handcrafted variant sudoku puzzles with diverse natural-language-described constrai
- **2025-11-12** — [[sources/01KJT8GR21-pan-a-world-model-for-general-interactable-and-long-horizon-world-simulation|PAN: A World Model for General, Interactable, and Long-Horizon World Simulation]]: PAN adopts a staged (divide-and-conquer) training strategy where individual modules are first traine
- **2025-10-29** — [[sources/01KJTBPFB9-scaling-latent-reasoning-via-looped-language-models|Scaling Latent Reasoning via Looped Language Models]]: Ouro 1.4B and 2.6B LoopLM models match the performance of models up to 12B parameters across a wide 
- **2025-10-20** — [[sources/01KJTCZ50C-the-free-transformer|The Free Transformer]]: During inference, the Free Transformer samples Z from a uniform prior over one-hot vectors, with no 
- **2025-10-06** — [[sources/01KJTEH94B-less-is-more-recursive-reasoning-with-tiny-networks|Less is More: Recursive Reasoning with Tiny Networks]]: TRM with self-attention and 7M parameters outperforms HRM with 27M parameters on all tested benchmar
- **2025-08-30** — [[sources/01KJTM1K7F-parathinker-native-parallel-thinking-as-a-new-paradigm-to-scale-llm-test-time-co|ParaThinker: Native Parallel Thinking as a New Paradigm to Scale LLM Test-time Compute]]: ParaThinker achieves 12.3% average accuracy improvement over sequential LLMs for 1.5B models with 8 
- **2025-06-26** — [[sources/01KJTMPYR9-hierarchical-reasoning-model|Hierarchical Reasoning Model]]: HRM executes sequential reasoning tasks in a single forward pass without explicit supervision of the
- **2025-05-19** — [[sources/01KJTTV05K-beyond-semantics-the-unreasonable-effectiveness-of-reasonless-intermediate-token|Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate Tokens]]: The study uses a model-organism paradigm: 0.5B parameter Qwen2.5 models trained from scratch on form
- **2025-05-08** — [[sources/01KJTVJC6B-continuous-thought-machines|Continuous Thought Machines]]: Each neuron in the CTM has a privately parameterized neuron-level model (NLM) with unique weights th
- **2025-04-05** — [[sources/01KJSVB9E8-rl-backlog-openais-many-rls-clarifying-distillation-and-latent-reasoning|RL backlog: OpenAI's many RLs, clarifying distillation, and latent reasoning]]: Deep Research was trained using end-to-end reinforcement learning on hard browsing and reasoning tas
- **2025-03-24** — [[sources/01KKT4SWNY-reasoning-to-learn-from-latent-thoughts|Reasoning to Learn from Latent Thoughts]]: New capability: Latent thought models can perform chain-of-thought reasoning in a latent space Z
- **2025-03-13** — [[sources/01KJSVYBCE-advances-in-generative-ai-latent-space-reasoning-comparing-continuous-chain-of-t|Advances in Generative AI Latent Space Reasoning: Comparing Continuous Chain of Thought and Recurrent Depth Models]]: The recurrent block in the Recurrent Depth Approach can be applied multiple times before generating 
- **2025-02-19** — [[sources/01KJVDMXGT-can-latent-program-networks-solve-abstract-reasoning-clement-bonnet|Can Latent Program Networks Solve Abstract Reasoning? [Clement Bonnet]]]: LPN (Latent Program Network) embeds programs into a continuous latent space, trained to be well-stru
- **2025-02-07** — [[sources/01KJV49W0K-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-approach|Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach]]: The large-scale model with shape (2, 4, 2) and hidden size 5280 has only 8 real layers, but when the
- **2024-12-11** — [[sources/01KJV61P52-large-concept-models-language-modeling-in-a-sentence-representation-space|Large Concept Models: Language Modeling in a Sentence Representation Space]]: The 7B Two-Tower LCM was pre-trained on 2.3B documents (2.7T tokens, 142.4B sentences) using 256 A10
- **2024-12-09** — [[sources/01KJV65FZD-training-large-language-models-to-reason-in-a-continuous-latent-space|Training Large Language Models to Reason in a Continuous Latent Space]]: Coconut continuous thoughts are fully differentiable, allowing end-to-end optimization by gradient d
- **2024-10-14** — [[sources/01KJVJ4E39-openai-o1s-new-paradigm-test-time-compute-explained|OpenAI o1's New Paradigm: Test-Time Compute Explained]]: OpenAI o1 natively incorporates Chain of Thought, where the model reasons internally for 5 to 60 sec
- **2024-03-14** — [[sources/01KJVAWHZ0-quiet-star-language-models-can-teach-themselves-to-think-before-speaking|Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking]]: The parallel generation algorithm achieves efficiency by caching each forward pass and concatenating
- **2024-03-07** — [[sources/01KJVCZ1FE-yann-lecun-meta-ai-open-source-limits-of-llms-agi-the-future-of-ai-lex-fridman-p|Yann Lecun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI | Lex Fridman Podcast #416]]: JEPA (Joint Embedding Predictive Architecture) trains a predictor to predict the representation of a
