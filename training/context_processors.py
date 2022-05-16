"""Add variables to global template context."""

from django.conf import settings as app_settings


def settings(request):
    """Inject TIaaS settings."""
    return {
        'settings': {
            'GIT_COMMIT_ID': app_settings.GIT_COMMIT_ID,
            'GIT_REMOTE_URL': app_settings.GIT_REMOTE_URL,
            'TIAAS_OWNER': app_settings.TIAAS_OWNER,
            'TIAAS_GALAXY_SITE': app_settings.TIAAS_GALAXY_SITE,
            'TIAAS_SHOW_ADVERTISING': app_settings.TIAAS_SHOW_ADVERTISING,
            'TIAAS_GDPR_RETAIN_EXTRA': app_settings.TIAAS_GDPR_RETAIN_EXTRA,
        },
    }
