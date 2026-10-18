# Bản nháp Phần C dành riêng TV3 — Môi trường và tái hiện

## C.1. Phạm vi và snapshot đối chiếu

**SESSION S05 — 19/10/2026 (UTC+07:00).** Đây là bản nháp để nhóm review/tích hợp, không chỉnh sửa `REPORT_R01_K03.md` hoặc nhận phần demo của TV2 là đã thực hiện. Hướng dẫn thao tác từng bước: [ONBOARDING_WINDOWS.md](ONBOARDING_WINDOWS.md).

| Thuộc tính | Kết quả quan sát S05 |
|---|---|
| Repo root | C:/Users/minht/Downloads/KiemThuPhanMem/Program/Mutation-Testing_-Spring-PetClinic-System |
| Branch hiện tại | TranMinhTai/Sessio4 |
| HEAD | 41c65b07636448fc92d44e7d641e63d1ca0ee59b |
| Commit message | S04 — PetVisitModelMutationTests.java: deep assertion, formatter và ngày ổn định |
| Working tree lúc bắt đầu | Sạch, git status --short không có output |
| Pinned SUT base | 500158f732419217507c7656904b8e6aa1bcc0d6 |
| Quan hệ với pinned base | git merge-base --is-ancestor trả exit 0 |
| Docs TV3 lúc bắt đầu | Chưa có ONBOARDING_WINDOWS.md và hai tài liệu thiết kế S01 trong branch này |
| Phạm vi thay đổi S05 | Tạo onboarding và bản nháp này trong docs/tv3; không sửa code/build/DB/báo cáo chung |

Tên nhánh `Sessio4` giữ nguyên như Git báo, không tự chuẩn hóa thành `Session4`. Tài liệu S01 có ở commit `1f1091b`, đã được S04 đọc qua git show; việc tích hợp docs giữa các nhánh chưa làm ở S05. Không đổi branch hoặc reset về pinned SHA.

## C.2. Cấu hình thực tế và biến môi trường

Đo bằng lệnh trên máy hiện tại khoảng **03:58 ngày 19/10/2026 +07:00**; không lấy version cài đặt từ giả định trong handover.

| Thành phần | Giá trị | Bằng chứng |
|---|---|---|
| Windows | Microsoft Windows 11 Home Single Language; 10.0.26200, build 26200, 64-bit | Get-CimInstance Win32_OperatingSystem |
| PowerShell | 5.1.26100.9711, Desktop | $PSVersionTable |
| Java runtime | openjdk 21.0.12.1; Temurin-21.0.12.1+1-LTS | java -version, exit 0 |
| Java compiler | javac 21.0.12.1 | javac -version, exit 0 |
| JAVA_HOME | C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot\ | $env:JAVA_HOME |
| java/javac trên PATH | bin/java.exe và bin/javac.exe trong cùng thư mục JDK trên | Get-Command java,javac |
| Maven thực thi | Apache Maven 3.9.16 | .\mvnw.cmd -v, exit 0 |
| JDK Maven dùng | 21.0.12.1, Eclipse Adoptium, runtime trùng JAVA_HOME | .\mvnw.cmd -v |
| Maven distribution cache | C:\Users\minht\.m2\wrapper\dists\apache-maven-3.9.16\… | Maven home trong output wrapper |
| Maven wrapper script | 3.3.4; distributionType=only-script | .mvn/wrapper/maven-wrapper.properties |
| URL Maven distribution | repo.maven.apache.org, artifact apache-maven-3.9.16-bin.zip | wrapper properties |
| Git | 2.55.0.windows.5 | git --version, exit 0 |
| Spring Boot parent | 4.1.0 | pom.xml |
| Target Java | java.version=17, Enforcer dùng cùng property | pom.xml |
| PIT / JUnit adapter | 1.30.0 / 1.2.3 | plugin và dependency trong pom.xml |
| PIT cấu hình | STRONGER, classes/tests owner.*, HTML/XML, timestampedReports=false | pom.xml |
| Quality gates | mutationThreshold=88, coverageThreshold=95 | pom.xml |

Nguồn cấu hình trong repo: [POM](../../pom.xml), [wrapper](../../.mvn/wrapper/maven-wrapper.properties), [cấu hình H2 mặc định](../../src/main/resources/application.properties).

Lần đọc OS qua CIM trong sandbox ban đầu bị Access denied; chạy lại lệnh chỉ đọc với quyền được cấp đã lấy được bảng OS trên (exit 0). Đây là trở ngại truy vấn metadata đã xử lý, không phải lỗi build/test. PowerShell BuildVersion không được dùng thay cho OS BuildNumber: chúng khác nhau trong lần đo này.

**JDK chạy và target compatibility:** JDK 21 là chương trình thực thi Maven và javac trên máy này. Java 17 là target cấu hình của dự án; log compile S04 ghi `release 17`. Tài liệu phân công yêu cầu tối thiểu JDK 17; handover bổ sung 18/10 dùng Temurin 21.0.12.1, khớp máy hiện tại. S05 không chứng minh runtime JDK 17 hoặc mọi dependency tương thích JDK 17; cần lần chạy riêng nếu dùng môi trường đó.

**Biến cần kiểm tra:** JAVA_HOME tới gốc JDK; PATH có bin của JDK và Git; Maven wrapper dùng JDK đúng như `mvnw -v`. Profile ứng dụng mặc định dùng H2 theo source; trước khi chạy kiểm tra terminal có đang đặt `SPRING_PROFILES_ACTIVE` hoặc tham số override khác hay không. Không cần cấu hình DB ngoài cho H2. S05 không in toàn bộ biến môi trường hoặc settings chứa thông tin nhạy cảm, không thay JAVA_HOME/PATH hệ thống.

## C.3. Lệnh build/test/run được bàn giao

Các lệnh dưới chạy từ repo root, dùng PowerShell; đây là quy trình để người nhận chạy. Chúng **không được thực thi lại trong S05**, ngoại trừ `mvnw.cmd -v` đã ghi ở C.2.

```powershell
# Môi trường.
.\mvnw.cmd -v

# Ba lớp TV3.
.\mvnw.cmd test '-Dtest=OwnerMutationTests,PetValidatorMutationTests,PetVisitModelMutationTests'
if ($LASTEXITCODE -ne 0) { throw 'TV3 thất bại.' }

# Package owner.
.\mvnw.cmd test '-Dtest=org.springframework.samples.petclinic.owner.**'
if ($LASTEXITCODE -ne 0) { throw 'Owner thất bại.' }

# Hồi quy theo filter dùng trong báo cáo nhóm.
.\mvnw.cmd test '-Dtest=!*IntegrationTests' '-DfailIfNoTests=false'
if ($LASTEXITCODE -ne 0) { throw 'Hồi quy có lọc thất bại.' }

# PIT, giữ nguyên ngưỡng và scope trong POM.
.\mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'
if ($LASTEXITCODE -ne 0) { throw 'PIT thất bại; xem log và quality gate.' }

# Đóng gói chỉ sau khi các lần test cần thiết đã đạt.
.\mvnw.cmd package '-DskipTests'
if ($LASTEXITCODE -ne 0) { throw 'Package thất bại.' }
```

Ứng dụng chạy ở terminal riêng:

```powershell
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.arguments=--server.port=8090'
```

`!*IntegrationTests` bỏ **cả bốn** lớp: MySqlIntegrationTests, PostgresIntegrationTests, PetClinicIntegrationTests và CrashControllerIntegrationTests. Hai lớp đầu cần Docker để chạy nội dung tích hợp CSDL; hai lớp sau không cần Docker với cấu hình hiện có. Vì thế “153 pass” lịch sử là kết quả bộ **có lọc**, không phải toàn bộ tests không cần Docker.

Một phạm vi rộng hơn, chưa chạy ở S05, là:

```powershell
.\mvnw.cmd test '-Dtest=!MySqlIntegrationTests,!PostgresIntegrationTests'
```

Lệnh này giữ hai integration tests không cần Docker; không dùng số lượng/kết quả của filter cũ cho nó. Đọc số tests thực chạy; `failIfNoTests=false` có thể che tình trạng run=0. Hướng dẫn cache, máy sạch, exit code và report chi tiết ở onboarding.

## C.4. Bằng chứng và thời điểm

| Kiểm tra | Thời điểm/nguồn | Kết quả | Phạm vi kết luận |
|---|---|---|---|
| Java, javac, Git | S05, 19/10/2026 khoảng 03:58 +07:00 | Các lệnh version exit 0; giá trị ở C.2 | Môi trường hiện tại |
| Maven wrapper | S05, 19/10/2026 khoảng 03:58 +07:00 | mvnw.cmd -v exit 0, Maven 3.9.16, JDK 21.0.12.1 | Wrapper khởi động được; không phải build/test pass |
| OS/shell/root/branch/POM | S05, lệnh đọc thực tế | Các giá trị C.1/C.2 | Không giả định đường dẫn của bản handover khác |
| Test model đơn lẻ | S04, 19/10/2026, kết thúc 03:51:06 +07:00 | 9 run, 0 failures/errors/skipped, exit 0 | Phiên trước; S05 không chạy lại |
| Ba lớp TV3 | S04, 19/10/2026, kết thúc 03:51:26 +07:00 | 45 run (27+9+9), 0 failures/errors/skipped, exit 0 | Phiên trước; đọc lại ba XML ở S05 |
| Owner package 130 tests | Handover lịch sử | Chưa tái hiện trong S05 | Không gọi là kết quả mới |
| Hồi quy có lọc 153 tests | Bổ sung 18/10, bản workspace khác | Historical, chưa chạy trong S05 | Không tương đương toàn suite |
| PIT 192/195, line 250/250 | Bổ sung 18/10, bản workspace khác | Historical; S05 không có target/pit-reports/index.html | S06 cần thực thi mới |
| Cài từ máy sạch / JDK 17 | Chưa thực hiện | Chưa kiểm chứng | Quy trình hướng dẫn, không phải nghiệm thu |
| Package / HTTP 8090 | Chưa thực hiện trong S05 | Chưa có log mới | Chưa demo |

S05 đọc lại ba file `target/surefire-reports/TEST-org.springframework.samples.petclinic.owner.<Class>.xml` với Class tương ứng:

| Class | Tests | Failures | Errors | Skipped | LastWriteTime +07:00, ngày 19/10/2026 |
|---|---|---|---|---|---|
| OwnerMutationTests | 27 | 0 | 0 | 0 | 03:51:24 |
| PetValidatorMutationTests | 9 | 0 | 0 | 0 | 03:51:24 |
| PetVisitModelMutationTests | 9 | 0 | 0 | 0 | 03:51:26 |

Các XML là artifact local có thể bị ghi đè, không phải tệp có sẵn khi clone. Snapshot báo cáo được đọc từ đúng ba lớp, không cộng XML cũ khác còn trong target. Lệnh S04 tương ứng:

```powershell
.\mvnw.cmd -B test '-Dtest=PetVisitModelMutationTests'
.\mvnw.cmd -B test '-Dtest=OwnerMutationTests,PetValidatorMutationTests,PetVisitModelMutationTests'
```

Bằng chứng 18/10 đã được S00 đọc tại `C:/Users/minht/Downloads/KiemThuPhanMem/bo-sung-tv3-2026-10-18/`; đường dẫn này thuộc máy người bàn giao, không là dependency hay đường dẫn bắt buộc của người nhận. PIT lần bổ sung đó ghi **28 tests examined**, khác metric 27 trong handover cũ; cả hai đều không phải tổng tests TV3/owner. Không đổi SURVIVED thành KILLED chỉ vì có phân tích equivalent.

S05 không lặp lại các bộ test đã pass khi không thay code; việc kiểm chứng toàn package, hồi quy và PIT thuộc S06.

## C.5. Quy tắc kết luận PASS, FAIL, BLOCKED

- **PASS:** lệnh test có exit 0, số tests và lớp chạy đúng phạm vi, không failures/errors; ghi skipped riêng. PIT cần report mới hợp lệ và đạt ngưỡng trong POM. Exit 0 của version/package bỏ test không chứng minh tests pass.
- **FAIL:** assertion/test error hoặc quality gate không đạt; ghi rõ case, exception và artifact. Nếu formatter chặn trước test thì gọi build fail, không bịa số test.
- **BLOCKED:** chưa thể kiểm chứng vì thiếu JDK/dependency, quyền truy cập, Docker khi chạy lớp Docker, cổng hoặc snapshot bàn giao. Giữ nguyên lỗi gốc; phân biệt lỗi môi trường với lỗi hành vi. Cấu hình POM/CI chuyển TV1, Controller chuyển TV4.
- **Chưa chạy:** không phải PASS hoặc FAIL. Dùng đúng nhãn này cho PIT/HTTP/máy sạch của S05.

Vị trí kết quả sau mỗi lần chạy: `target/surefire-reports/`, `target/pit-reports/index.html`, `target/pit-reports/mutations.xml`. Report không timestamped có thể bị ghi đè; khi thu evidence S06 cần gắn ngày giờ, revision và phạm vi lệnh. Không đưa cache/target vào commit nguồn.

## C.6. Phối hợp TV2/TV3: HTTP cổng 8090

TV2 phụ trách luồng ứng dụng và dữ liệu; TV3 hỗ trợ JDK/Maven/onboarding và trình bày kiểm thử Validator. Chỉ xác nhận demo sau khi có startup log và response thực tế.

| Luồng dự kiến | Chứng cứ cần có | Trạng thái S05 |
|---|---|---|
| GET /owners?lastName=Davis | Status đầu tiên, nội dung owner tìm được, timestamp | Chưa thực hiện |
| GET /owners/1 | Status và owner/pets đúng dữ liệu | Chưa thực hiện |
| GET /owners/1/pets/new | Status và form tạo pet | Chưa thực hiện |

Ghi riêng 200 và 3xx/Location; công cụ tự theo redirect có thể chỉ hiển thị 200 cuối cùng. Không nhận HTTP 200 là đủ chứng minh mọi field đúng, không nhận mở GET form là đã test POST. Hướng dẫn gọi request không tự theo redirect có trong onboarding. Không sửa DB/seed hoặc production để phục vụ S05.

## C.7. Trước/sau và việc còn lại

| Hạng mục | Trước S05 | Sau S05 |
|---|---|---|
| Onboarding ở branch hiện tại | Chưa có | Có quy trình JDK/Git/root/wrapper/test/PIT/package/HTTP và xử lý lỗi |
| Draft Phần C của TV3 | Chưa có | Có môi trường đo thực tế, bảng evidence phân biệt thời điểm và phạm vi |
| Filter integration | Cần diễn giải đúng | Nêu rõ hai lớp không cần Docker cũng bị loại |
| Kiểm chứng máy sạch/HTTP/PIT mới | Chưa có | Vẫn chưa chạy; không gán thành tích từ hướng dẫn |
| Docs thiết kế S01 | Không có ở branch hiện tại | Vẫn cần tích hợp từ commit 1f1091b ở phiên phù hợp |

Checklist nghiệm thu máy sạch nằm ở C.8 của onboarding; chưa đánh dấu thay người thực hiện. S05 chỉ thay hai tài liệu trong docs/tv3, không chỉnh bản báo cáo chung, không tạo commit/PR và không chạy ứng dụng. **Next: S06** để thu test/PIT evidence hiện tại; S07 đối chiếu docs và đóng gói bàn giao.
