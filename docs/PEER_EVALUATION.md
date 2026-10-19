# BẢNG ĐÁNH GIÁ ĐÓNG GÓP THÀNH VIÊN (PEER EVALUATION)
**Học phần:** Kiểm thử phần mềm — Khoa Công nghệ Thông tin, Trường Đại học Đà Lạt  
**Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm  
**Đề tài:** Mutation Testing bằng PIT trên Spring PetClinic (K03 – Program_R01)  
**Nhóm thực hiện:** Nhóm 20 (Program_R01-K03)  
**Thời điểm lập:** 19/10/2026 (Phiên S8 — Tổng duyệt & Đánh giá nội bộ)  

---

## 1. MỤC ĐÍCH VÀ NGUYÊN TẮC ĐÁNH GIÁ

1. **Nguyên tắc dựa trên bằng chứng thực nghiệm (Evidence-Based):** Mọi điểm số và đánh giá bắt buộc phải quy chiếu trực tiếp từ các dữ liệu khách quan đo lường được:
   - Số lượng commit được ghi nhận trong lịch sử Git (`git shortlog -sn 500158f..HEAD`).
   - Khối lượng và chất lượng ca kiểm thử đóng góp (số lượng test method `@Test`, độ phức tạp kỹ thuật).
   - Khối lượng mã nguồn CI/CD, script tự động hóa, biểu đồ phân tích và chứng minh toán học.
   - Các chương mục cụ thể trong Báo cáo tổng thể [`REPORT_R01_K03.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/REPORT_R01_K03.md).
   - Sản phẩm phục vụ bảo vệ đề tài: Bài giảng PowerPoint, kịch bản Live Demo, tài liệu Q&A.
2. **Nguyên tắc dân chủ và minh bạch:**
   - Tài liệu này liệt kê đầy đủ **Dữ liệu thô (Raw Evidence)** và **Công thức tính điểm trọng số chuẩn**.
   - Cột *"Điểm tự chấm"*, *"Điểm nhóm thống nhất"*, và *"Xác nhận (Chữ ký)"* được **để trống** để toàn thể 5 thành viên nhóm họp bàn, thảo luận và đồng thuận ký xác nhận trước khi nộp chính thức lên Giảng viên hướng dẫn.

---

## 2. KHUNG TIÊU CHÍ VÀ TRỌNG SỐ ĐÁNH GIÁ (4 TIÊU CHÍ: 40 / 30 / 15 / 15)

Khung tiêu chí đánh giá được thiết lập theo đúng Đề cương chi tiết học phần và Kế hoạch thực hiện đề tài K03:

| Mã tiêu chí | Tên tiêu chí đánh giá | Trọng số ($W_i$) | Thang điểm | Mô tả nội dung và bằng chứng kiểm chứng |
| :---: | :--- | :---: | :---: | :--- |
| **TC1** | **Khối lượng công việc & Kết quả bàn giao** | **40%** ($0.40$) | 0.0 – 10.0 | Hoàn thành đầy đủ các đầu việc được phân công: số lượng unit test (@Test) mới đóng góp, cấu hình Maven/PIT, thiết lập CI/CD, phân tích dữ liệu, xuất bản báo cáo & slide. |
| **TC2** | **Chất lượng kỹ thuật & Đóng góp báo cáo** | **30%** ($0.30$) | 0.0 – 10.0 | Độ sâu học thuật và tính chính xác kỹ thuật: BVA, Decision Table, CFG/McCabe, Detached Entity, Boolean proof, chuẩn IEEE 1044/610.12, chất lượng văn phong các chương báo cáo phụ trách. |
| **TC3** | **Kỷ luật tiến độ & Đóng góp Git** | **15%** ($0.15$) | 0.0 – 10.0 | Tuân thủ tiến độ qua các Session (S0 $\to$ S8), số lượng commit Git (`git shortlog`), chất lượng commit message, tuân thủ kỷ luật nhánh, không làm vỡ build (`BUILD SUCCESS`). |
| **TC4** | **Chuẩn bị bảo vệ đề tài (Slide, Demo, Q&A)** | **15%** ($0.15$) | 0.0 – 10.0 | Chuẩn bị nội dung slide thuyết trình (12 slides), speaker notes, phối hợp kịch bản Live Demo (35–45s) và cẩm nang phản xạ nhanh 15 câu hỏi phản biện Hội đồng. |

### Công thức tính điểm tổng hợp:
$$\text{Điểm Tổng} = (\text{TC1} \times 0.40) + (\text{TC2} \times 0.30) + (\text{TC3} \times 0.15) + (\text{TC4} \times 0.15)$$

### Thang xếp loại học phần:
- **Loại A (Xuất sắc):** $9.0 \le \text{Điểm Tổng} \le 10.0$
- **Loại B (Giỏi / Khá):** $7.0 \le \text{Điểm Tổng} \le 8.9$
- **Loại C (Trung bình):** $5.0 \le \text{Điểm Tổng} \le 6.9$
- **Loại D (Yếu / Không đạt):** $\text{Điểm Tổng} < 5.0$

---

## 3. BẢNG DỮ LIỆU THÔ (RAW EVIDENCE) CỦA 5 THÀNH VIÊN

Nguồn đối chiếu: [`logs/git_history.log`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/logs/git_history.log), [`REPORT_R01_K03.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/REPORT_R01_K03.md), [`slides/SLIDES_CONTENT.md`](file:///d:/Kiểm%20Thử%20Phần%20Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/slides/SLIDES_CONTENT.md), và báo cáo kết quả kiểm thử PIT.

| STT | Thành viên nhóm | Vai trò chính | Commits Git (500158f..HEAD) | Ca kiểm thử (@Test) / Artifacts phụ trách | Chương báo cáo phụ trách | Vai trò trong Buổi bảo vệ |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- |
| **1** | **Trịnh Trung Hiếu**<br>(MSSV: 2312618) | QA Lead & DevSecOps | **37 commits**<br>(Hubert Trinh: 28,<br>2312618 Trinh Trung Hieu: 9) | • Nâng cấp PIT 1.30.0 + JUnit 5 plugin 1.2.3.<br>• Mutator STRONGER & Quality Gate 88%.<br>• CI/CD GitHub Actions 6 bước fail-fast.<br>• Điều hành kịch bản live demo 1-lệnh. | • **Phần A:** Tổng quan đề tài & Phân công nhiệm vụ.<br>• **Phần D:** Đường ống CI/CD & Khả năng tái hiện 1-lệnh. | • Mở đầu (Slide 1 — 60s).<br>• Lý thuyết RIP & IEEE (Slide 3 — 75s).<br>• JUnit 6 & Quality Gate (Slide 4 — 75s).<br>• CI/CD (Slide 10 — 75s).<br>• Live Demo terminal (35s). |
| **2** | **Trần Đình Việt Huy**<br>(MSSV: 2312619) | System Architect & Test Lead | **11 commits**<br>(Bơ: 7,<br>idewithasmile: 4) | • Khóa cứng Pinned Commit SHA 500158f.<br>• Phân tích kiến trúc 8 lớp gói `owner.*`.<br>• Kiểm chứng HTTP 200 cho 3 luồng nghiệp vụ trên runtime cổng 8090.<br>• Điều phối kiến trúc test (153 tests pass). | • **Phần B:** Bài toán nghiệp vụ & 3 Luồng nghiệp vụ cốt lõi.<br>• **Phần C:** Cơ sở lý thuyết Kiểm thử đột biến & PIT. | • Nghiệp vụ & Phạm vi SUT (Slide 2 — 90s).<br>• Hỗ trợ giải đáp kiến trúc trong phiên Q&A. |
| **3** | **Trần Minh Tài**<br>(MSSV: 2312794) | Domain & Black-Box Test Engineer | **5 commits**<br>(minhtai05: 5) | • Thiết kế & thực thi **45 ca test hộp đen**:<br>  - `OwnerMutationTests`: 27 tests<br>  - `PetValidatorMutationTests`: 9 tests<br>  - `PetVisitModelMutationTests`: 9 tests<br>• BVA biên 30/31 ký tự diệt `ConditionalsBoundary`.<br>• Bảng quyết định 8 quy tắc cho Owner/Pet. | • **Phần E:** Thiết kế Kiểm thử Hộp đen Domain & Validator (BVA 2-point, Bảng quyết định 2 chiều, Deep Assert). | • Thiết kế Kiểm thử Hộp đen (Slide 5 — 90s).<br>• Trả lời các câu hỏi phản biện về BVA và Bảng quyết định. |
| **4** | **Trương Bảo Bảo**<br>(MSSV: 2312582) | White-Box & Controller Test Engineer | **5 commits**<br>(Truong Bao Bao: 5) | • Thiết kế & thực thi **36 ca test hộp trắng**:<br>  - `PetControllerMutationTests`: 19 tests<br>  - `VisitControllerMutationTests`: 6 tests<br>  - `OwnerControllerMutationTests`: 6 tests<br>  - `ControllerBinderMutationTests`: 5 tests<br>• Đồ thị luồng CFG, McCabe $V(G)=3$ (3 đường BP).<br>• Kỹ thuật Detached Entity + ArgumentCaptor. | • **Phần F:** Thiết kế Kiểm thử Hộp trắng Web Controller (Đồ thị luồng CFG, Độc lập đường cơ sở McCabe, Tử huyệt Model Aliasing). | • Thiết kế Kiểm thử Hộp trắng (Slide 6 — 120s).<br>• Trả lời các câu hỏi phản biện về MockMvc và Detached Entity. |
| **5** | **Hoàng Việt Linh**<br>(MSSV: 2312664) | Metrics, RCA & Quality Analyst | **6 commits**<br>(VietLinh: 6) | • Đối soát chỉ số: 67% $\to$ 98.46%, Line 100%.<br>• 4 Biểu đồ học thuật G.1–G.4 (200 DPI).<br>• RCA chuẩn IEEE 1044 cho 64 survivors & 6 Code Smells.<br>• Chứng minh hình thức 3 Equivalent Mutants (Bảng chân trị 5 lớp) $\to$ Adjusted Score 100%.<br>• Biên tập báo cáo A$\to$H (DOCX/PDF/HTML).<br>• Biên soạn Slide PPTX 12 trang, Q&A 15 câu. | • **Phần G:** Báo cáo Phân tích Định lượng (Log/Metrics, Code Smells, RCA IEEE 1044, Chứng minh Đột biến tương đương).<br>• Tổng hợp Bìa, Mục lục, Danh mục Bảng/Hình, Tài liệu tham khảo, Slide thuyết trình. | • "Ảo giác an toàn" 97% vs 67% (Slide 7 — 65s).<br>• RCA 64 survivors & Code Smells (Slide 8 — 75s).<br>• Chứng minh 3 Equivalent Mutants (Slide 9 — 70s).<br>• Tổng kết Baseline vs Final (Slide 11 — 60s).<br>• Thuyết minh Live Demo trực tiếp (35s). |

---

## 4. BẢNG TỔNG HỢP ĐÁNH GIÁ ĐÓNG GÓP (DÀNH CHO BUỔI HỌP NHÓM)

> **Hướng dẫn sử dụng bảng:**  
> - Các cột **TC1, TC2, TC3, TC4** và **Điểm Tổng** được chấm theo thang điểm 10 với trọng số tương ứng:  
>   $$\text{Điểm Tổng} = \text{TC1} \times 0.40 + \text{TC2} \times 0.30 + \text{TC3} \times 0.15 + \text{TC4} \times 0.15$$  
> - Các thành viên đối chiếu với **Bảng Dữ liệu thô** ở Mục 3 để tự cho điểm và thống nhất điểm nhóm.  
> - Ký tên vào cột **Xác nhận (Chữ ký)** sau khi đạt được sự đồng thuận 100%.

| STT | Họ và tên thành viên | Mã số sinh viên | Vai trò trong nhóm | TC1 (40%) | TC2 (30%) | TC3 (15%) | TC4 (15%) | Điểm tự chấm | Điểm nhóm thống nhất | Xếp loại | Xác nhận (Chữ ký) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Trịnh Trung Hiếu** | 2312618 | QA Lead & DevSecOps | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *(để trống)* |
| **2** | **Trần Đình Việt Huy** | 2312619 | System Architect & Test Lead | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *(để trống)* |
| **3** | **Trần Minh Tài** | 2312794 | Domain & Black-Box Test Engineer | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *(để trống)* |
| **4** | **Trương Bảo Bảo** | 2312582 | White-Box & Controller Test Engineer | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *(để trống)* |
| **5** | **Hoàng Việt Linh** | 2312664 | Metrics, RCA & Quality Analyst | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *[......]* | *(để trống)* |

---

## 5. BẢNG TRÌNH BÀY CHO TỆP WORD (`REPORT_R01_K03.docx`)

Dưới đây là phiên bản bảng rút gọn chuẩn học thuật đã được đồng bộ để chèn trực tiếp vào Phụ lục hoặc Trang đầu của tệp báo cáo chính thức `REPORT_R01_K03.docx`:

### BẢNG ĐÁNH GIÁ ĐÓNG GÓP THÀNH VIÊN VÀ PHÂN CÔNG TRÁCH NHIỆM

| STT | Họ và tên | MSSV | Phân công nhiệm vụ | Sản phẩm & Bằng chứng thực tế | Đóng góp (%) | Chữ ký xác nhận |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| 1 | Trịnh Trung Hiếu | 2312618 | QA Lead & DevSecOps | Cấu hình PIT 1.30.0 / JUnit 5; Mutator STRONGER; Quality Gate 88%; CI/CD GitHub Actions; Live Demo; 37 commits; Báo cáo Phần A, D. | 20% | *(Ký tên)* |
| 2 | Trần Đình Việt Huy | 2312619 | System Architect & Test Lead | Khóa commit 500158f; Xác minh 3 luồng runtime thật (HTTP 200); Quản trị repo (153 tests pass); 11 commits; Báo cáo Phần B, C. | 20% | *(Ký tên)* |
| 3 | Trần Minh Tài | 2312794 | Domain & Black-Box Test Engineer | Thiết kế 45 unit tests Domain & Validator; Kỹ thuật BVA 30/31 ký tự; Bảng quyết định 8 rules; 5 commits; Báo cáo Phần E. | 20% | *(Ký tên)* |
| 4 | Trương Bảo Bảo | 2312582 | White-Box & Controller Test Engineer | Thiết kế 36 unit tests Controller; Đồ thị luồng CFG, McCabe $V(G)=3$; Detached Entity + ArgumentCaptor; 5 commits; Báo cáo Phần F. | 20% | *(Ký tên)* |
| 5 | Hoàng Việt Linh | 2312664 | Metrics, RCA & Quality Analyst | Bảng số liệu đối soát; 4 Biểu đồ G.1–G.4; RCA IEEE 1044 (64 survivors); Chứng minh 3 Equivalent Mutants (100% Adjusted Score); Báo cáo Phần G; Xuất bản DOCX/PDF; Slide PPTX 12 trang; Q&A 15 câu; 6 commits. | 20% | *(Ký tên)* |

---

## 6. BIÊN BẢN HỌP ĐỒNG THUẬN CỦA NHÓM 20

- **Thời gian họp:** Ngày ..... tháng 10 năm 2026.
- **Địa điểm:** Phòng máy / Trực tuyến Google Meet.
- **Thành phần tham dự:** Đủ 5/5 thành viên (Trịnh Trung Hiếu, Trần Đình Việt Huy, Trần Minh Tài, Trương Bảo Bảo, Hoàng Việt Linh).
- **Nội dung cuộc họp:**
  1. Rà soát lại toàn bộ sản phẩm thực tế và dữ liệu Git của từng thành viên.
  2. Tự cho điểm và thảo luận thống nhất điểm số theo 4 tiêu chí 40/30/15/15.
  3. Ký xác nhận biên bản đồng thuận và cam kết chịu trách nhiệm tập thể trước Giảng viên hướng dẫn.
- **Kết luận:** Toàn thể 5 thành viên nhóm 20 nhất trí 100% với bảng đánh giá đóng góp trên, không có khiếu nại hay tranh chấp.

*(Ký và ghi rõ họ tên của 5 thành viên)*
```text
  Trịnh Trung Hiếu        Trần Đình Việt Huy        Trần Minh Tài        Trương Bảo Bảo        Hoàng Việt Linh
```
