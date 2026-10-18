# Đặc tả và ánh xạ 45 test của Thành viên 3

## Phạm vi và cách đọc

SESSION S01 — 19/10/2026, branch `personal`, HEAD `ab1cecc`. Đây là đặc tả đối chiếu **code hiện có trong workspace**, không phải bản sao kết quả PASS của bản bổ sung 18/10 ở thư mục khác. Phiên này không chạy test/PIT và không sửa Java.

Tham khảo [bảng EP/BVA/Decision Table](DESIGN_TABLES.md). Các mã giữ theo bộ bàn giao: TV3-O01–O27, TV3-V01–V09, TV3-M01–M09. 45 mã ánh xạ một-một tới 45 methods `@Test`; không có `@ParameterizedTest`, `@RepeatedTest` hay `@TestFactory` trong ba lớp. Các lớp bị disable trong native image. Không coi số methods là số lần chạy hoặc số tổ hợp dữ liệu.

| Nhóm | File test | Methods phân công/hiện có | Mã |
|---|---|---|---|
| Owner | [OwnerMutationTests.java](../../src/test/java/org/springframework/samples/petclinic/owner/OwnerMutationTests.java) | 27/27 | TV3-O01–O27 |
| Validator | [PetValidatorMutationTests.java](../../src/test/java/org/springframework/samples/petclinic/owner/PetValidatorMutationTests.java) | 9/9 | TV3-V01–V09 |
| Model/Formatter | [PetVisitModelMutationTests.java](../../src/test/java/org/springframework/samples/petclinic/owner/PetVisitModelMutationTests.java) | 9/9 | TV3-M01–M09 |

**Trạng thái chung của mọi case:** đã đọc source/test; chưa chạy trong S01. Chưa có JavaDoc chứa ID từng case trong ba file hiện tại; các ID dưới đây là ánh xạ tài liệu để S02–S04 bổ sung. Mục “Assertion hiện có/GAP” mô tả chính xác điều test đang kiểm tra; một tên method có chữ RequiredCode hoặc Subclasses không tự chứng minh assertion tương ứng đã tồn tại.

**Cơ sở expected:** source được liên kết trong DESIGN_TABLES, không giả định requirements ngoài code. Mục rủi ro là phân tích thiết kế; không gán killingTest, số mutant hay trạng thái KILLED nếu chưa đối chiếu report phù hợp với phiên chạy và revision. Không suy diễn mỗi test phải giết được một mutant riêng.

Fixture Validator mặc định: `Pet` id=null, name=Buddy, type là `PetType` có name=dog, birthDate=2015-02-12; mỗi test nhận `PetValidator` và `MapBindingResult` mới qua `@BeforeEach`. Các thay đổi từng case được nêu riêng. Fixture formatter: repository mock `PetTypeRepository`, formatter mới qua `@BeforeEach`, Locale.ENGLISH. Chỉ mock repository, không truy cập DB/mạng.

## Danh mục ánh xạ

| ID | Lớp.method | Chức năng | Kỹ thuật |
|---|---|---|---|
| TV3-O01 | `OwnerMutationTests.addPetIgnoresNull` | Owner.addPet | EP — pet null |
| TV3-O02 | `OwnerMutationTests.addPetAddsNewPet` | Owner.addPet | Decision Table A2 |
| TV3-O03 | `OwnerMutationTests.addPetRejectsSameInstanceTwice` | Owner.addPet | Decision Table A3 |
| TV3-O04 | `OwnerMutationTests.addPetRejectsSameNewInstanceTwice` | Owner.addPet | Decision Table A4 |
| TV3-O05 | `OwnerMutationTests.addPetRejectsDifferentInstanceWithSameId` | Owner.addPet | Decision Table A5 |
| TV3-O06 | `OwnerMutationTests.addPetAllowsDifferentIds` | Owner.addPet | Decision Table A6 |
| TV3-O07 | `OwnerMutationTests.addPetAllowsTwoNewPets` | Owner.addPet | Decision Table A7 |
| TV3-O08 | `OwnerMutationTests.addPetAllowsNewPetAlongsidePersistedPet` | Owner.addPet | Decision Table A8 |
| TV3-O09 | `OwnerMutationTests.addPetAllowsPersistedPetAfterNewPet` | Owner.addPet | Decision Table A9 |
| TV3-O10 | `OwnerMutationTests.getPetByIdReturnsMatchingPet` | Owner.getPet(Integer) | EP — ID tồn tại; I1 |
| TV3-O11 | `OwnerMutationTests.getPetByIdReturnsNullWhenAbsent` | Owner.getPet(Integer) | EP — ID không tồn tại; I2 |
| TV3-O12 | `OwnerMutationTests.getPetByIdSkipsNewPets` | Owner.getPet(Integer) | EP — pet mới; I3 |
| TV3-O13 | `OwnerMutationTests.getPetByIdWithNullIdReturnsNull` | Owner.getPet(Integer) | EP — ID null; I4 |
| TV3-O14 | `OwnerMutationTests.getPetByNameIsCaseInsensitive` | Owner.getPet(String) | EP — khớp khác hoa/thường; N4 |
| TV3-O15 | `OwnerMutationTests.getPetByNameReturnsNullWhenAbsent` | Owner.getPet(String) | EP — tên không tồn tại; N2 |
| TV3-O16 | `OwnerMutationTests.getPetByNameSkipsPetsWithNullName` | Owner.getPet(String) | EP — tên pet null; N1/N2/N4 |
| TV3-O17 | `OwnerMutationTests.getPetByNameWithIgnoreNewSkipsNewPet` | Owner.getPet(String,boolean) | Decision Table N3 |
| TV3-O18 | `OwnerMutationTests.getPetByNameWithIgnoreNewReturnsPersistedPet` | Owner.getPet(String,boolean) | Decision Table N4 |
| TV3-O19 | `OwnerMutationTests.getPetByNameWithoutIgnoreNewReturnsNewPet` | Owner.getPet(String,boolean) và overload mặc định | Decision Table N5 |
| TV3-O20 | `OwnerMutationTests.addVisitDelegatesToPet` | Owner.addVisit | Decision Table AV4; kiểm tra trạng thái |
| TV3-O21 | `OwnerMutationTests.addVisitRejectsNullPetId` | Owner.addVisit | EP — null; Decision Table AV1 |
| TV3-O22 | `OwnerMutationTests.addVisitRejectsNullVisit` | Owner.addVisit | EP — null; Decision Table AV2 |
| TV3-O23 | `OwnerMutationTests.addVisitRejectsUnknownPetId` | Owner.addVisit | EP — ID không tồn tại; Decision Table AV3 |
| TV3-O24 | `OwnerMutationTests.toStringContainsKeyFields` | Owner.toString | Kiểm tra đầu ra; bảng TS1 |
| TV3-O25 | `OwnerMutationTests.getPetsStartsEmpty` | Owner.getPets | EP — trạng thái khởi tạo |
| TV3-O26 | `OwnerMutationTests.getAddressCityTelephoneRoundTrip` | Owner accessors | Kiểm tra trạng thái |
| TV3-O27 | `OwnerMutationTests.birthDateHelperAcceptsLocalDate` | Pet birthDate accessors | Kiểm tra trạng thái |
| TV3-V01 | `PetValidatorMutationTests.nameExactlyAtMaxLengthIsAccepted` | PetValidator.validate — tên hợp lệ | BVA; V-T2 |
| TV3-V02 | `PetValidatorMutationTests.nameOneOverMaxLengthIsRejectedWithSizeCode` | PetValidator.validate — tên quá dài | BVA |
| TV3-V03 | `PetValidatorMutationTests.emptyNameIsRejectedWithRequiredCode` | PetValidator.validate — tên rỗng | EP — không hợp lệ |
| TV3-V04 | `PetValidatorMutationTests.blankNameIsRejectedWithRequiredCode` | PetValidator.validate — tên trắng | EP — không hợp lệ |
| TV3-V05 | `PetValidatorMutationTests.nullNameIsRejectedWithRequiredCode` | PetValidator.validate — tên null | EP — không hợp lệ |
| TV3-V06 | `PetValidatorMutationTests.persistedPetWithoutTypeIsAccepted` | PetValidator.validate — type | Decision Table V-T3 |
| TV3-V07 | `PetValidatorMutationTests.newPetWithoutTypeIsRejected` | PetValidator.validate — type | Decision Table V-T1 |
| TV3-V08 | `PetValidatorMutationTests.persistedPetWithoutBirthDateIsStillRejected` | PetValidator.validate — birthDate/type | EP — thiếu ngày; Decision Table V-T4 |
| TV3-V09 | `PetValidatorMutationTests.supportsPetAndSubclassesOnly` | PetValidator.supports | EP — lớp được/không được hỗ trợ |
| TV3-M01 | `PetVisitModelMutationTests.petAddVisitStoresVisit` | Pet.addVisit/getVisits | Kiểm tra trạng thái |
| TV3-M02 | `PetVisitModelMutationTests.petTypeAndBirthDateRoundTrip` | Pet type/birthDate accessors | Kiểm tra trạng thái |
| TV3-M03 | `PetVisitModelMutationTests.visitDefaultsToTomorrow` | Visit constructor/getDate | Kiểm tra trạng thái; BVA ngày dự kiến |
| TV3-M04 | `PetVisitModelMutationTests.visitDescriptionRoundTrip` | Visit description accessors | Kiểm tra trạng thái |
| TV3-M05 | `PetVisitModelMutationTests.visitDateRoundTrip` | Visit date accessors | Kiểm tra trạng thái |
| TV3-M06 | `PetVisitModelMutationTests.formatterPrintsNullNameAsPlaceholder` | PetTypeFormatter.print | EP — tên type null; F1 |
| TV3-M07 | `PetVisitModelMutationTests.formatterPrintsConfiguredName` | PetTypeFormatter.print | EP — tên type có giá trị; F2 |
| TV3-M08 | `PetVisitModelMutationTests.formatterParsesKnownType` | PetTypeFormatter.parse | EP — tên có trong repository; F3 |
| TV3-M09 | `PetVisitModelMutationTests.formatterRejectsUnknownType` | PetTypeFormatter.parse | EP — tên không có; F4 |

## Đặc tả chi tiết

Expected rộng hơn assertion ở một số case được ghi rõ là GAP; không coi phần chưa assert là đã được test bảo vệ. Các input dự kiến như 29 ký tự/subclass/ngày cố định không được nhập vào mô tả input hiện có.

### TV3-O01 — addPetIgnoresNull

- **Chức năng/kỹ thuật:** Owner.addPet; EP — pet null.
- **Tiền điều kiện:** Owner mới, danh sách rỗng.
- **Input và bước thực hiện:** pet=null; gọi addPet(null).
- **Expected theo source:** Danh sách pets vẫn rỗng.
- **Assertion hiện có/GAP:** isEmpty() trên getPets().
- **Java method:** `OwnerMutationTests.addPetIgnoresNull`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ guard null có thể đưa null vào danh sách hoặc gây lỗi.

### TV3-O02 — addPetAddsNewPet

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A2.
- **Tiền điều kiện:** Owner mới; Pet Buddy mới (id=null).
- **Input và bước thực hiện:** Gọi addPet(Buddy).
- **Expected theo source:** Danh sách chứa đúng instance Buddy.
- **Assertion hiện có/GAP:** containsExactly(pet).
- **Java method:** `OwnerMutationTests.addPetAddsNewPet`.
- **Rủi ro/mục tiêu thiết kế:** Mất thao tác thêm pet hoặc trả về sớm sai.

### TV3-O03 — addPetRejectsSameInstanceTwice

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A3.
- **Tiền điều kiện:** Owner mới; một instance Buddy có id=5.
- **Input và bước thực hiện:** Thêm cùng instance hai lần.
- **Expected theo source:** Chỉ có một pet trong danh sách.
- **Assertion hiện có/GAP:** hasSize(1).
- **Java method:** `OwnerMutationTests.addPetRejectsSameInstanceTwice`.
- **Rủi ro/mục tiêu thiết kế:** Thêm lặp cùng pet đã lưu; ca này không cô lập guard contains vì guard ID cũng có thể ngăn trùng.

### TV3-O04 — addPetRejectsSameNewInstanceTwice

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A4.
- **Tiền điều kiện:** Owner mới; một instance Buddy có id=null.
- **Input và bước thực hiện:** Thêm cùng instance hai lần.
- **Expected theo source:** Chỉ có một pet trong danh sách.
- **Assertion hiện có/GAP:** hasSize(1).
- **Java method:** `OwnerMutationTests.addPetRejectsSameNewInstanceTwice`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ guard contains: hai ID null không được guard pet đã lưu chặn; danh sách có thể tăng thành 2.

### TV3-O05 — addPetRejectsDifferentInstanceWithSameId

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A5.
- **Tiền điều kiện:** Owner mới; hai instance khác nhau: first=(5,Buddy), second=(5,Max).
- **Input và bước thực hiện:** Thêm first rồi second.
- **Expected theo source:** Chỉ giữ đúng first.
- **Assertion hiện có/GAP:** containsExactly(first).
- **Java method:** `OwnerMutationTests.addPetRejectsDifferentInstanceWithSameId`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ so sánh ID trùng hoặc giữ nhầm instance.

### TV3-O06 — addPetAllowsDifferentIds

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A6.
- **Tiền điều kiện:** Owner mới; hai instance đã lưu khác ID.
- **Input và bước thực hiện:** Thêm (5,Buddy), rồi (6,Max).
- **Expected theo source:** Danh sách có 2 pet.
- **Assertion hiện có/GAP:** hasSize(2); chưa assert nội dung từng phần tử.
- **Java method:** `OwnerMutationTests.addPetAllowsDifferentIds`.
- **Rủi ro/mục tiêu thiết kế:** Từ chối nhầm pet khác ID.

### TV3-O07 — addPetAllowsTwoNewPets

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A7.
- **Tiền điều kiện:** Owner mới; hai instance mới khác nhau, đều id=null.
- **Input và bước thực hiện:** Thêm Buddy rồi Max.
- **Expected theo source:** Danh sách có 2 pet mới.
- **Assertion hiện có/GAP:** hasSize(2); chưa assert nội dung từng phần tử.
- **Java method:** `OwnerMutationTests.addPetAllowsTwoNewPets`.
- **Rủi ro/mục tiêu thiết kế:** Coi hai ID null là cùng pet và từ chối pet thứ hai.

### TV3-O08 — addPetAllowsNewPetAlongsidePersistedPet

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A8.
- **Tiền điều kiện:** Owner mới; pet đã lưu và pet mới khác instance.
- **Input và bước thực hiện:** Thêm (5,Buddy), rồi (null,Max).
- **Expected theo source:** Danh sách có 2 pet.
- **Assertion hiện có/GAP:** hasSize(2).
- **Java method:** `OwnerMutationTests.addPetAllowsNewPetAlongsidePersistedPet`.
- **Rủi ro/mục tiêu thiết kế:** Từ chối sai pet mới sau pet đã lưu.

### TV3-O09 — addPetAllowsPersistedPetAfterNewPet

- **Chức năng/kỹ thuật:** Owner.addPet; Decision Table A9.
- **Tiền điều kiện:** Owner mới; pet mới và pet đã lưu khác instance.
- **Input và bước thực hiện:** Thêm (null,Max), rồi (5,Buddy).
- **Expected theo source:** Danh sách có 2 pet.
- **Assertion hiện có/GAP:** hasSize(2).
- **Java method:** `OwnerMutationTests.addPetAllowsPersistedPetAfterNewPet`.
- **Rủi ro/mục tiêu thiết kế:** Phụ thuộc sai vào thứ tự pet mới/pet đã lưu.

### TV3-O10 — getPetByIdReturnsMatchingPet

- **Chức năng/kỹ thuật:** Owner.getPet(Integer); EP — ID tồn tại; I1.
- **Tiền điều kiện:** Owner chứa Buddy id=5 và Max id=6.
- **Input và bước thực hiện:** Gọi getPet(5).
- **Expected theo source:** Trả đúng instance Buddy.
- **Assertion hiện có/GAP:** isSameAs(buddy).
- **Java method:** `OwnerMutationTests.getPetByIdReturnsMatchingPet`.
- **Rủi ro/mục tiêu thiết kế:** Trả null hoặc chọn sai pet khi ID khớp.

### TV3-O11 — getPetByIdReturnsNullWhenAbsent

- **Chức năng/kỹ thuật:** Owner.getPet(Integer); EP — ID không tồn tại; I2.
- **Tiền điều kiện:** Owner chỉ chứa Buddy id=5.
- **Input và bước thực hiện:** Gọi getPet(42).
- **Expected theo source:** Trả null.
- **Assertion hiện có/GAP:** isNull().
- **Java method:** `OwnerMutationTests.getPetByIdReturnsNullWhenAbsent`.
- **Rủi ro/mục tiêu thiết kế:** Trả pet đầu tiên dù ID không khớp.

### TV3-O12 — getPetByIdSkipsNewPets

- **Chức năng/kỹ thuật:** Owner.getPet(Integer); EP — pet mới; I3.
- **Tiền điều kiện:** Owner chỉ chứa Buddy id=null.
- **Input và bước thực hiện:** Gọi getPet(5).
- **Expected theo source:** Trả null.
- **Assertion hiện có/GAP:** isNull().
- **Java method:** `OwnerMutationTests.getPetByIdSkipsNewPets`.
- **Rủi ro/mục tiêu thiết kế:** Chọn nhầm pet transient; riêng dữ liệu này không đảm bảo phát hiện mọi thay đổi guard isNew.

### TV3-O13 — getPetByIdWithNullIdReturnsNull

- **Chức năng/kỹ thuật:** Owner.getPet(Integer); EP — ID null; I4.
- **Tiền điều kiện:** Owner chứa Buddy id=null và Max id=5.
- **Input và bước thực hiện:** Gọi getPet((Integer) null).
- **Expected theo source:** Trả null; không chọn Buddy mới.
- **Assertion hiện có/GAP:** isNull().
- **Java method:** `OwnerMutationTests.getPetByIdWithNullIdReturnsNull`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ guard isNew có thể làm Objects.equals(null,null) chọn pet mới.

### TV3-O14 — getPetByNameIsCaseInsensitive

- **Chức năng/kỹ thuật:** Owner.getPet(String); EP — khớp khác hoa/thường; N4.
- **Tiền điều kiện:** Owner chứa Buddy id=5.
- **Input và bước thực hiện:** Gọi getPet("buddy"), getPet("BUDDY").
- **Expected theo source:** Cả hai trả đúng instance Buddy.
- **Assertion hiện có/GAP:** Hai assertion isSameAs(buddy).
- **Java method:** `OwnerMutationTests.getPetByNameIsCaseInsensitive`.
- **Rủi ro/mục tiêu thiết kế:** So sánh sai hoa/thường hoặc trả sai instance.

### TV3-O15 — getPetByNameReturnsNullWhenAbsent

- **Chức năng/kỹ thuật:** Owner.getPet(String); EP — tên không tồn tại; N2.
- **Tiền điều kiện:** Owner chỉ chứa Buddy id=5.
- **Input và bước thực hiện:** Gọi getPet("Max").
- **Expected theo source:** Trả null.
- **Assertion hiện có/GAP:** isNull().
- **Java method:** `OwnerMutationTests.getPetByNameReturnsNullWhenAbsent`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ điều kiện so tên.

### TV3-O16 — getPetByNameSkipsPetsWithNullName

- **Chức năng/kỹ thuật:** Owner.getPet(String); EP — tên pet null; N1/N2/N4.
- **Tiền điều kiện:** Owner chứa pet id=7, name=null trước Buddy id=5.
- **Input và bước thực hiện:** Gọi getPet("Buddy"), rồi getPet("anything").
- **Expected theo source:** Trả đúng Buddy cho lần đầu; null cho lần sau, không phát sinh lỗi do tên null.
- **Assertion hiện có/GAP:** isSameAs(buddy) và isNull().
- **Java method:** `OwnerMutationTests.getPetByNameSkipsPetsWithNullName`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ kiểm tra compName null gây NullPointerException; dừng tìm quá sớm.

### TV3-O17 — getPetByNameWithIgnoreNewSkipsNewPet

- **Chức năng/kỹ thuật:** Owner.getPet(String,boolean); Decision Table N3.
- **Tiền điều kiện:** Owner chứa Rex mới (id=null).
- **Input và bước thực hiện:** Gọi getPet("Rex",true).
- **Expected theo source:** Trả null.
- **Assertion hiện có/GAP:** isNull().
- **Java method:** `OwnerMutationTests.getPetByNameWithIgnoreNewSkipsNewPet`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ qua ignoreNew và trả pet mới.

### TV3-O18 — getPetByNameWithIgnoreNewReturnsPersistedPet

- **Chức năng/kỹ thuật:** Owner.getPet(String,boolean); Decision Table N4.
- **Tiền điều kiện:** Owner chứa Rex id=8.
- **Input và bước thực hiện:** Gọi getPet("Rex",true).
- **Expected theo source:** Trả đúng Rex.
- **Assertion hiện có/GAP:** isSameAs(rex).
- **Java method:** `OwnerMutationTests.getPetByNameWithIgnoreNewReturnsPersistedPet`.
- **Rủi ro/mục tiêu thiết kế:** Loại cả pet đã lưu khi ignoreNew=true.

### TV3-O19 — getPetByNameWithoutIgnoreNewReturnsNewPet

- **Chức năng/kỹ thuật:** Owner.getPet(String,boolean) và overload mặc định; Decision Table N5.
- **Tiền điều kiện:** Owner chứa Rex mới (id=null).
- **Input và bước thực hiện:** Gọi getPet("Rex",false) và getPet("Rex").
- **Expected theo source:** Cả hai trả đúng Rex; overload mặc định dùng ignoreNew=false.
- **Assertion hiện có/GAP:** Hai assertion isSameAs(rex).
- **Java method:** `OwnerMutationTests.getPetByNameWithoutIgnoreNewReturnsNewPet`.
- **Rủi ro/mục tiêu thiết kế:** Đổi giá trị mặc định ignoreNew hoặc loại pet mới vô điều kiện.

### TV3-O20 — addVisitDelegatesToPet

- **Chức năng/kỹ thuật:** Owner.addVisit; Decision Table AV4; kiểm tra trạng thái.
- **Tiền điều kiện:** Owner chứa Buddy id=7; Visit có description="Annual checkup".
- **Input và bước thực hiện:** Gọi addVisit(7,visit).
- **Expected theo source:** Collection visits của Buddy chứa đúng visit.
- **Assertion hiện có/GAP:** containsExactly(visit); kiểm tra identity qua equals mặc định, không assert lại description.
- **Java method:** `OwnerMutationTests.addVisitDelegatesToPet`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ lời gọi pet.addVisit hoặc gắn sai pet.

### TV3-O21 — addVisitRejectsNullPetId

- **Chức năng/kỹ thuật:** Owner.addVisit; EP — null; Decision Table AV1.
- **Tiền điều kiện:** Owner mới; một Visit khác null.
- **Input và bước thực hiện:** Gọi addVisit(null,new Visit()).
- **Expected theo source:** IllegalArgumentException, message="Pet identifier must not be null!".
- **Assertion hiện có/GAP:** assertThatThrownBy kiểm tra loại và message chính xác.
- **Java method:** `OwnerMutationTests.addVisitRejectsNullPetId`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ guard petId hoặc báo sai lỗi.

### TV3-O22 — addVisitRejectsNullVisit

- **Chức năng/kỹ thuật:** Owner.addVisit; EP — null; Decision Table AV2.
- **Tiền điều kiện:** Owner chứa Buddy id=7.
- **Input và bước thực hiện:** Gọi addVisit(7,null).
- **Expected theo source:** IllegalArgumentException, message="Visit must not be null!".
- **Assertion hiện có/GAP:** assertThatThrownBy kiểm tra loại và message chính xác.
- **Java method:** `OwnerMutationTests.addVisitRejectsNullVisit`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ guard visit hoặc chấp nhận null.

### TV3-O23 — addVisitRejectsUnknownPetId

- **Chức năng/kỹ thuật:** Owner.addVisit; EP — ID không tồn tại; Decision Table AV3.
- **Tiền điều kiện:** Owner chứa Buddy id=7; một Visit khác null.
- **Input và bước thực hiện:** Gọi addVisit(404,new Visit()).
- **Expected theo source:** IllegalArgumentException, message="Invalid Pet identifier!".
- **Assertion hiện có/GAP:** assertThatThrownBy kiểm tra loại và message chính xác.
- **Java method:** `OwnerMutationTests.addVisitRejectsUnknownPetId`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ kiểm tra kết quả lookup hoặc báo lỗi khác.

### TV3-O24 — toStringContainsKeyFields

- **Chức năng/kỹ thuật:** Owner.toString; Kiểm tra đầu ra; bảng TS1.
- **Tiền điều kiện:** Owner đã đặt đủ trường như input.
- **Input và bước thực hiện:** id=1; firstName=George; lastName=Franklin; address=110 W. Liberty St.; city=Madison; telephone=6085551023; gọi toString().
- **Expected theo source:** Chuỗi biểu diễn các trường id/new/lastName/firstName/address/city/telephone theo source; yêu cầu đang được kiểm tra là có Franklin, Madison, 6085551023.
- **Assertion hiện có/GAP:** Ba contains cho lastName/city/telephone; chưa assert id/new/firstName/address.
- **Java method:** `OwnerMutationTests.toStringContainsKeyFields`.
- **Rủi ro/mục tiêu thiết kế:** Mất nội dung ba trường được assert; không suy ra đã bảo vệ tất cả append trong source.

### TV3-O25 — getPetsStartsEmpty

- **Chức năng/kỹ thuật:** Owner.getPets; EP — trạng thái khởi tạo.
- **Tiền điều kiện:** Chưa thêm pet.
- **Input và bước thực hiện:** new Owner().getPets().
- **Expected theo source:** Collection rỗng.
- **Assertion hiện có/GAP:** isEmpty().
- **Java method:** `OwnerMutationTests.getPetsStartsEmpty`.
- **Rủi ro/mục tiêu thiết kế:** Khởi tạo collection sai; ca này không phân biệt collection rỗng thật với một giá trị rỗng thay thế.

### TV3-O26 — getAddressCityTelephoneRoundTrip

- **Chức năng/kỹ thuật:** Owner accessors; Kiểm tra trạng thái.
- **Tiền điều kiện:** Owner mới.
- **Input và bước thực hiện:** Set address="123 Caramel Street", city="London", telephone="1316761638"; đọc lại ba getter.
- **Expected theo source:** Ba getter trả đúng ba chuỗi đã gán.
- **Assertion hiện có/GAP:** Ba isEqualTo tương ứng.
- **Java method:** `OwnerMutationTests.getAddressCityTelephoneRoundTrip`.
- **Rủi ro/mục tiêu thiết kế:** Setter không lưu/getter trả chuỗi rỗng hoặc sai trường; không kiểm tra Bean Validation của telephone.

### TV3-O27 — birthDateHelperAcceptsLocalDate

- **Chức năng/kỹ thuật:** Pet birthDate accessors; Kiểm tra trạng thái.
- **Tiền điều kiện:** Pet Buddy mới.
- **Input và bước thực hiện:** Set birthDate=2015-02-12; đọc getBirthDate().
- **Expected theo source:** Ngày trả về bằng 2015-02-12.
- **Assertion hiện có/GAP:** isEqualTo(LocalDate.of(2015,2,12)).
- **Java method:** `OwnerMutationTests.birthDateHelperAcceptsLocalDate`.
- **Rủi ro/mục tiêu thiết kế:** Mất giá trị ngày hoặc getter trả null.

### TV3-V01 — nameExactlyAtMaxLengthIsAccepted

- **Chức năng/kỹ thuật:** PetValidator.validate — tên hợp lệ; BVA; V-T2.
- **Tiền điều kiện:** Pet hợp lệ mới: type dog, birthDate=2015-02-12; Errors mới.
- **Input và bước thực hiện:** Đổi name thành A×30; gọi validate(pet,errors).
- **Expected theo source:** Không có lỗi name; với tất cả trường hợp lệ thì không có lỗi nào.
- **Assertion hiện có/GAP:** Chỉ assert hasFieldErrors("name")=false. MISSING: dữ liệu A×29; INCOMPLETE: chưa assert toàn bộ errors hoặc trường type.
- **Java method:** `PetValidatorMutationTests.nameExactlyAtMaxLengthIsAccepted`.
- **Rủi ro/mục tiêu thiết kế:** ConditionalsBoundaryMutator đổi >30 thành >=30 sẽ từ chối tên dài 30; đây là mục tiêu thiết kế, chưa kết luận killed trong phiên.

### TV3-V02 — nameOneOverMaxLengthIsRejectedWithSizeCode

- **Chức năng/kỹ thuật:** PetValidator.validate — tên quá dài; BVA.
- **Tiền điều kiện:** Pet hợp lệ mới; Errors mới.
- **Input và bước thực hiện:** Đổi name thành A×31; gọi validate.
- **Expected theo source:** Có lỗi name với code="size".
- **Assertion hiện có/GAP:** hasFieldErrors("name")=true và getFieldError("name").getCode()="size".
- **Java method:** `PetValidatorMutationTests.nameOneOverMaxLengthIsRejectedWithSizeCode`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ nhánh chặn tên quá dài hoặc trả sai mã lỗi.

### TV3-V03 — emptyNameIsRejectedWithRequiredCode

- **Chức năng/kỹ thuật:** PetValidator.validate — tên rỗng; EP — không hợp lệ.
- **Tiền điều kiện:** Pet hợp lệ mới; Errors mới.
- **Input và bước thực hiện:** name=""; gọi validate.
- **Expected theo source:** Lỗi name/required.
- **Assertion hiện có/GAP:** Kiểm tra có lỗi name và code required.
- **Java method:** `PetValidatorMutationTests.emptyNameIsRejectedWithRequiredCode`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ kiểm tra tên bắt buộc hoặc dùng sai mã lỗi.

### TV3-V04 — blankNameIsRejectedWithRequiredCode

- **Chức năng/kỹ thuật:** PetValidator.validate — tên trắng; EP — không hợp lệ.
- **Tiền điều kiện:** Pet hợp lệ mới; Errors mới.
- **Input và bước thực hiện:** name="   "; gọi validate.
- **Expected theo source:** Lỗi name/required.
- **Assertion hiện có/GAP:** Chỉ hasFieldErrors("name")=true. INCOMPLETE: chưa assert code required.
- **Java method:** `PetValidatorMutationTests.blankNameIsRejectedWithRequiredCode`.
- **Rủi ro/mục tiêu thiết kế:** Chấp nhận chuỗi chỉ khoảng trắng; thay mã lỗi chưa được assertion hiện tại phát hiện.

### TV3-V05 — nullNameIsRejectedWithRequiredCode

- **Chức năng/kỹ thuật:** PetValidator.validate — tên null; EP — không hợp lệ.
- **Tiền điều kiện:** Pet hợp lệ mới; Errors mới.
- **Input và bước thực hiện:** name=null; gọi validate.
- **Expected theo source:** Lỗi name/required; không gọi length() trên null.
- **Assertion hiện có/GAP:** Chỉ hasFieldErrors("name")=true. INCOMPLETE: chưa assert code required.
- **Java method:** `PetValidatorMutationTests.nullNameIsRejectedWithRequiredCode`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ xử lý null hoặc trả sai mã lỗi (mã lỗi chưa được bảo vệ).

### TV3-V06 — persistedPetWithoutTypeIsAccepted

- **Chức năng/kỹ thuật:** PetValidator.validate — type; Decision Table V-T3.
- **Tiền điều kiện:** Pet hợp lệ, đổi id=42; Errors mới.
- **Input và bước thực hiện:** type=null; gọi validate.
- **Expected theo source:** Không có lỗi type; các trường còn lại hợp lệ.
- **Assertion hiện có/GAP:** hasFieldErrors("type")=false; không phải assertion toàn đối tượng.
- **Java method:** `PetValidatorMutationTests.persistedPetWithoutTypeIsAccepted`.
- **Rủi ro/mục tiêu thiết kế:** Bắt buộc type sai cho pet đã lưu.

### TV3-V07 — newPetWithoutTypeIsRejected

- **Chức năng/kỹ thuật:** PetValidator.validate — type; Decision Table V-T1.
- **Tiền điều kiện:** Pet mới id=null, tên/ngày sinh hợp lệ; Errors mới.
- **Input và bước thực hiện:** type=null; gọi validate.
- **Expected theo source:** Có lỗi type/required.
- **Assertion hiện có/GAP:** Chỉ hasFieldErrors("type")=true. INCOMPLETE: chưa assert code required.
- **Java method:** `PetValidatorMutationTests.newPetWithoutTypeIsRejected`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ yêu cầu type cho pet mới; thay mã lỗi chưa được phát hiện.

### TV3-V08 — persistedPetWithoutBirthDateIsStillRejected

- **Chức năng/kỹ thuật:** PetValidator.validate — birthDate/type; EP — thiếu ngày; Decision Table V-T4.
- **Tiền điều kiện:** Pet id=42, name=Buddy, type=dog; Errors mới.
- **Input và bước thực hiện:** birthDate=null; gọi validate.
- **Expected theo source:** Có lỗi birthDate/required, đồng thời không có lỗi type.
- **Assertion hiện có/GAP:** Chỉ hasFieldErrors("birthDate")=true. INCOMPLETE: thiếu assert required và hasFieldErrors("type")=false.
- **Java method:** `PetValidatorMutationTests.persistedPetWithoutBirthDateIsStillRejected`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ yêu cầu birthDate đối với pet đã lưu; lỗi giả trên type chưa được phát hiện.

### TV3-V09 — supportsPetAndSubclassesOnly

- **Chức năng/kỹ thuật:** PetValidator.supports; EP — lớp được/không được hỗ trợ.
- **Tiền điều kiện:** PetValidator mới.
- **Input và bước thực hiện:** Gọi supports(Pet.class), supports(String.class).
- **Expected theo source:** true với Pet; false với String. Theo isAssignableFrom, subclass Pet cũng phải true.
- **Assertion hiện có/GAP:** Có assert true/false cho Pet/String. MISSING: chưa khai báo/truyền subclass Pet.
- **Java method:** `PetValidatorMutationTests.supportsPetAndSubclassesOnly`.
- **Rủi ro/mục tiêu thiết kế:** Chỉ nhận đúng Pet mà từ chối subclass; hai assertion hiện tại chưa phân biệt trường hợp đó.

### TV3-M01 — petAddVisitStoresVisit

- **Chức năng/kỹ thuật:** Pet.addVisit/getVisits; Kiểm tra trạng thái.
- **Tiền điều kiện:** Pet mới; Visit có description="Checkup".
- **Input và bước thực hiện:** Gọi pet.addVisit(visit), đọc getVisits().
- **Expected theo source:** Collection chứa đúng instance visit.
- **Assertion hiện có/GAP:** containsExactly(visit); chưa kiểm tra lại từng field của Visit.
- **Java method:** `PetVisitModelMutationTests.petAddVisitStoresVisit`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ thêm visit hoặc getter trả collection rỗng.

### TV3-M02 — petTypeAndBirthDateRoundTrip

- **Chức năng/kỹ thuật:** Pet type/birthDate accessors; Kiểm tra trạng thái.
- **Tiền điều kiện:** Pet mới; PetType tên cat.
- **Input và bước thực hiện:** Set type và birthDate=2020-05-04; đọc getter.
- **Expected theo source:** Trả cùng instance type và đúng ngày 2020-05-04.
- **Assertion hiện có/GAP:** isSameAs(type), isEqualTo(ngày cố định); không kiểm tra PetType null.
- **Java method:** `PetVisitModelMutationTests.petTypeAndBirthDateRoundTrip`.
- **Rủi ro/mục tiêu thiết kế:** Mất type, trả sai object hoặc mất birthDate.

### TV3-M03 — visitDefaultsToTomorrow

- **Chức năng/kỹ thuật:** Visit constructor/getDate; Kiểm tra trạng thái; BVA ngày dự kiến.
- **Tiền điều kiện:** Dùng đồng hồ hệ thống; không cố định ngày trong test hiện tại.
- **Input và bước thực hiện:** new Visit().getDate(), so với LocalDate.now().plusDays(1).
- **Expected theo source:** Ngày mặc định là ngày kế tiếp ngày hệ thống tại lúc khởi tạo Visit.
- **Assertion hiện có/GAP:** Có isEqualTo nhưng hai lần đọc now độc lập: có thể lệch khi qua nửa đêm. MISSING: dữ liệu ngày thường/đổi năm/năm nhuận cố định trong bảng BVA.
- **Java method:** `PetVisitModelMutationTests.visitDefaultsToTomorrow`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ plusDays(1), đổi bước cộng hoặc trả sai ngày; tính ổn định tại biên nửa đêm chưa được đảm bảo.

### TV3-M04 — visitDescriptionRoundTrip

- **Chức năng/kỹ thuật:** Visit description accessors; Kiểm tra trạng thái.
- **Tiền điều kiện:** Visit mới.
- **Input và bước thực hiện:** Set description="Annual checkup"; đọc lại.
- **Expected theo source:** Trả đúng chuỗi Annual checkup.
- **Assertion hiện có/GAP:** isEqualTo chuỗi; không gọi Bean Validation.
- **Java method:** `PetVisitModelMutationTests.visitDescriptionRoundTrip`.
- **Rủi ro/mục tiêu thiết kế:** Getter trả rỗng/null hoặc setter không giữ mô tả; không chứng minh biên 255/256.

### TV3-M05 — visitDateRoundTrip

- **Chức năng/kỹ thuật:** Visit date accessors; Kiểm tra trạng thái.
- **Tiền điều kiện:** Visit mới.
- **Input và bước thực hiện:** Set date=2025-03-18; đọc lại.
- **Expected theo source:** Ngày trả về bằng 2025-03-18.
- **Assertion hiện có/GAP:** isEqualTo ngày cố định.
- **Java method:** `PetVisitModelMutationTests.visitDateRoundTrip`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ setter, trả ngày mặc định hoặc null; không kiểm tra quy tắc ngày tương lai của Controller.

### TV3-M06 — formatterPrintsNullNameAsPlaceholder

- **Chức năng/kỹ thuật:** PetTypeFormatter.print; EP — tên type null; F1.
- **Tiền điều kiện:** Formatter có repository mock; PetType khác null, name=null.
- **Input và bước thực hiện:** Gọi print(type,Locale.ENGLISH).
- **Expected theo source:** Trả chuỗi <null>.
- **Assertion hiện có/GAP:** isEqualTo("<null>").
- **Java method:** `PetVisitModelMutationTests.formatterPrintsNullNameAsPlaceholder`.
- **Rủi ro/mục tiêu thiết kế:** Bỏ nhánh placeholder hoặc trả null/rỗng; chưa phải test đối số PetType null.

### TV3-M07 — formatterPrintsConfiguredName

- **Chức năng/kỹ thuật:** PetTypeFormatter.print; EP — tên type có giá trị; F2.
- **Tiền điều kiện:** PetType có name=Hamster.
- **Input và bước thực hiện:** Gọi print(type,Locale.ENGLISH).
- **Expected theo source:** Trả Hamster.
- **Assertion hiện có/GAP:** isEqualTo("Hamster").
- **Java method:** `PetVisitModelMutationTests.formatterPrintsConfiguredName`.
- **Rủi ro/mục tiêu thiết kế:** Luôn trả placeholder hoặc chuỗi rỗng.

### TV3-M08 — formatterParsesKnownType

- **Chức năng/kỹ thuật:** PetTypeFormatter.parse; EP — tên có trong repository; F3.
- **Tiền điều kiện:** Repository mock trả List.of(dog), dog.name=Dog.
- **Input và bước thực hiện:** Gọi parse("Dog",Locale.ENGLISH).
- **Expected theo source:** Trả chính instance dog.
- **Assertion hiện có/GAP:** isSameAs(dog).
- **Java method:** `PetVisitModelMutationTests.formatterParsesKnownType`.
- **Rủi ro/mục tiêu thiết kế:** Trả null/sai instance hoặc không nhận tên khớp; danh sách một phần tử không kiểm chứng bỏ qua phần tử không khớp.

### TV3-M09 — formatterRejectsUnknownType

- **Chức năng/kỹ thuật:** PetTypeFormatter.parse; EP — tên không có; F4.
- **Tiền điều kiện:** Repository mock trả danh sách rỗng.
- **Input và bước thực hiện:** Gọi parse("Fish",Locale.ENGLISH).
- **Expected theo source:** ParseException với message="type not found: Fish", errorOffset=0 theo source.
- **Assertion hiện có/GAP:** Chỉ assert loại ParseException; chưa assert message/offset, chưa thử danh sách không rỗng nhưng không khớp.
- **Java method:** `PetVisitModelMutationTests.formatterRejectsUnknownType`.
- **Rủi ro/mục tiêu thiết kế:** Trả null thay vì ném lỗi; ca này không đi qua vòng lặp so tên.

## Kế hoạch bổ sung dữ liệu và kiểm chứng

| Case hiện có | Phần dự kiến, chưa thực hiện ở S01 | Expected cần quan sát | Session |
|---|---|---|---|
| V01 | Thử riêng A×29 và A×30, mỗi dữ liệu có Errors mới | Không có lỗi; bao gồm type và birthDate | S03 |
| V04/V05 | Assert code trên name | required | S03 |
| V07 | Assert code trên type | required | S03 |
| V08 | Assert code birthDate và kết quả type | birthDate/required và không lỗi type | S03 |
| V09 | Thử một subclass Pet thật | supports=true | S03 |
| M03 | Cố định today=2026-10-18 / 2026-12-31 / 2024-02-28 | 2026-10-19 / 2027-01-01 / 2024-02-29 | S04 |
| O01–O27, V01–V09, M01–M09 | JavaDoc chứa ID/kỹ thuật và liên kết tài liệu | Mapping đúng method; không đổi số lượng vì hình thức | S02–S04 |

Không tăng số test giả để ép 45. Khi thay đổi một lớp test ở phiên sau, chạy lớp đó rồi cả ba lớp TV3; S06 mới tổng hợp runtime và PIT trong workspace hiện tại. Trạng thái PASS/FAIL/SKIPPED phải đọc từ kết quả thực thi, không suy ra từ bảng expected.

S01 kiểm tra đủ 45 ID và method thật, liên kết tương đối, cấu trúc bảng Markdown và whitespace. Chỉ hai tài liệu này được tạo; chưa tạo onboarding, CSV, JSON, nhật ký hay bằng chứng runtime. Các tài liệu khác được nhắc bằng tên trong kế hoạch, không gắn liên kết tới file chưa tồn tại.
