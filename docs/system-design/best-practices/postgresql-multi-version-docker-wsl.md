---
title: PostgreSQL đa phiên bản trong WSL Ubuntu với Docker
description: Cài đặt, vận hành PostgreSQL 16/17/18 bằng Docker Compose trong WSL2 Ubuntu, kết nối DBeaver Windows và Spring Boot, sao lưu và xử lý lỗi mạng NAT.
tags:
  - PostgreSQL
  - Docker
  - WSL2
  - Spring Boot
  - Development
---

# PostgreSQL đa phiên bản trong WSL Ubuntu với Docker

> **Mục tiêu:** Chạy PostgreSQL trong **WSL2 Ubuntu + Docker Engine** để **Windows không phải cài PostgreSQL Server hoặc Docker Desktop**; hỗ trợ đồng thời PostgreSQL **16, 17, 18**, kết nối **DBeaver trên Windows** và các dự án **Spring Boot**.
>
> **Phạm vi:** Môi trường development trên một máy cá nhân, ưu tiên dễ bảo trì, dữ liệu bền vững, hạn chế mở dịch vụ ra mạng ngoài. Ví dụ mạng WSL là **NAT**.

## 1. Kiến trúc và nguyên tắc

```text
Windows 11
├── DBeaver / pgAdmin (chỉ là công cụ quản trị DB)
│   ├── 127.0.0.1:5436  ───────────┐
│   ├── 127.0.0.1:5437  ───────────┤ WSL NAT localhost forwarding
│   └── 127.0.0.1:5433  ───────────┘
│
└── WSL2 Ubuntu
    ├── Docker Engine + Docker Compose
    │   ├── postgres16:5432 ← WSL port 5436 ← postgres16_data
    │   ├── postgres17:5432 ← WSL port 5437 ← postgres17_data
    │   └── postgres:5432   ← WSL port 5433 ← postgres_data
    └── Spring Boot / Maven / Java 17
        └── jdbc:postgresql://127.0.0.1:<HOST_PORT>/app_db
```

| Thành phần | Khuyến nghị | Lý do |
|---|---|---|
| Docker | Docker Engine trong WSL Ubuntu | Không cần Docker Desktop trên Windows |
| Quản lý container | Một `compose.yaml` + Compose Profiles | Bật riêng phiên bản cần sử dụng |
| Version | `postgres:16`, `postgres:17`, `postgres:18` | Không dùng `latest`, tránh nâng major ngoài ý muốn |
| Storage | Mỗi major một **Docker Named Volume** | Không trộn data directory giữa các major |
| Cổng | Host khác nhau; bên trong đều `5432` | Tránh xung đột port |
| Network | Publish `127.0.0.1` | Hạn chế truy cập từ các interface khác của máy |
| Quản trị | DBeaver cài trên Windows | Không cần PostgreSQL Server trên Windows |

!!! tip "Nên chạy bao nhiêu phiên bản?"
    Chỉ **khởi động phiên bản đang cần**. Mỗi PostgreSQL đang chạy đều dùng RAM và tài nguyên hệ thống. Nếu chỉ cần kiểm thử tự động trên nhiều phiên bản, có thể cân nhắc **Testcontainers** thay vì giữ cả ba container chạy thường trực.

!!! warning "Không dùng chung dữ liệu cho các major version"
    PostgreSQL 16/17/18 có định dạng dữ liệu nội bộ riêng. **Không** mount cùng một data directory hoặc tự đổi image từ `postgres:17` sang `postgres:18` rồi dùng lại volume cũ. Muốn nâng major phải dùng quy trình migration (`pg_upgrade` hoặc dump/restore).

## 2. Điều kiện tiên quyết

Hướng dẫn này giả định đã cài **WSL2 Ubuntu, Docker Engine và Docker Compose plugin**. Trong terminal Ubuntu:

```bash
wslinfo --networking-mode      # Dự kiến: nat
docker --version
docker compose version
docker info                    # Xác nhận Docker daemon hoạt động
```

Nếu daemon chưa chạy và Ubuntu đã bật `systemd`:

```bash
sudo systemctl enable --now docker
```

> Nếu `docker info` bị lỗi quyền truy cập socket, kiểm tra cấu hình quyền Docker của Ubuntu. Không nên dùng `chmod 666 /var/run/docker.sock` để khắc phục.

Tạo thư mục trong **filesystem Linux**, không đặt dữ liệu PostgreSQL trực tiếp dưới `/mnt/c`:

```bash
mkdir -p ~/docker/postgres/backups
cd ~/docker/postgres
```

Cấu trúc:

```text
~/docker/postgres/
├── compose.yaml
├── .env
├── .gitignore
└── backups/
```

## 3. Tạo Docker Compose cho PostgreSQL 16/17/18

Tạo `~/docker/postgres/compose.yaml`:

```yaml title="compose.yaml"
x-postgres-common: &postgres-common
  restart: "no"                 # Chỉ bật phiên bản cần dùng khi phát triển
  shm_size: 256mb
  healthcheck:
    test:
      - CMD-SHELL
      - pg_isready -U "$${POSTGRES_USER}" -d "$${POSTGRES_DB}"
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 10s

services:
  postgres16:
    <<: *postgres-common
    image: postgres:16
    container_name: postgres16-dev
    profiles: [pg16]
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?required}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD_16:?required}
      POSTGRES_DB: ${POSTGRES_DB:?required}
    ports:
      - "127.0.0.1:5436:5432"    # HOST:CONTAINER
    volumes:
      - postgres16_data:/var/lib/postgresql/data

  postgres17:
    <<: *postgres-common
    image: postgres:17
    container_name: postgres17-dev
    profiles: [pg17]
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?required}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD_17:?required}
      POSTGRES_DB: ${POSTGRES_DB:?required}
    ports:
      - "127.0.0.1:5437:5432"
    volumes:
      - postgres17_data:/var/lib/postgresql/data

  postgres:
    <<: *postgres-common
    image: postgres:18
    container_name: postgres-dev
    profiles: [pg18]
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?required}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD_18:?required}
      POSTGRES_DB: ${POSTGRES_DB:?required}
    ports:
      - "127.0.0.1:5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres16_data:
  postgres17_data:
  postgres_data:
```

### Giải thích các cấu hình quan trọng

- `profiles: [pg16]`, `[pg17]`, `[pg18]`: Chỉ khởi động những phiên bản được chọn; có thể target service trực tiếp.
- `restart: "no"`: Không tự khởi động các DB ít sử dụng khi Docker daemon chạy. Với bản dùng thường xuyên, có thể đổi riêng service đó sang `unless-stopped`.
- `127.0.0.1:5433:5432`: **cổng host WSL `5433` → cổng container `5432`**. Thứ tự là `IP_HOST:HOST_PORT:CONTAINER_PORT`.
- `volumes`: Dữ liệu tách biệt, **không mất khi recreate container** nếu volume được giữ nguyên.
- `shm_size`: Tăng kích thước `/dev/shm` so với mức Docker mặc định. Không có nghĩa PostgreSQL tự được cấp 256 MB RAM cố định.
- `healthcheck`: Kiểm tra server sẵn sàng chấp nhận kết nối; **không thay thế kiểm tra username/password thật**.
- YAML anchor `&postgres-common` và alias `*postgres-common`: Tránh lặp cấu hình chung.

!!! warning "Đường dẫn volume thay đổi từ PostgreSQL 18"
    - **PostgreSQL 16/17:** mount `/var/lib/postgresql/data`.
    - **PostgreSQL 18:** mount `/var/lib/postgresql` (PGDATA mặc định ở dưới `/var/lib/postgresql/18/docker`).

    Đây là thay đổi của **PostgreSQL Official Docker Image**. Mount sai có thể khiến dữ liệu thực tế rơi vào anonymous volume và không được giữ đúng như mong đợi.

### Tạo file `.env`

```dotenv title=".env"
POSTGRES_USER=postgres
POSTGRES_DB=app_db

POSTGRES_PASSWORD_16=REPLACE_WITH_STRONG_PASSWORD_16
POSTGRES_PASSWORD_17=REPLACE_WITH_STRONG_PASSWORD_17
POSTGRES_PASSWORD_18=REPLACE_WITH_STRONG_PASSWORD_18
```

Tạo từng mật khẩu mạnh rồi thay các giá trị ví dụ:

```bash
openssl rand -hex 24
chmod 600 .env
```

Tạo `.gitignore`:

```gitignore title=".gitignore"
.env
backups/
```

!!! danger "Bảo mật"
    Không commit `.env` chứa mật khẩu thật lên Git. Biến môi trường trong Docker phục vụ **development**; người có quyền truy cập Docker thường có thể xem cấu hình container. Trong môi trường nhạy cảm cần dùng secret manager/phương thức quản lý credentials phù hợp.

!!! info "Nếu đã có PostgreSQL 18 từ lần cài trước"
    Nếu đang sử dụng volume cũ chứa dữ liệu, **giữ nguyên thư mục Compose và tên volume thực tế**. Việc đổi thư mục project, đổi tên volume, hoặc đổi từ khóa đặt tên của Compose có thể tạo **volume mới trống** làm bạn tưởng dữ liệu đã mất.

    Cấu hình mới dùng `POSTGRES_PASSWORD_18` thay cho `POSTGRES_PASSWORD`. Với **volume đã có dữ liệu**, biến này **không đổi password trong database**. Có thể đặt giá trị mới trong `.env` cho đúng mật khẩu hiện hành, hoặc thay đổi password bằng `psql` sau khi xác nhận kết nối.

## 4. Khởi động và quản lý từng phiên bản

Kiểm tra cấu hình trước khi chạy:

```bash
cd ~/docker/postgres
docker compose config --quiet
```

### Khởi động một phiên bản

=== "PostgreSQL 16"

    ```bash
    docker compose up -d postgres16
    ```

=== "PostgreSQL 17"

    ```bash
    docker compose up -d postgres17
    ```

=== "PostgreSQL 18"

    ```bash
    docker compose up -d postgres
    ```

Có thể dùng profile tương đương:

```bash
docker compose --profile pg18 up -d
```

### Khởi động nhiều phiên bản cùng lúc

```bash
docker compose \
  --profile pg16 \
  --profile pg17 \
  --profile pg18 \
  up -d
```

!!! note "Profiles không tự dừng service trước đó"
    Nếu đang chạy PostgreSQL 16 và bật profile 18 thì PostgreSQL 16 **không tự dừng**. Muốn tiết kiệm RAM, chủ động `stop` bản không dùng.

### Các lệnh thường dùng

| Tác vụ | Lệnh (ví dụ PostgreSQL 18) |
|---|---|
| Khởi động | `docker compose up -d postgres` |
| Dừng | `docker compose stop postgres` |
| Chạy lại container đã dừng | `docker compose start postgres` |
| Restart | `docker compose restart postgres` |
| Xem container | `docker ps -a --filter name=postgres` |
| Xem log | `docker compose logs -f postgres` |
| Kiểm tra tài nguyên | `docker stats postgres-dev` |
| Xem port thực tế | `docker port postgres-dev` |
| Vào psql | `docker compose exec postgres psql -U postgres -d app_db` |
| Xóa container, giữ volume | `docker compose down` |

!!! danger "Tuyệt đối cẩn thận với `down -v`"
    `docker compose down -v` có thể **xóa các named volume do Compose quản lý và toàn bộ dữ liệu tương ứng**. Không dùng trong quá trình vận hành thông thường.

## 5. Kiểm tra PostgreSQL và port mapping

Ví dụ PostgreSQL 18 dùng host port **5433**:

```bash
# Trong WSL Ubuntu
docker ps --filter name=postgres-dev
docker port postgres-dev
```

Kết quả mong đợi:

```text
5432/tcp -> 127.0.0.1:5433
```

**Phân biệt quan trọng:**

```text
127.0.0.1:5433->5432/tcp     # ĐÚNG: host 5433 → container 5432
127.0.0.1:5432->5433/tcp     # SAI khi PostgreSQL container nghe 5432
```

Xem cổng mà PostgreSQL thực sự lắng nghe bên trong container:

```bash
docker exec postgres-dev \
  psql -U postgres -d app_db -c "SHOW port;"
```

Kết quả thông thường là `5432`.

Kiểm tra **TCP từ Ubuntu tới host-published port**:

```bash
nc -vz 127.0.0.1 5433
```

Nếu chưa có `nc`: `sudo apt-get update && sudo apt-get install -y netcat-openbsd`.

!!! tip "Đổi port không cần xóa volume"
    Sau khi sửa `ports:` trong `compose.yaml`, áp dụng bằng:

    ```bash
    docker compose up -d --force-recreate postgres
    ```

    Container được tạo lại nhưng named volume vẫn giữ nguyên. Kiểm tra bằng `docker port postgres-dev`.

## 6. Kết nối DBeaver trên Windows (WSL2 NAT)

DBeaver **chạy trên Windows**, PostgreSQL Server **chạy trong Docker của WSL**.

| PostgreSQL | Host | Port | Database | User |
|---|---|---:|---|---|
| 16 | `127.0.0.1` | `5436` | `app_db` | `postgres` |
| 17 | `127.0.0.1` | `5437` | `app_db` | `postgres` |
| 18 | `127.0.0.1` | `5433` | `app_db` | `postgres` |

Trong **DBeaver → New Database Connection → PostgreSQL**:

1. Host: `127.0.0.1`.
2. Port: `5433` (nếu dùng PostgreSQL 18).
3. Database: `app_db`.
4. Username: `postgres`; Password: mật khẩu thực tế **đang lưu trong DB**.
5. Chọn **Test Connection**.

Trước khi kiểm tra trong DBeaver, mở **Windows PowerShell**:

```powershell
Test-NetConnection 127.0.0.1 -Port 5433
```

- `TcpTestSucceeded : True`: Windows đã truy cập được tới cổng TCP; tiếp tục kiểm tra tài khoản, DB name, SSL/authentication trong DBeaver.
- `TcpTestSucceeded : False`: **chưa tới bước xác thực PostgreSQL**; kiểm tra Docker port mapping và đường kết nối Windows ↔ WSL.

!!! note "WSL NAT và localhost forwarding"
    Theo Microsoft, WSL2 NAT mặc định hỗ trợ Windows truy cập Linux server qua `localhost`. Tuy nhiên, tùy phiên bản WSL và cách Docker publish cổng, có thể xảy ra trường hợp **TCP trong WSL thành công nhưng Windows thất bại**. Không kết luận ngay lỗi do password hoặc DBeaver.

### Nếu Windows không truy cập được nhưng WSL truy cập được

Thực hiện **theo thứ tự**, chưa vội tắt firewall hoặc mở port ra LAN:

**Bước 1 – kiểm tra port publish:**

```bash
# WSL
docker port postgres-dev
nc -vz 127.0.0.1 5433
```

**Bước 2 – kiểm tra port trên Windows:**

```powershell
# Windows PowerShell
Test-NetConnection 127.0.0.1 -Port 5433
Get-NetTCPConnection -LocalPort 5433 -ErrorAction SilentlyContinue
```

Lệnh thứ hai giúp kiểm tra port đã bị tiến trình khác chiếm trên Windows hay chưa; kết quả rỗng không tự nó chứng minh WSL forwarding hỏng.

**Bước 3 – kiểm tra `.wslconfig` (trên Windows):**

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Nội dung liên quan:

```ini title="%USERPROFILE%\.wslconfig"
[wsl2]
networkingMode=nat
localhostForwarding=true
```

`localhostForwarding` mặc định là `true`; chỉ cần khai báo nếu bạn muốn quản lý tường minh. **Giữ các cấu hình WSL khác đang dùng**, không thay thế toàn bộ file chỉ bằng hai dòng trên.

Nếu đã sửa `.wslconfig`, đóng ứng dụng WSL đang chạy rồi từ PowerShell:

```powershell
wsl --shutdown
```

Mở lại Ubuntu và bật PostgreSQL:

```bash
cd ~/docker/postgres
docker compose up -d postgres
```

**Bước 4 – nếu vẫn thất bại:**

- Kiểm tra `docker info`, `docker ps`, Docker daemon và trạng thái WSL.
- Kiểm tra sự trùng port với dịch vụ PostgreSQL/ứng dụng khác trên Windows.
- Nếu buộc phải kết nối qua **WSL IP** thay cho localhost, phải kiểm tra lại Docker bind address, đường đi mạng và firewall. **Không tự đổi thành `0.0.0.0` hoặc dùng `netsh portproxy` như giải pháp đầu tiên**, vì có thể mở dịch vụ DB ngoài ý muốn.

### Bảng xử lý lỗi nhanh

| Hiện tượng | Nguyên nhân cần kiểm tra | Hướng xử lý |
|---|---|---|
| `TcpTestSucceeded: False` | Sai host port, Docker chưa publish, WSL forwarding | `docker port`, kiểm tra TCP trong WSL, `.wslconfig` |
| `Connection refused` | Không có server lắng nghe tại địa chỉ/port đã chọn | Kiểm tra container, port mapping |
| `Connection timed out` | Đường mạng/firewall không chuyển gói đến đích | Kiểm tra WSL/Windows network và firewall |
| `password authentication failed` | Sai mật khẩu thực tế trong DB | Kiểm tra password khởi tạo, đổi mật khẩu qua `psql` |
| `database ... does not exist` | Sai tên DB hoặc DB chưa được tạo | `psql -l`; tạo DB đúng server |
| Có DB nhưng dữ liệu "biến mất" sau recreate | Compose project/volume name thay đổi | `docker volume ls`, `docker inspect`, rà soát tên volume |

## 7. Sử dụng với Spring Boot / Java trong WSL

### Backend Spring Boot chạy trực tiếp trong WSL Ubuntu

Dùng **host port** đã publish:

```yaml title="application-local.yml"
spring:
  datasource:
    url: jdbc:postgresql://127.0.0.1:5433/app_db
    username: ${DB_USERNAME:app_user}
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver
```

- PostgreSQL 16: thay `5433` bằng `5436`.
- PostgreSQL 17: thay `5433` bằng `5437`.
- PostgreSQL 18: giữ `5433`.
- Thêm dependency PostgreSQL JDBC Driver qua Maven/Gradle nếu dự án chưa có.
- Tránh đưa password thật vào Git; inject qua environment variables / secrets.

### Backend Spring Boot cũng chạy trong Docker

Nếu container Spring Boot **cùng Compose network** với PostgreSQL 18, dùng **service name và container port**:

```properties
spring.datasource.url=jdbc:postgresql://postgres:5432/app_db
```

Tương tự PostgreSQL 16 dùng `postgres16:5432`; PostgreSQL 17 dùng `postgres17:5432`.

!!! warning "Không dùng `localhost` trong container Spring Boot để trỏ sang DB container khác"
    `localhost` trong container Spring Boot chỉ trỏ về **chính container Spring Boot**. Nếu hai ứng dụng ở **hai Compose project khác nhau**, chúng không mặc nhiên dùng cùng Docker network; cần cấu hình shared network trước khi sử dụng tên service của nhau.

## 8. Thao tác database, role và mật khẩu

Truy cập PostgreSQL 18 từ Ubuntu:

```bash
docker compose exec postgres psql -U postgres -d app_db
```

Các lệnh `psql` hữu ích:

```sql
\conninfo
\l
\du
\dn
\dt
SELECT version();
SHOW port;
\q
```

Tạo role cho ứng dụng (ví dụ ứng dụng cần quản lý schema qua Flyway/Liquibase):

```sql
CREATE ROLE app_user LOGIN;
GRANT CONNECT ON DATABASE app_db TO app_user;
GRANT USAGE, CREATE ON SCHEMA public TO app_user;
```

Đặt mật khẩu tương tác trong `psql` (không ghi thẳng password vào lịch sử câu lệnh):

```text
\password app_user
```

!!! note "Phân quyền"
    Ví dụ trên phù hợp khi role ứng dụng cần tạo bảng trong schema `public` của **DB hiện tại**. Nếu bảng đã tồn tại và thuộc role khác, cần cấp quyền trên bảng/sequence tương ứng. Với production, nên tách **migration role** (DDL) và **runtime role** (DML) theo nguyên tắc least privilege.

### Đổi password PostgreSQL đã có volume

Thay `.env` **không tự đổi mật khẩu** trong database đã được khởi tạo. Muốn đổi tài khoản quản trị:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

Trong `psql`:

```text
\password postgres
```

Sau đó cập nhật mật khẩu tương ứng trong `.env`/DBeaver/app để không bị lệch. Với kết nối remote, mật khẩu được yêu cầu theo cấu hình authentication hiện hành; việc `psql` chạy được **ngay trong container** chưa chứng minh mật khẩu kết nối từ DBeaver là đúng.

## 9. Backup và restore đúng cách

Named Volume giúp data tồn tại qua **container recreate**, nhưng **không thay thế backup**. Nên chép backup quan trọng ra khỏi WSL virtual disk, ví dụ sang một ổ lưu trữ khác sau khi xuất.

### Backup PostgreSQL 18

```bash
cd ~/docker/postgres
mkdir -p backups

docker compose exec -T postgres \
  pg_dump -U postgres -d app_db -Fc \
  > "backups/app_db_pg18_$(date +%F_%H%M%S).dump"
```

- `-Fc`: PostgreSQL custom archive, hỗ trợ `pg_restore`.
- `-T`: Tắt pseudo-TTY, phù hợp khi redirect ra file binary.
- `pg_dump` backup **một database**, không bao gồm toàn bộ role/global objects của PostgreSQL cluster.

### Kiểm tra file backup

```bash
ls -lh backups/
pg_restore --list backups/app_db_pg18_YYYY-MM-DD_HHMMSS.dump | head
```

Nếu Ubuntu không có `pg_restore` cục bộ, dùng:

```bash
docker compose exec -T postgres pg_restore --list \
  < backups/app_db_pg18_YYYY-MM-DD_HHMMSS.dump | head
```

### Restore vào database rỗng (khuyến nghị)

Tạo trước một DB mới, ví dụ `app_db_restore`:

```bash
docker compose exec -T postgres \
  psql -U postgres -d postgres \
  -c 'CREATE DATABASE app_db_restore;'
```

Restore:

```bash
docker compose exec -T postgres \
  pg_restore -U postgres -d app_db_restore \
  --no-owner --no-acl \
  < backups/app_db_pg18_YYYY-MM-DD_HHMMSS.dump
```

!!! danger "Không restore nhầm database"
    Restore có thể tạo/ghi đè đối tượng và thất bại khi object đã tồn tại. Luôn xác nhận đúng **server, version, database** trước khi chạy. Không tùy tiện dùng `--clean` trên DB có dữ liệu quan trọng.

### Backup database khác

Thay `postgres` (service name) và cổng theo phiên bản:

```bash
# PostgreSQL 17
# Sử dụng service postgres17 và database app_db
docker compose exec -T postgres17 \
  pg_dump -U postgres -d app_db -Fc \
  > backups/app_db_pg17.dump
```

!!! note "Backup và version compatibility"
    Khi di chuyển dữ liệu giữa major version, kiểm tra **phiên bản `pg_dump`/`pg_restore`** và các extension tương ứng. Không xem một file backup là đảm bảo restore được vào mọi major PostgreSQL.

## 10. Tối ưu tài nguyên và vận hành lâu dài

1. **Chỉ bật các container đang cần:** `docker compose stop postgres16 postgres17` nếu đang dùng PostgreSQL 18.
2. **Đo trước khi tune:** `docker stats`, `free -h`, `docker system df`. Không tự tăng `shared_buffers`, `work_mem`, `max_connections` nếu chưa có workload đo được.
3. **Named Volume nằm trong storage Linux của Docker:** tránh bind-mount data PostgreSQL vào `/mnt/c/...` vì hiệu năng filesystem và đặc tính I/O có thể bất lợi.
4. **Không dùng `latest`:** cố định major; cập nhật minor/patch có kiểm tra và backup.
5. **Không tự động publish toàn bộ interface:** ưu tiên `127.0.0.1` cho máy cá nhân; chỉ mở truy cập từ mạng ngoài khi có yêu cầu và phương án firewall/authentication rõ ràng.
6. **Backup ra nơi độc lập:** VM/distro WSL và named volume không phải hệ thống sao lưu.
7. **Kiểm tra dung lượng:** `docker volume ls`, `docker system df -v`; đừng `docker volume prune` khi chưa xác minh các volume cần giữ.

## 11. Checklist triển khai

- [ ] Docker Engine và `docker compose` hoạt động trong Ubuntu.
- [ ] Các file đặt tại `~/docker/postgres` trên Linux filesystem.
- [ ] `.env` có mật khẩu mạnh, `chmod 600`, đã được `.gitignore`.
- [ ] PostgreSQL 16/17 mount `/var/lib/postgresql/data`; PostgreSQL 18 mount `/var/lib/postgresql`.
- [ ] Port mapping là `HOST_PORT:5432`, **không bị đảo ngược**.
- [ ] `docker compose config --quiet` thành công.
- [ ] `docker ps` cho thấy container `healthy` và port được publish đúng.
- [ ] `nc -vz 127.0.0.1 5433` trong WSL thành công (đối với PostgreSQL 18).
- [ ] `Test-NetConnection 127.0.0.1 -Port 5433` trong Windows thành công.
- [ ] DBeaver kết nối và chạy `SELECT version();` thành công.
- [ ] Spring Boot kết nối bằng host port; nếu chạy container cùng network thì dùng service name.
- [ ] Đã thử **backup và restore vào DB kiểm thử**, không chỉ tạo file backup.

## 12. Tài liệu tham khảo chính thức

1. [Docker Official Image — PostgreSQL](https://hub.docker.com/_/postgres) — Environment variables, data volumes, initialization.
2. [PostgreSQL Docker Official Image README](https://github.com/docker-library/docs/blob/master/postgres/README.md) — `PGDATA` và thay đổi volume từ PostgreSQL 18.
3. [Docker Compose — Profiles](https://docs.docker.com/reference/compose-file/profiles/) — Bật tắt service theo profile.
4. [Docker Compose — Networking](https://docs.docker.com/compose/how-tos/networking/) — Phân biệt `HOST_PORT`, `CONTAINER_PORT`, service DNS.
5. [Microsoft — Accessing network applications with WSL](https://learn.microsoft.com/en-us/windows/wsl/networking) — Kết nối Windows ↔ WSL trong NAT.
6. [Microsoft — Advanced settings configuration in WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) — `localhostForwarding` và `.wslconfig`.
7. [PostgreSQL — Backup and Restore](https://www.postgresql.org/docs/current/backup.html) — Backup/restore chuẩn PostgreSQL.
8. [Material for MkDocs — Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) và [Content Tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/) — Cú pháp trình bày tài liệu.

---

**Tóm tắt:** Một Docker Engine trong WSL Ubuntu có thể phục vụ nhiều dự án qua PostgreSQL 16/17/18. **Mỗi major có service, host port và volume riêng**; bật đúng phiên bản bằng Docker Compose Profiles; Windows chỉ cần DBeaver, không cần PostgreSQL Server. Với ví dụ PostgreSQL 18, **Windows/WSL kết nối `127.0.0.1:5433`**, còn port **bên trong container luôn là `5432`**.
