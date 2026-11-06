"""Exercice 6 : les garde-fous, sécuriser son agent.

Les "callbacks" sont des fonctions Python appelées AUTOMATIQUEMENT à certains moments :
  - before_model_callback : juste AVANT d'envoyer le message au LLM,
                            on peut bloquer des données sensibles (elles ne partent jamais).
  - before_tool_callback  : juste AVANT qu'un outil soit exécuté,
                            on peut interdire une action dangereuse.

Si le callback renvoie None = on laisse passer.
S'il renvoie une réponse = on court-circuite (le LLM ou l'outil n'est jamais appelé).
"""

import re
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types

from commun import choisir_modele

# === Garde-fou n°1 : ne jamais envoyer de données sensibles au LLM ===

MOTIFS_SENSIBLES = {
    "un IBAN": re.compile(r"\bFR\d{2}[ ]?(?:\d{4}[ ]?){5}\d{3}\b", re.IGNORECASE),
    "un numéro de carte bancaire": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "un mot de passe": re.compile(r"mot de passe\s*[:=]", re.IGNORECASE),
}


def _dernier_message_utilisateur(llm_request: LlmRequest) -> str:
    for contenu in reversed(llm_request.contents or []):
        if contenu.role == "user" and contenu.parts:
            return " ".join(p.text for p in contenu.parts if p.text)
    return ""


def bloquer_donnees_sensibles(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspecte le message AVANT qu'il parte chez le fournisseur d'IA."""
    texte = _dernier_message_utilisateur(llm_request)
    for nom, motif in MOTIFS_SENSIBLES.items():
        if motif.search(texte):
            print(f"🛡️ [GARDE-FOU] Message bloqué : il contenait {nom}.")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=(
                        f"🛡️ Stop ! Votre message semble contenir {nom}. "
                        "Je ne l'ai PAS transmis à l'IA. Retirez cette information et reformulez."
                    ))],
                )
            )
    return None  # tout va bien, on laisse passer


# === Garde-fou n°2 : limiter ce que les outils ont le droit de faire ===

DOMAINES_AUTORISES = ("@monentreprise.fr",)


def envoyer_email(destinataire: str, objet: str, message: str) -> dict:
    """Envoie un email (SIMULATION : rien n'est réellement envoyé).

    Args:
        destinataire: L'adresse email du destinataire.
        objet: L'objet de l'email.
        message: Le corps du message.
    """
    return {"statut": "envoyé (simulation)", "a": destinataire, "objet": objet}


def verifier_outil(tool, args: dict, tool_context) -> Optional[dict]:
    """Vérifie les arguments AVANT l'exécution d'un outil."""
    if tool.name == "envoyer_email":
        dest = str(args.get("destinataire", "")).lower()
        if not dest.endswith(DOMAINES_AUTORISES):
            print(f"🛡️ [GARDE-FOU] Envoi bloqué vers {dest}")
            return {"erreur": f"Envoi refusé : {dest} n'est pas une adresse interne autorisée."}
    return None  # autorisé


root_agent = Agent(
    name="assistant_securise",
    model=choisir_modele(),
    description="Assistant qui rédige et envoie des emails internes, avec garde-fous.",
    instruction="""
Vous aidez à rédiger et envoyer des emails internes avec l'outil envoyer_email. Vous vouvoyez votre interlocuteur.
Si un outil renvoie une erreur, expliquez-la simplement à l'utilisateur, sans contourner la règle.
""",
    tools=[envoyer_email],
    before_model_callback=bloquer_donnees_sensibles,
    before_tool_callback=verifier_outil,
)
