"""Regenerate deep summaries for sources that have placeholder content.

Placeholder deep summaries occur when an upstream API limit message (e.g.
"You've hit your limit · resets 12am") was saved as the final artifact
instead of a real summary.  This script detects those placeholders and
re-runs the deep summarisation step.

By default, uses the Claude CLI (Max subscription — no API key needed).
Falls back to OpenRouter or Anthropic API if API keys are configured.

Usage (from the project root):
    PYTHONPATH=. python -m scripts.regenerate_deep_summaries --dry-run
    PYTHONPATH=. python -m scripts.regenerate_deep_summaries --limit 5
    PYTHONPATH=. python -m scripts.regenerate_deep_summaries
    PYTHONPATH=. python -m scripts.regenerate_deep_summaries --resume
    PYTHONPATH=. python -m scripts.regenerate_deep_summaries --ids 01KJTNZS7X36EGSKTVH7B5S18M 01KJTP54EYE9CBWV7A593AFAQP

Backend priority (first available wins):
    1. Claude CLI (Max subscription) — default, no API key needed
    2. OPENROUTER_API_KEY — if set in .env
    3. ANTHROPIC_API_KEY  — if set in .env or environment

Options:
    --dry-run     Print what would be processed without making any API calls
    --limit N     Process at most N sources
    --resume      Skip sources that already have a non-placeholder summary
    --ids ...     Process only the specified source IDs
    --workers N   Number of concurrent API workers (default: 3)
    --delay F     Seconds between submissions per worker (default: 0.5)
    --verbose     Debug logging
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx
import yaml

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "library"
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "regenerate_deep_summaries_progress.json"

# ── Placeholder detection ─────────────────────────────────────────────────────

PLACEHOLDER_PATTERNS = [
    r"you'?ve hit your limit",
    r"resets \d+(am|pm)",
    r"summary (generation failed|pending)",
    r"summary pending",
    r"failed to generate",
    r"rate.?limit",
    r"token limit",
    r"context.?length",
    r"overloaded",
    r"try again",
    r"something went wrong",
]
_PLACEHOLDER_RE = re.compile("|".join(PLACEHOLDER_PATTERNS), re.IGNORECASE)

# Minimum length for a real summary (placeholders are tiny)
MIN_REAL_SUMMARY_CHARS = 500

# The full list of 147 source IDs identified as having placeholder summaries
# (from docs/bulk-ingestion-recovery-evaluation-2026-03-10.md)
PLACEHOLDER_SOURCE_IDS: list[str] = [
    "01KJTNZS7X36EGSKTVH7B5S18M",
    "01KJTP54EYE9CBWV7A593AFAQP",
    "01KJTP56NVHW0GKJH3XQCG4E4V",
    "01KJTP7WMBW5WAB4NJAB1ESNTJ",
    "01KJTPAM3DXFNX3FEHJJTZ73H3",
    "01KJTPB47QAEMCV664AH1X89Y6",
    "01KJTPC0T74FVTRCTH3Q6YM2XC",
    "01KJTPFD62H29TJN51149EYX48",
    "01KJTPFVK63FP9BRNCF5F7XXC2",
    "01KJTPGRRAEH18W4SK0C0J6SEV",
    "01KJTPMJBF37SDX28VSNECG0AW",
    "01KJTPP5WBNZNR9WY0VMZ7TH3T",
    "01KJTPV81QCQHFFQ4QGCPKJ8FY",
    "01KJTPVSWTK7XQS7HT1TQQVXV2",
    "01KJTPVV117TGWN29DZEAS90WA",
    "01KJTQ0EQT3NPZSQAZ4D1D8SJA",
    "01KJTQ0XQRB50VSN951C5WB06K",
    "01KJTQ0YV3DYY4VZD2DA8XQWKX",
    "01KJTQ65VXMV31FEDTS7ZXS8VH",
    "01KJTQ6SB0CMGZ7EKYGMYAWPGD",
    "01KJTQ74E7CE1V0S09YFQEF1Q3",
    "01KJTQCEKYJAG3872TW79TNCZ8",
    "01KJTQCH1TD2GP3Y316YC5PX06",
    "01KJTQD302SP6FG6TY60GF5Q1E",
    "01KJTQH65719Z4P50D125AY4H2",
    "01KJTQH6AARJQYQXWEP3E5GY52",
    "01KJTQH85KRGRP02JGFVY2ZZF6",
    "01KJTQRK4149XWRK6QFSAHABQX",
    "01KJTQRXBY5D86ATF1V7EGZ234",
    "01KJTQSWGFZP6G4KFH7FXBA089",
    "01KJV31KSHB04ZMJ4EYSDJBXJ8",
    "01KJV3AME561KWT5RJ1EJ0BTQ3",
    "01KJV3DVFC97VTBMSKRB726WDH",
    "01KJV3EHT79TRZC43MWGV8AFJ9",
    "01KJV3G6RYWC5JM8X47AK9AAGE",
    "01KJV3M3CCRCTJ0M3XV0TM1W6Y",
    "01KJV3MZFWPT1XMRZ5BZYQ0DMX",
    "01KJV3PQ9W8J5XF8VBCBBYZEF3",
    "01KJV3VT1CZCW1CH2F11Y2B6ND",
    "01KJV3W9QTWHPKY0X75EST48R9",
    "01KJV3X90H49CTVN35T1QDQR8V",
    "01KJV42M0KB822AY266HGWP4JD",
    "01KJV42RE16RXA64ZVX352JNJ0",
    "01KJV44APF5CB8BG6AH8428PA3",
    "01KJV47G2KX4WPZ9E3Y2JY5AF1",
    "01KJV47KDZ75MQ27779QTQTGET",
    "01KJV49W0K92F6SQQ3HMJTR25N",
    "01KJV4D04E2B7T3FE86HZTW793",
    "01KJV4D5YXR99VW5J24NP6VPEV",
    "01KJV4HRBK6JRFK1M5EVM7SWP9",
    "01KJV4KX85J6NJAA4F3RAMSYRT",
    "01KJV4M1H37QFTG0NF996MPAA3",
    "01KJV4QZ2D36W4SHVYMB30SQEQ",
    "01KJV4T8S3Z42W7X5WDZ4VHT1R",
    "01KJV4TENFJVB1SFDHWQ7S13DB",
    "01KJV4YYANBM1GBBMZN5JZ41KC",
    "01KJV50FH1MQXMHQ5PN1HY1V5H",
    "01KJV50MCDN3MJA7NSEB9CDW07",
    "01KJV54RZQPDJQRT35JX596THH",
    "01KJV56Z979BYNF24090F4GS3V",
    "01KJV56ZJP3YQ2YAG3JP5SXGQ9",
    "01KJV5B2QGE5H6X8PHDC4VKPV5",
    "01KJV5D2Z7MBVHR0KNHYB9AWNN",
    "01KJV5E1EBTAMS77SPACEPGAMJ",
    "01KJV5GK45PQ35EM1MKMTW3S3D",
    "01KJV5HWSHN2WAY8MNS8DJ7GGR",
    "01KJV5MK13QFXGWZX2B14E1256",
    "01KJV5S7TQ43GW6XHHXNQ6EFCD",
    "01KJV5SBG07KYAVYZW3MP8Q5PK",
    "01KJV5VMCP73BDWGE27RDDZF82",
    "01KJV5Z0M13PSHR7W5AF96FMPP",
    "01KJV5Z47180HNS6GWHJ322R11",
    "01KJV61P523MA947YC2AG7ZZ2Y",
    "01KJV64ZDFQ7S86XPVP6FNANGM",
    "01KJV65FZDWMAWMC6AV3HP5XFS",
    "01KJV68FPFQGPKRY2YQEF12W1Z",
    "01KJV6C0D1QTS98FMWFF8MZ02H",
    "01KJV6C78WQY03ZNVYQNK4HSNJ",
    "01KJV6G030GM66QCNBBZCETGSN",
    "01KJV6J7A4PJ91RSCRYNM08706",
    "01KJV6JNEC6GFA7ADGS68H01C6",
    "01KJV6PJWCZR91CR34XBKX2QC3",
    "01KJV6RRM0P2ZKE7JH4GXYJTWQ",
    "01KJV6RXXKMVXC5S8G3B55E8Y3",
    "01KJV6X74JDVGQFRCVXY0381BG",
    "01KJV6YYQP486TG5V2MHN93FJ1",
    "01KJV6ZWE5FB28K6MXQ6G4S161",
    "01KJV749E6WKMFMYWCX4C8G0XN",
    "01KJV75D184XZYHHEGQC0R3Z9X",
    "01KJV75HGRX7X4V2Y5C4QMP3PR",
    "01KJV79X7AQ5A1HM6FJ7H94JEY",
    "01KJV7CCFG6EWQVMGT0J196AVQ",
    "01KJV7DD3SM8YFQ5FA54VAY8AJ",
    "01KJV7N48DXDR5PVV35ZAP2N82",
    "01KJV7NM6AWC5CXT3SRS8DRN77",
    "01KJV7PXBQFTHEVGHDCGE868Q0",
    "01KJV7TRY28HAYF81PCXPPZCAW",
    "01KJV7V9DKPNV4479NX1BZSD1S",
    "01KJV7XNNNZZKZQZ5ZYP58GQ2V",
    "01KJV8271TDJ2R7E09R133E9V0",
    "01KJV83GN1RMMXTNYQWH3W34F5",
    "01KJV84KVSHNA6GM9MPCTDT8Q5",
    "01KJV8790RPPM2TQYQAXJ37F8K",
    "01KJV89Q4XJ3GHGFF55XY78V0D",
    "01KJV8BD2M08NZNP5XVEDCJ3KC",
    "01KJV8DVH3CJGCY00XAEE8YT2P",
    "01KJV8HGEPZYBJ5JXYBKCNJR3W",
    "01KJV8JK292KN8R7YPV9Y8P533",
    "01KJV8MTT26XS883PR5T1B9DDN",
    "01KJV8RNT6FBW0VTJM3BEEZ7J9",
    "01KJV8TCC8ZC7V7N7J8K8CYWTX",
    "01KJV8WEM4N2QDRN4NSWYE8XX1",
    "01KJV8YY98H1JVRFWY0MPHRY2F",
    "01KJV8ZDJ2H3FJFSRW52DE18X7",
    # Videos / podcasts
    "01KJVJ4GHWQJ4E9T3EKKD6DZAG",
    "01KJVJSX48VT7YXSTKZWDHE8PK",
    "01KJVKAKDJCQKZ7MT9P788V9NE",
    "01KJVKQCHAW52432VG8DSK3X0Q",
    "01KJVM69GCN7QYSPPE2KFMZ0Y5",
    "01KJVMA9D5RWMZX4M4V63DP5Q5",
    "01KJVMZ5JN297P9C62F7TWE66Q",
    "01KJVN12YGX8RAPPKMD78XE889",
    "01KJVNDJDQGM250BPX1Y2V8GBE",
    "01KJVNEG9Q5ACG8Q4DVQCMHBBT",
    "01KJVP2MKSVAYJF4F716NXXEA2",
    "01KJVPQYT8FQG5P4E0Q2C5TQSB",
    "01KJVQ7KAHS4EZYYEFFQR2Q2QR",
    "01KJVQ9TRDYXW6XS2EBHS2CGS7",
    "01KJVQZ7YX1N9TKVXRTVC768TN",
    "01KJVR0B99DNB238SCFEE07RYH",
    "01KJVR2WJ1ZQPBM0QNT2P4DPK0",
    "01KJVR7GAMPTJ34WZSTP6K1VC1",
    "01KJVRC3JX821XQE4V2NJEHFN1",
    "01KJVRMEM42XRWXZK83SHG7C2R",
    "01KJVRQP8RVNXWK6W8H42CAQ4X",
    "01KJVRTAEMF1MPY6WT7CJTMG8D",
    "01KJVRVSPK1Y9D0ZHTMTTNNXEC",
    "01KJVS00V26Z39NDSVB07QJT1D",
    "01KJVS330Y43TH4W93FNY7NB65",
    "01KJVS64WBC54M2T10FRNC2E0G",
    "01KJVSF4MB346QV6T275HAV1HA",
    "01KJVSGCXW0PSCS647AEFRRCPS",
    "01KJVSM49BGZ5XDSQ5EBPJ71WE",
    "01KJVV7HTPJHZ7F7Y3VMSAQT45",
    "01KJVVA0Q269HQCAFH3CZYQXE5",
    "01KJVVDA1FXWKWMM3JTRR2704T",
    "01KJVVDN9728146YK7HQXCNGA0",
]


# ── Progress tracking ─────────────────────────────────────────────────────────

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            text = PROGRESS_FILE.read_text(encoding="utf-8").strip()
            if text:
                return json.loads(text)
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupted progress file, resetting")
    return {"completed": [], "errors": []}


def save_progress(progress: dict) -> None:
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress, indent=2, default=str), encoding="utf-8")
    tmp.replace(PROGRESS_FILE)


# ── Placeholder detection ─────────────────────────────────────────────────────

def is_placeholder(summary_path: Path) -> tuple[bool, str]:
    """Return (is_placeholder, reason)."""
    if not summary_path.exists():
        return True, "file missing"
    try:
        text = summary_path.read_text(encoding="utf-8").strip()
    except OSError as e:
        return True, f"read error: {e}"

    if len(text) < MIN_REAL_SUMMARY_CHARS:
        return True, f"too short ({len(text)} chars)"

    match = _PLACEHOLDER_RE.search(text[:2000])
    if match:
        return True, f"placeholder pattern: '{match.group()[:60]}'"

    return False, "ok"


# ── Source metadata loading ───────────────────────────────────────────────────

def load_meta(source_id: str) -> dict:
    meta_path = LIBRARY_PATH / source_id / "meta.yaml"
    if not meta_path.exists():
        return {}
    try:
        return yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        logger.warning("Failed to load meta.yaml for %s: %s", source_id, e)
        return {}


def load_clean_text(source_id: str) -> str | None:
    clean_path = LIBRARY_PATH / source_id / "clean.md"
    if not clean_path.exists():
        return None
    try:
        return clean_path.read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("Failed to read clean.md for %s: %s", source_id, e)
        return None


def get_source_themes(source_id: str, get_conn_fn) -> list[dict]:
    """Fetch theme assignments from DB."""
    try:
        with get_conn_fn() as conn:
            rows = conn.execute(
                "SELECT theme_id, relevance FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.debug("Could not fetch themes for %s: %s", source_id, e)
        return []


# ── API caller ────────────────────────────────────────────────────────────────

def call_api(prompt: str, config, executor=None) -> str:
    """Make a single-turn API call.  Tries Claude CLI first, then OpenRouter, then Anthropic."""
    # Claude CLI (Max subscription — no API key needed)
    if executor is not None:
        return _call_claude_cli(prompt, executor)

    openrouter_key = config.openrouter_api_key
    if openrouter_key:
        return _call_openrouter(prompt, config)

    anthropic_key = __import__("os").getenv("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        return _call_anthropic_direct(prompt, anthropic_key)

    raise RuntimeError(
        "No API key or Claude CLI available. Use Claude Max subscription, "
        "or set OPENROUTER_API_KEY or ANTHROPIC_API_KEY in .env"
    )


def _call_openrouter(prompt: str, config) -> str:
    """Call OpenRouter API with the deep model."""
    import os
    base_url = config.openrouter_base_url.rstrip("/")
    model = config.openrouter_model_deep

    # Strip the "openrouter/" prefix if present (it's a routing prefix, not part of the model name)
    api_model = model.removeprefix("openrouter/")

    headers = {
        "Authorization": f"Bearer {config.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/knowledge-base",
        "X-Title": "knowledge-base deep summarizer",
    }
    payload = {
        "model": api_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8192,
    }

    logger.debug("OpenRouter call: model=%s, prompt_chars=%d", api_model, len(prompt))
    with httpx.Client(timeout=600.0) as client:
        resp = client.post(f"{base_url}/v1/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    text = data["choices"][0]["message"]["content"]
    return text.strip()


def _call_anthropic_direct(prompt: str, api_key: str) -> str:
    """Call Anthropic API directly using httpx."""
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}],
    }
    logger.debug("Anthropic direct call: prompt_chars=%d", len(prompt))
    with httpx.Client(timeout=600.0) as client:
        resp = client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    text = data["content"][0]["text"]
    return text.strip()


def _call_claude_cli(prompt: str, executor) -> str:
    """Call Claude via the local CLI (Max subscription — no API key needed)."""
    result = executor.run_raw(
        prompt,
        session_id="regen_summary",
        model="sonnet",
        timeout=600,
    )
    if not result.text or len(result.text.strip()) < 50:
        raise ValueError(
            f"Claude CLI returned empty/too-short response ({len(result.text or '')} chars)"
        )
    return result.text.strip()


# ── Core processing ───────────────────────────────────────────────────────────

def process_source(source_id: str, config, get_conn_fn, executor=None) -> str:
    """Generate and save a deep summary for one source.  Returns summary text."""
    from ingest.deep_summarizer import build_summary_prompt
    from ingest.section_slicer import strip_backmatter

    meta = load_meta(source_id)
    if not meta:
        raise ValueError(f"No meta.yaml found for {source_id}")

    clean_text = load_clean_text(source_id)
    if not clean_text:
        raise ValueError(f"No clean.md found for {source_id}")

    themes = get_source_themes(source_id, get_conn_fn) if get_conn_fn else []

    full_text = strip_backmatter(clean_text)

    prompt = build_summary_prompt(
        sliced_text=full_text,
        title=meta.get("title", source_id),
        source_type=meta.get("source_type", "article"),
        url=meta.get("url"),
        authors=meta.get("authors"),
        published_at=str(meta["published_at"]) if meta.get("published_at") else None,
        themes=themes or None,
        show_name=meta.get("show_name") or meta.get("channel_name"),
    )

    summary = call_api(prompt, config, executor=executor)

    if not summary or len(summary) < 100:
        raise ValueError(f"API returned empty/too-short response ({len(summary)} chars)")

    summary_path = LIBRARY_PATH / source_id / "deep_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    logger.info("Saved deep_summary.md for %s (%d chars)", source_id, len(summary))

    return summary


# ── Main driver ───────────────────────────────────────────────────────────────

def run_regeneration(
    source_ids: list[str],
    config,
    get_conn_fn,
    *,
    dry_run: bool = False,
    limit: int | None = None,
    resume: bool = False,
    workers: int = 3,
    delay: float = 0.5,
    executor=None,
) -> None:
    progress = load_progress() if resume else {"completed": [], "errors": []}
    done = set(progress.get("completed", []))

    # Filter to sources still needing work
    candidates = []
    for sid in source_ids:
        if resume and sid in done:
            continue
        summary_path = LIBRARY_PATH / sid / "deep_summary.md"
        placeholder, reason = is_placeholder(summary_path)
        if not placeholder and resume:
            # Already has a real summary — skip even if not in progress file
            logger.debug("Skipping %s — already has real summary", sid)
            continue
        candidates.append((sid, reason))

    if limit:
        candidates = candidates[:limit]

    total = len(candidates)

    if dry_run:
        print(f"\n{'='*70}")
        print(f"  DRY RUN: {total} sources need regeneration")
        print(f"{'='*70}\n")
        for i, (sid, reason) in enumerate(candidates):
            meta = load_meta(sid)
            title = meta.get("title", "?")[:60]
            stype = meta.get("source_type", "?")
            print(f"  [{i+1:3d}] {sid}  {title:60s}  type={stype:8s}  reason={reason}")
        print(f"\nRun without --dry-run to regenerate these summaries.\n")
        return

    print(f"\nRegenerating {total} deep summaries (workers={workers}, delay={delay}s)\n")

    completed_count = 0
    error_count = 0
    progress_lock = threading.Lock()

    def _process(i: int, sid: str, reason: str) -> None:
        nonlocal completed_count, error_count
        meta = load_meta(sid)
        title = meta.get("title", "?")[:60]
        logger.info("[%d/%d] %s — %s (was: %s)", i + 1, total, sid, title, reason)
        try:
            summary = process_source(sid, config, get_conn_fn, executor=executor)
            with progress_lock:
                progress["completed"].append(sid)
                completed_count += 1
                if completed_count % 5 == 0:
                    save_progress(progress)
            logger.info("  [OK] %s — %d chars", sid, len(summary))
        except Exception as e:
            logger.error("  [FAIL] %s — %s", sid, e)
            with progress_lock:
                progress["errors"].append({"source_id": sid, "error": str(e)[:300]})
                error_count += 1

    if workers <= 1:
        for i, (sid, reason) in enumerate(candidates):
            _process(i, sid, reason)
            if delay > 0 and i < total - 1:
                time.sleep(delay)
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for i, (sid, reason) in enumerate(candidates):
                fut = pool.submit(_process, i, sid, reason)
                futures[fut] = sid
                if delay > 0 and i < total - 1:
                    time.sleep(delay / workers)  # stagger per-worker

            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception as e:
                    logger.error("Worker exception: %s", e)

    save_progress(progress)

    print(f"\n{'='*60}")
    print(f"  Regeneration complete")
    print(f"{'='*60}")
    print(f"  Processed:   {total}")
    print(f"  Completed:   {completed_count}")
    print(f"  Errors:      {error_count}")
    print()
    if progress["errors"]:
        print("  Failed sources:")
        for err in progress["errors"][-20:]:
            print(f"    {err['source_id']}: {err['error'][:80]}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate placeholder deep summaries via direct API",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no API calls")
    parser.add_argument("--limit", type=int, default=None, help="Max sources to process")
    parser.add_argument("--resume", action="store_true", help="Skip already-completed sources")
    parser.add_argument("--workers", type=int, default=3, help="Parallel workers (default 3)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between submissions (s)")
    parser.add_argument("--ids", nargs="+", metavar="SOURCE_ID", help="Process specific IDs only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    config = Config()

    # Try to get DB connection for theme lookups; gracefully degrade if unavailable
    get_conn_fn = None
    try:
        from reading_app.db import init_pool, get_conn
        init_pool(config.postgres_dsn)
        get_conn_fn = get_conn
        logger.info("DB connected — theme lookups enabled")
    except Exception as e:
        logger.warning("DB unavailable, proceeding without theme context: %s", e)

    # Refresh theme classifier cache if DB available
    if get_conn_fn:
        try:
            from ingest.theme_classifier import refresh_static_theme_block
            refresh_static_theme_block(get_conn_fn)
        except Exception as e:
            logger.debug("Could not refresh theme block: %s", e)

    # Try Claude CLI executor (Max subscription — no API key needed)
    executor = None
    if not (config.openrouter_api_key or __import__("os").getenv("ANTHROPIC_API_KEY")):
        try:
            from agents.executor import MultiBackendExecutor
            executor = MultiBackendExecutor(
                workspace=PROJECT_ROOT, default_backend_id="claude",
            )
            logger.info("Claude CLI executor ready — using Max subscription (no API key needed)")
        except Exception as e:
            logger.warning("Claude CLI not available: %s", e)

    source_ids = args.ids if args.ids else PLACEHOLDER_SOURCE_IDS

    run_regeneration(
        source_ids=source_ids,
        config=config,
        get_conn_fn=get_conn_fn,
        dry_run=args.dry_run,
        limit=args.limit,
        resume=args.resume,
        workers=args.workers,
        delay=args.delay,
        executor=executor,
    )


if __name__ == "__main__":
    main()
