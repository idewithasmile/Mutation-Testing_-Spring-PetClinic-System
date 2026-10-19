#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script hợp nhất báo cáo toàn diện REPORT_R01_K03.md (Phần A -> H + Bìa + Mục lục + References).
- Đọc Phần A -> F từ REPORT_R01_K03.md gốc.
- Đọc Phần G chuyên sâu từ reports/PART_G.md (chuẩn hóa heading).
- Đọc Phần H từ REPORT_R01_K03.md gốc.
- Tạo Trang bìa, Bảng phân công 5 thành viên, Mục lục, Danh mục Bảng, Danh mục Hình, và Tài liệu tham khảo.
"""

import os
import shutil

REPORT_PATH = "REPORT_R01_K03.md"
REPORT_BAK_PATH = "REPORT_R01_K03.md.bak"
PART_G_PATH = os.path.join("reports", "PART_G.md")

def main():
    print("Sao luu REPORT_R01_K03.md sang .bak...")
    shutil.copyfile(REPORT_PATH, REPORT_BAK_PATH)
    
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report_content = f.read()
        
    with open(PART_G_PATH, "r", encoding="utf-8") as f:
        part_g_content = f.read()
        
    # Tìm các mốc phân chia trong REPORT_R01_K03.md
    part_a_idx = report_content.find("## PHẦN A:")
    part_g_idx = report_content.find("## PHẦN G:")
    part_h_idx = report_content.find("## PHẦN H:")
    
    if part_a_idx == -1 or part_g_idx == -1 or part_h_idx == -1:
        raise ValueError("Khong tim thay day du cac phan A, G, H trong REPORT_R01_K03.md")
        
    part_a_to_f = report_content[part_a_idx:part_g_idx].strip()
    part_h = report_content[part_h_idx:].strip()
    
    # Chuẩn hóa Phần G từ PART_G.md
    # Trong PART_G.md:
    # # PHẦN G: ... -> ## PHẦN G: BÁO CÁO PHÂN TÍCH CHẤT LƯỢNG, NGUYÊN NHÂN CỐT LÕI (RCA) & ĐỘT BIẾN TƯƠNG ĐƯƠNG
    # ## G.1. ... -> ### G.1. ...
    # ### G.1.1. ... -> #### G.1.1. ...
    # #### 1. ... -> ##### 1. ...
    
    # Bỏ phần header metadata đầu của PART_G.md (trước ## G.1.)
    g_1_idx = part_g_content.find("## G.1.")
    if g_1_idx == -1:
        raise ValueError("Khong tim thay ## G.1. trong PART_G.md")
        
    part_g_body = part_g_content[g_1_idx:]
    
    # Chuyển đổi các heading trong part_g_body
    lines = part_g_body.splitlines()
    new_g_lines = []
    for line in lines:
        if line.startswith("#### "):
            new_g_lines.append("##### " + line[5:])
        elif line.startswith("### "):
            new_g_lines.append("#### " + line[4:])
        elif line.startswith("## "):
            new_g_lines.append("### " + line[3:])
        else:
            new_g_lines.append(line)
            
    part_g_formatted_body = "\n".join(new_g_lines)
    
    part_g_full = """## PHẦN G: BÁO CÁO PHÂN TÍCH CHẤT LƯỢNG, NGUYÊN NHÂN CỐT LÕI (RCA) & ĐỘT BIẾN TƯƠNG ĐƯƠNG

> **Phạm vi phụ trách:** Thành viên 5 (TV5) – Metrics, RCA & Quality Analyst  
> **Dữ liệu kiểm chứng:** Trích xuất từ nhật ký thực thi `logs/` và 4 tệp dữ liệu chuẩn hóa trong `reports/data/`.  
> **Cam kết khoa học:** 100% số liệu có nguồn gốc thực nghiệm, không sửa đổi mã nguồn `src/main/java`.

---

""" + part_g_formatted_body

    front_matter = """# BÁO CÁO TỔNG KẾT HỌC PHẦN: ĐỀ TÀI R01 (SPRING PETCLINIC) + K03 (MUTATION TESTING)

**TRƯỜNG ĐẠI HỌC ĐÀ LẠT — KHOA CÔNG NGHỆ THÔNG TIN**  
**Học phần:** Kiểm thử phần mềm | **Mã lớp học phần:** 2411448  
**Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm  
**Nhóm thực hiện:** Nhóm 20 (Program_R01-K03)  
**Hệ thống kiểm thử (SUT):** Spring PetClinic (Pinned Commit SHA: `500158f732419217507c7656904b8e6aa1bcc0d6`)  
**Kỹ thuật kiểm thử:** Kiểm thử đột biến (Mutation Testing) bằng PIT (pitest-maven 1.30.0, pitest-junit5-plugin 1.2.3, Mutator Group STRONGER)  
**Phạm vi đột biến:** Gói nghiệp vụ cốt lõi `org.springframework.samples.petclinic.owner.*`  
**Kết quả tổng thể:** **Mutation Score 98.46% (192/195 killed)** — **Line Coverage 100.00% (250/250 lines)** — **153/153 Tests Passed** — **03 Equivalent Mutants (Adjusted Score 100.00%)**

---

### BẢNG THÔNG TIN VÀ PHÂN CÔNG NHIỆM VỤ THÀNH VIÊN NHÓM 20

| STT | Họ và tên | Mã số sinh viên | Vai trò dự án | Nhiệm vụ chính & Phạm vi báo cáo | Tỷ lệ đóng góp |
| :---: | :--- | :---: | :--- | :--- | :---: |
| 1 | **Trịnh Trung Hiếu** *(Nhóm trưởng)* | 2312618 | QA Lead & DevSecOps | Phụ trách Phần D (Nguyên lý K03, IEEE Error-Fault-Failure, RIP), Phần H (Commit pinning, CI/CD GitHub Actions, hướng dẫn 1-lệnh), cấu hình `pom.xml`, Quality Gate. | 100% |
| 2 | **Trần Đình Việt Huy** | 2312619 | System Architect & Test Lead | Phụ trách Phần A (Mục tiêu & Công nghệ), Phần B (Kiến trúc 3 luồng nghiệp vụ), Phần C (Dựng môi trường, Live HTTP validation), biên tập tài liệu tổng thể. | 100% |
| 3 | **Trần Minh Tài** | 2312794 | Domain & Black-Box Test Engineer | Phụ trách Phần E.1 (Thiết kế test hộp đen: BVA, Decision Table, Phân vùng tương đương), triển khai 45 unit tests cho `Owner`, `PetValidator`, `PetVisitModel`. | 100% |
| 4 | **Trương Bảo Bảo** | 2312582 | White-Box & Controller Test Engineer | Phụ trách Phần E.2 & Phần F (Thiết kế test hộp trắng: McCabe Basis Path, Mocking & ArgumentCaptor, Test Harness), triển khai 36 unit tests cho các Controller và Binder. | 100% |
| 5 | **Hoàng Việt Linh** | 2312664 | Metrics, RCA & Quality Analyst | Phụ trách Phần G (Hệ thống Metrics, phân tích Code Smell/Defect, RCA Error-Fault-Failure, chứng minh hình thức 3 Equivalent Mutants, điểm hiệu chỉnh, Peer Evaluation). | 100% |

---

## MỤC LỤC TỔNG THỂ (TABLE OF CONTENTS)

- [PHẦN A: MỤC TIÊU VÀ KIẾN TRÚC HỆ THỐNG](#phần-a-mục-tiêu-và-kiến-trúc-hệ-thống)
  - [A.1. Bài toán nghiệp vụ](#a1-bài-toán-nghiệp-vụ)
  - [A.2. Mục tiêu của đề tài kết hợp R01 + K03](#a2-mục-tiêu-của-đề-tài-kết-hợp-r01--k03)
  - [A.3. Technology Stack](#a3-technology-stack-thực-tế-đo-được-từ-pomxml-tại-commit-đã-khóa)
  - [A.4. Bốn module/actor cốt lõi](#a4-bốn-moduleactor-cốt-lõi)
  - [A.5. Ghi chú kỹ thuật quan trọng](#a5-ghi-chú-kỹ-thuật-quan-trọng-trung-thực)
- [PHẦN B: SƠ ĐỒ KIẾN TRÚC VÀ LUỒNG DỮ LIỆU CỦA 03 NGHIỆP VỤ TRỌNG TÂM](#phần-b-sơ-đồ-kiến-trúc-và-luồng-dữ-liệu-của-03-nghiệp-vụ-trọng-tâm)
  - [B.1. Kiến trúc phân tầng](#b1-kiến-trúc-phân-tầng-controller--repository--modeldatabase)
  - [B.2. Luồng 1 — Tìm kiếm & hiển thị danh sách chủ nuôi](#b2-luồng-1--tìm-kiếm--hiển-thị-danh-sách-chủ-nuôi-search--paginate-owners)
  - [B.3. Luồng 2 — Thêm mới thú cưng với trình xác thực](#b3-luồng-2--thêm-mới-thú-cưng-với-trình-xác-thực-create-pet-with-petvalidator)
  - [B.4. Luồng 3 — Đặt lịch khám & ghi bệnh án](#b4-luồng-3--đặt-lịch-khám--ghi-bệnh-án-book-visit-for-pet)
- [PHẦN C: THIẾT LẬP MÔI TRƯỜNG & CHỨNG MINH 03 LUỒNG CHẠY THÀNH CÔNG](#phần-c-thiết-lập-môi-trường--chứng-minh-03-luồng-chạy-thành-công)
  - [C.1. Yêu cầu runtime](#c1-yêu-cầu-runtime)
  - [C.2. Lệnh build & chạy](#c2-lệnh-build--chạy)
  - [C.3. Bằng chứng baseline test](#c3-bằng-chứng-baseline-test)
  - [C.4. Bằng chứng 03 luồng chạy thành công trên server thật](#c4-bằng-chứng-03-luồng-chạy-thành-công-trên-server-thật)
- [PHẦN D: NGUYÊN LÝ KỸ THUẬT KIỂM THỬ ĐỘT BIẾN (K03)](#phần-d-nguyên-lý-kỹ-thuật-kiểm-thử-đột-biến-k03)
  - [D.1. Mô hình chuẩn IEEE Error – Fault – Failure và Chuỗi điều kiện RIP trong Pitest](#d1-mô-hình-chuẩn-ieee-error--fault--failure-và-chuỗi-điều-kiện-rip-trong-pitest)
  - [D.2. Giới hạn của Độ bao phủ truyền thống và Minh chứng thực nghiệm](#d2-giới-hạn-của-độ-bao-phủ-truyền-thống-coverage-cấp-1--cấp-2-và-minh-chứng-thực-nghiệm)
  - [D.3. Phân biệt Weak Mutation vs Strong Mutation & Tập toán tử STRONGER](#d3-phân-biệt-weak-mutation-vs-strong-mutation--tập-toán-tử-stronger)
  - [D.4. Giới hạn phạm vi, Ràng buộc bất biến & Cổng chất lượng Quality Gate](#d4-giới-hạn-phạm-vi-scope-restriction-ràng-buộc-bất-biến-xử-lý-xung-đột-kỹ-thuật--cổng-chất-lượng)
  - [D.5. Khái niệm Đột biến tương đương & Đánh giá hiệu năng thực tế](#d5-khái-niệm-đột-biến-tương-đương-equivalent-mutants--đánh-giá-hiệu-năng-thực-tế)
- [PHẦN E: THIẾT KẾ KỊCH BẢN KIỂM THỬ](#phần-e-thiết-kế-kịch-bản-kiểm-thử)
  - [E.1. Chiến lược kỹ thuật kiểm thử hộp đen (BVA, Decision Table, Partitioning)](#e1-chiến-lược-kỹ-thuật)
  - [E.2. Bảng test case tiêu biểu và ánh xạ đường dẫn McCabe](#e2-bảng-test-case-tiêu-biểu-1081-test-mới-toàn-bộ-81-test-đều-deterministic-thuần-unit-hoặc-mockmvc-không-phụ-thuộc-mạngthời-gian-thực)
- [PHẦN F: MÃ NGUỒN HARNESS VÀ CẤU HÌNH TỰ ĐỘNG](#phần-f-mã-nguồn-harness-và-cấu-hình-tự-động)
  - [F.1. Cấu hình pitest-maven trong pom.xml](#f1-cấu-hình-pitest-maven-trong-pomxml-toàn-văn-khối-plugin)
  - [F.2. Các lớp test mới bổ sung](#f2-các-lớp-test-mới-7-files-81-test-methods-toàn-bộ-trong-srctestjavaowner)
  - [F.3. Trích dẫn mã nguồn test tiêu biểu](#f3-trích-dẫn-mã-tiêu-biểu)
- [PHẦN G: BÁO CÁO PHÂN TÍCH CHẤT LƯỢNG, NGUYÊN NHÂN CỐT LÕI (RCA) & ĐỘT BIẾN TƯƠNG ĐƯƠNG](#phần-g-báo-cáo-phân-tích-chất-lượng-nguyên-nhân-cốt-lõi-rca--đột-biến-tương-đương)
  - [G.1. Nhật ký thực thi (Logs) & Hệ thống chỉ số kiểm thử (Metrics)](#g1-nhật-ký-thực-thi-logs--hệ-thống-chỉ-số-kiểm-thử-metrics)
  - [G.2. Phân tích khiếm khuyết mã nguồn (Code Smell & Defect Analysis)](#g2-phân-tích-khiếm-khuyết-mã-nguồn-code-smell--defect-analysis)
  - [G.3. Phân tích nguyên nhân gốc rễ (RCA) theo chuẩn IEEE Error – Fault – Failure](#g3-phân-tích-nguyên-nhân-gốc-rễ-rca-theo-chuẩn-ieee-error--fault--failure)
  - [G.4. Chứng minh toán học hình thức 03 Đột biến tương đương (Equivalent Mutants)](#g4-chứng-minh-toán-học-hình-thức-03-đột-biến-tương-đương-equivalent-mutants)
  - [G.5. Kết luận & Bài học kinh nghiệm](#g5-kết-luận--bài-học-kinh-nghiệm)
- [PHẦN H: CỐ ĐỊNH PHIÊN BẢN (PIN COMMIT), ĐƯỜNG ỐNG CI/CD & HƯỚNG DẪN TÁI HIỆN](#phần-h-cố-định-phiên-bản-pin-commit-đường-ống-cicd--hướng-dẫn-tái-hiện)
  - [H.1. Khóa cứng Phiên bản (Commit Pinning) & Tính toàn vẹn mã nguồn](#h1-khóa-cứng-phiên-bản-commit-pinning--tính-toàn-vẹn-của-mã-nguồn)
  - [H.2. Đường ống Tích hợp liên tục CI/CD trên GitHub Actions](#h2-đường-ống-tích-hợp-liên-tục-cicd-trên-github-actions-githubworkflowsmutation-testyml)
  - [H.3. Hướng dẫn từng bước tái hiện 1-lệnh trên máy mới](#h3-hướng-dẫn-từng-bước-step-by-step-tái-hiện-1-lệnh-trên-máy-mới)
- [TÀI LIỆU THAM KHẢO (REFERENCES)](#tài-liệu-tham-khảo-references)

---

## DANH MỤC BẢNG BIỂU (LIST OF TABLES)
- **Bảng 1:** Bảng phân công nhiệm vụ và tỷ lệ đóng góp của 5 thành viên nhóm 20
- **Bảng A.1:** Công nghệ và phiên bản phần mềm cốt lõi (Technology Stack)
- **Bảng A.2:** Bốn module nghiệp vụ trung tâm của Spring PetClinic
- **Bảng C.1:** Kết quả kiểm chứng 03 luồng nghiệp vụ trên máy chủ HTTP thực tế
- **Bảng D.1:** Danh mục các toán tử đột biến trong nhóm `STRONGER` của PIT
- **Bảng E.1:** Danh mục 10 ca kiểm thử tiêu biểu cho các lớp đối tượng gói `owner`
- **Bảng F.1:** Bảng phân bổ 81 ca kiểm thử mới trên 7 lớp kiểm thử bổ sung
- **Bảng G.1:** Bảng đối sánh chỉ số kiểm thử đột biến tổng thể (Baseline vs Final)
- **Bảng G.2:** Phân rã hiệu suất tiêu diệt đột biến theo lớp đối tượng nghiệp vụ
- **Bảng G.3:** Phân rã hiệu suất kiểm thử theo toán tử đột biến (Mutator Group STRONGER)
- **Bảng G.4:** Bảng tổng hợp các Code Smell & Defect phát hiện trong gói `owner`
- **Bảng G.5:** Bảng phân loại nguyên nhân gốc rễ (RCA) của 64 mutants tồn dư ở Baseline
- **Bảng G.6:** Ma trận truy vết nguyên nhân gốc rễ và ca kiểm thử khắc phục
- **Bảng G.7:** Bảng đối chiếu chỉ số chất lượng chính thức vs hiệu chỉnh

---

## DANH MỤC HÌNH ẢNH & BIỂU ĐỒ (LIST OF FIGURES)
- **Sơ đồ B.1:** Sơ đồ kiến trúc phân tầng (Controller → Repository → Model/Database)
- **Sơ đồ D.1:** Chuỗi chuyển hóa IEEE Error – Fault – Failure và mô hình điều kiện RIP
- **Hình G.1:** Đối sánh Line Coverage vs Mutation Score và Khoảng trống kiểm thử (Test Gap)
- **Hình G.2:** Cơ cấu phân bổ trạng thái đột biến (Killed vs Survived vs No Coverage)
- **Hình G.3:** Phân bố 64 mutants chưa diệt tại Baseline theo nhóm toán tử
- **Hình G.4:** Biểu đồ tăng trưởng số lượng test case theo từng tệp kiểm thử
- **Sơ đồ H.1:** Lưu đồ kiến trúc đường ống CI/CD 6 bước Fail-Fast trên GitHub Actions

---

"""

    references = """

---

## TÀI LIỆU THAM KHẢO (REFERENCES)

1. **IEEE Computer Society**, *"IEEE Standard Glossary of Software Engineering Terminology"*, IEEE Std 610.12-1990, Dec. 1990.
2. **ISO/IEC/IEEE**, *"ISO/IEC/IEEE 29119-1:2022 Software and systems engineering — Software testing — Part 1: General concepts"*, 2022.
3. **A. J. Offutt and R. H. Untch**, *"Mutation 2000: Uniting the orthogonal"*, in Mutation 2000: Mutation Testing in the Twentieth and the Twenty-First Centuries, San Jose, CA, USA: Springer, 2001, pp. 34–44.
4. **H. Coles, T. Laurent, C. Henard, M. Papadakis, and A. Ventresque**, *"PIT: a practical mutation testing tool for Java"*, in Proceedings of the 25th International Symposium on Software Testing and Analysis (ISSTA 2016), Saarbrücken, Germany: ACM, 2016, pp. 449–452.
5. **M. Papadakis, M. Kintis, J. Zhang, Y. Jia, M. Le Traon, and M. Harman**, *"Mutation Testing Advances: An Analysis and Survey"*, Advances in Computers, vol. 112, pp. 275–378, 2019.
6. **Paul Ammann and Jeff Offutt**, *"Introduction to Software Testing"*, 2nd ed., Cambridge University Press, 2016.
7. **Spring Projects**, *"Spring PetClinic Sample Application"*, GitHub repository: `https://github.com/spring-projects/spring-petclinic`, commit SHA `500158f732419217507c7656904b8e6aa1bcc0d6`, 2026.
8. **JUnit Team**, *"JUnit 5 / JUnit Platform User Guide (v6.0)"*, `https://junit.org/junit5/docs/current/user-guide/`, 2026.
9. **Martin Fowler**, *"Refactoring: Improving the Design of Existing Code"*, 2nd ed., Addison-Wesley Professional, 2018.
10. **Khoa Công nghệ Thông tin – Trường Đại học Đà Lạt**, *"Đề cương chi tiết học phần Kiểm thử phần mềm (Software Testing)"*, GVHD: ThS. Nguyễn Thế Lâm, 2026.

================================================================================
"""

    merged_content = front_matter + "\n\n" + part_a_to_f + "\n\n---\n\n" + part_g_full + "\n\n---\n\n" + part_h + references

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(merged_content)
        
    print(f"Da hop nhat thanh cong vao {REPORT_PATH}!")
    print(f"Kich thuoc moi: {len(merged_content.splitlines())} dong, {len(merged_content)} bytes")

if __name__ == "__main__":
    main()
