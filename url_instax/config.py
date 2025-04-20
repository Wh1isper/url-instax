from __future__ import annotations

import dotenv

dotenv.load_dotenv()

import os

from pydantic import BaseModel, ConfigDict


def get_config() -> Config:
    return Config.from_env()


DEFAULT_TOKEN = ""


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    api_token: str

    api_base_url: str | None
    """For mcp mode, this is the url of the sserver."""

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            api_token=os.getenv("API_TOKEN", DEFAULT_TOKEN),
            api_base_url=os.getenv("API_BASE_URL", None),
        )
