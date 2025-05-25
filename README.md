# Smart Job Finder

A modern web application that helps job seekers find their dream positions through an interactive chat interface. The application uses AI to understand user preferences and provides relevant job opportunities.

## Features

- 🤖 Interactive chat interface for job search
- 🌍 Location-based job filtering
- 💼 Position-specific job recommendations
- 🎯 Smart parameter extraction from natural language
- 📱 Responsive design for all devices
- ⚡ Fast and efficient job search results

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap 5
- **Icons**: Font Awesome
- **AI Integration**: Custom Job Search Agent

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/smart-job-finder.git
cd smart-job-finder
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add necessary environment variables.

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Open your browser and navigate to:

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
