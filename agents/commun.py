"""Outils partagés par tous les agents de l'atelier.

Ce fichier n'est PAS un agent (ce n'est pas un dossier),
donc il n'apparaît pas dans la liste de l'interface `adk web`.
"""

import os

from google.adk.models.lite_llm import LiteLlm


def choisir_modele():
    """Renvoie le 'cerveau' de l'agent, lu dans la variable MODELE_IA du fichier .env.

    - Un nom simple (ex. "gemini-flash-latest") = Gemini, utilisé directement par ADK.
    - Un nom avec un "/" (ex. "openrouter/...", "ollama_chat/...") = passage par LiteLLM,
      qui sait parler à des dizaines d'autres fournisseurs.

    Résultat : on change de fournisseur d'IA en modifiant UNE ligne du .env,
    sans toucher au code des agents.
    """
    nom = os.getenv("MODELE_IA", "gemini-flash-latest")
    if "/" in nom:
        return LiteLlm(model=nom)
    return nom
