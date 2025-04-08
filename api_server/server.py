from flask import Flask, request, jsonify
from api_server.node_manager import NodeManager

app = Flask(_name_)
node_manager = NodeManager()

@app.route('/api/nodes', methods=['GET'])
def list_nodes():
    nodes = node_manager.get_all_nodes()
    return jsonify({"nodes": nodes})

@app.route('/api/nodes', methods=['POST'])
def add_node():
    data = request.get_json()
    if not data or 'cpu_cores' not in data:
        return jsonify({"error": "CPU cores must be specified"}), 400
    
    # Validate CPU cores
    cpu_cores = data['cpu_cores']
    if not isinstance(cpu_cores, int) or cpu_cores <= 0:
        return jsonify({"error": "CPU cores must be a positive integer"}), 400
    
    # Create the node
    node_id = node_manager.add_node(cpu_cores)
    return jsonify({"node_id": node_id, "message": "Node added successfully"}), 201

@app.route('/api/heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.get_json()
    if not data or 'node_id' not in data:
        return jsonify({"error": "Node ID must be specified"}), 400
    
    node_manager.update_node_status(data['node_id'], data.get('status', {}))
    return jsonify({"status": "Heartbeat received"})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)
