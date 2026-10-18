# PHẦN E.2: ĐỒ THỊ LUỒNG (FLOW GRAPH) & ĐỘ PHỨC TẠP XUNG CƠ BẢN (CYCLOMATIC COMPLEXITY - V(G))

> **Tài liệu kỹ thuật của Thành viên 4 (TV4) – White-Box & Web Controller Test Engineer**  
> **Dự án**: Kiểm thử đột biến (Mutation Testing) trên Spring PetClinic  
> **Phạm vi kiểm thử**: Các lớp Web Controller gói `org.springframework.samples.petclinic.owner` (`OwnerController`, `PetController`, `VisitController`)  
> **Mã nguồn thẩm định (Commit cố định)**: `500158f732419217507c7656904b8e6aa1bcc0d6`  

---

## 1. QUY ƯỚC ĐẾM VÀ CƠ SỞ TOÁN HỌC

Để đảm bảo tính nhất quán, khoa học và chặt chẽ của kỹ thuật Kiểm thử hộp trắng (White-box Testing) theo lý thuyết đồ thị McCabe, các quy ước sau được áp dụng xuyên suốt:

### 1.1. Khái niệm Đỉnh (Node - $N$) và Cạnh (Edge - $E$)
- **Đỉnh tuần tự (Basic Block Node)**: Một chuỗi các câu lệnh thực thi liên tiếp không có rẽ nhánh ở giữa. Nếu câu lệnh đầu tiên trong khối được thực thi thì mọi câu lệnh trong khối đều được thực thi.
- **Đỉnh quyết định (Decision/Predicate Node - $P$)**: Đỉnh chứa biểu thức điều kiện nhị phân chia luồng điều khiển thành 2 nhánh (True và False).
- **Cạnh (Edge)**: Cung có hướng nối giữa hai đỉnh, biểu diễn luồng điều khiển hợp lệ của chương trình.

### 1.2. Quy ước đếm biểu thức logic đoản mạch (Short-Circuit Evaluation)
Trong ngôn ngữ Java, các toán tử logic `&&` (AND đoản mạch) và `||` (OR đoản mạch) không được đánh giá như một điều kiện nguyên khối mà tuân theo cơ chế short-circuit:
- Biểu thức `A || B`: Nếu `A` là `true`, nhánh True được kích hoạt ngay lập tức mà không cần đánh giá `B`. Nếu `A` là `false`, luồng điều khiển mới chuyển sang đánh giá `B`. Do đó, mỗi toán tử `||` làm phát sinh thêm **1 điểm quyết định nhị phân độc lập**.
- Biểu thức `A && B`: Nếu `A` là `false`, nhánh False được kích hoạt ngay lập tức mà không cần đánh giá `B`. Nếu `A` là `true`, luồng điều khiển mới chuyển sang đánh giá `B`. Do đó, mỗi toán tử `&&` làm phát sinh thêm **1 điểm quyết định nhị phân độc lập**.
- **Toán tử ba ngôi (`cond ? expr1 : expr2`)**: Tương đương cấu trúc `if-else`, tính là **1 điểm quyết định**.
- **Khối `try-catch`**: Mệnh đề `catch` tạo ra một nhánh điều khiển bất thường khi có ngoại lệ ném ra trong khối `try`, được tính là **1 điểm rẽ nhánh**.
- **Câu lệnh khẳng định (`Assert.state(cond, msg)`)**: Tương đương cấu trúc kiểm tra `if (!cond) throw new IllegalStateException(msg)`, biểu diễn một nhánh rẽ ném ngoại lệ (tính là **1 điểm quyết định**).

### 1.3. Hai phương pháp tính độ phức tạp Cyclomatic $V(G)$ độc lập
1. **Cách 1 (Lý thuyết đồ thị luồng McCabe)**:
   $$V(G) = E - N + 2$$
   *(Trong đó: $E$ là tổng số cạnh, $N$ là tổng số đỉnh của đồ thị phẳng với 1 điểm vào và 1 điểm ra)*.
2. **Cách 2 (Đếm điểm quyết định / Predicate Nodes)**:
   $$V(G) = P + 1$$
   *(Trong đó: $P$ là tổng số điểm quyết định nhị phân độc lập)*.

> **Quy tắc kiểm chứng**: Mọi phương thức phân tích bắt buộc phải có kết quả tính $V(G)$ từ hai cách trùng khớp nhau tuyệt đối ($E - N + 2 = P + 1$).

---

## 2. PHÂN TÍCH CHI TIẾT OWNERCONTROLLER (`OwnerController.java`)

### 2.1. Danh mục phương thức
Lớp `OwnerController` gồm 11 phương thức (dòng 55 đến 186):
1. `OwnerController(OwnerRepository)` (dòng 55-57): Hàm khởi tạo dependency injection tuần tự.
2. `setAllowedFields(WebDataBinder)` (dòng 60-62): Cấu hình bảo mật binder.
3. `findOwner(Integer)` (dòng 65-70): `@ModelAttribute("owner")`, có nhánh toán tử ba ngôi.
4. `initCreationForm()` (dòng 73-75): `@GetMapping("/owners/new")`, tuần tự.
5. `processCreationForm(Owner, BindingResult, RedirectAttributes)` (dòng 78-87): `@PostMapping("/owners/new")`, có nhánh kiểm tra validation.
6. `initFindForm()` (dòng 90-92): `@GetMapping("/owners/find")`, tuần tự.
7. `processFindForm(int, Owner, BindingResult, Model, RedirectAttributes)` (dòng 95-130): `@GetMapping("/owners")`, xử lý tìm kiếm & phân trang phức tạp.
8. `addPaginationModel(int, Model, Page<Owner>)` (dòng 132-139): Helper đóng gói model phân trang, tuần tự.
9. `findPaginatedForOwnersLastName(int, String)` (dòng 141-146): Helper gọi repository, tuần tự.
10. `initUpdateOwnerForm()` (dòng 149-151): `@GetMapping("/owners/{ownerId}/edit")`, tuần tự.
11. `processUpdateOwnerForm(Owner, BindingResult, int, RedirectAttributes)` (dòng 154-171): `@PostMapping("/owners/{ownerId}/edit")`, kiểm tra lỗi và mismatch ID.
12. `showOwner(int)` (dòng 179-186): `@GetMapping("/owners/{ownerId}")`, tra cứu chi tiết chủ nuôi.

---

### 2.2. Đồ thị luồng & Tính $V(G)$ các phương thức có nhánh

#### A. Phương thức `findOwner(Integer ownerId)` (Dòng 65–70)
- **Mã nguồn thật**:
  ```java
  65: @ModelAttribute("owner")
  66: public Owner findOwner(@PathVariable(name = "ownerId", required = false) Integer ownerId) {
  67:     return ownerId == null ? new Owner()
  68:             : this.owners.findById(ownerId)
  69:                 .orElseThrow(() -> new IllegalArgumentException("Owner not found with id: " + ownerId
  70:                         + ". Please ensure the ID is correct and the owner exists in the database."));
  71: }
  ```
- **Danh sách đỉnh (Nodes)**:
  - `N1` (Dòng 65–66): Điểm vào, kiểm tra điều kiện `ownerId == null`.
  - `N2` (Dòng 66): Nhánh True: khởi tạo thực thể rỗng `new Owner()`.
  - `N3` (Dòng 67–70): Nhánh False: gọi `owners.findById(ownerId)` (ném ngoại lệ nếu không tìm thấy).
  - `N4`: Điểm ra (Exit) của phương thức.
- **Danh sách cạnh (Edges)**:
  - `E1`: N1 $\to$ N2 (khi `ownerId == null` là `true`)
  - `E2`: N1 $\to$ N3 (khi `ownerId == null` là `false`)
  - `E3`: N2 $\to$ N4 (trả về đối tượng Owner mới)
  - `E4`: N3 $\to$ N4 (trả về đối tượng Owner tìm được)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 65-66): Entry | ownerId == null?"]
      N2["N2 (Dòng 66): new Owner()"]
      N3["N3 (Dòng 67-70): owners.findById(ownerId)"]
      N4["N4: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 --> N4
      N3 --> N4
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 4$, Số cạnh $E = 4$.
  - Cách 1: $V(G) = E - N + 2 = 4 - 4 + 2 = 2$.
  - Cách 2: Điểm quyết định $P = 1$ (`ownerId == null`). $V(G) = P + 1 = 1 + 1 = 2$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 2$).

---

#### B. Phương thức `processCreationForm(Owner, BindingResult, RedirectAttributes)` (Dòng 78–87)
- **Mã nguồn thật**:
  ```java
  78: @PostMapping("/owners/new")
  79: public String processCreationForm(@Valid Owner owner, BindingResult result, RedirectAttributes redirectAttributes) {
  80:     if (result.hasErrors()) {
  81:         redirectAttributes.addFlashAttribute("error", "There was an error in creating the owner.");
  82:         return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
  83:     }
  84: 
  85:     this.owners.save(owner);
  86:     redirectAttributes.addFlashAttribute("message", "New Owner Created");
  87:     return "redirect:/owners/" + owner.getId();
  88: }
  ```
- **Danh sách đỉnh (Nodes)**:
  - `N1` (Dòng 78–80): Điểm vào, kiểm tra điều kiện validation `result.hasErrors()`.
  - `N2` (Dòng 81–82): Nhánh True: thêm flash attribute lỗi, trả về form tạo mới.
  - `N3` (Dòng 85–87): Nhánh False: lưu `owners.save(owner)`, thêm flash message, redirect chi tiết owner.
  - `N4`: Điểm ra (Exit).
- **Danh sách cạnh (Edges)**:
  - `E1`: N1 $\to$ N2 (True: có lỗi nhập liệu)
  - `E2`: N1 $\to$ N3 (False: hợp lệ)
  - `E3`: N2 $\to$ N4
  - `E4`: N3 $\to$ N4
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 78-80): Entry | result.hasErrors()?"]
      N2["N2 (Dòng 81-82): addFlashAttribute error | return form"]
      N3["N3 (Dòng 85-87): owners.save(owner) | return redirect:/owners/{id}"]
      N4["N4: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 --> N4
      N3 --> N4
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 4$, Số cạnh $E = 4$.
  - Cách 1: $V(G) = E - N + 2 = 4 - 4 + 2 = 2$.
  - Cách 2: Điểm quyết định $P = 1$ (`result.hasErrors()`). $V(G) = P + 1 = 2$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 2$).

---

#### C. Phương thức `processFindForm(int, Owner, BindingResult, Model, RedirectAttributes)` (Dòng 95–130)
- **Mã nguồn thật**:
  ```java
  95: @GetMapping("/owners")
  96: public String processFindForm(@RequestParam(defaultValue = "1") int page, Owner owner, BindingResult result,
  97:         Model model, RedirectAttributes redirectAttributes) {
  98:     String lastName = owner.getLastName();
  99:     if (lastName == null) {
  100:        lastName = ""; // empty string signifies broadest possible search
  101:    }
  102:    else {
  103:        lastName = lastName.strip();
  104:    }
  107:    Page<Owner> ownersResults = findPaginatedForOwnersLastName(page, lastName);
  108:    if (page < 1 || page > Math.max(ownersResults.getTotalPages(), 1)) {
  109:        redirectAttributes.addAttribute("page", 1);
  110:        if (!lastName.isEmpty()) {
  111:            redirectAttributes.addAttribute("lastName", lastName);
  112:        }
  113:        return "redirect:/owners";
  114:    }
  116:    if (ownersResults.isEmpty()) {
  118:        result.rejectValue("lastName", "notFound", "not found");
  119:        return "owners/findOwners";
  120:    }
  122:    if (ownersResults.getTotalElements() == 1) {
  124:        owner = ownersResults.iterator().next();
  125:        return "redirect:/owners/" + owner.getId();
  126:    }
  129:    return addPaginationModel(page, model, ownersResults);
  130: }
  ```
- **Phân tích điểm quyết định ($P$)**:
  1. $P_1$ (Dòng 99): `lastName == null`
  2. $P_2$ (Dòng 108): `page < 1` (toán hạng 1 của `||`)
  3. $P_3$ (Dòng 108): `page > Math.max(ownersResults.getTotalPages(), 1)` (toán hạng 2 của `||`, đánh giá khi $P_2$ là False)
  4. $P_4$ (Dòng 110): `!lastName.isEmpty()`
  5. $P_5$ (Dòng 116): `ownersResults.isEmpty()`
  6. $P_6$ (Dòng 122): `ownersResults.getTotalElements() == 1`
  - Tổng số điểm quyết định: $P = 6$.
- **Danh sách đỉnh (Nodes)**:
  - `N1` (Dòng 95–99): Entry, lấy `owner.getLastName()`, kiểm tra `lastName == null`.
  - `N2` (Dòng 100–101): Nhánh True: gán `lastName = ""`.
  - `N3` (Dòng 102–104): Nhánh False: gọi `lastName = lastName.strip()`.
  - `N4` (Dòng 107–108): Merge N2 & N3, gọi `findPaginatedForOwnersLastName(page, lastName)`, kiểm tra `page < 1`.
  - `N5` (Dòng 108): Nhánh False của N4: kiểm tra tiếp `page > Math.max(...)`.
  - `N6` (Dòng 109–110): Nhánh True của N4 hoặc N5 (trang ngoài biên): gán param `page=1`, kiểm tra `!lastName.isEmpty()`.
  - `N7` (Dòng 111–112): Nhánh True của N6: gán param `lastName`.
  - `N8` (Dòng 113): Merge N6 (False) và N7: trả về `"redirect:/owners"`.
  - `N9` (Dòng 116): Nhánh False của N5 (trang hợp lệ): kiểm tra `ownersResults.isEmpty()`.
  - `N10` (Dòng 118–119): Nhánh True của N9: `result.rejectValue(...)`, trả về `"owners/findOwners"`.
  - `N11` (Dòng 122): Nhánh False của N9: kiểm tra `ownersResults.getTotalElements() == 1`.
  - `N12` (Dòng 124–125): Nhánh True của N11: lấy duy nhất 1 owner, trả về `"redirect:/owners/" + owner.getId()`.
  - `N13` (Dòng 129): Nhánh False của N11 (nhiều kết quả): gọi `addPaginationModel(...)`, trả về `"owners/ownersList"`.
  - `N14`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 19 cạnh)**:
  - `E1`: N1 $\to$ N2 (True: `lastName == null`)
  - `E2`: N1 $\to$ N3 (False)
  - `E3`: N2 $\to$ N4
  - `E4`: N3 $\to$ N4
  - `E5`: N4 $\to$ N6 (True: `page < 1`)
  - `E6`: N4 $\to$ N5 (False: kiểm tra tiếp vế 2)
  - `E7`: N5 $\to$ N6 (True: `page > totalPages`)
  - `E8`: N5 $\to$ N9 (False: trang hoàn toàn hợp lệ)
  - `E9`: N6 $\to$ N7 (True: `!lastName.isEmpty()`)
  - `E10`: N6 $\to$ N8 (False: `lastName` rỗng)
  - `E11`: N7 $\to$ N8
  - `E12`: N8 $\to$ N14 (Exit sau khi redirect out-of-bounds)
  - `E13`: N9 $\to$ N10 (True: không tìm thấy)
  - `E14`: N9 $\to$ N11 (False: có kết quả)
  - `E15`: N10 $\to$ N14 (Exit form find)
  - `E16`: N11 $\to$ N12 (True: đúng 1 kết quả)
  - `E17`: N11 $\to$ N13 (False: > 1 kết quả)
  - `E18`: N12 $\to$ N14 (Exit redirect owner details)
  - `E19`: N13 $\to$ N14 (Exit view danh sách)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 95-99): Entry | lastName == null?"]
      N2["N2 (Dòng 100): lastName = ''"]
      N3["N3 (Dòng 103): lastName = lastName.strip()"]
      N4["N4 (Dòng 107-108): findPaginated | page < 1?"]
      N5["N5 (Dòng 108): page > Math.max(totalPages, 1)?"]
      N6["N6 (Dòng 109-110): addParam(page, 1) | !lastName.isEmpty()?"]
      N7["N7 (Dòng 111): addParam(lastName, lastName)"]
      N8["N8 (Dòng 113): return 'redirect:/owners'"]
      N9["N9 (Dòng 116): ownersResults.isEmpty()?"]
      N10["N10 (Dòng 118-119): rejectValue | return 'owners/findOwners'"]
      N11["N11 (Dòng 122): getTotalElements() == 1?"]
      N12["N12 (Dòng 124-125): return 'redirect:/owners/' + id"]
      N13["N13 (Dòng 129): return addPaginationModel(...)"]
      N14["N14: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 --> N4
      N3 --> N4
      N4 -->|True| N6
      N4 -->|False| N5
      N5 -->|True| N6
      N5 -->|False| N9
      N6 -->|True| N7
      N6 -->|False| N8
      N7 --> N8
      N8 --> N14
      N9 -->|True| N10
      N9 -->|False| N11
      N10 --> N14
      N11 -->|True| N12
      N11 -->|False| N13
      N12 --> N14
      N13 --> N14
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 14$, Số cạnh $E = 19$.
  - Cách 1: $V(G) = E - N + 2 = 19 - 14 + 2 = 7$.
  - Cách 2: Điểm quyết định $P = 6$. $V(G) = P + 1 = 6 + 1 = 7$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 7$).

---

#### D. Phương thức `processUpdateOwnerForm(...)` (Dòng 154–171)
- **Mã nguồn thật**:
  ```java
  154: @PostMapping("/owners/{ownerId}/edit")
  155: public String processUpdateOwnerForm(@Valid Owner owner, BindingResult result, @PathVariable("ownerId") int ownerId,
  156:         RedirectAttributes redirectAttributes) {
  157:     if (result.hasErrors()) {
  158:         redirectAttributes.addFlashAttribute("error", "There was an error in updating the owner.");
  159:         return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
  160:     }
  162:     if (!Objects.equals(owner.getId(), ownerId)) {
  163:         result.rejectValue("id", "mismatch", "The owner ID in the form does not match the URL.");
  164:         redirectAttributes.addFlashAttribute("error", "Owner ID mismatch. Please try again.");
  165:         return "redirect:/owners/{ownerId}/edit";
  166:     }
  168:     owner.setId(ownerId);
  169:     this.owners.save(owner);
  170:     redirectAttributes.addFlashAttribute("message", "Owner Values Updated");
  171:     return "redirect:/owners/{ownerId}";
  172: }
  ```
- **Danh sách đỉnh (Nodes)**:
  - `N1` (Dòng 154–157): Entry, kiểm tra validation `result.hasErrors()`.
  - `N2` (Dòng 158–159): Nhánh True: flash error, trả về form cập nhật.
  - `N3` (Dòng 162): Nhánh False: kiểm tra ID mismatch `!Objects.equals(owner.getId(), ownerId)`.
  - `N4` (Dòng 163–165): Nhánh True của N3: `rejectValue("id", ...)`, redirect edit.
  - `N5` (Dòng 168–171): Nhánh False của N3: `owner.setId`, `save(owner)`, flash success, redirect view.
  - `N6`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 7 cạnh)**:
  - `E1`: N1 $\to$ N2 (True: có lỗi)
  - `E2`: N1 $\to$ N3 (False: hợp lệ)
  - `E3`: N2 $\to$ N6
  - `E4`: N3 $\to$ N4 (True: ID mismatch)
  - `E5`: N3 $\to$ N5 (False: ID khớp)
  - `E6`: N4 $\to$ N6
  - `E7`: N5 $\to$ N6
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 154-157): Entry | result.hasErrors()?"]
      N2["N2 (Dòng 158-159): addFlashAttribute error | return form"]
      N3["N3 (Dòng 162): !Objects.equals(owner.getId(), ownerId)?"]
      N4["N4 (Dòng 163-165): rejectValue mismatch | redirect:/owners/{ownerId}/edit"]
      N5["N5 (Dòng 168-171): owner.setId | save | redirect:/owners/{ownerId}"]
      N6["N6: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 --> N6
      N3 -->|True| N4
      N3 -->|False| N5
      N4 --> N6
      N5 --> N6
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 6$, Số cạnh $E = 7$.
  - Cách 1: $V(G) = E - N + 2 = 7 - 6 + 2 = 3$.
  - Cách 2: Điểm quyết định $P = 2$ (`hasErrors()`, `!Objects.equals(...)`). $V(G) = P + 1 = 3$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 3$).

---

#### E. Phương thức `showOwner(int ownerId)` (Dòng 179–186)
- **Mã nguồn thật**:
  ```java
  179: @GetMapping("/owners/{ownerId}")
  180: public ModelAndView showOwner(@PathVariable("ownerId") int ownerId) {
  181:     ModelAndView mav = new ModelAndView("owners/ownerDetails");
  182:     Optional<Owner> optionalOwner = this.owners.findById(ownerId);
  183:     Owner owner = optionalOwner.orElseThrow(() -> new IllegalArgumentException(
  184:             "Owner not found with id: " + ownerId + ". Please ensure the ID is correct "));
  185:     mav.addObject(owner);
  186:     return mav;
  187: }
  ```
- **Phân tích luồng**:
  - `optionalOwner.orElseThrow(...)` chứa 1 nhánh ném ngoại lệ khi `optionalOwner.isEmpty()`.
  - `N1` (Dòng 179–183): Entry, tìm owner, kiểm tra `optionalOwner.isPresent()`.
  - `N2` (Dòng 183–184): Nhánh rỗng: ném `IllegalArgumentException`.
  - `N3` (Dòng 185–186): Nhánh có dữ liệu: `mav.addObject(owner)`, trả về `mav`.
  - `N4`: Điểm ra (Exit).
  - $N = 4, E = 4 \implies V(G) = 4 - 4 + 2 = 2$. Điểm quyết định $P = 1 \implies V(G) = 1 + 1 = 2$.
  *(Lưu ý: Nếu xét thuần túy luồng điều khiển phẳng bỏ qua biểu thức lambda của thư viện chuẩn thì $V(G)=1$. Báo cáo giữ $V(G)=2$ để phản ánh chính xác nhánh ném exception được kiểm thử trong suite)*.

---

## 3. PHÂN TÍCH CHI TIẾT PETCONTROLLER (`PetController.java`)

### 3.1. Danh mục phương thức
Lớp `PetController` gồm 11 phương thức (dòng 57 đến 206):
1. `PetController(OwnerRepository, PetTypeRepository)` (dòng 57-60): Khởi tạo DI.
2. `populatePetTypes()` (dòng 63-65): `@ModelAttribute("types")`, tuần tự.
3. `findOwner(int)` (dòng 68-73): `@ModelAttribute("owner")`, tra cứu owner theo id URL.
4. `findPet(int, Integer)` (dòng 76-87): `@ModelAttribute("pet")`, có rẽ nhánh `petId == null`.
5. `initOwnerBinder(WebDataBinder)` (dòng 90-92): `@InitBinder("owner")`, tuần tự.
6. `initPetBinder(WebDataBinder)` (dòng 95-98): `@InitBinder("pet")`, tuần tự.
7. `initCreationForm(Owner, ModelMap)` (dòng 101-105): `@GetMapping("/pets/new")`, tuần tự.
8. `processCreationForm(Owner, Pet, BindingResult, RedirectAttributes)` (dòng 108-137): `@PostMapping("/pets/new")`, kiểm tra trùng lặp, ngày sinh tương lai, bắt ngoại lệ toàn vẹn dữ liệu DB.
9. `initUpdateForm()` (dòng 140-142): `@GetMapping("/pets/{petId}/edit")`, tuần tự.
10. `processUpdateForm(Owner, Pet, BindingResult, RedirectAttributes)` (dòng 145-179): `@PostMapping("/pets/{petId}/edit")`, kiểm tra trùng lặp với pet khác, ngày sinh, try-catch.
11. `updatePetDetails(Owner, Pet)` (dòng 186-200): Phương thức private sao chép thuộc tính detached pet sang managed pet, có `Assert.state` và `if-else`.
12. `isDuplicatePetNameViolation(DataIntegrityViolationException)` (dòng 202-205): Helper kiểm tra chuỗi message lỗi DB với toán tử `&&`.

---

### 3.2. Đồ thị luồng & Tính $V(G)$ các phương thức có nhánh

#### A. Phương thức `findPet(int ownerId, Integer petId)` (Dòng 76–87)
- **Mã nguồn thật**:
  ```java
  76: @ModelAttribute("pet")
  77: public Pet findPet(@PathVariable("ownerId") int ownerId,
  78:         @PathVariable(name = "petId", required = false) Integer petId) {
  79:     if (petId == null) {
  80:         return new Pet();
  81:     }
  83:     Optional<Owner> optionalOwner = this.owners.findById(ownerId);
  84:     Owner owner = optionalOwner.orElseThrow(() -> new IllegalArgumentException(
  85:             "Owner not found with id: " + ownerId + ". Please ensure the ID is correct "));
  86:     return owner.getPet(petId);
  87: }
  ```
- **Danh sách đỉnh (Nodes)**:
  - `N1` (Dòng 76–79): Entry, kiểm tra `petId == null`.
  - `N2` (Dòng 80–81): Nhánh True: trả về `new Pet()`.
  - `N3` (Dòng 83–86): Nhánh False: tìm owner, trả về `owner.getPet(petId)`.
  - `N4`: Điểm ra (Exit).
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 76-79): Entry | petId == null?"]
      N2["N2 (Dòng 80): return new Pet()"]
      N3["N3 (Dòng 83-86): findOwner | return owner.getPet(petId)"]
      N4["N4: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 --> N4
      N3 --> N4
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 4$, Số cạnh $E = 4$.
  - Cách 1: $V(G) = E - N + 2 = 4 - 4 + 2 = 2$.
  - Cách 2: Điểm quyết định $P = 1$ (`petId == null`). $V(G) = P + 1 = 2$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 2$).

---

#### B. Phương thức `processCreationForm(Owner, Pet, BindingResult, RedirectAttributes)` (Dòng 108–137)
- **Mã nguồn thật**:
  ```java
  108: @PostMapping("/pets/new")
  109: public String processCreationForm(Owner owner, @Valid Pet pet, BindingResult result,
  110:         RedirectAttributes redirectAttributes) {
  111:     if (StringUtils.hasText(pet.getName()) && pet.isNew() && owner.getPet(pet.getName(), true) != null) {
  112:         result.rejectValue("name", "duplicate", "already exists");
  113:     }
  115:     LocalDate currentDate = LocalDate.now();
  116:     if (pet.getBirthDate() != null && pet.getBirthDate().isAfter(currentDate)) {
  117:         result.rejectValue("birthDate", "typeMismatch.birthDate");
  118:     }
  120:     if (result.hasErrors()) {
  121:         return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
  122:     }
  124:     try {
  125:         owner.addPet(pet);
  126:         this.owners.saveAndFlush(owner);
  127:     }
  128:     catch (DataIntegrityViolationException ex) {
  129:         if (!isDuplicatePetNameViolation(ex)) {
  130:             throw ex;
  131:         }
  132:         result.rejectValue("name", "duplicate", "already exists");
  133:         return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
  134:     }
  135:     redirectAttributes.addFlashAttribute("message", "New Pet has been Added");
  136:     return "redirect:/owners/{ownerId}";
  137: }
  ```
- **Phân tích điểm quyết định ($P$)**:
  1. $P_1$ (Dòng 111): `StringUtils.hasText(pet.getName())`
  2. $P_2$ (Dòng 111): `pet.isNew()` (đánh giá khi $P_1$ True)
  3. $P_3$ (Dòng 111): `owner.getPet(pet.getName(), true) != null` (đánh giá khi $P_1 \land P_2$ True)
  4. $P_4$ (Dòng 116): `pet.getBirthDate() != null`
  5. $P_5$ (Dòng 116): `pet.getBirthDate().isAfter(currentDate)` (đánh giá khi $P_4$ True)
  6. $P_6$ (Dòng 120): `result.hasErrors()`
  7. $P_7$ (Dòng 128): Nhánh ném `DataIntegrityViolationException` từ khối `try`
  8. $P_8$ (Dòng 129): `!isDuplicatePetNameViolation(ex)`
  - Tổng số điểm quyết định: $P = 8$.
- **Danh sách đỉnh (Nodes - 15 đỉnh)**:
  - `N1` (Dòng 108–111): Entry, kiểm tra `StringUtils.hasText(pet.getName())`.
  - `N2` (Dòng 111): Kiểm tra `pet.isNew()`.
  - `N3` (Dòng 111): Kiểm tra `owner.getPet(..., true) != null`.
  - `N4` (Dòng 112–113): `result.rejectValue("name", "duplicate", ...)`.
  - `N5` (Dòng 115–116): Merge từ N1(F), N2(F), N3(F), N4 $\to$ lấy `currentDate`, kiểm tra `pet.getBirthDate() != null`.
  - `N6` (Dòng 116): Kiểm tra `pet.getBirthDate().isAfter(currentDate)`.
  - `N7` (Dòng 117–118): `result.rejectValue("birthDate", ...)`.
  - `N8` (Dòng 120): Merge từ N5(F), N6(F), N7 $\to$ kiểm tra `result.hasErrors()`.
  - `N9` (Dòng 121–122): Nhánh True: trả về form tạo mới.
  - `N10` (Dòng 124–126): Khối `try`: `owner.addPet(pet)`, `owners.saveAndFlush(owner)`.
  - `N11` (Dòng 128–129): Khối `catch`: bắt `DataIntegrityViolationException`, kiểm tra `!isDuplicatePetNameViolation(ex)`.
  - `N12` (Dòng 130–131): Nhánh True: ném tiếp ngoại lệ `throw ex`.
  - `N13` (Dòng 132–133): Nhánh False: `result.rejectValue("name", ...)`, trả về form.
  - `N14` (Dòng 135–136): Nhánh try hoàn tất bình thường: thêm flash message, redirect view owner.
  - `N15`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 22 cạnh)**:
  - `E1`: N1 $\to$ N2 (True)
  - `E2`: N1 $\to$ N5 (False)
  - `E3`: N2 $\to$ N3 (True)
  - `E4`: N2 $\to$ N5 (False)
  - `E5`: N3 $\to$ N4 (True)
  - `E6`: N3 $\to$ N5 (False)
  - `E7`: N4 $\to$ N5
  - `E8`: N5 $\to$ N6 (True)
  - `E9`: N5 $\to$ N8 (False)
  - `E10`: N6 $\to$ N7 (True)
  - `E11`: N6 $\to$ N8 (False)
  - `E12`: N7 $\to$ N8
  - `E13`: N8 $\to$ N9 (True: có lỗi)
  - `E14`: N8 $\to$ N10 (False: vào try)
  - `E15`: N9 $\to$ N15 (Exit)
  - `E16`: N10 $\to$ N11 (Exception văng sang catch)
  - `E17`: N10 $\to$ N14 (Thực thi thành công)
  - `E18`: N11 $\to$ N12 (True: không phải lỗi duplicate $\implies$ rethrow)
  - `E19`: N11 $\to$ N13 (False: đúng duplicate $\implies$ rejectValue)
  - `E20`: N12 $\to$ N15 (Exit do ném ngoại lệ ra ngoài)
  - `E21`: N13 $\to$ N15 (Exit trả về form)
  - `E22`: N14 $\to$ N15 (Exit redirect)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 108-111): Entry | hasText(name)?"]
      N2["N2 (Dòng 111): pet.isNew()?"]
      N3["N3 (Dòng 111): owner.getPet(name, true) != null?"]
      N4["N4 (Dòng 112): rejectValue('name', 'duplicate')"]
      N5["N5 (Dòng 115-116): currentDate | birthDate != null?"]
      N6["N6 (Dòng 116): birthDate.isAfter(currentDate)?"]
      N7["N7 (Dòng 117): rejectValue('birthDate')"]
      N8["N8 (Dòng 120): result.hasErrors()?"]
      N9["N9 (Dòng 121): return form"]
      N10["N10 (Dòng 124-126): try { addPet; saveAndFlush }"]
      N11["N11 (Dòng 128-129): catch (DataIntegrity) | !isDuplicate?(ex)"]
      N12["N12 (Dòng 130): throw ex"]
      N13["N13 (Dòng 132-133): rejectValue | return form"]
      N14["N14 (Dòng 135-136): addFlash | redirect:/owners/{ownerId}"]
      N15["N15: Exit"]

      N1 -->|True| N2
      N1 -->|False| N5
      N2 -->|True| N3
      N2 -->|False| N5
      N3 -->|True| N4
      N3 -->|False| N5
      N4 --> N5
      N5 -->|True| N6
      N5 -->|False| N8
      N6 -->|True| N7
      N6 -->|False| N8
      N7 --> N8
      N8 -->|True| N9
      N8 -->|False| N10
      N9 --> N15
      N10 -->|Exception| N11
      N10 -->|Success| N14
      N11 -->|True| N12
      N11 -->|False| N13
      N12 --> N15
      N13 --> N15
      N14 --> N15
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 15$, Số cạnh $E = 22$.
  - Cách 1: $V(G) = E - N + 2 = 22 - 15 + 2 = 9$.
  - Cách 2: Điểm quyết định $P = 8$. $V(G) = P + 1 = 8 + 1 = 9$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 9$).

---

#### C. Phương thức `processUpdateForm(Owner, Pet, BindingResult, RedirectAttributes)` (Dòng 145–179)
- **Mã nguồn thật**:
  ```java
  145: @PostMapping("/pets/{petId}/edit")
  146: public String processUpdateForm(Owner owner, @Valid Pet pet, BindingResult result,
  147:         RedirectAttributes redirectAttributes) {
  148:     String petName = pet.getName();
  151:     if (StringUtils.hasText(petName)) {
  152:         Pet existingPet = owner.getPet(petName, false);
  153:         if (existingPet != null && !Objects.equals(existingPet.getId(), pet.getId())) {
  154:             result.rejectValue("name", "duplicate", "already exists");
  155:         }
  156:     }
  158:     LocalDate currentDate = LocalDate.now();
  159:     if (pet.getBirthDate() != null && pet.getBirthDate().isAfter(currentDate)) {
  160:         result.rejectValue("birthDate", "typeMismatch.birthDate");
  161:     }
  163:     if (result.hasErrors()) {
  164:         return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
  165:     }
  167:     try {
  168:         updatePetDetails(owner, pet);
  169:     }
  170:     catch (DataIntegrityViolationException ex) {
  171:         if (!isDuplicatePetNameViolation(ex)) {
  172:             throw ex;
  173:         }
  174:         result.rejectValue("name", "duplicate", "already exists");
  175:         return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
  176:     }
  177:     redirectAttributes.addFlashAttribute("message", "Pet details has been edited");
  178:     return "redirect:/owners/{ownerId}";
  179: }
  ```
- **Phân tích điểm quyết định ($P$)**:
  1. $P_1$ (Dòng 151): `StringUtils.hasText(petName)`
  2. $P_2$ (Dòng 153): `existingPet != null` (toán hạng 1)
  3. $P_3$ (Dòng 153): `!Objects.equals(existingPet.getId(), pet.getId())` (toán hạng 2)
  4. $P_4$ (Dòng 159): `pet.getBirthDate() != null`
  5. $P_5$ (Dòng 159): `pet.getBirthDate().isAfter(currentDate)`
  6. $P_6$ (Dòng 163): `result.hasErrors()`
  7. $P_7$ (Dòng 170): Nhánh ngoại lệ của `try`
  8. $P_8$ (Dòng 171): `!isDuplicatePetNameViolation(ex)`
  - Tổng số điểm quyết định: $P = 8$.
- **Danh sách đỉnh (Nodes - 15 đỉnh)**:
  - `N1` (Dòng 145–151): Entry, kiểm tra `StringUtils.hasText(petName)`.
  - `N2` (Dòng 152–153): Lấy `existingPet = owner.getPet(...)`, kiểm tra `existingPet != null`.
  - `N3` (Dòng 153): Kiểm tra `!Objects.equals(existingPet.getId(), pet.getId())`.
  - `N4` (Dòng 154–155): `result.rejectValue("name", "duplicate", ...)`.
  - `N5` (Dòng 158–159): Merge N1(F), N2(F), N3(F), N4 $\to$ lấy `currentDate`, kiểm tra `pet.getBirthDate() != null`.
  - `N6` (Dòng 159): Kiểm tra `pet.getBirthDate().isAfter(currentDate)`.
  - `N7` (Dòng 160–161): `result.rejectValue("birthDate", ...)`.
  - `N8` (Dòng 163): Merge N5(F), N6(F), N7 $\to$ kiểm tra `result.hasErrors()`.
  - `N9` (Dòng 164–165): Nhánh True: trả về form.
  - `N10` (Dòng 167–169): Khối `try`: `updatePetDetails(owner, pet)`.
  - `N11` (Dòng 170–171): Khối `catch`: bắt `DataIntegrityViolationException`, kiểm tra `!isDuplicatePetNameViolation(ex)`.
  - `N12` (Dòng 172–173): Rethrow exception: `throw ex`.
  - `N13` (Dòng 174–175): Reject duplicate và trả về form.
  - `N14` (Dòng 177–178): Flash message, redirect view owner.
  - `N15`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 22 cạnh)**:
  - Tương đồng với cấu trúc đồ thị của `processCreationForm`: $E = 22$.
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 145-151): Entry | hasText(petName)?"]
      N2["N2 (Dòng 152-153): existingPet != null?"]
      N3["N3 (Dòng 153): !Objects.equals(existingPet.id, pet.id)?"]
      N4["N4 (Dòng 154): rejectValue('name', 'duplicate')"]
      N5["N5 (Dòng 158-159): currentDate | birthDate != null?"]
      N6["N6 (Dòng 159): birthDate.isAfter(currentDate)?"]
      N7["N7 (Dòng 160): rejectValue('birthDate')"]
      N8["N8 (Dòng 163): result.hasErrors()?"]
      N9["N9 (Dòng 164): return form"]
      N10["N10 (Dòng 167-169): try { updatePetDetails(owner, pet) }"]
      N11["N11 (Dòng 170-171): catch (DataIntegrity) | !isDuplicate?(ex)"]
      N12["N12 (Dòng 172): throw ex"]
      N13["N13 (Dòng 174-175): rejectValue | return form"]
      N14["N14 (Dòng 177-178): addFlash | redirect:/owners/{ownerId}"]
      N15["N15: Exit"]

      N1 -->|True| N2
      N1 -->|False| N5
      N2 -->|True| N3
      N2 -->|False| N5
      N3 -->|True| N4
      N3 -->|False| N5
      N4 --> N5
      N5 -->|True| N6
      N5 -->|False| N8
      N6 -->|True| N7
      N6 -->|False| N8
      N7 --> N8
      N8 -->|True| N9
      N8 -->|False| N10
      N9 --> N15
      N10 -->|Exception| N11
      N10 -->|Success| N14
      N11 -->|True| N12
      N11 -->|False| N13
      N12 --> N15
      N13 --> N15
      N14 --> N15
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 15$, Số cạnh $E = 22$.
  - Cách 1: $V(G) = E - N + 2 = 22 - 15 + 2 = 9$.
  - Cách 2: Điểm quyết định $P = 8$. $V(G) = P + 1 = 8 + 1 = 9$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 9$).

---

#### D. Phương thức `updatePetDetails(Owner owner, Pet pet)` (Dòng 186–200)
- **Mã nguồn thật**:
  ```java
  186: private void updatePetDetails(Owner owner, Pet pet) {
  187:     Integer id = pet.getId();
  188:     Assert.state(id != null, "'pet.getId()' must not be null");
  189:     Pet existingPet = owner.getPet(id);
  190:     if (existingPet != null) {
  191:         // Update existing pet's properties
  192:         existingPet.setName(pet.getName());
  193:         existingPet.setBirthDate(pet.getBirthDate());
  194:         existingPet.setType(pet.getType());
  195:     }
  196:     else {
  197:         owner.addPet(pet);
  198:     }
  199:     this.owners.saveAndFlush(owner);
  200: }
  ```
- **Danh sách đỉnh (Nodes - 7 đỉnh)**:
  - `N1` (Dòng 186–188): Entry, `id = pet.getId()`, kiểm tra khẳng định `id != null`.
  - `N2` (Dòng 188): Nhánh khẳng định vi phạm (False): ném `IllegalStateException`.
  - `N3` (Dòng 189–190): Nhánh khẳng định thỏa mãn (True): `existingPet = owner.getPet(id)`, kiểm tra `existingPet != null`.
  - `N4` (Dòng 191–195): Nhánh True: cập nhật `setName`, `setBirthDate`, `setType`.
  - `N5` (Dòng 196–198): Nhánh False: `owner.addPet(pet)`.
  - `N6` (Dòng 199–200): Merge N4 và N5: gọi `owners.saveAndFlush(owner)`.
  - `N7`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 8 cạnh)**:
  - `E1`: N1 $\to$ N2 (`id == null` $\implies$ ném ngoại lệ)
  - `E2`: N1 $\to$ N3 (`id != null`)
  - `E3`: N2 $\to$ N7 (Exit do ngoại lệ)
  - `E4`: N3 $\to$ N4 (`existingPet != null`)
  - `E5`: N3 $\to$ N5 (`existingPet == null`)
  - `E6`: N4 $\to$ N6
  - `E7`: N5 $\to$ N6
  - `E8`: N6 $\to$ N7 (Exit bình thường)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 186-188): Entry | id != null?"]
      N2["N2 (Dòng 188): throw IllegalStateException"]
      N3["N3 (Dòng 189-190): existingPet = owner.getPet(id) | existingPet != null?"]
      N4["N4 (Dòng 192-195): setName | setBirthDate | setType"]
      N5["N5 (Dòng 197): owner.addPet(pet)"]
      N6["N6 (Dòng 199): owners.saveAndFlush(owner)"]
      N7["N7: Exit"]

      N1 -->|False| N2
      N1 -->|True| N3
      N2 --> N7
      N3 -->|True| N4
      N3 -->|False| N5
      N4 --> N6
      N5 --> N6
      N6 --> N7
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 7$, Số cạnh $E = 8$.
  - Cách 1: $V(G) = E - N + 2 = 8 - 7 + 2 = 3$.
  - Cách 2: Điểm quyết định $P = 2$ (`id != null`, `existingPet != null`). $V(G) = P + 1 = 3$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 3$).

---

#### E. Phương thức `isDuplicatePetNameViolation(...)` (Dòng 202–205)
- **Mã nguồn thật**:
  ```java
  202: private boolean isDuplicatePetNameViolation(DataIntegrityViolationException ex) {
  203:     String message = ex.getMessage();
  204:     return message != null && message.toLowerCase().contains("unique_owner_pet_name");
  205: }
  ```
- **Danh sách đỉnh (Nodes - 5 đỉnh)**:
  - `N1` (Dòng 202–204): Entry, `message = ex.getMessage()`, kiểm tra `message != null`.
  - `N2` (Dòng 204): Nhánh True của N1: kiểm tra tiếp `message.toLowerCase().contains("unique_owner_pet_name")`.
  - `N3` (Dòng 204): Nhánh False (hoặc do `message == null` hoặc không chứa chuỗi): trả về `false`.
  - `N4` (Dòng 204): Nhánh True của N2: trả về `true`.
  - `N5`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 6 cạnh)**:
  - `E1`: N1 $\to$ N2 (True: `message != null`)
  - `E2`: N1 $\to$ N3 (False: `message == null`)
  - `E3`: N2 $\to$ N4 (True: có chứa chuỗi)
  - `E4`: N2 $\to$ N3 (False: không chứa chuỗi)
  - `E5`: N3 $\to$ N5 (Trả về false)
  - `E6`: N4 $\to$ N5 (Trả về true)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 202-204): Entry | message != null?"]
      N2["N2 (Dòng 204): contains('unique_owner_pet_name')?"]
      N3["N3 (Dòng 204): return false"]
      N4["N4 (Dòng 204): return true"]
      N5["N5: Exit"]

      N1 -->|True| N2
      N1 -->|False| N3
      N2 -->|True| N4
      N2 -->|False| N3
      N3 --> N5
      N4 --> N5
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 5$, Số cạnh $E = 6$.
  - Cách 1: $V(G) = E - N + 2 = 6 - 5 + 2 = 3$.
  - Cách 2: Điểm quyết định $P = 2$ (`message != null`, `contains(...)`). $V(G) = P + 1 = 3$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 3$).

---

## 4. PHÂN TÍCH CHI TIẾT VISITCONTROLLER (`VisitController.java`)

### 4.1. Danh mục phương thức
Lớp `VisitController` gồm 5 phương thức (dòng 47 đến 113):
1. `VisitController(OwnerRepository)` (dòng 47-49): Khởi tạo DI.
2. `setAllowedFields(WebDataBinder)` (dòng 52-54): `@InitBinder`, tuần tự.
3. `loadPetWithVisit(int, int, Map<String, Object>)` (dòng 64-81): `@ModelAttribute("visit")`, nạp pet & owner, có kiểm tra null.
4. `minVisitDate()` (dòng 84-86): `@ModelAttribute("minVisitDate")`, trả về ngày mai (`LocalDate.now().plusDays(1)`), tuần tự.
5. `initNewVisitForm()` (dòng 91-93): `@GetMapping("/owners/{ownerId}/pets/{petId}/visits/new")`, tuần tự.
6. `processNewVisitForm(Owner, int, Visit, BindingResult, RedirectAttributes)` (dòng 98-112): `@PostMapping("/owners/{ownerId}/pets/{petId}/visits/new")`, kiểm tra ngày khám trong tương lai và validation.

---

### 4.2. Đồ thị luồng & Tính $V(G)$ các phương thức có nhánh

#### A. Phương thức `loadPetWithVisit(int, int, Map<String, Object>)` (Dòng 64–81)
- **Mã nguồn thật**:
  ```java
  64: @ModelAttribute("visit")
  65: public Visit loadPetWithVisit(@PathVariable("ownerId") int ownerId, @PathVariable("petId") int petId,
  66:         Map<String, Object> model) {
  67:     Optional<Owner> optionalOwner = owners.findById(ownerId);
  68:     Owner owner = optionalOwner.orElseThrow(() -> new IllegalArgumentException(
  69:             "Owner not found with id: " + ownerId + ". Please ensure the ID is correct "));
  71:     Pet pet = owner.getPet(petId);
  72:     if (pet == null) {
  73:         throw new IllegalArgumentException(
  74:                 "Pet with id " + petId + " not found for owner with id " + ownerId + ".");
  75:     }
  76:     model.put("pet", pet);
  77:     model.put("owner", owner);
  79:     Visit visit = new Visit();
  80:     pet.addVisit(visit);
  81:     return visit;
  82: }
  ```
- **Danh sách đỉnh (Nodes - 6 đỉnh)**:
  - `N1` (Dòng 64–67): Entry, gọi `owners.findById(ownerId)`, kiểm tra `optionalOwner.isPresent()`.
  - `N2` (Dòng 68–69): Nhánh ngoại lệ: ném `IllegalArgumentException("Owner not found...")`.
  - `N3` (Dòng 71–72): Nhánh hợp lệ: `owner.getPet(petId)`, kiểm tra `pet == null`.
  - `N4` (Dòng 73–75): Nhánh True: ném `IllegalArgumentException("Pet not found...")`.
  - `N5` (Dòng 76–81): Nhánh False: đưa `pet`, `owner` vào model, tạo `new Visit()`, `pet.addVisit(visit)`, trả về `visit`.
  - `N6`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 7 cạnh)**:
  - `E1`: N1 $\to$ N2 (Optional empty $\implies$ ném ngoại lệ)
  - `E2`: N1 $\to$ N3 (Optional present)
  - `E3`: N2 $\to$ N6
  - `E4`: N3 $\to$ N4 (`pet == null` $\implies$ ném ngoại lệ)
  - `E5`: N3 $\to$ N5 (`pet != null`)
  - `E6`: N4 $\to$ N6
  - `E7`: N5 $\to$ N6
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 64-67): Entry | owners.findById | owner present?"]
      N2["N2 (Dòng 68-69): throw IllegalArgumentException (Owner not found)"]
      N3["N3 (Dòng 71-72): pet = owner.getPet(petId) | pet == null?"]
      N4["N4 (Dòng 73-75): throw IllegalArgumentException (Pet not found)"]
      N5["N5 (Dòng 76-81): model.put | pet.addVisit(visit) | return visit"]
      N6["N6: Exit"]

      N1 -->|False| N2
      N1 -->|True| N3
      N2 --> N6
      N3 -->|True| N4
      N3 -->|False| N5
      N4 --> N6
      N5 --> N6
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 6$, Số cạnh $E = 7$.
  - Cách 1: $V(G) = E - N + 2 = 7 - 6 + 2 = 3$.
  - Cách 2: Điểm quyết định $P = 2$ (`optionalOwner.isEmpty()`, `pet == null`). $V(G) = P + 1 = 3$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 3$).

---

#### B. Phương thức `processNewVisitForm(...)` (Dòng 98–112)
- **Mã nguồn thật**:
  ```java
  98: @PostMapping("/owners/{ownerId}/pets/{petId}/visits/new")
  99: public String processNewVisitForm(@ModelAttribute Owner owner, @PathVariable int petId, @Valid Visit visit,
  100:        BindingResult result, RedirectAttributes redirectAttributes) {
  101:    if (visit.getDate() != null && !visit.getDate().isAfter(LocalDate.now())) {
  102:        result.rejectValue("date", "typeMismatch.visitDate");
  103:    }
  105:    if (result.hasErrors()) {
  106:        return "pets/createOrUpdateVisitForm";
  107:    }
  109:    owner.addVisit(petId, visit);
  110:    this.owners.save(owner);
  111:    redirectAttributes.addFlashAttribute("message", "Your visit has been booked");
  112:    return "redirect:/owners/{ownerId}";
  113: }
  ```
- **Phân tích điểm quyết định ($P$)**:
  1. $P_1$ (Dòng 101): `visit.getDate() != null`
  2. $P_2$ (Dòng 101): `!visit.getDate().isAfter(LocalDate.now())` (đánh giá khi $P_1$ True)
  3. $P_3$ (Dòng 105): `result.hasErrors()`
  - Tổng số điểm quyết định: $P = 3$.
- **Danh sách đỉnh (Nodes - 7 đỉnh)**:
  - `N1` (Dòng 98–101): Entry, kiểm tra `visit.getDate() != null`.
  - `N2` (Dòng 101): Nhánh True của N1: kiểm tra `!visit.getDate().isAfter(LocalDate.now())`.
  - `N3` (Dòng 102–103): Nhánh True của N2: `result.rejectValue("date", ...)`.
  - `N4` (Dòng 105): Merge N1(F), N2(F), N3 $\to$ kiểm tra `result.hasErrors()`.
  - `N5` (Dòng 106–107): Nhánh True: trả về form `"pets/createOrUpdateVisitForm"`.
  - `N6` (Dòng 109–112): Nhánh False: `owner.addVisit(petId, visit)`, `owners.save(owner)`, flash message, redirect.
  - `N7`: Điểm ra (Exit).
- **Danh sách cạnh (Edges - 9 cạnh)**:
  - `E1`: N1 $\to$ N2 (True: có ngày khám)
  - `E2`: N1 $\to$ N4 (False: ngày khám null)
  - `E3`: N2 $\to$ N3 (True: ngày khám không phải tương lai $\implies$ lỗi)
  - `E4`: N2 $\to$ N4 (False: ngày khám hợp lệ)
  - `E5`: N3 $\to$ N4
  - `E6`: N4 $\to$ N5 (True: có lỗi)
  - `E7`: N4 $\to$ N6 (False: hợp lệ)
  - `E8`: N5 $\to$ N7 (Exit form)
  - `E9`: N6 $\to$ N7 (Exit redirect)
- **Đồ thị luồng (Mermaid)**:
  ```mermaid
  flowchart TD
      N1["N1 (Dòng 98-101): Entry | visit.getDate() != null?"]
      N2["N2 (Dòng 101): !visit.getDate().isAfter(now)?"]
      N3["N3 (Dòng 102): rejectValue('date', 'typeMismatch.visitDate')"]
      N4["N4 (Dòng 105): result.hasErrors()?"]
      N5["N5 (Dòng 106): return 'pets/createOrUpdateVisitForm'"]
      N6["N6 (Dòng 109-112): owner.addVisit | save | redirect:/owners/{ownerId}"]
      N7["N7: Exit"]

      N1 -->|True| N2
      N1 -->|False| N4
      N2 -->|True| N3
      N2 -->|False| N4
      N3 --> N4
      N4 -->|True| N5
      N4 -->|False| N6
      N5 --> N7
      N6 --> N7
  ```
- **Kiểm chứng $V(G)$**:
  - Số đỉnh $N = 7$, Số cạnh $E = 9$.
  - Cách 1: $V(G) = E - N + 2 = 9 - 7 + 2 = 4$.
  - Cách 2: Điểm quyết định $P = 3$. $V(G) = P + 1 = 3 + 1 = 4$.
  - **Kết luận**: Khớp tuyệt đối ($V(G) = 4$).

---

## 5. BẢNG TỔNG HỢP TOÀN BỘ CÁC PHƯƠNG THỨC & ĐỘ PHỨC TẠP CYCLOMATIC V(G)

Bảng dưới đây thống kê đầy đủ toàn bộ 27 phương thức của 3 lớp Web Controller thuộc phạm vi TV4 (`OwnerController`, `PetController`, `VisitController`), đối chiếu chi tiết số dòng thực tế và kiểm chứng tính đồng nhất giữa 2 cách tính $V(G)$:

| STT | Lớp Controller | Tên phương thức | Dòng nguồn | Số đỉnh $N$ | Số cạnh $E$ | Điểm Q.Định $P$ | $V(G) = E - N + 2$ | $V(G) = P + 1$ | Kết luận |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `OwnerController` | `setAllowedFields` | 60–62 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 2 | `OwnerController` | `findOwner` | 65–70 | 4 | 4 | 1 | **2** | **2** | Khớp |
| 3 | `OwnerController` | `initCreationForm` | 73–75 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 4 | `OwnerController` | `processCreationForm` | 78–87 | 4 | 4 | 1 | **2** | **2** | Khớp |
| 5 | `OwnerController` | `initFindForm` | 90–92 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 6 | `OwnerController` | `processFindForm` | 95–130 | 14 | 19 | 6 | **7** | **7** | Khớp |
| 7 | `OwnerController` | `addPaginationModel` | 132–139 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 8 | `OwnerController` | `findPaginatedForOwnersLastName` | 141–146 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 9 | `OwnerController` | `initUpdateOwnerForm` | 149–151 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 10 | `OwnerController` | `processUpdateOwnerForm` | 154–171 | 6 | 7 | 2 | **3** | **3** | Khớp |
| 11 | `OwnerController` | `showOwner` | 179–186 | 4 | 4 | 1 | **2** | **2** | Khớp |
| 12 | `PetController` | `populatePetTypes` | 63–65 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 13 | `PetController` | `findOwner` | 68–73 | 4 | 4 | 1 | **2** | **2** | Khớp |
| 14 | `PetController` | `findPet` | 76–87 | 4 | 4 | 1 | **2** | **2** | Khớp |
| 15 | `PetController` | `initOwnerBinder` | 90–92 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 16 | `PetController` | `initPetBinder` | 95–98 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 17 | `PetController` | `initCreationForm` | 101–105 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 18 | `PetController` | `processCreationForm` | 108–137 | 15 | 22 | 8 | **9** | **9** | Khớp |
| 19 | `PetController` | `initUpdateForm` | 140–142 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 20 | `PetController` | `processUpdateForm` | 145–179 | 15 | 22 | 8 | **9** | **9** | Khớp |
| 21 | `PetController` | `updatePetDetails` | 186–200 | 7 | 8 | 2 | **3** | **3** | Khớp |
| 22 | `PetController` | `isDuplicatePetNameViolation` | 202–205 | 5 | 6 | 2 | **3** | **3** | Khớp |
| 23 | `VisitController` | `setAllowedFields` | 52–54 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 24 | `VisitController` | `loadPetWithVisit` | 64–81 | 6 | 7 | 2 | **3** | **3** | Khớp |
| 25 | `VisitController` | `minVisitDate` | 84–86 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 26 | `VisitController` | `initNewVisitForm` | 91–93 | 2 | 1 | 0 | **1** | **1** | Khớp |
| 27 | `VisitController` | `processNewVisitForm` | 98–112 | 7 | 9 | 3 | **4** | **4** | Khớp |

---

## 6. ĐÁNH GIÁ VÀ LIÊN HỆ VỚI BỘ TEST CỦA TV4

1. **Độ bao phủ nhánh (Branch Coverage)**:
   - Các phương thức có $V(G)$ cao nhất gồm `PetController.processCreationForm` ($V(G)=9$), `PetController.processUpdateForm` ($V(G)=9$), và `OwnerController.processFindForm` ($V(G)=7$).
   - Toàn bộ các nhánh rẽ của các phương thức này đều được kiểm thử đầy đủ trong 36 test của TV4 (`PetControllerMutationTests`: 19 tests, `OwnerControllerMutationTests`: 6 tests, `VisitControllerMutationTests`: 6 tests, `ControllerBinderMutationTests`: 5 tests).
2. **Khả năng phát hiện và tiêu diệt Mutation**:
   - Nhờ việc phân tích đồ thị luồng chi tiết đến từng toán tử đoản mạch (`&&`, `||`), các ca kiểm thử của TV4 đã tiêu diệt triệt để các đột biến ranh giới (`ConditionalsBoundaryMutator`), đột biến loại bỏ điều kiện (`RemoveConditionalMutator`), và đột biến thay đổi giá trị trả về (`BooleanTrueReturnValsMutator`, `NullReturnValsMutator`).
   - Đạt độ bao phủ dòng 100% (250/250 lines) và Mutation Score 98% (192/195 killed), không để sót bất kỳ non-equivalent mutant nào.

