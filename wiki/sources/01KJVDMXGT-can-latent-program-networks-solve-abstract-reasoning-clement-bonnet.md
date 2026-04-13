---
type: source
title: Can Latent Program Networks Solve Abstract Reasoning? [Clement Bonnet]
source_id: 01KJVDMXGTPVFBNRWJPYHXYQX1
source_type: video
authors: []
published_at: '2025-02-19 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- latent_reasoning
- model_architecture
- reasoning_and_planning
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Can Latent Program Networks Solve Abstract Reasoning? [Clement Bonnet]

**Authors:** 
**Published:** 2025-02-19 00:00:00
**Type:** video

## Analysis

Introduction to ARC Benchmark and LPN Overview

- The ARC benchmark, Abstraction and Reasoning Corpus, is a programme synthesis benchmark whose goal is to assess how AI systems can adapt to novelty at test time\. 
	- It’s an interesting benchmark because pre\-trained LLMs actually perform very poorly on it because the tasks that are seen at test time are very different from their training sets\. 
- The ARC challenge is so impervious to neural networks because it was designed to be robust to memorisation\. And it is robust to memorisation because the input\-output tasks are so different from whatever has been seen in the training distribution\. 
	- It is guaranteed that these tasks do not exist anywhere on the internet, and therefore, the task similarity is not high enough for LLMs to generalise zero shot\.
- Many of people’s conversation do not exist on the Internet either, but the difference is that these discussions can be embedded into a rather small latent space that the LLMs have learned to emulate and compose\. 
	- On the other hand, the ARC tasks are truly novel\. They are only based on the core human knowledge priors, but composed in arbitrary ways that are not on the internet anywhere and the pre\-trained models cannot make sense of\. Otherwise, you would get zero\-shot generalisation\.
	- If the distribution of tasks that are in the test sets was known, and you would finetune an LLM on it\. The reason why the test task cannot be solved is because the test distribution is quite far away from the training distribution\. So it is not able to do extreme generalisation and needs to try to come up with a novel way of combining knowledge to perform the task\.
- The proposed solution looks to build in search in the architecture such that it is going to do test\-time search\. And the way this is done is that the programmes are embedded into a latent space that is trained such that it is conducive to search\. 
- There have been many approaches to the ARC challenge\. Ellis had a neural guided search where we train a neural network\. And then these days, everyone is embracing the Greenblatt approach, where you just make an LLM generate programmes\. 
	- This approach seems to be completely different to all of the other types of test\-time adaptation, where it is about embedding the programmes in a latent space, and then searching that latent space\. It is not actually creating programmes, but generating the solutions directly\.
- The main idea was to do search at test time in a programme space in an efficient manner\. This involved embedding combinatorially hard programmes into a continuous latent space that then can be searched using any search method\. 
	- And so by learning the manifold of programmes into a single coherent latent space, this allows for efficient test adaptation\. 
- The top performing methods are using test time training, which is essentially parameter efficient finetuning\. Even at test time with newly input test inputs, it searches parameters in the parameter space that would better perform on the test inputs\. And that is an effective way to do recombination synthesis at test time\. 
	- However, arguably it’s a very inefficient way to do so because the parameter space is huge, and it is not obvious that you can recombine low level primitives in a compositional way\. 
	- So it is to be seen whether these approaches can solve ARC, and embedding programs into a more coherent and compressed representation may be an easier, more efficient way to do search\.

Induction vs Transduction in Machine Learning

- The distinction between the two methods is that transductive methods is more about creating a model from the data rather than reusing an existing model\. 
	- So for example, this method could be transductive if the encoder was finetuned based on some augmentations of the data\. But it is not because we’re doing some kind of gradient optimisation through the model, but not changing the model\. Therefore, it’s inductive\.
- In some ways the distinction between induction and transduction does not actually matter so much\. What is more important is how much representations are compressed\. 
	- With a method that comes up a Python programme or some kind of latent programme, i\.e\., a smaller representation that is supposed to emulate your outputs, this an induction method because there is this representation compression bottleneck\. 
		- The proposed method represents a very compressed representation of programmes in which can be effectively searched\. And when you have methods that generate Python programs, these are very similar methods of generating a very compressed programme in Python that can then generate an output\.
	- Instead, if you are trying to do a shallower recombination of just test\-time training, then this should fall under in the group of transductive methods\. 
		- It’s all about the compression, because compression allows for more efficient search\.
- Arguably, LPN search also fits in a spectrum of test\-time training methods, if the latent space is seen as an input\-conditioned parameter space that is being training\. We are searching through this space using zero\-order, first\-order optimisation methods to find a better explanation for your data\. 
	- It’s quite similar to searching through your parameter space while doing parameter finetuning at test time\. So it fits in the same spectrum, but is more efficient given that it is not searching a vast parameter space\. 

LPN Architecture and Latent Space Implementation

- To embed programmes into a latent space, there is an encoder that takes input\-output pairs independently and embeds them into a programme similar to a VAE architecture\. 
	- As an input\-output can be explained by an infinite number of programmes of varying description length or complexity, a variational framework is used, encoding these input\-output pairs into a distribution of programmes\. 
- And then there is this search component i

## Key Claims

1. Pre-trained LLMs perform very poorly on ARC because the test-time tasks are very different from the training distribution, making zero-shot generalization impossible.
2. ARC is designed to be robust to memorization by ensuring that test input-output tasks are not present anywhere on the internet.
3. ARC is not intrinsically unsolvable by neural networks — if the test distribution were known and any neural network architecture were trained on data including that distribution, it would solve the be
4. LPN (Latent Program Network) embeds programs into a continuous latent space, trained to be well-structured for search, enabling efficient test-time adaptation.
5. The top-performing ARC methods at time of publication use test-time training — parameter-efficient fine-tuning conditioned on a new test input.
6. Test-time training is argued to be inefficient for ARC because the parameter space is huge and compositional recombination of low-level primitives in parameter space is unclear.
7. Without a VAE prior (using only an autoencoder), the learned latent space becomes unstructured and spiky, with programs clustered as far from each other as possible, making search impossible.
8. LPN uses a leave-one-out strategy during training to prevent the latent space from simply memorizing output — each input-output pair is encoded using all other pairs in the specification, and the held
9. Activating search (random local search or gradient-based optimization) during training is essential for producing a latent space that is amenable to search at inference time, analogous to meta-learnin
10. LPN achieves approximately 10% accuracy on the ARC evaluation set without pre-trained LLMs, trained only on 400 ARC training tasks with augmented data.

## Capabilities

- Latent program network architecture embeds programs into continuous latent space and performs test-time search to solve ARC tasks without pre-trained models or prior knowledge of task distribution
- Test-time optimization in learned program latent spaces achieves more efficient search than parameter-space fine-tuning by leveraging structured, smooth geometric representation of programs

## Limitations

- Continuous latent space architecture fundamentally cannot represent program composition — only superposition of learned programs possible
- Transductive and transitive tasks fundamentally unsupported — tasks requiring no inductive representation (memorization of mappings) have no corresponding point in learned latent space
- Latent space smoothness and searchability degrades as problem distribution complexity increases, making simple gradient-based test-time search less effective at scale
- Training did not reach convergence due to insufficient compute; full training time and convergence properties unknown
- Decoder must have sufficient architectural capacity to execute learned programs; capacity-expressiveness trade-off with latent space dimensionality not fully characterized
- Lack of systematic analysis of which task types succeed vs fail — no principled characterization of performance across ARC task classes
- Latent space structure not analyzed for interpretability — no evidence of task-specific clustering or directional semantic meaning in learned representations
- Scaling computational cost: search-enabled training during full optimization adds 'significant overhead at training time'; combined encoder-decoder-latent scaling 'quite costly'
- Requires ~100M synthetic data points generated from 400 ARC tasks to train Transformers from scratch; data generation is task-specific and not generalizable

## Bottlenecks

- Program composition impossible in fixed continuous latent spaces; can only represent superposition. Blocks solving hierarchical/compositional ARC tasks and scaling approach beyond trivial problem classes.
- As task distribution complexity increases, learned latent spaces become less smooth and less amenable to gradient-based test-time search; trade-off between space coverage and searchability unresolved.
- Decoder capacity must scale with latent space dimensionality and program complexity; fundamental trade-off between expressiveness and trainability not characterized.

## Breakthroughs

- Conceptual clarification: ARC difficulty is fundamentally due to out-of-distribution generalization and data scarcity, not due to neural networks being architecturally incapable of symbolic reasoning or program induction

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/representation_learning|representation_learning]]

## Key Concepts

- [[entities/test-time-training|Test-Time Training]]
