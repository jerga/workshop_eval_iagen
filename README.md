# Workshop — Évaluation d'une application GenAI

Workshop pratique (1 h à 2 h) pour apprendre à évaluer une application GenAI (agent de support IT), de façon progressive : du smoke test jusqu'à une démarche industrielle.

## Démarrer

Deux approches sont possibles : **dans le cloud avec GitHub Codespaces** (rien à installer) ou **en local** (avec les prérequis ci-dessous).

> [!WARNING]
> Sur des laptops "entreprise", attention aux VPN ou proxy qui peuvent bloquer les installations ou les accès aux LLM grand public "cloud".

### GitHub Codespaces

Evite tout problème de configuration locale (mais demande un compte Github + de ne pas avoir épuisé sont "quota" Codespace).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jerga/workshop_eval_iagen?quickstart=1)


### En local

Installe les prérequis suivants :

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/) (ou `winget install Python.Python.3.12` sous Windows).
- **uv** (gestionnaire de paquets/venv) :
  - Windows : `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - macOS / Linux : `curl -LsSf https://astral.sh/uv/install.sh | sh`


### Backend LLM

Un endpoint **OpenAI-compatible** pour un LLM et un modèle embeddings est nécessaire.

Un service par défaut et des clés sont fournies pour le workshop en présentiel.



## Documentation

Tout le parcours se trouve dans [`docs/`](docs/index.md), il suffit de suivre les étapes :

- [00 — Overview](docs/00-overview.md)
- [01 — Setup](docs/01-setup.md)
- [02 — Foundations](docs/02-foundations.md)
- [03 — Industrialization](docs/03-industrialization.md)
- [04 — Production](docs/04-production.md)

👉 Commence par [docs/00-overview.md](docs/00-overview.md).
