---
type: source
title: 'Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking'
source_id: 01KJVAWHZ045ZT5CYX1J84DDRB
source_type: paper
authors:
- Eric Zelikman
- Georges Harik
- Yijia Shao
- Varuna Jayasiri
- Nick Haber
- Noah D. Goodman
published_at: '2024-03-14 00:00:00'
theme_ids:
- chain_of_thought
- latent_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking

**Authors:** Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, Noah D. Goodman
**Published:** 2024-03-14 00:00:00
**Type:** paper

## Analysis

# Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
2024-03-14 · paper · Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber et al. (6 total)
https://arxiv.org/pdf/2403.09629

---

### Motivation & Prior Limitations
Prior work on training LMs to reason was constrained to curated QA datasets, which limited both the scale and generalizability of learned reasoning.
- The Self-Taught Reasoner (STaR, Zelikman et al. 2022) could only bootstrap reasoning from task-specific labeled datasets, meaning rationale quality was bounded by the coverage and quality of those datasets.
  - High-quality QA datasets require costly manual curation and will inherently cover only a subset of reasoning tasks, providing no clear path to solving problems harder than what annotators can handle.
- Chain-of-thought and scratchpad approaches all presuppose a question-answer structure and provide reasoning signals only at the level of full answers, not at the level of arbitrary text prediction.
  - Methods like Wang & Zhou (2024) still relied on QA framing and heuristics to identify answer tokens, remaining fundamentally task-scoped.
- No prior work had explicitly trained LMs to generate intermediate rationales for general, unstructured text prediction — despite reasoning being implicit in all written language.

---

### Proposed Approach
Quiet-STaR generalizes STaR by training a language model to generate internal rationales after every token in an arbitrary text sequence, using those rationales to improve predictions of future tokens via REINFORCE.
- Rather than learning to reason on curated QA tasks, Quiet-STaR trains on large internet text corpora (OpenWebMath, C4), treating the diversity of language itself as a multitask reasoning curriculum — grounded in the "language models are unsupervised multitask learners" paradigm.
- The algorithm proceeds in three steps: (1) **Think** — generate multiple rationale candidates in parallel at every token position; (2) **Talk** — mix post-rationale and base next-token predictions using a learned shallow MLP "mixing head"; (3) **Learn** — apply REINFORCE to increase the likelihood of rationales whose inclusion improves prediction of subsequent tokens relative to the average rationale for that position.
- A tokenwise parallel sampling algorithm enables scalable rationale generation across all positions simultaneously, using a diagonal attention mask so each thought attends only to its own preceding tokens and the base text — avoiding the intractable cost of a separate forward pass per token.
- Learned `<|startofthought|>` and `<|endofthought|>` meta-tokens are introduced to signal thought boundaries; their embeddings are initialized from the em-dash token (a natural pause indicator in text) and receive amplified gradient updates to accelerate optimization.
- A **non-myopic loss** extends the REINFORCE reward signal over multiple future tokens (not just the immediate next token) using teacher-forcing on ground-truth continuations, reducing the noise of single-token reward and encouraging rationales that improve broader semantic prediction.
- The mixing head smooths the distribution shift early in fine-tuning: when thoughts are initially out-of-distribution and harmful, the mixer can down-weight them, with the balance shifting as rationale quality improves over training.

---

### Results & Capabilities
Quiet-STaR applied to Mistral 7B via continued pretraining on OpenWebMath yields zero-shot accuracy improvements on both GSM8K (5.9% → 10.9%) and CommonsenseQA (36.3% → 47.2%), with no fine-tuning on either downstream task.
- These gains scale monotonically with rationale length across all evaluated configurations (8–24 thought tokens), providing direct empirical evidence that longer internal reasoning translates to better downstream task performance.
- Training on the more diverse C4 corpus also produces improvements (GSM8K: 5.9% → 8.1%; CommonsenseQA: 36.3% → 42.6%), though smaller than on the math-focused OpenWebMath, consistent with the hypothesis that token density requiring reasoning drives the learning signal.
- Quiet-STaR outperforms "pause token" fine-tuning (Goyal et al. 2023) substantially: pause token fine-tuning yielded only CommonsenseQA 26.9% → 28.8% with no GSM8K gain and multi-token pauses harmed performance, whereas Quiet-STaR achieves much larger improvements with multi-token rationales — supporting the value of generative, interpretable internal thoughts over single compressed tokens.
- When Quiet-STaR's internal rationales are combined with zero-shot chain-of-thought prompting on GSM8K, majority-vote accuracy over 8 samples (cot-maj@8) rises from 40.6% to 47.7%, demonstrating that implicit internal reasoning and explicit chain-of-thought are orthogonal and complementary.
- The distribution of token-level improvement is highly skewed: average improvements across all tokens are small, but improvements on difficult-to-predict tokens are disproportionately large — consistent with the hypothesis that thinking helps specifically when recalling relevant information or bridging reasoning steps is necessary.
- Qualitative inspection shows generated thoughts include near-future-text continuations, relevant theorem or formula recalls, and intermediate procedural steps — all partially human-interpretable despite no explicit interpretability objective.

---

### Implications
Quiet-STaR provides a proof of concept that reasoning ability can be learned from the latent structure of arbitrary internet text rather than requiring labeled reasoning traces, opening a path to scaling reasoning training beyond the bottleneck of curated dataset size and coverage.
- The demonstration that reasoning improves with thought-token length during pretraining (not just at inference) suggests a previously unexploited axis of scaling: more compute at training time, allocated to internal rationale generation over unstructured text, may compound into gener

## Key Claims

1. Quiet-STaR achieves zero-shot improvements on GSM8K from 5.9% to 10.9% without any fine-tuning on the task.
2. Quiet-STaR achieves zero-shot improvements on CommonsenseQA from 36.3% to 47.2% without any fine-tuning on the task.
3. Quiet-STaR generalizes STaR by training LMs to generate rationales at every token position in arbitrary text, rather than only on curated QA datasets.
4. STaR's limitation is that training from curated QA datasets limits the scale and generalizability of rationales, since QA datasets will inherently only cover a subset of reasoning tasks.
5. Quiet-STaR uses a tokenwise parallel sampling algorithm to efficiently generate rationales at every token position, making training scalable.
6. The parallel generation algorithm achieves efficiency by caching each forward pass and concatenating a diagonal attention mask so each generated thought token attends to all tokens used to generate it
7. Quiet-STaR uses learnable <|startofthought|> and <|endofthought|> meta-tokens to mark the boundaries of each rationale, initialized to the em dash embedding.
8. A learned mixing head (shallow MLP) interpolates between the LM's next-token predictions with and without rationales, easing distribution shift early in fine-tuning.
9. Quiet-STaR uses REINFORCE with a reward defined as the difference between a rationale's log-likelihood of future tokens and the average across all rationales for that token, to optimize rationale gene
10. Excluding the negative reward from the REINFORCE loss term leads to more stable training, though it may introduce some bias.

## Capabilities

- Language models can learn to generate internal silent rationales at every token position during continued pretraining on arbitrary internet text, improving zero-shot reasoning without any task-specific fine-tuning
- Parallel token-level rationale generation via custom diagonal attention masks enables simultaneous internal thought generation across all sequence positions in a single forward pass family, making per-token rationale training computationally tractable
- Internal silent rationales trained via Quiet-STaR improve explicit chain-of-thought majority-vote accuracy — cot-maj@8 on GSM8K improves from 40.6% to 47.7% zero-shot
- A purely predictive REINFORCE signal derived from language modeling improvement (not task correctness labels) can serve as a domain-general self-improvement signal for training reasoning rationales

## Limitations

- Quiet-STaR generates rationales at every token regardless of necessity, producing substantial computational overhead with no dynamic gating — the model cannot predict in advance which tokens will benefit from thinking
- On average, thinking provides little improvement across arbitrary tokens — gains concentrate disproportionately on a small fraction of difficult-to-predict tokens, meaning most rationale compute is wasted
- Method validated only on a 7B parameter model — unverified whether gains transfer to larger models, whether the approach can train from scratch, or whether disproportionate reasoning gains at larger scale materialise
- Performance on downstream reasoning tasks deteriorates with extended training, suggesting thought token representations drift toward general language modeling rather than structured reasoning when not anchored by task-specific signal
- The parallel generation approach is hard-capped by memory — thought length is bounded by available GPU memory for storing all counterfactual continuation paths simultaneously
- REINFORCE requires multiple rationale samples per token to reduce gradient variance, multiplying compute cost proportionally — the variance reduction strategy itself is computationally expensive
- Mathematical reasoning gains are modest — GSM8K improves from 5.9% to 10.9% zero-shot — suggesting that rationales learned from general web text do not transfer deeply to structured arithmetic reasoning
- Faithfulness of expressed rationales to actual model computation is fundamentally unverifiable — the natural language rationales may be post-hoc projections unrelated to the actual mechanism producing the output
- No safeguards against learning harmful or biased reasoning patterns — if such patterns improve next-token prediction on the training corpus, REINFORCE will reinforce them without any semantic filter
- Evaluation is limited to two benchmarks (GSM8K, CommonsenseQA) — no assessment of coding, multi-step planning, scientific reasoning, harder math, or out-of-distribution tasks, leaving the generality claim undertested
- Quiet-STaR has only been applied as continued pretraining — whether the reasoning bootstrapping works when training a model from scratch remains unknown, limiting understanding of whether the approach requires pre-existing language ability as scaffolding

## Bottlenecks

- Per-token rationale generation creates multiplicative compute overhead (sequence_length × thought_length × n_samples) that becomes intractable for long sequences or large models without dynamic gating — blocking practical deployment of self-taught reasoning
- No mechanism to predict thought utility before generating the thought — the mixing head that determines incorporation weight is computed post-thought, making pre-generation gating architecturally unavailable and wasting compute on low-value tokens
- REINFORCE variance for token-level rationale reward signals requires many samples per position to produce stable gradients — high variance compounds with the multiplicative cost of per-token generation, blocking sample-efficient self-supervised reasoning training

## Breakthroughs

- First demonstration of training language models to generate and leverage internal reasoning rationales from arbitrary unstructured internet text — without curated QA datasets, annotated reasoning traces, or task-specific fine-tuning

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gsm8k|GSM8K]]
- [[entities/openwebmath|OpenWebMath]]
- [[entities/quiet-star|Quiet-STaR]]
- [[entities/reinforce|REINFORCE]]
- [[entities/star|STaR]]
