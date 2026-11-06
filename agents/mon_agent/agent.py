"""🚀 MON AGENT : votre projet personnel.

Remplissez d'abord la FICHE_CONCEPTION.md (à la racine du projet),
puis complétez les zones marquées TODO ci-dessous.
Inspirez-vous des exercices 1 à 6 : tout ce dont vous avez besoin s'y trouve.
"""

from google.adk.agents import Agent

from commun import choisir_modele


# TODO 1 : vos outils (exercices 2 et 3).
# Une fonction = un outil. Soignez la docstring : c'est le mode d'emploi de l'agent.
def mon_premier_outil(parametre: str) -> dict:
    """TODO : décrivez en une phrase ce que fait cet outil.

    Args:
        parametre: TODO : à quoi sert ce paramètre.
    """
    return {"resultat": f"TODO : traiter {parametre}"}


root_agent = Agent(
    # TODO 2 : un nom en minuscules, sans espace ni accent (ex. assistant_compta)
    name="mon_agent",
    model=choisir_modele(),
    # TODO 3 : à quoi sert votre agent, en une phrase
    description="TODO : description de mon agent.",
    # TODO 4 : sa fiche de poste : rôle, public, règles, ton, format de réponse
    instruction="""
Vous êtes ... (rôle)
Vous aidez ... (qui) à ... (quoi).

Vos règles :
- ...
- Vous répondez uniquement à partir de vos outils lorsqu'il s'agit de chiffres.
- Si vous ne savez pas, vous le dites.

Format de vos réponses : ...
""",
    tools=[mon_premier_outil],
    # TODO 5 (optionnel) : une équipe (exercice 4) : sub_agents=[...]
    # TODO 6 (optionnel) : des garde-fous (exercice 6) : before_model_callback=..., before_tool_callback=...
)
