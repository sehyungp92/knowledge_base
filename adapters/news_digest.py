"""News digest adapter: polls email newsletters and harvests web sources."""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo

import yaml

from gateway.models import Event, Job
from gateway.queue import Queue
from ingest.news_topics import (
    build_story_key,
    canonicalize_url,
    classify_digest_story,
    explain_digest_story_classification,
    merge_social_proof,
    score_patterns,
    title_similarity,
)
from ingest.social_media import SocialMediaFetcher
from reading_app.scheduler_ledger import SchedulerLedger

logger = logging.getLogger(__name__)

_DEFAULT_DAILY_SCHEDULE = "10:00"
_DEFAULT_WEEKLY_SCHEDULE = "19:00"
_DEFAULT_TECHCRUNCH_LOOKBACK_HOURS = 24
_DEFAULT_TECHCRUNCH_MAX_ITEMS = 8
_DEFAULT_TECHCRUNCH_FEED_SUFFIX = "feed/"
_MIN_NEWSLETTER_CHARS = 50
_CONTENT_REGION_SELECTORS = (
    "main",
    "article",
    '[role="main"]',
    "#content",
    ".content",
)
_CONTENT_NOISE_PATTERN = re.compile(
    r"\b(ad|ads|advert|advertisement|tracking|tracker|cookie-banner|cookie-consent|cookie-notice|popup|modal-overlay|gdpr|consent|banner-promo)\b",
    flags=re.IGNORECASE,
)


class NewsDigestAdapter:
    """Polls digest sources at scheduled times."""

    name: str = "news_digest"

    def __init__(
        self,
        queue: Queue,
        config,
        config_path: Path,
        state_path: Path,
        timezone: str = "America/New_York",
    ):
        self.queue = queue
        self._config = config
        self._config_path = Path(config_path)
        self._state_path = Path(state_path)
        self.timezone = ZoneInfo(timezone)
        self._timer: threading.Timer | None = None
        self._running = False
        self._startup_replay_pending = True

        self._daily_schedule: tuple[int, int] = (10, 0)
        self._weekly_schedule: tuple[int, int] = (19, 0)
        self._quiet_start = 23
        self._quiet_end = 6
        runtime_db_path = getattr(config, "runtime_db_path", None)
        if not isinstance(runtime_db_path, (str, Path)):
            runtime_db_path = None
        self._ledger = SchedulerLedger(runtime_db_path)

    def _load_config(self) -> dict:
        if not self._config_path.exists():
            return {}
        try:
            return yaml.safe_load(self._config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            logger.error("Failed to parse news_digest config", exc_info=True)
            return {}

    def _load_state(self) -> dict:
        if not self._state_path.exists():
            return {}
        try:
            return json.loads(self._state_path.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Corrupt news_digest state, resetting", exc_info=True)
            return {}

    def _save_state(self, state: dict) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _load_processed_entry_ids(self, state: dict) -> set[str]:
        processed = set(state.get("processed_entry_ids", []))
        processed.update(state.get("processed_message_ids", []))
        return processed

    def _store_processed_entry_ids(self, state: dict, processed_entry_ids: set[str]) -> None:
        state["processed_entry_ids"] = sorted(processed_entry_ids)
        state["processed_message_ids"] = sorted(
            entry_id for entry_id in processed_entry_ids if ":" not in entry_id
        )

    def _split_sources(self, sources: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
        email_sources: list[dict] = []
        web_sources: list[dict] = []
        social_sources: list[dict] = []
        for source in sources:
            delivery = str(source.get("delivery", "email")).strip().lower()
            if delivery == "web":
                web_sources.append(source)
            elif delivery == "social":
                social_sources.append(source)
            else:
                email_sources.append(source)
        return email_sources, web_sources, social_sources

    def _identify_source(self, text: str, sources: list[dict]) -> str | None:
        fwd_marker = "---------- Forwarded message ---------"
        if fwd_marker not in text:
            return None

        idx = text.index(fwd_marker)
        block = text[idx : idx + 500]

        for line in block.split("\n"):
            line_stripped = line.strip()
            if line_stripped.startswith("From:"):
                from_field = line_stripped[5:].strip()
                match = re.search(r"<([^>]+)>", from_field)
                email = match.group(1) if match else from_field.split()[0]

                for source in sources:
                    if email == source.get("sender"):
                        return source.get("name")
        return None

    def _clean_newsletter_content(self, message) -> str:
        html = getattr(message, "html", None)
        text = None

        if html:
            try:
                import trafilatura

                text = trafilatura.extract(
                    html,
                    include_comments=False,
                    include_tables=True,
                    favor_recall=True,
                    output_format="txt",
                )
            except Exception:
                pass

        if not text or len(text) < 200:
            text = (
                getattr(message, "text", None)
                or getattr(message, "extracted_text", None)
                or ""
            )

        fwd_marker = "---------- Forwarded message ---------"
        if fwd_marker in text:
            idx = text.index(fwd_marker)
            rest = text[idx + len(fwd_marker) :]
            lines = rest.split("\n")
            body_start = 0
            for i, line in enumerate(lines):
                if not line.strip() and i > 0:
                    body_start = i + 1
                    break
            text = "\n".join(lines[body_start:])

        text = re.sub(r"[\u034f\u00ad\u200b\u200c\u200d\ufeff\u2060]", "", text)
        text = re.sub(r"https?://[^\s]*substack\.com/redirect/[^\s]*", "[link]", text)
        text = re.sub(r"\?utm_[^\s&]*(&[^\s]*)*", "", text)

        for marker in ["Unsubscribe", "View in browser", "Manage your preferences"]:
            idx = text.lower().rfind(marker.lower())
            if idx != -1 and idx > len(text) * 0.8:
                text = text[:idx].rstrip()

        text = re.sub(r"\[image[^\]]*\]", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)

        return text.strip()

    def _extract_links(self, message_html: str, max_links: int = 5) -> list[str]:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(message_html, "html.parser")
        seen: set[str] = set()
        links: list[str] = []
        skip_domains = {
            "substack.com",
            "twitter.com",
            "x.com",
            "facebook.com",
            "linkedin.com",
            "instagram.com",
        }

        for anchor in soup.find_all("a", href=True):
            url = anchor["href"].strip()
            if not url.startswith("http"):
                continue
            if any(domain in url.lower() for domain in skip_domains):
                continue
            if "unsubscribe" in url.lower() or "mailto:" in url.lower():
                continue

            parsed = urlparse(url)
            key = f"{parsed.netloc}{parsed.path}"
            if key not in seen:
                seen.add(key)
                links.append(url)
            if len(links) >= max_links:
                break

        return links

    def _fetch_linked_articles(self, links: list[str]) -> list[dict]:
        from ingest.article import _extract_trafilatura, _fetch_html

        results = []
        for url in links:
            try:
                html = _fetch_html(url, timeout=10)
                text = _extract_trafilatura(html, url)
                if text and len(text) > 100:
                    results.append({"url": url, "snippet": text[:3000]})
            except Exception:
                logger.debug("Failed to fetch linked article: %s", url)
        return results

    def _scope_html_to_content(self, html: str, *, preserve_structured_data: bool = False) -> str:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        for script in soup.find_all("script"):
            if preserve_structured_data and script.get("type") == "application/ld+json":
                continue
            script.decompose()

        for tag in soup.find_all(["style", "noscript", "svg", "iframe", "nav", "footer", "header", "aside"]):
            tag.decompose()

        for node in list(soup.find_all(True)):
            if getattr(node, "attrs", None) is None:
                continue
            style = str(node.get("style", "")).replace(" ", "").lower()
            if "display:none" in style or "visibility:hidden" in style:
                node.decompose()
                continue
            if node.get("aria-hidden") == "true" or node.has_attr("hidden"):
                node.decompose()
                continue

            class_names = " ".join(node.get("class", []))
            element_id = str(node.get("id", ""))
            if _CONTENT_NOISE_PATTERN.search(f"{class_names} {element_id}"):
                node.decompose()

        for selector in _CONTENT_REGION_SELECTORS:
            regions = soup.select(selector)
            if len(regions) != 1:
                continue
            region = regions[0]
            if len(region.get_text(" ", strip=True)) >= 100:
                return str(region)

        body = soup.body or soup
        return str(body)

    def _canonicalize_url(self, url: str) -> str:
        return canonicalize_url(url)

    def _derive_techcrunch_feed_url(self, listing_url: str) -> str:
        normalized_listing_url = listing_url if listing_url.endswith("/") else f"{listing_url}/"
        return urljoin(normalized_listing_url, _DEFAULT_TECHCRUNCH_FEED_SUFFIX)

    def _extract_techcrunch_feed_url(self, html: str, listing_url: str) -> str:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        preferred_feed_path = urlparse(self._derive_techcrunch_feed_url(listing_url)).path.rstrip("/")

        for link in soup.select('link[rel="alternate"][type="application/rss+xml"][href]'):
            href = link.get("href", "").strip()
            if not href:
                continue
            normalized_href = urljoin(listing_url, href)
            link_path = urlparse(normalized_href).path.rstrip("/")
            title = str(link.get("title", ""))
            if link_path == preferred_feed_path or "category feed" in title.lower():
                return normalized_href

        return self._derive_techcrunch_feed_url(listing_url)

    def _is_techcrunch_article_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if not parsed.netloc.endswith("techcrunch.com"):
            return False
        return bool(re.search(r"/\d{4}/\d{2}/\d{2}/", parsed.path))

    def _parse_datetime(self, raw: str | None) -> datetime | None:
        if not raw:
            return None
        value = raw.strip()
        if not value:
            return None
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                from email.utils import parsedate_to_datetime

                dt = parsedate_to_datetime(value)
            except Exception:
                try:
                    from dateutil.parser import parse as dateutil_parse

                    dt = dateutil_parse(value)
                except Exception:
                    return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(self.timezone)

    def _clean_techcrunch_title(self, title: str) -> str:
        cleaned = title.strip()
        cleaned = re.sub(r"\s+[|:-]\s+TechCrunch$", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def _extract_structured_article_candidates(
        self,
        soup,
        listing_url: str,
        candidates: dict[str, dict],
    ) -> None:
        import json as json_lib

        def walk(node):
            if isinstance(node, dict):
                yield node
                for value in node.values():
                    yield from walk(value)
            elif isinstance(node, list):
                for item in node:
                    yield from walk(item)

        for script in soup.find_all("script", type="application/ld+json"):
            raw = (script.string or script.get_text() or "").strip()
            if not raw:
                continue
            try:
                data = json_lib.loads(raw)
            except Exception:
                continue

            for node in walk(data):
                raw_node_type = node.get("@type")
                if isinstance(raw_node_type, str):
                    node_types = {raw_node_type.strip()}
                elif isinstance(raw_node_type, (list, tuple, set)):
                    node_types = {str(item).strip() for item in raw_node_type if str(item).strip()}
                else:
                    node_types = set()
                if not node_types.intersection({"Article", "NewsArticle"}):
                    continue
                url = node.get("url") or node.get("@id")
                if not url:
                    continue
                normalized_url = self._canonicalize_url(urljoin(listing_url, url))
                if not self._is_techcrunch_article_url(normalized_url):
                    continue
                self._merge_techcrunch_candidate(
                    candidates,
                    url=normalized_url,
                    subject=str(node.get("headline") or node.get("name") or "").strip(),
                    published_at=self._parse_datetime(str(node.get("datePublished") or "")),
                    excerpt=str(node.get("description") or "").strip(),
                )

    def _merge_techcrunch_candidate(
        self,
        candidates: dict[str, dict],
        *,
        url: str,
        subject: str = "",
        published_at: datetime | None = None,
        listing_category: str = "",
        excerpt: str = "",
    ) -> None:
        normalized_url = self._canonicalize_url(url)
        if not self._is_techcrunch_article_url(normalized_url):
            return

        candidate = candidates.setdefault(normalized_url, {"url": normalized_url})
        clean_subject = self._clean_techcrunch_title(subject) if subject else ""
        if clean_subject and (
            not candidate.get("subject") or len(clean_subject) > len(str(candidate.get("subject") or ""))
        ):
            candidate["subject"] = clean_subject
        if published_at and not candidate.get("published_at"):
            candidate["published_at"] = published_at
        if listing_category and not candidate.get("listing_category"):
            candidate["listing_category"] = listing_category.strip()
        clean_excerpt = excerpt.strip()
        if clean_excerpt and len(clean_excerpt) > len(str(candidate.get("excerpt") or "")):
            candidate["excerpt"] = clean_excerpt

    def _merge_techcrunch_candidate_record(
        self,
        candidates: dict[str, dict],
        candidate: dict,
    ) -> None:
        url = str(candidate.get("url") or "").strip()
        if not url:
            return
        self._merge_techcrunch_candidate(
            candidates,
            url=url,
            subject=str(candidate.get("subject") or ""),
            published_at=candidate.get("published_at"),
            listing_category=str(candidate.get("listing_category") or ""),
            excerpt=str(candidate.get("excerpt") or ""),
        )

    def _extract_techcrunch_feed_candidates(self, xml_text: str, feed_url: str) -> list[dict]:
        import xml.etree.ElementTree as ET

        candidates: dict[str, dict] = {}

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            logger.warning("TechCrunch feed parse failed", exc_info=True)
            return []

        for item in root.findall(".//item"):
            link = (item.findtext("link") or "").strip()
            if not link:
                continue
            self._merge_techcrunch_candidate(
                candidates,
                url=urljoin(feed_url, link),
                subject=(item.findtext("title") or "").strip(),
                published_at=self._parse_datetime(item.findtext("pubDate")),
                listing_category=(item.findtext("category") or "").strip(),
                excerpt=(item.findtext("description") or "").strip(),
            )

        atom_ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall(".//atom:entry", atom_ns):
            link_href = ""
            link_node = entry.find("atom:link", atom_ns)
            if link_node is not None:
                link_href = link_node.get("href", "").strip()
            if not link_href:
                continue
            self._merge_techcrunch_candidate(
                candidates,
                url=urljoin(feed_url, link_href),
                subject=(entry.findtext("atom:title", default="", namespaces=atom_ns) or "").strip(),
                published_at=self._parse_datetime(
                    entry.findtext("atom:published", default="", namespaces=atom_ns)
                    or entry.findtext("atom:updated", default="", namespaces=atom_ns)
                ),
                excerpt=(entry.findtext("atom:summary", default="", namespaces=atom_ns) or "").strip(),
            )

        return sorted(
            candidates.values(),
            key=lambda item: item.get("published_at") or datetime.min.replace(tzinfo=self.timezone),
            reverse=True,
        )

    def _write_techcrunch_drift_artifact(
        self,
        reason: str,
        *,
        listing_url: str,
        listing_html: str = "",
        feed_url: str = "",
        feed_xml: str = "",
    ) -> None:
        drift_dir = self._state_path.parent / "news_digest_techcrunch_drift"
        drift_dir.mkdir(parents=True, exist_ok=True)

        captured_at = datetime.now(timezone.utc)
        slug = re.sub(r"[^a-z0-9]+", "-", reason.lower()).strip("-")[:60] or "unknown"
        stem = f"{captured_at.strftime('%Y%m%dT%H%M%SZ')}-{slug}"

        metadata = {
            "captured_at": captured_at.isoformat(),
            "reason": reason,
            "listing_url": listing_url,
            "feed_url": feed_url,
        }
        (drift_dir / f"{stem}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        if listing_html:
            (drift_dir / f"{stem}.listing.html").write_text(listing_html[:500000], encoding="utf-8")
        if feed_xml:
            (drift_dir / f"{stem}.feed.xml").write_text(feed_xml[:250000], encoding="utf-8")

    def _write_techcrunch_triage_artifact(
        self,
        run_date: str,
        *,
        source_name: str,
        accepted_count: int,
        recent_candidate_count: int,
        rejected_candidates: list[dict],
    ) -> None:
        triage_dir = self._state_path.parent / "news_digest_techcrunch_triage"
        triage_dir.mkdir(parents=True, exist_ok=True)

        captured_at = datetime.now(timezone.utc)
        stem = f"{captured_at.strftime('%Y%m%dT%H%M%SZ')}-{run_date}-triage"
        payload = {
            "captured_at": captured_at.isoformat(),
            "run_date": run_date,
            "source": source_name,
            "accepted_count": accepted_count,
            "recent_candidate_count": recent_candidate_count,
            "rejected_candidates": rejected_candidates[:10],
        }
        (triage_dir / f"{stem}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _extract_techcrunch_candidates(self, html: str, listing_url: str) -> list[dict]:
        from bs4 import BeautifulSoup

        raw_soup = BeautifulSoup(html, "html.parser")
        scoped_html = self._scope_html_to_content(html, preserve_structured_data=True)
        soup = BeautifulSoup(scoped_html, "html.parser")
        candidates: dict[str, dict] = {}
        self._extract_structured_article_candidates(raw_soup, listing_url, candidates)

        containers = []
        for selector in (
            "ul.wp-block-post-template li.wp-block-post",
            "article",
            "div.loop-card",
        ):
            containers.extend(soup.select(selector))

        for node in containers:
            link = node.select_one("h3.loop-card__title a[href]")
            if link is None:
                link = node.select_one("h2 a[href], h3 a[href], a[href]")
            if link is None:
                continue

            raw_url = link.get("href", "").strip()
            if not raw_url:
                continue
            normalized_url = self._canonicalize_url(urljoin(listing_url, raw_url))
            if not self._is_techcrunch_article_url(normalized_url):
                continue

            title = link.get_text(" ", strip=True)
            if not title:
                continue

            time_tag = node.select_one("time[datetime]")
            published_at = self._parse_datetime(time_tag.get("datetime", "") if time_tag else "")
            category_tag = node.select_one(".loop-card__cat")
            excerpt_tag = node.select_one("p")

            self._merge_techcrunch_candidate(
                candidates,
                url=normalized_url,
                subject=title,
                published_at=published_at,
                listing_category=category_tag.get_text(" ", strip=True) if category_tag else "",
                excerpt=excerpt_tag.get_text(" ", strip=True) if excerpt_tag else "",
            )

        if not candidates:
            logger.warning("TechCrunch parser drift: no valid article cards or structured entries found")
            return []

        if not any(candidate.get("published_at") for candidate in candidates.values()):
            logger.warning("TechCrunch parser drift: no listing timestamps found")

        return sorted(
            candidates.values(),
            key=lambda item: item.get("published_at") or datetime.min.replace(tzinfo=self.timezone),
            reverse=True,
        )

    def _score_patterns(self, text: str, patterns: tuple[tuple[str, int], ...]) -> int:
        return score_patterns(text, patterns)

    def _explain_techcrunch_article_classification(
        self,
        title: str,
        listing_category: str,
        clean_text: str,
    ) -> dict:
        return explain_digest_story_classification(title, listing_category, clean_text)

    def _classify_techcrunch_article(
        self,
        title: str,
        listing_category: str,
        clean_text: str,
    ) -> dict | None:
        return classify_digest_story(title, listing_category, clean_text)

    def _extract_techcrunch_article_payload(self, html: str, url: str) -> dict | None:
        from ingest.article import (
            _extract_bs4,
            _extract_published_at,
            _extract_title_from_html,
            _extract_trafilatura,
            _normalize_text,
        )

        scoped_html = self._scope_html_to_content(html, preserve_structured_data=True)
        text = _extract_trafilatura(scoped_html, url)
        if not text:
            text = _extract_trafilatura(html, url)
        if not text:
            text = _extract_bs4(scoped_html)
        if not text:
            text = _extract_bs4(html)
        if not text or len(text) < 200:
            return None

        published_at = self._parse_datetime(_extract_published_at(scoped_html) or _extract_published_at(html))
        subject = self._clean_techcrunch_title(_extract_title_from_html(html))
        clean_text = _normalize_text(text)

        return {
            "subject": subject,
            "published_at": published_at,
            "clean_text": clean_text,
        }

    def _fetch_techcrunch_article(self, url: str) -> dict | None:
        from ingest.article import _fetch_html

        html = ""
        try:
            html = _fetch_html(url, timeout=20)
        except Exception:
            logger.warning("Failed to fetch TechCrunch article: %s", url, exc_info=True)
        else:
            article = self._extract_techcrunch_article_payload(html, url)
            if article is not None:
                return article

        try:
            from ingest.stealth_fetch import fetch_html_stealth

            stealth_html = fetch_html_stealth(url)
        except Exception:
            logger.warning("TechCrunch article extraction too short: %s", url, exc_info=True)
            return None

        article = self._extract_techcrunch_article_payload(stealth_html, url)
        if article is None:
            logger.warning("TechCrunch article extraction too short: %s", url)
        return article

    def _fallback_techcrunch_article_from_candidate(self, candidate: dict) -> dict | None:
        from html import unescape

        excerpt = unescape(str(candidate.get("excerpt") or ""))
        excerpt = re.sub(r"<[^>]+>", " ", excerpt)
        excerpt = re.sub(r"\s+", " ", excerpt).strip()
        if len(excerpt) < 120:
            return None

        published_at = candidate.get("published_at")
        return {
            "subject": str(candidate.get("subject") or "").strip(),
            "published_at": published_at,
            "clean_text": excerpt,
        }

    def _collect_techcrunch_items(
        self,
        source: dict,
        run_date: str,
        processed_entry_ids: set[str],
        *,
        window_start: datetime | None = None,
        window_end: datetime | None = None,
    ) -> tuple[list[dict], set[str]]:
        from ingest.article import _fetch_html

        listing_url = source.get("listing_url")
        if not listing_url:
            logger.warning("TechCrunch source missing listing_url")
            return [], set()

        listing_html = ""
        feed_url = str(source.get("feed_url") or self._derive_techcrunch_feed_url(listing_url)).strip()
        feed_xml = ""
        try:
            listing_html = _fetch_html(listing_url, timeout=20)
        except Exception:
            logger.warning("Failed to fetch TechCrunch listing", exc_info=True)
        else:
            feed_url = str(source.get("feed_url") or self._extract_techcrunch_feed_url(listing_html, listing_url)).strip()

        candidate_map: dict[str, dict] = {}
        if listing_html:
            for candidate in self._extract_techcrunch_candidates(listing_html, listing_url):
                self._merge_techcrunch_candidate_record(candidate_map, candidate)

        if (not listing_html) or (not candidate_map) or (not any(candidate.get("published_at") for candidate in candidate_map.values())):
            try:
                from ingest.stealth_fetch import fetch_html_stealth

                stealth_listing_html = fetch_html_stealth(listing_url)
                for candidate in self._extract_techcrunch_candidates(stealth_listing_html, listing_url):
                    self._merge_techcrunch_candidate_record(candidate_map, candidate)
                if not feed_url:
                    feed_url = self._extract_techcrunch_feed_url(stealth_listing_html, listing_url)
                if not listing_html or not candidate_map:
                    listing_html = stealth_listing_html
            except Exception:
                logger.warning("TechCrunch stealth fallback failed", exc_info=True)

        if feed_url:
            try:
                feed_xml = _fetch_html(feed_url, timeout=20)
            except Exception:
                logger.warning("Failed to fetch TechCrunch feed: %s", feed_url, exc_info=True)
            else:
                for candidate in self._extract_techcrunch_feed_candidates(feed_xml, feed_url):
                    self._merge_techcrunch_candidate_record(candidate_map, candidate)

        candidates = sorted(
            candidate_map.values(),
            key=lambda item: item.get("published_at") or datetime.min.replace(tzinfo=self.timezone),
            reverse=True,
        )
        if not candidates:
            logger.warning("TechCrunch parser drift: no article candidates found after HTML, stealth, and feed fallbacks")
            self._write_techcrunch_drift_artifact(
                "no_candidates_after_fallbacks",
                listing_url=listing_url,
                listing_html=listing_html,
                feed_url=feed_url,
                feed_xml=feed_xml,
            )
            return [], set()

        if not any(candidate.get("published_at") for candidate in candidates):
            logger.warning("TechCrunch parser drift: no timestamps found after HTML and feed extraction")
            self._write_techcrunch_drift_artifact(
                "no_candidate_timestamps_after_fallbacks",
                listing_url=listing_url,
                listing_html=listing_html,
                feed_url=feed_url,
                feed_xml=feed_xml,
            )

        lookback_hours = int(source.get("lookback_hours", _DEFAULT_TECHCRUNCH_LOOKBACK_HOURS))
        max_items = int(source.get("max_items", _DEFAULT_TECHCRUNCH_MAX_ITEMS))
        include_topics = {str(topic).strip().lower() for topic in source.get("include_topics", [])}
        topic_routes = {
            str(topic).strip().lower(): destination
            for topic, destination in source.get("topic_routes", {}).items()
        }
        cutoff = window_start or (datetime.now(self.timezone) - timedelta(hours=lookback_hours))

        items: list[dict] = []
        new_processed_ids: set[str] = set()
        recent_candidate_count = 0
        rejected_recent_candidates: list[dict] = []

        for candidate in candidates:
            processed_id = f"techcrunch:{candidate['url']}"
            if processed_id in processed_entry_ids or processed_id in new_processed_ids:
                continue

            article = self._fetch_techcrunch_article(candidate["url"])
            if article is None:
                article = self._fallback_techcrunch_article_from_candidate(candidate)
            if article is None:
                candidate_published_at = candidate.get("published_at")
                if (
                    candidate_published_at is not None
                    and candidate_published_at >= cutoff
                    and (window_end is None or candidate_published_at < window_end)
                ):
                    recent_candidate_count += 1
                    rejected_recent_candidates.append(
                        {
                            "url": candidate["url"],
                            "subject": str(candidate.get("subject") or "").strip(),
                            "published_at": candidate_published_at.isoformat(),
                            "reason": "article_extraction_failed",
                        }
                    )
                continue

            published_at = article.get("published_at") or candidate.get("published_at")
            if published_at is None:
                logger.warning("TechCrunch parser drift: missing published_at for %s", candidate["url"])
                continue
            if published_at < cutoff:
                continue
            if window_end is not None and published_at >= window_end:
                continue
            recent_candidate_count += 1

            classification = self._explain_techcrunch_article_classification(
                article.get("subject") or candidate.get("subject") or "",
                candidate.get("listing_category", ""),
                article.get("clean_text", ""),
            )
            if not classification["accepted"]:
                rejected_recent_candidates.append(
                    {
                        "url": candidate["url"],
                        "subject": article.get("subject") or candidate.get("subject") or "",
                        "published_at": published_at.isoformat(),
                        "reason": classification["reason"],
                        "primary_topic": classification["primary"],
                        "scores": classification["scores"],
                        "policy_score": classification["policy_score"],
                        "non_target_score": classification["non_target_score"],
                        "best_score": classification["best_score"],
                        "second_score": classification["second_score"],
                    }
                )
                continue

            primary_topic = classification["primary"]
            if include_topics and primary_topic not in include_topics:
                rejected_recent_candidates.append(
                    {
                        "url": candidate["url"],
                        "subject": article.get("subject") or candidate.get("subject") or "",
                        "published_at": published_at.isoformat(),
                        "reason": "topic_excluded",
                        "primary_topic": primary_topic,
                        "scores": classification["scores"],
                    }
                )
                continue

            category = topic_routes.get(primary_topic, source.get("category", "other"))
            items.append(
                {
                    "kind": "article",
                    "source": source.get("name", "TechCrunch"),
                    "category": category,
                    "subject": article.get("subject") or candidate.get("subject") or "",
                    "url": candidate["url"],
                    "published_at": published_at.isoformat(),
                    "topic_tags": classification["tags"],
                    "clean_text": article.get("clean_text", "")[:7000],
                    "links_context": [],
                    "story_key": build_story_key(candidate["url"], article.get("subject") or candidate.get("subject") or ""),
                    "date": run_date,
                }
            )
            new_processed_ids.add(processed_id)
            if len(items) >= max_items:
                break

        if rejected_recent_candidates and (
            not items or len(rejected_recent_candidates) >= max(3, len(items) + 2)
        ):
            self._write_techcrunch_triage_artifact(
                run_date,
                source_name=str(source.get("name") or "TechCrunch"),
                accepted_count=len(items),
                recent_candidate_count=recent_candidate_count,
                rejected_candidates=rejected_recent_candidates,
            )
            logger.warning(
                "TechCrunch semantic triage audit saved: %s accepted, %s rejected recent candidates",
                len(items),
                len(rejected_recent_candidates),
            )

        return items, new_processed_ids

    def _email_item_from_message(
        self,
        msg,
        source_name: str,
        category: str,
        fetch_articles: bool,
        max_links: int,
    ) -> dict | None:
        clean_text = self._clean_newsletter_content(msg)
        if len(clean_text) < _MIN_NEWSLETTER_CHARS:
            return None

        links_context = []
        msg_html = getattr(msg, "html", None)
        if fetch_articles and msg_html:
            raw_links = self._extract_links(msg_html, max_links=max_links)
            links_context = self._fetch_linked_articles(raw_links)

        return {
            "kind": "newsletter",
            "source": source_name,
            "category": category,
            "subject": getattr(msg, "subject", "") or "",
            "url": "",
            "published_at": "",
            "topic_tags": [],
            "clean_text": clean_text,
            "links_context": links_context,
            "story_key": build_story_key("", getattr(msg, "subject", "") or ""),
        }

    def _collect_social_items(
        self,
        source: dict,
        run_date: str,
        processed_entry_ids: set[str],
        *,
        window_start: datetime | None = None,
        window_end: datetime | None = None,
    ) -> tuple[list[dict], set[str]]:
        fetcher = SocialMediaFetcher(str(self.timezone))
        effective_source = dict(source)
        if window_start is not None:
            effective_source["_window_start"] = window_start.isoformat()
            lookback_hours = max(
                int(source.get("lookback_hours", 24)),
                max(1, int((datetime.now(self.timezone) - window_start).total_seconds() // 3600) + 1),
            )
            effective_source["_fetch_lookback_hours"] = lookback_hours
        if window_end is not None:
            effective_source["_window_end"] = window_end.isoformat()
        try:
            items = fetcher.fetch_source_items(effective_source)
        except Exception:
            logger.warning("Failed to fetch social source: %s", source.get("name"), exc_info=True)
            return [], set()
        accepted: list[dict] = []
        new_processed_ids: set[str] = set()

        for item in items:
            published_at = self._parse_datetime(item.get("published_at"))
            if window_start is not None and (published_at is None or published_at < window_start):
                continue
            if window_end is not None and (published_at is None or published_at >= window_end):
                continue
            platform = str(item.get("platform") or source.get("platform") or "social").strip().lower()
            platform_item_id = str(item.get("platform_item_id") or "").strip()
            processed_id = f"{platform}:{platform_item_id}" if platform_item_id else ""
            if processed_id and (processed_id in processed_entry_ids or processed_id in new_processed_ids):
                continue

            item["date"] = run_date
            item.setdefault("story_key", build_story_key(item.get("url", ""), item.get("subject", "")))
            accepted.append(item)
            if processed_id:
                new_processed_ids.add(processed_id)

        return accepted, new_processed_ids

    def _item_story_keys(self, item: dict) -> set[str]:
        keys: set[str] = set()
        story_key = str(item.get("story_key") or "").strip()
        if story_key:
            keys.add(story_key)

        url = canonicalize_url(item.get("url", ""))
        if url:
            keys.add(url)

        for link in item.get("links_context", []) or []:
            link_url = canonicalize_url((link or {}).get("url", ""))
            if link_url:
                keys.add(link_url)

        if not keys:
            fallback = build_story_key("", item.get("subject", ""))
            if fallback:
                keys.add(fallback)

        return keys

    def _within_story_merge_window(self, item_a: dict, item_b: dict, *, hours: int) -> bool:
        dt_a = self._parse_datetime(item_a.get("published_at"))
        dt_b = self._parse_datetime(item_b.get("published_at"))
        if dt_a is None or dt_b is None:
            return True
        return abs((dt_a - dt_b).total_seconds()) <= (hours * 3600)

    def _merge_story_items(
        self,
        items: list[dict],
        *,
        merge_window_hours: int,
        similarity_threshold: float,
    ) -> list[dict]:
        if not items:
            return items

        base_items = [dict(item) for item in items if item.get("kind") != "social"]
        social_items = [dict(item) for item in items if item.get("kind") == "social"]
        if social_items:
            social_items = SocialMediaFetcher(str(self.timezone)).merge_related_items(
                social_items,
                title_threshold=similarity_threshold,
                merge_window_hours=merge_window_hours,
            )
        base_item_keys = [self._item_story_keys(item) for item in base_items]

        for social_item in social_items:
            social_keys = self._item_story_keys(social_item)
            target_index = None

            for index, item in enumerate(base_items):
                base_keys = base_item_keys[index]
                if social_keys & base_keys:
                    target_index = index
                    break
                if not self._within_story_merge_window(social_item, item, hours=merge_window_hours):
                    continue
                if title_similarity(social_item.get("subject", ""), item.get("subject", "")) >= similarity_threshold:
                    target_index = index
                    break

            if target_index is None:
                base_items.append(social_item)
                base_item_keys.append(social_keys)
                continue

            target = base_items[target_index]
            target["social_proof"] = merge_social_proof(
                list(target.get("social_proof", []) or []),
                list(social_item.get("social_proof", []) or []),
            )
            target["topic_tags"] = sorted(set(target.get("topic_tags", []) or []) | set(social_item.get("topic_tags", []) or []))
            if social_item.get("url") and not target.get("url"):
                target["url"] = social_item.get("url", "")
                target["story_key"] = build_story_key(target["url"], target.get("subject", ""))
            elif not target.get("story_key"):
                target["story_key"] = next(iter(self._item_story_keys(target)), "")
            if social_item.get("published_at") and not target.get("published_at"):
                target["published_at"] = social_item.get("published_at")
            base_item_keys[target_index] = self._item_story_keys(target)

        return base_items

    def _sanitize_item_for_payload(self, item: dict) -> dict:
        clean = dict(item)
        clean.pop("_classification", None)
        if isinstance(clean.get("social_proof"), list):
            clean["social_proof"] = [dict(proof) for proof in clean["social_proof"]]
        return clean

    def _is_quiet_hour(self) -> bool:
        now = datetime.now(self.timezone)
        hour = now.hour
        if self._quiet_start > self._quiet_end:
            return hour >= self._quiet_start or hour < self._quiet_end
        return self._quiet_start <= hour < self._quiet_end

    def _resolve_replay_days(self) -> int:
        try:
            return max(1, int(getattr(self._config, "scheduler_replay_days", 3)))
        except (TypeError, ValueError):
            return 3

    def _daily_slot_for_date(self, day) -> datetime:
        return datetime(
            day.year,
            day.month,
            day.day,
            self._daily_schedule[0],
            self._daily_schedule[1],
            tzinfo=self.timezone,
        )

    def _weekly_slot_for_date(self, day) -> datetime:
        return datetime(
            day.year,
            day.month,
            day.day,
            self._weekly_schedule[0],
            self._weekly_schedule[1],
            tzinfo=self.timezone,
        )

    @staticmethod
    def _slot_key(slot_dt: datetime) -> str:
        return slot_dt.isoformat()

    def _scheduled_payload(self, *, job_type: str, slot_dt: datetime, metadata: dict) -> dict:
        return {
            "adapter": self.name,
            "job_type": job_type,
            "slot_key": self._slot_key(slot_dt),
            "scheduled_for": slot_dt.isoformat(),
            "metadata": metadata,
        }

    def _iter_due_daily_slots(self, now: datetime, *, startup: bool) -> list[datetime]:
        replay_days = self._resolve_replay_days() if startup else 1
        due_slots: list[datetime] = []
        for offset in range(replay_days - 1, -1, -1):
            day = (now - timedelta(days=offset)).date()
            slot_dt = self._daily_slot_for_date(day)
            if slot_dt <= now:
                due_slots.append(slot_dt)
        return due_slots

    def _iter_due_weekly_slots(self, now: datetime, *, startup: bool) -> list[datetime]:
        if startup:
            days_since_sunday = (now.weekday() + 1) % 7
            most_recent_sunday = (now - timedelta(days=days_since_sunday)).date()
            slot_dt = self._weekly_slot_for_date(most_recent_sunday)
            return [slot_dt] if slot_dt <= now else []

        if now.weekday() != 6:
            return []
        slot_dt = self._weekly_slot_for_date(now.date())
        return [slot_dt] if slot_dt <= now else []

    def _message_datetime(self, msg) -> datetime:
        ts = getattr(msg, "timestamp", None)
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts, tz=self.timezone)
        if isinstance(ts, datetime):
            return ts.astimezone(self.timezone) if ts.tzinfo else ts.replace(tzinfo=self.timezone)
        return datetime.now(self.timezone)

    def _fetch_email_items_for_window(
        self,
        email_sources: list[dict],
        source_by_name: dict[str, dict],
        *,
        processed_entry_ids: set[str],
        slot_start: datetime,
        slot_end: datetime,
        fetch_articles: bool,
        max_links: int,
    ) -> tuple[list[dict], set[str]]:
        if not email_sources:
            return [], set()

        try:
            from agentmail import AgentMail

            client = AgentMail(api_key=self._config.agentmail_api_key)
            result = client.inboxes.messages.list(
                inbox_id=self._config.agentmail_inbox_id,
                limit=100,
                after=slot_start,
            )
        except Exception:
            logger.warning("AgentMail API call failed", exc_info=True)
            return [], set()

        items: list[dict] = []
        processed_ids: set[str] = set()
        for msg in result.messages:
            msg_id = getattr(msg, "id", None) or getattr(msg, "message_id", "")
            if not msg_id or msg_id in processed_entry_ids or msg_id in processed_ids:
                continue

            msg_text = getattr(msg, "text", None) or getattr(msg, "html", None) or ""
            source_name = self._identify_source(msg_text, email_sources)
            if not source_name:
                continue

            msg_dt = self._message_datetime(msg)
            if msg_dt < slot_start or msg_dt >= slot_end:
                continue

            source = source_by_name.get(source_name, {})
            item = self._email_item_from_message(
                msg,
                source_name=source_name,
                category=source.get("category", "other"),
                fetch_articles=fetch_articles,
                max_links=max_links,
            )
            if item is None:
                continue

            item["date"] = slot_end.strftime("%Y-%m-%d")
            items.append(item)
            processed_ids.add(msg_id)

        return items, processed_ids

    def _collect_items_for_slot(
        self,
        sources: list[dict],
        settings: dict,
        *,
        processed_entry_ids: set[str],
        slot_dt: datetime,
    ) -> tuple[list[dict], set[str]]:
        slot_start = slot_dt - timedelta(days=1)
        run_date = slot_dt.strftime("%Y-%m-%d")
        email_sources, web_sources, social_sources = self._split_sources(sources)
        source_by_name = {source.get("name"): source for source in email_sources}

        fetch_articles = settings.get("fetch_linked_articles", False)
        max_links = int(settings.get("max_links_per_newsletter", 5))

        items: list[dict] = []
        new_processed_ids: set[str] = set()

        email_items, email_ids = self._fetch_email_items_for_window(
            email_sources,
            source_by_name,
            processed_entry_ids=processed_entry_ids,
            slot_start=slot_start,
            slot_end=slot_dt,
            fetch_articles=fetch_articles,
            max_links=max_links,
        )
        items.extend(email_items)
        new_processed_ids.update(email_ids)

        for source in web_sources:
            source_name = str(source.get("name", "")).strip().lower()
            if source_name != "techcrunch":
                logger.warning("Unsupported web news source: %s", source.get("name"))
                continue
            slot_items, processed_ids = self._collect_techcrunch_items(
                source,
                run_date=run_date,
                processed_entry_ids=processed_entry_ids | new_processed_ids,
                window_start=slot_start,
                window_end=slot_dt,
            )
            items.extend(slot_items)
            new_processed_ids.update(processed_ids)

        if social_sources and settings.get("social_fetch_enabled", True):
            for source in social_sources:
                try:
                    slot_items, processed_ids = self._collect_social_items(
                        source,
                        run_date=run_date,
                        processed_entry_ids=processed_entry_ids | new_processed_ids,
                        window_start=slot_start,
                        window_end=slot_dt,
                    )
                except Exception:
                    logger.warning(
                        "Unexpected social source failure: %s",
                        source.get("name"),
                        exc_info=True,
                    )
                    continue
                items.extend(slot_items)
                new_processed_ids.update(processed_ids)

        return items, new_processed_ids

    def _seconds_until_next_scheduled(self) -> int:
        now = datetime.now(self.timezone)

        dh, dm = self._daily_schedule
        daily_candidate = now.replace(hour=dh, minute=dm, second=0, microsecond=0)
        if daily_candidate > now:
            return max(1, int((daily_candidate - now).total_seconds()))

        if now.weekday() == 6:
            wh, wm = self._weekly_schedule
            weekly_candidate = now.replace(hour=wh, minute=wm, second=0, microsecond=0)
            if weekly_candidate > now:
                return max(1, int((weekly_candidate - now).total_seconds()))

        tomorrow = (now + timedelta(days=1)).replace(
            hour=dh, minute=dm, second=0, microsecond=0
        )
        return max(1, int((tomorrow - now).total_seconds()))

    def _apply_settings(self, settings: dict) -> None:
        daily = settings.get("daily_schedule", _DEFAULT_DAILY_SCHEDULE)
        parts = daily.strip().split(":")
        self._daily_schedule = (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

        weekly = settings.get("weekly_schedule", _DEFAULT_WEEKLY_SCHEDULE)
        parts = weekly.strip().split(":")
        self._weekly_schedule = (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

        quiet_spec = settings.get("quiet_hours", "23:00-06:00")
        qparts = quiet_spec.replace("\u2013", "-").split("-")
        self._quiet_start = int(qparts[0].strip().split(":")[0])
        self._quiet_end = int(qparts[1].strip().split(":")[0])

    def tick(self, *, startup: bool = False) -> int:
        if self._is_quiet_hour() and not startup:
            logger.debug("News digest skipped: quiet hours")
            return 0

        config = self._load_config()
        sources = config.get("sources", [])
        if not sources:
            logger.debug("News digest skipped: no sources configured")
            return 0

        settings = config.get("settings", {})
        self._apply_settings(settings)

        if self._is_quiet_hour() and not startup:
            logger.debug("News digest skipped: quiet hours (after settings load)")
            return 0

        state = self._load_state()
        processed_entry_ids = self._load_processed_entry_ids(state)
        new_processed_ids: set[str] = set()
        now = datetime.now(self.timezone)
        enqueued = 0

        for slot_dt in self._iter_due_daily_slots(now, startup=startup):
            slot_key = self._slot_key(slot_dt)
            if not self._ledger.should_enqueue(self.name, "daily", slot_key):
                continue

            date = slot_dt.strftime("%Y-%m-%d")
            items, processed_ids = self._collect_items_for_slot(
                sources,
                settings,
                processed_entry_ids=processed_entry_ids | new_processed_ids,
                slot_dt=slot_dt,
            )
            new_processed_ids.update(processed_ids)
            if not items:
                self._ledger.mark_skipped_empty(
                    self.name,
                    "daily",
                    slot_key,
                    scheduled_for=slot_dt.isoformat(),
                    metadata={"date": date},
                )
                continue

            merged_items = self._merge_story_items(
                items,
                merge_window_hours=int(settings.get("social_story_merge_window_hours", 48)),
                similarity_threshold=float(settings.get("social_dedupe_threshold", 0.65)),
            )
            payload_items = [self._sanitize_item_for_payload(item) for item in merged_items]
            event = Event(
                type="news_digest",
                payload={
                    "date": date,
                    "items": payload_items,
                    "_schedule": self._scheduled_payload(
                        job_type="daily",
                        slot_dt=slot_dt,
                        metadata={"date": date},
                    ),
                },
                source="news_digest",
            )
            event_id = self.queue.insert_event(event)
            self.queue.insert_job(Job(event_id=event_id, skill="news_digest"))
            logger.info("News digest enqueued for %s (%d items)", date, len(payload_items))
            self._ledger.mark_enqueued(
                self.name,
                "daily",
                slot_key,
                scheduled_for=slot_dt.isoformat(),
                metadata={"date": date},
            )
            enqueued += 1

        for slot_dt in self._iter_due_weekly_slots(now, startup=startup):
            slot_key = self._slot_key(slot_dt)
            if not self._ledger.should_enqueue(self.name, "weekly", slot_key):
                continue
            week_label = slot_dt.strftime("%Y-W%V")
            event = Event(
                type="news_weekly",
                payload={
                    "week_label": week_label,
                    "_schedule": self._scheduled_payload(
                        job_type="weekly",
                        slot_dt=slot_dt,
                        metadata={"week_label": week_label},
                    ),
                },
                source="news_digest",
            )
            event_id = self.queue.insert_event(event)
            self.queue.insert_job(Job(event_id=event_id, skill="news_weekly"))
            logger.info("News weekly enqueued for %s", week_label)
            self._ledger.mark_enqueued(
                self.name,
                "weekly",
                slot_key,
                scheduled_for=slot_dt.isoformat(),
                metadata={"week_label": week_label},
            )
            state["last_weekly_generated"] = week_label
            enqueued += 1

        state["last_checked_at"] = time.time()
        self._store_processed_entry_ids(state, processed_entry_ids | new_processed_ids)
        self._save_state(state)

        if enqueued:
            logger.info("News digest tick: %d events enqueued", enqueued)
        return enqueued

    async def start(self) -> None:
        self._running = True
        self._schedule_next(2)
        logger.info(
            "News digest adapter started (daily=%02d:%02d, weekly=%02d:%02d, startup tick in 2s)",
            *self._daily_schedule,
            *self._weekly_schedule,
        )

    async def stop(self) -> None:
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def send_message_sync(self, chat_id: str, text: str) -> None:
        """No-op: digest adapter doesn't send messages."""

    def send_typing_sync(self, chat_id: str) -> None:
        """No-op: digest adapter doesn't send typing indicators."""

    def _schedule_next(self, delay_seconds: int) -> None:
        if not self._running:
            return
        self._timer = threading.Timer(delay_seconds, self._on_timer)
        self._timer.daemon = True
        self._timer.start()

    def _on_timer(self) -> None:
        startup = self._startup_replay_pending
        self._startup_replay_pending = False
        try:
            self.tick(startup=startup)
        except Exception:
            logger.error("News digest tick failed", exc_info=True)
        finally:
            if self._running:
                delay = self._seconds_until_next_scheduled()
                next_time = datetime.now(self.timezone) + timedelta(seconds=delay)
                logger.info(
                    "Next news digest tick at %s (%ds)",
                    next_time.strftime("%H:%M"),
                    delay,
                )
                self._schedule_next(delay)
