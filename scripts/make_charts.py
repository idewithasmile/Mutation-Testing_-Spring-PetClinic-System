#!/usr/bin/env python3
"""
make_charts.py - Generate publication-ready 200 DPI figures for Session S2.

Input: reports/data/*.csv (NO hardcoded data, strict assert on CSV values)
Output: reports/figures/
 1. fig1_coverage_vs_mutation.png: Line Coverage vs Mutation Score (Baseline vs Final)
 2. fig2_mutant_status.png: Stacked bar chart (Killed / Survived / No Coverage)
 3. fig3_survivors_by_mutator.png: Baseline survivors by mutator
 4. fig4_tests_growth.png: Test cases growth by file (Baseline vs Final)

Requirements:
- Vietnamese Unicode font without clipping/tofu (Segoe UI / Arial)
- Numbers labeled on bars
- Distinct hatch patterns and contrasting luminance for grayscale / B&W printing
- Academic title + subtitle + data source footnote
- 200 DPI resolution
"""

import csv
import os
import sys
from pathlib import Path

# Force UTF-8 for console output
if sys.platform.startswith("win"):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Global styling configuration
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "Tahoma", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False


def load_csv(path: Path):
    """Load CSV into list of dicts."""
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def plot_fig1_coverage_vs_mutation(metrics, out_path: Path):
    """
    Figure 1: Grouped bar chart Line Coverage vs Mutation Score (Baseline vs Final).
    Key message: 97% line coverage but only 67% mutation score (false sense of security).
    """
    baseline = next(m for m in metrics if m["Phase"] == "Baseline")
    final = next(m for m in metrics if m["Phase"] == "Final")

    # Parse and assert values
    base_cov = float(baseline["Line Coverage (%)"].rstrip("%"))
    base_mut = float(baseline["Mutation Score (%)"].rstrip("%"))
    fin_cov = float(final["Line Coverage (%)"].rstrip("%"))
    fin_mut = float(final["Mutation Score (%)"].rstrip("%"))

    assert abs(base_cov - 96.80) < 1e-2, f"Expected 96.80%, got {base_cov}%"
    assert abs(base_mut - 67.18) < 1e-2, f"Expected 67.18%, got {base_mut}%"
    assert abs(fin_cov - 100.00) < 1e-2, f"Expected 100.00%, got {fin_cov}%"
    assert abs(fin_mut - 98.46) < 1e-2, f"Expected 98.46%, got {fin_mut}%"

    phases = ["Baseline (Gốc)", "Final (Sau cải tiến)"]
    line_covs = [base_cov, fin_cov]
    mut_scores = [base_mut, fin_mut]

    x = np.arange(len(phases))
    width = 0.30

    fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=200)

    # Grayscale-friendly styling: contrasting colors + distinct hatch patterns
    color_cov = "#1f4e79"   # Deep Navy
    color_mut = "#c55a11"   # Warm Terracotta Amber
    hatch_cov = "//"        # Diagonal stripes
    hatch_mut = ".."        # Dot matrix

    rects1 = ax.bar(x - width/2, line_covs, width, label="Line Coverage (%)",
                    color=color_cov, hatch=hatch_cov, edgecolor="#0d233a", linewidth=1.2)
    rects2 = ax.bar(x + width/2, mut_scores, width, label="Mutation Score (%)",
                    color=color_mut, hatch=hatch_mut, edgecolor="#612800", linewidth=1.2)

    # Add numeric labels on top of bars
    for rect, val in zip(rects1, line_covs):
        height = rect.get_height()
        ax.annotate(f"{val:.2f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontsize=11, fontweight="bold", color="#0d233a")

    for rect, val in zip(rects2, mut_scores):
        height = rect.get_height()
        ax.annotate(f"{val:.2f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontsize=11, fontweight="bold", color="#612800")

    # Clean annotation for Baseline Test Gap - placed cleanly in the middle void (x=0.5)
    gap = base_cov - base_mut
    ax.annotate(
        f"KHOẢNG TRỐNG KIỂM THỬ: {gap:.2f}%\n• Line Coverage 96.80% (~97%) tạo ảo giác an toàn\n• Mutation Score chỉ 67.18% (~67%)\n• Bỏ sót 64 mutants chưa được phát hiện",
        xy=(x[0] + width/2, base_mut),
        xytext=(0.50, 48),
        arrowprops=dict(facecolor="#7f6000", edgecolor="#7f6000", arrowstyle="->", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff2cc", edgecolor="#d6b656", lw=1.2),
        ha="center", va="center", fontsize=9.5, fontweight="bold", color="#7f6000"
    )

    # Clean badge for Final: placed neatly above the Final bars
    ax.text(x[1], 108,
            "Tiêu diệt 192/195 mutants (98.46% ~ 98%)\n3 survivors còn lại là Equivalent Mutants (100% hiệu dụng)",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color="#274e13",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#d9ead3", edgecolor="#6aa84f", lw=1.1))

    ax.set_ylabel("Tỷ lệ phần trăm (%)", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title("SO SÁNH ĐỘ BAO PHỦ DÒNG (LINE COVERAGE) VÀ ĐIỂM ĐỘT BIẾN (MUTATION SCORE)",
                 fontsize=12.5, fontweight="bold", pad=16, color="#1a1a1a")
    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=11.5, fontweight="bold")
    ax.set_ylim(0, 126)
    ax.set_xlim(-0.55, 1.55)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    ax.legend(loc="upper left", framealpha=0.95, facecolor="#ffffff", edgecolor="#cccccc", fontsize=10.5)

    # Source footnote
    fig.text(0.5, 0.015,
             "Nguồn dữ liệu: reports/data/metrics_summary.csv | Công cụ: PIT 1.30.0 (STRONGER) | Gói kiểm thử: owner",
             ha="center", fontsize=8.5, style="italic", color="#555555")

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] Generated {out_path}")


def plot_fig2_mutant_status(metrics, out_path: Path):
    """
    Figure 2: Stacked bar chart of mutant statuses: Killed / Survived / No Coverage.
    Baseline vs Final.
    """
    baseline = next(m for m in metrics if m["Phase"] == "Baseline")
    final = next(m for m in metrics if m["Phase"] == "Final")

    # Assert values
    b_total = int(baseline["Total Mutants"])
    b_killed = int(baseline["Killed"])
    b_surv = int(baseline["Survived"])
    b_nocov = int(baseline["No Coverage"])

    f_total = int(final["Total Mutants"])
    f_killed = int(final["Killed"])
    f_surv = int(final["Survived"])
    f_nocov = int(final["No Coverage"])

    assert b_total == 195 and b_killed == 131 and b_surv == 55 and b_nocov == 9
    assert f_total == 195 and f_killed == 192 and f_surv == 3 and f_nocov == 0
    assert (b_killed + b_surv + b_nocov) == 195
    assert (f_killed + f_surv + f_nocov) == 195

    phases = ["Baseline (Gốc)", "Final (Sau cải tiến)"]
    killed_vals = np.array([b_killed, f_killed])
    surv_vals = np.array([b_surv, f_surv])
    nocov_vals = np.array([b_nocov, f_nocov])

    x = np.arange(len(phases))
    width = 0.38

    fig, ax = plt.subplots(figsize=(9.6, 6.6), dpi=200)

    # Grayscale-friendly color palette with distinct textures
    c_killed = "#2e5b88"   # Slate Blue
    c_surv = "#d9822b"     # Amber Orange
    c_nocov = "#b83b3b"    # Brick Red

    h_killed = ""          # Solid
    h_surv = "xx"          # Cross-hatch
    h_nocov = "//"         # Diagonal stripes

    ax.bar(x, killed_vals, width, label="Killed (Đã diệt)",
           color=c_killed, hatch=h_killed, edgecolor="#1a1a1a", linewidth=1.2)
    ax.bar(x, surv_vals, width, bottom=killed_vals, label="Survived (Sống sót)",
           color=c_surv, hatch=h_surv, edgecolor="#1a1a1a", linewidth=1.2)
    ax.bar(x, nocov_vals, width, bottom=killed_vals + surv_vals, label="No Coverage (Không có test chạm tới)",
           color=c_nocov, hatch=h_nocov, edgecolor="#1a1a1a", linewidth=1.2)

    # 1. Baseline segment labels
    # Killed (131)
    ax.text(x[0], b_killed / 2, f"131\n({b_killed/195*100:.1f}%)",
            ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=11)
    # Survived (55)
    ax.text(x[0], b_killed + b_surv / 2, f"55\n({b_surv/195*100:.1f}%)",
            ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=10.5)
    # No Coverage (9) - Leader line pointing from outer left
    ax.annotate(f"9 No Coverage\n({b_nocov/195*100:.1f}%)",
                xy=(x[0] - width/2, b_killed + b_surv + b_nocov / 2),
                xytext=(x[0] - 0.28, b_killed + b_surv + b_nocov / 2),
                arrowprops=dict(facecolor="#b83b3b", edgecolor="#b83b3b", arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#fce5cd", edgecolor="#e69138", lw=1),
                va="center", ha="right", fontsize=9, fontweight="bold", color="#8c2323")

    # 2. Final segment labels
    # Killed (192)
    ax.text(x[1], f_killed / 2, f"192\n({f_killed/195*100:.1f}%)",
            ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=11)
    # Survived (3) - Leader line pointing from outer right
    ax.annotate("3 Survived (1.5%)\n[100% Equivalent Mutants:\n Owner:108 (x2)\n OwnerController:167]",
                xy=(x[1] + width/2, 193.5),
                xytext=(x[1] + 0.28, 175),
                arrowprops=dict(facecolor="#7f6000", edgecolor="#7f6000", arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff2cc", edgecolor="#d6b656", lw=1),
                va="center", ha="left", fontsize=9, fontweight="bold", color="#7f6000")

    # Annotate total on top of bars
    for i in range(len(phases)):
        ax.text(x[i], 200, "Tổng: 195 mutants", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color="#1a1a1a")

    ax.set_ylabel("Số lượng Mutants", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title("CƠ CẤU TRẠNG THÁI MUTANT: BASELINE VS FINAL",
                 fontsize=13, fontweight="bold", pad=28, color="#1a1a1a")
    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=11.5, fontweight="bold")
    ax.set_ylim(0, 235)
    ax.set_xlim(-0.65, 1.65)  # Ample room on left and right for outer callouts
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    # Place legend cleanly at the top center to prevent any overlap
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.08), ncol=3,
              framealpha=0.95, facecolor="#ffffff", edgecolor="#cccccc", fontsize=9.5)

    fig.text(0.5, 0.015,
             "Nguồn dữ liệu: reports/data/metrics_summary.csv | Gói: org.springframework.samples.petclinic.owner",
             ha="center", fontsize=8.5, style="italic", color="#555555")

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] Generated {out_path}")


def plot_fig3_survivors_by_mutator(mutator_data, out_path: Path):
    """
    Figure 3: Horizontal stacked bar chart of Baseline survivors (Survived + No Coverage) by Mutator.
    """
    mut_rows = [r for r in mutator_data if r["dimension"] == "BY_MUTATOR"]
    
    items = []
    total_surv = 0
    total_nocov = 0

    for r in mut_rows:
        surv = int(r["baseline_survived"])
        nocov = int(r["baseline_no_coverage"])
        tot_non_killed = surv + nocov
        if tot_non_killed > 0:
            items.append({
                "mutator": r["category"],
                "survived": surv,
                "no_coverage": nocov,
                "total": tot_non_killed,
            })
            total_surv += surv
            total_nocov += nocov

    assert total_surv == 55, f"Expected 55 baseline survived, got {total_surv}"
    assert total_nocov == 9, f"Expected 9 baseline no_coverage, got {total_nocov}"
    assert (total_surv + total_nocov) == 64, f"Expected 64 non-killed, got {total_surv + total_nocov}"

    # Sort ascending so the largest mutators appear at the top of the horizontal bar chart
    items.sort(key=lambda x: (x["total"], x["survived"]), reverse=False)

    mutator_names = [it["mutator"] for it in items]
    surv_counts = [it["survived"] for it in items]
    nocov_counts = [it["no_coverage"] for it in items]

    y = np.arange(len(items))
    height = 0.58

    fig, ax = plt.subplots(figsize=(11, 6.6), dpi=200)

    c_surv = "#d9822b"   # Amber Orange
    c_nocov = "#b83b3b"  # Brick Red
    h_surv = ".."        # Dots
    h_nocov = "//"       # Diagonal stripes

    ax.barh(y, surv_counts, height, label="Survived (Có test chạm tới nhưng không bắt được lỗi)",
            color=c_surv, hatch=h_surv, edgecolor="#1a1a1a", linewidth=1.1)
    ax.barh(y, nocov_counts, height, left=surv_counts, label="No Coverage (Hoàn toàn chưa có test bao phủ)",
            color=c_nocov, hatch=h_nocov, edgecolor="#1a1a1a", linewidth=1.1)

    # Add numeric labels at end of each bar with sufficient margin
    for idx, it in enumerate(items):
        tot = it["total"]
        s = it["survived"]
        nc = it["no_coverage"]
        if nc > 0:
            label_text = f"{tot} (S: {s}, NC: {nc})"
        else:
            label_text = f"{tot}"

        ax.text(tot + 0.45, y[idx], label_text, va="center", ha="left",
                fontsize=9.5, fontweight="bold", color="#1a1a1a")

    ax.set_xlabel("Số lượng Mutants chưa bị tiêu diệt ở Baseline", fontsize=11.5, fontweight="bold", labelpad=8)
    ax.set_title("PHÂN BỐ 64 MUTANT SỐNG SÓT Ở BASELINE THEO TOÁN TỬ ĐỘT BIẾN (MUTATOR)",
                 fontsize=12.5, fontweight="bold", pad=16, color="#1a1a1a")
    ax.set_yticks(y)
    ax.set_yticklabels(mutator_names, fontsize=10, fontweight="bold")
    ax.set_xlim(0, 26.5)  # Extended to fit labels comfortably
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    ax.legend(loc="lower right", framealpha=0.95, facecolor="#ffffff", edgecolor="#cccccc", fontsize=9.5)

    # Summary footnote
    fig.text(0.5, 0.015,
             "Nguồn dữ liệu: reports/data/mutator_breakdown.csv | Tổng cộng: 55 Survived + 9 No Coverage = 64 Mutants",
             ha="center", fontsize=8.5, style="italic", color="#555555")

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] Generated {out_path}")


def plot_fig4_tests_growth(tests_data, out_path: Path):
    """
    Figure 4: Test cases growth by file (Baseline vs Final).
    13 files in org.springframework.samples.petclinic.owner.*
    """
    total_base = sum(int(r["baseline_tests"]) for r in tests_data)
    total_fin = sum(int(r["final_tests"]) for r in tests_data)
    total_delta = sum(int(r["delta_tests"]) for r in tests_data)

    assert len(tests_data) == 13, f"Expected 13 test files, got {len(tests_data)}"
    assert total_base == 49, f"Expected 49 baseline tests, got {total_base}"
    assert total_fin == 130, f"Expected 130 final tests, got {total_fin}"
    assert total_delta == 81, f"Expected +81 delta tests, got {total_delta}"

    # Sort: Baseline files first (by final_tests), then Mutation files (by final_tests)
    sorted_data = sorted(tests_data, key=lambda r: (r["category"] == "Mutation mới", int(r["final_tests"])))

    filenames = [r["file"].replace(".java", "") for r in sorted_data]
    base_counts = [int(r["baseline_tests"]) for r in sorted_data]
    fin_counts = [int(r["final_tests"]) for r in sorted_data]
    categories = [r["category"] for r in sorted_data]

    y = np.arange(len(filenames))
    height = 0.38

    fig, ax = plt.subplots(figsize=(11.5, 8.0), dpi=200)

    c_base = "#708090"   # Slate Gray
    c_fin = "#1f4e79"    # Deep Navy
    h_base = "//"        # Stripes
    h_fin = ".."         # Dots

    ax.barh(y - height/2, base_counts, height, label="Baseline Tests (Gốc: 6 files, 49 tests)",
            color=c_base, hatch=h_base, edgecolor="#1a1a1a", linewidth=1.1)
    ax.barh(y + height/2, fin_counts, height, label="Final Tests (Sau cải tiến: 13 files, 130 tests)",
            color=c_fin, hatch=h_fin, edgecolor="#1a1a1a", linewidth=1.1)

    # Label values on bars
    for idx, (b, f, cat) in enumerate(zip(base_counts, fin_counts, categories)):
        # Baseline bar label
        if b > 0:
            ax.text(b + 0.4, y[idx] - height/2, f"{b}", va="center", ha="left",
                    fontsize=9, color="#404040", fontweight="bold")

        # Final bar label with delta
        delta_str = f"+{f-b}" if (f-b) > 0 else "0"
        tag = f" ({delta_str})" if (f-b) > 0 else ""
        ax.text(f + 0.4, y[idx] + height/2, f"{f}{tag}", va="center", ha="left",
                fontsize=9.5, color="#0d233a", fontweight="bold")

    # Dividing line between Baseline original files and New Mutation files
    split_idx = next(i for i, c in enumerate(categories) if c == "Mutation mới")
    ax.axhline(split_idx - 0.5, color="#b83b3b", linestyle=":", linewidth=1.4, alpha=0.8)
    ax.text(22, split_idx - 0.8, "▲ 6 File Test Gốc (Baseline: 49 tests)",
            color="#555555", fontsize=9.5, fontweight="bold")
    ax.text(22, split_idx - 0.2, "▼ 7 File Test Đột Biến Bổ Sung (+81 tests)",
            color="#1f4e79", fontsize=9.5, fontweight="bold")

    ax.set_xlabel("Số lượng Test Methods (@Test, @ParameterizedTest)", fontsize=11.5, fontweight="bold", labelpad=8)
    ax.set_title("TĂNG TRƯỞNG SỐ LƯỢNG TEST CASE THEO FILE (BASELINE VS FINAL)",
                 fontsize=13, fontweight="bold", pad=16, color="#1a1a1a")
    ax.set_yticks(y)
    ax.set_yticklabels(filenames, fontsize=9.5, fontweight="bold")
    ax.set_xlim(0, 32.5)  # Extended to fit labels comfortably
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    # Summary box
    summary_text = (
        "Tổng kết quy mô kiểm thử:\n"
        "• Baseline:  49 tests / 6 files\n"
        "• Final:    130 tests / 13 files\n"
        "• Tăng trưởng: +81 tests (+165.3%)"
    )
    ax.text(0.97, 0.16, summary_text, transform=ax.transAxes,
            va="bottom", ha="right",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#f2f2f2", edgecolor="#999999", lw=1.2),
            fontsize=9.5, fontweight="bold", color="#1a1a1a")

    ax.legend(loc="lower right", framealpha=0.95, facecolor="#ffffff", edgecolor="#cccccc", fontsize=9.5)

    fig.text(0.5, 0.015,
             "Nguồn dữ liệu: reports/data/tests_by_file.csv | Gói kiểm thử: org.springframework.samples.petclinic.owner",
             ha="center", fontsize=8.5, style="italic", color="#555555")

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] Generated {out_path}")


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    data_dir = repo_root / "reports" / "data"
    fig_dir = repo_root / "reports" / "figures"

    print("=" * 60)
    print("SESSION S2: GENERATING PUBLICATION CHARTS (MATPLOTLIB 200 DPI)")
    print("=" * 60)

    metrics_path = data_dir / "metrics_summary.csv"
    mutator_path = data_dir / "mutator_breakdown.csv"
    tests_path = data_dir / "tests_by_file.csv"

    metrics = load_csv(metrics_path)
    mutator_data = load_csv(mutator_path)
    tests_data = load_csv(tests_path)

    print(f"[LOAD] metrics_summary.csv:   {len(metrics)} rows")
    print(f"[LOAD] mutator_breakdown.csv: {len(mutator_data)} rows")
    print(f"[LOAD] tests_by_file.csv:     {len(tests_data)} rows")

    plot_fig1_coverage_vs_mutation(metrics, fig_dir / "fig1_coverage_vs_mutation.png")
    plot_fig2_mutant_status(metrics, fig_dir / "fig2_mutant_status.png")
    plot_fig3_survivors_by_mutator(mutator_data, fig_dir / "fig3_survivors_by_mutator.png")
    plot_fig4_tests_growth(tests_data, fig_dir / "fig4_tests_growth.png")

    print("=" * 60)
    print("[SUCCESS] All 4 publication charts generated at 200 DPI successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
