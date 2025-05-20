import re
import pandas as pd

# Define severity and breadcrumb mappings
breadcrumb_map = {
    'ERROR': '🔴 Critical',
    'CRITICAL': '🔥 Failure',
}

# Regex to parse log lines
log_pattern = re.compile(
    r'^\[(?P<timestamp>[\d\-:\s,]+)\]\s(?P<level>\w+)\s+-\s+\[(?P<component>[^\]]+)\]\s(?P<message>.*)$'
)

def extract_critical_breadcrumbs(filepath):
    critical_trail = []

    with open(filepath, 'r') as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()
                level = data['level']
                if level in breadcrumb_map:
                    critical_trail.append({
                        "Timestamp": data["timestamp"],
                        "Component": data["component"],
                        "Message": data["message"],
                        "Breadcrumb": breadcrumb_map[level]
                    })

    return pd.DataFrame(critical_trail)

# Example usage
df_critical = extract_critical_breadcrumbs("system_trace.log")
print(df_critical.to_string(index=False))

"""
              Timestamp       Component                                                        Message Breadcrumb
2010-04-24 07:51:56,220  CircuitBreaker      Threshold crossed on 5 symbols, circuit-breakers passive. 🔴 Critical
2010-04-24 07:51:58,120  MarketDataFeed            Price for MSFT = 0.01 (check failed sanity bounds). 🔴 Critical
2010-04-24 07:51:59,000 ExchangeGateway     Trade confirmations delayed >1s, dropping client sessions.  🔥 Failure
2010-04-24 07:51:59,005  AlertingSystem Dispatching high-priority alert: “Market instability cascade”.  🔥 Failure
"""