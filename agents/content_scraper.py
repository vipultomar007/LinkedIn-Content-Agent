"""
Content Scraper Agent - RSS Feed Based
Uses RSS feeds instead of scraping HTML — no 403 blocks.
"""

import logging
import random
import re
from typing import Optional, Dict
import httpx
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

RSS_SOURCES = {
    "AI": [
        "https://huggingface.co/blog/feed.xml",
        "https://www.deeplearning.ai/feed/",
        "https://blogs.microsoft.com/ai/feed/",
    ],
    "Java": [
        "https://feeds.feedburner.com/baeldung",
        "https://spring.io/blog.atom",
        "https://inside.java/feed.xml",
    ],
    "LLD": [
        "https://feeds.feedburner.com/baeldung",
    ],
    "HLD": [
        "https://feeds.feedburner.com/baeldung",
        "https://martinfowler.com/feed.atom",
    ],
    "Tech": [
        "https://dev.to/feed",
        "https://feeds.feedburner.com/baeldung",
        "https://thenewstack.io/feed/",
    ],
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
]


class ContentScraperAgent:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    async def scrape(self, topic: Dict) -> Optional[str]:
        category = topic.get("category", "Tech")
        feeds = RSS_SOURCES.get(category, RSS_SOURCES["Tech"])
        random.shuffle(feeds)

        for feed_url in feeds:
            content = await self._fetch_rss(feed_url, topic["title"])
            if content and len(content) > 200:
                logger.info("Got content from RSS: %s", feed_url)
                return content

        logger.warning("Could not get content for: %s", topic["title"])
        return self._fallback_content(topic)

    async def _fetch_rss(self, url: str, topic_title: str) -> Optional[str]:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                return self._parse_rss(resp.text)
        except Exception as e:
            logger.warning("RSS fetch failed %s: %s", url, e)
            return None

    def _parse_rss(self, xml_text: str) -> str:
        try:
            root = ET.fromstring(xml_text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = []

            # RSS 2.0
            for item in root.findall(".//item")[:5]:
                title = item.findtext("title", "").strip()
                desc = item.findtext("description", "").strip()
                desc = re.sub(r"<[^>]+>", " ", desc)
                desc = re.sub(r"\s+", " ", desc).strip()
                if title and desc:
                    items.append("Title: " + title + "\n" + desc[:500])

            # Atom
            for entry in root.findall(".//atom:entry", ns)[:5]:
                title = entry.findtext("atom:title", namespaces=ns, default="").strip()
                summary = entry.findtext("atom:summary", namespaces=ns, default="").strip()
                content_el = entry.find("atom:content", ns)
                content_text = content_el.text if content_el is not None else ""
                if content_text:
                    content_text = re.sub(r"<[^>]+>", " ", content_text)
                    content_text = re.sub(r"\s+", " ", content_text).strip()[:500]
                text = summary or content_text
                if title and text:
                    items.append("Title: " + title + "\n" + text)

            if not items:
                return ""

            combined = "\n\n---\n\n".join(items[:3])
            return combined[:4000]
        except Exception as e:
            logger.warning("RSS parse error: %s", e)
            return ""

    def _fallback_content(self, topic: Dict) -> str:
        lines = [
            "Topic: " + topic["title"],
            "Category: " + topic["category"],
            "",
            "Key concepts to cover:",
            "- Core definition and why it matters in " + topic["category"],
            "- Common mistakes developers make",
            "- 3-5 practical tips or best practices",
            "- Real-world use cases",
            "- What beginners often overlook",
        ]
        return "\n".join(lines)
