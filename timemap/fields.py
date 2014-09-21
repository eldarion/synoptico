from django.core import validators
from django.db import models


class ISBNField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 13
        super(ISBNField, self).__init__(*args, **kwargs)
        self.validators.append(validators.validate_integer)
