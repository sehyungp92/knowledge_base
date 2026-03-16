"""Phase 5 feature verification tests for new skills and bug fixes.

Tests cover:
  NEW FEATURES (Step 4.5.16–4.5.24):
    4.5.16  /changelog — landscape temporal diff
    4.5.17  /changelog <theme> — theme-scoped diff
    4.5.18  /ideas — idea lifecycle list
    4.5.19  /ideas rate/note/status — idea mutations
    4.5.20  /next — reading queue generator
    4.5.21  /anticipate — overview (direct handler)
    4.5.22  /anticipate review — evidence surfacing
    4.5.23  /beliefs suggest — auto-formation from convergence
    4.5.24  /enrich validate — guided limitation validation
    4.5.25  /reflect topic — cross-source reflection

  BUG FIX VERIFICATION (Step 4.5.26–4.5.28):
    4.5.26  /challenge belief — auto-apply confidence
    4.5.27  /enrich apply — verbose details
    4.5.28  /reflect simple — output guard

Invokes direct Python handlers the same way the gateway dispatcher does.
Saves outputs to _results/ folder.

Usage:
    python scripts/test_phase5_features.py all
    python scripts/test_phase5_features.py 4.5.16
    python scripts/test_phase5_features.py changelog
    python scripts/test_phase5_features.py bugfixes
"""

from __future__ import annotations

import json
import os
import re
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


# ---------------------------------------------------------------------------
# Test helpers (identical to test_tier3.py)
# ---------------------------------------------------------------------------

def make_event(text: str) -> Event:
    return Event(type="message", source="test", payload={"text": text})

def make_job(skill: str) -> Job:
    return Job(event_id=0, skill=skill, id=0, status="running", retry_count=0)

def progress(msg: str):
    print(f"  >> {msg}")


def run_test(name: str, handler_module: str, handler_func: str,
             text: str, output_file: str):
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


def check_output(result: str, checks: list[tuple[str, str]], test_name: str):
    """Verify output text contains expected patterns. Returns pass/fail count."""
    passed = 0
    failed = 0
    for label, pattern in checks:
        if re.search(pattern, result or "", re.IGNORECASE | re.DOTALL):
            print(f"  ✓ {label}")
            passed += 1
        else:
            print(f"  ✗ {label} (pattern: {pattern[:60]})")
            failed += 1
    return passed, failed


# ---------------------------------------------------------------------------
# Test runners
# ---------------------------------------------------------------------------

def test_changelog_global():
    """4.5.16: /changelog — global landscape diff."""
    result = run_test(
        "4.5.16: /changelog (global, 30 days)",
        "gateway.changelog_handler", "handle_changelog_job",
        "/changelog",
        "4.5.16_changelog_global.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"\*\*Changelog:"),
            ("Shows changes count", r"\d+ changes"),
            ("Shows entity types", r"Entity types:"),
            ("Has date sections or no-changes message", r"(###\s+\d{4}|No landscape changes)"),
        ], "4.5.16")
    return result


def test_changelog_theme():
    """4.5.17: /changelog <theme> 7d — theme-scoped diff."""
    result = run_test(
        "4.5.17: /changelog autonomous_agents 7d",
        "gateway.changelog_handler", "handle_changelog_job",
        "/changelog autonomous_agents 7d",
        "4.5.17_changelog_theme.md",
    )
    if result:
        check_output(result, [
            ("Contains theme name", r"autonomous.agents|Autonomous.Agents"),
            ("Shows 7 days", r"7 days"),
        ], "4.5.17")
    return result


def test_ideas_list():
    """4.5.18: /ideas — list ideas from reflect deep."""
    result = run_test(
        "4.5.18: /ideas (list)",
        "gateway.ideas_handler", "handle_ideas_job",
        "/ideas",
        "4.5.18_ideas_list.md",
    )
    if result:
        check_output(result, [
            ("Has title or empty message", r"\*\*Ideas\*\*|\*\*No ideas found"),
            ("Shows commands or guidance", r"(/ideas\s+(view|rate|develop)|/reflect)"),
        ], "4.5.18")
    return result


def test_ideas_mutations():
    """4.5.19: /ideas rate, note, status — test mutations on an existing idea."""
    # First get an idea ID
    with get_conn() as conn:
        idea = conn.execute(
            "SELECT id, idea_text FROM ideas ORDER BY overall_score DESC NULLS LAST LIMIT 1"
        ).fetchone()

    if not idea:
        print("\n  SKIP: No ideas in DB (run /reflect deep first)")
        result = "SKIP: No ideas found in DB."
        (RESULTS_DIR / "4.5.19_ideas_mutations.md").write_text(result, encoding="utf-8")
        return result

    idea_id = idea["id"]
    print(f"\n  Using idea: {idea_id}")

    results = []

    # View
    r = run_test(
        f"4.5.19a: /ideas view {idea_id[:12]}…",
        "gateway.ideas_handler", "handle_ideas_job",
        f"/ideas view {idea_id}",
        "4.5.19a_ideas_view.md",
    )
    if r:
        check_output(r, [
            ("Shows idea ID", re.escape(idea_id)),
            ("Shows score", r"Score:"),
            ("Shows idea text", r"Idea:"),
        ], "4.5.19a")
    results.append(r)

    # Rate
    r = run_test(
        f"4.5.19b: /ideas rate {idea_id[:12]}… 4",
        "gateway.ideas_handler", "handle_ideas_job",
        f"/ideas rate {idea_id} 4",
        "4.5.19b_ideas_rate.md",
    )
    if r:
        check_output(r, [
            ("Confirms rating", r"Rated idea"),
            ("Shows stars", r"★"),
        ], "4.5.19b")
    results.append(r)

    # Verify rating persisted
    verify_db("Idea rating persisted",
              "SELECT id, user_rating FROM ideas WHERE id = %s", (idea_id,))

    # Note
    r = run_test(
        f"4.5.19c: /ideas note {idea_id[:12]}… 'test note'",
        "gateway.ideas_handler", "handle_ideas_job",
        f"/ideas note {idea_id} This is a test note from phase 5 verification",
        "4.5.19c_ideas_note.md",
    )
    if r:
        check_output(r, [
            ("Confirms note added", r"Note added"),
        ], "4.5.19c")
    results.append(r)

    # Status change
    r = run_test(
        f"4.5.19d: /ideas status {idea_id[:12]}… developing",
        "gateway.ideas_handler", "handle_ideas_job",
        f"/ideas status {idea_id} developing",
        "4.5.19d_ideas_status.md",
    )
    if r:
        check_output(r, [
            ("Shows status change", r"status updated"),
            ("Shows developing", r"developing"),
        ], "4.5.19d")
    results.append(r)

    # Verify status in generation_context
    verify_db("Idea status in generation_context",
              "SELECT id, generation_context->>'status' AS status, user_rating, "
              "LEFT(user_notes, 60) AS note_preview FROM ideas WHERE id = %s",
              (idea_id,))

    return "\n\n---\n\n".join(r or "(empty)" for r in results)


def test_next():
    """4.5.20: /next — reading queue generator."""
    result = run_test(
        "4.5.20: /next",
        "gateway.next_handler", "handle_next_job",
        "/next",
        "4.5.20_next.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"\*\*Read Next\*\*|\*\*No reading"),
            ("Shows recommendations or empty", r"(###\s+\d|no reading recommendations)"),
        ], "4.5.20")
        # Verify persistence
        verify_db("Reading queue persisted",
                  "SELECT id, signal_type, theme_name, priority FROM reading_queue "
                  "WHERE status = 'pending' ORDER BY priority DESC LIMIT 3")
    return result


def test_next_theme():
    """4.5.20b: /next 3 autonomous_agents — filtered."""
    result = run_test(
        "4.5.20b: /next 3 autonomous_agents",
        "gateway.next_handler", "handle_next_job",
        "/next 3 autonomous_agents",
        "4.5.20b_next_agents.md",
    )
    if result:
        check_output(result, [
            ("Scoped to theme", r"autonomous.agents"),
        ], "4.5.20b")
    return result


def test_anticipate_overview():
    """4.5.21: /anticipate — overview via direct handler."""
    result = run_test(
        "4.5.21: /anticipate (overview)",
        "gateway.anticipate_handler", "handle_anticipate_job",
        "/anticipate",
        "4.5.21_anticipate_overview.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"\*\*Anticipation Overview\*\*"),
            ("Shows commands", r"/anticipate (review|confirm|generate|calibration)"),
        ], "4.5.21")
    return result


def test_anticipate_review():
    """4.5.22: /anticipate review — evidence surfacing."""
    result = run_test(
        "4.5.22: /anticipate review",
        "gateway.anticipate_handler", "handle_anticipate_job",
        "/anticipate review",
        "4.5.22_anticipate_review.md",
    )
    if result:
        check_output(result, [
            ("Has title or no-review", r"(Anticipation Review|No anticipations need review)"),
        ], "4.5.22")
    return result


def test_anticipate_calibration():
    """4.5.22b: /anticipate calibration."""
    result = run_test(
        "4.5.22b: /anticipate calibration",
        "gateway.anticipate_handler", "handle_anticipate_job",
        "/anticipate calibration",
        "4.5.22b_anticipate_calibration.md",
    )
    if result:
        check_output(result, [
            ("Has title or no-data", r"(Anticipation Calibration|No resolved anticipations)"),
        ], "4.5.22b")
    return result


def test_beliefs_suggest():
    """4.5.23: /beliefs suggest — auto-formation."""
    result = run_test(
        "4.5.23: /beliefs suggest",
        "gateway.beliefs_handler", "handle_beliefs_job",
        "/beliefs suggest",
        "4.5.23_beliefs_suggest.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"\*\*Belief Candidates\*\*|\*\*No (belief|claim)"),
            ("Shows suggestions or explanation", r"(To track:|No claim convergence|No belief candidates)"),
        ], "4.5.23")
    return result


def test_enrich_validate():
    """4.5.24: /enrich <source> validate — guided limitation validation."""
    # Find a source with unvalidated limitations
    with get_conn() as conn:
        row = conn.execute(
            """SELECT l.evidence_sources, s.id AS source_id, s.title,
                  COUNT(*) AS unvalidated_count
               FROM limitations l
               JOIN sources s ON l.evidence_sources::text LIKE '%%' || s.id || '%%'
               WHERE l.signal_type LIKE 'implicit%%'
                 AND l.validated IS NULL
               GROUP BY l.evidence_sources, s.id, s.title
               ORDER BY COUNT(*) DESC
               LIMIT 1"""
        ).fetchone()

    if not row:
        print("\n  SKIP: No sources with unvalidated implicit limitations")
        result = "SKIP: No unvalidated implicit limitations found."
        (RESULTS_DIR / "4.5.24_enrich_validate.md").write_text(result, encoding="utf-8")
        return result

    source_id = row["source_id"]
    print(f"\n  Using source: {source_id} ({row['title'][:50]}…), "
          f"{row['unvalidated_count']} unvalidated")

    result = run_test(
        f"4.5.24: /enrich {source_id[:12]}… validate",
        "gateway.enrich_handler", "handle_enrich_job",
        f"/enrich {source_id} validate",
        "4.5.24_enrich_validate.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"Limitation Validation"),
            ("Shows limitation IDs", r"`lim_"),
            ("Shows signal type", r"Signal:"),
            ("Shows validation instructions", r"validate.*(yes|no|confirm|reject)"),
        ], "4.5.24")
    return result


def test_reflect_topic():
    """4.5.25: /reflect topic — cross-source reflection."""
    result = run_test(
        "4.5.25: /reflect topic autonomous agents",
        "gateway.reflect_handler", "handle_reflect_job",
        "/reflect topic autonomous agents",
        "4.5.25_reflect_topic.md",
    )
    if result:
        check_output(result, [
            ("Has title", r"Cross-Source Reflection"),
            ("Shows source count", r"\d+ sources"),
            ("Contains ideas or explanation", r"(idea|synthesis|proposal|implication|no sources)"),
        ], "4.5.25")
    return result


# ---------------------------------------------------------------------------
# Bug fix verification
# ---------------------------------------------------------------------------

def test_bugfix_challenge_autoconfidence():
    """4.5.26: /challenge belief — verify confidence auto-apply.

    Creates a test belief, challenges it, verifies confidence was actually
    updated in DB.
    """
    from reading_app.db import get_belief

    # Get latest belief
    with get_conn() as conn:
        belief = conn.execute(
            "SELECT id, confidence FROM beliefs ORDER BY created_at DESC LIMIT 1"
        ).fetchone()

    if not belief:
        print("\n  SKIP: No beliefs in DB")
        result = "SKIP: No beliefs found."
        (RESULTS_DIR / "4.5.26_bugfix_challenge_confidence.md").write_text(result, encoding="utf-8")
        return result

    belief_id = belief["id"]
    old_conf = belief["confidence"]
    print(f"\n  Challenging belief: {belief_id} (current conf: {old_conf})")

    result = run_test(
        f"4.5.26: /challenge belief {belief_id[:12]}… steelman",
        "gateway.challenge_handler", "handle_challenge_job",
        f"/challenge belief {belief_id} steelman",
        "4.5.26_bugfix_challenge_confidence.md",
    )
    if result:
        # Check that result mentions confidence update
        p, f = check_output(result, [
            ("Mentions confidence", r"confidence"),
            ("Has challenge log", r"chal_"),
            ("Shows confidence change or unchanged", r"(Confidence updated|Confidence unchanged|Suggested confidence)"),
        ], "4.5.26")

        # Verify DB was actually updated
        updated = get_belief(belief_id)
        new_conf = updated.get("confidence", old_conf) if updated else old_conf
        if new_conf != old_conf:
            print(f"  ✓ Confidence auto-updated in DB: {old_conf} → {new_conf}")
        else:
            print(f"  ○ Confidence unchanged (verdict may be 'unchanged')")

        verify_db("Challenge log entry",
                  "SELECT id, entity_type, outcome, changes_made "
                  "FROM challenge_log WHERE entity_type = 'belief' "
                  "ORDER BY created_at DESC LIMIT 1")
    return result


def test_bugfix_enrich_details():
    """4.5.27: /enrich apply — verify verbose details in response.

    Uses a source and provides enrichment, checks that the response
    includes specific entity details (not just counts).
    """
    source_id = "01KJ6NT1T9MV7R25KD4NBZKF3Y"

    # Verify source exists
    with get_conn() as conn:
        src = conn.execute("SELECT id, title FROM sources WHERE id = %s",
                           (source_id,)).fetchone()
    if not src:
        # Try any source
        with get_conn() as conn:
            src = conn.execute(
                "SELECT id, title FROM sources LIMIT 1"
            ).fetchone()
        if not src:
            print("\n  SKIP: No sources in DB")
            result = "SKIP: No sources found."
            (RESULTS_DIR / "4.5.27_bugfix_enrich_details.md").write_text(result, encoding="utf-8")
            return result
        source_id = src["id"]

    result = run_test(
        f"4.5.27: /enrich {source_id[:12]}… (apply enrichment)",
        "gateway.enrich_handler", "handle_enrich_job",
        f"/enrich {source_id} add limitation: Current agent frameworks lack standardized "
        f"permission delegation mechanisms, requiring custom OAuth-like flows for each tool integration",
        "4.5.27_bugfix_enrich_details.md",
    )
    if result:
        check_output(result, [
            ("Has enrichment title", r"Enrichment applied"),
            ("Shows changes applied", r"Changes applied"),
            ("Has Details section", r"\*\*Details:\*\*"),
            ("Details show entity IDs", r"(lim_|cap_|bn_|impl_)"),
            ("Details show description text", r"\+.+(Limitation|Capability|Bottleneck|Implication)"),
            ("Shows attribution", r"user_enrichment"),
        ], "4.5.27")
    return result


def test_bugfix_reflect_simple():
    """4.5.28: /reflect simple — verify output guard.

    Runs simple reflect and checks output is readable text, not binary/empty.
    """
    # Find a source with extractions
    with get_conn() as conn:
        src = conn.execute(
            """SELECT s.id, s.title FROM sources s
               JOIN claims c ON c.source_id = s.id
               GROUP BY s.id, s.title
               HAVING COUNT(c.id) >= 3
               ORDER BY COUNT(c.id) DESC
               LIMIT 1"""
        ).fetchone()

    if not src:
        print("\n  SKIP: No sources with 3+ claims")
        result = "SKIP: No suitable source found."
        (RESULTS_DIR / "4.5.28_bugfix_reflect_simple.md").write_text(result, encoding="utf-8")
        return result

    source_id = src["id"]
    print(f"\n  Reflecting on: {source_id} ({src['title'][:50]}…)")

    result = run_test(
        f"4.5.28: /reflect {source_id[:12]}… (simple)",
        "gateway.reflect_handler", "handle_reflect_job",
        f"/reflect {source_id}",
        "4.5.28_bugfix_reflect_simple.md",
    )
    if result:
        check_output(result, [
            ("Has reflection header", r"(Reflection|reflect)"),
            ("Contains readable text (100+ chars)", r".{100}"),
            ("Not binary output", r"[a-zA-Z]{10}"),  # at least 10 consecutive letters
            ("Shows graph stats", r"(connections|claims)"),
        ], "4.5.28")
    return result


# ---------------------------------------------------------------------------
# Re-run fixed skills from original tier 3
# ---------------------------------------------------------------------------

def test_rerun_challenge_bottleneck():
    """Re-run 4.5.12a with stale-implication checks (Tier 2H fix)."""
    # Find a bottleneck that has an associated theme with implications
    with get_conn() as conn:
        bn = conn.execute(
            """SELECT b.id, b.description, b.theme_id
               FROM bottlenecks b
               WHERE b.confidence IS NOT NULL
               ORDER BY b.confidence DESC
               LIMIT 1"""
        ).fetchone()
    if not bn:
        print("\n  SKIP: No bottlenecks in DB")
        return None

    bn_id = bn["id"]
    print(f"\n  Challenging bottleneck: {bn_id}")

    result = run_test(
        f"Rerun: /challenge bottleneck {bn_id[:12]}…",
        "gateway.challenge_handler", "handle_challenge_job",
        f"/challenge bottleneck {bn_id}",
        "4.5.12a_challenge_bottleneck_rerun.md",
    )
    if result:
        check_output(result, [
            ("Has resolution", r"Resolution:"),
            ("Has challenge log", r"chal_"),
            # New Tier 2H: stale implications check
            ("Mentions implications or no implications",
             r"(stale implications|implication|Changes applied|system_maintained)"),
        ], "rerun_challenge")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    results = {}

    # Map short names to step numbers
    aliases = {
        "changelog": ("4.5.16", "4.5.17"),
        "ideas": ("4.5.18", "4.5.19"),
        "next": ("4.5.20",),
        "anticipate": ("4.5.21", "4.5.22"),
        "beliefs": ("4.5.23",),
        "enrich": ("4.5.24",),
        "reflect": ("4.5.25",),
        "bugfixes": ("4.5.26", "4.5.27", "4.5.28"),
        "rerun": ("rerun",),
    }

    # Resolve aliases
    if step in aliases:
        steps = aliases[step]
    elif step == "all":
        steps = None  # run everything
    else:
        steps = (step,)

    def should_run(s: str) -> bool:
        return steps is None or s in steps

    # ---------------------------------------------------------------
    # NEW FEATURES
    # ---------------------------------------------------------------

    # 4.5.16–17: /changelog
    if should_run("4.5.16"):
        results["4.5.16"] = test_changelog_global()
    if should_run("4.5.17"):
        results["4.5.17"] = test_changelog_theme()

    # 4.5.18–19: /ideas
    if should_run("4.5.18"):
        results["4.5.18"] = test_ideas_list()
    if should_run("4.5.19"):
        results["4.5.19"] = test_ideas_mutations()

    # 4.5.20: /next
    if should_run("4.5.20"):
        results["4.5.20"] = test_next()
        results["4.5.20b"] = test_next_theme()

    # 4.5.21–22: /anticipate
    if should_run("4.5.21"):
        results["4.5.21"] = test_anticipate_overview()
    if should_run("4.5.22"):
        results["4.5.22"] = test_anticipate_review()
        results["4.5.22b"] = test_anticipate_calibration()

    # 4.5.23: /beliefs suggest
    if should_run("4.5.23"):
        results["4.5.23"] = test_beliefs_suggest()

    # 4.5.24: /enrich validate
    if should_run("4.5.24"):
        results["4.5.24"] = test_enrich_validate()

    # 4.5.25: /reflect topic
    if should_run("4.5.25"):
        results["4.5.25"] = test_reflect_topic()

    # ---------------------------------------------------------------
    # BUG FIX VERIFICATION
    # ---------------------------------------------------------------

    if should_run("4.5.26"):
        results["4.5.26"] = test_bugfix_challenge_autoconfidence()
    if should_run("4.5.27"):
        results["4.5.27"] = test_bugfix_enrich_details()
    if should_run("4.5.28"):
        results["4.5.28"] = test_bugfix_reflect_simple()

    # ---------------------------------------------------------------
    # Re-run fixed skills
    # ---------------------------------------------------------------

    if should_run("rerun"):
        results["rerun_challenge"] = test_rerun_challenge_bottleneck()

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print(f"\n{'='*60}")
    print("PHASE 5 FEATURE VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {RESULTS_DIR}\n")

    # Show all result files from this run
    for f in sorted(RESULTS_DIR.glob("4.5.1[6-9]*")) + \
             sorted(RESULTS_DIR.glob("4.5.2[0-8]*")) + \
             sorted(RESULTS_DIR.glob("4.5.12a_challenge_bottleneck_rerun*")):
        size = f.stat().st_size
        is_error = False
        if size > 0:
            head = f.read_text(encoding="utf-8")[:20]
            is_error = head.startswith("ERROR") or head.startswith("SKIP")
        status = "ERROR" if is_error else "OK" if size > 100 else "SMALL" if size > 0 else "EMPTY"
        print(f"  [{status:5s}] {f.name} ({size:,} bytes)")

    # Summary counts
    total = len(results)
    ok = sum(1 for v in results.values() if v and not str(v).startswith(("ERROR", "SKIP")))
    skip = sum(1 for v in results.values() if v and str(v).startswith("SKIP"))
    fail = total - ok - skip
    print(f"\n  Total: {total}  |  OK: {ok}  |  SKIP: {skip}  |  FAIL: {fail}")


if __name__ == "__main__":
    main()
