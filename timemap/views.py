import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Project, Timeline


class ProjectDetailView(DetailView):
    model = Project


class TimelineDetailView(DetailView):
    model = Timeline

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = queryset.filter(project__slug=slug)
        try:
            obj = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404("No timeline found matching the query")
        return obj


def ajax_autocomplete_events(request, pk):
    project = get_object_or_404(Project, pk=pk)
    events = project.events.all()
    data = [
        {"pk": event.pk, "description": event.description}
        for event in events
    ]  # NOTE: It will likely be useful to return details of where this event is already logged
    return HttpResponse(json.dumps(data), content_type="application/json")
