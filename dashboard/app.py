from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_FILE = os.path.join(BASE_DIR, "../automation/metrics.json")

def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return []

    try:
        with open(METRICS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/metrics")
def get_metrics():
    data = load_metrics()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)