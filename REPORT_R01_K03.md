# BÁO CÁO TỔNG KẾT HỌC PHẦN: ĐỀ TÀI R01 (SPRING PETCLINIC) + K03 (MUTATION TESTING)

> **Nhóm thực hiện:** Program_R01-K03 — Mutation Testing bằng PIT trên Spring PetClinic
> **Phạm vi đột biến:** `org.springframework.samples.petclinic.owner.*` (đúng syllabus, không chạy toàn repo)
> **Commit đã khóa (pin):** `500158f732419217507c7656904b8e6aa1bcc0d6` (`main`, ngày 2026-09-29)
> **Kết quả cuối:** **192/195 mutants bị tiêu diệt — Mutation Score 98% (ngưỡng yêu cầu ≥ 88%) — Line Coverage 100%**
> **Nguyên tắc bất biến:** không sửa `src/main/java`; mọi bổ sung nằm trong `src/test/java` + cấu hình `pom.xml`.

---

## PHẦN A: MỤC TIÊU VÀ KIẾN TRÚC HỆ THỐNG

### A.1. Bài toán nghiệp vụ

Spring PetClinic là ứng dụng mẫu của hệ sinh thái Spring, mô phỏng **hệ thống quản lý phòng khám thú y**:
quản lý chủ nuôi (owners), thú cưng (pets), bác sĩ thú y (vets) và các lượt khám/bệnh án (visits).
Nghiệp vụ điển hình: tìm kiếm chủ nuôi theo họ, phân trang danh sách, thêm/sửa thú cưng
(kèm kiểm chuẩn dữ liệu đầu vào), đặt lịch khám trong tương lai và lưu mô tả bệnh án.

### A.2. Mục tiêu của đề tài kết hợp R01 + K03

1. Dựng và kiểm chứng 03 luồng nghiệp vụ trọng tâm chạy thành công trên runtime thật (HTTP 200).
2. Tiêm harness Mutation Testing (PIT/Pitest) giới hạn ở package nghiệp vụ lõi `...owner.*`.
3. Thiết lập **baseline mutation score**, sau đó lặp vòng kill-mutant tới khi đạt **≥ 88%**.
4. Phân tích nguyên nhân cốt lõi (RCA) cho mutant cứng đầu và phân loại theo chuẩn Error–Fault–Failure.
5. Bàn giao báo cáo + hướng dẫn tái hiện 1-lệnh trên máy mới.

### A.3. Technology Stack (thực tế đo được từ `pom.xml` tại commit đã khóa)

| Thành phần | Phiên bản / giá trị |
|---|---|
| Ngôn ngữ | Java 17 (`<java.version>17</java.version>`, Temurin 17.0.20.1) |
| Framework | Spring Boot **4.1.0** (parent), Spring Data JPA, Spring MVC + Thymeleaf |
| Kiểm thử | JUnit **6.0.3** (Jupiter, theo BOM Spring Boot 4), AssertJ, Mockito 5.23.0, MockMvc (`@WebMvcTest`) |
| Đột biến | `pitest-maven` **1.30.0** + `pitest-junit5-plugin` **1.2.3** (xem A.5) |
| Build | Maven 3.9.16 (qua wrapper `./mvnw` / `mvnw.cmd`), JaCoCo 0.8.15 |
| CSDL | H2 (mặc định, seed tự động), MySQL / PostgreSQL (profile riêng, cần Docker) |

### A.4. Bốn module/actor cốt lõi

| Module | Lớp trung tâm | Vai trò |
|---|---|---|
| Owner | `Owner`, `OwnerController`, `OwnerRepository` | Chủ nuôi: CRUD, tìm kiếm + phân trang |
| Pet | `Pet`, `PetController`, `PetValidator`, `PetType(Formatter)` | Thú cưng: thêm/sửa, kiểm chuẩn tên–loại–ngày sinh |
| Vet | `Vet`, `VetController` | Bác sĩ thú y: danh sách + chuyên khoa (ngoài phạm vi đột biến) |
| Visit | `Visit`, `VisitController` | Lượt khám: đặt lịch tương lai + mô tả bệnh án |

### A.5. Ghi chú kỹ thuật quan trọng (trung thực)

Theo syllabus gợi ý `pitest-maven` 1.15.8+ / plugin 1.2.1+, nhưng Spring Boot 4 kéo JUnit Platform **6.0.3**
trong khi plugin 1.2.1 chỉ tương thích Platform 1.x → minion coverage của PIT sập với lỗi
`Coverage generation minion exited abnormally! (UNKNOWN_ERROR)`.
Khắc phục bằng cách nâng lên **`pitest-maven` 1.30.0 + `pitest-junit5-plugin` 1.2.3**
(vẫn thỏa mãn điều kiện "1.15.8+" / "1.2.1+", đã có tiền lệ chạy tốt với JUnit 6),
giữ nguyên mọi tham số syllabus yêu cầu (`STRONGER`, HTML+XML, `timestampedReports=false`,
`targetClasses/Test = owner.*`).

---

## PHẦN B: SƠ ĐỒ KIẾN TRÚC VÀ LUỒNG DỮ LIỆU CỦA 03 NGHIỆP VỤ TRỌNG TÂM

### B.1. Kiến trúc phân tầng (Controller → Repository → Model/Database)

```text
                        +------------------ Thymeleaf view ------------------+
                        | findOwners | ownersList | ownerDetails |           |
                        | createOrUpdateOwnerForm | createOrUpdatePetForm |   |
                        | createOrUpdateVisitForm                           |
                        +------^------------------------------v-------------+
                               | (form params / model attrs)  | (HTML)
+------------------------------+------------------------------+------------------------------+
|                              CONTROLLER LAYER                                            |
|  OwnerController  <-- OwnerRepository (Spring Data JPA)                                   |
|  PetController    <-- OwnerRepository + PetTypeRepository + PetValidator                  |
|  VisitController  <-- OwnerRepository                                                     |
+------------------------------+------------------------------+------------------------------+
                               | JPA entities / validation   |
+------------------------------v----------------------------v------------------------------+
|                              MODEL + DATABASE                                           |
|  Owner 1───* Pet 1───* Visit   |   PetType (dictionary)    |   H2 (mặc định)            |
|  Bean Validation: @NotBlank @Size @Pattern | PetValidator (thủ công)    |   seed: db/h2/data.sql |
+------------------------------------------------------------------------------------------+
```

### B.2. Luồng 1 — Tìm kiếm & hiển thị danh sách chủ nuôi (Search & Paginate Owners)

```text
Browser GET /owners?lastName=Davis&page=2
  -> OwnerController.processFindForm(page, owner, result, model, redirectAttrs)
     1. lastName null -> "" | strip() khoảng trắng thừa
     2. findPaginatedForOwnersLastName: validatedPage = max(page,1);
        Pageable = PageRequest.of(validatedPage - 1, 5)
        owners.findByLastNameStartingWith(lastName, pageable)
     3. page < 1 hoặc page > max(totalPages,1) -> redirect /owners?page=1 (+lastName nếu khác rỗng)
     4. kết quả rỗng  -> rejectValue(lastName, notFound) -> findOwners
        1 kết quả      -> redirect /owners/{id}
        nhiều kết quả  -> addPaginationModel -> owners/ownersList
```

### B.3. Luồng 2 — Thêm mới thú cưng với trình xác thực (Create Pet with PetValidator)

```text
Browser GET  /owners/{o}/pets/new  -> PetController.initCreationForm: owner.addPet(new Pet())
Browser POST /owners/{o}/pets/new (name, type, birthDate)
  -> @ModelAttribute findOwner/findPet + @InitBinder("pet"): PetValidator + cấm bind "id"
  -> processCreationForm:
     1. trùng tên (hasText && isNew && getPet(name,true) != null) -> reject "duplicate"
     2. birthDate trong tương lai -> reject "typeMismatch.birthDate"
     3. PetValidator: tên rỗng/blank -> "required"; tên > 30 ký tự -> "size";
        pet mới thiếu type -> "required"; thiếu birthDate -> "required"
     4. có lỗi -> createOrUpdatePetForm | ok -> owner.addPet + saveAndFlush
        (DataIntegrityViolationException lạ -> ném lại; trùng unique_owner_pet_name -> "duplicate")
```

### B.4. Luồng 3 — Đặt lịch khám & ghi bệnh án (Book Visit for Pet)

```text
Browser GET  /owners/{o}/pets/{p}/visits/new -> VisitController.loadPetWithVisit:
     owner.getPet(petId) null -> IllegalArgumentException; else pet.addVisit(new Visit())
Browser POST /owners/{o}/pets/{p}/visits/new (date, description)
  -> processNewVisitForm:
     1. date != null && !date.isAfter(today) -> reject "typeMismatch.visitDate"
        (ngày mặc định = tomorrow; minVisitDate = tomorrow)
     2. @Valid: description @NotBlank + @Size(max=255)
     3. ok -> owner.addVisit(petId, visit) -> owners.save -> redirect /owners/{o}
```

---

## PHẦN C: THIẾT LẬP MÔI TRƯỜNG & CHỨNG MINH 03 LUỒNG CHẠY THÀNH CÔNG

### C.1. Yêu cầu runtime

- JDK 17+ (đã kiểm chứng: `Temurin-17.0.20.1+1`, `java -version` → `openjdk 17.0.20.1`).
- Maven qua wrapper (`mvnw` / `mvnw.cmd` → Apache Maven 3.9.16, không cần cài Maven rời).
- Không cần Docker/MySQL cho luồng mặc định (dùng H2 in-memory + seed tự động).
- Biến môi trường `JAVA_HOME` trỏ tới JDK 17.

### C.2. Lệnh build & chạy

```bash
git clone https://github.com/spring-projects/spring-petclinic.git
cd spring-petclinic
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6   # pin commit (xem Phần H)
./mvnw clean test                                        # baseline unit test
./mvnw spring-boot:run                                   # chạy app (mặc định :8080, H2)
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true   # mutation
```

Seed tự động: `src/main/resources/db/h2/data.sql` (6 vets, 3 specialties, **10 owners**,
13 pets, visits mẫu) + `schema.sql`; các profile MySQL/Postgres dùng `db/mysql/*`, `db/postgres/*`.

### C.3. Bằng chứng baseline test

- `./mvnw clean test` toàn repo: **81 tests, 79 pass, 2 errors** — cả 2 lỗi đều thuộc
  `PostgresIntegrationTests`, nguyên nhân môi trường (cần Docker daemon cung cấp Postgres
  qua Testcontainers/Docker Compose, không phải lỗi logic). Không có failure nào ở logic nghiệp vụ.
- Riêng package mục tiêu: `org.springframework.samples.petclinic.owner.*` → **49/49 pass**.
- Sau khi bổ sung test (Phần E/F): toàn repo (trừ các lớp `*IntegrationTests` cần Docker:
  `Postgres`/`MySql`/`PetClinic`, tổng 8 tests) →
  **153 tests, 0 failures, 0 errors**; riêng owner → **130 tests, 100% pass**.

### C.4. Bằng chứng 03 luồng chạy thành công trên server thật

Khởi chạy `./mvnw spring-boot:run --server.port=8090` (port 8080 của máy thực nghiệm đã bị
chiếm — app báo rõ `Port 8080 was already in use`, chuyển sang 8090 và boot thành công),
sau đó gọi HTTP và ghi nhận:

| Luồng | Request | Kết quả |
|---|---|---|
| 1. Tìm kiếm chủ nuôi | `GET /owners?lastName=Davis` | **HTTP 200**, trang `ownersList` (3420 bytes) |
| 2. Chi tiết chủ nuôi | `GET /owners/1` | **HTTP 200**, trang `ownerDetails` (4343 bytes) |
| 3. Form thêm thú cưng | `GET /owners/1/pets/new` | **HTTP 200**, trang `createOrUpdatePetForm` (4650 bytes, có PetValidator) |
| 1b. Trang vượt biên | `GET /owners?page=99&lastName=Davis` | **redirect 3xx** về `/owners?page=1` (đúng nhánh `page > max(totalPages,1)`) |

---

## PHẦN D: NGUYÊN LÝ KỸ THUẬT KIỂM THỬ ĐỘT BIẾN (K03)

### D.1. Định nghĩa

- **Mutant (thể đột biến):** bản sao của chương trình bị gieo một lỗi cú pháp nhỏ có chủ đích
  (ví dụ `>` → `>=`, xóa lời gọi hàm, ép `return true`).
- **Mutation Operator:** quy tắc sinh mutant. Cấu hình `STRONGER` của PIT gộp:
  `ConditionalsBoundary`, `Increments`, `InvertNegatives`, `Math`, `VoidMethodCall`,
  `ReturnVals` (null/empty/primitive/boolean), `NegateConditionals`, `RemoveConditionals`,
  `InlineConsts`.
- **Mutation Score:** `Killed / (Total − Invalid)`; mutant **KILLED** nếu có ít nhất một test
  fail trên nó mà pass trên code gốc; **SURVIVED** nếu mọi test đều pass (test yếu/thiếu);
  **NO_COVERAGE** nếu không test nào chạm tới dòng đột biến.
- Tiêu chí Pass của đề tài: **Mutation Score ≥ 88%** cho package `...owner.*`.

### D.2. Vì sao Coverage truyền thống (Statement/Branch 100%) vẫn bỏ sót lỗi

Ba ví dụ真实 rút từ chính codebase này (đã chứng minh bằng mutant trong Phần G):

1. **Hoán đổi toán tử so sánh (`&&`/`||`, `<`/`<=`):** `PetValidator` dòng
   `name.length() > MAX_NAME_LENGTH` (30). Suite cũ chỉ có test tên 31 ký tự → branch
   `else if` được cover 100%, nhưng mutant `>=` (tên đúng 30 ký tự bị từ chối) vẫn sống —
   chỉ Boundary Value Analysis (30 vs 31) mới giết được (test `nameExactlyAtMaxLengthIsAccepted`).
2. **Rẽ nhánh bị nuốt bởi assert thiếu:** `PetController.updatePetDetails` sao chép
   `setName/setBirthDate/setType` sang entity được quản lý. Mọi test MockMvc cũ đều pass
   vì data-binding đã ghi đè cùng object (branch cover đủ) — nhưng mutant xóa `setName`
   vẫn sống. Chỉ assert sâu trên detached instance (`updateCopiesFieldsOntoManagedPet`) mới giết được.
3. **Lời gọi void bị xóa:** `owner.addPet(pet)` trong `processCreationForm` — test cũ chỉ
   assert redirect 3xx nên mutant xóa lời gọi vẫn pass; phải capture entity đã save và
   assert pet tồn tại (`creationPersistsNewPetThroughOwner`) mới giết được.

### D.3. Weak Mutation vs Strong Mutation

- **Weak Mutation:** mutant bị phát hiện ngay sau điểm đột biến (state trung gian khác nhau).
- **Strong Mutation:** sự khác biệt phải lan truyền tới **output quan sát được** (test fail).
  PIT đo Strong Mutation. Thực nghiệm cho thấy nhiều mutant "được cover nhưng không bị giết"
  (baseline: line coverage 97% mà mutation score chỉ 67%) — đúng bản chất weak≠strong.

### D.4. Equivalent Mutants (đột biến tương đương)

Mutant giữ nguyên ngữ nghĩa chương trình nên **không test nào có thể giết**; phải chứng minh
bằng lập luận và loại khỏi mẫu số khi đánh giá. Đề tài tồn tại **03 equivalent mutants**
(chứng minh chi tiết ở G.4), đạt 192/195 killed = **98%**, vượt xa ngưỡng 88%.

---

## PHẦN E: THIẾT KẾ KỊCH BẢN KIỂM THỬ

### E.1. Chiến lược kỹ thuật

- **Boundary Value Analysis (BVA):** tên pet 30/31 ký tự; ngày visit hôm nay/ngày mai/null;
  page = 0/1/2/99; mô tả 255/256 ký tự (kế thừa test cũ).
- **Equivalence Partitioning:** tên null/rỗng/blank/hợp lệ; pet mới/cũ × type null/có.
- **Decision Table:** `hasText && isNew && getPet()!=null` (8 tổ hợp, bao gồm ca biên
  tên blank nhưng owner đã có pet tên blank); `!isNew && !isNew && idEquals` trong `addPet`.
- **Basis Path:** cả hai nhánh của mọi `if` (bằng mutant RemoveConditional IF/ELSE),
  nhánh `orElseThrow`, nhánh catch `DataIntegrityViolationException` (trùng/không trùng).

### E.2. Bảng test case tiêu biểu (10/81 test mới; toàn bộ 81 test đều deterministic, thuần unit hoặc MockMvc, không phụ thuộc mạng/thời gian thực)

| ID | Class under Test | Kỹ thuật | Input / Precondition | Mutation Operator nhắm tới | Expected |
|---|---|---|---|---|---|
| MT-01 | `PetValidator` | BVA | tên đúng 30 ký tự, pet mới đủ type/birthDate | `ConditionalsBoundary` (`>`→`>=`) | không lỗi `name` |
| MT-02 | `PetValidator` | Decision Table | pet đã persist (`id=42`), `type=null` | `RemoveConditional` (`isNew && type==null`→true) | không lỗi `type` |
| MT-03 | `Owner.addPet` | Decision Table | 2 instance khác nhau, cùng `id=5` | `RemoveConditional` vòng so id | size=1, giữ instance đầu |
| MT-04 | `Owner.addPet` | Partition | cùng 1 instance **mới** (id null) add 2 lần | `RemoveConditional` (`contains`→false) | size=1 |
| MT-05 | `Owner.getPet(id)` | Partition | owner chỉ có pet mới; tìm `getPet((Integer) null)` | `RemoveConditional` (`!isNew`→true) | `null` |
| MT-06 | `PetController.processCreationForm` | Basis Path | violation message **không** chứa `unique_owner_pet_name` (+ 1 biến thể message `null`) | `RemoveConditional` (else→nuốt exception) + `TrueReturn` + null-check | ném lại `DataIntegrityViolationException` |
| MT-07 | `PetController.updatePetDetails` | State assert | detached pet id=1 ("Betty"/2015-02-12/hamster) vs managed pet id=1 ("petty"/2010-01-01/null) | `VoidMethodCall` (`setName/setBirthDate/setType`) + `RemoveConditional` (`existingPet!=null`→false) | entity đã save mang giá trị mới |
| MT-08 | `OwnerController` | BVA + captor | `GET /owners?page=2` (tổng 12 bản ghi) | `Math` (`validatedPage-1`→`+1`) | `Pageable(page=1, size=5)` |
| MT-09 | `OwnerController` | Branch | `GET /owners?page=99` không lastName | `RemoveConditional` (`!lastName.isEmpty()`→true) | redirect đúng `/owners?page=1` (không kèm `lastName=`) |
| MT-10 | `VisitController` | Null-guard | `visit.date=null`, description hợp lệ (gọi trực tiếp) | `RemoveConditional` (`date!=null`→true) | redirect + visit được persist (mutant sẽ NPE) |

Các nhóm bổ trợ: 4 test `verify(setDisallowedFields)` cho các `@InitBinder` (giết VoidMethodCall
trên binder), test `minVisitDate==tomorrow`, test `print(null-name)=="<null>"`,
test `getDescription` round-trip (giết EmptyReturn), test `orElseThrow` qua direct-call
(tránh phụ thuộc thứ tự `@ModelAttribute`), test `Assert.state(id!=null)` với pet id null.

---

## PHẦN F: MÃ NGUỒN HARNESS VÀ CẤU HÌNH TỰ ĐỘNG

### F.1. Cấu hình `pitest-maven` trong `pom.xml` (toàn văn khối plugin)

```xml
<properties>
  ...
  <pitest.version>1.30.0</pitest.version>
  <pitest-junit5.version>1.2.3</pitest-junit5.version>
</properties>
<build>
  <plugins>
    ...
    <!-- Mutation Testing harness (K03): PIT targeting core business package owner.* -->
    <plugin>
      <groupId>org.pitest</groupId>
      <artifactId>pitest-maven</artifactId>
      <version>${pitest.version}</version>
      <dependencies>
        <dependency>
          <groupId>org.pitest</groupId>
          <artifactId>pitest-junit5-plugin</artifactId>
          <version>${pitest-junit5.version}</version>
        </dependency>
      </dependencies>
      <configuration>
        <targetClasses>
          <param>org.springframework.samples.petclinic.owner.*</param>
        </targetClasses>
        <targetTests>
          <param>org.springframework.samples.petclinic.owner.*</param>
        </targetTests>
        <outputFormats>
          <param>HTML</param>
          <param>XML</param>
        </outputFormats>
        <mutators>
          <param>STRONGER</param>
        </mutators>
        <timestampedReports>false</timestampedReports>
        <threads>4</threads>
        <verbose>false</verbose>
      </configuration>
    </plugin>
```

Lệnh chạy (1 lệnh duy nhất, xem thêm Phần H):

```bash
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true
```

(`-Djacoco.skip=true` để JaCoCo agent không xung đột với coverage minion của PIT;
trên Windows PowerShell cần đặt trong dấu nháy: `'-Djacoco.skip=true'`.)
Báo cáo sinh tại `target/pit-reports/` (`index.html`, `mutations.xml`, HTML từng class).

### F.2. Các lớp test mới (7 files, 81 test methods, toàn bộ trong `src/test/java/.../owner/`)

| File | Số test | Phủ |
|---|---|---|
| `OwnerMutationTests` | 27 | `addPet`/`getPet`/`addVisit`/`toString` — decision table thuần unit |
| `PetValidatorMutationTests` | 9 | BVA 30/31 ký tự + decision table `isNew×type` |
| `PetVisitModelMutationTests` | 9 | `Pet`/`Visit` model + `PetTypeFormatter.print(null)` |
| `ControllerBinderMutationTests` | 5 | 4 binder `verify(setDisallowedFields)` + `minVisitDate` |
| `OwnerControllerMutationTests` | 6 | Pageable captor, OOB redirect, 2 lambda unknown-owner, id-mismatch direct |
| `PetControllerMutationTests` | 19 | side-effect captors, rethrow, detached-update, null-id guard, lambda direct |
| `VisitControllerMutationTests` | 6 | pending-visit assert, pet/owner unknown, null-date direct, delegation captor |

### F.3. Trích dẫn mã tiêu biểu

**Assert trạng thái sâu + bắt exception (MT-07, MT-10):**

```java
String view = controller.processUpdateForm(owner, detached, result,
        new RedirectAttributesModelMap());
assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
verify(repository).saveAndFlush(captor.capture());
Pet updated = captor.getValue().getPet(1);
assertThat(updated.getName()).isEqualTo("Betty");                    // giết VoidMethodCall setName
assertThat(updated.getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12)); // giết setBirthDate
assertThat(updated.getType().getName()).isEqualTo("hamster");        // giết setType
```

```java
assertThatThrownBy(() -> controller.processUpdateForm(owner, detached,
        new BeanPropertyBindingResult(detached, "pet"), new RedirectAttributesModelMap()))
    .isInstanceOf(IllegalStateException.class)
    .hasMessageContaining("'pet.getId()' must not be null");        // giết Assert.state removal
```

**Verify tương tác mock (binder):**

```java
new OwnerController(owners).setAllowedFields(binder);
verify(binder).setDisallowedFields("id", "*.id");                    // giết VoidMethodCall binder
```

**BVA biên 30 ký tự (MT-01):**

```java
pet.setName("A".repeat(30));
validator.validate(pet, errors);
assertThat(errors.hasFieldErrors("name")).isFalse();                 // giết ConditionalsBoundary
```

---

## PHẦN G: BÁO CÁO LOG, METRICS VÀ PHÂN TÍCH NGUYÊN NHÂN CỐT LÕI (RCA)

### G.1. Bảng so sánh Baseline vs Final (package `...owner.*`, mutator `STRONGER`, 195 mutants)

| Chỉ số | Baseline (test gốc) | Final (sau kill-loop) |
|---|---|---|
| Tổng mutants sinh ra | 195 | 195 |
| Killed | 131 (**67%**) | **192 (98%)** ✅ (ngưỡng ≥ 88%) |
| Survived | 55 | 3 (cả 3 là equivalent — xem G.4) |
| No coverage | 9 | **0** |
| Line coverage (lớp bị đột biến) | 242/250 (97%) | **250/250 (100%)** |
| Test units PIT xét | 20 | 27 |
| Số test chạy/mutant | 657 (3,37) | ~680+ (3,49+) |
| Thời gian phân tích | ~21 s | ~30–40 s |

Phân bố Killed cuối theo class: Owner 32, OwnerController 44, Pet 3, PetController 69,
PetTypeFormatter 6, PetValidator 17, Visit 2, VisitController 18 (+3 survived tương đương).

### G.2. Phân tích 2 mutant cứng đầu đã bị tiêu diệt

**Mutant 1 — `PetController.updatePetDetails:192-194` (`VoidMethodCall`: xóa `setName/setBirthDate/setType`).**
- Code gốc: `existingPet.setName(pet.getName()); existingPet.setBirthDate(...); existingPet.setType(...);`
- Code đột biến: ba dòng bị xóa (entity giữ giá trị cũ).
- Vì sao cứng đầu: mọi test MockMvc cũ đều pass — Spring binding đã ghi giá trị mới **lên cùng
  một instance** (`findPet` trả về entity trong `Owner`), khiến các lệnh copy thành no-op
  (branch cover đủ nhưng weak mutation không lan tới output).
- Test đã kill (`updateCopiesFieldsOntoManagedPet`): gọi trực tiếp với **detached instance**
  (managed `petty/2010-01-01/null` vs detached `Betty/2015-02-12/hamster`), capture entity
  `saveAndFlush` và assert từng field — mutant giữ giá trị cũ → fail. Đồng thời kill luôn
  mutant `RemoveConditional` dòng 190 (`existingPet != null`→false).

**Mutant 2 — `Owner.addPet:104` (`RemoveConditional`: `contains(pet)`→false, tức không return sớm).**
- Code gốc: `if (getPets().contains(pet)) return;`
- Vì sao cứng đầu: test cũ `addPetDoesNotAddDuplicatePet` dùng pet **đã persist (id=5)** —
  mutant bỏ `contains` vẫn bị vòng so-id phía dưới chặn lại (size vẫn 1) → sống.
- Test đã kill (`addPetRejectsSameNewInstanceTwice`): add cùng instance **mới (id null)** 2 lần —
  vòng so-id không thể kích hoạt (id null), chỉ `contains` mới chặn được; mutant cho size=2 → fail.

### G.3. Kết quả vòng lặp kill-loop (3 vòng)

- Vòng 0 (baseline): 67% — parse `mutations.xml`, nhóm 64 điểm yếu theo operator.
- Vòng 1 (+75 tests): **94%** (184/195) — xử lý toàn bộ binder-void, validator-BVA,
  delegation-captor, rethrow, pagination-math, OOB-redirect, lambda-Obi.
- Vòng 2 (+6 tests): **98%** (192/195) — xử lý detached-update (4 kills), same-new-instance (1),
  direct `findPet` lambda (1). Dừng vì 3 điểm còn lại được chứng minh equivalent (G.4).

### G.4. Equivalent Mutants (3/195) — chứng minh kỹ thuật

1. **`Owner.addPet:108` ×2 (`RemoveConditional_EQUAL_IF` trên `!existingPet.isNew()` và
   `!pet.isNew()`):** ép một trong hai conjunct thành `true`. Vì `isNew() ⟺ id == null`
   (`BaseEntity.isNew()` → `return this.id == null`), khi conjunct bị ép vốn đang `false`
   thì id tương ứng là `null`, kéo theo `Objects.equals(...)` chỉ có thể `true` khi id còn lại
   cũng `null` — tức conjunct kia cũng đang `false`. Hợp `&&` vẫn `false`; khi conjunct vốn
   `true` thì ép bằng giá trị thật. Mọi input cho cùng một kết quả ⇒ **tương đương, không thể kill**.
2. **`OwnerController.processUpdateOwnerForm:167` (`VoidMethodCall` xóa `owner.setId(ownerId)`):**
   nhánh mismatch (`!Objects.equals(owner.getId(), ownerId)`) đã return sớm, nên tới dòng này
   hai id **tất yếu bằng nhau** (thêm nữa `id` là disallowed field nên form không thể đổi id);
   gán cùng giá trị → `save` + redirect hoàn toàn giống nhau ⇒ **tương đương**.

### G.5. Báo cáo Defect theo chuẩn Error – Fault – Failure

- **Kết luận chính: KHÔNG phát hiện Fault trong `src/main/java`.** Production code giữ nguyên
  100% (chỉ `pom.xml` + `src/test` thay đổi). Mọi survived ban đầu đều do test yếu, không phải bug.
- **Điểm yếu thiết kế ghi nhận (không phải bug, không sửa code theo ràng buộc đề bài):**
  1. `OwnerController.showOwner` tra cứu `findById` lần 2 sau khi `@ModelAttribute findOwner`
     đã tra cứu — nhánh `orElseThrow` của nó chỉ reachable khi kết quả 2 lần đọc khác nhau
     (chỉ cover được bằng stub consecutive). *Error* tiềm ẩn: lập trình phòng thủ dư thừa;
     *Failure*: không quan sát được.
  2. `owner.setId(ownerId)` sau guard mismatch là dead-store phòng thủ (equivalent mutant).
  3. Hai integration test (`PostgresIntegrationTests`, MySQL tương ứng) phụ thuộc Docker daemon —
     *Failure* môi trường, không phải logic (đã loại khỏi gate tái hiện, ghi rõ trong README).

---

## PHẦN H: CỐ ĐỊNH PHIÊN BẢN (PIN COMMIT) & TÁI HIỆN TRÊN MÁY MỚI

### H.1. Commit đã khóa

- **Upstream:** `https://github.com/spring-projects/spring-petclinic`
- **SHA (HEAD tại thời điểm thực hiện):** `500158f732419217507c7656904b8e6aa1bcc0d6`
- **Branch:** `main` — message: *"added redirection to the page when the user types a page that is out of bounds"*
- **Ngày commit:** 2026-09-29. Kiểm tra: `git rev-parse HEAD` phải in đúng SHA trên.

### H.2. Tái hiện 100% trên máy mới (Windows; Linux/macOS dùng `./mvnw` tương ứng)

**Bước 0 — Cài JDK 17+** (ví dụ `winget install -e --id EclipseAdoptium.Temurin.17.JDK`)
và Git; đặt `JAVA_HOME` trỏ tới JDK 17. Không cần cài Maven (dùng wrapper) hay Docker
(Docker chỉ cần cho 2 lớp `*IntegrationTests`, đã loại khỏi gate).

```bash
git clone https://github.com/spring-projects/spring-petclinic.git Program_R01-K03
cd Program_R01-K03
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6
# chép đè 2 file cấu hình + 7 file test của nhóm (pom.xml, src/test/.../owner/*MutationTests.java,
#   ControllerBinderMutationTests.java) vào đúng vị trí, rồi chạy 1 lệnh:
./mvnw test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true
```

**Kết quả kỳ vọng:** `Generated 195 mutations Killed 192 (98%)`, `Line Coverage 250/250 (100%)`,
`BUILD SUCCESS`; báo cáo HTML tại `target/pit-reports/index.html`.
Gate nhanh (không PIT): `./mvnw test -Dtest='!*IntegrationTests'` → `Tests run: 153, Failures: 0, Errors: 0`.
Gate riêng owner: `./mvnw test -Dtest='org.springframework.samples.petclinic.owner.**'` → 130/130 pass.

> Lưu ý PowerShell: đặt `-D...` trong dấu nháy đơn (`'-Djacoco.skip=true'`).
> Lưu ý mạng lần đầu: Maven tải dependencies (~200 MB) nên lần chạy đầu cần Internet.
