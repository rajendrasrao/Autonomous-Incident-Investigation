import fastapi
from src.IncidentState import run_incident_intake

app=fastapi.FastAPI()


@app.post("/intake")
def intake_incident(raw_report:str):
    incident_state=run_incident_intake(raw_report)
    return incident_state


@app.get("/")
def health():
    return {"status": "ok"}