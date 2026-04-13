---
type: source
title: How Hugging Face Is Using E2B to Replicate DeepSeek-R1 — E2B Blog
source_id: 01KJSVF89AC5SD4TVRMZP07V8E
source_type: article
authors: []
published_at: None
theme_ids:
- ai_market_dynamics
- code_and_software_ai
- code_generation
- model_commoditization_and_open_source
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# How Hugging Face Is Using E2B to Replicate DeepSeek-R1 — E2B Blog

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# How Hugging Face Is Using E2B to Replicate DeepSeek-R1 — E2B Blog
article
https://e2b.dev/blog/how-hugging-face-is-using-e2b-to-replicate-deepseek-r1

---

## Briefing

**Hugging Face's Open R1 project is replicating DeepSeek-R1's training pipeline using reinforcement learning with verifiable rewards (RLVR), and the key infrastructure problem it had to solve was how to safely and cheaply execute hundreds of LLM-generated code snippets per training step as reward signals. The answer — E2B cloud sandboxes — reveals an underappreciated bottleneck in scaling code-execution-grounded RL: secure, fast, and cheap sandboxing is a genuine infrastructure prerequisite, not an afterthought.**

### Key Takeaways
1. **RLVR is the core mechanism behind DeepSeek-R1's reasoning** — the model receives binary rewards for correct answers, and maximizing these across training produces robust reasoning that generalizes to public benchmarks.
2. **Code execution rewards require running untrusted code at scale** — for competitive programming domains, the only way to verify correctness is to actually run the LLM's generated code against hidden test cases.
3. **Local code execution is a security non-starter** — LLM-generated code can corrupt filesystems or execute destructive commands; sandboxing is not optional.
4. **E2B's 150-170ms VM startup time is the critical performance spec** — GPU idle time during reward computation is a real training cost, so sandbox latency directly impacts RL efficiency.
5. **A full training run costs only a few dollars of E2B compute** — this makes sandboxed code execution economically viable as a reward signal at current RL training scales.
6. **Open R1 launches hundreds of sandboxes per training step** — async parallel execution via `asyncio.gather` is the pattern that makes this feasible.
7. **Multi-language support unlocks broader reasoning domains** — Python, JavaScript, and C++ are live; Rust and Lean4 are planned, with Lean4 being particularly significant for formal verification.
8. **Sandbox persistence (headless Jupyter) is a required feature, not a nice-to-have** — RL reward evaluation needs to reference previously defined state within a single evaluation episode.
9. **The current string-matching validator is an acknowledged limitation** — exact stdout comparison is a proxy for correctness, not a proper semantic validator; this is an open TODO in the codebase.
10. **The entire integration took only a few hours** — the practical barrier to adopting sandboxed code execution in RL pipelines is lower than expected.
11. **Hugging Face plans to scale this pipeline to OlympicCoder** — signaling intent to use code execution feedback as a primary training signal for frontier coding models.

---

### Why Code Execution is the Hard Problem in Verifiable Reward RL

- For RLVR to work, rewards must be computable without human annotation, relying entirely on automated verification.
  - **Math is the easy case**: string parsing with libraries like Math-Verify can compare a model's numerical answer to ground truth without execution.
  - **Competitive programming is the hard case**: there is no way to verify a code solution's correctness without actually running it against the hidden test cases — the program must execute and produce output.
    - This creates a fundamental asymmetry: math RLVR is cheap and safe; code RLVR requires infrastructure.
- The security problem is not hypothetical — LLMs may generate programs that perform destructive file system operations (`rm -rf`), network operations, or privilege escalation.
  - **Running LLM code locally is categorically unsafe** in a training loop where thousands of programs are executed without human review.
- The reward signal itself is a success rate: the fraction of test cases passed out of the total, returning a continuous scalar in [0, 1] rather than a binary reward.
  - This provides a richer gradient signal than binary pass/fail, allowing RL to distinguish partial solutions from complete failures.

---

### The Open R1 Reward Pipeline Architecture

- The `code_reward` function is the integration point between the RL training loop and E2B.
  - It accepts a batch of model completions and `verification_info` (test cases), extracts code from each completion, and dispatches parallel evaluation.
  - Each code snippet is wrapped in a standardized evaluation script template that handles subprocess execution, timeout enforcement (5 seconds per test case), and per-case pass/fail tallying.
- **The evaluation script runs inside the sandbox, not the host** — it uses `subprocess.run(["python3", "-c", code], ...)` internally, so even the evaluation logic is isolated.
  - This means the sandbox is running Python that itself spawns Python subprocesses — a clean double-isolation pattern.
- The async execution model is essential for throughput.
  - A single `AsyncSandbox` instance is created, then all scripts are dispatched concurrently via `asyncio.gather`, and the sandbox is killed after all results return.
  - This avoids per-completion sandbox startup overhead while maintaining isolation.
- **Current validator limitation**: the comparison between actual and expected output is pure line-by-line exact string matching.
  - The codebase explicitly marks this as a TODO, acknowledging that a proper semantic validator is needed — floating point output, whitespace differences, or multiple valid output formats would all cause false failures.

---

### E2B Sandbox Technical Properties Relevant to RL Training

- **Security via Firecracker microVMs**: E2B uses AWS's Firecracker, a production-hardened microVM monitor originally designed for AWS Lambda and Fargate, to create fully isolated VM instances per sandbox.
  - This is a meaningful security boundary — not just container-level isolation, but hypervisor-level isolation.
- **Startup latency of 150-170ms** is the key performance specification for RL use cases.
  - In a training loop, the GPU sits idle while wa

## Key Claims

1. DeepSeek-R1 demonstrated that maximising verifiable rewards with reinforcement learning enables LLMs to obtain robust reasoning capabilities that translate into high accuracy on public benchmarks.
2. Reinforcement learning with verifiable rewards trains an LLM using binary rewards based on whether it produces correct answers to problems checkable against ground truth.
3. For mathematics, verifying LLM output correctness can be achieved by parsing strings with libraries like Math-Verify.
4. For competitive programming domains, the reward is obtained by executing LLM-generated code and comparing results against expected outcomes from test cases.
5. Executing LLM-generated code locally poses serious security risks, including potential corruption of the host system.
6. Hugging Face uses E2B Sandboxes as the reward function execution environment for code during Open R1 training, targeting competitive programming competitions like CodeForces.
7. The Open R1 code reward function returns the overall success rate across test cases as the final reward signal.
8. The current Open R1 reward validator uses exact string matching per line of stdout to compare LLM output against ground truth, which is acknowledged as a limitation.
9. E2B uses Firecracker microVMs by AWS to create isolated execution environments, providing security for running LLM-generated code.
10. E2B sandbox startup latency is approximately 150-170 milliseconds, which is critical for minimising GPU idle time during reinforcement learning training.

## Capabilities

- Open-source RLVR training pipeline for code reasoning using sandboxed execution of LLM-generated code against competitive programming test cases, enabling safe and cost-effective reward computation at scale
- Parallel execution of hundreds of isolated code evaluation sandboxes per RL training step with ~150–170ms startup latency, minimising GPU idle time during reward computation in RLVR pipelines

## Limitations

- Code output validation in RLVR reward functions uses exact string matching rather than semantic correctness, causing false negatives for programs that produce equivalent but differently formatted output and injecting noise into the reward signal
- Hard 5-second per-test-case execution timeout structurally excludes computationally intensive problems from the RLVR training distribution, artificially narrowing the range of code reasoning the model can learn
- RLVR code rewards are structurally restricted to competitive programming format (deterministic test case I/O), preventing training on the broader software engineering task distribution that lacks clean ground-truth test suites
- Code RLVR training evaluates only final submissions with no reward signal for runtime errors or iterative debugging — failed executions are silently discarded, wasting informative signal about why solutions fail
- Language support for RLVR code execution is restricted; Rust and Lean4 — critical for systems programming and formal verification reward signals — are not yet available, limiting the domains where code reasoning can be trained
- Dependency on an external paid sandbox service (E2B) for reward computation introduces operational fragility and per-call cost into the RL training loop, creating a ceiling on how cheaply or reliably the pipeline can be scaled

## Bottlenecks

- Absence of robust semantic validators for code output comparison forces reliance on exact string matching, injecting systematic reward noise that degrades training signal quality for code reasoning models
- RLVR training for code reasoning is structurally confined to problems with ground-truth test suites (competitive programming), blocking generalisation of the training signal to the broader software engineering task distribution

## Breakthroughs

- Open R1 demonstrates that the DeepSeek-R1 RLVR code execution training pipeline can be replicated by open-source teams at negligible infrastructure cost (~few dollars per run) using commodity sandbox services, removing the proprietary infrastructure barrier to code-based RL training

## Themes

- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
