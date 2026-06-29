#!/usr/bin/env bash
set -euo pipefail

# Installe les dépendances dans un venv isolé (.venv) à partir du pyproject.toml
uv sync

# Prépare le fichier .env si absent (les clés restent à compléter)
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Fichier .env créé à partir de .env.example — pense à renseigner tes clés."
fi

# Active automatiquement le venv (.venv) dans chaque nouveau terminal bash
ACTIVATE_LINE="source \"${PWD}/.venv/bin/activate\" 2>/dev/null || true"
if ! grep -qF "$ACTIVATE_LINE" ~/.bashrc 2>/dev/null; then
  echo "$ACTIVATE_LINE" >> ~/.bashrc
  echo "Activation automatique du venv ajoutée à ~/.bashrc."
fi

echo "Environnement prêt : Python 3.12 + uv + dépendances installées."
