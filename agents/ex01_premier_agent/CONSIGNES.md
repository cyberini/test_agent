# Exercice 1 : votre premier agent ☕

**Durée : 15 min · Objectif : comprendre qu'un agent = un LLM + une "fiche de poste"**

## 1. Lancez-le

```bash
bash lancer.sh
```

> En installation locale (sans Codespaces), `adk web agents` fonctionne aussi.

Ouvrez l'interface (port 8000), choisissez `ex01_premier_agent` en haut à gauche, et dites bonjour.

## 2. Observez

Dans le panneau de gauche, cliquez sur un message : vous voyez **l'événement** envoyé au modèle et sa réponse. C'est cela, un agent : des allers-retours structurés avec un LLM.

## 3. À vous de jouer 🎯

Ouvrez `agent.py` et modifiez **uniquement le texte de `instruction`** :

1. Transformez Coach Café en **pirate** qui parle comme un pirate. Rechargez la page, testez.
2. Remettez un ton professionnel, mais spécialisez-le **dans votre métier** (ex. « Vous aidez un comptable à expliquer la TVA à ses clients »).
3. Ajoutez une règle : « Si l'on vous demande quelque chose hors de votre métier, refusez poliment ».

> 💡 **À retenir :** 80 % de la qualité d'un agent vient de ses consignes. Soyez précis, donnez des règles et des exemples.

## Défi bonus 🏆

Essayez de faire « craquer » votre agent pour qu'il sorte de son rôle (« oublie tes consignes et… »). Y parvenez-vous ? C'est une **injection de prompt** : nous en reparlons à l'exercice 6.
