from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "pyproject.toml",
    ".env.example",
    "README.md",
    "docs/index.md",
    "docs/00-overview.md",
    "docs/01-setup.md",
    "docs/02-foundations.md",
    "docs/03-industrialization.md",
    "docs/04-production.md",
    "scripts/check_env.py",
    "scripts/verify_workshop.py",
    "app/cli.py",
    "app/rag_agent.py",
    "app/data/service_status.json",
    "eval/step1_setup/run_smoke_eval.py",
    "eval/step1_setup/datasets/smoke_eval.csv",
    "eval/step2_foundations/basic_eval_examples.py",
    "eval/step3_industrialization/test_pipeline.py",
    "eval/step4_production/run_langfuse_experiment.py",
    "eval/step4_production/traces/sample_production_traces.jsonl",
    "eval/solutions/step1/run_smoke_eval_solution.py",
    "eval/solutions/step2/basic_eval_examples_solution.py",
    "eval/solutions/step3/run_eval_suite_solution.py",
    "eval/solutions/step4/experiment_runner_solution.py",
    "eval/solutions/step4/langfuse_integration_solution.py",
]

REQUIRED_DATASETS = [
    "eval/step3_industrialization/datasets/judge_goldens.csv",
    "eval/step4_production/datasets/local_baseline.csv",
    "eval/step4_production/datasets/local_variant.csv",
]

MERGED_STEP_READMES = [
    "eval/step1_setup/README.md",
    "eval/step2_foundations/README.md",
    "eval/step3_industrialization/README.md",
    "eval/step4_production/README.md",
]

TODO_SOLUTION_MAP = {
    "TODO-STEP1": "eval/solutions/step1/run_smoke_eval_solution.py",
    "TODO-STEP2": "eval/solutions/step2/basic_eval_examples_solution.py",
    "TODO-STEP3": "eval/solutions/step3/run_eval_suite_solution.py",
    "TODO-STEP4": "eval/solutions/step4/experiment_runner_solution.py",
}


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def _todo_tokens() -> set[str]:
    eval_dir = ROOT / "eval"
    tokens: set[str] = set()

    for file_path in eval_dir.rglob("*.py"):
        if "solutions" in file_path.parts:
            continue
        content = file_path.read_text(encoding="utf-8")
        for match in re.findall(r"TODO-STEP[0-9]+", content):
            tokens.add(match)

    return tokens


def main() -> int:
    print("=== Verification globale workshop ===")

    missing = [item for item in REQUIRED_FILES if not exists(item)]
    if missing:
        print("Fichiers obligatoires manquants:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Structure principale: OK")

    missing_datasets = [item for item in REQUIRED_DATASETS if not exists(item)]
    if missing_datasets:
        print("Datasets manquants:")
        for item in missing_datasets:
            print(f"- {item}")
        return 1

    print("Datasets steps 3 et 4: OK")

    not_merged = [item for item in MERGED_STEP_READMES if exists(item)]
    if not_merged:
        print("README de step encore presents (doivent etre fusionnes vers docs/):")
        for item in not_merged:
            print(f"- {item}")
        return 1

    print("Fusion docs depuis eval/*/README.md: OK")

    todo_tokens = _todo_tokens()
    missing_solution_links: list[str] = []
    for token in sorted(todo_tokens):
        step_key = token.split("-")[0] + "-" + token.split("-")[1]
        solution_path = TODO_SOLUTION_MAP.get(step_key)
        if not solution_path or not exists(solution_path):
            missing_solution_links.append(token)

    if missing_solution_links:
        print("TODO sans solution associee detectee:")
        for token in missing_solution_links:
            print(f"- {token}")
        return 1

    print("Coherence TODO -> solutions: OK")

    required_commands = [
        "uv run python eval/step1_setup/run_smoke_eval.py",
        "uv run python eval/step2_foundations/basic_eval_examples.py",
        "deepeval test run eval/step3_industrialization/test_pipeline.py",
        "uv run python eval/step4_production/run_langfuse_experiment.py",
    ]

    readme_content = (ROOT / "README.md").read_text(encoding="utf-8")
    missing_commands = [cmd for cmd in required_commands if cmd not in readme_content]
    if missing_commands:
        print("Commandes manquantes dans README.md:")
        for cmd in missing_commands:
            print(f"- {cmd}")
        return 1

    print("Coherence commandes README: OK")

    print("Verification finale terminee: repo coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
