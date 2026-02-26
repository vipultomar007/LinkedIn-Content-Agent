"""
Humanizer Agent
Uses Groq (free) to transform raw scraped content into
a genuine, engaging LinkedIn post that sounds like YOU — not AI.
"""

import logging
from typing import Dict
import httpx

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior software engineer with 8+ years of experience.
You write LinkedIn posts that are:
- Personal and conversational (use "I", "we", "you")
- Story-driven — start with a hook or relatable pain point
- Practically useful — give 3-5 concrete takeaways
- NOT corporate-sounding, NOT buzzword-heavy
- Structured with line breaks for readability (LinkedIn style)
- End with a question to spark engagement
- Include relevant emojis sparingly (2-4 max)
- 150-250 words — punchy, not exhausting

You NEVER say "In this post", "I wanted to share", "As a professional", or "I hope this helps".
You write like a real person talking to a peer, not a content marketer.
"""


class HumanizerAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def humanize(self, topic: Dict, raw_content: str) -> Dict:
        hashtags = " ".join(topic.get("hashtags", []))

        user_prompt = f"""
Topic: {topic['title']}
Category: {topic['category']}

Here is reference content scraped from the web:
---
{raw_content[:3000]}
---

Write a LinkedIn post about this topic.
- Extract the most interesting/useful insights from the content above.
- Don't copy sentences — rewrite everything in your own voice.
- End the post with these hashtags on a new line: {hashtags}
"""

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        "max_tokens": 1000,
                        "temperature": 0.8,
                    },
                )
                response.raise_for_status()
                post_text = response.json()["choices"][0]["message"]["content"].strip()
                return {
                    "topic": topic["title"],
                    "category": topic["category"],
                    "post": post_text,
                    "hashtags": topic.get("hashtags", []),
                }
        except Exception as e:
            logger.error(f"Humanizer failed for {topic['title']}: {e}")
            return {
                "topic": topic["title"],
                "category": topic["category"],
                "post": f"[Failed to generate post: {e}]",
                "hashtags": [],
            }
