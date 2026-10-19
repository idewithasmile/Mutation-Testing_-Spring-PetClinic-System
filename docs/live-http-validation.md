# Chạy thực tế — 3 luồng HTTP (chi tiết & log đầy đủ)

> Môi trường kiểm chứng: macOS, JDK 21 (Homebrew Temurin-compatible), Spring Boot 4.1.0, H2 in-memory.  
> Lệnh khởi chạy: `./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090`  
> Base URL: `http://localhost:8090`  
> Ngày kiểm chứng: 2026-10-19.  
> Phạm vi: Member 2 (System Analyst & Environment / Live-HTTP Engineer) — Session 2.

## 0. Chuẩn bị & khởi động

```bash
$ java -version
openjdk version "21.0.12.1" 2026-08-18
OpenJDK Runtime Environment Homebrew (build 21.0.12.1)
OpenJDK 64-Bit Server VM Homebrew (build 21.0.12.1, mixed mode, sharing)

$ ./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090
...
2026-10-19T10:10:51.542+07:00  INFO ... Tomcat started on port 8090 (http) with context path '/'
2026-10-19T10:10:51.551+07:00  INFO ... Started PetClinicApplication in 4.344 seconds
```

Seed data H2 tự nạp từ `src/main/resources/db/h2/schema.sql` + `data.sql` (6 vets, pet types, owners/pets/visits mẫu).

## 1. Luồng 1 — Tìm kiếm chủ nuôi (Search Owners)

- **Request**: `GET /owners?lastName=Davis`
- **Kỳ vọng**: HTTP 200, view `ownersList`, danh sách chủ nuôi họ Davis.

```bash
$ curl -sS -D - -o /tmp/flow1.body -w "\nHTTP_CODE=%{http_code}\nTIME_TOTAL=%{time_total}s\nSIZE_DOWNLOAD=%{size_download}\n" \
  "http://localhost:8090/owners?lastName=Davis"

HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Language: en
Transfer-Encoding: chunked
Date: Mon, 19 Oct 2026 03:11:14 GMT

HTTP_CODE=200
TIME_TOTAL=0.526258s
SIZE_DOWNLOAD=3300
```

- **Kiểm tra nội dung**: body chứa "Davis" (George Davis, Betty Davis); `<title>PetClinic :: a Spring Framework demonstration`.
- **Kết luận**: **PASS** — HTTP 200, render đúng view `ownersList`.

## 2. Luồng 2 — Chi tiết chủ nuôi (Owner Details)

- **Request**: `GET /owners/1`
- **Kỳ vọng**: HTTP 200, view `ownerDetails` (thông tin chủ nuôi + thú cưng + lượt khám).

```bash
$ curl -sS -D - -o /tmp/flow2.body -w "\nHTTP_CODE=%{http_code}\nTIME_TOTAL=%{time_total}s\nSIZE_DOWNLOAD=%{size_download}\n" \
  "http://localhost:8090/owners/1"

HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Language: en
Transfer-Encoding: chunked
Date: Mon, 19 Oct 2026 03:11:14 GMT

HTTP_CODE=200
TIME_TOTAL=0.046588s
SIZE_DOWNLOAD=4180
```

- **Kiểm tra nội dung**: body chứa "George Franklin"; `<title>PetClinic :: a Spring Framework demonstration`.
- **Kết luận**: **PASS** — HTTP 200, render đúng view `ownerDetails`.

## 3. Luồng 3 — Form thêm thú cưng (Create Pet Form)

- **Request**: `GET /owners/1/pets/new`
- **Kỳ vọng**: HTTP 200, view `createOrUpdatePetForm` (form nhập tên, loại, ngày sinh).

```bash
$ curl -sS -D - -o /tmp/flow3.body -w "\nHTTP_CODE=%{http_code}\nTIME_TOTAL=%{time_total}s\nSIZE_DOWNLOAD=%{size_download}\n" \
  "http://localhost:8090/owners/1/pets/new"

HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Language: en
Transfer-Encoding: chunked
Date: Mon, 19 Oct 2026 03:11:14 GMT

HTTP_CODE=200
TIME_TOTAL=0.065327s
SIZE_DOWNLOAD=4499
```

- **Kiểm tra nội dung**: body chứa "birthDate" và "George Franklin"; `<title>PetClinic :: a Spring Framework demonstration`.
- **Kết luận**: **PASS** — HTTP 200, render đúng view `createOrUpdatePetForm`.

## 4. Tổng kết

| Luồng | URL | HTTP | View kỳ vọng | Kết quả | Thời gian | Kích thước |
|---|---|---|---|---|---|---|
| 1 | `/owners?lastName=Davis` | 200 | `ownersList` | PASS | 0.526s | 3300 B |
| 2 | `/owners/1` | 200 | `ownerDetails` | PASS | 0.047s | 4180 B |
| 3 | `/owners/1/pets/new` | 200 | `createOrUpdatePetForm` | PASS | 0.065s | 4499 B |

Cả 3 luồng nghiệp vụ trọng tâm đều trả về **HTTP 200** và render đúng view Thymeleaf, xác nhận hệ thống chạy thành công trên máy (Thẩm định — Validation). Không cần Docker (chỉ H2 in-memory).

## 5. Ghi chú & khắc phục sự cố

- Port mặc định 8080; khi bận dùng 8090 như trên (`--server.port=8090`).
- Seed data H2 tự nạp từ `src/main/resources/db/h2/data.sql` (owners/pets/visits mẫu).
- Nếu `mvnw` chậm lần đầu do tải dependencies (~200 MB) → cần Internet ổn định.
- Dừng ứng dụng: `Ctrl+C` hoặc `pkill -f spring-boot:run`.
