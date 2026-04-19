from env import CreativeOpsEnv
from models import Action


def policy(obs):
    assignments = []

    # Use full lead objects directly from observation
    pending_leads_objects = list(obs.pending_leads)

    # Sort leads by priority (high > medium > low)
    priority_map = {"high": 3, "medium": 2, "low": 1}
    pending_leads_objects.sort(key=lambda l: priority_map.get(l.priority, 0), reverse=True)

    # Track simulated load during this step to prevent overbooking designers
    simulated_loads = {d.designer_id: d.current_load for d in obs.designers}

    for lead in pending_leads_objects:
        best_designer = None
        best_score = -float('inf')

        for d in obs.designers:
            if not d.available:
                continue

            # Don't assign if they are already at their max project limit
            if simulated_loads[d.designer_id] >= d.max_projects:
                continue

            score = 1.0

            # Evaluate skill match
            if d.primary_skill != lead.required_skill:
                if lead.required_skill in getattr(d, "secondary_skills", []):
                    score -= 0.1
                else:
                    score -= 0.5

            # Evaluate zone match
            if d.zone != lead.zone:
                score -= 0.15

            # Evaluate budget match
            if d.cost_tier != lead.budget_tier:
                score -= 0.15

            if score > best_score:
                best_score = score
                best_designer = d

        if best_designer:
            assignments.append({"lead_id": lead.lead_id, "designer_id": best_designer.designer_id})
            simulated_loads[best_designer.designer_id] += 1

    return Action(assignments=assignments)


if __name__ == "__main__":
    env = CreativeOpsEnv()

    from models import Project
    from dissector import dissect_project

    for i in range(4):
        print(f"\n[START TASK {i+1}]")
        obs = env.reset()

        # For the 4th task, let's inject a complex DAG project to test dependencies
        if i == 3:
            print("--- Injecting Complex Project with Dependencies ---")
            p = Project(
                project_id="DAG_1",
                client_name="TestCorp",
                description="We need a new logo, an app ui, and 3 promo videos for instagram.",
                total_budget="high",
                zone="north",
                priority="high"
            )
            obs = env.add_project_leads(p)

        done = False
        step_idx = 1
        while not done:
            # Print tasks that are in review
            in_review = [l.lead_id for l in env.state().leads if l.status == "in_review"]
            if in_review:
                print(f"[STEP {step_idx}] Tasks In Review: {in_review}")

            action = policy(obs)
            print(f"[STEP {step_idx}] Pending Leads: {[l.lead_id for l in obs.pending_leads]} | Action: {action.assignments}")

            obs, reward, done, info = env.step(action)

            # Print events (like approvals or rejections)
            if obs.event_log:
                print(f"   > Events: {obs.event_log[-2:]}") # Print the last few events

            step_idx += 1

        print(f"[END] Score: {reward.score:.2f} | Total Steps Taken: {step_idx - 1}")