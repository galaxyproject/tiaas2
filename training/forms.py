from django import forms
from django.conf import settings
from django_countries.widgets import CountrySelectWidget

from . import models
from .validators import validate_start_date

from django.core.exceptions import ValidationError
from django.utils import timezone


class TrainingForm(forms.ModelForm):

    error_css_class = 'error'

    @property
    def all_error_messages(self):
        # self.errors is a dict-like collection with values as lists; we only need the list items
        return [e for elist in self.errors.values() for e in elist]

    def clean_start(self):
        start = self.cleaned_data['start']
        now = timezone.now().date()
        validate_start_date(start)

        if 'apology' in self.data and self.data['apology'] == "I am very sorry":
            # They're allowed to submit it.
            return start
        else:
            if (start - now).days < settings.TIAAS_LATE_REQUEST_PREVENTION:
                raise ValidationError("You are too late to submit this, unfortunately.")

        return start

    def clean_end(self):
        data = self.cleaned_data['end']
        now = timezone.now().date()
        if data < now:
            raise ValidationError("This event would have already ended")
        return data

    class Meta:
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
            "advertise_eu",
            "other_requests",
        )

        labels = {
            "title": "Training title",
            "email": "Contact email",
            "retain_contact":
                "Permission to retain your contact information for %s months"
                % settings.TIAAS_GDPR_RETAIN_EXTRA,
            "description": "Brief overview of the Training Course",
            "start": "Start of your course",
            "end": "End of your course",
            "website": "Training website (if available)",
            "location": "Training location",
            "use_gtn": "Will you be using official Galaxy Training materials? ",
            "gtn_links": "Official training material",
            "non_gtn_links": "Other training materials",
            "attendance": "Approximately how many people do you expect to attend?",
            "advertise_eu": "Would you like us to advertise this on useGalaxy.eu?",
            "other_requests": "Anything else?",
            "blogpost": "Write us a blogpost?",
        }
        help_texts = {
            "description":
                "Just tell us briefly about the training, what topics you'll cover, etc.",
            "use_gtn": "Those available on https://training.galaxyproject.org/training-material/",
            "advertise_eu":
                'We can create an "event" and direct users in your region to your training event.'
                "E.g https://usegalaxy-eu.github.io/event/2017-11-16-Announcement-Galaxy-course/",
            "location": "Country where it is hosted, used in aggregate statistics",
            "gtn_links":
                "If you are using official training materials: which ones? Please provide the "
                "topic + material name, or URLs so we can find it.",
            "non_gtn_links":
                "If not using official training materials, please provide URLs to your workflows, "
                "or just simply a list of all tool IDs that you will run. We need the internal "
                "Galaxy tool IDs (if you right click a tool in the Galaxy UI + copy link location, "
                " this will provide the tool ID in the URL)",
            "name": "First name is fine, however you wish to be addressed in emails",
            "retain_contact":
                "If you consent we will retain your information for a longer period of time. We "
                "will use this to contact you regarding letters of support for our continued "
                "funding, and similar matters.",
            "blogpost":
                "Would you be willing to write a blogpost after your event, summarising your "
                "experience with TIaaS and how it helped you?",
            "training_identifier":
                "Training identifier should consist of lowercase letters, numbers, underscores "
                "or hyphens.",
        }

        widgets = {
            "country": CountrySelectWidget(),
            "start": forms.SelectDateWidget(),
            "end": forms.SelectDateWidget(),
            "title": forms.TextInput(),
            "description": forms.TextInput(),
            "attendance": forms.NumberInput(attrs={"min": 1}),
        }
