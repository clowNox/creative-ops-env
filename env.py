from typing import List, Dict
from models import *
import copy


class CreativeOpsEnv:
    def __init__(self):
        self.task_index = -1
        self.tasks = [
            self._task_easy(),
            self._task_medium(),
            self._task_hard(),
        ]
        self.state_data: State = None

    # ---------- TASKS ----------
    def _task_easy(self):
        return {
            "task_id": "easy_single_assign",
            "designers": [
                Designer(
                    designer_id="D1",
                    name="A",
                    primary_skill="branding",
                    secondary_skills=["ui_ux"],
                    years_experience=3,
                    portfolio_score=0.8,
                    zone="north",
                    cost_tier="medium",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D2",
                    name="B",
                    primary_skill="social_media",
                    secondary_skills=[],
                    years_experience=1,
                    portfolio_score=0.6,
                    zone="south",
                    cost_tier="low",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D3",
                    name="C",
                    primary_skill="social_media",
                    secondary_skills=["video_editing"],
                    years_experience=4,
                    portfolio_score=0.7,
                    zone="north",
                    cost_tier="medium",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
            ],
            "leads": [
                Lead(
                    lead_id="L1",
                    client_name="Cafe Bloom",
                    required_skill="social_media",
                    zone="north",
                    priority="high",
                    budget_tier="medium"
                )
            ]
        }

    def _task_medium(self):
        return {
            "task_id": "medium_multi_assign",
            "designers": [
                Designer(
                    designer_id="D1",
                    name="A",
                    primary_skill="social_media",
                    secondary_skills=[],
                    years_experience=3,
                    portfolio_score=0.8,
                    zone="north",
                    cost_tier="medium",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D2",
                    name="B",
                    primary_skill="branding",
                    secondary_skills=[],
                    years_experience=1,
                    portfolio_score=0.6,
                    zone="south",
                    cost_tier="low",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D3",
                    name="C",
                    primary_skill="video_editing",
                    secondary_skills=[],
                    years_experience=6,
                    portfolio_score=0.9,
                    zone="west",
                    cost_tier="high",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D4",
                    name="D",
                    primary_skill="social_media",
                    secondary_skills=[],
                    years_experience=1,
                    portfolio_score=0.5,
                    zone="north",
                    cost_tier="low",
                    available=False,
                    max_projects=2,
                    current_load=0
                ),
            ],
            "leads": [
                Lead(
                    lead_id="L1",
                    client_name="Cafe Bloom",
                    required_skill="social_media",
                    zone="north",
                    priority="high",
                    budget_tier="medium"
                ),
                Lead(
                    lead_id="L2",
                    client_name="FitNest",
                    required_skill="branding",
                    zone="south",
                    priority="medium",
                    budget_tier="low"
                ),
                Lead(
                    lead_id="L3",
                    client_name="UrbanBite",
                    required_skill="video_editing",
                    zone="north",
                    priority="low",
                    budget_tier="high"
                ),
            ]
        }

    def _task_hard(self):
        return {
            "task_id": "hard_reassign_after_unavailable",
            "designers": [
                Designer(
                    designer_id="D1",
                    name="A",
                    primary_skill="social_media",
                    secondary_skills=[],
                    years_experience=3,
                    portfolio_score=0.8,
                    zone="north",
                    cost_tier="medium",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D2",
                    name="B",
                    primary_skill="branding",
                    secondary_skills=[],
                    years_experience=1,
                    portfolio_score=0.6,
                    zone="south",
                    cost_tier="low",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D3",
                    name="C",
                    primary_skill="video_editing",
                    secondary_skills=[],
                    years_experience=6,
                    portfolio_score=0.9,
                    zone="north",
                    cost_tier="high",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
                Designer(
                    designer_id="D4",
                    name="D",
                    primary_skill="branding",
                    secondary_skills=[],
                    years_experience=3,
                    portfolio_score=0.7,
                    zone="south",
                    cost_tier="medium",
                    available=True,
                    max_projects=2,
                    current_load=0
                ),
            ],
            "leads": [
                Lead(
                    lead_id="L1",
                    client_name="Nova Cafe",
                    required_skill="social_media",
                    zone="north",
                    priority="high",
                    budget_tier="medium"
                ),
                Lead(
                    lead_id="L2",
                    client_name="SkinSoul",
                    required_skill="branding",
                    zone="south",
                    priority="high",
                    budget_tier="medium"
                ),
                Lead(
                    lead_id="L3",
                    client_name="Reeltap",
                    required_skill="video_editing",
                    zone="north",
                    priority="medium",
                    budget_tier="high"
                ),
            ]
        }

    # ---------- RESET ----------
    def reset(self):
        self.task_index = (self.task_index + 1) % len(self.tasks)
        task = self.tasks[self.task_index]

        self.state_data = State(
            task_id=task["task_id"],
            leads=copy.deepcopy(task["leads"]),
            designers=copy.deepcopy(task["designers"]),
            assignments={},
            pending_leads=[l.lead_id for l in task["leads"]],
            step_count=0,
            disruption_triggered=False,
            event_log=[]
        )
        return self._get_obs()

    # ---------- STEP ----------
    def step(self, action: Action):
        self.state_data.step_count += 1
        info = {"per_lead": {}}

        for a in action.assignments:
            lid = a["lead_id"]
            did = a["designer_id"]

            if lid not in self.state_data.pending_leads:
                continue

            designer = next((d for d in self.state_data.designers if d.designer_id == did), None)
            lead = next((l for l in self.state_data.leads if l.lead_id == lid), None)

            if not designer or not lead:
                continue

            self.state_data.assignments[lid] = did
            self.state_data.pending_leads.remove(lid)
            designer.current_load += 1

        # HARD TASK DISRUPTION
        if self.state_data.task_id == "hard_reassign_after_unavailable" and not self.state_data.disruption_triggered:
            self.state_data.disruption_triggered = True
            self.state_data.event_log.append("D2 became unavailable")

            for d in self.state_data.designers:
                if d.designer_id == "D2":
                    d.available = False

            for lid, did in list(self.state_data.assignments.items()):
                if did == "D2":
                    self.state_data.pending_leads.append(lid)
                    del self.state_data.assignments[lid]

            return self._get_obs(), Reward(score=0.0, breakdown={}), False, info

        reward = self._compute_reward(info)
        done = True
        return self._get_obs(), reward, done, info

    # ---------- REWARD ----------
    def _compute_reward(self, info):
        scores = []

        for lead in self.state_data.leads:
            score = 1.0
            did = self.state_data.assignments.get(lead.lead_id)

            if not did:
                if lead.priority == "high":
                    score -= 0.2
                scores.append(max(0, score))
                continue

            designer = next(d for d in self.state_data.designers if d.designer_id == did)

            if designer.primary_skill != lead.required_skill:
                score -= 0.5
            if not designer.available:
                score -= 0.6
            if designer.zone != lead.zone:
                score -= 0.15
            if designer.cost_tier != lead.budget_tier:
                score -= 0.15
            if designer.current_load > designer.max_projects:
                score -= 0.25

            score = max(0, min(1, score))
            info["per_lead"][lead.lead_id] = score
            scores.append(score)

        final = sum(scores) / len(scores)
        return Reward(score=max(0, min(1, final)), breakdown=info["per_lead"])

    # ---------- OBS ----------
    def _get_obs(self):
        return Observation(
            task_id=self.state_data.task_id,
            pending_leads=self.state_data.pending_leads,
            designers=self.state_data.designers,
            current_assignments=self.state_data.assignments,
            event_log=self.state_data.event_log,
            step_count=self.state_data.step_count
        )

    def state(self):
        return self.state_data