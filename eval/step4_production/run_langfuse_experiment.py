from __future__ import annotations

from pathlib import Path

from eval.step4_production.experiment_runner import ExperimentRunner


def main() -> int:
    datasets_dir = Path(__file__).resolve().parent / "datasets"
    baseline_csv = datasets_dir / "local_baseline.csv"
    variant_csv = datasets_dir / "local_variant.csv"

    runner = ExperimentRunner()
    baseline_result, variant_result = runner.run(
        baseline_csv=baseline_csv,
        variant_csv=variant_csv,
    )

    print("=== Step4 Experiment (Langfuse traces) ===")
    print(
        f"Baseline: {baseline_result.passed}/{baseline_result.total} "
        f"({baseline_result.score:.2%})"
    )
    print(
        f"Variant : {variant_result.passed}/{variant_result.total} "
        f"({variant_result.score:.2%})"
    )

    if variant_result.score > baseline_result.score:
        print("Gagnant: variant")
    elif variant_result.score < baseline_result.score:
        print("Gagnant: baseline")
    else:
        print("Resultat: egalite")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
