"""Shared story classification and canonicalization helpers for digest sources."""

from __future__ import annotations

import hashlib
import re
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, quote, urlsplit, urlunsplit

_TRACKING_QUERY_PREFIXES = (
    "utm_",
    "fbclid",
    "gclid",
    "mc_",
    "mkt_",
    "trk",
    "ref",
)

STARTUP_PATTERNS = (
    (r"\bstartup(?:s)?\b", 4),
    (r"\bspinout(?:s)?\b", 3),
    (r"\bfunding\b", 3),
    (r"\bfundraise\b", 3),
    (r"\bseed\b", 3),
    (r"\bseries\s+[a-f]\b", 4),
    (r"\bvaluation\b", 3),
    (r"\bventure capital\b", 3),
    (r"\bvc\b", 2),
    (r"\bacquisition\b", 4),
    (r"\bacqui-?hire(?:s|d)?\b", 4),
    (r"\bacquire(?:s|d)?\b", 4),
    (r"\bmerger\b", 3),
    (r"\bipo\b", 3),
    (r"\bfounder(?:s)?\b", 2),
    (r"\braised\s+\$?\d", 5),
    (r"\braises\s+\$?\d", 5),
)

CAPABILITY_PATTERNS = (
    (r"\blaunch(?:es|ed)?\b", 3),
    (r"\brelease(?:s|d)?\b", 3),
    (r"\brolls?\s+out\b", 3),
    (r"\bintroduc(?:e|es|ed)\b", 3),
    (r"\bdebut(?:s|ed)?\b", 3),
    (r"\bmodel(?:s)?\b", 2),
    (r"\bagent(?:s)?\b", 3),
    (r"\bassistant\b", 2),
    (r"\bapi\b", 2),
    (r"\btool(?:s|ing)?\b", 2),
    (r"\bfeature(?:s)?\b", 2),
    (r"\bcapabilit(?:y|ies)\b", 3),
    (r"\bbenchmark(?:s)?\b", 2),
    (r"\bmultimodal\b", 3),
    (r"\breasoning\b", 2),
    (r"\bcoding\b", 2),
    (r"\brobotics?\b", 2),
    (r"\bfoundation model(?:s)?\b", 3),
    (r"\bopen[- ]weights?\b", 3),
    (r"\bcomputer use\b", 3),
    (r"\btool use\b", 2),
    (r"\bbrowser\b", 2),
    (r"\bsearch\b", 2),
    (r"\bvoice\b", 2),
    (r"\bvideo\b", 2),
    (r"\bcontext window\b", 2),
)

BREAKTHROUGH_PATTERNS = (
    (r"\bbreakthrough(?:s)?\b", 4),
    (r"\bresearch\b", 3),
    (r"\bpaper(?:s)?\b", 3),
    (r"\bscientists?\b", 3),
    (r"\bstudy\b", 2),
    (r"\bdiscover(?:y|ies)?\b", 3),
    (r"\bnovel\b", 2),
    (r"\befficien(?:t|cy)\b", 2),
    (r"\btraining\b", 2),
    (r"\binference\b", 2),
    (r"\bcompute\b", 2),
    (r"\bchip(?:s)?\b", 2),
    (r"\binfrastructure\b", 2),
    (r"\barchitecture\b", 2),
    (r"\bopen source\b", 2),
    (r"\bdataset(?:s)?\b", 2),
    (r"\bevaluation(?:s)?\b", 2),
    (r"\blatency\b", 2),
    (r"\bthroughput\b", 2),
    (r"\bdistillation\b", 3),
    (r"\bpre-?training\b", 3),
    (r"\bpost-?training\b", 3),
    (r"\bscaling\b", 2),
    (r"\bgpu cluster(?:s)?\b", 3),
    (r"\bdata cent(?:er|re)(?:s)?\b", 2),
    (r"\bserving\b", 2),
)

POLICY_PATTERNS = (
    (r"\bpolicy\b", 3),
    (r"\bregulat(?:ion|ory)\b", 3),
    (r"\blawsuit(?:s)?\b", 3),
    (r"\blegal\b", 2),
    (r"\bantitrust\b", 3),
    (r"\bgovernment\b", 2),
    (r"\bcongress\b", 2),
    (r"\bsenate\b", 2),
    (r"\bwhite house\b", 2),
    (r"\bpentagon\b", 3),
    (r"\bcopyright\b", 2),
    (r"\bprivacy\b", 2),
    (r"\bban(?:s|ned)?\b", 2),
    (r"\bethics?\b", 2),
    (r"\bbill\b", 2),
    (r"\bcourt\b", 2),
    (r"\bjudge\b", 2),
)

NON_TARGET_PATTERNS = (
    (r"\bsong(?:s)?\b", 3),
    (r"\bmusic\b", 3),
    (r"\balbum\b", 3),
    (r"\bmovie(?:s)?\b", 3),
    (r"\bfilm(?:s)?\b", 3),
    (r"\bactor(?:s)?\b", 2),
    (r"\bactress(?:es)?\b", 2),
    (r"\bcelebrit(?:y|ies)\b", 2),
    (r"\bentertainment\b", 3),
    (r"\bviral\b", 2),
    (r"\bfans?\b", 2),
    (r"\bsocial media\b", 2),
    (r"\binfluencer(?:s)?\b", 2),
)

TOPIC_PRIORITY = {
    "startups": 3,
    "capabilities": 2,
    "breakthroughs": 1,
}


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def canonicalize_url(url: str) -> str:
    """Normalize URL for cross-source matching and dedupe."""
    raw = str(url or "").strip()
    if not raw:
        return ""

    parsed = urlsplit(raw)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    if not netloc:
        return ""

    path = quote(parsed.path or "/", safe="/%:@")
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/") + "/"
    elif path != "/" and not path.endswith("/"):
        path = f"{path}/"

    query_items = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=False):
        key_lower = key.lower()
        if key_lower.startswith(_TRACKING_QUERY_PREFIXES):
            continue
        query_items.append((key, value))
    query = "&".join(f"{quote(key, safe='')}={quote(value, safe='')}" for key, value in sorted(query_items))

    return urlunsplit((scheme, netloc, path, query, ""))


def score_patterns(text: str, patterns: tuple[tuple[str, int], ...]) -> int:
    score = 0
    for pattern, weight in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            score += weight
    return score


def explain_digest_story_classification(
    title: str,
    listing_category: str = "",
    clean_text: str = "",
) -> dict:
    """Return classification diagnostics for a digest story."""
    snippet = clean_text[:2500]
    weighted_text = " ".join(
        part for part in [title, title, listing_category, snippet] if part
    ).lower()

    scores = {
        "startups": score_patterns(weighted_text, STARTUP_PATTERNS),
        "capabilities": score_patterns(weighted_text, CAPABILITY_PATTERNS),
        "breakthroughs": score_patterns(weighted_text, BREAKTHROUGH_PATTERNS),
    }
    policy_score = score_patterns(weighted_text, POLICY_PATTERNS)
    non_target_score = score_patterns(weighted_text, NON_TARGET_PATTERNS)
    ranked_topics = sorted(
        scores.items(),
        key=lambda item: (item[1], TOPIC_PRIORITY[item[0]]),
        reverse=True,
    )
    best_topic, best_score = ranked_topics[0]
    second_score = ranked_topics[1][1] if len(ranked_topics) > 1 else 0

    tags = [
        topic
        for topic, score in scores.items()
        if score >= 2 and score + 1 >= best_score
    ] or [best_topic]
    tags.sort(key=lambda topic: (-scores[topic], -TOPIC_PRIORITY[topic], topic))

    return {
        "accepted": (
            best_score >= 2
            and not (policy_score >= 3 and best_score < 4)
            and not (non_target_score >= 4 and non_target_score >= best_score + 2)
        ),
        "primary": best_topic,
        "tags": tags,
        "scores": scores,
        "policy_score": policy_score,
        "non_target_score": non_target_score,
        "best_score": best_score,
        "second_score": second_score,
        "reason": (
            "policy_dominant"
            if policy_score >= 3 and best_score < 4
            else "non_target_human_interest"
            if non_target_score >= 4 and non_target_score >= best_score + 2
            else "weak_topic_signal"
            if best_score < 2
            else "classified"
        ),
    }


def classify_digest_story(
    title: str,
    listing_category: str = "",
    clean_text: str = "",
) -> dict | None:
    """Classify a digest story into one of the supported routes."""
    explanation = explain_digest_story_classification(title, listing_category, clean_text)
    if not explanation["accepted"]:
        return None

    return {
        "primary": explanation["primary"],
        "tags": explanation["tags"],
        "scores": explanation["scores"],
    }


def normalize_title(title: str) -> str:
    text = re.sub(r"[^\w\s]", " ", str(title or "").lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def title_similarity(title_a: str, title_b: str) -> float:
    normalized_a = normalize_title(title_a)
    normalized_b = normalize_title(title_b)
    if not normalized_a or not normalized_b:
        return 0.0
    return SequenceMatcher(None, normalized_a, normalized_b).ratio()


def build_story_key(url: str = "", title: str = "") -> str:
    canonical = canonicalize_url(url)
    if canonical:
        return canonical
    normalized = normalize_title(title)
    if not normalized:
        return ""
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]
    return f"title:{digest}"


def merge_social_proof(
    existing: list[dict] | None,
    incoming: list[dict] | None,
    *,
    limit: int = 5,
) -> list[dict]:
    merged: list[dict] = []
    seen: set[str] = set()

    for proof in [*(existing or []), *(incoming or [])]:
        proof_dict = dict(proof or {})
        key = "|".join(
            [
                str(proof_dict.get("platform") or ""),
                str(proof_dict.get("discussion_url") or ""),
                str(proof_dict.get("author") or ""),
                str(proof_dict.get("subreddit") or ""),
            ]
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(proof_dict)

    merged.sort(
        key=lambda proof: (
            _safe_int(proof.get("score")),
            _safe_int(proof.get("points")) + _safe_int(proof.get("likes")),
            _safe_int(proof.get("comments")) + _safe_int(proof.get("reposts")),
        ),
        reverse=True,
    )
    return merged[: max(0, limit)]
