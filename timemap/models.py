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
    description = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)[:50]
        super(Project, self).save(*args, **kwargs)


class Timeline(CreatedByModel):

    MEDIA_TYPE_KINDLE = "kindle"
    MEDIA_TYPE_BOOK = "book"
    MEDIA_TYPE_MOVIE = "movie"
    MEDIA_TYPE_CHOICES = [
        (MEDIA_TYPE_BOOK, "Book"),
        (MEDIA_TYPE_KINDLE, "Kindle Book"),
        (MEDIA_TYPE_MOVIE, "Movie")
    ]
    MEDIA_TYPE_OFFSET_DISPLAYS = {
        MEDIA_TYPE_KINDLE: "Location {}",
        MEDIA_TYPE_BOOK: "Page {}",
        MEDIA_TYPE_MOVIE: "{}"
    }

    project = models.ForeignKey(Project, related_name="timelines")
    identifier = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = [("identifier", "media_type")]

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

    project = models.ForeignKey(Project, related_name="events")
    description = models.TextField()

    def __unicode__(self):
        return u"<Event {} by {}>".format(self.pk, self.created_by.username)


class TimelineMapping(CreatedByModel):

    timeline = models.ForeignKey(Timeline, related_name="mappings")
    event = models.ForeignKey(Event, related_name="mappings")
    offset = models.CharField(max_length=50)

    def __unicode__(self):
        return u"<TimelineMapping timeline={}, event={}, offset={}>".format(
            unicode(self.timeline),
            self.event.pk,
            self.offset
        )

    def offset_display(self):
        return Timeline.MEDIA_TYPE_OFFSET_DISPLAYS[self.timeline.media_type].format(self.offset)

    @classmethod
    def validate_offset(cls, timeline, offset):
        if timeline.media_type == Timeline.MEDIA_TYPE_BOOK:
            validate_page_number(offset)
        elif timeline.media_type == Timeline.MEDIA_TYPE_MOVIE:
            validate_timecode(offset)

    def clean(self):
        TimelineMapping.validate_offset(self.timeline, self.offset)
        super(TimelineMapping, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(TimelineMapping, self).save(*args, **kwargs)
