# 🚀 LinkedIn Content Agent

> An AI-powered agent that auto-picks 2–3 trending tech topics, scrapes insights from reputable sources, humanizes them into LinkedIn posts, and emails them to you — fully automated via GitHub Actions.

---

## 📸 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌────────────────┐
│  Topic Selector │────▶│ Content Scraper  │────▶│  Humanizer (AI)   │────▶│  Email Sender  │
│                 │     │                  │     │                   │     │                │
│ Randomly picks  │     │ Fetches content  │     │ Claude rewrites   │     │ Sends you      │
│ 2-3 topics from │     │ from Baeldung,   │     │ raw content into  │     │ a beautiful    │
│ AI, Java, LLD,  │     │ Martin Fowler,   │     │ your LinkedIn     │     │ HTML email     │
│ HLD, Tech       │     │ HuggingFace, etc │     │ voice             │     │ ready to post  │
└─────────────────┘     └──────────────────┘     └───────────────────┘     └────────────────┘
```

---

## 🗂️ Project Structure

```
linkedin-content-agent/
├── main.py                        # Pipeline orchestrator
├── requirements.txt
├── .env.example                   # Copy this to .env
├── .gitignore
├── agents/
│   ├── topic_selector.py          # Randomly picks topics with curated sources
│   ├── content_scraper.py         # Scrapes and extracts clean text
│   ├── humanizer.py               # Claude API: turns content → LinkedIn post
│   └── email_sender.py            # Sends beautiful HTML email
├── config/
│   └── settings.py                # All env var config
└── .github/
    └── workflows/
        └── content-agent.yml      # Runs every weekday at 7:30 AM IST
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/linkedin-content-agent.git
cd linkedin-content-agent
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

| Variable | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `SENDER_EMAIL` | Your Gmail address |
| `SENDER_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) (not your real password!) |
| `RECIPIENT_EMAIL` | Where to receive posts (can be same as sender) |

### 3. Run Locally

```bash
python main.py
```

Check your inbox — you should receive 2 LinkedIn posts within ~30 seconds.

---

## 🤖 Automate with GitHub Actions

No server needed. GitHub runs this for free every weekday morning.

### Setup Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:
- `ANTHROPIC_API_KEY`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `RECIPIENT_EMAIL`

### Schedule

The workflow runs every **weekday at 7:30 AM IST** (configurable in `.github/workflows/content-agent.yml`).

You can also trigger it manually:
- Go to **Actions tab** → **LinkedIn Content Agent** → **Run workflow**

---

## 🎯 Topics Covered

| Category | Topics |
|---|---|
| **AI** | LLMs, AI Agents, Prompt Engineering |
| **Java** | Java 21+ Features, Spring Boot, Virtual Threads |
| **LLD** | SOLID Principles, Design Patterns, Clean Code |
| **HLD** | System Design (URL Shortener, etc.), Microservices, CAP Theorem |
| **Tech** | GitHub Trending, REST vs GraphQL vs gRPC |

### Adding Your Own Topics

Edit `agents/topic_selector.py` and add a new entry to `TOPIC_POOL`:

```python
{
    "category": "DSA",
    "title": "Top 5 Graph Algorithms for Interviews",
    "urls": [
        "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/",
    ],
    "hashtags": ["#DSA", "#Algorithms", "#CodingInterview"],
},
```

---

## 🛠️ Customization

| What to change | Where |
|---|---|
| Number of posts per run | `TOPICS_PER_RUN` in `.env` |
| Writing tone/style | `SYSTEM_PROMPT` in `agents/humanizer.py` |
| Schedule (cron) | `.github/workflows/content-agent.yml` |
| Email template | `agents/email_sender.py` |

---

## 📧 Gmail Setup (2 minutes)

1. Enable **2-Step Verification** on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Select **Mail** → **Windows Computer** → Generate
4. Use the 16-character password as `SENDER_PASSWORD`

---

## 📝 License

MIT — use it, modify it, make it your own.

---

> Built to help developers stay visible without spending hours writing content. Post consistently, grow your brand. 🚀
