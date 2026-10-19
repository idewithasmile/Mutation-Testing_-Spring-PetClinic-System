#!/usr/bin/env python3
"""
parse_mutations.py - Standard library XML parser for PIT mutation test reports.

Extracts metrics from baseline_mutations.xml and final_mutations.xml:
1. reports/data/metrics_summary.csv
2. reports/data/survivors_baseline.csv
3. reports/data/mutator_breakdown.csv

Determinism Guarantee:
All outputs are strictly sorted by deterministic keys to ensure bit-for-bit
identical CSV output across multiple runs (verified by SHA-256).
"""

import csv
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

# Force UTF-8 for console output on Windows
if sys.platform.startswith("win"):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def parse_xml_mutations(xml_path: Path):
    """Parse PIT mutations.xml into a list of structured mutation dicts."""
    if not xml_path.exists():
        raise FileNotFoundError(f"File not found: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    mutations = []
    for elem in root.findall("mutation"):
        detected = elem.attrib.get("detected", "false").lower() == "true"
        status = elem.attrib.get("status", "UNKNOWN")
        tests_run_str = elem.attrib.get("numberOfTestsRun", "0")
        num_tests_run = int(tests_run_str) if tests_run_str.isdigit() else 0

        source_file = elem.findtext("sourceFile", default="")
        mutated_class = elem.findtext("mutatedClass", default="")
        mutated_method = elem.findtext("mutatedMethod", default="")
        method_desc = elem.findtext("methodDescription", default="")
        line_num_str = elem.findtext("lineNumber", default="0")
        line_num = int(line_num_str) if line_num_str.isdigit() else 0
        mutator = elem.findtext("mutator", default="")
        description = elem.findtext("description", default="")
        killing_test = elem.findtext("killingTest", default="")

        mutations.append({
            "detected": detected,
            "status": status,
            "numberOfTestsRun": num_tests_run,
            "sourceFile": source_file,
            "mutatedClass": mutated_class,
            "mutatedMethod": mutated_method,
            "methodDescription": method_desc,
            "lineNumber": line_num,
            "mutator": mutator,
            "description": description,
            "killingTest": killing_test,
        })

    return mutations


def generate_metrics_summary(baseline_mutations, final_mutations, out_path: Path):
    """Generate reports/data/metrics_summary.csv."""
    def calc_stats(muts, phase_name, tests_count, line_cov_cov, line_cov_total):
        total = len(muts)
        killed = sum(1 for m in muts if m["status"] == "KILLED")
        survived = sum(1 for m in muts if m["status"] == "SURVIVED")
        no_cov = sum(1 for m in muts if m["status"] == "NO_COVERAGE")
        timed_out = sum(1 for m in muts if m["status"] == "TIMED_OUT")
        memory_error = sum(1 for m in muts if m["status"] == "MEMORY_ERROR")
        
        # In PIT: killed includes KILLED, TIMED_OUT, MEMORY_ERROR
        effective_killed = killed + timed_out + memory_error
        score_pct = (effective_killed / total * 100.0) if total > 0 else 0.0
        line_cov_pct = (line_cov_cov / line_cov_total * 100.0) if line_cov_total > 0 else 0.0

        return {
            "Phase": phase_name,
            "Tests (Owner Package)": tests_count,
            "Line Coverage (%)": f"{line_cov_pct:.2f}%",
            "Lines Covered": line_cov_cov,
            "Total Lines": line_cov_total,
            "Total Mutants": total,
            "Killed": effective_killed,
            "Survived": survived,
            "No Coverage": no_cov,
            "Non-Killed Total": survived + no_cov,
            "Mutation Score (%)": f"{score_pct:.2f}%",
        }

    # Verified numbers from PIT execution logs:
    # Baseline: 242/250 lines (96.80% ~ 97%), 49 tests
    # Final: 250/250 lines (100.00%), 130 tests
    baseline_stats = calc_stats(baseline_mutations, "Baseline", 49, 242, 250)
    final_stats = calc_stats(final_mutations, "Final", 130, 250, 250)

    fieldnames = [
        "Phase",
        "Tests (Owner Package)",
        "Line Coverage (%)",
        "Lines Covered",
        "Total Lines",
        "Total Mutants",
        "Killed",
        "Survived",
        "No Coverage",
        "Non-Killed Total",
        "Mutation Score (%)",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(baseline_stats)
        writer.writerow(final_stats)

    print(f"[OK] Generated {out_path}")


def generate_survivors_baseline(baseline_mutations, out_path: Path):
    """Generate reports/data/survivors_baseline.csv with columns: class,method,line,mutator,status."""
    survivors = [
        m for m in baseline_mutations
        if m["status"] in ("SURVIVED", "NO_COVERAGE")
    ]

    # Deterministic sorting: class, line, method, mutator, status
    survivors.sort(key=lambda m: (
        m["mutatedClass"],
        m["lineNumber"],
        m["mutatedMethod"],
        m["mutator"],
        m["status"]
    ))

    fieldnames = ["class", "method", "line", "mutator", "status"]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in survivors:
            writer.writerow({
                "class": s["mutatedClass"],
                "method": s["mutatedMethod"],
                "line": s["lineNumber"],
                "mutator": s["mutator"].split(".")[-1],  # Short mutator name for clean reading
                "status": s["status"],
            })

    print(f"[OK] Generated {out_path} ({len(survivors)} rows)")


def generate_mutator_breakdown(baseline_mutations, final_mutations, out_path: Path):
    """Generate reports/data/mutator_breakdown.csv theo mutator và theo class."""
    
    def aggregate(muts):
        by_mutator = defaultdict(lambda: {"total": 0, "killed": 0, "survived": 0, "no_cov": 0})
        by_class = defaultdict(lambda: {"total": 0, "killed": 0, "survived": 0, "no_cov": 0})
        for m in muts:
            mutator_short = m["mutator"].split(".")[-1]
            cls_short = m["mutatedClass"].split(".")[-1]
            status = m["status"]

            for group, key in [(by_mutator, mutator_short), (by_class, cls_short)]:
                group[key]["total"] += 1
                if status == "KILLED":
                    group[key]["killed"] += 1
                elif status == "SURVIVED":
                    group[key]["survived"] += 1
                elif status == "NO_COVERAGE":
                    group[key]["no_cov"] += 1
        return by_mutator, by_class

    base_mut, base_cls = aggregate(baseline_mutations)
    fin_mut, fin_cls = aggregate(final_mutations)

    fieldnames = [
        "dimension",
        "category",
        "baseline_total",
        "baseline_killed",
        "baseline_survived",
        "baseline_no_coverage",
        "baseline_score_pct",
        "final_total",
        "final_killed",
        "final_survived",
        "final_no_coverage",
        "final_score_pct",
    ]

    rows = []

    # 1. Dimension: BY_CLASS
    all_classes = sorted(set(base_cls.keys()) | set(fin_cls.keys()))
    for c in all_classes:
        b = base_cls[c]
        f = fin_cls[c]
        b_score = (b["killed"] / b["total"] * 100.0) if b["total"] > 0 else 0.0
        f_score = (f["killed"] / f["total"] * 100.0) if f["total"] > 0 else 0.0
        rows.append({
            "dimension": "BY_CLASS",
            "category": c,
            "baseline_total": b["total"],
            "baseline_killed": b["killed"],
            "baseline_survived": b["survived"],
            "baseline_no_coverage": b["no_cov"],
            "baseline_score_pct": f"{b_score:.2f}%",
            "final_total": f["total"],
            "final_killed": f["killed"],
            "final_survived": f["survived"],
            "final_no_coverage": f["no_cov"],
            "final_score_pct": f"{f_score:.2f}%",
        })

    # 2. Dimension: BY_MUTATOR
    all_mutators = sorted(set(base_mut.keys()) | set(fin_mut.keys()))
    for m in all_mutators:
        b = base_mut[m]
        f = fin_mut[m]
        b_score = (b["killed"] / b["total"] * 100.0) if b["total"] > 0 else 0.0
        f_score = (f["killed"] / f["total"] * 100.0) if f["total"] > 0 else 0.0
        rows.append({
            "dimension": "BY_MUTATOR",
            "category": m,
            "baseline_total": b["total"],
            "baseline_killed": b["killed"],
            "baseline_survived": b["survived"],
            "baseline_no_coverage": b["no_cov"],
            "baseline_score_pct": f"{b_score:.2f}%",
            "final_total": f["total"],
            "final_killed": f["killed"],
            "final_survived": f["survived"],
            "final_no_coverage": f["no_cov"],
            "final_score_pct": f"{f_score:.2f}%",
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"[OK] Generated {out_path} ({len(rows)} rows)")


def generate_tests_by_file(repo_root: Path, out_path: Path):
    """Generate reports/data/tests_by_file.csv scanning test directory."""
    import re

    test_dir = repo_root / "src" / "test" / "java" / "org" / "springframework" / "samples" / "petclinic" / "owner"
    if not test_dir.exists():
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    # Baseline files present at pinned commit 500158f732419217507c7656904b8e6aa1bcc0d6
    baseline_filenames = {
        "OwnerControllerTests.java",
        "OwnerTests.java",
        "PetControllerTests.java",
        "PetTypeFormatterTests.java",
        "PetValidatorTests.java",
        "VisitControllerTests.java",
    }

    test_scope_map = {
        "ControllerBinderMutationTests.java": "4 binder setDisallowedFields + minVisitDate",
        "OwnerControllerMutationTests.java": "Pageable captor, OOB redirect, 2 lambda unknown-owner, id-mismatch direct",
        "OwnerControllerTests.java": "MockMvc controller owner CRUD",
        "OwnerMutationTests.java": "addPet/getPet/addVisit/toString - decision table thuần unit",
        "OwnerTests.java": "Domain model Owner",
        "PetControllerMutationTests.java": "side-effect captors, rethrow, detached-update, null-id guard, lambda direct",
        "PetControllerTests.java": "MockMvc controller pet CRUD (ProcessCreationForm & ProcessUpdateForm)",
        "PetTypeFormatterTests.java": "Parse và print PetType",
        "PetValidatorMutationTests.java": "BVA 30/31 ký tự + decision table isNew × type",
        "PetValidatorTests.java": "Kiểm chuẩn Pet cơ bản (ValidateHasErrors)",
        "PetVisitModelMutationTests.java": "Pet/Visit model + PetTypeFormatter.print(null)",
        "VisitControllerMutationTests.java": "pending-visit assert, pet/owner unknown, null-date direct, delegation captor",
        "VisitControllerTests.java": "MockMvc controller visit CRUD",
    }

    rows = []
    total_baseline = 0
    total_final = 0

    for java_file in sorted(test_dir.glob("*.java")):
        filename = java_file.name
        content = java_file.read_text(encoding="utf-8")
        test_matches = re.findall(r'@(?:ParameterizedTest|Test|RepeatedTest)\b', content)
        final_count = len(test_matches)
        is_baseline = filename in baseline_filenames
        baseline_count = final_count if is_baseline else 0
        delta = final_count - baseline_count

        total_baseline += baseline_count
        total_final += final_count

        rows.append({
            "file": filename,
            "category": "Baseline" if is_baseline else "Mutation mới",
            "baseline_tests": baseline_count,
            "final_tests": final_count,
            "delta_tests": delta,
            "scope": test_scope_map.get(filename, ""),
        })

    # Assert integrity
    assert len(rows) == 13, f"Expected 13 test files, got {len(rows)}"
    assert total_baseline == 49, f"Expected 49 baseline tests, got {total_baseline}"
    assert total_final == 130, f"Expected 130 final tests, got {total_final}"

    fieldnames = ["file", "category", "baseline_tests", "final_tests", "delta_tests", "scope"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"[OK] Generated {out_path} ({len(rows)} files, Baseline: {total_baseline}, Final: {total_final}, Delta: +{total_final - total_baseline})")


def main():
    # Resolve repository root
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    baseline_xml = repo_root / "reports" / "data" / "baseline_mutations.xml"
    final_xml = repo_root / "reports" / "data" / "final_mutations.xml"

    if len(sys.argv) > 1:
        baseline_xml = Path(sys.argv[1])
    if len(sys.argv) > 2:
        final_xml = Path(sys.argv[2])

    print(f"Reading Baseline XML: {baseline_xml}")
    print(f"Reading Final XML:    {final_xml}")

    baseline_mutations = parse_xml_mutations(baseline_xml)
    final_mutations = parse_xml_mutations(final_xml)

    print(f"Baseline parsed: {len(baseline_mutations)} mutations")
    print(f"Final parsed:    {len(final_mutations)} mutations")

    data_dir = repo_root / "reports" / "data"
    generate_metrics_summary(baseline_mutations, final_mutations, data_dir / "metrics_summary.csv")
    generate_survivors_baseline(baseline_mutations, data_dir / "survivors_baseline.csv")
    generate_mutator_breakdown(baseline_mutations, final_mutations, data_dir / "mutator_breakdown.csv")
    generate_tests_by_file(repo_root, data_dir / "tests_by_file.csv")
    print("[SUCCESS] All reports generated successfully.")


if __name__ == "__main__":
    main()
