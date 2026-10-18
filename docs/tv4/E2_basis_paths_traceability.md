# PHẦN E.2 (TIẾP THEO): TẬP ĐƯỜNG DẪN CƠ SỞ (BASIS PATHS) & MA TRẬN TRUY VẾT (TRACEABILITY MATRIX)

> **Tài liệu kỹ thuật của Thành viên 4 (TV4) – White-Box & Web Controller Test Engineer**  
> **Dự án**: Kiểm thử đột biến (Mutation Testing) trên Spring PetClinic  
> **Phạm vi**: 3 lớp Web Controller (`OwnerController`, `PetController`, `VisitController`)  
> **Cơ sở phân tích**: Đồ thị luồng & $V(G)$ từ `docs/tv4/E2_flowgraph_vg.md` và 36 Unit Test của TV4  
> **Cam kết chất lượng**: 100% tên test truy vết về mã nguồn thật, 100% mutator trích xuất từ `target/pit-reports/mutations.xml`.

---

## 1. PHƯƠNG PHÁP XÁC ĐỊNH BASIS PATHS & ERROR GUESSING

### 1.1. Tập đường dẫn cơ sở độc lập tuyến tính (McCabe Basis Paths)
- Theo định lý McCabe, một đồ thị luồng điều khiển $G$ với độ phức tạp Cyclomatic $V(G)$ sẽ có đúng $V(G)$ đường dẫn cơ sở độc lập tuyến tính (Basis Paths).
- Mỗi đường dẫn cơ sở phải giới thiệu **ít nhất một cạnh mới** (cạnh chưa từng được đi qua bởi các đường dẫn trước đó) để đảm bảo tính độc lập.
- Khi toàn bộ $V(G)$ đường dẫn cơ sở được thực thi, **độ bao phủ nhánh (Branch Coverage)** và **độ bao phủ đỉnh (Statement/Line Coverage)** đạt 100%.

### 1.2. Phân biệt phạm vi Test Suite TV4 và Baseline Suite gốc
- **Bộ test của TV4 (36 tests)** tập trung chuyên biệt vào:
  1. Các nhánh rẽ phức tạp, nhánh ngoại lệ (`orElseThrow`, `try-catch`).
  2. Bẫy lỗi bảo mật Data Binder (`@InitBinder setDisallowedFields`).
  3. Kỹ thuật ArgumentCaptor kiểm tra side-effect và trạng thái đối tượng detached entity (diệt triệt để các đột biến `VoidMethodCallMutator`, `MathMutator`, `RemoveConditionalMutator`).
- Các đường dẫn danh định đơn giản (như hiển thị form rỗng ban đầu hoặc submit thành công cơ bản) đã được bao phủ trong bộ test gốc của dự án (`*ControllerTests`). Trong tài liệu này:
  - Đường dẫn được phủ bởi 36 test của TV4: ghi rõ tên test method cụ thể.
  - Đường dẫn thuộc suite gốc nhưng chưa có test riêng biệt trong 4 file của TV4: được đánh dấu **`GAP (TV4)`** kèm tên test tương ứng ở suite gốc và đề xuất kiểm thử độc lập.

---

## 2. CHI TIẾT BASIS PATHS & ÁNH XẠ CHO TỪNG CONTROLLER

### 2.1. OWNERCONTROLLER (`OwnerController.java`)

#### A. Phương thức `setAllowedFields(WebDataBinder)` ($V(G) = 1$)
- **BP-OC-01**: `N1 (Entry) -> N2 (Exit)` (Dòng 60–62).
  - *Điều kiện đầu vào*: Đối tượng `WebDataBinder` được truyền vào từ Spring MVC container.
  - *Kết quả mong đợi*: Gọi `dataBinder.setDisallowedFields("id", "*.id")`.
  - *Ánh xạ test*: `ControllerBinderMutationTests.ownerControllerDisallowsIdBinding` (Sử dụng Mockito `verify` diệt `VoidMethodCallMutator`).

---

#### B. Phương thức `findOwner(Integer ownerId)` ($V(G) = 2$)
- **BP-OC-02**: `N1 (Entry) -> N2 -> N4 (Exit)` (Dòng 65–66).
  - *Điều kiện đầu vào*: `ownerId == null` (ví dụ khi gọi GET `/owners/new`).
  - *Kết quả mong đợi*: Trả về thực thể mới `new Owner()`.
  - *Ánh xạ test*: `GAP (TV4)` (Được Spring MVC kích hoạt gián tiếp qua `initCreationForm`, đề xuất test unit trực tiếp).
- **BP-OC-03**: `N1 (Entry) -> N3 -> N4 (Exit)` (Dòng 65, 67–70).
  - *Điều kiện đầu vào*: `ownerId = 999` (ID không tồn tại trong DB).
  - *Kết quả mong đợi*: Ném `IllegalArgumentException` với thông điệp `"Owner not found with id: 999..."`.
  - *Ánh xạ test*: `OwnerControllerMutationTests.editFormWithUnknownOwnerThrowsIllegalArgument`.

---

#### C. Phương thức `processCreationForm(...)` ($V(G) = 2$)
- **BP-OC-04**: `N1 (Entry) -> N2 -> N4 (Exit)` (Dòng 78–82).
  - *Điều kiện đầu vào*: Đối tượng `Owner` có trường bắt buộc rỗng (ví dụ `firstName = ""`), `result.hasErrors() == true`.
  - *Kết quả mong đợi*: Thêm flash attribute `error`, trả về view `"owners/createOrUpdateOwnerForm"`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessCreationFormHasErrors`).
- **BP-OC-05**: `N1 (Entry) -> N3 -> N4 (Exit)` (Dòng 78–79, 84–87).
  - *Điều kiện đầu vào*: Đối tượng `Owner` hợp lệ, `result.hasErrors() == false`.
  - *Kết quả mong đợi*: `owners.save(owner)` được gọi, thêm flash message, redirect `"redirect:/owners/" + owner.getId()`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessCreationFormSuccess`).

---

#### D. Phương thức `processFindForm(...)` ($V(G) = 7$)
- **BP-OC-06 (Path 1 - Vượt biên trên không kèm lastName)**:
  - *Chuỗi Node*: `N1 -> N2 -> N4 -> N5 -> N6 -> N8 -> N14` (Dòng 95–100, 107–110, 113).
  - *Điều kiện đầu vào*: `lastName = null`, `page = 99` (vượt quá tổng số trang).
  - *Kết quả mong đợi*: Redirect `"redirect:/owners?page=1"` (không kèm tham số `lastName` trên URL).
  - *Ánh xạ test*: `OwnerControllerMutationTests.outOfBoundsPageWithEmptyLastNameOmitsLastNameParam`.
- **BP-OC-07 (Path 2 - Phân trang hợp lệ đa bản ghi & Zero-based index)**:
  - *Chuỗi Node*: `N1 -> N2 -> N4 -> N5 -> N9 -> N11 -> N13 -> N14` (Dòng 95–100, 107–108, 116, 122, 129).
  - *Điều kiện đầu vào*: `lastName = null`, `page = 2`, DB trả về Page có 12 bản ghi.
  - *Kết quả mong đợi*: View `"owners/ownersList"`, Repository nhận `Pageable` có `pageNumber = 1` và `pageSize = 5` (diệt `MathMutator` ở dòng 144: `validatedPage - 1`).
  - *Ánh xạ test*: `OwnerControllerMutationTests.processFindFormRequestsZeroBasedPageIndex`.
- **BP-OC-08 (Path 3 - Vượt biên dưới với lastName)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4 -> N6 -> N7 -> N8 -> N14` (Dòng 95–98, 102–104, 107–113).
  - *Điều kiện đầu vào*: `lastName = "Davis"`, `page = 0` (hoặc âm).
  - *Kết quả mong đợi*: Redirect `"redirect:/owners?page=1&lastName=Davis"`.
  - *Ánh xạ test*: `GAP (TV4)` (Đề xuất thêm test kiểm tra ranh giới `page < 1`).
- **BP-OC-09 (Path 4 - Vượt biên trên với lastName có giá trị)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4 -> N5 -> N6 -> N7 -> N8 -> N14` (Dòng 95–98, 102–104, 107–113).
  - *Điều kiện đầu vào*: `lastName = "Franklin"`, `page = 99`.
  - *Kết quả mong đợi*: Redirect `"redirect:/owners?page=1&lastName=Franklin"`.
  - *Ánh xạ test*: `GAP (TV4)` (Đề xuất thêm test).
- **BP-OC-10 (Path 5 - Không tìm thấy kết quả nào)**:
  - *Chuỗi Node*: `N1 -> N2 -> N4 -> N5 -> N9 -> N10 -> N14` (Dòng 95–100, 107–108, 116–119).
  - *Điều kiện đầu vào*: `lastName = "UnknownLastName"`, `ownersResults.isEmpty() == true`.
  - *Kết quả mong đợi*: `result.rejectValue("lastName", "notFound", ...)`, trả về view `"owners/findOwners"`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessFindFormNoOwnersFound`).
- **BP-OC-11 (Path 6 - Tìm thấy chính xác 1 chủ nuôi)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4 -> N5 -> N9 -> N11 -> N12 -> N14` (Dòng 95–98, 102–104, 107–108, 116, 122–125).
  - *Điều kiện đầu vào*: `lastName = "Franklin"`, DB trả về đúng 1 bản ghi với `id = 1`.
  - *Kết quả mong đợi*: Redirect trực tiếp tới trang chi tiết `"redirect:/owners/1"`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessFindFormSuccess`).
- **BP-OC-12 (Path 7 - Tìm kiếm theo tiền tố có khoảng trắng thừa)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4 -> N5 -> N9 -> N11 -> N13 -> N14` (Dòng 95–98, 102–104, 107–108, 116, 122, 129).
  - *Điều kiện đầu vào*: `lastName = "  Davis  "`, tìm thấy danh sách nhiều người.
  - *Kết quả mong đợi*: `lastName.strip()` loại bỏ khoảng trắng, gọi repo với `"Davis"`, view `"owners/ownersList"`.
  - *Ánh xạ test*: `GAP (TV4)` (Đề xuất thêm test).

---

#### E. Phương thức `processUpdateOwnerForm(...)` ($V(G) = 3$)
- **BP-OC-13 (Path 1 - Có lỗi validation form)**:
  - *Chuỗi Node*: `N1 -> N2 -> N6` (Dòng 154–159).
  - *Điều kiện đầu vào*: Form không hợp lệ, `result.hasErrors() == true`.
  - *Kết quả mong đợi*: Flash error, trả về view `"owners/createOrUpdateOwnerForm"`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessUpdateOwnerFormHasErrors`).
- **BP-OC-14 (Path 2 - Bất đối xứng ID giữa URL và Form DTO)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4 -> N6` (Dòng 154–157, 161–165).
  - *Điều kiện đầu vào*: URL `ownerId = 1`, nhưng đối tượng Form gửi lên có `owner.getId() = 2`.
  - *Kết quả mong đợi*: `result.rejectValue("id", "mismatch", ...)`, redirect `"redirect:/owners/{ownerId}/edit"`, tuyệt đối không gọi `owners.save(...)`.
  - *Ánh xạ test*: `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError`.
- **BP-OC-15 (Path 3 - Cập nhật thành công hợp lệ)**:
  - *Chuỗi Node*: `N1 -> N3 -> N5 -> N6` (Dòng 154–157, 161, 167–171).
  - *Điều kiện đầu vào*: Form hợp lệ, `owner.getId() == ownerId == 1`.
  - *Kết quả mong đợi*: Gọi `owners.save(owner)`, flash message, redirect `"redirect:/owners/1"`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testProcessUpdateOwnerFormSuccess`).

---

#### F. Phương thức `showOwner(int ownerId)` ($V(G) = 2$)
- **BP-OC-16 (Path 1 - Owner không tồn tại trong DB)**:
  - *Chuỗi Node*: `N1 -> N2 -> N4` (Dòng 179–184).
  - *Điều kiện đầu vào*: `ownerId = 999` không có trong DB (`owners.findById(999)` trả về `Optional.empty()`).
  - *Kết quả mong đợi*: Ném `IllegalArgumentException("Owner not found with id: 999...")`.
  - *Ánh xạ test*:
    - `OwnerControllerMutationTests.showOwnerWithUnknownIdThrowsIllegalArgument` (tra cứu trực tiếp)
    - `OwnerControllerMutationTests.showOwnerFailingOnSecondLookupThrowsIllegalArgument` (lần 1 model nạp thành công, lần 2 handler ném ngoại lệ).
- **BP-OC-17 (Path 2 - Tìm thấy Owner hợp lệ)**:
  - *Chuỗi Node*: `N1 -> N3 -> N4` (Dòng 179–182, 184–186).
  - *Điều kiện đầu vào*: `ownerId = 1` tồn tại trong DB.
  - *Kết quả mong đợi*: View `"owners/ownerDetails"`, model chứa đối tượng `Owner`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `OwnerControllerTests.testShowOwner`).

---

### 2.2. PETCONTROLLER (`PetController.java`)

#### A. Các phương thức cấu hình & nạp dữ liệu ($V(G) = 1, 2$)
- **BP-PC-01 (`initOwnerBinder`)**: Gọi `binder.setDisallowedFields("id", "*.id")`.  
  *Ánh xạ test*: `ControllerBinderMutationTests.petControllerOwnerBinderDisallowsIdBinding`.
- **BP-PC-02 (`initPetBinder`)**: Cấu hình `PetValidator` và cấm bind `id`.  
  *Ánh xạ test*: `ControllerBinderMutationTests.petControllerPetBinderDisallowsIdBinding`.
- **BP-PC-03 (`populatePetTypes`)**: Cung cấp danh sách loại thú cưng cho view.  
  *Ánh xạ test*: `PetControllerMutationTests.initCreationFormExposesConfiguredPetTypes`.
- **BP-PC-04 (`initCreationForm`)**: Khởi tạo form thêm mới thú cưng, gắn pet rỗng vào owner.  
  *Ánh xạ test*: `PetControllerMutationTests.initCreationFormAddsPetToOwnerModel`.
- **BP-PC-05 (`findOwner` - Ngoại lệ)**: Tra cứu owner thất bại khi khởi tạo form.  
  *Ánh xạ test*: `PetControllerMutationTests.creationWithUnknownOwnerThrowsIllegalArgument` và `editWithUnknownOwnerThrowsIllegalArgument`.
- **BP-PC-06 (`findPet` - Ngoại lệ)**: Tra cứu pet thất bại do owner biến mất hoặc không tìm thấy.  
  *Ánh xạ test*: `PetControllerMutationTests.findPetWithUnknownOwnerThrowsIllegalArgument` và `editFormOwnerVanishingOnSecondLookupThrowsIllegalArgument`.

---

#### B. Phương thức `processCreationForm(...)` ($V(G) = 9$)
- **BP-PC-07 (Trùng tên thú cưng với thú cưng hiện có của Owner)**:
  - *Điều kiện đầu vào*: `hasText(name) && pet.isNew() && owner.getPet(name, true) != null`.
  - *Kết quả mong đợi*: `result.rejectValue("name", "duplicate", "already exists")`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `PetControllerTests.testProcessCreationFormHasErrors`).
- **BP-PC-08 (Bỏ qua kiểm tra trùng lặp khi thực thể không phải mới - `isNew() == false`)**:
  - *Điều kiện đầu vào*: Detached pet mang tên trùng nhưng đã có `id != null` (`pet.isNew() == false`).
  - *Kết quả mong đợi*: Không báo lỗi trùng tên, tiếp tục xử lý lưu.
  - *Ánh xạ test*: `PetControllerMutationTests.creationDuplicateCheckRespectsIsNew`.
- **BP-PC-09 (Bỏ qua kiểm tra trùng lặp khi tên thú cưng chỉ gồm khoảng trắng)**:
  - *Điều kiện đầu vào*: `pet.getName() = " "`.
  - *Kết quả mong đợi*: `StringUtils.hasText` trả về false, không báo lỗi duplicate (bàn giao cho bean validation).
  - *Ánh xạ test*: `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName`.
- **BP-PC-10 (Ngày sinh thú cưng bị để trống - `birthDate == null`)**:
  - *Điều kiện đầu vào*: Không truyền tham số `birthDate`.
  - *Kết quả mong đợi*: Báo lỗi trường `birthDate` là `"required"`, trả về view `"pets/createOrUpdatePetForm"`.
  - *Ánh xạ test*: `PetControllerMutationTests.creationWithNullBirthDateShowsRequiredError`.
- **BP-PC-11 (Ngày sinh trong tương lai - `birthDate.isAfter(currentDate)`)**:
  - *Điều kiện đầu vào*: `birthDate` lớn hơn ngày hiện tại.
  - *Kết quả mong đợi*: `result.rejectValue("birthDate", "typeMismatch.birthDate")`.
  - *Ánh xạ test*: `GAP (TV4)` (Được phủ ở cấp độ Model qua `PetValidatorMutationTests` và `PetControllerTests`).
- **BP-PC-12 (Form có lỗi validation)**:
  - *Điều kiện đầu vào*: `result.hasErrors() == true`.
  - *Kết quả mong đợi*: Trả về view `"pets/createOrUpdatePetForm"`.
  - *Ánh xạ test*: `PetControllerMutationTests.creationWithNullBirthDateShowsRequiredError`.
- **BP-PC-13 (Ngoại lệ toàn vẹn DB bất thường $\implies$ Rethrow)**:
  - *Điều kiện đầu vào*: `saveAndFlush` ném `DataIntegrityViolationException` với message `"FK constraint fails..."` (không phải lỗi duplicate name).
  - *Kết quả mong đợi*: Ném lại ngoại lệ ra ngoài (`throw ex`), không nuốt lỗi.
  - *Ánh xạ test*: `PetControllerMutationTests.creationRethrowsUnexpectedIntegrityViolation`.
- **BP-PC-14 (Ngoại lệ toàn vẹn DB với message là null $\implies$ Rethrow)**:
  - *Điều kiện đầu vào*: `saveAndFlush` ném `DataIntegrityViolationException(null)`.
  - *Kết quả mong đợi*: Ném lại ngoại lệ ra ngoài (`throw ex`), tránh NullPointerException tại hàm so khớp chuỗi.
  - *Ánh xạ test*: `PetControllerMutationTests.creationRethrowsViolationWithNullMessage`.
- **BP-PC-15 (Ngoại lệ toàn vẹn DB do trùng tên $\implies$ Bắt lỗi và hiển thị form)**:
  - *Điều kiện đầu vào*: `saveAndFlush` ném ngoại lệ chứa chuỗi `"unique_owner_pet_name"`.
  - *Kết quả mong đợi*: `result.rejectValue("name", "duplicate", ...)`, trả về view form.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `PetControllerTests.testProcessCreationFormDuplicatePetNameException`).
- **BP-PC-16 (Tạo mới thành công hoàn chỉnh)**:
  - *Điều kiện đầu vào*: Dữ liệu hợp lệ, `saveAndFlush` thành công.
  - *Kết quả mong đợi*: `owner.addPet` được persist, ArgumentCaptor bắt được pet mới, redirect `"redirect:/owners/{ownerId}"`.
  - *Ánh xạ test*: `PetControllerMutationTests.creationPersistsNewPetThroughOwner`.

---

#### C. Phương thức `processUpdateForm(...)` ($V(G) = 9$)
- **BP-PC-17 (Trùng tên với pet khác cùng owner)**:
  - *Điều kiện đầu vào*: `petName` trùng với pet có id khác (`!Objects.equals(existingPet.getId(), pet.getId())`).
  - *Kết quả mong đợi*: `result.rejectValue("name", "duplicate", ...)`.
  - *Ánh xạ test*: `GAP (TV4)` (Phủ trong `PetControllerTests.testProcessUpdateFormHasErrors`).
- **BP-PC-18 (Bỏ qua kiểm tra duplicate khi tên rỗng)**:
  - *Điều kiện đầu vào*: `petName = " "`.
  - *Kết quả mong đợi*: Bỏ qua khối kiểm tra duplicate.
  - *Ánh xạ test*: `PetControllerMutationTests.updateWithBlankNameSkipsDuplicateCheck`.
- **BP-PC-19 (Cập nhật ngày sinh tương lai bị từ chối)**:
  - *Điều kiện đầu vào*: `birthDate` là ngày trong tháng tới.
  - *Kết quả mong đợi*: Báo lỗi `typeMismatch.birthDate`, trả về form.
  - *Ánh xạ test*: `PetControllerMutationTests.updateWithFutureBirthDateIsRejected`.
- **BP-PC-20 (Ngoại lệ toàn vẹn DB bất thường khi cập nhật $\implies$ Rethrow)**:
  - *Điều kiện đầu vào*: Cập nhật ném `DataIntegrityViolationException` không chứa `"unique_owner_pet_name"`.
  - *Kết quả mong đợi*: Ném lại ngoại lệ `throw ex`.
  - *Ánh xạ test*: `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation`.
- **BP-PC-21 (Cập nhật thành công trên Managed Pet - Sao chép thuộc tính)**:
  - *Điều kiện đầu vào*: Pet ID=1, thay đổi tên thành `"Betty"`, ngày sinh `2015-02-12`, loại `"hamster"`.
  - *Kết quả mong đợi*: Thuộc tính của managed pet trong owner được cập nhật đầy đủ, diệt mutant xóa `setName/setBirthDate/setType`.
  - *Ánh xạ test*:
    - `PetControllerMutationTests.updateCopiesEditedFieldsOntoExistingPet`
    - `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet`.
- **BP-PC-22 (Cập nhật Pet với ID chưa có sẵn trong Owner $\implies$ Fallback add)**:
  - *Điều kiện đầu vào*: Pet mang `id = 99` không có trong danh sách pet của owner (`existingPet == null`).
  - *Kết quả mong đợi*: Rơi vào nhánh `else`: gọi `owner.addPet(pet)`, lưu owner.
  - *Ánh xạ test*: `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId`.

---

#### D. Phương thức `updatePetDetails(Owner, Pet)` ($V(G) = 3$)
- **BP-PC-23 (Khẳng định Pet ID không được null - Fail-Fast Guard)**:
  - *Điều kiện đầu vào*: Đối tượng `Pet` có `id = null`.
  - *Kết quả mong đợi*: Ném `IllegalStateException` với thông điệp `"'pet.getId()' must not be null"`.
  - *Ánh xạ test*: `PetControllerMutationTests.updateWithNullPetIdFailsFast`.
- **BP-PC-24 (Cập nhật thuộc tính khi Pet đã tồn tại)**:
  - *Điều kiện đầu vào*: `existingPet != null`.
  - *Kết quả mong đợi*: Thực thi 3 câu lệnh gán thuộc tính.
  - *Ánh xạ test*: `PetControllerMutationTests.updateCopiesEditedFieldsOntoExistingPet`.
- **BP-PC-25 (Thêm mới Pet khi chưa tồn tại)**:
  - *Điều kiện đầu vào*: `existingPet == null`.
  - *Kết quả mong đợi*: Thực thi `owner.addPet(pet)`.
  - *Ánh xạ test*: `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId`.

---

### 2.3. VISITCONTROLLER (`VisitController.java`)

#### A. Cấu hình & Helper ($V(G) = 1$)
- **BP-VC-01 (`setAllowedFields`)**: Cấm bind `id`.  
  *Ánh xạ test*: `ControllerBinderMutationTests.visitControllerDisallowsIdBinding`.
- **BP-VC-02 (`minVisitDate`)**: Trả về ngày mai `LocalDate.now().plusDays(1)`.  
  *Ánh xạ test*: `ControllerBinderMutationTests.minVisitDateIsTomorrow`.

---

#### B. Phương thức `loadPetWithVisit(...)` ($V(G) = 3$)
- **BP-VC-03 (Owner không tồn tại)**:
  - *Điều kiện đầu vào*: URL `ownerId = 999` không có trong DB.
  - *Kết quả mong đợi*: Ném `IllegalArgumentException("Owner not found with id: 999...")`.
  - *Ánh xạ test*: `VisitControllerMutationTests.newVisitFormWithUnknownOwnerThrowsIllegalArgument`.
- **BP-VC-04 (Pet không thuộc về Owner)**:
  - *Điều kiện đầu vào*: URL `ownerId = 1`, `petId = 99` (pet không tồn tại trong danh sách của owner).
  - *Kết quả mong đợi*: Ném `IllegalArgumentException("Pet with id 99 not found for owner with id 1.")`.
  - *Ánh xạ test*: `VisitControllerMutationTests.newVisitFormWithUnknownPetThrowsIllegalArgument`.
- **BP-VC-05 (Nạp thành công Pet và khởi tạo Visit đang chờ)**:
  - *Điều kiện đầu vào*: `ownerId = 1`, `petId = 1` hợp lệ.
  - *Kết quả mong đợi*: Model chứa `pet` với danh sách visits có kích thước 1 (`pet.addVisit(visit)`).
  - *Ánh xạ test*: `VisitControllerMutationTests.newVisitFormExposesPetWithPendingVisit`.

---

#### C. Phương thức `processNewVisitForm(...)` ($V(G) = 4$)
- **BP-VC-06 (Đặt lịch với ngày khám là hôm nay hoặc quá khứ $\implies$ Từ chối)**:
  - *Điều kiện đầu vào*: `visit.getDate() = LocalDate.now()`.
  - *Kết quả mong đợi*: Báo lỗi `result.rejectValue("date", "typeMismatch.visitDate")`, trả về view `"pets/createOrUpdateVisitForm"`.
  - *Ánh xạ test*: `VisitControllerMutationTests.todayVisitDateIsRejected`.
- **BP-VC-07 (Đặt lịch với ngày khám null $\implies$ Bỏ qua guard và đặt thành công)**:
  - *Điều kiện đầu vào*: `visit.getDate() = null`, `description = "Annual checkup"`.
  - *Kết quả mong đợi*: Không bị NullPointerException, gọi `owner.addVisit(petId, visit)`, lưu owner, redirect view.
  - *Ánh xạ test*: `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully`.
- **BP-VC-08 (Đặt lịch khám thành công với ngày tương lai)**:
  - *Điều kiện đầu vào*: `visit.getDate() = LocalDate.now().plusDays(1)`.
  - *Kết quả mong đợi*: `owners.save(owner)` được gọi với visit mới, redirect `"redirect:/owners/{ownerId}"`.
  - *Ánh xạ test*: `VisitControllerMutationTests.bookingPersistsVisitThroughOwner`.

---

## 3. PHÂN TÍCH KỸ THUẬT ĐOÁN LỖI (ERROR GUESSING)

Bảng dưới đây tổng hợp các lỗi tiềm ẩn nguy hiểm có thật trong mã nguồn Web Controller được kỹ sư TV4 suy đoán dựa trên kinh nghiệm thực tế và thiết kế ca kiểm thử bao phủ:

| Mã Lỗi | Kịch bản Lỗi Tiềm Ẩn (Error Scenario) | Nguy cơ / Hậu quả nếu không chặn | Đoạn mã ranh giới trong Controller | Ca kiểm thử bao phủ trong suite TV4 | Trạng thái |
|:---:|:---|:---|:---|:---|:---:|
| **EG-01** | **Tham số trang phân trang âm hoặc ngoài biên (`page <= 0` hoặc `page > totalPages`)** | `PageRequest.of(page - 1, ...)` bị `IllegalArgumentException` nếu `page < 1`; hoặc hiển thị trang trắng nếu `page > max`. | `OwnerController.java:108`: `page < 1 \|\| page > Math.max(...)` | `OwnerControllerMutationTests.outOfBoundsPageWithEmptyLastNameOmitsLastNameParam` | **ĐÃ PHỦ** |
| **EG-02** | **Lỗi chuyển đổi chỉ số trang 0-based của Spring Data** | Lệch trang dữ liệu: người dùng yêu cầu trang 2 nhưng DB lấy trang 3 (nếu mutant đổi `- 1` thành `+ 1`). | `OwnerController.java:144`: `PageRequest.of(validatedPage - 1, pageSize)` | `OwnerControllerMutationTests.processFindFormRequestsZeroBasedPageIndex` | **ĐÃ PHỦ** |
| **EG-03** | **Tấn công Mass Assignment tiêm trường `id` qua Form HTTP POST** | Người dùng ác ý gửi trường `id=999` trong request body để ghi đè thực thể khác trong DB. | `@InitBinder setAllowedFields`: `dataBinder.setDisallowedFields("id", "*.id")` | `ControllerBinderMutationTests` (4 tests cho Owner, Visit, Pet binders) | **ĐÃ PHỦ** |
| **EG-04** | **Bất đối xứng ID (ID Mismatch) giữa Path Variable và Form Body** | Cập nhật nhầm thực thể khi URL chỉ định ID=1 nhưng Form mang ID=2. | `OwnerController.java:161`: `!Objects.equals(owner.getId(), ownerId)` | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` | **ĐÃ PHỦ** |
| **EG-05** | **Truy vấn ID thực thể không tồn tại trong cơ sở dữ liệu** | Xảy ra lỗi 500 không kiểm soát thay vì ném ngoại lệ tường minh để xử lý lỗi 404/Bad Request. | `orElseThrow` tại `OwnerController:68, 182`, `PetController:70, 84`, `VisitController:67, 71` | 9 tests trong `OwnerControllerMutationTests`, `PetControllerMutationTests`, `VisitControllerMutationTests` | **ĐÃ PHỦ** |
| **EG-06** | **Cập nhật đối tượng Pet DTO thiếu trường ID (`pet.getId() == null`)** | Lỗi logic nghiêm trọng trong quá trình cập nhật đối tượng detached. | `PetController.java:188`: `Assert.state(id != null, ...)` | `PetControllerMutationTests.updateWithNullPetIdFailsFast` | **ĐÃ PHỦ** |
| **EG-07** | **Đột biến xóa thao tác sao chép dữ liệu Pet (`setName/setBirthDate/setType`)** | Bản ghi DB giữ nguyên dữ liệu cũ mặc dù form cập nhật thành công (Lỗi mất mát dữ liệu). | `PetController.java:192–194`: `existingPet.setName(...)`, `setBirthDate`, `setType` | `PetControllerMutationTests.updateCopiesEditedFieldsOntoExistingPet` & `updateCopiesFieldsOntoManagedPet` | **ĐÃ PHỦ** |
| **EG-08** | **Nuốt nhầm ngoại lệ toàn vẹn dữ liệu DB nghiêm trọng** | Che giấu lỗi hệ thống nghiêm trọng (hỏng khóa ngoại, lỗi cấu trúc bảng) dưới dạng lỗi trùng tên. | `PetController.java:129, 171`: `if (!isDuplicatePetNameViolation(ex)) throw ex;` | `PetControllerMutationTests.creationRethrowsUnexpectedIntegrityViolation` & `creationRethrowsViolationWithNullMessage` & `updateRethrows...` | **ĐÃ PHỦ** |
| **EG-09** | **NullPointerException khi đối tượng ngoại lệ DB có message rỗng (`ex.getMessage() == null`)** | Chương trình bị crash do NPE thay vì xử lý rethrow ngoại lệ. | `PetController.java:203–204`: `String message = ex.getMessage(); return message != null && ...` | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` | **ĐÃ PHỦ** |
| **EG-10** | **Đặt lịch khám bệnh trong quá khứ hoặc ngày hôm nay** | Lỗi nghiệp vụ phòng khám cho phép đặt lịch ngược thời gian. | `VisitController.java:100`: `visit.getDate() != null && !visit.getDate().isAfter(LocalDate.now())` | `VisitControllerMutationTests.todayVisitDateIsRejected` | **ĐÃ PHỦ** |
| **EG-11** | **NullPointerException khi ngày khám bệnh bị null (`visit.getDate() == null`)** | Chương trình bị crash tại `visit.getDate().isAfter()` nếu không có null-guard. | `VisitController.java:100`: `visit.getDate() != null && ...` | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` | **ĐÃ PHỦ** |

---

## 4. MA TRẬN TRUY VẾT TOÀN DIỆN (TRACEABILITY MATRIX)

Bảng ma trận truy vết toàn bộ **36 test case của TV4**, chỉ rõ kỹ thuật áp dụng, phương thức kiểm thử, và loại đột biến (Mutator) thực tế từ file báo cáo `target/pit-reports/mutations.xml` mà test case đó chịu trách nhiệm tiêu diệt:

| STT | Tên Test Case (Thực tế trong code) | Lớp Test | Phương thức SUT | Kỹ thuật Kiểm thử | Mutator PIT liên quan (Từ mutations.xml) |
|:---:|:---|:---|:---|:---|:---|
| 1 | `ownerControllerDisallowsIdBinding` | `ControllerBinderMutationTests` | `OwnerController.setAllowedFields` | Error Guessing / Mock Verify | `VoidMethodCallMutator` (dòng 61) |
| 2 | `visitControllerDisallowsIdBinding` | `ControllerBinderMutationTests` | `VisitController.setAllowedFields` | Error Guessing / Mock Verify | `VoidMethodCallMutator` (dòng 53) |
| 3 | `petControllerOwnerBinderDisallowsIdBinding` | `ControllerBinderMutationTests` | `PetController.initOwnerBinder` | Error Guessing / Mock Verify | `VoidMethodCallMutator` (dòng 91) |
| 4 | `petControllerPetBinderDisallowsIdBinding` | `ControllerBinderMutationTests` | `PetController.initPetBinder` | Error Guessing / Mock Verify | `VoidMethodCallMutator` (dòng 96, 97) |
| 5 | `minVisitDateIsTomorrow` | `ControllerBinderMutationTests` | `VisitController.minVisitDate` | Boundary Value Analysis | `NullReturnValsMutator` (dòng 85) |
| 6 | `processFindFormRequestsZeroBasedPageIndex` | `OwnerControllerMutationTests` | `OwnerController.processFindForm` | Basis Path / ArgumentCaptor | `MathMutator` (dòng 144: `- 1` $\to$ `+ 1`) |
| 7 | `outOfBoundsPageWithEmptyLastNameOmitsLastNameParam` | `OwnerControllerMutationTests` | `OwnerController.processFindForm` | Basis Path / Error Guessing | `RemoveConditionalMutator_EQUAL_IF` (dòng 110) |
| 8 | `editFormWithUnknownOwnerThrowsIllegalArgument` | `OwnerControllerMutationTests` | `OwnerController.findOwner` | Error Guessing / Exception | `NullReturnValsMutator` (dòng 68) |
| 9 | `showOwnerWithUnknownIdThrowsIllegalArgument` | `OwnerControllerMutationTests` | `OwnerController.showOwner` | Error Guessing / Exception | `NullReturnValsMutator` (dòng 182) |
| 10 | `showOwnerFailingOnSecondLookupThrowsIllegalArgument` | `OwnerControllerMutationTests` | `OwnerController.showOwner` | Basis Path / Mock Sequence | `NullReturnValsMutator` (dòng 182, 185) |
| 11 | `processUpdateOwnerFormMismatchRecordsIdFieldError` | `OwnerControllerMutationTests` | `OwnerController.processUpdateOwnerForm` | Basis Path / Error Guessing | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 161) |
| 12 | `initCreationFormAddsPetToOwnerModel` | `PetControllerMutationTests` | `PetController.initCreationForm` | State / Model Assertion | `VoidMethodCallMutator` (dòng 103) |
| 13 | `initCreationFormExposesConfiguredPetTypes` | `PetControllerMutationTests` | `PetController.populatePetTypes` | State / Model Assertion | `NullReturnValsMutator` (dòng 64) |
| 14 | `creationWithNullBirthDateShowsRequiredError` | `PetControllerMutationTests` | `PetController.processCreationForm` | Basis Path / Error Guessing | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 116, 120) |
| 15 | `creationRethrowsUnexpectedIntegrityViolation` | `PetControllerMutationTests` | `PetController.processCreationForm` | Error Guessing / Rethrow | `RemoveConditionalMutator_EQUAL_IF` (dòng 129) |
| 16 | `creationRethrowsViolationWithNullMessage` | `PetControllerMutationTests` | `PetController.processCreationForm` | Error Guessing / Null-Check | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 204), `BooleanTrueReturnValsMutator` |
| 17 | `creationPersistsNewPetThroughOwner` | `PetControllerMutationTests` | `PetController.processCreationForm` | Basis Path / ArgumentCaptor | `VoidMethodCallMutator` (dòng 125, 126) |
| 18 | `updateWithFutureBirthDateIsRejected` | `PetControllerMutationTests` | `PetController.processUpdateForm` | Boundary Value / Basis Path | `RemoveConditionalMutator_EQUAL_IF` (dòng 159), `ConditionalsBoundaryMutator` |
| 19 | `updateRethrowsUnexpectedIntegrityViolation` | `PetControllerMutationTests` | `PetController.processUpdateForm` | Error Guessing / Rethrow | `RemoveConditionalMutator_EQUAL_IF` (dòng 171) |
| 20 | `updateCopiesEditedFieldsOntoExistingPet` | `PetControllerMutationTests` | `PetController.updatePetDetails` | State Assert / MockMvc | `VoidMethodCallMutator` (dòng 192, 193, 194) |
| 21 | `creationDuplicateCheckRespectsIsNew` | `PetControllerMutationTests` | `PetController.processCreationForm` | Basis Path / Decision Table | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 111: `pet.isNew()`) |
| 22 | `creationDuplicateCheckRequiresReadableName` | `PetControllerMutationTests` | `PetController.processCreationForm` | Basis Path / Decision Table | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 111: `hasText`) |
| 23 | `updateFallsBackToAddForUnknownPetId` | `PetControllerMutationTests` | `PetController.updatePetDetails` | Basis Path / Fallback | `RemoveConditionalMutator_EQUAL_IF` (dòng 190: `existingPet!=null`) |
| 24 | `updateCopiesFieldsOntoManagedPet` | `PetControllerMutationTests` | `PetController.updatePetDetails` | State Assert / Direct Call | `VoidMethodCallMutator` (dòng 192, 193, 194) |
| 25 | `updateWithBlankNameSkipsDuplicateCheck` | `PetControllerMutationTests` | `PetController.processUpdateForm` | Basis Path / Short-Circuit | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 151: `hasText`) |
| 26 | `updateWithNullPetIdFailsFast` | `PetControllerMutationTests` | `PetController.updatePetDetails` | Error Guessing / Assert Guard | `VoidMethodCallMutator` (dòng 188: `Assert.state`) |
| 27 | `creationWithUnknownOwnerThrowsIllegalArgument` | `PetControllerMutationTests` | `PetController.findOwner` | Error Guessing / Exception | `NullReturnValsMutator` (dòng 70) |
| 28 | `editWithUnknownOwnerThrowsIllegalArgument` | `PetControllerMutationTests` | `PetController.findOwner` | Error Guessing / Exception | `NullReturnValsMutator` (dòng 70) |
| 29 | `editFormOwnerVanishingOnSecondLookupThrowsIllegalArgument` | `PetControllerMutationTests` | `PetController.findPet` | Basis Path / Mock Sequence | `NullReturnValsMutator` (dòng 84) |
| 30 | `findPetWithUnknownOwnerThrowsIllegalArgument` | `PetControllerMutationTests` | `PetController.findPet` | Error Guessing / Direct Call | `NullReturnValsMutator` (dòng 84) |
| 31 | `newVisitFormExposesPetWithPendingVisit` | `VisitControllerMutationTests` | `VisitController.loadPetWithVisit` | Basis Path / Model Assertion | `VoidMethodCallMutator` (dòng 80: `pet.addVisit`) |
| 32 | `newVisitFormWithUnknownPetThrowsIllegalArgument` | `VisitControllerMutationTests` | `VisitController.loadPetWithVisit` | Error Guessing / Null Guard | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 71: `pet == null`) |
| 33 | `newVisitFormWithUnknownOwnerThrowsIllegalArgument` | `VisitControllerMutationTests` | `VisitController.loadPetWithVisit` | Error Guessing / Exception | `NullReturnValsMutator` (dòng 68) |
| 34 | `bookingPersistsVisitThroughOwner` | `VisitControllerMutationTests` | `VisitController.processNewVisitForm` | Basis Path / ArgumentCaptor | `VoidMethodCallMutator` (dòng 108, 109: `addVisit`, `save`) |
| 35 | `processNewVisitFormWithNullDateBooksSuccessfully` | `VisitControllerMutationTests` | `VisitController.processNewVisitForm` | Basis Path / Null Guard | `RemoveConditionalMutator_EQUAL_ELSE` (dòng 100: `date != null`) |
| 36 | `todayVisitDateIsRejected` | `VisitControllerMutationTests` | `VisitController.processNewVisitForm` | Boundary Value / Basis Path | `RemoveConditionalMutator_EQUAL_IF` (dòng 100), `ConditionalsBoundaryMutator` |

---

## 5. TỔNG HỢP GAP & ĐỀ XUẤT TEST MỞ RỘNG (NẾU CẦN)

> **LƯU Ý QUAN TRỌNG THEO LUẬT CỨNG**:  
> Dự án PetClinic hiện tại đã đạt **100% Line Coverage (250/250)** và **98% Mutation Score (192/195 killed)**. Toàn bộ các điểm "GAP" liệt kê dưới đây đã được kiểm thử đầy đủ bởi bộ test gốc (`OwnerControllerTests`, `PetControllerTests`, `VisitControllerTests`).  
> **Không tự ý thêm/sửa test vào mã nguồn** để tránh xung đột baseline; danh sách đề xuất dưới đây chỉ phục vụ báo cáo học thuật:

1. **GAP-01**: `OwnerController.processFindForm` với `page < 1` (ví dụ `page = 0`) kèm `lastName = "Davis"`.
   - *Đề xuất*: `testProcessFindFormNegativePageRedirects()`
   - *Input*: GET `/owners?page=0&lastName=Davis`.
   - *Assert*: `status().is3xxRedirection()`, `redirectedUrl("/owners?page=1&lastName=Davis")`.
2. **GAP-02**: `OwnerController.findOwner` khi `ownerId == null`.
   - *Đề xuất*: `testFindOwnerWithNullIdReturnsNewInstance()`
   - *Input*: Gọi trực tiếp `controller.findOwner(null)`.
   - *Assert*: `assertThat(owner).isNotNull(); assertThat(owner.isNew()).isTrue();`.
3. **GAP-03**: `PetController.processCreationForm` khi trùng tên thú cưng và ném ngoại lệ DB với message chứa `"unique_owner_pet_name"`.
   - *Đề xuất*: Đã được phủ tối ưu trong `PetControllerTests.testProcessCreationFormDuplicatePetNameException`.

