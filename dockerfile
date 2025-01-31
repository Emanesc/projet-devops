# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port 5000
EXPOSE 5000

# Commande par défaut pour lancer l'application
CMD ["python", "app.py"]
