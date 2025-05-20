import re
import pandas as pd
from datetime import datetime

# Sample log lines in the new format
log_lines = [
    "[2010-04-24 07:51:54,401] INFO - [main] OrderEngine: Received market sell order for 75,000 ES futures contracts",
    "[2010-04-24 07:51:54,405] DEBUG - [main] RiskManager: Order within risk limits, skipping throttle",
    "[2010-04-24 07:51:54,408] INFO - [main] AlgoTrader: Executing strategy: VWAP, 100% rate, ignore price/time",
    "[2010-04-24 07:51:55,120] WARN - [main] OrderBook: Liquidity < 10% of 30-day average in ES_F",
    "[2010-04-24 07:51:55,131] DEBUG - [main] HFTModule: Increased trade rate to exploit price volatility",
    "[2010-04-24 07:51:55,212] WARN - [main] OrderBook: Bid-ask spread widens to abnormal range: 5x normal",
    "[2010-04-24 07:51:55,900] INFO - [main] AlgoTrader: 22% of parent order executed, remaining: 58,500 contracts",
    "[2010-04-24 07:51:56,001] WARN - [main] LatencyMonitor: Spike detected in order response time (avg 250ms > baseline 70ms)",
    "[2010-04-24 07:51:56,220] ERROR - [main] CircuitBreaker: Threshold crossed on 5 symbols, circuit-breaker not triggered (mode: passive)",
    "[2010-04-24 07:51:57,013] DEBUG - [main] RiskManager: Real-time VaR increased by 350% in last 4s",
    "[2010-04-24 07:51:58,120] ERROR - [main] MarketDataFeed: Price for MSFT = 0.01 (check failed sanity bounds)",
    "[2010-04-24 07:51:58,122] INFO - [main] FallbackEngine: Switching to backup data feed due to anomaly",
    "[2010-04-24 07:51:59,000] FATAL - [main] ExchangeGateway: Trade confirmations delayed >1s, dropping client sessions",
    "[2010-04-24 07:51:59,005] INFO - [main] AlertingSystem: Dispatching high-priority alert: “Market instability detected: auto-sell avalanche”"
]

# Regex pattern to parse each log line
log_pattern = re.compile(r'\[(.*?)\] (\w+) - \[.*?\] (\w+): (.*)')

# Parsed logs
parsed_logs = []

for line in log_lines:
    match = log_pattern.match(line)
    if match:
        timestamp_str, severity, component, message = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
        parsed_logs.append((timestamp, component, message, severity))

# Create DataFrame
df_logs = pd.DataFrame(parsed_logs, columns=["Timestamp", "Component", "Message", "Severity"])
df_logs = df_logs.sort_values("Timestamp")

# Assign breadcrumb types
def assign_breadcrumb(row):
    msg = row["Message"].lower()
    if "sell order" in msg:
        return "🔴 Trigger"
    elif "vwap" in msg or "100%" in msg:
        return "🟠 Risk Bypass"
    elif "liquidity" in msg or "bid-ask" in msg:
        return "🟡 Market Stress"
    elif "latency" in msg:
        return "🟠 Platform Stress"
    elif "circuit-breaker" in msg:
        return "🔴 Control Failure"
    elif "var" in msg:
        return "🟡 Risk Acceleration"
    elif "msft = 0.01" in msg or "sanity bounds" in msg:
        return "🔴 Data Anomaly"
    elif "dropping client sessions" in msg:
        return "🔥 Final Failure"
    elif "alert" in msg:
        return "📣 Alerting"
    else:
        return "ℹ️ Info"

df_logs["Breadcrumb"] = df_logs.apply(assign_breadcrumb, axis=1)
df_logs.reset_index(drop=True, inplace=True)
df_logs[["Timestamp", "Component", "Message", "Breadcrumb"]]

"""
Timestamp   Component   Message Breadcrumb
0   2010-04-24 07:51:54.401 OrderEngine Received market sell order for 75,000 ES futur...   🔴 Trigger
1   2010-04-24 07:51:54.405 RiskManager Order within risk limits, skipping throttle ℹ️ Info
2   2010-04-24 07:51:54.408 AlgoTrader  Executing strategy: VWAP, 100% rate, ignore pr...   🟠 Risk Bypass
3   2010-04-24 07:51:55.120 OrderBook   Liquidity < 10% of 30-day average in ES_F   🟡 Market Stress
4   2010-04-24 07:51:55.131 HFTModule   Increased trade rate to exploit price volatility    ℹ️ Info
5   2010-04-24 07:51:55.212 OrderBook   Bid-ask spread widens to abnormal range: 5x no...   🟡 Market Stress
6   2010-04-24 07:51:55.900 AlgoTrader  22% of parent order executed, remaining: 58,50...   ℹ️ Info
7   2010-04-24 07:51:56.001 LatencyMonitor  Spike detected in order response time (avg 250...   ℹ️ Info
8   2010-04-24 07:51:56.220 CircuitBreaker  Threshold crossed on 5 symbols, circuit-breake...   🔴 Control Failure
9   2010-04-24 07:51:57.013 RiskManager Real-time VaR increased by 350% in last 4s  🟡 Risk Acceleration
10  2010-04-24 07:51:58.120 MarketDataFeed  Price for MSFT = 0.01 (check failed sanity bou...   🔴 Data Anomaly
11  2010-04-24 07:51:58.122 FallbackEngine  Switching to backup data feed due to anomaly    ℹ️ Info
12  2010-04-24 07:51:59.000 ExchangeGateway Trade confirmations delayed >1s, dropping clie...   🔥 Final Failure
13  2010-04-24 07:51:59.005 AlertingSystem  Dispatching high-priority alert: “Market insta...   📣 Alerting

"""