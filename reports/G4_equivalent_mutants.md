# PHẦN G.4: CHỨNG MINH HÌNH THỨC CÁC ĐỘT BIẾN TƯƠNG ĐƯƠNG (EQUIVALENT MUTANTS PROOF)

> **Dự án:** Kiểm thử đột biến (Mutation Testing) bằng PIT trên Spring Boot PetClinic (K03 – R01)  
> **Phạm vi đối tượng:** 03 mutants sống sót cuối cùng trong gói `org.springframework.samples.petclinic.owner.*`  
> **Thành viên phụ trách:** Thành viên 5 (Metrics, RCA & Quality Analyst)  
> **Phiên thực hiện:** SESSION S4 — Chứng minh hình thức bằng Đại số Boolean & Đồ thị luồng điều khiển (CFG)  
> **Mã nguồn đối chiếu:** [`src/main/java`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java), [`reports/data/final_mutations.xml`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/final_mutations.xml), script kiểm chứng [`scripts/verify_equivalence.py`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/verify_equivalence.py).

---

## 1. TỔNG QUAN VÀ BỐI CẢNH 03 SURVIVING MUTANTS

Sau khi hoàn thành vòng lặp kiểm thử đột biến (Kill-loop) với 13 file kiểm thử và 130 unit tests, kết quả phân tích PIT tại báo cáo cuối cùng ([`reports/data/final_mutations.xml`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/data/final_mutations.xml)) ghi nhận:
- **Tổng số mutants sinh ra:** 195 mutants.
- **Số mutants bị tiêu diệt (Killed):** 192 mutants (**98.46%**).
- **Số mutants sống sót (Survived):** Đúng **03 mutants** (chiếm 1.54%).
- **Độ bao phủ dòng (Line Coverage):** 250/250 lines (**100.00%**).
- **Mutations with no coverage:** 0 (100% mutants đều có test case chạm tới).

Chi tiết trích xuất nguyên văn từ tệp `final_mutations.xml` cho 3 mutants còn lại:

| STT | Lớp đối tượng | Phương thức | Dòng | Toán tử PIT (Mutator) | Index (Bytecode) | Mô tả của PIT | Trạng thái |
|:---:|:---|:---|:---:|:---|:---:|:---|:---:|
| **M1** | `Owner` | `addPet` | 108 | `RemoveConditionalMutator_EQUAL_IF` | 39 | `removed conditional - replaced equality check with true` | SURVIVED |
| **M2** | `Owner` | `addPet` | 108 | `RemoveConditionalMutator_EQUAL_IF` | 42 | `removed conditional - replaced equality check with true` | SURVIVED |
| **M3** | `OwnerController` | `processUpdateOwnerForm` | 167 | `VoidMethodCallMutator` | 50 | `removed call to org/springframework/samples/petclinic/owner/Owner::setId` | SURVIVED |

Theo lý thuyết kiểm thử đột biến (J. Offutt & R. Untch), một **Đột biến tương đương (Equivalent Mutant)** là một mutant có cú pháp khác với chương trình gốc nhưng có ngữ nghĩa và hành vi hoàn toàn đồng nhất trên **mọi đầu vào khả thi thuộc miền xác định** ($M(P, x) = P(x), \forall x \in D$). Không có bất kỳ ca kiểm thử nào (kể cả kiểm thử vét cạn) có thể làm đứt gãy luồng thực thi để tiêu diệt một Equivalent Mutant.

Dưới đây là chứng minh toán học và luồng điều khiển chứng minh tính tương đương tuyệt đối của cả 3 mutants trên.

---

## 2. TRÍCH DẪN NGUYÊN VĂN MÃ NGUỒN THỰC TẾ

### 2.1. Lớp cơ sở `BaseEntity.java` (dòng 37–49)
File: [`src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java#L37-L49)
```java
37: 	private Integer id;
38: 
39: 	public Integer getId() {
40: 		return id;
41: 	}
42: 
43: 	public void setId(Integer id) {
44: 		this.id = id;
45: 	}
46: 
47: 	public boolean isNew() {
48: 		return this.id == null;
49: 	}
```

> **Định lý 1 (Bản chất của thực thể mới):** Với mọi thực thể `e` kế thừa từ `BaseEntity`, phương thức `e.isNew()` trả về `true` khi và chỉ khi thuộc tính `e.getId() == null`.  
> Ngược lại, `!e.isNew() ⟺ e.getId() != null`.

---

### 2.2. Lớp `Owner.java` (dòng 100–113)
File: [`src/main/java/org/springframework/samples/petclinic/owner/Owner.java`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/Owner.java#L100-L113)
```java
100: 	public void addPet(Pet pet) {
101: 		if (pet == null) {
102: 			return;
103: 		}
104: 		if (getPets().contains(pet)) {
105: 			return;
106: 		}
107: 		for (Pet existingPet : getPets()) {
108: 			if (!existingPet.isNew() && !pet.isNew() && Objects.equals(existingPet.getId(), pet.getId())) {
109: 				return;
110: 			}
111: 		}
112: 		getPets().add(pet);
113: 	}
```

---

### 2.3. Lớp `OwnerController.java` (dòng 153–171)
File: [`src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L153-L171)
```java
153: 	@PostMapping("/owners/{ownerId}/edit")
154: 	public String processUpdateOwnerForm(@Valid Owner owner, BindingResult result, @PathVariable("ownerId") int ownerId,
155: 			RedirectAttributes redirectAttributes) {
156: 		if (result.hasErrors()) {
157: 			redirectAttributes.addFlashAttribute("error", "There was an error in updating the owner.");
158: 			return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
159: 		}
160: 
161: 		if (!Objects.equals(owner.getId(), ownerId)) {
162: 			result.rejectValue("id", "mismatch", "The owner ID in the form does not match the URL.");
163: 			redirectAttributes.addFlashAttribute("error", "Owner ID mismatch. Please try again.");
164: 			return "redirect:/owners/{ownerId}/edit";
165: 		}
166: 
167: 		owner.setId(ownerId);
168: 		this.owners.save(owner);
169: 		redirectAttributes.addFlashAttribute("message", "Owner Values Updated");
170: 		return "redirect:/owners/{ownerId}";
171: 	}
```

---

## 3. CHỨNG MINH ĐẠI SỐ BOOLEAN CHO MUTANT M1 & M2 (`Owner.java:108`)

### 3.1. Ký hiệu hóa mệnh đề Boolean
Xét một bước lặp `for` tại dòng 107–111 của phương thức `Owner.addPet`:
- Đặt $x = \text{existingPet.getId()} \in \mathbb{Z} \cup \{\text{null}\}$.
- Đặt $y = \text{pet.getId()} \in \mathbb{Z} \cup \{\text{null}\}$.

Định nghĩa các biến mệnh đề:
- $a = \text{existingPet.isNew()}$. Theo Định lý 1: $a \iff (x == \text{null})$.  
  Do đó $\neg a = !\text{existingPet.isNew()} \iff (x \neq \text{null})$.
- $b = \text{pet.isNew()}$. Theo Định lý 1: $b \iff (y == \text{null})$.  
  Do đó $\neg b = !\text{pet.isNew()} \iff (y \neq \text{null})$.
- $e = \text{Objects.equals}(x, y)$.  
  Theo đặc tả Java SE (`java.util.Objects.equals(Object a, Object b)`):
  $$e = \text{true} \iff (x == y) \lor (x \neq \text{null} \land x.\text{equals}(y))$$

### 3.2. Biểu thức điều kiện gốc và các biểu thức đột biến
- **Hàm gốc (Original):**
  $$C_{\text{orig}} = \neg a \land \neg b \land e$$
- **Mutant M1 (PIT Index 39):**
  Toán tử `RemoveConditionalMutator_EQUAL_IF` loại bỏ nhánh rẽ kiểm tra `!existingPet.isNew()`, thay thế điều kiện này bằng `true`:
  $$C_{\text{M1}} = \text{true} \land \neg b \land e = \neg b \land e$$
- **Mutant M2 (PIT Index 42):**
  Toán tử `RemoveConditionalMutator_EQUAL_IF` loại bỏ nhánh rẽ kiểm tra `!pet.isNew()`, thay thế điều kiện này bằng `true`:
  $$C_{\text{M2}} = \neg a \land \text{true} \land e = \neg a \land e$$

---

### 3.3. Ràng buộc quan hệ miền (Domain Constraints)
Hãy phân tích mối liên hệ logic phụ thuộc giữa $e$ và các mệnh đề $a, b$:
1. Nếu $x == \text{null}$ và $y == \text{null}$:
   Khi đó $a = \text{true}$ ($\neg a = \text{false}$) và $b = \text{true}$ ($\neg b = \text{false}$).  
   Hàm `Objects.equals(null, null)` trả về `true` $\implies e = \text{true}$.  
   - $C_{\text{orig}} = \text{false} \land \text{false} \land \text{true} = \mathbf{false}$.
   - $C_{\text{M1}} = \neg b \land e = \text{false} \land \text{true} = \mathbf{false}$.
   - $C_{\text{M2}} = \neg a \land e = \text{false} \land \text{true} = \mathbf{false}$.  
   *(Cả 3 hàm đều trả về `false`).*

2. Nếu $x == \text{null}$ và $y \neq \text{null}$ (hoặc ngược lại $x \neq \text{null}$ và $y == \text{null}$):
   Khi đó một bên có giá trị, một bên `null`.  
   Hàm `Objects.equals(null, y)` hoặc `Objects.equals(x, null)` luôn trả về `false` $\implies e = \mathbf{false}$.  
   Vì $e = \text{false}$, phép hội $\land$ với $e$ luôn cho kết quả `false`:
   - $C_{\text{orig}} = \dots \land \text{false} = \mathbf{false}$.
   - $C_{\text{M1}} = \dots \land \text{false} = \mathbf{false}$.
   - $C_{\text{M2}} = \dots \land \text{false} = \mathbf{false}$.  
   *(Cả 3 hàm đều trả về `false`).*

3. Nếu $x \neq \text{null}$ và $y \neq \text{null}$:
   Khi đó $\neg a = \text{true}$ và $\neg b = \text{true}$.
   - $C_{\text{orig}} = \text{true} \land \text{true} \land e = e$.
   - $C_{\text{M1}} = \text{true} \land e = e$.
   - $C_{\text{M2}} = \text{true} \land e = e$.  
   *(Cả 3 hàm đều bằng chính giá trị của $e$: nếu cùng ID thì `true`, nếu khác ID thì `false`).*

---

### 3.4. Bảng chân trị toàn diện có ràng buộc miền (Truth Table)

Không gian giá trị của cặp $(x, y)$ phân hoạch thành 5 lớp tương đương bao quát 100% các khả năng:
- **Lớp 1:** Cả hai cùng là thực thể mới (`id == null`, `id == null`).
- **Lớp 2:** Thực thể cũ mới (`null`), thực thể mới đã có ID (`id = 1`).
- **Lớp 3:** Thực thể cũ đã có ID (`id = 1`), thực thể mới chưa có ID (`null`).
- **Lớp 4:** Cả hai đều có ID nhưng khác nhau (`id = 1`, `id = 2`).
- **Lớp 5:** Cả hai đều có ID và trùng nhau (`id = 1`, `id = 1`).

| Lớp đầu vào $(x, y)$ | $a$ ($x=\text{null}$) | $b$ ($y=\text{null}$) | $\neg a$ | $\neg b$ | $e$ ($x=y$) | $C_{\text{orig}}$ ($\neg a \land \neg b \land e$) | $C_{\text{M1}}$ ($\neg b \land e$) | $C_{\text{M2}}$ ($\neg a \land e$) | So sánh tương đương |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. (null, null)** | 1 | 1 | 0 | 0 | 1 | **0** | **0** | **0** | **ĐỒNG NHẤT** |
| **2. (null, 1)** | 1 | 0 | 0 | 1 | 0 | **0** | **0** | **0** | **ĐỒNG NHẤT** |
| **3. (1, null)** | 0 | 1 | 1 | 0 | 0 | **0** | **0** | **0** | **ĐỒNG NHẤT** |
| **4. (1, 2)** | 0 | 0 | 1 | 1 | 0 | **0** | **0** | **0** | **ĐỒNG NHẤT** |
| **5. (1, 1)** | 0 | 0 | 1 | 1 | 1 | **1** | **1** | **1** | **ĐỒNG NHẤT** |

### 3.5. Kết luận hình thức cho M1 và M2
Từ bảng chân trị:
$$\forall (x, y) \in (\mathbb{Z} \cup \{\text{null}\})^2: \quad C_{\text{orig}}(x, y) \equiv C_{\text{M1}}(x, y) \equiv C_{\text{M2}}(x, y)$$

Hai mệnh đề $\neg a$ (`!existingPet.isNew()`) và $\neg b$ (`!pet.isNew()`) về mặt toán học là **tập con phụ thuộc (subsumed)** của quan hệ đẳng thức $e$. Khi $e = \text{true}$ thì hoặc cả hai cùng null, hoặc cả hai cùng khác null. Trong trường hợp cả hai cùng null, cả $\neg a$ và $\neg b$ đều là `false`, do đó chỉ cần giữ lại một vế hoặc bỏ bớt một vế thì kết quả phép hội vẫn bị triệt tiêu về `false`.

Do đó, **Mutant M1 (Index 39)** và **Mutant M2 (Index 42)** không bao giờ có thể làm thay đổi bất kỳ kết quả rẽ nhánh nào của phương thức `addPet`. **Cả hai 100% là Equivalent Mutants.**

---

## 4. CHỨNG MINH ĐỒ THỊ LUỒNG ĐIỀU KHIỂN CHO MUTANT M3 (`OwnerController.java:167`)

### 4.1. Đồ thị luồng điều khiển (Control Flow Graph - CFG)
Xét phương thức `processUpdateOwnerForm`:

```
               [Entry: Nhận request POST /owners/{ownerId}/edit]
                                      │
                                      ▼
                        [Node 1: result.hasErrors()?]
                                ├── True ──► [Trả về form lỗi]
                                │
                              False
                                │
                                ▼
               [Node 2: !Objects.equals(owner.getId(), ownerId)?] (Dòng 161)
                                ├── True ──► [rejectValue("id", "mismatch")]
                                │            [Redirect /owners/{ownerId}/edit]
                              False
                                │
                                ▼  <─── [ĐIỂM GIAO THOA P1: Tiền điều kiện đảm bảo]
                 [Node 3: owner.setId(ownerId)] (Dòng 167 - LỆNH ĐỘT BIẾN)
                                │
                                ▼
                 [Node 4: this.owners.save(owner)] (Dòng 168)
                                │
                                ▼
                 [Node 5: Redirect /owners/{ownerId}] (Dòng 170)
```

---

### 4.2. Chứng minh bất biến trạng thái (State Invariance Proof)

1. **Phân tích tiền điều kiện tại Node 3 (Dòng 167):**
   Để luồng điều khiển đi từ `Node 2` tới `Node 3`, điều kiện rẽ nhánh tại dòng 161 bắt buộc phải nhận giá trị `false`:
   $$\text{Condition}_{\text{Node 2}} = !\text{Objects.equals}(owner.\text{getId}(), ownerId) == \text{false}$$
   Tương đương với:
   $$\text{Objects.equals}(owner.\text{getId}(), ownerId) == \text{true}$$
   
   Vì tham số đường dẫn `ownerId` có kiểu nguyên thủy `int` (trong phương thức Java: `@PathVariable("ownerId") int ownerId`), giá trị của `ownerId` luôn là một số nguyên xác định ($ownerId \in \mathbb{Z}$), không bao giờ là `null`.
   
   Theo định nghĩa của `Objects.equals(Object a, Object b)`:
   $$\text{Objects.equals}(owner.\text{getId}(), ownerId) == \text{true} \iff owner.\text{getId}() \neq \text{null} \land owner.\text{getId}().\text{intValue}() == ownerId$$
   
   Do đó, tại điểm vào ngay trước dòng 167 (ký hiệu là trạng thái $S_{\text{pre}}$):
   $$owner.\text{getId}() \equiv ownerId$$

2. **So sánh trạng thái sau dòng 167:**
   - **Chương trình gốc:**
     Thực thi lệnh: `owner.setId(ownerId);`.
     Trạng thái sau lệnh gán:
     $$owner.\text{getId()}_{\text{post_orig}} = ownerId$$
   - **Chương trình đột biến (Mutant M3 - Index 50):**
     PIT loại bỏ lệnh `owner.setId(ownerId);`.
     Vì không có lệnh gán, thuộc tính `id` giữ nguyên giá trị vốn có từ trạng thái $S_{\text{pre}}$:
     $$owner.\text{getId()}_{\text{post_mutant}} = owner.\text{getId()}_{\text{pre}} = ownerId$$

3. **Tính đồng nhất của các tác dụng phụ tiếp theo:**
   - Cả hai chương trình cùng thực thi: `this.owners.save(owner);`.
     Do đối tượng `owner` có toàn bộ các trường (bao gồm cả `id`) hoàn toàn đồng nhất, câu lệnh SQL phát sinh (`UPDATE owners SET ... WHERE id = ?`) nhận các tham số giống hệt nhau.
   - Cả hai chương trình cùng thêm Flash attribute `"Owner Values Updated"`.
   - Cả hai chương trình cùng trả về chuỗi điều hướng: `"redirect:/owners/" + ownerId`.

4. **Yếu tố bảo mật bổ trợ ngăn chặn giả mạo (Tampering Prevention):**
   Tại dòng 61 của [`OwnerController.java`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java#L61):
   ```java
   @InitBinder
   public void setAllowedFields(WebDataBinder dataBinder) {
       dataBinder.setDisallowedFields("id", "*.id");
   }
   ```
   Lệnh này cấm tuyệt đối Spring DataBinder can thiệp sửa đổi trường `id` từ các tham số HTTP POST form. Đối tượng `owner` chỉ có thể nhận `id` khi được nạp từ cơ sở dữ liệu qua `@ModelAttribute("owner") findOwner(ownerId)`.

### 4.3. Kết luận hình thức cho M3
Lệnh `owner.setId(ownerId);` tại dòng 167 là một thao tác **gán lại giá trị mà biến đã sẵn có (Dead Store / Redundant Assignment)**. Loại bỏ câu lệnh này không tạo ra bất kỳ sự phân kỳ nào (no divergence) về bộ nhớ, trạng thái cơ sở dữ liệu, hay phản hồi HTTP trên bất kỳ luồng thực thi nào.
=> **Mutant M3 (Index 50) 100% là Equivalent Mutant.**

---

## 5. THỰC NGHIỆM KIỂM CHỨNG TỰ ĐỘNG BẰNG SCRIPT PYTHON

Để củng cố bằng chứng thực nghiệm, nhóm đã phát triển script kiểm chứng tự động [`scripts/verify_equivalence.py`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/scripts/verify_equivalence.py) duyệt vét cạn toàn bộ không gian trạng thái của các trường ID và mô phỏng luồng rẽ nhánh của Controller.

### 5.1. Lệnh thực thi
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/verify_equivalence.py
```

### 5.2. Kết quả đầu ra (Console Output)
```text
=== KIỂM CHỨNG VÉT CẠN OWNER.JAVA:108 ===
existing_id  | pet_id     | Original   | Mutant1    | Mutant2    | Match?
-----------------------------------------------------------------
None         | None       | False      | False      | False      | EQUIVALENT
None         | 1          | False      | False      | False      | EQUIVALENT
None         | 2          | False      | False      | False      | EQUIVALENT
1            | None       | False      | False      | False      | EQUIVALENT
1            | 1          | True       | True       | True       | EQUIVALENT
1            | 2          | False      | False      | False      | EQUIVALENT
2            | None       | False      | False      | False      | EQUIVALENT
2            | 1          | False      | False      | False      | EQUIVALENT
2            | 2          | True       | True       | True       | EQUIVALENT
-----------------------------------------------------------------
Tổng số tổ hợp kiểm thử: 9
Số tổ hợp Mutant 1 khớp Original: 9/9 (100.0%)
Số tổ hợp Mutant 2 khớp Original: 9/9 (100.0%)
=> KẾT LUẬN: Đột biến index 39 và 42 tại Owner.java:108 là EQUIVALENT 100% trên toàn bộ không gian trạng thái.

=== KIỂM CHỨNG LUỒNG ĐIỀU KHIỂN OWNERCONTROLLER.JAVA:167 ===
Case owner.id=1, url_id=1 -> Vượt qua guard, chạm dòng 167:
   Original ID sau dòng 167: 1
   Mutant ID sau dòng 167:   1
   => Trạng thái HOÀN TOÀN ĐỒNG NHẤT (1 == 1).
Case owner.id=1, url_id=2 -> Bị guard chặn (redirect edit), KHÔNG BAO GIỜ chạm dòng 167.
Case owner.id=2, url_id=1 -> Bị guard chặn (redirect edit), KHÔNG BAO GIỜ chạm dòng 167.
Case owner.id=None, url_id=1 -> Bị guard chặn (redirect edit), KHÔNG BAO GIỜ chạm dòng 167.
=> KẾT LUẬN: Đột biến xóa setId tại OwnerController.java:167 là EQUIVALENT 100% do guard bất biến.
```

---

## 6. CÁC GIẢ ĐỊNH VÀ HẠN CHẾ TRUNG THỰC (TECHNICAL ASSUMPTIONS & LIMITATIONS)

Nhằm đảm bảo tính trung thực và chuẩn mực khoa học, báo cáo nêu rõ các biên giả định kỹ thuật của chứng minh:

1. **Giả định tính bất biến của lớp dẫn xuất (No Subclass Polymorphic Override):**  
   Chứng minh giả định rằng lớp `Pet` kế thừa trực tiếp triển khai của `BaseEntity.java` mà không ghi đè (override) phương thức `isNew()` hoặc `getId()` bằng logic đặc thù khác (ví dụ: gán ID ảo trước khi persist). Thực tế kiểm tra mã nguồn cho thấy `Pet.java` kế thừa `NamedEntity`, và `NamedEntity` kế thừa `BaseEntity` hoàn toàn không ghi đè `isNew()`.
2. **Không xét thao tác can thiệp động (No Reflection / Bytecode Manipulation):**  
   Chứng minh không tính đến trường hợp có mã độc hoặc framework can thiệp runtime bằng Java Reflection để ép đổi trường `private Integer id` của `Owner` ngay giữa dòng 166 và 167.
3. **Môi trường luồng thực thi chuẩn (Deterministic Single-Threaded Execution):**  
   Chứng minh áp dụng trên luồng thực thi HTTP request chuẩn của Spring MVC, không xét trường hợp có luồng nền không đồng bộ (asynchronous thread) chia sẻ và biến đổi thuộc tính đối tượng `owner` mà không có cơ chế lock.

---

## 7. ĐIỂM SỐ ĐỘT BIẾN HIỆU CHỈNH (ADJUSTED MUTATION SCORE)

Trong lý thuyết kiểm thử phần mềm, công thức tính Mutation Score thô của PIT (Raw Mutation Score) chưa loại trừ đột biến tương đương:
$$\text{MS}_{\text{raw}} = \frac{\text{Killed Mutants}}{\text{Total Mutants}} = \frac{192}{195} \approx \mathbf{98.46\%}$$

Khi áp dụng công thức chuẩn hóa theo tiêu chuẩn nghiên cứu (Adjusted Mutation Score), loại bỏ các đột biến tương đương đã được chứng minh hình thức khỏi mẫu số:
$$\text{MS}_{\text{adjusted}} = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} = \frac{192}{195 - 3} = \frac{192}{192} = \mathbf{100.00\%}$$

### Bảng đối chiếu số liệu chất lượng:
| Chỉ số kiểm thử | Giá trị đo lường | Đánh giá chất lượng |
|:---|:---:|:---|
| **Line Coverage** | 250 / 250 dòng (**100.00%**) | Độ bao phủ thực thi tuyệt đối |
| **PIT Raw Mutation Score** | 192 / 195 mutants (**98.46%**) | Vượt xa ngưỡng yêu cầu của đề tài (≥ 88%) |
| **Equivalent Mutants đã chứng minh** | **03 mutants** (100% survivors) | Đã chứng minh hình thức bằng Đại số Boolean & CFG |
| **Adjusted Mutation Score** | **192 / 192 mutants (100.00%)** | **Tiệm cận sự hoàn hảo tuyệt đối của bộ kiểm thử** |

---

## 8. KỊCH BẢN PHẢN XẠ NHANH CHO PHIÊN HỎI ĐÁP (Q&A 30 GIÂY) VỚI HỘI ĐỒNG

> **Câu hỏi giả định của Giảng viên/Hội đồng:**  
> *"Tại sao nhóm đã đạt 100% Line Coverage (250/250 lines) nhưng Mutation Score chính thức của PIT chỉ dừng lại ở 98.46% (192/195) mà không thể đạt 100%? Có phải do bộ test của nhóm vẫn còn thiếu sót?"*

> **Đoạn trả lời chuẩn học thuật (30 giây):**  
> *"Dạ thưa Thầy/Cô và Hội đồng, 3 mutant sống sót không phải do thiếu sót của bộ kiểm thử, mà đây là **03 Đột biến tương đương (Equivalent Mutants)** do đặc thù mã nguồn của dự án Spring PetClinic:*  
> *1. Tại `Owner.java:108`, hai mutant ép điều kiện `!existingPet.isNew()` và `!pet.isNew()` thành `true`. Nhưng về mặt đại số Boolean, điều kiện này là **tập con phụ thuộc** của `Objects.equals(...)` khi hai ID khác null. Khi kiểm tra vét cạn 9 tổ hợp ID, cả 2 mutant đều cho chân trị đồng nhất 100% với code gốc.*  
> *2. Tại `OwnerController.java:167`, mutant xóa lệnh `owner.setId(ownerId)`. Tuy nhiên, khối guard dòng 161 phía trước đã chặn mọi trường hợp lệch ID. Tại dòng 167, `owner.getId()` chắc chắn đã bằng `ownerId`, nên việc xóa lệnh gán này là xóa một dead-store không gây tác dụng phụ.*  
> *Khi loại bỏ 3 mutant tương đương này, **Adjusted Mutation Score thực tế của nhóm đạt tuyệt đối 100% (192/192)**."*
