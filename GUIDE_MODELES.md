# 🧠 Changer le « cerveau » de tes agents

Tous les agents de l'atelier lisent le modèle à utiliser dans **une seule ligne** du fichier `.env` :

```
MODELE_IA=gemini-flash-latest
```

Tu changes cette ligne, tu relances `bash lancer.sh`, et **tous** tes agents changent de cerveau, sans toucher au code. C'est le rôle de `agents/commun.py`.

---

## Option 1 — Gemini (par défaut, gratuit)

Clé sur https://aistudio.google.com/apikey → variable `GOOGLE_API_KEY`.

| Valeur de `MODELE_IA` | Quand l'utiliser |
|---|---|
| `gemini-flash-latest` | Par défaut. Pointe toujours vers le Flash le plus récent. |
| `gemini-flash-lite-latest` | Si tu prends des erreurs **429** (quota) : plus rapide, quotas gratuits plus larges. |
| `gemini-2.5-flash` (ou un autre numéro précis) | Si tu veux un comportement **figé**, qui ne change pas quand Google sort un nouveau modèle. |

> Les alias `-latest` évitent que les tutos cassent quand un modèle est retiré, mais le comportement peut changer légèrement d'un mois à l'autre.

**Limites du gratuit :** quelques requêtes par minute et un plafond par jour. Les quotas sont **par clé/projet** : chacun doit avoir **sa propre clé**. Les données envoyées peuvent être utilisées par Google pour améliorer ses modèles → **données fictives uniquement**.

## Option 2 — OpenRouter (plan B gratuit, sans Google)

1. Compte sur https://openrouter.ai → **Keys** → crée une clé.
2. Sur https://openrouter.ai/models, filtre par prix **Free** et choisis un modèle qui gère les **tools**. Son nom se termine par `:free`.
3. Dans `.env` :

```
MODELE_IA=openrouter/NOM-DU-MODELE:free
OPENROUTER_API_KEY=ta_cle
```

> La liste des modèles gratuits change souvent : vérifie le nom sur le site le jour J.

## Option 3 — Ollama (100 % local, confidentiel, sans clé)

Uniquement **sur ton propre ordinateur** (pas dans Codespaces : trop lent sans carte graphique). Il faut une machine correcte (16 Go de RAM conseillés).

1. Installe Ollama : https://ollama.com
2. Télécharge un modèle qui gère les outils : `ollama pull qwen2.5:7b`
3. Dans `.env` :

```
MODELE_IA=ollama_chat/qwen2.5:7b
# Si tu travailles dans le conteneur Docker (Dev Container) :
OLLAMA_API_BASE=http://host.docker.internal:11434
# Si tu travailles sans Docker (Python installé directement) :
# OLLAMA_API_BASE=http://localhost:11434
```

> ⚠️ Utilise bien le préfixe `ollama_chat/` (et pas `ollama/`), sinon les outils fonctionnent mal.
>
> 💡 C'est **la seule option où tes données ne quittent pas ta machine**. Idéal pour discuter confidentialité en formation.
