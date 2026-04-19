import uuid
import re
from typing import Tuple, List
from models import DesignerApplication, Designer

def parse_application(app: DesignerApplication) -> Designer:
    """
    Parses a resume and portfolio URL to extract designer skills, experience, and cost tier.
    In a real system, this would call an LLM API (like OpenAI) or an ML model.
    Here, we use heuristics to mock the process.
    """
    resume_text = app.resume_text.lower()

    # 1. Extract Primary & Secondary Skills
    skills = ["branding", "social_media", "video_editing", "ui_ux", "illustration", "3d_modeling"]
    found_skills = []

    for skill in skills:
        skill_clean = skill.replace("_", " ")
        if skill_clean in resume_text or skill in resume_text:
            found_skills.append(skill)

    if "graphic design" in resume_text:
        if "branding" not in found_skills: found_skills.append("branding")
    if "premiere" in resume_text or "after effects" in resume_text:
        if "video_editing" not in found_skills: found_skills.append("video_editing")
    if "figma" in resume_text or "sketch" in resume_text:
        if "ui_ux" not in found_skills: found_skills.append("ui_ux")

    primary_skill = found_skills[0] if found_skills else "general_design"
    secondary_skills = found_skills[1:] if len(found_skills) > 1 else []

    # 2. Extract Years of Experience
    experience = 0
    # Match patterns like "5 years", "3+ years of experience"
    exp_matches = re.findall(r'(\d+)(?:\+| years| yrs)', resume_text)
    if exp_matches:
        experience = max(int(m) for m in exp_matches)

    # 3. Determine Cost Tier
    if experience >= 5:
        cost_tier = "high"
    elif experience >= 2:
        cost_tier = "medium"
    else:
        cost_tier = "low"

    # 4. Evaluate Portfolio (Mock Scoring)
    portfolio_score = 0.0
    if app.portfolio_url:
        # Mock logic: if they have a real portfolio, give a score between 0.5 and 0.9.
        # In reality, this would use a vision-language model to evaluate design quality.
        if "behance" in app.portfolio_url.lower() or "dribbble" in app.portfolio_url.lower():
            portfolio_score = 0.8
        else:
            portfolio_score = 0.6

    # Generate unique ID
    designer_id = f"D_{uuid.uuid4().hex[:8]}"

    return Designer(
        designer_id=designer_id,
        name=app.name,
        primary_skill=primary_skill,
        secondary_skills=secondary_skills,
        years_experience=experience,
        portfolio_score=portfolio_score,
        zone=app.zone,
        cost_tier=cost_tier,
        available=True,
        max_projects=2 if cost_tier == "low" else 3 if cost_tier == "medium" else 4,
        current_load=0
    )
