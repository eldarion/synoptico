from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from slugify import slugify

from .validators import (
    validate_imdb_url,
    validate_isbn,
    validate_timecode,
    validate_page_number
)


class CreatedByModel(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)

    class Meta:
        abstract = True


class Project(CreatedByModel):

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)[:50]
        super(Project, self).save(*args, **kwargs)


class Timeline(CreatedByModel):

    MEDIA_TYPE_BOOK = "book"
    MEDIA_TYPE_MOVIE = "movie"
    MEDIA_TYPE_CHOICES = [
        (MEDIA_TYPE_BOOK, "Book"),
        (MEDIA_TYPE_MOVIE, "Movie")
    ]

    project = models.ForeignKey(Project, related_name="timelines")
    identifier = models.CharField(max_length=200, unique=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{}: {}".format(self.identifier, self.name)

    def clean(self):
        if self.media_type == Timeline.MEDIA_TYPE_BOOK:
            validate_isbn(self.identifier)
        elif self.media_type == Timeline.MEDIA_TYPE_MOVIE:
            validate_imdb_url(self.identifier)
        super(Timeline, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Timeline, self).save(*args, **kwargs)


class Event(CreatedByModel):

    description = models.TextField()

    def __unicode__(self):
        return u"<Event {} by {}>".format(self.pk, self.created_by.username)


class TimelineMapping(CreatedByModel):

    timeline = models.ForeignKey(Timeline)
    event = models.ForeignKey(Event)
    offset = models.CharField(max_length=50)

    def __unicode__(self):
        return u"<TimelineMapping timeline={}, event={}, offset={}>".format(
            unicode(self.timeline),
            self.event.pk,
            self.offset
        )

    def clean(self):
        if self.timeline.media_type == Timeline.MEDIA_TYPE_BOOK:
            validate_page_number(self.offset)
        elif self.timeline.media_type == Timeline.MEDIA_TYPE_MOVIE:
            validate_timecode(self.offset)
        super(TimelineMapping, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(TimelineMapping, self).save(*args, **kwargs)
