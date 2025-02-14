import os

from django import forms
from django_jsonform.forms.fields import JSONFormField
from mdeditor.fields import MDTextFormField
from openai import OpenAI

from modules.action_registry import register_action, ActionFunction


@register_action("llm_openai_like")
class LLMOpenAILikeAction(ActionFunction):
    OUTPUT_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "output": {
                "type": "string"
            },
            "token": {
                "type": "integer"
            }
        },
        "required": ["output", "token"]
    }

    def get_config_form(self):
        return LLMOpenAILikeActionConfigForm

    def get_input_form(self):
        return LLMOpenAILikeActionInputForm

    def __call__(self, inputs, config):
        api_key = config.get('api_key') or os.environ.get("OPENAI_API_KEY")
        if config['base_url']:
            client = OpenAI(base_url=config['base_url'], api_key=api_key)
        else:
            client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(**config)
        return {"output": " ".join(inputs['input'])}


class LLMOpenAILikeActionInputForm(forms.Form):
    prompt_context = forms.CharField(widget=forms.Textarea, required=False)


class LLMOpenAILikeActionConfigForm(forms.Form):
    DATA_SCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "OpenAI Chat Completion Request",
        "type": "object",
        "description": "Schema per una richiesta di completamento chat all'API OpenAI.",
        "properties": {
            "model": {
                "type": "string",
                "description": "Il modello da utilizzare per la generazione del testo (es. 'gpt-3.5-turbo')."
            },
            # "audio": {
            #     "type": "object",
            #     "description": "Specifica il formato dell'output audio e la voce utilizzata per la risposta.",
            #     "properties": {
            #         "format": {
            #             "type": "string",
            #             "enum": ["wav", "mp3", "flac", "opus", "pcm16"],
            #             "description": "Formato dell'audio di output."
            #         },
            #         "voice": {
            #             "type": "string",
            #             "enum": ["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse"],
            #             "description": "La voce usata dal modello per rispondere."
            #         }
            #     },
            #     "required": ["format", "voice"]
            # },
            # "frequency_penalty": {
            #     "type": ["number", "null"],
            #     "description": "Penalizza la ripetizione delle parole nel completamento."
            # },
            # "function_call": {
            #     "type": ["object", "null"],
            #     "description": "Specifica se e come il modello deve chiamare una funzione.",
            #     "properties": {
            #         "name": {"type": "string", "description": "Nome della funzione da chiamare."},
            #         "arguments": {"type": "object", "description": "Parametri della funzione in formato JSON."}
            #     }
            # },
            # "functions": {
            #     "type": "array",
            #     "description": "Elenco delle funzioni che il modello può chiamare.",
            #     "items": {
            #         "type": "object",
            #         "properties": {
            #             "name": {"type": "string", "description": "Nome della funzione."},
            #             "description": {"type": "string", "description": "Descrizione della funzione."},
            #             "parameters": {"type": "object",
            #                            "description": "Definizione dei parametri della funzione in JSON Schema."}
            #         }
            #     }
            # },
            # "logit_bias": {
            #     "type": ["object", "null"],
            #     "description": "Mappa di token e del loro peso di probabilità. Le chiavi sono gli ID dei token (stringhe) e i valori sono interi tra -100 e 100.",
            #     "additionalProperties": {
            #         "type": "integer",
            #         "minimum": -100,
            #         "maximum": 100
            #     }
            # },
            # "logprobs": {
            #     "type": ["boolean", "null"],
            #     "description": "Se true, restituisce la probabilità logaritmica dei token generati."
            # },
            # "max_completion_tokens": {
            #     "type": ["integer", "null"],
            #     "description": "Numero massimo di token generati dal modello."
            # },
            "max_tokens": {
                "type": ["integer", "null"],
                "description": "Numero massimo di token totali (input + output)."
            },
            # "metadata": {
            #     "type": ["object", "null"],
            #     "description": "Metadati opzionali da includere nella richiesta.",
            #     "properties": {
            #         "request_id": {
            #             "type": "string",
            #             "description": "Identificatore univoco della richiesta."
            #         },
            #         "timestamp": {
            #             "type": "string",
            #             "format": "date-time",
            #             "description": "Timestamp della richiesta in formato ISO 8601."
            #         },
            #         "user_info": {
            #             "type": "object",
            #             "description": "Informazioni opzionali sull'utente.",
            #             "properties": {
            #                 "user_id": {
            #                     "type": "string",
            #                     "description": "Identificatore univoco dell'utente."
            #                 },
            #                 "role": {
            #                     "type": "string",
            #                     "description": "Ruolo dell'utente, ad esempio 'admin', 'editor', 'viewer'."
            #                 }
            #             }
            #         },
            #         "tags": {
            #             "type": "array",
            #             "description": "Lista di tag associati alla richiesta.",
            #             "items": {
            #                 "type": "string"
            #             }
            #         }
            #     },
            #     "additionalProperties": True
            # },
            # "modalities": {
            #     "type": ["array", "null"],
            #     "description": "Modalità di output (es. 'text', 'image', 'audio').",
            #     "items": {"type": "string"}
            # },
            # "n": {
            #     "type": ["integer", "null"],
            #     "description": "Numero di completamenti da generare."
            # },
            # "parallel_tool_calls": {
            #     "type": "boolean",
            #     "description": "Se true, consente più chiamate di strumenti contemporaneamente."
            # },
            # "prediction": {
            #     "type": ["object", "null"],
            #     "description": "Parametri relativi alla predizione del completamento."
            # },
            # "presence_penalty": {
            #     "type": ["number", "null"],
            #     "description": "Penalizza la generazione di parole già presenti nel prompt."
            # },
            # "reasoning_effort": {
            #     "type": "string",
            #     "description": "Livello di impegno cognitivo richiesto per la risposta."
            # },
            # "response_format": {
            #     "type": "string",
            #     "description": "Formato della risposta del modello."
            # },
            # "seed": {
            #     "type": ["integer", "null"],
            #     "description": "Seme casuale per generare risposte riproducibili."
            # },
            # "service_tier": {
            #     "type": ["string", "null"],
            #     "enum": ["auto", "default"],
            #     "description": "Livello di servizio della richiesta."
            # },
            # "stop": {
            #     "type": ["string", "array", "null"],
            #     "description": "Stringhe che indicano dove interrompere l'output."
            # },
            # "store": {
            #     "type": ["boolean", "null"],
            #     "description": "Se true, la richiesta viene salvata per analisi future."
            # },
            # "stream": {
            #     "type": ["boolean", "null"],
            #     "description": "Se true, la risposta viene trasmessa in streaming."
            # },
            # "stream_options": {
            #     "type": ["object", "null"],
            #     "description": "Opzioni per la gestione dello streaming dei dati."
            # },
            "temperature": {
                "type": ["number", "null"],
                "description": "Controlla la casualità dell'output. Valori più bassi rendono il modello più deterministico."
            },
            # "tool_choice": {
            #     "type": ["object", "null"],
            #     "description": "Specifica quale strumento deve essere usato per la risposta."
            # },
            # "tools": {
            #     "type": "array",
            #     "description": "Elenco degli strumenti disponibili per la richiesta.",
            #     "items": {"type": "object"}
            # },
            # "top_logprobs": {
            #     "type": ["integer", "null"],
            #     "description": "Numero di token con le probabilità più alte da restituire."
            # },
            # "top_p": {
            #     "type": ["number", "null"],
            #     "description": "Filtraggio basato su nucleare sampling (Top-P)."
            # },
            # "user": {
            #     "type": "string",
            #     "description": "Identificatore dell'utente che effettua la richiesta."
            # },
            # "extra_headers": {
            #     "type": ["object", "null"],
            #     "description": "Header HTTP aggiuntivi da includere nella richiesta."
            # },
            # "extra_query": {
            #     "type": ["object", "null"],
            #     "description": "Parametri di query extra per la richiesta HTTP."
            # },
            # "extra_body": {
            #     "type": ["object", "null"],
            #     "description": "Corpo della richiesta HTTP aggiuntivo."
            # },
            # "timeout": {
            #     "type": ["number", "object", "null"],
            #     "description": "Tempo massimo di attesa della risposta."
            # }
        },
        "required": ["model"]
    }

    system_prompt = MDTextFormField(required=False)
    prompt_context = forms.CharField(required=False)
    data = JSONFormField(schema=DATA_SCHEMA, required=False)
