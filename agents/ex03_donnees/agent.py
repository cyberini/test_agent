"""Exercice 3 : brancher l'agent sur VOS données.

L'agent ne lit pas le fichier lui-même : ce sont les outils qui le lisent
et lui renvoient seulement ce dont il a besoin. Avantages :
  - les calculs sont exacts (faits par Python, pas par le LLM) ;
  - on contrôle précisément ce que l'IA a le droit de voir.
"""

import csv
from collections import defaultdict
from pathlib import Path

from google.adk.agents import Agent

from commun import choisir_modele

FICHIER = Path(__file__).parent / "donnees" / "depenses.csv"


def _lire_depenses() -> list[dict]:
    """Fonction interne (commence par _) : ce n'est PAS un outil pour l'agent."""
    with open(FICHIER, encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    for ligne in lignes:
        ligne["montant_ttc"] = float(ligne["montant_ttc"])
    return lignes


def total_par_categorie() -> dict:
    """Calcule le total des dépenses TTC pour chaque catégorie, et le total général.

    Returns:
        Un dictionnaire {catégorie: total} et le total général.
    """
    totaux = defaultdict(float)
    for d in _lire_depenses():
        totaux[d["categorie"]] += d["montant_ttc"]
    totaux_arrondis = {k: round(v, 2) for k, v in sorted(totaux.items())}
    return {
        "totaux": totaux_arrondis,
        "total_general": round(sum(totaux.values()), 2),
    }


def chercher_depenses(mot_cle: str) -> dict:
    """Cherche les dépenses dont le fournisseur ou la catégorie contient un mot-clé.

    Args:
        mot_cle: Le texte à chercher (ex. "SNCF", "repas"). Insensible aux majuscules.

    Returns:
        La liste des dépenses trouvées et leur total.
    """
    mot = mot_cle.lower()
    trouvees = [
        d for d in _lire_depenses()
        if mot in d["fournisseur"].lower() or mot in d["categorie"].lower()
    ]
    return {
        "nombre": len(trouvees),
        "depenses": trouvees,
        "total": round(sum(d["montant_ttc"] for d in trouvees), 2),
    }


def plus_grosses_depenses(nombre: int = 3) -> dict:
    """Renvoie les plus grosses dépenses, de la plus chère à la moins chère.

    Args:
        nombre: Combien de dépenses afficher (3 par défaut).
    """
    triees = sorted(_lire_depenses(), key=lambda d: d["montant_ttc"], reverse=True)
    return {"plus_grosses": triees[:nombre]}


root_agent = Agent(
    name="analyste_depenses",
    model=choisir_modele(),
    description="Analyse un fichier de dépenses et répond aux questions à son sujet.",
    instruction="""
Vous êtes un assistant de gestion qui analyse les dépenses de septembre 2026.
Vous vouvoyez votre interlocuteur.
- Vous répondez UNIQUEMENT à partir des résultats de vos outils. N'inventez aucun chiffre.
- Si une question ne peut pas être traitée avec les outils, dites-le clairement.
- Présentez les montants avec le symbole € et, si c'est utile, sous forme de petit tableau.
- Vous pouvez proposer une observation utile (ex. "les déplacements représentent la moitié du budget").
""",
    tools=[total_par_categorie, chercher_depenses, plus_grosses_depenses],
)
