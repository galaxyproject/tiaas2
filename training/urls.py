from django.urls import path
from django.shortcuts import redirect

from . import views


# Useful for development
def redirect_about(request):
    return redirect('/tiaas/')


urlpatterns = [
    path("", redirect_about, name="about"),
    path("tiaas/", views.about, name="about"),
    path("tiaas/new/", views.register, name="register"),
    path("tiaas/thanks/", views.thanks, name="thanks"),
    path("tiaas/stats/", views.stats, name="stats"),
    path("tiaas/stats.csv", views.stats_csv, name="stats_csv"),
    path("tiaas/numbers.csv", views.numbers_csv, name="numbers_csv"),
    path("tiaas/calendar/", views.calendar_view, name="calendar"),
    path("join-training/<training_id>/", views.join, name="join"),
    path("join-training/<training_id>/status/", views.status, name="status"),
]
