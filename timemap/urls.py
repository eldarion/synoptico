from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import (
    ajax_autocomplete_events,
    ProjectDetailView,
    TimelineDetailView,
    TimelineMappingCreateView
)


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(
        r"^projects/(?P<slug>[\w-]+)/$",
        ProjectDetailView.as_view(),
        name="project_detail"
    ),
    url(
        r"^projects/(?P<slug>[\w-]+)/timelines/(?P<pk>\d+)/$",
        TimelineDetailView.as_view(),
        name="timeline_detail"
    ),
    url(
        r"projects/(?P<slug>[\w-]+)/timelines/(?P<pk>\d+)/events/$",
        TimelineMappingCreateView.as_view(),
        name="timeline_events_mapping_create"
    ),
    url(
        r"^ajax/project-events/(?P<pk>\d+)/$",
        ajax_autocomplete_events,
        name="ajax_autocomplete_events"
    )
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
