"""Tests for timeout scaling curves across the ingest pipeline."""

from __future__ import annotations

import pytest

from ingest.section_slicer import timeout_for_text


class TestTimeoutForText:
    """Verify sub-linear power-law scaling in timeout_for_text()."""

    def test_small_text_gets_lower_timeout(self):
        """5K chars should get a tighter timeout than the old 180s base."""
        assert timeout_for_text(5_000) < 160

    def test_medium_text_comparable(self):
        """50K chars should get a comparable timeout (~270s)."""
        t = timeout_for_text(50_000)
        assert 250 <= t <= 300

    def test_large_text_comparable(self):
        """200K chars should get a comparable timeout (~475s)."""
        t = timeout_for_text(200_000)
        assert 450 <= t <= 500

    def test_ceiling_respected(self):
        """Very large text should never exceed the ceiling."""
        assert timeout_for_text(1_000_000) == 720

    def test_ceiling_not_hit_at_300k(self):
        """300K should still be below ceiling."""
        assert timeout_for_text(300_000) < 720

    def test_monotonically_increasing(self):
        """Timeout should increase (or stay flat at ceiling) as text grows."""
        sizes = [1_000, 5_000, 10_000, 50_000, 100_000, 200_000, 500_000]
        timeouts = [timeout_for_text(s) for s in sizes]
        for i in range(1, len(timeouts)):
            assert timeouts[i] >= timeouts[i - 1]

    def test_sub_linear_growth(self):
        """Doubling text length should less-than-double the timeout increase."""
        t_50k = timeout_for_text(50_000)
        t_100k = timeout_for_text(100_000)
        t_200k = timeout_for_text(200_000)
        delta_1 = t_100k - t_50k
        delta_2 = t_200k - t_100k
        assert delta_2 < delta_1 * 2

    def test_zero_length_returns_base(self):
        """Zero-length text should return the base timeout."""
        assert timeout_for_text(0) == 120

    def test_negative_length_returns_base(self):
        """Negative text_len must not crash (guards against complex numbers)."""
        assert timeout_for_text(-1) == 120
        assert timeout_for_text(-100_000) == 120

    def test_custom_parameters(self):
        """Custom base/scale/ceiling should be respected."""
        t = timeout_for_text(10_000, base=60, scale=30, ceiling=500)
        assert t == 60 + int(30 * 1.0 ** 0.65)

    @pytest.mark.parametrize(
        "text_len,expected_approx",
        [
            (5_000, 152),
            (10_000, 170),
            (50_000, 262),
            (100_000, 344),
            (200_000, 474),
            (300_000, 576),
        ],
    )
    def test_expected_values(self, text_len, expected_approx):
        """Timeout values should match the planned curve (within ±5s)."""
        assert abs(timeout_for_text(text_len) - expected_approx) <= 5


class TestSummarizerTimeout:
    """Verify sub-linear scaling for the deep summarizer timeout formula."""

    @staticmethod
    def _summarizer_timeout(text_len: int) -> int:
        """Replicate the formula from deep_summarizer.py for testing."""
        return min(300 + int(50 * max(0, (text_len - 20_000) / 10_000) ** 0.65), 720)

    def test_small_text_lower_base(self):
        """Text ≤20K should get exactly 300s (not old 480s)."""
        assert self._summarizer_timeout(10_000) == 300
        assert self._summarizer_timeout(20_000) == 300

    def test_medium_text(self):
        """50K should be around 408s."""
        t = self._summarizer_timeout(50_000)
        assert 390 <= t <= 420

    def test_large_text_more_headroom(self):
        """200K should be ~627s (old was capped at 600s)."""
        t = self._summarizer_timeout(200_000)
        assert 610 <= t <= 650

    def test_zero_and_negative_return_base(self):
        """Zero or negative text_len should return the base 300s."""
        assert self._summarizer_timeout(0) == 300
        assert self._summarizer_timeout(-1) == 300

    def test_ceiling_respected(self):
        """Very large text should cap at 720s."""
        assert self._summarizer_timeout(1_000_000) == 720

    def test_monotonically_increasing(self):
        sizes = [5_000, 20_000, 50_000, 100_000, 200_000, 500_000]
        timeouts = [self._summarizer_timeout(s) for s in sizes]
        for i in range(1, len(timeouts)):
            assert timeouts[i] >= timeouts[i - 1]
