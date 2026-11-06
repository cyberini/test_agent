#!/usr/bin/env bash
# ═════════════════════════════════════════════════════════════════════
#  Installation des agents IA en production sur un VPS Ubuntu 24.04 / Debian 12
#
#  Usage (depuis la racine du dépôt cloné sur le VPS) :
#     sudo bash deploiement/installer.sh agents.mondomaine.fr [dossier_agents]
#
#  dossier_agents : dossier contenant UNIQUEMENT les agents à mettre en service
#                   + commun.py (par défaut : agents_prod, sinon agents).
#
#  Le script peut être relancé sans risque pour mettre à jour le code :
#  il ne remplace jamais la configuration ni les données existantes.
# ═════════════════════════════════════════════════════════════════════
set -euo pipefail

DOMAINE="${1:?Usage : sudo bash deploiement/installer.sh agents.mondomaine.fr [dossier_agents]}"
DEPOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -n "${2:-}" ]]; then SOURCE_AGENTS="$2"
elif [[ -d "$DEPOT/agents_prod" ]]; then SOURCE_AGENTS="$DEPOT/agents_prod"
else SOURCE_AGENTS="$DEPOT/agents"; fi

APP=/opt/agents-ia
DATA=/var/lib/agents-ia
CONF=/etc/agents-ia
UTILISATEUR=agents

info()  { echo -e "\n\033[1;34m▶ $*\033[0m"; }
alerte(){ echo -e "\033[1;33m⚠ $*\033[0m"; }
stop()  { echo -e "\033[1;31m✖ $*\033[0m" >&2; exit 1; }

# ── Vérifications ────────────────────────────────────────────────────
[[ $EUID -eq 0 ]] || stop "Lancez ce script avec sudo."
[[ -r /etc/os-release ]] && . /etc/os-release
[[ "${ID:-}" == "ubuntu" || "${ID:-}" == "debian" ]] || stop "Système non pris en charge (Ubuntu 24.04 ou Debian 12 attendu)."
[[ "$DOMAINE" =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]] || stop "Nom de domaine invalide : $DOMAINE"
[[ -f "$SOURCE_AGENTS/commun.py" ]] || stop "commun.py introuvable dans $SOURCE_AGENTS"
[[ -f "$DEPOT/requirements.txt" ]] || stop "requirements.txt introuvable dans $DEPOT"
if find "$SOURCE_AGENTS" -name ".env" | grep -q .; then
  stop "Un fichier .env est présent dans $SOURCE_AGENTS : retirez-le, les secrets vont dans $CONF/agents.env"
fi

# ── 1. Paquets système ───────────────────────────────────────────────
info "Installation des paquets système"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q python3 python3-venv python3-pip sqlite3 ufw fail2ban \
  unattended-upgrades curl gnupg debian-keyring debian-archive-keyring apt-transport-https openssl

if ! command -v caddy >/dev/null; then
  info "Installation de Caddy (serveur HTTPS) depuis son dépôt officiel"
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor --yes -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' > /etc/apt/sources.list.d/caddy-stable.list
  chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg /etc/apt/sources.list.d/caddy-stable.list
  apt-get update -q && apt-get install -y -q caddy
fi

# ── 2. Utilisateur dédié et dossiers ─────────────────────────────────
info "Création de l'utilisateur de service '$UTILISATEUR' (sans shell, sans droits d'administration)"
id "$UTILISATEUR" &>/dev/null || useradd --system --home-dir "$DATA" --shell /usr/sbin/nologin "$UTILISATEUR"
install -d -m 755 -o root -g root "$APP" "$APP/deploiement"
install -d -m 700 -o "$UTILISATEUR" -g "$UTILISATEUR" "$DATA" "$DATA/artifacts"
install -d -m 750 -o root -g "$UTILISATEUR" "$CONF"

# ── 3. Code (lecture seule pour le service) ──────────────────────────
info "Copie du code depuis $SOURCE_AGENTS"
rm -rf "$APP/agents"
cp -r "$SOURCE_AGENTS" "$APP/agents"
find "$APP/agents" -name "__pycache__" -prune -exec rm -rf {} +
cp "$DEPOT/requirements.txt" "$APP/"
cp "$DEPOT/deploiement/telegram_pont.py" "$DEPOT/deploiement/maintenance.sh" "$DEPOT/deploiement/README.md" "$APP/deploiement/"
chown -R root:root "$APP"
chmod -R go-w "$APP"
chmod 755 "$APP/deploiement/maintenance.sh"

info "Environnement Python (versions figées de requirements.txt)"
[[ -x "$APP/venv/bin/python" ]] || python3 -m venv "$APP/venv"
"$APP/venv/bin/pip" install -q --upgrade pip
"$APP/venv/bin/pip" install -q -r "$APP/requirements.txt"

# ── 4. Configuration et secrets (jamais écrasés) ─────────────────────
if [[ ! -f "$CONF/agents.env" ]]; then
  info "Création de $CONF/agents.env avec un jeton d'accès aléatoire"
  JETON="$(openssl rand -hex 32)"
  sed "s/^AGENTS_API_TOKEN=.*/AGENTS_API_TOKEN=$JETON/" "$DEPOT/deploiement/agents.env.modele" > "$CONF/agents.env"
  NOUVELLE_CONF=1
else
  info "Configuration existante conservée ($CONF/agents.env)"
  JETON="$(grep -E '^AGENTS_API_TOKEN=' "$CONF/agents.env" | cut -d= -f2- | tr -d '"'"'"' ')"
  NOUVELLE_CONF=0
fi
[[ "$JETON" =~ ^[A-Za-z0-9_-]{32,}$ ]] || stop "AGENTS_API_TOKEN absent ou trop court dans $CONF/agents.env (openssl rand -hex 32)"
chown root:"$UTILISATEUR" "$CONF/agents.env"
chmod 640 "$CONF/agents.env"

# ── 5. Caddy : HTTPS + jeton obligatoire ─────────────────────────────
info "Configuration de Caddy pour https://$DOMAINE"
[[ -f /etc/caddy/Caddyfile && ! -f /etc/caddy/Caddyfile.origine ]] && cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.origine
sed -e "s/__DOMAINE__/$DOMAINE/g" -e "s/__JETON__/$JETON/g" "$DEPOT/deploiement/Caddyfile.modele" > /etc/caddy/Caddyfile
chown root:caddy /etc/caddy/Caddyfile
chmod 640 /etc/caddy/Caddyfile
install -d -m 750 -o caddy -g caddy /var/log/caddy
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null || stop "Caddyfile invalide"

# ── 6. Services systemd ──────────────────────────────────────────────
info "Installation des services systemd"
install -m 644 "$DEPOT/deploiement/agents-ia.service" /etc/systemd/system/agents-ia.service
install -m 644 "$DEPOT/deploiement/agents-telegram.service" /etc/systemd/system/agents-telegram.service
systemctl daemon-reload
systemctl enable --now agents-ia.service
systemctl restart agents-ia.service
systemctl reload caddy 2>/dev/null || systemctl restart caddy
if grep -qE '^TELEGRAM_BOT_TOKEN=.+' "$CONF/agents.env"; then
  systemctl enable --now agents-telegram.service
  systemctl restart agents-telegram.service
fi

# ── 7. Maintenance quotidienne (sauvegarde + purge RGPD) ─────────────
info "Planification de la maintenance quotidienne (03:15)"
cat > /etc/cron.d/agents-ia <<EOF
# Sauvegarde et purge des conversations (voir $APP/deploiement/maintenance.sh)
15 3 * * * root $APP/deploiement/maintenance.sh >> /var/log/agents-ia-maintenance.log 2>&1
EOF
chmod 644 /etc/cron.d/agents-ia

# ── 8. Durcissement du serveur ───────────────────────────────────────
info "Pare-feu : seuls SSH, HTTP et HTTPS sont ouverts"
PORT_SSH="$(sshd -T 2>/dev/null | awk '/^port /{print $2; exit}')"; PORT_SSH="${PORT_SSH:-22}"
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow "$PORT_SSH"/tcp >/dev/null
ufw allow 80/tcp >/dev/null
ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null

info "Protection contre le bruteforce SSH (fail2ban) et mises à jour de sécurité automatiques"
systemctl enable --now fail2ban >/dev/null
echo 'APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";' > /etc/apt/apt.conf.d/20auto-upgrades

# ── 9. Vérifications finales ─────────────────────────────────────────
info "Vérification du service"
for _ in $(seq 1 30); do curl -fsS http://127.0.0.1:8000/list-apps >/dev/null 2>&1 && break; sleep 1; done
if AGENTS="$(curl -fsS http://127.0.0.1:8000/list-apps)"; then
  echo "   Agents en service : $AGENTS"
else
  alerte "Le service ne répond pas. Consultez : journalctl -u agents-ia -n 50"
fi
grep -qE '^PasswordAuthentication\s+no' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null \
  || alerte "SSH accepte encore les mots de passe : passez aux clés SSH (voir README, étape 1)."

echo
echo "════════════════════════════════════════════════════════════════"
echo " ✅ Installation terminée : https://$DOMAINE"
echo "════════════════════════════════════════════════════════════════"
if [[ "$NOUVELLE_CONF" == 1 ]]; then
  echo " 1. Renseignez le modèle et la clé API :  sudo nano $CONF/agents.env"
  echo "    puis :                                  sudo systemctl restart agents-ia"
fi
echo " • Jeton d'accès à l'API (à conserver dans un gestionnaire de mots de passe) :"
echo "     $JETON"
echo " • Test :     bash deploiement/tester_api.sh https://$DOMAINE <jeton> <agent>"
echo " • Journaux : journalctl -u agents-ia -f"
echo "════════════════════════════════════════════════════════════════"
