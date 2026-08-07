async function refreshDashboard() {

    try {

        // Fetch live system metrics
        const metricsResponse = await fetch("/metrics");
        const metrics = await metricsResponse.json();

        document.getElementById("cpu").innerText =
            metrics.cpu + "%";

        document.getElementById("memory").innerText =
            metrics.memory + "%";

        document.getElementById("disk").innerText =
            metrics.disk + "%";

        // Fetch Docker info
        const dockerResponse = await fetch("/docker");
        const docker = await dockerResponse.json();

        document.getElementById("containers").innerText =
            docker.running;

    } catch (err) {

        console.log(err);

    }

}

// Refresh every 5 seconds
setInterval(refreshDashboard, 5000);

// Run once immediately
refreshDashboard();