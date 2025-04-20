from playwright.async_api import async_playwright

from url_instax.log import logger


class FailedToInitializeError(RuntimeError):
    pass


class FailedToTakeScreenshotError(RuntimeError):
    pass


async def take_screenshot(
    url: str,
) -> bytes:
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
        except Exception as e:
            raise FailedToInitializeError(f"Failed to initialize Playwright: {e}") from e
        try:
            await page.goto(url)
            return await page.screenshot(
                type="png",
            )
        except Exception as e:
            logger.exception(e)
            raise FailedToTakeScreenshotError(f"Failed to take screenshot: {e}") from e
        finally:
            await browser.close()
