---
title: Cài đặt Amazon Corretto 17, Maven, Node.js và npm trên WSL Ubuntu
description: Hướng dẫn thiết lập môi trường phát triển Spring Boot và Nuxt trên WSL Ubuntu với Amazon Corretto 17, Maven Wrapper, NVM và npm.
tags:
  - WSL
  - Ubuntu
  - Java
  - Amazon Corretto
  - Maven
  - Node.js
  - npm
  - Nuxt
  - Spring Boot
---

# Cài đặt Amazon Corretto 17, Maven, Node.js và npm trên WSL Ubuntu

> **Mục tiêu:** Thiết lập môi trường development dùng cho **Java Spring Boot** và **Nuxt** trực tiếp trong WSL Ubuntu; đồng thời dễ quản lý, cập nhật và tái tạo giữa các dự án.

Hướng dẫn giả định **WSL 2 và Ubuntu đã được cài đặt**, và sử dụng terminal **Ubuntu** (không chạy các lệnh Linux trong PowerShell).

## 1. Tổng quan kiến trúc và lựa chọn công cụ

| Thành phần | Phương án khuyến nghị | Lý do |
| --- | --- | --- |
| JDK | **Amazon Corretto 17 LTS**, APT repository của AWS | Nhận bản cập nhật bảo mật qua APT, phù hợp dự án Spring Boot dùng Java 17 |
| Maven | **Maven 3.x** qua APT; ưu tiên **Maven Wrapper** của dự án | Giảm sai khác Maven version giữa developer và CI/CD |
| Node.js | **Node.js 24 LTS** qua NVM, nếu đáp ứng yêu cầu của dự án | Quản lý phiên bản Node riêng cho từng dự án |
| npm | Phiên bản đi kèm Node.js | Không cần cài npm độc lập qua APT |
| Công cụ hệ thống | Git, curl, wget, build-essential, Python 3 | Hỗ trợ tải dependencies và biên dịch native Node.js modules |
| Docker | Docker Engine trong WSL Ubuntu (nếu đã cài) | Chạy PostgreSQL, Redis và các dịch vụ phụ trợ |

!!! tip "Tư duy cấu hình tối ưu"
    - **Java, Maven, Node.js và source code** nằm trong filesystem của Ubuntu (`~/projects`).
    - **Database, Redis và các service phụ trợ** có thể chạy bằng Docker Engine trong WSL.
    - **IDE trên Windows** kết nối qua WSL extension; trình biên dịch và công cụ build vẫn chạy trong Ubuntu.
    - **Phiên bản công cụ của từng dự án** nên được cố định bằng Maven Wrapper và `.nvmrc`.

## 2. Chuẩn bị Ubuntu

Cập nhật thông tin repository:

```bash
sudo apt update
```

Nếu bạn muốn cập nhật các package hệ thống hiện có, có thể chạy (không bắt buộc trong quá trình cài toolchain):

```bash
sudo apt upgrade
```

Cài các công cụ thiết yếu:

```bash
sudo apt install -y \
  curl \
  wget \
  ca-certificates \
  gnupg \
  git \
  unzip \
  zip \
  build-essential \
  python3
```

Kiểm tra phiên bản Ubuntu:

```bash
cat /etc/os-release
uname -m
```

!!! note "Vì sao cài build-essential và Python 3?"
    Một số npm package sử dụng native modules và cần compiler, `make`, Python 3 khi phải build từ source. Không phải dự án Node.js nào cũng cần đến chúng, nhưng cài sẵn sẽ hữu ích cho môi trường development.

## 3. Cài Amazon Corretto JDK 17

### 3.1. Thêm APT repository của Amazon Corretto

Tải và đăng ký khóa GPG của repository:

```bash
curl -fsSL https://apt.corretto.aws/corretto.key \
  | sudo gpg --batch --yes --dearmor \
      -o /usr/share/keyrings/corretto-keyring.gpg
```

Thêm repository:

```bash
echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" \
  | sudo tee /etc/apt/sources.list.d/corretto.list
```

Cập nhật package index:

```bash
sudo apt update
```

### 3.2. Cài JDK 17

```bash
sudo apt install -y java-17-amazon-corretto-jdk
```

Kiểm tra:

```bash
java -version
javac -version
```

Kết quả kỳ vọng có dạng:

```text
openjdk version "17.0.x" ...
OpenJDK Runtime Environment Corretto-17...
OpenJDK 64-Bit Server VM Corretto-17...
```

!!! info "Vì sao chọn JDK thay vì JRE?"
    JDK chứa `javac` và các công cụ cần thiết để **biên dịch** và debug Java. JRE đơn thuần không đáp ứng đầy đủ nhu cầu phát triển phần mềm.

### 3.3. Đặt Corretto 17 làm Java mặc định

Nếu máy có nhiều JDK:

```bash
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

Chọn bản **Amazon Corretto 17** ở cả hai lệnh.

Xem Java và compiler hiện tại:

```bash
readlink -f /usr/bin/java
readlink -f /usr/bin/javac
```

### 3.4. Cấu hình `JAVA_HOME`

Tìm thư mục gốc JDK từ `javac` hiện được chọn:

```bash
dirname "$(dirname "$(readlink -f /usr/bin/javac)")"
```

Ví dụ kết quả:

```text
/usr/lib/jvm/java-17-amazon-corretto
```

Mở cấu hình Bash:

```bash
nano ~/.bashrc
```

Thêm **một lần** vào cuối file:

```bash
# Dùng JDK đang được chọn bởi update-alternatives
export JAVA_HOME="$(dirname "$(dirname "$(readlink -f /usr/bin/javac)")")"
```

Nạp lại shell:

```bash
source ~/.bashrc
printf 'JAVA_HOME=%s\n' "$JAVA_HOME"
java -version
```

!!! tip "Đường dẫn JAVA_HOME"
    Lấy `JAVA_HOME` từ đường dẫn của `javac` giúp tránh hard-code một đường dẫn có thể khác nhau giữa các phiên bản Ubuntu hoặc kiến trúc. Nếu dự án bắt buộc sử dụng Corretto 17 dù Java mặc định thay đổi, hãy cố định `JAVA_HOME` theo đường dẫn JDK Corretto thực tế trên máy.

## 4. Cài Apache Maven

### 4.1. Cài Maven qua APT

```bash
sudo apt install -y maven
```

Kiểm tra:

```bash
mvn -version
```

Đầu ra cần xác nhận Maven và Java 17:

```text
Apache Maven 3.x.x
Java version: 17.x.x
Java home: /usr/lib/jvm/...
```

!!! note "Có cần Maven mới nhất không?"
    Phiên bản Maven từ repository Ubuntu có thể không phải phiên bản mới nhất. Điều quan trọng là **phiên bản phù hợp với project**. Với dự án có Maven Wrapper, phiên bản Maven của dự án sẽ được quản lý riêng mà không cần nâng Maven hệ thống.

### 4.2. Ưu tiên Maven Wrapper trong dự án

Nếu repository đã có `mvnw` và thư mục `.mvn/wrapper/`, hãy chạy:

```bash
cd ~/projects/spring-backend
./mvnw clean verify
```

Maven Wrapper sử dụng bản Maven theo cấu hình của project, thay vì phụ thuộc hoàn toàn vào lệnh `mvn` hệ thống.

Nếu project chưa có wrapper và bạn có quyền cập nhật repository:

```bash
mvn wrapper:wrapper
```

Commit các file Maven Wrapper cần thiết vào Git theo quy ước của dự án.

### 4.3. Giữ Maven dependency cache trên Linux filesystem

Theo mặc định, Maven lưu artifacts trong:

```text
~/.m2/repository
```

Nên giữ cache tại đây. Không cần thiết lập `MAVEN_HOME` hoặc `M2_HOME` khi cài Maven qua APT.

## 5. Cài Node.js và npm bằng NVM

**NVM (Node Version Manager)** quản lý nhiều phiên bản Node.js trong thư mục home của user. Đây là phương án phù hợp cho nhiều project Nuxt có yêu cầu runtime khác nhau.

### 5.1. Cài NVM

Ví dụ sử dụng NVM `v0.40.8` (nên đối chiếu release mới nhất trước khi nâng cấp):

```bash
curl -fsSLo /tmp/install-nvm.sh \
  https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh

# Xem nội dung script trước khi chạy
less /tmp/install-nvm.sh

bash /tmp/install-nvm.sh
```

NVM thông thường cập nhật shell profile (chẳng hạn `~/.bashrc`). Nạp lại shell:

```bash
source ~/.bashrc
```

Kiểm tra:

```bash
command -v nvm
nvm --version
```

!!! note "NVM là shell function"
    `command -v nvm` nên in ra `nvm`. Không nhất thiết có file binary `nvm` trong `/usr/bin` hoặc `/usr/local/bin`.

### 5.2. Cài Node.js LTS

Trong hướng dẫn này, sử dụng **Node.js 24 LTS** làm ví dụ. Hãy ưu tiên version được khai báo bởi dự án Nuxt (`package.json`, `.nvmrc`) nếu khác.

```bash
nvm install 24
nvm alias default 24
nvm use 24
```

Kiểm tra:

```bash
node --version
npm --version
```

!!! warning "Không cài npm riêng bằng APT"
    Khi dùng NVM, `npm` đi kèm bản Node.js đã cài. Tránh chạy `sudo apt install nodejs npm` hoặc `sudo npm install` vì dễ dẫn đến nhiều bộ Node/npm và xung đột quyền file.

### 5.3. Quản lý Node.js theo từng project bằng `.nvmrc`

Ví dụ:

```text
projects/
├── nuxt-project-a/
│   └── .nvmrc       # 22
└── nuxt-project-b/
    └── .nvmrc       # 24
```

Nội dung `nuxt-project-b/.nvmrc`:

```text
24
```

Trong terminal:

```bash
cd ~/projects/nuxt-project-b
nvm install
nvm use
node --version
```

!!! tip "Best practice cho CI/CD và teamwork"
    Commit `.nvmrc` vào Git để mọi developer dễ sử dụng cùng major Node.js. Đồng thời khai báo `engines.node` trong `package.json` nếu dự án cần ràng buộc tương thích rõ ràng.

## 6. Cấu hình npm cho development

### 6.1. Không dùng `sudo` với npm do NVM quản lý

Cài dependencies cho project:

```bash
npm install
```

Nếu project đã có `package-lock.json`, ưu tiên lệnh:

```bash
npm ci
```

`npm ci` yêu cầu lockfile hợp lệ, cài theo lockfile và phù hợp cho môi trường cần tái tạo dependencies nhất quán. Nó cũng thay thế `node_modules` hiện tại khi chạy.

### 6.2. Kiểm tra npm config

```bash
npm config get registry
npm config get cache
npm config get prefix
```

Registry công khai mặc định:

```text
https://registry.npmjs.org/
```

Không tùy tiện đặt `prefix` global khi sử dụng NVM; có thể gây xung đột với cách NVM quản lý Node.js/npm.

## 7. Kiểm tra toàn bộ toolchain

Chạy lần lượt:

```bash
echo '===== JAVA ====='
java -version
javac -version
printf 'JAVA_HOME=%s\n' "$JAVA_HOME"

echo '===== MAVEN ====='
mvn -version

echo '===== NODE.JS ====='
node --version

echo '===== NPM ====='
npm --version

echo '===== NVM ====='
nvm --version
nvm current
```

Kiểm tra các đường dẫn executable:

```bash
type -a java
type -a javac
type -a mvn
type -a node
type -a npm
```

| Thành phần | Đường dẫn kỳ vọng |
| --- | --- |
| Java | `/usr/bin/java` → JDK trong `/usr/lib/jvm/` |
| Javac | `/usr/bin/javac` → Amazon Corretto JDK 17 |
| Maven | `/usr/bin/mvn` |
| Node.js | `~/.nvm/versions/node/.../bin/node` |
| npm | `~/.nvm/versions/node/.../bin/npm` |

!!! warning "Tránh sử dụng nhầm executable trên Windows"
    Nếu `node`, `npm`, `java` hoặc `mvn` trỏ đến `/mnt/c/...`, kiểm tra lại `PATH` và shell profile. Trong WSL, nên sử dụng phiên bản Linux thay vì gọi trực tiếp executable từ Windows.

## 8. Best practices cho Spring Boot và Nuxt trong WSL

### 8.1. Lưu source code trong Linux filesystem

Khuyến nghị:

```text
/home/<linux-user>/projects/
├── spring-backend/
├── nuxt-frontend/
└── dev-infra/
```

Tránh đặt workspace thường xuyên build trong `/mnt/c/` vì I/O và file watching xuyên filesystem Windows/Linux có thể kém hiệu quả hơn.

### 8.2. Cách khởi chạy project

**Spring Boot:**

```bash
cd ~/projects/spring-backend
./mvnw spring-boot:run
```

**Nuxt:**

```bash
cd ~/projects/nuxt-frontend
nvm use
npm ci
npm run dev
```

!!! note "Điều kiện áp dụng các lệnh ví dụ"
    `./mvnw` chỉ sử dụng được khi project có Maven Wrapper; `nvm use` không truyền phiên bản cần file `.nvmrc`; `npm ci` cần `package-lock.json`; `npm run dev` cần script `dev` trong `package.json`.

### 8.3. IDE và Docker

- Chạy **VS Code trên Windows** với extension **WSL**, mở thư mục project trong Ubuntu.
- Chạy Maven, Node.js và npm trong terminal WSL.
- Chạy PostgreSQL, Redis và dịch vụ phụ trợ bằng Docker Engine trong WSL nếu đã cài.
- Giữ `~/.m2/repository` và `node_modules` trong Linux filesystem.

### 8.4. Nguyên tắc quản lý phiên bản

- **JDK:** Dùng phiên bản theo tiêu chuẩn của project, ở đây là Corretto 17.
- **Maven:** Ưu tiên `./mvnw` hơn `mvn` khi project có Maven Wrapper.
- **Node.js:** Ưu tiên `.nvmrc` của project; dùng `nvm alias default 24` cho shell không thuộc project cụ thể.
- **npm:** Sử dụng lockfile và `npm ci` khi cần môi trường reproducible.

## 9. Troubleshooting thường gặp

??? question "`nvm: command not found` sau khi cài"
    Thử mở terminal mới hoặc nạp lại profile:

    ```bash
    source ~/.bashrc
    command -v nvm
    ```

    Nếu vẫn không có, xem hướng dẫn cài NVM chính thức và kiểm tra script đã cập nhật đúng shell profile hay chưa.

??? question "`mvn -version` không sử dụng Java 17"
    Kiểm tra:

    ```bash
    java -version
    javac -version
    echo "$JAVA_HOME"
    sudo update-alternatives --config java
    sudo update-alternatives --config javac
    ```

    Nếu dùng nhiều JDK, chắc chắn `JAVA_HOME` trỏ đến JDK đúng yêu cầu của dự án.

??? question "npm hoặc Node.js đang trỏ đến đường dẫn Windows"
    Kiểm tra:

    ```bash
    type -a node npm
    echo "$PATH"
    nvm current
    ```

    Đảm bảo NVM được load trong `~/.bashrc` và ưu tiên executable từ `~/.nvm/versions/node/.../bin/`.

??? question "APT/curl/npm gặp lỗi certificate khi ở mạng công ty"
    Kiểm tra certificate chain và root CA của proxy doanh nghiệp. Nếu cần, cài CA tin cậy vào trust store Ubuntu theo quy trình được tổ chức cho phép. **Không tắt SSL/TLS verification** bằng các tùy chọn như `strict-ssl=false` hoặc `curl -k` để xử lý lâu dài.

## 10. Checklist hoàn thành

- [ ] Ubuntu đã cài các development utilities cần thiết.
- [ ] `java -version` trả về Amazon Corretto 17.
- [ ] `javac -version` là phiên bản 17.
- [ ] `JAVA_HOME` trỏ đến JDK đúng.
- [ ] `mvn -version` sử dụng Java 17.
- [ ] Maven Wrapper hoạt động ở project Java (nếu có).
- [ ] `nvm --version` chạy thành công.
- [ ] `node --version` khớp phiên bản yêu cầu của project.
- [ ] `npm --version` chạy thành công.
- [ ] Node/npm trỏ đến thư mục NVM trên Linux.
- [ ] Source code được lưu trong `/home/...`, không phải `/mnt/c/...`.
- [ ] Build Spring Boot và chạy Nuxt thành công.

## 11. Tài liệu tham khảo chính thức

1. [Amazon Corretto 17 — Linux installation](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/generic-linux-install.html)
2. [Apache Maven — Installation](https://maven.apache.org/install.html)
3. [Apache Maven Wrapper](https://maven.apache.org/wrapper/)
4. [NVM — GitHub repository và hướng dẫn cài đặt](https://github.com/nvm-sh/nvm)
5. [npm Docs — Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
6. [npm Docs — npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
7. [Node.js — Release schedule](https://github.com/nodejs/Release#release-schedule)
8. [Microsoft Learn — Working across Windows and Linux file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems)

---

**Kết luận:** Sử dụng **Corretto 17 qua APT**, **Maven + Maven Wrapper**, **Node.js/npm qua NVM** và lưu source trong filesystem Ubuntu là cấu hình dễ bảo trì cho môi trường phát triển Spring Boot/Nuxt trên WSL.
