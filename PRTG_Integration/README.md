## ⚙️ PRTG Integration

L'intégration à **PRTG** se fait très facilement via la Web UI.

---

### ⚡ Étapes de configuration

1. Allez dans le menu : **Configuration** → **Transmission de notifications**.  
2. Selon la documentation PRTG :  

   > Saisissez la chaîne d'URL de votre fournisseur SMS.  
   > Utilisez **%SMSNUMBER** et **%SMSTEXT** comme variables pour le numéro de téléphone du destinataire et le contenu du message.  
   >  
   > **Remarque :** utilisez la méthode **GET** pour interroger l’URL.  
   > Les requêtes **POST** ne sont pas prises en charge.

---

### 🔗 Exemple d’URL pour notre intégration

http://HOST_IP:8282/sms/send.aspx?tel=%SMSNUMBER&message=%SMSTEXT

---

### 🖼️ Capture d’écran

![Capture écran](https://i.imgur.com/e5dw4gu.png)

---

### ✅ Dernières étapes

- Indiquez le **numéro de téléphone** de votre utilisateur dans :  
  **Configuration → Utilisateur → Contact par notification**  
- Configurez vos alertes sur vos sondes en selectionnant l’**envoi par SMS** comme méthode de notification.
