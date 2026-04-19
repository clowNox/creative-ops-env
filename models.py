from pydantic import BaseModel
from typing import List, Dict


from typing import Optional

class Designer(BaseModel):
    designer_id: str
    name: str
    primary_skill: str
    secondary_skills: List[str] = []
    years_experience: Optional[int] = None
    portfolio_score: Optional[float] = None
    zone: str
    cost_tier: str
    available: bool
    max_projects: int
    current_load: int


class DesignerApplication(BaseModel):
    name: str
    resume_text: str
    portfolio_url: Optional[str] = None
    zone: str


class Project(BaseModel):
    project_id: str
    client_name: str
    description: str
    total_budget: str
    zone: str
    priority: str


class Lead(BaseModel):
    lead_id: str
    project_id: Optional[str] = None
    client_name: str
    required_skill: str
    zone: str
    priority: str
    budget_tier: str


class Action(BaseModel):
    assignments: List[Dict[str, str]]


class Observation(BaseModel):
    task_id: str
    pending_leads: List[Lead]
    designers: List[Designer]
    current_assignments: Dict[str, str]
    event_log: List[str]
    step_count: int


class State(BaseModel):
    task_id: str
    leads: List[Lead]
    designers: List[Designer]
    assignments: Dict[str, str]
    pending_leads: List[str]
    step_count: int
    disruption_triggered: bool
    event_log: List[str]


class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float]