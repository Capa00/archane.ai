# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Altri URL della tua app…
    path('get_step_form/', views.get_step_form, name='get_step_form'),
    path('validate_step/', views.validate_step, name='validate_step'),
]
