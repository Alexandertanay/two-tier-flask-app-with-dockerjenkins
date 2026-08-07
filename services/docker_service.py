import docker


def get_docker_info():
    """
    Returns information about all running Docker containers.
    """

    try:
        client = docker.from_env()

        containers = client.containers.list()

        container_list = []

        for container in containers:

            # Fetch live stats
            stats = container.stats(stream=False)

            # -----------------------
            # CPU Usage
            # -----------------------
            cpu_percent = 0.0

            try:

                cpu_delta = (
                    stats["cpu_stats"]["cpu_usage"]["total_usage"]
                    - stats["precpu_stats"]["cpu_usage"]["total_usage"]
                )

                system_delta = (
                    stats["cpu_stats"]["system_cpu_usage"]
                    - stats["precpu_stats"]["system_cpu_usage"]
                )

                cpu_count = len(
                    stats["cpu_stats"]["cpu_usage"].get(
                        "percpu_usage", []
                    )
                )

                if system_delta > 0 and cpu_delta > 0:

                    cpu_percent = (
                        cpu_delta / system_delta
                    ) * cpu_count * 100

            except Exception:
                cpu_percent = 0.0

            # -----------------------
            # Memory Usage
            # -----------------------

            memory_usage = (
                stats["memory_stats"]["usage"] / (1024 * 1024)
            )

            memory_limit = (
                stats["memory_stats"]["limit"] / (1024 * 1024)
            )

            memory_percent = (
                (memory_usage / memory_limit) * 100
                if memory_limit
                else 0
            )

            # -----------------------
            # Ports
            # -----------------------

            ports = []

            port_info = container.attrs["NetworkSettings"]["Ports"]

            if port_info:

                for container_port, host in port_info.items():

                    if host:

                        ports.append(
                            f"{host[0]['HostPort']} → {container_port}"
                        )

            # -----------------------
            # Build object
            # -----------------------

            container_list.append(

                {

                    "id": container.short_id,

                    "name": container.name,

                    "image": (
                        container.image.tags[0]
                        if container.image.tags
                        else "Unknown"
                    ),

                    "status": container.status,

                    "cpu": round(cpu_percent, 2),

                    "memory": round(memory_usage, 2),

                    "memory_percent": round(
                        memory_percent,
                        2
                    ),

                    "ports": (
                        ", ".join(ports)
                        if ports
                        else "-"
                    ),

                }

            )

        return {

            "running": len(containers),

            "containers": container_list,

        }

    except Exception as e:

        print("Docker Error:", e)

        return {

            "running": 0,

            "containers": []

        }


def get_container_logs(container_name, lines=100):
    """
    Returns logs for a given container.
    """

    try:

        client = docker.from_env()

        container = client.containers.get(container_name)

        logs = container.logs(
            tail=lines,
            timestamps=True
        ).decode("utf-8")

        return logs

    except Exception as e:

        return str(e)


def restart_container(container_name):
    """
    Restart a Docker container.
    """

    try:

        client = docker.from_env()

        container = client.containers.get(container_name)

        container.restart()

        return True

    except Exception:

        return False


def stop_container(container_name):
    """
    Stop a Docker container.
    """

    try:

        client = docker.from_env()

        container = client.containers.get(container_name)

        container.stop()

        return True

    except Exception:

        return False


def start_container(container_name):
    """
    Start a Docker container.
    """

    try:

        client = docker.from_env()

        container = client.containers.get(container_name)

        container.start()

        return True

    except Exception:

        return False