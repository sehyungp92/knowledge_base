---
type: source
title: 'Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach'
source_id: 01KJV49W0K92F6SQQ3HMJTR25N
source_type: paper
authors:
- Jonas Geiping
- Sean McLeish
- Neel Jain
- John Kirchenbauer
- Siddharth Singh
- Brian R. Bartoldson
- Bhavya Kailkhura
- Abhinav Bhatele
- Tom Goldstein
published_at: '2025-02-07 00:00:00'
theme_ids:
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
# Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach

**Authors:** Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Tom Goldstein
**Published:** 2025-02-07 00:00:00
**Type:** paper

## Analysis

# Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach
2025-02-07 · paper · Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh et al. (9 total)
https://arxiv.org/pdf/2502.05171

---

### Motivation & Prior Limitations
- Mainstream test-time compute scaling forces all reasoning to be verbalized as tokens, which is wasteful because it compresses rich internal computation into a single predicted next token and cannot capture reasoning that defies verbalization (e.g., spatial thinking, physical intuition, motor planning).
  - Chain-of-thought scaling requires bespoke long-context training data constructed per domain, demands large context windows with specialized training methods like token-parallelization, and is constrained to linear reasoning rather than parallel exploration of a high-dimensional latent space.
- Scaling model size through pretraining (the prior dominant axis) requires extreme data and compute, and there was no demonstrated third axis of scaling distinct from parameter count and context length.
- Recurrent-depth language models had been theorized and studied at small scale but had never been shown to scale reliably to billions of parameters and hundreds of billions of training tokens, with prior attempts at scale suffering hidden-state collapse and failure to leverage recurrence.

---

### Proposed Approach
- The paper proposes Huginn-0125, a 3.5B-parameter depth-recurrent transformer that iterates a shared recurrent block R for a variable number of steps at both train and test time, reasoning entirely in continuous latent space without producing intermediate tokens.
  - Unlike chain-of-thought models, the architecture requires no specialized training data and no long context windows; it is trained on standard pretraining data with recurrence count r randomly sampled per sequence from a log-normal Poisson distribution, optimizing the expectation of loss over both data and iteration counts.
  - The architecture is divided into three functional groups: a **prelude** P that embeds input tokens into latent space, a **core recurrent block** R that iteratively updates a hidden state s with input e re-injected at every step (analogous to gradient descent on data-dependent functions), and a **coda** C that unembeds the final state to produce output probabilities; the initial state s₀ is randomized to promote path independence.
- Stabilizing training at scale required a "sandwich" normalization format (alternating norm layers around attention and MLP), a learned adapter concatenating hidden state and embedded input rather than addition, careful initialization (Takase et al. 2024 variance prescription), and a reduced peak learning rate of 4×10⁻⁵; earlier runs with simpler setups collapsed to token correlation ≈1.0 or learned to ignore incoming state entirely.
- Backpropagation is truncated to only the last k=8 iterations of the recurrence to keep memory and compute independent of the sampled depth r, analogous to truncated BPTT in RNNs but applied in the depth rather than time dimension.

---

### Results & Capabilities
- Huginn-0125 (3.5B parameters, 800B tokens) matches or exceeds the performance of OLMo-7B (first generation, 2.5T tokens) on standard benchmarks and dramatically outperforms same-size models like Pythia-2.8B across ARC, HellaSwag, MMLU, PiQA, and SciQ when run at r=16–32, despite having far fewer parameters and training tokens.
  - At r=32, the model scores 38.23% on ARC-Challenge, 65.21% on HellaSwag, and 31.38% on MMLU zero-shot; by increasing recurrence to r=64, effective compute reaches the equivalent of a ~50B parameter fixed-depth transformer, with "materialized parameters" reaching 103B.
- On mathematical reasoning, the model at r=32 achieves 28.05%/38.13% GSM8K (flexible/strict with system prompt), 34.80%/42.08% on GSM8K CoT, and 12.58% on Minerva MATH, surpassing all compared models except OLMo-2-1124 which was trained on 5× more tokens with a much larger model.
  - The EMA-averaged model at r=64 reaches 47.23% GSM8K flexible, and math/code performance continues to scale almost linearly with training tokens throughout the 800B run, unlike general language tasks which saturate earlier.
- On coding, the model achieves 24.80% MBPP and 23.17% HumanEval pass@1, beating all comparable general-purpose open-source models, though it falls short of dedicated code models like StarCoder2 trained on 3.3–3.7T tokens.
- The recurrent design naturally enables several zero-shot inference-time capabilities without any additional training: per-token adaptive compute via KL-divergence exit criterion (mean ~12–16 steps depending on task difficulty), KV-cache sharing with minimal performance loss (MTBench 5.86 at cache budget 4 vs. 5.63 standard), continuous chain-of-thought via warm-starting hidden state across tokens, and self-speculative decoding using fewer recurrence steps to draft and more to verify.
- Latent trajectory analysis reveals emergent computation patterns: tokens requiring complex reasoning (e.g., numerical values, key semantic tokens) follow orbital patterns in PCA-projected latent space rather than converging monotonically, analogous to periodic patterns observed in fixed-depth transformers trained on modular arithmetic but appearing far more broadly; some tokens exhibit "slider" drifts interpretable as iteration counters.
- Compute saturation is task-dependent: easier tasks like OpenBookQA and HellaSwag saturate at r=8, while GSM8K CoT continues improving through r=64; saturation point also correlates with available context—providing 25–50 few-shot examples shifts ARC-C saturation from r≈8 to r≈32.

---

### Implications
- Latent recurrence constitutes a third independent axis of scaling beyond parameter count and context length, suggesting future scaling laws may need to account for depth-recurrence alongside the established parameter and data axes.
- The zero-shot emergence of adaptive compute, KV-cache shar

## Key Claims

1. A recurrent depth language model can scale test-time computation by implicitly reasoning in latent space, without producing additional tokens.
2. Latent recurrent reasoning does not require any specialized training data, unlike chain-of-thought approaches.
3. The recurrent depth architecture introduces a 'third axis' for scaling model performance, complementary to inference scaling via extended verbalization and pretraining parameter scaling.
4. The recurrent model architecture consists of three functional groups: a prelude (embedding), a core recurrent block (iterated), and a coda (unembedding and prediction head).
5. The latent state is initialized with random noise and data is re-injected at every recurrence step to stabilize the recurrence and promote path independence.
6. The large-scale model with shape (2, 4, 2) and hidden size 5280 has only 8 real layers, but when the recurrent block is iterated 32 times, it unfolds to an effective depth of 132 layers.
7. A 'sandwich' normalization format is required to train the recurrence at scale; other normalization strategies (pre-norm, post-norm) fail at large scale.
8. Truncated backpropagation through only the last k=8 iterations is used to keep memory and compute low, making training cost independent of the sampled recurrence depth.
9. The degree of test-time compute saturation is highly task-dependent: easier tasks saturate with fewer recurrences while harder reasoning tasks benefit from more compute.
10. At 180B tokens, the recurrent model outperforms its non-recurrent baseline on harder tasks such as ARC challenge, with especially pronounced gains on GSM8K where the recurrent model is 5 times better.

## Capabilities

- A 3.5B parameter recurrent-depth language model (Huginn-0125) scales test-time compute by iterating a recurrent block in latent space, achieving reasoning performance equivalent to a 50B parameter transformer — without chain-of-thought verbalization or specialized training data
- Zero-shot per-token adaptive compute allocation in recurrent-depth models using KL-divergence between successive latent states as an exit criterion — harder tasks automatically receive more compute iterations without any specialized early-exit training
- Zero-shot KV-cache sharing across recurrence iterations by cycling a fixed budget of cache entries — reduces memory footprint without retraining, validated at cache budget of 4 with no measurable MTBench degradation
- Zero-shot self-speculative decoding using fewer recurrence iterations to draft tokens, verified by more iterations — no separate draft model, fine-tuning, or Medusa heads required; draft states are reused during verification without waste
- Zero-shot continuous chain-of-thought via latent warm-starting: initializing the recurrent state from the previous token's final latent state reduces average convergence steps by 1–2, enabling implicit reasoning carried across token boundaries
- Context-proportional compute allocation emerges naturally: providing 25–50 few-shot examples shifts the recurrence saturation point from ~8–12 iterations (zero-shot) to ~32 iterations — the model allocates more latent compute when given more information to reason about
- Structured geometric computational patterns — orbital trajectories, convergent fixed-point paths, and directional drift ('sliders') — emerge spontaneously in recurrent-depth latent space from scale alone, without any explicit training objective for them; convergence rates vary by semantic importance

## Limitations

- The model is a single proof-of-concept training run without learning rate cooldown and on an unablated data mixture — gains from better hyperparameter search, data curation, and LR schedule are unknown but likely substantial
- Training recurrent-depth models at scale requires highly specific normalization ordering ('sandwich' format) and initialization variance — two training runs failed due to hidden state correlation collapse and recurrence collapse before the correct configuration was found; this sensitivity does not m
- At a single recurrence iteration (r=1), the recurrent model performs near-randomly on most reasoning benchmarks (GSM8K CoT: 0.00/0.00, HellaSwag: 29.34, MMLU: 23.60) — the architecture provides almost no useful output without multiple iterations, making it unusable in low-compute regimes
- The compute-heavy, parameter-light architecture has reduced factual memorization capacity relative to same-parameter-count dense transformers — closing the gap to OLMo-2 on OpenBookQA requires providing facts as context, indicating the model cannot recall them from weights
- Post-training approaches (RLHF, RLVR, instruction tuning, CoT internalization fine-tuning) are entirely absent — the full capability of recurrent-depth models after post-training is unknown, leaving a large potential capability gap uncharacterized
- Test-time compute scaling saturates rapidly on knowledge-recall tasks (OpenBookQA converges at ~4 recurrences) while the compute cannot be redistributed to harder tokens or co-occurring harder tasks — the model cannot concentrate its recurrence budget selectively on hard sub-problems
- Truncated backpropagation through only the last k=8 recurrence iterations limits gradient signal quality for very deep recurrence — long-range credit assignment across many recurrence steps is not learned
- Integration with modern efficiency architecture improvements (linear attention, mixture-of-experts, multi-stage recurrence) is entirely unexplored — interaction effects between recurrent depth and these techniques are unknown
- At scale, the model achieved only 41–51% achievable FLOP utilization on AMD MI250X GPUs due to interconnect issues that required a hand-crafted distributed implementation — training efficiency on commodity GPU clusters is not established
- Safety alignment, jailbreak resistance, and robustness of latent reasoning are entirely unstudied — the model's refusal behavior is noted only anecdotally; the opacity of latent computation makes alignment auditing fundamentally harder than token-level chain-of-thought
- The model significantly trails OLMo-2 (trained on 4T tokens vs 800B here) across most benchmarks, demonstrating that data scale effects persist even when architectural compute efficiency is substantially improved — data quantity remains a primary performance driver

## Bottlenecks

- Chain-of-thought test-time scaling forces all internal computation through a single-token projection bottleneck at each step — non-verbalizable reasoning (spatial thinking, physical intuition, motor planning) is inaccessible to CoT-based approaches and parallel latent exploration is impossible in li
- Chain-of-thought requires domain-specific training data construction — long demonstrations in the target domain — creating a data acquisition bottleneck that limits generalization to new reasoning domains and concentrates capability development at labs with data pipelines
- Stable training of recurrent-depth models at scale requires precise normalization and initialization choices that are non-obvious and do not manifest at small scale — two failed large-scale runs demonstrate that the parameter space of stable configurations is narrow and not transferable from small-s
- No established post-training paradigm (RLHF, RLVR, instruction tuning, CoT internalization) exists for recurrent-depth models — the capability uplift that post-training delivers in standard transformers remains entirely unavailable for this architecture class

## Breakthroughs

- First demonstration at billion-parameter scale that latent recurrent depth enables test-time compute scaling without chain-of-thought verbalization or specialized training data — a 3.5B parameter model iterates a shared recurrent block to achieve reasoning performance equivalent to a 50B parameter f
- Structured geometric computation patterns — orbital trajectories, directional drifts, and convergent fixed points — emerge spontaneously in latent space of recurrent-depth models from truncated unrolling training alone, revealing that high-dimensional latent iteration enables novel computational str

## Themes

- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
