import argparse
import requests
import json

API_SERVER_URL = "http://localhost:5000"

def list_nodes():
    """List all nodes in the cluster"""
    response = requests.get(f"{API_SERVER_URL}/api/nodes")
    if response.status_code == 200:
        nodes = response.json().get("nodes", [])
        if not nodes:
            print("No nodes found in the cluster.")
            return
        
        print("Nodes in the cluster:")
        print("-" * 80)
        print(f"{'ID':<36} | {'CPU Cores':<9} | {'Status':<10} | {'Pods':<5}")
        print("-" * 80)
        
        for node in nodes:
            print(f"{node['id']:<36} | {node['cpu_cores']:<9} | {node['status']:<10} | {node['pods_count']:<5}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def add_node(cpu_cores):
    """Add a new node to the cluster"""
    response = requests.post(
        f"{API_SERVER_URL}/api/nodes",
        json={"cpu_cores": cpu_cores}
    )
    
    if response.status_code == 201:
        data = response.json()
        print(f"Node added successfully with ID: {data['node_id']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Kubernetes Simulator CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List nodes command
    list_parser = subparsers.add_parser("list-nodes", help="List all nodes in the cluster")
    
    # Add node command
    add_parser = subparsers.add_parser("add-node", help="Add a new node to the cluster")
    add_parser.add_argument("--cpu", type=int, required=True, help="Number of CPU cores for the node")
    
    args = parser.parse_args()
    
    if args.command == "list-nodes":
        list_nodes()
    elif args.command == "add-node":
        add_node(args.cpu)
    else:
        parser.print_help()

if _name_ == "_main_":
    main()
