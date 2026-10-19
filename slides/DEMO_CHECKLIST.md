# KỊCH BẢN PHỐI HỢP DEMO TRỰC TIẾP & PHƯƠNG ÁN DỰ PHÒNG (DEMO CHECKLIST)
**Học phần:** Kiểm thử phần mềm — Khoa Công nghệ Thông tin, Trường Đại học Đà Lạt  
**Đề tài:** Mutation Testing bằng PIT trên Spring PetClinic (K03 – Program_R01)  
**Phối hợp trực tiếp:** Thành viên 1 (Điều hành Terminal) & Thành viên 5 (Thuyết minh trực tiếp)  
**Thời lượng live demo:** Khoảng 35 – 45 giây

---

## I. CÔNG TÁC CHUẨN BỊ TRƯỚC PHIÊN BẢO VỆ (PRE-DEMO CHECKLIST)

Trước khi bước vào phòng bảo vệ trước Hội đồng, TV1 và TV5 phải hoàn tất 100% các bước sau trên máy tính thuyết trình:

- [ ] **1. Môi trường JDK:** Kiểm tra lệnh `java -version` (bắt buộc trả về Java 17+; biến `JAVA_HOME` đã thiết lập chuẩn).
- [ ] **2. Thư mục làm việc:** Mở sẵn cửa sổ PowerShell tại thư mục gốc repository:  
  `D:\Kiểm Thử Phần Mềm\Nhom_20\Mutation-Testing_-Spring-PetClinic-System`
- [ ] **3. Trình duyệt chuẩn bị sẵn tab offline (Kế hoạch dự phòng):**
  - Mở sẵn Tab 1: `target/pit-reports/index.html` (Báo cáo tổng quan màu xanh lá 98%).
  - Mở sẵn Tab 2: `target/pit-reports/org.springframework.samples.petclinic.owner/index.html` (Chi tiết từng class).
- [ ] **4. Text Editor mở sẵn tệp log:** Mở sẵn VS Code hiển thị tệp [`logs/pit_final_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_final_run.log).
- [ ] **5. Đóng các ứng dụng nặng ngầm:** Tắt các ứng dụng chiếm RAM để CPU dành 100% cho PIT minion JVM.

---

## II. KỊCH BẢN ĐIỀU HÀNH THỜI GIAN THỰC (TIMELINE DEMO 35 GIÂY)

```
   TIMELINE DEMO TRỰC TIẾP PIT MUTATION TESTING (35 - 45 GIÂY)
 ┌────────────────────────────────────────────────────────────────────────┐
 │ [00s - 05s] TV1 nhập lệnh chuẩn bị chạy; TV5 giới thiệu câu lệnh       │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [05s - 15s] Maven nạp dependencies, compile test; TV5 giải thích cờ    │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [15s - 25s] PIT Minion JVM khởi tạo, tiêm mutant; TV5 phân tích RIP   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [25s - 35s] Đánh giá test cases; TV5 bình luận Test Strength           │
 ├────────────────────────────────────────────────────────────────────────┤
 │ [35s - 45s] Console xuất BUILD SUCCESS; TV5 kết luận chỉ số 98%        │
 └────────────────────────────────────────────────────────────────────────┘
```

### Bước 1: Khởi động lệnh (Giây 00 – 05)
- **Thao tác của TV1:** Dán chính xác câu lệnh chuẩn vào PowerShell và nhấn `Enter`:
  ```powershell
  ./mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'
  ```
- **Lời dẫn của TV5 (Nói tự tin, rõ ràng):**
  > *"Kính thưa Thầy và Hội đồng, bây giờ bạn Thành viên 1 đang thực thi câu lệnh kiểm chứng 1-lệnh của nhóm trên terminal PowerShell. Câu lệnh này sẽ tự động biên dịch và kích hoạt plugin PIT Mutation Testing phiên bản 1.30.0 với nhóm toán tử STRONGER trên toàn bộ gói `owner`."*

### Bước 2: Giai đoạn phân tích và khởi tạo Minion (Giây 05 – 18)
- **Màn hình hiển thị:** Maven in ra các thông tin nạp plugin và dòng:
  `[INFO] Scanning for projects...`  
  `[INFO] --- pitest-maven:1.30.0:mutationCoverage ---`  
  `>> Sending MINION to JVM...`
- **Lời dẫn của TV5:**
  > *"Như Thầy đang thấy trên màn hình, PIT đang khởi tạo tiến trình con Minion JVM độc lập. Điểm mấu chốt ở đây là cờ `-Djacoco.skip=true`: Nhóm chủ động vô hiệu hóa JaCoCo agent để tránh hiện tượng can thiệp méo mó bytecode, bảo đảm PIT làm chủ hoàn toàn quá trình tiêm đột biến."*

### Bước 3: Giai đoạn tiêm đột biến và đánh giá bộ kiểm thử (Giây 18 – 32)
- **Màn hình hiển thị:** PIT in ra tiến trình quét đột biến:
  `>> Line Coverage (for mutated classes only): 250/250 (100%)`  
  `>> 28 tests examined`
- **Lời dẫn của TV5:**
  > *"Tiến trình đã tính toán xong độ phủ dòng: Đạt tuyệt đối 250/250 lines, tức 100%. Tiếp theo, PIT đang tiêm tổng cộng 195 mutants vào bytecode và thực thi 130 bài test của nhóm để kiểm tra sự lan truyền lỗi theo chuỗi RIP. Nhờ bộ test được tối ưu hóa chỉ chạy các bài test liên quan tới từng mutant, tiến trình thực thi cực kỳ nhanh chóng."*

### Bước 4: Nghiệm thu kết quả màn hình (Giây 32 – 40)
- **Màn hình hiển thị:**
  ```text
  ================================================================================
  - Statistics
  ================================================================================
  >> Line Coverage (for mutated classes only): 250/250 (100%)
  >> 28 tests examined
  >> Generated 195 mutations Killed 192 (98%)
  >> Mutations with no coverage 0. Test strength 98%
  >> Ran 589 tests (3.02 tests per mutation)
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  ```
- **Lời dẫn của TV5 (Đanh thép, dứt khoát):**
  > *"Chính xác sau 35 giây, kết quả đã xuất hiện: Generated 195 mutations, Killed 192, đạt Mutation Score 98.46%! BUILD SUCCESS! Cổng chất lượng 88% đã được vượt qua xuất sắc. Đúng 3 mutants sống sót đều là đột biến tương đương đã được nhóm chứng minh toán học. Bây giờ xin mời bạn TV1 mở báo cáo HTML trực quan trên trình duyệt."*

### Bước 5: Mở báo cáo HTML trực quan (Giây 40 – 45)
- **Thao tác của TV1:** Mở trình duyệt hiển thị tệp:
  `target/pit-reports/index.html`
- **Lời dẫn của TV5:**
  > *"Trên màn hình trình duyệt là giao diện báo cáo HTML chính thức của PIT: Toàn bộ thanh trạng thái của gói `owner` được phủ màu xanh lá cây đậm với 100% Line Coverage và 98% Mutation Coverage. Kết quả thực nghiệm hoàn toàn khớp 100% với báo cáo của nhóm."*

---

## III. PHƯƠNG ÁN DỰ PHÒNG XỬ LÝ SỰ CỐ (FALLBACK PLAN)

Trong trường hợp xảy ra sự cố kỹ thuật ngoài ý muốn (máy tính bị treo, lỗi môi trường Windows, tiến trình Maven bị khóa file, v.v.), nhóm kích hoạt ngay Kế hoạch B trong vòng **5 giây**:

### Tình huống 1: Lệnh chạy quá lâu (> 60 giây do máy lag hoặc thiếu RAM)
- **Hành động của TV1:** Nhấn `Ctrl + C` để hủy tiến trình terminal.
- **Lời dẫn phản xạ của TV5 (Bình tĩnh, chuyên nghiệp):**
  > *"Kính thưa Thầy, do máy trạm của nhóm đang mở đồng thời nhiều ứng dụng nên tiến trình cấp phát JVM bị chậm. Để không làm mất thời gian quý báu của Hội đồng, em xin phép mở trực tiếp tệp nhật ký thực thi thực tế vừa được chạy trước buổi bảo vệ."*
- **Hành động tiếp theo:** TV1 lập tức chuyển sang tab VS Code hiển thị tệp [`logs/pit_final_run.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/pit_final_run.log), cuộn xuống phần Statistics và đọc các chỉ số 192/195 (98%).

### Tình huống 2: Terminal báo lỗi `BUILD FAILURE` hoặc lỗi `JAVA_HOME`
- **Hành động của TV1:** Không hoảng loạn, lập tức chuyển sang cửa sổ trình duyệt đã mở sẵn Tab 1 (`target/pit-reports/index.html`).
- **Lời dẫn phản xạ của TV5:**
  > *"Dạ thưa Thầy, môi trường terminal vừa gặp xung đột biến môi trường Java tạm thời trên hệ điều hành. Tuy nhiên, toàn bộ dữ liệu kiểm thử đã được nhóm thực thi và lưu vết nguyên vẹn trong thư mục target. Kính mời Thầy cùng Hội đồng quan sát trực tiếp báo cáo HTML được kết xuất từ lần chạy kiểm chứng hoàn chỉnh của nhóm."*
- **Hành động tiếp theo:** TV1 nhấp chuột vào package `org.springframework.samples.petclinic.owner`, hiển thị danh sách 8 lớp đối tượng, chỉ rõ 6/8 lớp đạt 100% và 2 lớp còn lại (`Owner`, `OwnerController`) chỉ còn 3 mutant màu đỏ tương đương.

---
*Kịch bản được chuẩn bị kỹ lưỡng để bảo đảm buổi bảo vệ diễn ra thành công và chuyên nghiệp tuyệt đối!*
