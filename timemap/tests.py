from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from .models import Project, Timeline, Event, TimelineMapping


class ValidationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="jtauber")
        self.project = Project.objects.create(title="The Hobbit", created_by=self.user)

    def test_isbn_validation_error(self):
        with self.assertRaises(ValidationError):
            Timeline.objects.create(
                project=self.project,
                media_type=Timeline.MEDIA_TYPE_BOOK,
                name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
                identifier="notanisbn",
                created_by=self.user
            )

    def test_isbn_validation_error_from_no_right_number_of_digits(self):
        with self.assertRaises(ValidationError):
            Timeline.objects.create(
                project=self.project,
                media_type=Timeline.MEDIA_TYPE_BOOK,
                name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
                identifier="132",
                created_by=self.user
            )

    def test_isbn_validation_valid_with_10_digits(self):
        timeline = Timeline.objects.create(
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
            identifier="0618968633",
            created_by=self.user
        )
        self.assertEquals(timeline.pk, 1)

    def test_isbn_validation_valid_with_13_digits(self):
        timeline = Timeline.objects.create(
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
            identifier="9780618968633",
            created_by=self.user
        )
        self.assertEquals(timeline.pk, 1)

    def test_page_number_validation_error(self):
        timeline = Timeline.objects.create(
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
            identifier="9780618968633",
            created_by=self.user
        )
        event = Event.objects.create(
            project=self.project,
            description="Thorin inserts the key",
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
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_BOOK,
            name="The Hobbit (Houghton Mifflin Seventieth Anniversary Edition)",
            identifier="9780618968633",
            created_by=self.user
        )
        event = Event.objects.create(
            project=self.project,
            description="Thorin inserts the key",
            created_by=self.user
        )
        mapping = TimelineMapping.objects.create(
            timeline=timeline,
            event=event,
            offset="194",
            created_by=self.user
        )
        self.assertEquals(mapping.pk, 1)

    def test_timecode_validation_error(self):
        timeline = Timeline.objects.create(
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_MOVIE,
            name="The Hobbit: An Unexpected Journey",
            identifier="http://www.imdb.com/title/tt0903624/",
            created_by=self.user
        )
        event = Event.objects.create(
            project=self.project,
            description="Thorin inserts the key",
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
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_MOVIE,
            name="The Hobbit: An Unexpected Journey",
            identifier="http://www.imdb.com/title/tt0903624/",
            created_by=self.user
        )
        event = Event.objects.create(
            project=self.project,
            description="Thorin inserts the key",
            created_by=self.user
        )
        mapping = TimelineMapping.objects.create(
            timeline=timeline,
            event=event,
            offset="00:30:15:44",
            created_by=self.user
        )
        self.assertEquals(mapping.pk, 1)

    def test_timecode_validation_works_no_frames(self):
        timeline = Timeline.objects.create(
            project=self.project,
            media_type=Timeline.MEDIA_TYPE_MOVIE,
            name="The Hobbit: An Unexpected Journey",
            identifier="http://www.imdb.com/title/tt0903624/",
            created_by=self.user
        )
        event = Event.objects.create(
            project=self.project,
            description="Thorin inserts the key",
            created_by=self.user
        )
        mapping = TimelineMapping.objects.create(
            timeline=timeline,
            event=event,
            offset="00:30:15",
            created_by=self.user
        )
        self.assertEquals(mapping.pk, 1)


class OrderingTests(TestCase):

    fixtures = ["projects", "hobbit_timelines", "hobbit_mappings"]

    def setUp(self):
        self.user = User.objects.create_user(username="jtauber")

    def test_page_ordering(self):
        pages = [
            x.offset.strip()
            for x in Timeline.objects.get(pk=1).events()
        ]
        self.assertEquals(pages, ["9", "40", "70", "102", "110", "137", "159", "194", "208", "248"])
