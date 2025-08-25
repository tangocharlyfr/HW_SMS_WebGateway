# Utilise Python officiel
FROM python:3.12-slim

# Installe les paquets système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crée le dossier de l'application
WORKDIR /app

# Copie les fichiers requirements et installe les packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer ping
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

# Copie les scripts
COPY huawei_sms_server.py .
COPY healthcheck.py .
COPY gunicorn.logs.py . 

# Expose le port utilisé par l'application
EXPOSE 8080

# Lance le serveur Flask avec Gunicorn et logs activés
CMD ["gunicorn", "-c", "gunicorn.logs.py", "-w", "1", "--threads", "4", "-b", "0.0.0.0:8080", "--error-logfile", "-", "huawei_sms_server:app"]
