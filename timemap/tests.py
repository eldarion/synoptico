from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from .models import Story, Timeline, Event, TimelineMapping


class ValidationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="paltman")
        self.story = Story.objects.create(title="A Land Remembered", created_by=self.user)

    def test_isbn_validation_error(self):
        with self.assertRaises(ValidationError):
            Timeline.objects.create(
                story=self.story,
                media_type=Timeline.MEDIA_TYPE_BOOK,
                name="Paperback Edition",
                isbn="notanisbn",
                created_by=self.user
            )

    def test_isbn_validation_works(self):
        timeline = Timeline.objects.create(
            story=self.story,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="Paperback Edition",
            isbn="9781561641161",
            created_by=self.user
        )
        self.assertEquals(timeline.pk, 1)

    def test_page_number_validation_error(self):
        timeline = Timeline.objects.create(
            story=self.story,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="Paperback Edition",
            isbn="9781561641161",
            created_by=self.user
        )
        event = Event.objects.create(
            description="Tobias MacIvey dies",
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            TimelineMapping.objects.create(
                timeline=timeline,
                event=event,
                offset="notapage",
                created_by=self.user
            )

    def test_page_number_validation_works(self):
        timeline = Timeline.objects.create(
            story=self.story,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="Paperback Edition",
            isbn="9781561641161",
            created_by=self.user
        )
        event = Event.objects.create(
            description="Tobias MacIvey dies",
            created_by=self.user
        )
        mapping = TimelineMapping.objects.create(
            timeline=timeline,
            event=event,
            offset="100",
            created_by=self.user
        )
        self.assertEquals(mapping.pk, 1)

    def test_timecode_validation_error(self):
        timeline = Timeline.objects.create(
            story=self.story,
            media_type=Timeline.MEDIA_TYPE_MOVIE,
            name="DVD",
            imdb="http://www.imdb.com/title/tt0210945/",
            created_by=self.user
        )
        event = Event.objects.create(
            description="Tobias MacIvey dies",
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            TimelineMapping.objects.create(
                timeline=timeline,
                event=event,
                offset="notatimecode",
                created_by=self.user
            )

    def test_timecode_validation_works(self):
        timeline = Timeline.objects.create(
            story=self.story,
            media_type=Timeline.MEDIA_TYPE_MOVIE,
            name="DVD",
            imdb="http://www.imdb.com/title/tt0210945/",
            created_by=self.user
        )
        event = Event.objects.create(
            description="Tobias MacIvey dies",
            created_by=self.user
        )
        mapping = TimelineMapping.objects.create(
            timeline=timeline,
            event=event,
            offset="00:30:15:44",
            created_by=self.user
        )
        self.assertEquals(mapping.pk, 1)