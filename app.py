from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

servers = {
    "1": {"name": "srv-harare-01", "status": "healthy", "dr_role": "primary", "last_seen": "2026-07-21T10:00:00Z"},
    "2": {"name": "srv-bulawayo-01", "status": "healthy", "dr_role": "standby", "last_seen": "2026-07-21T09:58:00Z"},
    "3": {"name": "srv-harare-02", "status": "degraded", "dr_role": "primary", "last_seen": "2026-07-21T09:45:00Z"},
}

@app.route('/servers')
def get_servers():
    return jsonify(servers)

@app.route('/servers/<server_id>')
def get_server(server_id):
    server = servers.get(server_id)
    if server is None:
        return jsonify({"error": "server not found"}), 404
    return jsonify(server)

@app.route('/servers/<server_id>/heartbeat', methods=['POST'])
def heartbeat(server_id):
    server = servers.get(server_id)
    if server is None:
        return jsonify({"error": "server not found"}), 404
    server["last_seen"] = datetime.now(timezone.utc).isoformat()
    return jsonify(server)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/metrics')
def metrics():
    healthy_count = sum(1 for s in servers.values() if s["status"] == "healthy")
    lines = [
        "# HELP infra_servers_total Total number of servers tracked",
        "# TYPE infra_servers_total gauge",
        f"infra_servers_total {len(servers)}",
        "# HELP infra_servers_healthy Number of healthy servers",
        "# TYPE infra_servers_healthy gauge",
        f"infra_servers_healthy {healthy_count}",
    ]
    return "\n".join(lines), 200, {"Content-Type": "text/plain"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
