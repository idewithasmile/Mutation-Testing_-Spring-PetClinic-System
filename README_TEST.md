# README_TEST — Hướng dẫn vận hành kiểm thử (R01 + K03)

Tài liệu vận hành cho giảng viên/người chấm: dựng môi trường, chạy test, chạy mutation testing
và đọc báo cáo. Báo cáo học thuật đầy đủ xem `REPORT_R01_K03.md`.

## 1. Yêu cầu môi trường

| Thành phần | Yêu cầu | Kiểm tra |
|---|---|---|
| JDK | 17 trở lên | `java -version` → `openjdk 17...` |
| `JAVA_HOME` | Trỏ tới JDK 17 | `echo %JAVA_HOME%` (Windows) |
| Git | bản mới | `git --version` |
| Internet | cần cho lần tải dependencies đầu tiên | — |
| Docker | **không bắt buộc** (chỉ dùng cho 2 lớp `*IntegrationTests`) | — |

> Không cần cài Maven rời: dùng wrapper `./mvnw` (Linux/macOS) hoặc `mvnw.cmd` (Windows).
> Đã kiểm chứng với Temurin 17.0.20.1 + Maven wrapper 3.9.16 + Spring Boot 4.1.0.

## 2. Dựng dự án (pin đúng commit)

```bash
git clone https://github.com/spring-projects/spring-petclinic.git Program_R01-K03
cd Program_R01-K03
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6
git rev-parse HEAD   # phải in: 500158f732419217507c7656904b8e6aa1bcc0d6
```

Sau đó chép các file bàn giao của nhóm vào đúng vị trí:

- `pom.xml` (đã tiêm plugin `pitest-maven` 1.30.0 + `pitest-junit5-plugin` 1.2.3,
  scope `org.springframework.samples.petclinic.owner.*`, mutator `STRONGER`)
- 7 file test mới trong `src/test/java/org/springframework/samples/petclinic/owner/`:
  `OwnerMutationTests`, `PetValidatorMutationTests`, `PetVisitModelMutationTests`,
  `ControllerBinderMutationTests`, `OwnerControllerMutationTests`,
  `PetControllerMutationTests`, `VisitControllerMutationTests`

## 3. Chạy kiểm thử (3 mức)

```bash
# Mức 1 — toàn bộ unit test (loại 2 lớp integration cần Docker):
./mvnw test -Dtest='!*IntegrationTests'
# Kỳ vọng: Tests run: 153, Failures: 0, Errors: 0, BUILD SUCCESS

# Mức 2 — riêng package đột biến:
./mvnw test -Dtest='org.springframework.samples.petclinic.owner.**'
# Kỳ vọng: 130/130 pass

# Mức 3 — MUTATION TESTING (1 lệnh tái hiện kết quả báo cáo):
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true
# Kỳ vọng: Generated 195 mutations Killed 192 (98%), Line Coverage 250/250 (100%)
```

> Windows PowerShell: đặt tham số `-D` trong dấu nháy đơn, ví dụ
> `./mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'`.
> `-Djacoco.skip=true` là bắt buộc để JaCoCo agent không xung đột với PIT minion.

## 4. Đọc báo cáo đột biến

- HTML tổng hợp: `target/pit-reports/index.html`
- Chi tiết từng class: `target/pit-reports/org.springframework.samples.petclinic.owner/*.html`
- Dữ liệu thô (máy đọc): `target/pit-reports/mutations.xml`
  (`status`: `KILLED` / `SURVIVED` / `NO_COVERAGE`; 3 `SURVIVED` còn lại là equivalent,
  đã chứng minh trong `REPORT_R01_K03.md` mục G.4)

## 5. Chạy ứng dụng & kiểm chứng 3 luồng nghiệp vụ

```bash
./mvnw spring-boot:run            # mặc định http://localhost:8080 (H2 + seed tự động)
```

| Luồng | URL kiểm chứng | Kỳ vọng |
|---|---|---|
| Tìm kiếm chủ nuôi | `GET /owners?lastName=Davis` | HTTP 200, trang `ownersList` |
| Chi tiết chủ nuôi | `GET /owners/1` | HTTP 200, trang `ownerDetails` |
| Form thêm thú cưng | `GET /owners/1/pets/new` | HTTP 200, trang `createOrUpdatePetForm` |

Nếu port 8080 bận: `./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090`.

## 6. Khắc phục sự cố thường gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Coverage generation minion exited abnormally` | plugin PIT 1.2.1 không hỗ trợ JUnit 6 của Spring Boot 4 | dùng đúng `pom.xml` bàn giao (PIT 1.30.0 + plugin 1.2.3) |
| `Unknown lifecycle phase ".skip=true"` (PowerShell) | `-D` bị tách tham số | đặt trong nháy đơn: `'-Djacoco.skip=true'` |
| `JAVA_HOME is not defined correctly` | wrapper không thấy JDK | đặt `JAVA_HOME` ở mức User/OS rồi mở terminal mới |
| `PostgresIntegrationTests` errors | thiếu Docker daemon | bỏ qua (đã loại khỏi gate): chạy với `-Dtest='!*IntegrationTests'` |
| `Port 8080 was already in use` | cổng bị chiếm | chạy với `--server.port=8090` như mục 5 |
| Lần đầu chạy lâu / tải dependencies | Maven central (~200 MB) | cần Internet ổn định cho lần đầu |

## 7. Quy ước chất lượng test

- Không sửa `src/main/java`; chỉ thêm test + cấu hình build.
- Test phải deterministic, nhanh, cô lập (thuần unit hoặc MockMvc, không gọi mạng/thời gian thực).
- Sau khi thêm/sửa test, chạy `./mvnw spring-javaformat:apply` để thống nhất format trước khi commit.
