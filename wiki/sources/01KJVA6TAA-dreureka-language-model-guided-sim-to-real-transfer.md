---
type: source
title: 'DrEureka: Language Model Guided Sim-To-Real Transfer'
source_id: 01KJVA6TAAEV91JT0VHM6N80F5
source_type: paper
authors:
- Yecheng Jason Ma
- William Liang
- Hung-Ju Wang
- Sam Wang
- Yuke Zhu
- Linxi Fan
- Osbert Bastani
- Dinesh Jayaraman
published_at: '2024-06-04 00:00:00'
theme_ids:
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DrEureka: Language Model Guided Sim-To-Real Transfer

**Authors:** Yecheng Jason Ma, William Liang, Hung-Ju Wang, Sam Wang, Yuke Zhu, Linxi Fan, Osbert Bastani, Dinesh Jayaraman
**Published:** 2024-06-04 00:00:00
**Type:** paper

## Analysis

# DrEureka: Language Model Guided Sim-To-Real Transfer
2024-06-04 · paper · Yecheng Jason Ma, William Liang, Hung-Ju Wang, Sam Wang, Yuke Zhu et al. (8 total)
https://arxiv.org/pdf/2406.01967

---

### Motivation & Prior Limitations
- Sim-to-real transfer for robot policies has traditionally required extensive manual design of both reward functions and domain randomization (DR) parameters, making the pipeline slow and human-labor intensive.
  - Prior LLM-based reward design systems such as Eureka were designed for simulation-only use and failed entirely in real-world deployment: plain Eureka-trained policies achieved 0.0 m/s forward velocity when transferred to a physical quadruped, because they do not include safety terms and are not trained with domain randomization.
  - Domain randomization configurations — which parameters to randomize and over what ranges — were typically chosen by human practitioners with domain expertise, despite evidence that these choices have large effects on downstream policy performance.
- Automatically optimizing both reward functions and DR parameters jointly is an intractable infinite-dimensional search problem, which prior automated DR methods (CEM, BayRn) sidestepped only by iteratively querying the real world, making them slow and potentially unsafe for novel tasks.
  - CEM and BayRn require 10–20 hours of iterative real-world evaluation versus DrEureka's 3 hours of parallel simulation, and intermediate unsafe policies must be deployed on the robot during those iterations.

---

### Proposed Approach
- DrEureka is a three-stage LLM-guided pipeline that sequentially synthesizes a safety-regularized reward function, constructs a Reward-Aware Physics Prior (RAPP) from simulation rollouts, and then uses the LLM to generate domain randomization configurations bounded by that prior — all without human intervention.
  - **Stage 1 (Reward design with safety instructions):** DrEureka builds on the Eureka reward design algorithm but augments the prompt with a safety instruction `lsafety` specifying stability, smoothness, and task-specific safety constraints. This allows the LLM to naturally balance the weighting and non-additive interactions of safety and task reward components, rather than post-hoc appending safety terms that can produce overly conservative behavior.
  - **Stage 2 (RAPP):** Given the initial policy trained with the safety-regularized reward, RAPP systematically evaluates that policy under each physics parameter varied independently across a wide search range, identifying the minimum and maximum "feasible" values — those under which the policy still meets a success criterion. This grounds the LLM's subsequent DR generation in policy-relevant and reward-consistent bounds rather than simulator-native extremes, which are typically too wide to support learning.
  - **Stage 3 (LLM-generated DR):** The LLM receives the RAPP bounds as context and zero-shot generates multiple DR configuration candidates, choosing both which parameters to randomize and their specific distributions within the RAPP range. Multiple DR configurations are trained in parallel and all real-world policies are evaluated, with both best and average performance reported. The LLM's physical reasoning (e.g., selecting lower restitution ranges "because we're not focusing on bouncing") produces more principled configurations than numerical black-box optimizers.
- DrEureka uses GPT-4 as its backbone and applies PPO (with teacher-student distillation for locomotion) as the RL algorithm, requiring only the simulator source code and a natural language task description as inputs.

---

### Results & Capabilities
- On quadruped forward locomotion (Unitree Go1), DrEureka's best policy achieves 1.83 m/s and 5.0 m traveled on a 5-meter track, outperforming the human-designed baseline by 34% in forward velocity and 20% in distance, while the average across 16 DrEureka DR samples (1.66 m/s, 4.64 m) still matches or beats the human baseline (1.32 m/s, 4.17 m).
  - Robustness across real-world terrains (artificial grass, robot wearing socks, outdoor sidewalk) is maintained, with DrEureka consistently matching or exceeding human-designed performance in all conditions.
- On dexterous in-hand cube rotation (LEAP hand, 16-DOF), DrEureka's best policy achieves 9.39 rad of rotation versus 3.24 rad for the human-designed baseline — approximately 3× more rotations within a 20-second window.
- DrEureka outperforms iterative real-world DR optimization baselines: CEM RAPP reaches 1.46 m/s in 10 hours, BayRn RAPP reaches 1.28 m/s in 20 hours, while DrEureka reaches 1.83 m/s (best) in 3 hours without any real-world interaction during training.
- On the novel "walking globe" task — a quadruped balancing and walking on an inflated yoga ball with no prior sim-to-real configuration — DrEureka produces a policy that balances for an average of 15.4 seconds in a lab setting and operates stably for over four minutes across outdoor terrains including grass, sidewalks, and wooden bridges, while also recovering from perturbations such as the ball being kicked or deflating.
  - This task is particularly notable because IsaacGym cannot faithfully model the deformable ball dynamics, yet the DrEureka-generated DR configuration is sufficient to bridge the sim-to-real gap.
- Ablation results confirm all three components are necessary: removing RAPP (No Prior, Uninformative Prior) causes policies that frequently trigger motor safety cutoffs (≈0 m/s); removing LLM sampling in favor of random sampling within RAPP degrades performance to 0.98 m/s; using the full RAPP range as DR (Prompt DR) forces over-exertion of hip torques and achieves only 1.43 m/s.

---

### Implications
- DrEureka demonstrates that the two hardest human bottlenecks in sim-to-real RL — reward engineering and domain randomization design — can both be automated by LLMs with physics common sense, suggesting that the remaining manual steps in robot skill acquisitio

## Key Claims

1. DrEureka can automatically construct suitable reward functions and domain randomization distributions for sim-to-real transfer, requiring only the physics simulation for the target task.
2. Typical sim-to-real approaches rely on manual design and tuning of both task reward functions and simulation physics parameters, making the process slow and human-labor intensive.
3. DrEureka-trained policies outperform human-designed configurations on quadruped locomotion by 34% in forward velocity and 20% in distance traveled across various real-world evaluation terrains.
4. DrEureka's best policy achieves nearly 300% more in-hand cube rotations than the human-developed policy within a fixed time period on dexterous manipulation.
5. A policy produced by reward-design algorithms alone (without safety consideration and domain randomization) is not effective for real-world deployment.
6. Without reward-aware physics priors, nearly all DrEureka domain randomization samples result in jerky, dangerous behavior that triggers motor protection faults.
7. LLM-generated domain randomization outperforms prior feedback-based optimization approaches (CEM and BayRn) in terms of final policy performance.
8. DrEureka has a wall-clock runtime of approximately 3 hours, compared to 10 and 20 hours for CEM and BayRn baselines respectively.
9. The choice of domain randomization parameter form and initial sampling distributions has a large effect on downstream policy performance.
10. Including safety instructions directly in the LLM reward generation prompt enables the model to naturally balance the weighting and non-additive interactions of all reward components, improving real-w

## Capabilities

- LLMs can automatically generate both reward functions and domain randomization configurations for sim-to-real robot training simultaneously, achieving competitive or superior performance to human-designed configurations without iterative manual design
- LLM-generated domain randomization configurations outperform iterative black-box optimization methods (CEM, BayRn) that use real-world feedback — running in 3 hours vs 10–20 hours while avoiding unsafe intermediate real-world deployments
- LLMs can solve novel robot tasks requiring sim-to-real transfer (quadruped yoga ball balancing) without any prior human-designed sim-to-real pipeline, producing policies stable for 4+ minutes across uncontrolled outdoor environments
- Safety-regularized reward generation via LLM instruction following — prompting LLMs with explicit safety instructions automatically produces reward functions that balance task performance and hardware safety without manual post-hoc safety term addition
- Reward-Aware Physics Prior (RAPP) mechanism identifies feasible simulation parameter ranges by evaluating initial policy under perturbed physics in parallel — grounding LLM domain randomization sampling and preventing infeasible configuration generation

## Limitations

- LLM-generated domain randomization without reward-aware physics priors causes near-complete failure — 15/16 policies produce dangerous motor-fault-triggering behaviour, revealing a hard performance cliff when RAPP grounding is removed
- Reward design without explicit safety instructions (plain Eureka) completely fails real-world deployment despite succeeding in simulation — achieving 0 m/s forward velocity in the real world
- DrEureka uses only low-dimensional proprioceptive state representations — no visual inputs — limiting applicability to tasks where visual cues are critical for navigation and interaction
- Domain randomization parameters are fixed once generated — no dynamic adjustment during training based on policy performance or real-world feedback, leaving performance gains from adaptive DR unrealised
- No systematic policy selection mechanism — all 16 DR-configured policies must be deployed and compared in the real world because simulation performance across different DR distributions is not directly comparable
- Physics simulation cannot faithfully model complex real-world dynamics such as deformable contact surfaces — the sim-to-real gap for non-rigid, soft-body, or fluid tasks cannot be bridged by domain randomisation alone
- DrEureka requires an existing physics simulator for the target task — it cannot operate in domains without available simulation environments, restricting application to well-modelled robotic systems
- Training 16 parallel policies per run to ensure at least one effective DR configuration is computationally expensive — the portfolio strategy scales the training cost linearly with the number of candidates because no simulation-based selection criterion exists
- Safety is enforced solely through natural language prompt instructions with no formal guarantees — the claim that LLMs 'naturally balance' reward component weighting is explicitly hypothesised, not proven
- DrEureka has only been validated on two low-cost robots (<$10K) with existing open-source simulators and RL infrastructure — generalization to novel platforms, high-DOF systems, or robots lacking simulator support is untested
- LLM physical knowledge priors (GPT-4) are necessary but only useful when grounded by RAPP — the method implicitly depends on GPT-4-class model capability and may degrade with weaker LLMs, though this is never tested

## Bottlenecks

- Manual iterative design of reward functions and domain randomization configurations requires expert robotics engineers per task, creating a human-labour ceiling on the rate at which new robot skills can be acquired via sim-to-real RL
- Absence of a simulation-based policy selection criterion blocks efficient identification of the best domain randomization configuration without deploying all candidate policies in the real world — a safety and cost barrier for novel or dangerous tasks
- Rigid-body physics simulation fidelity gap for non-rigid contact dynamics (deformable objects, fluid, soft-body) limits LLM-guided sim-to-real to tasks with well-modelled physics — a ceiling that domain randomization cannot compensate for

## Breakthroughs

- DrEureka demonstrates that LLMs can fully automate both reward design and domain randomization configuration for sim-to-real transfer — eliminating iterative human expert design while matching or exceeding its performance across diverse robotic platforms and novel tasks

## Themes

- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]

## Key Concepts

- [[entities/eureka|Eureka]]
- [[entities/gpt-4|GPT-4]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/domain-randomization|domain randomization]]
