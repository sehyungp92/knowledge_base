from __future__ import annotations

import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch


def _make_adapter(tmp_path):
    from adapters.news_digest import NewsDigestAdapter

    config_path = tmp_path / "news_digest_config.yaml"
    state_path = tmp_path / "news_digest_state.json"
    queue = MagicMock()
    queue.insert_event.return_value = 1
    config = MagicMock()
    config.agentmail_api_key = "test-key"
    config.agentmail_inbox_id = "test@agentmail.to"

    return NewsDigestAdapter(
        queue=queue,
        config=config,
        config_path=config_path,
        state_path=state_path,
    )


class TestTechCrunchCandidateExtraction:
    def test_content_scoping_tolerates_detached_nodes(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        html = """
        <html>
          <body>
            <main>
              <div class="cookie-banner">
                <span style="display:none">Hidden text</span>
                <div>Banner content</div>
              </div>
              <article>
                <h1>Real content</h1>
                <p>This article body is long enough to pass the content threshold.</p>
                <p>This second paragraph keeps the scoped region comfortably over one hundred characters.</p>
              </article>
            </main>
          </body>
        </html>
        """

        scoped_html = adapter._scope_html_to_content(html, preserve_structured_data=True)

        assert "Real content" in scoped_html

    def test_extracts_loop_card_candidates(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        html = """
        <html><body>
          <ul class="wp-block-post-template">
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title">
                  <a href="https://techcrunch.com/2026/03/09/ai-startup-raises-12m/">AI startup raises $12M</a>
                </h3>
                <time datetime="2026-03-09T10:00:00-07:00" class="loop-card__time">2 hours ago</time>
              </div>
            </li>
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title">
                  <a href="/2026/03/09/new-coding-agent-benchmark/">New coding agent benchmark</a>
                </h3>
                <time datetime="2026-03-09T08:30:00-07:00" class="loop-card__time">4 hours ago</time>
              </div>
            </li>
          </ul>
        </body></html>
        """

        candidates = adapter._extract_techcrunch_candidates(
            html,
            "https://techcrunch.com/category/artificial-intelligence/",
        )

        assert len(candidates) == 2
        assert candidates[0]["url"].startswith("https://techcrunch.com/2026/03/09/")
        assert candidates[0]["subject"]
        assert candidates[0]["published_at"] is not None

    def test_extracts_json_ld_candidates_and_canonicalizes_urls(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        html = """
        <html>
          <head>
            <script type="application/ld+json">
              {
                "@context": "https://schema.org",
                "@graph": [
                  {
                    "@type": ["Thing", "NewsArticle"],
                    "url": "https://techcrunch.com/2026/03/09/ai-startup-raises-12m/?utm_source=newsletter#fragment",
                    "headline": "AI startup raises $12M | TechCrunch",
                    "datePublished": "2026-03-09T17:00:00Z"
                  }
                ]
              }
            </script>
          </head>
          <body><main><div>Listing body</div></main></body>
        </html>
        """

        candidates = adapter._extract_techcrunch_candidates(
            html,
            "https://techcrunch.com/category/artificial-intelligence/",
        )

        assert len(candidates) == 1
        assert candidates[0]["url"] == "https://techcrunch.com/2026/03/09/ai-startup-raises-12m/"
        assert candidates[0]["subject"] == "AI startup raises $12M"
        assert candidates[0]["published_at"] is not None

    def test_extracts_feed_candidates(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        xml = """
        <rss version="2.0">
          <channel>
            <item>
              <title>AI startup raises $12M</title>
              <link>https://techcrunch.com/2026/03/09/ai-startup-raises-12m/?utm_source=rss#fragment</link>
              <pubDate>Mon, 09 Mar 2026 17:00:00 GMT</pubDate>
              <category>AI</category>
              <description>Seed funding for an enterprise AI startup.</description>
            </item>
          </channel>
        </rss>
        """

        candidates = adapter._extract_techcrunch_feed_candidates(
            xml,
            "https://techcrunch.com/category/artificial-intelligence/feed/",
        )

        assert len(candidates) == 1
        assert candidates[0]["url"] == "https://techcrunch.com/2026/03/09/ai-startup-raises-12m/"
        assert candidates[0]["subject"] == "AI startup raises $12M"
        assert candidates[0]["published_at"] is not None


class TestTechCrunchClassification:
    def test_cleans_techcrunch_title_suffix(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        assert adapter._clean_techcrunch_title("New coding agent benchmark | TechCrunch") == "New coding agent benchmark"

    def test_routes_startups(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "AI startup raises $12M seed round",
            "Artificial Intelligence",
            "The startup raised $12M in a seed funding round led by a VC firm.",
        )
        assert result is not None
        assert result["primary"] == "startups"

    def test_routes_capabilities(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "OpenAI launches a new coding agent",
            "Artificial Intelligence",
            "The company released a new coding agent with stronger reasoning and benchmark gains.",
        )
        assert result is not None
        assert result["primary"] == "capabilities"

    def test_routes_capabilities_from_open_weight_features(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "Mistral ships an open-weight voice model",
            "Artificial Intelligence",
            "The open-weight voice model adds browser and tool use for enterprise deployments.",
        )
        assert result is not None
        assert result["primary"] == "capabilities"

    def test_routes_breakthroughs_from_infrastructure_terms(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "New serving stack cuts inference latency for frontier models",
            "Artificial Intelligence",
            "Researchers built a new serving architecture and distillation pipeline that improves throughput and lowers latency for model inference.",
        )
        assert result is not None
        assert result["primary"] == "breakthroughs"

    def test_excludes_policy_only_articles(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "Lawmakers debate new AI regulation",
            "Government & Policy",
            "Congress is considering a new regulatory framework and legal obligations for AI companies.",
        )
        assert result is None

    def test_excludes_human_interest_ai_story(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        result = adapter._classify_techcrunch_article(
            "AI actor releases a new song",
            "Artificial Intelligence",
            "An AI-generated song went viral online and drew reactions from fans across social media and entertainment circles.",
        )
        assert result is None


class TestTechCrunchCollection:
    @patch("ingest.stealth_fetch.fetch_html_stealth")
    @patch("ingest.article._fetch_html", side_effect=RuntimeError("blocked"))
    def test_fetch_article_uses_stealth_when_primary_fetch_fails(
        self,
        _mock_fetch_html,
        mock_stealth,
        tmp_path,
    ):
        adapter = _make_adapter(tmp_path)
        mock_stealth.return_value = """
        <html>
          <head>
            <title>New coding agent benchmark | TechCrunch</title>
          </head>
          <body>
            <main>
              <article>
                <time datetime="2026-03-09T17:00:00Z">March 9, 2026</time>
                <p>The release introduces a coding agent with stronger reasoning, faster execution, and much better benchmark performance for real developer workflows.</p>
                <p>Teams can hand off multi-step debugging and implementation tasks while keeping a human in the loop for review and final approval.</p>
              </article>
            </main>
          </body>
        </html>
        """

        article = adapter._fetch_techcrunch_article(
            "https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/"
        )

        assert article is not None
        assert article["subject"] == "New coding agent benchmark"
        assert "coding agent" in article["clean_text"].lower()

    @patch("ingest.article._fetch_html")
    def test_collects_recent_items_and_routes_by_topic(self, mock_fetch_html, tmp_path):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        listing_html = """
        <html><body>
          <ul class="wp-block-post-template">
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title"><a href="https://techcrunch.com/2026/03/09/ai-startup-raises-12m/">AI startup raises $12M</a></h3>
                <time datetime="2026-03-09T10:00:00-07:00" class="loop-card__time">2 hours ago</time>
              </div>
            </li>
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title"><a href="https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/">New coding agent benchmark</a></h3>
                <time datetime="2026-03-09T08:30:00-07:00" class="loop-card__time">4 hours ago</time>
              </div>
            </li>
          </ul>
        </body></html>
        """
        mock_fetch_html.return_value = listing_html

        def fake_fetch_article(url: str):
            if "raises" in url:
                return {
                    "subject": "AI startup raises $12M",
                    "published_at": now - timedelta(hours=2),
                    "clean_text": "The startup raised $12M in seed funding from a venture capital firm.",
                }
            return {
                "subject": "New coding agent benchmark",
                "published_at": now - timedelta(hours=3),
                "clean_text": "The release introduces a coding agent with stronger reasoning and benchmark gains.",
            }

        adapter._fetch_techcrunch_article = fake_fetch_article
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date=now.strftime("%Y-%m-%d"),
            processed_entry_ids=set(),
        )

        assert len(items) == 2
        by_subject = {item["subject"]: item for item in items}
        assert by_subject["AI startup raises $12M"]["category"] == "startups"
        assert by_subject["New coding agent benchmark"]["category"] == "ai_tech"
        assert all(processed_id.startswith("techcrunch:") for processed_id in processed_ids)

    @patch("ingest.stealth_fetch.fetch_html_stealth", return_value="<html><body></body></html>")
    @patch("ingest.article._fetch_html")
    def test_falls_back_to_feed_when_listing_markup_drifts(
        self,
        mock_fetch_html,
        _mock_stealth,
        tmp_path,
    ):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        listing_url = "https://techcrunch.com/category/artificial-intelligence/"
        feed_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        listing_html = f"""
        <html>
          <head>
            <link rel="alternate" type="application/rss+xml" title="TechCrunch AI Category Feed" href="{feed_url}" />
          </head>
          <body><main><div>No usable cards here</div></main></body>
        </html>
        """
        feed_xml = """
        <rss version="2.0">
          <channel>
            <item>
              <title>AI startup raises $12M</title>
              <link>https://techcrunch.com/2026/03/09/ai-startup-raises-12m/</link>
              <pubDate>Mon, 09 Mar 2026 17:00:00 GMT</pubDate>
              <category>AI</category>
              <description>Seed funding for an enterprise AI startup.</description>
            </item>
          </channel>
        </rss>
        """

        def fake_fetch_html(url: str, timeout: int = 20):
            if url == listing_url:
                return listing_html
            if url == feed_url:
                return feed_xml
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_fetch_html.side_effect = fake_fetch_html
        adapter._fetch_techcrunch_article = lambda _url: {
            "subject": "AI startup raises $12M",
            "published_at": now - timedelta(hours=2),
            "clean_text": "The startup raised $12M in seed funding from a venture capital firm.",
        }
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": listing_url,
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date=now.strftime("%Y-%m-%d"),
            processed_entry_ids=set(),
        )

        assert len(items) == 1
        assert items[0]["category"] == "startups"
        assert processed_ids == {"techcrunch:https://techcrunch.com/2026/03/09/ai-startup-raises-12m/"}

    @patch("ingest.stealth_fetch.fetch_html_stealth", side_effect=RuntimeError("no browser fallback"))
    @patch("ingest.article._fetch_html")
    def test_falls_back_to_feed_when_listing_fetch_fails(
        self,
        mock_fetch_html,
        _mock_stealth,
        tmp_path,
    ):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        listing_url = "https://techcrunch.com/category/artificial-intelligence/"
        feed_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        feed_xml = """
        <rss version="2.0">
          <channel>
            <item>
              <title>New coding agent benchmark</title>
              <link>https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/</link>
              <pubDate>Mon, 09 Mar 2026 16:00:00 GMT</pubDate>
              <category>AI</category>
              <description>A new coding agent improves reasoning and benchmark performance.</description>
            </item>
          </channel>
        </rss>
        """

        def fake_fetch_html(url: str, timeout: int = 20):
            if url == listing_url:
                raise RuntimeError("listing unavailable")
            if url == feed_url:
                return feed_xml
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_fetch_html.side_effect = fake_fetch_html
        adapter._fetch_techcrunch_article = lambda _url: {
            "subject": "New coding agent benchmark",
            "published_at": now - timedelta(hours=2),
            "clean_text": "The release introduces a coding agent with stronger reasoning and benchmark gains.",
        }
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": listing_url,
            "feed_url": feed_url,
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date=now.strftime("%Y-%m-%d"),
            processed_entry_ids=set(),
        )

        assert len(items) == 1
        assert items[0]["category"] == "ai_tech"
        assert processed_ids == {"techcrunch:https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/"}

    @patch("ingest.article._fetch_html")
    def test_skips_articles_older_than_lookback(self, mock_fetch_html, tmp_path):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        mock_fetch_html.return_value = """
        <html><body>
          <ul class="wp-block-post-template">
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title"><a href="https://techcrunch.com/2026/03/08/older-ai-startup-round/">Older AI startup round</a></h3>
                <time datetime="2026-03-08T08:00:00-07:00" class="loop-card__time">Yesterday</time>
              </div>
            </li>
          </ul>
        </body></html>
        """

        adapter._fetch_techcrunch_article = lambda _url: {
            "subject": "Older AI startup round",
            "published_at": now - timedelta(hours=30),
            "clean_text": "The startup raised funding yesterday from several investors.",
        }
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date=now.strftime("%Y-%m-%d"),
            processed_entry_ids=set(),
        )

        assert items == []
        assert processed_ids == set()

    @patch("ingest.stealth_fetch.fetch_html_stealth", return_value="<html><body></body></html>")
    @patch("ingest.article._fetch_html")
    def test_writes_drift_artifact_when_listing_and_feed_fail(
        self,
        mock_fetch_html,
        _mock_stealth,
        tmp_path,
    ):
        adapter = _make_adapter(tmp_path)
        listing_url = "https://techcrunch.com/category/artificial-intelligence/"
        feed_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        listing_html = f"""
        <html>
          <head>
            <link rel="alternate" type="application/rss+xml" title="TechCrunch AI Category Feed" href="{feed_url}" />
          </head>
          <body><main><div>No usable cards here</div></main></body>
        </html>
        """

        def fake_fetch_html(url: str, timeout: int = 20):
            if url == listing_url:
                return listing_html
            if url == feed_url:
                return "<rss version='2.0'><channel></channel></rss>"
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_fetch_html.side_effect = fake_fetch_html
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": listing_url,
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date="2026-03-09",
            processed_entry_ids=set(),
        )

        drift_dir = tmp_path / "news_digest_techcrunch_drift"
        assert items == []
        assert processed_ids == set()
        assert drift_dir.exists()
        assert any(path.suffix == ".json" for path in drift_dir.iterdir())
        assert any(path.name.endswith(".listing.html") for path in drift_dir.iterdir())
        assert any(path.name.endswith(".feed.xml") for path in drift_dir.iterdir())

    @patch("ingest.article._fetch_html")
    def test_uses_excerpt_fallback_when_article_fetch_fails(self, mock_fetch_html, tmp_path):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        listing_published_at = (now - timedelta(hours=2)).isoformat()
        mock_fetch_html.return_value = """
        <html><body>
          <ul class="wp-block-post-template">
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title"><a href="https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/">New coding agent benchmark</a></h3>
                <p>The release introduces a coding agent with stronger reasoning, better benchmark performance, and improved workflow automation for developers.</p>
                <time datetime="__LISTING_PUBLISHED_AT__" class="loop-card__time">2 hours ago</time>
              </div>
            </li>
          </ul>
        </body></html>
        """.replace("__LISTING_PUBLISHED_AT__", listing_published_at)
        adapter._fetch_techcrunch_article = lambda _url: None
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date=now.strftime("%Y-%m-%d"),
            processed_entry_ids=set(),
        )

        assert len(items) == 1
        assert items[0]["category"] == "ai_tech"
        assert "coding agent" in items[0]["clean_text"].lower()
        assert processed_ids == {"techcrunch:https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/"}

    @patch("ingest.article._fetch_html")
    def test_writes_triage_artifact_when_recent_candidates_are_rejected(self, mock_fetch_html, tmp_path):
        adapter = _make_adapter(tmp_path)
        now = datetime.now(adapter.timezone)
        listing_published_at = (now - timedelta(hours=2)).isoformat()
        mock_fetch_html.return_value = """
        <html><body>
          <ul class="wp-block-post-template">
            <li class="wp-block-post">
              <div class="loop-card__content">
                <span class="loop-card__cat">Artificial Intelligence</span>
                <h3 class="loop-card__title"><a href="https://techcrunch.com/2026/03/09/ai-actor-song/">AI actor releases a new song</a></h3>
                <time datetime="__LISTING_PUBLISHED_AT__" class="loop-card__time">2 hours ago</time>
              </div>
            </li>
          </ul>
        </body></html>
        """.replace("__LISTING_PUBLISHED_AT__", listing_published_at)
        adapter._fetch_techcrunch_article = lambda _url: {
            "subject": "AI actor releases a new song",
            "published_at": now - timedelta(hours=2),
            "clean_text": "An AI-generated song went viral online and drew reactions from fans across social media and entertainment circles.",
        }
        source = {
            "name": "TechCrunch",
            "delivery": "web",
            "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
            "lookback_hours": 24,
            "max_items": 8,
            "include_topics": ["capabilities", "breakthroughs", "startups"],
            "topic_routes": {
                "capabilities": "ai_tech",
                "breakthroughs": "ai_tech",
                "startups": "startups",
            },
        }

        items, processed_ids = adapter._collect_techcrunch_items(
            source,
            run_date="2026-03-09",
            processed_entry_ids=set(),
        )

        triage_dir = tmp_path / "news_digest_techcrunch_triage"
        triage_files = list(triage_dir.glob("*.json"))
        assert items == []
        assert processed_ids == set()
        assert triage_files
        payload = json.loads(triage_files[0].read_text(encoding="utf-8"))
        assert payload["accepted_count"] == 0
        assert payload["recent_candidate_count"] == 1
        assert payload["rejected_candidates"][0]["reason"] == "non_target_human_interest"


class TestMixedSourceTick:
    @patch.dict("sys.modules", {"agentmail": MagicMock()})
    def test_tick_enqueues_items_payload_for_email_and_techcrunch(self, tmp_path):
        import yaml

        from reading_app.scheduler_ledger import SchedulerLedger

        adapter = _make_adapter(tmp_path)
        adapter._ledger = SchedulerLedger(tmp_path / "scheduler.db")
        adapter._is_quiet_hour = lambda: False
        # Use a fixed noon timestamp to avoid midnight boundary flakiness.
        # Return fixed_now from _iter_due_daily_slots instead of tick's
        # datetime.now() so the payload date is deterministic.
        fixed_now = datetime(2026, 3, 9, 12, 0, 0, tzinfo=adapter.timezone)
        now = fixed_now
        adapter._iter_due_daily_slots = lambda _now, startup: [fixed_now]
        adapter._iter_due_weekly_slots = lambda _now, startup: []

        config = {
            "sources": [
                {
                    "name": "AINews",
                    "delivery": "email",
                    "sender": "swyx+ainews@substack.com",
                    "category": "ai_tech",
                },
                {
                    "name": "TechCrunch",
                    "delivery": "web",
                    "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
                    "lookback_hours": 24,
                    "max_items": 8,
                    "include_topics": ["capabilities", "breakthroughs", "startups"],
                    "topic_routes": {
                        "capabilities": "ai_tech",
                        "breakthroughs": "ai_tech",
                        "startups": "startups",
                    },
                },
            ],
            "settings": {
                "daily_schedule": "10:00",
                "weekly_schedule": "19:00",
                "quiet_hours": "23:00-06:00",
                "fetch_linked_articles": False,
                "max_links_per_newsletter": 5,
            },
        }
        adapter._config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

        msg = MagicMock()
        msg.id = "msg_1"
        msg.text = (
            "---------- Forwarded message ---------\n"
            "From: AINews <swyx+ainews@substack.com>\n"
            "Date: Mon, 9 Mar 2026\n"
            "Subject: AI News\n\n"
            "OpenAI released a new multimodal model with stronger coding skills."
        )
        msg.html = None
        msg.extracted_text = None
        msg.subject = "AI News"
        msg.timestamp = fixed_now - timedelta(hours=2)

        mock_client = MagicMock()
        mock_client.inboxes.messages.list.return_value = MagicMock(messages=[msg])
        import sys
        sys.modules["agentmail"].AgentMail.return_value = mock_client

        adapter._collect_techcrunch_items = MagicMock(
            return_value=(
                [
                    {
                        "kind": "article",
                        "source": "TechCrunch",
                        "category": "startups",
                        "subject": "AI startup raises $12M",
                        "url": "https://techcrunch.com/2026/03/09/ai-startup-raises-12m/",
                        "published_at": now.isoformat(),
                        "topic_tags": ["startups"],
                        "clean_text": "The startup raised $12M in seed funding.",
                        "links_context": [],
                    }
                ],
                {"techcrunch:https://techcrunch.com/2026/03/09/ai-startup-raises-12m/"},
            )
        )

        result = adapter.tick(startup=True)

        assert result == 1
        adapter.queue.insert_event.assert_called_once()
        event = adapter.queue.insert_event.call_args[0][0]
        assert event.payload["date"] == "2026-03-09"
        assert "items" in event.payload
        assert len(event.payload["items"]) == 2

        saved_state = json.loads(adapter._state_path.read_text(encoding="utf-8"))
        assert "msg_1" in saved_state["processed_entry_ids"]
        assert any(entry.startswith("techcrunch:") for entry in saved_state["processed_entry_ids"])


class TestHandlerItemsPayload:
    @patch("gateway.news_digest_handler.load_digest_voice", return_value="")
    @patch("gateway.news_digest_handler.gather_landscape_briefing", return_value="")
    @patch("gateway.news_digest_handler.scan_digest_for_signals", return_value={
        "anticipation_flags": [],
        "bottleneck_signals": [],
        "belief_tensions": [],
    })
    @patch("gateway.news_digest_handler.persist_signal_scan_results", return_value={})
    @patch("gateway.news_digest_handler.send_signal_alerts", return_value={})
    @patch("gateway.news_digest_handler.send_digest_email", return_value=True)
    @patch("gateway.news_digest_handler.send_telegram_message", return_value=False)
    def test_handler_uses_items_payload_and_includes_techcrunch_metadata(
        self,
        _mock_telegram,
        _mock_email,
        _mock_alerts,
        _mock_persist,
        _mock_scan,
        _mock_briefing,
        _mock_voice,
        tmp_path,
        monkeypatch,
    ):
        from gateway.models import Event, Job
        from gateway.news_digest_handler import handle_news_digest_job

        monkeypatch.chdir(tmp_path)
        (tmp_path / "var" / "news_digests" / "daily").mkdir(parents=True)

        event = Event(
            type="news_digest",
            payload={
                "date": "2026-03-09",
                "items": [
                    {
                        "kind": "article",
                        "source": "TechCrunch",
                        "category": "ai_tech",
                        "subject": "New coding agent benchmark",
                        "url": "https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/",
                        "published_at": "2026-03-09T10:00:00-07:00",
                        "topic_tags": ["capabilities"],
                        "clean_text": "The release introduces a new coding agent with strong benchmark gains.",
                        "links_context": [],
                    }
                ],
            },
            source="news_digest",
            id=1,
        )
        job = Job(event_id=1, skill="news_digest", id=1)
        executor = MagicMock()
        executor.run_raw.return_value = MagicMock(text="# Daily Digest -- 2026-03-09\n")
        config = MagicMock()

        handle_news_digest_job(event, job, config, executor)

        prompt = executor.run_raw.call_args.kwargs["prompt"]
        assert "SOURCE MATERIALS" in prompt
        assert "Topic Tags: capabilities" in prompt
        assert "URL: https://techcrunch.com/2026/03/09/new-coding-agent-benchmark/" in prompt
