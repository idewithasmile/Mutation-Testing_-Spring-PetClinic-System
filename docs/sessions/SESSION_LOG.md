# NHẬT KÝ PHIÊN LÀM VIỆC (SESSION LOG) — TV5: METRICS, RCA & QUALITY ANALYST

## SESSION S0: Recon & Reproduce (READ-ONLY)
- **Ngày thực hiện:** 2026-10-19
- **Nhánh làm việc:** `docs/metrics-rca-final-report`
- **Mục tiêu:**
  - Kiểm tra môi trường hệ thống: phiên bản Java, git branch, git status, kiểm tra HEAD so với pinned SHA (`500158f732419217507c7656904b8e6aa1bcc0d6`).
  - Tạo nhánh làm việc `docs/metrics-rca-final-report`.
  - Rà soát tài liệu bàn giao và cấu trúc các lớp kiểm thử tại `src/test/java/org/springframework/samples/petclinic/owner/` (đếm file, đếm test method).
  - Tái hiện thực thi kiểm thử và Mutation Testing bằng `./mvnw.cmd`.
  - Thu thập logs và lập bảng đối chiếu số liệu bàn giao với số liệu đo thực tế.

---

### 1. KẾT QUẢ RECON (MÔI TRƯỜNG & GIT)

| Thành phần | Yêu cầu / Bàn giao | Thực tế kiểm tra | Đánh giá / Nguồn |
|---|---|---|---|
| **Git Branch** | `docs/metrics-rca-final-report` | Đã tạo và chuyển từ `personal` sang `docs/metrics-rca-final-report` | `git checkout -b docs/metrics-rca-final-report` |
| **Git Status** | Sạch (clean) | `nothing to commit, working tree clean` | `git status` |
| **HEAD Commit** | Hậu duệ của `500158f7...` | `33c801b1189c7bff4d9d1c785c10df0f3d069494` | `git rev-parse HEAD` |
| **Kiểm tra Pinned SHA** | Là con/cháu của `500158f7...` | Exit code `0` (Hợp lệ, là hậu duệ trực tiếp) | `git merge-base --is-ancestor 500158f732419217507c7656904b8e6aa1bcc0d6 HEAD` |
| **JDK / Java Version** | Java 17 trở lên | **CHƯA CÀI ĐẶT / CHƯA CÓ TRÊN PATH** (`JAVA_HOME` rỗng) | Lệnh `java -version` báo `CommandNotFoundException` |

---

### 2. RÀ SOÁT TÀI LIỆU BÀN GIAO & CẤU TRÚC KIỂM THỬ

- **Tài liệu `HANDOVER_SESSION.md`:** Không tìm thấy file vật lý có tên `HANDOVER_SESSION.md` trong workspace lẫn lịch sử git. Toàn bộ thông tin bàn giao kỹ thuật, bảng số liệu và hướng dẫn vận hành được lưu trữ chi tiết tại:
  - [`REPORT_R01_K03.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/REPORT_R01_K03.md) (mục F.2, G, H)
  - [`README_TEST.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/README_TEST.md) (mục 2, 3, 4)

- **Cấu trúc kiểm thử package `org.springframework.samples.petclinic.owner`:**
  - Tổng số file test: **13 files**
  - Chi tiết từng file và số lượng `@Test` / `@ParameterizedTest`:

| STT | Tên file test | Phân loại | Số lượng test | Ghi chú phạm vi kiểm thử |
|---|---|---|---|---|
| 1 | `OwnerControllerTests.java` | Baseline (gốc) | 18 | MockMvc controller owner CRUD |
| 2 | `OwnerTests.java` | Baseline (gốc) | 2 | Domain model Owner |
| 3 | `PetControllerTests.java` | Baseline (gốc) | 14 | MockMvc controller pet CRUD |
| 4 | `PetTypeFormatterTests.java` | Baseline (gốc) | 3 | Parse và print PetType |
| 5 | `PetValidatorTests.java` | Baseline (gốc) | 7 | Kiểm chuẩn Pet cơ bản |
| 6 | `VisitControllerTests.java` | Baseline (gốc) | 5 | MockMvc controller visit CRUD |
| **—** | **Tiểu kế Baseline** | **6 files** | **49 tests** | **Khớp 100% với tài liệu bàn giao (49 tests)** |
| 7 | `ControllerBinderMutationTests.java` | Mutation mới | 5 | 4 binder `setDisallowedFields` + `minVisitDate` |
| 8 | `OwnerControllerMutationTests.java` | Mutation mới | 6 | Pageable captor, OOB redirect, lambda |
| 9 | `OwnerMutationTests.java` | Mutation mới | 27 | Bảng quyết định `addPet`/`getPet`/`addVisit`/`toString` |
| 10 | `PetControllerMutationTests.java` | Mutation mới | 19 | Side-effect captors, rethrow, detached-update |
| 11 | `PetValidatorMutationTests.java` | Mutation mới | 9 | BVA 30/31 ký tự + bảng quyết định `isNew × type` |
| 12 | `PetVisitModelMutationTests.java` | Mutation mới | 9 | Model `Pet`/`Visit` + `PetTypeFormatter.print(null)` |
| 13 | `VisitControllerMutationTests.java` | Mutation mới | 6 | Pending-visit, pet/owner unknown, null-date |
| **—** | **Tiểu kế Mutation** | **7 files** | **81 tests** | **Khớp 100% với tài liệu bàn giao (81 tests)** |
| **TỔNG** | **Toàn bộ package owner** | **13 files** | **130 tests** | **Khớp 100% tài liệu bàn giao (49 -> 130 tests)** |

---

### 3. THỰC THI KIỂM CHỨNG & BẢNG ĐỐI CHIẾU SỐ LIỆU

- **Lệnh 1:** `cmd.exe /c "mvnw.cmd test -Dtest=org.springframework.samples.petclinic.owner.** > logs\test_owner_run.log 2>&1"`
  - Kết quả: Không thể thực thi (Exit code 1).
  - Chi tiết log ([`test_owner_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/test_owner_run.log)):
    ```text
    The JAVA_HOME environment variable is not defined correctly, 
    this environment variable is needed to run this program.
    ```
- **Lệnh 2:** `cmd.exe /c "mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true > logs\pit_final_run.log 2>&1"`
  - Kết quả: Không thể thực thi (Exit code 1).
  - Chi tiết log ([`pit_final_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_final_run.log)):
    ```text
    The JAVA_HOME environment variable is not defined correctly, 
    this environment variable is needed to run this program.
    ```

#### Bảng đối chiếu: Số Handover bàn giao vs Số thực đo tại Session S0

| Chỉ số | Số bàn giao (Handover) | Số thực đo (Session S0) | Trạng thái đối chiếu | Ghi chú & Nguồn dẫn |
|---|---|---|---|---|
| **Tổng file test owner** | 13 files (6 gốc + 7 mới) | 13 files | **KHỚP 100%** | Quét thư mục `src/test/.../owner/` |
| **Tổng test methods owner** | 130 tests (49 gốc + 81 mới) | 130 tests | **KHỚP 100%** | Đếm regex `@Test`/`@ParameterizedTest` |
| **Tests owner PASS** | 130/130 pass | **CHƯA ĐO ĐƯỢC (BLOCKER)** | **LỆCH MÔI TRƯỜNG** | Thiếu Java 17 runtime trên hệ điều hành |
| **Line Coverage** | 100% (250/250 lines) | **CHƯA ĐO ĐƯỢC (BLOCKER)** | **LỆCH MÔI TRƯỜNG** | Chưa sinh được `mutations.xml` |
| **Tổng Mutants sinh ra** | 195 | **CHƯA ĐO ĐƯỢC (BLOCKER)** | **LỆCH MÔI TRƯỜNG** | Chưa chạy được PIT minion |
| **Mutants Killed** | 192 (98%) | **CHƯA ĐO ĐƯỢC (BLOCKER)** | **LỆCH MÔI TRƯỜNG** | Chưa chạy được PIT minion |
| **Mutants Survived** | 3 (100% equivalent) | **CHƯA ĐO ĐƯỢC (BLOCKER)** | **LỆCH MÔI TRƯỜNG** | Chưa chạy được PIT minion |
| **File `mutations.xml`** | Có tại `target/pit-reports/` | **CHƯA TỒN TẠI** | **CHƯA TỒN TẠI** | `target/` chưa được tạo do chưa build |

---

### 4. DANH MỤC FILE TẠO / SỬA TRONG SESSION S0

1. [`logs/test_owner_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/test_owner_run.log): Ghi nhận toàn bộ console output của lệnh chạy kiểm thử package owner.
2. [`logs/pit_final_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_final_run.log): Ghi nhận toàn bộ console output của lệnh chạy Mutation Testing bằng PIT.
3. [`docs/sessions/SESSION_LOG.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/docs/sessions/SESSION_LOG.md): Ghi nhận chi tiết kết quả rà soát, nhật ký và blocker của Session S0.
*(Tuân thủ tuyệt đối: Không sửa bất kỳ file mã nguồn nào trong `src/main/java`, `src/test/java`, hay `pom.xml`)*

---

### 5. GIẢI QUYẾT BLOCKER S0 & TÁI HIỆN TOÀN BỘ KẾT QUẢ FINAL

Sau khi được phê duyệt cài đặt Java 17 (Microsoft OpenJDK 17.0.20.1+1 LTS) và cấu hình ổ đĩa ảo thuần ASCII `K:` (`subst K: "d:\Kiểm Thử Phần Mềm\Nhom_20"`):
1. **Kiểm thử đơn vị package owner:**
   - Lệnh: `cmd.exe /c "mvnw.cmd test -Dtest=org.springframework.samples.petclinic.owner.** > logs\test_owner_run.log 2>&1"`
   - Kết quả: **130/130 tests PASS** (13 test files), không có test nào lỗi hay thất bại.
2. **Mutation Testing Final:**
   - Lệnh: `cmd.exe /c "mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true > logs\pit_final_run.log 2>&1"`
   - Kết quả:
     - **Line Coverage:** 250/250 lines (**100.00%**)
     - **Total Mutants:** 195
     - **Killed Mutants:** 192 (**98.46%** ~ 98%)
     - **Survived Mutants:** 3 (100% equivalent mutants: `Owner:108` x2 và `OwnerController:167`)
     - **Mutations with no coverage:** 0
     - File sinh ra: `target/pit-reports/mutations.xml` (185,394 bytes) và `index.html`.
   - Toàn bộ kết quả khớp 100% với tài liệu bàn giao kỹ thuật của nhóm.

---
---

## SESSION S1: Metrics Extraction & Baseline Reconstruction
- **Ngày thực hiện:** 2026-10-19
- **Nhánh làm việc:** `docs/metrics-rca-final-report`
- **Mục tiêu:**
  1. Sao lưu `target/pit-reports/mutations.xml` thành `reports/data/final_mutations.xml`.
  2. Dựng môi trường Baseline cô lập và an toàn bằng `git worktree add ../baseline-wt 500158f732419217507c7656904b8e6aa1bcc0d6` (6 file test gốc, 49 tests). Bổ sung cấu hình PIT 1.30.0 + STRONGER vào `baseline-wt/pom.xml` (tuyệt đối không đụng cây chính). Thực thi PIT trên Baseline, lưu `reports/data/baseline_mutations.xml` và `logs/pit_baseline_run.log`.
  3. Dọn dẹp worktree an toàn (`git worktree remove --force ../baseline-wt`).
  4. Viết công cụ chuẩn hóa `scripts/parse_mutations.py` (chỉ sử dụng Python standard library: `xml.etree.ElementTree`, `csv`, `collections`, `pathlib`) để đọc 2 file XML và xuất 3 file dữ liệu CSV:
     - `reports/data/metrics_summary.csv`
     - `reports/data/survivors_baseline.csv`
     - `reports/data/mutator_breakdown.csv`
  5. Cài đặt Python 3.11 embeddable sau khi có sự đồng ý của người dùng (tuân thủ Ràng buộc 4), đảm bảo script chạy được trên Windows console UTF-8.
  6. Kiểm chứng tính tất định (Determinism Verification): Chạy script 2 lần độc lập, kiểm tra đối chiếu mã băm SHA-256 của các file CSV đầu ra.
  7. Lập báo cáo bảng Markdown tổng hợp `reports/G1_metrics_table.md` cho Phần G.1.

---

### 1. KẾT QUẢ THỰC HIỆN CHECKLIST SESSION S1

| Mục tiêu / Checklist | Yêu cầu kiểm tra | Kết quả thực tế đạt được | Trạng thái | Nguồn kiểm chứng |
| :--- | :--- | :--- | :---: | :--- |
| **1. Tái dựng Baseline** | 49 tests, 195 mutants, ~131 killed (67%), 64 survivors+no_cov | **131/195 killed (67.18%)**, 55 survived, 9 no-coverage (tổng 64 non-killed), Line coverage: 242/250 (96.80% ~ 97%) | **ĐẠT (✓)** | `reports/data/baseline_mutations.xml`<br>`logs/pit_baseline_run.log` |
| **2. Tái kiểm chứng Final** | 130 tests, 195 mutants, 192 killed (98%), 3 survivors (`Owner:108` x2, `OwnerController:167`) | **192/195 killed (98.46%)**, 3 survived (đúng `Owner.java:108` index 39, 42 và `OwnerController.java:167` index 50), 0 no-coverage, Line coverage: 250/250 (100.00%) | **ĐẠT (✓)** | `reports/data/final_mutations.xml`<br>`logs/pit_final_run.log` |
| **3. Thuật toán parse stdlib** | Viết `scripts/parse_mutations.py` thuần thư viện chuẩn Python | Script hoàn thành, tự động cấu hình UTF-8 console, xử lý chính xác cấu trúc XML của PIT | **ĐẠT (✓)** | `scripts/parse_mutations.py` |
| **4. Xuất 3 tệp CSV** | `metrics_summary.csv`<br>`survivors_baseline.csv`<br>`mutator_breakdown.csv` | Đã xuất đầy đủ tại `reports/data/`:<br>- `metrics_summary.csv`: 2 dòng so sánh Baseline vs Final<br>- `survivors_baseline.csv`: đúng 64 dòng mutant chưa diệt ở baseline<br>- `mutator_breakdown.csv`: 19 dòng phân rã theo 8 class và 11 mutator | **ĐẠT (✓)** | `reports/data/*.csv` |
| **5. Tính tất định (Determinism)** | Chạy 2 lần liên tiếp, so sánh SHA-256 checksum của các file CSV | Cả 3 file CSV đều có mã băm SHA-256 trùng khớp 100% từng byte giữa Run 1 và Run 2 | **ĐẠT (✓)** | Lệnh PowerShell `Compare-Object` trả về 0 sai khác |
| **6. Báo cáo Markdown G.1** | `reports/G1_metrics_table.md` truy nguyên mọi số liệu | Báo cáo Markdown chi tiết, trình bày hàn lâm, kèm bảng mã băm SHA-256 và liên kết file nguồn | **ĐẠT (✓)** | `reports/G1_metrics_table.md` |
| **7. Dọn dẹp Worktree** | `git worktree remove` sau khi chạy xong | Worktree `../baseline-wt` đã được xóa sạch hoàn toàn | **ĐẠT (✓)** | `git worktree list` (chỉ còn lại 1 worktree chính) |

---

### 2. BẢNG MÃ BĂM DỮ LIỆU ĐÃ KIỂM CHỨNG (SHA-256 INTEGRITY)

```text
metrics_summary.csv:
94958694C60BA286E22B3A94CBBC2A40C58F727A20B18B0BBF06AC0FCAE303C2

survivors_baseline.csv:
FD400736422A98D9305FB6638CF13CAE2F7BD8AEBB9E37D763830D2D6BBB4389

mutator_breakdown.csv:
C8ED123B40B03880D55AA771D5C6DDFF65B8382FFA8D4E2F97797F107CF97126

baseline_mutations.xml:
819DB886426E8C85B74D128AC18870F70F472B3DE370455B0A25BCE3436A6853

final_mutations.xml:
48F9E5726737801B84CFA0A436E8E8D66C53EE842DBFC118382D3962EF311DE9
```

---

### 3. DANH MỤC TỆP TIN TẠO / CẬP NHẬT TRONG SESSION S1

1. [`reports/data/final_mutations.xml`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/final_mutations.xml): Sao lưu từ `target/pit-reports/mutations.xml` (185,394 bytes).
2. [`reports/data/baseline_mutations.xml`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/baseline_mutations.xml): Báo cáo đột biến Baseline thu được từ worktree cô lập (170,860 bytes).
3. [`logs/pit_baseline_run.log`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_baseline_run.log): Log thực thi PIT Baseline (17,528 bytes).
4. [`scripts/parse_mutations.py`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/parse_mutations.py): Script Python stdlib phân tích báo cáo và xuất CSV tất định.
5. [`reports/data/metrics_summary.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/metrics_summary.csv): CSV tóm lược các chỉ số cốt lõi Baseline vs Final.
6. [`reports/data/survivors_baseline.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/survivors_baseline.csv): Danh sách 64 mutant chưa bị diệt tại Baseline.
7. [`reports/data/mutator_breakdown.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/mutator_breakdown.csv): Phân rã tỷ lệ diệt theo 8 lớp và 11 loại toán tử đột biến.
8. [`reports/G1_metrics_table.md`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/G1_metrics_table.md): Tài liệu báo cáo Markdown hoàn chỉnh cho mục G.1.
9. [`docs/sessions/SESSION_LOG.md`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/docs/sessions/SESSION_LOG.md): Cập nhật tiến độ toàn bộ phiên làm việc.

*(Ràng buộc bất biến: Hoàn toàn không sửa đổi các tệp `src/main/java`, `src/test/java`, hay `pom.xml` của cây làm việc chính).*

---

### 4. ĐIỂM CÒN MỞ & KẾ HOẠCH CHO SESSION TIẾP THEO (SESSION S2)

- **Điểm còn mở:** Toàn bộ tiêu chí nghiệm thu của Session S1 đã hoàn thành xuất sắc 100%, không còn blocker nào.
- **Kế hoạch cho Session S2:**
  - Thực hiện nhiệm vụ trực quan hóa (Visualization): Viết `scripts/make_charts.py` xuất 4 biểu đồ PNG chuẩn in ấn 200 DPI dựa trên dữ liệu CSV.
  - Lập hướng dẫn chụp màn hình báo cáo PIT HTML (`pit_index.png`).

---
---

## SESSION S2: Trực quan hóa số liệu kiểm thử (Data Visualization)
- **Ngày thực hiện:** 2026-10-19
- **Nhánh làm việc:** `docs/metrics-rca-final-report`
- **Mục tiêu:**
  1. Xin cấp phép sử dụng mạng ngoài (tuân thủ Ràng buộc bất biến số 4) để tải `get-pip.py` và cài đặt `matplotlib` (3.11.2) vào môi trường Python 3.11 portable (`C:\Users\Admin\.python`).
  2. Bổ sung trích xuất dữ liệu tăng trưởng test case theo file vào `scripts/parse_mutations.py` để sinh tệp chuẩn `reports/data/tests_by_file.csv` với cơ chế assert dữ liệu nghiêm ngặt (13 files, 49 baseline tests, 130 final tests, delta +81 tests).
  3. Xây dựng công cụ đồ họa `scripts/make_charts.py` (sử dụng `matplotlib`), xuất 4 hình ảnh PNG độ phân giải 200 DPI vào `reports/figures/` phục vụ báo cáo học thuật:
     - `fig1_coverage_vs_mutation.png`: Cột nhóm Line Coverage vs Mutation Score (Baseline vs Final), làm nổi bật thông điệp khoảng trống kiểm thử 29.62% (Line coverage 96.80% ~ 97% nhưng Mutation score chỉ 67.18%).
     - `fig2_mutant_status.png`: Cột chồng (stacked bar) Killed / Survived / No Coverage (Baseline vs Final).
     - `fig3_survivors_by_mutator.png`: Biểu đồ ngang phân rã 64 mutants chưa diệt ở Baseline theo 8 toán tử (Survived + No Coverage).
     - `fig4_tests_growth.png`: Tăng trưởng test case theo từng file kiểm thử (Baseline vs Final).
  4. Tuân thủ tiêu chuẩn trình bày biểu đồ: Font tiếng Việt chuẩn Unicode (`Segoe UI`, `Arial`), nhãn số liệu trực tiếp trên từng cột/thanh, phối màu tương phản cao kết hợp vân sọc (hatch patterns) giúp nhận diện rõ ràng khi in ấn đen trắng, tiêu đề học thuật và chú thích nguồn dữ liệu CSV minh bạch.
  5. Biên soạn tài liệu hướng dẫn chụp ảnh màn hình báo cáo HTML gốc của PIT: `reports/figures/GUIDE_CAPTURE_PIT_INDEX.md` để thành viên tự lưu thành `reports/figures/pit_index.png` (tuyệt đối không giả mạo ảnh).
  6. Thực hiện vòng lặp VERIFY - FIX trực quan: Dùng công cụ `view_file` xem lại từng ảnh PNG, tinh chỉnh khoảng cách tọa độ để triệt tiêu hoàn toàn hiện tượng chồng chữ, lẹm chữ, hay tràn viền.

---

### 1. KẾT QUẢ THỰC HIỆN CHECKLIST SESSION S2

| Mục tiêu / Tiêu chí nghiệm thu | Yêu cầu kỹ thuật | Kết quả thực tế đạt được | Trạng thái | Nguồn kiểm chứng |
| :--- | :--- | :--- | :---: | :--- |
| **1. Cài đặt Matplotlib** | Python 3.11 portable + pip + matplotlib | Đã cài đặt thành công `pip-26.2.1` và `matplotlib-3.11.2` sau khi người dùng phê chuẩn qua `ask_question` | **ĐẠT (✓)** | `python -c "import matplotlib; print(matplotlib.__version__)"` → `3.11.2` |
| **2. Tệp `tests_by_file.csv`** | Đầy đủ 13 file test, khớp 49 baseline / 130 final | Đã sinh tệp `reports/data/tests_by_file.csv`, assert dữ liệu khớp 100% tài liệu bàn giao | **ĐẠT (✓)** | `reports/data/tests_by_file.csv`<br>`scripts/parse_mutations.py` |
| **3. Script `make_charts.py`** | Đọc dữ liệu từ CSV, tự động `assert` trước khi vẽ | Script hoàn thành, tự động assert đúng từng chỉ số: 96.80%, 67.18%, 100%, 98.46%, tổng 195 mutants, 64 survivors | **ĐẠT (✓)** | `scripts/make_charts.py` |
| **4. Xuất 4 tệp PNG 200 DPI** | `fig1`, `fig2`, `fig3`, `fig4` tại `reports/figures/` | Đã xuất đủ 4 tệp PNG độ phân giải cao 200 DPI, kích thước chuẩn ấn phẩm khoa học | **ĐẠT (✓)** | `reports/figures/*.png` |
| **5. Kiểm chứng trực quan ảnh** | Không chồng chữ, không cắt nhãn, phân biệt khi in B&W | Đã mở xem trực tiếp cả 4 file ảnh qua `view_file`, tinh chỉnh layout không lỗi font/tofu, có họa tiết vân sọc | **ĐẠT (✓)** | Công cụ `view_file` xác nhận ảnh sắc nét |
| **6. Hướng dẫn `pit_index.png`** | Hướng dẫn tự chụp màn hình, không giả mạo ảnh | Đã tạo tài liệu `reports/figures/GUIDE_CAPTURE_PIT_INDEX.md` hướng dẫn chi tiết 4 bước chụp ảnh | **ĐẠT (✓)** | `reports/figures/GUIDE_CAPTURE_PIT_INDEX.md` |

---

### 2. ĐẶC TẢ CHI TIẾT 4 BIỂU ĐỒ NGUYỆM THU

#### 2.1. `fig1_coverage_vs_mutation.png` (So sánh Line Coverage vs Mutation Score)
- **Thông điệp cốt lõi:** Làm nổi bật sự tương phản giữa Line Coverage cao (96.80% ~ 97%) và Mutation Score thực tế (67.18% ~ 67%) tại giai đoạn Baseline, vạch rõ "Khoảng trống kiểm thử (Test Gap) 29.62%" và sự nguy hiểm của ảo giác an toàn khi chỉ đo độ bao phủ dòng.
- **Tại Final:** Độ bao phủ dòng đạt tuyệt đối 100.00% (250/250 lines) và điểm đột biến tiệm cận tối đa 98.46% (192/195 killed), toàn bộ 3 mutant sống sót đều là Equivalent Mutants (điểm đột biến hữu hiệu đạt 100%).
- **Trình bày:** Cột nhóm 2 pha, màu xanh Navy vân sọc chéo (`//`) cho Line Coverage và màu cam đất hạt chấm (`..`) cho Mutation Score; hộp chú thích nổi bật khoảng trống 29.62% ở vị trí trung tâm thoáng đãng.

#### 2.2. `fig2_mutant_status.png` (Cơ cấu trạng thái Mutant)
- **Thông điệp cốt lõi:** Phân bổ toàn diện 195 mutants theo 3 trạng thái: Killed (Đã diệt), Survived (Sống sót) và No Coverage (Không có test chạm tới).
- **Số liệu:**
  - *Baseline:* 131 Killed (67.2%), 55 Survived (28.2%), 9 No Coverage (4.6%).
  - *Final:* 192 Killed (98.5%), 3 Survived (1.5% - 100% Equivalent Mutants), 0 No Coverage (0.0%).
- **Trình bày:** Cột chồng (stacked bar) chuẩn xác; đường chỉ dẫn (leader line) trỏ từ ngoài vào cho các lát cắt nhỏ (9 No Coverage và 3 Survived) chống đè chữ; nhãn tổng số 195 mutants rõ nét trên đỉnh cột.

#### 2.3. `fig3_survivors_by_mutator.png` (Phân bố 64 mutant sống sót ở Baseline theo Toán tử)
- **Thông điệp cốt lõi:** Bóc tách nguyên nhân vì sao bộ test gốc để lọt 64 mutants non-killed trên 8 toán tử đột biến khác nhau, phân định rõ giữa mutant có test chạm tới nhưng thiếu assert (55 Survived) và mutant hoàn toàn thiếu test (9 No Coverage).
- **Toán tử trọng điểm:** `RemoveConditionalMutator_EQUAL_IF` (20 mutants: 19 S, 1 NC), `VoidMethodCallMutator` (20 mutants: 18 S, 2 NC), `RemoveConditionalMutator_EQUAL_ELSE` (12 mutants: 11 S, 1 NC), `NullReturnValsMutator` (6 mutants: 1 S, 5 NC).
- **Trình bày:** Cột ngang phân cấp giảm dần từ trên xuống dưới, hiển thị chi tiết số lượng Survived và No Coverage trên từng thanh.

#### 2.4. `fig4_tests_growth.png` (Tăng trưởng Test Case theo từng file)
- **Thông điệp cốt lõi:** Minh họa trực quan quá trình nâng cấp toàn diện bộ test suite từ 6 file gốc (49 tests) lên 13 file (130 tests), bổ sung 7 file chuyên biệt (+81 tests, tỷ lệ tăng trưởng +165.31%).
- **Trình bày:** Cột ngang đôi (paired horizontal bars) với đường ranh giới phân tách trực quan giữa nhóm file gốc (Baseline) và nhóm file đột biến mới (Mutation), nhãn số lượng test và mức tăng (`+Δ`) hiển thị rõ ràng bên cạnh mỗi thanh.

---

### 3. BẢNG MÃ BĂM DỮ LIỆU ĐÃ KIỂM CHỨNG (SHA-256 INTEGRITY)

```text
fig1_coverage_vs_mutation.png:
BCA1118EE42A868B792441DA249C42C5685F7D3F1C80934D2D60FB743D5CB9A2

fig2_mutant_status.png:
7E8041823B672EE9CE77D52EB1A7F81AFB33B6ED15DBBD06557AB66526483509

fig3_survivors_by_mutator.png:
2391071638671A69B2F1ECA832062B34D4251D0180FD2F146382F410C7135686

fig4_tests_growth.png:
1F27D444E6C3C5897071CBD04716DD233A049BBBEBD857B65F522A0AF6055150

tests_by_file.csv:
AA501AD4EC4BCD8C6866EC2099F6989A78999E45BC64CD5C1F8DCF06F31799BC

make_charts.py:
D94737645523C15C2AD3B145B8B612943192C4045F02B59DEC636EF18C6995A0

GUIDE_CAPTURE_PIT_INDEX.md:
F10B2D71BEE70527D4D46E647F50574CF059F2451E4AC0A56C5A24BDC6F2DB29
```

---

### 4. DANH MỤC TỆP TIN TẠO / CẬP NHẬT TRONG SESSION S2

1. [`scripts/make_charts.py`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/make_charts.py): Script Python xuất 4 biểu đồ 200 DPI tự động kiểm chứng assert với dữ liệu CSV.
2. [`scripts/parse_mutations.py`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/parse_mutations.py): Bổ sung hàm `generate_tests_by_file` tự động sinh `tests_by_file.csv`.
3. [`reports/data/tests_by_file.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/tests_by_file.csv): Bảng dữ liệu thống kê số lượng test case theo từng file giữa Baseline và Final.
4. [`reports/figures/fig1_coverage_vs_mutation.png`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/fig1_coverage_vs_mutation.png): Biểu đồ Line Coverage vs Mutation Score (200 DPI).
5. [`reports/figures/fig2_mutant_status.png`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/fig2_mutant_status.png): Biểu đồ cột chồng cơ cấu trạng thái mutant (200 DPI).
6. [`reports/figures/fig3_survivors_by_mutator.png`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/fig3_survivors_by_mutator.png): Biểu đồ phân rã survivor baseline theo mutator (200 DPI).
7. [`reports/figures/fig4_tests_growth.png`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/fig4_tests_growth.png): Biểu đồ tăng trưởng số test theo file (200 DPI).
8. [`reports/figures/GUIDE_CAPTURE_PIT_INDEX.md`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/GUIDE_CAPTURE_PIT_INDEX.md): Hướng dẫn thành viên tự chụp ảnh màn hình báo cáo PIT HTML.
9. [`docs/sessions/SESSION_LOG.md`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/docs/sessions/SESSION_LOG.md): Cập nhật toàn diện tiến độ phiên làm việc Session S2.

*(Ràng buộc bất biến tuân thủ 100%: Không chỉnh sửa `src/main/java`, `src/test/java`, hay `pom.xml`).*

---

### 5. ĐIỂM CÒN MỞ & KẾ HOẠCH CHO SESSION TIẾP THEO (SESSION S3)

- **Điểm còn mở:** Toàn bộ tiêu chí nghiệm thu của Session S2 đã hoàn thành xuất sắc 100%, không còn blocker nào.
- **Kế hoạch cho Session S3:** Đã hoàn thành trong Session S3 dưới đây.

---
---

## SESSION S3: Phân tích nguyên nhân cốt lõi (RCA) & Khiếm khuyết mã nguồn (Code Smell)
- **Ngày thực hiện:** 2026-10-19
- **Nhánh làm việc:** `docs/metrics-rca-final-report`
- **Mục tiêu:**
  1. Phân nhóm toàn bộ 64 mutant sống sót ở Baseline (`reports/data/survivors_baseline.csv`) thành các nguyên nhân gốc rễ cụ thể theo chuẩn IEEE 1044 / IEEE 610.12 (**Error – Fault – Failure**).
  2. Đảm bảo tính toàn vẹn toán học: tổng số mutant trong các nhóm RCA đúng bằng 64, không sót, không trùng (100% được chứng minh bằng script kiểm chứng `scripts/verify_rca.py`).
  3. Lập bảng đối chiếu chi tiết 64 mutants: vị trí file:dòng trong `src/main/java`, phương thức, toán tử đột biến, mô tả thay đổi, test case tương ứng của TV3/TV4 đã tiêu diệt và kỹ thuật kiểm thử được áp dụng (POJO Unit Test, ArgumentCaptor, BVA, Decision Table, Exception Testing, Mockito verify).
  4. Phân tích 06 Code Smells / Defect đặc thù trong mã nguồn `src/main/java/org/springframework/samples/petclinic/owner/*` có bằng chứng trích dẫn mã nguồn thực tế và số dòng chính xác (Smell 1: Dead-store `OwnerController:167`; Smell 2: Defensive guard `Owner:108`; Smell 3: Double query `OwnerController:68, 182`; Smell 4: Model binding aliasing `PetController:186-200`; Smell 5: Magic number `OwnerController:142`; Smell 6: DB vendor tight coupling `PetController:204`).
  5. Xuất báo cáo Markdown học thuật hoàn chỉnh tại `reports/G3_RCA.md`.
  6. Xây dựng công cụ kiểm chứng tự động `scripts/verify_rca.py` kiểm tra đối chiếu tính hợp lệ của mọi trích dẫn mã nguồn và tính toán mã băm SHA-256.

---

### 1. KẾT QUẢ THỰC HIỆN CHECKLIST SESSION S3

| Mục tiêu / Tiêu chí nghiệm thu | Yêu cầu kỹ thuật | Kết quả thực tế đạt được | Trạng thái | Nguồn kiểm chứng |
| :--- | :--- | :--- | :---: | :--- |
| **1. Tổng số mutant RCA = 64** | Phân loại 64 survivors không sót, không trùng | **Đúng 64/64 mutants** (5+14+6+3+9+27 = 64), tỷ lệ 100.0% | **ĐẠT (✓)** | `reports/G3_RCA.md`<br>`scripts/verify_rca.py` |
| **2. Chuẩn phân tích IEEE** | Mô hình 3 tầng Error -> Fault -> Failure | Đã xây dựng hoàn chỉnh cho cả 6 nhóm nguyên nhân gốc rễ | **ĐẠT (✓)** | Mục 1 & 2 `reports/G3_RCA.md` |
| **3. Trích dẫn file:dòng chính xác** | Mọi mutant và smell đều tồn tại trong `src/main/java` | **100% 64 mutants** và **6 Code Smells** khớp chính xác từng số dòng và trích đoạn code | **ĐẠT (✓)** | `scripts/verify_rca.py`<br>`src/main/java` |
| **4. Bằng chứng Code Smell** | Không nêu smell chung chung, phải có code trích dẫn | Đã phân tích chi tiết 6 code smell kèm trích đoạn code và đề xuất tái cấu trúc (không sửa code) | **ĐẠT (✓)** | Mục 4 `reports/G3_RCA.md` |
| **5. Báo cáo Markdown G.3** | Xuất `reports/G3_RCA.md` văn phong học thuật | Báo cáo chi tiết, chuyên nghiệp, bảng biểu rõ ràng, kèm ma trận truy vết test TV3/TV4 | **ĐẠT (✓)** | `reports/G3_RCA.md` |
| **6. Tính toàn vẹn dữ liệu** | Kiểm chứng tự động bằng script Python | Script `scripts/verify_rca.py` chạy thành công không lỗi, xuất mã băm SHA-256 | **ĐẠT (✓)** | Console output `scripts/verify_rca.py` |

---

### 2. PHÂN BỔ 64 MUTANTS THEO 6 NHÓM NGUYÊN NHÂN CỐT LÕI (RCA)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   CƠ CẤU 64 MUTANT BASELINE THEO NGUYÊN NHÂN GỐC RỄ          │
└─────────────────────────────────────────────────────────────────────────────┘
  1. MockMvc che khuất cập nhật thực thể & gán dư thừa:   5 mutants ( 7.81%)
  2. Thiếu kiểm chứng tác dụng phụ & phương thức void:   14 mutants (21.88%)
  3. Thiếu kiểm thử giá trị biên & tính toán số học:       6 mutants ( 9.38%)
  4. Thiếu assert nội dung sâu & giá trị trả về:          3 mutants ( 4.69%)
  5. Nhánh ngoại lệ & luồng rẽ thiếu độ bao phủ (NO_COV): 9 mutants (14.06%)
  6. Thiếu bảng quyết định cho tổ hợp điều kiện logic:   27 mutants (42.19%)
───────────────────────────────────────────────────────────────────────────────
  TỔNG CỘNG:                                             64 mutants (100.0%)
```

---

### 3. BẢNG MÃ BĂM DỮ LIỆU ĐÃ KIỂM CHỨNG (SHA-256 INTEGRITY)

```text
reports/G3_RCA.md:
96EFE5513AA8174F204DBD9D6890BB3C517EA57248D1A3BA5DBAD6A69AA6B733

scripts/analyze_rca.py:
CF9F34027471F8C5815EF45A253457D25DAE7227448B5C036F26DDFE05A42921

scripts/verify_rca.py:
8B70A06B923B280783F418939768B4B489E530BD9ED73B1BF5122BA3659A5A41
```

---

### 4. DANH MỤC TỆP TIN TẠO / CẬP NHẬT TRONG SESSION S3

1. [`reports/G3_RCA.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/G3_RCA.md): Báo cáo chuyên sâu về RCA và Code Smell (Phần G.2 & G.3) gồm 6 nhóm RCA và 6 Code Smells trích dẫn mã nguồn thực tế.
2. [`scripts/analyze_rca.py`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/analyze_rca.py): Script Python phân tích đối chiếu 64 baseline survivors với final mutations.
3. [`scripts/verify_rca.py`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/verify_rca.py): Công cụ kiểm chứng tự động tính toàn vẹn của báo cáo và vị trí mã nguồn.
4. [`docs/sessions/SESSION_LOG.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/docs/sessions/SESSION_LOG.md): Ghi nhận chi tiết kết quả thực hiện Session S3.

*(Ràng buộc bất biến tuân thủ 100%: Không chỉnh sửa `src/main/java`, `src/test/java`, hay `pom.xml`).*

---

### 5. ĐIỂM CÒN MỞ & KẾ HOẠCH CHO SESSION TIẾP THEO (SESSION S4)

- **Điểm còn mở:** Toàn bộ tiêu chí nghiệm thu của Session S3 đã hoàn thành xuất sắc 100%, không còn blocker nào.
- **Kế hoạch cho Session S4:**
  1. **Phần G.4 (Boolean Algebraic Proof):** Thực hiện chứng minh hình thức bằng đại số Boolean cho 3 Equivalent Mutants (`Owner.java:108` x2 và `OwnerController.java:167`).
  2. **Tổng hợp báo cáo Phần G:** Tích hợp G.1, G.2, G.3, G.4 thành báo cáo hoàn chỉnh phục vụ biên tập `REPORT_R01_K03.docx`.


