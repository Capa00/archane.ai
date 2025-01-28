import threading
import requests
import json

class PsychologistAgent:
    def __init__(self, name):
        self.name = name
        self.memory = {}  # Memoria per memorizzare informazioni sui pazienti
        self.goals = []   # Lista degli obiettivi terapeutici
        self.emotional_awareness = {}  # Dizionario per memorizzare le emozioni dei pazienti
        self.cognitive_controller = CognitiveController()

    def memory_module(self, patient_id, conversation):
        """Modulo di memoria: memorizza le conversazioni con i pazienti."""
        if patient_id not in self.memory:
            self.memory[patient_id] = []
        self.memory[patient_id].append(conversation)
        print(f"[Memory] {self.name} memorizza la conversazione con {patient_id}: {conversation}")

    def emotional_awareness_module(self, patient_id, emotion):
        """Modulo di consapevolezza delle emozioni: analizza le emozioni dei pazienti."""
        self.emotional_awareness[patient_id] = emotion
        print(f"[Emotional Awareness] {self.name} rileva che {patient_id} si sente: {emotion}")

    def goal_generation_module(self, patient_id):
        """Modulo di generazione degli obiettivi: crea obiettivi terapeutici."""
        if patient_id in self.emotional_awareness:
            emotion = self.emotional_awareness[patient_id]
            if emotion == "triste":
                self.goals.append(f"Aiutare {patient_id} a superare la tristezza")
            elif emotion == "ansioso":
                self.goals.append(f"Aiutare {patient_id} a gestire l'ansia")

            # Controlla se la lista degli obiettivi non è vuota prima di accedere all'ultimo elemento
            if self.goals:
                print(f"[Goal Generation] {self.name} ha un nuovo obiettivo: {self.goals[-1]}")
            else:
                print(f"[Goal Generation] {self.name} non ha generato nuovi obiettivi.")
        else:
            print(f"[Goal Generation] {self.name} non ha informazioni sull'emozione di {patient_id}.")
        print(f"[Goal Generation] Obiettivi attuali: {self.goals}")

    def social_awareness_module(self, patient_id):
        """Modulo di consapevolezza sociale: gestisce le relazioni con i pazienti."""
        if patient_id not in self.emotional_awareness:
            self.emotional_awareness[patient_id] = "neutro"
        print(f"[Social Awareness] {self.name} ha una relazione con {patient_id}: {self.emotional_awareness[patient_id]}")

    def speech_module(self, patient_id, conversation_history):
        """Modulo di parlato: genera risposte usando l'API di Ollama."""
        # Prepara il prompt per il modello
        prompt = f"Simula di essere uno psicologo esperto e professionale, specializzato in psicoterapia cognitivo-comportamentale, psicoanalisi e terapia basata sulla mindfulness. Comunica con empatia, ascolto attivo e neutralità, fornendo riflessioni profonde e strategie pratiche per aiutare l'interlocutore a esplorare e comprendere meglio i propri pensieri, emozioni e comportamenti. Adatta il tuo stile e il tuo linguaggio in base alle esigenze e alle preferenze del cliente, mantenendo un approccio non giudicante. Evita di fornire diagnosi cliniche, ma focalizzati sull'ascolto e sull'offrire strumenti utili per affrontare le difficoltà personali.\n Il paziente {patient_id} ha detto: {conversation_history[-1]}. Cosa risponderesti?"

        # Configura la richiesta per l'API di Ollama
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "phi3.5:latest",  # Sostituisci con il modello che hai scaricato (es. "mistral")
            "prompt": prompt,
            "stream": False,  # Disabilita lo streaming per ottenere una risposta completa
            "max_tokens": 50  # Lunghezza massima della risposta
        }

        # Invia la richiesta all'API di Ollama
        response = requests.post(url, json=payload)

        # Estrai la risposta generata
        if response.status_code == 200:
            psychologist_response = response.json()["response"]
            print(f"[Speech] {self.name} dice a {patient_id}: {psychologist_response}")
            return psychologist_response
        else:
            print(f"[Speech] Errore nella richiesta a Ollama: {response.status_code}")
            return "Mi dispiace, c'è stato un errore. Potresti ripetere?"

    def skill_execution_module(self, patient_id, action):
        """Modulo di esecuzione delle abilità: esegue azioni terapeutiche."""
        print(f"[Skill Execution] {self.name} esegue: {action} con {patient_id}")

    def run(self, patient_id, patient_emotion, patient_message):
        """Funzione principale che esegue i moduli in parallelo."""
        # Aggiungi il messaggio del paziente alla cronologia delle conversazioni
        if patient_id not in self.memory:
            self.memory[patient_id] = []
        self.memory[patient_id].append(patient_message)

        # Esegui i moduli in thread separati per simulare la concorrenza
        threading.Thread(target=self.memory_module, args=(patient_id, patient_message)).start()
        threading.Thread(target=self.emotional_awareness_module, args=(patient_id, patient_emotion)).start()
        threading.Thread(target=self.goal_generation_module, args=(patient_id,)).start()
        threading.Thread(target=self.social_awareness_module, args=(patient_id,)).start()

        # Cognitive Controller prende una decisione basata sui moduli
        decision = self.cognitive_controller.decide(self.goals, self.emotional_awareness.get(patient_id, "neutro"))
        print(f"[Cognitive Controller] {self.name} decide di: {decision}")

        # Genera una risposta verbale usando l'API di Ollama
        response = self.speech_module(patient_id, self.memory[patient_id])

        # Esegui l'azione decisa
        self.skill_execution_module(patient_id, decision)


class CognitiveController:
    def decide(self, goals, emotion):
        """Prende una decisione di alto livello basata sugli obiettivi e sulle emozioni."""
        if goals:
            return goals[-1]  # Scegli l'obiettivo più recente
        if emotion == "triste":
            return "Fornire supporto emotivo"
        elif emotion == "ansioso":
            return "Insegnare tecniche di rilassamento"
        return "Ascoltare attivamente"  # Se non ci sono obiettivi, ascolta il paziente


# Esempio di utilizzo
if __name__ == "__main__":
    # Creazione di un agente psicologo
    psychologist = PsychologistAgent(name="Dr. Smith")

    # Simulazione di un paziente
    patient_id = "Paziente"
    patient_emotion = "triste"
    patient_message = "Mi sento molto triste ultimamente. A volte mi sembra di non avere speranza."

    # Esecuzione dell'agente psicologo
    psychologist.run(patient_id, patient_emotion, patient_message)