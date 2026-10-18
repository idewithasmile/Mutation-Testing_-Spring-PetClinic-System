# HƯỚNG DẪN CHỤP ẢNH BÁO CÁO PIT MUTATION TESTING (pit_index.png)

Tài liệu này hướng dẫn Thành viên 5 (Metrics, RCA & Quality Analyst) tự chụp ảnh màn hình báo cáo tổng quan PIT Mutation Testing và lưu vào `reports/figures/pit_index.png` để đưa vào báo cáo nghiệm thu và slide bảo vệ.

---

## 1. Vị trí tệp báo cáo gốc
Báo cáo HTML tổng quan của PIT Mutation Testing được sinh tự động tại:
`target/pit-reports/index.html`

Hoặc đường dẫn tuyệt đối trên máy tính:
`file:///d:/Kiểm Thử Phần Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/target/pit-reports/index.html`

---

## 2. Các bước thực hiện chụp màn hình

1. **Mở tệp `index.html` trên trình duyệt:**
   - Mở trình duyệt web (Google Chrome / Microsoft Edge / Firefox).
   - Nhấn `Ctrl + O` và duyệt đến tệp `target/pit-reports/index.html`.
   - Hoặc dán đường dẫn tệp vào thanh địa chỉ của trình duyệt:
     ```text
     d:/Kiểm Thử Phần Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/target/pit-reports/index.html
     ```

2. **Kiểm tra thông số trên màn hình trước khi chụp:**
   - **Package:** `org.springframework.samples.petclinic.owner`
   - **Number of Classes:** `8`
   - **Line Coverage:** `100% (250/250)`
   - **Mutation Coverage:** `98% (192/195)`
   - **Test Strength:** `98% (192/195)`

3. **Chụp ảnh màn hình:**
   - Sử dụng công cụ Snipping Tool (`Windows + Shift + S`) hoặc tính năng chụp toàn trang của trình duyệt (`Ctrl + Shift + I` > `Ctrl + Shift + P` > gõ `Capture full size screenshot`).
   - Cắt khung hình rõ nét bao gồm tiêu đề "Pit Test Coverage Report", bảng tóm tắt chỉ số và danh sách các lớp trong package `owner`.

4. **Lưu tệp ảnh:**
   - Đặt tên tệp chính xác là: `pit_index.png`
   - Lưu vào thư mục:
     `d:/Kiểm Thử Phần Mềm/Nhom_20/Mutation-Testing_-Spring-PetClinic-System/reports/figures/pit_index.png`
   - Định dạng ảnh: PNG, khuyến nghị độ phân giải rõ nét (tối thiểu 1280x720 hoặc 1920x1080).

---

> [!NOTE]
> Tuân thủ Ràng buộc bất biến số 3: Trợ lý AI không tự tạo ảnh giả mạo. Ảnh chụp thực tế từ trình duyệt sẽ đảm bảo 100% tính xác thực học thuật khi nộp báo cáo cho Giảng viên hướng dẫn.
