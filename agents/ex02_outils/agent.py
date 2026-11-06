"""Exercice 2 : donner des "mains" à l'agent, les outils.

Un outil = une simple fonction Python.
L'agent lit son NOM, sa DOCSTRING (le texte entre triples guillemets) et ses PARAMÈTRES
pour décider tout seul quand l'appeler. La docstring, c'est son mode d'emploi !
"""

from datetime import date, datetime

from google.adk.agents import Agent

from commun import choisir_modele


def calculer_ttc(montant_ht: float, taux_tva: float = 20.0) -> dict:
    """Calcule le montant TTC et la TVA à partir d'un montant hors taxes.

    Args:
        montant_ht: Le montant hors taxes, en euros.
        taux_tva: Le taux de TVA en pourcentage (20, 10, 5.5 ou 2.1). 20 par défaut.

    Returns:
        Un dictionnaire avec le HT, la TVA et le TTC arrondis au centime.
    """
    tva = round(montant_ht * taux_tva / 100, 2)
    return {
        "montant_ht": round(montant_ht, 2),
        "taux_tva": taux_tva,
        "tva": tva,
        "montant_ttc": round(montant_ht + tva, 2),
    }


def jours_entre_deux_dates(date_debut: str, date_fin: str) -> dict:
    """Compte le nombre de jours entre deux dates.

    Args:
        date_debut: Date au format AAAA-MM-JJ (ex. 2026-01-15).
        date_fin: Date au format AAAA-MM-JJ.

    Returns:
        Le nombre de jours, ou un message d'erreur si le format est incorrect.
    """
    try:
        d1 = datetime.strptime(date_debut, "%Y-%m-%d").date()
        d2 = datetime.strptime(date_fin, "%Y-%m-%d").date()
    except ValueError:
        return {"erreur": "Format attendu : AAAA-MM-JJ"}
    return {"nombre_de_jours": (d2 - d1).days}


def date_du_jour() -> dict:
    """Donne la date d'aujourd'hui (le LLM ne la connaît pas tout seul !)."""
    return {"aujourd_hui": date.today().isoformat()}


root_agent = Agent(
    name="assistant_calculs",
    model=choisir_modele(),
    description="Assistant qui fait des calculs fiables grâce à des outils.",
    instruction="""
Vous êtes un assistant administratif précis. Vous vouvoyez votre interlocuteur.
- Pour TOUT calcul de TVA, utilisez l'outil calculer_ttc. Ne calculez jamais de tête.
- Pour les durées entre deux dates, utilisez jours_entre_deux_dates.
- Si l'on vous parle d'"aujourd'hui", appelez d'abord date_du_jour.
- Présentez les résultats clairement, avec le symbole €.
""",
    tools=[calculer_ttc, jours_entre_deux_dates, date_du_jour],
)
