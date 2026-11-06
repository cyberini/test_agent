#!/usr/bin/env bash
# Maintenance quotidienne (lancée par /etc/cron.d/agents-ia) :
#   1. sauvegarde de la base des conversations et des fichiers produits ;
#   2. suppression des sauvegardes trop anciennes ;
#   3. suppression des conversations au-delà de la durée de conservation (RGPD).
set -euo pipefail

CONF="${CONF:-/etc/agents-ia/agents.env}"
DATA="${DATA:-/var/lib/agents-ia}"
SAUVEGARDES="${SAUVEGARDES:-/var/backups/agents-ia}"

# Lecture d'une variable du fichier de configuration, sans l'exécuter
lire() { grep -E "^$1=" "$CONF" | tail -n1 | cut -d= -f2- | tr -d '"'"'"' '; }
RETENTION_JOURS="$(lire RETENTION_JOURS)"; RETENTION_JOURS="${RETENTION_JOURS:-30}"
SAUVEGARDE_JOURS="$(lire SAUVEGARDE_JOURS)"; SAUVEGARDE_JOURS="${SAUVEGARDE_JOURS:-14}"
[[ "$RETENTION_JOURS" =~ ^[0-9]+$ && "$SAUVEGARDE_JOURS" =~ ^[0-9]+$ ]] || { echo "Durées invalides dans $CONF" >&2; exit 1; }

BASE="$DATA/sessions.db"
DATE="$(date +%F)"
umask 077
mkdir -p "$SAUVEGARDES"
chmod 700 "$SAUVEGARDES"

# 1. Sauvegardes (cohérentes même pendant que le service tourne)
if [[ -f "$BASE" ]]; then
  sqlite3 "$BASE" ".backup '$SAUVEGARDES/sessions-$DATE.db'"
  gzip -f "$SAUVEGARDES/sessions-$DATE.db"
fi
if [[ -d "$DATA/artifacts" ]]; then
  tar -czf "$SAUVEGARDES/fichiers-$DATE.tar.gz" -C "$DATA" artifacts
fi

# 2. Rotation des sauvegardes
find "$SAUVEGARDES" -type f -mtime +"$SAUVEGARDE_JOURS" -delete

# 3. Purge des conversations inactives depuis plus de RETENTION_JOURS jours
if [[ -f "$BASE" ]]; then
  LIMITE="$(( $(date +%s) - RETENTION_JOURS * 86400 ))"
  SUPPRIMEES="$(sqlite3 "$BASE" "
    PRAGMA foreign_keys = ON;
    DELETE FROM events WHERE (app_name, user_id, session_id) IN
      (SELECT app_name, user_id, id FROM sessions WHERE update_time < $LIMITE);
    DELETE FROM sessions WHERE update_time < $LIMITE;
    SELECT changes();")"
  sqlite3 "$BASE" "VACUUM;"
  echo "$(date -Is) maintenance OK : $SUPPRIMEES conversation(s) purgée(s), rétention ${RETENTION_JOURS} j"
fi
