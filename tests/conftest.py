import db_internal
import pytest
import os


@pytest.fixture(scope="function")
def db_session():
    # Set up: Connect to your test database and create tables
    db_internal.create_db()

    # This yields control to your test function, allowing it to run with a fresh database
    yield

    # Tear down: Disconnect and drop the tables, or delete the database file
    os.remove("test.db")
