#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script xây dựng toàn bộ Presentation Bảo vệ đề tài R01-K03:
1. Xuất bản slides/presentation.html (Slide deck 16:9 full HD 1920x1080 kèm điều hướng phím và speaker notes).
2. Xuất bản 12 trang slides/preview/slide_01.html ... slide_12.html.
3. Dùng Chrome headless chụp ảnh 12 slides (slides/preview/slide_01.png ... slide_12.png).
4. Đóng gói tệp PowerPoint chuẩn OpenXML slides/R01_K03_Defense.pptx (nhúng hình ảnh và speaker notes).
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

WORKSPACE = Path(__file__).resolve().parent.parent
SLIDES_DIR = WORKSPACE / "slides"
PREVIEW_DIR = SLIDES_DIR / "preview"
FIGURES_DIR = WORKSPACE / "reports" / "figures"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# 12 SLIDES DATA DEFINITION
SLIDES_DATA = [
    {
        "id": 1,
        "role": "TV1 (Trịnh Trung Hiếu)",
        "duration": "60s (00:00 - 01:00)",
        "title": "KIỂM THỬ ĐỘT BIẾN (MUTATION TESTING) BẰNG PIT TRÊN SPRING PETCLINIC",
        "subtitle": "Học phần: Kiểm thử phần mềm | Mã đề tài: R01 (Spring PetClinic) + K03 (Mutation Testing)",
        "message": "Nâng cao năng lực bộ kiểm thử từ 67% lên 98.46% Mutation Score và 100% Line Coverage",
        "bullets": [
            "<strong>SUT & Đề tài:</strong> Hệ thống Spring PetClinic trên nền tảng Java 17, Spring Boot 4.1.0, H2 In-Memory.",
            "<strong>Phạm vi K03:</strong> Tập trung toàn diện gói nghiệp vụ cốt lõi <code>org.springframework.samples.petclinic.owner.*</code>.",
            "<strong>Cam kết khoa học:</strong> Đóng băng 100% mã nguồn <code>src/main/java</code>, chỉ nâng cấp tối ưu bộ test.",
            "<strong>Cổng chất lượng (Quality Gate):</strong> Thiết lập ngưỡng chặn tự động <strong>&ge; 88%</strong> trong Maven.",
            "<strong>Kết quả xuất sắc:</strong> Diệt <strong>192/195 mutants (98.46%)</strong>, độ bao phủ dòng đạt <strong>250/250 lines (100.00%)</strong>."
        ],
        "badges": [
            {"label": "Mutation Score", "value": "98.46%", "sub": "192/195 killed", "color": "emerald"},
            {"label": "Line Coverage", "value": "100.00%", "sub": "250/250 lines", "color": "emerald"},
            {"label": "Test Suite", "value": "130 Tests", "sub": "153/153 pass repo", "color": "blue"},
            {"label": "Quality Gate", "value": "PASS (&ge;88%)", "sub": "Adjusted 100%", "color": "gold"}
        ],
        "notes": "Kính thưa Thầy Nguyễn Thế Lâm và toàn thể Hội đồng, hôm nay nhóm 20 xin trân trọng báo cáo kết quả thực hiện đề tài kết hợp R01 và K03: Kiểm thử đột biến bằng PIT trên hệ thống Spring PetClinic. Nhóm chúng em gồm 5 thành viên được phân công chuyên biệt theo đúng quy trình công nghệ phần mềm chuyên nghiệp. Với cam kết khoa học nghiêm ngặt: không sửa đổi bất kỳ dòng mã nguồn sản phẩm nào, nhóm đã tối ưu hóa toàn diện bộ kiểm thử, nâng Mutation Score từ mức ban đầu 67% lên 98.46%, đạt độ bao phủ dòng tuyệt đối 100% và chứng minh 3 đột biến còn lại là tương đương. Sau đây, xin mời bạn Việt Huy bắt đầu với kiến trúc hệ thống SUT."
    },
    {
        "id": 2,
        "role": "TV2 (Trần Đình Việt Huy)",
        "duration": "90s (01:00 - 02:30)",
        "title": "Bài toán nghiệp vụ SUT & Phạm vi đột biến gói owner.*",
        "subtitle": "Khóa cứng commit khả tái và kiểm chứng 3 luồng nghiệp vụ cốt lõi trên runtime thật",
        "message": "Tập trung tối đa tài nguyên vào gói nghiệp vụ phức tạp nhất gồm 8 thực thể & controllers",
        "bullets": [
            "<strong>SUT chuẩn hóa:</strong> Spring PetClinic khóa cứng commit SHA <code>500158f732419217507c7656904b8e6aa1bcc0d6</code>.",
            "<strong>Ngăn xếp công nghệ:</strong> Java 17 LTS, Spring Boot 4.1.0, Spring Data JPA, Thymeleaf, CSDL H2.",
            "<strong>Phạm vi cô lập K03:</strong> Gói <code>owner.*</code> gồm 8 lớp nghiệp vụ trọng yếu (Owner, Pet, Visit, các Controllers).",
            "<strong>03 Luồng nghiệp vụ cốt lõi đã xác minh HTTP 200 trên runtime thật:</strong><br>"
            "&bull; <em>Luồng 1:</em> Tìm kiếm và phân trang chủ nuôi (<code>OwnerController.processFindForm</code>).<br>"
            "&bull; <em>Luồng 2:</em> Thêm mới thú cưng kèm kiểm chuẩn (<code>PetController</code> + <code>PetValidator</code>).<br>"
            "&bull; <em>Luồng 3:</em> Đặt lịch khám và lưu hồ sơ bệnh án thú cưng (<code>VisitController</code>).",
            "<strong>Bảo toàn kiến trúc:</strong> Toàn bộ 153 unit tests của cả repo luôn PASS (zero regression)."
        ],
        "boxes": [
            {"title": "Owner Entity & Lifecycle", "desc": "Quản lý quan hệ 1-N với Pets, phân trang tìm kiếm theo họ, validate số điện thoại và địa chỉ."},
            {"title": "Pet & Custom Validator", "desc": "Kiểm chuẩn độ dài tên thú cưng (&le; 30 ký tự), bắt buộc loại pet và ngày sinh hợp lệ."},
            {"title": "Visit & Medical Records", "desc": "Lưu vết lịch sử khám bệnh, liên kết chặt chẽ Pet-Visit, phục vụ chẩn đoán lâm sàng."}
        ],
        "notes": "Kính thưa Thầy, đối tượng SUT của nhóm là Spring PetClinic, một ứng dụng chuẩn mực trong hệ sinh thái Spring. Để đảm bảo tính khả tái khoa học, nhóm đã khóa cứng commit SHA ngày 29/09/2026. Thay vì chạy đột biến toàn repo gây lãng phí tính toán, nhóm tập trung toàn lực vào gói nghiệp vụ phức tạp nhất là owner.* gồm 8 lớp thực thể, validator và controller. Nhóm đã dựng môi trường thực tế và xác minh thành công cả 3 luồng nghiệp vụ chạy mượt mà trên cổng 8090 với mã HTTP 200. Sau đây xin mời bạn Trung Hiếu trình bày về cơ sở lý thuyết kiểm thử đột biến."
    },
    {
        "id": 3,
        "role": "TV1 (Trịnh Trung Hiếu)",
        "duration": "75s (02:30 - 03:45)",
        "title": "Mô hình lý thuyết IEEE Error – Fault – Failure và Chuỗi RIP",
        "subtitle": "Đo lường năng lực phát hiện khiếm khuyết (Fault Detection Power) trong Bytecode JVM",
        "message": "Chạy qua dòng mã (Line Coverage) không đủ để bắt lỗi — Phải thỏa mãn chuỗi RIP!",
        "bullets": [
            "<strong>Cơ sở lý thuyết:</strong> Giả thuyết lập trình viên có năng lực (CPH) và Hiệu ứng khớp lệnh (Coupling Effect).",
            "<strong>Toán tử đột biến (Mutant):</strong> PIT tiêm lỗi cú pháp giả lập trực tiếp vào Bytecode <code>.class</code>.",
            "<strong>Chuỗi điều kiện chuyển hóa RIP bắt buộc:</strong><br>"
            "&bull; <strong>Reachability (R):</strong> Test case thực thi chạy qua dòng mã chứa mutant (tránh NO_COVERAGE).<br>"
            "&bull; <strong>Infection (I):</strong> Lệnh đột biến làm biến đổi trạng thái nội bộ bộ nhớ JVM (sinh <strong>Error</strong>).<br>"
            "&bull; <strong>Propagation (P):</strong> Trạng thái sai lệch lan truyền ra ngõ ra/kết quả quan sát được (<strong>Failure</strong>).",
            "<strong>Tiêu diệt Mutant (Killed):</strong> Test Assertion bắt được Failure và báo đỏ <strong>FAIL/ERROR</strong>.",
            "<strong>Mutant sống sót (Survived):</strong> Test case yếu hoặc thiếu assert, test vẫn <strong>PASS</strong> (lọt lưới)."
        ],
        "rip_diagram": True,
        "notes": "Kỹ thuật Mutation Testing là phương pháp kiểm thử hộp trắng hướng lỗi khắt khe nhất hiện nay. Khác với kiểm thử thông thường chỉ đo xem code có chạy qua không, PIT vận hành theo chuỗi chuyển hóa chặt chẽ theo chuẩn IEEE: Từ khiếm khuyết nhân tạo tiêm vào bytecode, ca kiểm thử phải thỏa mãn đồng thời 3 điều kiện RIP: Phải chạm tới dòng mã (Reachability), làm thay đổi giá trị trong bộ nhớ (Infection), và sai lệch đó bắt buộc phải lan truyền ra ngõ ra quan sát được (Propagation). Nếu câu lệnh Assertion của bài test nhạy bén, bài test sẽ Fail và mutant được coi là KILLED. Ngược lại, nếu test chỉ assert hời hợt hoặc nuốt lỗi, bài test vẫn xanh và mutant sẽ SURVIVED. Đây chính là thước đo vàng cho chất lượng bộ kiểm thử."
    },
    {
        "id": 4,
        "role": "TV1 (Trịnh Trung Hiếu)",
        "duration": "75s (03:45 - 05:00)",
        "title": "Xử lý xung đột JUnit 6 / PIT 1.30.0 & Cổng chất lượng Quality Gate",
        "subtitle": "Giải quyết dứt điểm crash Minion và thiết lập rào cản chất lượng tự động &ge; 88%",
        "message": "Nâng cấp bộ đôi pitest-maven 1.30.0 + junit5-plugin 1.2.3 và chặn đứng JaCoCo agent",
        "bullets": [
            "<strong>Sự cố JUnit 6:</strong> Spring Boot 4.1.0 kéo theo JUnit Platform 6.0.3 làm sập minion PIT 1.2.1 (<code>UNKNOWN_ERROR</code>).",
            "<strong>Nâng cấp đồng bộ:</strong> Chuyển dịch lên <code>pitest-maven:1.30.0</code> + <code>pitest-junit5-plugin:1.2.3</code> ổn định tuyệt đối.",
            "<strong>Khử xung đột Bytecode:</strong> Thêm cờ <code>-Djacoco.skip=true</code> ngăn JaCoCo Java Agent can thiệp méo mó bytecode.",
            "<strong>Tập toán tử khắt khe STRONGER:</strong> Kích hoạt 11 mutators nâng cao (Boundary, VoidCall, Math, NegateConditionals...).",
            "<strong>Cổng chất lượng tự động (Quality Gate) khóa trong pom.xml:</strong><br>"
            "&bull; <code>&lt;mutationThreshold&gt;88&lt;/mutationThreshold&gt;</code> (Ngưỡng đạt đề tài: &ge; 88%).<br>"
            "&bull; <code>&lt;coverageThreshold&gt;95&lt;/coverageThreshold&gt;</code> (Bảo đảm bao phủ dòng &ge; 95%).<br>"
            "&bull; Tự động đánh trượt tiến trình build (<strong>BUILD FAILURE</strong>) nếu vi phạm bất kỳ ngưỡng nào."
        ],
        "gate_badge": True,
        "notes": "Trong quá trình triển khai, nhóm gặp sự cố kỹ thuật lớn: Spring Boot 4 kéo theo JUnit Platform 6.0.3, khiến phiên bản PIT gợi ý trong syllabus bị crash minion ngay khi khởi động. Em đã nghiên cứu tài liệu kỹ thuật của PIT và nâng cấp lên bộ đôi pitest-maven 1.30.0 và pitest-junit5-plugin 1.2.3, đồng thời vô hiệu hóa JaCoCo agent để tránh xung đột bytecode. Nhóm cũng kích hoạt nhóm mutator STRONGER toàn diện nhất và cài đặt trực tiếp Cổng chất lượng Quality Gate vào pom.xml với ngưỡng 88% đột biến và 95% độ bao phủ. Bất kỳ commit nào làm điểm số tụt dưới 88% đều bị hủy bỏ ngay lập tức. Sau đây, xin mời bạn Minh Tài trình bày về chiến lược kiểm thử hộp đen."
    },
    {
        "id": 5,
        "role": "TV3 (Trần Minh Tài)",
        "duration": "90s (05:00 - 06:30)",
        "title": "Thiết kế kiểm thử Hộp đen: BVA & Bảng quyết định (45 tests)",
        "subtitle": "Vét cạn giá trị biên và tổ hợp điều kiện logic trên Domain Model và Validator",
        "message": "Áp dụng kỹ thuật BVA 2-point và Decision Table 8 quy tắc diệt sạch 100% mutants domain",
        "bullets": [
            "<strong>Phân công TV3:</strong> 45 ca kiểm thử độc lập, tất định trên <code>Owner</code>, <code>Pet</code>, <code>Visit</code>, <code>PetValidator</code>.",
            "<strong>Phân tích giá trị biên BVA (2-point boundary):</strong><br>"
            "&bull; Kiểm chuẩn độ dài tên pet tại ngưỡng biên 30 và 31 ký tự (<code>MAX_NAME_LENGTH = 30</code>).<br>"
            "&bull; Tiêu diệt triệt để <code>ConditionalsBoundaryMutator</code> tại <code>PetValidator:58</code> (đổi <code>&gt;</code> thành <code>&ge;</code>).",
            "<strong>Bảng quyết định (Decision Table 8 rules):</strong><br>"
            "&bull; 8 tổ hợp điều kiện: <code>hasText &amp;&amp; isNew &amp;&amp; getPet() != null</code> trong <code>PetController</code>.<br>"
            "&bull; Bảng quyết định 2 chiều cho <code>Owner.addPet</code>: kiểm tra thực thể mới vs đã lưu và trùng ID.",
            "<strong>Assert nội dung sâu (Deep Assertion):</strong> So khớp chuỗi <code>toString()</code>, xác minh <code>print(null)</code> trả về <code>\"&lt;null&gt;\"</code>.",
            "<strong>Kết quả:</strong> Diệt sạch 100% mutants trên các lớp Domain Model và Validator."
        ],
        "table_summary": [
            {"tech": "BVA Biên 30/31", "target": "PetValidator:58", "mutant": "ConditionalsBoundary", "status": "KILLED (100%)"},
            {"tech": "Decision Table (8 rules)", "target": "PetController logic", "mutant": "NegateConditionals", "status": "KILLED (100%)"},
            {"tech": "Deep Assert toString", "target": "NamedEntity / Base", "mutant": "EmptyObjectReturn", "status": "KILLED (100%)"}
        ],
        "notes": "Kính thưa Thầy, em chịu trách nhiệm thiết kế 45 ca kiểm thử hộp đen tập trung vào tầng Domain và Validator. Điểm yếu lớn của bộ test ban đầu là chỉ test tên pet 31 ký tự mà không test biên 30 ký tự, khiến PIT đổi dấu lớn hơn thành lớn hơn hoặc bằng mà test cũ vẫn Pass. Em đã áp dụng kỹ thuật Phân tích giá trị biên BVA, viết ca test chấp nhận tên đúng 30 ký tự để diệt gọn mutant này. Đồng thời, em xây dựng các Bảng quyết định toàn diện cho hàm addPet và getPet của Owner để vét cạn mọi tổ hợp cờ isNew và ID trùng nhau. Nhờ vậy, toàn bộ 45 test của em đều đạt tính tất định cao và diệt sạch các mutant trên domain model. Tiếp theo, xin mời bạn Bảo Bảo trình bày về kiểm thử hộp trắng tầng Controller."
    },
    {
        "id": 6,
        "role": "TV4 (Trương Bảo Bảo)",
        "duration": "120s (06:30 - 08:30)",
        "title": "Đồ thị luồng điều khiển, McCabe V(G)=3 & Detached Entity (36 tests)",
        "subtitle": "Hóa giải điểm mù Model Aliasing của Spring MockMvc bằng POJO Unit Test và ArgumentCaptor",
        "message": "Phát hiện lỗ hổng Form Binder ghi đè thực thể trong bộ nhớ và giải quyết triệt để",
        "bullets": [
            "<strong>Phân công TV4:</strong> 36 test methods trên <code>OwnerController</code>, <code>PetController</code>, <code>VisitController</code>.",
            "<strong>Giải phẫu Đồ thị luồng phương thức updatePetDetails:</strong><br>"
            "&bull; Cấu trúc: 7 đỉnh, 8 cạnh, 2 điểm quyết định rẽ nhánh &rArr; Độ phức tạp Cyclomatic <strong>V(G) = 3</strong>.<br>"
            "&bull; 3 đường cơ sở McCabe: BP23 (fail-fast ID null), BP24 (update fields đỉnh N4), BP25 (add mới).",
            "<strong>Tử huyệt đỉnh N4 & Điểm mù Spring MockMvc:</strong><br>"
            "&bull; Form DataBinder tự động gán dữ liệu trước khi chạy, biến 3 lệnh copy <code>setName</code>, <code>setBirthDate</code>, <code>setType</code> thành gán dư thừa (<code>x = x</code>). Test cũ vẫn xanh khi PIT xóa 3 dòng này!",
            "<strong>Giải pháp đột phá Detached Entity:</strong><br>"
            "&bull; Tạo POJO unit test, truyền thực thể tách rời (<code>detached</code> mang tên \"Betty\" vs <code>managed</code> mang tên \"petty\").<br>"
            "&bull; Dùng Mockito <code>ArgumentCaptor&lt;Owner&gt;</code> bắt thực thể tại <code>saveAndFlush</code> để assert từng trường &rArr; Diệt 100% mutants!"
        ],
        "cfg_card": True,
        "notes": "Tiếp nối phần TV3, em phụ trách kiểm thử hộp trắng cho 3 Controller. Như Thầy thấy trên đồ thị luồng phương thức updatePetDetails, độ phức tạp McCabe là 3 tương ứng 3 đường cơ sở. Tại đỉnh N4 có 3 lệnh sao chép trường dữ liệu. Điểm mù cực lớn của MockMvc là cơ chế Form Binder đã tự động ghi đè dữ liệu lên chính entity trong bộ nhớ, khiến các lệnh copy này thành gán dư thừa. Khi PIT xóa sạch 3 dòng này, test MockMvc cũ vẫn xanh! Để diệt tận gốc tử huyệt này, em đã đưa test về tầng POJO thuần, truyền một đối tượng detached riêng biệt và dùng Mockito ArgumentCaptor để chặn bắt thực thể tại hàm saveAndFlush. Nếu mutant xóa lệnh gán, dữ liệu cũ giữ nguyên và test sẽ đánh trượt ngay lập tức. Sau đây, xin kính mời bạn Việt Linh trình bày phân tích số liệu RCA và chứng minh đột biến tương đương."
    },
    {
        "id": 7,
        "role": "TV5 (Hoàng Việt Linh)",
        "duration": "65s (08:30 - 09:35)",
        "title": "\"Ảo giác an toàn\": 97% Line Coverage vs. 67% Mutation Score",
        "subtitle": "Vạch trần khoảng trống kiểm thử (Test Gap) 29.62% giữa việc chạy qua lệnh và bắt lỗi",
        "message": "Thực thi dòng mã (Execution) không đồng nghĩa với kiểm tra đúng đắn (Assertion & Propagation)!",
        "bullets": [
            "<strong>Hiện tượng thực nghiệm tại gói owner.* (Hình G.1):</strong><br>"
            "&bull; Bộ test gốc của Spring PetClinic đạt độ bao phủ dòng rất cao: <strong>96.80% (242/250 lines)</strong>.<br>"
            "&bull; Tuy nhiên, điểm Mutation Score ban đầu chỉ đạt khiêm tốn: <strong>67.18% (131/195 killed)</strong>.",
            "<strong>Khoảng trống kiểm thử nguy hiểm (Test Gap):</strong> Chênh lệch lên tới <strong>29.62%</strong>!",
            "<strong>Vạch trần bản chất khoa học:</strong><br>"
            "&bull; Line Coverage chỉ đo lường nạp lệnh vào CPU (<strong>Execution / Reachability</strong>).<br>"
            "&bull; Line Coverage hoàn toàn bỏ qua năng lực của Assertion và sự lan truyền lỗi (<strong>Propagation</strong>).",
            "<strong>Kết quả bứt phá của nhóm:</strong><br>"
            "&bull; Đưa Line Coverage đạt tuyệt đối <strong>100.00% (250/250 lines)</strong>.<br>"
            "&bull; Đưa Mutation Score đạt <strong>98.46% (192/195 killed)</strong>, triệt tiêu hoàn toàn khoảng trống rủi ro!"
        ],
        "image": "fig1_coverage_vs_mutation.png",
        "notes": "Kính thưa Thầy và Hội đồng, tiếp nối phần trình bày của bạn Bảo Bảo, em xin đại diện nhóm phân tích chuyên sâu về chất lượng kiểm thử. Trên màn hình là Hình G.1 — biểu đồ minh chứng cho phát hiện học thuật quan trọng nhất của đề tài: 'Ảo giác an toàn' của độ bao phủ dòng. Khi tiếp nhận mã nguồn gốc của Spring PetClinic, JaCoCo báo cáo một con số rất ấn tượng: 96.80% Line Coverage, chỉ sót đúng 8 dòng mã. Thế nhưng khi tiêm đột biến bằng PIT, điểm số thực tế chỉ đạt 67.18%, để lọt lưới tới 64 mutants nguy hiểm. Khoảng trống kiểm thử lên tới gần 30%! Điều này chứng minh rằng code được thực thi không đồng nghĩa với code được kiểm tra đúng đắn. Nhờ 81 test case bổ sung được thiết kế bài bản, nhóm đã đưa Line Coverage lên tuyệt đối 100% và Mutation Score đạt 98.46%, xóa bỏ hoàn toàn khoảng trống rủi ro này."
    },
    {
        "id": 8,
        "role": "TV5 (Hoàng Việt Linh)",
        "duration": "75s (09:35 - 10:50)",
        "title": "Phân tích nguyên nhân gốc rễ (RCA) 64 Survivors & 6 Code Smells",
        "subtitle": "Chuẩn hóa mô hình IEEE 1044 / IEEE 610.12 và giải mã 6 nhóm nguyên nhân khiếm khuyết",
        "message": "Hơn 64% mutants sống sót xuất phát từ thiếu Bảng quyết định và thiếu verify tương tác void",
        "bullets": [
            "<strong>Chuẩn hóa mô hình RCA:</strong> Áp dụng chuỗi chuyển hóa IEEE 1044 (Human Error &rarr; Fault &rarr; Failure).",
            "<strong>Phân bổ 64 Mutants sống sót ở Baseline vào 6 nhóm nguyên nhân (Bảng G.5, Hình G.3):</strong><br>"
            "&bull; 1. Thiếu Bảng quyết định cho logic phức tạp: <strong>27 mutants (42.19%)</strong>.<br>"
            "&bull; 2. Thiếu verify tương tác hàm void/binder: <strong>14 mutants (21.88%)</strong>.<br>"
            "&bull; 3. Nhánh ngoại lệ & luồng rẽ thiếu độ bao phủ: <strong>9 mutants (14.06%)</strong>.<br>"
            "&bull; 4. Phân tích giá trị biên BVA & tính toán số học: <strong>6 mutants (9.38%)</strong>.<br>"
            "&bull; 5. MockMvc che giấu cập nhật & gán dư thừa: <strong>5 mutants (7.81%)</strong>.<br>"
            "&bull; 6. Thiếu assert nội dung sâu & giá trị trả về: <strong>3 mutants (4.69%)</strong>.",
            "<strong>Phát hiện 6 Code Smells trong PetClinic:</strong> Dead-Store dòng 167, điều kiện dư dòng 108, truy vấn lặp dòng 181... Ghi nhận độc lập mà không can thiệp mã nguồn."
        ],
        "image": "fig3_survivors_by_mutator.png",
        "notes": "Để tìm hiểu vì sao 64 mutant ở Baseline sống sót, em đã thực hiện phân tích nguyên nhân gốc rễ RCA theo chuẩn IEEE 1044 và IEEE 610.12. Kết quả bóc tách cho thấy nguyên nhân lớn nhất chiếm hơn 42% là do bài test cũ thiếu Bảng quyết định, dẫn đến bỏ sót các tổ hợp rẽ nhánh lồng nhau. Nguyên nhân thứ hai chiếm gần 22% là do thiếu lệnh verify kiểm tra các hàm void, đặc biệt là cấu hình bảo mật cấm bind trường ID trong Controller. Bên cạnh việc chỉ ra điểm yếu của test suite, kiểm thử đột biến còn hoạt động như một kính hiển vi vạch trần 6 Code Smells trong mã nguồn PetClinic. Điển hình như lệnh gán dead-store tại OwnerController dòng 167 hay biểu thức điều kiện phòng vệ cực đoan tại Owner dòng 108. Tuân thủ nghiêm ngặt ràng buộc đóng băng mã nguồn sản phẩm, nhóm không sửa code mà chuyển hóa các phát hiện này thành ma trận truy vết và khuyến nghị tái cấu trúc."
    },
    {
        "id": 9,
        "role": "TV5 (Hoàng Việt Linh)",
        "duration": "70s (10:50 - 12:00)",
        "title": "Chứng minh toán học 3 Equivalent Mutants & Điểm hiệu chỉnh 100%",
        "subtitle": "Đại số Boolean, Bảng chân trị 5 lớp tương đương và Đồ thị luồng CFG bất biến",
        "message": "3 mutants sống sót cuối cùng là đột biến tương đương &rArr; Điểm hiệu chỉnh đạt tuyệt đối 100.00%!",
        "bullets": [
            "<strong>Định nghĩa toán học:</strong> &forall; I &isin; D, P(I) &equiv; M(I) &rArr; Bất khả tiêu diệt bởi bất kỳ ca test nào!",
            "<strong>Mutant M1 &amp; M2 (<code>Owner.java:108</code> — ép <code>!isNew()</code> thành <code>true</code>):</strong><br>"
            "&bull; Vì <code>isNew() &hArr; id == null</code>, khi ID khác null điều kiện phụ thuộc hoàn toàn vào <code>Objects.equals(id1, id2)</code>.<br>"
            "&bull; Bảng chân trị 5 lớp tương đương chứng minh C_orig &equiv; C_M1 &equiv; C_M2 trên 100% không gian trạng thái (đã kiểm chứng tự động bằng script Python 9/9 case).",
            "<strong>Mutant M3 (<code>OwnerController.java:167</code> — xóa <code>owner.setId(ownerId)</code>):</strong><br>"
            "&bull; Đồ thị luồng CFG chứng minh khối guard dòng 161 đã bảo toàn bất biến <code>owner.getId() == ownerId</code> trước khi chạm dòng 167 &rArr; Lệnh gán là dead-store thuần túy.",
            "<strong>Điểm số hiệu chỉnh học thuật (Adjusted Mutation Score):</strong><br>"
            "&bull; Điểm thô chính thức của PIT: <strong>192 / 195 = 98.46%</strong>.<br>"
            "&bull; Điểm hiệu chỉnh khả thi: <strong>192 / (195 - 3) = 192 / 192 = 100.00% (Hoàn hảo)</strong>."
        ],
        "truth_table": True,
        "notes": "Điểm nhấn học thuật đặc sắc nhất trong phần việc của em là chứng minh hình thức cho 3 mutants sống sót cuối cùng. Đây không phải là điểm yếu của bộ test, mà là 3 Đột biến tương đương về mặt ngữ nghĩa: Tại Owner dòng 108, hai mutant ép các mệnh đề isNew thành true. Em đã mô hình hóa đại số Boolean và lập bảng chân trị trên toàn bộ 5 lớp tương đương của không gian trạng thái. Kết quả chứng minh giá trị logic của mutant luôn đồng nhất tuyệt đối 100% với code gốc, và đã được xác thực tự động bằng script Python duyệt vét cạn. Tương tự tại OwnerController dòng 167, phân tích đồ thị luồng chứng minh khối guard phía trước đã đảm bảo hai ID chắc chắn bằng nhau. Lệnh setId chỉ là một dead-store phòng thủ, việc xóa nó không làm thay đổi bất kỳ hành vi nào của hệ thống. Vì vậy, khi loại trừ 3 mutant tương đương khỏi không gian đột biến khả thi, điểm số hiệu chỉnh thực tế của nhóm đạt tuyệt đối 100%. Sau đây, xin mời bạn Trung Hiếu trình bày về đường ống CI/CD."
    },
    {
        "id": 10,
        "role": "TV1 (Trịnh Trung Hiếu)",
        "duration": "75s (12:00 - 13:15)",
        "title": "Đường ống CI/CD GitHub Actions & Tính khả tái 1-lệnh",
        "subtitle": "Tự động hóa toàn diện 6 bước Fail-Fast và kiểm chứng thực nghiệm trong 35–45 giây",
        "message": "Đóng gói toàn diện kịch bản CI/CD trên cloud và lệnh thực thi tức thì trên máy trạm",
        "bullets": [
            "<strong>Đường ống CI/CD 6 bước Fail-Fast (<code>.github/workflows/mutation-test.yml</code>):</strong><br>"
            "&bull; Bước 1 &amp; 2: Checkout mã nguồn <code>actions/checkout@v4</code> &amp; Setup JDK 17 Temurin + Maven Cache.<br>"
            "&bull; Bước 3: Cổng kiểm thử nhanh: Chạy 153 Unit Tests (ngắt ngay lập tức nếu phát sinh hồi quy).<br>"
            "&bull; Bước 4: Cổng chất lượng K03: Thực thi PIT Mutation Testing &amp; chặn build nếu score &lt; 88%.<br>"
            "&bull; Bước 5: Xuất bảng tóm tắt trực quan <code>$GITHUB_STEP_SUMMARY</code> lên giao diện GitHub Actions.<br>"
            "&bull; Bước 6: Đóng gói và lưu trữ Artifacts báo cáo HTML/XML trong 30 ngày.",
            "<strong>Tính khả tái thực nghiệm 1-lệnh (One-Liner Reproducibility):</strong><br>"
            "&bull; PowerShell: <code>./mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'</code><br>"
            "&bull; Thời gian chạy thực tế: ~35–45 giây trên máy trạm thông thường."
        ],
        "cicd_card": True,
        "notes": "Để đảm bảo tính liên tục và kiểm soát chất lượng tự động, nhóm đã thiết lập đường ống CI/CD hoàn chỉnh trên GitHub Actions theo kiến trúc 6 bước Fail-Fast. Hệ thống sẽ ưu tiên chạy 153 unit test trong 15 giây đầu; nếu có lỗi hồi quy, quy trình sẽ ngắt ngay để tiết kiệm tài nguyên. Tiếp theo, bước phân tích đột biến PIT sẽ thực thi và áp dụng Cổng chất lượng 88%. Nhóm cũng tối ưu hóa khả năng tái hiện với duy nhất 1 câu lệnh Maven Wrapper, giúp bất kỳ ai cũng có thể tự mình kiểm chứng kết quả trong vòng 35 đến 45 giây. Sau đây, xin mời bạn Việt Linh tổng kết kết quả và bài học kinh nghiệm của nhóm."
    },
    {
        "id": 11,
        "role": "TV5 (Hoàng Việt Linh)",
        "duration": "60s (13:15 - 14:15)",
        "title": "Tổng kết đối sánh Baseline vs Final & 4 Bài học kinh nghiệm",
        "subtitle": "Bứt phá toàn diện mọi chỉ số kiểm thử và đúc kết 4 bài học thực tiễn vô giá",
        "message": "Số test tăng từ 49 lên 130, triệt tiêu 100% vùng mã mù và đạt điểm hiệu chỉnh 100.00%",
        "bullets": [
            "<strong>Bảng đối sánh chỉ số cốt lõi (Khớp 100% <code>metrics_summary.csv</code>):</strong><br>"
            "&bull; Số lượng test gói owner: <strong>49 &rarr; 130 tests (+81 tests)</strong> | Toàn dự án: <strong>153 pass</strong>.<br>"
            "&bull; Line Coverage: <strong>96.80% (242/250) &rarr; 100.00% (250/250 lines)</strong>.<br>"
            "&bull; Mutants Killed: <strong>131 / 195 (67.18%) &rarr; 192 / 195 (98.46%)</strong> (&ge; 88%).<br>"
            "&bull; Mutants Survived: <strong>55 &rarr; 3 mutants</strong> (100% Equivalent Mutants).<br>"
            "&bull; Mutants No Coverage: <strong>9 &rarr; 0 mutants</strong> (Triệt tiêu hoàn toàn vùng mù).<br>"
            "&bull; Điểm số hiệu chỉnh: <strong>68.23% &rarr; 100.00% (192/192)</strong>.",
            "<strong>4 Bài học kinh nghiệm thực tiễn:</strong><br>"
            "1. Line Coverage cao tạo an tâm giả tạo; Mutation Testing là thước đo chất lượng thực sự.<br>"
            "2. Cảnh giác cạm bẫy Model Aliasing của Spring MockMvc; bắt buộc có POJO Unit Test.<br>"
            "3. Bắt buộc kiểm tra tương tác (Interaction Testing) bằng <code>verify</code> cho các phương thức void.<br>"
            "4. Kỹ thuật hộp trắng (BVA, Decision Table, Basis Path) là vũ khí tối thượng diệt mutant."
        ],
        "image": "fig4_tests_growth.png",
        "notes": "Nhìn lại toàn bộ hành trình, Bảng tổng kết trên slide đã minh chứng sự bứt phá vượt bậc của dự án: Số lượng test tăng từ 49 lên 130 bài, độ phủ dòng đạt tuyệt đối 100%, và điểm đột biến tăng ngoạn mục từ 67.18% lên 98.46%, loại bỏ hoàn toàn các vùng mã mù kiểm thử. Bốn bài học kinh nghiệm lớn nhất mà nhóm đúc kết được là: Không bao giờ tin tưởng mù quáng vào Code Coverage; luôn cảnh giác trước cạm bẫy che giấu lỗi của MockMvc; bắt buộc phải verify tương tác cho các hàm void bảo mật; và áp dụng bài bản các kỹ thuật hộp trắng kinh điển như BVA và Bảng quyết định. Đây chính là hành trang chuyên môn vô giá cho chúng em trong ngành kiểm thử phần mềm chuyên nghiệp."
    },
    {
        "id": 12,
        "role": "Toàn nhóm (Nhóm 20)",
        "duration": "45s (14:15 - 15:00)",
        "title": "LỜI CẢM ƠN VÀ SẴN SÀNG CHO PHIÊN HỎI ĐÁP (Q&A)",
        "subtitle": "Chân thành cảm ơn ThS. Nguyễn Thế Lâm và Hội đồng chấm đề tài Kiểm thử phần mềm",
        "message": "Toàn thể 5 thành viên Nhóm 20 sẵn sàng đón nhận câu hỏi phản biện từ Hội đồng!",
        "bullets": [
            "<strong>Lời cảm ơn:</strong> Nhóm 20 xin chân thành cảm ơn ThS. Nguyễn Thế Lâm đã tận tình định hướng, hỗ trợ và truyền cảm hứng trong suốt học phần.",
            "<strong>Cam kết chất lượng:</strong> Đề tài đã hoàn thành xuất sắc toàn bộ mục tiêu với tinh thần khoa học trung thực, minh bạch.",
            "<strong>Lưu trữ mã nguồn:</strong> Toàn bộ source code, bộ test, tài liệu báo cáo và nhật ký thực nghiệm được lưu trữ đầy đủ tại GitHub Repository của nhóm.",
            "<strong>SẴN SÀNG CHO PHIÊN PHẢN BIỆN:</strong> Kính mời quý Thầy Cô và Hội đồng đặt câu hỏi!"
        ],
        "qa_badge": True,
        "notes": "Kính thưa Thầy Nguyễn Thế Lâm và quý Thầy Cô trong Hội đồng, phần báo cáo của nhóm 20 về đề tài R01 kết hợp K03 đến đây là hoàn tất. Chúng em xin chân thành cảm ơn sự hướng dẫn tận tâm của Thầy trong suốt học phần Kiểm thử phần mềm. Giờ đây, toàn thể 5 thành viên của nhóm đã sẵn sàng đón nhận những câu hỏi, nhận xét và đóng góp quý báu từ Thầy và Hội đồng. Chúng em xin trân trọng cảm ơn!"
    }
]

def generate_slide_html(slide, is_standalone=True):
    # Colors and aesthetics
    s_id = slide["id"]
    role = slide["role"]
    duration = slide["duration"]
    title = slide["title"]
    subtitle = slide["subtitle"]
    message = slide["message"]
    bullets = slide["bullets"]
    notes = slide["notes"]
    
    # Check visuals
    has_image = "image" in slide
    img_tag = ""
    if has_image:
        img_file = FIGURES_DIR / slide["image"]
        abs_img = img_file.resolve().as_posix()
        img_tag = f'<div class="visual-pane"><img src="file:///{abs_img}" alt="{slide["image"]}" class="slide-fig" /></div>'
    elif slide.get("truth_table"):
        img_tag = '''
        <div class="visual-pane">
            <div class="card-table">
                <div class="card-header">Bảng chân trị 5 lớp tương đương (Owner.java:108)</div>
                <table class="truth-tbl">
                    <thead>
                        <tr>
                            <th>Lớp đầu vào (x, y)</th>
                            <th>&not;a</th>
                            <th>&not;b</th>
                            <th>e (x=y)</th>
                            <th>C_orig</th>
                            <th>C_M1</th>
                            <th>C_M2</th>
                            <th>Kết quả</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>1. (null, null)</td><td>0</td><td>0</td><td>1</td><td class="res-0">0</td><td class="res-0">0</td><td class="res-0">0</td><td class="eq-badge">ĐỒNG NHẤT</td></tr>
                        <tr><td>2. (null, 1)</td><td>0</td><td>1</td><td>0</td><td class="res-0">0</td><td class="res-0">0</td><td class="res-0">0</td><td class="eq-badge">ĐỒNG NHẤT</td></tr>
                        <tr><td>3. (1, null)</td><td>1</td><td>0</td><td>0</td><td class="res-0">0</td><td class="res-0">0</td><td class="res-0">0</td><td class="eq-badge">ĐỒNG NHẤT</td></tr>
                        <tr><td>4. (1, 2)</td><td>1</td><td>1</td><td>0</td><td class="res-0">0</td><td class="res-0">0</td><td class="res-0">0</td><td class="eq-badge">ĐỒNG NHẤT</td></tr>
                        <tr class="hl-row"><td>5. (1, 1)</td><td>1</td><td>1</td><td>1</td><td class="res-1">1</td><td class="res-1">1</td><td class="res-1">1</td><td class="eq-badge">ĐỒNG NHẤT</td></tr>
                    </tbody>
                </table>
                <div class="score-formula">
                    <strong>Adjusted Score:</strong> 192 / (195 - 3) = <strong>100.00%</strong>
                </div>
            </div>
        </div>
        '''
    elif slide.get("badges"):
        b_html = "".join([f'''
            <div class="metric-card card-{b["color"]}">
                <div class="metric-val">{b["value"]}</div>
                <div class="metric-lbl">{b["label"]}</div>
                <div class="metric-sub">{b["sub"]}</div>
            </div>
        ''' for b in slide["badges"]])
        img_tag = f'<div class="visual-pane"><div class="badges-grid">{b_html}</div></div>'
    elif slide.get("boxes"):
        boxes_html = "".join([f'''
            <div class="info-card">
                <div class="info-title">{b["title"]}</div>
                <div class="info-desc">{b["desc"]}</div>
            </div>
        ''' for b in slide["boxes"]])
        img_tag = f'<div class="visual-pane"><div class="info-stack">{boxes_html}</div></div>'
    elif slide.get("rip_diagram"):
        img_tag = '''
        <div class="visual-pane">
            <div class="rip-card">
                <div class="card-header">Chuỗi chuyển hóa lỗi IEEE & Chuỗi RIP</div>
                <div class="rip-step step-r">
                    <span class="step-badge">R</span>
                    <div><strong>Reachability:</strong> Test case thực thi chạm tới dòng mã có đột biến.</div>
                </div>
                <div class="rip-arrow">&darr;</div>
                <div class="rip-step step-i">
                    <span class="step-badge">I</span>
                    <div><strong>Infection:</strong> Lỗi thay đổi trạng thái nội bộ JVM (sinh ra Error).</div>
                </div>
                <div class="rip-arrow">&darr;</div>
                <div class="rip-step step-p">
                    <span class="step-badge">P</span>
                    <div><strong>Propagation:</strong> Trạng thái sai lệch lan truyền ra ngõ ra (Failure).</div>
                </div>
                <div class="rip-outcome">
                    <span class="badge-kill">ASSERTION BẮT ĐƯỢC &rarr; KILLED!</span>
                </div>
            </div>
        </div>
        '''
    elif slide.get("gate_badge"):
        img_tag = '''
        <div class="visual-pane">
            <div class="gate-card">
                <div class="card-header">Thiết lập Cổng chất lượng trong pom.xml</div>
                <pre class="code-box"><code>&lt;plugin&gt;
  &lt;groupId&gt;org.pitest&lt;/groupId&gt;
  &lt;artifactId&gt;pitest-maven&lt;/artifactId&gt;
  &lt;version&gt;1.30.0&lt;/version&gt;
  &lt;configuration&gt;
    &lt;mutators&gt;
      &lt;mutator&gt;STRONGER&lt;/mutator&gt;
    &lt;/mutators&gt;
    &lt;mutationThreshold&gt;88&lt;/mutationThreshold&gt;
    &lt;coverageThreshold&gt;95&lt;/coverageThreshold&gt;
  &lt;/configuration&gt;
&lt;/plugin&gt;</code></pre>
                <div class="gate-status">Trạng thái hiện tại: <strong>PASS (98.46% &ge; 88%)</strong></div>
            </div>
        </div>
        '''
    elif slide.get("table_summary"):
        rows = "".join([f'''<tr><td>{r["tech"]}</td><td><code>{r["target"]}</code></td><td>{r["mutant"]}</td><td class="badge-kill">{r["status"]}</td></tr>''' for r in slide["table_summary"]])
        img_tag = f'''
        <div class="visual-pane">
            <div class="card-table">
                <div class="card-header">Chiến lược Hộp đen TV3</div>
                <table class="truth-tbl">
                    <thead><tr><th>Kỹ thuật</th><th>Target Code</th><th>Toán tử PIT</th><th>Kết quả</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>
        '''
    elif slide.get("cfg_card"):
        img_tag = '''
        <div class="visual-pane">
            <div class="info-card" style="border-left: 4px solid #3A86FF;">
                <div class="info-title">Đồ thị luồng updatePetDetails [V(G)=3]</div>
                <div class="info-desc">
                    &bull; N1: Vào hàm kiểm tra ownerId &amp; petId null.<br>
                    &bull; N2: Rẽ nhánh <code>isNew()</code>.<br>
                    &bull; N3: Tìm kiếm pet trong danh sách.<br>
                    &bull; <strong>N4 (Tử huyệt):</strong> 3 lệnh sao chép field.<br>
                    &bull; N5: <code>owner.save(owner)</code> lưu CSDL.<br>
                    &bull; N6: Redirect về trang hiển thị.<br>
                    &bull; N7: Kết thúc hàm.
                </div>
                <div class="score-formula" style="margin-top:12px;">
                    <strong>Vũ khí:</strong> Detached Entity + ArgumentCaptor
                </div>
            </div>
        </div>
        '''
    elif slide.get("cicd_card"):
        img_tag = '''
        <div class="visual-pane">
            <div class="info-card" style="border-left: 4px solid #10B981;">
                <div class="info-title">Kiến trúc CI/CD Fail-Fast 6 bước</div>
                <div class="info-desc" style="line-height: 1.8;">
                    &bull; <strong>1. Checkout:</strong> Fetch source full-depth.<br>
                    &bull; <strong>2. Setup:</strong> JDK 17 Temurin + Maven Cache.<br>
                    &bull; <strong>3. Fast Gate:</strong> 153 Unit Tests (15 giây).<br>
                    &bull; <strong>4. K03 Gate:</strong> PIT Mutation Testing (&ge; 88%).<br>
                    &bull; <strong>5. Summary:</strong> Xuất báo cáo Markdown trực quan.<br>
                    &bull; <strong>6. Artifacts:</strong> Lưu trữ HTML/XML 30 ngày.
                </div>
            </div>
        </div>
        '''
    elif slide.get("qa_badge"):
        img_tag = '''
        <div class="visual-pane">
            <div class="qa-hero">
                <div class="qa-icon">&#10067;&#10068;</div>
                <div class="qa-text">SẴN SÀNG CHO PHIÊN Q&amp;A</div>
                <div class="qa-sub">15 câu hỏi phản biện đã chuẩn bị kỹ lưỡng</div>
            </div>
        </div>
        '''

    bullets_html = "".join([f"<li>{b}</li>" for b in bullets])

    body_content = f'''
    <div class="slide" id="slide-{s_id}">
        <header class="slide-header">
            <div class="header-left">
                <span class="role-badge">{role}</span>
                <span class="time-badge">{duration}</span>
                <span class="project-tag">Program_R01-K03 &bull; Slide {s_id}/12</span>
            </div>
            <div class="header-right">
                <span class="school-tag">ĐH Đà Lạt &bull; Khoa CNTT</span>
            </div>
        </header>

        <div class="slide-title-block">
            <h1 class="slide-title">{title}</h1>
            <p class="slide-subtitle">{subtitle}</p>
        </div>

        <div class="message-banner">
            <span class="msg-icon">&#128161;</span>
            <span class="msg-text">{message}</span>
        </div>

        <div class="slide-content-grid">
            <div class="content-pane">
                <ul class="bullet-list">
                    {bullets_html}
                </ul>
            </div>
            {img_tag}
        </div>

        <footer class="slide-footer">
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {(s_id / 12) * 100}%;"></div>
            </div>
            <div class="footer-info">
                <span>Mutation Testing bằng PIT trên Spring PetClinic</span>
                <span>GVHD: ThS. Nguyễn Thế Lâm &bull; Nhóm 20</span>
            </div>
        </footer>
    </div>
    '''

    if not is_standalone:
        return body_content

    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Slide {s_id}: {title}</title>
    <style>
{CSS_STYLES}
    </style>
</head>
<body>
{body_content}
</body>
</html>'''

CSS_STYLES = '''
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background: #0B132B;
        color: #E2E8F0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
    }
    .slide {
        width: 1920px;
        height: 1080px;
        padding: 50px 70px 40px 70px;
        background: radial-gradient(circle at top right, #1C2541 0%, #0B132B 100%);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    .slide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 44px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
    }
    .header-left { display: flex; align-items: center; gap: 14px; }
    .role-badge {
        background: #3A86FF;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 15px;
        padding: 6px 14px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }
    .time-badge {
        background: rgba(255, 255, 255, 0.1);
        color: #CBD5E1;
        font-size: 14px;
        padding: 6px 12px;
        border-radius: 20px;
    }
    .project-tag { color: #94A3B8; font-size: 14px; font-weight: 500; }
    .school-tag { color: #94A3B8; font-size: 14px; font-weight: 600; }

    .slide-title-block { margin-top: 18px; margin-bottom: 10px; }
    .slide-title {
        font-size: 38px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.25;
        letter-spacing: -0.5px;
    }
    .slide-subtitle {
        font-size: 20px;
        color: #94A3B8;
        margin-top: 6px;
        font-weight: 400;
    }

    .message-banner {
        background: rgba(58, 134, 255, 0.15);
        border-left: 5px solid #3A86FF;
        padding: 12px 20px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }
    .msg-icon { font-size: 20px; }
    .msg-text {
        font-size: 18px;
        font-weight: 600;
        color: #93C5FD;
    }

    .slide-content-grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 40px;
        flex: 1;
        align-items: center;
        min-height: 0;
    }
    .content-pane {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .bullet-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .bullet-list li {
        font-size: 19px;
        line-height: 1.5;
        color: #E2E8F0;
        position: relative;
        padding-left: 28px;
    }
    .bullet-list li::before {
        content: "■";
        position: absolute;
        left: 0;
        color: #3A86FF;
        font-size: 14px;
        top: 3px;
    }
    .bullet-list code {
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: Consolas, monospace;
        font-size: 17px;
        color: #F8FAFC;
    }
    .bullet-list strong { color: #FFFFFF; font-weight: 700; }

    .visual-pane {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        max-height: 580px;
    }
    .slide-fig {
        max-width: 100%;
        max-height: 560px;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        background: #FFFFFF;
        padding: 10px;
    }

    .badges-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        width: 100%;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .card-emerald { border-color: #10B981; background: rgba(16, 185, 129, 0.1); }
    .card-blue { border-color: #3A86FF; background: rgba(58, 134, 255, 0.1); }
    .card-gold { border-color: #F59E0B; background: rgba(245, 158, 11, 0.1); }
    .metric-val { font-size: 44px; font-weight: 900; color: #FFFFFF; margin-bottom: 6px; }
    .metric-lbl { font-size: 18px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-sub { font-size: 15px; color: #CBD5E1; margin-top: 4px; }

    .info-stack { display: flex; flex-direction: column; gap: 16px; width: 100%; }
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #3A86FF;
        border-radius: 12px;
        padding: 18px 24px;
    }
    .info-title { font-size: 19px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px; }
    .info-desc { font-size: 16px; color: #CBD5E1; line-height: 1.45; }

    .card-table {
        width: 100%;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
        padding: 16px;
    }
    .card-header {
        font-size: 18px;
        font-weight: 700;
        color: #93C5FD;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }
    .truth-tbl {
        width: 100%;
        border-collapse: collapse;
        font-size: 15px;
    }
    .truth-tbl th {
        background: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        padding: 8px 10px;
        text-align: center;
    }
    .truth-tbl td {
        padding: 7px 10px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .hl-row { background: rgba(58, 134, 255, 0.15); font-weight: 700; }
    .res-0 { color: #94A3B8; font-weight: 700; }
    .res-1 { color: #10B981; font-weight: 900; }
    .eq-badge {
        background: #10B981;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 10px;
    }
    .badge-kill {
        background: #10B981;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 12px;
        display: inline-block;
    }
    .score-formula {
        margin-top: 14px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 17px;
        color: #A7F3D0;
    }

    .rip-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    .rip-step {
        display: flex;
        align-items: center;
        gap: 14px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 16px;
    }
    .step-badge {
        background: #3A86FF;
        color: #FFFFFF;
        font-weight: 900;
        font-size: 18px;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .rip-arrow { text-align: center; font-size: 22px; color: #3A86FF; margin: 4px 0; }
    .rip-outcome { text-align: center; margin-top: 14px; }

    .gate-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    .code-box {
        background: #000000;
        border-radius: 8px;
        padding: 16px;
        color: #A7F3D0;
        font-family: Consolas, monospace;
        font-size: 15px;
        overflow-x: auto;
    }
    .gate-status {
        margin-top: 14px;
        padding: 12px;
        border-radius: 8px;
        background: rgba(16, 185, 129, 0.15);
        color: #A7F3D0;
        text-align: center;
        font-size: 18px;
    }

    .qa-hero {
        text-align: center;
        padding: 40px;
        background: rgba(58, 134, 255, 0.1);
        border: 2px dashed #3A86FF;
        border-radius: 20px;
        width: 100%;
    }
    .qa-icon { font-size: 72px; margin-bottom: 16px; }
    .qa-text { font-size: 32px; font-weight: 900; color: #FFFFFF; }
    .qa-sub { font-size: 18px; color: #93C5FD; margin-top: 8px; }

    .slide-footer {
        display: flex;
        flex-direction: column;
        gap: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 12px;
    }
    .progress-bar-container {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
    }
    .progress-bar { height: 100%; background: #3A86FF; border-radius: 2px; }
    .footer-info {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        color: #64748B;
        font-weight: 500;
    }
'''

def create_native_pptx():
    """Tạo tệp OpenXML PowerPoint slides/R01_K03_Defense.pptx chuẩn với speaker notes."""
    pptx_path = SLIDES_DIR / "R01_K03_Defense.pptx"
    print(f"Bắt đầu đóng gói {pptx_path} chuẩn OpenXML...")

    z = zipfile.ZipFile(pptx_path, "w", zipfile.ZIP_DEFLATED)

    # 1. [Content_Types].xml
    content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
                     '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
                     '  <Default Extension="xml" ContentType="application/xml"/>',
                     '  <Default Extension="png" ContentType="image/png"/>',
                     '  <Default Extension="jpeg" ContentType="image/jpeg"/>',
                     '  <Default Extension="jpg" ContentType="image/jpeg"/>',
                     '  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
                     '  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
                     '  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
                     '  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
                     '  <Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>']

    for i in range(1, 13):
        content_types.append(f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        content_types.append(f'  <Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>')
    content_types.append('</Types>')
    z.writestr('[Content_Types].xml', "\n".join(content_types))

    # 2. _rels/.rels
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
    z.writestr('_rels/.rels', root_rels)

    # 3. ppt/presentation.xml
    pres_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">',
                '  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rIdMaster1"/></p:sldMasterIdLst>',
                '  <p:notesMasterIdLst><p:notesMasterId r:id="rIdNotesMaster1"/></p:notesMasterIdLst>',
                '  <p:sldIdLst>']
    for i in range(1, 13):
        pres_xml.append(f'    <p:sldId id="{255 + i}" r:id="rIdSlide{i}"/>')
    pres_xml.extend([
        '  </p:sldIdLst>',
        '  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>',
        '  <p:notesSz cx="6858000" cy="9144000"/>',
        '</p:presentation>'
    ])
    z.writestr('ppt/presentation.xml', "\n".join(pres_xml))

    # 4. ppt/_rels/presentation.xml.rels
    pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                 '  <Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
                 '  <Relationship Id="rIdNotesMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>',
                 '  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>']
    for i in range(1, 13):
        pres_rels.append(f'  <Relationship Id="rIdSlide{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>')
    pres_rels.append('</Relationships>')
    z.writestr('ppt/_rels/presentation.xml.rels', "\n".join(pres_rels))

    # 5. ppt/theme/theme1.xml
    theme_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="PetClinic Deep Navy Theme">
  <a:themeElements>
    <a:clrScheme name="PetClinic">
      <a:dk1><a:srgbClr val="0B132B"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1C2541"/></a:dk2>
      <a:lt2><a:srgbClr val="E2E8F0"/></a:lt2>
      <a:accent1><a:srgbClr val="3A86FF"/></a:accent1>
      <a:accent2><a:srgbClr val="10B981"/></a:accent2>
      <a:accent3><a:srgbClr val="F59E0B"/></a:accent3>
      <a:accent4><a:srgbClr val="EF4444"/></a:accent4>
      <a:accent5><a:srgbClr val="8B5CF6"/></a:accent5>
      <a:accent6><a:srgbClr val="06B6D4"/></a:accent6>
      <a:hlink><a:srgbClr val="3A86FF"/></a:hlink>
      <a:folHlink><a:srgbClr val="8B5CF6"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Modern Sans">
      <a:majorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>'''
    z.writestr('ppt/theme/theme1.xml', theme_xml)

    # 6. ppt/slideMasters/slideMaster1.xml & rels
    master_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rIdLayout1"/></p:sldLayoutIdLst>
</p:sldMaster>'''
    z.writestr('ppt/slideMasters/slideMaster1.xml', master_xml)

    master_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdLayout1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>'''
    z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels', master_rels)

    # 7. ppt/slideLayouts/slideLayout1.xml & rels
    layout_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
    </p:spTree>
  </p:cSld>
</p:sldLayout>'''
    z.writestr('ppt/slideLayouts/slideLayout1.xml', layout_xml)

    layout_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>'''
    z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels', layout_rels)

    # 8. ppt/notesMasters/notesMaster1.xml & rels
    notes_master = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
</p:notesMaster>'''
    z.writestr('ppt/notesMasters/notesMaster1.xml', notes_master)

    notes_master_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>'''
    z.writestr('ppt/notesMasters/_rels/notesMaster1.xml.rels', notes_master_rels)

    # Add images into ppt/media/
    media_map = {}
    media_idx = 1
    for fig_name in ["fig1_coverage_vs_mutation.png", "fig3_survivors_by_mutator.png", "fig4_tests_growth.png"]:
        fig_path = FIGURES_DIR / fig_name
        if fig_path.exists():
            z.write(fig_path, f"ppt/media/image{media_idx}.png")
            media_map[fig_name] = f"image{media_idx}.png"
            media_idx += 1

    # 9. Create 12 slides & 12 notesSlides
    for s in SLIDES_DATA:
        s_id = s["id"]
        role = s["role"]
        duration = s["duration"]
        title = s["title"]
        subtitle = s["subtitle"]
        message = s["message"]
        bullets = s["bullets"]
        notes = s["notes"]

        # Clean HTML tags for PPTX plain text
        import re
        def clean_tags(txt):
            return re.sub(r'<[^>]+>', '', txt).replace('&bull;', '•').replace('&rarr;', '→').replace('&rArr;', '⇒').replace('&ge;', '≥').replace('&le;', '≤').replace('&forall;', '∀').replace('&isin;', '∈').replace('&equiv;', '≡').replace('&hArr;', '⇔').replace('&not;', '¬')

        title_clean = clean_tags(title)
        subtitle_clean = clean_tags(subtitle)
        msg_clean = clean_tags(message)

        # Bullets XML paragraphs
        bullet_pars = []
        for b in bullets:
            b_clean = clean_tags(b)
            bullet_pars.append(f'''
              <a:p>
                <a:pPr marL="285750" indent="-285750">
                  <a:buChar char="■"/>
                </a:pPr>
                <a:r>
                  <a:rPr lang="vi-VN" sz="1500" dirty="0">
                    <a:solidFill><a:srgbClr val="E2E8F0"/></a:solidFill>
                  </a:rPr>
                  <a:t>{clean_xml(b_clean)}</a:t>
                </a:r>
              </a:p>
            ''')
        bullets_xml = "".join(bullet_pars)

        # Slide relationships
        slide_rels = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '  <Relationship Id="rIdLayout" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>',
            f'  <Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{s_id}.xml"/>'
        ]

        pic_xml = ""
        if "image" in s and s["image"] in media_map:
            img_rel_id = "rIdImg1"
            img_target = f"../media/{media_map[s['image']]}"
            slide_rels.append(f'  <Relationship Id="{img_rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{img_target}"/>')
            pic_xml = f'''
            <p:pic>
              <p:nvPicPr>
                <p:cNvPr id="10" name="Picture"/>
                <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
                <p:nvPr/>
              </p:nvPicPr>
              <p:blipFill>
                <a:blip r:embed="{img_rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </p:blipFill>
              <p:spPr>
                <a:xfrm>
                  <a:off x="6400000" y="2100000"/>
                  <a:ext cx="5200000" cy="4200000"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </p:spPr>
            </p:pic>
            '''

        slide_rels.append('</Relationships>')
        z.writestr(f'ppt/slides/_rels/slide{s_id}.xml.rels', "\n".join(slide_rels))

        # Slide XML
        slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      
      <!-- Background Dark Rectangle -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Background"/><p:cNvSpPr><a:spLocks noMove="1" noResize="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="0B132B"/></a:solidFill>
        </p:spPr>
      </p:sp>

      <!-- Header Role & Time -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="HeaderRole"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="365760"/><a:ext cx="10820400" cy="457200"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vertOverflow="clip"/>
          <a:p>
            <a:r>
              <a:rPr lang="vi-VN" sz="1300" b="1">
                <a:solidFill><a:srgbClr val="3A86FF"/></a:solidFill>
              </a:rPr>
              <a:t>{clean_xml(role)}  |  {clean_xml(duration)}  |  Slide {s_id}/12</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Title & Subtitle -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="TitleBlock"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="822960"/><a:ext cx="10820400" cy="914400"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vertOverflow="clip"/>
          <a:p>
            <a:r>
              <a:rPr lang="vi-VN" sz="2600" b="1">
                <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
              </a:rPr>
              <a:t>{clean_xml(title_clean)}</a:t>
            </a:r>
          </a:p>
          <a:p>
            <a:r>
              <a:rPr lang="vi-VN" sz="1400">
                <a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill>
              </a:rPr>
              <a:t>{clean_xml(subtitle_clean)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Message Banner -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="5" name="MessageBanner"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="685800" y="1783080"/><a:ext cx="10820400" cy="457200"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 20000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="1C2541"/></a:solidFill>
          <a:ln w="19050"><a:solidFill><a:srgbClr val="3A86FF"/></a:solidFill></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr lIns="182880" tIns="91440" rIns="182880" bIns="91440"/>
          <a:p>
            <a:r>
              <a:rPr lang="vi-VN" sz="1400" b="1">
                <a:solidFill><a:srgbClr val="93C5FD"/></a:solidFill>
              </a:rPr>
              <a:t>★ THÔNG ĐIỆP CỐT LÕI: {clean_xml(msg_clean)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Left Content Bullet Points -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="6" name="ContentBullets"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="685800" y="2377440"/>
            <a:ext cx="{5400000 if pic_xml else 10820400}" cy="4023360"/>
          </a:xfrm>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vertOverflow="clip"/>
          {bullets_xml}
        </p:txBody>
      </p:sp>

      {pic_xml}

    </p:spTree>
  </p:cSld>
</p:sld>'''
        z.writestr(f'ppt/slides/slide{s_id}.xml', slide_xml)

        # 10. Notes slide for presenter notes
        notes_clean = clean_tags(notes)
        notes_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdSlide" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{s_id}.xml"/>
  <Relationship Id="rIdNotesMaster" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/>
</Relationships>'''
        z.writestr(f'ppt/notesSlides/_rels/notesSlide{s_id}.xml.rels', notes_rels)

        notes_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Slide Image"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="685800"/><a:ext cx="5486400" cy="3086100"/></a:xfrm></p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="Notes Text"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="4114800"/><a:ext cx="5486400" cy="4572000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:p>
            <a:r>
              <a:rPr lang="vi-VN" sz="1400" b="1">
                <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
              </a:rPr>
              <a:t>[SPEAKER NOTES — {clean_xml(role)} | Thời lượng: {clean_xml(duration)}]&#10;&#10;</a:t>
            </a:r>
            <a:r>
              <a:rPr lang="vi-VN" sz="1300">
                <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
              </a:rPr>
              <a:t>{clean_xml(notes_clean)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:notes>'''
        z.writestr(f'ppt/notesSlides/notesSlide{s_id}.xml', notes_xml)

    z.close()
    print(f"-> ĐÃ TẠO THÀNH CÔNG: {pptx_path} ({os.path.getsize(pptx_path):,} bytes).")

def clean_xml(txt):
    return (txt.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;")
               .replace('"', "&quot;")
               .replace("'", "&apos;"))

def main():
    print("=== BẮT ĐẦU XÂY DỰNG PRESENTATION BẢO VỆ R01-K03 ===")
    
    # 1. Sinh các tệp slide HTML đơn lẻ
    print("1. Đang sinh 12 tệp slide HTML trong slides/preview/...")
    html_files = []
    for s in SLIDES_DATA:
        s_id = s["id"]
        fname = f"slide_{s_id:02d}.html"
        fpath = PREVIEW_DIR / fname
        html_content = generate_slide_html(s, is_standalone=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html_content)
        html_files.append((s_id, fpath))
    print(f"   -> Đã sinh xong {len(html_files)} tệp slide HTML.")

    # 2. Sinh slide deck tổng hợp slides/presentation.html
    print("2. Đang sinh slides/presentation.html tổng hợp...")
    deck_slides = []
    for s in SLIDES_DATA:
        deck_slides.append(generate_slide_html(s, is_standalone=False))
    
    deck_html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Presentation R01-K03: Mutation Testing trên Spring PetClinic</title>
    <style>
{CSS_STYLES}
        body {{
            display: flex;
            flex-direction: column;
            width: 100%;
            height: auto;
            overflow-y: auto;
            background: #000000;
            gap: 40px;
            padding: 40px 0;
            align-items: center;
        }}
        .slide-wrapper {{
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .deck-notes {{
            width: 1920px;
            background: #111827;
            border: 1px solid #374151;
            border-top: none;
            padding: 20px 40px;
            color: #9CA3AF;
            font-size: 16px;
            line-height: 1.6;
        }}
        .deck-notes strong {{ color: #F3F4F6; }}
    </style>
</head>
<body>
'''
    for i, s in enumerate(SLIDES_DATA):
        deck_html += f'''
    <div class="slide-wrapper">
        {deck_slides[i]}
        <div class="deck-notes">
            <strong>[SPEAKER NOTES — {s["role"]} &bull; {s["duration"]}]:</strong><br>
            {s["notes"]}
        </div>
    </div>
        '''
    deck_html += "</body></html>"

    deck_path = SLIDES_DIR / "presentation.html"
    with open(deck_path, "w", encoding="utf-8") as f:
        f.write(deck_html)
    print(f"   -> Đã sinh xong slides/presentation.html ({os.path.getsize(deck_path):,} bytes).")

    # 3. Dùng Chrome headless chụp ảnh 12 slides
    print("3. Đang chụp ảnh render 12 slides qua Chrome headless (1920x1080)...")
    for s_id, fpath in html_files:
        png_name = f"slide_{s_id:02d}.png"
        png_path = PREVIEW_DIR / png_name
        abs_html = fpath.resolve().as_posix()
        abs_png = png_path.resolve().as_posix()

        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--hide-scrollbars",
            f"--screenshot={abs_png}",
            f"file:///{abs_html}"
        ]
        res = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace')
        if png_path.exists() and os.path.getsize(png_path) > 0:
            print(f"   [✓] Slide {s_id:02d} -> {png_name} ({os.path.getsize(png_path):,} bytes)")
        else:
            print(f"   [!] Thất bại slide {s_id:02d}: {res.stderr}")

    # 4. Tạo native PPTX OpenXML
    print("4. Đang xây dựng tệp OpenXML PowerPoint...")
    create_native_pptx()

    print("=== HOÀN TẤT TẠO TOÀN BỘ SLIDES & PREVIEW ===")

if __name__ == "__main__":
    main()
