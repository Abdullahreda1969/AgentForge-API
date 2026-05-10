# 🤖 AgentForge AI Engine

## Generate complete applications from text descriptions using AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Deployed on](https://img.shields.io/badge/Deployed%20on-Diploi-3B82F6)](https://diploi.com)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-Marketplace-0066FF?logo=rapidapi)](https://rapidapi.com/abdullahreda1969/api/agentforge-ai-engine)

---

## 🚀 What is AgentForge?

AgentForge is an **API-as-a-Service** that generates complete, ready-to-run Streamlit applications from a simple text description. Stop writing boilerplate code. Just describe what you want, and AgentForge builds it for you.

**Try it live:** [AgentForge on RapidAPI](https://rapidapi.com/abdullahreda1969/api/agentforge-ai-engine)

---

## ✨ Features

| Feature                 | Description                                         |
| ----------------------- | --------------------------------------------------- |
| **🚀 Smart Templates**  | Fastest option, pre-built templates for common apps |
| **🦙 Ollama AI**        | Local AI generation (offline, free, private)        |
| **☁️ Gemini AI**        | Cloud-based generation (powerful, fast)             |
| **📦 Instant Download** | Get a ZIP file with full project                    |
| **🔧 SQLite Database**  | Persistent storage for your apps                    |
| **📊 Analytics Ready**  | Track usage with built-in analytics                 |

---

## 🎯 Supported Application Types

| Type                | Functions                                             | Example                           |
| ------------------- | ----------------------------------------------------- | --------------------------------- |
| **Task Manager**    | `get_tasks()`, `add_task()`, `delete_task()`          | "Create a todo list app"          |
| **Contact Book**    | `get_contacts()`, `add_contact()`, `delete_contact()` | "Contact book with phone numbers" |
| **Inventory**       | `get_products()`, `add_product()`, `delete_product()` | "Product inventory system"        |
| **Library Manager** | `get_books()`, `add_book()`, `delete_book()`          | "Library management system"       |
| **Calculator**      | Dynamic generation                                    | "Simple calculator app"           |

---

## 🏗️ How It Works

User sends description
↓
AgentForge API (FastAPI)
↓
Choose Engine (Smart / Ollama / Gemini)
↓
Generate files (main.py, helpers.py, database.py, config.py)
↓
Return ZIP download link
↓
User runs: streamlit run main.py

text

---

## 🔧 Tech Stack

| Tool           | Purpose                     |
| -------------- | --------------------------- |
| **FastAPI**    | REST API framework          |
| **SQLite**     | Lightweight database        |
| **Streamlit**  | Generated UI framework      |
| **Ollama**     | Local AI models (gemma3)    |
| **Gemini API** | Cloud AI (gemini-2.5-flash) |
| **Diploi**     | Cloud hosting               |
| **RapidAPI**   | API marketplace & payments  |

---

## 📊 Three Engines Comparison

| Engine              | Speed            | Quality    | Internet | Cost      | Best For          |
| ------------------- | ---------------- | ---------- | -------- | --------- | ----------------- |
| **Smart Templates** | ⚡ Very Fast     | ⭐⭐⭐⭐   | ❌ No    | Free      | Production        |
| **Ollama AI**       | 🐢 Slow (30-90s) | ⭐⭐⭐⭐   | ❌ No    | Free      | Offline / Private |
| **Gemini AI**       | ⚡ Fast (5-15s)  | ⭐⭐⭐⭐⭐ | ✅ Yes   | Free tier | Production        |

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Ollama (for local AI)

### Installation

```bash
# Clone repository
git clone <https://github.com/abdullahreda1969/AgentForge-API.git>
cd AgentForge-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python run_api.py

# Run the UI (optional)
streamlit run app.py
```

### Using Ollama (Local AI)

```bash
# Install Ollama from https://ollama.com
ollama pull gemma3

# Run Ollama server (keep this terminal open)
ollama serve

# Now use "Ollama AI" option in the UI
```

### Environment Variables

Create .env file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

🔗 API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /v1/api-key | Get API key |
| POST | /v1/generate | Generate application |
| GET | /v1/stats | Usage statistics |
| GET | /docs | Swagger documentation |

Example Request

```bash
# 1. Get API key
curl -X POST "https://my-dev--agentforge-f0bc.diploi.me/v1/api-key" \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@example.com","plan":"free"}'

# 2. Generate application
curl -X POST "https://my-dev--agentforge-f0bc.diploi.me/v1/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"description":"Simple calculator app","project_name":"MyApp"}'

# 3. Download the ZIP file
# Use the download_url from the response
```

💰 Pricing Plans (via RapidAPI)

| Plan | Price | Requests/month |
| --- | --- | --- |
| Free | $0 | 100 |
| Pro | $49 | 5,000 |
| Business | $99 | 50,000 |
| Enterprise | $499 | Unlimited |

🌍 Links

| Resource | Link |
| --- | --- |
| Live API | [https://my-dev--agentforge-f0bc.diploi.me](https://my-dev--agentforge-f0bc.diploi.me) |
| RapidAPI | [AgentForge on RapidAPI](https://rapidapi.com/abdullahreda1969/api/agentforge-ai-engine) |
| Documentation | [Swagger UI](https://my-dev--agentforge-f0bc.diploi.me/docs) |
| GitHub | [github.com/abdullahreda1969/AgentForge-API](https://github.com/abdullahreda1969/AgentForge-API) |
| Portfolio | [abdullahreda1969.github.io/Portfolio](https://abdullahreda1969.github.io/Portfolio) |

📝 Articles
How I Built an API That Generates Full Applications from Text

API-as-a-Service: How I Turned Code into a Recurring Revenue Business

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

📧 Contact
Email: abdallahreda1969@gmail.com

LinkedIn: Abdullah Reda

📜 License
MIT License - see LICENSE file for details.

Built with ❤️ by Abdullah Reda

text

---
