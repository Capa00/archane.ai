# Usa un'immagine ufficiale di Python basata su Debian 12 "bookworm".
FROM python:3.12-slim-bookworm

# Aggiungi un utente che sarà utilizzato nel container.
RUN useradd django

# Porta usata da questo container per servire HTTP.
EXPOSE 8000

# Imposta variabili di ambiente.
# 1. Forza Python per non fare buffering su stdout e stderr.
# 2. Imposta la variabile PORT che viene utilizzata da Gunicorn. Dovrebbe corrispondere alla porta definita con EXPOSE.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Installa pacchetti di sistema necessari da Wagtail e Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Installa il server applicativo (Gunicorn).
RUN pip install "gunicorn==20.0.4"

# Installa le dipendenze del progetto.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Usa la cartella /app come directory dove risiede il codice sorgente.
WORKDIR /app

# Imposta questa cartella come di proprietà dell'utente "django".
RUN chown django:django /app

# Copia il codice sorgente del progetto nel container.
COPY --chown=django:django . .

# Usa l'utente "django" per eseguire i comandi di build e il server.
USER django

# Colleziona i file statici.
RUN python manage.py collectstatic --noinput --clear

# Comando di runtime che viene eseguito quando viene chiamato "docker run".
# 1. Esegui le migrazioni del database.
# 2. Avvia il server dell'applicazione.
CMD set -xe; gunicorn project.wsgi:application
