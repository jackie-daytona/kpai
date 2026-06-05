def build_prompt(kpi_data: dict) -> str:
    period = kpi_data["report_period"]
    ops = kpi_data["operational"]
    fin = kpi_data["financial"]
    cust = kpi_data["customer"]
    MONTHS = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    prompt = f"""
You are an airline operations analyst. Evaluate the following KPI data for {MONTHS[period["month"]]} {period["year"]} at {kpi_data["station"]["name"]} ({kpi_data["station"]["code"]}).
STRICT FORMATTING RULES:
- Use ONLY these status indicators: 🔴 CRITICAL, 🟡 CAUTION, 🟢 POSITIVE
- No other emojis or symbols
- Every metric must include: gap to target, YoY change, one Concern or Status note (2 sentences max), one Recommendation (1-2 sentences per tier)
- Keep recommendations concise — no dollar estimates or passenger projections
- Recommendations must be tiered: IMMEDIATE (0-30 days), SHORT-TERM (30-90 days), STRATEGIC (90+ days)
- Top 3 Concerns: 3-4 sentences each, no financial projections
- Bottom Line: 3-4 sentences max

OUTPUT STRUCTURE (follow exactly):
1. Overall Performance Summary (2-3 sentences)
2. Metric-by-Metric Analysis (Operational, Financial, Customer sections)
3. Top 3 Concerns (numbered, with impact explanation)
4. Priority Recommendations (tiered)
5. Bottom Line

OPERATIONAL:
- On-time performance: {ops["on_time_performance"]["mtd"]:.1%} (target: {ops["on_time_performance"]["target"]:.1%}, prior year: {ops["on_time_performance"]["prior_year_mtd"]:.1%})
- Load factor: {ops["load_factor"]["mtd"]:.1%} (target: {ops["load_factor"]["target"]:.1%}, prior year: {ops["load_factor"]["prior_year_mtd"]:.1%})
- Cancellation rate: {ops["cancellation_rate"]["mtd"]:.1%} (target: {ops["cancellation_rate"]["target"]:.1%}, prior year: {ops["cancellation_rate"]["prior_year_mtd"]:.1%})

FINANCIAL:
- Revenue per ASM: {fin["revenue_per_available_seat_mile_cents"]["mtd"]}¢ (target: {fin["revenue_per_available_seat_mile_cents"]["target"]}¢, prior year: {fin["revenue_per_available_seat_mile_cents"]["prior_year_mtd"]}¢)
- Cost per ASM: {fin["cost_per_available_seat_mile_cents"]["mtd"]}¢ (target: {fin["cost_per_available_seat_mile_cents"]["target"]}¢, prior year: {fin["cost_per_available_seat_mile_cents"]["prior_year_mtd"]}¢)
- Total revenue: ${fin["total_revenue_millions"]["mtd"]}M (target: ${fin["total_revenue_millions"]["target"]}M, prior year: ${fin["total_revenue_millions"]["prior_year_mtd"]}M)

CUSTOMER:
- CSAT: {cust["csat_score"]["mtd"]} / 5 (target: {cust["csat_score"]["target"]}, prior year: {cust["csat_score"]["prior_year_mtd"]})
- NPS: {cust["net_promoter_score"]["mtd"]} (target: {cust["net_promoter_score"]["target"]}, prior year: {cust["net_promoter_score"]["prior_year_mtd"]})
- Baggage claim rate: {cust["baggage_claim_rate_per_1000"]["mtd"]} per 1,000 (target: {cust["baggage_claim_rate_per_1000"]["target"]}, prior year: {cust["baggage_claim_rate_per_1000"]["prior_year_mtd"]})
""".strip()

    return prompt