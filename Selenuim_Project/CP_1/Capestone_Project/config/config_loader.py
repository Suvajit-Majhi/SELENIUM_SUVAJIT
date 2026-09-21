"""
config_loader.py
-----------------
Loads config/config.yaml, validates it with pydantic (so a malformed
config fails immediately with a clear error instead of a cryptic
Selenium exception 20 steps later), and exposes a singleton `settings`
object that the rest of the framework imports.

Active environment is selected via the ENV environment variable:
    export ENV=staging   (Linux/Mac)
    set ENV=staging      (Windows)
If ENV is not set, `default_env` from config.yaml is used.
"""

import os
from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel, Field, field_validator

CONFIG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CONFIG_DIR.parent
CONFIG_FILE = CONFIG_DIR / "config.yaml"


class EnvironmentConfig(BaseModel):
    base_url: str
    browser: str = "chrome"
    headless: bool = False
    implicit_wait: int = Field(ge=0, default=5)
    explicit_wait: int = Field(ge=0, default=15)
    page_load_timeout: int = Field(ge=0, default=30)

    @field_validator("browser")
    @classmethod
    def browser_supported(cls, v: str) -> str:
        allowed = {"chrome", "firefox", "edge"}
        if v.lower() not in allowed:
            raise ValueError(f"browser must be one of {allowed}, got '{v}'")
        return v.lower()

    @field_validator("base_url")
    @classmethod
    def url_well_formed(cls, v: str) -> str:
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError(f"base_url must start with http:// or https://, got '{v}'")
        return v


class RetryConfig(BaseModel):
    max_attempts: int = Field(ge=1, default=3)
    base_delay_seconds: float = Field(ge=0, default=1)
    backoff_multiplier: float = Field(ge=1, default=2)


class ReportingConfig(BaseModel):
    html_report_dir: str = "reports/html_report"
    screenshot_dir: str = "reports/screenshots"
    run_history_db: str = "reports/run_history.db"


class Settings(BaseModel):
    default_env: str
    environments: Dict[str, EnvironmentConfig]
    retry: RetryConfig
    reporting: ReportingConfig
    active_env_name: str = ""
    active: Optional[EnvironmentConfig] = None  # resolved active environment


def _load_raw_yaml() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_FILE}. "
            "Did you rename or move config/config.yaml?"
        )
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if not raw:
        raise ValueError("config.yaml is empty or invalid YAML.")
    return raw


def load_settings() -> Settings:
    raw = _load_raw_yaml()

    try:
        settings = Settings(
            default_env=raw["default_env"],
            environments=raw["environments"],
            retry=raw["retry"],
            reporting=raw["reporting"],
        )
    except KeyError as e:
        raise ValueError(f"config.yaml is missing required top-level key: {e}") from e

    env_name = os.getenv("ENV", settings.default_env)
    if env_name not in settings.environments:
        available = ", ".join(settings.environments.keys())
        raise ValueError(
            f"Environment '{env_name}' not defined in config.yaml. "
            f"Available environments: {available}"
        )

    settings.active_env_name = env_name
    settings.active = settings.environments[env_name]
    return settings


# Singleton import target: `from config.config_loader import settings`
settings = load_settings()


def resolve_path(relative_path: str) -> Path:
    """Resolve a path from config.yaml relative to the project root."""
    return PROJECT_ROOT / relative_path


if __name__ == "__main__":
    # Quick manual sanity check: python config/config_loader.py
    print(f"Active environment : {settings.active_env_name}")
    print(f"Base URL           : {settings.active.base_url}")
    print(f"Browser            : {settings.active.browser}")
    print(f"Headless           : {settings.active.headless}")
    print(f"Retry max attempts : {settings.retry.max_attempts}")
