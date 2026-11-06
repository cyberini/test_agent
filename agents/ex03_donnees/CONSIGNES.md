# Exercice 3 : brancher l'agent sur vos données 📊

**Durée : 25 min · Objectif : connecter un agent à un fichier métier (CSV)**

## 1. Testez

Choisissez `ex03_donnees` et demandez :

- « Combien ai-je dépensé par catégorie ? »
- « Combien m'a coûté la SNCF ce mois-ci ? »
- « Quelles sont mes 3 plus grosses dépenses ? »
- « Quel est mon chiffre d'affaires ? » Attention, piège : l'information n'existe pas. L'agent invente-t-il ?

## 2. Observez 🔍

L'agent **ne voit jamais le fichier entier**. Il ne reçoit que ce que les outils lui renvoient. C'est une bonne pratique de sécurité : on contrôle ce que l'IA voit.

## 3. À vous de jouer 🎯

1. Ouvrez `donnees/depenses.csv` et ajoutez 2 ou 3 lignes. Testez à nouveau.
2. **Remplacez le fichier par des données de votre métier** (ventes, stocks, heures, clients fictifs…). Adaptez les noms de colonnes dans le code.
3. Ajoutez un outil `depenses_entre(date_debut, date_fin)`.

> ⚠️ **Règle d'or :** jamais de vraies données clients ou personnelles avec une clé API gratuite, car le fournisseur peut s'en servir pour entraîner ses modèles. Utilisez des données **fictives**.

> 💡 **À retenir :** « Répondez uniquement à partir de vos outils » est la phrase magique contre les hallucinations.
