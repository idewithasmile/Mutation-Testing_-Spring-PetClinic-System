# Phần E.1 — Thiết kế kiểm thử hộp đen Domain và Validator

## Phạm vi và trạng thái

Tài liệu này đặc tả ba lớp TV3 trong snapshot `589a505` ngày 19/10/2026:
`OwnerMutationTests` (27 methods), `PetValidatorMutationTests` (9 methods) và
`PetVisitModelMutationTests` (9 methods). Tổng 45 methods là số phương thức
JUnit, không phải một kết quả chạy. Kết quả thực thi S06 được ghi tại
[TV3_HANDOFF.md](TV3_HANDOFF.md) và report sinh ra ở `target/`.

Nguồn hành vi là `Owner`, `PetValidator`, `Pet`, `Visit`, `PetTypeFormatter`
và `BaseEntity` trong source. Các bảng mô tả hành vi observable của source,
không thêm quy tắc nghiệp vụ chưa có trong source.

## EP — phân hoạch tương đương

| Chức năng | Partition đầu vào | Expected theo source | Case |
|---|---|---|---|
| `PetValidator.name` | `null`, rỗng, chỉ trắng | lỗi `name` mã `required` | V03–V05 |
| `PetValidator.name` | có chữ, độ dài `<= 30` | không có lỗi `name` | V01; dữ liệu 29 là GAP |
| `PetValidator.name` | có chữ, độ dài `> 30` | lỗi `name` mã `size` | V02 |
| `PetValidator.type` | pet mới, `type=null` | lỗi `type` mã `required` | V07 |
| `PetValidator.type` | pet đã lưu, `type=null` | không có lỗi `type` | V06 |
| `PetValidator.birthDate` | `null`, bất kể `isNew` | lỗi `birthDate` mã `required` | V08 |
| `supports` | `Pet` hoặc subclass | `true` | V09; subclass là GAP |
| `supports` | lớp không phải `Pet` | `false` | V09 |
| `Owner.addPet` | `null`, cùng instance, ID persisted trùng | danh sách không tăng | O01, O03–O05 |
| `Owner.addPet` | instance mới hợp lệ, ID khác, hai transient khác instance | thêm pet | O02, O06–O09 |
| `Owner.getPet(id)` | ID persisted khớp / không khớp / pet mới | instance / `null` / `null` | O10–O13 |
| `Owner.getPet(name)` | tên khớp khác hoa-thường / không khớp / `name=null` | instance / `null` / bỏ phần tử | O14–O19 |
| `Owner.addVisit` | ID null, visit null, pet thiếu, hợp lệ | `IllegalArgumentException` / gắn visit | O20–O23 |
| Formatter | name type null/có giá trị; parse tìm thấy/không thấy | `<null>`/name; instance/`ParseException` | M06–M09 |

`isNew()` của `BaseEntity` là `id == null`. Trạng thái new/persisted là dữ liệu
đầu vào cho các luật type và owner, không tự là một lỗi validation.

## BVA — tên và ngày mặc định

`PetValidator` khai báo `MAX_NAME_LENGTH = 30` và kiểm tra `name.length() > 30`
sau kiểm tra `hasText`. Chuỗi `A` được lặp để cô lập độ dài khỏi whitespace.

| Biên | Input | Expected theo source | Tình trạng snapshot S07 |
|---|---|---|---|
| 29 | `A × 29` | không lỗi `name` | GAP: chưa có input/assertion riêng |
| 30 | `A × 30` | không lỗi `name` | V01 có assertion trường `name` |
| 31 | `A × 31` | `name/size` | V02 assert field và code |
| qua năm | today 2026-12-31 | default visit 2027-01-01 | GAP: test hiện dùng đồng hồ hệ thống |
| năm nhuận | today 2024-02-28 | default visit 2024-02-29 | GAP: test hiện dùng đồng hồ hệ thống |

Biên 30 nhằm phân biệt `> 30` với `>= 30`. Không gán BVA 29 là đã kiểm chứng
chỉ vì thiết kế có nêu nó. `Visit` khởi tạo `LocalDate.now().plusDays(1)`;
test hiện tại đọc `now()` hai lần nên có rủi ro qua nửa đêm.

## Decision Table — `Owner.addPet`

| Rule | pet null | cùng instance đã có | pet cũ/pet thêm mới | ID bằng nhau | Action | Case |
|---|---|---|---|---|---|---|
| A1 | có | — | — | — | không thêm | O01 |
| A2 | không | không, danh sách rỗng | — / mới | — | thêm đúng instance | O02 |
| A3 | không | có | cũ / cũ | có | không thêm lần hai | O03 |
| A4 | không | có | mới / mới | null/null | `contains` chặn | O04 |
| A5 | không | không | cũ / cũ | có | giữ instance đầu | O05 |
| A6 | không | không | cũ / cũ | không | thêm | O06 |
| A7 | không | không | mới / mới | null/null | thêm hai instance khác | O07 |
| A8 | không | không | cũ / mới | không | thêm | O08 |
| A9 | không | không | mới / cũ | không | thêm | O09 |

`contains` là guard riêng: O04 kiểm chứng transient cùng instance, trong khi
vòng lặp ID không chặn hai transient khác instance. Với `BaseEntity`, các tổ hợp
new/persisted có ID bằng nhau ngoài bảng là bất khả thi tại cùng thời điểm.

## Decision Table — lookup và visit

| Chức năng | Điều kiện | Expected | Case |
|---|---|---|---|
| `getPet(Integer)` | persisted ID khớp | đúng instance đầu tiên khớp | O10 |
| `getPet(Integer)` | vắng mặt, `null`, hoặc chỉ pet mới | `null` | O11–O13 |
| `getPet(String, true)` | khớp pet mới | bỏ pet mới | O17 |
| `getPet(String, true)` | khớp pet persisted | đúng instance | O18 |
| `getPet(String, false)` | khớp pet mới | đúng instance; overload mặc định | O19 |
| `addVisit` | petId/visit null, pet không có | exception với message source | O21–O23 |
| `addVisit` | persisted pet và visit hợp lệ | collection chứa đúng visit | O20 |
| `toString` | Owner đã gán trường | chuỗi chứa các field observable | O24 |

## Deep assertions Model và Formatter

| Hành vi | Expected quan sát được | Case / giới hạn hiện tại |
|---|---|---|
| `Pet.addVisit` | collection chứa chính instance `Visit` | M01 `containsExactly` |
| Pet type/birthDate | cùng instance type và ngày cố định | M02 |
| Visit description/date | round-trip đúng chuỗi/ngày | M04–M05 |
| `PetTypeFormatter.print` | name null thành `<null>`, name có giá trị giữ nguyên | M06–M07 |
| `PetTypeFormatter.parse` | object khớp trả cùng instance; không tìm thấy ném `ParseException` | M08–M09 |

M09 hiện chỉ khẳng định loại exception; message và offset là GAP. Những GAP này
không phải lý do tăng số method lên quá 45 hoặc sửa production.

## Liên kết 45 case

Input, expected, tiền điều kiện, method Java và rủi ro cho từng mã TV3-O01…O27,
TV3-V01…V09, TV3-M01…M09 nằm trong
[TEST_DESIGN_TV3.md](TEST_DESIGN_TV3.md).
