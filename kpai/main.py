from fastapi import FastAPI
from dotenv import load_dotenv
import json
import os

from prompt_builder import build_prompt
import anthropic

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.get("/")
def root():
    return {"status": "kpai is running"}

@app.post("/evaluate")
def evaluate_kpis():
    with open("dummy_kpis.json") as f:
        kpi_data = json.load(f)

    prompt = build_prompt(kpi_data)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    evaluation = message.content[0].text

    with open("evaluation_report.md", "w") as f:
        f.write(evaluation)

    return {"status": "report saved", "file": "evaluation_report.md"}