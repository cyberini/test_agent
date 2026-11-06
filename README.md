# 🤖 Atelier — Crée tes agents IA avec Google ADK

Bienvenue ! En quelques heures, tu vas passer de « c'est quoi un agent ? » à **ton propre agent IA pour ton métier**.

[![Ouvrir dans GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TON-COMPTE/TON-DEPOT?quickstart=1)

> 🔧 *Formateur : remplace `TON-COMPTE/TON-DEPOT` par l'adresse de ton dépôt GitHub (voir `GUIDE_FORMATEUR.md`).*

---

## 🚀 Démarrage en 5 minutes

### Étape 1 — Récupère ta clé IA gratuite
1. Va sur **https://aistudio.google.com/apikey** (connexion avec un compte Google).
2. Clique sur **Create API key** et copie la clé.

> 🔐 Cette clé est **personnelle**, comme un mot de passe. Ne la partage pas, ne la publie pas.

### Étape 2 — Ouvre ton environnement

**Option A — En ligne, rien à installer (recommandé)**
1. Crée un compte gratuit sur **https://github.com** si tu n'en as pas.
2. Sur la page du dépôt, clique sur **Use this template → Create a new repository** (tu obtiens ta propre copie, tu pourras garder ton travail).
3. Dans ta copie : **Code → Codespaces → Create codespace on main**.
4. Patiente 1 à 2 minutes : VS Code s'ouvre dans ton navigateur, tout est installé.

**Option B — Sur ton ordinateur** → suis `GUIDE_INSTALL_LOCAL.md`.

### Étape 3 — Colle ta clé
Ouvre le fichier **`.env`** (à gauche), remplace `colle_ta_cle_ici` par ta clé, enregistre (Ctrl+S / Cmd+S).

### Étape 4 — Lance l'interface
Dans le terminal en bas, tape :

```bash
bash lancer.sh
```

Une fenêtre s'ouvre (sinon : onglet **Ports** → port 8000 → icône 🌐). Choisis un agent en haut à gauche et discute avec lui !

> Pour arrêter : clique dans le terminal et fais **Ctrl+C**.

---

## 🗺️ Le parcours

| # | Dossier | Tu apprends à… | Durée |
|---|---------|----------------|-------|
| 1 | `agents/ex01_premier_agent` | Donner une personnalité et des règles à un agent | 15 min |
| 2 | `agents/ex02_outils` | Lui donner des « mains » : des fonctions Python | 20 min |
| 3 | `agents/ex03_donnees` | Le brancher sur un fichier de données métier | 25 min |
| 4 | `agents/ex04_equipe` | Créer une équipe d'agents avec un chef | 25 min |
| 5 | `agents/ex05_chaine` | Enchaîner des agents dans un ordre fixe | 20 min |
| 6 | `agents/ex06_garde_fou` | Sécuriser son agent avec des garde-fous | 25 min |
| 🚀 | `agents/mon_agent` | **Créer TON agent pour TON métier** | le reste ! |

Chaque dossier contient un fichier **`CONSIGNES.md`** : lis-le, puis ouvre `agent.py`.

Pour ton projet perso, commence par remplir **`FICHE_CONCEPTION.md`**.

---

## 🆘 Ça ne marche pas ?

| Symptôme | Solution |
|----------|----------|
| `API key not valid` | Vérifie le `.env` : pas d'espace ni de guillemets autour de la clé. |
| `429` / `RESOURCE_EXHAUSTED` | Quota gratuit atteint : attends 1 minute, ou passe sur `gemini-flash-lite-latest` (voir `GUIDE_MODELES.md`). |
| `404` / modèle introuvable | Le nom du modèle a changé : voir `GUIDE_MODELES.md`. |
| Mon agent n'apparaît pas | Son dossier doit contenir `__init__.py` + `agent.py` avec une variable `root_agent`. |
| J'ai modifié le code, rien ne change | Recharge la page de l'interface. Au besoin, Ctrl+C puis relance `bash lancer.sh`. |
| `Failed to create session` | Tu as lancé `adk web agents` au lieu de `bash lancer.sh` : arrête (Ctrl+C) et lance `bash lancer.sh`. |
| `adk: command not found` | Tape `pip install -r requirements.txt`. |

## ⏱️ Bon à savoir (Codespaces gratuit)

- Ton compte GitHub gratuit inclut environ **60 h d'utilisation par mois** : largement assez pour la formation.
- Quand tu as fini : **arrête ton Codespace** (github.com/codespaces → `…` → *Stop codespace*). Sinon il s'arrête seul après 30 min d'inactivité.
- ⚠️ N'utilise **jamais de vraies données personnelles ou clients** avec une clé gratuite : le fournisseur peut les utiliser pour améliorer ses modèles.
