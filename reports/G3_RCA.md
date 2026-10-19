# PHẦN G.2 & G.3: BÁO CÁO PHÂN TÍCH NGUYÊN NHÂN CỐT LÕI (RCA) & KHIẾM KHUYẾT MÃ NGUỒN (CODE SMELL)

> **Dự án:** Kiểm thử đột biến (Mutation Testing) bằng PIT trên Spring Boot PetClinic (K03 – R01)  
> **Phạm vi phân tích:** Toàn bộ package nghiệp vụ lõi `org.springframework.samples.petclinic.owner.*`  
> **Thành viên phụ trách:** Thành viên 5 (Metrics, RCA & Quality Analyst)  
> **Phiên thực hiện:** SESSION S3 — Chuẩn phân tích lỗi IEEE 1044 / IEEE 610.12  
> **Dữ liệu đầu vào:** [`reports/data/survivors_baseline.csv`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/survivors_baseline.csv) (64 mutants), [`reports/data/final_mutations.xml`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/final_mutations.xml), mã nguồn `src/main/java` và 7 file test mới.

---

## 1. PHƯƠNG PHÁP LUẬN PHÂN TÍCH THEO CHUẨN IEEE 1044 / IEEE 610.12

Để thực hiện phân tích nguyên nhân gốc rễ (Root Cause Analysis - RCA) một cách khoa học và hệ thống, báo cáo áp dụng mô hình phân rã lỗi ba tầng tiêu chuẩn của IEEE:

```
┌───────────────────────────────┐
│     ERROR (Sai sót con người) │  Nhận thức sai lầm của Tester/Dev về hành vi khung làm việc,
└──────────────┬────────────────┘  chỉ kiểm tra luồng danh định (happy-path), bỏ qua tác dụng phụ.
               │ sinh ra
               ▼
┌───────────────────────────────┐
│  FAULT (Khiếm khuyết trong    │  Sự thiếu sót cụ thể trong bộ kiểm thử (Test Suite): thiếu verify(),
│         bộ kiểm thử)          │  thiếu test biên BVA, thiếu Decision Table, thiếu assert nội dung sâu.
└──────────────┬────────────────┘
               │ dẫn đến
               ▼
┌───────────────────────────────┐
│ FAILURE (Thất bại quan sát)   │  Khi PIT tiêm đột biến thay đổi mã nguồn, test suite vẫn PASS (Xanh)
│    = MUTANT SỐNG SÓT          │  thay vì FAIL (Đỏ). Lỗi lọt lưới không bị phát hiện tại Baseline.
└───────────────────────────────┘
```

- **Error (Human Mistake):** Hành động sai lầm của con người trong quá trình thiết kế kịch bản kiểm thử (ví dụ: ngộ nhận rằng `MockMvc` bao phủ toàn bộ logic cập nhật của controller; tin rằng mã trạng thái HTTP 200/302 là đủ để đảm bảo thực thể đã được lưu; bỏ qua kiểm thử ranh giới).
- **Fault (Defect in Test Suite):** Khiếm khuyết hoặc lỗ hổng cụ thể tồn tại trong mã kiểm thử (ví dụ: thiếu lệnh `verify()` kiểm tra lời gọi void; thiếu các ca kiểm thử ném ngoại lệ khi ID không tồn tại; thiếu tổ hợp điều kiện trong bảng quyết định).
- **Failure (Observable Deviation / Mutant Survival):** Biểu hiện thất bại quan sát được trong kiểm thử đột biến: khi bộ mã bị đột biến (xóa câu lệnh, đảo biểu thức logic, đổi giá trị biên), bộ kiểm thử không thể làm đứt gãy luồng thực thi (không gây fail test), dẫn đến **mutant sống sót (`SURVIVED` hoặc `NO_COVERAGE`)**.

---

## 2. BẢNG TỔNG HỢP NGUYÊN NHÂN GỐC RỄ (RCA SUMMARY TABLE)

Tại giai đoạn Baseline (bộ test gốc gồm 49 tests), toàn bộ gói `owner` có **64 mutants không bị tiêu diệt** (gồm 55 mutants trạng thái `SURVIVED` và 9 mutants trạng thái `NO_COVERAGE`). Toàn bộ 64 mutants này được phân loại chính xác, không sót, không trùng vào 6 nhóm nguyên nhân gốc rễ như sau:

| STT | Nhóm nguyên nhân gốc rễ | Số mutant | Tỷ lệ (%) | Error (Sai sót con người) | Fault (Khiếm khuyết Test Suite) | Failure (Biểu hiện đột biến) | Biện pháp & Kỹ thuật diệt (TV3 / TV4) |
|:---:|:---|:---:|:---:|:---|:---|:---|:---|
| **1** | **MockMvc che khuất cập nhật thực thể & gán dư thừa** | 5 | 7.81% | Ngộ nhận `MockMvc` bao phủ toàn diện; không nhận thức được cơ chế in-place mutation của Spring DataBinder; lập trình phòng thủ dư thừa. | Chỉ test qua `MockMvc` nơi `existingPet` và `pet` trỏ cùng một vùng nhớ heap (aliasing); dòng `owner.setId` là dead-store sau guard. | Xóa 3 lệnh copy trường (`setName`, `setBirthDate`, `setType`) và `setId` nhưng test `MockMvc` vẫn PASS do đối tượng đã được cập nhật trước đó. | Khởi tạo Controller trực tiếp bằng POJO Unit Test, truyền thực thể tách rời (`detached entity`), dùng `ArgumentCaptor` kiểm tra; chứng minh Equivalent cho `setId`. |
| **2** | **Thiếu kiểm chứng tác dụng phụ & phương thức void** | 14 | 21.88% | Chỉ kiểm tra HTTP status (200/302) hoặc view name; giả định khung làm việc tự động thực thi các lời gọi phương thức `void`. | Bộ test thiếu hoàn toàn Mockito `verify()` kiểm tra tương tác mock và thiếu test kích hoạt các assertion kiểm tra tiền điều kiện (`Assert.notNull`). | PIT loại bỏ toàn bộ lời gọi hàm `void` (`VoidMethodCallMutator`): xóa cấm gán ID binder, xóa thêm visit, xóa lưu model nhưng test vẫn xanh. | Sử dụng Mockito `verify()` kiểm tra lệnh gọi `@InitBinder setDisallowedFields`; kiểm thử ngoại lệ `IllegalArgumentException` cho các guard `Assert.notNull`. |
| **3** | **Thiếu kiểm thử giá trị biên & tính toán số học** | 6 | 9.38% | Chỉ kiểm tra dữ liệu danh định điển hình (nominal values); không áp dụng kỹ thuật Phân tích giá trị biên (BVA) và kiểm thử chỉ số phân trang. | Thiếu ca kiểm thử tại biên 30 và 31 ký tự; thiếu kiểm tra tính toán chỉ số trang 0-based vs 1-based (`validatedPage - 1`); thiếu kiểm tra ngày mai (`now + 1`). | PIT sửa toán tử biên (`>` thành `>=`), sửa phép trừ thành cộng (`- 1` thành `+ 1`), thay đổi ngày tối thiểu nhưng test không phát hiện được. | Áp dụng BVA 2-point/3-point (30 vs 31 ký tự); dùng Mockito `ArgumentCaptor<Pageable>` kiểm tra chính xác `pageNumber`; kiểm thử ranh giới redirect khi vượt trang. |
| **4** | **Thiếu assert nội dung sâu & giá trị trả về** | 3 | 4.69% | Tin rằng chỉ cần phương thức thực thi không ném lỗi là dữ liệu trả về đã đúng; không kiểm tra nội dung chuỗi hoặc tập hợp. | Test suite không có bất kỳ lệnh assertion nào trên chuỗi `toString()`, getter `getDescription()` hoặc danh sách `types` trong Model. | PIT thay thế giá trị trả về bằng chuỗi rỗng `""` hoặc tập hợp rỗng (`EmptyObjectReturnValsMutator`) nhưng test vẫn bỏ lọt. | Viết test kiểm tra trạng thái sâu: `assertThat(owner.toString()).contains(...)`, `assertThat(visit.getDescription()).isEqualTo(...)`, assert model attributes. |
| **5** | **Nhánh ngoại lệ & luồng rẽ thiếu độ bao phủ (`NO_COVERAGE`)** | 9 | 14.06% | Bỏ qua hoàn toàn kiểm thử đường dẫn phủ định (Negative Testing); không thiết kế ca kiểm thử cho trường hợp bản ghi không tồn tại trong CSDL. | Không có test nào truyền ID không tồn tại (`id = 999`); không có test mô phỏng form update thất bại; thiếu stubbing tuần tự cho tra cứu lần 2. | Các biểu thức lambda `orElseThrow`, câu lệnh fallback `addPet` và lệnh nạp model khi lỗi hoàn toàn không được thực thi (`NO_COVERAGE`). | Bổ sung test truyền ID lạ ép ném `IllegalArgumentException`; thiết kế test form lỗi; dùng Mockito Sequential Stubbing (`thenReturn(...).thenReturn(empty)`). |
| **6** | **Thiếu bảng quyết định cho tổ hợp điều kiện logic phức tạp** | 27 | 42.19% | Áp dụng kiểm thử sơ sài cho các mệnh đề `if` ghép nhiều điều kiện (`&&`, `||`); không lập Bảng quyết định (Decision Table) cho các biến trạng thái. | Thiếu ca kiểm thử cho các tổ hợp: pet mới vs pet cũ, cùng ID khác instance, khác ID, tên trùng/không trùng, cờ `ignoreNew`, vi phạm unique key CSDL. | PIT loại bỏ từng vế điều kiện logic (`RemoveConditionalMutator_EQUAL_IF` / `EQUAL_ELSE`, ép nhánh thành `true`/`false`) nhưng test suite không bắt được. | Xây dựng Bảng quyết định toàn diện: bộ 9 test cho `Owner.addPet`, bộ 6 test cho `Owner.getPet`, bảng 2 chiều cho `PetValidator`, bẫy `DataIntegrityViolationException`. |
| **—** | **TỔNG CỘNG** | **64** | **100.0%** | *(Khớp 100% số liệu `survivors_baseline.csv`, không sót bất kỳ mutant nào)* | | | |

---

## 3. PHÂN TÍCH CHI TIẾT TỪNG NHÓM NGUYÊN NHÂN CỐT LÕI

### 3.1. Nhóm 1: MockMvc che khuất cập nhật thực thể & gán giá trị dư thừa (5 mutants)
- **Đặc trưng:** Đây là nhóm khiếm khuyết tinh vi và phức tạp nhất, xuất phát từ sự tương tác giữa kiến trúc Spring MVC và kiểm thử hộp trắng.
- **Cơ chế lỗi:**
  - Trong Spring MVC, khi phương thức controller nhận đối tượng qua `@ModelAttribute("pet")` hoặc form binding, `ServletModelAttributeMethodProcessor` nạp thực thể từ CSDL thông qua `findPet(ownerId, petId)`.
  - Thực thể này nằm trong bộ nhớ cache của Model và trỏ thẳng tới đối tượng `existingPet` bên trong `owner.getPets()`.
  - Khi HTTP POST request gửi dữ liệu lên, Spring DataBinder ghi đè trực tiếp các tham số HTTP (`name`, `birthDate`, `type`) lên chính instance `existingPet` đó TRƯỚC KHI phương thức `updatePetDetails` được gọi.
  - Khi vào phương thức `updatePetDetails(Owner owner, Pet pet)`:
    ```java
    Pet existingPet = owner.getPet(id);
    if (existingPet != null) {
        existingPet.setName(pet.getName());       // Dòng 192: existingPet == pet!
        existingPet.setBirthDate(pet.getBirthDate()); // Dòng 193: existingPet == pet!
        existingPet.setType(pet.getType());       // Dòng 194: existingPet == pet!
    }
    ```
  - Vì `existingPet` và `pet` là cùng một con trỏ bộ nhớ, các câu lệnh gán ở dòng 192-194 thực chất là gán giá trị của đối tượng cho chính nó. Khi PIT xóa 3 dòng này, đối tượng `existingPet` VẪN MANG GIÁ TRỊ MỚI do DataBinder đã ghi trước đó. Mọi test chạy qua `MockMvc` đều thấy CSDL lưu dữ liệu mới và khẳng định test PASS!
  - Đối với `OwnerController.java:167` (`owner.setId(ownerId)`): Đây là lệnh gán phòng thủ dư thừa vì dòng 161 đã chặn mismatch ID. Xóa dòng này không làm thay đổi trạng thái hệ thống (Equivalent Mutant).

#### Danh mục 5 mutants thuộc Nhóm 1:
| STT | Lớp : Dòng | Phương thức | Toán tử đột biến (Mutator) | Baseline | Final | Test đã diệt (TV3 / TV4) & Kỹ thuật |
|:---:|:---|:---|:---|:---:|:---:|:---|
| 1 | `PetController:190` | `updatePetDetails` | `RemoveConditionalMutator_EQUAL_ELSE` | SURVIVED | KILLED | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` (POJO Unit Test + Detached Entity) |
| 2 | `PetController:192` | `updatePetDetails` | `VoidMethodCallMutator` | SURVIVED | KILLED | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` (Khởi tạo `new`, inject detached `Pet`) |
| 3 | `PetController:193` | `updatePetDetails` | `VoidMethodCallMutator` | SURVIVED | KILLED | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` (Khởi tạo `new`, inject detached `Pet`) |
| 4 | `PetController:194` | `updatePetDetails` | `VoidMethodCallMutator` | SURVIVED | KILLED | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` (Khởi tạo `new`, inject detached `Pet`) |
| 5 | `OwnerController:167` | `processUpdateOwnerForm` | `VoidMethodCallMutator` | SURVIVED | **SURVIVED** | **NONE — Equivalent Mutant** (Chứng minh đại số Boolean tại Phần G.4) |

---

### 3.2. Nhóm 2: Thiếu kiểm chứng tác dụng phụ & lời gọi phương thức void (14 mutants)
- **Đặc trưng:** Các câu lệnh thực thi có kiểu trả về `void`, bao gồm: cấu hình bảo mật Binder (`setDisallowedFields`), kiểm tra tiền điều kiện (`Assert.notNull`, `Assert.state`), và chuyển tiếp nghiệp vụ miền (`pet.addVisit`, `owner.addPet`, `result.rejectValue`).
- **Cơ chế lỗi:**
  - Bộ test baseline chỉ kiểm tra kết quả cuối cùng ở bề mặt (HTTP Status Code 200/302, redirected URL, tên template view).
  - Lập trình viên không viết các câu lệnh kiểm tra tương tác (Interaction Testing) để xác minh xem phương thức `void` có thực sự được gọi với tham số mong đợi hay không.
  - Ví dụ: Phương thức `@InitBinder public void setAllowedFields(WebDataBinder dataBinder)` gọi `dataBinder.setDisallowedFields("id", "*.id")` để chặn lỗ hổng Mass Assignment. Khi PIT xóa dòng này (`VoidMethodCallMutator`), HTTP request thông thường vẫn trả về view thành công, do đó mutant sống sót hoàn toàn.

#### Danh mục 14 mutants thuộc Nhóm 2:
| STT | Lớp : Dòng | Phương thức | Lời gọi bị đột biến | Baseline | Final | Test đã diệt (TV3 / TV4) & Kỹ thuật |
|:---:|:---|:---|:---|:---:|:---:|:---|
| 6 | `OwnerController:61` | `setAllowedFields` | `dataBinder.setDisallowedFields` | SURVIVED | KILLED | `ControllerBinderMutationTests.ownerControllerDisallowsIdBinding` (`verify()`) |
| 7 | `PetController:91` | `initOwnerBinder` | `dataBinder.setDisallowedFields` | SURVIVED | KILLED | `ControllerBinderMutationTests.petControllerOwnerBinderDisallowsIdBinding` (`verify()`) |
| 8 | `PetController:97` | `initPetBinder` | `dataBinder.setDisallowedFields` | SURVIVED | KILLED | `ControllerBinderMutationTests.petControllerPetBinderDisallowsIdBinding` (`verify()`) |
| 9 | `VisitController:53` | `setAllowedFields` | `dataBinder.setDisallowedFields` | SURVIVED | KILLED | `ControllerBinderMutationTests.visitControllerDisallowsIdBinding` (`verify()`) |
| 10 | `Owner:178` | `addVisit` | `Assert.notNull(petId, ...)` | SURVIVED | KILLED | `OwnerMutationTests.addVisitRejectsNullPetId` (`assertThatThrownBy`) |
| 11 | `Owner:179` | `addVisit` | `Assert.notNull(visit, ...)` | SURVIVED | KILLED | `OwnerMutationTests.addVisitRejectsNullVisit` (`assertThatThrownBy`) |
| 12 | `Owner:183` | `addVisit` | `Assert.notNull(pet, ...)` | SURVIVED | KILLED | `OwnerMutationTests.addVisitRejectsUnknownPetId` (`assertThatThrownBy`) |
| 13 | `Owner:185` | `addVisit` | `pet.addVisit(visit)` | SURVIVED | KILLED | `OwnerMutationTests.addVisitDelegatesToPet` (State Verification) |
| 14 | `PetController:103` | `initCreationForm` | `owner.addPet(pet)` | SURVIVED | KILLED | `PetControllerMutationTests.initCreationFormAddsPetToOwnerModel` (`assertThat`) |
| 15 | `PetController:125` | `processCreationForm` | `owner.addPet(pet)` | SURVIVED | KILLED | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` (`ArgumentCaptor`) |
| 16 | `PetController:188` | `updatePetDetails` | `Assert.state(id != null, ...)` | SURVIVED | KILLED | `PetControllerMutationTests.updateWithNullPetIdFailsFast` (`assertThrows`) |
| 17 | `VisitController:79` | `loadPetWithVisit` | `pet.addVisit(visit)` | SURVIVED | KILLED | `VisitControllerMutationTests.newVisitFormExposesPetWithPendingVisit` (Model inspect) |
| 18 | `VisitController:108` | `processNewVisitForm` | `owner.addVisit(petId, visit)` | SURVIVED | KILLED | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` |
| 19 | `OwnerController:162` | `processUpdateOwnerForm` | `result.rejectValue(...)` | SURVIVED | KILLED | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` |

---

### 3.3. Nhóm 3: Thiếu kiểm thử giá trị biên & tính toán số học (6 mutants)
- **Đặc trưng:** Lỗi xuất hiện tại các ranh giới so sánh (`>`, `<`, `Math.max`), tính toán dịch chuyển vị trí (off-by-one trong phân trang) và các giá trị ngày ranh giới.
- **Cơ chế lỗi:**
  - `PetValidator.java:46`: Quy tắc `name.length() > 30` quy định tên thú cưng tối đa 30 ký tự. Bộ test baseline dùng tên `"George"` (6 ký tự) hoặc chuỗi rỗng `""`. Khi PIT đổi thành `name.length() >= 30` (`ConditionalsBoundaryMutator`), chuỗi 30 ký tự bị từ chối sai quy cách nhưng test baseline không bắt được.
  - `OwnerController.java:144`: Tính toán `PageRequest.of(validatedPage - 1, pageSize)` chuyển đổi chỉ số trang 1-based (người dùng nhập) sang 0-based (Spring Data). PIT đổi `- 1` thành `+ 1` (`MathMutator`). Test baseline chỉ yêu cầu trang 1 và repository giả lập trả về trang 1 mà không kiểm tra tham số `Pageable` thực nhận.

#### Danh mục 6 mutants thuộc Nhóm 3:
| STT | Lớp : Dòng | Phương thức | Toán tử đột biến | Nội dung đột biến | Baseline | Final | Test đã diệt & Kỹ thuật |
|:---:|:---|:---|:---|:---|:---:|:---:|:---|
| 20 | `PetValidator:46` | `validate` | `ConditionalsBoundaryMutator` | Đổi `> 30` thành `>= 30` | SURVIVED | KILLED | `PetValidatorMutationTests.nameExactlyAtMaxLengthIsAccepted` (BVA 30 ký tự) |
| 21 | `OwnerController:144` | `findPaginatedForOwnersLastName` | `MathMutator` | Đổi `validatedPage - 1` thành `+ 1` | SURVIVED | KILLED | `OwnerControllerMutationTests.processFindFormRequestsZeroBasedPageIndex` (`ArgumentCaptor<Pageable>`) |
| 22 | `OwnerController:110` | `processFindForm` | `RemoveConditionalMutator_EQUAL_IF` | Ép `page > totalPages` thành `true` | SURVIVED | KILLED | `OwnerControllerMutationTests.outOfBoundsPageWithEmptyLastNameOmitsLastNameParam` |
| 23 | `VisitController:85` | `minVisitDate` | `NullReturnValsMutator` | Trả về `null` thay vì `now().plusDays(1)` | SURVIVED | KILLED | `ControllerBinderMutationTests.minVisitDateIsTomorrow` (Assert `LocalDate`) |
| 24 | `PetTypeFormatter:48` | `print` | `RemoveConditionalMutator_EQUAL_IF` | Ép kiểm tra `petType == null` thành `true` | SURVIVED | KILLED | `PetVisitModelMutationTests.formatterPrintsNullNameAsPlaceholder` (Null-value EP) |
| 25 | `PetController:188` | `updatePetDetails` | `RemoveConditionalMutator_EQUAL_IF` | Ép kiểm tra `id != null` thành `true` | SURVIVED | KILLED | `PetControllerMutationTests.updateWithNullPetIdFailsFast` (Boundary Null Check) |

---

### 3.4. Nhóm 4: Thiếu assert nội dung sâu & giá trị trả về (3 mutants)
- **Đặc trưng:** Các phương thức sinh dữ liệu định dạng (`toString`), getter nghiệp vụ hoặc nạp dữ liệu danh mục (`@ModelAttribute`).
- **Cơ chế lỗi:** Bộ test thực thi phương thức nhưng không kiểm tra nội dung trả về. Khi PIT thay thế kết quả bằng chuỗi rỗng `""` hoặc tập hợp rỗng (`EmptyObjectReturnValsMutator`), không có assertion nào bị vi phạm.

#### Danh mục 3 mutants thuộc Nhóm 4:
| STT | Lớp : Dòng | Phương thức | Toán tử đột biến | Nội dung đột biến | Baseline | Final | Test đã diệt & Kỹ thuật |
|:---:|:---|:---|:---|:---|:---:|:---:|:---|
| 26 | `Owner:161` | `toString` | `EmptyObjectReturnValsMutator` | Trả về `""` thay vì chuỗi mô tả | SURVIVED | KILLED | `OwnerMutationTests.toStringContainsKeyFields` (Assert chứa đủ 6 trường khóa) |
| 27 | `Visit:63` | `getDescription` | `EmptyObjectReturnValsMutator` | Trả về `""` thay vì `description` | SURVIVED | KILLED | `PetVisitModelMutationTests.visitDescriptionRoundTrip` (Assert getter/setter) |
| 28 | `PetController:64` | `populatePetTypes` | `EmptyObjectReturnValsMutator` | Trả về `emptyList()` thay vì types | SURVIVED | KILLED | `PetControllerMutationTests.initCreationFormExposesConfiguredPetTypes` (Model assert) |

---

### 3.5. Nhóm 5: Nhánh ngoại lệ & luồng rẽ thiếu độ bao phủ (`NO_COVERAGE` - 9 mutants)
- **Đặc trưng:** Các dòng lệnh hoàn toàn chưa từng được chạm tới bởi bất kỳ test case nào tại Baseline (`NO_COVERAGE`), chủ yếu nằm ở các biểu thức lambda ném ngoại lệ khi không tìm thấy thực thể hoặc luồng xử lý form lỗi.
- **Cơ chế lỗi:**
  - Bộ test baseline 100% chỉ giả lập tìm thấy bản ghi (`findById(id)` luôn trả về `Optional.of(owner)`). Do đó, biểu thức lambda `() -> new IllegalArgumentException(...)` trong `.orElseThrow()` không bao giờ được khởi tạo hay thực thi.
  - Tại `OwnerController.java:182`, hàm `showOwner` thực hiện truy vấn `findById` lần 2, tạo ra nhánh lỗi không thể kích hoạt được nếu không dùng kỹ thuật Mockito Sequential Stubbing.

#### Danh mục 9 mutants thuộc Nhóm 5 (`NO_COVERAGE` tại Baseline):
| STT | Lớp : Dòng | Phương thức | Toán tử đột biến | Nội dung dòng lệnh / Biểu thức | Baseline | Final | Test đã diệt & Kỹ thuật |
|:---:|:---|:---|:---|:---|:---:|:---:|:---|
| 29 | `OwnerController:68` | `lambda$findOwner$0` | `NullReturnValsMutator` | Lambda ném ngoại lệ khi ownerId không tìm thấy | NO_COVERAGE | KILLED | `OwnerControllerMutationTests.showOwnerWithUnknownIdThrowsIllegalArgument` |
| 30 | `OwnerController:182` | `lambda$showOwner$1` | `NullReturnValsMutator` | Lambda ném ngoại lệ tại tra cứu lần 2 trong `showOwner` | NO_COVERAGE | KILLED | `OwnerControllerMutationTests.showOwnerFailingOnSecondLookupThrowsIllegalArgument` |
| 31 | `PetController:70` | `lambda$findOwner$0` | `NullReturnValsMutator` | Lambda ném ngoại lệ khi ownerId không tìm thấy | NO_COVERAGE | KILLED | `PetControllerMutationTests.creationWithUnknownOwnerThrowsIllegalArgument` |
| 32 | `PetController:84` | `lambda$findPet$1` | `NullReturnValsMutator` | Lambda ném ngoại lệ khi petId không tìm thấy | NO_COVERAGE | KILLED | `PetControllerMutationTests.findPetWithUnknownOwnerThrowsIllegalArgument` |
| 33 | `VisitController:67` | `lambda$loadPetWithVisit$0` | `NullReturnValsMutator` | Lambda ném ngoại lệ khi ownerId không tìm thấy | NO_COVERAGE | KILLED | `VisitControllerMutationTests.newVisitFormWithUnknownOwnerThrowsIllegalArgument` |
| 34 | `PetController:160` | `processUpdateForm` | `VoidMethodCallMutator` | `model.put("pet", pet)` khi form update có lỗi | NO_COVERAGE | KILLED | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` (Error flow) |
| 35 | `PetController:197` | `updatePetDetails` | `VoidMethodCallMutator` | `owner.addPet(pet)` fallback khi không tìm thấy pet cũ | NO_COVERAGE | KILLED | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` (Fallback flow) |
| 36 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_ELSE` | Nhánh đoản mạch đánh giá vế 3 trong biểu thức `&&` (index 33) | NO_COVERAGE | KILLED | `OwnerMutationTests.addPetRejectsDifferentInstanceWithSameId` (Decision Table) |
| 37 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_IF` | Nhánh đoản mạch đánh giá vế 3 trong biểu thức `&&` (index 34) | NO_COVERAGE | KILLED | `OwnerMutationTests.addPetAllowsDifferentIds` (Decision Table) |

---

### 3.6. Nhóm 6: Thiếu bảng quyết định cho tổ hợp điều kiện logic phức tạp (27 mutants)
- **Đặc trưng:** Chiếm tỷ trọng lớn nhất (**42.19%**). Tập trung tại các biểu thức điều kiện nhiều vế trong `Owner.addPet`, `Owner.getPet`, `PetValidator.validate` và xử lý trùng lặp dữ liệu `PetController`.
- **Cơ chế lỗi:**
  - Một câu lệnh `if (A && B && C)` có tới 8 tổ hợp chân trị ($2^3$). Nếu chỉ kiểm thử một kịch bản danh định (ví dụ cả A, B, C đều đúng), PIT sẽ lần lượt tiêm đột biến thay thế từng vế A, B, hoặc C bằng `true` hoặc `false`.
  - Bộ test baseline thiếu Bảng quyết định (Decision Table), dẫn tới việc không kiểm thử các tổ hợp biên: thực thể mới thêm lần 2, thực thể cũ trùng ID, khác ID, cờ `ignoreNew` bật/tắt khi pet có ID null.

#### Danh mục 27 mutants thuộc Nhóm 6:
| STT | Lớp : Dòng | Phương thức | Toán tử đột biến | Nội dung điều kiện bị đột biến | Baseline | Final | Test đã diệt & Kỹ thuật |
|:---:|:---|:---|:---|:---|:---:|:---:|:---|
| 38 | `Owner:101` | `addPet` | `RemoveConditionalMutator_EQUAL_ELSE` | `if (pet == null)` | SURVIVED | KILLED | `OwnerMutationTests.addPetIgnoresNull` |
| 39 | `Owner:104` | `addPet` | `RemoveConditionalMutator_EQUAL_ELSE` | `if (getPets().contains(pet))` | SURVIVED | KILLED | `OwnerMutationTests.addPetRejectsSameNewInstanceTwice` |
| 40 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_ELSE` | `Objects.equals(...)` (index 31) | SURVIVED | KILLED | `OwnerMutationTests.addPetRejectsDifferentInstanceWithSameId` |
| 41 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_ELSE` | `Objects.equals(...)` (index 32) | SURVIVED | KILLED | `OwnerMutationTests.addPetRejectsDifferentInstanceWithSameId` |
| 42 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_IF` | `!existingPet.isNew()` (index 35) | SURVIVED | **SURVIVED** | **NONE — Equivalent Mutant** (Phần G.4) |
| 43 | `Owner:108` | `addPet` | `RemoveConditionalMutator_EQUAL_IF` | `!pet.isNew()` (index 36) | SURVIVED | **SURVIVED** | **NONE — Equivalent Mutant** (Phần G.4) |
| 44 | `Owner:131` | `getPet` | `RemoveConditionalMutator_EQUAL_IF` | `pet.getId().equals(id)` | SURVIVED | KILLED | `OwnerMutationTests.getPetByIdWithNullIdReturnsNull` |
| 45 | `Owner:150` | `getPet` | `RemoveConditionalMutator_EQUAL_IF` | `pet.getName() == null` | SURVIVED | KILLED | `OwnerMutationTests.getPetByNameReturnsNullWhenAbsent` |
| 46 | `Owner:151` | `getPet` | `RemoveConditionalMutator_EQUAL_ELSE` | `!ignoreNew \|\| !pet.isNew()` | SURVIVED | KILLED | `OwnerMutationTests.getPetByNameWithIgnoreNewReturnsPersistedPet` |
| 47 | `Owner:151` | `getPet` | `RemoveConditionalMutator_EQUAL_IF` | `!ignoreNew` (vế 1) | SURVIVED | KILLED | `OwnerMutationTests.getPetByNameWithIgnoreNewSkipsNewPet` |
| 48 | `Owner:151` | `getPet` | `RemoveConditionalMutator_EQUAL_IF` | `!pet.isNew()` (vế 2) | SURVIVED | KILLED | `OwnerMutationTests.getPetByNameWithIgnoreNewSkipsNewPet` |
| 49 | `PetController:111` | `processCreationForm` | `RemoveConditionalMutator_EQUAL_IF` | `owner.getPet(name, false)` (vế 1) | SURVIVED | KILLED | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| 50 | `PetController:111` | `processCreationForm` | `RemoveConditionalMutator_EQUAL_IF` | `owner.getPet(name, false)` (vế 2) | SURVIVED | KILLED | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| 51 | `PetController:116` | `processCreationForm` | `RemoveConditionalMutator_EQUAL_IF` | `StringUtils.hasText(pet.getName())` | SURVIVED | KILLED | `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName` |
| 52 | `PetController:129` | `processCreationForm` | `RemoveConditionalMutator_EQUAL_ELSE` | `isDuplicatePetNameViolation(ex)` | SURVIVED | KILLED | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` |
| 53 | `PetController:151` | `processUpdateForm` | `RemoveConditionalMutator_EQUAL_IF` | `StringUtils.hasText(pet.getName())` | SURVIVED | KILLED | `PetControllerMutationTests.updateWithBlankNameSkipsDuplicateCheck` |
| 54 | `PetController:153` | `processUpdateForm` | `RemoveConditionalMutator_EQUAL_IF` | `owner.getPet(name, false)` | SURVIVED | KILLED | `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation` |
| 55 | `PetController:159` | `processUpdateForm` | `RemoveConditionalMutator_EQUAL_ELSE` | `pet.getBirthDate().isAfter(...)` (vế 1) | SURVIVED | KILLED | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| 56 | `PetController:159` | `processUpdateForm` | `RemoveConditionalMutator_EQUAL_ELSE` | `pet.getBirthDate().isAfter(...)` (vế 2) | SURVIVED | KILLED | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| 57 | `PetController:171` | `processUpdateForm` | `RemoveConditionalMutator_EQUAL_ELSE` | `isDuplicatePetNameViolation(ex)` | SURVIVED | KILLED | `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation` |
| 58 | `PetController:190` | `updatePetDetails` | `RemoveConditionalMutator_EQUAL_IF` | `if (existingPet != null)` | SURVIVED | KILLED | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` |
| 59 | `PetController:204` | `isDuplicatePetNameViolation` | `BooleanTrueReturnValsMutator` | Trả về `true` khi không vi phạm | SURVIVED | KILLED | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` |
| 60 | `PetController:204` | `isDuplicatePetNameViolation` | `RemoveConditionalMutator_EQUAL_IF` | `message != null` | SURVIVED | KILLED | `PetControllerMutationTests.creationRethrowsUnexpectedIntegrityViolation` |
| 61 | `PetController:204` | `isDuplicatePetNameViolation` | `RemoveConditionalMutator_EQUAL_IF` | `message.toLowerCase().contains(...)` | SURVIVED | KILLED | `PetControllerMutationTests.creationRethrowsUnexpectedIntegrityViolation` |
| 62 | `PetValidator:51` | `validate` | `RemoveConditionalMutator_EQUAL_IF` | `pet.isNew() && pet.getType() == null` | SURVIVED | KILLED | `PetValidatorTests.validate` (Decision Table `isNew × type`) |
| 63 | `VisitController:71` | `loadPetWithVisit` | `RemoveConditionalMutator_EQUAL_ELSE` | `if (pet == null)` | SURVIVED | KILLED | `VisitControllerMutationTests.newVisitFormWithUnknownPetThrowsIllegalArgument` |
| 64 | `VisitController:100` | `processNewVisitForm` | `RemoveConditionalMutator_EQUAL_IF` | `!visit.getDate().isAfter(...)` | SURVIVED | KILLED | `VisitControllerTests.processNewVisitFormSuccess` |

---

## 4. BÁO CÁO KHIẾM KHUYẾT MÃ NGUỒN (CODE SMELL & DEFECT ANALYSIS)

Quá trình phân tích kiểm thử đột biến không chỉ giúp tăng cường chất lượng bộ kiểm thử mà còn đóng vai trò như một **kính hiển vi tĩnh** vạch rõ các vấn đề về thiết kế, dead-code và code smell trong mã nguồn `src/main/java`.

> [!IMPORTANT]
> **Tuân thủ Ràng buộc bất biến số 1:** Toàn bộ 6 code smell dưới đây được phát hiện kèm bằng chứng mã nguồn cụ thể, nhưng **tuyệt đối không chỉnh sửa `src/main/java`** trong khuôn khổ đề tài. Các giải pháp được đưa ra dưới dạng khuyến nghị tái cấu trúc (Refactoring Proposal) phục vụ đánh giá chất lượng phần mềm.

---

### Smell 1: Dead-Store / Lệnh gán phòng thủ dư thừa (Redundant Field Assignment)
- **Vị trí:** [`OwnerController.java:161-168`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L161-L168)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  161: 		if (!Objects.equals(owner.getId(), ownerId)) {
  162: 			result.rejectValue("id", "mismatch", "The owner ID in the form does not match the URL.");
  163: 			redirectAttributes.addFlashAttribute("error", "Owner ID mismatch. Please try again.");
  164: 			return "redirect:/owners/{ownerId}/edit";
  165: 		}
  166: 
  167: 		owner.setId(ownerId); // <-- SMELL: Dead-store gán dư thừa
  168: 		this.owners.save(owner);
  ```
- **Mô tả kỹ thuật:**
  - Khối lệnh guard ở dòng 161–165 đã kiểm tra và điều hướng trả về sớm nếu `owner.getId()` khác `ownerId`.
  - Khi luồng thực thi đi tới dòng 167, điều kiện chắc chắn xảy ra là `owner.getId() == ownerId`. Vì vậy, lệnh `owner.setId(ownerId)` là thao tác gán lại đúng giá trị mà đối tượng đang nắm giữ.
  - Hơn nữa, tại dòng 61, `@InitBinder` đã cấu hình `dataBinder.setDisallowedFields("id", "*.id")`, loại bỏ hoàn toàn khả năng ID bị sửa đổi qua HTTP request params.
  - Thao tác gán này sinh ra một **Equivalent Mutant** trong PIT (`VoidMethodCallMutator` xóa dòng 167). Do đột biến này không gây ra bất kỳ sai lệch trạng thái nào, không có test nào có thể diệt được.
- **Mức độ ảnh hưởng:** **Thấp (Minor Code Smell)** — Không gây lỗi logic nhưng tạo ra dead-code và mutant bất tử giả tạo trong báo cáo kiểm thử.
- **Đề xuất khắc phục:** Loại bỏ hoàn toàn dòng 167.

---

### Smell 2: Biểu thức điều kiện phòng vệ cực đoan tạo Equivalent Mutants
- **Vị trí:** [`Owner.java:107-111`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/Owner.java#L107-L111)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  107: 		for (Pet existingPet : getPets()) {
  108: 			if (!existingPet.isNew() && !pet.isNew() && Objects.equals(existingPet.getId(), pet.getId())) {
  109: 				return;
  110: 			}
  111: 		}
  ```
- **Mô tả kỹ thuật:**
  - Theo lớp cha `BaseEntity.java:49`, `isNew()` có định nghĩa: `return this.id == null;`. Như vậy `!pet.isNew() ⟺ pet.getId() != null`.
  - Phép so sánh `Objects.equals(existingPet.getId(), pet.getId())` chỉ có thể lượng giá thành `true` khi cả hai ID cùng khác `null` và bằng nhau (trường hợp cả 2 cùng null đối với cùng một thể hiện đã bị chặn ở dòng 104 `getPets().contains(pet)`).
  - Về mặt đại số Boolean, điều kiện `!existingPet.isNew() && !pet.isNew()` là **tập con phụ thuộc (subsumed)** của phép so sánh `Objects.equals(...)` khi hai ID hợp lệ. Khi PIT ép một trong hai vế này thành `true` (`RemoveConditionalMutator_EQUAL_IF`), giá trị chân trị của toàn bộ biểu thức `if` không đổi. Điều này tạo ra **02 Equivalent Mutants sống sót vĩnh viễn** tại dòng 108.
- **Mức độ ảnh hưởng:** **Trung bình (Code Bloat / Unkillable Mutants)** — Gây lãng phí tính toán trong vòng lặp và làm giảm điểm Mutation Score hữu hiệu nếu không có chứng minh hình thức.
- **Đề xuất khắc phục:** Rút gọn thành `if (Objects.equals(existingPet.getId(), pet.getId())) { return; }` hoặc kiểm tra `if (pet.isNew()) { getPets().add(pet); return; }` ngay trước vòng lặp.

---

### Smell 3: Truy vấn CSDL lặp lại & Nhánh lỗi bất khả đạt (Unreachable Branch)
- **Vị trí:** [`OwnerController.java:64-70`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L64-L70) và [`OwnerController.java:178-186`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L178-L186)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  // Dòng 64-70 (findOwner - nạp tự động trước handler):
  64: 	@ModelAttribute("owner")
  65: 	public Owner findOwner(@PathVariable(name = "ownerId", required = false) Integer ownerId) {
  66: 		return ownerId == null ? new Owner()
  67: 				: this.owners.findById(ownerId)
  68: 					.orElseThrow(() -> new IllegalArgumentException("Owner not found with id: " + ownerId ...));
  69: 	}

  // Dòng 178-186 (showOwner - hiển thị chi tiết):
  178: 	@GetMapping("/owners/{ownerId}")
  179: 	public ModelAndView showOwner(@PathVariable("ownerId") int ownerId) {
  180: 		ModelAndView mav = new ModelAndView("owners/ownerDetails");
  181: 		Optional<Owner> optionalOwner = this.owners.findById(ownerId); // <-- SMELL: Query CSDL lần 2
  182: 		Owner owner = optionalOwner.orElseThrow(() -> new IllegalArgumentException( // <-- SMELL: Unreachable
  183: 				"Owner not found with id: " + ownerId + ". Please ensure the ID is correct "));
  184: 		mav.addObject(owner);
  185: 		return mav;
  186: 	}
  ```
- **Mô tả kỹ thuật:**
  - Khi nhận request `GET /owners/{ownerId}`, Spring MVC luôn thực thi `@ModelAttribute("owner") findOwner(...)` TRƯỚC. Nếu ID không tồn tại trong CSDL, dòng 68 đã ném `IllegalArgumentException` lập tức.
  - Tuy nhiên, khi phương thức `showOwner` chạy, nó lại gọi tiếp `this.owners.findById(ownerId)` lần thứ hai (dòng 181) và lại `.orElseThrow(...)` (dòng 182).
  - Nhánh `.orElseThrow(...)` ở dòng 182 là **hoàn toàn không thể chạm tới (Unreachable)** trong điều kiện bình thường. Để kích hoạt dòng này trong unit test, TV4 buộc phải sử dụng kỹ thuật Mockito Sequential Stubbing (`when.thenReturn(owner).thenReturn(Optional.empty())`). Đây là lý do mutant `lambda$showOwner$1` bị `NO_COVERAGE` ở baseline.
- **Mức độ ảnh hưởng:** **Trung bình (Performance & Architecture Smell)** — Gây dư thừa 1 truy vấn CSDL độc lập trên mỗi lượt xem chi tiết chủ nuôi và tạo mã chết khó kiểm thử.
- **Đề xuất khắc phục:** Thay đổi chữ ký của `showOwner` để tiếp nhận trực tiếp thực thể đã nạp từ model:
  ```java
  @GetMapping("/owners/{ownerId}")
  public ModelAndView showOwner(@ModelAttribute("owner") Owner owner) {
      ModelAndView mav = new ModelAndView("owners/ownerDetails");
      mav.addObject(owner);
      return mav;
  }
  ```

---

### Smell 4: Ảo ảnh tác dụng phụ do cơ chế Spring Model Binding
- **Vị trí:** [`PetController.java:186-200`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/PetController.java#L186-L200)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  186: 	private void updatePetDetails(Owner owner, Pet pet) {
  187: 		Integer id = pet.getId();
  188: 		Assert.state(id != null, "'pet.getId()' must not be null");
  189: 		Pet existingPet = owner.getPet(id);
  190: 		if (existingPet != null) {
  191: 			// Update existing pet's properties
  192: 			existingPet.setName(pet.getName());
  193: 			existingPet.setBirthDate(pet.getBirthDate());
  194: 			existingPet.setType(pet.getType());
  195: 		}
  196: 		else {
  197: 			owner.addPet(pet);
  198: 		}
  199: 		this.owners.saveAndFlush(owner);
  200: 	}
  ```
- **Mô tả kỹ thuật:**
  - Logic phương thức được viết theo tư duy thủ tục: coi `pet` là một DTO tách rời mang dữ liệu cần copy sang `existingPet`.
  - Nhưng trong kiến trúc Spring MVC, `findPet` đã nạp chính thực thể trong `Owner` và DataBinder đã mutate trực tiếp lên nó. Việc coi `pet` và `existingPet` là hai đối tượng tách biệt trong Controller là một sự sai lệch mô hình (Mental Model Mismatch).
  - Hậu quả: Dẫn tới hiện tượng "Ảo ảnh kiểm thử" (Testing Illusion) — kiểm thử bằng `MockMvc` hoàn toàn mù trước các đột biến xóa dòng 192–194.
- **Mức độ ảnh hưởng:** **Nghiêm trọng về thiết kế (Architectural Inconsistency)** — Vi phạm nguyên lý hướng đối tượng (Tell, Don't Ask) và che giấu lỗi kiểm thử.
- **Đề xuất khắc phục:** Đẩy nghiệp vụ cập nhật vào bên trong domain entity `Owner` hoặc `Pet`: `existingPet.updateDetails(petDto)`.

---

### Smell 5: Magic Number và Hardcoding trong phân trang
- **Vị trí:** [`OwnerController.java:141-146`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L141-L146)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  141: 	private Page<Owner> findPaginatedForOwnersLastName(int page, String lastname) {
  142: 		int pageSize = 5; // <-- SMELL: Hardcoded magic number
  143: 		int validatedPage = Math.max(page, 1);
  144: 		Pageable pageable = PageRequest.of(validatedPage - 1, pageSize);
  145: 		return owners.findByLastNameStartingWith(lastname, pageable);
  146: 	}
  ```
- **Mô tả kỹ thuật:**
  - Kích thước trang `pageSize = 5` bị fix cứng trực tiếp bằng hằng số nguyên (magic number).
  - Phép chuyển đổi chỉ số trang `validatedPage - 1` là nguồn gốc của lỗi lệch 1 đơn vị (Off-by-one). Khi PIT đổi `- 1` thành `+ 1`, bộ test baseline không bắt được do repository mock chấp nhận mọi `Pageable`.
- **Mức độ ảnh hưởng:** **Thấp (Maintainability Smell)** — Giảm tính linh hoạt khi cần cấu hình giao diện.
- **Đề xuất khắc phục:** Khai báo hằng số `private static final int DEFAULT_PAGE_SIZE = 5;` hoặc đưa vào `application.properties` với `@Value("${petclinic.page-size:5}")`.

---

### Smell 6: Khớp chuỗi ngoại lệ CSDL đặc thù (Tight Coupling to DB Vendor)
- **Vị trí:** [`PetController.java:202-205`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/PetController.java#L202-L205)
- **Trích dẫn mã nguồn thực tế:**
  ```java
  202: 	private boolean isDuplicatePetNameViolation(DataIntegrityViolationException ex) {
  203: 		String message = ex.getMessage();
  204: 		return message != null && message.toLowerCase().contains("unique_owner_pet_name");
  205: 	}
  ```
- **Mô tả kỹ thuật:**
  - Phương thức nhận biết trùng tên thú cưng bằng cách tìm kiếm chuỗi con `"unique_owner_pet_name"` trong thông điệp ngoại lệ của Hibernate/Spring Data.
  - Chuỗi thông điệp này phụ thuộc hoàn toàn vào hệ quản trị CSDL bên dưới (H2 format khác MySQL, PostgreSQL format khác Oracle). Khi chạy trên CSDL thật ở môi trường staging/production, format ngoại lệ có thể bị thay đổi hoặc mã hóa, khiến phương thức trả về `false` sai lầm và làm sập ứng dụng với lỗi HTTP 500 thay vì hiển thị lỗi binding.
- **Mức độ ảnh hưởng:** **Trung bình (Portability & Fragility Smell)** — Mã nguồn dễ vỡ khi thay đổi hoặc nâng cấp database engine.
- **Đề xuất khắc phục:** Thực hiện kiểm tra trùng lặp chủ động ở tầng service hoặc validation annotation (`@UniquePetName`) trước khi gọi lệnh persist, hoặc sử dụng `SQLExceptionTranslator` chuẩn của Spring để phân giải mã lỗi SQL State chuẩn.

---

## 5. TỔNG KẾT VÀ BÀI HỌC KINH NGHIỆM

Quá trình phân tích RCA trên 64 mutants sống sót của PetClinic mang lại ba bài học kinh nghiệm sâu sắc cho quy trình đảm bảo chất lượng phần mềm:

1. **Vạch trần "Ảo giác an toàn" của Line Coverage:** Baseline đạt tới **96.80% (~97%) độ bao phủ dòng** nhưng điểm đột biến thực tế chỉ đạt **67.18%**. Hơn 32% đột biến nguy hiểm lọt lưới hoàn toàn dù dòng mã có chạy qua. Độ bao phủ dòng chỉ chứng minh mã có được thực thi, chỉ có Mutation Testing mới chứng minh mã có được kiểm tra (tested).
2. **Cạm bẫy của MockMvc và Framework Aliasing:** Khung kiểm thử web (`MockMvc`) rất mạnh mẽ cho kiểm thử tích hợp HTTP, nhưng lại che giấu các lỗi cập nhật thực thể do cơ chế tự động ghi đè của DataBinder. Cần kết hợp hài hòa giữa **Framework Slice Test** và **Pure POJO Unit Test** để bảo vệ toàn diện các tác dụng phụ.
3. **Sức mạnh của Bảng quyết định và Kiểm thử biên:** 42.19% mutants sống sót xuất phát từ việc thiếu Bảng quyết định cho các biểu thức logic phức tạp, và 21.88% từ việc thiếu kiểm chứng phương thức void. Việc áp dụng bài bản các kỹ thuật kiểm thử hộp trắng kinh điển (BVA, Decision Table, State Verification) là chìa khóa duy nhất để nâng Mutation Score từ 67% lên tiệm cận tuyệt đối 98.46%.
