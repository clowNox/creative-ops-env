---
title: Creative Ops Env
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Creative Ops Env

An OpenEnv-style reinforcement learning environment that simulates a marketing agency project coordinator. The environment manages the complex allocation of design tasks (Leads) to available creatives (Designers) based on skill matching, bandwidth, cost tiers, and geographical zones.

## 🚀 Features

- **Dynamic Task Allocation**: Evaluates and assigns leads based on primary/secondary skills, current load, and availability.
- **Complex Scenarios**: Includes `easy`, `medium`, and `hard` scenarios (featuring mid-task disruptions like a designer becoming suddenly unavailable).
- **Multi-step DAG System**: Handles tasks that have dependencies before they can be assigned.
- **FastAPI Integration**: Includes a REST API (`main.py`) for evaluating designers (`/evaluate-designer`) and dissecting high-level projects into actionable leads (`/dissect-project`).
- **Pydantic Models**: Strictly typed state representation using Pydantic.
- **Reward System**: Calculates partial credit rewards based on how well designers match the lead's requirements.

## 🏗 Environment Structure

- **`env.py`**: The core RL environment (`CreativeOpsEnv`). Implements `reset()`, `step()`, and `_compute_reward()` logic.
- **`main.py`**: A FastAPI application providing endpoints to interact with the environment's data parsers.
- **`models.py`**: Pydantic schemas defining `Designer`, `Lead`, `State`, `Action`, and `Observation`.
- **`inference.py`**: Sample script for running inference against the environment.
- **`dissector.py` & `parser.py`**: Utilities for parsing unstructured data into the environment's strict schemas.

## 💻 Running Locally

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the inference script:
   ```bash
   python inference.py
   ```

3. (Optional) Run the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 7860
   ```