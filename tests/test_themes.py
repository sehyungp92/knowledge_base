"""Tests for the 3-level theme taxonomy system."""

from db.seed_themes import ALL_NODES, HIERARCHY_EDGES, CROSS_CUTTING_EDGES

# Derived views for convenience
META_DOMAINS  = [n for n in ALL_NODES if n[3] == 0]   # level-0
THEMES        = [n for n in ALL_NODES if n[3] == 1]   # level-1 subthemes
SUBTHEMES     = [n for n in ALL_NODES if n[3] == 2]   # level-2 subsubthemes
ALL_EDGES     = HIERARCHY_EDGES + CROSS_CUTTING_EDGES
ALL_NODE_IDS  = {n[0] for n in ALL_NODES}


# -----------------------------------------------------------------------
# Structure / counts
# -----------------------------------------------------------------------

def test_level_counts_reasonable():
    """Taxonomy must have sane counts at each level."""
    assert 4 <= len(META_DOMAINS) <= 10, f"Expected 4-10 meta domains, got {len(META_DOMAINS)}"
    assert 15 <= len(THEMES) <= 35, f"Expected 15-35 subthemes, got {len(THEMES)}"
    assert 20 <= len(SUBTHEMES), f"Expected at least 20 subsubthemes, got {len(SUBTHEMES)}"


def test_levels_valid():
    """All level values must be in {0, 1, 2}."""
    for node_id, name, desc, level in ALL_NODES:
        assert level in {0, 1, 2}, f"Node {node_id} has invalid level {level}"


def test_theme_ids_unique():
    ids = [n[0] for n in ALL_NODES]
    assert len(ids) == len(set(ids)), "Duplicate theme IDs found"


def test_theme_ids_snake_case():
    """All theme IDs must be valid snake_case."""
    import re
    pattern = re.compile(r"^[a-z][a-z0-9_]*$")
    for node_id, _, _, _ in ALL_NODES:
        assert pattern.match(node_id), f"Theme ID not snake_case: {node_id}"


def test_names_under_40_chars():
    """All theme names must be under 40 characters."""
    for node_id, name, _, _ in ALL_NODES:
        assert len(name) <= 40, f"Theme name too long ({len(name)} chars): {name} ({node_id})"


def test_descriptions_nonempty():
    """All themes must have a non-empty description."""
    for node_id, _, desc, _ in ALL_NODES:
        assert desc and desc.strip(), f"Theme {node_id} has empty description"


# -----------------------------------------------------------------------
# Edge correctness
# -----------------------------------------------------------------------

def test_edges_reference_valid_themes():
    for parent, child, _, _ in ALL_EDGES:
        assert parent in ALL_NODE_IDS, f"Unknown parent in edge: {parent}"
        assert child in ALL_NODE_IDS, f"Unknown child in edge: {child}"


def test_no_self_edges():
    for parent, child, _, _ in ALL_EDGES:
        assert parent != child, f"Self-edge on {parent}"


def test_relationship_types():
    valid = {"contains", "enables", "overlaps", "depends_on", "related", "constrains"}
    for _, _, rel, _ in ALL_EDGES:
        assert rel in valid, f"Unknown relationship type: {rel}"


def test_strength_range():
    for _, _, _, strength in ALL_EDGES:
        assert 0 <= strength <= 1.0, f"Strength {strength} out of range"


# -----------------------------------------------------------------------
# Hierarchy integrity
# -----------------------------------------------------------------------

def test_every_subsubtheme_has_contains_edge():
    """Every level-2 node must have at least one 'contains' edge from a level-1 node."""
    level1_ids = {n[0] for n in THEMES}
    contains_children = {
        child for parent, child, rel, _ in HIERARCHY_EDGES
        if rel == "contains" and parent in level1_ids
    }
    missing = [n[0] for n in SUBTHEMES if n[0] not in contains_children]
    assert not missing, (
        f"Level-2 nodes missing a 'contains' edge from a level-1 node: {missing}"
    )


def test_every_subtheme_has_meta_domain_edge():
    """Every level-1 node must have at least one 'contains' edge from a level-0 node."""
    level0_ids = {n[0] for n in META_DOMAINS}
    contains_children = {
        child for parent, child, rel, _ in HIERARCHY_EDGES
        if rel == "contains" and parent in level0_ids
    }
    missing = [n[0] for n in THEMES if n[0] not in contains_children]
    assert not missing, (
        f"Level-1 subthemes missing a 'contains' edge from a level-0 meta node: {missing}"
    )


def test_no_meta_node_as_edge_child_of_non_meta():
    """Level-0 meta nodes must not appear as children of level-1 nodes."""
    level0_ids = {n[0] for n in META_DOMAINS}
    for parent, child, rel, _ in ALL_EDGES:
        if child in level0_ids:
            assert parent in level0_ids, (
                f"Meta node {child} is a child of non-meta node {parent}"
            )


def test_every_subtheme_has_at_least_one_subsubtheme():
    """Every level-1 node should have at least one level-2 child."""
    level2_parents = set()
    for parent, child, rel, _ in HIERARCHY_EDGES:
        if rel == "contains":
            child_level = {n[0]: n[3] for n in ALL_NODES}.get(child)
            if child_level == 2:
                level2_parents.add(parent)
    missing = [n[0] for n in THEMES if n[0] not in level2_parents]
    assert not missing, (
        f"Level-1 subthemes with no level-2 children: {missing}"
    )


# -----------------------------------------------------------------------
# Key source-grounded themes present
# (spot-checks that the taxonomy covers key research areas from the library)
# -----------------------------------------------------------------------

def test_key_research_areas_covered():
    """Taxonomy must cover the key research areas in the reading library.

    Uses flexible matching — checks that at least one theme ID contains
    the keyword, so this test survives taxonomy regeneration.
    """
    ids_lower = {n[0].lower() for n in ALL_NODES}

    # Key areas that must be represented somewhere in the taxonomy
    key_areas = [
        "reason",        # reasoning, planning
        "rl",            # reinforcement learning
        "scal",          # scaling laws
        "safety",        # safety, alignment
        "agent",         # autonomous agents
        "eval",          # evaluation, benchmarks
        "interpret",     # interpretability
        "architect",     # architecture, transformer alternatives
    ]

    for area in key_areas:
        matched = any(area in tid for tid in ids_lower)
        assert matched, (
            f"No theme ID contains '{area}' — key research area not covered"
        )


# -----------------------------------------------------------------------
# Cross-cutting edges
# -----------------------------------------------------------------------

def test_cross_cutting_edges_exist():
    """There should be a meaningful number of cross-cutting edges."""
    assert len(CROSS_CUTTING_EDGES) >= 10, (
        f"Expected at least 10 cross-cutting edges, got {len(CROSS_CUTTING_EDGES)}"
    )


def test_cross_cutting_edges_between_level1():
    """Cross-cutting edges should connect level-1 nodes."""
    level1_ids = {n[0] for n in THEMES}
    for parent, child, rel, _ in CROSS_CUTTING_EDGES:
        assert parent in level1_ids or child in level1_ids, (
            f"Cross-cutting edge {parent}→{child} doesn't involve any level-1 node"
        )
