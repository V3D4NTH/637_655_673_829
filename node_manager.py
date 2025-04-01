import uuid
import time
from api_server.models import Node
from utils.docker_manager import DockerManager

class NodeManager:
    def _init_(self):
        self.nodes = {}  # Dictionary mapping node IDs to Node objects
        self.docker_manager = DockerManager()
    
    def add_node(self, cpu_cores):
        """
        Add a new node to the cluster with specified CPU cores
        Returns the new node's ID
        """
        # Generate a unique ID for the node
        node_id = str(uuid.uuid4())
        
        # Create a container for the node
        container_id = self.docker_manager.create_node_container(node_id, cpu_cores)
        
        # Create and store the node object
        node = Node(
            id=node_id,
            cpu_cores=cpu_cores,
            container_id=container_id,
            status="Creating",
            created_at=time.time(),
            last_heartbeat=None
        )
        
        self.nodes[node_id] = node
        
        # Start the container
        self.docker_manager.start_container(container_id)
        
        # Update node status
        node.status = "Ready"
        
        return node_id
    
    def get_all_nodes(self):
        """Return all registered nodes"""
        return [node.to_dict() for node in self.nodes.values()]
    
    def get_node(self, node_id):
        """Get a specific node by ID"""
        return self.nodes.get(node_id)
    
    def update_node_status(self, node_id, status_data):
        """Update node status based on heartbeat data"""
        node = self.nodes.get(node_id)
        if node:
            node.last_heartbeat = time.time()
            node.status = "Ready"  # We'll expand this in week 2
            return True
        return False
