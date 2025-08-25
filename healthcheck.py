import sys
import requests
import subprocess
import os

# Récupère l'IP du routeur depuis les variables d'environnement
HUAWEI_IP = os.getenv("ROUTER_IP")

if not HUAWEI_IP:
    print("❌ ERREUR : la variable d'environnement ROUTER_IP n'est pas définie")
    sys.exit(1)

# Test HTTP GET vers Gunicorn Web Server
try:
    r = requests.get("http://localhost:8080", timeout=5)
except requests.RequestException:
    print("❌ ERREUR : Gunicorn ne répond pas sur http://localhost:8080")
    sys.exit(1)

# Test Ping vers Huawei Router
try:
    subprocess.check_call(["ping", "-c", "1", "-W", "2", HUAWEI_IP])
except subprocess.CalledProcessError:
    print(f"❌ ERREUR : impossible de joindre le routeur {HUAWEI_IP}")
    sys.exit(1)

print(f"✅ Healthcheck OK : Gunicorn + Huawei router {HUAWEI_IP} joignables")
sys.exit(0)
