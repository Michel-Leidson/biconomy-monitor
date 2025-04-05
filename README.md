# Biconomy Monitor

This project monitors the health of your Biconomy Operator endpoint and optionally sends alerts to a Discord channel via webhook.

## 🔧 Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/Michel-Leidson/biconomy-monitor.git
cd biconomy-monitor
```

Navigate to the app edit the .env file
```bash
cd app
# nano .env
URL=https://your-operator-url.com
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your-webhook-url
```

Build and run the project with Docker Compose
```bash
docker compose up --build -d
```

Access the metrics at
- Metrics: http://localhost:7500/metrics
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Access Pre-Configured Dashboards

![image](https://github.com/user-attachments/assets/5e66a8d3-2c2c-4065-80ab-2fc8cadda541)

