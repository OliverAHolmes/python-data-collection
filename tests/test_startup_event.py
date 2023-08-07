import unittest
from unittest.mock import patch

from main import startup_event


class TestStartupEvent(unittest.TestCase):
    @patch("main.db_internal.create_db")
    def test_startup_event(self, mock_create_db):
        # When it's called
        import asyncio

        asyncio.run(startup_event())

        # Then it should call the db_internal.create_db method once
        mock_create_db.assert_called_once()


if __name__ == "__main__":
    unittest.main()
