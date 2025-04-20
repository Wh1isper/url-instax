# url-instax

[![Release](https://img.shields.io/github/v/release/wh1isper/url-instax)](https://img.shields.io/github/v/release/wh1isper/url-instax)
[![Build status](https://img.shields.io/github/actions/workflow/status/wh1isper/url-instax/main.yml?branch=main)](https://github.com/wh1isper/url-instax/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/wh1isper/url-instax/branch/main/graph/badge.svg)](https://codecov.io/gh/wh1isper/url-instax)
[![Commit activity](https://img.shields.io/github/commit-activity/m/wh1isper/url-instax)](https://img.shields.io/github/commit-activity/m/wh1isper/url-instax)
[![License](https://img.shields.io/github/license/wh1isper/url-instax)](https://img.shields.io/github/license/wh1isper/url-instax)

Screenshot for web page.

- **Github repository**: <https://github.com/wh1isper/url-instax/>
- **Documentation** <https://wh1isper.github.io/url-instax/>

## Quickstart

```bash
uvx url-instax http
```

or use docker image

```bash
docker run -p 8890:8890 ghcr.io/wh1isper/url-instax:latest
```

Access `http://localhost:8890/docs` for openapi docs.

## Usage

Open https://url-instax.wh1isper.top:8890?url=https://example.com in your browser, and you will see a screenshot of the page.

I created a demo server, check https://url-instax.wh1isper.top:8890/docs for `GET`/`POST` API specification. This is only for testing and you should not use it for production.

## MCP Server

This package includes a simple MCP server for LLM to view web page via screenshot. You can use this config to set up the server:

```json
{
  "mcpServers": {
    "yourware-mcp": {
      "command": "uvx",
      "args": ["url-instax@latest", "mcp"],
      "env": {
        "API_BASE_URL": "http://localhost:8890"
      }
    }
  }
}
```

if `API_BASE_URL` is not provided, it will directly use [playwright](https://playwright.dev/) to take screenshot, which you need to install Playwright first via `playwright install` or `uv tool run playwright install`.

You can use `https://url-instax.wh1isper.top:8890` as the `API_BASE_URL` for testing.
