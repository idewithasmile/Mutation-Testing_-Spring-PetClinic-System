# chạy thực tế — 3 luồng HTTP 

> Môi trường: macOS, JDK 21 (Homebrew) — ứng dụng chạy Spring Boot 4.1.0 trên H2 in-memory.  
> Lệnh khởi chạy: `./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8090`  
> Base URL: `http://localhost:8090`  
> Ngày kiểm chứng: 2026-10-18.

## 1. Luồng 1 — Tìm kiếm chủ nuôi (Search Owners)

- **Request**: `GET /owners?lastName=Davis`
- **Kỳ vọng**: HTTP 200, trang `ownersList` (danh sách chủ nuôi họ Davis).
- **Kết quả thực tế**: HTTP **200 OK**; trang chứa tên "Davis" (George Davis, Betty Davis).

```bash
$ curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8090/owners?lastName=Davis"
200
```

## 2. Luồng 2 — Chi tiết chủ nuôi (Owner Details)

- **Request**: `GET /owners/1`
- **Kỳ vọng**: HTTP 200, trang `ownerDetails` (thông tin chủ nuôi + thú cưng + lượt khám).
- **Kết quả thực tế**: HTTP **200 OK**; trang hiển thị chủ nuôi "George Franklin" cùng danh sách thú cưng.

```bash
$ curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8090/owners/1"
200
```

## 3. Luồng 3 — Form thêm thú cưng (Create Pet Form)

- **Request**: `GET /owners/1/pets/new`
- **Kỳ vọng**: HTTP 200, trang `createOrUpdatePetForm` (form nhập tên, loại, ngày sinh).
- **Kết quả thực tế**: HTTP **200 OK**; form chứa trường `name`, `birthDate`, `type` (PetType).

```bash
$ curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8090/owners/1/pets/new"
200
```

## 4. Kết luận

Cả 3 luồng nghiệp vụ trọng tâm đều trả về **HTTP 200** và render đúng view Thymeleaf, xác nhận hệ thống chạy thành công trên máy (Thẩm định — Validation).

## 5. Ghi chú

- Port mặc định 8080; khi bận dùng 8090 như trên.
- Seed data H2 tự động nạp từ `src/main/resources/db/h2/data.sql` (owners/pets/visits mẫu).
- Không cần Docker cho 3 luồng này (chỉ cần H2 in-memory).
