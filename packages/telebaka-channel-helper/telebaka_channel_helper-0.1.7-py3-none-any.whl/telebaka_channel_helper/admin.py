from django.contrib import admin

from .models import PlannedPost


@admin.register(PlannedPost)
class PlannedPostAdmin(admin.ModelAdmin):
    pass
