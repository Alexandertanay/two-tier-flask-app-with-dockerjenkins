


from flask import Flask, render_template, jsonify, redirect

from services.system_service import get_system_metrics
from services.docker_service import get_docker_info
from services.health_service import get_health

app = Flask(__name__)


@app.route("/")
def dashboard():
    """
    Main Dashboard
    """
    try:
        metrics = get_system_metrics()
        docker = get_docker_info()
        health = get_health()

        return render_template(
            "index.html",
            metrics=metrics,
            docker=docker,
            health=health
        )

    except Exception as e:
        return f"""
        <h2>NimbusOps Error</h2>
        <p>{str(e)}</p>
        """, 500


@app.route("/health")
def health_check():
    """
    Health Check Endpoint
    """
    return jsonify({
        "status": "UP",
        "application": "NimbusOps"
    }), 200


@app.route("/metrics")
def metrics():
    """
    Live System Metrics API
    """
    try:
        return jsonify(get_system_metrics())

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


from services.docker_service import (
    restart_container,
    stop_container,
    start_container
)

@app.route("/restart/<container_name>")
def restart(container_name):
    restart_container(container_name)
    return redirect("/")

@app.route("/stop/<container_name>")
def stop(container_name):
    stop_container(container_name)
    return redirect("/")

@app.route("/start/<container_name>")
def start(container_name):
    start_container(container_name)
    return redirect("/")

@app.route("/docker")
def docker():
    """
    Docker Information API
    """
    try:
        return jsonify(get_docker_info())

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


@app.route("/status")
def status():
    """
    Combined System Status
    """
    try:
        return jsonify({
            "health": get_health(),
            "metrics": get_system_metrics(),
            "docker": get_docker_info()
        })

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )