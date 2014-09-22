import re

from django.core.validators import RegexValidator, validate_integer
from django.utils.deconstruct import deconstructible


@deconstructible
class TimecodeValidator(RegexValidator):
    regex = re.compile(r"\d{2}:\d{2}:\d{2}")
    message = "Invalid timecode. Format: 00:00:00"


@deconstructible
class IMDBUrlValidator(RegexValidator):
    regex = re.compile(r"http://www.imdb.com/title/.*")
    message = "Invalid URL. Should be a valid IMDB url."


@deconstructible
class ISBNValidator(RegexValidator):
    regex = re.compile(r"([0-9]{3})?[0-9]{9}[0-9X]")
    message = "Invalid ISBN. Should be a valid ISBN-10 or ISBN-13 without hyphens or spaces."


validate_timecode = TimecodeValidator()
validate_imdb_url = IMDBUrlValidator()
validate_isbn = ISBNValidator()


def validate_page_number(value):
    validate_integer(value)
