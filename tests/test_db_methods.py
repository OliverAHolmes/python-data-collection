import os
from unittest import mock
from unittest.mock import patch
from db_internal import create_db, settings, SQLModel
from config import Settings


@patch.dict(os.environ, {"ENV": "testing"})
def test_create_db_with_testing_env_and_db_exists():
    assert settings.ENV == "testing"
    assert settings.db_path == "test.db"

    mock_exists = mock.Mock()
    mock_exists.side_effect = [True, False]

    with mock.patch("os.path.exists", mock_exists):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_called_once_with(settings.db_path)
                mock_create_all.assert_called_once()


def test_create_db_with_testing_env_and_db_not_exists():
    assert settings.ENV == "testing"
    assert settings.db_path == "test.db"

    with mock.patch("os.path.exists", return_value=False):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_not_called()
                mock_create_all.assert_called_once()


@patch.dict(os.environ, {"ENV": "development"})
def test_create_db_with_non_testing_env_and_db_not_exists():
    local_settings = Settings()
    assert local_settings.ENV == "development"
    assert local_settings.db_path == "database.db"

    with mock.patch("os.path.exists", return_value=False):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_not_called()
                mock_create_all.assert_called_once()
