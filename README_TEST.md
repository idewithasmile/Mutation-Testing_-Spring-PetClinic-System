# README_TEST — HƯỚNG DẪN VẬN HÀNH & TÁI HIỆN KIỂM THỬ (R01 + K03)

> **Dự án:** R01 — Spring PetClinic  
> **Kỹ thuật kiểm thử:** K03 — Mutation Testing bằng PIT (Pitest)  
> **Người phụ trách:** Thành viên 1 (Nhóm trưởng) — Phụ trách Nguyên lý K03, CI/CD Pipeline & Vận hành Tái hiện  
> **Commit SHA cố định (Pinned):** `500158f732419217507c7656904b8e6aa1bcc0d6` (Upstream: `https://github.com/spring-projects/spring-petclinic`)  
> **Phạm vi kiểm thử đột biến:** `org.springframework.samples.petclinic.owner.*`  

---

## 1. Yêu cầu môi trường tối thiểu

Hệ thống được thiết kế để vận hành độc lập, không yêu cầu cài đặt Maven rời hay cài đặt cơ sở dữ liệu bên ngoài.

| Thành phần | Yêu cầu tối thiểu | Lệnh kiểm tra | Ghi chú |
|:---|:---|:---|:---|
| **JDK** | Java 17 trở lên | `java -version` | Đã kiểm chứng tương thích tối ưu trên Eclipse Adoptium Temurin 17.0.20.1 |
| **Biến `JAVA_HOME`** | Trỏ tới thư mục cài đặt JDK 17 | Windows: `echo %JAVA_HOME%`<br>Linux/macOS: `echo $JAVA_HOME` | Bắt buộc để Maven Wrapper khởi tạo JVM chính xác |
| **Git** | Phiên bản 2.30+ | `git --version` | Dùng để clone mã nguồn và checkout đúng commit SHA |
| **Maven** | Không cần cài rời | `./mvnw -v` hoặc `.\mvnw.cmd -v` | Sử dụng Maven Wrapper đi kèm dự án (Apache Maven 3.9.16) |
| **Docker** | **Không bắt buộc** | — | Chỉ dùng cho 2 lớp tích hợp DB ngoài (`*IntegrationTests`), đã loại khỏi test gate mặc định |
| **Internet** | Chỉ cần lần đầu | — | Để Maven Wrapper tải các dependencies cần thiết (~200 MB) |

---

## 2. Dựng dự án và khóa cứng phiên bản (Pin Commit SHA)

Thực hiện sao chép kho mã nguồn gốc và chuyển về đúng commit SHA đã được nhóm nghiên cứu khóa cứng:

```bash
git clone https://github.com/spring-projects/spring-petclinic.git Program_R01-K03
cd Program_R01-K03
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6
git rev-parse HEAD   # Kết quả đầu ra phải chính xác: 500158f732419217507c7656904b8e6aa1bcc0d6
```

Sau đó, tích hợp bộ mã nguồn và cấu hình kiểm thử do nhóm bàn giao:
- `pom.xml`: Đã cấu hình plugin `pitest-maven:1.30.0` + `pitest-junit5-plugin:1.2.3`, nhóm toán tử `STRONGER`, cổng chất lượng `mutationThreshold=88`, `coverageThreshold=95`.
- 7 tệp kiểm thử mới trong `src/test/java/org/springframework/samples/petclinic/owner/`:
  1. `OwnerMutationTests.java` (27 tests)
  2. `PetValidatorMutationTests.java` (9 tests)
  3. `PetVisitModelMutationTests.java` (9 tests)
  4. `ControllerBinderMutationTests.java` (5 tests)
  5. `OwnerControllerMutationTests.java` (6 tests)
  6. `PetControllerMutationTests.java` (19 tests)
  7. `VisitControllerMutationTests.java` (6 tests)

---

## 3. Lệnh tái hiện nhanh 1-lệnh (One-liner Reproducibility)

Hội đồng chấm thi và giảng viên có thể copy-paste trực tiếp các lệnh dưới đây theo từng hệ điều hành:

### 3.1. Chạy trên Windows (PowerShell)

```powershell
# [MỨC 1] Chạy toàn bộ 153 Unit Tests của dự án (loại bỏ Docker Integration Tests)
.\mvnw.cmd test '-Dtest=!*IntegrationTests' '-DfailIfNoTests=false'
# Kỳ vọng: Tests run: 153, Failures: 0, Errors: 0, Skipped: 0, BUILD SUCCESS

# [MỨC 2] Chạy riêng 130 Unit Tests của gói nghiệp vụ cốt lõi 'owner'
.\mvnw.cmd test '-Dtest=org.springframework.samples.petclinic.owner.**'
# Kỳ vọng: Tests run: 130, Failures: 0, Errors: 0, Skipped: 0, BUILD SUCCESS (100% Pass)

# [MỨC 3] TÁI HIỆN MUTATION TESTING VỚI QUALITY GATE (LỆNH QUAN TRỌNG NHẤT)
.\mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true' '-DmutationThreshold=88' '-DcoverageThreshold=95'
# Kỳ vọng: Line Coverage 250/250 (100%), Generated 195 mutations Killed 192 (98%), BUILD SUCCESS
```

### 3.2. Chạy trên Linux / macOS (Bash)

```bash
# Phân quyền thực thi cho script wrapper (nếu cần)
chmod +x mvnw

# [MỨC 1] Chạy toàn bộ 153 Unit Tests của dự án (loại bỏ Docker Integration Tests)
./mvnw test -Dtest='!*IntegrationTests' -DfailIfNoTests=false
# Kỳ vọng: Tests run: 153, Failures: 0, Errors: 0, Skipped: 0, BUILD SUCCESS

# [MỨC 2] Chạy riêng 130 Unit Tests của gói nghiệp vụ cốt lõi 'owner'
./mvnw test -Dtest='org.springframework.samples.petclinic.owner.**'
# Kỳ vọng: Tests run: 130, Failures: 0, Errors: 0, Skipped: 0, BUILD SUCCESS (100% Pass)

# [MỨC 3] TÁI HIỆN MUTATION TESTING VỚI QUALITY GATE (LỆNH QUAN TRỌNG NHẤT)
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true -DmutationThreshold=88 -DcoverageThreshold=95
# Kỳ vọng: Line Coverage 250/250 (100%), Generated 195 mutations Killed 192 (98%), BUILD SUCCESS
```

> **Ghi chú kỹ thuật bắt buộc:**
> 1. Tham số `-Djacoco.skip=true` là **bắt buộc** để ngăn chặn xung đột bytecode instrumentation giữa Java Agent của JaCoCo và Coverage Minion của PIT.
> 2. Cổng chất lượng tự động (`Quality Gate`): Nếu điểm đột biến thực tế dưới 88% hoặc Line Coverage dưới 95%, tiến trình build của Maven sẽ lập tức bị hủy (`BUILD FAILURE`).

---

## 4. Báo cáo trực quan & Bảng tóm tắt kết quả thực nghiệm

### 4.1. Đường dẫn mở báo cáo trực quan
Sau khi thực thi lệnh Mức 3, toàn bộ kết quả phân tích được kết xuất trực quan:
- **Báo cáo HTML tổng hợp toàn gói:** `target/pit-reports/index.html` (Mở trực tiếp bằng trình duyệt Chrome, Edge hoặc Firefox).
- **Báo cáo HTML chi tiết từng lớp:** `target/pit-reports/org.springframework.samples.petclinic.owner/*.html`.
- **Dữ liệu thô máy đọc (Machine-readable XML):** `target/pit-reports/mutations.xml`.

### 4.2. Bảng tóm tắt kết quả thực nghiệm trước và sau tối ưu

| Tiêu chí đánh giá | Trước tối ưu (Baseline) | Sau tối ưu (Final) | Cổng chất lượng (Quality Gate) | Đánh giá học thuật |
|:---|:---:|:---:|:---:|:---:|
| **Line Coverage (Mutated Classes)** | 97% (242/250 dòng) | **100% (250/250 dòng)** | $\ge 95\%$ | 🟢 **Hoàn hảo (250/250)** |
| **Mutation Score** | **67%** (131/195 mutants) | **98%** (192/195 mutants) | $\ge 88\%$ | 🟢 **VƯỢT CHỈ TIÊU (+10%)** |
| **Đột biến sống sót (Survived)** | 64 mutants | **3 mutants** | 0 mutant không rõ nguyên nhân | 🟢 **Đã chứng minh Equivalent** |
| **Tỉ lệ diệt trên Mutant khả thi** | 70.4% (131/186) | **100% (192/192)** | $100\%$ | 🟢 **Tuyệt đối (192/192)** |
| **Số Unit Test gói `owner`** | 49 tests (6 tệp) | **130 tests** (13 tệp) | 100% Pass | 🟢 Tăng 81 tests |
| **Toàn bộ Unit Test dự án** | 79 pass, 2 error (Docker) | **153 pass, 0 fail, 0 error** | 100% Pass | 🟢 Đạt chuẩn CI/CD |

> **Về 03 đột biến sống sót:** Cả 3 mutant đều là **Equivalent Mutants** (đột biến tương đương về ngữ nghĩa), đã được nhóm chứng minh toán học và logic đầy đủ tại mục **D.4** và **G.4** trong `REPORT_R01_K03.md`. Không thể tiêu diệt bằng bất kỳ test case nào mà không thay đổi mã nguồn gốc.

---

## 5. Kiểm tra tự động qua đường ống CI/CD (GitHub Actions)

Dự án đã tích hợp quy trình kiểm thử tự động hóa toàn diện qua tệp cấu hình `.github/workflows/mutation-test.yml`.

### 5.1. Cơ chế kích hoạt (Triggers)
Đường ống CI/CD tự động kích hoạt khi:
- Tạo `Pull Request` vào nhánh `main`.
- Đẩy mã (`Push`) lên các nhánh: `main`, `feature/**`, `chore/**`, `docs/**`, `test/**`.
- Kích hoạt thủ công qua giao diện GitHub (`workflow_dispatch`).

### 5.2. Kiến trúc 6 bước Fail-Fast
1. **Checkout Source Code:** Lấy toàn bộ lịch sử commit (`actions/checkout@v4`).
2. **Set up JDK 17:** Khởi tạo OpenJDK Temurin 17 và bật Maven dependency caching (`actions/setup-java@v4`).
3. **Execute Full Unit Test Suite:** Chạy nhanh 153 unit test (`./mvnw test -Dtest='!*IntegrationTests'`). Nếu có bất kỳ test nào thất bại, build dừng ngay lập tức (Fail-Fast).
4. **Execute PIT Mutation Testing & Enforce Quality Gate:** Chạy kiểm thử đột biến với cờ `-DmutationThreshold=88 -DcoverageThreshold=95`. Build tự động FAIL nếu không đạt chỉ tiêu.
5. **Generate Summary Metrics on GitHub UI:** Tự động tạo bảng tổng hợp Markdown hiển thị trực tiếp trên tab Summary của GitHub Actions.
6. **Upload PIT HTML & XML Reports Artifact:** Đóng gói toàn bộ thư mục `target/pit-reports/` thành Artifact lưu trữ trong 30 ngày cho Hội đồng tải về thẩm định.

---

## 6. Chạy ứng dụng và kiểm chứng 03 luồng nghiệp vụ trên trình duyệt

```bash
# Khởi chạy ứng dụng (sử dụng cổng 8090 nếu cổng 8080 mặc định bị chiếm)
./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090
```

| Luồng | Endpoint kiểm tra | Kết quả kỳ vọng |
|:---|:---|:---|
| **1. Tìm kiếm chủ nuôi** | `GET http://localhost:8090/owners?lastName=Davis` | HTTP 200, hiển thị bảng danh sách `ownersList` |
| **2. Xem chi tiết chủ nuôi** | `GET http://localhost:8090/owners/1` | HTTP 200, trang `ownerDetails` với đầy đủ thông tin pet và visit |
| **3. Thêm mới thú cưng** | `GET http://localhost:8090/owners/1/pets/new` | HTTP 200, form `createOrUpdatePetForm` kèm PetValidator |
| **1b. Chuyển hướng trang ngoài biên** | `GET http://localhost:8090/owners?page=99&lastName=Davis` | HTTP 3xx Redirect về `page=1` theo đúng logic phân trang |

---

## 7. Bảng xử lý sự cố thường gặp (Troubleshooting)

| Sự cố | Nguyên nhân | Biện pháp xử lý |
|:---|:---|:---|
| `Coverage generation minion exited abnormally` | `pitest-junit5-plugin:1.2.1` cũ không hỗ trợ JUnit Platform 6.0.3 của Spring Boot 4 | Đảm bảo `pom.xml` sử dụng đúng `pitest-maven:1.30.0` và `pitest-junit5-plugin:1.2.3` |
| `Unknown lifecycle phase ".skip=true"` trên PowerShell | PowerShell hiểu nhầm dấu `.` trong `-Djacoco.skip=true` | Đặt toàn bộ tham số `-D` trong cặp dấu nháy đơn: `'-Djacoco.skip=true'` |
| `JAVA_HOME is not defined correctly` | Chưa cấu hình hoặc cấu hình sai biến môi trường `JAVA_HOME` | Thiết lập `JAVA_HOME` trỏ tới thư mục cài đặt JDK 17 và mở lại cửa sổ Terminal mới |
| `PostgresIntegrationTests` báo lỗi kết nối | Máy tính chưa khởi động Docker daemon | Bình thường và hợp lệ; các bài test Docker đã được loại trừ bằng cờ `-Dtest='!*IntegrationTests'` |
| `Port 8080 was already in use` | Cổng 8080 đang bị ứng dụng khác chiếm giữ | Thêm tham số `--server.port=8090` vào lệnh `spring-boot:run` |
