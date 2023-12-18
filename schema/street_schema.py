from marshmallow import Schema, fields, validates, ValidationError
import re


class StreetSchema(Schema):
    zip_code = fields.String(required=True)
    house_number = fields.String(required=True)
    add_on = fields.String(required=False)

    @validates('zip_code')
    def validate_zip_code(self, value):
        """
        Validate that the zip code is in the Dutch postal code format.
        """
        if not re.match(r'^\d{4}\s?[A-Z]{2}$', value):
            raise ValidationError('Invalid Dutch postal code format. Expected format: 1234 AB.')
