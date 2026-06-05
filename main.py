from stat import filemode

from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime
import json
import os
from pathlib import Path

from prompt_builder import build_prompt
import anthropic
from fastapi.middleware.cors import CORSMiddleware
from database import get_station_kpis

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "kpai is running"}

@app.get("/kpis")
def get_kpis():
    with open("dummy_kpis.json") as f:
        return json.load(f)

@app.post("/evaluate")
def evaluate_kpis():
    with open("dummy_kpis.json") as f:
        kpi_data = json.load(f)

    prompt = build_prompt(kpi_data)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    evaluation = message.content[0].text
    date_dir = Path(f"reports/{datetime.now().strftime('%Y_%m_%d')}")
    date_dir.mkdir(parents=True, exist_ok=True)
    filename = date_dir / f"evaluation_report_{datetime.now().strftime('%H%M%S')}.md"

    with open(filename, "w") as f:
        f.write(evaluation)

    return {"status": "report saved", "file": filename, "evaluation": evaluation}

@app.post("/evaluate/{station}/{year}/{month}")
def evaluate_station(station: str, year: int, month: int):
    kpi_data = get_station_kpis(station, year, month)

    if not kpi_data:
        return {"error": f"No data found for {station} {month}/{year}"}

    prompt = build_prompt(kpi_data)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    evaluation = message.content[0].text

    date_dir = Path(f"reports/{station}/{year}_{month:02d}")
    date_dir.mkdir(parents=True, exist_ok=True)
    filename = date_dir / f"evaluation_report_{datetime.now().strftime('%H_%M_%S')}.md"

    with open(filename, "w") as f:
        f.write(evaluation)

    return {"evaluation": evaluation, "station": station, "year": year, "month": month}

@app.get("/kpis/{station}/{year}/{month}")
def get_kpis(station: str, year: int, month: int):
    data = get_station_kpis(station, year, month)
    if not data:
        return {"error": f"No data found for {station} {month}/{year}"}
    return data