"""Seed the 3-level AI taxonomy DAG. Idempotent (ON CONFLICT DO NOTHING).

Taxonomy is grounded in the actual reading library, derived from curated
summaries and source titles. Three levels:
  Level 0 (meta): broad organisational groupings — never classified into directly
  Level 1 (subtheme): primary analytical units — landscape state summaries, bottlenecks,
                      capabilities tracking; equivalent to the old 27 flat themes
  Level 2 (subsubtheme): leaf nodes for source classification — specific enough to
                         attach to individual sources

ALL_NODES tuples: (id, name, description, level)
HIERARCHY_EDGES tuples: (parent_id, child_id, relationship, strength)
  - Uses relationship="contains" for level-0→level-1 and level-1→level-2 edges
CROSS_CUTTING_EDGES tuples: (parent_id, child_id, relationship, strength)
  - Semantic edges between level-1 nodes
"""

from __future__ import annotations

import logging

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

# (id, name, description, level)
ALL_NODES = [
    # ----------------------------------------------------------------
    # Level 0 — Meta / Themes (organisational groupings, ~5-6 nodes)
    # Never classified into directly; provide hierarchy for navigation.
    # ----------------------------------------------------------------
    ("meta_foundations", "Intelligence Foundations",
     "Core learning, reasoning, and generalisation mechanisms", 0),
    ("meta_capabilities", "AI Capabilities",
     "Applied capabilities and vertical domains", 0),
    ("meta_embodiment", "Embodiment & Physical AI",
     "Physical-world grounding, robots, vehicles", 0),
    ("meta_reliability", "Reliability & Safety",
     "Robustness, evaluation, alignment", 0),
    ("meta_infrastructure", "Infrastructure & Economics",
     "Compute, data, market dynamics", 0),

    # ----------------------------------------------------------------
    # Level 1 — Subthemes (primary analytical units, ~17 nodes)
    # These are the units for landscape state summaries, bottleneck
    # tracking, and /landscape queries.
    # ----------------------------------------------------------------
    ("reasoning_and_planning", "Reasoning & Planning",
     "Search, planning, chain-of-thought, system-2 thinking", 1),
    ("reinforcement_learning", "Reinforcement Learning",
     "Self-play, RL scaling, reward modeling, test-time compute", 1),
    ("learning_dynamics", "Learning Dynamics",
     "Scaling laws, synthetic data, continual learning, test-time training", 1),
    ("memory_and_context", "Memory & Context",
     "RAG, long context, memory systems, retrieval-augmented generation", 1),
    ("world_models", "World Models",
     "Learned simulators, model-based RL, video physics", 1),
    ("architectural_innovation", "Architecture & Representation",
     "Transformer alternatives, adaptive computation, representation learning", 1),
    ("language_and_communication", "Language & Communication",
     "Dialogue, translation, assistants, multilinguality", 1),
    ("code_and_software", "Code & Software",
     "Code generation, software agents, program synthesis", 1),
    ("autonomous_agents", "Autonomous Agents",
     "Multi-step tasks, computer use, multi-agent systems, personal assistants", 1),
    ("creative_generation", "Creative Generation",
     "Image, music, video generation, generative art", 1),
    ("scientific_discovery", "Scientific Discovery",
     "Biology, mathematics, materials, drug discovery, medical AI", 1),
    ("robotics", "Robotics",
     "Manipulation, locomotion, sim-to-real transfer, self-driving", 1),
    ("multimodality", "Multimodal Perception",
     "Vision-language, video, audio understanding and generation", 1),
    ("robustness_and_reliability", "Robustness & Reliability",
     "Jagged intelligence, hallucination, calibration, edge cases", 1),
    ("evaluation_and_benchmarks", "Evaluation & Benchmarks",
     "Reasoning benchmarks, saturation, contamination, eval design", 1),
    ("interpretability", "Interpretability",
     "Mechanistic analysis, circuit probing, uncertainty quantification", 1),
    ("safety_and_alignment", "Safety & Alignment",
     "RLHF alignment, deception, constitutional AI, governance", 1),
    ("compute_and_hardware", "Compute & Hardware",
     "GPUs, chips, inference efficiency, energy, serving", 1),
    ("ai_economics", "AI Economics",
     "SaaS disruption, model commoditisation, developer tooling", 1),

    # ----------------------------------------------------------------
    # Level 2 — Subsubthemes (leaf classification targets, ~42 nodes)
    # Specific enough to attach to individual sources.
    # Each must be evidenced by at least one source title or summary.
    # ----------------------------------------------------------------

    # Under reasoning_and_planning
    ("mcts_and_tree_search", "MCTS & Tree Search",
     "Monte Carlo Tree Search, AlphaGo-style planning, game search", 2),
    ("hierarchical_planning", "Hierarchical Planning",
     "Temporal abstraction, goal decomposition, task hierarchies", 2),
    ("reasoning", "Reasoning",
     "CoT prompting, o1-style inference search, slow thinking, System 2", 2),
    ("program_synthesis", "Program Synthesis",
     "Code as reasoning, DSL search, ARC program induction", 2),

    # Under reinforcement_learning
    ("self_play_and_expert_iteration", "Self-Play & Expert Iteration",
     "AlphaZero distillation, synthetic data loops, iterated amplification", 2),
    ("rlhf_and_reward_modeling", "RLHF & Reward Modeling",
     "PPO, DPO, reward hacking, constitutional AI, preference learning", 2),
    ("test_time_compute", "Test-Time Compute",
     "Inference-time search, RLVR, compute-optimal inference, best-of-N sampling", 2),
    ("value_functions", "Value Functions",
     "Dense vs sparse rewards, credit assignment, multi-step RL", 2),

    # Under learning_dynamics
    ("scaling_laws", "Scaling Laws",
     "Data/compute/model tradeoffs, chinchilla, diminishing returns", 2),
    ("synthetic_data_generation", "Synthetic Data",
     "Self-generated data, data wall solutions, distillation pipelines", 2),
    ("continual_learning", "Continual Learning",
     "Online adaptation, catastrophic forgetting, memory consolidation", 2),
    ("test_time_learning", "Test-Time Learning",
     "Test-time training, weight adaptation at inference, problem-specific fine-tuning, TTT", 2),
    ("in_context_learning", "In-Context Learning",
     "Few-shot adaptation, ICL limits and mechanisms, meta-learning", 2),
    ("sample_efficiency", "Sample Efficiency",
     "Human vs model data requirements, few-shot, zero-shot", 2),
    ("data", "Data",
     "Data curation, filtering, deduplication, quality, licensing", 2),

    # Under memory_and_context
    ("retrieval_augmented_generation", "Retrieval-Augmented Generation",
     "RAG pipelines, vector search, retrieval grounding, hybrid retrieval", 2),
    ("long_context", "Long Context",
     "Extended context windows, efficient attention, infinite context", 2),

    # Under creative_generation
    ("image_generation", "Image Generation",
     "Diffusion models, text-to-image, image editing, style transfer", 2),
    ("audio_and_music", "Audio & Music",
     "Text-to-speech, music generation, voice synthesis, audio understanding", 2),

    # Under world_models
    ("model_based_rl", "Model-Based RL",
     "MuZero, latent simulators, Dreamer, world model planning", 2),
    ("video_and_physics_models", "Video & Physics Models",
     "Sora/Veo, physics prediction from video, generative simulators", 2),
    ("embodied_grounding", "Embodied Grounding",
     "Sensory grounding, Moravec paradox, symbol grounding problem", 2),

    # Under architectural_innovation
    ("transformer_alternatives", "Transformer Alternatives",
     "SSMs, Mamba, RNNs, diffusion LMs, hybrid architectures", 2),
    ("adaptive_computation", "Adaptive Computation",
     "CTM, NTMs, dynamic depth, mixture-of-experts routing", 2),
    ("representation_learning", "Representation Learning",
     "JEPA, contrastive learning, joint embedding, latent spaces", 2),
    ("neurosymbolic_hybrid", "Neurosymbolic & Hybrid",
     "Symbolic+neural integration, compositional generalisation", 2),
    ("neuroscience_intersection", "Neuroscience Intersection",
     "Bio-inspired architectures, brain-AI parallels, cognitive science", 2),

    # Under language_and_communication
    ("dialogue_and_assistants", "Dialogue & Assistants",
     "Chatbots, conversational AI, instruction following, RLHF-tuned assistants", 2),
    ("multilingual_and_translation", "Multilingual & Translation",
     "Cross-lingual transfer, machine translation, low-resource languages", 2),

    # Under code_and_software
    ("software_agents", "Software Agents",
     "Agentic coding, SWE-bench, Claude Code, autonomous dev", 2),
    ("finetuning_and_distillation", "Finetuning & Distillation",
     "LoRA, SFT, knowledge distillation, PEFT, adapter methods", 2),

    # Under scientific_discovery
    ("protein_and_biology", "Protein & Biology AI",
     "AlphaFold, genomics, synthetic biology, drug target identification", 2),
    ("mathematics_and_proofs", "Mathematics & Formal Reasoning",
     "AlphaProof, ARC challenge, theorem proving, formal verification", 2),
    ("drug_discovery", "Drug Discovery",
     "AI-driven drug design, molecular generation, clinical trial optimization", 2),
    ("medical_ai", "Medical AI",
     "Clinical decision support, medical imaging, diagnostic AI", 2),

    # Under robustness_and_reliability
    ("jagged_intelligence", "Jagged Intelligence",
     "Uneven capability profiles, PhD-level vs trivial failures", 2),
    ("hallucination_and_calibration", "Hallucination & Calibration",
     "Confidence scores, grounding, factuality, sycophancy", 2),

    # Under evaluation_and_benchmarks
    ("reasoning_benchmarks", "Reasoning Benchmarks",
     "ARC, ARC-AGI-2, MATH, GSM8K, reasoning challenge design", 2),
    ("benchmark_saturation", "Benchmark Saturation",
     "Contamination, Goodharting, eval evolution, leaderboard gaming", 2),

    # Under interpretability
    ("mechanistic_interpretability", "Mechanistic Interpretability",
     "Circuit analysis, attention head probing, superposition", 2),
    ("uncertainty_quantification", "Uncertainty Quantification",
     "Calibration, conformal prediction, epistemic vs aleatoric", 2),

    # Under safety_and_alignment
    ("deception_and_corrigibility", "Deception & Corrigibility",
     "Scheming, goal misgeneralisation, corrigibility, shutdown", 2),
    ("ai_governance", "AI Governance & Regulation",
     "EU AI Act, executive orders, international coordination, labs policy", 2),

    # Under compute_and_hardware
    ("inference_efficiency", "Inference Efficiency",
     "Quantisation, small model deployment, speculative decoding", 2),
    ("training_infrastructure", "Training Infrastructure",
     "Distributed training, cluster design, energy and cooling", 2),

    # Under ai_economics
    ("saas_disruption", "SaaS & Service-as-Software",
     "AI eating software services, vertical AI, workflow automation", 2),
    ("model_commoditisation", "Model Commoditisation",
     "Price compression, open vs closed source, race dynamics", 2),

    # Under multimodality
    ("vision_language_models", "Vision-Language Models",
     "VLMs, GPT-4V, Gemini, visual QA, image-text alignment", 2),
    ("video_understanding", "Video Understanding",
     "Temporal reasoning, action recognition, video generation", 2),

    # Under robotics
    ("manipulation_and_locomotion", "Manipulation & Locomotion",
     "Dexterous manipulation, legged robots, whole-body control", 2),
    ("sim_to_real", "Sim-to-Real Transfer",
     "Domain randomisation, reality gap, simulation fidelity", 2),
    ("self_driving", "Self-Driving",
     "Autonomous vehicles, end-to-end driving, perception-planning", 2),

    # Under autonomous_agents
    ("multi_agent_systems", "Multi-Agent Systems",
     "Agent coordination, emergent cooperation, agent debates", 2),
    ("computer_use_agents", "Computer Use Agents",
     "Desktop/browser automation, GUI agents, tool use", 2),
    ("personal_assistants", "Personal Assistants",
     "AI assistants, personalisation, persistent memory, task delegation", 2),
]

# -----------------------------------------------------------------------
# HIERARCHY_EDGES — structural parent→child containment edges
# relationship="contains" for all level-0→1 and level-1→2 edges
# -----------------------------------------------------------------------
HIERARCHY_EDGES = [
    # meta_foundations → level-1
    ("meta_foundations", "reasoning_and_planning", "contains", 1.0),
    ("meta_foundations", "reinforcement_learning", "contains", 1.0),
    ("meta_foundations", "learning_dynamics", "contains", 1.0),
    ("meta_foundations", "memory_and_context", "contains", 1.0),
    ("meta_foundations", "world_models", "contains", 1.0),
    ("meta_foundations", "architectural_innovation", "contains", 1.0),

    # meta_capabilities → level-1
    ("meta_capabilities", "language_and_communication", "contains", 1.0),
    ("meta_capabilities", "code_and_software", "contains", 1.0),
    ("meta_capabilities", "autonomous_agents", "contains", 1.0),
    ("meta_capabilities", "creative_generation", "contains", 1.0),
    ("meta_capabilities", "scientific_discovery", "contains", 1.0),
    ("meta_capabilities", "multimodality", "contains", 1.0),

    # meta_embodiment → level-1
    ("meta_embodiment", "robotics", "contains", 1.0),
    ("meta_embodiment", "world_models", "contains", 1.0),  # also in foundations

    # meta_reliability → level-1
    ("meta_reliability", "robustness_and_reliability", "contains", 1.0),
    ("meta_reliability", "evaluation_and_benchmarks", "contains", 1.0),
    ("meta_reliability", "interpretability", "contains", 1.0),
    ("meta_reliability", "safety_and_alignment", "contains", 1.0),

    # meta_infrastructure → level-1
    ("meta_infrastructure", "compute_and_hardware", "contains", 1.0),
    ("meta_infrastructure", "ai_economics", "contains", 1.0),

    # reasoning_and_planning → level-2
    ("reasoning_and_planning", "mcts_and_tree_search", "contains", 1.0),
    ("reasoning_and_planning", "hierarchical_planning", "contains", 1.0),
    ("reasoning_and_planning", "reasoning", "contains", 1.0),
    ("reasoning_and_planning", "program_synthesis", "contains", 1.0),

    # reinforcement_learning → level-2
    ("reinforcement_learning", "self_play_and_expert_iteration", "contains", 1.0),
    ("reinforcement_learning", "rlhf_and_reward_modeling", "contains", 1.0),
    ("reinforcement_learning", "test_time_compute", "contains", 1.0),
    ("reinforcement_learning", "value_functions", "contains", 1.0),

    # learning_dynamics → level-2
    ("learning_dynamics", "scaling_laws", "contains", 1.0),
    ("learning_dynamics", "synthetic_data_generation", "contains", 1.0),
    ("learning_dynamics", "continual_learning", "contains", 1.0),
    ("learning_dynamics", "test_time_learning", "contains", 1.0),
    ("learning_dynamics", "in_context_learning", "contains", 1.0),
    ("learning_dynamics", "sample_efficiency", "contains", 1.0),
    ("learning_dynamics", "data", "contains", 1.0),

    # memory_and_context → level-2
    ("memory_and_context", "retrieval_augmented_generation", "contains", 1.0),
    ("memory_and_context", "long_context", "contains", 1.0),

    # creative_generation → level-2
    ("creative_generation", "image_generation", "contains", 1.0),
    ("creative_generation", "audio_and_music", "contains", 1.0),

    # world_models → level-2
    ("world_models", "model_based_rl", "contains", 1.0),
    ("world_models", "video_and_physics_models", "contains", 1.0),
    ("world_models", "embodied_grounding", "contains", 1.0),

    # architectural_innovation → level-2
    ("architectural_innovation", "transformer_alternatives", "contains", 1.0),
    ("architectural_innovation", "adaptive_computation", "contains", 1.0),
    ("architectural_innovation", "representation_learning", "contains", 1.0),
    ("architectural_innovation", "neurosymbolic_hybrid", "contains", 1.0),
    ("architectural_innovation", "neuroscience_intersection", "contains", 1.0),

    # language_and_communication → level-2
    ("language_and_communication", "dialogue_and_assistants", "contains", 1.0),
    ("language_and_communication", "multilingual_and_translation", "contains", 1.0),

    # code_and_software → level-2
    ("code_and_software", "software_agents", "contains", 1.0),
    ("code_and_software", "finetuning_and_distillation", "contains", 1.0),
    ("code_and_software", "program_synthesis", "contains", 1.0),

    # autonomous_agents → level-2
    ("autonomous_agents", "multi_agent_systems", "contains", 1.0),
    ("autonomous_agents", "computer_use_agents", "contains", 1.0),
    ("autonomous_agents", "personal_assistants", "contains", 1.0),

    # scientific_discovery → level-2
    ("scientific_discovery", "protein_and_biology", "contains", 1.0),
    ("scientific_discovery", "mathematics_and_proofs", "contains", 1.0),
    ("scientific_discovery", "drug_discovery", "contains", 1.0),
    ("scientific_discovery", "medical_ai", "contains", 1.0),

    # robotics → level-2
    ("robotics", "manipulation_and_locomotion", "contains", 1.0),
    ("robotics", "sim_to_real", "contains", 1.0),
    ("robotics", "self_driving", "contains", 1.0),

    # multimodality → level-2
    ("multimodality", "vision_language_models", "contains", 1.0),
    ("multimodality", "video_understanding", "contains", 1.0),
    ("multimodality", "video_and_physics_models", "contains", 1.0),

    # robustness_and_reliability → level-2
    ("robustness_and_reliability", "jagged_intelligence", "contains", 1.0),
    ("robustness_and_reliability", "hallucination_and_calibration", "contains", 1.0),

    # evaluation_and_benchmarks → level-2
    ("evaluation_and_benchmarks", "reasoning_benchmarks", "contains", 1.0),
    ("evaluation_and_benchmarks", "benchmark_saturation", "contains", 1.0),

    # interpretability → level-2
    ("interpretability", "mechanistic_interpretability", "contains", 1.0),
    ("interpretability", "uncertainty_quantification", "contains", 1.0),

    # safety_and_alignment → level-2
    ("safety_and_alignment", "deception_and_corrigibility", "contains", 1.0),
    ("safety_and_alignment", "ai_governance", "contains", 1.0),
    ("safety_and_alignment", "rlhf_and_reward_modeling", "contains", 1.0),

    # compute_and_hardware → level-2
    ("compute_and_hardware", "inference_efficiency", "contains", 1.0),
    ("compute_and_hardware", "training_infrastructure", "contains", 1.0),

    # ai_economics → level-2
    ("ai_economics", "saas_disruption", "contains", 1.0),
    ("ai_economics", "model_commoditisation", "contains", 1.0),
]

# -----------------------------------------------------------------------
# CROSS_CUTTING_EDGES — semantic edges between level-1 nodes
# Encode research-meaningful connections across subthemes.
# -----------------------------------------------------------------------
CROSS_CUTTING_EDGES = [
    ("world_models", "robotics", "enables", 0.8),               # sim-to-real transfer
    ("world_models", "reasoning_and_planning", "enables", 0.7), # model-based planning
    ("reinforcement_learning", "reasoning_and_planning", "enables", 0.7),  # RL as search
    ("reasoning_and_planning", "scientific_discovery", "enables", 0.7),    # hypothesis gen
    ("reasoning_and_planning", "autonomous_agents", "enables", 0.8),       # task decomp
    ("learning_dynamics", "architectural_innovation", "related", 0.6),     # scale × arch
    ("interpretability", "safety_and_alignment", "enables", 0.8),          # verifiable align
    ("compute_and_hardware", "learning_dynamics", "constrains", 0.9),      # compute wall
    ("architectural_innovation", "language_and_communication", "enables", 0.7),
    ("architectural_innovation", "code_and_software", "enables", 0.7),
    ("architectural_innovation", "multimodality", "enables", 0.7),
    ("architectural_innovation", "reasoning_and_planning", "enables", 0.6),
    ("reinforcement_learning", "autonomous_agents", "enables", 0.7),       # RL for agents
    ("evaluation_and_benchmarks", "robustness_and_reliability", "related", 0.6),
    ("safety_and_alignment", "autonomous_agents", "constrains", 0.7),       # alignment for agents
    ("ai_economics", "compute_and_hardware", "related", 0.6),               # cost drives access
    ("scientific_discovery", "multimodality", "related", 0.5),              # vision in science
]


def seed_themes(dsn: str):
    """Insert all themes and edges. Idempotent."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        for theme_id, name, description, level in ALL_NODES:
            conn.execute(
                """INSERT INTO themes (id, name, description, level)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                (theme_id, name, description, level),
            )

        all_edges = HIERARCHY_EDGES + CROSS_CUTTING_EDGES
        for parent_id, child_id, relationship, strength in all_edges:
            conn.execute(
                """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (parent_id, child_id) DO NOTHING""",
                (parent_id, child_id, relationship, strength),
            )

        conn.commit()

    meta = [n for n in ALL_NODES if n[3] == 0]
    subthemes = [n for n in ALL_NODES if n[3] == 1]
    subsubthemes = [n for n in ALL_NODES if n[3] == 2]
    logger.info(
        "Seeded %d meta + %d subthemes + %d subsubthemes (%d total), %d edges",
        len(meta), len(subthemes), len(subsubthemes), len(ALL_NODES), len(all_edges),
    )


def main():
    logging.basicConfig(level=logging.INFO)
    from reading_app.config import Config
    config = Config()
    seed_themes(config.postgres_dsn)


if __name__ == "__main__":
    main()
