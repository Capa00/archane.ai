from django.db import models, transaction
from django_jsonform.models.fields import JSONField

class Agent(models.Model):
    # SETTINGS_SCHEMA = {
    #     "$schema": "https://json-schema.org/draft/2020-12/schema",
    #     "title": "Social Media Strategy Brief",
    #     "description": "Schema per la raccolta di informazioni per una strategia social media personalizzata.",
    #     "type": "object",
    #     "properties": {
    #         "brand": {
    #             "type": "object",
    #             "properties": {
    #                 "name": {"type": "string", "description": "Nome del brand o azienda"},
    #                 "industry": {
    #                     "type": "string",
    #                     "format": "textarea",
    #                     "description": "Descrizione dettagliata del settore di riferimento"
    #                 },
    #                 "website": {"type": "string", "format": "uri", "description": "Sito web ufficiale"},
    #                 "social_media_accounts": {
    #                     "type": "array",
    #                     "items": {"type": "string", "format": "uri"},
    #                     "description": "Elenco degli account social media attuali"
    #                 }
    #             },
    #             "required": ["name", "industry"]
    #         },
    #         "goals": {
    #             "type": "array",
    #             "items": {
    #                 "type": "string",
    #                 "enum": [
    #                     "aumentare_visibilita",
    #                     "generare_vendite",
    #                     "migliorare_engagement",
    #                     "creare_community",
    #                     "lanciare_prodotto",
    #                     "altro"
    #                 ]
    #             },
    #             "description": "Obiettivi principali della strategia"
    #         },
    #         "target_audience": {
    #             "type": "object",
    #             "properties": {
    #                 "age_range": {
    #                     "type": "string",
    #                     "description": "Fascia di età del pubblico target"
    #                 },
    #                 "gender": {
    #                     "type": "string",
    #                     "enum": ["maschile", "femminile", "tutti"],
    #                     "description": "Genere principale del pubblico"
    #                 },
    #                 "interests": {
    #                     "type": "array",
    #                     "items": {"type": "string"},
    #                     "description": "Principali interessi del pubblico target"
    #                 },
    #                 "problems_solved": {
    #                     "type": "string",
    #                     "description": "Problemi o necessità che il brand risolve"
    #                 }
    #             }
    #         },
    #         "platforms": {
    #             "type": "array",
    #             "items": {
    #                 "type": "string",
    #                 "enum": [
    #                     "instagram",
    #                     "facebook",
    #                     "tiktok",
    #                     "linkedin",
    #                     "youtube",
    #                     "twitter",
    #                     "pinterest",
    #                     "altro"
    #                 ]
    #             },
    #             "description": "Piattaforme social su cui il brand vuole essere attivo"
    #         },
    #         "tone_of_voice": {
    #             "type": "string",
    #             "enum": [
    #                 "professionale",
    #                 "amichevole",
    #                 "ispirazionale",
    #                 "ironico",
    #                 "elegante",
    #                 "altro"
    #             ],
    #             "description": "Stile e tono di voce del brand"
    #         },
    #         "content_types": {
    #             "type": "array",
    #             "items": {
    #                 "type": "string",
    #                 "enum": [
    #                     "post_grafici",
    #                     "video_brevi",
    #                     "stories",
    #                     "blog_post",
    #                     "infografiche",
    #                     "live_streaming",
    #                     "recensioni",
    #                     "altro"
    #                 ]
    #             },
    #             "description": "Tipologia di contenuti da pubblicare"
    #         },
    #         "posting_frequency": {
    #             "type": "object",
    #             "properties": {
    #                 "feed_posts_per_week": {"type": "integer", "description": "Numero di post nel feed a settimana"},
    #                 "stories_per_day": {"type": "integer", "description": "Numero di stories giornaliere"},
    #                 "videos_per_month": {"type": "integer", "description": "Numero di video (Reels/TikTok) al mese"}
    #             }
    #         },
    #         "call_to_action": {
    #             "type": "string",
    #             "description": "Azione principale che si vuole far compiere agli utenti"
    #         },
    #         "important_links": {
    #             "type": "array",
    #             "items": {"type": "string", "format": "uri"},
    #             "description": "Link utili da includere nelle pubblicazioni"
    #         }
    #     },
    #     "required": ["brand", "goals", "platforms"]
    # }

    name = models.CharField(max_length=50)

    def get_state(self):
        state = {}
        for module in self.modules.all():
            state[module.name] = module.output
        return state

    def duplicate(self) -> "Agent":
        with transaction.atomic():
            dup_agent = Agent.objects.create(
                name=f"{self.name} (copy)",
            )
            for module in self.modules.all():
                dup_module = module.duplicate()
                dup_module.agents.clear()
                dup_module.agents.add(dup_agent)
            return dup_agent

    def __str__(self):
        return f"Agent - {self.name}"
