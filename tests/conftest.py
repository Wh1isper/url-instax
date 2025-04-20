import os
import socket
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from url_instax.config import get_config
from url_instax.web_app import app as APP

_HERE = Path(__file__).parent
MOCK_SERVER = _HERE / "mock_server.py"


def get_port():
    # Get an unoccupied port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def mock_server_url():
    """Fixture to start the mock server and return its URL."""
    port = get_port()
    url = f"http://127.0.0.1:{port}"

    # Start the mock server in a separate process
    import subprocess

    server_process = subprocess.Popen(
        ["python", str(MOCK_SERVER)],
        env={"PORT": str(port), **os.environ},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # Wait for the server to start
        for _ in range(10):
            # Check if the server is running
            try:
                socket.create_connection(("127.0.0.1", port))
                break
            except ConnectionRefusedError:
                time.sleep(0.5)
        yield url
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()
        if server_process.returncode is None:
            server_process.kill()
        if server_process.returncode is not None:
            print(f"Mock server exited with code {server_process.returncode}")
        else:
            print("Mock server terminated")
        # Check for any errors in the server output
        stderr = server_process.stderr.read()
        if stderr:
            print(f"Mock server error output: {stderr.decode()}")
        else:
            print("No errors in mock server output")


@pytest.fixture
async def app():
    yield APP


@pytest.fixture
def client(app):
    config = get_config()
    with TestClient(
        app,
        headers=({"Authorization": f"Bearer {config.api_token}"} if config.api_token else {}),
    ) as client:
        yield client
