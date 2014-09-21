import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_integer
from django.utils.deconstruct import deconstructible


@deconstructible
class TimecodeValidator(RegexValidator):
    regex = re.compile(r"\d{2}:\d{2}:\d{2}:\d{2}")
    message = "Invalid timecode. Format: 00:00:00:00"


@deconstructible
class IMDBUrlValidator(RegexValidator):
    regex = re.compile(r"http://www.imdb.com/title/.*")
    message = "Invalid URL. Should be a valid IMDB url."


validate_timecode = TimecodeValidator()
validate_imdb_url = IMDBUrlValidator()


def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError("ISBN should be 13 digits.", code="invalid")
    validate_integer(value)


def validate_page_number(value):
    validate_integer(value)
