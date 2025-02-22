from django.contrib import admin

from modules.admin import JSONWidgetAdminMixin
from .forms.admin import MemoryAdminForm
from .models import Memory

class MemoryAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    form = MemoryAdminForm

admin.site.register(Memory, MemoryAdmin)
