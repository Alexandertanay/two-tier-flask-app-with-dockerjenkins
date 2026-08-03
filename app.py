from flask import Flask, render_template
from db import connection, cursor
import socket
from datetime import datetime

app = Flask(__name__)

APP_VERSION = "v1.0.0"


@app.route("/")
def home():
    # Check database status
    try:
        cursor.execute("SELECT 1")
        db_status = "Connected"
    except Exception:
        db_status = "Disconnected"

    return render_template(
        "index.html",
        app_status="Running",
        db_status=db_status,
        docker_status="Running",
        environment="AWS EC2",
        cicd="Jenkins",
        registry="Docker Hub",
        version=APP_VERSION,
        hostname=socket.gethostname(),
        current_time=datetime.now().strftime("%d %b %Y %I:%M:%S %p"),
    )


@app.route("/health")
def health():
    return {"status": "UP"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)