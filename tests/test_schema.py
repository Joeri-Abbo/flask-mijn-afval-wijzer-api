import pytest
from marshmallow import ValidationError
from schema.street_schema import StreetSchema


@pytest.fixture
def schema():
    return StreetSchema()


class TestStreetSchemaValidZipCodes:
    def test_zip_code_with_space(self, schema):
        result = schema.load({"zip_code": "1234 AB", "house_number": "1"})
        assert result["zip_code"] == "1234 AB"

    def test_zip_code_without_space(self, schema):
        result = schema.load({"zip_code": "1234AB", "house_number": "1"})
        assert result["zip_code"] == "1234AB"

    def test_add_on_is_optional(self, schema):
        result = schema.load({"zip_code": "1234 AB", "house_number": "1"})
        assert "add_on" not in result

    def test_add_on_accepted_when_provided(self, schema):
        result = schema.load({"zip_code": "1234 AB", "house_number": "1", "add_on": "A"})
        assert result["add_on"] == "A"


class TestStreetSchemaInvalidZipCodes:
    def test_lowercase_letters_rejected(self, schema):
        with pytest.raises(ValidationError):
            schema.load({"zip_code": "1234 ab", "house_number": "1"})

    def test_too_few_digits_rejected(self, schema):
        with pytest.raises(ValidationError):
            schema.load({"zip_code": "123 AB", "house_number": "1"})

    def test_too_many_digits_rejected(self, schema):
        with pytest.raises(ValidationError):
            schema.load({"zip_code": "12345 AB", "house_number": "1"})

    def test_missing_zip_code_rejected(self, schema):
        with pytest.raises(ValidationError):
            schema.load({"house_number": "1"})

    def test_missing_house_number_rejected(self, schema):
        with pytest.raises(ValidationError):
            schema.load({"zip_code": "1234 AB"})
