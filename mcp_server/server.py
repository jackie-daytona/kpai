import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

from mcp.server.fastmcp import FastMCP
from database import get_station_kpis, get_connection

mcp = FastMCP("kpai")

@mcp.tool()
def get_kpi_report(station: str, year: int, month: int) -> dict:
    """Get KPI data for a specific station and month."""
    data = get_station_kpis(station, year, month)
    if not data:
        return {"error": f"No data found for {station} {month}/{year}"}
    return data

@mcp.tool()
def list_stations() -> list:
    """List all available stations in the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT code, name, hub FROM stations ORDER BY code")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"code": r[0], "name": r[1], "hub": r[2]} for r in rows]

@mcp.tool()
def get_station_trend(station: str, year: int) -> list:
    """Get all monthly KPI data for a station across a full year."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT k.month, k.on_time_performance, k.load_factor, 
               k.cancellation_rate, k.nps, k.csat_score
        FROM kpi_reports k
        JOIN stations s ON s.id = k.station_id
        WHERE s.code = %s AND k.year = %s
        ORDER BY k.month
    """, (station.upper(), year))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "month": r[0],
            "on_time_performance": float(r[1]),
            "load_factor": float(r[2]),
            "cancellation_rate": float(r[3]),
            "nps": r[4],
            "csat_score": float(r[5])
        }
        for r in rows
    ]

if __name__ == "__main__":
    mcp.run()