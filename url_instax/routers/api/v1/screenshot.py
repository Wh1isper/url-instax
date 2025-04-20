from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter(
    tags=["Component"],
    prefix="/api/v1",
)


class ScreenshotResponse(Response):
    media_type = "image/png"

    def render(self, content: bytes) -> bytes:
        self.headers["Content-Disposition"] = 'inline; filename="screenshot.png"'
        return super().render(content)


@router.get("/screenshot")
async def screenshot_get() -> ScreenshotResponse:
    return


class ScreenshotParams(BaseModel):
    url: str


@router.post("/screenshot")
async def screenshot_post(
    params: ScreenshotParams,
) -> ScreenshotResponse:
    return
