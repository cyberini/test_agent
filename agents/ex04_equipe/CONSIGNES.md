# Exercice 4 : une équipe d'agents 👥

**Durée : 25 min · Objectif : faire collaborer plusieurs agents spécialisés**

## Le principe

Comme dans une entreprise : un **accueil** reçoit la demande et la transfère au bon **spécialiste**. Le chef choisit en lisant la `description` de chaque membre de l'équipe.

```
              accueil (chef)
         ┌────────┼─────────┐
  expert_chiffres  redacteur  vulgarisateur
```

## 1. Testez

Choisissez `ex04_equipe` et demandez successivement :

- « Combien font 850 € HT en TTC ? »
- « Rédigez un mail pour relancer un client qui n'a pas payé sa facture »
- « Qu'est-ce que l'amortissement, en termes simples ? »

## 2. Observez 🔍

Dans l'interface, regardez **qui répond** (le nom de l'agent apparaît) et repérez l'action **transfer_to_agent**. L'onglet graphe montre l'organigramme de votre équipe.

## 3. À vous de jouer 🎯

1. **Expérience :** changez la description de `redacteur` en « Agent n°2 ». La délégation fonctionne-t-elle encore ? Quelle conclusion en tirez-vous ? Remettez-la ensuite.
2. **Ajoutez un 4ᵉ membre** utile à votre métier (ex. « juriste » qui rappelle les mentions obligatoires d'une facture, « commercial » qui propose des arguments de vente…).
3. Demandez quelque chose qui nécessite **deux** spécialistes (« calculez le TTC de 850 € HT puis rédigez le mail de devis »). Que se passe-t-il ?

> 💡 **À retenir :** dans une équipe, la `description` sert au chef, l'`instruction` sert à l'agent lui-même.
