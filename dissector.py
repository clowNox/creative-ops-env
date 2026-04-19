import uuid
from typing import List
from models import Project, Lead

def dissect_project(project: Project) -> List[Lead]:
    """
    Parses a top-level Project description and breaks it down into individual Leads (sub-tasks).
    In a real system, this would be backed by an LLM parsing natural language.
    Here we use keyword matching heuristics.
    """
    desc = project.description.lower()
    leads = []

    # Variables to hold generated leads for dependency linking
    branding_lead = None
    ui_ux_lead = None

    # Foundational Tasks (No dependencies)
    if "logo" in desc or "brand" in desc or "identity" in desc:
        branding_lead = _create_lead(project, "branding")
        leads.append(branding_lead)

    if "website" in desc or "app" in desc or "ui" in desc or "ux" in desc:
        ui_ux_lead = _create_lead(project, "ui_ux")
        # UI/UX might depend on branding if both are created
        if branding_lead:
            ui_ux_lead.depends_on.append(branding_lead.lead_id)
        leads.append(ui_ux_lead)

    if "illustration" in desc or "drawing" in desc or "art" in desc:
        ill_lead = _create_lead(project, "illustration")
        if branding_lead:
            ill_lead.depends_on.append(branding_lead.lead_id)
        leads.append(ill_lead)

    # Downstream Tasks (Depend on foundational tasks)
    if "video" in desc or "promo" in desc or "reel" in desc:
        video_lead = _create_lead(project, "video_editing")
        if branding_lead:
            video_lead.depends_on.append(branding_lead.lead_id)
        leads.append(video_lead)

    if "social" in desc or "instagram" in desc or "post" in desc:
        social_lead = _create_lead(project, "social_media")
        # Social media usually needs branding and UI assets first
        if branding_lead:
            social_lead.depends_on.append(branding_lead.lead_id)
        if ui_ux_lead:
            social_lead.depends_on.append(ui_ux_lead.lead_id)
        leads.append(social_lead)

    # If no specific keywords matched, default to general design
    if not leads:
        leads.append(_create_lead(project, "general_design"))

    return leads

def _create_lead(project: Project, skill: str) -> Lead:
    """Helper to instantiate a Lead based on the parent Project."""
    return Lead(
        lead_id=f"L_{uuid.uuid4().hex[:8]}",
        project_id=project.project_id,
        client_name=project.client_name,
        required_skill=skill,
        zone=project.zone,
        priority=project.priority,
        # A real system might split the total_budget among leads.
        # Here we just pass the overall project tier down.
        budget_tier=project.total_budget
    )
