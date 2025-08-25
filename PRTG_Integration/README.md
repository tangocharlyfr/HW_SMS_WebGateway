## ⚙️ PRTG_Integration

L'intégration à **PRTG** se fait très facilement via la Web UI.

### Configuration dans PRTG
- Ouvrez le menu : **Configuration** → **Transmission de notifications**.  
- Selon la documentation PRTG :  

> Saisissez la chaîne d'URL de votre fournisseur SMS.  
> Utilisez **%SMSNUMBER** et **%SMSTEXT** comme variables pour le numéro de téléphone du destinataire et le contenu du message.  
>  
> **Remarque :** utilisez la méthode **GET** pour interroger l’URL. Les requêtes **POST** ne sont pas prises en charge.

### Exemple pour notre intégration

`http://HOST_IP:8282/sms/send.aspx?tel=%SMSNUMBER&message=%SMSTEXT`

---

![Capture écran](https://i.imgur.com/e5dw4gu.png)


Il ne vous reste plus qu'à configurer vos alertes sur vos sondes et de choisir l'envoi par SMS de la notification.
