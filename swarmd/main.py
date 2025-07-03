import logging

import typer

from swarmd.commands.deploy import deploy
from swarmd.commands.promote import promote
from swarmd.commands.rollback import rollback
from swarmd.commands.status import status
from swarmd.commands.cleanup import cleanup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = typer.Typer(help="CLI for progressive (canary) deployments in Docker Swarm using Nginx.")

app.command()(deploy)
app.command()(promote)
app.command()(rollback)
app.command()(status)
app.command()(cleanup)

if __name__ == "__main__":
    app() 