---
type: source
title: Improving Interactive In-Context Learning from Natural Language Feedback
source_id: 01KJT1CPWRVXKQYVCG6CPW69WC
source_type: paper
authors:
- Martin Klissarov
- Jonathan Cook
- Diego Antognini
- Hao Sun
- Jingling Li
- Natasha Jaques
- Claudiu Musat
- Edward Grefenstette
published_at: '2026-02-17 00:00:00'
theme_ids:
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Improving Interactive In-Context Learning from Natural Language Feedback

**Authors:** Martin Klissarov, Jonathan Cook, Diego Antognini, Hao Sun, Jingling Li, Natasha Jaques, Claudiu Musat, Edward Grefenstette
**Published:** 2026-02-17 00:00:00
**Type:** paper

## Analysis

# Improving Interactive In-Context Learning from Natural Language Feedback
2026-02-17 · paper · Martin Klissarov, Jonathan Cook, Diego Antognini, Hao Sun, Jingling Li et al. (8 total)
https://arxiv.org/pdf/2602.16066v1

---

### Motivation & Prior Limitations
- Current LLM training paradigms rely on static corpora, which builds knowledge effectively but leaves models unable to adapt dynamically to corrective feedback within a conversation — a capability central to human collaborative learning.
  - Experiments on flagship models (Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite, GPT-5) across HardMath2, ARC-AGI, Codeforces, and BIG-Bench Extra Hard reveal that even the largest models show poor cumulative accuracy gains across feedback turns, demonstrating substantial headroom.
  - The bottleneck is not missing knowledge but the model's inability to acquire and integrate knowledge through interaction: users must resort to complex prompt engineering to elicit desired behaviors, and researchers must manually curate datasets when models fail.
- Standard single-turn RL (RLVR) on verifiable tasks improves single-turn accuracy but does not train models to utilize conversational feedback across turns, leaving multi-turn interactive learning capabilities essentially unchanged.
- Interactive in-context learning has been treated as an emergent property of scale rather than a trainable skill, meaning there is no principled method to directly improve it.

---

### Proposed Approach
- The paper introduces RL2F (Reinforcement Learning with Language Feedback), a framework that reframes interactive in-context learning as a distinct, trainable skill by converting single-turn verifiable problems into multi-turn didactic dialogues between a teacher and a student model optimized via RL.
  - Unlike distillation-based teacher-student frameworks that require a larger, more capable teacher model, RL2F exploits information asymmetry: the teacher and student can share the same base model, with the teacher conditioned on privileged information (e.g., ground-truth solution, unit test outputs) and prompted to guide without directly revealing the answer (this leakage occurs in less than 0.3% of cases under verified checks).
  - The student is modeled as a POMDP agent whose policy is optimized by sparse reward (correct solution = +1, else 0 at max turns T_max) over multi-turn trajectories; weight updates occur after full trajectories, improving the model's meta-learning ability — its capacity to learn from interactions — without requiring inner-loop gradient meta-gradients.
  - The method draws an explicit connection to black-box meta-learning (RL²): language feedback visible only after incorrect turns functions as an augmented reward observation, and the LLM implements an in-context RL algorithm whose weights are in turn optimized by outer-loop RL.
- For self-improvement, the model is trained on the full dialogue including the teacher's critique turns, treating the teacher as an environment to be world-modeled; at inference the model plays both teacher and student roles, generating self-critiques without access to privileged information.

---

### Results & Capabilities
- RL2F applied to Gemini 2.5 Flash (a thinking model) nearly closes the performance gap to Gemini 2.5 Pro on the challenging HardMath2 Advanced benchmark — a model one full tier larger — after fine-tuning on a private set of hard mathematics problems, demonstrating that multi-turn didactic training can substitute for roughly an order-of-magnitude increase in model size.
  - On HardMath2 Advanced at turn 3, RL2F Flash reaches ~0.62 cumulative accuracy vs. ~0.65 for Pro, compared to ~0.52 for the baseline Flash.
- Training exclusively on math interactions produces strong out-of-distribution generalization: RL2F boosts average performance by ~7% across ARC-AGI, Codeforces, and Linguini (BBEH) for Gemini 2.5 Flash, whereas single-turn RL yields outcomes statistically indistinguishable from the baseline on those same benchmarks.
- RL2F generalizes to 10 diverse general multi-turn agentic tasks (Poker, Wordle, Maze Navigation, Only Connect Wall, movie recommendations, etc.) with a ~5% average performance boost, outperforming both baseline and single-turn RL on 7 of 10 tasks despite no exposure to those domains during training.
  - Maze Navigation improves by +12.5% and Only Connect Wall by +19%, suggesting the learned capability is a domain-general cognitive skill.
- Qualitative analysis identifies in-context plasticity as the mechanism: RL2F-trained models use thinking traces to reason about teacher hints and revise answers, while baseline models repeat the same incorrect answer verbatim across turns, eventually abandoning thinking tokens entirely.
- Self-improvement (autodidact) mode — where the model predicts teacher critiques as an auxiliary world-modeling objective and then self-critiques at inference — outperforms even the didactic-interaction setting with a privileged teacher, demonstrating that internalizing the feedback loop builds a more robust internal evaluator than relying on external correction alone.

---

### Implications
- Treating interactive in-context learning as a trainable skill rather than an emergent property opens a scalable post-training pathway: any existing single-turn verifiable dataset can be repurposed into multi-turn didactic interactions at negligible synthesis cost, allowing the field to leverage its entire corpus of verifiable tasks for improving interactive capabilities.
- The result that a smaller model fine-tuned via RL2F can rival a much larger model reframes the capability-model-size relationship for interactive settings: interactive training efficiency may partially substitute for raw scale, with significant implications for deployment cost and accessibility.
- The in-context plasticity framing — borrowing the plasticity concept from RL and extending it to the in-context regime — introduces a new diagnostic lens

## Key Claims

1. Current flagship LLMs struggle to integrate corrective feedback on hard reasoning tasks, revealing significant headroom in frontier models' multi-turn reasoning abilities.
2. Interactive in-context learning from natural language feedback can be treated as a distinct, trainable skill rather than an emergent property of scale.
3. Generating high-quality corrective feedback on verifiable domains does not require a superior teacher model; information asymmetry (access to ground-truth solutions or unit test outputs) is sufficient
4. Gemini 2.5 Flash fine-tuned with RL2F on multi-turn didactic interactions nearly reaches the multi-turn performance of Gemini 2.5 Pro on the HardMath2 dataset, bridging a full model-tier gap.
5. RL2F trained exclusively on math problems achieves ~7% average performance improvement over baseline on three out-of-distribution multi-turn benchmarks (ARC-AGI, Codeforces, Linguini), while single-tu
6. RL2F continuously widens the performance gap over baselines as the number of interaction turns increases, whereas standard single-turn RL and SFT only match single-turn improvements.
7. Baseline LLMs lacking RL2F training tend to repeat their initial incorrect answers when given corrective feedback, eventually ceasing to use thinking tokens entirely — a phenomenon the authors attribu
8. In-context plasticity — the ability to change predictions in response to new in-context information — is a phenomenon analogous to weight-level plasticity in RL but has not previously been studied for
9. Training a model on full multi-turn didactic dialogues including the teacher's critiques — as a world-modeling objective — enables the model to self-correct without an external teacher at inference ti
10. Self-improvement via world-modeling significantly outperforms didactic interaction training alone on Omni MATH when evaluated at inference time without a teacher.

## Capabilities

- LLMs can be trained via RL on multi-turn didactic interactions (RL2F) to interactively learn from natural language corrective feedback, treating it as a distinct trainable skill rather than an emergent property of scale
- A smaller thinking model (Gemini 2.5 Flash) fine-tuned via RL2F on multi-turn didactic math interactions nearly matches a tier-higher model (Gemini 2.5 Pro) on challenging math reasoning benchmarks
- Interactive reasoning capabilities trained exclusively on math problems transfer robustly to diverse out-of-distribution domains — ARC-AGI, competitive coding, logic puzzles, game playing (Poker, Wordle), maze navigation — achieving 5–7% average performance gains
- Models trained to predict teacher critiques during didactic interactions develop self-correction capability that outperforms externally-guided models at inference time, enabling self-improvement without an external teacher
- High-quality corrective feedback for teacher-student training can be generated using information asymmetry alone (access to ground truth), without requiring a larger or more capable teacher model — the teacher and student can be the same base model

## Limitations

- Current flagship LLMs (Gemini 2.5 Pro, Flash, Flash-Lite, GPT-5) show severely limited ability to integrate corrective language feedback across multiple turns on hard reasoning tasks — accuracy improves only marginally despite receiving precise corrections
- Without RL2F training, LLMs exhibit near-zero in-context plasticity: they repeat identical incorrect answers across turns regardless of corrective feedback, stop using thinking tokens, and fail to integrate even mathematically precise corrections
- Even thinking models with internal chain-of-thought revision do not substitute for explicit interactive feedback training — internal thinking traces do not confer the same multi-turn adaptation capability as RL2F training on external feedback
- RL2F improves transient within-context adaptation but cannot consolidate these gains into persistent model knowledge — improvements are ephemeral and lost at the end of each conversation context
- Standard single-turn RL (RLVR/RLMF) fails to improve multi-turn interactive reasoning: it barely improves upon baseline at turns 2+ and shows no out-of-distribution generalization to interactive tasks despite improving single-turn accuracy
- RL2F training requires verifiable tasks with objective ground-truth measures — the framework has no demonstrated path to extend to open-ended, non-verifiable domains where automated reward signals are unavailable
- Enhanced adaptability to feedback risks incentivizing sycophantic behavior — models trained to update based on user corrections may shift toward agreement regardless of correctness
- RL2F training uses a static problem set with no adaptive curriculum — the teacher plays no role in selecting or sequencing problems based on observed student mistakes, leaving significant efficiency gains on the table
- RL2F performance gains are uneven across out-of-distribution tasks: it underperforms single-turn RL or baseline on 3 of 10 diverse tasks (Aider Polyglot Code Edit, Circuit Decoding, Word Chaining), indicating transfer is not universal
- The didactic teacher-student setup is evaluated only in cooperative settings with fully aligned goals; real-world interactive learning involves mixed-motive and adversarial scenarios that are entirely unaddressed

## Bottlenecks

- Absence of in-context plasticity in current LLMs blocks efficient user-guided model adaptation — the bottleneck is not knowledge availability but the model's capacity to acquire it through interaction, forcing researchers to manually curate failures instead
- Absence of mechanisms to consolidate in-context learning gains into persistent model weights blocks robust continual learning — models that adapt within a context cannot permanentize what they have learned

## Breakthroughs

- RL2F demonstrates that interactive in-context learning from natural language feedback is a distinct, trainable skill — enabling a smaller model (Gemini 2.5 Flash) to nearly match a tier-higher flagship (Gemini 2.5 Pro) on hard math, with strong cross-domain transfer and self-improvement capability t

## Themes

- [[themes/continual_learning|continual_learning]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/in_context_and_meta_learning|in_context_and_meta_learning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
