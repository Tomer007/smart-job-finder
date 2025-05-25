from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from app.chat_agent import JobSearchAgent
#from app.langchain_agent import fetch_and_summarize_jobs
from urllib.parse import quote
import json
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize the agent
job_search_agent = JobSearchAgent()

class SearchRequest(BaseModel):
    country: str
    city: str
    position_name: str
    salary_range: Optional[str] = None
    experience_level: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "results": None})

@app.post("/", response_class=HTMLResponse)
def submit_form(request: Request, country: str = Form(...), city: str = Form(...), job_title: str = Form(...)):
    return templates.TemplateResponse("chat.html", {"request": request, "country": country, "city": city, "job_title": job_title})

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat/api")
def chat_api(user_message: str = Query(..., alias="user_message")):
    response = job_search_agent.process_chat_message(user_message)
    
    # Check if we have all mandatory fields
    if all([
        job_search_agent.country != "Unknown",
        job_search_agent.city != "Unknown",
        job_search_agent.job_title != "Unknown"
    ]):
        # Always use the confirmation prompt here!
        response = {
            "message": f"I've collected all the information about {job_search_agent.job_title} positions in {job_search_agent.city}, {job_search_agent.country}. Would you like to see the available opportunities?",
            "has_all_fields": True,
            "search_params": {
                "country": job_search_agent.country,
                "city": job_search_agent.city,
                "position_name": job_search_agent.job_title
            }
        }
    
    return JSONResponse({"reply": response})

@app.get("/results", response_class=HTMLResponse)
def results_page(request: Request):
    country = request.query_params.get("country", "")
    city = request.query_params.get("city", "")
    position_name = request.query_params.get("position_name", "")
    
    try:
        # Fetch jobs using the search parameters
        jobs_data = job_search_agent.process_message(f"{position_name} in {city}, {country}")
        if isinstance(jobs_data, str):
            jobs_data = json.loads(jobs_data)
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        jobs_data = []
    
    # Reset the agent's memory after showing results
    job_search_agent.reset()
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "jobs": jobs_data,
            "summary": f"Showing results for {position_name} positions in {city}, {country}"
        }
    )
