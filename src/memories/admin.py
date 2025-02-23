from django.contrib import admin

from modules.admin.mixins import SchemaBasedAdminMixin
from .models import Memory

class MemoryAdmin(SchemaBasedAdminMixin, admin.ModelAdmin):
    schemas_mapping = {"schema": "data"}

admin.site.register(Memory, MemoryAdmin)
