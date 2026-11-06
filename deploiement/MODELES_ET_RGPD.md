# 🧠 Choisir son modèle : RGPD, entraînement, localisation

Grâce à `agents/commun.py` et LiteLLM, **n'importe quel modèle** se branche en changeant une ligne (`MODELE_IA`) dans `/etc/agents-ia/agents.env`. Le vrai choix n'est donc pas technique : il dépend des **données** que vos agents vont traiter.

> Ce document est une aide à la décision, pas un avis juridique. Les conditions des fournisseurs évoluent : relisez-les à chaque nouveau projet. Situation vérifiée en novembre 2026.

---

## La règle d'or

**Aucun niveau gratuit et aucun abonnement grand public en production.**

- Les niveaux gratuits peuvent utiliser vos données pour entraîner les modèles, et des humains peuvent les relire.
- Les conditions de Google sont explicites : seuls les **services payants** de l'API Gemini peuvent être utilisés pour une application proposée à des utilisateurs situés dans l'**Espace économique européen**, en Suisse ou au Royaume-Uni.
- Les abonnements grand public (Claude Pro/Max, ChatGPT Plus, application Gemini…) relèvent de conditions grand public, sans contrat de sous-traitance adapté à des données clients.

---

## Comparatif des options

| Option (`agents.env`) | Entraînement sur vos données | Où sont traitées les données | Point d'attention |
|---|---|---|---|
| **Gemini gratuit** | **Oui**, relecture humaine possible | Monde | Formation uniquement. **Interdit** pour un service à des utilisateurs dans l'UE. |
| **A. Gemini API payante** | Non | Monde : stockage temporaire ou cache possible dans tout pays où Google a des installations | Journaux conservés une durée limitée pour détecter les abus. |
| **B. Gemini via Vertex AI** | Non | **Région européenne choisie** (ex. `europe-west1`) | La meilleure option Google pour la localisation UE. Demande un compte de service Google Cloud. |
| **C. Mistral AI** | **Possible par défaut** : à désactiver dans la console Mistral (Admin, Privacy, « Anonymous improvement data ») | Société française | Pensez à décocher l'option, sinon les données API peuvent entrer dans les programmes d'entraînement. Vérifiez le DPA et l'option ZDR. |
| **D. Claude (API Anthropic)** | Non, sauf autorisation expresse | Inférence : `us` ou `global` uniquement ; stockage aux États-Unis | Contenu non conservé par défaut (sauf modèles Fable et Mythos : 30 jours). Transfert hors UE à encadrer. ZDR sur demande. |
| **E. OpenAI API** | Non par défaut | **Résidence Europe possible** : créer un nouveau projet avec la région Europe (clients éligibles) | Un projet existant ne peut pas être converti : il faut le créer en région Europe dès le départ. |
| **F/G. Modèle local** (vLLM, Ollama) | Non | **Chez vous** | Le seul cas où rien ne sort de votre infrastructure. Vérifiez la licence du modèle (usage commercial autorisé ?) et sa gestion des outils. |

### Comment choisir en 3 questions

1. **Les données sont-elles personnelles, confidentielles ou sensibles** (santé, RH, données bancaires, secret des affaires) ?
   Oui : Vertex AI en région UE, OpenAI en résidence Europe, ou modèle local. Et une analyse d'impact (AIPD) si le traitement est à risque.
2. **Faut-il la meilleure qualité de raisonnement possible ?**
   Comparez Claude, Gemini et OpenAI sur **vos** cas réels (voir `adk eval` dans la checklist), en tenant compte du point 1.
3. **Le budget est-il serré et prévisible ?**
   Modèles « Flash », « Lite » ou « Haiku » pour le quotidien, modèle plus puissant seulement pour les tâches qui le justifient. Fixez un **plafond de dépenses** chez le fournisseur.

---

## Vos obligations RGPD (la TPE est responsable du traitement)

| Obligation | Concrètement |
|---|---|
| **Base légale et information** | Indiquer aux personnes concernées que leurs données sont traitées par un assistant IA, pourquoi, et combien de temps. |
| **Registre des traitements** | Ajouter une ligne « assistant IA » : finalité, données, destinataires, durée. |
| **Contrats de sous-traitance (art. 28)** | Accepter le DPA du fournisseur du modèle **et** celui de l'hébergeur du VPS. |
| **Transferts hors UE** | Fournisseur américain : vérifier le mécanisme de transfert (Data Privacy Framework ou clauses contractuelles types) et le documenter. |
| **Minimisation** | Ne donner à l'agent que les données utiles (outils ciblés, comme dans l'exercice 3). Garde-fous de l'exercice 6 pour bloquer les données interdites. |
| **Durée de conservation** | `RETENTION_JOURS` dans `agents.env` : purge automatique chaque nuit. Les sauvegardes sont elles aussi supprimées après `SAUVEGARDE_JOURS`. |
| **Sécurité (art. 32)** | Assurée par l'installation : chiffrement HTTPS, jeton, pare-feu, moindre privilège, mises à jour. |
| **Droits des personnes** | Effacement : `DELETE /apps/AGENT/users/UTILISATEUR/sessions/SESSION` sur l'API (ou suppression en base). |
| **AIPD** | Obligatoire si le traitement est à risque élevé : données sensibles, surveillance de salariés, évaluation de personnes… |

## AI Act : ce qui s'applique déjà

- **Transparence (article 50), en vigueur depuis le 2 août 2026 :** une personne qui échange avec une IA doit en être informée, sauf si c'est évident. Le pont Telegram le fait au premier message. Faites de même sur tout autre canal (site web, email).
- **Maîtrise de l'IA (article 4) :** les entreprises qui utilisent des systèmes d'IA doivent veiller à ce que leur personnel ait un niveau suffisant de connaissances. Une formation comme celle-ci y contribue directement.
- **Systèmes à haut risque :** si l'agent intervient dans le recrutement, l'évaluation de salariés, l'accès au crédit ou à des services essentiels, des obligations beaucoup plus lourdes s'appliquent. Dans ce cas, faites-vous accompagner avant toute mise en service.

---

## Et l'abonnement Claude (Pro/Max) ?

Il n'est **pas** utilisable pour faire fonctionner ces agents. D'après la documentation d'Anthropic, les développeurs qui construisent des produits ou services, y compris avec l'Agent SDK, doivent passer par une **clé API** (Claude Console ou fournisseur cloud). Faire passer les requêtes d'autres utilisateurs par les identifiants d'un abonnement Free, Pro ou Max n'est pas autorisé. Pour Claude dans vos agents : option D avec une clé API.
