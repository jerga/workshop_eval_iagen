# 04 — Production

## 📚 Ressources

- Scripts production : `eval/step4_production/`
- Datasets locaux : `eval/step4_production/datasets/`
- Traces exemple : `eval/step4_production/traces/sample_production_traces.jsonl`

---

## Pourquoi Langfuse ?

Les TP précédents couvrent bien l'évaluation locale. Mais en production, tu veux :
- **Tracer** chaque exécution (input, output, latence, tokens)
- **Versionner** tes datasets de référence
- **Comparer** des variantes (prompt A vs prompt B) sur un protocole identique

C'est exactement ce que Langfuse apporte. À ce TP, tu vas :
1. Promouvoir un dataset CSV local vers Langfuse
2. Importer des traces en dataset pour créer des cas de test à partir du vrai usage
3. Lancer une expérimentation baseline vs variante

---

## Prérequis supplémentaires

En plus de l'env déjà configuré, ajoute les clés Langfuse Cloud dans ton `.env` :

```
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

> [!IMPORTANT]
> Ces clés sont différentes des clés LLM. Ajoute-les maintenant avant de continuer.

---

## Étape 1 — Promouvoir un dataset local vers Langfuse

Ouvre [`eval/step4_production/promote_dataset_to_langfuse.py`](../eval/step4_production/promote_dataset_to_langfuse.py).

### TODO-STEP4-01 : Nom du dataset promu

Complète le suffixe du nom du dataset pour le versionner clairement.

💡 Un suffixe comme `-v1` ou `-baseline` permet de distinguer les versions dans l'UI Langfuse.

<details>
  <summary>Indice — nom de dataset</summary>

  ```python
  dataset_name = f"it-support-baseline-v1"
  ```
</details>

Lance ensuite :

```bash
uv run python eval/step4_production/promote_dataset_to_langfuse.py
```

✅ Un dataset doit apparaître dans ton projet Langfuse Cloud.

---

## Étape 2 — Importer des traces en dataset

Ouvre [`eval/step4_production/import_traces_to_dataset.py`](../eval/step4_production/import_traces_to_dataset.py).

### TODO-STEP4-02 : Extraction de l'expected_output

Complète l'extraction de `expected_output` depuis les traces.

⚠️ Si `expected_output` est absent de la trace, ne plante pas — utilise la réponse de la trace comme valeur par défaut.

<details>
  <summary>Indice — traces vers dataset</summary>

  ```python
  expected_output = record.get("expected_output") or record.get("answer", "")
  ```
</details>

```bash
uv run python eval/step4_production/import_traces_to_dataset.py
```

---

## Étape 3 — Comparer des variantes

Ouvre [`eval/step4_production/experiment_runner.py`](../eval/step4_production/experiment_runner.py) — c'est ici que se passe la comparaison.

### TODO-STEP4-03 : Prompt de la variante

Définis le prompt pour la variante à comparer contre la baseline.

💡 Une variante simple peut ajouter une contrainte de style sans changer la logique — c'est ce qu'on cherche à mesurer ici.

<details>
  <summary>Indice — variante</summary>

  ```python
  variant_instruction = "Répondez en 2 phrases maximum, avec une action immédiate."
  ```
</details>

```bash
uv run python eval/step4_production/run_langfuse_experiment.py
```

### ✅ Résultat attendu

- Le script affiche les scores des deux variantes
- Un gagnant est désigné
- Les traces sont visibles dans Langfuse Cloud


---

## Solutions complètes

  - [`eval/solutions/step4/experiment_runner_solution.py`](../eval/solutions/step4/experiment_runner_solution.py)
  - [`eval/solutions/step4/langfuse_integration_solution.py`](../eval/solutions/step4/langfuse_integration_solution.py)

