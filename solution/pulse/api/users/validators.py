from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from api.countries.models import Country


@deconstructible
class CountryCodeValidator(BaseValidator):
    def __init__(self, message=None):
        self.message = message or "There is no such country"

    def __call__(self, value):
        try:
            Country.objects.get(alpha2=value)
        except Country.DoesNotExist:
            raise ValidationError(self.message) from None
