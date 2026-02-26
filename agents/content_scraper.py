"""
Content Scraper Agent
Fetches and extracts clean text from reputable tech websites.
"""

import asyncio
import logging
import random
from typing import Optional, Dict
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
]

# Tags that contain the main article content
CONTENT_SELECTORS = [
    "article",
    "main",
    ".post-content",
    ".entry-content",
    ".article-content",
    ".content",
    "#content",
    ".blog-post",
]


class ContentScraperAgent:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    async def scrape(self, topic: Dict) -> Optional[str]:
        """Try each URL for a topic until one succeeds."""
        for url in topic["urls"]:
            content = await self._fetch_url(url)
            if content and len(content) > 300:
                return content
        logger.warning(f"⚠️  Could not scrape any URL for topic: {topic['title']}")
        return None

    async def _fetch_url(self, url: str) -> Optional[str]:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                return self._extract_text(resp.text, url)
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

    def _extract_text(self, html: str, url: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Try to find the main content area
        content_tag = None
        for selector in CONTENT_SELECTORS:
            content_tag = soup.select_one(selector)
            if content_tag:
                break

        target = content_tag if content_tag else soup.body or soup

        # Extract paragraphs
        paragraphs = target.find_all(["p", "h1", "h2", "h3", "li"])
        lines = []
        for p in paragraphs:
            text = p.get_text(separator=" ", strip=True)
            if len(text) > 40:  # filter out short/empty lines
                lines.append(text)

        raw = "\n\n".join(lines)
        # Limit to ~4000 chars to stay within token budget
        return raw[:4000] if raw else ""
