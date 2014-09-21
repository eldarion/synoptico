import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from account.decorators import login_required

from .forms import TimelineMappingForm
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

    def get_context_data(self, **kwargs):
        context = super(TimelineDetailView, self).get_context_data(**kwargs)
        context.update({
            "form": TimelineMappingForm(timeline=self.get_object())
        })
        return context


def ajax_autocomplete_events(request, pk):
    project = get_object_or_404(Project, pk=pk)
    events = project.events.all()
    data = [
        {"pk": event.pk, "description": event.description}
        for event in events
    ]  # NOTE: It will likely be useful to return details of where this event is already logged
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_POST
def ajax_create_an_event_mapping(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk)
    form = TimelineMappingForm(request.POST, timeine=timeline)
    data = {}
    if form.is_valid():
        mapping = form.create_mapping()
        form = TimelineMappingForm(timeline=timeline)
        data = {
            "html": render_to_string("timemap/_mapping.html", RequestContext(request, {
                "mapping": mapping}
            ))
        }
    data["fragments"] = {
        ".mapping-form": render_to_string(
            "timemap/_mapping_form.html", RequestContext(request, {"form": form})
        ),
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
