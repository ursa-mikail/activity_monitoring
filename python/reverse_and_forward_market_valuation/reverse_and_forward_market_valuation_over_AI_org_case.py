import plotly.express as px
import pandas as pd

# CLIF Model: Conditional Leverage Investment Forecasting

def clif_model(mv_0, strategies, hostiles):
    positive = sum(p * l * m * g for p, l, m, g, _, _ in strategies)
    negative = sum(h * d * f for h, d, f, _, _ in hostiles)
    return mv_0 + positive - negative

# Initial market value
mv_0 = 10e6  # $10 million

# Strategies: (P_i, L_i, M_i, G_i, strategy_desc, reason_success)
strategies = [
    (0.6, 0.3, 2e12, 5, 'Enter AI Assistant Market', 'Enterprise adoption of AI assistants growing fast')
]

# Hostile conditions: (H_j, D_j, F_j, hostile_desc, reason_failure)
hostiles = [
    (0.5, 0.6, 500e9, 'Regulation Risk', 'Government caps on commercial AI usage'),
    (0.7, 0.4, 1e12, 'Open-source Disruption', 'Open models reduce commercial moat')
]

# Step values
mv_strategy = mv_0 + sum(p * l * m * g for p, l, m, g, _, _ in strategies)
mv_hostile = mv_strategy - sum(h * d * f for h, d, f, _, _ in hostiles)
mv_forecast = clif_model(mv_0, strategies, hostiles)

# Timepoints and explanations
timeline = ['t₀: Start', 't₁: After Strategy', 't₂: After Hostiles', 't₃: Final Forecast']
values = [mv_0, mv_strategy, mv_hostile, mv_forecast]
reasons = [
    "Initial valuation",
    "Strategy success: " + strategies[0][4] + " — " + strategies[0][5],
    "Impact of hostile: " + hostiles[0][3] + ", " + hostiles[1][3],
    "Forecast considering all factors"
]

df = pd.DataFrame({
    "Timepoint": timeline,
    "Market Value (USD)": values,
    "Reason": reasons
})

# Plot using Plotly
fig = px.scatter(
    df,
    x="Timepoint",
    y="Market Value (USD)",
    text="Reason",
    hover_data={
        "Reason": True,
        "Market Value (USD)": ':.2f'
    },
    title="CLIF Forecast Model: Market Value Over Time"
)

fig.update_traces(mode="markers+lines+text", textposition="top center")

fig.update_layout(
    hovermode="closest",
    plot_bgcolor="white",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

fig.show()

# Save and display
fig.write_html("clif_model_forecast.html", include_plotlyjs="cdn")
print("✅ Plot exported to 'clif_model_forecast.html'. Open it in your browser to see tooltips.")

