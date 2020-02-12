from django.db import models
from datetime import date
from django_countries.fields import CountryField


class Training(models.Model):
    received = models.DateField("date received", default=date.today)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    title = models.TextField()
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()
    website = models.URLField(blank=True)
    location = CountryField(multiple=True, blank_label="(select country)")
    use_gtn = models.CharField(
        max_length=1, choices=(("Y", "Yes"), ("N", "No")), default="N"
    )
    gtn_links = models.TextField(blank=True)
    non_gtn_links = models.TextField(blank=True)
    attendance = models.TextField()
    training_identifier = models.CharField(max_length=12)
    advertise_eu = models.CharField(
        max_length=1, choices=(("Y", "Yes"), ("N", "No")), default="N"
    )

    other_requests = models.TextField(blank=True)
    # Internal
    processed = models.CharField(
        max_length=2,
        choices=(("UN", "unprocessed"), ("AP", "Approved"), ("RE", "Rejected")),
        default="UN",
    )

    @property
    def days_until(self):
        return (self.start - date.today()).days

    @property
    def days_since_received(self):
        return (date.today() - self.received).days

    @property
    def gdpr_clean(self):
        return (date.today() - self.end).days > 60

    @property
    def safe_email(self):
        if self.gdpr_clean:
            self.name = "GDPR Redacted"
            self.email = "<gdpr-redacted>"
            self.save()
            return f"gdpr-removed+{self.id}@localhost"
        else:
            return self.email

    @property
    def safe_name(self):
        if self.gdpr_clean:
            self.name = "GDPR Redacted"
            self.email = "<gdpr-redacted>"
            self.save()
            return f"Redacted"
        else:
            return self.name

    def __str__(self):
        return self.training_identifier
