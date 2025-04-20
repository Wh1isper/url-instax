import os


def test_screenshot(mock_server_url, client):
    response = client.get("/api/v1/screenshot", params={"url": mock_server_url})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Content-Disposition"] == "inline; filename=screenshot.png"
    # Check if the image is not empty
    assert len(response.content) > 0
    # Check if the response body is a valid PNG image
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n")
    assert response.content.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82")

    response = client.post(
        "/api/v1/screenshot",
        json={"url": mock_server_url},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Content-Disposition"] == "inline; filename=screenshot.png"
    # Check if the image is not empty
    assert len(response.content) > 0
    # Check if the response body is a valid PNG image
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n")
    assert response.content.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82")


async def test_screenshot_mcp(mock_server_url):
    # FIXME: This only test local way

    # With a temporary file
    import tempfile

    from url_instax.mcp import screenshot

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        await screenshot(
            url=mock_server_url,
            save_path=tmp_file_path,
        )
        assert tmp_file_path
        assert os.path.exists(tmp_file_path)
