# Phần C — Onboarding Windows từ máy sạch (TV3)

## C.1. Phạm vi và môi trường tham chiếu

Cập nhật S05 ngày **19/10/2026**. TV3 phụ trách hướng dẫn cài đặt, build/test và phối hợp TV2 trong demo HTTP. Đây là hướng dẫn thực hiện trên máy sạch; S05 **chưa thử cài mới trên máy sạch**, chưa chạy lại test/PIT và chưa khởi động ứng dụng. Bằng chứng, thời điểm và giới hạn nằm trong [bản nháp Phần C TV3](REPORT_C_TV3_DRAFT.md).

| Thành phần | Giá trị đo/cấu hình của workspace |
|---|---|
| OS | Microsoft Windows 11 Home Single Language, 10.0.26200, build 26200, 64-bit |
| Shell | Windows PowerShell 5.1.26100.9711, PSEdition Desktop |
| JDK chạy Maven | Eclipse Temurin 21.0.12.1+1-LTS, javac 21.0.12.1 |
| Java mục tiêu | 17 trong POM; Enforcer yêu cầu tối thiểu theo java.version |
| Maven / wrapper script | Maven 3.9.16 / wrapperVersion 3.3.4 |
| Git đang cài | 2.55.0.windows.5 |
| Spring Boot parent | 4.1.0 |
| PIT / JUnit adapter | pitest-maven 1.30.0 / pitest-junit5-plugin 1.2.3 |
| PIT scope / mutators / ngưỡng | owner.* cho cả classes và tests; STRONGER; mutation ≥88%, line ≥95% |
| CSDL mặc định | H2, schema/data nạp theo application.properties |

Nguồn cấu hình: [pom.xml](../../pom.xml), [wrapper properties](../../.mvn/wrapper/maven-wrapper.properties), [application.properties](../../src/main/resources/application.properties).

**JDK thực thi khác Java mục tiêu:** Maven/Javac đang chạy trên JDK 21. POM đặt Java mục tiêu 17; log S04 ghi javac `release 17`. Điều này không chứng minh toàn bộ ứng dụng/dependency đã chạy trên JDK 17. Yêu cầu tài liệu là JDK tối thiểu 17; bàn giao bổ sung và máy hiện tại dùng Temurin 21.0.12.1. Máy dùng JDK 17 cần chạy kiểm chứng riêng. Số phiên bản adapter PIT 1.2.3 không phải phiên bản JUnit Jupiter.

## C.2. Cài công cụ và kiểm tra JAVA_HOME/PATH

1. Cài Temurin **JDK 21 Windows x64** để cùng major version với môi trường đã kiểm chứng; chọn gói JDK, không chỉ JRE. Trong bộ cài MSI, bật PATH và JAVA_HOME theo [hướng dẫn Adoptium](https://adoptium.net/installation/windows/). Ghi lại phiên bản thực cài, không mặc định bản tải mới trùng patch 21.0.12.1.
2. Cài Git từ [trang Git for Windows chính thức](https://git-scm.com/install/windows). Không bắt buộc máy mới phải có đúng phiên bản Git đang đo trên máy TV3.
3. Mở PowerShell mới. Thay đường dẫn ví dụ dưới đây bằng thư mục JDK thực tế nếu cần.

```powershell
$jdkPath = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot'
if (-not (Test-Path -LiteralPath "$jdkPath\bin\javac.exe")) {
    throw 'Thay $jdkPath bằng thư mục JDK đã cài, không phải thư mục bin.'
}

# Chỉ áp dụng cho terminal hiện tại.
$env:JAVA_HOME = $jdkPath
$env:Path = "$jdkPath\bin;$env:Path"

$env:JAVA_HOME
Get-Command java, javac | Select-Object Name, Source
java -version
javac -version
git --version
```

Nếu muốn lưu lâu dài, dùng tùy chọn của installer hoặc Environment Variables của tài khoản Windows, giữ các mục PATH khác và mở terminal mới để kiểm tra. S05 không thay biến môi trường hệ thống/tài khoản.

`JAVA_HOME` phải trỏ tới gốc JDK có `bin\java.exe` và `bin\javac.exe`. PowerShell dùng `$env:JAVA_HOME`; cú pháp `%JAVA_HOME%` dành cho CMD. Sau khi vào repo, `.\mvnw.cmd -v` phải báo đúng JDK đã chọn; chỉ nhìn `java -version` chưa đủ.

## C.3. Lấy đúng repo của nhóm và xác nhận revision

Với máy hiện tại, thư mục root đã xác minh là:

```powershell
Set-Location -LiteralPath 'C:\Users\minht\Downloads\KiemThuPhanMem\Program\Mutation-Testing_-Spring-PetClinic-System'
```

**Chỉ trên máy mới hoặc thư mục clone mới**, có thể lấy repo nhóm theo quy trình dưới đây. Thư mục đích PetClinic-TV3 phải chưa tồn tại; không chạy đoạn này để thay thế working tree đang làm.

```powershell
$checkoutParent = Join-Path $env:USERPROFILE 'source'
New-Item -ItemType Directory -Force -Path $checkoutParent | Out-Null
Set-Location -LiteralPath $checkoutParent
git clone 'https://github.com/idewithasmile/Mutation-Testing_-Spring-PetClinic-System.git' 'PetClinic-TV3'
if ($LASTEXITCODE -ne 0) { throw 'Clone thất bại; kiểm tra quyền truy cập/mạng.' }
Set-Location -LiteralPath 'PetClinic-TV3'
git status --short
git branch --show-current
git log -1 --oneline
```

TV1 cần cung cấp branch/commit bàn giao có đủ test nhóm và cấu hình PIT. Snapshot S05 tại máy TV3 là `41c65b07636448fc92d44e7d641e63d1ca0ee59b`, branch `TranMinhTai/Sessio4` (đúng tên đang có). S05 không kiểm tra snapshot đó đã có trên remote. Nếu clone mới chứa commit này, để tái hiện đúng snapshot có thể chạy riêng:

```powershell
# Chỉ trong clone mới, working tree sạch; detached HEAD phục vụ tái hiện.
git switch --detach 41c65b07636448fc92d44e7d641e63d1ca0ee59b
if ($LASTEXITCODE -ne 0) {
    throw 'Chưa có commit bàn giao trong clone; liên hệ TV1 để nhận đúng branch/snapshot.'
}
```

Nếu nhận ZIP, lấy **bộ repo nhóm đầy đủ** từ TV1, giữ cả `.mvn`, wrapper, POM và các test bổ sung. Các lệnh Git không áp dụng khi ZIP không có `.git`; cần ghi mã revision mà TV1 xác nhận. Chỉ clone Spring PetClinic upstream tại pinned SHA chưa có đầy đủ công việc nhóm.

Từ root chứa POM, kiểm tra trước khi chạy:

```powershell
$requiredPaths = @(
    'pom.xml',
    'mvnw.cmd',
    '.mvn\wrapper\maven-wrapper.properties',
    'src\test\java\org\springframework\samples\petclinic\owner\OwnerMutationTests.java',
    'src\test\java\org\springframework\samples\petclinic\owner\PetValidatorMutationTests.java',
    'src\test\java\org\springframework\samples\petclinic\owner\PetVisitModelMutationTests.java'
)
foreach ($requiredPath in $requiredPaths) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Thiếu tệp bàn giao: $requiredPath"
    }
}
Get-Location
Get-Content -LiteralPath '.mvn\wrapper\maven-wrapper.properties'
.\mvnw.cmd -v
if ($LASTEXITCODE -ne 0) { throw 'Maven Wrapper chưa sẵn sàng.' }
```

Kiểm tra pinned base bằng lệnh chỉ đọc nếu là Git clone:

```powershell
git merge-base --is-ancestor 500158f732419217507c7656904b8e6aa1bcc0d6 HEAD
$LASTEXITCODE
```

Exit 0 nghĩa là HEAD có pinned base trong lịch sử. Không yêu cầu HEAD bằng pinned base; không reset hoặc checkout working tree đang làm về SHA gốc. Nhánh S05 hiện chưa có hai tài liệu thiết kế S01; chúng tồn tại ở commit `1f1091b`. Việc tích hợp docs từ branch khác cần xử lý ở phiên bàn giao, không tự coi docs đã có trong clone.

Wrapper tải Maven từ URL đã ghi trong properties (repo.maven.apache.org), sau đó Maven tải dependency theo cấu hình của dự án/settings. Máy sạch cần mạng ở lần đầu, **không thêm `-o`**. Cache mặc định ở `$env:USERPROFILE\.m2`; máy hiện tại dùng cache này. Nếu có lỗi quyền ghi, chọn cache có quyền hợp lệ hoặc yêu cầu cấp quyền; không coi cache ngoài repo của một máy cũ là điều kiện bắt buộc. Không sao chép cache vào Git/bài nộp.

## C.4. Chạy kiểm thử tăng dần

Chạy từ root, trong PowerShell. Dừng sau mỗi lỗi, giữ nguyên console output và report để phân tích. Tất cả lệnh dưới đây là **hướng dẫn**, không phải các lần chạy mới ở S05.

```powershell
# 1. Ba lớp TV3.
.\mvnw.cmd test '-Dtest=OwnerMutationTests,PetValidatorMutationTests,PetVisitModelMutationTests'
if ($LASTEXITCODE -ne 0) { throw 'TV3 thất bại; đọc Surefire trước khi tiếp tục.' }

# 2. Toàn bộ test trong package owner.
.\mvnw.cmd test '-Dtest=org.springframework.samples.petclinic.owner.**'
if ($LASTEXITCODE -ne 0) { throw 'Owner thất bại; đọc Surefire trước khi tiếp tục.' }

# 3. Bộ hồi quy theo filter báo cáo của nhóm.
.\mvnw.cmd test '-Dtest=!*IntegrationTests' '-DfailIfNoTests=false'
if ($LASTEXITCODE -ne 0) { throw 'Hồi quy có lọc thất bại.' }
```

Tham chiếu số lượng: TV3 45 methods; lịch sử owner 130 tests và bộ có lọc 153 tests. Đọc số thực tế mỗi lần chạy. `-DfailIfNoTests=false` có thể cho phép build thành công khi không tìm thấy test, nên phải kiểm tra thêm **Tests run > 0** và đúng danh sách lớp. Không chỉ dựa vào BUILD SUCCESS.

Các lớp tích hợp hiện có và tác dụng filter:

| Lớp | Có cần Docker để thực thi nội dung test? | Bị loại bởi !*IntegrationTests? |
|---|---|---|
| MySqlIntegrationTests | Có, MySQL Testcontainers; có cơ chế skip khi thiếu Docker | Có |
| PostgresIntegrationTests | Có, PostgreSQL/Docker Compose và kiểm tra Docker | Có |
| PetClinicIntegrationTests | Không với cấu hình H2 mặc định; khởi động server cổng ngẫu nhiên | Có |
| CrashControllerIntegrationTests | Không; ứng dụng test riêng, loại auto-configuration DB, server cổng ngẫu nhiên | Có |

Vì vậy gọi đúng là **“bộ hồi quy loại các lớp *IntegrationTests”**, không phải toàn bộ tests không cần Docker. Nguồn: [PetClinicIntegrationTests](../../src/test/java/org/springframework/samples/petclinic/PetClinicIntegrationTests.java), [CrashControllerIntegrationTests](../../src/test/java/org/springframework/samples/petclinic/system/CrashControllerIntegrationTests.java), [MySqlIntegrationTests](../../src/test/java/org/springframework/samples/petclinic/MySqlIntegrationTests.java), [PostgresIntegrationTests](../../src/test/java/org/springframework/samples/petclinic/PostgresIntegrationTests.java).

Nếu muốn chạy cả các integration tests không cần Docker, dùng **thay cho bước 3**, với cấu hình mặc định:

```powershell
.\mvnw.cmd test '-Dtest=!MySqlIntegrationTests,!PostgresIntegrationTests'
if ($LASTEXITCODE -ne 0) { throw 'Bộ test loại hai lớp Docker thất bại.' }
```

Lệnh này chưa được chạy trong S05; có thêm Spring context/HTTP local nên cần quyền mở cổng. Không gắn số 153 của bộ lọc cũ cho lệnh này, và không tuyên bố đã kiểm tra hai lớp Docker. Không cần chạy cả hai filter cho mỗi thay đổi nhỏ.

## C.5. PIT, report và build

POM hiện có quality gates 88/95, output HTML+XML và `timestampedReports=false`. Dùng lệnh:

```powershell
.\mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage '-Djacoco.skip=true'
if ($LASTEXITCODE -ne 0) { throw 'PIT thất bại hoặc chưa đạt quality gate; đọc log/report.' }
Test-Path -LiteralPath 'target\pit-reports\index.html'
Test-Path -LiteralPath 'target\pit-reports\mutations.xml'
```

`'-Djacoco.skip=true'` được quote nguyên tham số PowerShell, tránh tách nhầm và tránh JaCoCo agent can thiệp PIT theo bàn giao. Không thay scope owner.* để nâng điểm. Mở `target/pit-reports/index.html` bằng trình duyệt sau khi lệnh hoàn tất; XML ở `target/pit-reports/mutations.xml`. Đây là đường dẫn output dự kiến, không phải artifact có sẵn trong clone. Surefire XML/text ở `target/surefire-reports/`.

Ghi giờ bắt đầu/kết thúc, exit code, số tests/failures/errors/skipped và timestamp của report. Surefire có thể giữ XML của lần chạy cũ: chỉ tổng hợp các lớp thuộc lần chạy vừa thực thi, không cộng bừa mọi XML còn trong target. PIT `tests examined` là metric riêng, không phải tổng test suite. Đọc KILLED/SURVIVED/NO_COVERAGE từ XML và line coverage từ HTML/log; kết luận tương đương không tự đổi SURVIVED thành KILLED.

Sau khi các kiểm thử cần thiết đạt, có thể đóng gói:

```powershell
.\mvnw.cmd package '-DskipTests'
if ($LASTEXITCODE -ne 0) { throw 'Đóng gói thất bại.' }
Get-ChildItem -LiteralPath target -Filter '*.jar'
```

`-DskipTests` bỏ thực thi test ở bước package; không dùng BUILD SUCCESS của lệnh đó làm bằng chứng tests pass. S05 chưa thực hiện package.

## C.6. Chạy ứng dụng và phối hợp HTTP TV2/TV3

Dùng terminal riêng tại root:

```powershell
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.arguments=--server.port=8090'
```

Chờ log `Started PetClinicApplication` và xác nhận cổng 8090. Dừng bằng Ctrl+C trong terminal chạy ứng dụng. Không cần cài H2/MySQL/PostgreSQL cho profile mặc định: [schema H2](../../src/main/resources/db/h2/schema.sql) và [seed H2](../../src/main/resources/db/h2/data.sql) được application.properties chỉ định. Không sửa seed để ép demo thành công.

TV2 dẫn dắt demo luồng nghiệp vụ; TV3 hỗ trợ onboarding, runtime và giải thích Validator. Các URL cần thu chứng cứ khi thực hiện demo:

| URL cổng 8090 | Nội dung cần kiểm tra | S05 |
|---|---|---|
| /owners?lastName=Davis | Kết quả tìm owner đúng dữ liệu, ghi status và nội dung | Chưa gọi |
| /owners/1 | Chi tiết đúng owner/pets, ghi status và nội dung | Chưa gọi |
| /owners/1/pets/new | Form tạo pet, ghi status và nội dung | Chưa gọi |

Để xem response đầu tiên, có thể dùng `curl.exe` nếu đã cài, không dùng alias `curl` của Windows PowerShell. Lệnh dưới không tự theo redirect vì không có `-L`:

```powershell
curl.exe -i 'http://localhost:8090/owners?lastName=Davis'
curl.exe -i 'http://localhost:8090/owners/1'
curl.exe -i 'http://localhost:8090/owners/1/pets/new'
```

Nếu thiếu curl.exe, dùng Network panel của trình duyệt và ghi rõ chuỗi request/redirect. Phân biệt HTTP 200, 3xx kèm Location và lỗi kết nối; status 200 chưa đủ để khẳng định dữ liệu đúng. Các GET trên không chứng minh form POST tạo pet thành công. Lưu log khởi động, timestamp và response/screenshot khi demo thật; không dùng bảng kỳ vọng làm log.

## C.7. Phân biệt FAIL/BLOCKED và xử lý

| Dấu hiệu | Phân loại và hành động |
|---|---|
| Không tìm thấy java/javac, JAVA_HOME sai | BLOCKED môi trường: kiểm tra JDK, PATH, JAVA_HOME và mvnw -v |
| Không thấy pom.xml/mvnw.cmd/.mvn | BLOCKED sai root hoặc gói bàn giao thiếu; kiểm tra C.3 |
| Dependency/plugin không tải được, proxy/TLS hoặc AccessDenied cache | BLOCKED môi trường/quyền; giữ lỗi gốc, kiểm tra mạng/settings với TV1; không đổi nguồn tải tùy ý |
| Formatter/Checkstyle chặn trước Surefire | Build FAIL trước test; không ghi tests fail hoặc 0 tests pass. Chỉ sửa file thuộc phạm vi được giao |
| Surefire failures/errors >0 | FAIL kiểm thử; xem assertion/stack trace, phân biệt lỗi test/logic và lỗi môi trường |
| No tests were executed hoặc run=0 | Chưa có bằng chứng kiểm thử, dù failIfNoTests=false cho exit 0 |
| Mockito dynamic agent warning nhưng tests pass, exit 0 | Ghi warning riêng; không gọi là FAIL, không tự sửa POM ngoài phạm vi TV3 |
| PIT minion crash | Chưa có mutation result hợp lệ; kiểm tra JaCoCo skip, JDK/PIT/adapter, chuyển TV1 nếu thuộc cấu hình |
| PIT score thấp hơn ngưỡng | Quality gate FAIL; ghi score thực tế và survivors, không chép số lịch sử |
| Cổng 8090 bị chiếm | BLOCKED demo; kiểm tra tiến trình đang dùng cổng; phối hợp đổi port, không tự dừng tiến trình lạ |
| Lệnh cần metadata OS bị Access denied | Ghi giới hạn quyền đọc; không suy ra Java/test đang lỗi. Dùng kết quả OS thực sự đọc được |

Mọi lỗi đều cần giữ exit code và bằng chứng; không biến mọi BUILD FAILURE thành lỗi production. Phạm vi TV3 không bao gồm sửa POM/CI/Controller.

## C.8. Checklist nghiệm thu từ máy sạch

Các ô dưới là việc người thực hiện trên máy sạch phải xác nhận, **chưa được đánh dấu hoàn thành bởi S05**:

- [ ] Cài JDK và Git từ nguồn chính thức; mở terminal mới.
- [ ] java, javac, JAVA_HOME và mvnw -v cùng trỏ tới JDK dự kiến.
- [ ] Nhận đúng repo/revision nhóm; có POM, wrapper, .mvn và các test bổ sung.
- [ ] Lần đầu tải Maven/dependencies thành công; ghi version thực tế.
- [ ] Chạy TV3, owner và chọn đúng bộ hồi quy; ghi số test, failures/errors/skipped, exit.
- [ ] Chạy PIT với jacoco.skip; đọc HTML/XML mới, đối chiếu ngưỡng 88/95.
- [ ] Nếu cần package, chỉ bỏ chạy test sau khi có bằng chứng kiểm thử.
- [ ] Phối hợp TV2 chạy HTTP 8090; lưu startup log/status/nội dung thật; chưa mặc định đã demo.
- [ ] Lưu report theo từng lần chạy và revision; kiểm tra Git diff không lẫn target/cache.
