# 🔍 Micro Data Observability Bot

An automated, LLM-powered data quality and anomaly detection agent for real-time financial data pipelines[cite: 1, 2]. Built with **Python**, **DuckDB**, **Groq (Llama 3.3)**, and **Telegram Webhooks**[cite: 1, 2].

---

## 📐 Architecture & Data Flow

```text
[Binance Public API]
       │
       ▼ (Every 30 mins via GitHub Actions)
[Data Ingestion & DuckDB Store]
       │
       ▼
[Data Observability Engine]
  ├── 1. Row Count Drop (Z-Score Anomaly)
  ├── 2. Null Rate Spike Check (>10%)
  └── 3. Schema Drift Validation
       │
       ▼ (If Anomaly Detected)
[LLM Root Cause Agent (Groq / Llama 3.3)]
       │
       ▼
[Telegram Alert Webhook]
```[cite: 1]

---

## ✨ Key Features

- **Live Data Ingestion:** Fetches real-time crypto ticker data from Binance Public API[cite: 1, 2].
- **Statistical Anomaly Detection:** Calculates Z-Scores ($Z = \frac{x - \mu}{\sigma}$) to detect sudden row count drops and tracks column-level null rates[cite: 1, 2].
- **AI-Powered Root Cause Analysis:** Utilizes Groq Llama models to analyze detected anomalies, provide technical descriptions, and generate remedial SQL queries[cite: 1, 2].
- **Real-Time Webhook Alerting:** Sends immediate incident reports to Telegram channels upon quality failures[cite: 1, 2].
- **Automated CI/CD:** Scheduled via GitHub Actions to run every 30 minutes[cite: 1, 2].

---

## 🛠️ Tech Stack

- **Language:** Python 3.11[cite: 2]
- **Database:** DuckDB (In-Memory Data Store)[cite: 1, 2]
- **LLM Engine:** Groq API (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`)[cite: 1, 2]
- **Alerting:** Telegram Bot Webhook[cite: 1, 2]
- **Orchestration:** GitHub Actions Workflow[cite: 1, 2]

---

## 📁 Project Structure

```text
micro-data-observability/
│
├── .github/
│   └── workflows/
│       └── observability.yml   # GitHub Actions scheduler
├── .env                        # Environment variables (API Keys)
├── .gitignore
├── requirements.txt            # Python dependencies
├── config.py                   # Environment configuration loader
├── ingestion.py                # Binance API fetcher & DuckDB setup
├── observability.py            # Z-Score, Null Check, and Schema Drift Engine
├── llm_agent.py                # Groq LLM integration for root cause analysis
├── notifier.py                 # Telegram Webhook alert delivery
└── main.py                     # Pipeline entry point
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/micro-data-observability.git
cd micro-data-observability
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv

# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

### 4. Run Locally
```bash
python main.py
```

---

## 🤖 GitHub Actions Setup (CI/CD)

To run this pipeline automatically every 30 minutes in the cloud[cite: 1, 2]:

1. Push your code to a GitHub repository[cite: 1].
2. Go to **Repository Settings** ➔ **Secrets and variables** ➔ **Actions**[cite: 1].
3. Add the following repository secrets[cite: 1]:
   - `GROQ_API_KEY`[cite: 1]
   - `TELEGRAM_BOT_TOKEN`[cite: 1]
   - `TELEGRAM_CHAT_ID`[cite: 1]