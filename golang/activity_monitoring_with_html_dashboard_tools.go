package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strings"
	"time"

	"github.com/brianvoe/gofakeit/v6"
)

type Record struct {
	Timestamp string    `json:"Timestamp"`
	Datetime  time.Time `json:"datetime"`
	Log       string    `json:"log"`
	Score     float64   `json:"score"`
	Reference string    `json:"reference"`
	Tags      []string  `json:"tags"`
}

func main() {
	gofakeit.Seed(0)
	startTime := time.Now().Add(-10 * 24 * time.Hour)

	var data []Record
	for i := 0; i < 100; i++ {
		offset := rand.Intn(14400)
		t := startTime.Add(time.Duration(offset) * time.Minute)
		unix := t.Unix()
		timestampStr := fmt.Sprintf("%s [%d]", t.Format("2006-01-02_1504:05"), unix)

		numTags := rand.Intn(3) + 1
		tags := make([]string, numTags)
		for j := range tags {
			tags[j] = gofakeit.Word()
		}

		data = append(data, Record{
			Timestamp: timestampStr,
			Datetime:  t,
			Log:       gofakeit.Sentence(10),
			Score:     float64(int(gofakeit.Float64Range(0, 100)*100)) / 100,
			Reference: gofakeit.UUID(),
			Tags:      tags,
		})
	}

	// ✅ Add this before writing files
	sort.Slice(data, func(i, j int) bool {
		return data[i].Datetime.Before(data[j].Datetime)
	})

	// Write CSV
	writeCSV(data)

	// Marshal JSON for embedding in HTML
	jsonBytes, _ := json.Marshal(data)
	jsonStr := string(jsonBytes)

	// Write HTML file with embedded JSON
	writeHTML(jsonStr)

	fmt.Println("Files written: score_data.csv and index.html")
}

func writeCSV(data []Record) {
	file, _ := os.Create("score_data.csv")
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()

	headers := []string{"Timestamp", "datetime", "log", "score", "reference", "tags"}
	w.Write(headers)

	for _, r := range data {
		row := []string{
			r.Timestamp,
			r.Datetime.Format(time.RFC3339),
			r.Log,
			fmt.Sprintf("%.2f", r.Score),
			r.Reference,
			strings.Join(r.Tags, ";"),
		}
		w.Write(row)
	}
}

func writeHTML(jsonData string) {
	html := fmt.Sprintf(`<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Score Time Series</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial; margin: 40px; }
        #controls { margin-bottom: 20px; }
        #logViewer { border: 1px solid #ccc; padding: 10px; margin-top: 20px; }
        label { font-weight: bold; }
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
    const data = %s;

    const uniqueTags = new Set();
    data.forEach(d => d.tags.forEach(t => uniqueTags.add(t)));

    const tagFilter = document.getElementById("tagFilter");
    [...uniqueTags].sort().forEach(tag => {
        const opt = document.createElement("option");
        opt.value = tag;
        opt.textContent = tag;
        tagFilter.appendChild(opt);
    });

    function drawChart(filtered) {
        const trace = {
            x: filtered.map(d => d.datetime),
            y: filtered.map(d => d.score),
            mode: "markers+lines",
            type: "scatter",
            text: filtered.map(d => d.Timestamp),
            customdata: filtered.map(d => [d.log, d.tags.join(", ")]),
            hovertemplate: "<b>%{text}</b><br>Score: %{y}<br>Tags: %{customdata[1]}<extra></extra>"
        };

        const layout = {
            title: "Score Time Series",
            xaxis: { title: "Time" },
            yaxis: { title: "Score" },
            hovermode: "closest"
        };

        Plotly.newPlot("chart", [trace], layout);
    }

    drawChart(data);

    document.getElementById("chart").on("plotly_click", function(evt) {
        const point = evt.points[0];
        document.getElementById("logContent").innerText = point.customdata[0];
    });

    tagFilter.addEventListener("change", () => {
        const selected = Array.from(tagFilter.selectedOptions).map(opt => opt.value);
        const filtered = data.filter(d => selected.length === 0 || d.tags.some(t => selected.includes(t)));
        drawChart(filtered);
    });

    function downloadCSV() {
        const headers = Object.keys(data[0]);
        const csv = [headers.join(",")].concat(
            data.map(row => headers.map(h => JSON.stringify(row[h] || "")).join(","))
        ).join("\\n");

        const blob = new Blob([csv], {type: "text/csv"});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "score_data.csv";
        link.click();
    }
</script>

</body>
</html>`, jsonData)

	os.WriteFile("score_time_series_with_dashboard_tools.html", []byte(html), 0644)
}

/*
% go mod tidy
% go run main.go

📌 Faker creates random logs, timestamps, UUIDs, and tags.
📌 Timestamps are formatted as "YYYY-MM-DD_hhmm:ss [linux time]".
📌 Plotly renders a time series graph with scores.
📌 Hovering over a point displays the log message via tooltip.

📌📌 Create a file named score_time_series.html in the working directory. You can open it in any browser or share it as a self-contained interactive chart.
+ include a download button, tags filter, or log viewer section in the HTML.

*/
