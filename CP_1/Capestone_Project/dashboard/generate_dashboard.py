"""
generate_dashboard.py
----------------------
Reads reports/run_history.db (populated automatically by conftest.py
on every test run) and renders a simple pass-rate trend dashboard
using Jinja2 + Chart.js.

Run after one or more `pytest` executions, from the project root:
    python dashboard/generate_dashboard.py

Output: reports/html_report/dashboard.html
"""

import sqlite3
import sys
from pathlib import Path

# Allow running this file directly (python dashboard/generate_dashboard.py)
# by putting the project root on sys.path, since Python only auto-adds the
# script's own directory (dashboard/), not the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from jinja2 import Environment, FileSystemLoader

from config.config_loader import settings, resolve_path
from utils.logger import get_logger

log = get_logger(__name__)

DB_PATH = resolve_path(settings.reporting.run_history_db)
DASHBOARD_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = resolve_path(settings.reporting.html_report_dir) / "dashboard.html"


def _fetch_run_summary():
    if not DB_PATH.exists():
        log.warning(f"No run history DB found at {DB_PATH}. Run pytest at least once first.")
        return [], []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # Group by the DATE portion of run_timestamp -> daily pass rate
    rows = conn.execute(
        """
        SELECT
            substr(run_timestamp, 1, 10) AS run_date,
            SUM(CASE WHEN outcome = 'passed' THEN 1 ELSE 0 END) AS passed,
            SUM(CASE WHEN outcome = 'failed' THEN 1 ELSE 0 END) AS failed,
            COUNT(*) AS total
        FROM test_runs
        GROUP BY run_date
        ORDER BY run_date ASC
        """
    ).fetchall()

    recent = conn.execute(
        """
        SELECT run_timestamp, test_name, outcome, duration_seconds, environment
        FROM test_runs
        ORDER BY id DESC
        LIMIT 25
        """
    ).fetchall()

    conn.close()
    return rows, recent


def generate():
    daily_rows, recent_rows = _fetch_run_summary()

    labels = [r["run_date"] for r in daily_rows]
    pass_rates = [
        round((r["passed"] / r["total"]) * 100, 1) if r["total"] else 0
        for r in daily_rows
    ]

    env = Environment(loader=FileSystemLoader(str(DASHBOARD_DIR)))
    template = env.get_template("template.html")

    html = template.render(
        labels=labels,
        pass_rates=pass_rates,
        recent_rows=recent_rows,
        has_data=bool(daily_rows),
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    log.info(f"Dashboard written to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
