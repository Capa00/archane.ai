# myapp/forms.py

from django import forms

from agents.models import Agent
from .widgets import JsonWizardWidget

### Form per il wizard (step-specific)
class Step1Form(forms.Form):
    tipo = forms.ChoiceField(choices=[("A", "Tipo A"), ("B", "Tipo B"), ("C", "Tipo C")])
    nome = forms.CharField(max_length=100)

class Step2AForm(forms.Form):
    campo_a = forms.CharField(max_length=100)
    valore_a = forms.IntegerField(min_value=0)

class Step2BForm(forms.Form):
    campo_b = forms.CharField(max_length=100)
    valore_b = forms.FloatField(min_value=0)

class Step2DefaultForm(forms.Form):
    campo_default = forms.CharField(max_length=100)
    valore_default = forms.CharField(max_length=100)

### ModelForm che utilizza il widget JSON wizard
class MyModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'
        widgets = {
            'settings': JsonWizardWidget(config_id="wizard1"),
        }
