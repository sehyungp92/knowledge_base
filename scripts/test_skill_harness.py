"""Lightweight test harness for invoking gateway skill handlers directly.

Usage:
    python scripts/test_skill_harness.py <skill_name> "<text>" [--output <file>]

Example:
    python scripts/test_skill_harness.py landscape "/landscape autonomous_agents"
    python scripts/test_skill_harness.py ask "/ask What are the main limitations of AI agents?"
"""

from __future__ import annotations

import argparse
import importlib
import sys
import os
import re
import time

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from gateway.models import Event, Job


# Map skill names to (module_path, function_name)
HANDLER_MAP = {
    "landscape": ("gateway.landscape_handler", "handle_landscape_job"),
    "ask": ("gateway.ask_handler", "handle_ask_job"),
    "anticipate": ("gateway.anticipate_handler", "handle_anticipate_job"),
    "beliefs": ("gateway.beliefs_handler", "handle_beliefs_job"),
    "challenge": ("gateway.challenge_handler", "handle_challenge_job"),
    "changelog": ("gateway.changelog_handler", "handle_changelog_job"),
    "delete": ("gateway.delete_handler", "handle_delete_job"),
    "enrich": ("gateway.enrich_handler", "handle_enrich_job"),
    "ideas": ("gateway.ideas_handler", "handle_ideas_job"),
    "implications": ("gateway.implications_handler", "handle_implications_job"),
    "model": ("gateway.model_handler", "handle_model_job"),
    "next": ("gateway.next_handler", "handle_next_job"),
    "path": ("gateway.path_handler", "handle_path_job"),
    "provider": ("gateway.provider_handler", "handle_provider_job"),
    "reflect": ("gateway.reflect_handler", "handle_reflect_job"),
    "save": ("gateway.save_handler", "handle_save_job"),
    "status": ("gateway.status_handler", "handle_status_job"),
    "summarise": ("gateway.summarise_handler", "handle_summarise_job"),
    "news_digest": ("gateway.news_digest_handler", "handle_news_digest_job"),
    "news_weekly": ("gateway.news_weekly_handler", "handle_news_weekly_job"),
}

# Skills that need a queue object (model/provider/status handlers need it)
NEEDS_QUEUE = {"model", "provider", "status"}


def make_event(text: str) -> Event:
    return Event(
        type="message",
        payload={"text": text},
        source="test",
        chat_id="test_harness",
        id=0,
        created_at=time.time(),
    )


def make_job(skill: str) -> Job:
    return Job(
        event_id=0,
        skill=skill,
        id=0,
        status="processing",
        provider_id="claude",
    )


def get_config():
    from gateway.main import Config
    return Config()


def get_executor(config):
    from pathlib import Path
    from agents.executor import MultiBackendExecutor
    workspace = Path(__file__).resolve().parent.parent / "workspace"
    workspace.mkdir(exist_ok=True)
    return MultiBackendExecutor(workspace=workspace)


def main():
    parser = argparse.ArgumentParser(description="Test skill handler harness")
    parser.add_argument("skill", help="Skill name (e.g., landscape, ask, model)")
    parser.add_argument("text", help="Full command text (e.g., '/landscape autonomous_agents')")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    skill = args.skill
    text = args.text

    # Fix MSYS2/Git Bash path mangling: /command → C:/Program Files/Git/command
    # Also reverses URL mangling: https:// → https;\\, / → \
    if re.match(r'^[A-Z]:[/\\]Program Files[/\\]Git[/\\]', text):
        text = re.sub(r'^[A-Z]:[/\\]Program Files[/\\]Git[/\\]', '/', text)
        text = text.replace('\\', '/')
        text = text.replace(';//', '://')

    config = get_config()

    # Ensure DB pool is initialized for all handlers
    from reading_app.db import ensure_pool
    ensure_pool()

    if skill in HANDLER_MAP:
        # Direct handler path
        module_path, func_name = HANDLER_MAP[skill]
        mod = importlib.import_module(module_path)
        handler_fn = getattr(mod, func_name)

        event = make_event(text)
        job = make_job(skill)
        kwargs = {"on_progress": lambda s: print(f"[progress] {s}", file=sys.stderr)}

        executor = get_executor(config)
        if skill in NEEDS_QUEUE:
            from gateway.queue import Queue
            kwargs["queue"] = Queue()
        result = handler_fn(event, job, config, executor, **kwargs)
    else:
        # LLM-based skill path — load prompt from registry and run via executor
        from skills import SkillRegistry
        registry = SkillRegistry()
        if skill not in registry.skills:
            print(f"Unknown skill: {skill}")
            print(f"Direct handlers: {', '.join(sorted(HANDLER_MAP.keys()))}")
            print(f"LLM skills: {', '.join(sorted(registry.skills.keys()))}")
            sys.exit(1)
        sk = registry.skills[skill]
        skill_text = sk.prompt_text(strip_frontmatter=True)
        executor = get_executor(config)
        prompt = executor.build_prompt("message", {"text": text}, skill_text, "")
        er = executor.run_raw(prompt, timeout=max(sk.timeout, 120), model="sonnet")
        result = er.text if er.text else f"[No output. Return code: {er.return_code}, stderr: {er.stderr[:500] if er.stderr else 'none'}]"

    # For save/ingest operations, append representative claims for quality visibility
    if skill == "save":
        claims_appendix = _extract_claims_quality_sample(text)
        if claims_appendix:
            result += "\n\n" + claims_appendix

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(result)


def _extract_claims_quality_sample(command_text: str) -> str:
    """After a /save, fetch representative claims for quality review.

    Shows 5 claims: highest confidence, lowest confidence, a limitation claim,
    and 2 random, each with their evidence snippet.
    """
    # Try to extract source_id from the save result by checking the DB for recent ingests
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            # Get the most recently ingested source
            source = conn.execute(
                """SELECT id, title FROM sources
                   ORDER BY ingested_at DESC NULLS LAST
                   LIMIT 1"""
            ).fetchone()
            if not source:
                return ""

            source_id = source["id"]
            title = source.get("title", source_id)

            # Get representative claims: highest conf, lowest conf, limitation, random
            all_claims = conn.execute(
                """SELECT claim_text, claim_type, confidence, evidence_snippet,
                          section, evidence_type, evidence_validation
                   FROM claims WHERE source_id = %s
                   ORDER BY confidence DESC NULLS LAST""",
                (source_id,),
            ).fetchall()

            if not all_claims:
                return ""

            sample = []

            # Highest confidence
            sample.append(("Highest confidence", all_claims[0]))

            # Lowest confidence
            if len(all_claims) > 1:
                sample.append(("Lowest confidence", all_claims[-1]))

            # A limitation claim (if any)
            limitation = next(
                (c for c in all_claims
                 if "limitation" in (c.get("claim_type") or "").lower()
                 or "limitation" in (c.get("section") or "").lower()),
                None,
            )
            if limitation and limitation not in [s[1] for s in sample]:
                sample.append(("Limitation", limitation))

            # Fill remaining with evenly-spaced claims
            used = {id(s[1]) for s in sample}
            remaining = [c for c in all_claims if id(c) not in used]
            if remaining:
                step = max(1, len(remaining) // 3)
                for i in range(0, len(remaining), step):
                    if len(sample) >= 5:
                        break
                    sample.append(("Representative", remaining[i]))

            # Format output
            lines = [
                f"---\n**Claim Quality Sample** ({len(all_claims)} total claims from \"{title}\")\n"
            ]
            for label, claim in sample:
                conf = claim.get("confidence")
                conf_str = f"{conf:.2f}" if conf is not None else "?"
                ctype = claim.get("claim_type", "?")
                ev_val = claim.get("evidence_validation", "strict")
                val_badge = f" ⚠ relaxed" if ev_val == "relaxed" else ""
                lines.append(f"**[{label}]** ({ctype}, conf: {conf_str}{val_badge})")
                lines.append(f"  Claim: {(claim.get('claim_text') or '')[:200]}")
                evidence = claim.get("evidence_snippet", "")
                if evidence:
                    lines.append(f"  Evidence: \"{evidence[:200]}\"")
                lines.append("")

            return "\n".join(lines)
    except Exception as e:
        return f"(Claims quality sample unavailable: {str(e)[:100]})"


if __name__ == "__main__":
    main()
