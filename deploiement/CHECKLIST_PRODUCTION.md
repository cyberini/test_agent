# ✅ Checklist avant mise en production

Cochez chaque point avant d'ouvrir le service à de vrais utilisateurs. Les points marqués **(auto)** sont réalisés par `installer.sh` : vérifiez simplement qu'ils sont en place.

## 1. Serveur

- [ ] VPS chez un hébergeur européen, DPA de l'hébergeur accepté
- [ ] Connexion SSH par clé uniquement, mot de passe et `root` désactivés (README, étape 1)
- [ ] Pare-feu : seuls SSH, 80 et 443 ouverts **(auto)** : `sudo ufw status`
- [ ] fail2ban actif **(auto)** : `sudo fail2ban-client status sshd`
- [ ] Mises à jour de sécurité automatiques **(auto)**
- [ ] Sauvegardes copiées **hors du serveur** (ex. `restic` ou `rclone` vers un stockage européen chiffré). Les sauvegardes locales ne protègent pas contre la perte du VPS.

## 2. Accès à l'API

- [ ] HTTPS valide sur le domaine **(auto)**
- [ ] Requête sans jeton refusée en 401 : `tester_api.sh`
- [ ] Jeton rangé dans un gestionnaire de mots de passe, jamais envoyé par email ou messagerie
- [ ] Le jeton n'est **jamais** placé dans du code exécuté par un navigateur (JavaScript d'un site). Un chatbot de site web doit passer par un serveur intermédiaire qui détient le jeton.
- [ ] Bien comprendre la limite : **un jeton = accès à tout** (tous les agents, toutes les conversations). Pour plusieurs clients ou plusieurs niveaux de droits, il faut une couche d'authentification applicative supplémentaire.

## 3. Secrets

- [ ] Clés API uniquement dans `/etc/agents-ia/agents.env` (droits 640) **(auto)**
- [ ] Aucun fichier `.env` dans le dépôt ni dans `/opt/agents-ia` (l'installateur refuse de continuer s'il en trouve un)
- [ ] Une clé API **dédiée** à ce service chez le fournisseur, révocable sans impact sur le reste

## 4. Agents

- [ ] Seuls les agents utiles sont déployés (`agents_prod`), pas les exercices
- [ ] Consignes claires : rôle, limites, « réponds uniquement à partir de tes outils » pour les chiffres
- [ ] Garde-fous en code pour les données interdites et les actions sensibles (exercice 6)
- [ ] Les actions irréversibles (envoi, paiement, suppression) demandent une **validation humaine** ou sont limitées par un `before_tool_callback`
- [ ] Les outils n'ont que les droits nécessaires (lecture seule quand c'est possible, comptes de service dédiés)
- [ ] Limite d'appels au modèle par requête : `MAX_APPELS_LLM` **(auto, 25 par défaut)**
- [ ] **Jeu de tests d'évaluation** : 10 à 20 questions types avec la réponse attendue, rejoués avec `adk eval` avant chaque modification
- [ ] Test d'injection de prompt : un document ou un email piégé ne doit pas faire dévier l'agent vers une action non prévue

## 5. Modèle, coûts et données

- [ ] Fournisseur en **niveau payant**, option d'entraînement désactivée si elle existe (voir `MODELES_ET_RGPD.md`)
- [ ] Plafond de dépenses et alertes configurés dans la console du fournisseur
- [ ] Région de traitement choisie et documentée (UE si possible)

## 6. RGPD et AI Act

- [ ] Traitement ajouté au registre (finalité, données, destinataires, durée)
- [ ] DPA du fournisseur du modèle accepté, transferts hors UE documentés
- [ ] Durée de conservation fixée (`RETENTION_JOURS`) et cohérente avec le registre
- [ ] Information des personnes : mention « assistant IA » visible sur chaque canal (AI Act, art. 50)
- [ ] AIPD réalisée si données sensibles ou traitement à risque
- [ ] Procédure d'effacement testée (suppression d'une conversation via l'API)

## 7. Exploitation

- [ ] Supervision externe de `https://VOTRE-DOMAINE/sante` (service de type « uptime monitor ») avec alerte email
- [ ] Une personne identifiée lit les journaux (`journalctl -u agents-ia`) et reçoit les alertes
- [ ] Procédure de restauration d'une sauvegarde **testée au moins une fois**
- [ ] Montées de version testées d'abord dans Codespaces (versions figées dans `requirements.txt`)
- [ ] Documentation remise au client : architecture, accès, procédures, contacts
