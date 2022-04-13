"""Add variables to global template context."""

from django.conf import settings as app_settings


def settings(request):
    """Inject TIaaS settings."""
    return {
        'settings': {
            'TIAAS_OWNER': app_settings.TIAAS_OWNER,
            'TIAAS_OWNER_SITE': app_settings.TIAAS_OWNER_SITE,
            'TIAAS_GALAXY_SITE': app_settings.TIAAS_GALAXY_SITE,
            'TIAAS_SHOW_ADVERTISING': app_settings.TIAAS_SHOW_ADVERTISING,
            'TIAAS_GDPR_RETAIN_EXTRA': app_settings.TIAAS_GDPR_RETAIN_EXTRA,
        },
    }
