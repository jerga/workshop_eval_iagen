# Workshop — Évaluation d'une application GenAI

Bienvenue ! Ce workshop t'apprend à évaluer une application IA Gen de façon progressive — de zéro jusqu'à une vraie démarche industrielle.

## Pourquoi c'est différent d'évaluer une app IA Gen ?

➡️ Une application **classique** est **déterministe** : pour une entrée donnée, elle produit toujours la même sortie. On peut donc écrire des tests d'intégration classiques (assertions exactes, valeurs attendues) et les rejouer à l'infini.

➡️ Une application **IA Gen** introduit du **non-déterminisme** via le LLM : la même question peut produire des réponses différentes (formulation, ordre, niveau de détail) tout en restant correctes. Une assertion d'égalité stricte n'a alors plus vraiment de sens.

Quelques conséquences :

- **Les tests d'intégration classiques ne suffisent plus.** Ils restent utiles (la chaîne technique tourne, le format est respecté, l'outil attendu est bien appelé), mais ils doivent être **complétés** par d'autres types d'évaluations (grounding, ton, sécurité, LLM-as-a-judge...).
- **C'est plus difficile à cadrer.** Les exigences ne s'expriment pas comme en IT classique : « la réponse doit rester fidèle au contexte », « le ton doit rester professionnel », « l'agent ne doit pas sortir de son rôle ». Ce n'est pas forcément naturel quand on vient du test logiciel traditionnel.
- **Il faut adapter l'évaluation au cas d'usage.** Tous ne s'évaluent pas de la même façon : le bon dispositif dépend de qui utilise l'app, du contexte métier, et des risques associés.

## L'application "exemple"

Pour ce workshop, on a besoin d'un cas d'usage concret à évaluer. On a donc créé une petite **application IA Gen agentique**, volontairement simple, qui sert de fil rouge à tous les exercices.

> [!NOTE]
> Cette app est **bricolée pour le workshop** : elle n'est **pas prod-ready**.
> Pas besoin de lire le code ni de comprendre son fonctionnement interne — il suffit de lire les explications ci-dessous.

Il s'agit d'un **CLI RAG** dans le domaine support IT / FAQ. Voici ce qu'elle fait :

```
Question utilisateur
        │
        ▼
┌─────────────────────┐
│  Retrieval          │  ← recherche dans la base de connaissances (embeddings)
└─────────┬───────────┘
          │  contexte récupéré
          ▼
┌─────────────────────┐
│  LLM                │  ← génère une réponse contextualisée
└─────────┬───────────┘
          │
          ▼
     Réponse + (optionnel) appel d'outil  →  ex: get_service_status
```

Fonctionnalités :
- Répond à des questions de support IT en français
- Utilise une base documentaire pour contextualiser les réponses
- Peut appeler des outils (ex : `get_service_status`)
- S'utilise en ligne de commande :


## Organisation du repo

```
app/                        → l'agent support IT
  cli.py                    → point d'entrée CLI
  rag_agent.py              → logique RAG + appels LLM + outils

eval/                       → le projet d'évaluation IA
  common/                   → utilitaires partagés (config, dataset loader, résultats)
  step1_setup/              → mise en place de l'environnement
  step2_foundations/        → introduction, exemples des familles d'évaluation
  step3_industrialization/  → pipelines avec deepeval
  step4_production/         → intégration Langfuse Cloud
  solutions/                → solutions exécutables, TP par TP

scripts/
  check_env.py              → vérifie que l'environnement est correctement configuré
  verify_workshop.py        → vérification globale du workshop

docs/                       → tu es ici 👋
```

## Progression

1. **01 - Setup** : vérifier que l'env tourne sur un cas simple déterministe
2. **02 - Foundations** : comprendre et implémenter les principales familles d'évaluation
3. **03 - Industrialization** : structurer un pipeline de non-régression avec un approche modulaire et DeepEval
4. **04 - Production** : ajouter Langfuse pour le suivi, les traces et les expérimentations


Chaque TP dispose d'une version solution exécutable dans `eval/solutions/`.

💡 Utilise les solutions pour débloquer si besoin — mais essaie d'abord !
