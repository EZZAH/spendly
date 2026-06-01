import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config["DATABASE"] = db_path
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            from database.db import init_db, seed_db
            init_db()
            seed_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
