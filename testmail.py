import smtplib
from email.mime.text import MIMEText

# --- TES INFORMATIONS ---
# 1. L'email "facteur" (le compte Gmail où tu as généré le code secret)
email_expediteur = "bendahouilyas09@gmail.com"  # <-- REMPLACE CELA PAR TON VRAI GMAIL !

# 2. Le mot de passe d'application de 16 lettres (sans espaces)
mot_de_passe_app = "sduahgzddgixxbti" 

# 3. Ton email perso pour vérifier que tu reçois bien le test
email_destinataire = "kakashi.lopok@yahoo.com" 

# --- LE MESSAGE ---
titre = "Test du serveur iysSTREAM"
texte = """
Salut ! 
Si tu reçois ce mail, ça veut dire que ton serveur Python est officiellement capable d'envoyer des mails ! 🎉
Ton code de vérification secret est le : 482910.
"""

msg = MIMEText(texte)
msg['Subject'] = titre
msg['From'] = email_expediteur
msg['To'] = email_destinataire

# --- L'ENVOI ---
try:
    print("⏳ Tentative de connexion aux serveurs de Google...")
    # On se connecte au serveur d'envoi de Gmail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # On s'identifie avec ton Gmail et le code à 16 lettres
    server.login(email_expediteur, mot_de_passe_app)
    # On envoie le message
    server.send_message(msg)
    # On coupe la connexion
    server.quit()
    print("✅ SUCCÈS ! Le mail a été envoyé. Va vérifier ta boîte Yahoo (regarde aussi dans les spams au cas où) !")
except Exception as e:
    print("❌ ERREUR :", e)