---
type: source
title: Mitigating Overthinking through Reasoning Shaping
source_id: 01KJTDB22B2J5EEMW45RTB34JS
source_type: paper
authors:
- Feifan Song
- Shaohang Wei
- Bofei Gao
- Yejie Wang
- Wen Luo
- Wei Li
- Linli Yao
- Weimin Xiong
- Liang Chen
- Tianyu Liu
- Houfeng Wang
published_at: '2025-10-10 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# Mitigating Overthinking through Reasoning Shaping

**Authors:** Feifan Song, Shaohang Wei, Bofei Gao, Yejie Wang, Wen Luo, Wei Li, Linli Yao, Weimin Xiong, Liang Chen, Tianyu Liu, Houfeng Wang
**Published:** 2025-10-10 00:00:00
**Type:** paper

## Analysis

# Mitigating Overthinking through Reasoning Shaping
2025-10-10 · paper · Feifan Song, Shaohang Wei, Bofei Gao, Yejie Wang, Wen Luo et al. (11 total)
https://arxiv.org/pdf/2510.09535

---

### Motivation & Prior Limitations
Large Reasoning Models (LRMs) trained via Reinforcement Learning with Verifiable Reward (RLVR) exhibit "overthinking" — excessive, meandering reasoning trajectories that inflate decoding tokens and computational cost without proportional accuracy gains.
- Token-level length penalties (the standard remedy) reduce token consumption but significantly degrade task accuracy, because individual tokens are weakly correlated with sparse verifier rewards and cannot be meaningfully identified as redundant or essential.
  - LCPO and O1-Pruner, the prior baselines, apply token-ratio weighting factors to the verifiable reward; while they compress output length, they produce degenerate reasoning patterns dominated by large proportions of extremely short segments (79–91% of segments in the shortest cluster), indicating the model resorts to rapid, shallow iteration rather than genuine compression.
- Token-level supervision lacks the semantic granularity needed to distinguish meaningful reasoning steps from redundant hedging: removing arbitrary tokens breaks coherence, yet any token-level penalty treats all tokens uniformly regardless of their role in the reasoning trajectory.

---

### Proposed Approach
The paper proposes Group Relative Segment Penalization (GRSP), a step-level RLVR penalty that operates on reasoning segments (coherent reasoning steps) rather than individual tokens, and applies length-aware descending weights across segment-length clusters to shape the distribution of reasoning rather than simply shortening it.
- Segments are identified either via keyword-based boundary matching (default; fast but language-specific) or via local minima in token log-probabilities (language-agnostic; segment transitions correspond to lower model confidence about continuations).
- For each rollout group, GRSP computes a z-score of segment counts per response (requiring no task-specific threshold), then decomposes segments into length clusters and applies cluster-specific penalties with descending weights — shorter segments are penalized more heavily than longer ones.
  - This counter-intuitive design is motivated by an empirical finding: across DeepSeek-R1, QwQ-32B, DS-Qwen-Distill-32B, and DS-Qwen-Distill-14B, failed cases contain disproportionately more short segments relative to correct cases, and stronger/more-trained models show a flatter ratio of correct-to-failed segment counts across clusters (smaller slope), suggesting that a balanced segment-length distribution correlates with both performance and training stability.
  - By discouraging short segments and tolerating long ones, GRSP pushes the model toward deeper within-segment reasoning, reducing total step count and thus token overhead without collapsing the exploratory reasoning that drives accuracy gains.
- GRSP is a drop-in replacement for the scalar token-length penalty term in standard RLVR objectives (Reinforce, GRPO), requiring no architectural changes.

---

### Results & Capabilities
GRSP achieves the best combined accuracy and token efficiency among all compared methods on the hardest benchmark (Omni-MATH 500), with advantages that grow as task difficulty increases.
- Under GRPO on Qwen-2.5-14B-it*, GRSP reaches 43.80% accuracy on Omni-MATH 500 at 4,897 average tokens, versus 45.40% at 5,315 tokens for vanilla GRPO and 40.60% at 5,497 for O1-Pruner — superior token efficiency with only a modest accuracy gap relative to the unpenalized baseline.
- GRSP reduces average segment count from 26.66 (no penalty) to 21.07, while competing baselines balloon to 51.97 (O1-Pruner) and 142.12 (LCPO) segments, dominated by short fragments — confirming that GRSP compresses reasoning structurally rather than fragmenting it.
- GRSP stabilizes RL training: ascending weights (penalizing long segments more) cause an accuracy collapse during mid-training as the model over-optimizes for brevity; descending weights produce smooth, monotonic accuracy improvement alongside efficiency gains, showing accuracy and length optimization are not a zero-sum game.
- GRSP scales consistently across Qwen-2.5 7B, 14B, and 32B: accuracy impact is negligible (≤0.19% drop) while token reduction grows with model size, with the 32B model achieving the largest absolute token savings (-191.61 tokens on average).
- Confidence-based segmentation (log-probability minima) matches or slightly outperforms keyword-based segmentation, achieving 64.91% accuracy at 3,415 tokens versus 64.72% at 3,477 tokens, while generalizing across languages.

---

### Implications
The central finding — that supervision granularity is a critical design axis in RLVR, not merely a secondary implementation detail — suggests that many existing efficiency methods may be fundamentally limited by their token-level framing, and that step-level or segment-level RL objectives deserve systematic investigation across other reasoning tasks beyond math.
- The empirical link between segment-length distribution balance and model capability/training stability provides a new diagnostic lens for evaluating LRM training health, potentially informing early-stopping criteria or curriculum design in RL pipelines.
- Confidence-based segmentation (log-probability local minima) as a language-agnostic boundary detector is a reusable primitive that could plug into other reasoning analysis frameworks, monitoring tools, or structured decoding methods beyond RLVR.
- The finding that larger models are inherently more token-efficient under RL — and that GRSP's compression benefit scales with model size — suggests that the overthinking problem may be partially self-correcting at scale, but that algorithmic shaping still adds measurable value even for frontier-sized models.

---

### Remaining Limitations & Next Steps
T

## Key Claims

1. The granularity of supervision plays a crucial role in balancing efficiency and accuracy when mitigating overthinking in LRMs
2. Reasoning segments (steps) are more natural units for identifying redundancy than individual tokens, because each step carries a semantically coherent piece of thought
3. Identifying which individual tokens are redundant is difficult because most tokens cannot be directly associated with the sparse verifier reward
4. The quantity of reasoning segments is positively correlated with total token consumption in open-source LRMs
5. Failed reasoning cases in LRMs tend to contain more segments than passed cases across most length clusters
6. Stronger LRMs show a more balanced distribution of segment lengths across clusters (smaller variation in the passed/failed segment ratio), suggesting a link between model performance and segment distr
7. GRSP assigns descending penalty weights from shorter to longer segment clusters, penalizing short segments more heavily and applying weaker penalties to longer ones
8. GRSP achieves the best scores on both task performance and token efficiency under both GRPO and REINFORCE frameworks compared to LCPO and O1-Pruner baselines
9. GRSP produces an average of 21.07 reasoning segments versus 26.66 from models trained without penalty, confirming it effectively regulates segment count
10. Models trained with descending weights shift toward generating longer individual segments, which paradoxically leads to overall shorter response length by requiring fewer total steps

## Capabilities

- Group Relative Segment Penalization (GRSP) reduces LRM token consumption by supervising at reasoning-segment granularity rather than token level, achieving improved efficiency without proportional accuracy degradation, with greatest gains on harder problems
- Confidence-based segmentation using local minima in token log-probabilities identifies reasoning segment boundaries without language-specific keywords, achieving comparable or better accuracy-efficiency trade-offs than keyword matching
- Larger LRMs exhibit a natural tendency toward more token-efficient reasoning under identical RL training setups — accuracy improves and token consumption decreases with scale without explicit efficiency supervision
- GRSP applied during RLVR training reduces average reasoning segment count (from 26.66 to 21.07 segments per response) and total token overhead on hard problems while preserving accuracy, verified across 7B, 14B, and 32B model scales

## Limitations

- Token-level length penalties in RLVR cause training instability and accuracy collapse — once penalty dominates the verifiable reward, task accuracy drifts sharply downward and training collapses
- Identifying which individual tokens in LRM reasoning are redundant is fundamentally intractable — most tokens cannot be associated with sparse verifier reward signals, making token-level compression ambiguous
- Token-level penalties cause reasoning models to degenerate into rapidly iterating many short steps rather than genuinely compressing reasoning — paradoxically increasing segment count and worsening overthinking
- LRMs fundamentally rely on token-length scaling to solve harder problems — accuracy on difficult tasks is structurally coupled to generating longer responses, making aggressive compression harmful
- Keyword-based reasoning segmentation is language-specific and cannot generalize to non-English reasoning without manual keyword curation per target language
- GRSP has only been evaluated on mathematical reasoning benchmarks — effectiveness on non-mathematical or open-ended reasoning domains is entirely undemonstrated
- GRSP experiments were conducted exclusively on the Qwen-2.5 model family — generalization to other LRM architectures (e.g., DeepSeek-R1, Gemini, Llama) is unvalidated beyond passive observation of open-source model statistics
- Warm-up data derived from DeepSeek-R1 reasoning patterns induces overly long responses before RL begins, masking length-scaling effects and making GRSP harder to evaluate — SFT data provenance structurally constrains subsequent RL behavior
- The correlation between segment length distribution and LRM performance is empirically observed but mechanistically unexplained — the causal basis for why balanced segment distributions correlate with stronger models is unestablished
- Continued RL training to further validate GRSP's token compression benefits is computationally infeasible at academic research scale — results are incomplete by the authors' own admission

## Bottlenecks

- Token-level supervision granularity in RLVR is insufficient to stably balance reasoning efficiency and accuracy — weak correlation between token penalties and verifiable rewards causes accuracy collapse or Goodhart failures in length compression
- LRM inference cost scales super-linearly with problem difficulty — harder problems induce disproportionately longer reasoning chains under RL training, creating prohibitive inference costs at the capability frontier even with compression techniques

## Breakthroughs

- Segment-level supervision in RLVR (GRSP) demonstrates that the reasoning efficiency-accuracy tradeoff is not fundamental but an artifact of coarse token-level supervision — step-granularity penalties with descending length-aware weights achieve simultaneous efficiency gains and training stabilizatio

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/grpo|GRPO]]
- [[entities/large-reasoning-model-lrm|Large Reasoning Model (LRM)]]
- [[entities/numinamath|NuminaMATH]]
- [[entities/overthinking|Overthinking]]
- [[entities/reinforce|REINFORCE]]
- [[entities/test-time-scaling|Test-time Scaling]]
