from __future__ import annotations


def family_summary(name: str, case_results: list[dict[str, object]]) -> dict[str, object]:
    passed = sum(1 for item in case_results if bool(item.get("passed")))
    total = len(case_results)
    return {
        "family": name,
        "passed": passed,
        "total": total,
        "success": passed == total,
        "details": case_results,
    }


def print_suite_report(family_reports: list[dict[str, object]]) -> int:
    print("\n=== EVAL SUITE REPORT ===")
    total_passed = 0
    total_cases = 0

    for report in family_reports:
        family = str(report["family"])
        passed = int(report["passed"])
        total = int(report["total"])
        success = bool(report["success"])
        status = "OK" if success else "FAIL"
        print(f"[{status}] {family}: {passed}/{total}")
        total_passed += passed
        total_cases += total

    print(f"Global: {total_passed}/{total_cases} cas OK")
    return 0 if all(bool(item["success"]) for item in family_reports) else 1
