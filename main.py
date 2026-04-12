from env import CreativeOpsEnv
from models import Action

env = CreativeOpsEnv()

obs = env.reset()
print("Initial Observation:", obs)

action = Action(assignments=[{"lead_id": "L1", "designer_id": "D3"}])

obs, reward, done, info = env.step(action)

print("After Step:", obs)
print("Reward:", reward)