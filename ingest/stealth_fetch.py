"""Stealth browser fetching for anti-bot protected sites.

Uses patchright (patched Playwright fork) with stealth bypass scripts
to avoid headless browser detection. Handles Cloudflare Turnstile/Interstitial
challenges automatically.

Extracted from Scrapling's stealth engine — only the essentials needed
for HTML fetching, without Scrapling's class hierarchy or Response types.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from pathlib import Path
from random import randint

logger = logging.getLogger(__name__)

_BYPASSES_DIR = Path(__file__).parent / "stealth_bypasses"

_CF_PATTERN = re.compile(r"challenges\.cloudflare\.com/cdn-cgi/challenge-platform/.*")

_STEALTH_SCRIPT_FILES = (
    "webdriver_fully.js",
    "window_chrome.js",
    "navigator_plugins.js",
    "notification_permission.js",
    "screen_props.js",
    "playwright_fingerprint.js",
)


@lru_cache(1)
def _compiled_stealth_scripts() -> tuple[str, ...]:
    """Pre-read stealth bypass scripts from disk."""
    scripts = []
    for name in _STEALTH_SCRIPT_FILES:
        path = _BYPASSES_DIR / name
        scripts.append(path.read_text(encoding="utf-8"))
    return tuple(scripts)


def _detect_cloudflare(page_content: str) -> str | None:
    """Detect Cloudflare challenge type from page HTML."""
    for ctype in ("non-interactive", "managed", "interactive"):
        if f"cType: '{ctype}'" in page_content:
            return ctype

    # Check for embedded turnstile via script tag
    if "challenges.cloudflare.com/turnstile/v" in page_content:
        return "embedded"

    return None


def _generate_google_referer(url: str) -> str:
    """Generate a convincing Google search referer for the URL's domain."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.hostname or ""
        # Strip www. and TLD suffix for search query
        parts = domain.replace("www.", "").split(".")
        name = parts[0] if parts else domain
        return f"https://www.google.com/search?q={name}"
    except Exception:
        return "https://www.google.com/"


def _solve_cloudflare(page, challenge_type: str) -> None:
    """Solve a Cloudflare challenge on the given page."""
    if challenge_type == "non-interactive":
        # Wait for the interstitial to resolve itself
        for _ in range(60):  # 60s max
            content = page.content()
            if "<title>Just a moment...</title>" not in content:
                break
            logger.info("Waiting for Cloudflare non-interactive challenge...")
            page.wait_for_timeout(1000)
            page.wait_for_load_state()
        logger.info("Cloudflare non-interactive challenge resolved")
        return

    # Interactive / managed / embedded — need to click the captcha
    box_selector = "#cf_turnstile div, #cf-turnstile div, .turnstile>div>div"
    if challenge_type != "embedded":
        box_selector = ".main-content p+div>div>div"
        # Wait for verify spinner to disappear
        for _ in range(30):
            if "Verifying you are human." not in page.content():
                break
            page.wait_for_timeout(500)

    outer_box = None
    iframe = page.frame(url=_CF_PATTERN)

    if iframe is not None:
        page.wait_for_load_state("domcontentloaded")
        if challenge_type != "embedded":
            for _ in range(20):
                if iframe.frame_element().is_visible():
                    break
                page.wait_for_timeout(500)
        outer_box = iframe.frame_element().bounding_box()

    if not iframe or not outer_box:
        if "<title>Just a moment...</title>" not in page.content():
            logger.info("Cloudflare challenge already resolved")
            return
        try:
            outer_box = page.locator(box_selector).last.bounding_box()
        except Exception:
            logger.warning("Could not find Cloudflare captcha box")
            return

    if not outer_box:
        logger.warning("Could not determine captcha coordinates")
        return

    # Click the captcha checkbox
    captcha_x = outer_box["x"] + randint(26, 28)
    captcha_y = outer_box["y"] + randint(25, 27)
    page.mouse.click(captcha_x, captcha_y, delay=randint(100, 200), button="left")
    page.wait_for_load_state("networkidle")

    if iframe is not None:
        # Wait for iframe removal (up to 30s)
        for _ in range(300):
            if iframe not in page.frames:
                break
            page.wait_for_timeout(100)

    if challenge_type != "embedded":
        try:
            page.locator(box_selector).last.wait_for(state="detached", timeout=10000)
        except Exception:
            pass

    logger.info("Cloudflare challenge solved")


def fetch_html_stealth(url: str, timeout_ms: int = 60000) -> str:
    """Fetch HTML from a URL using a stealth headless browser.

    Launches patchright Chromium with anti-detection scripts, navigates
    to the URL with a Google search referer, and handles Cloudflare
    challenges if present.

    Args:
        url: The URL to fetch.
        timeout_ms: Navigation timeout in milliseconds (default 60s).

    Returns:
        The page HTML content as a string.

    Raises:
        RuntimeError: If the browser fails to fetch the page.
    """
    from patchright.sync_api import sync_playwright

    referer = _generate_google_referer(url)
    stealth_scripts = _compiled_stealth_scripts()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
        )

        # Inject stealth bypass scripts
        for script in stealth_scripts:
            context.add_init_script(script=script)

        page = context.new_page()

        try:
            page.goto(url, referer=referer, timeout=timeout_ms)
            page.wait_for_load_state("domcontentloaded")

            # Check for Cloudflare challenge
            content = page.content()
            challenge_type = _detect_cloudflare(content)
            if challenge_type:
                logger.info("Cloudflare %s challenge detected for %s", challenge_type, url)
                _solve_cloudflare(page, challenge_type)
                # Re-wait after solving
                page.wait_for_load_state("domcontentloaded")

            html = page.content()
            return html

        finally:
            context.close()
            browser.close()
