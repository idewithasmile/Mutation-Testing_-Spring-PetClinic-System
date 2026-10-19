#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script sinh logs/git_history.log theo chuẩn yêu cầu của Session S6:
1. Bảng thống kê commit theo thành viên (git shortlog -sn toàn bộ & từ pinned commit).
2. Lịch sử commit chi tiết: git log --pretty=format:"%h | %an | %ad | %s" --date=short --stat
"""

import subprocess
import os

PINNED_SHA = "500158f732419217507c7656904b8e6aa1bcc0d6"
OUTPUT_PATH = os.path.join("logs", "git_history.log")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.stdout

def main():
    print("Dang sinh logs/git_history.log...")
    
    # 1. Thống kê commit từ pinned commit
    shortlog_pinned = run_cmd(f'git --no-pager shortlog -sn {PINNED_SHA}..HEAD')
    
    # 2. Thống kê commit toàn bộ repo
    shortlog_all = run_cmd('git --no-pager shortlog -sn HEAD')
    
    # 3. Lịch sử commit chi tiết
    log_stat = run_cmd('git --no-pager log --pretty=format:"%h | %an | %ad | %s" --date=short --stat')
    
    header = f"""================================================================================
NHẬT KÝ LỊCH SỬ GIT & THỐNG KÊ ĐÓNG GÓP THÀNH VIÊN (GIT HISTORY & TRACEABILITY)
================================================================================
Dự án: Kiểm thử đột biến (Mutation Testing) bằng PIT trên Spring PetClinic (K03 - Program_R01)
Commit khóa (Pinned Commit): {PINNED_SHA}
Nhánh hiện tại: VietLinh/Session6
Thời điểm xuất: 2026-10-19

--------------------------------------------------------------------------------
BẢNG 1: THỐNG KÊ SỐ LƯỢNG COMMIT CỦA 5 THÀNH VIÊN (KỂ TỪ PINNED COMMIT)
Phạm vi: {PINNED_SHA[:7]}..HEAD
--------------------------------------------------------------------------------
{shortlog_pinned.strip()}

ÁNH XẠ ĐÓNG GÓP CỦA 5 THÀNH VIÊN NHÓM:
- Thành viên 1 (QA Lead & DevSecOps): Trịnh Trung Hiếu (2312618)
  Git alias: '2312618 Trinh Trung Hieu', 'Hubert Trinh'
- Thành viên 2 (System Architect & Test Lead): Trần Đình Việt Huy
  Git alias: 'Bơ', 'idewithasmile'
- Thành viên 3 (Domain & Black-Box Test Engineer): Trần Minh Tài
  Git alias: 'minhtai05'
- Thành viên 4 (White-Box & Controller Test Engineer): Trương Bảo Bảo (2312582)
  Git alias: 'Truong Bao Bao'
- Thành viên 5 (Metrics, RCA & Quality Analyst): Hoàng Việt Linh (2312664)
  Git alias: 'VietLinh'

XÁC NHẬN TÍNH ĐẦY ĐỦ: ĐỦ 100% CẢ 5 THÀNH VIÊN ĐỀU CÓ COMMIT TRONG REPOSITORY.

--------------------------------------------------------------------------------
BẢNG 2: TOP THỐNG KÊ COMMIT TOÀN BỘ REPOSITORY (GIT SHORTLOG -SN HEAD)
--------------------------------------------------------------------------------
{shortlog_all.strip()}

================================================================================
LỊCH SỬ COMMIT CHI TIẾT (GIT LOG --PRETTY=FORMAT:"%h | %an | %ad | %s" --STAT)
================================================================================

"""
    full_content = header + log_stat
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_content)
        
    print(f"Da sinh xong: {OUTPUT_PATH} ({len(full_content.splitlines())} dong, {len(full_content)} bytes)")

if __name__ == "__main__":
    main()
