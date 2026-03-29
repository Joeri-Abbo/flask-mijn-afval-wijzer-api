import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from trash_can_client import TrashCanClient


@pytest.fixture
def client():
    with patch("trash_can_client.MijnAfvalWijzerClient"), patch("trash_can_client.MongoDBClient"):
        return TrashCanClient()


class TestGetCollectionKey:
    def test_basic_key(self, client):
        assert client.get_collection_key("1234AB", "1", "") == "1234AB-1-"

    def test_space_in_zip_code_replaced(self, client):
        assert client.get_collection_key("1234 AB", "1", "") == "1234-AB-1-"

    def test_with_add_on(self, client):
        assert client.get_collection_key("1234AB", "10", "A") == "1234AB-10-A"


class TestIsDateInThePast:
    def test_past_date_returns_true(self, client):
        past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        assert client.is_date_in_the_past(past) is True

    def test_future_date_returns_false(self, client):
        future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        assert client.is_date_in_the_past(future) is False

    def test_invalid_date_string_returns_false(self, client):
        assert client.is_date_in_the_past("not-a-date") is False

    def test_wrong_format_returns_false(self, client):
        assert client.is_date_in_the_past("29-03-2026") is False
