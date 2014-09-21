import re

from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator


@deconstructible
class TimecodeValidator(RegexValidator):
    regex = re.compile(r"\d{2}:\d{2}:\d{2}:\d{2}")
    message = "Invalid timecode. Format: 00:00:00:00"


validate_timecode = TimecodeValidator()
