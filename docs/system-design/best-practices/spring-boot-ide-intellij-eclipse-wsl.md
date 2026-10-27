---
title: Phát triển Spring Boot với IntelliJ IDEA và Eclipse Linux trên WSL Ubuntu
description: Hướng dẫn cấu hình IDE cho dự án Spring Boot sử dụng JDK, Maven, Git và Docker đã có sẵn trong WSL Ubuntu.
tags:
  - spring-boot
  - java
  - wsl
  - ubuntu
  - intellij-idea
  - eclipse
  - wslg
---

# Phát triển Spring Boot với IntelliJ IDEA và Eclipse Linux trên WSL Ubuntu

> **Mục tiêu:** Giữ source code, JDK 17 (Amazon Corretto), Maven, Git và Docker Engine trong **WSL Ubuntu**; sử dụng một trong hai IDE: **IntelliJ IDEA cài trên Windows** hoặc **Eclipse/Spring Tools chạy trong Ubuntu bằng WSLg**.
>
> **Phạm vi:** Các công cụ JDK/Maven/Git/Docker **đã được cài đặt và cấu hình**. Tài liệu **không hướng dẫn cài đặt lại** chúng; chỉ kiểm tra và kết nối IDE với môi trường hiện có.

!!! tip "Khuyến nghị"
    - **IntelliJ IDEA Windows + WSL:** phù hợp nếu ưu tiên khả năng refactor Java và trải nghiệm IDE native Windows. Chọn **JDK/Git trong WSL**, kiểm tra Maven và Run/Debug thực sự dùng Ubuntu.
    - **Eclipse Linux/Spring Tools + WSLg:** phù hợp nếu muốn tiếp tục sử dụng Eclipse, đồng thời cho IDE, công cụ build và source code chạy trong **cùng môi trường Linux**.
    - Không cần Docker Desktop nếu Docker Engine trong WSL đã hoạt động và IDE/CLI sử dụng được Docker socket của Ubuntu.

## 1. Kiến trúc và nguyên tắc chung

```text
Windows 11
├── IntelliJ IDEA (Windows GUI)  ─────┐
├── Windows desktop / Browser         │
└── WSLg hiển thị Eclipse Linux ──────┤
                                      │
WSL 2 - Ubuntu                        │
├── /home/<linux-user>/workspace/  ◄──┘
│   └── backend/my-spring-app/
├── Amazon Corretto JDK 17 (đã có)
├── Maven / Maven Wrapper (đã có)
├── Git Linux (đã có)
├── Docker Engine + Docker CLI (đã có)
├── Eclipse / Spring Tools Linux (phương án B)
└── Maven local repository: ~/.m2/repository
```

!!! warning "Không nhầm đường dẫn Windows và Linux"
    - Dự án trong WSL: `/home/<linux-user>/workspace/backend/my-spring-app`.
    - Truy cập cùng dự án từ Windows: `\\wsl.localhost\Ubuntu\home\<linux-user>\workspace\backend\my-spring-app`.
    - **Không** copy dự án sang `C:\` chỉ để IDE mở được.
    - Tránh dùng đồng thời Git for Windows và Git Ubuntu để merge/rebase trên cùng working tree; nên thống nhất Git Ubuntu.

### 1.1. Kiểm tra một lần các công cụ sẵn có

Trong **Ubuntu terminal**:

```bash
printf 'Linux user: %s\n' "$USER"
printf 'Distro: '; grep '^PRETTY_NAME=' /etc/os-release
printf '\nExecutables:\n'
for tool in java javac mvn git docker; do
  printf '%-8s %s\n' "$tool" "$(command -v "$tool" || echo NOT_FOUND)"
done

java -version
mvn -version
git --version
docker info --format 'Docker server: {{.ServerVersion}}'

# Đường dẫn JDK thực sự (không đoán theo tên thư mục)
JDK_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")"
printf 'JDK_HOME=%s\n' "$JDK_HOME"
```

Kỳ vọng: `java`, `javac`, `mvn`, `git` và `docker` xuất phát từ **Ubuntu**; Maven dùng **JDK 17**; Docker kết nối được daemon.

!!! note "Nếu dự án có Maven Wrapper"
    Ưu tiên `./mvnw` để build theo phiên bản Maven được dự án quy định. Không cần gỡ Maven đã cài trong Ubuntu. Kiểm tra `./mvnw -version` trước khi sử dụng.

### 1.2. Lưu source code ở đâu?

```bash
mkdir -p ~/workspace/backend
cd ~/workspace/backend
# Nếu repository chưa được clone:
# git clone <repository-url> my-spring-app
cd my-spring-app
pwd
```

Lưu dự án trên filesystem Linux (ví dụ `/home/...`) giúp Maven, Git và Docker bind mounts hạn chế overhead khi thao tác hàng nghìn file so với thư mục `/mnt/c/...`.

---

## 2. Phương án A — IntelliJ IDEA Windows + WSL Ubuntu

### 2.1. Cơ chế hoạt động

IntelliJ IDEA chạy **giao diện và IDE process trên Windows** nhưng có hỗ trợ chính thức **mở project nằm trong WSL**, chọn JDK/Git WSL, và **run/debug ứng dụng trong WSL**. Đây **không phải** mô hình tương tự VS Code Remote WSL, nơi extension host chạy trong distro.

Tài liệu chính thức: [JetBrains — WSL](https://www.jetbrains.com/help/idea/how-to-use-wsl-development-environment-in-product.html).

### 2.2. Cài IDE trên Windows

1. Cài **IntelliJ IDEA** từ [JetBrains](https://www.jetbrains.com/idea/download/).
2. Khởi động IntelliJ trên Windows (không cần cài thêm IntelliJ Linux).
3. **Không** cài lại JDK/Maven/Git/Docker trên Windows chỉ để mở project WSL.

!!! info "Tính năng theo phiên bản/gói cấp phép"
    IDE có tính năng Java cốt lõi, nhưng một số tính năng chuyên sâu về Spring yêu cầu quyền sử dụng Ultimate. Cần kiểm tra phiên bản IDE và quyền truy cập đang dùng. Nội dung bên dưới tập trung vào Java/Maven/WSL thông thường.

### 2.3. Mở project Maven nằm trong WSL

Trong IntelliJ chọn **File → Open**, nhập hoặc điều hướng tới:

```text
\\wsl.localhost\Ubuntu\home\<linux-user>\workspace\backend\my-spring-app
```

- Chọn thư mục chứa `pom.xml` của parent/root module (nếu là dự án Maven multi-module).
- Đợi IntelliJ index source code và import/sync Maven.
- **Không** chọn thư mục copy trên Windows nếu mục tiêu là build với Ubuntu.

!!! note "Khả năng nhận diện WSL"
    IntelliJ hỗ trợ `\\wsl.localhost\...` và có cơ chế nhận diện WSL cho JDK/Git. Nếu IDE không tự nhận đúng, kiểm tra các mục cấu hình tiếp theo thay vì giả định tất cả công cụ đã chạy trong Linux.

### 2.4. Chọn Amazon Corretto 17 từ WSL

Trong IntelliJ:

1. **File → Project Structure → SDKs → Add SDK → JDK**.
2. Chọn JDK nằm trong WSL; dùng `JDK_HOME` đã kiểm tra ở phần 1.1 để tìm vị trí tương ứng.
3. **Project → SDK:** chọn JDK 17 từ WSL.
4. Với từng module: kiểm tra **Modules → Dependencies → Module SDK / Language level**.

Ví dụ: nếu `JDK_HOME` trong Linux là `/usr/lib/jvm/...`, vị trí tương ứng từ Windows sẽ nằm dưới:

```text
\\wsl.localhost\Ubuntu\usr\lib\jvm\...
```

**Không** tự gõ tên thư mục `java-17-amazon-corretto` nếu máy không có thư mục đó.

### 2.5. Cấu hình Maven project

Trong **Settings → Build, Execution, Deployment → Build Tools → Maven**:

- **Maven home path:** ưu tiên *Maven Wrapper* nếu project có `.mvn/wrapper`; nếu chọn Maven khác, bảo đảm thuộc môi trường phù hợp với project WSL.
- **Runner → JRE:** chọn JDK WSL 17 / Project JDK.
- **Importing → JDK for importer:** kiểm tra JDK sử dụng cho import.
- Kiểm tra `settings.xml`, repository local và profile riêng của môi trường Ubuntu nếu dự án yêu cầu.

Trong **Ubuntu terminal**, xác minh phiên bản build chuẩn của dự án:

```bash
cd ~/workspace/backend/my-spring-app
if [[ -x ./mvnw ]]; then
  ./mvnw -version
  ./mvnw -DskipTests package
else
  mvn -version
  mvn -DskipTests package
fi
```

!!! warning "Phân biệt Maven chạy trong IDE và Maven ngoài terminal"
    Việc `mvn -version` trong Ubuntu đúng **không chứng minh** Maven Runner của IntelliJ cũng đang dùng JDK/Maven Ubuntu. Kiểm tra **Maven settings**, **Run Configuration** và console của lần chạy trong IDE. Nếu không tương thích môi trường, build bằng terminal Ubuntu là đường kiểm chứng chuẩn.

JetBrains yêu cầu bật thành phần **Remote Execution Agent: Binary Files** để hỗ trợ dự án Maven/Gradle chạy trên WSL; kiểm tra trạng thái plugin/tính năng nếu quá trình Maven import hoặc remote execution gặp lỗi.

### 2.6. Chạy và debug Spring Boot trong WSL

- Mở class có `@SpringBootApplication`.
- Tạo/chọn **Application Run Configuration**, kiểm tra JDK/target được IDE gán cho **WSL**.
- Run hoặc Debug; xác minh process Java thực sự xuất hiện trong Ubuntu:

```bash
ps -ef | grep '[j]ava'
```

Hoặc dùng terminal Ubuntu để chạy chuẩn trước:

```bash
cd ~/workspace/backend/my-spring-app
./mvnw spring-boot:run     # Nếu dự án có Maven Wrapper
# hoặc: mvn spring-boot:run
```

Nếu IDE không chạy trong WSL như mong muốn, kiểm tra **Run → Edit Configurations**, Project SDK và khả năng chọn WSL run target theo phiên bản IDE. Với project nằm trong WSL, JetBrains có cơ chế run/debug trực tiếp mà không cần chuyển code ra Windows.

### 2.7. Git từ Ubuntu trong IntelliJ

Vào **Settings → Version Control → Git**:

- Kiểm tra **Path to Git executable** trỏ tới Git của WSL.
- Nếu cần chọn thủ công, dùng vị trí Git WSL, ví dụ:

```text
\\wsl$\Ubuntu\usr\bin\git
```

- Nhấn **Test** để xác minh.
- Dùng terminal Ubuntu cho các thao tác chuẩn hóa trong nhóm: `git status`, `git fetch`, `git merge`, `git rebase`.

**Lưu ý:** IntelliJ có Git GUI riêng. Nếu muốn dùng **TortoiseGitMerge** đã cấu hình như custom Git mergetool, hãy chạy `git mergetool` từ Ubuntu terminal; nút Resolve Conflicts của IntelliJ không mặc định mở TortoiseGitMerge.

### 2.8. Docker và Spring Boot

Docker Engine đã chạy trong WSL, vì vậy cách chắc chắn nhất là quản lý container từ Ubuntu:

```bash
docker ps
docker compose ps
```

Nếu IntelliJ có tính năng Docker integration và bạn muốn dùng GUI, cấu hình kết nối tới Docker Engine trong WSL phù hợp với phiên bản IDE; **không cần expose Docker daemon ra TCP không mã hóa**. Trong mọi trường hợp, CLI Ubuntu vẫn có thể dùng Docker Engine đã cài.

---

## 3. Phương án B — Eclipse Linux / Spring Tools + WSLg

### 3.1. Cơ chế hoạt động

Khác IntelliJ Windows, phương án này chạy **toàn bộ tiến trình Eclipse trên Ubuntu**. Windows 11 chỉ hiển thị cửa sổ qua WSLg. IDE, Java project, Git CLI và Maven nằm cùng Linux filesystem.

```text
Windows 11 desktop
   └── WSLg (GUI bridge)
         └── Eclipse / Spring Tools Linux process
                ├── Spring Boot project: /home/<user>/workspace/backend/...
                ├── JDK project: Corretto 17 trong Ubuntu
                ├── Maven/m2e và CLI Ubuntu
                ├── Git CLI Ubuntu
                └── Docker Engine Ubuntu
```

Hướng dẫn WSLg chính thức: [Microsoft — Run Linux GUI apps with WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

### 3.2. Kiểm tra WSLg (không cài lại WSL)

Trong **Windows PowerShell**:

```powershell
wsl --version
wsl -l -v
```

Distro `Ubuntu` phải là **WSL 2**. Phiên bản WSL có WSLg sẽ được hiển thị trong kết quả `wsl --version`.

Trong Ubuntu:

```bash
printf 'DISPLAY=%s\n' "$DISPLAY"
printf 'WAYLAND_DISPLAY=%s\n' "$WAYLAND_DISPLAY"
ls -ld /mnt/wslg 2>/dev/null || true
```

Nếu muốn kiểm thử GUI và chưa có chương trình đồ họa:

```bash
# Chỉ cài công cụ kiểm tra giao diện (không phải JDK/Maven/Git/Docker)
sudo apt update
sudo apt install -y x11-apps
xclock
```

Nếu cửa sổ đồng hồ hiện trên Windows, WSLg đã hiển thị được ứng dụng Linux.

### 3.3. Chọn và cài Eclipse/Spring Tools Linux

**Ưu tiên:** tải gói **Spring Tools for Eclipse (Linux)** từ [spring.io/tools](https://spring.io/tools/), vì đã có sẵn các công cụ phục vụ Spring Boot.

**Lựa chọn khác:** tải [Eclipse IDE for Enterprise Java and Web Developers](https://www.eclipse.org/downloads/packages/), sau đó cài Spring Tools từ **Help → Eclipse Marketplace** hoặc [update site chính thức](https://github.com/spring-projects/spring-tools/wiki/Installation).

!!! important "Spring Tools 5 và Java 17"
    Tính đến tháng 10/2026, Spring Tools for Eclipse là nhánh **5.x**. Bản phân phối Spring Tools 5 đi kèm **JDK 25 để chạy IDE**, nhưng **dự án Spring Boot vẫn có thể biên dịch/chạy với Corretto 17 đã cài** bằng cách chọn JDK project phù hợp. **Không** thay JDK project sang 25 chỉ vì IDE dùng JDK 25. Spring Tools 5 yêu cầu Eclipse phiên bản tương thích (tối thiểu Eclipse 2025-12 theo FAQ chính thức).

Tải **Linux x86_64** nếu kiến trúc Ubuntu là `x86_64`:

```bash
uname -m
```

Từ Ubuntu, lưu file tải về ở `~/Downloads`. Nếu gói là `tar.gz`, có thể giải nén như sau (đổi đúng tên file thực tế đã tải):

```bash
mkdir -p ~/opt/spring-tools
# Ví dụ khi bạn đã đổi tên file vừa tải thành spring-tools-linux.tar.gz:
tar -xzf ~/Downloads/spring-tools-linux.tar.gz -C ~/opt/spring-tools

# Liệt kê để tìm launcher thực tế trong gói
find ~/opt/spring-tools -maxdepth 4 -type f \
  \( -name 'SpringToolSuite*' -o -name 'eclipse' \) -print
```

Để mở IDE, chạy **đúng file launcher tìm được** từ terminal Ubuntu, chẳng hạn:

```bash
# Ví dụ áp dụng cho gói Eclipse thuần có launcher này:
# ~/opt/eclipse/eclipse
# Gói Spring Tools có thể dùng tên launcher khác; kiểm tra bằng find ở trên.
```

!!! note "Không dùng Eclipse Windows executable trong WSL"
    Launcher phải là binary **Linux**; không chạy file `eclipse.exe` hay `SpringToolSuite*.exe` của Windows nếu mục tiêu là Eclipse Linux + WSLg.

### 3.4. Workspace và project

Nên tách **Eclipse workspace metadata** khỏi thư mục source Git:

```text
/home/<linux-user>/workspace/
├── backend/
│   └── my-spring-app/         # Git repository / pom.xml
└── eclipse-workspace/         # Eclipse workspace metadata
```

Tạo nơi lưu workspace:

```bash
mkdir -p ~/workspace/eclipse-workspace
```

Trong Eclipse, chọn workspace trên; sau đó **File → Import → Maven → Existing Maven Projects** và trỏ tới:

```text
/home/<linux-user>/workspace/backend/my-spring-app
```

Đối với Maven multi-module, import từ `pom.xml` gốc để m2e nhận diện đủ modules.

### 3.5. Cấu hình JDK 17 cho dự án (không cài lại JDK)

Trong **Ubuntu terminal** lấy đường dẫn JDK:

```bash
JDK_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")"
echo "$JDK_HOME"
```

Trong Eclipse:

1. **Window → Preferences → Java → Installed JREs**.
2. Chọn **Add → Standard VM** và trỏ tới `$JDK_HOME` thật (thư mục có `bin/java`, `bin/javac`).
3. Đặt runtime thích hợp cho **project**.
4. Kiểm tra **Project → Properties → Java Build Path**, **Java Compiler** và **Project Facets** (nếu có).
5. Trong **Run Configurations** của Spring Boot, kiểm tra JRE của ứng dụng là **Corretto 17**.

!!! tip "IDE JDK khác Project JDK là bình thường"
    Spring Tools/Eclipse có thể chạy bằng runtime được đóng gói; **Java Compiler compliance**, **Run Configuration JRE** và Maven build của project vẫn phải tuân theo `pom.xml` (Java 17).

### 3.6. Maven trong Eclipse Linux

Eclipse tích hợp **m2e** để import và quản lý dự án Maven. Vào **Window → Preferences → Maven → Installations** để xem Maven runtime. Nếu cần Maven ngoài, cấu hình Maven Ubuntu đã cài; nếu dự án dùng Maven Wrapper, vẫn ưu tiên workflow wrapper trong terminal.

**Xác minh bằng CLI**:

```bash
cd ~/workspace/backend/my-spring-app
./mvnw -version          # Nếu có Maven Wrapper
./mvnw clean verify      # Nếu có Maven Wrapper
# hoặc dùng: mvn -version && mvn clean verify
```

Trong Eclipse: **Right-click project → Maven → Update Project** để refresh dependencies. Không dùng `mvn clean` tùy tiện khi IDE đang indexing/build liên tục; ưu tiên chạy sau khi dừng các tiến trình liên quan.

### 3.7. Run / Debug Spring Boot trong Eclipse

Nếu dùng Spring Tools for Eclipse:

1. Mở project Maven đã import.
2. Dùng **Run As / Debug As → Spring Boot App** nếu mục này có trong phiên bản Spring Tools của bạn.
3. Hoặc chạy class chứa `@SpringBootApplication` với **Run As → Java Application / Debug As → Java Application**.
4. Đặt breakpoints, xem variables/call stack trong Debug Perspective.
5. Xác minh cổng ứng dụng và Java process đang chạy trong Ubuntu.

```bash
ps -ef | grep '[j]ava'
# Thay 8080 nếu ứng dụng dùng cổng khác
ss -ltn | grep ':8080' || true
```

Trên Windows, thử `http://localhost:8080` nếu ứng dụng bind cổng phù hợp và WSL forwarding/network đang hoạt động. Trường hợp không kết nối được, kiểm tra mạng WSL, cổng và host bind của Spring Boot trước khi thay đổi firewall.

### 3.8. Git và Docker trong Eclipse Linux

- **EGit** (GUI tích hợp Eclipse) có thể sử dụng để xem status/diff/log; **EGit dùng JGit**, không nên hiểu rằng mọi thao tác GUI đang gọi `/usr/bin/git`.
- Để giữ quy trình Git nhất quán (đặc biệt merge/rebase và custom mergetool), ưu tiên **Git Ubuntu CLI** trong terminal.
- Docker Engine sử dụng qua `docker ps`, `docker compose` trong terminal Ubuntu hoặc công cụ tương thích Linux nếu cần.

Ví dụ:

```bash
cd ~/workspace/backend/my-spring-app
git status
docker ps
```

### 3.9. Tinh chỉnh WSLg nếu Eclipse có lỗi GUI

| Hiện tượng | Kiểm tra / hướng khắc phục |
|---|---|
| Không hiện cửa sổ | Kiểm tra `DISPLAY`, `WAYLAND_DISPLAY`, phiên bản WSL 2 và WSLg |
| Lỗi thư viện GTK/SWT | Kiểm tra dependency GUI của Ubuntu; tham khảo trang Equinox launcher issues |
| Giao diện lỗi dưới Wayland | Thử chạy launcher với `GDK_BACKEND=x11` để sử dụng XWayland |
| Eclipse quá chậm | Đặt workspace và repository trong `/home/...`, tắt indexing/plugin không dùng, đánh giá tài nguyên WSL |
| `Java 17` không chạy được IDE mới | Dùng runtime đi kèm IDE; chỉ cấu hình Corretto 17 cho project; không ép IDE mới chạy bằng Java 17 |

Ví dụ chạy bằng X11 (thay `<path-to-linux-launcher>` bằng đường dẫn thật):

```bash
GDK_BACKEND=x11 "<path-to-linux-launcher>"
```

---

## 4. Git merge / conflict: quy trình dùng chung cho cả hai IDE

!!! info "Tách trách nhiệm"
    - **Git Ubuntu**: checkout, fetch, pull, merge, rebase, commit, push.
    - **IntelliJ/Eclipse**: edit source code, xem diff, test và debug.
    - **TortoiseGitMerge Windows**: chỉ là GUI được gọi bởi `git mergetool` từ Git Ubuntu (khi đã cấu hình wrapper).

Để tiếp tục sử dụng TortoiseGitMerge với Git Ubuntu, xem hướng dẫn riêng: [VS Code Windows + WSL Ubuntu + Git Merge](vscode-wsl-ubuntu-git-merge.md) *(nếu bạn đã thêm trang đó vào cùng thư mục tài liệu)*.

Kiểm tra trước khi merge:

```bash
cd ~/workspace/backend/my-spring-app
git status --short
git config --get merge.tool || true
```

Nếu wrapper TortoiseGitMerge đã được cấu hình trước đó:

```bash
# Ví dụ merge feature vào develop (working tree phải được xử lý trước)
git fetch origin
git switch develop
git merge feature/login

# Khi có file conflict:
git diff --name-only --diff-filter=U
git mergetool
```

Sau khi giải quyết trong GUI và **lưu** kết quả:

```bash
git status
git diff --name-only --diff-filter=U
git diff --cached --check
# Kiểm tra nội dung/các test phù hợp trước khi hoàn tất
git merge --continue
```

Nếu đang **rebase**, dùng `git rebase --continue` thay vì `git merge --continue`. Trường hợp conflict liên quan file bị xóa, binary hoặc submodule có thể cần xử lý trực tiếp bằng Git CLI.

!!! warning "Không tự động xác nhận mergetool đã giải quyết đúng"
    Kết thúc cửa sổ TortoiseGitMerge **không đảm bảo** kết quả đã đúng nghiệp vụ. Kiểm tra file sau khi lưu, `git status`, danh sách unmerged và chạy test trước khi commit.

---

## 5. So sánh và lựa chọn IDE

| Tiêu chí | IntelliJ IDEA trên Windows + WSL | Eclipse Linux / Spring Tools + WSLg |
|---|---|---|
| IDE process | Windows | Ubuntu |
| Màn hình IDE | Windows native | WSLg trên Windows |
| Source code | Ubuntu (`/home/...`) | Ubuntu (`/home/...`) |
| JDK/Maven/Git đã cài | Cần đảm bảo chọn đúng **WSL runtime** | Trực tiếp trong Ubuntu |
| Debug Spring Boot | Được hỗ trợ với WSL, cần kiểm tra Run Configuration | Debug trực tiếp trong Ubuntu |
| Git GUI | IntelliJ Git UI | EGit (JGit) |
| Git merge thống nhất | CLI Git Ubuntu + TortoiseGitMerge | CLI Git Ubuntu + TortoiseGitMerge |
| Tích hợp Spring chuyên sâu | Tùy phiên bản/gói cấp phép | Spring Tools miễn phí, mã nguồn mở |
| Chi phí truy cập file qua ranh giới OS | Có phần overhead | Thấp hơn khi thao tác nội bộ Linux |
| Độ quen thuộc khi đang dùng Eclipse | Cần làm quen | Rất phù hợp |

**Đề xuất theo thứ tự ưu tiên:**

1. **Đang quen Eclipse và muốn ít thay đổi thao tác:** chọn **Spring Tools for Eclipse Linux + WSLg**, kiểm tra độ mượt GUI với dự án Maven thực tế.
2. **Ưu tiên code navigation/refactoring/debug chuyên sâu:** thử **IntelliJ IDEA Windows + WSL** và xác minh toàn bộ toolchain khi import, build, run/debug.
3. **Nếu Eclipse WSLg chậm đáng kể:** cân nhắc IntelliJ Windows + WSL hoặc VS Code Remote WSL, không cần chuyển source code sang ổ Windows.

---

## 6. Checklist nghiệm thu

### Chung

- [ ] Source code ở `/home/<linux-user>/workspace/...`.
- [ ] `java -version` báo JDK mục tiêu của project (Corretto 17).
- [ ] `mvn -version` hoặc `./mvnw -version` dùng Java 17.
- [ ] `git --version` là Git Ubuntu.
- [ ] `docker info` kết nối Docker Engine trong Ubuntu.
- [ ] Build/test bằng terminal Ubuntu thành công.

### IntelliJ IDEA

- [ ] Mở dự án bằng đường dẫn `\\wsl.localhost\Ubuntu\...`.
- [ ] Project SDK là JDK 17 **trong WSL**.
- [ ] Maven Runner/Importer và Run Configuration sử dụng runtime phù hợp.
- [ ] Java process của Spring Boot xuất hiện trong Ubuntu khi Run/Debug.
- [ ] Git executable được xác minh là Git WSL.

### Eclipse Linux + WSLg

- [ ] WSLg hiển thị ứng dụng GUI được.
- [ ] Eclipse/Spring Tools **Linux** khởi động thành công.
- [ ] Workspace metadata và repository nằm trong filesystem Ubuntu.
- [ ] Project Java compliance/JRE = 17 (dù IDE có thể chạy trên JDK mới hơn).
- [ ] Maven import thành công, Run/Debug Spring Boot được.
- [ ] Có thể sử dụng terminal Git Ubuntu / custom mergetool khi conflict.

---

## 7. Troubleshooting nhanh

??? question "IntelliJ mở project được nhưng Maven dùng Java Windows?"
    Kiểm tra **Project SDK**, **Maven → Runner → JRE**, **Maven → Importing → JDK for importer**, **Maven home path** và thực tế process chạy. Build từ Ubuntu terminal để đối chiếu. Đừng giả định IDE tự dùng mọi công cụ Ubuntu chỉ vì project đặt trong WSL.

??? question "Eclipse WSLg chạy được nhưng Spring Boot khởi động bằng Java không đúng phiên bản?"
    Tách biệt runtime **chạy Eclipse** và JRE **chạy project**. Trong **Installed JREs**, Project Properties và Run Configurations, chọn Corretto 17. Không sửa runtime được đóng gói cùng Spring Tools nếu nó đang hoạt động bình thường.

??? question "Không dùng được Docker từ IDE?"
    Kiểm tra trước với `docker info` trong Ubuntu. Nếu CLI hoạt động mà integration trong IDE lỗi, vấn đề nằm ở cấu hình tích hợp IDE; tránh expose `dockerd` ra `0.0.0.0:2375` không TLS.

??? question "`git mergetool` không mở TortoiseGitMerge?"
    Kiểm tra `git config --get merge.tool`, quyền chạy wrapper, đường dẫn tuyệt đối đến `TortoiseGitMerge.exe`, WSL interoperability và chuyển đường dẫn bằng `wslpath -aw`. Không dùng Git for Windows để thay thế giữa chừng.

??? question "Tại sao Windows có thể mở Spring Boot chạy trong WSL bằng localhost?"
    WSL 2 hỗ trợ localhost forwarding trong các cấu hình mạng phổ biến. Kiểm tra `server.port`, địa chỉ bind, chế độ NAT/mirrored và firewall nếu không truy cập được. Không mở debug port (JDWP) ra Internet.

---