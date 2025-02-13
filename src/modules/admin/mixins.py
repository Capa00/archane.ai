from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget


class JSONWidgetAdminMixin:
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }