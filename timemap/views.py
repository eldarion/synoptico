from django.http import Http404
from django.views.generic import DetailView

from account.mixins import LoginRequiredMixin

from .models import Timeline


class TimelineDetailView(LoginRequiredMixin, DetailView):
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
