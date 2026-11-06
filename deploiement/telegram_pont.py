"""Pont Telegram : relie un bot Telegram à un agent ADK qui tourne sur le même serveur.

Sécurité :
  - liste blanche d'utilisateurs (TELEGRAM_UTILISATEURS_AUTORISES) : tout le reste est refusé ;
  - le pont parle à ADK en local (127.0.0.1), jamais via Internet ;
  - transparence (AI Act, art. 50) : l'utilisateur est informé qu'il échange avec une IA.

Attention RGPD : les messages transitent par les serveurs de Telegram.
Pas de données sensibles ou de données clients via ce canal sans analyse préalable.

Commandes : /start (présentation), /nouveau (nouvelle conversation), /id (affiche votre identifiant).
"""

import logging
import os
import sys
import time

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("telegram_pont")

JETON_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
AGENT = os.environ.get("TELEGRAM_AGENT", "mon_agent").strip()
ADK_URL = os.environ.get("ADK_URL", "http://127.0.0.1:8000").rstrip("/")
TELEGRAM_API = os.environ.get("TELEGRAM_API_BASE", "https://api.telegram.org").rstrip("/")
AUTORISES = {
    int(x) for x in os.environ.get("TELEGRAM_UTILISATEURS_AUTORISES", "").replace(" ", "").split(",") if x
}

MESSAGE_ACCUEIL = (
    "🤖 Bonjour ! Vous échangez avec un assistant fonctionnant grâce à l'intelligence artificielle. "
    "Ses réponses peuvent contenir des erreurs : vérifiez les informations importantes.\n\n"
    "/nouveau pour démarrer une nouvelle conversation."
)
LIMITE_TELEGRAM = 4000  # Telegram limite un message à 4096 caractères

# Session ADK courante pour chaque conversation Telegram (remise à zéro au redémarrage du service)
sessions: dict[int, str] = {}


def api_telegram(client: httpx.Client, methode: str, **params) -> dict:
    r = client.post(f"{TELEGRAM_API}/bot{JETON_BOT}/{methode}", json=params, timeout=70)
    r.raise_for_status()
    return r.json()


def envoyer(client: httpx.Client, chat_id: int, texte: str) -> None:
    for i in range(0, max(len(texte), 1), LIMITE_TELEGRAM):
        api_telegram(client, "sendMessage", chat_id=chat_id, text=texte[i : i + LIMITE_TELEGRAM] or "…")


def session_adk(client: httpx.Client, utilisateur: str, chat_id: int) -> str:
    """Renvoie l'identifiant de session ADK de cette conversation, en la créant si besoin."""
    session_id = sessions.setdefault(chat_id, f"tg-{chat_id}")
    url = f"{ADK_URL}/apps/{AGENT}/users/{utilisateur}/sessions/{session_id}"
    if client.get(url, timeout=10).status_code == 404:
        client.post(url, json={}, timeout=10).raise_for_status()
    return session_id


def demander_a_l_agent(client: httpx.Client, utilisateur: str, chat_id: int, texte: str) -> str:
    session_id = session_adk(client, utilisateur, chat_id)
    r = client.post(
        f"{ADK_URL}/run",
        json={
            "appName": AGENT,
            "userId": utilisateur,
            "sessionId": session_id,
            "newMessage": {"role": "user", "parts": [{"text": texte}]},
        },
        timeout=300,
    )
    r.raise_for_status()
    reponses = []
    for evenement in r.json():
        contenu = evenement.get("content") or {}
        if contenu.get("role") == "model":
            reponses += [p["text"] for p in contenu.get("parts", []) if p.get("text")]
    return reponses[-1] if reponses else "Je n'ai pas de réponse à vous donner, pouvez-vous reformuler ?"


def traiter(client: httpx.Client, message: dict) -> None:
    chat_id = message["chat"]["id"]
    expediteur = message.get("from", {}).get("id")
    texte = (message.get("text") or "").strip()

    if texte == "/id":
        envoyer(client, chat_id, f"Votre identifiant Telegram : {expediteur}")
        return
    if expediteur not in AUTORISES:
        log.warning("Accès refusé pour l'identifiant %s", expediteur)
        envoyer(client, chat_id, "⛔ Accès non autorisé. Communiquez votre identifiant (/id) à l'administrateur.")
        return
    if texte in ("/start", ""):
        envoyer(client, chat_id, MESSAGE_ACCUEIL)
        return
    if texte == "/nouveau":
        sessions[chat_id] = f"tg-{chat_id}-{int(time.time())}"
        envoyer(client, chat_id, "🆕 Nouvelle conversation démarrée.")
        return

    try:
        api_telegram(client, "sendChatAction", chat_id=chat_id, action="typing")
        reponse = demander_a_l_agent(client, f"telegram-{expediteur}", chat_id, texte)
    except Exception:
        log.exception("Erreur lors de l'appel à l'agent")
        reponse = "⚠️ Une erreur est survenue. Réessayez dans un instant."
    envoyer(client, chat_id, reponse)


def main() -> None:
    if not JETON_BOT:
        sys.exit("TELEGRAM_BOT_TOKEN manquant dans /etc/agents-ia/agents.env")
    if not AUTORISES:
        log.warning("Aucun utilisateur autorisé : seule la commande /id fonctionnera.")
    log.info("Pont Telegram démarré pour l'agent '%s' (%d utilisateur(s) autorisé(s))", AGENT, len(AUTORISES))

    decalage = 0
    with httpx.Client() as client:
        while True:
            try:
                maj = api_telegram(client, "getUpdates", offset=decalage, timeout=50, allowed_updates=["message"])
                for u in maj.get("result", []):
                    decalage = u["update_id"] + 1
                    if "message" in u:
                        traiter(client, u["message"])
            except httpx.HTTPError:
                log.exception("Erreur réseau, nouvelle tentative dans 5 s")
                time.sleep(5)


if __name__ == "__main__":
    main()
