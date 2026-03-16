from __future__ import annotations

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
    config.runtime_db_path = tmp_path / "runtime.db"

    return NewsDigestAdapter(
        queue=queue,
        config=config,
        config_path=config_path,
        state_path=state_path,
    )


def _make_fetcher():
    from ingest.social_media import SocialMediaFetcher

    return SocialMediaFetcher("America/New_York")


def _response(payload):
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = payload
    return response


class TestSocialScoring:
    def test_reddit_top_comment_bonus_improves_score(self):
        fetcher = _make_fetcher()
        now = datetime.now(fetcher.timezone).isoformat()
        source_cfg = {"min_score_threshold": 0, "native_discussion_floor": 0}
        base_item = {
            "kind": "social",
            "platform": "reddit",
            "subject": "New AI startup raises seed funding",
            "clean_text": "New AI startup raises seed funding and expands product capabilities.",
            "published_at": now,
            "url": "https://example.com/story/",
            "discussion_url": "https://www.reddit.com/r/ArtificialIntelligence/comments/abc/story/",
            "category": "startups",
            "topic_tags": ["startups"],
            "story_key": "https://example.com/story/",
            "_classification": {"primary": "startups", "scores": {"startups": 6}},
            "social_proof": [{
                "platform": "reddit",
                "discussion_url": "https://www.reddit.com/r/ArtificialIntelligence/comments/abc/story/",
                "subreddit": "ArtificialIntelligence",
                "points": 120,
                "comments": 40,
                "upvote_ratio": 0.95,
                "top_comment_score": 0,
            }],
        }
        boosted_item = {
            **base_item,
            "discussion_url": "https://www.reddit.com/r/ArtificialIntelligence/comments/def/story/",
            "social_proof": [{
                "platform": "reddit",
                "discussion_url": "https://www.reddit.com/r/ArtificialIntelligence/comments/def/story/",
                "subreddit": "ArtificialIntelligence",
                "points": 120,
                "comments": 40,
                "upvote_ratio": 0.95,
                "top_comment_score": 250,
            }],
        }

        scored = fetcher.score_items([base_item, boosted_item], source_cfg)
        assert scored[1]["score"] > scored[0]["score"]

    def test_score_items_use_window_end_for_replay_recency(self):
        fetcher = _make_fetcher()
        source_cfg = {
            "lookback_hours": 24,
            "min_score_threshold": 0,
            "native_discussion_floor": 0,
            "_window_end": "2026-03-10T12:00:00-04:00",
        }
        item = {
            "kind": "social",
            "platform": "reddit",
            "subject": "AI coding agent launch",
            "clean_text": "AI coding agent launch reaches developers and benchmark results look strong.",
            "published_at": "2026-03-10T11:30:00-04:00",
            "url": "https://example.com/agent-launch/",
            "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/agent_launch/",
            "category": "ai_tech",
            "topic_tags": ["capabilities"],
            "story_key": "https://example.com/agent-launch/",
            "_classification": {"primary": "capabilities", "scores": {"capabilities": 6}},
            "social_proof": [{
                "platform": "reddit",
                "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/agent_launch/",
                "subreddit": "MachineLearning",
                "points": 120,
                "comments": 20,
                "upvote_ratio": 0.95,
            }],
        }

        scored = fetcher.score_items([item], source_cfg)

        assert scored[0]["social_subscores"]["recency"] >= 90

    def test_fetch_x_items_skips_without_token(self, monkeypatch):
        monkeypatch.delenv("X_BEARER_TOKEN", raising=False)
        fetcher = _make_fetcher()
        source_cfg = {
            "name": "TwitterX",
            "platform": "x",
            "queries": ["AI"],
            "max_candidates": 10,
            "max_items": 5,
        }

        assert fetcher.fetch_x_items(source_cfg) == []

    @patch("ingest.social_media.httpx.get")
    def test_fetch_x_items_allows_native_discussions_when_links_are_not_required(self, mock_get, monkeypatch):
        monkeypatch.setenv("X_BEARER_TOKEN", "test-token")
        fetcher = _make_fetcher()
        now = datetime.now(fetcher.timezone)

        mock_get.return_value = _response({
            "data": [{
                "id": "tweet123",
                "author_id": "user123",
                "created_at": now.isoformat(),
                "text": "New AI coding agent launch shows big benchmark gains for developers.",
                "public_metrics": {
                    "like_count": 120,
                    "retweet_count": 25,
                    "reply_count": 18,
                    "quote_count": 3,
                },
                "entities": {"urls": []},
            }],
            "includes": {
                "users": [{
                    "id": "user123",
                    "username": "builder",
                }]
            },
        })

        source_cfg = {
            "name": "TwitterX",
            "platform": "x",
            "queries": ["AI"],
            "lookback_hours": 24,
            "max_candidates": 10,
            "max_items": 5,
            "min_score_threshold": 0,
            "require_linked_url": False,
            "topic_routes": {"capabilities": "ai_tech"},
        }

        items = fetcher.fetch_x_items(source_cfg)

        assert len(items) == 1
        assert items[0]["url"] == ""
        assert items[0]["discussion_url"] == "https://x.com/i/web/status/tweet123"
        assert mock_get.call_count == 2


class TestSocialFetchers:
    @patch("ingest.social_media.httpx.get")
    def test_fetch_reddit_items_collects_top_comment_and_external_url(self, mock_get):
        fetcher = _make_fetcher()
        now = datetime.now(fetcher.timezone)

        def fake_get(url, **kwargs):
            if url.endswith("/top.json"):
                return _response({
                    "data": {
                        "children": [{
                            "data": {
                                "id": "abc123",
                                "created_utc": now.timestamp(),
                                "title": "AI startup raises $12M to scale its coding agents",
                                "selftext": "The company says its agents now help engineering teams ship faster.",
                                "permalink": "/r/ArtificialIntelligence/comments/abc123/ai_startup_raises_12m/",
                                "url": "https://example.com/ai-startup-raises-12m",
                                "author": "founderfan",
                                "subreddit": "ArtificialIntelligence",
                                "score": 300,
                                "num_comments": 55,
                                "upvote_ratio": 0.97,
                            }
                        }]
                    }
                })
            if url.endswith("/new.json"):
                return _response({"data": {"children": []}})
            if url.endswith(".json"):
                return _response([
                    {},
                    {
                        "data": {
                            "children": [{
                                "data": {
                                    "body": "This is the strongest discussion thread because the launch includes real revenue proof.",
                                    "score": 87,
                                }
                            }]
                        }
                    },
                ])
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_get.side_effect = fake_get
        source_cfg = {
            "name": "Reddit",
            "platform": "reddit",
            "subreddits": ["ArtificialIntelligence"],
            "sorts": ["top_day", "new"],
            "lookback_hours": 24,
            "max_candidates": 10,
            "max_items": 5,
            "min_score_threshold": 0,
            "native_discussion_floor": 0,
            "topic_routes": {"startups": "startups"},
        }

        items = fetcher.fetch_reddit_items(source_cfg)

        assert len(items) == 1
        item = items[0]
        assert item["url"] == "https://example.com/ai-startup-raises-12m/"
        assert item["discussion_url"].startswith("https://www.reddit.com/r/ArtificialIntelligence/")
        assert item["social_proof"][0]["top_comment"].startswith("This is the strongest discussion thread")

    @patch("ingest.social_media.httpx.get")
    def test_fetch_reddit_items_skip_native_posts_when_links_are_required(self, mock_get):
        fetcher = _make_fetcher()
        now = datetime.now(fetcher.timezone)

        def fake_get(url, **kwargs):
            if url.endswith("/top.json"):
                return _response({
                    "data": {
                        "children": [{
                            "data": {
                                "id": "native123",
                                "created_utc": now.timestamp(),
                                "title": "AI coding agent launch sparks developer debate",
                                "selftext": "This self post describes a concrete launch with benchmark gains.",
                                "permalink": "/r/MachineLearning/comments/native123/agent_launch/",
                                "url": "https://www.reddit.com/r/MachineLearning/comments/native123/agent_launch/",
                                "author": "opsfan",
                                "subreddit": "MachineLearning",
                                "score": 250,
                                "num_comments": 40,
                                "upvote_ratio": 0.96,
                            }
                        }]
                    }
                })
            if url.endswith("/new.json"):
                return _response({"data": {"children": []}})
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_get.side_effect = fake_get
        source_cfg = {
            "name": "Reddit",
            "platform": "reddit",
            "subreddits": ["MachineLearning"],
            "sorts": ["top_day", "new"],
            "lookback_hours": 24,
            "max_candidates": 10,
            "max_items": 5,
            "min_score_threshold": 0,
            "require_linked_url": True,
            "topic_routes": {"capabilities": "ai_tech"},
        }

        assert fetcher.fetch_reddit_items(source_cfg) == []

    @patch("ingest.social_media.httpx.get")
    def test_fetch_reddit_items_widen_top_window_for_replay(self, mock_get):
        fetcher = _make_fetcher()

        def fake_get(url, **kwargs):
            if url.endswith("/top.json"):
                assert kwargs["params"]["t"] == "week"
                return _response({"data": {"children": []}})
            if url.endswith("/new.json"):
                return _response({"data": {"children": []}})
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_get.side_effect = fake_get
        source_cfg = {
            "name": "Reddit",
            "platform": "reddit",
            "subreddits": ["MachineLearning"],
            "sorts": ["top_day", "new"],
            "lookback_hours": 24,
            "_fetch_lookback_hours": 72,
        }

        assert fetcher.fetch_reddit_items(source_cfg) == []

    @patch("ingest.social_media.httpx.get")
    def test_fetch_hn_items_enriches_top_comment(self, mock_get):
        fetcher = _make_fetcher()
        now = datetime.now(fetcher.timezone)

        def fake_get(url, **kwargs):
            if "hn.algolia.com/api/v1/search" in url:
                return _response({
                    "hits": [{
                        "objectID": "999",
                        "created_at": now.isoformat(),
                        "title": "Open-source multimodal model hits new efficiency milestone",
                        "url": "https://example.com/multimodal-model",
                        "author": "pg",
                        "points": 220,
                        "num_comments": 91,
                    }]
                })
            if "hn.algolia.com/api/v1/items/999" in url:
                return _response({
                    "children": [{
                        "text": "<p>The interesting part is the inference efficiency, not just the benchmark headline.</p>",
                        "points": 42,
                    }]
                })
            raise AssertionError(f"Unexpected URL fetched: {url}")

        mock_get.side_effect = fake_get
        source_cfg = {
            "name": "HackerNews",
            "platform": "hn",
            "queries": ["AI"],
            "lookback_hours": 24,
            "max_candidates": 10,
            "max_items": 5,
            "min_score_threshold": 0,
            "native_discussion_floor": 0,
            "enrich_top_comments": 1,
            "topic_routes": {"breakthroughs": "ai_tech"},
        }

        items = fetcher.fetch_hn_items(source_cfg)

        assert len(items) == 1
        item = items[0]
        assert item["url"] == "https://example.com/multimodal-model/"
        assert item["discussion_url"] == "https://news.ycombinator.com/item?id=999"
        assert "inference efficiency" in item["social_proof"][0]["top_comment"]


class TestAdapterSocialMerge:
    def test_merge_story_items_attaches_social_proof_to_article(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        article_item = {
            "kind": "article",
            "source": "TechCrunch",
            "category": "ai_tech",
            "subject": "New coding agent benchmark",
            "url": "https://example.com/coding-agent",
            "published_at": "2026-03-09T10:00:00-07:00",
            "topic_tags": ["capabilities"],
            "clean_text": "A new coding agent benchmark shows large gains.",
            "links_context": [],
            "story_key": "https://example.com/coding-agent/",
        }
        social_item = {
            "kind": "social",
            "source": "Reddit",
            "platform": "reddit",
            "category": "ai_tech",
            "subject": "People are discussing the new coding agent benchmark",
            "url": "https://example.com/coding-agent/",
            "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/",
            "published_at": "2026-03-09T11:00:00-07:00",
            "topic_tags": ["capabilities"],
            "clean_text": "The launch looks strong and developers are comparing benchmarks.",
            "story_key": "https://example.com/coding-agent/",
            "social_proof": [{
                "platform": "reddit",
                "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/",
                "subreddit": "MachineLearning",
                "points": 180,
                "comments": 60,
            }],
        }

        merged = adapter._merge_story_items(
            [article_item, social_item],
            merge_window_hours=48,
            similarity_threshold=0.65,
        )

        assert len(merged) == 1
        assert merged[0]["kind"] == "article"
        assert merged[0]["social_proof"][0]["platform"] == "reddit"
        assert merged[0]["url"] == "https://example.com/coding-agent"

    def test_merge_story_items_prefer_stronger_cross_source_social_item(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        tweet_item = {
            "kind": "social",
            "source": "TwitterX",
            "platform": "x",
            "category": "ai_tech",
            "subject": "New AI coding agent launch sparks discussion",
            "url": "",
            "discussion_url": "https://x.com/i/web/status/123",
            "published_at": "2026-03-09T10:30:00-07:00",
            "topic_tags": ["capabilities"],
            "clean_text": "People are reacting to the new AI coding agent launch.",
            "story_key": "title:a1",
            "score": 61,
            "social_score": 61,
            "social_proof": [{
                "platform": "x",
                "discussion_url": "https://x.com/i/web/status/123",
                "author": "builder",
                "likes": 120,
                "reposts": 20,
                "score": 61,
            }],
        }
        hn_item = {
            "kind": "social",
            "source": "HackerNews",
            "platform": "hn",
            "category": "ai_tech",
            "subject": "New AI coding agent launch wins developers over",
            "url": "https://example.com/agent-launch/",
            "discussion_url": "https://news.ycombinator.com/item?id=555",
            "published_at": "2026-03-09T11:00:00-07:00",
            "topic_tags": ["capabilities"],
            "clean_text": "The launch coverage points to benchmark gains and better repo-sized task performance.",
            "story_key": "https://example.com/agent-launch/",
            "score": 84,
            "social_score": 84,
            "social_proof": [{
                "platform": "hn",
                "discussion_url": "https://news.ycombinator.com/item?id=555",
                "points": 220,
                "comments": 80,
                "score": 84,
            }],
        }

        merged = adapter._merge_story_items(
            [tweet_item, hn_item],
            merge_window_hours=48,
            similarity_threshold=0.65,
        )

        assert len(merged) == 1
        assert merged[0]["subject"] == "New AI coding agent launch wins developers over"
        assert merged[0]["url"] == "https://example.com/agent-launch/"
        assert len(merged[0]["social_proof"]) == 2

    def test_tick_merges_social_item_into_existing_story(self, tmp_path):
        import json
        import yaml

        adapter = _make_adapter(tmp_path)
        adapter._is_quiet_hour = lambda: False
        now = datetime.now(adapter.timezone)

        config = {
            "sources": [
                {
                    "name": "TechCrunch",
                    "delivery": "web",
                    "listing_url": "https://techcrunch.com/category/artificial-intelligence/",
                    "lookback_hours": 24,
                    "max_items": 8,
                    "include_topics": ["capabilities"],
                    "topic_routes": {"capabilities": "ai_tech"},
                },
                {
                    "name": "Reddit",
                    "delivery": "social",
                    "platform": "reddit",
                    "subreddits": ["MachineLearning"],
                    "max_items": 5,
                    "min_score_threshold": 0,
                    "native_discussion_floor": 0,
                    "topic_routes": {"capabilities": "ai_tech"},
                },
            ],
            "settings": {
                "daily_schedule": "00:00",
                "weekly_schedule": "19:00",
                "quiet_hours": "23:00-06:00",
                "fetch_linked_articles": False,
                "max_links_per_newsletter": 5,
                "social_fetch_enabled": True,
                "social_dedupe_threshold": 0.65,
                "social_story_merge_window_hours": 48,
            },
        }
        adapter._config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

        adapter._collect_techcrunch_items = MagicMock(
            return_value=(
                [{
                    "kind": "article",
                    "source": "TechCrunch",
                    "category": "ai_tech",
                    "subject": "New coding agent benchmark",
                    "url": "https://example.com/coding-agent/",
                    "published_at": now.isoformat(),
                    "topic_tags": ["capabilities"],
                    "clean_text": "Benchmark coverage.",
                    "links_context": [],
                    "story_key": "https://example.com/coding-agent/",
                }],
                {"techcrunch:https://example.com/coding-agent/"},
            )
        )
        adapter._collect_social_items = MagicMock(
            return_value=(
                [{
                    "kind": "social",
                    "source": "Reddit",
                    "platform": "reddit",
                    "category": "ai_tech",
                    "subject": "Thread about the new coding agent benchmark",
                    "url": "https://example.com/coding-agent/",
                    "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/",
                    "published_at": now.isoformat(),
                    "topic_tags": ["capabilities"],
                    "clean_text": "Reddit reaction.",
                    "story_key": "https://example.com/coding-agent/",
                    "social_proof": [{
                        "platform": "reddit",
                        "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/",
                        "subreddit": "MachineLearning",
                        "points": 100,
                        "comments": 25,
                    }],
                }],
                {"reddit:xyz"},
            )
        )

        result = adapter.tick()

        assert result == 1
        event = adapter.queue.insert_event.call_args[0][0]
        assert len(event.payload["items"]) == 1
        assert event.payload["items"][0]["social_proof"][0]["platform"] == "reddit"

        saved_state = json.loads(adapter._state_path.read_text(encoding="utf-8"))
        assert "reddit:xyz" in saved_state["processed_entry_ids"]

    def test_tick_skips_failed_social_source_without_failing_digest(self, tmp_path):
        import yaml

        adapter = _make_adapter(tmp_path)
        adapter._is_quiet_hour = lambda: False

        config = {
            "sources": [
                {
                    "name": "Reddit",
                    "delivery": "social",
                    "platform": "reddit",
                    "subreddits": ["MachineLearning"],
                    "max_items": 5,
                    "min_score_threshold": 0,
                    "native_discussion_floor": 0,
                    "topic_routes": {"capabilities": "ai_tech"},
                }
            ],
            "settings": {
                "daily_schedule": "00:00",
                "weekly_schedule": "19:00",
                "quiet_hours": "23:00-06:00",
                "social_fetch_enabled": True,
            },
        }
        adapter._config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

        adapter._collect_social_items = MagicMock(side_effect=RuntimeError("boom"))

        result = adapter.tick()

        assert result == 0
        assert not adapter.queue.insert_event.called


class TestHandlerSocialProof:
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
    def test_handler_renders_social_proof_in_prompt(
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
                "items": [{
                    "kind": "article",
                    "source": "TechCrunch",
                    "category": "ai_tech",
                    "subject": "New coding agent benchmark",
                    "url": "https://example.com/coding-agent/",
                    "published_at": "2026-03-09T10:00:00-07:00",
                    "topic_tags": ["capabilities"],
                    "clean_text": "Benchmark coverage.",
                    "links_context": [],
                    "social_proof": [{
                        "platform": "reddit",
                        "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/",
                        "subreddit": "MachineLearning",
                        "points": 100,
                        "comments": 25,
                        "top_comment": "The benchmark finally includes realistic repo-sized tasks.",
                    }],
                }],
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
        assert "Social Proof:" in prompt
        assert "Discussion URL:" not in prompt or "https://www.reddit.com/r/MachineLearning/comments/xyz/coding_agent/" in prompt
        assert "Top comment:" in prompt


class TestPayloadSanitization:
    def test_internal_classification_does_not_leak_to_payload(self, tmp_path):
        adapter = _make_adapter(tmp_path)
        item = {
            "kind": "social",
            "source": "Reddit",
            "category": "ai_tech",
            "subject": "Benchmark thread",
            "url": "https://example.com/benchmark/",
            "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/benchmark/",
            "published_at": "2026-03-09T10:00:00-07:00",
            "topic_tags": ["capabilities"],
            "clean_text": "Discussion text",
            "social_proof": [{"platform": "reddit", "discussion_url": "https://www.reddit.com/r/MachineLearning/comments/xyz/benchmark/"}],
            "_classification": {"primary": "capabilities"},
        }

        sanitized = adapter._sanitize_item_for_payload(item)

        assert "_classification" not in sanitized
