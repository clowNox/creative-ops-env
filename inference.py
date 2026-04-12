from env import CreativeOpsEnv
from models import Action


def policy(obs):
    assignments = []

    for lid in obs.pending_leads:
        best = None
        best_score = -1

        for d in obs.designers:
            score = 0
            if not d.available:
                continue

            if d.primary_skill:
                score += 1
            if d.zone:
                score += 1
            if d.cost_tier:
                score += 1

            if score > best_score:
                best_score = score
                best = d

        if best:
            assignments.append({"lead_id": lid, "designer_id": best.designer_id})

    return Action(assignments=assignments)


if __name__ == "__main__":
    env = CreativeOpsEnv()

    for i in range(3):
        print(f"\n[START TASK {i+1}]")
        obs = env.reset()

        done = False
        while not done:
            action = policy(obs)
            print("[STEP]", action)

            obs, reward, done, info = env.step(action)

        print("[END] Score:", reward.score)