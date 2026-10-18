# BÁO CÁO PHẦN G.1: BẢNG ĐỐI SÁNH CHỈ SỐ KIỂM THỬ ĐỘT BIẾN (BASELINE VS FINAL)

**Nhóm thực hiện:** Program_R01-K03  
**Học phần:** Kiểm thử phần mềm – Khoa CNTT, Trường Đại học Đà Lạt  
**Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm  
**Người lập bảng / Phân tích:** Thành viên 5 (Metrics, RCA & Quality Analyst)  
**Phạm vi kiểm thử:** Gói `org.springframework.samples.petclinic.owner.*`  
**SUT & Phiên bản:** Spring PetClinic (Pinned Commit: `500158f732419217507c7656904b8e6aa1bcc0d6`)  
**Công cụ & Cấu hình:** PIT (pitest-maven 1.30.0, pitest-junit5-plugin 1.2.3), mutator group `STRONGER`, Java 17 (Microsoft OpenJDK 17.0.20.1+1 LTS).

---

## 1. Bảng đối sánh tổng hợp (Executive Summary)

Dữ liệu được trích xuất tự động bằng `scripts/parse_mutations.py` từ hai báo cáo thực nghiệm gốc:
- Baseline: `reports/data/baseline_mutations.xml` (chạy trên 6 file test gốc, 49 tests)
- Final: `reports/data/final_mutations.xml` (chạy trên toàn bộ 13 file test, 130 tests)

| Chỉ số (Metric) | Baseline (Gốc) | Final (Sau cải tiến) | Chênh lệch (Delta) | Tỷ lệ tăng trưởng |
| :--- | :---: | :---: | :---: | :---: |
| **Số lượng test case (owner package)** | 49 | 130 | +81 tests | +165.31% |
| **Dòng lệnh được bao phủ (Covered Lines)** | 242 / 250 | 250 / 250 | +8 lines | +3.31% |
| **Line Coverage (%)** | **96.80%** (97%) | **100.00%** | **+3.20%** | Tuyệt đối (100%) |
| **Tổng số đột biến sinh ra (Total Mutants)** | 195 | 195 | 0 | Giữ nguyên (STRONGER) |
| **Mutant bị tiêu diệt (Killed Mutants)** | 131 | 192 | +61 mutants | +46.56% |
| **Mutant sống sót (Survived Mutants)** | 55 | 3 | -52 mutants | Giảm 94.55% |
| **Mutant không có test bao phủ (No Coverage)**| 9 | 0 | -9 mutants | Triệt tiêu hoàn toàn (0) |
| **Tổng số mutant chưa diệt (Non-Killed)** | 64 | 3 | -61 mutants | Giảm 95.31% |
| **Điểm đột biến (Mutation Score)** | **67.18%** (~67%) | **98.46%** (~98%) | **+31.28%** | **Tiệm cận tối đa (98.46%)** |
| **Năng lực bộ test (Test Strength)** | 70.43% (131/186) | 98.46% (192/195) | +28.03% | Đạt mức tối ưu |

> [!NOTE]
> - Nguồn dữ liệu bảng: [`reports/data/metrics_summary.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/metrics_summary.csv)
> - Toàn bộ 3 mutant sống sót còn lại ở giai đoạn Final (192/195) đều là các **Equivalent Mutants** (được chứng minh bằng đại số Boolean tại Mục 4 và chi tiết tại Phần G.4). Nếu trừ 3 equivalent mutants, mutation score hữu hiệu đạt **100% (192/192)**.

---

## 2. Phân rã theo Lớp nghiệp vụ (Breakdown by Class)

Chi tiết tỷ lệ diệt đột biến của từng lớp thuộc gói `org.springframework.samples.petclinic.owner.*`:

| STT | Lớp nghiệp vụ (Class) | Tổng số Mutants | Baseline Killed | Baseline Score | Final Killed | Final Survived | Final Score | Trạng thái cải tiến |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `Owner` | 34 | 16 | 47.06% | 32 | 2 | **94.12%** | +47.06% (2 equivalent) |
| 2 | `OwnerController` | 45 | 38 | 84.44% | 44 | 1 | **97.78%** | +13.34% (1 equivalent) |
| 3 | `Pet` | 3 | 3 | 100.00% | 3 | 0 | **100.00%** | Duy trì 100% |
| 4 | `PetController` | 70 | 42 | 60.00% | 70 | 0 | **100.00%** | +40.00% (Diệt 28/28) |
| 5 | `PetTypeFormatter` | 6 | 5 | 83.33% | 6 | 0 | **100.00%** | +16.67% (Diệt 1/1) |
| 6 | `PetValidator` | 17 | 15 | 88.24% | 17 | 0 | **100.00%** | +11.76% (Diệt 2/2) |
| 7 | `Visit` | 2 | 1 | 50.00% | 2 | 0 | **100.00%** | +50.00% (Diệt 1/1) |
| 8 | `VisitController` | 18 | 11 | 61.11% | 18 | 0 | **100.00%** | +38.89% (Diệt 7/7) |
| | **TỔNG CỘNG** | **195** | **131** | **67.18%** | **192** | **3** | **98.46%** | **+31.28%** |

> [!TIP]
> - Nguồn dữ liệu lớp: [`reports/data/mutator_breakdown.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/mutator_breakdown.csv) (các dòng có `dimension=BY_CLASS`).
> - 6 trên 8 lớp đạt tỷ lệ tiêu diệt đột biến tuyệt đối **100.00%**. Hai lớp còn lại (`Owner` và `OwnerController`) chỉ còn các đột biến tương đương không thể tiêu diệt về mặt lý thuyết.

---

## 3. Phân rã theo Toán tử đột biến (Breakdown by Mutator)

Nhóm toán tử `STRONGER` sinh ra 11 loại mutator khác nhau trên phạm vi gói `owner`:

| STT | Toán tử đột biến (Mutator) | Tổng Mutants | Baseline Killed | Baseline Score | Final Killed | Final Survived | Final Score | Tồn dư Final |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `BooleanFalseReturnValsMutator` | 1 | 1 | 100.00% | 1 | 0 | 100.00% | 0 |
| 2 | `BooleanTrueReturnValsMutator` | 2 | 1 | 50.00% | 2 | 0 | 100.00% | 0 |
| 3 | `ConditionalsBoundaryMutator` | 3 | 2 | 66.67% | 3 | 0 | 100.00% | 0 |
| 4 | `EmptyObjectReturnValsMutator` | 33 | 30 | 90.91% | 33 | 0 | 100.00% | 0 |
| 5 | `MathMutator` | 1 | 0 | 0.00% | 1 | 0 | 100.00% | 0 |
| 6 | `NullReturnValsMutator` | 20 | 14 | 70.00% | 20 | 0 | 100.00% | 0 |
| 7 | `RemoveConditionalMutator_EQUAL_ELSE` | 48 | 36 | 75.00% | 48 | 0 | 100.00% | 0 |
| 8 | `RemoveConditionalMutator_EQUAL_IF` | 48 | 28 | 58.33% | 46 | 2 | **95.83%** | 2 (`Owner:108`) |
| 9 | `RemoveConditionalMutator_ORDER_ELSE` | 3 | 3 | 100.00% | 3 | 0 | 100.00% | 0 |
| 10 | `RemoveConditionalMutator_ORDER_IF` | 3 | 3 | 100.00% | 3 | 0 | 100.00% | 0 |
| 11 | `VoidMethodCallMutator` | 33 | 13 | 39.39% | 32 | 1 | **96.97%** | 1 (`OwnerController:167`) |
| | **TỔNG CỘNG** | **195** | **131** | **67.18%** | **192** | **3** | **98.46%** | **3** |

---

## 4. Danh sách và Đặc tả 3 Mutant sống sót tại Final (Equivalent Mutants)

Toàn bộ 3 mutant tồn dư tại báo cáo Final đều nằm trong danh sách đã được định danh chính xác, không phát sinh bất kỳ survivor ngoài ý muốn nào:

| STT | File nguồn & Vị trí dòng | Phương thức (Method) | Toán tử (Mutator) | Nội dung đột biến sinh ra | Bản chất kiểm thử |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **EQ-01** | [`Owner.java:108`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/Owner.java#L108) | `addPet(Pet pet)` | `RemoveConditionalMutator_EQUAL_IF` (index 39) | `removed conditional - replaced equality check with true` | **Equivalent Mutant** (Đại số Boolean: Dead branch / Biểu thức dư thừa) |
| **EQ-02** | [`Owner.java:108`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/Owner.java#L108) | `addPet(Pet pet)` | `RemoveConditionalMutator_EQUAL_IF` (index 42) | `removed conditional - replaced equality check with true` | **Equivalent Mutant** (Đại số Boolean: Biểu thức con tương đương hàm) |
| **EQ-03** | [`OwnerController.java:167`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L167) | `processUpdateOwnerForm(...)` | `VoidMethodCallMutator` (index 50) | `removed call to org/springframework/samples/petclinic/owner/Owner::setId` | **Equivalent Mutant** (State Invariance: `@PathVariable` binding đã gán ID trùng khớp) |

---

## 5. Bằng chứng kiểm chứng & Truy xuất nguồn gốc (Traceability & Checksum)

Tuân thủ nghiêm ngặt **Ràng buộc bất biến số 3**: Mọi con số trong báo cáo đều được trích xuất trực tiếp từ các file dữ liệu và nhật ký thực thi, không làm tròn sai lệch hay suy đoán.

### 5.1. Bảng mã băm toàn vẹn (SHA-256 Checksums)

| Tên tệp dữ liệu / log | Đường dẫn tệp | Kích thước | Mã băm SHA-256 |
| :--- | :--- | :---: | :--- |
| `metrics_summary.csv` | [`reports/data/metrics_summary.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/metrics_summary.csv) | 250 B | `94958694C60BA286E22B3A94CBBC2A40C58F727A20B18B0BBF06AC0FCAE303C2` |
| `survivors_baseline.csv` | [`reports/data/survivors_baseline.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/survivors_baseline.csv) | 7,351 B | `FD400736422A98D9305FB6638CF13CAE2F7BD8AEBB9E37D763830D2D6BBB4389` |
| `mutator_breakdown.csv` | [`reports/data/mutator_breakdown.csv`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/mutator_breakdown.csv) | 1,432 B | `C8ED123B40B03880D55AA771D5C6DDFF65B8382FFA8D4E2F97797F107CF97126` |
| `baseline_mutations.xml` | [`reports/data/baseline_mutations.xml`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/baseline_mutations.xml) | 170,860 B | `819DB886426E8C85B74D128AC18870F70F472B3DE370455B0A25BCE3436A6853` |
| `final_mutations.xml` | [`reports/data/final_mutations.xml`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/final_mutations.xml) | 185,394 B | `48F9E5726737801B84CFA0A436E8E8D66C53EE842DBFC118382D3962EF311DE9` |
| `pit_baseline_run.log` | [`logs/pit_baseline_run.log`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_baseline_run.log) | 17,528 B | Trích xuất tại commit `500158f` trên worktree cô lập |
| `pit_final_run.log` | [`logs/pit_final_run.log`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_final_run.log) | 18,348 B | Trích xuất trên nhánh `docs/metrics-rca-final-report` |

### 5.2. Tính tất định và khả năng tái lập (Determinism Verification)

Script [`scripts/parse_mutations.py`](file:///D:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/parse_mutations.py) đã được chạy kiểm chứng 2 lần độc lập:
```powershell
& "C:\Users\Admin\.python\python.exe" scripts/parse_mutations.py
```
Kết quả kiểm tra đối chiếu bằng lệnh `Compare-Object` cho thấy 100% các giá trị băm SHA-256 của toàn bộ các file CSV đầu ra hoàn toàn trùng khớp từng byte (bit-for-bit identical), đảm bảo tính tất định cao nhất phục vụ chấm điểm và thẩm định học thuật.
