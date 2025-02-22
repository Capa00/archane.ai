from django import forms


class TestForm(forms.Form):
    pippo = forms.CharField(max_length=25)