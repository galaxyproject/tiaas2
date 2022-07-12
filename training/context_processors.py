"""Add variables to global template context."""

from django.conf import settings as app_settings


def settings(request):
    """Inject TIaaS settings."""
    return {
        'settings': app_settings,
    }
