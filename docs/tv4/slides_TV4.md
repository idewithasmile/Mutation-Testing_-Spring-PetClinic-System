# TÀI LIỆU SLIDE BÁO CÁO KỸ THUẬT — THÀNH VIÊN 4 (TV4)
**Vị trí:** White-Box & Web Controller Test Engineer  
**Chuyên đề:** Phân tích Đồ thị luồng (Control Flow Graph), McCabe $V(G)$, Kỹ thuật Detached Entity và Mockito ArgumentCaptor  
**Tích hợp:** TV5 sẽ tích hợp nội dung này vào bộ slide tổng của nhóm.

---

## SLIDE 1: NGHỊCH LÝ ĐỘ PHỦ — VÌ SAO 97% LINE COVERAGE NHƯNG CHỈ ĐẠT 67% MUTATION SCORE?

### 1. Nội dung hiển thị trên Slide

#### Tiêu đề chính
> **Nghịch lý độ phủ: 97% Line Coverage vs. 67% Mutation Score tại tầng Controller**

#### Các điểm chính (Bullet Points)
- **"Ảo tưởng an toàn" từ độ phủ dòng (Line Coverage):**
  - Baseline ban đầu của dự án đạt **97% Line Coverage** nhưng Mutation Score chỉ đạt **67%**.
  - Bài test truyền thống chỉ kiểm tra việc *dòng lệnh có được thực thi qua hay không*, hoàn toàn bỏ qua việc *trạng thái dữ liệu có bị biến đổi sai lệch hay không*.
- **Điểm mù của Spring MockMvc (MockMvc Blinding):**
  - Cơ chế `WebDataBinder` tự động gán tham số từ HTTP Request vào entity trong Model trước khi Controller chạy.
  - Dẫn đến hiện tượng **Redundant Assignment (Gán dư thừa)**: Các lệnh gán thuộc tính thủ công trong Controller trở nên "vô hình" trên pipeline HTTP.
- **Hậu quả trên Mutation Testing:**
  - PIT xóa bỏ các lệnh gán cốt lõi (`setName`, `setBirthDate`, `setType`), bài test MockMvc vẫn **GREEN** $\longrightarrow$ **Mutant sống sót nguy hiểm (SURVIVED)**.
- **Sứ mệnh của TV4:** Xây dựng **36 test methods** bổ sung, nâng Mutation Score từ **67% lên 98%** (diệt 192/195 mutants, 3 mutant còn lại là equivalent).

---

### 2. Ghi chú thuyết trình (Speaker Notes — Slide 1)
> *"Kính thưa Thầy và các bạn, khi bắt đầu dự án với mã nguồn Spring PetClinic gốc, một con số rất ấn tượng xuất hiện: Line Coverage của gói owner đạt tới 97%. Tuy nhiên, khi nhóm chạy công cụ PIT Mutation Testing với bộ mutator STRONGER, điểm đột biến thực tế chỉ đạt khiêm tốn ở mức 67%!*  
> *Tại sao lại có độ vênh lên tới 30% như vậy? Đó chính là hiện tượng 'Ảo tưởng an toàn' (False Sense of Security) của kiểm thử hộp đen. Điển hình tại các Controller, Spring Framework cung cấp cơ chế DataBinder tự động ghi dữ liệu vào Model Entity. Khi viết test bằng MockMvc thông thường, các lập trình viên chỉ kiểm tra HTTP Status 200 hay View Name, khiến các lệnh gán dữ liệu nghiệp vụ bên trong Controller trở thành 'gán dư thừa'. Khi PIT xóa sạch các lệnh gán này, test vẫn Pass và mutant ngang nhiên sống sót. Để giải quyết triệt để vấn đề này, em đã áp dụng phương pháp kiểm thử hộp trắng chặt chẽ, bắt đầu từ việc giải phẫu cấu trúc đồ thị luồng điều khiển."*

---

## SLIDE 2: PHÂN TÍCH HỘP TRẮNG — FLOW GRAPH, MCCABE V(G) VÀ BASIS PATHS CỦA `updatePetDetails`

### 1. Nội dung hiển thị trên Slide

#### Tiêu đề chính
> **Mô hình hóa Đồ thị luồng (Flow Graph) và Xác định Độ phức tạp $V(G)$**

#### Trực quan hóa Đồ thị luồng (Sơ đồ thu nhỏ trên slide)
*(Nhúng trực tiếp vector file [`docs/tv4/img/flowgraph_updatePetDetails.svg`](file:///d:/kiemthu/Mutation-Testing_-Spring-PetClinic-System/docs/tv4/img/flowgraph_updatePetDetails.svg))*

```
       [N1: Entry | Assert id != null?]
          │                      │
     (False)                  (True)
          ▼                      ▼
  [N2: Throw IllegalState]   [N3: existingPet != null?]
          │                      │             │
          │                   (True)        (False)
          │                      ▼             ▼
          │              [N4: Update fields] [N5: owner.addPet]
          │                      │             │
          │                      └──────┬──────┘
          │                             ▼
          │                   [N6: saveAndFlush]
          │                             │
          └─────────────────────────────┴──────────> [N7: Exit]
```

#### Phân tích số liệu cấu trúc (Metrics)
- **Cấu trúc đồ thị:** $N = 7$ đỉnh (Nodes), $E = 8$ cạnh (Edges), $P = 2$ điểm quyết định nhị phân ($N_1, N_3$).
- **Độ phức tạp Cyclomatic $V(G)$ theo 2 phương pháp độc lập:**
  - **Cách 1 (Euler):** $V(G) = E - N + 2 = 8 - 7 + 2 = \mathbf{3}$
  - **Cách 2 (McCabe Predicate):** $V(G) = P + 1 = 2 + 1 = \mathbf{3}$
- **Tập 3 đường cơ sở độc lập tuyến tính (Basis Paths):**
  - **BP-PC-23:** $N_1 \to N_2 \to N_7$ *(Fail-fast khi `pet.getId() == null`)*
  - **BP-PC-24:** $N_1 \to N_3 \to N_4 \to N_6 \to N_7$ *(Cập nhật thú cưng đã tồn tại — Nhánh trọng tâm)*
  - **BP-PC-25:** $N_1 \to N_3 \to N_5 \to N_6 \to N_7$ *(Thêm mới khi thú cưng chưa có trong chủ nuôi)*

---

### 2. Ghi chú thuyết trình (Speaker Notes — Slide 2)
> *"Trên màn hình là Đồ thị luồng điều khiển (Control Flow Graph) của phương thức then chốt `updatePetDetails` trong PetController. Phương thức này chịu trách nhiệm đồng bộ thông tin thú cưng vào cơ sở dữ liệu.*  
> *Áp dụng lý thuyết kiểm thử hộp trắng của Thomas McCabe, đồ thị có 7 đỉnh và 8 cạnh với 2 điểm quyết định rẽ nhánh nhị phân tại N1 và N3. Tính toán bằng cả hai công thức độc lập: E trừ N cộng 2, và P cộng 1, ta đều thu được kết quả đồng nhất: Độ phức tạp Cyclomatic V(G) đúng bằng 3.*  
> *Con số 3 này mang ý nghĩa toán học sống còn: nó bảo đảm rằng tồn tại đúng 3 đường cơ sở độc lập tuyến tính để bao phủ toàn bộ không gian thực thi của phương thức. Trong đó, đường cơ sở số 2 — đi qua đỉnh N4 — chính là nơi diễn ra 3 thao tác gán: setName, setBirthDate và setType. Đây chính là 'tử huyệt' sinh ra 3 mutant sống sót mà bộ test MockMvc cũ hoàn toàn bất lực."*

---

## SLIDE 3: GIẢI PHÁP ĐỘT PHÁ — DETACHED ENTITY & ARGUMENTCAPTOR DIỆT MUTANT

### 1. Nội dung hiển thị trên Slide

#### Tiêu đề chính
> **Kỹ thuật Detached Entity kết hợp Mockito ArgumentCaptor**

#### So sánh Trước vs. Sau cải tiến

| Tiêu chuẩn | Trước cải tiến (Black-Box / MockMvc) | Sau cải tiến (White-Box / TV4 Detached Entity) |
|:---|:---|:---|
| **Mô hình đối tượng** | Cùng 1 tham chiếu: `existingPet == pet` (Binder ghi đè sẵn) | Hai cá thể tách rời: `managed` (cũ) vs. `detached` (mới) |
| **Bản chất lệnh gán** | Dư thừa trên HTTP pipeline (`x = x`) | Bắt buộc phải thực thi để sao chép trường dữ liệu |
| **Cơ chế xác minh** | Chỉ kiểm tra HTTP 302 Redirect URL | `ArgumentCaptor<Owner>` bắt thực thể tại `saveAndFlush` |
| **Kết quả diệt mutant** | **SURVIVED (3 mutants sống sót tại dòng 192, 193, 194)** | **KILLED 100% (Tiêu diệt toàn bộ 3 mutants)** |

#### Trích đoạn mã nguồn diệt mutant ($\le 12$ dòng từ file thật)
```java
// Trích: PetControllerMutationTests.java (Dòng 280-305)
Owner owner = new Owner();
Pet managed = new Pet(); managed.setId(1); managed.setName("petty");
owner.addPet(managed); // Thực thể cũ đang quản lý
Pet detached = new Pet(); detached.setId(1); detached.setName("Betty");
detached.setType(this.hamster); detached.setBirthDate(LocalDate.of(2015, 2, 12));

controller.processUpdateForm(owner, detached, result, redirectAttributes);

ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
verify(repository).saveAndFlush(captor.capture());
assertThat(captor.getValue().getPet(1).getName()).isEqualTo("Betty");
assertThat(captor.getValue().getPet(1).getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12));
```

---

### 2. Ghi chú thuyết trình (Speaker Notes — Slide 3)
> *"Để phá vỡ điểm mù của MockMvc, giải pháp đột phá mà em thiết kế là đưa kiểm thử về tầng Unit thuần với kỹ thuật 'Detached Entity' kết hợp Mockito 'ArgumentCaptor'.*  
> *Như quý Thầy cô thấy trong đoạn code 10 dòng trích từ file kiểm thử thật: Em chủ động tạo ra hai đối tượng Pet hoàn toàn tách biệt trên bộ nhớ Heap. Đối tượng 'managed' nằm trong Owner mang tên cũ là 'petty'. Trong khi đối tượng 'detached' mô phỏng Form DTO mang tên mới là 'Betty'.*  
> *Khi gọi trực tiếp controller.processUpdateForm, Controller bắt buộc phải chạy qua nhánh N4 để sao chép từng trường từ detached sang managed. Ngay tại thời điểm lưu xuống database, em dùng ArgumentCaptor chặn bắt đối tượng Owner và assert trực tiếp: Tên thú cưng lưu vào kho dữ liệu bắt buộc phải đổi thành 'Betty'.*  
> *Nếu bất kỳ mutant nào xóa bỏ dòng lệnh setName, setBirthDate hay setType, giá trị trong captor sẽ giữ nguyên dữ liệu cũ, phép so sánh thất bại và mutant bị tiêu diệt ngay lập tức! Kỹ thuật này đã diệt gọn toàn bộ 3 mutant cứng đầu nhất của PetController."*


---

## KỊCH BẢN THUYẾT TRÌNH CHI TIẾT (3,5 PHÚT: 05:00 – 08:30)

**Người trình bày:** Thành viên 4 (TV4) — White-Box & Web Controller Test Engineer  
**Thời lượng chuẩn:** 3 phút 30 giây (210 giây) | **Dung lượng:** ~465 từ (tốc độ nói tiêu chuẩn 135 từ/phút)  
**Mục tiêu:** Thuyết phục hội đồng về giá trị của kỹ thuật kiểm thử hộp trắng trong việc phát hiện các lỗi logic và điểm mù mà kiểm thử hộp đen hoàn toàn bỏ sót.

```
   TIMELINE THUYẾT TRÌNH 3,5 PHÚT CỦA THÀNH VIÊN 4 (PHÚT 05:00 - 08:30)
 ┌────────────────────────────────────────────────────────────────────────┐
 │ [05:00 - 05:40] Nghịch lý 97% Line Coverage vs. 67% Mutation Score    │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [05:40 - 06:40] Đồ thị luồng, McCabe V(G) = 3 và Tử huyệt Đỉnh N4     │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [06:40 - 07:50] Kỹ thuật Detached Entity + ArgumentCaptor diệt Mutant  │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [07:50 - 08:20] Tổng kết đóng góp TV4 (36 tests, Binder, Phân trang)  │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [08:20 - 08:30] Câu chuyển giao sang TV5 (RCA & Báo cáo tổng hợp)     │
 └────────────────────────────────────────────────────────────────────────┘
```

---

### [05:00 – 05:40] Đặt vấn đề: Nghịch lý độ phủ tại tầng Web Controller (40 giây — ~90 từ)

> "Kính thưa Thầy và các bạn, tiếp nối phần trình bày của TV3, em xin đại diện nhóm phụ trách kiểm thử hộp trắng cho tầng Web Controller.
> Khi bắt đầu với mã nguồn gốc của Spring PetClinic, chúng em ghi nhận nghịch lý lớn: Line Coverage đạt tới 97%, nhưng Mutation Score chỉ đạt 67%!
> Nguyên nhân cốt lõi nằm ở 'điểm mù' của Spring MockMvc: cơ chế DataBinder tự động ghi dữ liệu vào Model trước khi Controller thực thi. Khi test chỉ kiểm tra mã HTTP 200 hoặc View Name, các lệnh gán dữ liệu nghiệp vụ trở thành gán dư thừa. Dù PIT xóa sạch các lệnh này, test vẫn Pass!"

---

### [05:40 – 06:40] Phân tích hộp trắng: Flow Graph và McCabe $V(G)$ (60 giây — ~135 từ)

> "Để giải quyết triệt để vấn đề, em tiến hành giải phẫu mã nguồn bằng lý thuyết kiểm thử hộp trắng của Thomas McCabe.
> Trên màn hình là Đồ thị luồng điều khiển của phương thức then chốt `updatePetDetails` trong `PetController`.
> Đồ thị gồm 7 đỉnh, 8 cạnh và 2 điểm quyết định rẽ nhánh tại N1 và N3. Áp dụng hai công thức tính độc lập: $E - N + 2$, và $P + 1$, ta đều thu được kết quả đồng nhất: Độ phức tạp Cyclomatic $V(G)$ đúng bằng 3.
> Tương ứng với $V(G) = 3$ là 3 đường cơ sở độc lập tuyến tính:
> Thứ nhất, nhánh fail-fast khi ID rỗng ném ngoại lệ;
> Thứ hai, nhánh thêm mới khi thú cưng chưa có trong chủ nuôi;
> Và quan trọng nhất là đường cơ sở số hai, đi qua đỉnh N4 — nơi thực hiện ba lệnh gán `setName`, `setBirthDate` và `setType`. Đây chính là 'tử huyệt' nơi 3 mutant sống sót lẩn trốn."

---

### [06:40 – 07:50] Giải pháp đột phá: Detached Entity & ArgumentCaptor (70 giây — ~145 từ)

> "Để diệt tận gốc 3 mutant này, em thiết kế kỹ thuật đột phá: đưa kiểm thử về tầng Unit thuần với mô hình 'Detached Entity' kết hợp Mockito 'ArgumentCaptor'.
> Thay vì dùng MockMvc, bài test chủ động khởi tạo hai đối tượng `Pet` tách biệt trên bộ nhớ Heap: đối tượng `managed` mang thông tin cũ là 'petty', còn đối tượng `detached` truyền từ Form mang thông tin mới là 'Betty'.
> Khi gọi cập nhật, Controller bắt buộc phải chạy qua đỉnh N4 để sao chép dữ liệu từ detached sang managed. Tại lệnh lưu cơ sở dữ liệu, em dùng `ArgumentCaptor` chặn bắt đối tượng `Owner` và xác nhận: Tên thú cưng lưu vào cơ sở dữ liệu bắt buộc phải là 'Betty'.
> Nếu mutant xóa bỏ lệnh `setName`, tên thú cưng vẫn giữ nguyên là 'petty', bài test lập tức thất bại. Nhờ đó, toàn bộ 3 mutant cứng đầu tại dòng 192, 193, 194 đã bị tiêu diệt hoàn toàn!"

---

### [07:50 – 08:20] Tổng kết đóng góp kỹ thuật của TV4 (30 giây — ~70 từ)

> "Bên cạnh `updatePetDetails`, trong 36 test methods do em xây dựng:
> Em đã bảo vệ an toàn cho cả ba Controller trước lỗ hổng Mass Assignment bằng cách dùng `verify` kiểm tra lệnh cấm bind trường ID;
> Đồng thời bắt trọn chỉ số phân trang zero-based trong `OwnerController`, nâng toàn diện Mutation Score của gói owner từ 67% lên mức 98%, đạt độ phủ dòng tuyệt đối 100% trên toàn bộ 250 dòng lệnh."

---

### [08:20 – 08:30] Câu chuyển giao sang Thành viên 5 (10 giây — ~25 từ)

> *"Và sau đây, xin kính mời bạn Thành viên 5 tiếp tục trình bày về Phân tích nguyên nhân gốc rễ RCA, minh chứng mutant tương đương và báo cáo tổng kết của nhóm."*

