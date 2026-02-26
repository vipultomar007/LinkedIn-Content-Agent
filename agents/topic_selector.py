"""
Topic Selector Agent
Randomly picks 2-3 topics from a curated list of tech categories
with reputable source URLs to scrape from.
"""

import random
from typing import List, Dict

TOPIC_POOL = [
    # ── AI / ML ──────────────────────────────────────────────────
    {
        "category": "AI",
        "title": "Latest in Large Language Models",
        "urls": [
            "https://huggingface.co/blog",
            "https://openai.com/blog",
            "https://www.deeplearning.ai/the-batch/",
        ],
        "hashtags": ["#AI", "#LLM", "#MachineLearning", "#GenAI"],
    },
    {
        "category": "AI",
        "title": "AI Agents & Agentic Workflows",
        "urls": [
            "https://www.langchain.com/blog",
            "https://blog.langchain.dev",
        ],
        "hashtags": ["#AIAgents", "#Agentic", "#AI", "#Automation"],
    },
    {
        "category": "AI",
        "title": "Prompt Engineering Best Practices",
        "urls": [
            "https://www.promptingguide.ai/",
            "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
        ],
        "hashtags": ["#PromptEngineering", "#AI", "#ChatGPT", "#Claude"],
    },

    # ── Java ─────────────────────────────────────────────────────
    {
        "category": "Java",
        "title": "Java 21+ Features Every Developer Should Know",
        "urls": [
            "https://www.baeldung.com/java-21-new-features",
            "https://openjdk.org/projects/jdk/21/",
        ],
        "hashtags": ["#Java", "#Java21", "#Backend", "#Programming"],
    },
    {
        "category": "Java",
        "title": "Spring Boot Best Practices",
        "urls": [
            "https://www.baeldung.com/spring-boot-best-practices",
            "https://spring.io/blog",
        ],
        "hashtags": ["#SpringBoot", "#Java", "#Microservices", "#Backend"],
    },
    {
        "category": "Java",
        "title": "Java Concurrency & Virtual Threads",
        "urls": [
            "https://www.baeldung.com/java-virtual-thread-vs-thread",
            "https://openjdk.org/jeps/444",
        ],
        "hashtags": ["#Java", "#Concurrency", "#VirtualThreads", "#Performance"],
    },

    # ── Low-Level Design (LLD) ────────────────────────────────────
    {
        "category": "LLD",
        "title": "SOLID Principles with Real Examples",
        "urls": [
            "https://www.baeldung.com/solid-principles",
            "https://refactoring.guru/refactoring/principles",
        ],
        "hashtags": ["#LLD", "#SOLID", "#DesignPatterns", "#SoftwareEngineering"],
    },
    {
        "category": "LLD",
        "title": "Design Patterns You Actually Use",
        "urls": [
            "https://refactoring.guru/design-patterns",
            "https://www.baeldung.com/design-patterns-series",
        ],
        "hashtags": ["#DesignPatterns", "#LLD", "#CleanCode", "#SoftwareDevelopment"],
    },
    {
        "category": "LLD",
        "title": "Clean Code & Code Review Tips",
        "urls": [
            "https://www.baeldung.com/cs/clean-code",
            "https://refactoring.guru/refactoring",
        ],
        "hashtags": ["#CleanCode", "#CodeReview", "#LLD", "#BestPractices"],
    },

    # ── High-Level Design (HLD) ───────────────────────────────────
    {
        "category": "HLD",
        "title": "Designing a URL Shortener at Scale",
        "urls": [
            "https://www.designgurus.io/blog/url-shortener-system-design",
            "https://systemdesign.one/url-shortening-system-design/",
        ],
        "hashtags": ["#SystemDesign", "#HLD", "#Scalability", "#Backend"],
    },
    {
        "category": "HLD",
        "title": "Microservices vs Monolith: When to Choose What",
        "urls": [
            "https://martinfowler.com/articles/microservices.html",
            "https://www.baeldung.com/microservices-vs-monolith",
        ],
        "hashtags": ["#Microservices", "#SystemDesign", "#HLD", "#Architecture"],
    },
    {
        "category": "HLD",
        "title": "CAP Theorem & Distributed Systems",
        "urls": [
            "https://www.baeldung.com/cs/cap-theorem",
            "https://systemdesign.one/cap-theorem/",
        ],
        "hashtags": ["#DistributedSystems", "#CAPTheorem", "#HLD", "#SystemDesign"],
    },

    # ── General Tech ─────────────────────────────────────────────
    {
        "category": "Tech",
        "title": "Top GitHub Repos Every Developer Should Star",
        "urls": [
            "https://github.com/trending",
        ],
        "hashtags": ["#GitHub", "#OpenSource", "#Developer", "#Tech"],
    },
    {
        "category": "Tech",
        "title": "REST vs GraphQL vs gRPC",
        "urls": [
            "https://www.baeldung.com/rest-vs-graphql-vs-grpc",
        ],
        "hashtags": ["#REST", "#GraphQL", "#gRPC", "#API", "#Backend"],
    },
]


class TopicSelectorAgent:
    def __init__(self):
        self.topics = TOPIC_POOL

    def select_topics(self, count: int = 2) -> List[Dict]:
        """Randomly select `count` unique topics, preferring category diversity."""
        count = max(2, min(count, 3))

        # Try to pick from different categories
        categories = list({t["category"] for t in self.topics})
        selected_categories = random.sample(categories, min(count, len(categories)))

        selected = []
        for cat in selected_categories:
            cat_topics = [t for t in self.topics if t["category"] == cat]
            selected.append(random.choice(cat_topics))

        # If we need more, fill randomly
        remaining = [t for t in self.topics if t not in selected]
        while len(selected) < count and remaining:
            pick = random.choice(remaining)
            selected.append(pick)
            remaining.remove(pick)

        return selected
