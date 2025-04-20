from fastapi import APIRouter, Query, Response, status
from pydantic import BaseModel

from url_instax.log import logger
from url_instax.main import ScreenshotError, take_screenshot

router = APIRouter(
    tags=["Component"],
    prefix="/api/v1",
)


def response_image(
    image: bytes,
) -> Response:
    return Response(
        content=image,
        media_type="image/png",
        headers={
            "Content-Disposition": "inline; filename=screenshot.png",
        },
    )


def response_error(exception: ScreenshotError) -> Response:
    return Response(
        content=str(exception),
        media_type="text/plain",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.get("/screenshot")
async def screenshot_get(
    url: str = Query(..., description="URL to take a screenshot of"),
    is_mobile: bool = Query(
        False,
        description="Whether to use mobile emulation",
    ),
    timeout: float = Query(
        30,
        description="Timeout in seconds",
    ),
    full_page: bool = Query(
        True,
        description="Whether to take a full page screenshot",
    ),
) -> Response:
    logger.debug(f"Taking screenshot of {url}")
    return response_image(
        await take_screenshot(
            url=url,
            is_mobile=is_mobile,
            timeout=timeout,
            full_page=full_page,
        )
    )


class ScreenshotParams(BaseModel):
    url: str
    user_agent: str | None = None
    extra_http_headers: dict[str, str] | None = None
    is_mobile: bool = False
    timeout: float = 30
    full_page: bool = True
    wait_for: int | None = None


@router.post("/screenshot")
async def screenshot_post(
    params: ScreenshotParams,
) -> bytes:
    logger.debug(f"Taking screenshot of {params.url} with params: {params.model_dump()}")
    return response_image(
        await take_screenshot(
            url=params.url,
            user_agent=params.user_agent,
            extra_http_headers=params.extra_http_headers,
            is_mobile=params.is_mobile,
            timeout=params.timeout,
            full_page=params.full_page,
            wait_for=params.wait_for,
        )
    )
