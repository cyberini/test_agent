# 📝 Fiche de conception — Mon agent métier

Avant d'écrire une ligne de code, réponds à ces 7 questions. 15 minutes ici = des heures gagnées ensuite.

---

### 1. Quelle tâche répétitive veux-tu confier à ton agent ?
*Une tâche précise, pas « m'aider dans mon travail ».*
> Ex. : « Répondre aux questions de mes clients sur les dates limites de TVA. »

**Ma réponse :**

### 2. Qui va lui parler ?
*Toi ? Un collègue ? Un client ? Son niveau ?*

**Ma réponse :**

### 3. De quelles informations a-t-il besoin ?
*Un fichier (CSV, liste de prix, FAQ…) ? Des règles métier ? → deviendront ses **outils** (ex. 3).*

**Ma réponse :**

### 4. Quels calculs ou actions doit-il faire ?
*Tout calcul ou action = un **outil** Python (ex. 2). Jamais « de tête ».*

**Ma réponse :**

### 5. Une seule tâche ou plusieurs étapes ?
- Toujours les mêmes étapes dans le même ordre → **chaîne** (ex. 5)
- Des demandes variées → **équipe avec un chef** (ex. 4)
- Simple → **un seul agent** (ex. 1-3)

**Ma réponse :**

### 6. Qu'est-ce qu'il ne doit JAMAIS faire ?
*Données interdites, actions dangereuses → **garde-fous en code** (ex. 6).*

**Ma réponse :**

### 7. À quoi ressemble une réponse parfaite ?
*Écris un exemple de question et la réponse idéale. Tu le colleras dans les consignes de l'agent.*

**Question type :**

**Réponse idéale :**

---

## 💡 Idées par métier

| Métier | Agent possible | Outils | Garde-fou |
|--------|---------------|--------|-----------|
| **Comptable** | Pré-contrôle des notes de frais | lire un CSV de dépenses, vérifier les plafonds, calculer HT/TVA | bloquer les IBAN |
| **Commercial** | Préparateur de devis | grille tarifaire (CSV), calcul de remises | remise max 15 % codée en dur |
| **RH** | FAQ congés et télétravail | lire la FAQ interne, calculer des jours | refuser toute donnée médicale |
| **Artisan** | Estimateur de chantier | prix des matériaux, calcul de surfaces | aucun prix sous le coût de revient |
| **Immobilier** | Rédacteur d'annonces | calcul m² / prix au m² | pas de critères discriminants |
| **Formateur** | Générateur de quiz | lire un support de cours, compter les questions | pas de données d'apprenants |
| **Cybersécurité** | Trieur d'emails suspects | extraire les liens, vérifier un domaine dans une liste | ne jamais ouvrir de lien |

Une fois la fiche remplie : ouvre `agents/mon_agent/agent.py` et suis les `TODO`.
