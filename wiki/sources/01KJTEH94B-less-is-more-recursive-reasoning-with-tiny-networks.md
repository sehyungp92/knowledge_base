---
type: source
title: 'Less is More: Recursive Reasoning with Tiny Networks'
source_id: 01KJTEH94BHV0E2PZ37AVE8EDG
source_type: paper
authors:
- Alexia Jolicoeur-Martineau
published_at: '2025-10-06 00:00:00'
theme_ids:
- adaptive_computation
- latent_reasoning
- model_architecture
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Less is More: Recursive Reasoning with Tiny Networks

**Authors:** Alexia Jolicoeur-Martineau
**Published:** 2025-10-06 00:00:00
**Type:** paper

## Analysis

# Less is More: Recursive Reasoning with Tiny Networks
2025-10-06 · paper · Alexia Jolicoeur-Martineau
https://arxiv.org/pdf/2510.04871

---

### Motivation & Prior Limitations
- LLMs struggle on hard structured reasoning tasks despite Chain-of-Thought and Test-Time Compute augmentations, because auto-regressive generation is fragile to single token errors and CoT reasoning traces can themselves be incorrect.
  - As of the paper's writing (Oct 2025), no LLM has reached human-level accuracy on ARC-AGI-1 despite six years of effort; Gemini 2.5 Pro achieves only 4.9% on ARC-AGI-2 even with high TTC.
  - Top LLMs including Deepseek R1 and o3-mini-high score 0.0% on Sudoku-Extreme and Maze-Hard with chain-of-thought.
- The prior state-of-the-art small-model approach, Hierarchical Reasoning Model (HRM, Wang et al. 2025), introduced recursive hierarchical reasoning but rested on theoretically questionable foundations that limited both interpretability and performance.
  - HRM applies the Implicit Function Theorem and 1-step gradient approximation to justify backpropagating through only 2 of 6 recursion steps, but fixed-point convergence is not guaranteed — and HRM's own visualization shows residuals remain substantially above zero when the approximation is invoked.
  - HRM's Adaptive Computational Time (ACT) mechanism requires two full forward passes per optimization step due to a Q-learning continue loss, doubling training compute cost without a documented justification.
  - HRM's design is motivated by complex biological arguments about brain temporal frequencies, making it difficult to isolate which components drive performance; the original paper provides no ablation table.
  - An independent ARC Prize Foundation analysis found that HRM's hierarchical recursion contributed only marginally (35.7% → 39.0%), while deep supervision was the primary driver (19% → 39%), suggesting the recursion design was underoptimized.

---

### Proposed Approach
- Tiny Recursion Model (TRM) is a single 2-layer network that recursively refines a latent reasoning state z and a proposed answer y over multiple steps, eliminating the need for two networks, fixed-point theorems, or biological justifications.
  - Where HRM uses two separate networks (fL and fH) operating at different frequencies with 4 layers each, TRM replaces both with one shared network that performs both latent update (z ← net(x, y, z)) and answer refinement (y ← net(y, z)), differentiated purely by whether the input question x is included.
  - Instead of the 1-step gradient approximation, TRM runs T−1 full recursion passes (n evaluations of the network) without gradients to improve (y, z), then one full pass with backpropagation — eliminating the need to assume fixed-point convergence while preserving memory efficiency.
- TRM reinterprets the two latent variables non-biologically: z is a latent chain-of-thought (reasoning state) and y is the current proposed solution, with x as the input question — providing a clean justification for why exactly two features are optimal.
  - Experiments confirm this: splitting z into n separate multi-scale features drops Sudoku-Extreme accuracy from 87.4% to 77.6%, and collapsing to a single feature drops it to 71.9%, because a single feature forces the model to encode the solution y within the reasoning state.
- TRM simplifies ACT by replacing the Q-learning continue loss (which required a second forward pass) with a single Binary Cross-Entropy halting probability trained on whether the current answer is correct, reducing training to one forward pass per step.
- For tasks with small, fixed context lengths (e.g., 9×9 Sudoku), TRM replaces self-attention with an MLP over the sequence dimension (inspired by MLP-Mixer), which is cheaper when L ≤ D and yields better generalization; for larger grids (30×30), self-attention is retained.
- Exponential Moving Average (EMA) of weights is used to stabilize training under small-data conditions where HRM tends to overfit and diverge.
- Counter-intuitively, TRM uses 2-layer networks rather than 4-layer networks, scaling recursion depth (n) proportionally to maintain similar effective compute — a deliberate inductive bias against overfitting on small datasets.

---

### Results & Capabilities
- TRM with 7M parameters achieves 44.6% on ARC-AGI-1 and 7.8% on ARC-AGI-2, outperforming all LLMs tested except Grok-4-based systems, while using less than 0.01% of their parameters.
  - Comparisons: Deepseek R1 (671B) scores 15.8% / 1.3%; o3-mini-high scores 34.5% / 3.0%; Gemini 2.5 Pro scores 37.0% / 4.9%; Claude 3.7 16K scores 28.6% / 0.7%. TRM outperforms all of these on both benchmarks.
  - HRM (27M parameters) achieves 40.3% / 5.0%; TRM (7M) improves both with 4× fewer parameters.
- TRM pushes state-of-the-art on Sudoku-Extreme from 55% (HRM) to 87.4% and on Maze-Hard from 74.5% (HRM) to 85.3%, on 1K training examples with 423K test examples for Sudoku.
- The ablation on Sudoku-Extreme isolates the contribution of each TRM design choice: replacing the 1-step gradient approximation with full-recursion backpropagation is the single largest contributor (56.5% → 87.4%); EMA adds 7.5 points; using a single network over two separate networks adds 5 points; 2-layer over 4-layer adds ~8 points; MLP over self-attention adds ~13 points.
- Effective depth per supervision step for TRM (T=3, n=6, 2 layers) is 42, compared to HRM's 24, achieved with a 5–7M parameter model versus HRM's 27M, demonstrating that recursive depth is a more parameter-efficient axis to scale than model width or layer count under data scarcity.

---

### Implications
- Recursive latent refinement over a fixed tiny network may be a fundamentally more parameter-efficient inductive bias for hard structured reasoning than scaling model size, suggesting that test-time compute via iterative latent improvement is a viable alternative to chain-of-thought over token sequences.
- The success of TRM challenges the implicit assumpti

## Key Claims

1. LLMs with Chain-of-Thought and Test-Time Compute are insufficient to solve every hard problem, as demonstrated by Gemini 2.5 Pro achieving only 4.9% test accuracy on ARC-AGI-2 with high TTC.
2. Deep supervision is the primary driver of HRM's performance gains on ARC-AGI, doubling accuracy from 19% to 39%, while recursive hierarchical reasoning only marginally improves performance from 35.7% 
3. HRM's Adaptive Computational Time mechanism requires two forward passes per optimization step because its Q-learning continue loss requires an extra full forward pass through HRM.
4. HRM's application of the Implicit Function Theorem with 1-step gradient approximation is theoretically unsound because there is no guarantee a fixed point is reached during its recursion steps.
5. HRM's two latent features can be reinterpreted simply as the current proposed solution (zH=y) and a latent reasoning feature (zL=z), without requiring biological or hierarchical justification.
6. Replacing two separate networks (fL and fH) in HRM with a single shared network in TRM improves generalization on Sudoku-Extreme from 82.4% to 87.4% while halving the number of parameters.
7. Reducing from 4 layers to 2 layers while scaling the number of recursions proportionally improves generalization on Sudoku-Extreme from 79.5% to 87.4% and reduces parameters by half, contrary to typic
8. Smaller networks generalize better in the low-data regime because larger models overfit when data is too scarce, making tiny networks with deep recursion and deep supervision effective at bypassing ov
9. Exponential Moving Average of weights prevents sharp collapse and improves generalization in the low-data regime, increasing Sudoku-Extreme accuracy from 79.9% to 87.4%.
10. TRM with self-attention and 7M parameters outperforms HRM with 27M parameters on all tested benchmarks, achieving 85.3% vs 74.5% on Maze-Hard, 44.6% vs 40.3% on ARC-AGI-1, and 7.8% vs 5.0% on ARC-AGI-

## Capabilities

- 7M parameter TRM achieves 44.6% on ARC-AGI-1 and 7.8% on ARC-AGI-2 public evaluation — surpassing Deepseek R1 (671B), o3-mini-high, and Gemini 2.5 Pro — using recursive latent reasoning with deep supervision on ~1000 training examples
- TRM (5M–7M parameters) achieves 87.4% test accuracy on Sudoku-Extreme trained on only 1K examples — surpassing HRM (27M, 55%) and achieving 0% baseline for all frontier LLMs including Deepseek R1, Claude 3.7, and o3-mini
- Full backpropagation through a complete recursion loop (without fixed-point approximation) enables tiny 2-layer networks to achieve dramatically better generalisation than larger hierarchical multi-network approaches — 87.4% vs 56.5% on Sudoku-Extreme
- Deep supervision (reusing latent states across iterative supervision steps) enables tiny networks to emulate 384+ effective layers of reasoning depth without backpropagating through all layers — the primary driver of recursive model performance gains over baselines
- Bespoke Grok-4 (1.7T parameters) achieves 79.6% on ARC-AGI-1 and 29.4% on ARC-AGI-2 — the highest reported ARC-AGI-2 score in this paper, significantly above the 'essentially unsolved' characterisation from earlier in 2025

## Limitations

- Frontier LLMs including Deepseek R1 (671B), Claude 3.7, and o3-mini-high achieve exactly 0% accuracy on Sudoku-Extreme and Maze-Hard despite chain-of-thought and test-time compute — a complete performance cliff for combinatorial constraint-satisfaction puzzles
- Recursive reasoning models (TRM, HRM) are deterministic supervised methods producing a single answer — they cannot generate multiple candidate solutions, express uncertainty, or be applied to open-ended generative tasks
- No theoretical explanation exists for why recursive latent computation outperforms equivalent-depth feedforward networks — the empirical advantage of recursion is observed but not mechanistically understood
- No scaling laws established for recursive reasoning architectures — optimal network size, recursion depth (n, T), and training data quantity cannot be principally determined for new problem domains
- Full backpropagation through recursion causes Out-of-Memory errors as recursion depth (n) increases — a hard memory ceiling constrains the maximum achievable reasoning depth for TRM
- Attention-free MLP architecture (TRM-MLP) fails catastrophically on tasks with large or variable context length — 0% on Maze-Hard and substantially worse than TRM-Att on ARC-AGI, making it non-general
- TRM and HRM results depend on extreme data augmentation — 1000 augmentations per training example for Sudoku and ARC-AGI — raising questions about whether the system generalises from reasoning or from augmentation-specific invariances
- Adding model capacity (more layers) decreases generalisation in recursive reasoning models trained on small data — the models are data-starved rather than parameter-starved, blocking straightforward scaling
- ARC-AGI-2 remains essentially unsolved: even the best system in this paper (Bespoke Grok-4) achieves only 29.4%, TRM achieves 7.8%, and most LLMs score below 5% — the benchmark is not being saturated at any meaningful rate
- TRM/HRM approaches have zero evaluation on natural language or open-domain tasks — the complete absence of NLP evaluation leaves unknown whether recursive latent reasoning generalises beyond structured discrete puzzles
- Limited computational resources at the lab level prevent full exploration of optimal recursion depth (T, n) for harder tasks — the relationship between recursion depth and ARC-AGI-2 performance is unknown
- CoT for LLMs is expensive, data-hungry (requires high-quality reasoning traces), and brittle to intermediate errors — it is not a robust foundation for hard structured reasoning

## Bottlenecks

- No theoretical understanding of recursive latent reasoning — why weight-shared recursion outperforms equivalent-depth feedforward networks, under what conditions it fails, and how to scale hyperparameters are all unknown, blocking principled design
- Memory cost of full backpropagation through recursion caps achievable reasoning depth in TRM — OOM errors prevent exploration of the deeper recursion that harder tasks likely require
- Recursive supervised reasoning models are architecturally confined to deterministic single-answer inference — extending to generative tasks, multi-hypothesis reasoning, or open-ended language requires solving the fundamental mismatch between fixed-point convergence and distributional output

## Breakthroughs

- TRM (7M parameters, ~1000 training examples) achieves ARC-AGI-1 and ARC-AGI-2 performance surpassing most frontier LLMs at 0.01% of their parameter count — establishing that recursive latent refinement with deep supervision is a viable alternative to massive parameter scaling for abstract structured
- Full backpropagation through a complete recursion loop — discarding the Implicit Function Theorem fixed-point approximation assumed by HRM — yields a 30+ percentage point generalisation gain (56.5% → 87.4% on Sudoku-Extreme), showing that theoretical shortcuts in gradient approximation are the prima

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/arc-agi-1|ARC-AGI-1]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/conceptarc|ConceptARC]]
- [[entities/rmsnorm|RMSNorm]]
- [[entities/swiglu|SwiGLU]]
- [[entities/test-time-compute|Test-time compute]]
