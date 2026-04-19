from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import DesignerApplication, Designer, Project, Lead
from typing import List
from parser import parse_application
from dissector import dissect_project

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>Creative Ops Env</title></head>
        <body>
            <h1>Creative Ops Env is running 🚀</h1>
            <p>RL environment for project allocation</p>
            <p>Check health: <a href="/health">/health</a></p>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"message": "Creative Ops Env is running"}

@app.post("/evaluate-designer", response_model=Designer)
def evaluate_designer(application: DesignerApplication):
    """
    Ingests a designer's resume and portfolio, and returns a structured Designer profile.
    """
    designer = parse_application(application)
    return designer

@app.post("/dissect-project", response_model=List[Lead])
def dissect_project_endpoint(project: Project):
    """
    Ingests a new high-level Project and breaks it down into individual Lead tasks.
    """
    leads = dissect_project(project)
    return leads
