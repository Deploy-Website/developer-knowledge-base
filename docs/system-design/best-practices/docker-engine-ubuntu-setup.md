---
title: Cài đặt Docker Engine trên WSL Ubuntu
summary: Hướng dẫn cài đặt và tối ưu Docker Engine, Docker Compose, Buildx trên WSL 2 Ubuntu cho môi trường phát triển phần mềm.
---

# Cài đặt và cấu hình Docker Engine trên WSL Ubuntu

> **Mục tiêu:** Xây dựng môi trường Docker thuần Linux ngay trong **WSL 2 Ubuntu**, **không sử dụng Docker Desktop**, phục vụ phát triển **Java Spring Boot, Nuxt, PostgreSQL, Redis** và các dịch vụ khác.

## 1. Tổng quan kiến trúc

Cấu hình khuyến nghị:

- **Windows 11:** Windows Terminal, VS Code và trình duyệt.
- **WSL 2 Ubuntu:** Git, JDK, Maven, Node.js, mã nguồn và Docker CLI.
- **Docker Engine trong Ubuntu:** Chạy PostgreSQL, Redis và các dịch vụ phụ trợ; quản lý bằng `systemd`.
- **Docker Compose V2:** Định nghĩa và vận hành nhiều container.
- **Buildx/BuildKit:** Build image hiệu quả, tận dụng cache và multi-stage builds.

```text
Windows 11
├── Windows Terminal
├── VS Code (WSL extension)
└── Browser
      │
      └── WSL 2 — Ubuntu
          ├── Git / JDK / Maven / Node.js
          ├── Source code: ~/projects/
          │   ├── hotel-backend/   (Spring Boot)
          │   ├── hotel-frontend/  (Nuxt)
          │   └── dev-infra/      (Compose)
          └── Docker Engine (dockerd + containerd)
              ├── Docker Compose V2 / Buildx
              ├── PostgreSQL container
              ├── Redis container
              └── Docker volumes / networks / images
```

!!! tip "Chiến lược phát triển khuyến nghị"
    Trong quá trình lập trình, chạy **Spring Boot và Nuxt trực tiếp trong Ubuntu** để debug và hot reload nhanh. Chạy **PostgreSQL, Redis và dịch vụ phụ trợ bằng Docker Compose**. Khi cần kiểm thử đóng gói hoặc triển khai, container hóa toàn bộ ứng dụng.

## 2. Kiểm tra môi trường Ubuntu

!!! info "Terminal sử dụng"
    Các lệnh `bash` bên dưới chạy **trong terminal WSL Ubuntu**. Chỉ các lệnh có nhãn `powershell` mới chạy trên **Windows PowerShell**.

Kiểm tra hệ điều hành, kiến trúc, Docker hiện có và hệ thống khởi tạo:

```bash
cat /etc/os-release
dpkg --print-architecture
command -v docker || true
dpkg -l | grep -E 'docker|containerd|runc' || true
ps -p 1 -o comm=
```

Docker Engine phải được cài từ repository phù hợp với **phiên bản Ubuntu và kiến trúc CPU**. Kiểm tra phiên bản Ubuntu hiện được hỗ trợ tại [Docker Engine — Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

### 2.1. Bật systemd (nếu cần)

Nếu lệnh sau trả về `systemd`, **bỏ qua** mục này:

```bash
ps -p 1 -o comm=
```

Nếu chưa bật, mở file cấu hình WSL:

```bash
sudo nano /etc/wsl.conf
```

Thêm vào section `[boot]` hiện có, hoặc tạo section khi chưa tồn tại:

```ini
[boot]
systemd=true
```

Khởi động lại distro từ **PowerShell**:

```powershell
wsl --terminate Ubuntu
wsl -d Ubuntu
```

Kiểm tra lại trong Ubuntu:

```bash
ps -p 1 -o comm=
```

!!! note
    `systemd` cho phép `systemctl` quản lý Docker khi Ubuntu chạy. Nó **không đảm bảo WSL luôn chạy ngầm** sau khi Windows hoặc distro đã dừng. Xem [Microsoft — Systemd trong WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd).

### 2.2. Tránh xung đột với Docker Desktop cũ

Nếu trước đây từng dùng Docker Desktop:

1. Thoát Docker Desktop và tắt tích hợp WSL với Ubuntu.
2. Không cài song song Docker Desktop Integration và Docker Engine độc lập để cùng thao tác trong một Ubuntu.
3. **Không** dùng `wsl --unregister docker-desktop` nếu chưa hiểu và sao lưu dữ liệu; thao tác này có thể xóa dữ liệu của distro đó.

## 3. Cài đặt Docker Engine từ repository chính thức

### 3.1. Kiểm tra và gỡ các package xung đột

Kiểm tra trước:

```bash
dpkg -l | grep -E 'docker.io|docker-compose|docker-doc|docker-buildx|podman-docker|containerd|runc' || true
```

Chỉ gỡ các package xung đột **nếu đang được cài**:

```bash
conflicting_packages=(
  docker.io docker-doc docker-compose docker-compose-v2
  docker-buildx podman-docker containerd runc
)
installed_packages=()

for pkg in "${conflicting_packages[@]}"; do
  if dpkg-query -W -f='${db:Status-Abbrev}' "$pkg" 2>/dev/null | grep -q '^ii'; then
    installed_packages+=("$pkg")
  fi
done

if ((${#installed_packages[@]} > 0)); then
  sudo apt-get remove "${installed_packages[@]}"
fi
```

!!! warning "Bảo toàn dữ liệu Docker"
    Nếu đã có Docker/container/volume chứa dữ liệu, hãy **sao lưu trước**. Không tùy tiện xóa `/var/lib/docker` hay chạy `apt purge` để làm sạch môi trường.

### 3.2. Cài dependencies và Docker GPG key

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL \
  https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### 3.3. Thêm Docker APT repository

```bash
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF_REPO
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF_REPO

sudo apt-get update
apt-cache policy docker-ce
```

Kiểm tra `Candidate` và repository `https://download.docker.com/linux/ubuntu` trong kết quả.

### 3.4. Cài Docker Engine, Compose V2 và Buildx

```bash
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

| Package | Vai trò |
| --- | --- |
| `docker-ce` | Docker Engine và daemon `dockerd` |
| `docker-ce-cli` | Docker CLI |
| `containerd.io` | Container runtime |
| `docker-buildx-plugin` | Buildx/BuildKit cho việc build image |
| `docker-compose-plugin` | Docker Compose V2 (`docker compose`) |

!!! tip
    Dùng cú pháp **`docker compose`** (Compose V2), không cần cài riêng binary `docker-compose` đời cũ.

### 3.5. Bật và kiểm tra dịch vụ

```bash
sudo systemctl enable --now docker.service
sudo systemctl enable --now containerd.service

systemctl is-active docker
systemctl is-enabled docker

sudo docker run --rm hello-world

docker --version
docker compose version
docker buildx version
```

Kỳ vọng `docker.service` trả về `active` và `enabled`, và container `hello-world` thực thi thành công.

## 4. Sử dụng Docker không cần sudo

Để thuận tiện trong môi trường phát triển cá nhân:

```bash
sudo groupadd -f docker
sudo usermod -aG docker "$USER"
newgrp docker
```

Kiểm tra:

```bash
groups
docker ps
docker run --rm hello-world
```

!!! danger "Quyền truy cập tương đương root"
    User thuộc group `docker` có thể giành quyền root trên máy Linux chạy daemon. Chỉ áp dụng cho tài khoản development đáng tin cậy. Nếu yêu cầu cách ly bảo mật cao, cân nhắc [Docker Rootless Mode](https://docs.docker.com/engine/security/rootless/).

## 5. Tối ưu Docker daemon

### 5.1. Giới hạn log container

Nếu không cấu hình rotation, log có thể phát triển rất lớn khi chạy service Spring Boot hoặc batch job. Với local development, nên dùng Docker logging driver `local`.

Mở file (nếu chưa có thì tạo):

```bash
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```

Cấu hình:

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

!!! warning
    Nếu `/etc/docker/daemon.json` **đã tồn tại**, hãy **gộp thuộc tính** vào JSON hiện tại thay vì ghi đè toàn bộ file.

Kiểm tra JSON và khởi động lại Docker:

```bash
python3 -m json.tool /etc/docker/daemon.json > /dev/null
sudo systemctl restart docker

docker info --format '{{.LoggingDriver}}'
```

Kết quả mong muốn: `local`.

| Cấu hình | Ý nghĩa |
| --- | --- |
| `log-driver: local` | Logging dạng local, có hỗ trợ rotation |
| `max-size: 10m` | Giới hạn kích thước mỗi file log trước khi xoay vòng |
| `max-file: 3` | Số file log giữ lại cho mỗi container |

!!! note
    Cấu hình log mặc định mới áp dụng cho **container được tạo sau khi thay đổi**. Container đã tồn tại cần recreate nếu muốn nhận cấu hình mới. Xem [Docker — Configure logging drivers](https://docs.docker.com/engine/logging/configure/).

### 5.2. Kiểm tra Docker Buildx/BuildKit

```bash
docker buildx ls
docker buildx inspect
```

Build image:

```bash
docker build -t my-app:dev .
```

BuildKit đã là build backend mặc định trên các phiên bản Docker Engine hiện đại. Không cần thêm biến `DOCKER_BUILDKIT=1` hoặc tạo builder tùy chỉnh nếu không có nhu cầu đặc biệt.

!!! tip "Tối ưu Dockerfile"
    Với Maven hoặc Node.js, nên kết hợp **multi-stage build**, `.dockerignore` và cache dependency layers. Sao chép các file khai báo dependency trước mã nguồn để tận dụng cache khi thay đổi code.

### 5.3. Đảm bảo Docker CLI dùng Engine trong Ubuntu

```bash
docker context ls
docker context show
docker info --format 'Name={{.Name}} RootDir={{.DockerRootDir}}'

echo "$DOCKER_HOST"
echo "$DOCKER_CONTEXT"
```

Với Docker Engine rootful cài trực tiếp, `RootDir` thường là `/var/lib/docker`.

Nếu CLI vẫn trỏ sang Docker Desktop, kiểm tra và chuyển context về mặc định:

```bash
unset DOCKER_HOST DOCKER_CONTEXT
docker context use default
docker ps
```

!!! note
    Không mở Docker daemon qua TCP (đặc biệt cổng `2375`) chỉ để VS Code trên Windows truy cập. Hãy dùng VS Code Remote WSL và kết nối với Docker socket nội bộ Ubuntu.

## 6. Cấu hình tài nguyên WSL 2

Docker Engine sử dụng RAM/CPU/disk của WSL 2 VM. Có thể đặt giới hạn tài nguyên chung bằng file **`%UserProfile%\.wslconfig`** trên Windows.

Mở **PowerShell**:

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Ví dụ cho máy Windows **32 GB RAM**:

```ini
[wsl2]
memory=12GB
swap=4GB
localhostForwarding=true
```

Sau khi lưu, áp dụng bằng PowerShell:

```powershell
wsl --shutdown
```

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `memory=12GB` | RAM tối đa của **toàn bộ WSL 2 VM**, không riêng Docker |
| `swap=4GB` | Dung lượng swap của WSL |
| `localhostForwarding=true` | Cho phép truy cập các cổng WSL qua localhost trong chế độ mạng phù hợp (ví dụ NAT) |

!!! tip "Chọn RAM phù hợp"
    - Máy 16 GB RAM: có thể **bắt đầu thử** với giới hạn WSL khoảng 6–8 GB.
    - Máy 32 GB RAM: có thể bắt đầu khoảng 12 GB.
    - Nếu build Java và chạy nhiều database cùng lúc, tăng/giảm theo mức tiêu thụ thực tế.

    Đây chỉ là **giá trị gợi ý**, không phải cấu hình bắt buộc. Không cần giới hạn số CPU khi chưa có vấn đề thực tế. Cũng không cần bật `networkingMode=mirrored` để chạy Docker Engine thông thường.

Tham khảo: [Microsoft — Advanced settings configuration in WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

## 7. Tổ chức source code và Docker Compose

### 7.1. Cấu trúc dự án khuyến nghị

```text
/home/<linux-user>/
└── projects/
    ├── hotel-backend/       # Spring Boot / Maven
    ├── hotel-frontend/      # Nuxt / Node.js
    └── dev-infra/
        ├── compose.yaml
        ├── .gitignore
        └── secrets/
            └── postgres_password.txt
```

!!! important "Lưu source trên Linux filesystem"
    Đặt project trong `~/projects`, **không dùng `/mnt/c/...`** làm nơi lưu source chính nếu công cụ build và runtime chạy trong Linux. File I/O, Git, Maven, `node_modules` và file watching thường hoạt động tốt hơn trên filesystem Linux.

### 7.2. Compose mẫu cho PostgreSQL và Redis

Tạo thư mục:

```bash
mkdir -p ~/projects/dev-infra
cd ~/projects/dev-infra
```

Tạo `compose.yaml`:

```yaml title="compose.yaml"
name: dev-infra

services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_DB: appdb
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    secrets:
      - postgres_password
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U "$${POSTGRES_USER}" -d "$${POSTGRES_DB}"
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis_data:/data

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt

volumes:
  postgres_data:
  redis_data:
```

Tạo file secret chứa mật khẩu PostgreSQL:

```bash
install -d -m 700 secrets
nano secrets/postgres_password.txt
chmod 600 secrets/postgres_password.txt
```

Nhập mật khẩu riêng cho môi trường local, lưu lại, rồi thêm vào `.gitignore`:

```gitignore title=".gitignore"
secrets/
.env
```

!!! warning "Bảo vệ thông tin nhạy cảm"
    Không commit file chứa mật khẩu lên Git. Compose secrets giúp tránh ghi mật khẩu trực tiếp vào environment trong file `compose.yaml`, nhưng file nguồn trên host vẫn cần được bảo vệ quyền truy cập.

Khởi chạy:

```bash
docker compose config --quiet
docker compose up -d
docker compose ps
```

Kiểm tra PostgreSQL và Redis:

```bash
docker compose exec postgres pg_isready -U dev -d appdb
docker compose exec redis redis-cli ping
```

Dừng service **nhưng vẫn giữ named volumes**:

```bash
docker compose down
```

!!! danger "Không xóa volume ngoài ý muốn"
    `docker compose down -v` sẽ xóa các volume do Compose quản lý, có thể làm mất dữ liệu database. Named volume **không thay thế backup**.

### 7.3. Kết nối từ Spring Boot

Nếu Spring Boot chạy **trực tiếp trong WSL Ubuntu**, truy cập database qua `localhost`:

```properties title="application-local.properties"
spring.datasource.url=jdbc:postgresql://localhost:5432/appdb
spring.datasource.username=dev
spring.datasource.password=${DB_PASSWORD}
```

`DB_PASSWORD` phải được cung cấp cho tiến trình Spring Boot bằng biến môi trường hoặc cơ chế quản lý secret phù hợp.

Nếu Spring Boot được đóng gói thành container và chạy **cùng Compose network** với PostgreSQL và Redis, sử dụng hostname service `postgres` / `redis`, **không sử dụng `localhost`** để truy cập các container khác.

!!! note "Giới hạn cổng"
    Compose trên bind cổng PostgreSQL/Redis vào `127.0.0.1` để phục vụ phát triển cục bộ, tránh publish mặc định lên tất cả network interfaces. Nếu một dịch vụ khác đã chiếm cổng `5432` hoặc `6379`, đổi **cổng host** trong `ports`.

## 8. Tích hợp VS Code trên Windows

Cài các extension do Microsoft cung cấp:

- **WSL**: Mở workspace và terminal Linux từ giao diện VS Code Windows.
- **Container Tools**: Hỗ trợ làm việc với Dockerfile, image, container và Compose.
- **Dev Containers** *(tùy chọn)*: Chuẩn hóa môi trường development bằng cấu hình container.

Mở dự án từ WSL Ubuntu:

```bash
cd ~/projects/hotel-backend
code .
```

Quy trình làm việc thường ngày:

1. `docker compose up -d` trong `~/projects/dev-infra` để bật database/cache.
2. Chạy và debug Spring Boot bằng JDK/Maven hoặc IDE trong WSL.
3. Chạy Nuxt bằng Node.js trong WSL, tận dụng hot module replacement.
4. Chỉ build app image khi cần kiểm thử runtime container hoặc quy trình triển khai.

## 9. Vận hành và bảo trì

| Công việc | Lệnh |
| --- | --- |
| Trạng thái Engine | `systemctl status docker` |
| Khởi động Engine | `sudo systemctl start docker` |
| Dừng Engine | `sudo systemctl stop docker` |
| Liệt kê container | `docker ps -a` |
| Theo dõi CPU/RAM container | `docker stats` |
| Kiểm tra dung lượng | `docker system df` |
| Xem log Compose | `docker compose logs -f` |
| Xem log daemon | `journalctl -u docker -n 100 --no-pager` |
| Dọn build cache không sử dụng | `docker builder prune` |
| Dừng stack Compose | `docker compose down` |
| Cập nhật package qua APT | `sudo apt-get update && sudo apt-get upgrade` |

!!! warning "Dọn dung lượng có kiểm soát"
    Không đưa `docker system prune -a --volumes` vào tác vụ dọn tự động: các image, cache và volume không còn được container sử dụng vẫn có thể quan trọng cho môi trường development.

Đối với PostgreSQL có dữ liệu cần giữ, hãy **backup định kỳ** (ví dụ bằng `pg_dump`), thay vì chỉ dựa vào named volume.

## 10. Checklist sau khi cài

- [ ] Ubuntu chạy bằng WSL 2, `systemd` hoạt động.
- [ ] Docker Engine được cài từ repository Docker chính thức.
- [ ] `docker` và `containerd` chạy qua `systemd`.
- [ ] `docker ps` chạy được theo chính sách quyền đã chọn.
- [ ] Docker CLI kết nối đúng Engine cục bộ trong Ubuntu.
- [ ] `docker compose` và `docker buildx` hoạt động.
- [ ] Logging driver được cấu hình và kiểm tra.
- [ ] Source code được lưu trong Linux filesystem (`~/projects`).
- [ ] PostgreSQL và Redis chạy qua Compose, có named volumes.
- [ ] VS Code kết nối với WSL Ubuntu.

## 11. Tài liệu tham khảo chính thức

- [Docker — Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker — Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
- [Docker — Configure logging drivers](https://docs.docker.com/engine/logging/configure/)
- [Docker — Rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Docker — Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/)
- [Docker — BuildKit](https://docs.docker.com/build/buildkit/)
- [Microsoft — Systemd in WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd)
- [Microsoft — Advanced WSL configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)
- [Microsoft — Working across Windows and Linux file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems)

---

## Đưa trang vào MkDocs Material

Ví dụ lưu file tại:

```text
docs/
└── devops/
    └── docker/
        └── docker-engine-wsl-ubuntu.md
```

Khai báo menu trong `mkdocs.yml` (gộp vào `nav` hiện tại, **không tạo thêm một khóa `nav` thứ hai**):

```yaml title="mkdocs.yml"
nav:
  - DevOps:
      - Docker:
          - Docker Engine trên WSL Ubuntu: devops/docker/docker-engine-wsl-ubuntu.md
```

Để hiển thị đẹp các **admonition** (`!!! note`, `!!! tip`, `!!! warning`), **checklist** và **code block** có tiêu đề, kiểm tra phần Markdown extensions:

```yaml title="mkdocs.yml"
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tasklist:
      custom_checkbox: true
```

!!! note
    Nếu `mkdocs.yml` đã có các mục `markdown_extensions`, hãy **gộp** các extension trên vào danh sách sẵn có. Đừng ghi đè cấu hình mà hệ thống Knowledge Base đang sử dụng.
