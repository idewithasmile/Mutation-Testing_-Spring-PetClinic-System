# Onboarding — Spring PetClinic (R01)

> Tài liệu dựng môi trường và chạy hệ thống từ máy sạch.  
> Chi tiết lệnh test/mutation xem `README_TEST.md`.

## 1. Yêu cầu môi trường

| Thành phần | Yêu cầu | Kiểm tra |
|---|---|---|
| JDK | 17 trở lên (đã kiểm chứng Temurin 17.0.20.1) | `java -version` |
| `JAVA_HOME` | Trỏ tới JDK 17 | `echo $JAVA_HOME` (macOS/Linux) / `echo %JAVA_HOME%` (Windows) |
| Git | bản mới | `git --version` |
| Maven | **không cần cài rời** — dùng wrapper `./mvnw` / `mvnw.cmd` | — |
| Docker | **không bắt buộc** (chỉ cho 2 lớp `*IntegrationTests`) | — |
| Internet | cần cho lần tải dependencies đầu tiên (~200 MB) | — |

## 2. Clone và pin commit

```bash
git clone https://github.com/spring-projects/spring-petclinic.git Program_R01-K03
cd Program_R01-K03
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6
git rev-parse HEAD   # phải in: 500158f732419217507c7656904b8e6aa1bcc0d6
```

Nếu dùng bản có sẵn mutation testing (commit nhóm `cba224f`), checkout nhánh `personal` và xác nhận `git log --oneline -1`.

## 3. Cấu hình & seed data

- DB mặc định: **H2 in-memory**, schema do `src/main/resources/db/h2/schema.sql`, seed do `src/main/resources/db/h2/data.sql`.
- JPA: `spring.jpa.hibernate.ddl-auto=none` (schema do SQL script).
- Seed data gồm: 6 vets, specialties, pet types (cat, dog, lizard, snake, bird, hamster), owners/pets/visits mẫu.
- Profile MySQL/PostgreSQL: `application-mysql.properties` / `application-postgres.properties` (cần Docker).

## 4. Chạy ứng dụng

```bash
# macOS/Linux
./mvnw spring-boot:run

# Windows
mvnw.cmd spring-boot:run
```

Mặc định http://localhost:8080. Nếu port bận:

```bash
./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090
```

## 5. Kiểm chứng 3 luồng nghiệp vụ

| Luồng | URL | Kỳ vọng |
|---|---|---|
| Tìm kiếm chủ nuôi | `GET /owners?lastName=Davis` | HTTP 200, trang `ownersList` |
| Chi tiết chủ nuôi | `GET /owners/1` | HTTP 200, trang `ownerDetails` |
| Form thêm thú cưng | `GET /owners/1/pets/new` | HTTP 200, trang `createOrUpdatePetForm` |

Chi tiết lệnh curl và log thực tế: `docs/live-http-validation.md`.

## 6. Build & test nhanh

```bash
# Toàn bộ unit test (loại 2 lớp integration cần Docker)
./mvnw test -Dtest='!*IntegrationTests'

# Riêng package owner
./mvnw test -Dtest='org.springframework.samples.petclinic.owner.**'

# Mutation testing (1 lệnh tái hiện)
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true
```

Kết quả kỳ vọng: `Tests run: 153, Failures: 0, Errors: 0, BUILD SUCCESS`; Mutation: `Generated 195 mutations Killed 192 (98%)`, `Line Coverage 250/250 (100%)`.

## 7. Khắc phục sự cố thường gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Coverage generation minion exited abnormally` | PIT 1.2.1 không hỗ trợ JUnit 6 | dùng `pom.xml` bàn giao (PIT 1.30.0 + plugin 1.2.3) |
| `Unknown lifecycle phase ".skip=true"` (PowerShell) | `-D` bị tách tham số | đặt trong nháy đơn `'-Djacoco.skip=true'` |
| `JAVA_HOME is not defined correctly` | wrapper không thấy JDK | đặt `JAVA_HOME` ở mức OS rồi mở terminal mới |
| `PostgresIntegrationTests` errors | thiếu Docker daemon | bỏ qua: `-Dtest='!*IntegrationTests'` |
| Port 8080 bận | cổng bị chiếm | chạy với `--server.port=8090` |
| Lần đầu chạy lâu | Maven central (~200 MB) | cần Internet ổn định |

## 8. Tham chiếu

- Kiến trúc & luồng dữ liệu: `docs/ARCHITECTURE.md`.
- Chứng cứ HTTP live: `docs/live-http-validation.md`.
- Báo cáo học thuật: `REPORT_R01_K03.md`.
- Lý thuyết kiểm thử: `THLYTHUYET.md`.
