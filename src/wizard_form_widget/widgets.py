# myapp/widgets.py

import json
from django import forms

from wizard_form_widget.wizard_config import WIZARD_CONFIGS


class JsonWizardWidget(forms.Widget):
    template_name = 'widgets/json_wizard_widget.html'

    def __init__(self, config_id=None, attrs=None):
        """
        Il parametro config_id è obbligatorio e deve corrispondere ad una chiave in WIZARD_CONFIGS.
        """
        super().__init__(attrs)
        if config_id is None:
            raise ValueError("Devi specificare un config_id per JsonWizardWidget.")
        self.config_id = config_id
        self.config = WIZARD_CONFIGS.get(config_id)
        if self.config is None:
            raise ValueError(f"Configurazione non trovata per config_id: {config_id}")

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Passiamo l'id della configurazione al template
        context['config_id'] = self.config_id
        # Il campo JSON (valore) viene gestito come stringa
        if isinstance(value, dict):
            value = json.dumps(value)
        context['field_value'] = value if value else '{}'
        context['field_name'] = name
        return context

    def format_value(self, value):
        if isinstance(value, dict):
            return json.dumps(value)
        return value or '{}'

    def value_from_datadict(self, data, files, name):
        # L'input nascosto trasmette il JSON aggregato
        return data.get(name, '{}')
