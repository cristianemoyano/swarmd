import logging
import yaml
from copy import deepcopy

logger = logging.getLogger(__name__)

class StackManager:
    def __init__(self, stack_file: str):
        self.stack_file = stack_file
        self.stack = None

    def load_stack(self):
        """Load the stack YAML file into memory."""
        logger.debug(f"Loading stack from {self.stack_file}")
        with open(self.stack_file, 'r') as f:
            self.stack = yaml.safe_load(f)

    def create_canary_service(self, base_service: str, canary_service: str, image: str, replicas: int):
        """
        Duplicate the base service as a canary service, changing the image and replicas.
        - base_service: name of the service to duplicate (e.g., 'myapp')
        - canary_service: name for the canary service (e.g., 'myapp_canary')
        - image: docker image/tag for the canary
        - replicas: number of replicas for the canary
        """
        if self.stack is None:
            raise RuntimeError("Stack not loaded. Call load_stack() first.")
        services = self.stack.get('services', {})
        if base_service not in services:
            raise ValueError(f"Base service '{base_service}' not found in stack.")
        canary_def = deepcopy(services[base_service])
        canary_def['image'] = image
        canary_def['deploy'] = canary_def.get('deploy', {})
        canary_def['deploy']['replicas'] = replicas
        services[canary_service] = canary_def
        self.stack['services'] = services

    def save_stack(self, output_file: str):
        """Save the modified stack to a new YAML file."""
        logger.debug(f"Saving stack to {output_file}")
        with open(output_file, 'w') as f:
            yaml.safe_dump(self.stack, f)

    def deploy_canary(self, canary_weight: int):
        """Deploy the stack with the specified canary weight."""
        logger.debug(f"Deploying stack with canary weight: {canary_weight}")

    def promote_canary(self):
        """Promote the canary deployment to stable."""
        pass

    def rollback(self):
        """Rollback the canary deployment."""
        pass

    def cleanup(self):
        """Clean up obsolete canary resources."""
        pass 