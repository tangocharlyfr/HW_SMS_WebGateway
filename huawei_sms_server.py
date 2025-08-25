from flask import Flask, request, jsonify
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
import logging
import threading
import queue
import time
import os

# --- CONFIGURATION ---
ROUTER_USER = os.getenv("ROUTER_USER")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")
ROUTER_IP = os.getenv("ROUTER_IP")
HUAWEI_URL = f"http://{ROUTER_USER}:{ROUTER_PASSWORD}@{ROUTER_IP}/"
DELAY_BEFORE_SMS = 2      # délai avant chaque envoi de SMS
DELAY_BETWEEN_SMS = 2     # délai entre 2 SMS
MAX_RETRIES = 3           # Nombre de tentatives Max
RETRY_DELAY = 2           # délai entre chaque tentative

# --- Logging configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# --- Flask app ---
app = Flask(__name__)

# --- Queue et lock ---
sms_queue = queue.Queue()
sms_lock = threading.Lock()

# --- Worker pour envoyer les SMS ---
def sms_worker():
    while True:
        tel, message = sms_queue.get()
        with sms_lock:
            time.sleep(DELAY_BEFORE_SMS)  # délai avant chaque envoi
            attempt = 0
            while attempt < MAX_RETRIES:
                try:
                    with Connection(HUAWEI_URL) as connection:
                        client = Client(connection)
                        client.sms.send_sms(tel, message)
                    logger.info(f"✅ SMS envoyé à {tel}")
                    break
                except Exception as e:
                    attempt += 1
                    if attempt < MAX_RETRIES:
                        logger.warning(f"❌ Tentative {attempt} échouée pour {tel}: {str(e)}, retry dans {RETRY_DELAY}s")
                        time.sleep(RETRY_DELAY)
                    else:
                        logger.error(f"❌ Échec après {MAX_RETRIES} tentatives pour {tel}: {str(e)}")
            time.sleep(DELAY_BETWEEN_SMS)  # délai entre 2 SMS
        sms_queue.task_done()

# --- Lancer le worker en thread daemon ---
threading.Thread(target=sms_worker, daemon=True).start()

# --- Logging des requêtes (avec filtre health check) ---
@app.before_request
def log_request_info():
    # Ignorer les health checks
    if request.path == '/' and request.remote_addr == '127.0.0.1':
        return
    logger.info(f"{request.method} {request.path} from {request.remote_addr} with args {request.args}")

# --- Route pour envoyer un SMS ---
@app.route('/sms/send.aspx', methods=['GET'])
def send_sms():
    tel = request.args.get('tel')
    message = request.args.get('message')

    if not tel or not message:
        return jsonify({"status": "error", "message": "Paramètres 'tel' et 'message' requis"}), 400

    # Ajouter à la queue
    sms_queue.put((tel, message))
    logger.info(f"📥 Ajouté à la queue : SMS vers {tel}")
    return jsonify({"status": "queued", "message": f"SMS ajouté à la queue pour {tel}"}), 200

# --- Lancement Flask ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
