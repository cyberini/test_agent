#!/usr/bin/env bash
# Teste l'API de production depuis n'importe quel poste.
# Usage : ./tester_api.sh https://agents.mondomaine.fr JETON mon_agent "Votre question"
set -euo pipefail

URL="${1:?URL manquante (ex. https://agents.mondomaine.fr)}"
JETON="${2:?Jeton manquant}"
AGENT="${3:-mon_agent}"
QUESTION="${4:-Bonjour, présentez-vous en une phrase.}"
UTILISATEUR="test-api"
AUTH="Authorization: Bearer $JETON"

echo "1) Sonde publique :"; curl -fsS "$URL/sante"; echo
echo "2) Sans jeton (doit être refusé) :"; curl -s -o /dev/null -w "   code HTTP %{http_code}\n" "$URL/list-apps"
echo "3) Agents disponibles :"; curl -fsS -H "$AUTH" "$URL/list-apps"; echo

SESSION="$(curl -fsS -X POST -H "$AUTH" -H 'Content-Type: application/json' -d '{}' \
  "$URL/apps/$AGENT/users/$UTILISATEUR/sessions" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
echo "4) Session créée : $SESSION"

echo "5) Question à l'agent :"
python3 - "$QUESTION" "$AGENT" "$UTILISATEUR" "$SESSION" <<'EOF' > /tmp/requete_agent.json
import json, sys
q, app, user, sess = sys.argv[1:]
print(json.dumps({"appName": app, "userId": user, "sessionId": sess,
                  "newMessage": {"role": "user", "parts": [{"text": q}]}}))
EOF
curl -fsS -X POST -H "$AUTH" -H 'Content-Type: application/json' --data @/tmp/requete_agent.json "$URL/run" \
  | python3 -c '
import sys, json
for e in json.load(sys.stdin):
    for p in (e.get("content") or {}).get("parts", []):
        if p.get("text"): print("   [" + e.get("author", "?") + "] " + p["text"])
        if p.get("functionCall"): print("   [outil appelé] " + p["functionCall"]["name"])
'
rm -f /tmp/requete_agent.json
