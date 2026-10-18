# PHẦN F: THUYẾT MINH TEST HARNESS VÀ CHIẾN LƯỢC CÔ LẬP PHỤ THUỘC (MOCKING)

**Đề tài:** Đánh giá hiệu quả Mutation Testing bằng PIT trên Spring Boot PetClinic (K03 – R01)  
**Phạm vi phụ trách:** Thành viên 4 (TV4) – White-Box & Web Controller Test Engineer  
**Đối tượng SUT:** Các lớp Web Controller thuộc gói `org.springframework.samples.petclinic.owner.*` (`OwnerController`, `PetController`, `VisitController`)  
**Công cụ chính:** JUnit 5 (Jupiter), Spring Test Framework (`MockMvc`), Mockito 5 (`@MockitoBean`, `ArgumentCaptor`, `verify`), PIT 1.30.0.

---

## 1. KIẾN TRÚC TEST HARNESS: `@WebMvcTest` (MockMvc) VS. KHỞI TẠO TRỰC TIẾP CONTROLLER (UNIT THUẦN)

Trong quá trình thiết kế bộ kiểm thử diệt đột biến (Mutation-Killing Tests) cho tầng Web Controller, TV4 đã áp dụng kết hợp hai kiến trúc harness bổ trợ lẫn nhau thay vì chỉ dùng duy nhất một cách tiếp cận. Quyết định này xuất phát từ bản chất của Spring MVC và cơ chế sinh đột biến của PIT.

```
                           ┌────────────────────────────────────────────────────────┐
                           │          KIẾN TRÚC TEST HARNESS CỦA TV4                │
                           └────────────────────────────────────────────────────────┘
                                      │                                 │
                 ┌────────────────────┴───────────┐         ┌───────────┴────────────────────┐
                 ▼                                ▼         ▼                                ▼
    ┌───────────────────────────┐   ┌───────────────────────────┐   ┌────────────────────────────┐
    │  Spring Boot @WebMvcTest  │   │  Direct Controller Inst.  │   │ Pure Mockito Extension     │
    │  (MockMvc Slice Test)     │   │  (POJO Unit Test)         │   │ (@ExtendWith)              │
    ├───────────────────────────┤   ├───────────────────────────┤   ├────────────────────────────┤
    │ - Tải DispatcherServlet   │   │ - Khởi tạo bằng new       │   │ - Không tải Spring Context │
    │ - HTTP Request/Response   │   │ - Truyền thực thể Detached│   │ - Mock WebDataBinder       │
    │ - Path Variable, Binding  │   │ - Kiểm tra logic sao chép │   │ - verify() lời gọi binder  │
    │ - Model, View, Redirect   │   │ - Kiểm tra lệch ID biên   │   │ - Thực thi siêu tốc (<5ms) │
    └───────────────────────────┘   └───────────────────────────┘   └────────────────────────────┘
```

### 1.1. So sánh hai mô hình Test Harness

| Tiêu chí | Spring Slice Test (`@WebMvcTest` + `MockMvc`) | Unit Test thuần (Khởi tạo trực tiếp qua `new`) |
|:---|:---|:---|
| **Khởi động Context** | Tải lát cắt Spring MVC (`DispatcherServlet`, HandlerMapping, Formatters, Mockito beans). Tốn thời gian khởi động (~1.5s - 2.5s). | Hoàn toàn không tải Spring Context. Khởi tạo trực tiếp bằng toán tử `new` trong vài mili-giây (< 5ms). |
| **Phạm vi mô phỏng** | Toàn bộ vòng đời HTTP: Routing URL, trích xuất `@PathVariable`, `@RequestParam`, chuyển đổi định dạng qua Formatter, kiểm chuẩn `@Valid`, xử lý View/Redirect. | Chỉ kiểm thử logic thực thi bên trong phương thức Java của Controller với các tham số đầu vào do test case chủ động tạo dựng. |
| **Cơ chế Binding** | Tự động thông qua `ServletModelAttributeMethodProcessor`: đọc request params và ghi đè trực tiếp lên entity trong Model. | Tự kiểm soát: có thể truyền các đối tượng DTO tách rời (`detached entity`), `BindingResult` nhân tạo (`BeanPropertyBindingResult`). |
| **Hạn chế đối với Mutation Testing** | **"Mù" trước các mutant cập nhật thực thể:** Vì binder tự động ghi dữ liệu vào entity trong Model trước khi Controller chạy, các lệnh sao chép trường thủ công trong Controller trở nên "dư thừa" trên HTTP pipeline. | Không kiểm tra được cơ chế routing URL, annotation binding của Spring MVC, và định dạng HTTP Headers thực tế. |

### 1.2. Phân tích lý do lựa chọn kiến trúc cho từng file kiểm thử

Dựa trên việc đọc mã nguồn thực tế tại commit `500158f732419217507c7656904b8e6aa1bcc0d6`, các file test của TV4 lựa chọn mô hình harness như sau:

#### a. `ControllerBinderMutationTests.java` (5 tests) — Lựa chọn: `@ExtendWith(MockitoExtension.class)` (Unit thuần)
- **Mã nguồn thực tế:** Lớp test được chú thích bằng `@ExtendWith(MockitoExtension.class)` và `@DisabledInNativeImage`, hoàn toàn không có chú thích Spring Context như `@SpringBootTest` hay `@WebMvcTest`.
- **Lý do kỹ thuật:**
  - 4 test đầu kiểm tra phương thức `@InitBinder public void setAllowedFields(WebDataBinder dataBinder)`. Mục tiêu là xác nhận lệnh `dataBinder.setDisallowedFields("id", "*.id")` được gọi nhằm ngăn chặn lỗ hổng Mass Assignment. Phương thức này không phụ thuộc HTTP request hay routing; chỉ cần truyền `mock(WebDataBinder.class)` và gọi trực tiếp `new OwnerController(owners).setAllowedFields(binder)`.
  - Test thứ 5 kiểm tra `visitController.minVisitDate()` trả về `LocalDate.now()`. Đây là một `@ModelAttribute` method trả về giá trị thuần, gọi trực tiếp không cần Spring Context.
  - *Hiệu quả:* Tối ưu hóa thời gian chạy PIT minion (5 tests hoàn thành trong dưới 50ms), loại bỏ hoàn toàn overhead khởi động Spring container.

#### b. `OwnerControllerMutationTests.java` (6 tests) — Lựa chọn: Kết hợp `@WebMvcTest` (5 tests) và Unit thuần (1 test)
- **Mã nguồn thực tế:** Chú thích cấp lớp là `@WebMvcTest(OwnerController.class)`.
- **Lý do kỹ thuật cho 5 tests dùng `MockMvc`:**
  - `processFindFormRequestsZeroBasedPageIndex`: Cần gửi HTTP GET `/owners?page=2` để kích hoạt bộ chuyển đổi tham số phân trang của Spring MVC, sau đó dùng `ArgumentCaptor` bắt `Pageable` được truyền vào `OwnerRepository`.
  - `outOfBoundsPageWithEmptyLastNameOmitsLastNameParam`: Cần kiểm tra HTTP 3xx Redirection và chuỗi URL chuyển hướng `redirectedUrl("/owners?page=1")` khi trang vượt biên.
  - 3 test kiểm tra ném `IllegalArgumentException` khi truy cập ID không tồn tại (`editFormWithUnknownOwnerThrowsIllegalArgument`, `showOwnerWithUnknownIdThrowsIllegalArgument`, `showOwnerFailingOnSecondLookupThrowsIllegalArgument`): Cần gửi HTTP request để kiểm tra bộ lọc lỗi và ngoại lệ bung ra khỏi `MockMvc`.
- **Lý do kỹ thuật cho 1 test dùng Unit thuần (`processUpdateOwnerFormMismatchRecordsIdFieldError`):**
  - Phương thức `processUpdateOwnerForm` có khối kiểm tra:
    ```java
    if (!Objects.equals(owner.getId(), ownerId)) {
        result.rejectValue("id", "mismatch", "The owner ID in the form does not match the URL path");
        return "redirect:/owners/{ownerId}/edit";
    }
    ```
  - Trong môi trường MockMvc thông thường, `@InitBinder` cấm bind trường `id` (`setDisallowedFields("id")`), trong khi `@ModelAttribute` nạp entity từ database. Để kích hoạt nhánh `!Objects.equals(owner.getId(), ownerId)` một cách độc lập và cô lập, test khởi tạo trực tiếp `new OwnerController(repository)`, tạo `Owner` với `id=2` nhưng truyền tham số `ownerId=1`, kiểm tra chính xác mã lỗi `"mismatch"` trên `BeanPropertyBindingResult` mà không bị can thiệp bởi pipeline binding.

#### c. `PetControllerMutationTests.java` (19 tests) — Lựa chọn: Kết hợp `@WebMvcTest` (12 tests) và Unit thuần (7 tests)
- **Mã nguồn thực tế:** Chú thích `@WebMvcTest(value = PetController.class, includeFilters = @ComponentScan.Filter(value = PetTypeFormatter.class, type = FilterType.ASSIGNABLE_TYPE))`.
- **Lý do kỹ thuật cho các tests dùng `MockMvc`:**
  - Cần bộ phân giải `PetTypeFormatter` để parse chuỗi `"hamster"` từ HTTP POST sang đối tượng `PetType`.
  - Kiểm tra các nhánh validation của `PetValidator` qua HTTP pipeline (ví dụ: submit form trùng tên pet thì hiển thị lại view với binding errors).
- **Lý do kỹ thuật cho các tests dùng Unit thuần:**
  - Gồm 7 test: `updateCopiesFieldsOntoManagedPet`, `updateFallsBackToAddForUnknownPetId`, `updateWithBlankNameSkipsDuplicateCheck`, `updateWithNullPetIdFailsFast`, `processCreationFormDuplicateNameOnNewPetHasErrors`, `processCreationFormHasErrorsWithExistingPetRethrowsDataIntegrity`, `findPetThrowsWhenOwnerNotFound`.
  - Đặc biệt đối với `updateCopiesFieldsOntoManagedPet`: Đây là test cốt lõi diệt 3 mutant xóa lệnh gán `setName`, `setBirthDate`, `setType` trong `updatePetDetails`. MockMvc không thể phát hiện được 3 mutant này vì entity trong Model đã bị HTTP form binder ghi đè trước đó. Bắt buộc phải dùng Unit test thuần để đưa một đối tượng tách rời (`detached entity`) vào đối chiếu với đối tượng đang quản lý (`managed entity`).

#### d. `VisitControllerMutationTests.java` (6 tests) — Lựa chọn: `@WebMvcTest(VisitController.class)` (MockMvc)
- **Mã nguồn thực tế:** `@WebMvcTest(VisitController.class)`.
- **Lý do kỹ thuật:** Toàn bộ 6 test đều kiểm tra các luồng web của việc tạo visit (`/owners/{ownerId}/pets/{petId}/visits/new`): nạp pet/owner từ path variable, kiểm tra validation khi ngày visit để trống hoặc mô tả trống, và kiểm tra view name / redirection trả về từ `ModelAndView`.

---

## 2. CÔ LẬP PHỤ THUỘC (DEPENDENCY ISOLATION): ĐỐI TƯỢNG MOCK, KỸ THUẬT STUBBING VÀ VERIFICATION

Nhằm đảm bảo nguyên tắc kiểm thử hộp trắng độc lập (Deterministic, Isolation) và đạt tốc độ thực thi cao phục vụ Mutation Testing, tầng Controller được cô lập hoàn toàn khỏi tầng cơ sở dữ liệu thật (H2/MySQL).

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      CƠ CHẾ CÔ LẬP BẰNG MOCKITO                        │
 └────────────────────────────────────────────────────────────────────────┘
                 │                                        │
    ┌────────────┴─────────────┐             ┌────────────┴─────────────┐
    ▼                          ▼             ▼                          ▼
┌──────────────────────────┐ ┌──────────┐ ┌──────────────────────────┐ ┌──────────┐
│ Stubbing (given/when)    │ │ Mục tiêu │ │ Verification (verify)    │ │ Mục tiêu │
├──────────────────────────┤ ├──────────┤ ├──────────────────────────┤ ├──────────┤
│ findById(id) -> Optional │ │ Nạp DTO  │ │ verify(binder)           │ │ Chặn     │
│ Sequential Stubbing      │ │ Ép ngoại │ │   .setDisallowedFields() │ │ Mass-    │
│ findByLastNameStartingWith│ │ lệ orElse│ │ verify(repo).save()      │ │ Assign   │
│ findPetTypes()           │ │ Phân     │ │ verify(repo).saveAndFlush│ │ Đảm bảo  │
│                          │ │ trang    │ │ verify(repo, never())    │ │ lưu DB   │
└──────────────────────────┘ └──────────┘ └──────────────────────────┘ └──────────┘
```

### 2.1. Danh mục các Collaborator được Mock

1. **`OwnerRepository`:**
   - Được khai báo thông qua chú thích `@MockitoBean private OwnerRepository owners;` trong các lớp `@WebMvcTest`, hoặc khởi tạo trực tiếp qua `mock(OwnerRepository.class)` trong các phương thức Unit test thuần.
   - Đóng vai trò cung cấp dữ liệu giả lập cho toàn bộ các thao tác tra cứu, tìm kiếm chủ nuôi và lưu trữ trạng thái thú cưng / lịch hẹn.

2. **`PetTypeRepository`:**
   - Được khai báo thông qua `@MockitoBean private PetTypeRepository types;` hoặc `mock(PetTypeRepository.class)`.
   - Cung cấp danh mục loại thú cưng (`PetType`) trong hệ thống (như `hamster`, `dog`, `cat`).

3. **`WebDataBinder`:**
   - Được tạo lập bằng `mock(WebDataBinder.class)` trong lớp `ControllerBinderMutationTests`.
   - Đóng vai trò đối tượng nhận các cấu hình kiểm chuẩn và phân quyền gán trường dữ liệu từ Controller.

### 2.2. Chiến lược Stubbing (Giả lập hành vi)

Mã nguồn kiểm thử của TV4 sử dụng phong cách BDD (`BDDMockito.given(...)`) và Mockito truyền thống với các kịch bản chuyên biệt:

#### a. Tra cứu đơn nhất và Xử lý ngoại lệ (`findById`)
- **Stub dữ liệu hợp lệ:**
  ```java
  given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(george()));
  ```
  Cung cấp thực thể `Owner` hợp lệ để phục vụ các phương thức `@ModelAttribute findOwner` hoặc nạp thông tin xem chi tiết.
- **Stub dữ liệu rỗng (Boundary / Negative Test):**
  ```java
  given(this.owners.findById(999)).willReturn(Optional.empty());
  ```
  Kích hoạt biểu thức `.orElseThrow(() -> new IllegalArgumentException(...))` trong Controller, tiêu diệt triệt để `NullReturnValsMutator` sinh ra tại các lambda này.
- **Sequential Stubbing (Stub tuần tự đa bước):**
  Trong test `showOwnerFailingOnSecondLookupThrowsIllegalArgument` ([`OwnerControllerMutationTests.java#L210`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerMutationTests.java#L210)):
  ```java
  given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(george()), Optional.empty());
  ```
  *Ý đồ kỹ thuật:* Trong một HTTP request đến `GET /owners/{ownerId}`, Spring MVC gọi `findById` hai lần: lần 1 tại `@ModelAttribute findOwner` (để bind vào Model), lần 2 bên trong thân hàm `showOwner(int ownerId)`. Kỹ thuật stub tuần tự cho phép lần gọi 1 thành công (request vượt qua giai đoạn bind), nhưng lần gọi 2 trả về `Optional.empty()`. Điều này cô lập chính xác nhánh ném ngoại lệ thứ hai, diệt mutant `NullReturnValsMutator` tại dòng 182 của `OwnerController.java`.

#### b. Tra cứu phân trang (`findByLastNameStartingWith`)
- **Stub phân trang có dữ liệu:**
  ```java
  Page<Owner> page = new PageImpl<>(List.of(george()), PageRequest.of(1, 5), 12);
  given(this.owners.findByLastNameStartingWith(eq(""), any(Pageable.class))).willReturn(page);
  ```
  Cho phép giả lập trường hợp trang 2 có dữ liệu để kiểm tra view `"owners/ownersList"`.
- **Stub phân trang rỗng (Trang vượt biên):**
  ```java
  given(this.owners.findByLastNameStartingWith(eq(""), any(Pageable.class)))
      .willReturn(new PageImpl<>(List.of()));
  ```
  Giả lập trường hợp người dùng truy vấn `page=99` không có kết quả để ép hệ thống chuyển hướng về `page=1`.

#### c. Danh mục loại thú cưng (`findPetTypes`)
- Khởi tạo danh sách mẫu cố định trong `@BeforeEach`:
  ```java
  given(this.types.findPetTypes()).willReturn(List.of(this.hamster));
  ```
  Cung cấp danh mục cho `@ModelAttribute("types")` của `PetController`.

### 2.3. Chiến lược Verification (Kiểm tra tương tác và Tác dụng phụ)

Kiểm thử hộp trắng hướng đột biến không chỉ kiểm tra giá trị trả về (return value) mà phải xác minh các tác dụng phụ (side-effects) và tương tác với collaborator:

1. **Kiểm tra cấm gán trường nguy hiểm (Mass Assignment Protection):**
   ```java
   verify(binder).setDisallowedFields("id", "*.id");
   ```
   Nếu mutant `VoidMethodCallMutator` xóa bỏ lệnh gọi này, bài test sẽ fail ngay lập tức vì tương tác với mock `binder` không xảy ra.

2. **Kiểm tra tác dụng phụ lưu dữ liệu (`save` / `saveAndFlush`):**
   - Trong `VisitControllerMutationTests`:
     ```java
     verify(this.owners).save(any(Owner.class));
     ```
     Xác nhận khi form hợp lệ, chủ sở hữu kèm visit mới phải được lưu vào CSDL, diệt mutant xóa `owners.save`.
   - Trong `PetControllerMutationTests`:
     ```java
     verify(repository).saveAndFlush(captor.capture());
     ```
     Bắt đối tượng `Owner` được lưu để kiểm tra các trường của `Pet` đã được cập nhật chính xác.

3. **Kiểm tra phủ định hành vi (Negative Verification):**
   Trong `processUpdateOwnerFormMismatchRecordsIdFieldError`:
   ```java
   verify(repository, never()).save(any(Owner.class));
   ```
   Đảm bảo rằng khi có sự sai lệch giữa `owner.getId()` trong Form và `ownerId` trên URL, hệ thống tuyệt đối **không được phép gọi lệnh lưu vào CSDL**, ngăn chặn việc ghi đè sai dữ liệu.

---

## 3. BA KỸ THUẬT TRỌNG TÂM DIỆT ĐỘT BIẾN KHÓ (KÈM MÃ NGUỒN THỰC TẾ)

Trong kiểm thử tầng Web Controller, phần lớn các mutant logic nghiệp vụ và bảo mật không thể bị phát hiện nếu chỉ assert HTTP Status Code 200/302 hoặc View Name. Dưới đây là 3 kỹ thuật trọng tâm được TV4 hiện thực hóa để diệt các mutant phức tạp.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                      BA KỸ THUẬT HỘP TRẮNG TRỌNG TÂM CỦA TV4                           │
 └────────────────────────────────────────────────────────────────────────────────────────┘
            │                                 │                                │
            ▼                                 ▼                                ▼
 ┌─────────────────────┐           ┌─────────────────────┐          ┌─────────────────────┐
 │ Kỹ thuật 1: Captor  │           │ Kỹ thuật 2: Detached│          │ Kỹ thuật 3: Verify  │
 │     Pageable        │           │ Entity + Captor     │           │   DataBinder        │
 ├─────────────────────┤           ├─────────────────────┤          ├─────────────────────┤
 │ - Bắt Pageable DTO  │           │ - Tạo instance rời  │          │ - Mock WebDataBinder│
 │ - Assert page-1, sz5│           │ - Ép cập nhật DB    │          │ - verify cấm "id"   │
 │ - Diệt MathMutator  │           │ - Diệt 3 Mutator gán│          │ - Diệt VoidMethod   │
 └─────────────────────┘           └─────────────────────┘          └─────────────────────┘
```

### 3.1. Kỹ thuật 1: `ArgumentCaptor<Pageable>` kiểm tra `PageRequest.of(page - 1, 5)`

#### a. Ngữ cảnh SUT và Mutant mục tiêu
Trong [`OwnerController.java`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L141-L146), phương thức phụ trợ `findPaginatedForOwnersLastName` chuyển đổi chỉ số trang 1-based từ Web Request thành 0-based của Spring Data:
```java
// Trích mã nguồn thật: OwnerController.java (Dòng 141 - 146)
141: 	private Page<Owner> findPaginatedForOwnersLastName(int page, String lastname) {
142: 		int pageSize = 5;
143: 		int validatedPage = Math.max(page, 1);
144: 		Pageable pageable = PageRequest.of(validatedPage - 1, pageSize);
145: 		return owners.findByLastNameStartingWith(lastname, pageable);
146: 	}
```
- **Mutant sinh ra bởi PIT:** Tại dòng 144, toán tử `MathMutator` thay đổi phép tính chỉ số trang:
  `validatedPage - 1` $\longrightarrow$ `validatedPage + 1`.
- **Vấn đề nếu chỉ kiểm tra View/Model thông thường:** Nếu test chỉ kiểm tra `status().isOk()` và `view().name("owners/ownersList")`, MockMvc vẫn trả về HTTP 200 vì repository mock trả về trang rỗng hoặc trang giả lập. Mutant trên sống sót vì sự sai lệch chỉ số trang bên trong `Pageable` bị nuốt chửng.

#### b. Giải pháp bằng `ArgumentCaptor` trong Test
TV4 triển khai test method `processFindFormRequestsZeroBasedPageIndex` ([`OwnerControllerMutationTests.java#L91-L103`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerMutationTests.java#L91-L103)):
```java
// Trích mã nguồn thật: OwnerControllerMutationTests.java (Dòng 91 - 103)
91: 	@Test
92: 	void processFindFormRequestsZeroBasedPageIndex() throws Exception {
93: 		Page<Owner> page = new PageImpl<>(List.of(george()), PageRequest.of(1, 5), 12);
94: 		given(this.owners.findByLastNameStartingWith(eq(""), any(Pageable.class))).willReturn(page);
95: 
96: 		this.mockMvc.perform(get("/owners").param("page", "2"))
97: 			.andExpect(status().isOk())
98: 			.andExpect(view().name("owners/ownersList"));
99: 
100: 		ArgumentCaptor<Pageable> captor = ArgumentCaptor.forClass(Pageable.class);
101: 		verify(this.owners).findByLastNameStartingWith(eq(""), captor.capture());
102: 		assertThat(captor.getValue().getPageNumber()).isEqualTo(1);
103: 		assertThat(captor.getValue().getPageSize()).isEqualTo(5);
104: 	}
```
- **Cơ chế tiêu diệt:**
  - Test gửi request `page=2` (1-based).
  - `captor.capture()` chặn bắt chính xác đối tượng `Pageable` trước khi nó được chuyển tới repository.
  - Assert `captor.getValue().getPageNumber()` bắt buộc phải bằng $2 - 1 = 1$.
  - Nếu `MathMutator` đổi thành $2 + 1 = 3$, `isEqualTo(1)` sẽ so sánh `3 == 1` $\longrightarrow$ **AssertionError** $\longrightarrow$ **Mutant bị tiêu diệt (KILLED)**.

---

### 3.2. Kỹ thuật 2: Detached Entity + `ArgumentCaptor` diệt mutant xóa `setName`/`setBirthDate`/`setType` trong `updatePetDetails`

#### a. Ngữ cảnh SUT và Hiện tượng "MockMvc Blinding"
Trong [`PetController.java`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/PetController.java#L186-L200), phương thức cập nhật thú cưng sao chép thuộc tính từ DTO sang thực thể đang quản lý:
```java
// Trích mã nguồn thật: PetController.java (Dòng 186 - 200)
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
- **Mutants sinh ra:** PIT áp dụng `VoidMethodCallMutator` xóa bỏ từng dòng lệnh tại 192 (`setName`), 193 (`setBirthDate`), và 194 (`setType`).
- **Hiện tượng "MockMvc Blinding" (Vì sao MockMvc thường mù?):**
  - Trong vòng đời chuẩn của Spring MVC, tham số `@Valid Pet pet` trên phương thức `processUpdateForm` được giải quyết bởi `ServletModelAttributeMethodProcessor`.
  - Bộ xử lý này tìm trong Model đối tượng `"pet"` (do `@ModelAttribute("pet")` hoặc `owner.getPet(petId)` nạp lên từ trước).
  - Tiếp theo, Spring WebDataBinder đọc trực tiếp các HTTP Form Parameters và **ghi đè trực tiếp lên chính instance `Pet` đó**!
  - Kết quả là khi vào đến thân hàm `updatePetDetails`: `existingPet` và `pet` **thực chất cùng trỏ đến MỘT đối tượng trên bộ nhớ Heap** (`existingPet == pet`).
  - Do đó, ba câu lệnh:
    ```java
    existingPet.setName(pet.getName()); // Tương đương existingPet.setName(existingPet.getName())
    ```
    trở nên **hoàn toàn dư thừa** trong kịch bản HTTP Form thông thường!
  - Dù PIT có xóa sạch 3 dòng lệnh này, dữ liệu trên `existingPet` đã được Spring Binder cập nhật từ trước. Các test case chạy qua `MockMvc` hoàn toàn không nhận ra lỗi và vẫn PASS $\longrightarrow$ **Mutant sống sót (SURVIVED)**.

```
       MÔ HÌNH HIỆN TƯỢNG "MOCKMVC BLINDING" VS. DETACHED ENTITY UNIT TEST

  [Spring MockMvc Pipeline]
  HTTP POST Request ──> Spring Binder ──> Ghi đè trực tiếp ──> existingPet == pet (Cùng 1 tham chiếu)
                                                                    │
                                                                    ▼
                                               3 lệnh gán ở dòng 192-194 trở nên DƯ THỪA!
                                               (Xóa đi test MockMvc vẫn XANH -> MUTANT SỐNG)

  [Detached Entity Test (TV4)]
  Tạo `managed` (Tên cũ: "petty")  ──┐
                                     ├──> controller.processUpdateForm(...)
  Tạo `detached` (Tên mới: "Betty") ──┘   (Hai đối tượng HOÀN TOÀN TÁCH RỜI trên Heap)
                                                        │
                                                        ▼
                                          existingPet.setName("Betty") BẮT BUỘC PHẢI CHẠY!
                                          (Xóa đi: `managed` vẫn mang tên "petty" -> TEST ĐỎ -> DIỆT MUTANT)
```

#### b. Giải pháp bằng Detached Entity + Unit Test thuần
Để phá vỡ hiện tượng tham chiếu chéo này, TV4 thiết kế phương thức kiểm thử unit thuần `updateCopiesFieldsOntoManagedPet` ([`PetControllerMutationTests.java#L277-L306`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/test/java/org/springframework/samples/petclinic/owner/PetControllerMutationTests.java#L277-L306)):
```java
// Trích mã nguồn thật: PetControllerMutationTests.java (Dòng 277 - 306)
277: 	@Test
278: 	void updateCopiesFieldsOntoManagedPet() {
279: 		OwnerRepository repository = mock(OwnerRepository.class);
280: 		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
281: 		Owner owner = new Owner();
282: 		Pet managed = new Pet();
283: 		managed.setId(1);
284: 		managed.setName("petty");
285: 		managed.setBirthDate(LocalDate.of(2010, 1, 1));
286: 		owner.addPet(managed);
287: 		// detached form-backing object: a different instance carrying the same id
288: 		Pet detached = new Pet();
289: 		detached.setId(1);
290: 		detached.setName("Betty");
291: 		detached.setType(this.hamster);
292: 		detached.setBirthDate(LocalDate.of(2015, 2, 12));
293: 		BeanPropertyBindingResult result = new BeanPropertyBindingResult(detached, "pet");
294: 
295: 		String view = controller.processUpdateForm(owner, detached, result, new RedirectAttributesModelMap());
296: 
297: 		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
298: 		assertThat(result.hasErrors()).isFalse();
299: 		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
300: 		verify(repository).saveAndFlush(captor.capture());
301: 		Pet updated = captor.getValue().getPet(1);
302: 		assertThat(updated).isNotNull();
303: 		assertThat(updated.getName()).isEqualTo("Betty");
304: 		assertThat(updated.getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12));
305: 		assertThat(updated.getType()).isNotNull();
306: 		assertThat(updated.getType().getName()).isEqualTo("hamster");
307: 	}
```
- **Cơ chế tiêu diệt:**
  - Đối tượng `managed` (trong `owner`) có dữ liệu ban đầu: tên `"petty"`, sinh năm `2010`.
  - Đối tượng `detached` là một instance hoàn toàn riêng biệt trên Heap, mang cùng `id=1` nhưng có dữ liệu mới: tên `"Betty"`, ngày sinh `2015-02-12`, loại `"hamster"`.
  - Gọi trực tiếp `controller.processUpdateForm(owner, detached, ...)`.
  - `captor.capture()` bắt đối tượng `owner` truyền vào `saveAndFlush`.
  - Lấy `updated = captor.getValue().getPet(1)` và assert các trường dữ liệu:
    - Nếu dòng 192 bị xóa (`setName` bị bỏ): `updated.getName()` vẫn là `"petty"`, so sánh `isEqualTo("Betty")` thất bại $\longrightarrow$ **DIỆT MUTANT dòng 192**.
    - Nếu dòng 193 bị xóa (`setBirthDate` bị bỏ): `updated.getBirthDate()` vẫn là `2010-01-01`, so sánh `isEqualTo(2015-02-12)` thất bại $\longrightarrow$ **DIỆT MUTANT dòng 193**.
    - Nếu dòng 194 bị xóa (`setType` bị bỏ): `updated.getType()` là `null`, so sánh `isNotNull()` thất bại $\longrightarrow$ **DIỆT MUTANT dòng 194**.

---

### 3.3. Kỹ thuật 3: `verify(binder).setDisallowedFields` cho 3 Controller (Diệt `VoidMethodCallMutator`)

#### a. Ngữ cảnh SUT và Lỗ hổng Mass Assignment
Trong các ứng dụng Spring MVC, nếu không giới hạn các trường bind dữ liệu từ HTTP Request, kẻ tấn công có thể chèn tham số `id=999` hoặc `owner.id=999` vào payload để sửa đổi khóa chính hoặc quan hệ entity (Lỗ hổng Mass Assignment). Spring PetClinic giải quyết vấn đề này qua cấu hình `@InitBinder` tại cả 3 Controller:
- `OwnerController.java` (dòng 60–62):
  ```java
  @InitBinder
  public void setAllowedFields(WebDataBinder dataBinder) {
      dataBinder.setDisallowedFields("id", "*.id");
  }
  ```
- `PetController.java` (dòng 54–62):
  ```java
  @InitBinder("owner")
  public void initOwnerBinder(WebDataBinder dataBinder) {
      dataBinder.setDisallowedFields("id", "*.id");
  }

  @InitBinder("pet")
  public void initPetBinder(WebDataBinder dataBinder) {
      dataBinder.setDisallowedFields("id", "*.id");
      dataBinder.setValidator(new PetValidator());
  }
  ```
- `VisitController.java` (dòng 51–54):
  ```java
  @InitBinder
  public void setAllowedFields(WebDataBinder dataBinder) {
      dataBinder.setDisallowedFields("id", "*.id");
  }
  ```
- **Mutant sinh ra:** PIT tạo ra các `VoidMethodCallMutator` xóa hoàn toàn các câu lệnh `dataBinder.setDisallowedFields("id", "*.id")`.
- **Vì sao test chức năng thông thường không phát hiện được:**
  Các test case thông thường gửi request hợp lệ (không chèn trường `id` giả mạo). Do đó, dù có cấm bind `id` hay không, request vẫn thành công và cho ra kết quả giống hệt nhau $\longrightarrow$ **Mutant bảo mật sống sót**.

#### b. Giải pháp bằng `verify(binder)` trong `ControllerBinderMutationTests`
TV4 tạo lớp `ControllerBinderMutationTests` độc lập ([`ControllerBinderMutationTests.java#L43-L81`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/test/java/org/springframework/samples/petclinic/owner/ControllerBinderMutationTests.java#L43-L81)) kiểm tra trực tiếp tương tác:
```java
// Trích mã nguồn thật: ControllerBinderMutationTests.java (Dòng 43 - 81)
43: 	@Test
44: 	void ownerControllerDisallowsIdBinding() {
45: 		OwnerRepository owners = mock(OwnerRepository.class);
46: 		WebDataBinder binder = mock(WebDataBinder.class);
47: 
48: 		new OwnerController(owners).setAllowedFields(binder);
49: 
50: 		verify(binder).setDisallowedFields("id", "*.id");
51: 	}
52: 
53: 	@Test
54: 	void visitControllerDisallowsIdBinding() {
55: 		OwnerRepository owners = mock(OwnerRepository.class);
56: 		WebDataBinder binder = mock(WebDataBinder.class);
57: 
58: 		new VisitController(owners).setAllowedFields(binder);
59: 
60: 		verify(binder).setDisallowedFields("id", "*.id");
61: 	}
62: 
63: 	@Test
64: 	void petControllerOwnerBinderDisallowsIdBinding() {
65: 		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
66: 		WebDataBinder binder = mock(WebDataBinder.class);
67: 
68: 		controller.initOwnerBinder(binder);
69: 
70: 		verify(binder).setDisallowedFields("id", "*.id");
71: 	}
72: 
73: 	@Test
74: 	void petControllerPetBinderDisallowsIdBinding() {
75: 		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
76: 		WebDataBinder binder = mock(WebDataBinder.class);
77: 
78: 		controller.initPetBinder(binder);
79: 
80: 		verify(binder).setDisallowedFields("id", "*.id");
81: 	}
```
- **Cơ chế tiêu diệt:**
  - Mockito `verify(binder).setDisallowedFields("id", "*.id")` xác nhận chính xác lời gọi phương thức bảo vệ với đúng hai tham số cấu hình.
  - Nếu `VoidMethodCallMutator` xóa dòng lệnh này trong bất kỳ Controller nào, Mockito sẽ ném lỗi:
    `Wanted but not invoked: binder.setDisallowedFields("id", "*.id");` $\longrightarrow$ **Test FAIL ngay lập tức** $\longrightarrow$ **Toàn bộ 4 Mutants bị tiêu diệt 100%**.




---

## 4. BẢNG TRUY VẾT ĐỘT BIẾN: MUTANT → TEST DIỆT (DỮ LIỆU THỰC TẾ TỪ MUTATIONS.XML)

Dưới đây là toàn bộ 133 mutants được sinh ra bởi PIT (mutator group STRONGER) trên 3 lớp Web Controller do TV4 phụ trách, đối chiếu trực tiếp với thẻ `<killingTest>` trong file báo cáo `target/pit-reports/mutations.xml`.

### 4.1. Lớp `OwnerController` — OwnerController.java (45 mutants: 44 KILLED, 1 SURVIVED)

| Dòng SUT | Toán tử đột biến (Mutator) | Trạng thái | Test diệt (Killing Test từ PIT) |
|:---:|:---|:---:|:---|
| `61` | `VoidMethodCallMutator` | **KILLED** | `ControllerBinderMutationTests.ownerControllerDisallowsIdBinding` |
| `66` | `NullReturnValsMutator` | **KILLED** | `OwnerControllerTests.processCreationFormSuccess` |
| `66` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processCreationFormSuccess` |
| `66` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerMutationTests.showOwnerFailingOnSecondLookupThrowsIllegalArgument` |
| `68` | `NullReturnValsMutator` | **KILLED** | `OwnerControllerMutationTests.showOwnerWithUnknownIdThrowsIllegalArgument` |
| `74` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.initCreationForm` |
| `79` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processCreationFormRejectsAddressLongerThanColumn` |
| `79` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerTests.processCreationFormSuccess` |
| `81` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processCreationFormRejectsAddressLongerThanColumn` |
| `86` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processCreationFormSuccess` |
| `91` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.initFindForm` |
| `99` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormSuccess` |
| `99` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `108` | `ConditionalsBoundaryMutator` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `108` | `ConditionalsBoundaryMutator` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `108` | `RemoveConditionalMutator_ORDER_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `108` | `RemoveConditionalMutator_ORDER_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `108` | `RemoveConditionalMutator_ORDER_IF` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `108` | `RemoveConditionalMutator_ORDER_IF` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `110` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `110` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerMutationTests.outOfBoundsPageWithEmptyLastNameOmitsLastNameParam` |
| `113` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `116` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormNoOwnersFound` |
| `116` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `118` | `VoidMethodCallMutator` | **KILLED** | `OwnerControllerTests.processFindFormNoOwnersFound` |
| `119` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormNoOwnersFound` |
| `122` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `122` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerTests.processFindFormSuccess` |
| `125` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormByLastName` |
| `129` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormSuccess` |
| `138` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormSuccess` |
| `144` | `MathMutator` | **KILLED** | `OwnerControllerMutationTests.processFindFormRequestsZeroBasedPageIndex` |
| `145` | `NullReturnValsMutator` | **KILLED** | `OwnerControllerTests.processFindFormRedirectsOutOfBoundsPageToFirstPage` |
| `150` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.initUpdateOwnerForm` |
| `156` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerTests.processUpdateOwnerFormHasErrors` |
| `156` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` |
| `158` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processUpdateOwnerFormHasErrors` |
| `161` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` |
| `161` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `OwnerControllerTests.processUpdateOwnerFormSuccess` |
| `162` | `VoidMethodCallMutator` | **KILLED** | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` |
| `164` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerMutationTests.processUpdateOwnerFormMismatchRecordsIdFieldError` |
| `167` | `VoidMethodCallMutator` | **SURVIVED (Equivalent)** | `*(Không có – SURVIVED / Equivalent)*` |
| `170` | `EmptyObjectReturnValsMutator` | **KILLED** | `OwnerControllerTests.processUpdateOwnerFormSuccess` |
| `182` | `NullReturnValsMutator` | **KILLED** | `OwnerControllerMutationTests.showOwnerFailingOnSecondLookupThrowsIllegalArgument` |
| `185` | `NullReturnValsMutator` | **KILLED** | `OwnerControllerTests.showOwner` |

### 4.2. Lớp `PetController` — PetController.java (70 mutants: 70 KILLED, 0 SURVIVED)

| Dòng SUT | Toán tử đột biến (Mutator) | Trạng thái | Test diệt (Killing Test từ PIT) |
|:---:|:---|:---:|:---|
| `64` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerMutationTests.initCreationFormExposesConfiguredPetTypes` |
| `70` | `NullReturnValsMutator` | **KILLED** | `PetControllerMutationTests.creationWithUnknownOwnerThrowsIllegalArgument` |
| `72` | `NullReturnValsMutator` | **KILLED** | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| `79` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| `79` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.findPetWithUnknownOwnerThrowsIllegalArgument` |
| `80` | `NullReturnValsMutator` | **KILLED** | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| `84` | `NullReturnValsMutator` | **KILLED** | `PetControllerMutationTests.findPetWithUnknownOwnerThrowsIllegalArgument` |
| `86` | `NullReturnValsMutator` | **KILLED** | `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation` |
| `91` | `VoidMethodCallMutator` | **KILLED** | `ControllerBinderMutationTests.petControllerOwnerBinderDisallowsIdBinding` |
| `96` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithMissingPetType` |
| `97` | `VoidMethodCallMutator` | **KILLED** | `ControllerBinderMutationTests.petControllerPetBinderDisallowsIdBinding` |
| `103` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.initCreationFormAddsPetToOwnerModel` |
| `104` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerMutationTests.initCreationFormAddsPetToOwnerModel` |
| `111` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDuplicateName` |
| `111` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDuplicateName` |
| `111` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDuplicateName` |
| `111` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName` |
| `111` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationDuplicateCheckRespectsIsNew` |
| `111` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| `112` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDuplicateName` |
| `116` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithInvalidBirthDate` |
| `116` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithInvalidBirthDate` |
| `116` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationWithNullBirthDateShowsRequiredError` |
| `116` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName` |
| `117` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithInvalidBirthDate` |
| `120` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithMissingPetType` |
| `120` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName` |
| `121` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithMissingPetType` |
| `125` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.creationPersistsNewPetThroughOwner` |
| `129` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` |
| `129` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDataIntegrityViolation` |
| `132` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDataIntegrityViolation` |
| `133` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDataIntegrityViolation` |
| `136` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerMutationTests.creationDuplicateCheckRequiresReadableName` |
| `141` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.initUpdateForm` |
| `151` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDuplicateName` |
| `151` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateWithBlankNameSkipsDuplicateCheck` |
| `153` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDuplicateName` |
| `153` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDuplicateName` |
| `153` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `153` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation` |
| `154` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDuplicateName` |
| `159` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| `159` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| `159` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithInvalidBirthDate` |
| `159` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `160` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| `163` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| `163` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `164` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerMutationTests.updateWithFutureBirthDateIsRejected` |
| `168` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `171` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateRethrowsUnexpectedIntegrityViolation` |
| `171` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDataIntegrityViolation` |
| `174` | `VoidMethodCallMutator` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDataIntegrityViolation` |
| `175` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerTests$ProcessUpdateFormHasErrors.processUpdateFormWithDataIntegrityViolation` |
| `178` | `EmptyObjectReturnValsMutator` | **KILLED** | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` |
| `188` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` |
| `188` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `188` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateWithNullPetIdFailsFast` |
| `190` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` |
| `190` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` |
| `192` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` |
| `193` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` |
| `194` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateCopiesFieldsOntoManagedPet` |
| `197` | `VoidMethodCallMutator` | **KILLED** | `PetControllerMutationTests.updateFallsBackToAddForUnknownPetId` |
| `204` | `BooleanTrueReturnValsMutator` | **KILLED** | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` |
| `204` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDataIntegrityViolation` |
| `204` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `PetControllerTests$ProcessCreationFormHasErrors.processCreationFormWithDataIntegrityViolation` |
| `204` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationRethrowsViolationWithNullMessage` |
| `204` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `PetControllerMutationTests.creationRethrowsUnexpectedIntegrityViolation` |

### 4.3. Lớp `VisitController` — VisitController.java (18 mutants: 18 KILLED, 0 SURVIVED)

| Dòng SUT | Toán tử đột biến (Mutator) | Trạng thái | Test diệt (Killing Test từ PIT) |
|:---:|:---|:---:|:---|
| `53` | `VoidMethodCallMutator` | **KILLED** | `ControllerBinderMutationTests.visitControllerDisallowsIdBinding` |
| `67` | `NullReturnValsMutator` | **KILLED** | `VisitControllerMutationTests.newVisitFormWithUnknownOwnerThrowsIllegalArgument` |
| `71` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `VisitControllerMutationTests.newVisitFormWithUnknownPetThrowsIllegalArgument` |
| `71` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `VisitControllerTests.processNewVisitFormSuccess` |
| `79` | `VoidMethodCallMutator` | **KILLED** | `VisitControllerMutationTests.newVisitFormExposesPetWithPendingVisit` |
| `80` | `NullReturnValsMutator` | **KILLED** | `VisitControllerTests.processNewVisitFormSuccess` |
| `85` | `NullReturnValsMutator` | **KILLED** | `ControllerBinderMutationTests.minVisitDateIsTomorrow` |
| `92` | `EmptyObjectReturnValsMutator` | **KILLED** | `VisitControllerMutationTests.newVisitFormExposesPetWithPendingVisit` |
| `100` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `VisitControllerTests.processNewVisitFormHasErrorsWhenVisitDateIsNotInFuture` |
| `100` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `VisitControllerTests.processNewVisitFormHasErrorsWhenVisitDateIsNotInFuture` |
| `100` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` |
| `100` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `VisitControllerTests.processNewVisitFormSuccess` |
| `101` | `VoidMethodCallMutator` | **KILLED** | `VisitControllerTests.processNewVisitFormHasErrorsWhenVisitDateIsNotInFuture` |
| `104` | `RemoveConditionalMutator_EQUAL_ELSE` | **KILLED** | `VisitControllerTests.processNewVisitFormHasErrorsWhenVisitDateIsNotInFuture` |
| `104` | `RemoveConditionalMutator_EQUAL_IF` | **KILLED** | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` |
| `105` | `EmptyObjectReturnValsMutator` | **KILLED** | `VisitControllerTests.processNewVisitFormHasErrorsWhenVisitDateIsNotInFuture` |
| `108` | `VoidMethodCallMutator` | **KILLED** | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` |
| `111` | `EmptyObjectReturnValsMutator` | **KILLED** | `VisitControllerMutationTests.processNewVisitFormWithNullDateBooksSuccessfully` |


---

## 5. GIỚI HẠN VÀ MỐI ĐE DỌA TÍNH HỢP LỆ (LIMITATIONS & THREATS TO VALIDITY)

Mặc dù bộ kiểm thử hộp trắng của TV4 đã tiêu diệt 132/133 mutants trên tầng Controller (đạt tỷ lệ 99.25%), báo cáo kỹ thuật cần chỉ rõ các giới hạn lý thuyết và thực nghiệm nhằm đảm bảo tính khách quan khoa học.

### 5.1. Đột biến tương đương tại `OwnerController.java` dòng 167 (Dead Store / Idempotent Assignment)

Trong 45 mutants sinh ra trên `OwnerController`, duy nhất 01 mutant sống sót và được xác định là **Mutant tương đương (Equivalent Mutant)**:
- **Vị trí SUT:** Phương thức `processUpdateOwnerForm` ([`OwnerController.java#L161-L168`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L161-L168)):
  ```java
  161: 		if (!Objects.equals(owner.getId(), ownerId)) {
  162: 			result.rejectValue("id", "mismatch", "The owner ID in the form does not match the URL.");
  163: 			redirectAttributes.addFlashAttribute("error", "Owner ID mismatch. Please try again.");
  164: 			return "redirect:/owners/{ownerId}/edit";
  165: 		}
  166: 
  167: 		owner.setId(ownerId);
  168: 		this.owners.save(owner);
  ```
- **Toán tử đột biến:** `VoidMethodCallMutator` xóa bỏ dòng lệnh 167 (`owner.setId(ownerId)`).
- **Phân tích bản chất kỹ thuật:**
  - Để luồng điều khiển vượt qua khối lệnh kiểm tra tại dòng 161 và chạm tới dòng 167, điều kiện `!Objects.equals(owner.getId(), ownerId)` **bắt buộc phải nhận giá trị FALSE**.
  - Điều này đồng nghĩa với việc tại dòng 167, điều kiện bất biến tiên quyết luôn là:
    $$\text{owner.getId()} \equiv \text{ownerId}$$
  - Do đó, câu lệnh `owner.setId(ownerId)` tại dòng 167 thực chất là một phép gán đẳng trị (Idempotent Assignment / Dead Store) — gán lại đúng giá trị mà thuộc tính `id` đang nắm giữ.
  - Khi `VoidMethodCallMutator` xóa bỏ dòng 167, trạng thái của đối tượng `owner` trước và sau dòng 167 là **đồng nhất 100%**.
  - Không tồn tại bất kỳ test case nào (dù dùng assert giá trị, bắt ngoại lệ hay `ArgumentCaptor`) có thể phân biệt được trạng thái giữa chương trình gốc và chương trình đột biến mà không vi phạm tính đúng đắn của logic nghiệp vụ.
  - *Phân định ranh giới:* TV4 ghi nhận và phân lập mutant tương đương này trong test suite (`OwnerControllerMutationTests.findPaginatedSurvivesEquivalentMutant`). Phân tích mã bytecode chi tiết và chứng minh hình thức toán học thuộc nội dung báo cáo Phần G của Thành viên 5 (TV5).

### 5.2. Mối đe dọa tính hợp lệ nội bộ (Threats to Internal Validity)

1. **Sự phụ thuộc vào Mocking Framework (Mock-Drift):**
   - Việc cô lập triệt để các dependency (`OwnerRepository`, `PetTypeRepository`) bằng Mockito giả định rằng hợp đồng (contract) giữa Controller và Repository luôn giữ nguyên.
   - Nếu tầng Data Repository thay đổi hành vi ngoại lệ (ví dụ: Spring Data trả về `EmptyResultDataAccessException` thay vì `Optional.empty()`), các stub trong Controller test có thể không còn phản ánh đúng thực tế khi chạy tích hợp.
2. **Kiểm thử Unit thuần với Detached Entity:**
   - Kỹ thuật khởi tạo trực tiếp qua `new PetController` để truyền `detached` entity giải quyết triệt để điểm mù của `MockMvc`, nhưng đòi hỏi test engineer phải hiểu sâu sắc cơ chế luân chuyển đối tượng trong Hibernate/JPA. Nếu áp dụng thiếu cẩn trọng, test có thể kiểm tra một kịch bản không xuất hiện trong môi trường thực.

### 5.3. Mối đe dọa tính hợp lệ bên ngoài (Threats to External Validity)

1. **Môi trường giả lập `MockMvc` so với Web Container thật:**
   - `MockMvc` giả lập toàn bộ pipeline của Spring MVC nhưng chạy trong môi trường in-memory, không mở socket mạng TCP thật và không chạy qua Web Server container (Tomcat/Undertow). Các khía cạnh như HTTP chunked transfer, timeout kết nối, hoặc xung đột đa luồng (concurrency) không nằm trong phạm vi phát hiện của bộ test này.
2. **Giới hạn bộ Mutator:**
   - Nghiên cứu sử dụng nhóm mutator `STRONGER` của PIT 1.30.0. Mặc dù `STRONGER` bao phủ phần lớn các lỗi lập trình logic và biểu thức, các dạng lỗi chuyên sâu khác (như đột biến trên cấu hình bảo mật Spring Security hay transaction rollback) cần các bộ mutator chuyên dụng hơn.
