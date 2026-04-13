---
type: source
title: 'The Quest to ‘Solve All Diseases’ with AI: Isomorphic Labs’ Max Jaderberg'
source_id: 01KJVP1SYGSWF8HX51C1RDP5TV
source_type: video
authors: []
published_at: '2025-04-29 00:00:00'
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- medical_and_biology_ai
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Quest to ‘Solve All Diseases’ with AI: Isomorphic Labs’ Max Jaderberg

**Authors:** 
**Published:** 2025-04-29 00:00:00
**Type:** video

## Analysis

- Isomorphic is pursuing the ambitious goal of reimagining drug discovery and development with AI to enable the solving of all diseases at a global scale\. AI will be completely transformative in understanding biology, manipulating chemistry, and designing therapeutics\.
	- AI will not only help design new drugs but also provide a much deeper understanding of the biological world, cellular function, and the root causes of disease, thereby reveal new therapeutic pathways\.
	- The core strategy is to build a very general drug design engine with AI\. This engine is intended to be applicable universally – across any disease area, any biological target, and any molecular modality – rather than being limited to single applications\.
- Previous generations of AI in drug design often involved local models typically trained on limited, specific datasets \(e\.g\., data about a single target or a class of molecules\) and used MLPs to make predictions for specific design rounds\.
	- Isomorphic's approach is the complete opposite, aiming for models that generalise broadly across chemistry and across target space\.
- AlphaFold and AlphaFold 3 are prime examples of generalisable models Isomorphic is building\. These models can be applied to virtually any protein or any small molecule without needing to be finetuned or adapted with local data for each new application\.
	- This fundamentally changes how chemists can use AI models, removing the need for adapting models to every single application\.
- Achieving a truly transformative, general drug design engine requires more than just structure prediction\.
	- AlphaFold was a massive breakthrough in understanding the structure of proteins, and AlphaFold 3 for understanding the structure of small molecules \(e\.g\., DNA and RNA\)\. This a fundamental step change that allows us to get experimental\-level accuracy of a core concept of biochemistry that unlocks a whole bunch of thinking and design work for chemists\.
	- <a id="_Hlk198862184"></a>However, half a dozen more breakthroughs of a similar magnitude to AlphaFold may be required <a id="_Hlk198863045"></a>to achieve experimental\-level accuracy in understanding other fundamental concepts of biology and chemistry crucial for drug design\.
		- Examples of these complex concepts include how a molecule behaves in the body \(absorption, distribution, metabolism, excretion – ADME\), how it reaches and affects specific cell types, and its overall pharmacological properties\.
		- Drug design is not just about understanding the structure of a protein or even designing a molecule that will modulate that protein in the way that you want\. This molecule should ideally be taken as a pill, go through the body, and be absorbed in the right way to reach the right cell type rather than be broken down by the liver\.

A holy grail model

- Some of the research areas being pursued, such as predicting the structure and properties of biomolecules, and understanding how these molecules interact and evolve over time, represent some of the "holy grail" predictive challenges in drug design\.
	- Isomorphic is making significant breakthroughs in creating these predictive models, achieving stunning accuracy, even reaching or surpassing experimental levels, fundamentally changing internal drug design processes\. However, even having a full suite of the best possible predictive models would not solve drug design entirely\.
- <a id="_Hlk198853299"></a>The core challenge lies in the sheer size of the chemical space of possible drug\-like molecule, estimated to contain around 10^60 molecules, or a reduced estimate of 10^40\. 
	- Even with the best predictive models allowing for the screening of a billion molecules \(10^9\), this is a minuscule fraction of the total space, leaving 10^31molecules unexplored\.
	- Therefore, predictive models alone, while powerful for evaluating candidates, cannot effectively explore this vast search space\. Generative models and agents are required to navigate and explore the vast molecular space intelligently\.
		- Molecular design is more akin to Go than Chess\. While Chess has a finite, albeit large, number of possible moves that could theoretically be exhaustively searched, the space of possible drug molecules is far too large for exhaustive search\.
- In simple terms, the process involves 2 stages:
	- Creating "world models" \(the predictive AI models that understand the biochemical world\)\.
	- Creating "agents" and "generative models" that know how to effectively explore and traverse this world to find the valuable molecules that could become life\-changing therapeutics\.

The breakthroughs of AlphaFold

- <a id="_Hlk198853616"></a>AlphaFold 2 was perhaps the biggest breakthrough, predicting the structure of individual proteins\. AlphaFold 2 Multimer extended this to predict the structure of protein complexes \(how proteins fit together\)\. 
	- While useful for understanding biology, it was still a step away from drug design, especially for small molecule drugs\.   
- AlphaFold 3 represents a significant leap by being able to model the structure and interactions of all molecules relevant to life, including proteins, small molecules, DNA and RNA\.
- <a id="_Hlk198854334"></a>Small molecules can have an effect by binding to proteins and modulating their function \(disrupting or enhancing interactions with other molecules\)\. AlphaFold 3 allows drug designers to visualise exactly how a small molecule interacts with a protein in 3D, including the literal physical interactions being made\. 
	- This is crucial for designing molecules that will effectively target a specific protein site\.   
	- The ability to model interactions with DNA and RNA opens up new classes of drug targets, such as transcription factors \(proteins that bind to and read DNA\)\. 
- AlphaFold 3 enables highly accurate in silico predictions of these interactions\. This replaces traditional lab methods, which can take months or years, a

## Key Claims

1. Demis Hassabis won the Nobel Prize in Chemistry in 2024.
2. Isomorphic Labs was launched out of DeepMind with a goal of revolutionizing drug discovery using AI.
3. Isomorphic Labs is designed from inception to build a general drug design engine applicable across any disease area and any molecular modality, not a single-target or single-indication approach.
4. Drug design requires approximately half a dozen AlphaFold-level breakthroughs beyond structure prediction to create a transformative drug design engine.
5. The total space of possible drug-like molecules is estimated at approximately 10^60, which cannot be exhaustively searched even with the best predictive models.
6. Even if one could screen a billion molecules (10^9), that still leaves approximately 10^31 or more molecules unexplored, making exhaustive predictive screening insufficient for drug design.
7. Drug molecule design requires both generative models and agents capable of navigating vast molecular space, analogous to how AlphaGo navigates Go move space rather than exhaustively searching like che
8. Reinforcement learning differs from supervised learning in that it does not require knowing the correct answer, only a signal of whether a given answer was good or not.
9. Supervised learning requires knowing the correct answer in advance, which limits its applicability to problems where human-level solutions already exist.
10. Multiplayer games create a combinatorial diversity of training tasks through varying opponent strategies, enabling better RL generalization compared to single-player environments.

## Capabilities

- Predict 3D structures of proteins, small molecules, DNA, RNA, and their interactions with experimental-level accuracy
- Generative models for molecule design that navigate chemical space to generate novel drug candidates
- General drug property prediction models that transfer across different targets and chemical modalities without fine-tuning
- AI agents that learn to explore and search through chemical space to find drug candidates, analogous to AlphaGo-style planning

## Limitations

- AlphaFold 3 does not achieve 100% accuracy; unclear what perfect accuracy means in real experimental context
- Models predict static crystal structures but not dynamic molecular behavior in physiological solutions where molecules constantly move
- Structure and property prediction models alone cannot solve drug design; even perfect predictions cannot exhaustively explore ~10^40-10^60 chemical space
- Approximately 6 more AlphaFold-level breakthroughs still needed to fully solve drug design beyond structure prediction
- Cannot generate synthetic in vivo experimental data; historical animal model data is scarce and new data generation technologies still emerging
- Cannot comprehensively predict off-target effects across entire proteome; toxicity from unintended protein interactions remains major cause of drug failure
- Biological and chemical experimental data historically available was not generated for machine learning purposes, limiting training utility
- Drug development involves many unaddressed bottlenecks beyond molecular design (clinical trials, regulatory approval, toxicity testing infrastructure)
- Isomorphic Labs lacks proprietary experimental laboratories, limiting ability to generate novel internal experimental data
- Models do not account for how drugs cause proteins to change conformations and cellular dynamics, critical for understanding functional effects
- No clear timeline provided for when AI-designed drugs will reach clinical trials; regulatory frameworks not yet adapted for AI-designed therapeutics

## Bottlenecks

- Chemical space exploration: with ~10^40-10^60 possible drug-like molecules, exhaustive screening impossible even with perfect predictive models; requires intelligent search/navigation
- Biological data generation: in vivo experimental data (from animal models) cannot be synthetically generated and is required for validating complex biological effects
- Clinical trial and regulatory paradigm mismatch: traditional clinical trial frameworks not designed for AI-predicted drug properties; regulatory bodies lack frameworks for AI-designed therapeutics
- Molecular dynamics and conformational modeling: current models predict static structures but not how proteins dynamically change shape in response to drugs or in cellular environments
- Off-target toxicity prediction: cannot comprehensively model how drug molecules interact with and affect thousands of other proteins in the human body

## Breakthroughs

- AlphaFold 3 extends molecular structure prediction from proteins alone to all molecules (small molecules, DNA, RNA) and their interactions with experimental-level accuracy
- Generative models for drug design have demonstrated capability to find molecular designs superior to human expert intuition when validated through experimental testing

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]

## Key Concepts

- [[entities/reinforcement-learning|Reinforcement Learning]]
- [[entities/supervised-learning|Supervised Learning]]
