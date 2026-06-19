# Application support CLI

Application support IT de type RAG (FAQ interne), avec un tool trivial:

- `get_service_status(service_name)`

## Objectif

Fournir une application simple a evaluer dans les tickets suivants.

## Prerequis

1. Completer les variables dans `.env`
2. Installer les dependances:

```bash
uv sync
```

## Lancer l'application

Question unique:

```bash
uv run python -m app.cli "Comment reinitialiser mon mot de passe ?"
```

Mode interactif:

```bash
uv run python -m app.cli
```

Afficher les metadonnees internes (debug/eval):

```bash
uv run python -m app.cli "Quel est le statut du vpn ?" --show-internal
```

## Notes

- Sortie utilisateur: reponse finale uniquement (style prod-like)
- Les metadonnees internes restent disponibles pour l'evaluation
- Domaine strict: FAQ / support IT
