"""
screenshot_util.py
-------------------
Saves timestamped screenshots. Called both manually (e.g. "capture
screenshot after add-to-cart") and automatically via the
pytest_runtest_makereport hook in conftest.py on test failure.
"""

from datetime import datetime
from pathlib import Path

from config.config_loader import settings, resolve_path
from utils.logger import get_logger

log = get_logger(__name__)


def _screenshot_dir() -> Path:
    directory = resolve_path(settings.reporting.screenshot_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def capture_screenshot(driver, name: str) -> str:
    """
    Capture a screenshot and save it as <name>_<timestamp>.png inside
    the configured screenshot directory. Returns the file path as a
    string (or empty string if capture failed -- never raises, so a
    screenshot failure never masks the real test failure).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
    filename = f"{safe_name}_{timestamp}.png"
    filepath = _screenshot_dir() / filename

    try:
        driver.save_screenshot(str(filepath))
        log.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    except Exception as e:
        log.error(f"Failed to capture screenshot '{name}': {e}")
        return ""
