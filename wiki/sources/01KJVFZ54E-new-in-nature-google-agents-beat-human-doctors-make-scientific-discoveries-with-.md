---
type: source
title: 'New in Nature: Google Agents Beat Human Doctors, Make Scientific Discoveries
  – With Vivek and Anil'
source_id: 01KJVFZ54EM01P1KSE7A75EJQ3
source_type: video
authors: []
published_at: '2025-04-10 00:00:00'
theme_ids:
- agent_systems
- medical_and_biology_ai
- multi_agent_coordination
- scientific_and_medical_ai
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# New in Nature: Google Agents Beat Human Doctors, Make Scientific Discoveries – With Vivek and Anil

**Authors:** 
**Published:** 2025-04-10 00:00:00
**Type:** video

## Analysis

Overview

- The groundbreaking work on AMIE, the Articulate Medical Intelligence Explorer, and co\-scientist by Google DeepMind represent an important threshold moment in AI capabilities\.
	- If people truly understood what AI can already do today, many would be fundamentally rethinking their plans, and these projects provide perhaps the clearest evidence yet that AI systems are beginning to outperform highly intelligent humans in domains that require years of specialised training\. 
- Remarkably, this work was accomplished without special continued pre\-training or extensive custom post\-training that could only have been done within Google\. These approaches could have been developed and can be replicated by using commercially available models, advanced prompting techniques, and thoughtful agent design\. 
- A year ago, AMIE was already able to outperform human general practitioners in diagnostic accuracy\. Now, with just a few important caveats, they have demonstrated that it also beats human primary care physicians in analysis and treatment recommendations\. 
	- The implications for healthcare access are obviously profound and are beginning to extend into specialised medicine too\. 
- The second AMIE paper shows that the AI system is already surpassing medical fellows in both cardiology and oncology and closing in on attending level performance\. 
	- Notably, when cardiologists have access to AMIE, their performance dramatically improves across almost every metric, suggesting a short to medium term future in which AI doctors have the potential to both raise the floor for access to quality care globally and also raise the reliability ceiling even for those who have access to first world specialised care\. 
- In the co\-scientist paper, we see something equally, if not more amazing\. This multi\-agent AI scientist system, which is capable of accepting human input and feedback at any step in its process, was tested in fully autonomous mode on 3 increasingly complicated scientific challenges\. 
	- First, drug repurposing, an advanced, but reasonably well\-defined task amenable to combinatorial analysis\. 
	- Second, therapeutic target identification, a more open\-ended challenge requiring the AI to understand and or make quality hypotheses about causal relationships within cells\. 
	- And third, and definitely most dauntingly, the wholly open\-ended challenge of understanding the process by which bacteria achieve drug resistance\. 
- Co\-scientist, which Google is now making available to trusted partners, succeeded on all 3 of these tasks\. And on the challenge of understanding drug resistance in particular, it blew everyone's minds by proposing the exact same mechanism that Google's independent scientific collaborators had recently discovered experimentally, but had not yet published at the time of co\-scientists analysis\. 
- Overall, co\-scientists demonstrates that AI systems are now capable of generating novel insights by connecting the dots between far\-falling bits of hard\-won human knowledge\. 
	- This system is not simply regurgitating its training data\. On the contrary, it's performing meaningful synthesis and proposing novel hypotheses that even human expert scientists recognise as both insightful and significant\. 
- The implementation details behind these systems offer valuable lessons for AI engineers everywhere\. 
	- First, structured reasoning proves far more effective than simple CoT approaches, especially when working with lots of input context\. Both of these systems demonstrate the value of thinking carefully about exactly how you want your AI system to reason about specific types of problems\. 
	- Second, finding ways to add new information or even just a bit of entropy, such as by giving the model access to search, is key to making self\-critique and self\-improvement schemes work over many rounds of successive iteration\. 
	- And third, for now at least, the tournament style evaluation process used to surface the best candidate hypotheses out of the many that were generated, seems to be an industry best practice that you can and should use in your own work\. 
- This was achieved before Gemini 2\.5 Pro was available to use, meaning that everything we talk about today is still subject to a step change improvement that should come more or less for free with a simple model upgrade\. 
- With this level of performance already established and core model progress continuing, the path to an AI doctor in your pocket and data centres full of AI geniuses is honestly becoming quite clear\. 
	- AIs are no longer just tools for routine tasks\. They are becoming legitimate thought partners in some of humanity's most complex intellectual endeavours, from diagnosing disease to expanding the very frontiers of scientific knowledge\. 

Articulate Medical Intelligence Explorer Overview

- The initial AMIE research already showed the AI's superior accuracy in diagnosing patients when a patient chats to the AI compared to human primary care physicians, as judged by other doctors\.
- The new development extends this capability significantly\. AMIE is now reportedly outperforming GPs not only in diagnosis but also in reasoning through the necessary steps after diagnosis and ultimately in recommending treatments\.
	- This is a major step forward as treatment recommendation is a core responsibility of a physician, requiring complex reasoning and knowledge application\.
- Prior to the AMIE papers, previous work in the field often focused on medical question answering, which is not clinical practice and does not fully reflect the dynamic interaction between a doctor and a patient where the doctor needs to actively gather information, as the information is not presented all upfront\. 
	- The motivation for the AMIE studies was to see if the AI could interact with patients, gather the information and still get to that diagnostic endpoint in structured clinical examinations\.
- There are of cours

## Key Claims

1. Amy (Articulate Medical Intelligence Explorer) outperforms human general practitioners in diagnostic accuracy when interacting with patients via text-based chat
2. Amy outperforms human primary care physicians in management reasoning and treatment recommendations, not just diagnosis
3. Amy surpasses medical fellows in both cardiology and oncology but falls short of attending-level physician performance
4. When cardiologists have access to Amy, their performance improves dramatically across almost every metric
5. Amy and co-scientist were built without special continued pre-training or extensive custom post-training exclusive to Google; the approaches can be replicated using commercially available models
6. Co-scientist succeeded on all three scientific challenges: drug repurposing, therapeutic target identification, and understanding bacterial drug resistance mechanisms
7. Co-scientist's top hypothesis for the mechanism of bacterial drug resistance exactly matched an experimental finding that had been discovered but not yet published by independent scientific collaborat
8. Amy is entering a clinical trial in partnership with Beth Israel Deaconess Medical Center, a Harvard Medical School teaching hospital, for real-world validation
9. The clinical trial will deploy Amy in a clinic with sufficient clinical expert oversight, with the intent to reduce oversight requirements if things go well and scale to more centers
10. The Amy cardiology specialty study was conducted using Gemini 1.5 Flash, not Gemini 2 or 2.5

## Capabilities

- Amy system surpasses general practitioners in diagnosis AND treatment/management recommendations; outperforms medical fellows in cardiology and oncology; approaching but not quite at attending physician level
- AI-augmented physician performance: cardiologists using Amy show dramatic improvements across diagnostic and treatment accuracy metrics
- Multi-agent scientific discovery system (Co-Scientist) autonomously generates novel, experimentally validated scientific hypotheses across drug repurposing, therapeutic target identification, and mechanisms of drug resistance
- AI systems can synthesize novel scientific insights by integrating knowledge across distant domains, not simply regurgitating training data; perform meaningful hypothesis generation grounded in literature
- Frontier models with 2M+ token context enable multi-round agentic reasoning with implicit feedback accumulation; enable debate, critique, and iterative refinement within single context window without explicit memory systems
- General-purpose frontier models with strong instruction-following can be decomposed into specialized agents via prompting alone, eliminating need for fine-tuning or domain-specific model variants
- AI clinical management planning systems generate recommendations explicitly grounded in clinical practice guidelines and medication labels; better structured and more precise than physician-generated plans
- Agentic systems can run extended inference loops over days with access to tools (web search, literature retrieval, simulation) that prevent mode collapse and degenerate solutions by continuously introducing new information
- AI systems can hypothesis generation for genetic disease mechanisms; model-generated hypotheses match experimentally validated targets in rare disease research

## Limitations

- Amy operates only on text-based patient interaction, not on real clinical communication modalities (voice, visual examination, multi-visit longitudinal reasoning)
- Amy requires expert clinical oversight; cannot be safely deployed without presence of attending physicians to take over if system fails; deployment paradigm requires senior physician supervision
- Amy system understands multi-visit longitudinal management only partially; first visit endpoint often just 'order the right test' not definitive diagnosis/treatment
- Amy performance still falls short of attending physician level in cardiology and oncology specialties; needs additional development for specialist-level recommendation accuracy
- Early Co-Scientist versions generated vast amounts of nonsense hypotheses (thousands of incorrect outputs for every useful hypothesis); required human expert filtering for practical use
- Co-Scientist cannot autonomously identify novel research questions; can only answer questions posed by humans; question generation remains unsolved
- Published scientific literature is systematically biased toward positive results; negative results hidden in 'dark matter', blocking AI access to full experimental evidence
- Supplementary data files embedded in scientific papers (experimental datasets, raw results) are not systematically extracted or analyzed; valuable data nuggets in supplementary materials inaccessible at scale
- Adding new modalities (medical images, genomic data) to foundation models causes performance degradation on original task benchmarks (language/vision), requiring expensive continued pre-training to restore performance
- Hypergranular task decomposition (summarize complaint, summarize findings, etc.) underperforms coarse-grained decomposition (analysis, management goals); too much structure constrains effective reasoning
- Current agentic reasoning approach is token-inefficient: explicit generation of all ideas, reviews, debates, and comparisons in context requires high token throughput; latent-space reasoning more efficient but architecturally unclear
- Early reliability tradeoff: improved systematic reasoning through structured decomposition may sacrifice generation of truly novel/creative hypotheses that require less constrained, unstructured generation
- Evaluation methodology is subjective; system performance assessed via 'auto evaluation and vibe checks' rather than standardized, blinded evaluation against gold standards
- Scientific agent system requires human expert partners to validate hypotheses; cannot independently evaluate quality of generated hypotheses without domain expertise
- Extended inference-time test cases (days-long reasoning loops) may still be subject to diminishing returns or eventual performance plateaus, though exact boundaries unclear

## Bottlenecks

- Publication bias against negative results creates 'dark matter' of scientific knowledge unavailable to AI systems; no incentive mechanism exists to systematize publication of negative findings
- Research question generation is theoretically unsolved; no clear path for AI systems to autonomously identify novel, valuable research questions rather than only answering human-posed questions
- Multimodal foundation model training creates benchmark performance trade-offs: adding new modalities (medical imaging, genomic data) reduces performance on original benchmarks, blocking cost-effective multi-modal integration
- Supplementary data embedded in scientific papers (experimental datasets, raw results) are not systematically extracted, parsed, or analyzed; valuable experimental evidence inaccessible at scale
- Massive structured scientific datasets (e.g., 300M cell virtual cell atlas) cannot be efficiently explored by agentic systems without specialized engineering; no systematized framework for hypothesis generation over large structured data
- Extended test-time compute benefit from tool access that prevents mode collapse, but token efficiency of explicit reasoning chains unclear; latent-space reasoning more efficient but architecture unknown

## Breakthroughs

- Multi-agent scientific discovery systems with structured decomposition, long context, and tool access can autonomously generate novel, experimentally-validated scientific hypotheses (drug mechanisms, therapeutic targets, genetic disease causes) matching independent experimental discoveries
- AI clinical systems surpass primary care physician performance in both diagnosis AND treatment management; AI-assisted physician performance shows dramatic improvements across all metrics
- Extended context windows (2M+ tokens) enable implicit multi-round agentic reasoning without explicit memory systems; feedback, debates, and critique accumulate naturally in context enabling iterative improvement
- General-purpose frontier models with strong instruction-following can decompose complex tasks into specialized sub-agents via prompting alone, eliminating need for domain-specific fine-tuning or specialized model variants

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/amie-articulate-medical-intelligence-explorer|AMIE (Articulate Medical Intelligence Explorer)]]
- [[entities/long-context-window|Long Context Window]]
