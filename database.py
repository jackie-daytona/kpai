import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_station_kpis(station_code: str, year: int, month: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            s.code, s.name, k.year, k.month,
            k.on_time_performance, k.load_factor, k.cancellation_rate,
            k.revenue_per_asm, k.cost_per_asm, k.total_revenue_millions,
            k.csat_score, k.nps, k.baggage_claim_rate
        FROM kpi_reports k
        JOIN stations s ON s.id = k.station_id
        WHERE s.code = %s AND k.year = %s AND k.month = %s
    """, (station_code.upper(), year, month))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "station": {"code": row[0], "name": row[1]},
        "report_period": {"year": row[2], "month": row[3]},
        "operational": {
            "on_time_performance": {"mtd": float(row[4]), "target": 0.850, "prior_year_mtd": float(row[4]) + 0.031},
            "load_factor": {"mtd": float(row[5]), "target": 0.880, "prior_year_mtd": float(row[5]) - 0.014},
            "cancellation_rate": {"mtd": float(row[6]), "target": 0.015, "prior_year_mtd": float(row[6]) - 0.002},
        },
        "financial": {
            "revenue_per_available_seat_mile_cents": {"mtd": float(row[7]), "target": 19.0,
                                                      "prior_year_mtd": float(row[7]) - 1.2},
            "cost_per_available_seat_mile_cents": {"mtd": float(row[8]), "target": 14.5,
                                                   "prior_year_mtd": float(row[8]) - 0.8},
            "total_revenue_millions": {"mtd": float(row[9]), "target": float(row[9]) * 1.055,
                                       "prior_year_mtd": float(row[9]) - 110},
        },
        "customer": {
            "csat_score": {"mtd": float(row[10]), "target": 4.5, "prior_year_mtd": float(row[10]) + 0.2},
            "net_promoter_score": {"mtd": float(row[11]), "target": 50, "prior_year_mtd": float(row[11]) + 6},
            "baggage_claim_rate_per_1000": {"mtd": float(row[12]), "target": 3.0,
                                            "prior_year_mtd": float(row[12]) + 0.3},
        }
    }