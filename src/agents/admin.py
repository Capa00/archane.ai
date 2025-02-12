from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django_jsonform.widgets import JSONFormWidget

from agents.models import Agent

class BaseAdmin(admin.ModelAdmin):
    ...


class ModuleAdmin(BaseAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Sovrascrive i widget solo per `data_schema` e `output_schema`
        e lascia il widget predefinito per `data` e `output`.
        """
        if db_field.name in ["data_schema", "output_schema"]:
            kwargs["widget"] = JSONEditorWidget

        if db_field.name in ["data", "output"]:
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                instance = self.model.objects.get(pk=obj_id)
                schema = getattr(instance, f"get_{db_field.name}_schema")()
            else:
                schema = {"type": "object", "properties": {}}
            kwargs["widget"] = JSONFormWidget(schema=schema)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ModuleInline(admin.StackedInline):
    max_num = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Sovrascrive i widget solo per `data_schema` e `output_schema`
        e lascia il widget predefinito per `data` e `output`.
        """
        if db_field.name in ["data_schema", "output_schema"]:
            kwargs["widget"] = JSONEditorWidget

        if db_field.name in ["data", "output"]:
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                instance = self.model.objects.get(agent__id=obj_id)
                schema = getattr(instance, f"get_{db_field.name}_schema")()
            else:
                schema = {"type": "object", "properties": {}}
            kwargs["widget"] = JSONFormWidget(schema=schema)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class AgentAdmin(BaseAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

admin.site.register(Agent, AgentAdmin)
