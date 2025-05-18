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
        "datetime": time,
        "log": fake.sentence(),
        "score": round(random.uniform(0, 100), 2),
        "reference": fake.uuid4(),
        "tags": [fake.word() for _ in range(random.randint(1, 3))]
    })

df = pd.DataFrame(data)
df = df.sort_values(by="datetime")

# Preprocess tags for filter UI
df["tag_str"] = df["tags"].apply(lambda x: ", ".join(x))

# Create the figure
fig = px.scatter(
    df,
    x="datetime",
    y="score",
    hover_data={
        "log": False,
        "Timestamp": True,
        "score": True,
        "datetime": False,
        "tag_str": True
    },
    title="Score Time Series with Logs and Timestamps",
    labels={"datetime": "Time", "score": "Score"}
)

fig.update_traces(mode="markers+lines")
fig.update_layout(
    hovermode="closest",
    plot_bgcolor="white",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

# HTML Output with interactive UI
custom_html = f"""
<html>
<head>
    <title>Score Time Series</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        #controls {{ margin-bottom: 20px; }}
        #logViewer {{ border: 1px solid #ccc; padding: 10px; margin-top: 20px; }}
        label {{ font-weight: bold; }}
    </style>
</head>
<body>

<h2>Score Time Series with Logs and Filters</h2>

<div id="controls">
    <label for="tagFilter">Filter by Tags:</label>
    <select id="tagFilter" multiple style="width:300px;height:100px;"></select>
    <button onclick="downloadCSV()">Download CSV</button>
</div>

<div id="chart"></div>

<div id="logViewer">
    <h3>Log Viewer</h3>
    <p id="logContent">Click on a point to view the log message.</p>
</div>

<script>
    const data = {df.to_json(orient="records", date_format="iso")};

    // Extract unique tags
    const uniqueTags = new Set();
    data.forEach(d => d.tags.forEach(t => uniqueTags.add(t)));

    // Populate tag filter
    const tagFilter = document.getElementById("tagFilter");
    [...uniqueTags].sort().forEach(tag => {{
        const opt = document.createElement("option");
        opt.value = tag;
        opt.textContent = tag;
        tagFilter.appendChild(opt);
    }});

    // Draw plot
    const trace = {{
        x: data.map(d => d.datetime),
        y: data.map(d => d.score),
        mode: "markers+lines",
        type: "scatter",
        text: data.map(d => d.Timestamp),
        customdata: data.map(d => [d.log, d.tags.join(", ")]),
        hovertemplate: "<b>%{{text}}</b><br>Score: %{{y}}<br>Tags: %{{customdata[1]}}<extra></extra>"
    }};

    const layout = {{
        title: "Score Time Series",
        xaxis: {{ title: "Time" }},
        yaxis: {{ title: "Score" }},
        hovermode: "closest"
    }};

    Plotly.newPlot("chart", [trace], layout);

    // Add log viewer interaction
    document.getElementById("chart").on("plotly_click", function(data) {{
        const point = data.points[0];
        const log = point.customdata[0];
        document.getElementById("logContent").innerText = log;
    }});

    // Add tag filter functionality
    tagFilter.addEventListener("change", () => {{
        const selected = Array.from(tagFilter.selectedOptions).map(opt => opt.value);
        const filtered = data.filter(d => selected.length === 0 || d.tags.some(t => selected.includes(t)));

        Plotly.react("chart", [{{
            x: filtered.map(d => d.datetime),
            y: filtered.map(d => d.score),
            mode: "markers+lines",
            type: "scatter",
            text: filtered.map(d => d.Timestamp),
            customdata: filtered.map(d => [d.log, d.tags.join(", ")]),
            hovertemplate: "<b>%{{text}}</b><br>Score: %{{y}}<br>Tags: %{{customdata[1]}}<extra></extra>"
        }}], layout);
    }});

    // Add download CSV functionality
    function downloadCSV() {{
        const headers = Object.keys(data[0]);
        const csv = [headers.join(",")].concat(
            data.map(row => headers.map(h => JSON.stringify(row[h] || "")).join(","))
        ).join("\\n");

        const blob = new Blob([csv], {{type: "text/csv"}});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "score_data.csv";
        link.click();
    }}
</script>

</body>
</html>
"""

# Save custom HTML with interactivity
with open("score_time_series_with_dashboard_tools.html", "w", encoding="utf-8") as f:
    f.write(custom_html)

print("✅ Enhanced HTML exported to score_time_series.html with tag filter, log viewer, and download button.")

"""
📌 Faker creates random logs, timestamps, UUIDs, and tags.
📌 Timestamps are formatted as "YYYY-MM-DD_hhmm:ss [linux time]".
📌 Plotly renders a time series graph with scores.
📌 Hovering over a point displays the log message via tooltip.

📌📌 Create a file named score_time_series.html in the working directory. You can open it in any browser or share it as a self-contained interactive chart.
+ include a download button, tags filter, or log viewer section in the HTML.
"""
