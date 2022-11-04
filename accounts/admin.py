from django.contrib import admin
from django.contrib.auth.models import Group

from accounts import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
