import unittest
import os
from unittest.mock import patch
from main import startup_event
from config import Settings


class TestStartupEvent(unittest.TestCase):
    @patch("main.db_internal.create_db")
    def test_startup_event(self, mock_create_db):
        # When it's called
        import asyncio

        asyncio.run(startup_event())

        # Then it should call the db_internal.create_db method once
        mock_create_db.assert_called_once()


class TestSettings(unittest.TestCase):
    def setUp(self):
        # Make sure any prior environment variable is removed to not affect the test
        if "ENV" in os.environ:
            del os.environ["ENV"]

    @patch.dict(os.environ, {"ENV": "development"})
    def test_default_configuration(self):
        settings = Settings()
        self.assertEqual(settings.ENV, "development")
        self.assertEqual(settings.db_path, "database.db")

    @patch.dict(os.environ, {"ENV": "testing"})
    def test_testing_configuration(self):
        settings = Settings()
        self.assertEqual(settings.ENV, "testing")
        self.assertEqual(settings.db_path, "test.db")
