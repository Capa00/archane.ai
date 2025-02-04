# myapp/views.py

import importlib
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from wizard_form_widget.wizard_config import WIZARD_CONFIGS


def import_class(path):
    """Importa una classe a partire dal percorso (stringa)"""
    module_name, class_name = path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def get_step_form(request):
    """
    Restituisce il form HTML per lo step richiesto.
    Parametri GET: config_id, (step opzionale) e prefix.
    Se "step" non viene passato, si usa lo step iniziale definito nella configurazione.
    """
    config_id = request.GET.get("config_id")
    prefix = request.GET.get("prefix")
    if not config_id or not prefix:
        return HttpResponse("Parametri mancanti (config_id o prefix)", status=400)
    wizard_conf = WIZARD_CONFIGS.get(config_id)
    if not wizard_conf:
        return HttpResponse("Configurazione wizard non trovata", status=400)

    # Se non viene passato "step", si usa l'iniziale definita nella configurazione
    step = request.GET.get("step") or wizard_conf.get("initial_step")
    step_conf = wizard_conf['steps'].get(step)
    if not step_conf:
        return HttpResponse("Step non valido", status=400)
    form_class_path = step_conf.get("form_class")
    form_class = import_class(form_class_path)
    form = form_class(prefix=prefix)
    html = render_to_string("wizard/step_form.html", {"form": form})
    return HttpResponse(html)


def validate_step(request):
    """
    Valida i dati inviati per lo step corrente.
    Parametri GET: config_id, step, prefix.
    Restituisce un JSON contenente:
      - valid: true/false
      - cleaned_data (se valido)
      - errors (se non valido)
      - next_step (se la validazione ha successo, la view decide il prossimo step)
    """
    if request.method != "POST":
        return JsonResponse({"valid": False, "errors": {"__all__": ["Metodo non valido"]}}, status=400)
    config_id = request.GET.get("config_id")
    step = request.GET.get("step")
    prefix = request.GET.get("prefix")
    if not config_id or not step or not prefix:
        return JsonResponse({"valid": False, "errors": {"__all__": ["Parametri mancanti (config_id o step o prefix)"]}}, status=400)
    wizard_conf = WIZARD_CONFIGS.get(config_id)
    if not wizard_conf:
        return JsonResponse({"valid": False, "errors": {"__all__": ["Configurazione non trovata"]}}, status=400)
    step_conf = wizard_conf['steps'].get(step) or wizard_conf['steps'].get(wizard_conf['initial_step'])
    if not step_conf:
        return JsonResponse({"valid": False, "errors": {"__all__": ["Step non valido"]}}, status=400)
    form_class_path = step_conf.get("form_class")
    form_class = import_class(form_class_path)
    form = form_class(request.POST, prefix=prefix)
    if form.is_valid():
        # Determina il prossimo step, gestendo anche i rami condizionali
        if isinstance(step_conf.get("next"), dict):
            branch_field = step_conf["next"].get("branch_field")
            field_value = form.cleaned_data.get(branch_field)
            next_step = step_conf["next"]["cases"].get(field_value, step_conf["next"].get("default"))
        else:
            next_step = step_conf.get("next")
        return JsonResponse({"valid": True, "cleaned_data": form.cleaned_data, "next_step": next_step})
    else:
        return JsonResponse({"valid": False, "errors": form.errors})
