from pathlib import Path
from typing import Annotated

from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from url_instax.config import get_config
from url_instax.main import ScreenshotError, take_screenshot
from url_instax.routers.api.v1.screenshot import ScreenshotParams

app = FastMCP("url_instax")
config = get_config()

if config.api_base_url:
    client = AsyncClient(
        base_url=config.api_base_url,
        headers=({"Authorization": f"Bearer {config.api_token}"} if config.api_token else {}),
    )
else:
    client = None


@app.tool("screenshot", description="Take a screenshot of a URL. e.g. https://example.com")
async def screenshot(
    url: Annotated[str, Field(description="URL to take a screenshot of")],
    is_mobile: Annotated[
        bool,
        Field(
            description="Whether to use mobile emulation",
            default=False,
        ),
    ] = False,
    timeout: Annotated[
        float,
        Field(
            description="Timeout in seconds",
            default=30,
        ),
    ] = 30.0,
    full_page: Annotated[
        bool,
        Field(
            description="Whether to take a full page screenshot",
            default=True,
        ),
    ] = True,
    save_path: Annotated[
        str,
        Field(
            description="Path to save the screenshot to",
            default="screenshot.png",
        ),
    ] = "screenshot.png",
) -> dict[str, str]:
    save_path: Path = Path(save_path).expanduser().resolve()
    save_path.parent.mkdir(parents=True, exist_ok=True)

    if client:
        response = await client.post(
            "/api/v1/screenshot",
            json=ScreenshotParams(
                url=url,
                is_mobile=is_mobile,
                timeout=timeout,
                full_page=full_page,
            ).model_dump(),
        )
        if response.status_code != 200:
            return {
                "message": "Failed to take screenshot",
                "error": response.text,
            }
        data = response.content

    else:
        try:
            data = await take_screenshot(
                url=url,
                is_mobile=is_mobile,
                timeout=timeout,
                full_page=full_page,
            )
        except ScreenshotError as e:
            return {
                "message": "Failed to take screenshot",
                "error": str(e),
            }
        except Exception as e:
            return {
                "message": "Unexpected error",
                "error": str(e),
            }

    with open(save_path, "wb") as f:
        f.write(data)
    return {"message": "Screenshot saved", "path": save_path.as_posix()}
