import os
import time
import requests
import json

# Get environment variables
NODE_ID = os.environ.get("NODE_ID")
CPU_CORES = int(os.environ.get("CPU_CORES", 1))
API_SERVER_URL = os.environ.get("API_SERVER_URL")

def send_heartbeat():
    """Send a heartbeat signal to the API server"""
    try:
        response = requests.post(
            f"{API_SERVER_URL}/api/heartbeat",
            json={
                "node_id": NODE_ID,
                "status": {
                    "cpu_cores": CPU_CORES,
                    "timestamp": time.time()
                }
            },
            timeout=5
        )
        print(f"Heartbeat sent. Response: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending heartbeat: {e}")
        return False

def main():
    print(f"Node {NODE_ID} starting with {CPU_CORES} CPU cores")
    
    # Send initial heartbeat
    send_heartbeat()
    
    # Send heartbeats every 10 seconds
    while True:
        time.sleep(10)
        send_heartbeat()

if _name_ == "_main_":
    main()
