"""
Configuration & Environment Settings
Copy .env.example to .env and fill in your values.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Anthropic / Claude API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Email Configuration (Gmail recommended)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", "")   # Use App Password for Gmail
    RECIPIENT_EMAIL: str = os.getenv("RECIPIENT_EMAIL", "")

    # Agent Behavior
    TOPICS_PER_RUN: int = int(os.getenv("TOPICS_PER_RUN", 2))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 3))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 15))

    def validate(self):
        missing = []
        for field in ["ANTHROPIC_API_KEY", "SENDER_EMAIL", "SENDER_PASSWORD", "RECIPIENT_EMAIL"]:
            if not getattr(self, field):
                missing.append(field)
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
