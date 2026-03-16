"""Tier 3 verification tests for /beliefs, /challenge, /enrich handlers.

Invokes the direct Python handlers the same way the gateway dispatcher does.
Saves outputs to _results/ folder.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.pop("CLAUDECODE", None)

from reading_app.config import Config
from reading_app.db import init_pool, ensure_pool, get_conn
from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
from gateway.models import Event, Job

RESULTS_DIR = Path(__file__).parent.parent / "_results"
RESULTS_DIR.mkdir(exist_ok=True)

# Fix Windows encoding issues
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

config = Config()
init_pool(config.postgres_dsn)
executor = ClaudeExecutor(DEFAULT_WORKSPACE)


def make_event(text: str) -> Event:
    return Event(type="message", source="test", payload={"text": text})

def make_job(skill: str) -> Job:
    return Job(event_id=0, skill=skill, id=0, status="running", retry_count=0)

def progress(msg: str):
    print(f"  >> {msg}")


def run_test(name: str, handler_module: str, handler_func: str, text: str, output_file: str):
    """Run a single handler test and save output."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    t0 = time.monotonic()

    import importlib
    mod = importlib.import_module(handler_module)
    fn = getattr(mod, handler_func)

    event = make_event(text)
    skill_name = handler_module.split(".")[-1].replace("_handler", "")
    job = make_job(skill_name)

    try:
        result = fn(event, job, config, executor, on_progress=progress)
        elapsed = time.monotonic() - t0
        print(f"\n--- Result ({elapsed:.1f}s) ---")
        print(result[:500] if result else "(empty)")
        if len(result or "") > 500:
            print(f"... ({len(result)} chars total)")

        out_path = RESULTS_DIR / output_file
        out_path.write_text(result or "(empty)", encoding="utf-8")
        print(f"\nSaved to: {out_path}")
        return result
    except Exception as e:
        elapsed = time.monotonic() - t0
        error_msg = f"ERROR ({elapsed:.1f}s): {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        out_path = RESULTS_DIR / output_file
        out_path.write_text(f"ERROR: {e}\n\n{traceback.format_exc()}", encoding="utf-8")
        return None


def verify_db(description: str, query: str, params: tuple = ()):
    """Run a DB verification query and print results."""
    print(f"\n  DB CHECK: {description}")
    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()
        for r in rows:
            print(f"    {dict(r)}")
        return rows


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "all"

    # ---------------------------------------------------------------
    # Step 4.5.11: /beliefs add + /beliefs list
    # ---------------------------------------------------------------
    if step in ("all", "4.5.11", "beliefs"):
        # First belief
        run_test(
            "4.5.11a: /beliefs add (predictive - AI agents as primary interface)",
            "gateway.beliefs_handler", "handle_beliefs_job",
            "/beliefs add Personal AI agents like OpenClaw will become the primary interface for most computing tasks within 3 years, displacing both traditional apps and web-based SaaS for personal productivity",
            "4.5.11_beliefs_add_1.md",
        )
        verify_db(
            "Belief 1 in DB",
            "SELECT id, claim, confidence, belief_type, domain_theme_id FROM beliefs ORDER BY created_at DESC LIMIT 1",
        )

        # Second belief
        run_test(
            "4.5.11b: /beliefs add (bottleneck - reliability)",
            "gateway.beliefs_handler", "handle_beliefs_job",
            "/beliefs add The main bottleneck for AI agents is not capability but reliability — error compounding in multi-step tasks makes agents unsuitable for mission-critical workflows until error rates drop by 10x",
            "4.5.11_beliefs_add_2.md",
        )
        verify_db(
            "Both beliefs in DB",
            "SELECT id, claim, confidence, belief_type, domain_theme_id FROM beliefs ORDER BY created_at DESC LIMIT 2",
        )

        # List beliefs
        run_test(
            "4.5.11c: /beliefs (list)",
            "gateway.beliefs_handler", "handle_beliefs_job",
            "/beliefs",
            "4.5.11_beliefs_list.md",
        )

    # ---------------------------------------------------------------
    # Step 4.5.12: /challenge
    # ---------------------------------------------------------------
    if step in ("all", "4.5.12", "challenge"):
        # Challenge bottleneck
        run_test(
            "4.5.12a: /challenge bottleneck (error compounding)",
            "gateway.challenge_handler", "handle_challenge_job",
            "/challenge bottleneck bn_01KJ5NY2VDP9WMMPEKEG91ASW3",
            "4.5.12_challenge_bottleneck.md",
        )
        verify_db(
            "Challenge log entry",
            "SELECT id, entity_type, entity_id, outcome FROM challenge_log ORDER BY created_at DESC LIMIT 1",
        )

        # Self-challenge belief (steelman)
        # Get latest belief ID
        with get_conn() as conn:
            belief = conn.execute(
                "SELECT id FROM beliefs ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        if belief:
            belief_id = belief["id"]
            run_test(
                f"4.5.12b: /challenge belief steelman ({belief_id})",
                "gateway.challenge_handler", "handle_challenge_job",
                f"/challenge belief {belief_id} steelman",
                "4.5.12_challenge_belief_steelman.md",
            )
            verify_db(
                "Challenge log for belief",
                "SELECT id, entity_type, entity_id, outcome FROM challenge_log WHERE entity_type = 'belief' ORDER BY created_at DESC LIMIT 1",
            )
        else:
            print("\n  SKIP: No beliefs to challenge (run 4.5.11 first)")

    # ---------------------------------------------------------------
    # Step 4.5.13: /enrich
    # ---------------------------------------------------------------
    if step in ("all", "4.5.13", "enrich"):
        source_id = "01KJ6NT1T9MV7R25KD4NBZKF3Y"

        # Present-only mode
        run_test(
            "4.5.13a: /enrich (present current state)",
            "gateway.enrich_handler", "handle_enrich_job",
            f"/enrich {source_id}",
            "4.5.13_enrich_present.md",
        )

        # Apply enrichment
        run_test(
            "4.5.13b: /enrich (add implication)",
            "gateway.enrich_handler", "handle_enrich_job",
            f"/enrich {source_id} OpenClaw's architecture implies that personal agents need OAuth-level permission delegation, which current security models don't support. This is a cross-theme implication from autonomous_agents to ai_safety_and_alignment.",
            "4.5.13_enrich_apply.md",
        )
        verify_db(
            "User enrichment entries",
            "SELECT entity_type, entity_id, field, new_value, attribution FROM landscape_history WHERE attribution = 'user_enrichment' ORDER BY changed_at DESC LIMIT 5",
        )

    # ---------------------------------------------------------------
    # Step 4.5.14-15: Tier 3b re-run
    # ---------------------------------------------------------------
    if step in ("all", "4.5.14", "4.5.15", "tier3b"):
        from skills import SkillRegistry
        registry = SkillRegistry()

        # 4.5.14: /gaps
        gaps_skill = registry.skills.get("gaps")
        if gaps_skill:
            gaps_prompt = gaps_skill.prompt_text(strip_frontmatter=True)
            print(f"\n{'='*60}")
            print("TEST: 4.5.14: /gaps (re-run after beliefs/challenge/enrich)")
            print(f"{'='*60}")
            t0 = time.monotonic()
            try:
                # Pre-fetch gaps context
                from retrieval.landscape import (
                    get_over_optimistic_themes, get_blind_spot_bottlenecks,
                    get_untested_anticipations, get_incomplete_capabilities,
                    get_unlinked_themes, get_validation_backlog,
                    get_theme_source_counts, get_belief_coverage_gaps,
                    get_predictive_beliefs_without_anticipations,
                )
                context_parts = ["## Pre-Fetched Gap Analysis Data\n"]
                # Over-optimistic
                oo = get_over_optimistic_themes()
                context_parts.append(f"**Over-optimistic themes (caps but no lims):** {len(oo)}")
                for t in oo[:5]: context_parts.append(f"- {t['name']}: {t['capability_count']} caps, {t['limitation_count']} lims")
                # Blind spot bottlenecks
                bs = get_blind_spot_bottlenecks()
                context_parts.append(f"\n**Blind-spot bottlenecks (no active approaches):** {len(bs)}")
                for b in bs[:5]: context_parts.append(f"- {b['description'][:80]}")
                # Untested anticipations
                ua = get_untested_anticipations()
                context_parts.append(f"\n**Untested anticipations (60+ days, no evidence):** {len(ua)}")
                for a in ua[:5]: context_parts.append(f"- {a['prediction'][:80]}")
                # Belief coverage gaps
                bcg = get_belief_coverage_gaps()
                lc = bcg.get("low_confidence_gaps", [])
                uc = bcg.get("unchallenged_beliefs", [])
                context_parts.append(f"\n**Low-confidence beliefs:** {len(lc)}")
                context_parts.append(f"**Unchallenged high-confidence beliefs:** {len(uc)}")
                # Predictive without anticipations
                pwa = get_predictive_beliefs_without_anticipations()
                context_parts.append(f"\n**Predictive beliefs without anticipations:** {len(pwa)}")

                full_prompt = gaps_prompt + "\n\n---\n\n" + "\n".join(context_parts) + "\n\nGenerate the /gaps report from this data. Do NOT call any Python functions."
                progress("Running /gaps analysis...")
                result = executor.run_raw(full_prompt, session_id="gaps_tier3b", timeout=300)
                elapsed = time.monotonic() - t0
                print(f"\n--- Result ({elapsed:.1f}s) ---")
                print(result.text[:500] if result.text else "(empty)")
                if len(result.text or "") > 500:
                    print(f"... ({len(result.text)} chars total)")
                out = RESULTS_DIR / "4.5.14_gaps.md"
                out.write_text(result.text or "(empty)", encoding="utf-8")
                print(f"Saved to: {out}")
            except Exception as e:
                print(f"ERROR: {e}")
                import traceback; traceback.print_exc()

        # 4.5.15: /landscape autonomous_agents
        landscape_skill = registry.skills.get("landscape")
        if landscape_skill:
            print(f"\n{'='*60}")
            print("TEST: 4.5.15: /landscape autonomous_agents (re-run)")
            print(f"{'='*60}")
            t0 = time.monotonic()
            try:
                from retrieval.landscape import get_theme_state, get_consolidated_implications
                state = get_theme_state("autonomous_agents")
                theme = state.get("theme", {})

                # Build context
                parts = [f"## Theme: {theme.get('name', 'autonomous_agents')}\n"]
                parts.append(f"**State Summary:** {(theme.get('state_summary') or 'N/A')[:500]}")
                parts.append(f"**Velocity:** {theme.get('velocity', 'N/A')}")

                caps = state.get("capabilities", [])
                parts.append(f"\n**Capabilities ({len(caps)}):**")
                for c in caps[:8]: parts.append(f"- {c['description'][:100]} (maturity: {c.get('maturity','?')})")

                lims = state.get("limitations", [])
                parts.append(f"\n**Limitations ({len(lims)}):**")
                for l in lims[:8]: parts.append(f"- {l['description'][:100]} (severity: {l.get('severity','?')})")

                bns = state.get("bottlenecks", [])
                parts.append(f"\n**Bottlenecks ({len(bns)}):**")
                for b in bns[:5]: parts.append(f"- {b['description'][:100]} (horizon: {b.get('resolution_horizon','?')})")

                bts = state.get("breakthroughs", [])
                parts.append(f"\n**Recent Breakthroughs ({len(bts)}):**")
                for b in bts[:5]: parts.append(f"- {b['description'][:100]}")

                ants = state.get("anticipations", [])
                parts.append(f"\n**Open Anticipations ({len(ants)}):**")
                for a in ants[:5]: parts.append(f"- {a['prediction'][:100]}")

                imps = get_consolidated_implications("autonomous_agents")
                parts.append(f"\n**Cross-Theme Implications ({len(imps)}):**")
                for i in imps[:5]: parts.append(f"- {i['source_theme']} -> {i['target_theme']}: {i['top_implication'][:80]}")

                # Get beliefs for this theme
                from reading_app.db import get_beliefs_for_theme
                beliefs = get_beliefs_for_theme("autonomous_agents")
                parts.append(f"\n**Tracked Beliefs ({len(beliefs)}):**")
                for b in beliefs: parts.append(f"- {b['claim'][:100]} (conf: {b.get('confidence','?')})")

                landscape_prompt = landscape_skill.prompt_text(strip_frontmatter=True)
                full_prompt = landscape_prompt + "\n\n---\n\n" + "\n".join(parts) + "\n\nGenerate the landscape narrative from this pre-fetched data. Do NOT call any Python functions."
                progress("Running /landscape autonomous_agents...")
                result = executor.run_raw(full_prompt, session_id="landscape_tier3b", timeout=180)
                elapsed = time.monotonic() - t0
                print(f"\n--- Result ({elapsed:.1f}s) ---")
                print(result.text[:500] if result.text else "(empty)")
                if len(result.text or "") > 500:
                    print(f"... ({len(result.text)} chars total)")
                out = RESULTS_DIR / "4.5.15_landscape_agents_rerun.md"
                out.write_text(result.text or "(empty)", encoding="utf-8")
                print(f"Saved to: {out}")
            except Exception as e:
                print(f"ERROR: {e}")
                import traceback; traceback.print_exc()

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print(f"\n{'='*60}")
    print("TIER 3 VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {RESULTS_DIR}")

    # Show all result files
    for f in sorted(RESULTS_DIR.glob("4.5.1[1-3]*")):
        size = f.stat().st_size
        status = "OK" if size > 100 else "SMALL" if size > 0 else "EMPTY"
        print(f"  [{status:5s}] {f.name} ({size} bytes)")


if __name__ == "__main__":
    main()
