# 🤖 Créer des agents IA avec Google ADK

Bienvenue ! En quelques heures, vous allez apprendre à créer **votre propre agent IA pour votre métier**.

[![Ouvrir dans GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cyberini/agent_IA?quickstart=1)

---

## 🚀 Démarrage en 5 minutes

### Étape 1 - Récupérer votre clé IA gratuite
1. Allez sur **https://aistudio.google.com/apikey** (connexion avec un compte Google).
2. Cliquez sur **Create API key** et copiz la clé.

> 🔐 Cette clé est **personnelle**, comme un mot de passe. Ne la partagez pas et ne la publiez pas.

### Étape 2 — Ouvrir votre environnement

**Option A — En ligne, rien à installer (recommandé)**
1. Créez un compte gratuit sur **https://github.com** si vous n'en avez pas.
2. Sur la page du dépôt, cliquez sur **Use this template puis Create a new repository** (vous obtiendrez votre propre copie).
3. Dans votre copie : **Code - Codespaces - Create codespace on main**.
4. Patientez 1 à 2 minutes : VS Code s'ouvre dans votre navigateur, tout est installé.

**Option B — Sur votre ordinateur** - suivre `GUIDE_INSTALL_LOCAL.md`.

### Étape 3 — Coller votre clé
Ouvrez le fichier **`.env`** (à gauche), remplace `collez_la_cle_ici` par votre clé, enregistrez (Ctrl+S / Cmd+S).

### Étape 4 — Lancer l'interface
Dans le terminal en bas, tapez :

```bash
adk web agents
```

Une fenêtre s'ouvre (sinon : onglet **Ports**, port 8000, icône 🌐). Choisissez un agent en haut à gauche et discutez avec lui !

> Pour arrêter : cliquez dans le terminal et faites **Ctrl+C**.

---

## 🗺️ Le parcours

| # | Dossier | Vous apprennez à… | Durée |
|---|---------|----------------|-------|
| 1 | `agents/ex01_premier_agent` | Donner une personnalité et des règles à un agent | 15 min |
| 2 | `agents/ex02_outils` | Lui donner des « mains » : des fonctions Python | 20 min |
| 3 | `agents/ex03_donnees` | Le brancher sur un fichier de données métier | 25 min |
| 4 | `agents/ex04_equipe` | Créer une équipe d'agents avec un chef | 25 min |
| 5 | `agents/ex05_chaine` | Enchaîner des agents dans un ordre fixe | 20 min |
| 6 | `agents/ex06_garde_fou` | Sécuriser son agent avec des garde-fous | 25 min |
| 🚀 | `agents/mon_agent` | **Créer VOTRE agent pour VOTRE métier** | le reste ! |

Chaque dossier contient un fichier **`CONSIGNES.md`** : lisez-le, puis ouvrez `agent.py`.

Pour votre projet perso, commencez par remplir **`FICHE_CONCEPTION.md`**.

---

## 🆘 Ça ne marche pas ?

| Symptôme | Solution |
|----------|----------|
| `API key not valid` | Vérifiez le `.env` : pas d'espace ni de guillemets autour de la clé. |
| `429` / `RESOURCE_EXHAUSTED` | Quota gratuit atteint : attendez 1 minute, ou passez sur `gemini-flash-lite-latest` (voir `GUIDE_MODELES.md`). |
| `404` / modèle introuvable | Le nom du modèle a changé : voir `GUIDE_MODELES.md`. |
| Mon agent n'apparaît pas | Son dossier doit contenir `__init__.py` + `agent.py` avec une variable `root_agent`. |
| J'ai modifié le code, rien ne change | Rechargez la page de l'interface. Au besoin, Ctrl+C puis relancez `adk web agents`. |
| `adk: command not found` | Tapez `pip install -r requirements.txt`. |

## ⏱️ Bon à savoir (Codespaces gratuit)

- Votre compte GitHub gratuit inclut environ **60 h d'utilisation par mois** : largement assez pour des travaux normaux.
- Quand vous avez fini : **arrêtez votre Codespace** (github.com/codespaces, `…`, *Stop codespace*). Sinon il s'arrête seul après 30 min d'inactivité.
- ⚠️ N'utilisez **jamais de vraies données personnelles ou clients** avec une clé gratuite : le fournisseur peut les utiliser pour améliorer ses modèles.
