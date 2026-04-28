# OpenClaw Playground - Automation

A modular job-scraping playground that automates data collection from multiple job portals (Indeed, Naukri, RemoteOK, Wellfound, Internshala, Cutshort) with memory persistence and Telegram notifications.

## 🎯 Project Vision

A lightweight, extensible framework for aggregating job postings across diverse platforms while maintaining a simple persistence layer. Designed for quick deployment and easy integration with notification channels (Telegram).

## 🏗️ Architecture

```
┌───────────────────┐
│  Main Entry Point │
│   runner.py       │
└───────┬───────────┘
        ▼
┌───────────────────┐
│   Scraper Module  │
│   (scraper.py)    │
│   ├─ Indeed       │
│   ├─ Naukri       │
│   ├─ RemoteOK     │
│   ├─ Wellfound    │
│   ├─ Internshala  │
│   └─ Cutshort     │
└───────┬───────────┘
        ▼
┌───────────────────┐
│  Memory Handler   │
│   (memory.py)     │
│   Terminal JSON   │
└───────┬───────────┘
        ▼
┌───────────────────┐
│  Telegram Sender  │
│   (telegram_sender.py) │
└───────────────────┘
```

## 🛠️ Technical Stack

- **Language**: Python 3.9+
- **Web Framework**: Playwright (browser automation)
- **Data Format**: JSON memory persistence
- **Messaging**: Telegram Bot API
- **Tools**: Sync API for stability

## 🔧 Deployment

### Prerequisites
- Python 3.9+
- Playwright browsers (automatically installed on first run)
- Telegram bot token and chat ID (for notifications)

### Setup
```bash
# Install dependencies
pip install playwright

# Install browser contexts (runs once)
python -m playwright install

# Optional: Configure Telegram credentials
# Edit memory.json or create .env.local with TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
```

### Running the Scraper
```bash
# Basic usage
python scraper.py --role "software engineer" --location "Bangalore"

# Save output for later use
python runner.py

# To resume from saved memory
python saver.py --resume
```

## 🧠 Memory System

The project uses `memory.json` to persist scraped data across sessions. Memory management includes:

- Automatic deduplication
- JSON-formatted storage for easy querying
- Memory validation on load/save operations

## 📦 Project Structure

| File/Dir            | Purpose                                   |
|---------------------|-------------------------------------------|
| `scraper.py`        | Core web scraping logic for 6 job platforms |
| `agent.py`          | CLI interface and command-line parsing      |
| `runner.py`         | Orchestrates scraping pipeline            |
| `saver.py`          | Memory persistence and storage management |
| `telegram_sender.py`| Sends scraped results via Telegram        |
| `tool.py`           | Utility functions and helpers             |
| `memory.py`         | Memory schema and validation utilities    |
| `logs/`             | Runtime logs and debugging output         |
| `output/`           | Persistent scraped data exports           |

## 📜 Development History

1. **Initial Prototype (v0.1)**
   - Core Playwright setup with Indeed scraper
   - Basic JSON output storage

2. **Portal Expansion (v0.2)**
   - Added Naukri, RemoteOK, Wellfound scrapers
   - Implemented parallel processing architecture
   - Memory persistence layer introduced

3. **Telegram Integration (v0.3)**
   - Added `telegram_sender.py` for notifications
   - Implemented async notification system

4. **Memory Optimization (v0.4)**
   - Added deduplication and validation
   - Enhanced memory schema (`memory.py`)
   - Structured terminal vs file storage modes

5. **Modularization (Current)**
   - Clean separation of concerns
   - Unified job posting schema
   - Extensible portal architecture
