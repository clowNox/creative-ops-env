from typing import List, Dict
from models import *
import copy
import random


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

    def add_project_leads(self, project: Project):
        """
        Dynamically adds parsed leads from a new project into the current environment state.
        """
        from dissector import dissect_project
        new_leads = dissect_project(project)

        # Add to state
        for lead in new_leads:
            self.state_data.leads.append(lead)

        self.state_data.event_log.append(f"Added {len(new_leads)} new leads from project {project.project_id}")
        self._update_pending_leads()
        return self._get_obs()

    # ---------- RESET ----------
    def reset(self):
        self.task_index = (self.task_index + 1) % len(self.tasks)
        task = self.tasks[self.task_index]

        self.state_data = State(
            task_id=task["task_id"],
            leads=copy.deepcopy(task["leads"]),
            designers=copy.deepcopy(task["designers"]),
            assignments={},
            pending_leads=[], # Will be populated dynamically based on DAG
            step_count=0,
            disruption_triggered=False,
            event_log=[]
        )
        self._update_pending_leads()
        return self._get_obs()

    def _update_pending_leads(self):
        """
        Calculates which leads are available to be worked on.
        A lead is pending if it is 'pending' AND all its dependencies are 'completed'.
        """
        completed_lead_ids = {l.lead_id for l in self.state_data.leads if l.status == "completed"}

        # We need to rebuild the pending_leads list from scratch each time
        # to ensure it only contains items that are actually pending.
        new_pending_leads = []
        for l in self.state_data.leads:
            if l.status == "pending":
                # Check if all dependencies are met
                if all(dep in completed_lead_ids for dep in l.depends_on):
                    new_pending_leads.append(l.lead_id)
        self.state_data.pending_leads = new_pending_leads

    # ---------- STEP ----------
    def step(self, action: Action):
        self.state_data.step_count += 1
        info = {"per_lead": {}}

        # Process Time Progression: Review tasks in "in_review" state
        for lead in list(self.state_data.leads):
            if lead.status == "in_review":
                did = self.state_data.assignments.get(lead.lead_id)
                designer = next((d for d in self.state_data.designers if d.designer_id == did), None)

                # Client approval probability is tied to the designer's portfolio score (default 80% if missing)
                approval_chance = getattr(designer, "portfolio_score", 0.8) if designer else 0.8

                if random.random() <= approval_chance:
                    # Client Approves
                    lead.status = "completed"
                    if designer: designer.current_load -= 1
                    self.state_data.event_log.append(f"Client approved Task {lead.lead_id}.")
                else:
                    # Client Rejects
                    lead.status = "pending" # Send back to pending queue to be re-assigned
                    if designer: designer.current_load -= 1
                    del self.state_data.assignments[lead.lead_id]
                    self.state_data.event_log.append(f"Client rejected Task {lead.lead_id}. Requires rework.")

        # Process Time Progression: Move in-progress tasks to in_review
        for lead in self.state_data.leads:
            if lead.status == "in_progress":
                lead.status = "in_review"
                self.state_data.event_log.append(f"Task {lead.lead_id} submitted for client review.")

        # Process New Assignments
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
            lead.status = "in_progress"
            designer.current_load += 1

        self._update_pending_leads()

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
                    lead = next((l for l in self.state_data.leads if l.lead_id == lid), None)
                    if lead: lead.status = "pending"
                    del self.state_data.assignments[lid]

            # In the new multi-step DAG system, we shouldn't return early and skip calculating the "done" condition
            # The agent still needs to know if the simulation is over.

        reward = self._compute_reward(info)
        done = all(l.status == "completed" for l in self.state_data.leads)
        return self._get_obs(), reward, done, info

    # ---------- REWARD ----------
    def _compute_reward(self, info):
        scores = []

        for lead in self.state_data.leads:
            score = 1.0
            did = self.state_data.assignments.get(lead.lead_id)

            # Do not penalize leads that are currently blocked by dependencies and cannot be assigned yet
            if not did:
                if lead.status == "pending" and lead.lead_id not in self.state_data.pending_leads:
                    continue # Ignore blocked leads for reward calculation

                if lead.priority == "high":
                    score -= 0.2
                scores.append(max(0, score))
                continue

            designer = next(d for d in self.state_data.designers if d.designer_id == did)

            if designer.primary_skill != lead.required_skill:
                if lead.required_skill in getattr(designer, "secondary_skills", []):
                    # Slight penalty for using a secondary skill instead of primary
                    score -= 0.1
                else:
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
        # Only include the full Lead objects that are actually pending
        pending_lead_objs = [l for l in self.state_data.leads if l.lead_id in self.state_data.pending_leads]

        return Observation(
            task_id=self.state_data.task_id,
            pending_leads=pending_lead_objs,
            designers=self.state_data.designers,
            current_assignments=self.state_data.assignments,
            event_log=self.state_data.event_log,
            step_count=self.state_data.step_count
        )

    def state(self):
        return self.state_data