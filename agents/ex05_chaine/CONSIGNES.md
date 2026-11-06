# Exercice 5 : la chaîne de production 🏭

**Durée : 20 min · Objectif : enchaîner des agents dans un ordre fixe**

## Le principe

Les agents travaillent les uns après les autres, comme sur une chaîne :

1. L'utilisateur donne un sujet.
2. Le **rédacteur** écrit un premier jet et le range dans le casier `{brouillon}`.
3. Le **relecteur** lit `{brouillon}` et range ses remarques dans le casier `{critiques}`.
4. Le **finaliseur** lit les deux casiers et produit la version finale.

Chaque agent dépose son travail dans un **casier** (`output_key`). Le suivant le lit avec `{nom_du_casier}`.

## 1. Testez

Choisissez `ex05_chaine` et donnez simplement un sujet :

- « Pourquoi les PME devraient sauvegarder leurs données »
- « Les 3 erreurs à éviter quand on crée son entreprise »

## 2. Observez 🔍

Vous voyez les **trois agents** répondre l'un après l'autre. Ouvrez l'onglet **State** : les casiers `brouillon` et `critiques` y sont visibles.

## 3. À vous de jouer 🎯

1. Transformez la chaîne pour **votre métier**. Exemples :
   - comptable : *extraire les informations d'une facture, vérifier les mentions obligatoires, rédiger un mail au client*
   - commercial : *résumer un compte rendu de rendez-vous, identifier les objections, proposer une relance*
2. Ajoutez un 4ᵉ agent « traducteur » qui traduit la version finale en anglais.

> 💡 **Quand choisir quoi ?** Processus toujours identique = **chaîne** (ex. 5). Demandes variées = **équipe avec chef** (ex. 4). Il existe aussi `ParallelAgent` (plusieurs agents en même temps) et `LoopAgent` (répéter jusqu'à obtenir un bon résultat).
