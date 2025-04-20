from aiocache import SimpleMemoryCache, cached
from playwright.async_api import async_playwright

from url_instax.log import logger


class ScreenshotError(Exception):
    pass


class FailedToInitializeError(ScreenshotError):
    pass


class FailedToTakeScreenshotError(ScreenshotError):
    pass


def _get_url_instax_headers():
    return {
        "HTTP-Referer": "url-instax",
    }


cache = SimpleMemoryCache()


@cached(cache)
async def take_screenshot(
    url: str,
    user_agent: str | None = None,
    extra_http_headers: dict[str, str] | None = None,
    is_mobile: bool | None = None,
    timeout: float | None = 30,
    full_page: bool | None = True,
    wait_for: int | None = None,
) -> bytes:
    extra_http_headers = {
        **_get_url_instax_headers(),
        **(extra_http_headers or {}),
    }
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                user_agent=user_agent,
                extra_http_headers=extra_http_headers,
                is_mobile=is_mobile,
            )
        except Exception as e:
            raise FailedToInitializeError(
                f"Failed to initialize Playwright: {e}, try `playwright install` or `uv tool run playwright install"
            ) from e
        try:
            await page.goto(url)
            if wait_for:
                await page.wait_for_timeout(wait_for * 1000)
            return await page.screenshot(
                timeout=timeout * 1000,
                type="png",
                full_page=full_page,
            )
        except Exception as e:
            logger.exception(e)
            raise FailedToTakeScreenshotError(f"Failed to take screenshot: {e}") from e
        finally:
            await browser.close()
