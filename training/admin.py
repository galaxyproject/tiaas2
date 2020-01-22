from django.contrib import admin

# Register your models here.
from .models import Training


class TrainingAdmin(admin.ModelAdmin):
    pass
    list_display = (
        "training_identifier",
        "safe_email",
        "days_since_received",
        "days_until",
        "processed",
    )

    readonly_fields = (
        'received',
    )

    list_filter = ('processed', )


admin.site.register(Training, TrainingAdmin)
