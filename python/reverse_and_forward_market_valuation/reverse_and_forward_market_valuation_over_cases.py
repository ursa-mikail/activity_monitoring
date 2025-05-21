import plotly.express as px
import pandas as pd

# Microsoft Case (Green) - Success Trajectory
microsoft_timeline = ['1980', '1985', '1990', '1995', '2000', '2010', '2020']
microsoft_values = [1e6, 10e6, 100e6, 500e6, 1e9, 10e9, 1000e9]  # Example estimations in USD
microsoft_reasons = [
    "Startup phase, collaboration with IBM",
    "Launch of Windows",
    "Dominance in PC OS market",
    "Expansion in Office Suite and enterprise deals",
    "IPO success and international expansion",
    "Cloud and enterprise services grow",
    "AI integration and trillion-dollar valuation"
]

# Polaroid Case (Red) - Failure Trajectory
polaroid_timeline = ['1980', '1985', '1990', '1995', '2000', '2008']
polaroid_values = [1e9, 1.2e9, 1e9, 800e6, 300e6, 0]  # Example estimations in USD
polaroid_reasons = [
    "Strong instant photo market",
    "Maintains analog camera leadership",
    "Misses early digital trends",
    "Declining relevance due to digital rise",
    "Severe losses and decline",
    "Bankruptcy filed"
]

# AI Org Forecast (Blue) - Hypothetical Success Trajectory
ai_timeline = ['2025', '2030', '2035', '2040', '2045']
ai_values = [10e6, 200e6, 5e9, 100e9, 500e9]  # Hypothetical in USD
ai_reasons = [
    "Early adoption and foundational models",
    "AI-as-a-Service gains traction",
    "Autonomous systems and enterprise AGI",
    "Global-scale deployments and regulation",
    "Becomes fundamental to daily operations"
]

# Combine all into one DataFrame
data = []

for year, val, reason in zip(microsoft_timeline, microsoft_values, microsoft_reasons):
    data.append({"Year": year, "Market Value": val, "Reason": reason, "Company": "Microsoft"})

for year, val, reason in zip(polaroid_timeline, polaroid_values, polaroid_reasons):
    data.append({"Year": year, "Market Value": val, "Reason": reason, "Company": "Polaroid"})

for year, val, reason in zip(ai_timeline, ai_values, ai_reasons):
    data.append({"Year": year, "Market Value": val, "Reason": reason, "Company": "Future AI Org"})

df = pd.DataFrame(data)

# Plot
fig = px.line(
    df,
    x="Year",
    y="Market Value",
    color="Company",
    markers=True,
    hover_data={"Reason": True, "Market Value": ':.2f'},
    title="Company Valuation Forecast: Microsoft vs Polaroid vs Future AI Org"
)

fig.update_traces(text=df["Reason"], mode="markers+lines")
fig.update_layout(
    hovermode="closest",
    plot_bgcolor="white",
    xaxis=dict(showgrid=True, title="Year"),
    yaxis=dict(showgrid=True, title="Market Value (USD)"),
    legend_title_text="Company"
)

fig.write_html("/company_valuation_forecast.html", include_plotlyjs="cdn")
fig.show()

