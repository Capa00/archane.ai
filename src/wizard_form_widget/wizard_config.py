# myapp/wizard_configs.py

WIZARD_CONFIGS = {
    "wizard1": {
        "steps": {
            "step1": {
                "form_class": "wizard_form_widget.forms.Step1Form",
                # Logica condizionale sul campo "tipo"
                "next": {
                    "branch_field": "tipo",
                    "cases": {
                        "A": "step2A",
                        "B": "step2B"
                    },
                    "default": "step2Default"
                }
            },
            "step2A": {
                "form_class": "wizard_form_widget.forms.Step2AForm",
                "next": None,  # Fine del wizard
            },
            "step2B": {
                "form_class": "wizard_form_widget.forms.Step2BForm",
                "next": None,
            },
            "step2Default": {
                "form_class": "wizard_form_widget.forms.Step2DefaultForm",
                "next": None,
            }
        },
        "initial_step": "step1"
    },
    # Puoi aggiungere altre configurazioni, per esempio:
    "wizard2": {
        "steps": {
            # ... altra configurazione ...
        },
        "initial_step": "step1"
    },
}
