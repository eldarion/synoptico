from django import forms
from django.core.urlresolvers import reverse

from .models import Event, TimelineMapping


class TimelineMappingForm(forms.ModelForm):

    offset = forms.CharField()
    event_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    event_description = forms.CharField(required=False)

    class Meta:
        model = TimelineMapping
        fields = [
            "offset",
            "event_pk",
            "event_description"
        ]

    def __init__(self, *args, **kwargs):
        self.timeline = kwargs.pop("timeline")
        super(TimelineMappingForm, self).__init__(*args, **kwargs)
        self.fields["event_description"].widget.attrs["data-ac-url"] = reverse(
            "ajax_autocomplete_events",
            args=[self.timeline.project.pk]
        )
        self.instance.timeline = self.timeline
        self.fields["offset"].label = self.timeline.offset_label()

    def clean_offset(self):
        offset = self.cleaned_data["offset"]
        TimelineMapping.validate_offset(self.timeline, offset)
        return offset

    def save(self, who):
        if self.cleaned_data["event_pk"] is not None:
            event = Event.objects.get(pk=self.cleaned_data["event_pk"])
        else:
            event = Event.objects.create(
                project=self.timeline.project,
                description=self.cleaned_data["event_description"],
                created_by=who
            )
        mapping = self.timeline.mappings.create(
            event=event,
            offset=self.cleaned_data["offset"],
            created_by=who
        )
        return mapping
