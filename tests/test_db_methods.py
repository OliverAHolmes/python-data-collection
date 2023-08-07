import os
from unittest import mock
import pytest

from db_internal import create_db, settings, SQLModel


def test_create_db_with_testing_env_and_db_exists():
    settings.ENV = "testing"
    settings.db_path = "test.db"

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
    settings.ENV = "testing"
    settings.db_path = "test.db"

    with mock.patch("os.path.exists", return_value=False):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_not_called()
                mock_create_all.assert_called_once()


def test_create_db_with_non_testing_env_and_db_not_exists():
    settings.ENV = "production"
    settings.db_path = "test.db"

    with mock.patch("os.path.exists", return_value=False):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_not_called()
                mock_create_all.assert_called_once()


def test_create_db_with_non_testing_env_and_db_exists():
    settings.ENV = "production"
    settings.db_path = "test.db"

    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("os.remove") as mock_remove:
            with mock.patch(
                "db_internal.SQLModel.metadata.create_all"
            ) as mock_create_all:
                create_db()
                mock_remove.assert_not_called()
                mock_create_all.assert_not_called()
