# Dockerfile pour le backend Flask
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt requirements_api.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_api.txt

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Créer les répertoires nécessaires
RUN mkdir -p /app/logs /app/uploads

# Exposer le port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=api.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "api:app"]
