import string
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from . import models
from .validators import validate_start_date

from django.utils import timezone

IDENTIFIER_ALLOWED_CHARS = (
    string.ascii_lowercase
    + string.digits
    + '-'
)


class TrainingForm(forms.ModelForm):
    """Define training request form."""

    error_css_class = 'error'

    class Meta:
        """Define form metadata."""

        model = models.Training
        fields = (
            "name",
            "email",
            "retain_contact",
            "title",
            "description",
            "start",
            "end",
            "website",
            "location",
            "blogpost",
            "use_gtn",
            "gtn_links",
            "non_gtn_links",
            "attendance",
            "training_identifier",
            "advertise",
            "other_requests",
        )

        labels = {
            "name": "Full name",
            "title": "Title of your training event",
            "email": "Contact email",
            "retain_contact": (
                "Permission to retain your contact information for"
                f" {settings.TIAAS_GDPR_RETAIN_EXTRA_MONTHS} months"
            ),
            "description": "Brief overview of your planned workshop content",
            "start": "Start of your course",
            "end": "End of your course",
            "website": "URL of your training website/materials (if available)",
            "location": "Training Location",
            "use_gtn":
                "Will you be using official Galaxy Training materials?",
            "gtn_links": "Official Training Material",
            "non_gtn_links": "Other Training Materials",
            "attendance": "Expected number of participants (approximate)",
            "advertise": (
                "Would you like us to advertise your workshop on"
                f" {settings.TIAAS_OWNER}?"),
            "other_requests": "Anything else?",
            "blogpost": "I will consider writing a blog post",
        }
        help_texts = {
            "use_gtn": (
                'These are available on the <a href="'
                'https://training.galaxyproject.org/training-material/'
                '" target="_blank"> Galaxy Training Network</a>.'),
            "advertise": (
                "We will create an event article that will be visible on"
                f' <a href="{settings.TIAAS_OWNER_SITE}">'
                f'{settings.TIAAS_OWNER_SITE}</a>'),
            "gtn_links": (
                "If you are using official training materials: which ones?"
                " Please provide the topic and material name, or URLs so we"
                " can find it."),
            "non_gtn_links": (
                "If not using official training materials, can you provide"
                " URLs to your workflows, or just simply a list of all tool"
                " IDs that you will run. We need the internal Galaxy tool IDs"
                " (if you right click a tool in the Galaxy UI and copy link"
                " location, the link will contain the tool ID)."),
            "retain_contact": (
                "If you consent we will retain your information for a longer"
                f" period of time ({settings.TIAAS_GDPR_RETAIN_EXTRA_MONTHS}"
                " months). We will use this to contact you regarding"
                " letters of support for our continued funding, and similar"
                " matters."),
            "blogpost": (
                "Would you be willing to write a blogpost after your event,"
                " summarising your experience with TIaaS and how it helped"
                " you?"),
            "training_identifier": (
                "A unique name to help identify your training resources."
                " Please use only lowercase letters, numbers and dash (-)"
                " characters. 20 characters maximum."),
        }

        widgets = {
            "start": forms.SelectDateWidget(),
            "end": forms.SelectDateWidget(),
            "title": forms.TextInput(),
            "description": forms.Textarea(attrs={'rows': 4}),
            "gtn_links": forms.Textarea(attrs={'rows': 4}),
            "non_gtn_links": forms.Textarea(attrs={'rows': 4}),
            "attendance": forms.NumberInput(attrs={"min": 1}),
            "other_requests": forms.Textarea(attrs={'rows': 4}),
        }

    @property
    def all_error_messages(self):
        """Return list items from self.errors.

        self.errors is a dict-like collection with values as lists. We only
        need the list items.
        """
        return [e for elist in self.errors.values() for e in elist]

    def clean_start(self):
        start = self.cleaned_data['start']
        now = timezone.now().date()
        validate_start_date(start)

        if (
                'apology' in self.data
                and self.data['apology'] == "I am very sorry"):
            # They're allowed to submit it.
            return start
        else:
            if (start - now).days < settings.TIAAS_LATE_REQUEST_PREVENTION:
                raise ValidationError(
                    "Unfortunately you are too late to submit this"
                    " start date.")

        return start

    def clean_end(self):
        data = self.cleaned_data['end']
        now = timezone.now().date()
        if data < now:
            raise ValidationError("This event would have already ended")
        return data

    def clean_training_identifier(self):
        """Validate that identifier complies with requirements."""
        identifier = self.cleaned_data['training_identifier'].lower()
        allowed = set(IDENTIFIER_ALLOWED_CHARS)
        submitted = set(identifier)
        if submitted - allowed:
            for i, char in enumerate(identifier):
                if char not in IDENTIFIER_ALLOWED_CHARS:
                    raise ValidationError(
                        f'Invalid character "{char}" at position {i + 1}.'
                    )
            # Should never get to this point, but let's catch anyway
            raise ValidationError(
                "Invalid character(s) in submitted identifier.")
        return identifier
