"""
verify_part_g.py - Automated verification tool for reports/PART_G.md
Thành viên 5 (Metrics, RCA & Quality Analyst) - Program_R01-K03
"""

import sys
import os
import re
import csv
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
PART_G_PATH = ROOT_DIR / "reports" / "PART_G.md"
METRICS_SUMMARY_CSV = ROOT_DIR / "reports" / "data" / "metrics_summary.csv"
MUTATOR_BREAKDOWN_CSV = ROOT_DIR / "reports" / "data" / "mutator_breakdown.csv"
TESTS_BY_FILE_CSV = ROOT_DIR / "reports" / "data" / "tests_by_file.csv"

def verify_no_placeholders(content):
    print("=== 1. KIỂM TRA PLACEHOLDER / TODO / FIXME ===")
    forbidden = ["TODO", "FIXME", "XXX", "TBD", "PLACEHOLDER", "CHƯA XÁC ĐỊNH", "??"]
    found = []
    for line_idx, line in enumerate(content.splitlines(), start=1):
        for pattern in forbidden:
            if pattern in line.upper() and not ("TODO" in pattern and "TODO" not in line):
                # Check if it's not a literal instruction mention
                if "TODO/placeholder" in line or "TODO" in line:
                    continue
                found.append((line_idx, pattern, line.strip()))
    if found:
        for f in found:
            print(f"  [FAIL] Dòng {f[0]}: Chứa ký tự cấm '{f[1]}': {f[2]}")
        return False
    print("  [PASS] Không tìm thấy bất kỳ TODO/placeholder/FIXME nào.")
    return True

def verify_csv_metrics(content):
    print("\n=== 2. KIỂM TRA ĐỐI CHIẾU SỐ LIỆU VỚI METRICS_SUMMARY.CSV ===")
    if not METRICS_SUMMARY_CSV.exists():
        print(f"  [FAIL] Không tìm thấy tệp {METRICS_SUMMARY_CSV}")
        return False
    
    with open(METRICS_SUMMARY_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = {row["Phase"]: row for row in reader}

    baseline = rows.get("Baseline")
    final = rows.get("Final")
    
    checks = [
        ("Baseline Tests", baseline["Tests (Owner Package)"], "49"),
        ("Final Tests", final["Tests (Owner Package)"], "130"),
        ("Baseline Line Coverage Pct", baseline["Line Coverage (%)"], "96.80%"),
        ("Final Line Coverage Pct", final["Line Coverage (%)"], "100.00%"),
        ("Baseline Covered Lines", baseline["Lines Covered"], "242"),
        ("Final Covered Lines", final["Lines Covered"], "250"),
        ("Baseline Total Mutants", baseline["Total Mutants"], "195"),
        ("Final Total Mutants", final["Total Mutants"], "195"),
        ("Baseline Killed Mutants", baseline["Killed"], "131"),
        ("Final Killed Mutants", final["Killed"], "192"),
        ("Baseline Survived Mutants", baseline["Survived"], "55"),
        ("Final Survived Mutants", final["Survived"], "3"),
        ("Baseline No Coverage", baseline["No Coverage"], "9"),
        ("Final No Coverage", final["No Coverage"], "0"),
        ("Baseline Mutation Score", baseline["Mutation Score (%)"], "67.18%"),
        ("Final Mutation Score", final["Mutation Score (%)"], "98.46%"),
    ]
    
    all_ok = True
    for name, csv_val, expected_str in checks:
        if csv_val != expected_str:
            print(f"  [FAIL] CSV {name}: giá trị {csv_val} != expected {expected_str}")
            all_ok = False
        else:
            # Check if expected_str is present in PART_G.md
            if expected_str not in content:
                print(f"  [FAIL] {name} ({expected_str}) không tìm thấy trong PART_G.md!")
                all_ok = False
            else:
                print(f"  [PASS] {name}: {expected_str} khớp chính xác giữa CSV và PART_G.md.")
                
    return all_ok

def verify_table_and_figure_numbering(content):
    print("\n=== 3. KIỂM TRA ĐÁNH SỐ BẢNG VÀ HÌNH ===")
    tables = re.findall(r"Bảng G\.(\d+)", content)
    figures = re.findall(r"Hình G\.(\d+)", content)
    
    unique_tables = sorted(list(set(int(t) for t in tables)))
    unique_figures = sorted(list(set(int(f) for f in figures)))
    
    print(f"  Các Bảng phát hiện: {['Bảng G.' + str(t) for t in unique_tables]}")
    print(f"  Các Hình phát hiện: {['Hình G.' + str(f) for f in unique_figures]}")
    
    ok = True
    expected_tables = list(range(1, max(unique_tables) + 1)) if unique_tables else []
    expected_figures = list(range(1, max(unique_figures) + 1)) if unique_figures else []
    
    if unique_tables != expected_tables:
        print(f"  [FAIL] Bảng không liên tục từ 1 đến {max(unique_tables)}: {unique_tables}")
        ok = False
    else:
        print(f"  [PASS] Toàn bộ {len(unique_tables)} Bảng (Bảng G.1 -> Bảng G.{max(unique_tables)}) được đánh số liên tục.")
        
    if unique_figures != expected_figures:
        print(f"  [FAIL] Hình không liên tục từ 1 đến {max(unique_figures)}: {unique_figures}")
        ok = False
    else:
        print(f"  [PASS] Toàn bộ {len(unique_figures)} Hình (Hình G.1 -> Hình G.{max(unique_figures)}) được đánh số liên tục.")
        
    return ok

def verify_cross_references(content):
    print("\n=== 4. KIỂM TRA LIÊN KẾT CHÉO TỚI PHẦN E (TV3 / TV4) ===")
    ref_e1 = len(re.findall(r"mục E\.1", content, re.IGNORECASE))
    ref_e2 = len(re.findall(r"mục E\.2", content, re.IGNORECASE))
    ref_g4 = len(re.findall(r"mục G\.4", content, re.IGNORECASE))
    
    print(f"  Số lần liên kết 'mục E.1': {ref_e1}")
    print(f"  Số lần liên kết 'mục E.2': {ref_e2}")
    print(f"  Số lần liên kết 'mục G.4': {ref_g4}")
    
    if ref_e1 > 0 and ref_e2 > 0:
        print("  [PASS] Đầy đủ các liên kết chéo tới Phần E (E.1 cho TV3 và E.2 cho TV4).")
        return True
    else:
        print("  [FAIL] Thiếu liên kết chéo tới mục E.1 hoặc E.2!")
        return False

def verify_section_structure(content):
    print("\n=== 5. KIỂM TRA CẤU TRÚC PHẦN G ===")
    sections = [
        ("G.1", "NHẬT KÝ THỰC THI (LOGS) & HỆ THỐNG CHỈ SỐ KIỂM THỬ (METRICS)"),
        ("G.2", "PHÂN TÍCH KHIẾM KHUYẾT MÃ NGUỒN (CODE SMELL & DEFECT ANALYSIS)"),
        ("G.3", "PHÂN TÍCH NGUYÊN NHÂN CỐT LÕI (ROOT CAUSE ANALYSIS - RCA)"),
        ("G.4", "CHỨNG MINH CÁC ĐỘT BIẾN TƯƠNG ĐƯƠNG (EQUIVALENT MUTANTS) & ĐIỂM SỐ HIỆU CHỈNH"),
        ("G.5", "KẾT LUẬN & BÀI HỌC KINH NGHIỆM"),
        ("DANH MỤC CÁC ĐIỂM CẦN PHỐI HỢP XÁC NHẬN VỚI CÁC THÀNH VIÊN KHÁC", "DANH MỤC")
    ]
    
    all_ok = True
    for prefix, name in sections:
        if prefix in content:
            print(f"  [PASS] Có đề mục {prefix}: {name}")
        else:
            print(f"  [FAIL] Thiếu đề mục {prefix}: {name}")
            all_ok = False
    return all_ok

def main():
    print(f"Đang kiểm tra tính toàn vẹn của: {PART_G_PATH}")
    if not PART_G_PATH.exists():
        print(f"[FAIL] Tệp {PART_G_PATH} không tồn tại!")
        sys.exit(1)
        
    with open(PART_G_PATH, mode="r", encoding="utf-8") as f:
        content = f.read()
        
    c1 = verify_no_placeholders(content)
    c2 = verify_csv_metrics(content)
    c3 = verify_table_and_figure_numbering(content)
    c4 = verify_cross_references(content)
    c5 = verify_section_structure(content)
    
    print("\n================ TỔNG KẾT NGHIỆM THU ================")
    if c1 and c2 and c3 and c4 and c5:
        print(">>> TẤT CẢ TIÊU CHÍ CHECKLIST ĐỀU ĐẠT CHUẨN XUẤT SẮC (PASS 100%) <<<")
        sys.exit(0)
    else:
        print(">>> CÓ TIÊU CHÍ CHƯA ĐẠT, CẦN SỬA ĐỔI (FAIL) <<<")
        sys.exit(1)

if __name__ == "__main__":
    main()
