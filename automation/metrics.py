import json
import os
from datetime import datetime

METRICS_FILE = "metrics.json"

def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return []

    with open(METRICS_FILE, "r") as f:
        return json.load(f)

def save_metrics(data):
    with open(METRICS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def record_failure(pod_name, namespace, reason, analysis):
    data = load_metrics()

    entry = {
        "timestamp": str(datetime.now()),
        "pod": pod_name,
        "namespace": namespace,
        "reason": reason,
        "analysis": analysis
    }

    data.append(entry)
    save_metrics(data)

    print("📊 Failure recorded in metrics.json")

def count_recent_failures(pod_name, limit=3):
    data = load_metrics()

    base_name = pod_name.split('-')[0]

    filtered = [d for d in data if d["pod"].startswith(base_name)]

    return len(filtered[-limit:])