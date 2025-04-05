from flask import Flask, Response
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")

if not URL:
    raise ValueError("The URL environment variable is not set. Please edit app/.env")

app = Flask(__name__)
uptime_tracker = {}

@app.route('/metrics')
def metrics():
    response = requests.get(URL)
    data = response.json()

    metrics = []
    metrics.append(f'biconomy_version{{version="{data["version"]}"}} 1')
    metrics.append(f'biconomy_node_info{{node="{data["node"]}", beneficiary="{data["beneficiary"]}"}} 1')
    metrics.append(f'biconomy_gas_premium_percentage {data["gas_premium_percentage"]}')

    current_time = int(time.time())

    for chain in data["supported_chains"]:
        chain_id = chain["chainId"]
        name = chain["name"]
        health = chain["healthCheck"]

        status = "HEALTHY" if health["status"] == "healthy" else "UNHEALTHY"
        balance = int(health["nativeBalance"]) / 1e18
        rpc_operational = ("true" if health["rpcOperational"] else "false").upper()
        debug_trace_call_supported = ("true" if health["debugTraceCallSupported"] else "false").upper()

        chain_key = f"{chain_id}-{name}"

        if status == "HEALTHY":
            if chain_key not in uptime_tracker:
                uptime_tracker[chain_key] = current_time
            uptime_seconds = current_time - uptime_tracker[chain_key]
        else:
            uptime_tracker.pop(chain_key, None)
            uptime_seconds = 0

        metrics.append(
            f'biconomy_chain_info{{time="{current_time}", ChainId="{chain_id}", Name="{name}", Balance="{balance}", Debug="{debug_trace_call_supported}", Rpc="{rpc_operational}", Status="{status}"}} 1'
        )
        metrics.append(
            f'biconomy_chain_uptime_seconds{{ChainId="{chain_id}", Name="{name}"}} {uptime_seconds}'
        )

    return Response("\n".join(metrics), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7500)
