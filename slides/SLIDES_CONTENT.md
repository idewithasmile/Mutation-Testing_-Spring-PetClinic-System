# NỘI DUNG VÀ KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỀ TÀI: R01-K03
**Đề tài:** Mutation Testing bằng PIT trên Spring PetClinic  
**Học phần:** Kiểm thử phần mềm — Khoa CNTT, Trường Đại học Đà Lạt  
**Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm  
**Nhóm thực hiện:** Nhóm 20 (Program_R01-K03)  
**Thời lượng toàn bài:** 15 phút (12 Slides, trong đó phần TV5 chiếm 3,5 phút: Slide 7, 8, 9)

---

## TỔNG QUAN PHÂN BỔ TIMELINE 15 PHÚT BẢO VỆ

| Slide | Thời gian | Người trình bày | Nội dung trọng tâm |
| :---: | :---: | :--- | :--- |
| **Slide 1** | 00:00 – 01:00 | TV1 (Trịnh Trung Hiếu) | Bìa đề tài, giới thiệu nhóm, mục tiêu K03 |
| **Slide 2** | 01:00 – 02:30 | TV2 (Trần Đình Việt Huy) | Bài toán nghiệp vụ SUT Spring PetClinic & 3 luồng cốt lõi gói `owner` |
| **Slide 3** | 02:30 – 03:45 | TV1 (Trịnh Trung Hiếu) | Nguyên lý Mutation Testing, Mô hình RIP và Chuỗi IEEE Error-Fault-Failure |
| **Slide 4** | 03:45 – 05:00 | TV1 (Trịnh Trung Hiếu) | Giải quyết xung đột JUnit 6 / PIT 1.30.0 & Cổng chất lượng Quality Gate 88% |
| **Slide 5** | 05:00 – 06:30 | TV3 (Trần Minh Tài) | Kiểm thử Hộp đen Domain & Validator: BVA và Decision Table (45 tests) |
| **Slide 6** | 06:30 – 08:30 | TV4 (Trương Bảo Bảo) | Kiểm thử Hộp trắng Web Controller: McCabe V(G)=3 & Detached Entity (36 tests) |
| **Slide 7** | **08:30 – 09:35** | **TV5 (Hoàng Việt Linh)** | **Ảo giác an toàn: 97% Line Coverage vs 67% Mutation Score (Test Gap 29.62%)** |
| **Slide 8** | **09:35 – 10:50** | **TV5 (Hoàng Việt Linh)** | **RCA 64 Baseline Survivors & 6 Code Smells theo chuẩn IEEE 1044** |
| **Slide 9** | **10:50 – 12:00** | **TV5 (Hoàng Việt Linh)** | **Chứng minh 3 Equivalent Mutants & Điểm số hiệu chỉnh 100.00% (192/192)** |
| **Slide 10** | 12:00 – 13:15 | TV1 (Trịnh Trung Hiếu) | Tự động hóa CI/CD GitHub Actions 6 bước & Khả năng tái hiện 1-lệnh |
| **Slide 11** | 13:15 – 14:15 | TV5 (Hoàng Việt Linh) | Tổng kết đối sánh Baseline vs Final & 4 Bài học kinh nghiệm thực tiễn |
| **Slide 12** | 14:15 – 15:00 | Toàn nhóm | Lời cảm ơn Hội đồng & Sẵn sàng cho phiên Hỏi - Đáp (Q&A) |

---

## CHI TIẾT NỘI DUNG & SPEAKER NOTES TỪNG SLIDE

### SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)
- **Tiêu đề:** KIỂM THỬ ĐỘT BIẾN (MUTATION TESTING) BẰNG PIT TRÊN SPRING PETCLINIC
- **Phụ đề:** Học phần: Kiểm thử phần mềm | Mã đề tài: R01 (Spring PetClinic) + K03 (Mutation Testing)
- **Đơn vị:** Khoa Công nghệ Thông tin — Trường Đại học Đà Lạt
- **Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm
- **Nhóm sinh viên thực hiện (Nhóm 20):**
  1. Trịnh Trung Hiếu (2312618) — QA Lead & DevSecOps
  2. Trần Đình Việt Huy (2312619) — System Architect & Test Lead
  3. Trần Minh Tài (2312794) — Domain & Black-Box Test Engineer
  4. Trương Bảo Bảo (2312582) — White-Box & Controller Test Engineer
  5. Hoàng Việt Linh (2312664) — Metrics, RCA & Quality Analyst
- **Kết quả cốt lõi:** Mutation Score: 98.46% (192/195 killed) — Line Coverage: 100.00% (250/250 lines) — 153/153 Tests Passed.
- **Speaker Notes (TV1 — 60s):**
  > *"Kính thưa Thầy Nguyễn Thế Lâm và toàn thể Hội đồng, hôm nay nhóm 20 xin trân trọng báo cáo kết quả thực hiện đề tài kết hợp R01 và K03: Kiểm thử đột biến (Mutation Testing) bằng PIT trên hệ thống Spring PetClinic. Nhóm chúng em gồm 5 thành viên được phân công chuyên biệt theo đúng quy trình công nghệ phần mềm chuyên nghiệp. Với cam kết khoa học nghiêm ngặt: không sửa đổi bất kỳ dòng mã nguồn sản phẩm nào, nhóm đã tối ưu hóa toàn diện bộ kiểm thử, nâng Mutation Score từ mức ban đầu 67% lên 98.46%, đạt độ bao phủ dòng tuyệt đối 100% và chứng minh 3 đột biến còn lại là tương đương. Sau đây, xin mời bạn Việt Huy bắt đầu với kiến trúc hệ thống SUT."*

---

### SLIDE 2: BÀI TOÁN NGHIỆP VỤ & PHẠM VI HỆ THỐNG SUT (TV2)
- **Tiêu đề:** Bài toán nghiệp vụ & Phạm vi đột biến gói `owner.*`
- **Các điểm chính (≤ 6 dòng):**
  - **SUT:** Spring PetClinic (Commit SHA khóa cứng `500158f732419217507c7656904b8e6aa1bcc0d6`).
  - **Công nghệ nền tảng:** Java 17, Spring Boot 4.1.0, Spring Data JPA, Thymeleaf, CSDL H2 in-memory.
  - **Phạm vi kiểm thử K03:** Giới hạn nghiêm ngặt tại gói nghiệp vụ trung tâm `org.springframework.samples.petclinic.owner.*`.
  - **03 Luồng nghiệp vụ cốt lõi đã kiểm chứng HTTP 200 trên runtime thật:**
    1. Tìm kiếm và phân trang chủ nuôi (`OwnerController.processFindForm`).
    2. Thêm mới thú cưng kèm kiểm chuẩn dữ liệu (`PetController` + `PetValidator`).
    3. Đặt lịch khám và lưu bệnh án thú cưng (`VisitController`).
- **Speaker Notes (TV2 — 90s):**
  > *"Kính thưa Thầy, đối tượng SUT của nhóm là Spring PetClinic, một ứng dụng chuẩn mực trong hệ sinh thái Spring. Để đảm bảo tính khả tái khoa học, nhóm đã khóa cứng commit SHA ngày 29/09/2026. Thay vì chạy đột biến toàn repo gây lãng phí tính toán, nhóm tập trung toàn lực vào gói nghiệp vụ phức tạp nhất là `owner.*` gồm 8 lớp thực thể, validator và controller. Nhóm đã dựng môi trường thực tế và xác minh thành công cả 3 luồng nghiệp vụ chạy mượt mà trên cổng 8090 với mã HTTP 200. Sau đây xin mời bạn Trung Hiếu trình bày về cơ sở lý thuyết kiểm thử đột biến."*

---

### SLIDE 3: NGUYÊN LÝ MUTATION TESTING & MÔ HÌNH CHUẨN IEEE / RIP (TV1)
- **Tiêu đề:** Mô hình lý thuyết IEEE Error – Fault – Failure và Chuỗi RIP trong PIT
- **Các điểm chính (≤ 6 dòng):**
  - **Cơ sở lý thuyết:** Giả thuyết lập trình viên có năng lực (CPH) và Hiệu ứng khớp lệnh (Coupling Effect).
  - **Toán tử đột biến (Mutant):** PIT tiêm lỗi cú pháp giả lập vào Bytecode compiled (`.class`).
  - **Chuỗi điều kiện RIP (Reachability – Infection – Propagation):**
    - **Reachability (R):** Test case chạy qua dòng mã chứa mutant (tránh `NO_COVERAGE`).
    - **Infection (I):** Lệnh đột biến làm biến đổi trạng thái nội bộ bộ nhớ JVM (sinh ra **Error**).
    - **Propagation (P):** Trạng thái sai lệch lan truyền ra ngõ ra/kết quả quan sát được (**Failure**).
  - **Tiêu diệt Mutant (Killed):** Test Assertion bắt được sai lệch và báo **FAIL / ERROR**.
  - **Mutant sống sót (Survived):** Test case yếu, thiếu assert hoặc bị che giấu trạng thái, test vẫn **PASS**.
- **Speaker Notes (TV1 — 75s):**
  > *"Kỹ thuật Mutation Testing là phương pháp kiểm thử hộp trắng hướng lỗi khắt khe nhất hiện nay. Khác với kiểm thử thông thường chỉ đo xem code có chạy qua không, PIT vận hành theo chuỗi chuyển hóa chặt chẽ theo chuẩn IEEE: Từ khiếm khuyết nhân tạo (Fault) tiêm vào bytecode, ca kiểm thử phải thỏa mãn đồng thời 3 điều kiện RIP: Phải chạm tới dòng mã (Reachability), làm thay đổi giá trị trong bộ nhớ (Infection), và sai lệch đó bắt buộc phải lan truyền ra ngõ ra quan sát được (Propagation). Nếu câu lệnh Assertion của bài test nhạy bén, bài test sẽ Fail và mutant được coi là KILLED. Ngược lại, nếu test chỉ assert hời hợt hoặc nuốt lỗi, bài test vẫn xanh và mutant sẽ SURVIVED. Đây chính là thước đo vàng cho chất lượng bộ kiểm thử."*

---

### SLIDE 4: GIẢI QUYẾT XUNG ĐỘT KỸ THUẬT & CỔNG CHẤT LƯỢNG QUALITY GATE (TV1)
- **Tiêu đề:** Xử lý xung đột JUnit 6 / PIT 1.30.0 & Thiết lập Cổng chất lượng
- **Các điểm chính (≤ 6 dòng):**
  - **Sự cố JUnit 6:** Spring Boot 4.1.0 kéo theo JUnit Platform 6.0.3 khiến plugin PIT 1.2.1 cũ sập minion (`UNKNOWN_ERROR`).
  - **Giải pháp đồng bộ:** Nâng cấp cấu hình Maven lên `pitest-maven:1.30.0` + `pitest-junit5-plugin:1.2.3`.
  - **Xử lý xung đột JaCoCo:** Dùng cờ `-Djacoco.skip=true` ngăn Java Agent can thiệp méo mó bytecode.
  - **Tập toán tử khắt khe `STRONGER`:** Kích hoạt 11 loại mutator nâng cao (Boundary, VoidCall, Math, NegateConditionals...).
  - **Cổng chất lượng tự động (Quality Gate) thiết lập trong `pom.xml`:**
    - `<mutationThreshold>88</mutationThreshold>` (Yêu cầu đề tài: $\ge 88\%$).
    - `<coverageThreshold>95</coverageThreshold>` (Bảo đảm bao phủ dòng $\ge 95\%$).
    - Tự động đánh trượt tiến trình build (`BUILD FAILURE`) nếu vi phạm bất kỳ ngưỡng nào.
- **Speaker Notes (TV1 — 75s):**
  > *"Trong quá trình triển khai, nhóm gặp sự cố kỹ thuật lớn: Spring Boot 4 kéo theo JUnit Platform 6.0.3, khiến phiên bản PIT gợi ý trong syllabus bị crash minion ngay khi khởi động. Em đã nghiên cứu tài liệu kỹ thuật của PIT và nâng cấp lên bộ đôi pitest-maven 1.30.0 và pitest-junit5-plugin 1.2.3, đồng thời vô hiệu hóa JaCoCo agent để tránh xung đột bytecode. Nhóm cũng kích hoạt nhóm mutator STRONGER toàn diện nhất và cài đặt trực tiếp Cổng chất lượng Quality Gate vào pom.xml với ngưỡng 88% đột biến và 95% độ bao phủ. Bất kỳ commit nào làm điểm số tụt dưới 88% đều bị hủy bỏ ngay lập tức. Sau đây, xin mời bạn Minh Tài trình bày về chiến lược kiểm thử hộp đen."*

---

### SLIDE 5: THIẾT KẾ TEST HỘP ĐEN DOMAIN & VALIDATOR — TV3 (TRẦN MINH TÀI)
- **Tiêu đề:** Thiết kế kiểm thử Hộp đen: BVA & Bảng quyết định (45 tests)
- **Các điểm chính (≤ 6 dòng):**
  - **Phạm vi TV3 phụ trách:** `OwnerMutationTests` (27 tests), `PetValidatorMutationTests` (9 tests), `PetVisitModelMutationTests` (9 tests).
  - **Phân tích giá trị biên (BVA 2-point):**
    - Kiểm chuẩn độ dài tên thú cưng tại ngưỡng biên 30 và 31 ký tự (`MAX_NAME_LENGTH = 30`).
    - Tiêu diệt triệt để `ConditionalsBoundaryMutator` tại `PetValidator:58` (`>` đổi thành `>=`).
  - **Bảng quyết định (Decision Table):**
    - Phân tích 8 tổ hợp điều kiện: `hasText && isNew && getPet() != null` trong `PetController`.
    - Phân tích bảng quyết định 2 chiều cho `Owner.addPet`: kiểm tra thực thể mới vs đã lưu và trùng ID.
  - **Assert nội dung sâu (Deep Assertion):** Assert chi tiết chuỗi `toString()`, kiểm tra `print(null)` trả về `"<null>"`.
- **Speaker Notes (TV3 — 90s):**
  > *"Kính thưa Thầy, em chịu trách nhiệm thiết kế 45 ca kiểm thử hộp đen tập trung vào tầng Domain và Validator. Điểm yếu lớn của bộ test ban đầu là chỉ test tên pet 31 ký tự mà không test biên 30 ký tự, khiến PIT đổi dấu lớn hơn thành lớn hơn hoặc bằng mà test cũ vẫn Pass. Em đã áp dụng kỹ thuật Phân tích giá trị biên BVA, viết ca test chấp nhận tên đúng 30 ký tự để diệt gọn mutant này. Đồng thời, em xây dựng các Bảng quyết định toàn diện cho hàm addPet và getPet của Owner để vét cạn mọi tổ hợp cờ isNew và ID trùng nhau. Nhờ vậy, toàn bộ 45 test của em đều đạt tính tất định cao và diệt sạch các mutant trên domain model. Tiếp theo, xin mời bạn Bảo Bảo trình bày về kiểm thử hộp trắng tầng Controller."*

---

### SLIDE 6: THIẾT KẾ TEST HỘP TRẮNG WEB CONTROLLER — TV4 (TRƯƠNG BẢO BẢO)
- **Tiêu đề:** Đồ thị luồng điều khiển, McCabe $V(G)=3$ & Detached Entity (36 tests)
- **Các điểm chính (≤ 6 dòng):**
  - **Phạm vi TV4 phụ trách:** 36 test methods trên 4 lớp Controller và Binder bổ sung.
  - **Giải phẫu Đồ thị luồng phương thức `updatePetDetails`:**
    - Cấu trúc: 7 đỉnh, 8 cạnh, 2 điểm quyết định rẽ nhánh $\implies$ Độ phức tạp Cyclomatic $V(G) = 3$.
    - 3 đường cơ sở McCabe: $BP_{23}$ (fail-fast ID null), $BP_{24}$ (update fields đỉnh N4), $BP_{25}$ (add mới).
  - **Tử huyệt đỉnh N4 & Điểm mù Spring MockMvc:**
    - Test MockMvc cũ bị cơ chế DataBinder ghi đè dữ liệu trước khi chạy, biến 3 lệnh copy `setName`, `setBirthDate`, `setType` thành gán trùng lặp (`x = x`).
  - **Giải pháp đột phá Detached Entity:**
    - Khởi tạo POJO unit test trực tiếp, truyền thực thể tách rời (`detached` mang tên "Betty" vs `managed` mang tên "petty").
    - Dùng Mockito `ArgumentCaptor<Owner>` bắt thực thể tại lệnh `saveAndFlush` để assert từng trường dữ liệu $\implies$ Diệt 100% mutants!
- **Speaker Notes (TV4 — 120s):**
  > *"Tiếp nối phần TV3, em phụ trách kiểm thử hộp trắng cho 3 Controller. Như Thầy thấy trên đồ thị luồng phương thức updatePetDetails, độ phức tạp McCabe là 3 tương ứng 3 đường cơ sở. Tại đỉnh N4 có 3 lệnh sao chép trường dữ liệu. Điểm mù cực lớn của MockMvc là cơ chế Form Binder đã tự động ghi đè dữ liệu lên chính entity trong bộ nhớ, khiến các lệnh copy này thành gán dư thừa. Khi PIT xóa sạch 3 dòng này, test MockMvc cũ vẫn xanh! Để diệt tận gốc tử huyệt này, em đã đưa test về tầng POJO thuần, truyền một đối tượng detached riêng biệt và dùng Mockito ArgumentCaptor để chặn bắt thực thể tại hàm saveAndFlush. Nếu mutant xóa lệnh gán, dữ liệu cũ giữ nguyên và test sẽ đánh trượt ngay lập tức. Sau đây, xin kính mời bạn Việt Linh trình bày phân tích số liệu RCA và chứng minh đột biến tương đương."*

---

### SLIDE 7: ẢO GIÁC AN TOÀN — LINE COVERAGE 97% VS MUTATION SCORE 67% — TV5 (HOÀNG VIỆT LINH)
- **Tiêu đề:** "Ảo giác an toàn": 97% Line Coverage vs. 67% Mutation Score
- **Nội dung hiển thị (≤ 6 dòng):**
  - **Hiện tượng thực nghiệm tại gói `owner.*` (Hình G.1):**
    - Bộ test gốc của Spring PetClinic đạt độ bao phủ dòng rất cao: **96.80% (242/250 lines)**.
    - Tuy nhiên, điểm Mutation Score ban đầu chỉ đạt khiêm tốn: **67.18% (131/195 killed)**.
  - **Khoảng trống kiểm thử nguy hiểm (Test Gap):** Lên tới **29.62%**!
  - **Vạch trần bản chất:**
    - Line Coverage chỉ đo lường việc lệnh có được nạp vào CPU hay không (**Execution Coverage**).
    - Line Coverage hoàn toàn bỏ qua năng lực của câu lệnh Assertion và sự lan truyền lỗi (**Propagation**).
  - **Kết quả cải tiến của nhóm:**
    - Line Coverage đạt **100.00% (250/250 lines)**.
    - Mutation Score đạt **98.46% (192/195 killed)**, triệt tiêu hoàn toàn khoảng trống rủi ro!
- **Hình ảnh nhúng:** `reports/figures/fig1_coverage_vs_mutation.png` (chiếm 50% diện tích slide).
- **Speaker Notes (TV5 — 65s, ~140 từ):**
  > *"Kính thưa Thầy và Hội đồng, tiếp nối phần trình bày của bạn Bảo Bảo, em xin đại diện nhóm phân tích chuyên sâu về chất lượng kiểm thử. Trên màn hình là Hình G.1 — biểu đồ minh chứng cho phát hiện học thuật quan trọng nhất của đề tài: 'Ảo giác an toàn' của độ bao phủ dòng.  
  > Khi tiếp nhận mã nguồn gốc của Spring PetClinic, JaCoCo báo cáo một con số rất ấn tượng: 96.80% Line Coverage, chỉ sót đúng 8 dòng mã. Thế nhưng khi tiêm đột biến bằng PIT, điểm số thực tế chỉ đạt 67.18%, để lọt lưới tới 64 mutants nguy hiểm. Khoảng trống kiểm thử lên tới gần 30%! Điều này chứng minh rằng code được thực thi không đồng nghĩa với code được kiểm tra đúng đắn. Nhờ 81 test case bổ sung được thiết kế bài bản, nhóm đã đưa Line Coverage lên tuyệt đối 100% và Mutation Score đạt 98.46%, xóa bỏ hoàn toàn khoảng trống rủi ro này."*

---

### SLIDE 8: PHÂN TÍCH NGUYÊN NHÂN CỐT LÕI (RCA) & CODE SMELLS — TV5 (HOÀNG VIỆT LINH)
- **Tiêu đề:** Phân tích nguyên nhân gốc rễ (RCA) 64 Survivors & 6 Code Smells
- **Nội dung hiển thị (≤ 6 dòng):**
  - **Chuẩn hóa mô hình:** Áp dụng tiêu chuẩn IEEE 1044 / IEEE 610.12 (Error $\to$ Fault $\to$ Failure).
  - **Phân bổ 64 Mutants sống sót ở Baseline vào 6 nhóm nguyên nhân (Bảng G.5, Hình G.3):**
    - Thiếu Bảng quyết định cho logic phức tạp: **27 mutants (42.19%)**.
    - Thiếu verify tương tác hàm void/binder: **14 mutants (21.88%)**.
    - Nhánh ngoại lệ & luồng rẽ thiếu độ bao phủ: **9 mutants (14.06%)**.
    - Phân tích giá trị biên BVA & tính toán số học: **6 mutants (9.38%)**.
    - MockMvc che giấu cập nhật & gán dư thừa: **5 mutants (7.81%)**.
    - Thiếu assert nội dung sâu & giá trị trả về: **3 mutants (4.69%)**.
  - **Phát hiện 6 Code Smells:** Độc lập ghi nhận các khiếm khuyết thiết kế (Dead-Store dòng 167, điều kiện dư dòng 108, truy vấn lặp dòng 181...) mà không sửa mã nguồn `src/main/java`.
- **Hình ảnh nhúng:** `reports/figures/fig3_survivors_by_mutator.png` kết hợp bảng tóm tắt 6 nhóm lỗi.
- **Speaker Notes (TV5 — 75s, ~160 từ):**
  > *"Để tìm hiểu vì sao 64 mutant ở Baseline sống sót, em đã thực hiện phân tích nguyên nhân gốc rễ RCA theo chuẩn IEEE 1044 và IEEE 610.12. Kết quả bóc tách cho thấy nguyên nhân lớn nhất chiếm hơn 42% là do bài test cũ thiếu Bảng quyết định, dẫn đến bỏ sót các tổ hợp rẽ nhánh lồng nhau. Nguyên nhân thứ hai chiếm gần 22% là do thiếu lệnh verify kiểm tra các hàm void, đặc biệt là cấu hình bảo mật cấm bind trường ID trong Controller.  
  > Bên cạnh việc chỉ ra điểm yếu của test suite, kiểm thử đột biến còn hoạt động như một kính hiển vi vạch trần 6 Code Smells trong mã nguồn PetClinic. Điển hình như lệnh gán dead-store tại OwnerController dòng 167 hay biểu thức điều kiện phòng vệ cực đoan tại Owner dòng 108. Tuân thủ nghiêm ngặt ràng buộc đóng băng mã nguồn sản phẩm, nhóm không sửa code mà chuyển hóa các phát hiện này thành ma trận truy vết và khuyến nghị tái cấu trúc."*

---

### SLIDE 9: CHỨNG MINH 3 EQUIVALENT MUTANTS & ĐIỂM HIỆU CHỈNH 100% — TV5 (HOÀNG VIỆT LINH)
- **Tiêu đề:** Chứng minh toán học 3 Equivalent Mutants & Điểm hiệu chỉnh 100%
- **Nội dung hiển thị (≤ 6 dòng):**
  - **Đột biến tương đương (Equivalent Mutant):** $\forall I \in \mathcal{D}, P(I) \equiv M(I)$ $\implies$ Không thể bị tiêu diệt bởi bất kỳ test case nào!
  - **Mutant M1 & M2 (`Owner.java:108` — ép `!existingPet.isNew()` và `!pet.isNew()` thành `true`):**
    - Đại số Boolean: Vì $isNew() \iff id == null$, khi ID khác null thì điều kiện này phụ thuộc hoàn toàn vào $Objects.equals(id_1, id_2)$.
    - Bảng chân trị 5 lớp tương đương chứng minh $C_{orig} \equiv C_{M1} \equiv C_{M2}$ trên 100% không gian trạng thái (đã kiểm chứng 9/9 case bằng Python script).
  - **Mutant M3 (`OwnerController.java:167` — xóa `owner.setId(ownerId)`):**
    - Đồ thị luồng CFG chứng minh khối guard dòng 161 đã bảo toàn bất biến $owner.getId() == ownerId$ trước khi chạm dòng 167 $\implies$ Lệnh gán là dead-store thuần túy.
  - **Điểm số hiệu chỉnh học thuật (Adjusted Mutation Score):**
    - Điểm thô chính thức của PIT: **192 / 195 = 98.46%**.
    - Điểm hiệu chỉnh khả thi: **192 / (195 - 3) = 192 / 192 = 100.00% (Hoàn hảo)**.
- **Hình ảnh nhúng:** Bảng chân trị tóm tắt 5 lớp tương đương và công thức điểm hiệu chỉnh.
- **Speaker Notes (TV5 — 70s, ~160 từ):**
  > *"Điểm nhấn học thuật đặc sắc nhất trong phần việc của em là chứng minh hình thức cho 3 mutants sống sót cuối cùng. Đây không phải là điểm yếu của bộ test, mà là 3 Đột biến tương đương về mặt ngữ nghĩa:  
  > Tại Owner dòng 108, hai mutant ép các mệnh đề isNew thành true. Em đã mô hình hóa đại số Boolean và lập bảng chân trị trên toàn bộ 5 lớp tương đương của không gian trạng thái. Kết quả chứng minh giá trị logic của mutant luôn đồng nhất tuyệt đối 100% với code gốc, và đã được xác thực tự động bằng script Python duyệt vét cạn.  
  > Tương tự tại OwnerController dòng 167, phân tích đồ thị luồng chứng minh khối guard phía trước đã đảm bảo hai ID chắc chắn bằng nhau. Lệnh setId chỉ là một dead-store phòng thủ, việc xóa nó không làm thay đổi bất kỳ hành vi nào của hệ thống.  
  > Vì vậy, khi loại trừ 3 mutant tương đương khỏi không gian đột biến khả thi, điểm số hiệu chỉnh thực tế của nhóm đạt tuyệt đối 100%. Sau đây, xin mời bạn Trung Hiếu trình bày về đường ống CI/CD."*

---

### SLIDE 10: TỰ ĐỘNG HÓA ĐƯỜNG ỐNG CI/CD & HƯỚNG DẪN TÁI HIỆN 1-LỆNH (TV1)
- **Tiêu đề:** Đường ống CI/CD GitHub Actions & Tính khả tái 1-lệnh
- **Các điểm chính (≤ 6 dòng):**
  - **Đường ống CI/CD 6 bước Fail-Fast (`.github/workflows/mutation-test.yml`):**
    1. Checkout mã nguồn `actions/checkout@v4` (fetch full depth).
    2. Setup JDK 17 Temurin + Maven Cache.
    3. Cổng kiểm thử nhanh: Chạy 153 Unit Tests toàn hệ thống (dừng ngay nếu có lỗi).
    4. Cổng chất lượng K03: Thực thi PIT Mutation Testing & chặn build nếu score $< 88\%$.
    5. Xuất bảng tóm tắt trực quan `$GITHUB_STEP_SUMMARY` lên giao diện GitHub.
    6. Đóng gói và lưu trữ Artifacts báo cáo HTML/XML trong 30 ngày.
  - **Tính khả tái thực nghiệm 1-lệnh (One-Liner Reproducibility):**
    - PowerShell: `.\mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'`
    - Thời gian chạy thực tế: ~35–45 giây trên máy trạm thông thường.
- **Speaker Notes (TV1 — 75s):**
  > *"Để đảm bảo tính liên tục và kiểm soát chất lượng tự động, nhóm đã thiết lập đường ống CI/CD hoàn chỉnh trên GitHub Actions theo kiến trúc 6 bước Fail-Fast. Hệ thống sẽ ưu tiên chạy 153 unit test trong 15 giây đầu; nếu có lỗi hồi quy, quy trình sẽ ngắt ngay để tiết kiệm tài nguyên. Tiếp theo, bước phân tích đột biến PIT sẽ thực thi và áp dụng Cổng chất lượng 88%. Nhóm cũng tối ưu hóa khả năng tái hiện với duy nhất 1 câu lệnh Maven Wrapper, giúp bất kỳ ai cũng có thể tự mình kiểm chứng kết quả trong vòng 35 đến 45 giây. Sau đây, xin mời bạn Việt Linh tổng kết kết quả và bài học kinh nghiệm của nhóm."*

---

### SLIDE 11: TỔNG KẾT KẾT QUẢ BASELINE VS FINAL & BÀI HỌC KINH NGHIỆM (TV5)
- **Tiêu đề:** Tổng kết đối sánh Baseline vs Final & 4 Bài học kinh nghiệm
- **Bảng đối sánh chỉ số cốt lõi (Khớp 100% `metrics_summary.csv`):**
  - Số lượng test gói `owner`: **49 tests $\to$ 130 tests (+81 tests)**.
  - Line Coverage: **96.80% (242/250) $\to$ 100.00% (250/250 lines)**.
  - Mutants Killed: **131 / 195 (67.18%) $\to$ 192 / 195 (98.46%)** *(Ngưỡng $\ge 88\%$)*.
  - Mutants Survived: **55 $\to$ 3 mutants** *(100% Equivalent Mutants)*.
  - Mutants No Coverage: **9 $\to$ 0 mutants** *(Triệt tiêu hoàn toàn vùng mù)*.
  - Điểm số hiệu chỉnh (Adjusted Score): **68.23% $\to$ 100.00% (192/192)**.
- **4 Bài học kinh nghiệm thực tiễn:**
  1. Line Coverage cao tạo ra an tâm giả tạo; Mutation Testing là thước đo chất lượng thực sự.
  2. Cảnh giác với cạm bẫy Model Aliasing của Spring MockMvc; cần bổ sung POJO Unit Test.
  3. Bắt buộc kiểm tra tương tác (Interaction Testing) bằng `verify` cho các phương thức void.
  4. Kỹ thuật hộp trắng (BVA, Decision Table, Basis Path) là vũ khí tối thượng để diệt mutant.
- **Speaker Notes (TV5 — 60s, ~130 từ):**
  > *"Nhìn lại toàn bộ hành trình, Bảng tổng kết trên slide đã minh chứng sự bứt phá vượt bậc của dự án: Số lượng test tăng từ 49 lên 130 bài, độ phủ dòng đạt tuyệt đối 100%, và điểm đột biến tăng ngoạn mục từ 67.18% lên 98.46%, loại bỏ hoàn toàn các vùng mã mù kiểm thử.  
  > Bốn bài học kinh nghiệm lớn nhất mà nhóm đúc kết được là: Không bao giờ tin tưởng mù quáng vào Code Coverage; luôn cảnh giác trước cạm bẫy che giấu lỗi của MockMvc; bắt buộc phải verify tương tác cho các hàm void bảo mật; và áp dụng bài bản các kỹ thuật hộp trắng kinh điển như BVA và Bảng quyết định. Đây chính là hành trang chuyên môn vô giá cho chúng em trong ngành kiểm thử phần mềm chuyên nghiệp."*

---

### SLIDE 12: LỜI CẢM ƠN & PHIÊN HỎI ĐÁP (Q&A SLIDE)
- **Tiêu đề:** LỜI CẢM ƠN VÀ SẴN SÀNG CHO PHIÊN HỎI ĐÁP (Q&A)
- **Nội dung hiển thị:**
  - Nhóm 20 (Program_R01-K03) xin chân thành cảm ơn ThS. Nguyễn Thế Lâm đã tận tình hướng dẫn trong suốt học phần Kiểm thử phần mềm!
  - Toàn bộ mã nguồn, cấu hình CI/CD, bộ test và báo cáo chi tiết được lưu trữ minh bạch tại GitHub Repository của nhóm.
  - **SẴN SÀNG TRẢ LỜI CÁC CÂU HỎI PHẢN BIỆN TỪ QUÝ THẦY CÔ VÀ HỘI ĐỒNG!**
- **Speaker Notes (Toàn nhóm — 45s):**
  > *"Kính thưa Thầy Nguyễn Thế Lâm và quý Thầy Cô trong Hội đồng, phần báo cáo của nhóm 20 về đề tài R01 kết hợp K03 đến đây là hoàn tất. Chúng em xin chân thành cảm ơn sự hướng dẫn tận tâm của Thầy trong suốt học phần Kiểm thử phần mềm. Giờ đây, toàn thể 5 thành viên của nhóm đã sẵn sàng đón nhận những câu hỏi, nhận xét và đóng góp quý báu từ Thầy và Hội đồng. Chúng em xin trân trọng cảm ơn!"*
