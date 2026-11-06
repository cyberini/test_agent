"""Exercice 5 : la chaîne de production, des agents qui travaillent À LA SUITE.

Différence avec l'exercice 4 :
  - Ex. 4 (sub_agents)      = le chef DÉCIDE à qui déléguer (flexible, imprévisible).
  - Ex. 5 (SequentialAgent) = l'ordre est FIXÉ à l'avance (fiable, prévisible).

Chaque agent range son résultat dans un "casier" (output_key).
L'agent suivant le lit grâce à {nom_du_casier} dans ses consignes.
"""

from google.adk.agents import Agent, SequentialAgent

from commun import choisir_modele

redacteur = Agent(
    name="redacteur",
    model=choisir_modele(),
    description="Écrit un premier jet de publication LinkedIn.",
    instruction="""
Écrivez un premier jet de publication LinkedIn (120 mots maximum) sur le sujet donné par l'utilisateur.
Ton : professionnel mais accessible. N'ajoutez pas de hashtags.
""",
    output_key="brouillon",
)

relecteur = Agent(
    name="relecteur",
    model=choisir_modele(),
    description="Critique le brouillon.",
    instruction="""
Voici un brouillon :
---
{brouillon}
---
Listez 3 améliorations précises (accroche, clarté, appel à l'action). Soyez exigeant mais bienveillant.
Ne réécrivez pas le texte.
""",
    output_key="critiques",
)

finaliseur = Agent(
    name="finaliseur",
    model=choisir_modele(),
    description="Produit la version finale.",
    instruction="""
Brouillon :
{brouillon}

Critiques à appliquer :
{critiques}

Réécrivez la publication en appliquant TOUTES les critiques. Ajoutez 3 hashtags pertinents à la fin.
Ne donnez que la version finale, sans commentaire.
""",
)

root_agent = SequentialAgent(
    name="atelier_linkedin",
    description="Rédige, critique puis finalise une publication LinkedIn.",
    sub_agents=[redacteur, relecteur, finaliseur],
)
