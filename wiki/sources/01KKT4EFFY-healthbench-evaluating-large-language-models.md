---
type: source
title: 'HealthBench: Evaluating Large Language Models'
source_id: 01KKT4EFFYW0ATQW8DWTPNM697
source_type: paper
authors: []
published_at: '2025-05-13 00:00:00'
theme_ids:
- alignment_and_safety
- benchmark_design
- evaluation_and_benchmarks
- hallucination_and_reliability
- medical_and_biology_ai
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# HealthBench: Evaluating Large Language Models

**Authors:** 
**Published:** 2025-05-13 00:00:00
**Type:** paper

## Analysis

# HealthBench: Evaluating Large Language Models
2025-05-13 · paper
https://cdn.openai.com/pdf/bd7a39d5-9e9f-47b3-903c-8b847ca650c7/healthbench_paper.pdf

---

### Motivation & Prior Limitations
Existing health benchmarks failed on three critical dimensions — meaningfulness, trustworthiness, and saturation — making them poor proxies for real-world LLM performance in healthcare.
- Prior evaluations relied predominantly on multiple-choice medical exam questions or narrow clinical queries, which are misaligned with the open-ended, dynamic nature of real clinical workflows and patient interactions.
  - Benchmarks like USMLE-style exams are now saturated by frontier models (e.g., GPT-4 level), removing their ability to discriminate between current models or incentivize further progress.
- Most existing evaluations lacked rigorous validation against expert medical opinion, meaning scores were not reliable indicators of physician judgment.
  - Without grounding in expert consensus, it was unclear whether benchmark improvements translated to clinically meaningful gains.
- No prior benchmark adequately measured behavioral dimensions critical for safe deployment, such as uncertainty handling, emergency escalation, context-seeking, and expertise-tailored communication across diverse global settings.

---

### Proposed Approach
HealthBench is an open-source rubric-based benchmark comprising 5,000 realistic multi-turn health conversations graded against 48,562 unique, physician-written, conversation-specific rubric criteria spanning seven themes and five behavioral axes.
- Unlike prior benchmarks using fixed multiple-choice or short-answer formats, HealthBench evaluates open-ended model responses against rubrics that capture what a specific response to a specific conversation should include, penalize, or reward — enabling nuanced, scalable grading of free-text outputs.
  - Each rubric criterion is assigned a point value between −10 and 10, allowing both positive reward and explicit penalization of harmful behaviors (e.g., failing to escalate an emergency).
  - A model-based grader (GPT-4.1) scores responses criterion-by-criterion; the final per-example score is the sum of earned points divided by the maximum possible, clipped to [0, 1] overall.
- The physician cohort of 262 physicians across 26 specialties, 60 countries, and 49 languages was vetted through a multi-step quality process starting from 1,021 applicants, and physicians were compensated; 31 were subsequently removed for quality, with their annotations purged.
- Two benchmark variants extend coverage: HealthBench Consensus (3,671 examples with 34 theme-specific criteria validated by physician majority agreement, enabling meta-evaluation of grader trustworthiness) and HealthBench Hard (1,000 examples selected for difficulty against frontier models, with the current top score of 32%).
- Conversations were primarily synthetically generated using physician-designed prompt seeds and a language model pipeline, supplemented by physician red-teaming data and reformatted HealthSearchQA queries, and filtered for realism, self-consistency, and health relevance.

---

### Results & Capabilities
Recent frontier models have improved rapidly on HealthBench, with o3 scoring 60% overall compared to GPT-4o's 32% and GPT-3.5 Turbo's 16%, representing a 28% improvement among OpenAI's frontier models in recent months alone — a larger step than the entire GPT-3.5-to-GPT-4o generation gap.
- Smaller models have improved dramatically in cost-performance efficiency: GPT-4.1 nano outperforms GPT-4o (Aug 2024) while being 25× cheaper, and a clear Pareto frontier emerges among April 2025 models (o3, o4-mini, GPT-4.1).
- Among non-OpenAI models, Grok 3 and Gemini 2.5 Pro achieved strong performance markedly above Claude 3.7 Sonnet and Llama 4 Maverick.
- Performance varies substantially by theme: emergency referrals and expertise-tailored communication score highest, while context-seeking, health data tasks, and global health lag; completeness and context-awareness are the weakest behavioral axes across all models, though o3 shows outsized improvement on completeness.
- Reliability analysis using worst-at-k scoring reveals that o3 achieves more than double the worst-at-16 score of GPT-4o (Aug 2024), but o3's worst-at-16 score is still one-third lower than its mean score of 60%, indicating persistent variance on individual problems.
- Physician-written responses without AI assistance underperformed recent models, and physicians could improve Sep 2024 model responses (improving over the reference 56.2% vs. worsening 39.8% of the time) but could not improve Apr 2025 model responses (46.8% vs. 47.7%).
- Model-based grading with GPT-4.1 achieves physician-level agreement: it exceeds the average physician MF1 score in 5 of 7 themes, falls above the median physician in 6 of 7 themes, and is above the 33rd percentile in all 7 themes, with model-physician agreement comparable to physician-physician agreement (ranging roughly 55–75%).
- HealthBench Hard exposes a significant unsolved frontier: even o3 scores only 32% on the 1,000 hardest examples, many models score zero, and the axis breakdown reveals accuracy and completeness as primary failure dimensions.

---

### Implications
HealthBench establishes a shared, open standard for evaluating LLM safety and performance in healthcare that is resistant to near-term saturation, providing the research community with a credible, physician-validated signal for model development targeting real-world health benefit.
- The benchmark's stratification by theme and axis enables targeted diagnosis of model weaknesses — for instance, the finding that context-seeking behavior remains underdeveloped across all models has direct implications for safe deployment in ambiguous clinical scenarios where incomplete user information is the norm.
- The cost-performance frontier results suggest that within months, small, cheap models may be capable enough 

## Key Claims

1. HealthBench is an open-source benchmark consisting of 5,000 multi-turn conversations evaluated using rubrics created by 262 physicians across 26 specialties and 60 countries.
2. HealthBench evaluates 48,562 unique rubric criteria spanning seven health themes and five behavioral axes.
3. LLM performance on HealthBench has improved from GPT-3.5 Turbo scoring 16% to o3 scoring 60%, reflecting both steady early progress and more rapid recent improvements.
4. GPT-4.1 nano outperforms GPT-4o on HealthBench while being 25 times cheaper, demonstrating significant improvement in small model efficiency.
5. Existing health LLM evaluations are limited by reliance on multiple-choice exams, lack of validation against expert medical opinions, and benchmark saturation.
6. HealthBench Hard has a top score of only 32% among all evaluated frontier models, providing headroom for future model development.
7. Model-based grading with GPT-4.1 achieves physician-level agreement on HealthBench consensus criteria, with model-physician agreement comparable to physician-physician agreement.
8. Recent LLM models outperform unassisted physicians on HealthBench, and physicians could improve model responses from September 2024 models but not April 2025 models.
9. Model performance on HealthBench is lowest for context-seeking, health data tasks, and global health themes, while emergency referrals and expertise-tailored communication score highest.
10. Model performance on HealthBench is lower for completeness and context-awareness axes compared to accuracy, communication quality, and instruction following.

## Capabilities

- Frontier LLMs can respond to open-ended, multi-turn health conversations at 60% quality as measured by physician-written rubrics, a near-4x improvement over GPT-3.5 Turbo's 16% baseline
- Small, cheap LLMs now match or exceed the healthcare response quality of earlier frontier models — GPT-4.1 nano outperforms GPT-4o while costing 25x less
- Frontier LLMs produce higher-quality health responses than unassisted physicians on open-ended conversation tasks
- Models have reduced error rates on critical safety-relevant health behaviors (e.g., emergency referral) by over 4x compared to GPT-3.5 Turbo
- Model-based graders can evaluate open-ended medical responses with agreement rates matching inter-physician agreement, enabling scalable trustworthy automated health benchmarking
- Test-time compute scaling (extended reasoning) demonstrably improves healthcare response quality, particularly on completeness — suggesting reasoning models will continue to push the health performance frontier

## Limitations

- Models remain unreliable in worst-case health scenarios: o3's worst-at-16 score drops by one-third relative to its average score, meaning that across many independent samples there are still frequent severe failures
- Models systematically underperform on context-seeking behavior — failing to recognize when a user has not provided sufficient clinical information and not asking targeted clarifying questions
- Models perform poorly on completeness — responses frequently omit key clinical information, safety flags, or necessary context even when what they do include is accurate
- Global health adaptation remains a lagging capability — models struggle to tailor responses for low-resource settings, regional disease patterns, and non-Western clinical norms
- Even best frontier models score only 32% on HealthBench Hard, a curated subset of 1,000 difficult healthcare questions — a large fraction of complex real-world health queries remain unsolved
- Models do not appropriately calibrate uncertainty in health responses — they still express overconfidence on topics where evidence is weak or evolving
- HealthBench evaluates only single model responses to conversations, not multi-step clinical workflows — the benchmark does not measure whether AI actually improves patient health outcomes in real deployments
- Model-based evaluation exhibits length bias: models producing longer responses tend to score higher, partially conflating verbosity with quality
- Inter-physician agreement on ideal health AI responses is low (55-75%), revealing that there is no single ground truth for healthcare AI quality — any benchmark is measuring against a contested standard
- The majority of HealthBench conversations are synthetically generated, not drawn from real patient-LLM interactions — real-world performance may differ from benchmark scores due to distribution mismatch
- Health data task performance (structured clinical documentation, diagnosis codes, clinical notes) lags significantly behind emergency referral and communication tasks, risking propagation of errors through patient care
- Physicians given April 2025 model responses could not improve them — suggesting current models may be approaching a ceiling where domain expert post-editing is ineffective, yet models remain far from reliable

## Bottlenecks

- Absence of meaningful, trustworthy, and unsaturated benchmarks for healthcare AI has blocked reliable measurement of and incentives for genuine clinical capability improvement
- Proactive context-seeking in health interactions — models cannot reliably detect when they lack essential clinical information and solicit the most informative clarification from users
- Worst-case reliability in healthcare: models have high variance across samples, meaning any deployment risks exposing some users to severely low-quality or unsafe responses even when average performance is good
- Lack of real-world clinical outcome studies measuring whether AI health responses actually improve patient outcomes — without this, even high benchmark scores cannot justify broad clinical deployment

## Breakthroughs

- Frontier LLMs now demonstrably outperform unassisted physicians on open-ended health response quality, measured via physician-validated rubrics on 5,000 realistic conversations
- Model-based grading of open-ended medical responses now matches inter-physician agreement, validating automated evaluation as a credible substitute for expensive physician review at scale
- Small, cheap models (GPT-4.1 nano) now exceed the health response quality of earlier frontier models (GPT-4o) at 25x lower inference cost, collapsing the cost-performance frontier for healthcare AI

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]

## Key Concepts

- [[entities/healthbench|HealthBench]]
- [[entities/length-controlled-win-rate|Length-Controlled Win Rate]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
