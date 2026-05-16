# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a personal expense tracking web application built with Flask. It's structured as a step-by-step student project where the core features are scaffolded but not yet fully implemented.

### Purpose
Users can:
- Register and log in securely
- Log expenses with category, amount, date, and description
- Edit and delete expenses
- View spending insights (category breakdowns, monthly summaries)
- Filter expenses by date range

Currently implemented: Landing, login, and registration pages. Stubbed routes exist for the remaining features (logout, profile, add/edit/delete expenses).

### Tech Stack
- **Backend**: Python + Flask 3.1.3 with Jinja2 templating
- **Database**: SQLite (via `sqlite3` module)
- **Frontend**: Plain HTML/CSS/JavaScript (no frameworks)
- **Testing**: pytest 8.3.5 + pytest-flask 1.3.0
- **Auth**: Werkzeug (password hashing, included with Flask)
- **Python version**: 3.8+

## Project Structure

```
expense-tracker/
├── app.py                    # Flask app entry point, all route definitions
├── database/
│   ├── __init__.py          # Package marker
│   └── db.py                # SQLite helpers (get_db, init_db, seed_db) — TODO
├── templates/
│   ├── base.html            # Shared layout (nav, main, footer)
│   ├── landing.html         # Public homepage
│   ├── login.html           # Login form
│   └── register.html        # Registration form
├── static/
│   ├── css/style.css        # All styles
│   └── js/main.js           # Client-side JavaScript
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── venv/                    # Virtual environment (not committed)
```

### Key Architecture Notes

1. **Routes & Templates**: `app.py` defines all routes. Each route renders a template from `templates/`. All templates extend `base.html`, which provides shared navbar, footer, and CSS/JS includes.

2. **Database Layer**: Currently stubbed in `database/db.py`. Students implement:
   - `get_db()` — returns a SQLite connection with row_factory and foreign keys enabled
   - `init_db()` — creates all tables using CREATE TABLE IF NOT EXISTS
   - `seed_db()` — inserts sample data for development

3. **Static Assets**: Served by Flask as-is. Linked from `base.html`. No build step.

4. **No ORM**: Raw SQLite queries. Intentional for a teaching project.

## Development Commands

### Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
pip install -r requirements.txt
```

### Running the App
```bash
# From project root with venv activated
python app.py
```
The app runs at `http://127.0.0.1:5001` in debug mode (auto-reload on code changes).

### Testing
```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov=database
```

### Database
Database operations should be implemented in `database/db.py`. Import and call from `app.py`:
```python
from database.db import get_db, init_db
```

## Important Design Notes

- **Step-by-Step Structure**: Routes are labeled "coming in Step X" where X increases (3, 4, 7, 8, 9). Each step represents a feature milestone students implement.
- **Placeholder Routes**: Return simple strings (e.g., "Logout — coming in Step 3"). Replace with actual implementations.
- **No Authentication Yet**: Login/register pages exist but don't interact with a database. Session management is stubbed.
- **No Expense Logic**: Routes like `/expenses/add` exist but don't process forms or touch the database.

## Git Workflow

- Main branch: `main`
- Remote: `https://github.com/EZZAH/spendly.git`
- Initial commit exists; further work should create feature branches or commit directly to main as needed.

## Port & Debug Settings

- **Port**: 5001 (configured in `app.py`)
- **Debug Mode**: Enabled by default in `app.run(debug=True)`
- **Auto-reload**: On when debug=True (watches for file changes)
