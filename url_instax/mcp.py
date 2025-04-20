from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP

from url_instax.config import get_config

app = FastMCP("url_instax")
config = get_config()
client = AsyncClient(
    base_url=config.api_base_url,
    headers={"Authorization": f"Bearer {config.api_token}"} if config.api_token else {},
)
