# ✉️ HW_SMS_WebGateway

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)

Une Web passerelle SMS pour les routeurs Huawei LTE via l'API huawei-lte-api

## 📑 Table des matières

- [Description technique](#⚙️-description-technique)  
- [Installation classique via Docker](#⚙️-installation-classique-via-docker)  
- [Installation via Portainer](#🖥️-installation-via-portainer-deploy-from-repository)

---

## ⚙️ Description technique

Cette application est une **Gateway SMS** développée en **Python (Flask)**.  
Elle permet d’envoyer des SMS via un modem **Huawei** en exposant une **API HTTP simple**.

Exemple d'utilisation : 
- Configurer des alertes SMS sur votre monitoring Zabbix ou PRTG.
- Intégrer des alertes SMS dans n'importe quel script.

---

### 🔄 Fonctionnement

#### 1. Réception des requêtes HTTP
- **Route disponible** : `/sms/send.aspx`
- **Paramètres** :
  - `tel` → numéro de téléphone du destinataire
  - `message` → contenu du SMS

✅ Exemple d’appel :  
`curl "http://Host_IP:8282/sms/send.aspx?tel=0612345678&message=Hello+World"`

#### 2. Ajout à la file d’attente
Chaque SMS est placé dans une **queue interne** afin d’être traité de manière asynchrone.

#### 3. Traitement par un worker
Un **worker en arrière-plan** prend en charge les SMS et applique :
- ⏳ Un délai configurable avant chaque envoi (`DELAY_BEFORE_SMS`)  
- 🕒 Un délai entre deux SMS consécutifs (`DELAY_BETWEEN_SMS`)  
- 🔁 Des retries automatiques en cas d’échec (`MAX_RETRIES`, `RETRY_DELAY`)  
- 📝 Un **logging détaillé** (succès, erreurs, retries, requêtes ignorées pour health-check)

#### 4. Logs & monitoring
- Toutes les requêtes entrantes (sauf health-checks) sont **journalisées**.  
- Les envois, échecs et retries sont tracés pour garantir un **suivi complet**.

---

## 🖥️ Installation classique via Docker

### 1. Prérequis
- [Docker](https://docs.docker.com/engine/install/) installé sur votre machine  
- URL du dépôt : [https://github.com/tangocharlyfr/HW_SMS_WebGateway.git]

### 2. Cloner le projet sur votre machine
`git clone https://github.com/tangocharlyfr/HW_SMS_WebGateway.git /opt/HW_SMS_WebGateway`

### 3. Se placer dans le répertoire cloné
`cd /opt/HW_SMS_WebGateway`

### 4. Copier le fichier `.env.template` vers `.env` et éditer le ficher `.env`
Ajouter le répertoire comme sur : 
`git config --global --add safe.directory /opt/HW_SMS_WebGateway`

Modifiez les variables pour transmettre à l’application le login, le mot de passe et l’IP de votre routeur Huawei :
`cp .env.template .env`

`nano .env`

ROUTER_USER: admin  
ROUTER_PASSWORD: password  
ROUTER_IP: IP_Routeur

### 5. Lancer le conteneur
`docker compose up -d --build`

Exemple de sortie :  
[+] Running 3/3  
 ✔ hw_sms_webgateway-huawei_sms_server  Built  
 ✔ Network hw_sms_webgateway_default    Created  
 ✔ Container HW_SMS_WebGateway          Started  

### 6. Vérifier que le conteneur tourne
`docker ps`

Exemple :  
CONTAINER ID   IMAGE                                 COMMAND                  CREATED         STATUS                   PORTS                                         NAMES  
8d117d4fbb4d   hw_sms_webgateway-huawei_sms_server   "gunicorn -c gunicor…"   8 minutes ago   Up 8 minutes (healthy)   0.0.0.0:8282->8080/tcp, [::]:8282->8080/tcp   HW_SMS_WebGateway

### 7. Vérifier que l’application fonctionne

Testez l’API depuis votre machine ou serveur :  
`curl "http://Host_IP:8282/sms/send.aspx?tel=0612345678&message=Hello+World"`

---

## 🔍 HealthCheck

`docker inspect --format='{{json .State.Health}}' HW_SMS_WebGateway | jq`

Exemple de sortie :  
{
  "Status": "healthy",
  "Output": "✅ Healthcheck OK : Gunicorn + Huawei router 192.168.3.1 joignables"
}

---

## 📜 Logs du conteneur

`docker logs -f HW_SMS_WebGateway`

Exemple :  
[2025-08-25 11:13:30 +0000] [1] [INFO] Starting gunicorn 23.0.0  
[2025-08-25 11:13:30 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)  
[2025-08-25 11:13:30 +0000] [1] [INFO] 🦄 Gunicorn est UP  
[2025-08-25 11:13:30 +0000] [7] [INFO] Booting worker avec pid: 7  
[2025-08-25 11:13:30 +0000] [7] [INFO] ✅ La passerelle SMS est prête !

---

## 🖥️ Installation via Portainer (Deploy from Repository)

Vous pouvez déployer la **Gateway SMS** directement depuis le dépôt GitHub en utilisant l’option **Deploy from repository** de Portainer.

### 1. Prérequis
- [Docker](https://docs.docker.com/engine/install/) installé sur votre machine  
- [Portainer](https://docs.portainer.io/start/install-ce/server/docker/linux) installé et accessible via votre navigateur  
- URL du dépôt : `https://github.com/tangocharlyfr/HW_SMS_WebGateway.git`

### 2. Déployer depuis le dépôt

1. Connectez-vous à Portainer.  
2. Allez dans **Stacks** → **Add stack** → **Deploy from repository**.  
Remplissez les champs :  
   - **Repository URL** : `https://github.com/tangocharlyfr/HW_SMS_WebGateway.git`  
   - **Repository reference/branch** : `refs/heads/main`  
   - **Compose path** : `docker-compose.yml`  
4. **Créer les variables d’environnement** nécessaires pour l’application :  
   - `ROUTER_USER` → utilisateur du modem/routeur  
   - `ROUTER_PASSWORD` → mot de passe du modem/routeur  
   - `ROUTER_IP` → adresse IP du modem/routeur  
5. Cliquez sur **Deploy the stack**.

> Portainer va automatiquement cloner le dépôt, lire le fichier `docker-compose.yml` et créer les conteneurs définis avec vos variables d’environnement.

### 3. Vérifier que l’application fonctionne

Testez l’API depuis votre machine ou serveur :  
`curl "http://Host_IP:8282/sms/send.aspx?tel=0612345678&message=Hello+World"`

## 📜 Logs du conteneur 

![Capture écran](https://i.imgur.com/TNZc0fH.png)

---

🚀 Votre passerelle SMS est maintenant opérationnelle !
