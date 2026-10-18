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
  1. **Phần G.2 (Code Smell & Defect Analysis):** Rà soát các vấn đề thiết kế mã nguồn, dead code, và code smell trong gói `owner` phát hiện qua quá trình kiểm thử đột biến (ví dụ: `addPet` dư thừa điều kiện, `@PathVariable` binding trùng lặp `setId`, các nhánh exception unreachable).
  2. **Phần G.3 (Root Cause Analysis - RCA):** Lập bảng phân tích nguyên nhân gốc rễ theo mô hình chuẩn IEEE **Error – Fault – Failure** cho các khiếm khuyết được phát hiện và giải thích vì sao bộ test baseline bỏ sót.
  3. **Phần G.4 (Boolean Algebraic Proof):** Thực hiện chứng minh hình thức bằng đại số Boolean cho 3 Equivalent Mutants (`EQ-01`, `EQ-02` tại `Owner.java:108` và `EQ-03` tại `OwnerController.java:167`).
