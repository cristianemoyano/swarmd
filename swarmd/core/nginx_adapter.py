import logging

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

def render_nginx_conf(
    stable_service: str,
    canary_service: str,
    stable_weight: int,
    canary_weight: int,
    output_path: str,
    template_dir: str = None
):
    """
    Render the nginx.conf.j2 template with the given weights and service names.
    """
    # Default to the templates directory in the package
    if template_dir is None:
        import os
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        template_dir = os.path.abspath(template_dir)
    logger.debug(f"Rendering Nginx configuration file from {template_dir}")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('nginx.conf.j2')
    rendered = template.render(
        stable_service=stable_service,
        canary_service=canary_service,
        stable_weight=stable_weight,
        canary_weight=canary_weight
    )
    logger.debug(f"Writing Nginx configuration file to {output_path}")
    with open(output_path, 'w') as f:
        f.write(rendered)
