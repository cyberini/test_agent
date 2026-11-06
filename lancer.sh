#!/usr/bin/env bash
# Lance l'interface web ADK (adk web) sur le port 8000.
#
# Dans GitHub Codespaces, le navigateur passe par une adresse en *.app.github.dev,
# relayée par le proxy de GitHub. Par sécurité, ADK refuse par défaut les requêtes
# qui ne viennent pas de localhost (protection contre le "DNS rebinding").
# Or le relais de GitHub réécrit l'en-tête "Origin" en https://localhost:8000
# (https, alors qu'ADK tourne en http) : ADK le refuse donc par défaut.
# On autorise UNIQUEMENT cette origine et l'adresse de votre propre Codespace.
# Le serveur reste en écoute sur 127.0.0.1. Ne passez jamais le port 8000 en "Public".
cd "$(dirname "$0")" || exit 1

if [ -n "${CODESPACE_NAME:-}" ]; then
  ORIGINE="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
  echo "🌐 Codespace détecté : adresse autorisée = $ORIGINE"
  pkill -f "adk web" 2>/dev/null && sleep 1   # arrête une éventuelle ancienne instance
  exec adk web --port 8000 \
    --allow_origins "https://localhost:8000" \
    --allow_origins "$ORIGINE" \
    "$@" agents
else
  exec adk web --port 8000 "$@" agents
fi
