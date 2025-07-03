import logging
import os

import typer

from swarmd.core.stack_manager import StackManager
from swarmd.core.nginx_adapter import render_nginx_conf

logger = logging.getLogger(__name__)

OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def deploy(
    service_name: str = typer.Option(..., "--service-name", "-n", help="Logical name for the stack"),
    stack_file: str = typer.Argument(..., help="Path to the stack.yml file"),
    version: str = typer.Option(..., "--version", "-v", help="Version or tag to deploy"),
    env: str = typer.Option(..., "--env", "-e", help="Target environment (e.g., staging, production)"),
    canary_weight: int = typer.Option(1, help="Traffic percentage for the canary"),
    canary_replicas: int = typer.Option(1, help="Number of replicas for the canary service")
):
    """Deploy the stack with the initial canary configuration, specifying version, environment, stack name, canary weight, and canary replicas."""
    if canary_weight > 20 and canary_replicas == 1:
        typer.secho("[WARNING] You are assigning more than 20% of the traffic to a single canary replica. Consider increasing --canary-replicas.", fg=typer.colors.YELLOW)

    # 1. Load the stack
    manager = StackManager(stack_file)
    manager.load_stack()

    # 2. Create the canary service (e.g., base: 'myapp', canary: 'myapp_canary')
    base_service = service_name
    canary_service = f"{base_service}_canary"
    manager.create_canary_service(
        base_service=base_service,
        canary_service=canary_service,
        image=version,
        replicas=canary_replicas
    )

    # 3. Save to a temporary stack file
    tmp_stack_path = os.path.join(OUTPUT_DIR, f"{env}_{service_name}.yml")
    manager.save_stack(tmp_stack_path)

    # 4. Render the Nginx configuration file
    nginx_conf_path = os.path.join(OUTPUT_DIR, "nginx.conf")
    render_nginx_conf(
        stable_service=base_service,
        canary_service=canary_service,
        stable_weight=100 - canary_weight,
        canary_weight=canary_weight,
        output_path=nginx_conf_path
    )

    # 5. Deploy the canary service
    manager.deploy_canary(canary_weight)

    typer.echo(f"Deployed stack: {stack_file} | version: {version} | env: {env} | service_name: {service_name} | canary_weight: {canary_weight}% | canary_replicas: {canary_replicas}")
