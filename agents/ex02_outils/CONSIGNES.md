# Exercice 2 : donner des "mains" à l'agent 🛠️

**Durée : 20 min · Objectif : comprendre les outils (tools)**

## Pourquoi des outils ?

Un LLM est un génie des mots… et un calculateur peu fiable. Il ne connaît pas non plus la date du jour. La solution : lui donner des **fonctions Python** qu'il peut appeler.

## 1. Testez

Dans l'interface (`bash lancer.sh`), choisissez `ex02_outils` et demandez :

- « Combien font 1 234,56 € HT en TTC ? »
- « Et avec une TVA à 5,5 % ? »
- « Combien de jours entre aujourd'hui et le 31 décembre ? »

## 2. Observez 🔍

Dans l'interface, repérez les blocs **functionCall** (l'agent demande un outil) et **functionResponse** (le résultat renvoyé). L'agent *choisit seul* quel outil appeler, grâce à la docstring.

## 3. À vous de jouer 🎯

1. **Expérience :** effacez la docstring de `jours_entre_deux_dates`, relancez, testez à nouveau. L'agent s'en sert-il toujours correctement ? Remettez-la ensuite.
2. **Ajoutez votre propre outil** pour votre métier, par exemple :
   - comptable : `calculer_ht(montant_ttc, taux_tva)`
   - commercial : `appliquer_remise(prix, pourcentage)`
   - RH : `calculer_conges(jours_travailles)`
3. N'oubliez pas de l'ajouter dans la liste `tools=[...]` !

> 💡 **À retenir :** un bon outil = un nom clair + une docstring précise + des paramètres typés (`float`, `str`…). Il renvoie de préférence un `dict`.
