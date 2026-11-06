# 💻 Installer l'atelier sur ton ordinateur

Deux méthodes. **Choisis la méthode 1 si tu débutes** : elle est plus simple et plus légère.

---

## Méthode 1 — Python directement (la plus simple)

### Ce qu'il faut
- **Python 3.11, 3.12 ou 3.13** : https://www.python.org/downloads/
  - 🪟 Windows : coche **« Add python.exe to PATH »** au début de l'installation !
- **VS Code** : https://code.visualstudio.com

### Installation
Télécharge le dossier de l'atelier (bouton **Code → Download ZIP** sur GitHub), décompresse-le, ouvre-le dans VS Code, puis dans le terminal (**Terminal → Nouveau terminal**) :

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
> Si PowerShell refuse d'activer : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, puis réessaie.

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Colle ta clé dans `.env`, puis : `adk web agents` et ouvre http://localhost:8000

> À chaque nouvelle session, réactive l'environnement (`.venv\Scripts\Activate.ps1` ou `source .venv/bin/activate`) avant `adk web agents`.

---

## Méthode 2 — Docker + Dev Container (identique à Codespaces)

Plus lourde à installer, mais l'environnement est **exactement le même** que dans Codespaces.

### Prérequis par système

| | Windows | macOS | Linux |
|---|---|---|---|
| Logiciel | Docker Desktop | Docker Desktop | Docker Engine (ou Docker Desktop) |
| Version | Windows 10 22H2 ou 11, **WSL 2** | 3 dernières versions de macOS | Ubuntu, Debian, Fedora récents |
| Particularité | Virtualisation activée dans le BIOS | Choisir **Apple Silicon** ou **Intel** au téléchargement | Ajouter ton utilisateur au groupe `docker` |
| Droits admin | **Oui** | Oui | Oui (sudo) |
| RAM / disque | 8 Go min. (16 conseillés) · ~10 Go libres | idem | idem |

### Installation
1. Installe **Docker Desktop** : https://www.docker.com/products/docker-desktop/ (Linux : https://docs.docker.com/engine/install/)
2. Lance Docker Desktop et attends que la baleine 🐳 soit verte.
3. Installe **VS Code** puis l'extension **Dev Containers** (Microsoft).
4. Ouvre le dossier de l'atelier dans VS Code → en bas à droite, clique sur **« Reopen in Container »** (ou F1 → *Dev Containers: Reopen in Container*).
5. Premier lancement : 3 à 5 minutes. Ensuite, comme dans Codespaces : clé dans `.env`, puis `adk web agents`.

### ⚠️ Les pièges fréquents
- **PC d'entreprise** : l'installation de Docker est souvent bloquée par le service informatique (droits admin, WSL 2 désactivé). Préfère alors Codespaces ou la méthode 1.
- **Licence Docker Desktop** : gratuite pour un usage personnel, pour l'apprentissage et pour les entreprises de moins de 250 salariés et 10 M$ de CA. Sur un poste pro d'une grande entreprise, pour un usage professionnel au-delà de la formation, une licence payante est requise. Alternatives gratuites et open source : **Podman Desktop** ou **Rancher Desktop**.
- **Windows** : si Docker affiche « WSL 2 installation is incomplete », ouvre PowerShell en admin et tape `wsl --install`, puis redémarre.
