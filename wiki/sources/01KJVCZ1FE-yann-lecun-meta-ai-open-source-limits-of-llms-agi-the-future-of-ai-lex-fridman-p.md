---
type: source
title: 'Yann Lecun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI |
  Lex Fridman Podcast #416'
source_id: 01KJVCZ1FE4PR5WMQSCFNE4T9X
source_type: video
authors: []
published_at: '2024-03-07 00:00:00'
theme_ids:
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- latent_reasoning
- model_commoditization_and_open_source
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Yann Lecun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI | Lex Fridman Podcast #416

**Authors:** 
**Published:** 2024-03-07 00:00:00
**Type:** video

## Analysis

Limits of LLMs

- Autoregressive LLMs may not present the way to make progress towards superhuman intelligence\.
- There is a number of characteristics of intelligent behaviour\. The 4 essential characteristics of intelligent systems or entities are:
	- The capacity to understand the physical world
	- The ability to remember and retrieve things, i\.e\., persistent memory
	- The ability to reason
	- The ability to plan
- LLMs can do none of the above, or can only do them in a very primitive way\. They don’t really understand the physical world, they don’t really have persistent memory, they can’t really reason and they certainly can’t plan\. And without having the possibility of doing these things, expectations for the system to become intelligent may be misplaced\. 
- That is not to say that autoregressive LLMs are not useful\. They are certainly useful and it is possible to build a whole ecosystem of applications around them, but they are missing essential components in order to achieve human\-level intelligence\. 
- LLMs are trained on enormous amounts of texts, essentially the entirety of all publicly available texts on the internet, typically on the order of 1013 tokens\. Each token is typically 2 bytes, so that’s 2x1013 bytes as training data, which would take a person 170,000 years just to read through this at 8 hours a day\. This seems like an enormous amount of knowledge that these systems can accumulate, but for a 4\-year\-old that has been awake for ~16,000 hours, the amount of information that has reached the visual cortex of that child is equivalent to ~1015 bytes\. 
	- This implies that we see a lot more information through sensory input than we do through language, and that despite our intuition, most of what we learn is through observation and interaction with the real world, not through language\. Everything that we learn in the first few years of life, and certainly everything that animals learn has nothing to do with language\.
- There is a debate among philosophers and also cognitive scientists whether intelligence needs to be grounded in some reality\. For those that believe this to be true, the environment is just much richer than what you can express in language, as language is a very approximate representation of percepts and/or mental models\.
	- There are a lot of tasks that we accomplish where we manipulate a mental model of the situation at hand, and that <a id="_Hlk181655671"></a>has nothing to do with language\. When we build something, accomplish a task etc\., we plan or action sequences by essentially imagining the outcome of a sequence of actions and that requires mental models that do not have much to do with language\. 
		- Arguably most of our knowledge is derived from that interaction with the physical world\. 
- <a id="_Hlk181657581"></a>It is hard to represent all the complexities that we take for granted in the real world that we do not require intelligence\. This is the Moravec paradox, which describes how it seems to be easy for computers to do high\-level complex tasks, such as playing chess and solving integrals, whereas the things we take for granted that we do every day, like learning to drive a car or grabbing an object, computers cannot do\.
- You can use all kinds of tricks to get an LLM to digest visual representations of images or video or audio\. A classical way of doing this is you train a vision system in some way that will turn any image into a high\-level representation, essentially a list of tokens, and then feed that to the LLM in addition to the text\. There are LLMs that have some vision extension, but they are still hacks as they are not being trained end to end to understand the world\. For example, they’re not trained with video\.
	- This will not be possible with the type of LLMs that are being used today\.
- The main reason is the way LLMs are trained using text, where some of the words in the text are masked and the models are trained to predict the missing words\. And if the neural net is built in a particular way so that it can only look at words that are to the left of the one it’s trying to predict, then it becomes a system that basically is trying to predict the next word \(or tokens\) in a text by producing a probability distribution of all the possible words in a dictionary\. The word sampled from the distribution is then used as a input, allowing the system to predict the second word\. 
	- This is called autoregressive prediction, where it is easy to handle the uncertainty in the prediction because there is only a finite number of possible words in the dictionary, and you can just compute a distribution over them, and the system can pick a word from that distribution\.
- <a id="_Hlk181657915"></a>In reality there is a more abstract level of representation in which we do most of our thinking, and if the output is uttered words, we plan what we’re going to say before we say it\. LLMs don’t do that, they just spit out one token after the other without planning the answer\. They just produce one word after the other in an almost instinctive manner\. An LLM doesn’t think about its answer, but retrieves it because it has accumulated a lot of knowledge\.
- <a id="_Hlk181997727"></a><a id="_Hlk181658089"></a>The fundamental question is can you build a world model using language, something that understands why the world is evolving the way it is and something that can predict how the world is going to evolve as a consequence of an action you might take\. The state of the world does not need to represent everything about the world, it just needs to represent enough that’s relevant for the planning of an action\.
	- It may be possible to build a world model by prediction, but not by predicting words because there’s just not enough information in language\.
- Generative models are not well suited for building world models\. For instance, it is difficult to train a model on video to predict what’s going to happen, which requires

## Key Claims

1. AI will cause a gradual shift across professions rather than mass unemployment.
2. The most in-demand professions 10–15 years from now cannot be predicted today.
3. The emergence of the mobile app developer profession was unpredictable before smartphones were invented, illustrating how new technologies create unanticipated job categories.
4. Open source AI empowers human goodness by making people smarter
5. AI doomers hold a pessimistic view because they do not believe people are fundamentally good, or they distrust people and institutions to behave properly.
6. Yann LeCun has been a prominent advocate for making AI research, models, and tools open source.
7. LLMs do not help design or build bio/chemical weapons beyond what a search engine and library already provide
8. Translating language-based instructions into physical-world outcomes requires tacit expertise that LLMs cannot supply
9. LLMs are not controllable
10. Objective-driven AI architectures can embed guardrails as part of the optimization objective, enabling controllable and safe behaviour

## Capabilities

- V-JEPA achieves stable, high-quality video representations through masked joint embedding — the first self-supervised video pretraining approach to produce representations good enough for a supervised classifier head to identify actions with high accuracy
- V-JEPA shows preliminary ability to detect physically impossible events in video — disappearing objects, teleportation between locations, sudden shape changes — suggesting an emerging capacity for intuitive physics constraint detection
- Non-contrastive joint embedding methods (BYOL, DINO, VICReg, I-JEPA) train stable image representations without explicit negative sample pairs, preventing representational collapse through architectural and regularisation tricks alone
- JEPA-based action-conditioned world model architecture for robotics: a predictor fed with action inputs (e.g. steering angle) forecasts abstract representations of future states, enabling model predictive control at inference time
- Self-supervised LLM pretraining supports multilingual translation across hundreds of languages, summarisation, and question answering within a single model at broad production scale
- V-JEPA: self-supervised learning from video using a joint-embedding predictive architecture, training neural networks to predict in embedding space from masked video frames without generative reconstruction
- Embodied AI robots can navigate indoor environments, open refrigerators, and retrieve specific trained objects on natural-language command — demonstrated on commercial robot platforms at Meta FAIR
- Two-level hierarchical planning for legged robot locomotion: high-level path planning paired with low-level leg movement control — functional but only when abstraction levels are hand-designed by engineers, not learned
- LLMs provide no meaningful uplift for CBRN weapon synthesis beyond what is accessible via search engines and libraries — confirmed by a growing body of studies as of early 2024
- Self-supervised learning for NLP enables multilingual content moderation and hate speech detection at production scale without per-language labeled data
- Wav2Vec-style self-supervised contrastive speech models achieve multilingual ASR with only minutes of labeled data per language via joint embedding pretraining on unlabeled audio
- Real-time speech-to-speech translation across hundreds of languages including spoken-only languages with no written form, bypassing text entirely via discrete speech unit representations
- JEPA (Joint Embedding Predictive Architecture) successfully learns high-quality visual representations by predicting in embedding space rather than pixel space, verified via downstream classification performance
- Open-source large language models (LLaMA 2) deployed at scale with millions of downloads and thousands of downstream business applications, demonstrating viable open-source AI ecosystem

## Limitations

- AI's economic impact on labor is expected to be a gradual profession shift rather than rapid mass displacement, implying current AI systems lack the breadth and reliability to simultaneously displace multiple occupation categories at scale
- AI safety and alignment concerns are significantly driven by distrust of human institutions and human nature rather than specific technical failure modes, suggesting the alignment problem cannot be solved by technical means alone
- LLMs lack all four characteristics of intelligent behaviour: understanding the physical world, persistent memory, genuine reasoning, and planning — these are primitive or absent, not merely limited
- Generative video world models (predicting pixel distributions over future frames) have comprehensively failed after 10 years of attempts — GANs, VAEs, masked autoencoders, and latent variable approaches all failed to produce useful representations
- Self-supervised reconstruction of images (MAE / masked autoencoder style) produces poor general-purpose image representations — significantly underperforming supervised or label-supervised contrastive approaches on recognition tasks
- Hierarchical planning — decomposing a high-level goal into multi-level temporally abstracted subgoal hierarchies — is an unsolved problem; no known method trains a system to learn appropriate representational levels for each tier
- LLMs cannot generate plans for genuinely novel situations — they can only produce plans that closely resemble templates seen during training
- Vision-language models use language supervision as an architectural crutch to compensate for deficient visual representation learning — this approach is structurally incapable of reaching even cat/dog-level physical world understanding
- LLMs generate output token-by-token without pre-planning — they structurally cannot formulate an abstract answer before beginning generation, unlike humans who plan responses in a language-independent representation space
- Language data is fundamentally too low-bandwidth and low-redundancy to support learning physical world models through self-supervised prediction — text contains orders of magnitude less information than a child's four years of sensory experience
- LLMs cannot plan tasks that require sub-linguistic resolution — any action requiring millisecond-level motor control or low-level physical manipulation is beyond what can be expressed, reasoned about, or planned in language tokens
- Current AI systems cannot learn to drive a car from 20 hours of experience or clear a dinner table in one shot — mundane embodied tasks trivially acquired by children remain out of reach despite LLMs passing the bar exam
- LLMs hallucinate planning steps — even for well-trodden domains like New York to Paris travel, answers at all abstraction levels may be plausible-sounding but non-factual
- V-JEPA's intuitive physics detection capability is preliminary and unvalidated — results have not been rigorously benchmarked and may not generalise beyond the specific physical implausibility patterns tested
- Contrastive self-supervised learning requires explicit negative pairs (images known to be different) and has scaling limitations — the method adds complexity and sampling overhead to joint embedding training
- LLMs are architecturally uncontrollable — autoregressive generation cannot embed hard behavioral guarantees, making alignment via fine-tuning fragile and unable to provide principled safety assurances
- AI systems cannot simultaneously satisfy the contradictory value systems, cultural norms, and political opinions of a global user base — making universal content policy for a single closed model technically and philosophically impossible
- Current robotics cannot perform general unstructured domestic tasks (clearing tables, cooking, washing dishes) — only specific pre-trained manipulation tasks in constrained environments with known object categories
- Level 5 fully autonomous driving has not been achieved as of early 2024 — and no system can train itself to drive competently from ~20 hours of experience the way a human teenager can
- AI cannot bridge the gap between language-based instructions and physical-world execution — translating text to real-world action requires grounded embodied knowledge not present in linguistic training data
- Current GPU hardware is 4–5 orders of magnitude less power-efficient than the human brain — 500W–1kW per GPU vs the brain's ~25W means 100,000–1,000,000 GPUs would be needed to match human brain compute at equivalent scale, blocking ubiquitous deployment
- No AI system has demonstrated learned hierarchical planning where abstraction levels and their representations were discovered from data — all functional multi-level planning systems require hand-designed abstraction hierarchies
- Robot object manipulation is brittle and limited to object categories the system has been trained to recognise — no generalisation to novel objects in real-world settings
- No principled framework exists for AI systems to plan multi-step sequences of tool-use actions (search, database queries, calculators, simulations) — existing tool-use work is preliminary and without general solutions
- Self-supervised video representation learning required approximately a decade of sustained research effort before yielding meaningful progress, signalling the fundamental difficulty of extracting world-model-quality representations from raw video
- Big tech companies face a structurally irresolvable tension between maximally capable generative AI deployment and managing legal, political, and reputational risk — creating strong commercial incentives to degrade model output quality via over-alignment, with negative feedback loops propagating int
- Classical robotics approaches based on handcrafted dynamical models (Boston Dynamics style) hit a hard ceiling for unstructured environments — cannot generalise to domestic or novel settings without learned world models replacing the handcrafted components
- Achieving systems that integrate memory, planning, reasoning, and hierarchical representations at human level requires at least a decade of further research, with acknowledged unknown unknowns in the problem space
- LLMs allocate constant computation per token regardless of problem difficulty, structurally preventing System 2 deliberate reasoning that devotes more resources to harder problems
- LLMs cannot plan their answer before generating it — there is no mechanism for elaborating an abstract internal plan that precedes and guides token-by-token decoding
- LLMs lack low-level embodied world experience — trained only on text, they are missing the physical, causal, and perceptual grounding on which high-level language is built
- Implicit: much of underlying physical reality is not expressed in language at all, creating a hard ceiling on what LLMs can learn about the world from text alone
- LLMs are brittle to out-of-distribution prompts — the training distribution covers a negligible fraction of all possible prompts, and any sufficiently novel prompt elicits nonsensical output
- Substituting individual words in an otherwise valid English prompt with words in another language can catastrophically degrade output quality — a sharp performance cliff at cross-lingual token boundaries
- RLHF and fine-tuning cannot cover the long tail of possible prompts — the behavioral conditioning is a lookup table approximation, not generalization, and will fail at the tail
- Generative pixel-prediction models systematically fail to learn good representations of images or videos despite a decade of sustained research effort — predicting irrelevant high-frequency detail prevents representation quality
- Reinforcement learning is too sample-inefficient to be a primary learning mechanism — should be minimized and used only to correct an already-learned world model or objective function
- Implicit: RLHF reward models are currently used only for parameter fine-tuning, not inference-time planning — the architectural insight that reward models could serve as energy functions for planning is not yet implemented
- Discrete token-space search for LLM reasoning (beam search, best-of-N) is computationally wasteful compared to gradient-based optimization in continuous representation space
- AI systems are structurally incapable of being unbiased — any de-biasing process simply relocates bias rather than eliminating it, because bias is observer-relative and training data is inherently value-laden
- Implicit: LLMs cannot determine whether novel physical or causal scenarios are feasible because physical feasibility judgment requires low-level simulation grounding absent from text-only training
- Implicit: Centralized fine-tuning of large language models by a small number of companies makes ideological homogenization structurally inevitable — commercial incentives push toward risk-averse, audience-pleasing output at scale

## Bottlenecks

- Societal and institutional trust deficit is a non-technical bottleneck for safe broad AI deployment — governance frameworks require stable, reliable institutions that cannot be engineered and are contested among researchers themselves
- Representing probability distributions over high-dimensional continuous video frames is an unsolved theoretical problem — blocking all generative video world model approaches regardless of scale or architecture
- No training method exists for learning multi-level representational hierarchies appropriate for hierarchical planning — blocking autonomous agents from decomposing long-horizon goals across temporal scales
- Language data bandwidth is fundamentally insufficient for learning grounded physical world models — the entire LLM training corpus contains orders of magnitude less information than a single child's four years of sensory experience
- Premature fusion of visual and language self-supervised learning risks using language as a crutch that masks inadequate visual representations — requiring visual grounding to be solved independently before multimodal integration
- Absence of learned world models from video observation blocks significant progress in robotics, autonomous driving, and generalised physical-world AI — current systems cannot train themselves to understand physical reality efficiently from experience
- Learned hierarchical representation of action plans is completely unsolved — no method can discover what the appropriate abstraction levels should be for multi-step planning from data, blocking any AGI-prerequisite long-horizon autonomous capability
- GPU power consumption is 4–5 orders of magnitude above human brain efficiency — blocks ubiquitous, on-device, and embedded AI deployment and creates prohibitive energy costs at scale; requires new fabrication principles beyond classical digital CMOS
- LLM autoregressive architecture is fundamentally incompatible with principled safety guarantees — content guardrails can only be applied through unreliable fine-tuning rather than embedded as hard constraints, blocking trustworthy high-stakes deployment and culturally diverse alignment
- Autoregressive LLM architectures have no mechanism for adaptive computation allocation — fixed compute per token structurally blocks System 2 planning and deliberate reasoning in language systems
- Absence of a practical training framework for energy-based models with gradient-based inference blocks development of AI systems that plan answers through latent optimization before decoding
- Absence of embodied low-level world models in language-only AI systems blocks reliable common sense reasoning, physical feasibility judgment, and grounded language understanding
- Structural concentration of AI development in a few large companies creates systemic bias and information monoculture — open source is the only viable countermeasure, but training frontier base models remains prohibitively expensive for most actors

## Breakthroughs

- V-JEPA achieves the first successful self-supervised video representation learning through non-generative masked joint embedding — bypassing the long-standing failure of generative video prediction approaches
- V-JEPA: first successful demonstration of video-based self-supervised learning using a JEPA joint-embedding predictive architecture — learning temporally coherent world-relevant representations from video without generative reconstruction
- Joint embedding architectures (JEPA / I-JEPA) succeed at self-supervised visual representation learning where pixel-prediction generative models failed across a decade of attempts — predicting in representation space rather than pixel space produces usable downstream features
- Self-supervised contrastive speech pretraining (Wav2Vec) enables multilingual ASR from minutes of labeled data — demonstrating that joint embedding pretraining transfers across languages with negligible task-specific supervision

## Themes

- [[themes/ai_governance|ai_governance]]
- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]

## Key Concepts

- [[entities/autoregressive-language-model|Autoregressive Language Model]]
- [[entities/contrastive-learning|Contrastive Learning]]
- [[entities/hierarchical-planning|Hierarchical Planning]]
- [[entities/llama|LLaMA]]
- [[entities/masked-autoencoder|Masked Autoencoder]]
- [[entities/model-predictive-control|Model Predictive Control]]
- [[entities/moravecs-paradox|Moravec's Paradox]]
- [[entities/self-supervised-learning|Self-Supervised Learning]]
- [[entities/system-1-system-2-thinking|System 1 / System 2 Thinking]]
- [[entities/variational-autoencoder|Variational Autoencoder]]
- [[entities/world-model|World Model]]
