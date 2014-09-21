from django.contrib import admin

from .models import Project, Timeline, Event, TimelineMapping


admin.site.register(
    Project,
    list_display=["title", "slug", "created_by", "created_at"],
    list_filter=["created_at", "created_by"],
    read_only_fields=["slug"],
    raw_id_fields=["created_by"],
    search_fields=["title"],
)
admin.site.register(
    Timeline,
    list_display=["project", "identifier", "media_type", "name", "created_by", "created_at"],
    list_filter=["project", "media_type", "created_at", "created_by"],
    raw_id_fields=["project", "created_by"],
    search_fields=["project__title", "name"]
)
admin.site.register(
    Event,
    list_display=["description", "created_by", "created_at"],
    list_filter=["created_at", "created_by"],
    search_fields=["description"]
)
admin.site.register(
    TimelineMapping,
    list_display=["created_by", "created_at"],
    list_filter=["timeline", "event", "created_at", "created_by"],
    search_fields=["timeline__name", "event__description", "timeline__project__title"],
    raw_id_fields=["timeline", "event"]
)
