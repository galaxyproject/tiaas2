from django.urls import path

from . import views

urlpatterns = [
    path("tiaas/new/", views.register, name="register"),
    path("tiaas/thanks/", views.thanks, name="thanks"),
    path("tiaas/stats/", views.stats, name="stats"),
    path("tiaas/stats.csv", views.stats_csv, name="stats_csv"),
    path("join-training/<training_id>/", views.join, name="join"),
    path("join-training/<training_id>/status/", views.status, name="status"),
]
