class Node:
    def _init_(self, id, cpu_cores, container_id, status, created_at, last_heartbeat):
        self.id = id
        self.cpu_cores = cpu_cores
        self.container_id = container_id
        self.status = status
        self.created_at = created_at
        self.last_heartbeat = last_heartbeat
        self.pods = []  # List to store pod IDs (will be used in week 2)
        
    def to_dict(self):
        """Convert node to dictionary for API responses"""
        return {
            "id": self.id,
            "cpu_cores": self.cpu_cores,
            "status": self.status,
            "created_at": self.created_at,
            "last_heartbeat": self.last_heartbeat,
            "pods_count": len(self.pods)
        }
