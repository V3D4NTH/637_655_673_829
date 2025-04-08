import docker

class DockerManager:
    def _init_(self):
        self.client = docker.from_env()
    
    def create_node_container(self, node_id, cpu_cores):
        """
        Create a Docker container to simulate a node
        
        Args:
            node_id: Unique identifier for the node
            cpu_cores: Number of CPU cores to allocate
            
        Returns:
            container_id: ID of the created container
        """
        # Build the node container if not already built
        self._build_node_image_if_needed()
        
        # Create the container with environment variables
        container = self.client.containers.create(
            image="kubernetes-simulator-node",
            name=f"node-{node_id}",
            environment={
                "NODE_ID": node_id,
                "CPU_CORES": str(cpu_cores),
                "API_SERVER_URL": "http://host.docker.internal:5000"
            },
            detach=True,
            cpu_count=cpu_cores  # Limit actual CPU resources to simulate constraints
        )
        
        return container.id
    
    def start_container(self, container_id):
        """Start a previously created container"""
        container = self.client.containers.get(container_id)
        container.start()
        return True
    
    def stop_container(self, container_id):
        """Stop a running container"""
        container = self.client.containers.get(container_id)
        container.stop()
        return True
    
    def _build_node_image_if_needed(self):
        """Build the node agent Docker image if it doesn't exist"""
        try:
            self.client.images.get("kubernetes-simulator-node")
        except docker.errors.ImageNotFound:
            # Build the image using the Dockerfile in the docker/node directory
            import os
            docker_path = os.path.join(os.path.dirname(_file_), "../docker/node")
            self.client.images.build(path=docker_path, tag="kubernetes-simulator-node")
