#!pip install faker
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import plotly.express as px
import pandas as pd

# Step 1: Generate fake data
fake = Faker()
data = []

start_time = datetime.now() - timedelta(days=10)

for _ in range(100):
    time = start_time + timedelta(minutes=random.randint(0, 14400))  # Spread over 10 days
    unix_time = int(time.timestamp())
    timestamp_str = f"{time.strftime('%Y-%m-%d_%H%M:%S')} [{unix_time}]"
    
    data.append({
        "Timestamp": timestamp_str,
        "datetime": time,  # true datetime object for plotting
        "log": fake.sentence(),
        "score": round(random.uniform(0, 100), 2),
        "reference": fake.uuid4(),
        "tags": [fake.word() for _ in range(random.randint(1, 3))]
    })

# Step 2: Convert to DataFrame
df = pd.DataFrame(data)

# Sort the DataFrame by datetime
df = df.sort_values(by="datetime")

fig.update_traces(mode="markers+lines")
fig.update_layout(hovermode="closest")

# Then re-plot (scatter only, or sorted lines)
fig = px.scatter(
    df,
    x="datetime",
    y="score",
    hover_data={
        "log": True,
        "Timestamp": True,
        "score": True,
        "datetime": False
    },
    title="Score Time Series with Logs and Timestamps (Chronologically Sorted)",
    labels={"datetime": "Time", "score": "Score"}
)

# Optional: If you want to include lines, keep this. Otherwise, comment it out for just scatter points.
fig.update_traces(mode="markers+lines")  # or use "markers" for scatter-only

fig.update_layout(
    hovermode="closest",
    plot_bgcolor="white",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

fig.show()

# After fig is created and configured
fig.write_html("score_time_series.html", full_html=True, include_plotlyjs="cdn")

# Optional confirmation
print("Exported to score_time_series.html")

"""
📌 Faker creates random logs, timestamps, UUIDs, and tags.
📌 Timestamps are formatted as "YYYY-MM-DD_hhmm:ss [linux time]".
📌 Plotly renders a time series graph with scores.
📌 Hovering over a point displays the log message via tooltip.

📌 
"""