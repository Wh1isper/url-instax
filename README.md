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

Open `https://url-instax.wh1isper.top:8890?url=https://example.com` in your browser, and you will see a screenshot of the page.

I created a demo server, check `https://url-instax.wh1isper.top:8890/docs` for GET/POST API specification. This is only for testing and you should not use it for production.
