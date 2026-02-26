"""
LinkedIn Content Agent - Main Orchestrator
Picks 2-3 random tech topics, scrapes content, humanizes it, and emails you.
"""

import asyncio
import logging
from agents.topic_selector import TopicSelectorAgent
from agents.content_scraper import ContentScraperAgent
from agents.humanizer import HumanizerAgent
from agents.email_sender import EmailSenderAgent
from config.settings import Settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


async def run_pipeline():
    settings = Settings()

    logger.info("🚀 Starting LinkedIn Content Agent Pipeline")

    # Step 1: Select 2-3 random topics
    topic_agent = TopicSelectorAgent()
    topics = topic_agent.select_topics(count=2)  # change to 3 if you want 3
    logger.info(f"📌 Selected topics: {[t['title'] for t in topics]}")

    # Step 2: Scrape content for each topic
    scraper = ContentScraperAgent()
    raw_contents = []
    for topic in topics:
        logger.info(f"🔍 Scraping content for: {topic['title']}")
        content = await scraper.scrape(topic)
        if content:
            raw_contents.append({"topic": topic, "content": content})

    if not raw_contents:
        logger.error("❌ No content scraped. Exiting.")
        return

    # Step 3: Humanize content into LinkedIn posts
    humanizer = HumanizerAgent(api_key=settings.GROQ_API_KEY)
    posts = []
    for item in raw_contents:
        logger.info(f"✍️  Humanizing: {item['topic']['title']}")
        post = await humanizer.humanize(item["topic"], item["content"])
        posts.append(post)

    # Step 4: Send email with all posts
    emailer = EmailSenderAgent(settings)
    logger.info(f"📧 Sending {len(posts)} posts to {settings.RECIPIENT_EMAIL}")
    await emailer.send(posts)

    logger.info("✅ Pipeline completed successfully!")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
