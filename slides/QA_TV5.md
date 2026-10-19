# TÀI LIỆU PHẢN XẠ NHANH HỎI ĐÁP BẢO VỆ (DEFENSE Q&A) — THÀNH VIÊN 5
**Học phần:** Kiểm thử phần mềm — Khoa Công nghệ Thông tin, Trường Đại học Đà Lạt  
**Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm  
**Người thực hiện:** Thành viên 5 (Metrics, RCA & Quality Analyst) — Nhóm 20 (Program_R01-K03)  
**Tập trung chuyên môn:** Chỉ số kiểm thử (Metrics), Nguyên nhân cốt lõi (RCA), Khiếm khuyết mã nguồn (Code Smell) và Chứng minh Đột biến tương đương (Equivalent Mutants).

---

## MỤC LỤC 15 CÂU HỎI PHẢN BIỆN HỘI ĐỒNG

1. [Câu 1: Mutation Score khác gì so với Code Coverage? Vì sao 97% Line Coverage mà Mutation Score chỉ đạt 67%?](#câu-1-mutation-score-khác-gì-so-với-code-coverage-vì-sao-97-line-coverage-mà-mutation-score-chỉ-đạt-67)
2. [Câu 2: Equivalent Mutant là gì? Vì sao không thể tiêu diệt được bằng bất kỳ test case nào?](#câu-2-equivalent-mutant-là-gì-vì-sao-không-thể-tiêu-diệt-được-bằng-bất-kỳ-test-case-nào)
3. [Câu 3: Làm thế nào chứng minh 3 mutants còn sống sót là Equivalent mà không phải do test suite còn yếu?](#câu-3-làm-thế-nào-chứng-minh-3-mutants-còn-sống-sót-là-equivalent-mà-không-phải-do-test-suite-còn-yếu)
4. [Câu 4: Vì sao nhóm chọn nhóm toán tử STRONGER mà không dùng DEFAULTS của PIT? STRONGER gồm những gì?](#câu-4-vì-sao-nhóm-chọn-nhóm-toán-tử-stronger-mà-không-dùng-defaults-của-pit-stronger-gồm-những-gì)
5. [Câu 5: Vì sao chọn ngưỡng Quality Gate là 88% mà không phải 80% hay 95%?](#câu-5-vì-sao-chọn-ngưỡng-quality-gate-là-88-mà-không-phải-80-hay-95)
6. [Câu 6: Có thể nâng ngưỡng Quality Gate lên 100% được không? Cần điều kiện gì?](#câu-6-có-thể-nâng-ngưỡng-quality-gate-lên-100-được-không-cần-điều-kiện-gì)
7. [Câu 7: Viết thêm nhiều test (từ 49 lên 130 tests) có chắc chắn chứng minh phần mềm không còn lỗi?](#câu-7-viết-thêm-nhiều-test-từ-49-lên-130-tests-có-chắc-chắn-chứng-minh-phần-mềm-không-còn-lỗi)
8. [Câu 8: Nếu mã nguồn sản phẩm (`src/main/java`) thay đổi (Code Drift), bộ test và kết quả Mutation Testing sẽ bị ảnh hưởng thế nào?](#câu-8-nếu-mã-nguồn-sản-phẩm-srcmainjava-thay-đổi-code-drift-bộ-test-và-kết-quả-mutation-testing-sẽ-bị-ảnh-hưởng-thế-nào)
9. [Câu 9: Điểm yếu và rào cản lớn nhất của Mutation Testing trong công nghiệp là gì? Nhóm đã khắc phục thế nào?](#câu-9-điểm-yếu-và-rào-cản-lớn-nhất-của-mutation-testing-trong-công-nghiệp-là-gì-nhóm-đã-khắc-phục-thế-nào)
10. [Câu 10: "Điểm mù" của Spring MockMvc là gì? Tại sao phải dùng POJO Unit Test kết hợp ArgumentCaptor?](#câu-10-điểm-mù-của-spring-mockmvc-là-gì-tại-sao-phải-dùng-pojo-unit-test-kết-hợp-argumentcaptor)
11. [Câu 11: Sự khác biệt bản chất giữa Weak Mutation Testing và Strong Mutation Testing? PIT thuộc loại nào?](#câu-11-sự-khác-biệt-bản-chất-giữa-weak-mutation-testing-và-strong-mutation-testing-pit-thuộc-loại-nào)
12. [Câu 12: Tại sao nhóm không sửa mã nguồn sản phẩm để loại bỏ dead-store dòng 167 hay đơn giản hóa dòng 108?](#câu-12-tại-sao-nhóm-không-sửa-mã-nguồn-sản-phẩm-để-loại-bỏ-dead-store-dòng-167-hay-đơn-giản-hóa-dòng-108)
13. [Câu 13: Chỉ số Test Strength 98.46% khác gì với Mutation Score 98.46% và Adjusted Score 100.00%?](#câu-13-chỉ-số-test-strength-9846-khác-gì-với-mutation-score-9846-và-adjusted-score-10000)
14. [Câu 14: Những hạn chế và giả định khoa học trung thực trong báo cáo của nhóm là gì?](#câu-14-những-hạn-chế-và-giả-định-khoa-học-trung-thực-trong-báo-cáo-của-nhóm-là-gì)
15. [Câu 15: Nếu được tiếp tục phát triển đề tài, nhóm sẽ mở rộng những hướng nghiên cứu nào?](#câu-15-nếu-được-tiếp-tục-phát-triển-đề-tài-nhóm-sẽ-mở-rộng-những-hướng-nghiên-cứu-nào)

---

## NỘI DUNG CHI TIẾT CÂU HỎI VÀ ĐÁP ÁN PHẢN XẠ NHANH

### Câu 1: Mutation Score khác gì so với Code Coverage? Vì sao 97% Line Coverage mà Mutation Score chỉ đạt 67%?
- **Thời lượng trả lời:** 40 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, sự khác biệt bản chất nằm ở mô hình chuyển hóa lỗi IEEE và chuỗi RIP:*  
  > *1. **Line Coverage** chỉ đo lường điều kiện đầu tiên là **Reachability** — tức lệnh có được CPU nạp và chạy qua hay không (**Execution Coverage**). Nó hoàn toàn bỏ qua việc lệnh chạy xong có làm sai lệch trạng thái (**Infection**) và sai lệch đó có lan truyền ra ngõ ra để Assertion kiểm tra (**Propagation**) hay không.*  
  > *2. **Mutation Testing** đo lường năng lực phát hiện lỗi (**Fault Detection Power**). Một bài test có thể chạy qua 100% dòng lệnh nhưng không có lệnh `assert` nào (Assertion-free Test) thì Line Coverage vẫn báo 100%, nhưng Mutation Score sẽ là 0%.*  
  > *Tại Spring PetClinic Baseline, 96.80% dòng lệnh được chạy qua nhưng có tới 64 mutants sống sót vì các bài test cũ chỉ assert mã HTTP 200 mà không assert trạng thái dữ liệu lưu trữ, hoặc dùng giá trị test nằm xa biên so sánh."*

---

### Câu 2: Equivalent Mutant là gì? Vì sao không thể tiêu diệt được bằng bất kỳ test case nào?
- **Thời lượng trả lời:** 30 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, theo định nghĩa toán học, một mutant $M$ được gọi là Đột biến tương đương (Equivalent Mutant) với chương trình gốc $P$ khi và chỉ khi: Với mọi dữ liệu đầu vào $I$ thuộc miền xác định, hành vi và kết quả của $M$ luôn trùng khớp hoàn toàn với $P$:*  
  > $$\forall I \in \mathcal{D}, \quad P(I) = M(I)$$  
  > *Vì đầu ra và tác dụng phụ của chương trình bị đột biến không hề khác biệt so với chương trình gốc, nên về mặt lý thuyết thông tin, không thể tồn tại bất kỳ test case nào có thể làm bài test FAIL để tiêu diệt mutant. Việc cố gắng viết test để diệt equivalent mutant là bất khả thi."*

---

### Câu 3: Làm thế nào chứng minh 3 mutants còn sống sót là Equivalent mà không phải do test suite còn yếu?
- **Thời lượng trả lời:** 45 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, nhóm đã sử dụng hai phương pháp chứng minh hình thức độc lập:*  
  > *1. **Với 2 mutant tại `Owner.java:108`:** Nhóm quy đổi biểu thức logic sang đại số Boolean. Vì $isNew() \iff id == null$, khi hai đối tượng có ID khác null thì mệnh đề phụ thuộc hoàn toàn vào $Objects.equals(id_1, id_2)$. Nhóm lập bảng chân trị trên toàn bộ 5 lớp tương đương và chạy script Python `verify_equivalence.py` vét cạn 9/9 tổ hợp, xác nhận 100% kết quả của mutant trùng khớp với code gốc.*  
  > *2. **Với mutant tại `OwnerController.java:167`:** Phân tích đồ thị luồng điều khiển (CFG) chứng minh khối guard dòng 161 đã chặn và chuyển hướng mọi trường hợp $owner.getId() \ne ownerId$. Do đó, tại dòng 167, giá trị ID đã chắc chắn bằng $ownerId$, lệnh gán lại `owner.setId(ownerId)` là một dead-store thuần túy. Xóa nó đi không làm thay đổi trạng thái lưu trữ CSDL."*

---

### Câu 4: Vì sao nhóm chọn nhóm toán tử STRONGER mà không dùng DEFAULTS của PIT? STRONGER gồm những gì?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, nhóm chọn `STRONGER` vì đây là yêu cầu khắt khe của syllabus K03 nhằm đánh giá toàn diện chất lượng kiểm thử:*  
  > *- Nhóm `DEFAULTS` chỉ có 7 toán tử cơ bản, bỏ sót các biến đổi số học và điều kiện biên phức tạp.*  
  > *- Nhóm `STRONGER` kích hoạt toàn bộ 11 toán tử cao cấp nhất của PIT: bao gồm `ConditionalsBoundaryMutator` (thay đổi quan hệ so sánh biên), `MathMutator` (đổi toán tử cộng trừ), `VoidMethodCallMutator` (xóa lệnh void), `RemoveConditionalMutator` (ép nhánh true/false), cùng các mutator ép giá trị trả về rỗng, null, true, false.*  
  > *Việc vượt qua nhóm `STRONGER` chứng minh bộ kiểm thử của nhóm có khả năng bảo vệ phần mềm trước những sai sót cú pháp tinh vi nhất."*

---

### Câu 5: Vì sao chọn ngưỡng Quality Gate là 88% mà không phải 80% hay 95%?
- **Thời lượng trả lời:** 30 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, con số 88% được nhóm thiết lập dựa trên 2 cơ sở:*  
  > *1. **Đặc tả yêu cầu của đề tài:** Giáo trình và đề cương học phần Kiểm thử phần mềm (GVHD: ThS. Nguyễn Thế Lâm) quy định rõ ngưỡng sàn nghiệm thu cho kỹ thuật K03 là **Mutation Coverage $\ge 88\%$**.*  
  > *2. **Cơ sở khoa học thực nghiệm:** Trong các dự án thực tế, mã nguồn luôn tồn tại một tỷ lệ đột biến tương đương (khoảng 1.5% đến 5%). Ngưỡng 88% là mức chất lượng tiêu chuẩn quốc tế (thường dao động 80–85%), vừa đảm bảo loại trừ triệt để các bài test hời hợt, vừa thực tế với chi phí công sức của đội ngũ kỹ thuật. Nhóm đã vượt ngưỡng này, đạt **98.46%**."*

---

### Câu 6: Có thể nâng ngưỡng Quality Gate lên 100% được không? Cần điều kiện gì?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, trên công cụ PIT tự động, **không thể thiết lập ngưỡng 100%** đối với mã nguồn Spring PetClinic hiện tại, vì PIT chỉ tính điểm thô (Raw Score) và không có khả năng tự động nhận biết Đột biến tương đương. Điểm tối đa trên mã nguồn gốc mà PIT có thể ghi nhận là $192 / 195 = \mathbf{98.46\%}$.*  
  > *Để có thể nâng cổng chất lượng tự động lên 100%, bắt buộc phải thỏa mãn 1 trong 2 điều kiện:*  
  > *1. Cấu hình cờ loại trừ đột biến tương đương (PIT Exclusion filters) hoặc sử dụng annotation `@MutantIgnore`.*  
  > *2. Tái cấu trúc mã nguồn sản phẩm (Refactoring) để xóa bỏ lệnh dead-store dòng 167 và đơn giản hóa điều kiện dòng 108. Khi đó tổng số mutant giảm xuống 192 và PIT sẽ báo 100%."*

---

### Câu 7: Viết thêm nhiều test (từ 49 lên 130 tests) có chắc chắn chứng minh phần mềm không còn lỗi?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, câu trả lời là **KHÔNG**. Theo định lý kinh điển của Edsger W. Dijkstra: 'Kiểm thử phần mềm chỉ có thể chứng minh sự hiện diện của lỗi, chứ không thể chứng minh sự vắng mặt của lỗi'.*  
  > *Tuy nhiên, việc tăng từ 49 lên 130 tests và nâng Mutation Score từ 67% lên 98.46% mang lại giá trị to lớn:*  
  > *- Nó chứng minh rằng bộ kiểm thử có **năng lực cảnh báo cực kỳ nhạy bén** trước các biến đổi cú pháp giả lập.*  
  > *- Dựa trên 'Giả thuyết lập trình viên có năng lực' và 'Hiệu ứng khớp lệnh', một bộ test diệt được 98.46% các lỗi đột biến đơn lẻ thì cũng sẽ phát hiện được phần lớn các lỗi phức tạp kết hợp trong thực tế."*

---

### Câu 8: Nếu mã nguồn sản phẩm (`src/main/java`) thay đổi (Code Drift), bộ test và kết quả Mutation Testing sẽ bị ảnh hưởng thế nào?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, khi mã nguồn sản phẩm thay đổi:*  
  > *1. Số lượng bytecode instructions thay đổi, dẫn đến PIT sẽ sinh ra một tập hợp mutants hoàn toàn mới.*  
  > *2. Nếu logic thay đổi làm phá vỡ các giả định kiểm thử cũ, các bài test có thể bị Fail (hồi quy logic).*  
  > *3. Nếu thêm logic mới mà không viết test bổ sung, Mutation Score sẽ tụt ngay lập tức.*  
  > *Chính vì vậy, nhóm đã tích hợp kiểm tra tự động trên **GitHub Actions CI/CD pipeline**. Mỗi khi có mã mới được đẩy lên, CI sẽ tự động chạy PIT và so khớp với Quality Gate 88%. Nếu điểm số bị tụt dưới 88%, pipeline sẽ báo đỏ và chặn không cho merge mã nguồn."*

---

### Câu 9: Điểm yếu và rào cản lớn nhất của Mutation Testing trong công nghiệp là gì? Nhóm đã khắc phục thế nào?
- **Thời lượng trả lời:** 40 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, rào cản lớn nhất của Mutation Testing là **chi phí tính toán và thời gian thực thi khổng lồ** (Execution Cost), do công cụ phải biên dịch và chạy lại bộ test hàng trăm, hàng nghìn lần cho từng mutant.*  
  > *Nhóm đã khắc phục bài toán này bằng 3 giải pháp công nghệ:*  
  > *1. **Giới hạn phạm vi nghiêm ngặt:** Chỉ đột biến trên gói nghiệp vụ cốt lõi `owner.*` (giảm thời gian chạy từ 30 phút xuống ~35 giây).*  
  > *2. **Tối ưu hóa bộ test:** Viết các unit test thuần POJO, deterministic, mock các phụ thuộc bên ngoài để thời gian chạy mỗi test chỉ vài mili-giây.*  
  > *3. **Chiến lược Fail-Fast trên CI/CD:** Chạy fast unit tests trước; chỉ khi 153 unit test đều pass mới kích hoạt pha Mutation Testing."*

---

### Câu 10: "Điểm mù" của Spring MockMvc là gì? Tại sao phải dùng POJO Unit Test kết hợp ArgumentCaptor?
- **Thời lượng trả lời:** 45 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, điểm mù lớn của `MockMvc` là cơ chế **Model Binding Aliasing**:*  
  > *- Trong controller, khi nhận request POST, `WebDataBinder` tự động tìm nạp đối tượng từ DB và gán tham số form trực tiếp lên chính thực thể đó trong bộ nhớ Heap.*  
  > *- Khi đó, các dòng lệnh copy thủ công trong controller như `existingPet.setName(pet.getName())` trở thành thao tác gán trùng lặp (`x = x`). Khi PIT xóa các dòng này, test MockMvc vẫn Pass vì dữ liệu đã nằm sẵn trong entity!*  
  > *- Giải pháp của nhóm là viết POJO Unit Test độc lập: Khởi tạo controller trực tiếp bằng `new`, truyền 2 instance hoàn toàn tách rời: `managed` (dữ liệu cũ) và `detached` (dữ liệu mới). Khi đó controller bắt buộc phải chạy lệnh copy, và nhóm dùng `ArgumentCaptor` bắt thực thể tại lệnh `saveAndFlush` để assert dữ liệu mới. Nhờ đó, toàn bộ mutant bị diệt triệt để."*

---

### Câu 11: Sự khác biệt bản chất giữa Weak Mutation Testing và Strong Mutation Testing? PIT thuộc loại nào?
- **Thời lượng trả lời:** 30 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy:*  
  > *- **Weak Mutation Testing (Đột biến yếu):** Chỉ yêu cầu thỏa mãn 2 điều kiện đầu của mô hình RIP là Reachability và Infection. Ngay sau khi lệnh đột biến chạy xong, hệ thống kiểm tra trạng thái bộ nhớ nội bộ. Nếu có khác biệt, mutant coi như đã bị diệt, bất kể lỗi có lan truyền ra ngoài hay không.*  
  > *- **Strong Mutation Testing (Đột biến mạnh):** Bắt buộc phải thỏa mãn trọn vẹn cả 3 điều kiện: Reachability, Infection, và **Propagation**. Toàn bộ test case phải chạy đến cùng và mutant chỉ bị diệt khi có ít nhất một bài test chính thức văng ngoại lệ hoặc Assertion Error.*  
  > *PIT là công cụ triển khai **Strong Mutation Testing**, bảo đảm tính chặt chẽ học thuật cao nhất."*

---

### Câu 12: Tại sao nhóm không sửa mã nguồn sản phẩm để loại bỏ dead-store dòng 167 hay đơn giản hóa dòng 108?
- **Thời lượng trả lời:** 30 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, nhóm không sửa mã nguồn sản phẩm vì tuân thủ nghiêm ngặt **Ràng buộc bất biến cốt lõi của đề tài**: 'Đóng băng hoàn toàn mã nguồn `src/main/java`'.*  
  > *Trong kiểm thử phần mềm chuyên nghiệp, nhiệm vụ của đội ngũ QA/Testing là đánh giá và bảo vệ hệ thống hiện hữu chứ không tự ý sửa đổi logic sản xuất để làm đẹp chỉ số. Mọi cải tiến chất lượng phải đến từ năng lực của bộ kiểm thử trong `src/test/java` và cấu hình build. Toàn bộ các phát hiện về dead-store hay biểu thức dư thừa đều được nhóm ghi nhận trung thực thành Báo cáo Code Smells (Mục G.2) và khuyến nghị tái cấu trúc."*

---

### Câu 13: Chỉ số Test Strength 98.46% khác gì với Mutation Score 98.46% và Adjusted Score 100.00%?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, ba chỉ số này có công thức tính và ý nghĩa khoa học khác nhau:*  
  > *1. **Mutation Score (Điểm đột biến thô):** $\frac{\text{Killed}}{\text{Total}} = \frac{192}{195} = \mathbf{98.46\%}$.*  
  > *2. **Test Strength (Năng lực kiểm thử):** $\frac{\text{Killed}}{\text{Covered}} = \frac{\text{Killed}}{\text{Total} - \text{No\_Coverage}}$. Tại Baseline, Test Strength là 70.43% (131/186) vì có 9 mutants không có test che phủ. Tại Final, do độ bao phủ dòng đạt 100% nên No Coverage bằng 0, kéo theo Test Strength bằng đúng Mutation Score là 98.46%.*  
  > *3. **Adjusted Score (Điểm số hiệu chỉnh):** $\frac{\text{Killed}}{\text{Total} - \text{Equivalent}} = \frac{192}{195 - 3} = \frac{192}{192} = \mathbf{100.00\%}$, phản ánh tỷ lệ diệt trên 100% các đột biến có khả năng tiêu diệt trong thực tế."*

---

### Câu 14: Những hạn chế và giả định khoa học trung thực trong báo cáo của nhóm là gì?
- **Thời lượng trả lời:** 35 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, tuân thủ nguyên tắc trung thực khoa học, nhóm đã công bố rõ 3 giả định và hạn chế trong báo cáo Phần G.4.5:*  
  > *1. **Giả định tính bất biến kế thừa:** Giả định lớp `Pet` kế thừa trực tiếp triển khai chuẩn của `BaseEntity` mà không ghi đè logic đặc thù cho phương thức `isNew()` hay `getId()`.*  
  > *2. **Không xét can thiệp Reflection động:** Chứng minh không áp dụng cho trường hợp có mã can thiệp runtime bằng Java Reflection để sửa trường private ID giữa chừng.*  
  > *3. **Thực thi đơn luồng chuẩn:** Chứng minh áp dụng trên luồng HTTP request chuẩn của Spring MVC, không xét các luồng bất đồng bộ chia sẻ trạng thái đối tượng mà không đồng bộ hóa."*

---

### Câu 15: Nếu được tiếp tục phát triển đề tài, nhóm sẽ mở rộng những hướng nghiên cứu nào?
- **Thời lượng trả lời:** 30 giây.
- **Đáp án chuẩn học thuật:**
  > *"Dạ thưa Thầy, nếu tiếp tục phát triển đề tài, nhóm định hướng 3 mở rộng lớn:*  
  > *1. **Tích hợp Mutation Testing cho toàn bộ hệ thống:** Mở rộng phạm vi từ gói `owner` sang các phân hệ `vet`, `system`, và tầng cấu hình bảo mật Spring Security.*  
  > *2. **Tự động hóa phát hiện Equivalent Mutants:** Ứng dụng các công cụ phân tích tĩnh SMT Solvers (như Z3 Theorem Prover) để tự động chứng minh đột biến tương đương mà không cần lập bảng chân trị thủ công.*  
  > *3. **Tối ưu hóa CI/CD bằng Test Impact Analysis (TIA):** Chỉ chạy kiểm thử đột biến trên các dòng mã có thay đổi trong Pull Request để rút ngắn thời gian build xuống dưới 10 giây."*

---
*Tài liệu được biên soạn phục vụ bảo vệ đề tài R01-K03. Người soạn: Thành viên 5 (Hoàng Việt Linh).*
