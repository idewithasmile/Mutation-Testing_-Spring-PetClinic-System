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
## E.1.1. Phạm vi, nguồn và trạng thái

SESSION S01, ngày 19/10/2026. Đối chiếu tại branch `personal`, HEAD `ab1cecc` trong workspace `Program/Mutation-Testing_-Spring-PetClinic-System`. Hai tài liệu TV3 chưa tồn tại trước S01; phiên này chỉ tạo tài liệu, không thay Java hoặc chạy Maven/PIT.

Nguồn phân công là `TaiLieuPhanCongCongViecNhom20.docx`; nguồn bàn giao là `HANDOVER_SESSION.md` (13/10, bổ sung 18/10), đều đã đọc từ thư mục `C:/Users/minht/Downloads/KiemThuPhanMem`. Bộ bổ sung ở `Program_R01-K03/Program_R01-K03` và bản `Mutation-Testing_-Spring-PetClinic-System-personal` có các assertion/JavaDoc mới nhưng chưa được tích hợp vào workspace này. Giữ cấu trúc E.1 và các mã TV3-O/V/M của bộ bàn giao; mọi mô tả hiện trạng dưới đây căn cứ vào code ở workspace hiện tại.

Các luật được suy ra từ source, không phải đặc tả nghiệp vụ độc lập do khách hàng cung cấp:

- [Owner.java](../../src/main/java/org/springframework/samples/petclinic/owner/Owner.java), [BaseEntity.java](../../src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java): pet mới khi id=null, các guard thêm/tìm pet và thêm visit.
- [PetValidator.java](../../src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java): MAX_NAME_LENGTH=30, required, isNew/type, birthDate và supports.
- [Pet.java](../../src/main/java/org/springframework/samples/petclinic/owner/Pet.java), [Visit.java](../../src/main/java/org/springframework/samples/petclinic/owner/Visit.java), [PetTypeFormatter.java](../../src/main/java/org/springframework/samples/petclinic/owner/PetTypeFormatter.java): trạng thái object, ngày mặc định và định dạng.

| Lớp test | Phân công | Methods hiện có | Parameterized/Repeated/Factory | Kết luận kiểm kê |
|---|---|---|---|---|
| OwnerMutationTests | 27 | 27 | 0 | VERIFIED về số lượng |
| PetValidatorMutationTests | 9 | 9 | 0 | VERIFIED về số lượng |
| PetVisitModelMutationTests | 9 | 9 | 0 | VERIFIED về số lượng |
| Tổng | 45 | 45 | 0 | Không đồng nghĩa 45 tests đã pass trong phiên |

Các lớp có `@DisabledInNativeImage`; số kiểm kê trên là methods JUnit, không phải số lần chạy trên mọi môi trường. Một method có thể kiểm tra nhiều giá trị. S01 không có kết quả runtime mới. Các báo cáo 45/153 pass, PIT 192/195 và line 250/250 ngày 18/10 thuộc lần chạy ở bản khác; không dùng chúng xác nhận assertions hoặc kết quả của workspace này.

Quy ước: `O01`, `V01`, `M01` viết tắt cho `TV3-O01`, `TV3-V01`, `TV3-M01`. Tên method, tiền điều kiện, input, expected, assertion thực tế và rủi ro của đủ 45 cases nằm trong [TEST_DESIGN_TV3.md](TEST_DESIGN_TV3.md). “Có assertion” là kiểm tra tĩnh, không phải PASS. “Dự kiến” là yêu cầu chưa được mã hóa, không thêm vào tổng 45 methods.

## E.1.2. Phân hoạch tương đương (EP)

| Chức năng/đầu vào | Partition | Đại diện | Kết quả theo source | Ca và mức kiểm chứng tĩnh |
|---|---|---|---|---|
| Validator.name | Không hợp lệ: null | null | name/required | V05: có lỗi; chưa assert code |
| Validator.name | Không hợp lệ: rỗng | "" | name/required | V03: có lỗi và code |
| Validator.name | Không hợp lệ: chỉ trắng | ba dấu cách | name/required | V04: có lỗi; chưa assert code |
| Validator.name | Hợp lệ: có chữ, dài ≤30 | A×29, A×30 | Không lỗi name | V01 chỉ có A×30; 29 dự kiến |
| Validator.name | Không hợp lệ: có chữ, dài >30 | A×31 | name/size | V02: có lỗi và code |
| Validator.type | Không hợp lệ đối với pet mới | id=null, type=null | type/required | V07: chưa assert code |
| Validator.type | Hợp lệ đối với pet đã lưu | id=42, type=null | Không lỗi type | V06 có assertion |
| Validator.type | Có type, pet mới/đã lưu | type=dog | Không lỗi type | V01/V08 có input, chưa assert kết quả type |
| Validator.birthDate | Không hợp lệ: thiếu | null, id=42 | birthDate/required | V08: có lỗi; chưa assert code |
| Validator.birthDate | Có ngày | 2015-02-12 | Không lỗi birthDate | Fixture V01–V07; chưa assert riêng birthDate |
| Validator.supports | Lớp được hỗ trợ | Pet, subclass Pet | true | V09 chỉ thử Pet; subclass dự kiến |
| Validator.supports | Lớp không được hỗ trợ | String | false | V09 |
| Owner.addPet | Bỏ qua null/trùng instance/trùng ID đã lưu | null; cùng pet; hai pet id=5 | Danh sách không tăng | O01/O03/O04/O05 |
| Owner.addPet | Pet được thêm | mới/ID khác; hai instance mới | Danh sách tăng | O02/O06–O09 |
| Owner.getPet(id) | ID tồn tại | 5 | Đúng instance | O10 |
| Owner.getPet(id) | ID không tồn tại/null | 42/null | null, không chọn pet mới | O11–O13 |
| Owner.getPet(name) | Tên khớp khác hoa/thường | buddy/BUDDY | Đúng instance nếu không bị ignoreNew loại | O14/O17–O19 |
| Owner.getPet(name) | Tên không khớp/tên pet null | Max/anything; pet.name=null | Bỏ pet không khớp; trả null khi không tìm được | O15/O16 |
| Owner.addVisit | ID null/không tồn tại/hợp lệ | null/404/7 | Ngoại lệ/ngoại lệ/gắn visit | O21/O23/O20 |
| Owner.addVisit | Visit null/khác null | null/Visit | Ngoại lệ/gắn visit nếu pet hợp lệ | O22/O20 |
| Formatter.print | Tên null/có giá trị | null/Hamster | "<null>"/"Hamster" | M06/M07; đối tượng type khác null |
| Formatter.parse | Tên tìm thấy/không có | Dog/Fish | Đúng instance/ParseException | M08/M09; M09 dùng repository rỗng |

Pet mới/cũ là trạng thái đầu vào, không tự nó là hợp lệ/không hợp lệ. Các luật name/type/birthDate độc lập: một pet có thể có nhiều lỗi. Không suy ra đã vét mọi Unicode/whitespace, đối số null của formatter hoặc mọi kích thước danh sách từ các đại diện này.

## E.1.3. Phân tích giá trị biên (BVA)

`PetValidator` khai báo `MAX_NAME_LENGTH=30`, kiểm tra `!StringUtils.hasText(name)` trước, rồi `name.length()>30`. Dùng A lặp để cô lập độ dài khỏi điều kiện whitespace.

| Biên | Input | Expected theo source | Mapping | Hiện trạng workspace |
|---|---|---|---|---|
| Tên tối đa 30 | A×29 | Không lỗi name; nếu các trường khác hợp lệ thì không lỗi nào | V01 dự kiến mở rộng | MISSING dữ liệu 29 |
| Tên tối đa 30 | A×30 | Không lỗi name | V01 | Có assertion name; chưa assert toàn bộ errors |
| Tên tối đa 30 | A×31 | name/size | V02 | Có assertion field và code |
| Visit ngày thường | today=2026-10-18 | default=2026-10-19 | M03 dự kiến | Chưa cố định today |
| Visit cuối năm | today=2026-12-31 | default=2027-01-01 | M03 dự kiến | MISSING |
| Visit trước ngày nhuận | today=2024-02-28 | default=2024-02-29 | M03 dự kiến | MISSING |

V01 ở 30 có thể phát hiện thay `>30` bằng `>=30` (ConditionalsBoundaryMutator): expected không lỗi nhưng mutant từ chối. Đây là phân tích mục tiêu, không phải bằng chứng PIT vừa ghi KILLED.

M03 hiện so `new Visit().getDate()` với `LocalDate.now().plusDays(1)`: hai lần đọc ngày có thể qua nửa đêm. Thiết kế bổ sung ở S04 dùng các ngày cố định trên; bộ bàn giao có cách static mock `LocalDate.now()` trong try-with-resources, giữ phép cộng ngày thật. S01 không áp dụng hoặc chạy cách đó. M05 chỉ kiểm tra set/get ngày cố định 2025-03-18, không thay thế kiểm tra ngày mặc định.

## E.1.4. Bảng quyết định Owner

### addPet

Dấu —: không cần xét do guard đã kết luận. “Cùng instance” dùng Pet chuẩn hiện tại; không giả định equals tùy biến của một subclass. Hàng A3–A9 xét pet thứ hai sau khi đã thêm pet đầu.

| Quy tắc | Pet thêm null | Cùng instance đã có | Pet trước mới | Pet thêm mới | ID bằng nhau | Hành động | Ca |
|---|---|---|---|---|---|---|---|
| A1 | Có | — | — | — | — | Không thêm, danh sách rỗng | O01 |
| A2 | Không | Không, danh sách rỗng | — | Có | — | Thêm đúng pet | O02 |
| A3 | Không | Có | Không | Không | Có | Không thêm lần hai | O03 |
| A4 | Không | Có | Có | Có | Có (null/null) | Không thêm lần hai | O04 |
| A5 | Không | Không | Không | Không | Có | Giữ instance đầu | O05 |
| A6 | Không | Không | Không | Không | Không | Thêm | O06 |
| A7 | Không | Không | Có | Có | Có (null/null) | Thêm | O07 |
| A8 | Không | Không | Không | Có | Không | Thêm | O08 |
| A9 | Không | Không | Có | Không | Không | Thêm | O09 |

Bất khả thi với Pet/BaseEntity hiện tại, tại cùng thời điểm: cùng instance nhưng hai ID khác nhau; cả hai mới nhưng ID khác nhau; một mới/một đã lưu nhưng ID bằng nhau. Đây là các quy tắc đại diện, không tuyên bố vét mọi chuỗi thao tác/danh sách.

O04 cô lập guard contains: vòng so ID không chặn hai pet mới. O03 không cô lập guard này vì ID đã lưu trùng cũng có thể chặn. Không sửa production để cố diệt những mutant được handover phân tích là tương đương.

### getPet(Integer)

Thực thi duyệt danh sách, bỏ pet mới, trả phần tử đã lưu đầu tiên có ID khớp; hết danh sách thì null.

| Quy tắc | Có pet đã lưu khớp ID | Input ID | Expected | Ca |
|---|---|---|---|---|
| I1 | Có | 5, danh sách gồm 5 và 6 | Đúng instance id=5 | O10 |
| I2 | Không | 42, danh sách chỉ có 5 | null | O11 |
| I3 | Không, chỉ có pet mới | 5 | null | O12 |
| I4 | Không thể có ID đã lưu bằng null | (Integer) null, có pet mới và id=5 | null | O13 |

### getPet(String[, boolean])

Bảng xét từng phần tử. “Tiếp tục” nghĩa là chỉ trả null sau khi không còn phần tử phù hợp. Overload một tham số tương đương `ignoreNew=false`.

| Quy tắc | Tên pet khác null | Khớp không phân biệt hoa/thường | ignoreNew | pet.isNew | Hành động | Ca |
|---|---|---|---|---|---|---|
| N1 | Không | — | — | — | Bỏ phần tử, tiếp tục | O16 |
| N2 | Có | Không | — | — | Bỏ phần tử, tiếp tục | O15/O16 |
| N3 | Có | Có | true | true | Bỏ pet mới, tiếp tục | O17 |
| N4 | Có | Có | bất kỳ | false | Trả đúng instance | O14 (false), O18 (true), O16 |
| N5 | Có | Có | false | true | Trả đúng instance | O19, gồm overload mặc định |

Các test hiện tại chưa thử input tên cần tìm null, cũng chưa thử nhiều phần tử cùng tên để assert thứ tự chọn. Không gán cho 45 cases các dữ liệu chưa có này.

### addVisit

| Quy tắc | petId khác null | visit khác null | getPet(petId) tìm thấy | Expected | Ca |
|---|---|---|---|---|---|
| AV1 | Không | — | — | IllegalArgumentException: Pet identifier must not be null! | O21 (visit khác null) |
| AV2 | Có | Không | — | IllegalArgumentException: Visit must not be null! | O22 |
| AV3 | Có | Có | Không | IllegalArgumentException: Invalid Pet identifier! | O23 |
| AV4 | Có | Có | Có | Gọi pet.addVisit; đúng visit nằm trong collection | O20 |

Guard petId chạy trước guard visit, rồi mới lookup pet. O21 chưa kiểm tra tình huống cả hai đối số đều null; dấu — diễn tả luật source, không khẳng định có test riêng cho mọi tổ hợp.

### toString và trạng thái Owner

`toString` không có if riêng để lập tổ hợp Boolean. Bảng quyết định đầu vào/đầu ra dưới đây ghi trạng thái có ý nghĩa; không dựng nhánh giả chỉ để gọi là Decision Table.

| Quy tắc | Điều kiện/đầu vào | Đầu ra source | Assertion hiện có | Ca |
|---|---|---|---|---|
| TS1 | Owner id=1, George Franklin, 110 W. Liberty St., Madison, 6085551023 | ToStringCreator chứa id/new/lastName/firstName/address/city/telephone | Chỉ contains Franklin, Madison, 6085551023; chưa kiểm tra bốn trường còn lại | O24 |
| TS2 | Owner mới, chưa gán trường | Giá trị new=true, các trường chưa gán là null trong biểu diễn | Chưa có case toString riêng | Ngoài 45 hiện có |
| ST1 | Owner mới chưa thêm pet | getPets rỗng | isEmpty | O25 |
| ST2 | Gán address/city/telephone | Getter trả đúng từng giá trị | Ba isEqualTo | O26 |

Không khóa định dạng toàn chuỗi hoặc identity hash của ToStringCreator. ST1/ST2 là kiểm tra trạng thái; không ép thành kỹ thuật BVA.

## E.1.5. Bảng quyết định PetValidator

| Quy tắc | isNew | type=null | Expected của trường type | Ca có input tương ứng | Assertion hiện có |
|---|---|---|---|---|---|
| V-T1 | true | true | type/required | V07 | Có lỗi type; thiếu assert required |
| V-T2 | true | false | Không lỗi type | V01 (và các fixture mới có type) | V01 chỉ assert name, thiếu kết quả type |
| V-T3 | false | true | Không lỗi type | V06 | Có assert không lỗi type |
| V-T4 | false | false | Không lỗi type | V08 | Chỉ assert birthDate; thiếu kết quả type |

V08 đồng thời thiếu birthDate, nên expected là birthDate/required **và** không lỗi type; không được gọi cả pet là hợp lệ.

| Luật độc lập | Điều kiện | Expected | Mapping/giới hạn |
|---|---|---|---|
| Tên bắt buộc | null/rỗng/blank | name/required | V03 đủ field/code; V04/V05 thiếu code |
| Độ dài | Có chữ và >30 | name/size | V02 |
| Ngày sinh | birthDate=null, bất kể isNew | birthDate/required | V08 thử pet đã lưu, thiếu code; chưa có case mới thiếu ngày trong ba lớp TV3 |
| Ngày sinh | birthDate có giá trị | Không lỗi birthDate | Có fixture, chưa assert riêng |
| supports | Pet hoặc subclass Pet | true | V09 chưa thử subclass |
| supports | String | false | V09 có assertion |

Validator chỉ kiểm tra birthDate khác null, không so với hôm nay; không tự thêm quy tắc cấm ngày tương lai. Các setter model không tự gọi Bean Validation.

## E.1.6. Pet, Visit và bốn kết quả formatter

| Quy tắc | Input/thao tác | Expected | Ca và giới hạn |
|---|---|---|---|
| M-P1 | Pet mới, addVisit(visit Checkup) | Collection chứa đúng visit | M01 dùng containsExactly, không chỉ non-null |
| M-P2 | Set type=cat, birthDate=2020-05-04 | Cùng instance type; đúng ngày | M02; không kiểm tra type=null |
| M-V1 | new Visit() tại ngày D | date=D+1 | M03; còn phụ thuộc đồng hồ thật |
| M-V2 | Set description/date | Đúng chuỗi/ngày được gán | M04/M05; không kiểm tra validation Controller |
| F1 | print(PetType name=null) | "<null>" | M06; PetType object không null |
| F2 | print(PetType name=Hamster) | "Hamster" | M07 |
| F3 | parse Dog, repository có object Dog | Chính object Dog | M08 |
| F4 | parse Fish, repository rỗng | ParseException, message "type not found: Fish", offset 0 | M09 chỉ assert loại exception |

Bốn kết quả formatter F1–F4 khác bốn tổ hợp Validator V-T1–V-T4. `parse` dùng Objects.equals, không có luật không phân biệt hoa/thường như Owner. Chưa có case parse null, repository có phần tử không khớp trước phần tử khớp, hoặc repository không rỗng nhưng không tìm thấy. Không nhận các trường hợp này là đã kiểm chứng.

“Deep assertion” ở đây nêu đúng mức quan sát: identity của type/visit, nội dung collection và giá trị ngày/chuỗi. Không khẳng định đã kiểm tra mọi field của object lồng nhau.

## E.1.7. Ánh xạ và GAP cho phiên tiếp theo

| Hạng mục | Hiện trạng sau S01 | Hành động sau S01 |
|---|---|---|
| Hai tài liệu thiết kế | Có EP/BVA/Decision Table và 45 đặc tả gắn method thật | Rà lại khi code đổi |
| JavaDoc mã case | MISSING trên cả 45 methods trong workspace | S02/S03/S04 gắn mã O/V/M; tham khảo bản bổ sung có sẵn |
| Owner logic chính | Có 27 methods, bao gồm transient contains/ID duplicate | S02 đối chiếu JavaDoc; không thêm test chỉ để tạo diff |
| BVA 29 | MISSING trong V01 | S03 bổ sung dữ liệu, không bắt buộc tăng số methods |
| required | V04/V05/V07/V08 INCOMPLETE | S03 assert đúng field và code |
| supports subclass | MISSING trong V09 | S03 bổ sung subclass Pet |
| isNew × type | Có input bốn tổ hợp, thiếu assertion kết quả V-T2/V-T4 | S03 bổ sung assertion V01/V08 |
| Ngày Visit cố định | M03 INCOMPLETE, nguy cơ qua nửa đêm | S04 bổ sung ngày thường/đổi năm/năm nhuận |
| Thực thi test/PIT hiện tại | Chưa chạy trong S01 | S06; không dùng lịch sử thay kết quả mới |
| Onboarding/Phần C | Chưa tạo trong workspace | S05, ngoài hai file được phép ở S01 |

Các giới hạn O24, M09 và lookup đã nêu là ranh giới assertion hiện tại, không mặc định yêu cầu mở rộng suite hoặc sửa production. Mỗi phiên sau chỉ xử lý GAP phù hợp phạm vi được giao. S01 hoàn tất về đặc tả; không kết luận việc triển khai hoặc kiểm chứng runtime của TV3 đã hoàn tất.
