"""Exercice 4 : une équipe d'agents, un chef d'orchestre qui délègue.

Le "chef" (root_agent) lit la DESCRIPTION de chaque sous-agent
pour décider à qui confier la demande. Les descriptions sont donc cruciales !
"""

from google.adk.agents import Agent

from commun import choisir_modele


def calculer_ttc(montant_ht: float, taux_tva: float = 20.0) -> dict:
    """Calcule la TVA et le montant TTC à partir d'un montant HT en euros."""
    tva = round(montant_ht * taux_tva / 100, 2)
    return {"montant_ht": montant_ht, "tva": tva, "montant_ttc": round(montant_ht + tva, 2)}


expert_chiffres = Agent(
    name="expert_chiffres",
    model=choisir_modele(),
    description="Spécialiste des calculs : TVA, prix HT/TTC, montants, pourcentages.",
    instruction="Vous faites les calculs demandés avec vos outils et vous répondez de façon concise, en vouvoyant.",
    tools=[calculer_ttc],
)

redacteur = Agent(
    name="redacteur",
    model=choisir_modele(),
    description="Spécialiste de la rédaction : emails, courriers, messages professionnels.",
    instruction="""
Vous rédigez des emails professionnels courts, polis et clairs, en français.
Structure : objet, formule d'appel, 3 à 5 phrases, formule de politesse, signature [Prénom Nom].
""",
)

vulgarisateur = Agent(
    name="vulgarisateur",
    model=choisir_modele(),
    description="Explique simplement une notion compliquée, avec une analogie du quotidien.",
    instruction="Vous expliquez la notion demandée simplement, en 5 phrases maximum, avec une analogie, en vouvoyant.",
)

root_agent = Agent(
    name="accueil",
    model=choisir_modele(),
    description="Point d'entrée qui oriente chaque demande vers le bon spécialiste.",
    instruction="""
Vous êtes l'accueil d'un petit cabinet. Vous ne traitez PAS les demandes vous-même :
vous les transférez au spécialiste le plus adapté parmi votre équipe.
Si la demande est floue, posez UNE question pour la préciser, en vouvoyant.
""",
    sub_agents=[expert_chiffres, redacteur, vulgarisateur],
)
