from flask import Flask, render_template_string, request
import socket
from concurrent.futures import ThreadPoolExecutor
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "history.json"

services = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    135: "RPC",
    3306: "MySQL",
}

def get_service(port):
    return services.get(port, "Unknown")

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    history = history[:10]
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)

def scan_target(ip):
    open_ports = []

    def scan(port):
        s = socket.socket()
        s.settimeout(0.2)
        if s.connect_ex((ip, port)) == 0:
            open_ports.append(port)
        s.close()

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan, range(1, 1025))

    return open_ports

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cyber Scanner</title>
    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: #0b0f17;
            color: #e5e7eb;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
        }

        .container {
            background: #111827;
            padding: 25px;
            border-radius: 12px;
            width: 100%;
            max-width: 700px;
            border: 1px solid #1f2937;
        }

        input {
            width: 65%;
            padding: 10px;
            background: #0b0f17;
            border: 1px solid #374151;
            color: white;
            border-radius: 8px;
        }

        button {
            padding: 10px 15px;
            background: #3b82f6;
            border: none;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }

        .card {
            background: #0b0f17;
            border: 1px solid #1f2937;
            padding: 10px;
            margin-top: 8px;
            border-radius: 8px;
        }

        .section {
            margin-top: 25px;
        }
    </style>
</head>

<body>

<h2>Network Security Scanner</h2>

<div class="container">

<form action="/scan">
    <input name="ip" placeholder="Enter IP">
    <button>Scan</button>
</form>

{% if result %}
<div class="section">
    <h3>Results</h3>
    {% for r in result %}
        <div class="card">{{ r }}</div>
    {% endfor %}

    <p>Security Score: {{ score }}/100</p>
</div>
{% endif %}

{% if history %}
<div class="section">
    <h3>History</h3>
    {% for h in history %}
        <div class="card">
            <b>{{ h["ip"] }}</b> - {{ h["time"] }}<br>
            Ports: {{ h["ports"] }}
        </div>
    {% endfor %}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, history=load_history())

@app.route("/scan")
def scan():
    ip = request.args.get("ip")

    ports = scan_target(ip)

    results = []
    score = 100

    for p in ports:
        service = get_service(p)
        results.append(f"{p} - {service}")

        if p in [21, 22, 3306]:
            score -= 20
        else:
            score -= 5

    if score < 0:
        score = 0

    save_history({
        "ip": ip,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ports": len(ports)
    })

    return render_template_string(HTML,
        result=results,
        score=score,
        history=load_history()
    )

if __name__ == "__main__":
    app.run(debug=True)