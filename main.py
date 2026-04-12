from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
