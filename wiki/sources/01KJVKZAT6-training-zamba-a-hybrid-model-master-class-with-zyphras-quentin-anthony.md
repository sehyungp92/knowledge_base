---
type: source
title: 'Training Zamba: A Hybrid Model Master Class with Zyphra''s Quentin Anthony'
source_id: 01KJVKZAT6SM5YTWQTNMC27MHW
source_type: video
authors: []
published_at: '2024-10-30 00:00:00'
theme_ids:
- continual_learning
- finetuning_and_distillation
- model_architecture
- post_training_methods
- pretraining_and_scaling
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Training Zamba: A Hybrid Model Master Class with Zyphra's Quentin Anthony

**Authors:** 
**Published:** 2024-10-30 00:00:00
**Type:** video

## Analysis

On\-Device Deployment and Local Inference

- <a id="_Hlk191047997"></a>Zyphra believes that the future of AGI will involve a combination of cloud and on device deployment with an increasing shift towards local inference\. 
- There are a few angles to this, but the main benefit from having the model locally in the device may be personalisability\. Personalisation is not an easy task\.
	- System prompt hacking alone cannot result in something that can specialise to every single person on the planet\. Changing a system prompt per person is not enough\. Instead each person needs to have their own set of weights\. 
- The second driving factor is privacy\. 
	- There's a lot of data in your laptops and phones that you do not want to be communicating to the cloud\. There are also a lot of enterprises out there who do not want to share all of their data with OpenAI, including all their proprietary code, keeping that all on device on\-prem in the organisation\. 
- And then there's just some very practical challenges, including run\-rate capex of the foundation model companies, a lot of which is being fuelled by VC money and is not something that can keep up forever\. 
	- If everyone's device is able to efficiently run their own models, then that expense can be offloaded to the users\. Running it offline this way is also much faster\. 
- However, there are some model capabilities that are more challenging\. While people may just need these higher level, more simplistic tasks for the majority of the time they communicate with models, this will not always be the case\. 
	- The 7B range is a turning point where you can fit it on like more powerful laptops, powerful on\-prem\. But you want those on\-device models to be able to know when they need to go back and ask something more powerful\. 
	- And then this should be all seamless to the user, where you can pick and choose how often your model wants to talk to the cloud etc\. 
- It is not entirely clear what the exact process of personalisation will look like until there are a bunch of people with Zamba on their phones, but the company has a lot of expertise in continual learning\. So perhaps it will involve something like a weight update overnight, while your phone is plugged in or your laptop is not actively being used on consumer hardware\. 
	- This is very cheap to do when the model is really small or involves something like updating LoRAs\. 
	- <a id="_Hlk192609263"></a>Continual learning on a per user basis seems like the way to go and works well for small models, helped by techniques like activation steering\. If the user tells the model it is being too dry, then you can very quickly steer the activation to be a bit more fun\.
- The Zamba 2 1\.2B is good if you are edge constrained, i\.e\., you don't want your phone to use much battery\. You can just download the model weights and just tokenise and just train on whatever personal emails or whatever else you want\. 
- The 2\.7B is really good for quality, and there are some finetunes for that\. So we have some role play models, some summarisation models if you want to summarise emails, meetings, etc\. There are some audio capabilities as well, i\.e\., generating personalised audio, note taking audio for meetings\. 
- The product vision is that you have a cloud across all of your devices, you can upload pictures, conversations, it'll be multimodal, and you can decide how much you want to share, and how much you want it to be personalised to you\. 
	- Training on that cloud of your own data, just as a continual pre\-training on whatever edge hardware you have, is the high level\. 

State Space Models & Efficiency

- <a id="_Hlk191048211"></a>When you think of what models to run locally, with the transformers, there are usually 2 bottlenecks\. 
	- The first place is memory, which may be that the model is just too large in terms of parameter count or the KV cache is growing and at some point you run out of memory\. Transformers are famously memory intensive, as the KV cache scales quadratically as you scale your sequence\. 
	- And second one is just computation\. Transformer has amazing properties, but it is computationally intensive, especially when compared to other architectures\. 
- One of the exciting things about Mamba is that it has properties that are much more memory efficient and more computationally efficient processing sequences due to its fixed state size\. 
	- So in the literature, there have been some early work with Mamba models in robotics, as these models would have to run locally as you could not do cloud API calls for split second decisions that need to be made\. 
	- This may be an architecture that helps inform what the ultimate models running locally could look like for these kind of applications\. 
- Mamba is great for its systems properties\. As a guiding principle, in terms of model training, the company tries to train the models that are perfect for inference because that's where they are going to need them to perform the most\. 
- This translates to a few different things:
	- <a id="_Hlk191048270"></a>Attention for dense transformers is just not going to be the answer\. It is not going to be efficient on a phone for doing text, email news article summarisation etc\., as those inputs are too long for the KV cache\. It is just going to grow outside of memory for most phones today\. 
	- However, attention has very nice properties, with exact cross sequence dependencies that are just required for some specific tasks\. 
		- Not every task needs attention, but there are some tasks, like in\-context learning and long sequence dependencies, for which attention is just necessary\. It may be more performant after training on several trillion tokens, but a pure SSM or pure RNN model is not going to be able to speak well in an in\-context learning regime\. 
- So pure SSMs have quality issues and pure attention dense transformers have performance issues, i\.e\., cannot realistically get

## Key Claims

1. Zyra has focused on producing the best models for one modality and is now ready to expand to other modalities.
2. Zyra plans to add visual question answering as a capability.
3. Zyra plans to enable live editing of pictures through the AI.
4. Zyra plans to support voice-to-voice interaction with the AI model.
5. Zyra plans to deploy personalized AI capabilities to individual users.
6. Zyra plans to launch 'Zaya' for both enterprise and on-device consumer deployment.
7. The broader AI ecosystem tools such as llama and llama.cpp are all Transformer-based.
8. Integrating hybrid architectures into the existing Transformer-based ecosystem (llama, llama.cpp) is one of Zyra's next priorities.
9. Current deployment of Zyra's hybrid architecture models relies on a fork of Hugging Face rather than mainstream ecosystem tooling.
10. Memory and retrieval are considered important for enabling personalization in AI assistants.

## Capabilities

- Hybrid recurrent/attention architecture models trained and operational in custom inference environments, enabling non-Transformer language model deployment
- Hybrid Mamba 2-Transformer architecture (Zamba 2) achieves Pareto frontier of efficiency and performance among open models at 1.2B, 2.7B, and 7B parameter scales, with superior inference throughput over pure Transformers at equivalent parameter counts
- Mamba 2 SSD algorithm enables GPU tensor-core matrix multiplication for SSM training, delivering significantly higher H100 throughput and larger state sizes with no model quality degradation compared to Mamba 1
- Context length extension via curriculum continual pre-training achieves full model quality on longer sequences for Mamba hybrid models — no quality loss versus native training at the extended length
- Tree attention reformulates distributed attention as topology-aware all-reduce operations, enabling efficient multi-node long-context training and inference beyond the 2-node ceiling of ring attention
- Zamba 1.2B model deployable with 4-bit quantization on edge devices (Raspberry Pi, Jetson Nano) for single-task use cases such as summarization with very low overhead
- LoRA adapters on shared MLP blocks within hybrid architectures provide per-depth specialization with low parameter and compute overhead, empirically improving accuracy over baseline
- Hybrid SSM-attention architecture (Zamba 2 7B) achieves 20-30% faster time-to-first-token and time-per-output-token compared to equivalent dense Transformer models, with significantly lower memory overhead
- Shared global attention blocks with depth-wise LoRA adapters reduce KV cache invocations to 10-13 per forward pass (versus 30-32 for dense Transformers) while maintaining comparable model quality
- Hybrid SSM-attention 7B models run on powerful laptops and on-premises hardware, enabling complex reasoning tasks at the edge without cloud API calls
- Continual pre-training on personal data (emails, messages) for small on-device models (1.2B–2.7B) via overnight weight updates on consumer hardware, enabling per-user weight specialization
- Activation steering enables rapid same-session behavioral adjustment (e.g., tone modification) in small language models as a real-time stopgap before permanent weight baking via continual learning
- Mamba-based models can handle robotics inference locally without cloud API calls, meeting real-time latency requirements that cloud round-trips cannot satisfy
- Two-phase annealing training: pretraining on broad web data with standard cosine decay, then rewarming learning rate on a curated high-quality data subset and aggressively decaying to zero, producing specialized model checkpoints from a single base without full retraining
- Hybrid SSM-Transformer architecture (6:1 Mamba-to-attention ratio with shared global attention) matches quality of dense Transformers trained on 5–15× more tokens, at 7B scale trained on only 1 trillion tokens
- μP (MuP) hyperparameter transfer enables exhaustive learning-rate and batch-size search on cheap small-width proxy models with exact analytic transfer to full-scale models, eliminating repeat hyperparameter sweeps at large scale
- Hardware-aware kernel-aligned model sizing (powers-of-two hidden dimensions, vocab size multiples of 64, per-block rounding to efficient kernel paths) delivers cross-platform inference speedups on any parallel hardware for the entire model lifetime
- Correlated attention blocks in hybrid SSM-Transformer architectures can be collapsed to a single shared global attention block with negligible quality loss, dramatically reducing inference cost while preserving attention's in-context retrieval benefits
- Synthetic data generated from large models serves as a tractable proxy for full logit-based distillation, allowing smaller labs to steer annealing and post-training strategies toward large-model output distributions without requiring live teacher inference
- Mamba 2 SSD algorithm — adding structure to the state-transition A matrix — enables SSM layers to use matrix multiplication and GPU tensor cores, allowing much faster training and substantially larger recurrent state sizes

## Limitations

- Hybrid SSM/Transformer architectures are not yet integrated into standard open-source inference frameworks (llama.cpp, GGML/GGUF), requiring custom forks and blocking accessible deployment
- Standard RLHF and preference-learning methods do not scale down to the tiny per-user datasets available in on-device personalization settings
- Continual pre-training alone is insufficient to achieve meaningful behavioral personalization on-device; preference alignment requires a distinct mechanism
- Optimal interaction between retrieval-augmented generation and extended long-context processing for personalization is unresolved — no principled framework determines when to retrieve vs. extend context
- Multimodal capabilities (visual question answering, live image editing, voice-to-voice) absent from hybrid architecture models as of late 2024 — single-modality text only
- On-device consumer AI with genuine personalization (Zaya-class product) remains undeployed as of Q4 2024 — framed as near-term roadmap rather than shipped capability
- Pure Mamba 2 without attention fails at in-context learning and long-sequence dependencies — attention is a mandatory component; fully SSM-based models remain non-viable
- No sequence parallelism implementation exists for Mamba blocks, preventing million-token context training on multi-GPU setups — activations plus gradient and optimizer states exceed H100 memory capacity
- Rotary positional embeddings (RoPE) trade long-range dependency gains for context length inflexibility — adding RoPE for recall quality improvement blocks context length generalization beyond training distribution
- Hybrid Mamba models not yet integrated with mainstream inference ecosystems (llama.cpp, ollama, vLLM, GGML) — requiring users to operate a custom HuggingFace fork as of publication date
- Production pre-training frameworks (Megatron-LM, DeepSpeed) are incompatible with Mamba hybrid training — large-scale pre-training requires custom in-house infrastructure that is not open-sourced
- Mamba hybrid models exhibit noticeable cross-sequence dependency degradation at very long contexts — behavior at million-token scale is genuinely unknown, and more attention blocks may be required
- Mamba state size is capped at 64 to preserve inference efficiency — larger state sizes (which improve long-range recall) cause measurable inference time degradation that outweighs quality benefit in hybrid architectures
- Ring attention cannot scale beyond ~2 nodes on standard GPU clusters due to point-to-point communication assumptions that don't account for the order-of-magnitude bandwidth gap between NVLink (intra-node) and InfiniBand (inter-node)
- Strong architectural lock-in effects at large labs make Transformer-to-hybrid migration effectively prohibitive: all accumulated ablations, fine-tuning recipes, interpretability tools, and serving optimizations must be rebuilt from scratch
- Optimal attention-to-Mamba ratio in hybrid architectures has no theoretical basis — all published ratios (6:1 at Zypher, varying 7:1 to 10:1 across Jamba/others) are purely empirical with no generalizable principles
- Scaling behavior of shared attention blocks in hybrid architectures under extended training (e.g., 15T+ tokens) is unknown — chinchilla optimality is reached faster than expected, and attention block saturation behavior is uncharted
- Emergent capabilities of new architectures are unpredictable without training to hundreds of billions of tokens — comparative architectural evaluation requires near-production-scale training runs, raising the cost of architecture search
- Mechanistic interpretability tooling for hybrid Mamba-Transformer architectures does not exist — circuit analysis, attention visualization, and probing methods built for Transformers do not transfer to SSM components
- Pure SSM architectures (without any attention) require 3–4+ trillion tokens before developing reliable in-context learning (as measured by MMLU signal emergence), versus hundreds of billions of tokens for hybrid or dense Transformer models
- Dense Transformer models cannot run efficiently on mobile phones due to linear KV cache growth with sequence length — long-context tasks like email and article summarization are practically infeasible on-device
- System-prompt-based personalization by major cloud AI providers cannot achieve deep individual adaptation — preferences, communication styles, and personal facts cannot be baked into weights via context alone
- Training loss is a poor and unreliable indicator of model quality — it is dataset-dependent, noise-dominated, and does not track emergent capabilities or real-world task performance
- Optimizing training data for benchmark performance produces brittle, dry models that fail on diverse real-world inputs — synthetic textbook-heavy data inflates benchmarks but degrades fine-tuning responsiveness and conversational quality
- Fine-tuning large frontier models (e.g., GPT-4o) on personal writing samples learns stylistic patterns but fails to reliably learn new facts — hallucinations persist even after personalisation fine-tuning
- No principled theory exists for which attention operations can be safely linearized — practitioners cannot predict whether a linearized-attention variant will preserve in-context learning or long-range dependencies
- Per-user on-device continual learning has no consumer-grade deployment tooling — users must manually download weights, configure tokenization, and run training via research-grade interfaces
- Cloud AI inference costs are unsustainable at projected scale and currently VC-subsidized — centralized frontier model serving cannot continue indefinitely without fundamental cost reduction through on-device offloading
- Pure Mamba MoE architectures (without attention) are unstable to train, exhibiting frequent loss spikes that require intervention
- MMLU and similar format-dependent benchmarks show near-random performance for most of training before suddenly improving — making it impossible to monitor quality progress during the majority of any training run
- Small on-device models (1B–2B parameters) cannot handle advanced multi-step reasoning (Olympiad math, complex compositional tasks) — routing to cloud models is required for these capability levels
- Post-training attention linearization (distilling a trained Transformer's attention into a linear/SSM block) is a theoretically motivated but unproven approach — the quality preservation of long-range dependencies under this transformation is unknown
- Relationship between model scale, emergent capabilities, and optimizer landscape remains empirically driven — practitioners cannot systematically predict when or why capabilities emerge, relying on 'vibes' evaluation alongside benchmarks
- Pre-training scale logit-based knowledge distillation is computationally prohibitive: synchronizing teacher inference (400B+ parameters) with every student training step costs as much as training a much larger model outright, making full distillation inaccessible to labs without frontier compute bud
- The true geometry of high-dimensional loss landscapes remains theoretically opaque: no principled understanding exists of landscape topology, optimal navigation strategies, or why any given optimizer choice succeeds; all training decisions remain empirical
- Alternative optimizers (Sophia, Adafactor, second-order optimizers) are brittle across training setups: they offer conditional improvements but fail unpredictably for different model sizes, architectures, and hyperparameter configurations, making Adam the only reliably deployable choice
- MoE architectures have fundamentally unstable training dynamics: attention blocks and expert blocks receive incompatible effective batch sizes within the same model, making hyperparameter optimization extremely difficult and failure frequent
- Gradient instability from data outliers at large batch sizes: in models with bumpy loss landscapes (small models, novel architectures), a small number of out-of-distribution samples in a large batch can cause cascading divergence when combined with elevated learning rates
- Catastrophic forgetting during annealing: models rapidly lose broad web-data distribution when trained exclusively on curated high-quality data; requires continuous phase-1 replay tokens in every batch to maintain generality, constraining the efficiency of the specialization step
- μP hyperparameter transfer is functionally inaccessible to small labs: papers are 30–40 pages of dense mathematics, requiring dedicated personnel for weeks of study and significant compute to validate, making the technique a de facto frontier-lab exclusive despite being publicly published
- Open-source labs are structurally disadvantaged on data quality: frontier labs have proprietary high-quality data (search, user interactions, curated corpora) and dedicated data engineering teams; open-source always lags on the data dimension regardless of algorithmic parity
- Optimal parallelism schemes for novel and hybrid architectures are empirical and non-portable: 4D parallelism topologies, checkpoint restart infrastructure, and optimizer state sharding for non-standard architectures are tightly coupled to proprietary training stacks and cannot be transferred betwee
- μP hyperparameter transfer cannot be applied to non-Adam optimizers without re-deriving the full theoretical framework: each new optimizer changes the activation scaling conditions, requiring months of mathematical work before the technique transfers
- Synthetic data as distillation proxy is informationally impoverished compared to full logits: argmax sampling captures only what the large model attends to, discarding near-zero logit values that encode what the model confidently ignores — critical signal for small model calibration
- Frontier lab training knowledge is hardening into organization-specific stacks: techniques are so deeply embedded in proprietary infrastructure that even engineers who possess the knowledge cannot easily port it when moving between organizations, creating compounding structural barriers
- Large models require lower learning rates despite smoother loss landscapes: at very large parameter counts, any gradient instability risks irreversible divergence before it can be corrected, requiring conservative step sizes that offset the smoothness advantage
- Hardware-specific model optimization creates a latent ecosystem fragmentation risk: as every chip vendor bakes model sizes optimized for their specific streaming multiprocessors and SRAM, models will become efficient only on their origin hardware, creating mutual incompatibility across the hardware 

## Bottlenecks

- Hybrid architecture models (SSM/Transformer) not integrated into mainstream open-source inference frameworks (llama.cpp, GGML), blocking accessible deployment by developers and end-users outside research settings
- No viable on-device RLHF or preference-learning approximation exists for the tiny per-user datasets available in personal AI applications, blocking genuine behavioral personalization
- Unresolved interaction between long-context processing and retrieval for personalization: no principled framework determines when to use extended in-context memory versus explicit retrieval
- Sequence parallelism for Mamba/SSM blocks does not exist, preventing hybrid models from training or running inference at million-token context lengths — device memory for activations, gradients, and optimizer states is exceeded even on H100
- The entire mainstream ML ecosystem (llama.cpp, ollama, vLLM, Megatron-LM, DeepSpeed, GGML) is architected around Transformer ops — each new hybrid architecture must re-implement fine-tuning recipes, serving kernels, and inference optimizations from scratch
- No theoretical framework exists to determine optimal attention-to-Mamba block ratios or dynamic attention allocation in hybrid architectures — design space must be explored empirically with expensive multi-hundred-billion-token training runs per configuration
- Pure SSM architectures require 3–4 trillion training tokens to develop in-context learning, making pure-SSM replacement of Transformers for general instruction-following tasks impractical
- No consumer-grade on-device continual learning pipeline exists — per-user weight updates require manual HuggingFace setup, blocking mass-market deployment of deeply personalized on-device AI
- No principled theory exists for which attention operations can be safely linearized — blocking systematic design of sub-quadratic attention alternatives with guaranteed quality preservation on in-context learning tasks
- Training quality monitoring is effectively blind for most of a training run — loss is dataset-dependent noise, key emergent benchmarks show no signal until late training, forcing reliance on subjective 'vibes' evaluation
- Pre-training scale logit-based knowledge distillation is blocked by compute: synchronized inference of a 400B+ teacher model at every student training step costs as much as training a substantially larger model from scratch, making full distillation inaccessible outside frontier labs
- Systematic knowledge asymmetry between frontier labs and the broader ecosystem: multi-phase annealing, logit distillation, second-order optimizers for small models, μP hyperparameter transfer, checkpoint restart infrastructure, and parallelism schemes are hoarded and stack-embedded rather than diffu
- MoE training instability from gradient scale mismatch: attention blocks see full batches while expert blocks see subdivided fractions, creating fundamentally incompatible effective batch sizes within a single forward pass that makes joint hyperparameter optimization extremely difficult
- μP hyperparameter transfer is not generalised beyond Adam: each new optimizer (second-order, adaptive) requires re-deriving the full scaling theory, blocking efficient hyperparameter search for novel training configurations without months of additional mathematical work per optimizer

## Breakthroughs

- Mamba 2 SSD (State Space Duality) algorithm restructures the SSM state matrix to admit GPU tensor-core matrix multiplication, dramatically increasing training throughput on modern hardware and enabling larger state sizes without quality loss
- Tree attention reformulates distributed attention computation as an all-reduce energy function, enabling topology-aware multi-node scaling that overcomes the hard 2-node ceiling of ring attention on standard GPU clusters
- Multiple independent groups discovered that attention blocks are highly correlated across Transformer depth — most layer-level specialization comes from MLP blocks, not attention — enabling a single shared attention block (with small depth-wise LoRA adapters) to match independent per-layer attention
- Two-phase annealing paradigm: after broad-web pretraining with cosine decay, rapidly rewarm learning rate on curated high-quality data and aggressively decay to zero, baking specific knowledge top-of-mind while retaining generality through phase-1 token replay
- Mamba 2 SSD algorithm: structuring the state-transition A matrix allows SSM layers to use dense matrix multiplication and GPU tensor cores, enabling substantially faster training throughput and much larger recurrent state sizes than Mamba 1
- Co-optimisation of architecture, training process, and data quality as a unified system (demonstrated in Zamba 1) achieves 5–15× training token efficiency versus optimising architecture alone, challenging the assumption that token count is the primary determinant of small-model quality

## Themes

- [[themes/continual_learning|continual_learning]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chinchilla-scaling-laws|Chinchilla Scaling Laws]]
- [[entities/continual-learning|Continual learning]]
- [[entities/dclm|DCLM]]
- [[entities/fineweb|FineWeb]]
- [[entities/grouped-query-attention|Grouped Query Attention]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/hugging-face|Hugging Face]]
- [[entities/kv-cache|KV Cache]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/llama|LLaMA]]
- [[entities/linear-attention|Linear Attention]]
- [[entities/lora|LoRA]]
- [[entities/mmlu|MMLU]]
- [[entities/platonic-representation-hypothesis|Platonic Representation Hypothesis]]
- [[entities/rlhf|RLHF]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/ring-attention|Ring Attention]]
- [[entities/grokking|grokking]]
- [[entities/long-context|long context]]
