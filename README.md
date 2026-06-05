# kpai — Airline KPI Evaluator

A full-stack AI-powered KPI evaluation tool built with FastAPI, PostgreSQL, and the Anthropic Claude API.

## Stack
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **AI:** Anthropic Claude API
- **Frontend:** HTML, Chart.js

## Features
- Station-level KPI scorecards with red/yellow/green indicators
- Actual vs target and YoY charts
- AI-generated evaluation reports powered by Claude
- Reports saved and organized by station and date

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Add a `.env` file with your `ANTHROPIC_API_KEY` and `DATABASE_URL`
4. Run the server: `uvicorn main:app --reload`
5. Open `index.html` in your browser