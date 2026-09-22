# E-Commerce Selenium Automation Framework
### Capstone 2 — Unittest + PyTest + Page Object Model

A Selenium Python automation framework for `tutorialsninja.com/demo`
(OpenCart demo store), covering Login and Product Search → Add to Cart
→ Update Quantity → Verify Cart.

## What makes this framework different

Most student submissions for this assignment build a plain POM
framework and pick either Unittest *or* PyTest. This one goes further:

1. **Self-healing locators** — every UI element has a *list* of
   fallback locator strategies (id → css → xpath → …) defined in
   `locators/*.yaml`. `BasePage.find_element()` tries each in order
   and logs which one actually worked, so a single broken `id`
   doesn't break the whole suite, and you get visibility into which
   locators are going stale.
2. **True Unittest + PyTest hybrid** — test classes inherit from
   `unittest.TestCase` (structure, `setUp`/`tearDown`, assertions),
   but the entire suite is discovered, parametrized, marked, and
   reported through PyTest (`pytest.ini`, `pytest-html`, custom
   markers, fixtures). See `conftest.py`'s `inject_driver` fixture for
   how the two are bridged.
3. **Externalized locator repository** — locators live in YAML, not
   hardcoded in page classes. UI changes → edit YAML, not code.
4. **Bonus: SQLite run-history + trend dashboard** — every test run is
   logged to `reports/run_history.db`. `dashboard/generate_dashboard.py`
   renders a pass-rate-over-time chart (Chart.js) from it.
5. **Bonus: hand-written retry decorator** (`utils/retry_util.py`) with
   exponential backoff for transient UI flakiness — not a plugin.
6. **Fail-fast config validation** via pydantic — a malformed
   `config.yaml` raises a clear error immediately instead of a
   confusing Selenium exception later.

## Project structure

```
Capestone_Project/
├── config/            # config.yaml + pydantic-validated loader (multi-env: qa/staging/prod)
├── locators/           # YAML locator repositories (self-healing fallback lists)
├── pages/              # Page Objects (BasePage has the self-healing engine)
├── tests/               # unittest.TestCase test classes, run via pytest
├── data/                # users.json, test_data.csv (data-driven inputs)
├── utils/               # driver factory, logger, retry, waits, screenshots
├── reports/             # pytest-html output, screenshots, run_history.db
├── dashboard/           # bonus trend dashboard generator
├── conftest.py          # fixtures, screenshot-on-fail hook, DB logging hook
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You need **Google Chrome installed**. Selenium 4's built-in Selenium
Manager will auto-download the matching chromedriver on first run (it
needs internet access to do this once). If your machine is
offline/locked-down, install chromedriver manually and set:

```bash
export CHROME_DRIVER_PATH=/path/to/chromedriver
```

## Test accounts — nothing to set up

`tutorialsninja.com/demo` has no pre-existing accounts, so the positive
login test (`test_valid_login_succeeds`) **creates its own**: it
registers a brand-new unique user (details from `data/users.json` ->
`new_user_template`), logs out, then logs back in with it. The negative
login test uses the non-existent `invalid_user` from the same file.

## Running the suite

```bash
# Everything
pytest

# Only smoke tests
pytest -m smoke

# Only regression
pytest -m regression

# A single file
pytest tests/test_cart.py -v

# Against staging config (headless=true in config.yaml)
ENV=staging pytest
```

HTML report: `reports/html_report/report.html`
Screenshots on failure: `reports/screenshots/`
Logs: `logs/framework.log`

## Generating the trend dashboard (bonus)

Run pytest at least once, then:

```bash
python dashboard/generate_dashboard.py
```

Open `reports/html_report/dashboard.html` in a browser.

## Adding a new page / locator

1. Add the element's fallback locator list to the right file in
   `locators/`.
2. Reference it by key in the corresponding Page Object using
   `self.click("key")`, `self.type_text("key", value)`, etc. — you
   never touch Selenium's `By` API directly in page classes.

## Troubleshooting notes (lessons learned)

- **`InvalidElementStateException` on `.clear()`** — the locator resolved to a
  wrapper `<div>` (OpenCart's `id="search"` is the *input-group div*, not the
  input). Locators now target the `<input>` itself, and `BasePage.type_text`
  also descends from a wrapper to its inner input as a safety net.
- **Duplicate elements (hidden + visible)** — `wait_util` now returns the first
  *displayed* match among all matches instead of only checking the first DOM
  match (e.g. the hidden header "Logout" vs. the visible sidebar one).
- **Implicit wait is 0** — mixing implicit and explicit waits makes every failed
  fallback locator crawl; all waiting is explicit.
- OpenCart's markup changes occasionally; if a test fails, check
  `logs/framework.log` for `[self-heal]` warnings — they show which locator
  stopped working so you can add a fresh fallback to the relevant YAML file.
