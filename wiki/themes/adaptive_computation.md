---
type: theme
title: Adaptive Computation
theme_id: adaptive_computation
level: 2
parent_theme: model_architecture
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 27
sources_since_update: 0
update_count: 1
velocity: 0.3
staleness: 0.0
status: active
tags: []
---
The wiki page already exists at `wiki/themes/adaptive_computation.md`. Here's the content it contains:

---

# Adaptive Computation

> Adaptive Computation is consolidating around a single organizing insight: architecture, optimizer, and memory are not independent design choices but a coupled system, and the field is now living with the consequences of having optimized them separately for so long. Ultra-sparse MoE has crossed from theory into narrow production; optimizer research is stabilizing at frontier scale while exposing deeper structural gaps; and adaptive memory architectures have reached honest maturity, meaning their failure modes are now named even if not yet fixed.

**Parent:** [[themes/model_architecture|Model Architecture]]

Key structural notes:
- Anticipations section is marked as unpopulated (no structured predictions were provided in the data)
- Contradictions captures the two internal tensions: training loss as proxy vs. observed reasoning gains, and sparsity scientific case vs. engineering cost
- Writing avoids em dashes per your style preferences

## Current State

## Capabilities

## Limitations

## Bottlenecks

## Breakthroughs

## Anticipations

## Cross-Theme Implications

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJS3BJW4-the-hidden-drivers-of-hrms-performance-on-arc-agi|The Hidden Drivers of HRM's Performance on ARC-AGI]]: Breakthrough: Iterative outer-loop refinement during training — not bio-inspired architecture 
- **2026-04-08** — [[sources/01KKTE8J95-kimi-k2-open-agentic-intelligence|Kimi K2: Open Agentic Intelligence]]: Breakthrough: MuonClip optimizer: qk-clip technique enables stable large-scale MoE LLM pre-tra
- **2025-12-16** — [[sources/01KJT367PQ-universal-reasoning-model|Universal Reasoning Model]]: Breakthrough: Systematic ablation demonstrates that recurrent inductive bias and nonlinearity 
- **2025-12-01** — [[sources/01KJT6H3QA-stabilizing-reinforcement-learning-with-llms-formulation-and-practices|Stabilizing Reinforcement Learning with LLMs: Formulation and Practices]]: New capability: Routing Replay (R2/R3) stabilises RL training for MoE models by fixing expert ro
- **2025-11-23** — [[sources/01KJVDXNW6-he-co-invented-the-transformer-now-continuous-thought-machines-llion-jones-luke-|He Co-Invented the Transformer. Now: Continuous Thought Machines [Llion Jones / Luke Darlow]]]: Breakthrough: Continuous Thought Machines (CTM) — a recurrent architecture achieving native ad
- **2025-11-15** — [[sources/01KJT8TG9R-mixture-of-states-routing-token-level-dynamics-for-multimodal-generation|Mixture of States: Routing Token-Level Dynamics for Multimodal Generation]]: New capability: Dynamic token-wise sparse routing for multimodal diffusion fusion: a learnable r
- **2025-11-12** — [[sources/01KJT9KDWV-tidar-think-in-diffusion-talk-in-autoregression|TiDAR: Think in Diffusion, Talk in Autoregression]]: TiDAR uses structured causal-bidirectional hybrid attention: causal attention for the prefix (AR sec
- **2025-11-06** — [[sources/01KJS173VZ-5-thoughts-on-kimi-k2-thinking|5 Thoughts on Kimi K2 Thinking]]: INT4 quantization via QAT provides roughly 2x generation speed improvement while maintaining state-o
- **2025-10-29** — [[sources/01KJTBPFB9-scaling-latent-reasoning-via-looped-language-models|Scaling Latent Reasoning via Looped Language Models]]: Breakthrough: Looped Language Models demonstrated at frontier training scale (7.7T tokens) to 
- **2025-10-17** — [[sources/01KKT3SS8Q-deepseek-ocr-contexts-optical-compression|DeepSeek-OCR: Contexts Optical Compression]]: DeepSeek-OCR's training data consists of 70% OCR data, 20% general vision data, and 10% text-only da
- **2025-10-06** — [[sources/01KJTEH94B-less-is-more-recursive-reasoning-with-tiny-networks|Less is More: Recursive Reasoning with Tiny Networks]]: Breakthrough: TRM (7M parameters, ~1000 training examples) achieves ARC-AGI-1 and ARC-AGI-2 pe
- **2025-09-11** — [[sources/01KKT42HFY-kimi-k2-open-agentic-intelligence|KIMI K2: OPEN AGENTIC INTELLIGENCE]]: Breakthrough: Empirical sparsity scaling law for MoE: increasing expert count at fixed active 
- **2025-08-08** — [[sources/01KJTMGSTS-glm-45-agentic-reasoning-and-coding-arc-foundation-models|GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models]]: A two-stage difficulty-based curriculum for RL enables models to surpass their performance ceiling b
- **2025-08-07** — [[sources/01KJS3SRMJ-gpt-5-and-the-arc-of-progress|GPT-5 and the arc of progress]]: Breakthrough: First commercially deployed AI system using multiple distinct model architecture
- **2025-07-14** — [[sources/01KJSRWREB-kimi-k2-and-when-deepseek-moments-become-normal|Kimi K2 and when "DeepSeek Moments" become normal]]: Kimi K2 was trained on 15.5 trillion tokens.
- **2025-07-14** — [[sources/01KJTN8HBD-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-token-level|Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation]]: Breakthrough: Mixture-of-Recursions (MoR): first architecture unifying parameter efficiency (w
- **2025-06-26** — [[sources/01KJTMPYR9-hierarchical-reasoning-model|Hierarchical Reasoning Model]]: Breakthrough: Hierarchical convergence mechanism overcomes premature convergence in RNNs, enab
- **2025-05-17** — [[sources/01KJTT48H0-model-merging-in-pre-training-of-large-language-models|Model Merging in Pre-training of Large Language Models]]: Merging checkpoints from the stable (constant learning rate) training phase produces consistent and 
- **2025-05-15** — [[sources/01KJTVCEFH-parallel-scaling-law-for-language-models|Parallel Scaling Law for Language Models]]: New capability: Dynamic parallel scaling enables a single frozen backbone to serve multiple capa
- **2025-05-14** — [[sources/01KJTVG7CE-qwen3-technical-report|Qwen3 Technical Report]]: Breakthrough: MoE architecture achieving performance parity with prior-generation dense baseli
- **2025-05-08** — [[sources/01KJTVJC6B-continuous-thought-machines|Continuous Thought Machines]]: Breakthrough: Adaptive computation time emerges as a natural architectural property of neural 
- **2025-04-10** — [[sources/01KJTPMJBF-kimi-vl-technical-report|Kimi-VL Technical Report]]: Breakthrough: RL-trained long-CoT on a ~3B activated parameter MoE VLM achieves reasoning benc
- **2025-02-04** — [[sources/01KJVHGZW3-how-deepseek-changes-the-llm-story|How DeepSeek Changes the LLM Story]]: New capability: Sparse Mixture-of-Experts routing with load balancing in distributed training: 6
- **2024-12-27** — [[sources/01KJV5S7TQ-deepseek-v3-technical-report|DeepSeek-V3 Technical Report]]: Breakthrough: Auxiliary-loss-free MoE load balancing via dynamic bias term proves strictly sup
- **2024-12-13** — [[sources/01KJV64ZDF-byte-latent-transformer-patches-scale-better-than-tokens|Byte Latent Transformer: Patches Scale Better Than Tokens]]: Breakthrough: Dynamic entropy-based patching discovers a new LLM scaling axis: model capacity 
- **2024-12-06** — [[sources/01KJV68FPF-smoothie-label-free-language-model-routing|Smoothie: Label Free Language Model Routing]]: SMOOTHIE does not consider cost tradeoffs between large and small models when routing, optimizing on
- **2023-10-03** — [[sources/01KJVBR6K0-ring-attention-with-blockwise-transformers-for-near-infinite-context|Ring Attention with Blockwise Transformers for Near-Infinite Context]]: Transformer self-attention has memory cost quadratic in input sequence length, making it challenging
