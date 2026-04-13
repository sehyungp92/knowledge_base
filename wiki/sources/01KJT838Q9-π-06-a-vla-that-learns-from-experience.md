---
type: source
title: '$π^{*}_{0.6}$: a VLA That Learns From Experience'
source_id: 01KJT838Q90YE4TNFW85BGDGQB
source_type: paper
authors:
- Physical Intelligence
- Ali Amin
- Raichelle Aniceto
- Ashwin Balakrishna
- Kevin Black
- Ken Conley
- Grace Connors
- James Darpinian
- Karan Dhabalia
- Jared DiCarlo
- Danny Driess
- Michael Equi
- Adnan Esmail
- Yunhao Fang
- Chelsea Finn
- Catherine Glossop
- Thomas Godden
- Ivan Goryachev
- Lachy Groom
- Hunter Hancock
- Karol Hausman
- Gashon Hussein
- Brian Ichter
- Szymon Jakubczak
- Rowan Jen
- Tim Jones
- Ben Katz
- Liyiming Ke
- Chandra Kuchi
- Marinda Lamb
- Devin LeBlanc
- Sergey Levine
- Adrian Li-Bell
- Yao Lu
- Vishnu Mano
- Mohith Mothukuri
- Suraj Nair
- Karl Pertsch
- Allen Z. Ren
- Charvi Sharma
- Lucy Xiaoyang Shi
- Laura Smith
- Jost Tobias Springenberg
- Kyle Stachowicz
- Will Stoeckle
- Alex Swerdlow
- James Tanner
- Marcel Torne
- Quan Vuong
- Anna Walling
- Haohuan Wang
- Blake Williams
- Sukwon Yoo
- Lili Yu
- Ury Zhilinsky
- Zhiyuan Zhou
published_at: '2025-11-18 00:00:00'
theme_ids:
- policy_optimization
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# $π^{*}_{0.6}$: a VLA That Learns From Experience

**Authors:** Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, Zhiyuan Zhou
**Published:** 2025-11-18 00:00:00
**Type:** paper

## Analysis

# $\pi^{*}_{0.6}$: a VLA That Learns From Experience
2025-11-18 · paper · Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black et al. (56 total)
https://arxiv.org/pdf/2511.14759

---

### Motivation & Prior Limitations
- Vision-language-action (VLA) models trained purely on imitation learning suffer from compounding errors and are bounded by the quality of the demonstration data, meaning they cannot surpass the teleoperation ceiling no matter how much offline data is added.
  - Standard behavior cloning has no mechanism to correct the specific mistakes the deployed policy makes; errors accumulate over a horizon in ways that demonstrations never cover.
- Existing approaches to RL fine-tuning of VLAs — primarily PPO and REINFORCE variants — are difficult to scale to large, flow-matching-based architectures because those architectures do not readily expose a tractable log-likelihood, making policy gradient objectives unwieldy.
  - Methods that work around this by training only a residual policy, fine-tuning only the action head, or selecting among VLA proposals avoid the log-likelihood problem but cannot improve the full model end-to-end.
- Prior end-to-end RL methods for VLAs have been evaluated on relatively simple tasks (moving a bowl, unfolding a mat, pushing objects) and rely on discrete or Gaussian action distributions, leaving open the question of whether RL can improve large generalist VLAs on dexterous, long-horizon tasks involving deformable objects or liquids.
- No prior work had established a unified recipe that folds together offline demonstrations, on-policy autonomous rollouts, and online human corrective interventions into a single, iterated RL training loop for a large generalist VLA.

---

### Proposed Approach
- RECAP (RL with Experience and Corrections via Advantage-conditioned Policies) is an iterated offline RL framework that trains a VLA to condition on a binarized advantage indicator, enabling policy improvement from any mix of demonstrations, autonomous rollouts, and expert corrections without requiring on-policy policy gradient objectives.
  - The core insight, derived from CFGRL, is that the KL-regularized optimal policy can be written as the reference policy conditioned on an improvement indicator $I$, so training the policy to represent both $\pi_\theta(a|o,\ell)$ and $\pi_\theta(a|I,o,\ell)$ is sufficient — analogous to classifier-free guidance in diffusion models.
  - In practice, the advantage indicator is binarized via a task-dependent threshold $\epsilon_\ell$ and injected as text ("Advantage: positive" / "Advantage: negative") into the VLA prefix, keeping the training objective a straightforward supervised cross-entropy plus flow-matching loss with no policy gradient terms.
- The value function is a multi-task distributional critic $p_\phi(V|o_t, \ell)$ over 201 discretized bins, initialized from a smaller pre-trained VLM and trained with Monte Carlo cross-entropy regression on empirical returns; it predicts expected steps to success, normalized to $(-1, 0)$.
  - This Monte Carlo on-policy estimator is explicitly acknowledged as less optimal than off-policy Q-function methods but was chosen for simplicity and stability at scale; the authors note off-policy extensions are future work.
- The model instantiating RECAP, called $\pi^*_{0.6}$, builds on $\pi_{0.6}$ (Gemma 3 4B backbone, 860M-parameter flow-matching action expert, Knowledge Insulation training, FAST action tokenizer) and differs from the base model only in the additional advantage-indicator input slot; both discrete and continuous (flow-matching) action heads are jointly trained.
- Human expert interventions during autonomous rollouts are incorporated by forcing $I_t = \text{True}$ for all corrected actions, under the assumption that teleoperated corrections are always improvements; this provides a dense corrective signal without requiring explicit reward labeling of intervention steps.

---

### Results & Capabilities
- On the hardest evaluated tasks, RECAP more than doubles task throughput and roughly halves the task failure rate compared to the imitation-learning baseline, demonstrating that iterated on-robot RL produces gains beyond what offline pre-training alone can achieve.
  - The laundry-folding specialist ran for over two hours in a new home without interruption, generalizing to novel clothing items not seen in training.
  - The espresso-making specialist ran continuously for 13 hours, handling pouring liquids and multi-stage sequencing with a professional machine.
  - The box-assembly specialist reliably handled flattened, bent, and stuck-together boxes at factory-grade packaging quality.
- Advantage conditioning significantly outperforms policy gradient-based extraction (the natural alternative for flow-matching VLAs), as shown in ablation comparisons within the paper, validating the core technical design choice.
- The value function produces qualitatively sensible estimates: it correctly identifies mid-episode mistakes (e.g., an arm swing that crumples a folded shirt) as drops in predicted return and tracks recovery in successful episodes, confirming it carries meaningful signal for policy conditioning.

---

### Implications
- RECAP establishes the first general-purpose RL recipe that demonstrably scales to large, flow-matching VLAs and complex real-world manipulation, suggesting that the "practice makes perfect" paradigm previously limited to simpler policies can now be applied to generalist foundation models for robotics.
- The advantage-conditioning strategy decouples policy improvement from the architectural constraints of policy gradient methods, which may prove important for the broader class of diffusion- and flow-based generative action models that are increasingly dominant in robotics.
- The ability to incorporate sparse terminal rewards plus human interventions within a unified offline RL framework lowers the infrastructure cost of real-world

## Key Claims

1. RECAP more than doubles task throughput on some of the hardest robotic manipulation tasks
2. RECAP roughly halves the task failure rate compared to baseline VLA performance
3. π*0.6 trained with RECAP can fold laundry in real homes with high reliability
4. π*0.6 can make espresso drinks on a professional espresso machine for 13 hours straight without interruption
5. Policies trained with imitation learning suffer from compounding errors and can at best only be as performant as the demonstration data
6. Applying PPO directly to VLA fine-tuning yields approaches that are difficult to extend to real-world RL in an efficient and scalable fashion
7. RECAP is the first demonstration that a general-purpose RL recipe with human reward feedback and interventions can significantly improve both robustness and throughput of VLA models
8. RECAP uses a Monte Carlo estimator for the value function rather than a classic off-policy Q-function estimator
9. The Monte Carlo value estimator is less optimal than an off-policy Q-function estimator but is simpler and more reliable in practice
10. Policy gradient methods are difficult to apply to flow matching models because they do not readily provide a tractable log-likelihood

## Capabilities

- VLA models can self-improve through iterative real-world RL deployment via advantage-conditioned offline RL (RECAP), incorporating demonstrations, autonomous rollouts, and expert teleoperated corrections into a unified training loop
- Generalist VLA (π*0.6) trained with RECAP achieves sustained autonomous operation in real environments — 13 hours continuous espresso preparation, 2+ hours laundry folding of novel items in an unseen home, box assembly for live factory packaging
- Advantage conditioning enables end-to-end offline RL training of large flow-matching VLA models by conditioning on a binarized improvement indicator, circumventing the intractable log-likelihood problem that blocks policy gradient methods
- Multi-task language-conditioned distributional value function — trained on a VLM backbone — can accurately detect manipulation failures and predict progress-to-completion, enabling advantage estimation across diverse long-horizon tasks

## Limitations

- Monte Carlo value estimation used in RECAP is acknowledged as less optimal than off-policy Q-function estimators — limiting value accuracy and potentially capping performance gains from the RL improvement loop
- RECAP requires human teleoperated expert interventions during autonomous execution — it is not a fully autonomous self-improvement loop, and the human supervision cost is never quantified
- The method assumes human expert corrections are always optimal actions — this assumption will fail when experts make suboptimal or inconsistent corrections, with no mechanism to detect or handle degraded supervision quality
- Policy gradient methods (PPO, REINFORCE, reparameterized gradients) are fundamentally difficult to apply to flow-matching and diffusion VLA models due to intractable log-likelihoods, blocking the most widely-used RL approaches for modern VLA architectures
- Reward signals in real-world robot RL are sparse (binary task outcome labels) and stochastic, providing no intermediate credit assignment signal across long-horizon manipulation sequences with many sub-steps
- RECAP requires initial task demonstrations for each downstream skill before RL improvement — it cannot bootstrap from purely autonomous experience, maintaining the demonstration bottleneck for each new task
- Evaluation is limited to three structured task categories (laundry, espresso, box assembly) in specific real environments — generalization to arbitrary household tasks or uncontrolled environments is entirely undemonstrated
- No discussion of safety mechanisms, failure containment, or injury/property risks during 13-hour autonomous operation in real homes — safety for unsupervised long-duration deployment is conspicuously absent from the paper
- The Markovian state assumption — that current observations constitute valid RL states — is acknowledged as a known theoretical simplification that does not hold in general, undermining formal guarantees of the RL framework for history-dependent tasks
- Weighted regression RL methods (AWR) for VLAs discard or heavily downweight suboptimal trajectory data, wasting potentially informative failure trajectories — a limitation of prior approaches the field is only now moving past

## Bottlenecks

- Standard policy gradient RL methods (PPO, REINFORCE) are incompatible with flow-matching and diffusion-based VLA action distributions due to intractable log-likelihoods, blocking direct RL optimization of the current frontier of generative robotic action models
- Real-world reward specification for dexterous manipulation is ambiguous and stochastic, requiring significant per-task engineering effort to obtain reliable training signal — a practical blocker for scalable, automated robot RL pipelines

## Breakthroughs

- RECAP demonstrates the first general-purpose offline RL recipe that significantly and reliably improves robustness and throughput of large flow-matching VLA models using heterogeneous real-world data — more than doubling throughput and halving failure rates on hard tasks

## Themes

- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/vision_language_action_models|vision_language_action_models]]

## Key Concepts

- [[entities/action-expert|Action expert]]
- [[entities/flow-matching|Flow Matching]]
- [[entities/gemma-3|Gemma 3]]
