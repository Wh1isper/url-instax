import asyncio
from functools import wraps

import click
import uvicorn

from .mcp import app as mcp_app
from .web_app import app as web_app


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option("--host", type=click.STRING, default="0.0.0.0")  # noqa: S104
@click.option("--port", type=click.INT, default=8890)
def http(host, port):
    """
    Start the server.
    """
    uvicorn.run(web_app, host=host, port=port, timeout_graceful_shutdown=60)


@click.command()
def mcp():
    """
    Start mcp server in stdio mode.

    Allows LLM use this package as a tool or access http server with mcp protocol.
    """
    mcp_app.run(transport="stdio")


@click.group()
def cli():
    pass


cli.add_command(http)
cli.add_command(mcp)
