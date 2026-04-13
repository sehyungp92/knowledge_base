---
type: source
title: 'He Co-Invented the Transformer. Now: Continuous Thought Machines [Llion Jones
  / Luke Darlow]'
source_id: 01KJVDXNW66VKHVRQTZAG9KJF4
source_type: video
authors: []
published_at: '2025-11-23 00:00:00'
theme_ids:
- adaptive_computation
- latent_reasoning
- model_architecture
- reasoning_and_planning
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# He Co-Invented the Transformer. Now: Continuous Thought Machines [Llion Jones / Luke Darlow]

**Authors:** 
**Published:** 2025-11-23 00:00:00
**Type:** video

## Analysis

Briefing

- The central argument is that the field of AI is trapped in a self\-reinforcing "local minimum" around the Transformer architecture – not because it is optimal, but because it is good enough to resist replacement, while simultaneously being too powerful for its fundamental representational failures to be taken seriously\. 
- The Continuous Thought Machine \(CTM\) is presented as a case study in the kind of biologically\-inspired, architecturally heterodox research that may be needed to escape this trap, with synchronisation\-based representations, neuron\-level models, and adaptive sequential computation as its 3 core novelties\. 
- The SudokuBench benchmark is introduced as evidence that current reasoning progress is largely illusory – a veneer of capability concealing a complete absence of genuine break\-in reasoning\.

Key Takeaways

- The field is in an architecture lottery analogous to the RNN era – just as endless LSTM tweaks were rendered irrelevant overnight by the Transformer, today's papers may be similarly wasted effort\.
- "Crushingly better" is the only exit threshold – a new architecture must be so obviously superior that it overrides the immense switching cost of the Transformer ecosystem \(tooling, training know\-how, finetuning infrastructure\)\.
- Neural networks are universal approximators, not natural representers – they can fit a spiral with piecewise linear boundaries without ever representing it as a spiral, and this distinction has deep consequences for extrapolation and generalisation\.
- Jagged intelligence is a structural symptom, not a quirk – the ability to solve PhD\-level problems while making trivially obvious errors reflects something probably fundamentally wrong with current architectures, not a tuning issue\.
- CTM achieves near\-perfect calibration without explicitly optimising for it – this emergent property is treated as a "smoking gun" that the architecture is doing something more correct at a representational level\.
- Adaptive computation time falls out naturally from the CTM's loss design – previous approaches \(e\.g\., Adaptive Computation Time paper\) required heavy hyperparameter sweeps and explicit compute\-penalty losses; the CTM achieves this organically\.
- Synchronisation as representation is a qualitatively different approach to what a "thought" is – rather than a state vector at a single timestep, a thought is something that exists over time, captured as pairwise neuron synchronisation patterns\.
- SudokuBench exposes that current RL\-based reasoning progress is shallow – the best models achieve ~15% accuracy only on the simplest puzzles, and fall back to brute\-force enumeration rather than genuine deductive break\-in reasoning\.
- Andrej Karpathy's "thought traces" insight motivated SudokuBench – the Cracking the Cryptic YouTube channel provides thousands of hours of expert human reasoning traces, a dataset of a qualitatively different kind than internet text\.
- The CTM's leapfrogging maze behaviour under time constraints is an emergent algorithmic discovery – constrained thinking time produced a novel backwards\-tracing, leapfrogging search strategy not explicitly designed in\.
- The research environment itself is the primary bottleneck – talented researchers in academia and industry are not given freedom to pursue speculative ideas; publish\-or\-perish pressure funnels them toward safe architectural tweaks\.
- Collective intelligence and shared memory across parallel CTM agents is an active frontier – the architecture's properties make it a natural candidate for multi\-agent memory experiments that could illuminate cultural knowledge formation\.

The Architecture Lottery and the RNN Analogy

- A direct historical parallel can be drawn between the current Transformer dominance and the pre\-Transformer era of RNNs\.
	- Character\-level language modelling on LSTMs/GRUs produced endless incremental results: 1\.26 > 1\.25 > 1\.24 bits per character, each publishable\.
		- Variants included: identity matrix initialisation for ReLU compatibility, repositioned gates, upward\-as\-well\-as\-sideways gating, hierarchical LSTMs, which appeared to learn sentence structure from Wikipedia, but improvements remained marginal\.
	- The first deep decoder\-only Transformer applied to language modelling immediately achieved ~1\.1 bits per character\. The result was so anomalous that all prior RNN research was rendered redundant essentially overnight\.
	- The same dynamic is arguably happening now: papers tweaking normalisation layer placement, training schedules, positional embeddings\.
- The concept of the hardware lottery is extended to an architecture lottery – entire research trajectories are shaped by which architecture happens to be winning at a given moment\.
	- The rise of "AI engineers" doing prompt engineering has replaced data scientists and ML engineers doing architectural work in mid\-size enterprises\. The fundamental skills needed to discover new architectures are atrophying at the population level\.

Why the Transformer Resists Displacement

- There are architectures that outperform Transformers in research settings, but "better" is not good enough; it must be "crushingly, obviously better\."
	- The Transformer displaced RNNs because it was faster to train, higher accuracy, and just worked when applied to new problems – the superiority was undeniable\. The deep learning revolution was similar: symbolic AI sceptics could not ignore the empirical gap\.
	- The gravitational pull of the established ecosystem is immense: tooling, training recipes, finetuning pipelines, inference infrastructure, institutional knowledge\.
		- OpenAI scaling a Transformer 10× can beat a novel architecture – this is always the available counter\-move\.
- Foundation models are too good at appearing to solve problems, which allows representational failures to be swept under the carpet\. With enough patience, compute, and data, a neural network can be f

## Key Claims

1. Transformer research is an oversaturated space, making exploration of alternative architectures more valuable
2. The Continuous Thought Machine (CTM) features native adaptive compute as a core architectural property
3. The CTM uses neural synchronization as its core representational mechanism rather than instantaneous neuron states
4. The CTM is biologically and neuroscience inspired, using higher-level concepts for neurons
5. Alternative architectures to transformers exist and have been shown to work better in research, but not by a sufficient margin to displace the transformer ecosystem
6. Transformers displaced RNNs because they were so dramatically better in training speed and accuracy that adoption was unavoidable
7. The deep learning revolution succeeded over symbolic AI because the performance gap was too large to ignore despite initial skepticism
8. Scaling transformers to larger sizes can outperform smaller novel architectures, reducing incentive to switch
9. The AI field is bolting adaptive computation and uncertainty quantification onto transformer architectures rather than building architectures that intrinsically support these properties
10. The CTM's first novelty is an internal thought dimension that applies compute sequentially, related to latent reasoning concepts

## Capabilities

- Continuous Thought Machine (CTM) — a recurrent architecture with native adaptive computation, biological inspiration (synchronization-based neuron representations), and intrinsic sequential reasoning through internal thought dimensions
- CTM-based maze solving with emergent backtracking and leapfrogging algorithms — models discover efficient solution strategies (backtracking mid-solution, forward-jumping-then-backward-filling) when constrained on thinking steps, rather than brute-force tracing
- CTM achieves near-perfect model calibration naturally without explicit optimization — when measuring calibration after training, models predict probabilities that align with actual correctness rates without post-hoc calibration tricks
- CTM on ImageNet classification with adaptive compute — the model can dynamically allocate reasoning steps (tested at 50 steps) based on image difficulty; easy samples require fewer steps, difficult samples use more
- Autonomous end-to-end AI research generation — AI system can seed with initial research idea, then independently generate hypotheses, write code, run experiments, collect results, and produce publication-quality paper; 100% AI-generated paper achieved workshop acceptance
- Sudoku Bench — reasoning benchmark of variant Sudoku puzzles with handcrafted, diverse constraints requiring strong natural language understanding and abstract reasoning (e.g., rule interpretation beyond standard Sudoku mechanics)

## Limitations

- Traditional neural network architectures (ReLU MLPs, CNNs) cannot natively solve sequential reasoning problems — they approximate spiral structure with piecewise linear boundaries rather than learning the spiral as an abstract pattern, preventing extrapolation beyond training domain
- Transformer architectures have no intrinsic mechanism for adaptive computation allocation — compute is fixed per token; adaptive computation must be bolted on rather than emerging naturally from the architecture
- Jagged intelligence — LLMs exhibit inconsistent reasoning across difficulty levels, solving PhD-level problems in one sequence while making obviously incorrect statements in the next, suggesting fundamental architectural mismatch for variable-difficulty reasoning
- Alternative architectures cannot displace transformers despite superior performance — research shows competing architectures work better, but improvements are not 'crushingly better' enough to justify switching costs; industry has invested all tooling, training know-how, inference optimization aroun
- Current AI research environment constrains radical architectural innovation — academic publish-or-perish pressure and industry commercialization pressure discourage risky or unconventional ideas; researchers self-censor radical proposals to increase acceptance likelihood
- Evolutionary/population-based search methods remain unexplored at scale despite theoretical promise — only tens of thousands of evolution-based runs conducted while hundreds of millions invested in transformer scaling, but industry captured by transformer momentum makes funding evolutionary search p
- Possible shortcut learning and 'mirage' in current LLMs — language models may rely on fractured entangled representations and brittle pattern-matching rather than robust understanding; fundamental problems with current approaches may be hidden or undetectable at current scales
- Current RL algorithms cannot discover rare abstract reasoning patterns — Sudoku variant reasoning requires sampling from an extremely sparse solution space where breakthrough reasoning strategies are rare; standard RL approaches fail because the sampling density is insufficient to discover novel rea
- Memory and coordination mechanisms underdeveloped in current systems — no effective approaches for long-term memory, multi-agent shared memory structures, or persistent learning across episodes in recurrent architectures
- AI systems cannot fully understand vague initial problem specifications without human steering — even advanced AI requires iterative back-and-forth with humans to maintain fidelity to original intent; path dependence and rich provenance cannot be fully captured in initial seed instructions

## Bottlenecks

- Transformer architecture lacks intrinsic adaptive computation mechanism — cannot naturally allocate variable compute to problems of different difficulty; fixed compute-per-token design prevents difficulty-dependent reasoning allocation
- Evolutionary and population-based search methods unexplored at scale due to industry momentum — hundreds of millions invested in transformer scaling while only tens of thousands of evolutionary runs conducted; institutional and capital constraints prevent exploring this research direction
- Academic and industry pressure toward established approaches — publish-or-perish incentives, commercialization demands, and technology capture discourage radical innovation; researchers self-censor unconventional ideas to maximize acceptance
- Sparse solution space for abstract reasoning patterns prevents RL from discovering novel reasoning strategies — variant Sudoku and similar reasoning tasks require discovering rare solution approaches that fall outside practical RL sampling distributions
- Quadratic memory and computational scaling of neural synchronization representation in CTM — the D²/2 possible neuron synchronization combinations grows quadratically with neuron count D, limiting deployment to small models
- Long-term memory mechanisms not yet integrated into recurrent reasoning architectures — multi-agent coordination, persistent learning, and memory retrieval are active research areas with no production solutions

## Breakthroughs

- Continuous Thought Machines (CTM) — a recurrent architecture achieving native adaptive computation, biological-inspired neural representations (synchronization-based), and intrinsic sequential reasoning without explicit architecture bolting or task-specific hacks
- Emergent discovery of efficient algorithms under computational constraints — when CTM is constrained on available thinking steps, models discover efficient solution strategies (leapfrogging, backtracking, forward-skipping-then-backward-filling) rather than brute-force tracing
- Synchronization-based latent representations for reasoning — using neuron synchronization patterns (D²/2 combinations) rather than neuron states (D dimensions) as the representation of thoughts enables richer latent structure, natural multi-timescale dynamics, and emergent calibration
- Autonomous end-to-end scientific paper generation — AI systems can generate publication-quality research papers from seed idea through hypothesis, code, experiments, and writeup with workshop acceptance without human intervention at any step

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/diffusion-language-model|Diffusion language model]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
