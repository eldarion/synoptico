from django.core import validators
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from slugify import slugify

from .fields import ISBNField
from .validators import validate_timecode


class CreatedByModel(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)

    class Meta:
        abstract = True


class Story(CreatedByModel):

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)[:50]
        super(Story, self).save(*args, **kwargs)


class Timeline(CreatedByModel):

    MEDIA_TYPE_BOOK = "book"
    MEDIA_TYPE_MOVIE = "movie"
    MEDIA_TYPE_CHOICES = [
        (MEDIA_TYPE_BOOK, "Book"),
        (MEDIA_TYPE_MOVIE, "Movie")
    ]

    story = models.ForeignKey(Story, related_name="timelines")
    isbn = ISBNField(blank=True)
    imdb = models.CharField(max_length=100, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.full_clean()  # have to do this to get validators to run on ISBNField. Is there a way to avoid this?
        return super(Timeline, self).save(*args, **kwargs)


class Event(CreatedByModel):

    description = models.TextField()


class TimelineMapping(CreatedByModel):

    timeline = models.ForeignKey(Timeline)
    event = models.ForeignKey(Event)
    offset = models.CharField(max_length=50)

    def clean(self):
        if self.timeline.media_type == Timeline.MEDIA_TYPE_BOOK:
            validators.validate_integer(self.offset)
        elif self.timeline.media_type == Timeline.MEDIA_TYPE_MOVIE:
            validate_timecode(self.offset)
        super(TimelineMapping, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(TimelineMapping, self).save(*args, **kwargs)
