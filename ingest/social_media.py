"""Social source fetchers and scoring for the news digest."""

from __future__ import annotations

import logging
import math
import os
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import httpx

from ingest.http_retry import with_retry
from ingest.news_topics import (
    build_story_key,
    canonicalize_url,
    classify_digest_story,
    merge_social_proof,
    title_similarity,
)

logger = logging.getLogger(__name__)

_X_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
_HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
_HN_ITEM_URL = "https://hn.algolia.com/api/v1/items"
_REDDIT_USER_AGENT = "knowledge-base-news-digest/0.1"
_DEFAULT_HTTP_USER_AGENT = "knowledge-base-news-digest/0.1 (+social-ingest)"

_LOW_SIGNAL_PATTERNS = (
    r"\bhiring\b",
    r"\bjob(?:s)?\b",
    r"\brecruit(?:ing|er|ment)\b",
    r"\bgiveaway\b",
    r"\bprompt pack\b",
    r"\btemplate pack\b",
    r"\bwaitlist\b",
    r"\bdiscount\b",
    r"\bmeme\b",
    r"\bshitpost\b",
)

_AI_SIGNAL_TERMS = (
    "ai",
    "llm",
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "multimodal",
    "reasoning",
    "agent",
    "model",
    "research",
)

_SOCIAL_HOSTS = (
    "x.com",
    "twitter.com",
    "reddit.com",
    "news.ycombinator.com",
)


class SocialMediaFetcher:
    """Fetch and score social signals for the digest."""

    def __init__(self, timezone_name: str = "America/New_York"):
        self.timezone = ZoneInfo(str(timezone_name))

    def fetch_source_items(self, source_cfg: dict[str, Any]) -> list[dict]:
        platform = str(source_cfg.get("platform", "")).strip().lower()
        if platform == "x":
            return self.fetch_x_items(source_cfg)
        if platform == "reddit":
            return self.fetch_reddit_items(source_cfg)
        if platform in {"hn", "hackernews", "hacker_news"}:
            return self.fetch_hn_items(source_cfg)
        return []

    def fetch_x_items(self, source_cfg: dict[str, Any]) -> list[dict]:
        token = os.getenv("X_BEARER_TOKEN", "").strip()
        if not token:
            return []

        queries = [str(query).strip() for query in source_cfg.get("queries", []) if str(query).strip()]
        if not queries:
            return []

        max_candidates = max(1, int(source_cfg.get("max_candidates", 20)))
        per_query = max(10, min(50, math.ceil(max_candidates / max(1, len(queries)))))
        cutoff, window_end = self._query_window(source_cfg)
        headers = {"Authorization": f"Bearer {token}"}
        items: list[dict] = []
        seen_ids: set[str] = set()

        for query in queries:
            for linked_only in self._x_query_modes(source_cfg):
                params = {
                    "query": self._build_x_query(query, linked_only=linked_only),
                    "max_results": str(per_query),
                    "tweet.fields": "created_at,public_metrics,lang,entities",
                    "expansions": "author_id",
                    "user.fields": "name,username",
                }
                if cutoff is not None:
                    params["start_time"] = self._format_api_datetime(cutoff)
                if window_end is not None:
                    params["end_time"] = self._format_api_datetime(window_end)
                try:
                    payload = self._get_json(_X_SEARCH_URL, headers=headers, params=params)
                except httpx.HTTPStatusError as exc:
                    status_code = exc.response.status_code
                    if status_code in {401, 403}:
                        logger.info("Skipping X social source because API auth failed (HTTP %d)", status_code)
                        return []
                    logger.debug("X query failed for '%s' (linked_only=%s)", query, linked_only, exc_info=True)
                    continue
                except Exception:
                    logger.debug("X query failed for '%s' (linked_only=%s)", query, linked_only, exc_info=True)
                    continue

                users = {
                    str(user.get("id")): user
                    for user in (payload.get("includes", {}) or {}).get("users", []) or []
                }

                for tweet in payload.get("data", []) or []:
                    tweet_id = str(tweet.get("id") or "").strip()
                    if not tweet_id or tweet_id in seen_ids:
                        continue

                    published_at = self._parse_datetime(tweet.get("created_at"))
                    if published_at is None or published_at < cutoff:
                        continue
                    if window_end is not None and published_at >= window_end:
                        continue

                    text = self._normalize_whitespace(str(tweet.get("text") or ""))
                    if not text:
                        continue

                    external_url = self._pick_external_url(
                        [
                            (entry.get("expanded_url") or entry.get("unwound_url") or entry.get("url") or "").strip()
                            for entry in (tweet.get("entities", {}) or {}).get("urls", []) or []
                        ]
                    )
                    discussion_url = f"https://x.com/i/web/status/{tweet_id}"
                    if not external_url and linked_only:
                        continue

                    classification = classify_digest_story(text[:160], "", text)
                    if classification is None or self._is_low_signal(text):
                        continue

                    author = users.get(str(tweet.get("author_id")), {})
                    item = self._build_social_item(
                        source_cfg,
                        platform="x",
                        platform_id=tweet_id,
                        subject=self._truncate_subject(text, 160),
                        clean_text=text,
                        published_at=published_at,
                        story_url=external_url,
                        discussion_url=discussion_url,
                        classification=classification,
                        proof={
                            "platform": "x",
                            "source": source_cfg.get("name", "TwitterX"),
                            "discussion_url": discussion_url,
                            "author": author.get("username") or author.get("name") or "",
                            "likes": self._metric_value(tweet, "like_count"),
                            "reposts": self._metric_value(tweet, "retweet_count"),
                            "replies": self._metric_value(tweet, "reply_count"),
                            "quotes": self._metric_value(tweet, "quote_count"),
                            "is_native": not bool(external_url),
                        },
                    )
                    items.append(item)
                    seen_ids.add(tweet_id)

        return self._finalize_items(items, source_cfg)

    def fetch_reddit_items(self, source_cfg: dict[str, Any]) -> list[dict]:
        subreddits = [str(sub).strip() for sub in source_cfg.get("subreddits", []) if str(sub).strip()]
        if not subreddits:
            return []

        sorts = [str(sort).strip().lower() for sort in source_cfg.get("sorts", ["top_day", "new"]) if str(sort).strip()]
        max_candidates = max(1, int(source_cfg.get("max_candidates", 20)))
        per_feed = max(5, min(20, math.ceil(max_candidates / max(1, len(subreddits) * len(sorts)))))
        fetch_lookback_hours = self._fetch_lookback_hours(source_cfg)
        cutoff, window_end = self._query_window(source_cfg)
        items: list[dict] = []
        by_post_id: dict[str, dict] = {}
        headers = {"User-Agent": _REDDIT_USER_AGENT, "Accept": "application/json"}

        for subreddit in subreddits:
            for sort_name in sorts:
                url, params = self._reddit_feed_request(
                    subreddit,
                    sort_name,
                    per_feed,
                    fetch_lookback_hours=fetch_lookback_hours,
                )
                if not url:
                    continue
                try:
                    payload = self._get_json(url, headers=headers, params=params)
                except Exception:
                    logger.debug(
                        "Reddit feed fetch failed for r/%s (%s)",
                        subreddit,
                        sort_name,
                        exc_info=True,
                    )
                    continue

                posts = (((payload or {}).get("data") or {}).get("children") or [])
                for post in posts:
                    data = post.get("data", {}) or {}
                    post_id = str(data.get("id") or "").strip()
                    if not post_id or post_id in by_post_id:
                        continue

                    published_at = self._from_unix_timestamp(data.get("created_utc"))
                    if published_at is None or published_at < cutoff:
                        continue
                    if window_end is not None and published_at >= window_end:
                        continue

                    title = self._normalize_whitespace(str(data.get("title") or ""))
                    selftext = self._normalize_whitespace(str(data.get("selftext") or ""))
                    if not title:
                        continue

                    permalink = str(data.get("permalink") or "").strip()
                    discussion_url = f"https://www.reddit.com{permalink}" if permalink else ""
                    external_url = self._pick_external_url([str(data.get("url") or "").strip()])
                    combined_text = "\n\n".join(part for part in [title, selftext] if part)
                    classification = classify_digest_story(title, "", combined_text)
                    if classification is None or self._is_low_signal(combined_text):
                        continue

                    item = self._build_social_item(
                        source_cfg,
                        platform="reddit",
                        platform_id=post_id,
                        subject=title,
                        clean_text=combined_text,
                        published_at=published_at,
                        story_url=external_url,
                        discussion_url=discussion_url,
                        classification=classification,
                        proof={
                            "platform": "reddit",
                            "source": source_cfg.get("name", "Reddit"),
                            "discussion_url": discussion_url,
                            "author": data.get("author") or "",
                            "subreddit": data.get("subreddit") or subreddit,
                            "points": int(data.get("score") or data.get("ups") or 0),
                            "comments": int(data.get("num_comments") or 0),
                            "upvote_ratio": float(data.get("upvote_ratio") or 0.0),
                            "is_native": not bool(external_url),
                        },
                    )
                    by_post_id[post_id] = item
                    items.append(item)

        self._enrich_reddit_top_comments(items, headers=headers, limit=max(3, int(source_cfg.get("max_items", 5))))
        return self._finalize_items(items, source_cfg)

    def fetch_hn_items(self, source_cfg: dict[str, Any]) -> list[dict]:
        queries = [str(query).strip() for query in source_cfg.get("queries", []) if str(query).strip()]
        if not queries:
            return []

        max_candidates = max(1, int(source_cfg.get("max_candidates", 20)))
        per_query = max(5, min(30, math.ceil(max_candidates / max(1, len(queries)))))
        cutoff, window_end = self._query_window(source_cfg)
        items: list[dict] = []
        by_object_id: dict[str, dict] = {}

        for query in queries:
            numeric_filters = [f"created_at_i>{int(cutoff.astimezone(timezone.utc).timestamp())}"]
            if window_end is not None:
                numeric_filters.append(f"created_at_i<{int(window_end.astimezone(timezone.utc).timestamp())}")
            params = {
                "query": query,
                "tags": "story",
                "numericFilters": ",".join(numeric_filters),
                "hitsPerPage": str(per_query),
            }
            try:
                payload = self._get_json(_HN_SEARCH_URL, params=params)
            except Exception:
                logger.debug("Hacker News search failed for '%s'", query, exc_info=True)
                continue

            for hit in payload.get("hits", []) or []:
                object_id = str(hit.get("objectID") or "").strip()
                if not object_id or object_id in by_object_id:
                    continue

                published_at = self._parse_datetime(hit.get("created_at"))
                if published_at is None or published_at < cutoff:
                    continue
                if window_end is not None and published_at >= window_end:
                    continue

                title = self._normalize_whitespace(str(hit.get("title") or ""))
                if not title:
                    continue

                article_url = self._pick_external_url([str(hit.get("url") or "").strip()])
                discussion_url = f"https://news.ycombinator.com/item?id={object_id}"
                classification = classify_digest_story(title, "", title)
                if classification is None or self._is_low_signal(title):
                    continue

                item = self._build_social_item(
                    source_cfg,
                    platform="hn",
                    platform_id=object_id,
                    subject=title,
                    clean_text=title,
                    published_at=published_at,
                    story_url=article_url,
                    discussion_url=discussion_url,
                    classification=classification,
                    proof={
                        "platform": "hn",
                        "source": source_cfg.get("name", "HackerNews"),
                        "discussion_url": discussion_url,
                        "author": hit.get("author") or "",
                        "points": int(hit.get("points") or 0),
                        "comments": int(hit.get("num_comments") or 0),
                        "is_native": not bool(article_url),
                    },
                )
                by_object_id[object_id] = item
                items.append(item)

        self._enrich_hn_top_comments(items, limit=int(source_cfg.get("enrich_top_comments", 3)))
        return self._finalize_items(items, source_cfg)

    def score_items(self, items: list[dict], source_cfg: dict[str, Any]) -> list[dict]:
        if not items:
            return items

        relevance_raw = [self._compute_relevance_raw(item) for item in items]
        engagement_raw = [self._compute_engagement_raw(item) for item in items]
        relevance_scores = self._normalize_to_100(relevance_raw, default=55)
        engagement_scores = self._normalize_to_100(engagement_raw, default=35)

        for index, item in enumerate(items):
            recency_score = self._compute_recency_score(
                item.get("published_at"),
                lookback_hours=int(source_cfg.get("lookback_hours", 24)),
                reference_end=self._window_end(source_cfg),
            )
            relevance_score = int(relevance_scores[index])
            engagement_score = int(engagement_scores[index])
            total = int((0.45 * relevance_score) + (0.25 * recency_score) + (0.30 * engagement_score))
            item["score"] = total
            item["social_score"] = total
            item["social_subscores"] = {
                "relevance": relevance_score,
                "recency": recency_score,
                "engagement": engagement_score,
            }
            for proof in self._proof_list(item):
                proof["score"] = total
        return items

    def merge_related_items(
        self,
        items: list[dict],
        *,
        title_threshold: float = 0.82,
        merge_window_hours: int = 48,
    ) -> list[dict]:
        merged: list[dict] = []

        for item in sorted(items, key=lambda entry: entry.get("score", 0), reverse=True):
            target = None
            for existing in merged:
                if self._same_story(
                    item,
                    existing,
                    title_threshold=title_threshold,
                    merge_window_hours=merge_window_hours,
                ):
                    target = existing
                    break

            if target is None:
                merged.append(item)
                continue

            target["social_proof"] = merge_social_proof(
                self._proof_list(target),
                self._proof_list(item),
            )
            target["score"] = max(int(target.get("score", 0)), int(item.get("score", 0)))
            target["social_score"] = target["score"]
            target["topic_tags"] = sorted(set(target.get("topic_tags", [])) | set(item.get("topic_tags", [])))
            if not target.get("url") and item.get("url"):
                target["url"] = item["url"]
                target["story_key"] = build_story_key(item.get("url", ""), target.get("subject", ""))
            if len(item.get("clean_text", "")) > len(target.get("clean_text", "")):
                target["clean_text"] = item.get("clean_text", "")
            if self._published_at_value(item.get("published_at")) < self._published_at_value(target.get("published_at")):
                target["published_at"] = item.get("published_at")

        return merged

    def _finalize_items(self, items: list[dict], source_cfg: dict[str, Any]) -> list[dict]:
        scored = self.score_items(items, source_cfg)
        merged = self.merge_related_items(
            scored,
            title_threshold=float(source_cfg.get("dedupe_title_threshold", 0.82)),
            merge_window_hours=int(source_cfg.get("merge_window_hours", 48)),
        )

        min_score = int(source_cfg.get("min_score_threshold", 0))
        max_items = int(source_cfg.get("max_items", len(merged) or 0))

        filtered = []
        for item in sorted(merged, key=lambda entry: entry.get("score", 0), reverse=True):
            threshold = self._threshold_for_item(item, source_cfg, min_score=min_score)
            if threshold is None:
                continue
            if int(item.get("score", 0)) < threshold:
                continue
            filtered.append(self._sanitize_item(item))
            if len(filtered) >= max_items:
                break
        return filtered

    def _build_x_query(self, query: str, *, linked_only: bool) -> str:
        base = f"({query}) lang:en -is:retweet -is:reply"
        if linked_only:
            base += " has:links"
        return base

    def _build_social_item(
        self,
        source_cfg: dict[str, Any],
        *,
        platform: str,
        platform_id: str,
        subject: str,
        clean_text: str,
        published_at: datetime,
        story_url: str,
        discussion_url: str,
        classification: dict,
        proof: dict[str, Any],
    ) -> dict:
        topic_routes = {
            str(topic).strip().lower(): str(destination).strip()
            for topic, destination in (source_cfg.get("topic_routes", {}) or {}).items()
        }
        primary = classification["primary"]
        category = topic_routes.get(primary, source_cfg.get("category", "other"))
        story_key = build_story_key(story_url, subject)

        return {
            "kind": "social",
            "source": source_cfg.get("name", platform),
            "platform": platform,
            "platform_item_id": platform_id,
            "category": category,
            "subject": subject,
            "url": story_url,
            "discussion_url": discussion_url,
            "published_at": published_at.isoformat(),
            "topic_tags": list(classification.get("tags", [])),
            "clean_text": clean_text[:5000],
            "links_context": [],
            "story_key": story_key,
            "social_proof": [proof],
            "_classification": classification,
        }

    def _compute_relevance_raw(self, item: dict) -> float:
        text = f"{item.get('subject', '')} {item.get('clean_text', '')[:2500]}".lower()
        score = 1.0
        classification = item.get("_classification") or {}
        if classification:
            primary = classification.get("primary", "")
            scores = classification.get("scores", {}) or {}
            score += 3.0
            score += float(scores.get(primary, 0)) * 0.4

        if item.get("url") and item.get("url") != item.get("discussion_url"):
            score += 1.2
        if self._proof_list(item) and self._proof_list(item)[0].get("top_comment"):
            score += 0.4

        for term in _AI_SIGNAL_TERMS:
            if term in text:
                score += 0.5

        if self._is_low_signal(text):
            score -= 3.0

        return max(0.0, score)

    def _compute_engagement_raw(self, item: dict) -> float:
        proof = self._proof_list(item)[0] if self._proof_list(item) else {}
        platform = item.get("platform")

        if platform == "x":
            likes = math.log1p(int(proof.get("likes") or 0))
            reposts = math.log1p(int(proof.get("reposts") or 0))
            replies = math.log1p(int(proof.get("replies") or 0))
            quotes = math.log1p(int(proof.get("quotes") or 0))
            return (0.55 * likes) + (0.25 * reposts) + (0.15 * replies) + (0.05 * quotes)

        if platform == "reddit":
            post_score = math.log1p(int(proof.get("points") or 0))
            comments = math.log1p(int(proof.get("comments") or 0))
            ratio = float(proof.get("upvote_ratio") or 0.0) * 10
            top_comment = math.log1p(int(proof.get("top_comment_score") or 0))
            return (0.50 * post_score) + (0.35 * comments) + (0.05 * ratio) + (0.10 * top_comment)

        if platform == "hn":
            points = math.log1p(int(proof.get("points") or 0))
            comments = math.log1p(int(proof.get("comments") or 0))
            return (0.55 * points) + (0.45 * comments)

        return 0.0

    def _compute_recency_score(
        self,
        published_at: str | None,
        *,
        lookback_hours: int,
        reference_end: datetime | None = None,
    ) -> int:
        dt = self._parse_datetime(published_at)
        if dt is None:
            return 50
        reference = reference_end or datetime.now(self.timezone)
        age_hours = max(0.0, (reference - dt).total_seconds() / 3600.0)
        score = 100.0 - (age_hours * (100.0 / max(1, lookback_hours)))
        return max(0, min(100, int(score)))

    def _same_story(
        self,
        item_a: dict,
        item_b: dict,
        *,
        title_threshold: float,
        merge_window_hours: int,
    ) -> bool:
        key_a = str(item_a.get("story_key") or "")
        key_b = str(item_b.get("story_key") or "")
        if key_a and key_b and key_a == key_b:
            return True

        if item_a.get("category") != item_b.get("category"):
            return False

        if not self._within_merge_window(
            item_a.get("published_at"),
            item_b.get("published_at"),
            hours=merge_window_hours,
        ):
            return False

        return title_similarity(item_a.get("subject", ""), item_b.get("subject", "")) >= title_threshold

    def _reddit_feed_request(
        self,
        subreddit: str,
        sort_name: str,
        limit: int,
        *,
        fetch_lookback_hours: int,
    ) -> tuple[str, dict[str, Any]]:
        if sort_name == "top_day":
            top_window = "week" if fetch_lookback_hours > 36 else "day"
            return (
                f"https://www.reddit.com/r/{subreddit}/top.json",
                {"t": top_window, "limit": limit},
            )
        if sort_name == "new":
            return (
                f"https://www.reddit.com/r/{subreddit}/new.json",
                {"limit": limit},
            )
        return "", {}

    def _enrich_reddit_top_comments(self, items: list[dict], *, headers: dict[str, str], limit: int) -> None:
        by_rank = sorted(
            items,
            key=lambda entry: (
                self._proof_list(entry)[0].get("points", 0) if self._proof_list(entry) else 0,
                self._proof_list(entry)[0].get("comments", 0) if self._proof_list(entry) else 0,
            ),
            reverse=True,
        )

        for item in by_rank[: max(0, limit)]:
            if self._proof_list(item) and int(self._proof_list(item)[0].get("comments", 0)) <= 0:
                continue
            discussion_url = str(item.get("discussion_url") or "").strip()
            if not discussion_url:
                continue
            api_url = discussion_url.rstrip("/") + ".json"
            try:
                payload = self._get_json(api_url, headers=headers, params={"limit": 8, "sort": "top"})
            except Exception:
                logger.debug("Reddit top-comment enrichment failed for %s", discussion_url, exc_info=True)
                continue

            if not isinstance(payload, list) or len(payload) < 2:
                continue
            comments_listing = (((payload[1] or {}).get("data") or {}).get("children") or [])
            top_comment = None
            for entry in comments_listing:
                data = entry.get("data", {}) or {}
                body = self._normalize_whitespace(str(data.get("body") or ""))
                if not body or body in {"[deleted]", "[removed]"}:
                    continue
                comment_score = int(data.get("score") or data.get("ups") or 0)
                if top_comment is None or comment_score > top_comment["score"]:
                    top_comment = {
                        "score": comment_score,
                        "body": body[:300],
                    }

            if top_comment is None:
                continue
            proof = self._proof_list(item)[0]
            proof["top_comment"] = top_comment["body"]
            proof["top_comment_score"] = top_comment["score"]

    def _enrich_hn_top_comments(self, items: list[dict], *, limit: int) -> None:
        by_rank = sorted(
            items,
            key=lambda entry: (
                self._proof_list(entry)[0].get("points", 0) if self._proof_list(entry) else 0,
                self._proof_list(entry)[0].get("comments", 0) if self._proof_list(entry) else 0,
            ),
            reverse=True,
        )

        for item in by_rank[: max(0, limit)]:
            if self._proof_list(item) and int(self._proof_list(item)[0].get("comments", 0)) <= 0:
                continue
            item_id = str(item.get("platform_item_id") or "").strip()
            if not item_id:
                continue
            try:
                payload = self._get_json(f"{_HN_ITEM_URL}/{item_id}")
            except Exception:
                logger.debug("Hacker News top-comment enrichment failed for %s", item_id, exc_info=True)
                continue

            children = payload.get("children", []) or []
            top_comment = None
            for child in children:
                body = self._strip_html(str(child.get("text") or ""))
                if not body:
                    continue
                score = int(child.get("points") or 0)
                if top_comment is None or score > top_comment["score"]:
                    top_comment = {"score": score, "body": body[:300]}

            if top_comment is None:
                continue
            proof = self._proof_list(item)[0]
            proof["top_comment"] = top_comment["body"]
            proof["top_comment_score"] = top_comment["score"]

    def _proof_list(self, item: dict) -> list[dict]:
        proofs = item.get("social_proof") or []
        if isinstance(proofs, dict):
            return [proofs]
        return list(proofs)

    def _pick_external_url(self, urls: list[str]) -> str:
        for candidate in urls:
            canonical = canonicalize_url(candidate)
            if not canonical:
                continue
            host = urlparse(canonical).netloc.lower()
            if any(host.endswith(domain) for domain in _SOCIAL_HOSTS):
                continue
            return canonical
        return ""

    def _is_native_discussion(self, item: dict) -> bool:
        url = str(item.get("url") or "").strip()
        discussion_url = str(item.get("discussion_url") or "").strip()
        return not url or url == discussion_url

    def _require_linked_url(self, source_cfg: dict[str, Any]) -> bool:
        return bool(source_cfg.get("require_linked_url", False))

    def _has_native_floor(self, source_cfg: dict[str, Any]) -> bool:
        if "native_discussion_floor" not in source_cfg:
            return False
        value = source_cfg.get("native_discussion_floor")
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        return True

    def _allow_native_discussions(self, source_cfg: dict[str, Any]) -> bool:
        return (not self._require_linked_url(source_cfg)) or self._has_native_floor(source_cfg)

    def _threshold_for_item(
        self,
        item: dict,
        source_cfg: dict[str, Any],
        *,
        min_score: int,
    ) -> int | None:
        if not self._is_native_discussion(item):
            return min_score
        if self._has_native_floor(source_cfg):
            return int(source_cfg.get("native_discussion_floor", min_score))
        if self._require_linked_url(source_cfg):
            return None
        return min_score

    def _fetch_lookback_hours(self, source_cfg: dict[str, Any]) -> int:
        return max(1, int(source_cfg.get("_fetch_lookback_hours", source_cfg.get("lookback_hours", 24))))

    def _window_start(self, source_cfg: dict[str, Any]) -> datetime | None:
        return self._parse_datetime(source_cfg.get("_window_start"))

    def _window_end(self, source_cfg: dict[str, Any]) -> datetime | None:
        return self._parse_datetime(source_cfg.get("_window_end"))

    def _query_window(self, source_cfg: dict[str, Any]) -> tuple[datetime, datetime | None]:
        cutoff = self._window_start(source_cfg)
        if cutoff is None:
            cutoff = datetime.now(self.timezone) - timedelta(hours=self._fetch_lookback_hours(source_cfg))
        return cutoff, self._window_end(source_cfg)

    def _format_api_datetime(self, dt: datetime) -> str:
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _x_query_modes(self, source_cfg: dict[str, Any]) -> list[bool]:
        modes = [True]
        if self._allow_native_discussions(source_cfg):
            modes.append(False)
        return modes

    def _within_merge_window(self, published_a: str | None, published_b: str | None, *, hours: int) -> bool:
        dt_a = self._parse_datetime(published_a)
        dt_b = self._parse_datetime(published_b)
        if dt_a is None or dt_b is None:
            return True
        return abs((dt_a - dt_b).total_seconds()) <= (hours * 3600)

    def _parse_datetime(self, raw: Any) -> datetime | None:
        if isinstance(raw, datetime):
            dt = raw
        else:
            value = str(raw or "").strip()
            if not value:
                return None
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                try:
                    dt = parsedate_to_datetime(value)
                except Exception:
                    return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(self.timezone)

    def _from_unix_timestamp(self, raw: Any) -> datetime | None:
        if raw in (None, ""):
            return None
        try:
            return datetime.fromtimestamp(float(raw), tz=timezone.utc).astimezone(self.timezone)
        except Exception:
            return None

    def _normalize_to_100(self, values: list[float], *, default: int) -> list[float]:
        valid = [value for value in values if value is not None]
        if not valid:
            return [float(default) for _ in values]

        min_value = min(valid)
        max_value = max(valid)
        if max_value == min_value:
            return [50.0 if value is not None else float(default) for value in values]

        result = []
        for value in values:
            if value is None:
                result.append(float(default))
            else:
                normalized = ((value - min_value) / (max_value - min_value)) * 100.0
                result.append(normalized)
        return result

    def _normalize_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _truncate_subject(self, text: str, max_length: int) -> str:
        cleaned = self._normalize_whitespace(text)
        return cleaned if len(cleaned) <= max_length else cleaned[: max_length - 3].rstrip() + "..."

    def _metric_value(self, payload: dict[str, Any], name: str) -> int:
        metrics = payload.get("public_metrics", {}) or {}
        return int(metrics.get(name) or 0)

    def _strip_html(self, text: str) -> str:
        text = re.sub(r"<[^>]+>", " ", text)
        return self._normalize_whitespace(text)

    def _is_low_signal(self, text: str) -> bool:
        lowered = text.lower()
        return any(re.search(pattern, lowered) for pattern in _LOW_SIGNAL_PATTERNS)

    def _published_at_value(self, raw: str | None) -> float:
        dt = self._parse_datetime(raw)
        if dt is None:
            return float("inf")
        return dt.timestamp()

    def _get_json(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        merged_headers = {"User-Agent": _DEFAULT_HTTP_USER_AGENT, **(headers or {})}

        def _do_get() -> Any:
            response = httpx.get(
                url,
                headers=merged_headers,
                params=params,
                follow_redirects=True,
                timeout=20,
            )
            response.raise_for_status()
            return response.json()

        return with_retry(_do_get, max_attempts=3, base_delay=1.5, label=f"social_get_json({url})")

    def _sanitize_item(self, item: dict) -> dict:
        clean = dict(item)
        clean.pop("_classification", None)
        proofs = []
        for proof in self._proof_list(clean):
            proof_clean = dict(proof)
            proofs.append(proof_clean)
        clean["social_proof"] = proofs
        return clean
