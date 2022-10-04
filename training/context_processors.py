"""Add variables to global template context."""

from django.conf import settings as app_settings


def settings(request):
    """Inject TIaaS settings."""
    return {
        "settings": {
            'TIAAS_DOMAIN': app_settings.TIAAS_DOMAIN,
            'TIAAS_OWNER_SITE': app_settings.TIAAS_OWNER_SITE,
            'TIAAS_OWNER': app_settings.TIAAS_OWNER,
            'TIAAS_EMAIL': app_settings.TIAAS_EMAIL,
            'TIAAS_SHOW_ADVERTISING': app_settings.TIAAS_SHOW_ADVERTISING,
            'TIAAS_RETAIN_CONTACT_REQUIRE_CONSENT': app_settings.TIAAS_RETAIN_CONTACT_REQUIRE_CONSENT,
            'TIAAS_GDPR_RETAIN_EXTRA_MONTHS': app_settings.TIAAS_GDPR_RETAIN_EXTRA_MONTHS,
            'TIAAS_EXPOSE_USERNAME': app_settings.TIAAS_EXPOSE_USERNAME,
            'TIAAS_SEND_EMAIL_TO': app_settings.TIAAS_SEND_EMAIL_TO,
            'TIAAS_SEND_EMAIL_FROM': app_settings.TIAAS_SEND_EMAIL_FROM,
            'TIAAS_SEND_EMAIL_TO_REQUESTER': app_settings.TIAAS_SEND_EMAIL_TO_REQUESTER,
            'TIAAS_LATE_REQUEST_PREVENTION_DAYS': app_settings.TIAAS_LATE_REQUEST_PREVENTION_DAYS,
        },
    }
