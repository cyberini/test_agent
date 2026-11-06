# 🚀 Mettre ses agents IA en production sur un VPS

Ce guide transforme les agents créés dans l'atelier en **service professionnel** : disponible 24 h/24, sécurisé, sauvegardé, conforme RGPD, et branché sur le modèle d'IA de votre choix.

Le code des agents est **exactement le même** que dans Codespaces. Seul l'environnement change.

---

## 🧱 L'architecture

```
 Internet (HTTPS uniquement)
        │
   ┌────┴─────────────────────────── VPS ───────────────────────────────┐
   │  Pare-feu ufw : ports 22, 80, 443 seulement · fail2ban            │
   │                                                                     │
   │  Caddy : certificat HTTPS automatique + jeton obligatoire           │
   │        │                                                            │
   │  adk api_server (127.0.0.1:8000, invisible depuis Internet)        │
   │   · utilisateur système "agents" sans droits                       │
   │   · code en lecture seule (/opt/agents-ia)                          │
   │   · conversations en base SQLite (/var/lib/agents-ia)               │
   │        │                                                            │
   │  Pont Telegram (optionnel) · Maintenance nocturne (sauvegarde+purge)│
   └────────┬────────────────────────────────────────────────────────────┘
            │
   Modèle d'IA au choix : Gemini, Mistral, Claude, OpenAI, ou votre propre serveur GPU
```

| Fichier | Rôle |
|---|---|
| `installer.sh` | Installe et sécurise tout, en une commande. Relançable pour les mises à jour. |
| `agents.env.modele` | Modèle de configuration : choix du modèle, clés, durées de conservation. |
| `agents-ia.service` | Service systemd durci (redémarrage automatique, moindre privilège). |
| `Caddyfile.modele` | HTTPS automatique + refus de toute requête sans jeton. |
| `maintenance.sh` | Sauvegarde quotidienne + suppression des vieilles conversations (RGPD). |
| `telegram_pont.py` | Pilotage par Telegram, avec liste blanche d'utilisateurs. |
| `tester_api.sh` | Vérifie l'installation depuis votre poste. |
| `MODELES_ET_RGPD.md` | Quel modèle choisir selon vos données, et vos obligations. |
| `CHECKLIST_PRODUCTION.md` | Les points à valider avant d'ouvrir le service. |

---

## ✅ Prérequis

- **Un VPS Ubuntu 24.04** (ou Debian 12), de préférence chez un **hébergeur européen**.
  - Modèle via API (Gemini, Mistral, Claude…) : **2 vCPU, 4 Go de RAM, 40 Go de disque** suffisent largement.
  - Modèle local : voir « Faire tourner un modèle local » plus bas.
- **Un nom de domaine** avec un enregistrement DNS de type **A** pointant vers l'adresse IP du VPS (ex. `agents.monentreprise.fr`).
- **Une clé API d'un fournisseur en niveau payant** (voir `MODELES_ET_RGPD.md`). Le niveau gratuit de Gemini est **interdit** pour un service proposé à des utilisateurs dans l'Union européenne.

---

## Étape 1 : sécuriser l'accès SSH (avant tout le reste)

Depuis **votre poste**, si vous n'avez pas encore de clé SSH :

```bash
ssh-keygen -t ed25519
ssh-copy-id root@ADRESSE_IP_DU_VPS
```

Puis, **sur le VPS**, créez un compte d'administration et interdisez les mots de passe :

```bash
adduser admin && usermod -aG sudo admin
mkdir -p /home/admin/.ssh && cp ~/.ssh/authorized_keys /home/admin/.ssh/ && chown -R admin:admin /home/admin/.ssh
printf 'PasswordAuthentication no\nPermitRootLogin no\n' > /etc/ssh/sshd_config.d/99-durcissement.conf
systemctl restart ssh
```

> ⚠️ Avant de fermer votre session, vérifiez dans un **second terminal** que `ssh admin@ADRESSE_IP_DU_VPS` fonctionne.

## Étape 2 : choisir les agents à mettre en service

On ne déploie **jamais** les exercices. Sur votre poste ou dans Codespaces, créez un dossier `agents_prod` avec uniquement ce qui doit tourner :

```bash
mkdir agents_prod
cp agents/commun.py agents_prod/
cp -r agents/mon_agent agents_prod/
```

Enregistrez (commit) et envoyez (push) sur votre dépôt GitHub.

## Étape 3 : récupérer le dépôt sur le VPS

```bash
sudo apt-get install -y git
git clone https://github.com/VOTRE-COMPTE/VOTRE-DEPOT.git atelier
cd atelier
```

> Dépôt privé ? Créez un jeton d'accès GitHub en **lecture seule** limité à ce dépôt (Settings, Developer settings, Fine-grained tokens) et utilisez-le comme mot de passe lors du `git clone`.

## Étape 4 : installer

```bash
sudo bash deploiement/installer.sh agents.monentreprise.fr
```

Le script, en quelques minutes :
1. installe Python, Caddy, le pare-feu, fail2ban et les mises à jour de sécurité automatiques ;
2. crée l'utilisateur système `agents`, sans shell ni droits d'administration ;
3. copie vos agents en lecture seule dans `/opt/agents-ia` et installe les **versions figées** de `requirements.txt` ;
4. génère un **jeton d'accès aléatoire** et la configuration `/etc/agents-ia/agents.env` ;
5. configure Caddy (HTTPS automatique + jeton obligatoire) et les services systemd ;
6. planifie la maintenance nocturne (sauvegarde + purge RGPD).

**Notez le jeton affiché à la fin** dans votre gestionnaire de mots de passe.

## Étape 5 : choisir le modèle et renseigner la clé

```bash
sudo nano /etc/agents-ia/agents.env
```

Décommentez **une** option de modèle (A à G), renseignez la clé correspondante, puis :

```bash
sudo systemctl restart agents-ia
```

## Étape 6 : tester depuis votre poste

```bash
bash deploiement/tester_api.sh https://agents.monentreprise.fr VOTRE_JETON mon_agent "Bonjour"
```

Résultat attendu : la sonde répond `ok`, la requête sans jeton est refusée (code **401**), puis l'agent répond.

## Étape 7 (optionnel) : piloter par Telegram

1. Dans Telegram, ouvrez **@BotFather**, envoyez `/newbot` et copiez le jeton.
2. Dans `/etc/agents-ia/agents.env`, renseignez `TELEGRAM_BOT_TOKEN` et `TELEGRAM_AGENT`.
3. Démarrez le pont : `sudo systemctl enable --now agents-telegram`
4. Envoyez `/id` à votre bot : il vous répond votre identifiant numérique.
5. Ajoutez cet identifiant dans `TELEGRAM_UTILISATEURS_AUTORISES`, puis `sudo systemctl restart agents-telegram`.

Toute personne absente de la liste blanche est refusée. Au premier message, le bot indique qu'il s'agit d'une IA (obligation de transparence de l'AI Act).

> ⚠️ Les messages transitent par les serveurs de Telegram. Pas de données sensibles ni de données clients par ce canal sans analyse préalable.

---

## 🔄 Mettre à jour

```bash
cd atelier && git pull
sudo bash deploiement/installer.sh agents.monentreprise.fr
```

La configuration, le jeton et les conversations sont **conservés**. Seuls le code et les dépendances sont remplacés.

**Avant toute montée de version** de `google-adk` dans `requirements.txt` : testez d'abord dans Codespaces, et lancez vos tests d'évaluation (`adk eval`, voir la checklist).

## 🖥️ Montrer l'interface web pendant une démonstration

L'interface `adk web` est un outil de **développement** : elle ne doit **jamais** être exposée sur Internet. Pour une démonstration, ouvrez un tunnel SSH chiffré depuis votre poste :

```bash
# Sur le VPS (s'arrête avec Ctrl+C)
sudo -u agents bash -c 'set -a; . /etc/agents-ia/agents.env; set +a; /opt/agents-ia/venv/bin/adk web --host 127.0.0.1 --port 8001 --session_service_uri memory:// --artifact_service_uri memory:// /opt/agents-ia/agents'

# Sur votre poste, dans un autre terminal
ssh -L 8001:127.0.0.1:8001 admin@agents.monentreprise.fr
```

Puis ouvrez http://localhost:8001 dans votre navigateur.

## 💪 Aller plus loin : « toutes les tâches possibles »

| Besoin | Où ça tourne | Ce qu'il faut |
|---|---|---|
| Raisonnement, rédaction, analyse | Chez le fournisseur du modèle | Le VPS de base suffit |
| Outils Python (calculs, fichiers, PDF, Excel, OCR) | Sur le VPS | Plus de RAM et de CPU selon le volume |
| Connexion aux logiciels de l'entreprise | Sur le VPS | Outils ADK ou serveurs **MCP** (ADK les prend en charge) |
| Tâches planifiées | Sur le VPS | Un `cron` ou un timer systemd qui appelle l'API |
| Modèle local, confidentialité maximale | Serveur GPU | Voir ci-dessous |

**Faire tourner un modèle local.** Un VPS classique n'a pas de carte graphique : un modèle local y sera très lent. La bonne architecture est un **serveur GPU séparé** (location chez un hébergeur européen) qui fait tourner **vLLM** ou **Ollama**, relié au VPS par un réseau privé (ou WireGuard). Dans `agents.env`, l'option F suffit à le brancher. Ordre de grandeur : un modèle de 7 à 8 milliards de paramètres quantifié tient dans environ 8 Go de mémoire graphique, un modèle de 30 milliards dans environ 24 Go. Vérifiez que le modèle choisi gère bien les **outils** (function calling).

## 🆘 Dépannage

| Symptôme | Commande |
|---|---|
| Voir ce que fait le service | `journalctl -u agents-ia -f` |
| Le service ne démarre pas | `journalctl -u agents-ia -n 50` (souvent une clé manquante dans `agents.env`) |
| Erreur HTTPS / certificat | `journalctl -u caddy -n 50` (le DNS pointe-t-il vers le VPS ? ports 80 et 443 ouverts ?) |
| Code 401 alors que le jeton est bon | L'en-tête doit être exactement `Authorization: Bearer VOTRE_JETON` |
| Changer le jeton | `openssl rand -hex 32`, le mettre dans `agents.env`, puis relancer `installer.sh` |
| Restaurer une sauvegarde | `sudo systemctl stop agents-ia`, puis `gunzip -c /var/backups/agents-ia/sessions-DATE.db.gz > /var/lib/agents-ia/sessions.db`, `chown agents:agents` ce fichier, puis `sudo systemctl start agents-ia` |
