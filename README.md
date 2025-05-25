# Smart Job Finder

Smart Job Finder is an AI-powered web app that allows users to search for jobs based on **country**, **city**, and **job title**. It uses **LangChain**, **OpenAI**, and a **web search tool** (e.g., Tavily) to find, summarize, and display relevant jobs in a clean, Bootstrap-based UI.

---

## 🔧 Features

- 🌐 Web search using LangChain + Tavily
- 🤖 OpenAI summarization of job postings
- 📄 Display job title, company, location, description, and apply link
- 🎨 Responsive UI with Bootstrap
- ⚡ FastAPI backend with Jinja2 templates

---

## 🧠 Architecture

- **Backend:** FastAPI + Jinja2 + LangChain + OpenAI
- **Search Tool:** TavilySearchResults (via LangChain)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-job-finder.git
cd smart-job-finder
```

### 2. Setup the Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file and add:

```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Setup

You can also run the app with Docker Compose:

```bash
docker compose up --build
```

The app will be available at [http://localhost:8000](http://localhost:8000)

---

## 📁 Folder Structure

```
smart-job-finder/
├── app/
│   ├── main.py
│   ├── langchain_agent.py
│   ├── __init__.py
├── templates/
│   └── index.html
├── static/
│   └── README.txt
├── requirements.txt
├── Dockerfile.backend
├── docker-compose.yml
└── README.md
```

---

## 🙏 Credits

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [Tavily](https://www.tavily.com/)
- [Bootstrap](https://getbootstrap.com/)
