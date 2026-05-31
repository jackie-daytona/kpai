def build_prompt(kpi_data: dict) -> str:
    period = kpi_data["report_period"]
    ops = kpi_data["operational"]
    fin = kpi_data["financial"]
    cust = kpi_data["customer"]

    prompt = f"""
You are an airline operations analyst. Evaluate the following KPI data for {period["month"]} {period["year"]}.
For each metric, compare against the target and prior year, flag any concerns, and provide a brief recommendation.

OPERATIONAL:
- On-time performance: {ops["on_time_performance"]["mtd"]:.1%} (target: {ops["on_time_performance"]["target"]:.1%}, prior year: {ops["on_time_performance"]["prior_year_mtd"]:.1%})
- Load factor: {ops["load_factor"]["mtd"]:.1%} (target: {ops["load_factor"]["target"]:.1%}, prior year: {ops["load_factor"]["prior_year_mtd"]:.1%})
- Cancellation rate: {ops["cancellation_rate"]["mtd"]:.1%} (target: {ops["cancellation_rate"]["target"]:.1%}, prior year: {ops["cancellation_rate"]["prior_year_mtd"]:.1%})

FINANCIAL:
- Revenue per ASM: {fin["revenue_per_available_seat_mile_cents"]["mtd"]}¢ (target: {fin["revenue_per_available_seat_mile_cents"]["target"]}¢, prior year: {fin["revenue_per_available_seat_mile_cents"]["prior_year_mtd"]}¢)
- Cost per ASM: {fin["cost_per_available_seat_mile_cents"]["mtd"]}¢ (target: {fin["cost_per_available_seat_mile_cents"]["target"]}¢, prior year: {fin["cost_per_available_seat_mile_cents"]["prior_year_mtd"]}¢)
- Total revenue: ${fin["total_revenue_millions"]["mtd"]}M (target: ${fin["total_revenue_millions"]["target_mtd"]}M, prior year: ${fin["total_revenue_millions"]["prior_year_mtd"]}M)

CUSTOMER:
- CSAT: {cust["csat_score"]["mtd"]} / 5 (target: {cust["csat_score"]["target"]}, prior year: {cust["csat_score"]["prior_year_mtd"]})
- NPS: {cust["net_promoter_score"]["mtd"]} (target: {cust["net_promoter_score"]["target"]}, prior year: {cust["net_promoter_score"]["prior_year_mtd"]})
- Baggage claim rate: {cust["baggage_claim_rate_per_1000"]["mtd"]} per 1,000 (target: {cust["baggage_claim_rate_per_1000"]["target"]}, prior year: {cust["baggage_claim_rate_per_1000"]["prior_year_mtd"]})

Provide a concise evaluation with: overall performance summary, top 2-3 concerns, and recommendations.
"""
    return prompt.strip()