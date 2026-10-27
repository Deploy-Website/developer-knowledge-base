---
title: VS Code Windows + WSL Ubuntu + Git Merge với TortoiseGitMerge
description: Thiết lập VS Code Remote WSL, sử dụng toolchain Linux và xử lý Git conflict bằng TortoiseGitMerge trên Windows.
---

# VS Code trên Windows + WSL Ubuntu + Git Merge với TortoiseGitMerge

> **Mục tiêu:** VS Code chạy giao diện trên Windows, còn source code, Java, Maven, Node.js/npm, Git và Docker Engine chạy trong **WSL Ubuntu**. Tất cả các thao tác Git dùng **Git Ubuntu**; khi gặp conflict, `git mergetool` có thể mở **TortoiseGitMerge trên Windows** để chỉnh sửa file.

!!! abstract "Phạm vi"
    - Áp dụng cho máy đã cài WSL 2/Ubuntu, VS Code Windows, Git Ubuntu, Java 17, Maven, NVM/Node.js và Docker Engine Ubuntu.
    - **Không cài lại** toolchain trong hướng dẫn này; chỉ kiểm tra và tích hợp.
    - Ví dụ sử dụng distro `Ubuntu`, user Linux `vinhnt` và thư mục dự án `~/workspace`. Thay tên nếu máy của bạn khác.
    - Cấu hình gọi TortoiseGitMerge thông qua WSL là **tích hợp tùy chỉnh**: cần kiểm thử trên máy thật, nhất là khả năng đọc/ghi đường dẫn `\\wsl.localhost` và thao tác lưu file của phiên bản TortoiseGitMerge hiện có.

## 1. Kiến trúc và nguyên tắc

```text
Windows 11
├── VS Code Desktop (giao diện)
├── WSL Extension (Microsoft)
├── TortoiseGitMerge.exe (chỉ là công cụ giải conflict)
└── Trình duyệt / các ứng dụng desktop
                │
                │ VS Code Remote / WSL interoperability
                ▼
WSL Ubuntu 2
├── VS Code Server + các extension chạy trong WSL
├── /home/vinhnt/workspace/<project>/     ← source code và .git
├── Git Ubuntu                             ← commit / fetch / pull / push / merge / rebase
├── Git custom mergetool                    ← gọi TortoiseGitMerge.exe
├── Java 17 + Maven
├── NVM + Node.js + npm
└── Docker Engine + Docker CLI
```

**Quy tắc:**

1. Lưu dự án trong filesystem Ubuntu (`/home/...`), **không** đặt source code cần build bằng Linux tại `/mnt/c/...`.
2. Sử dụng **Git Ubuntu** cho toàn bộ vòng đời repository; không luân phiên TortoiseGit/ Git for Windows để thao tác `.git`.
3. Chỉ gọi chương trình Windows bằng đường dẫn rõ ràng khi có nhu cầu (VS Code, TortoiseGitMerge).
4. Sau khi sử dụng merge GUI, **luôn kiểm tra nội dung và trạng thái Git** trước khi hoàn tất merge/rebase.

## 2. Kiểm tra môi trường WSL Ubuntu

Trong **PowerShell (Windows)**:

```powershell
wsl --list --verbose
wsl -d Ubuntu
```

Trong **Ubuntu**:

```bash
printf 'Distro: '; cat /etc/os-release | grep '^PRETTY_NAME='

type -a java javac mvn node npm git docker
java -version
mvn -version
node -v
npm -v
git --version
docker info
```

!!! tip "`/usr/bin` và `/bin`"
    Nếu `type -a java` hiển thị cả `/usr/bin/java` và `/bin/java` thì thường là bình thường do cơ chế *merged-/usr*. Chú ý **không** để các bản Maven/Node/npm trên Windows (`/mnt/c/...`) được ưu tiên trước công cụ Linux.

### 2.1. Tách Windows PATH và Linux PATH (khuyến nghị)

Mở `/etc/wsl.conf` **trong Ubuntu**:

```bash
sudo nano /etc/wsl.conf
```

Đảm bảo có section sau (chỉ **một** section `[interop]`; giữ nguyên các section hiện có khác):

```ini
[interop]
enabled=true
appendWindowsPath=false
```

- `enabled=true`: vẫn cho phép gọi ứng dụng Windows `.exe` từ WSL.
- `appendWindowsPath=false`: không tự động ghép toàn bộ Windows PATH vào Linux PATH.

!!! warning "Nếu đang dùng Docker Engine với systemd"
    Không xóa hoặc ghi đè `[boot]`/`systemd=true` đang sử dụng. Đây là thiết lập độc lập với `[interop]`.

Sau khi lưu, mở **PowerShell**:

```powershell
wsl --terminate Ubuntu
wsl -d Ubuntu
```

Kiểm tra lại:

```bash
type -a mvn node npm
printf '%s\n' "$PATH" | tr ':' '\n' | grep -E '^/mnt/[a-z]/' || true
```

## 3. Cài VS Code Windows và kết nối WSL

### 3.1. Cài extension WSL

1. Cài **Visual Studio Code cho Windows**, không cài bản Desktop Linux trong Ubuntu.
2. Mở VS Code Windows → Extensions (`Ctrl+Shift+X`).
3. Cài extension **WSL** của **Microsoft** (`ms-vscode-remote.remote-wsl`).
4. Extension sẽ thiết lập **VS Code Server** trong Ubuntu ở lần kết nối đầu tiên.

### 3.2. Đặt dự án trong filesystem Ubuntu

Trong Ubuntu:

```bash
mkdir -p ~/workspace/backend ~/workspace/frontend
cd ~/workspace/backend
# Ví dụ (thay URL repository của bạn)
git clone <repository-url>
cd <project-directory>
```

Mở từ terminal Ubuntu:

```bash
code .
```

Sau khi kết nối thành công, VS Code phải hiển thị trạng thái **`WSL: Ubuntu`** ở góc dưới bên trái. Mở Terminal của VS Code (`` Ctrl+` ``) để chạy các lệnh Linux.

Cách khác: từ VS Code Windows nhấn `Ctrl+Shift+P` → **WSL: Connect to WSL using Distro...** → chọn **Ubuntu** → **File → Open Folder** → `/home/vinhnt/workspace/...`.

### 3.3. Khắc phục `code: command not found` khi tắt Windows PATH

VS Code Windows có thể được cài theo **User Installer** hoặc **System Installer**. Trong Ubuntu, kiểm tra đường dẫn thực tế trước:

```bash
ls -ld "/mnt/c/Users/vinh.nt/AppData/Local/Programs/Microsoft VS Code/bin" \
       "/mnt/c/Program Files/Microsoft VS Code/bin" 2>/dev/null
```

Nếu cài theo User Installer như ví dụ, thêm vào cuối `~/.bashrc`:

```bash
# Chỉ cho phép gọi VS Code Windows; không thêm toàn bộ Windows PATH.
VSCODE_BIN="/mnt/c/Users/vinh.nt/AppData/Local/Programs/Microsoft VS Code/bin"
if [ -d "$VSCODE_BIN" ]; then
    case ":$PATH:" in
        *":$VSCODE_BIN:"*) ;; # đã có trong PATH
        *) export PATH="$PATH:/mnt/c/Windows/System32:$VSCODE_BIN" ;;
    esac
fi
```

Nếu cài VS Code dạng System Installer, thay giá trị `VSCODE_BIN` bằng thư mục `bin` tương ứng trong `Program Files`. Sau đó:

```bash
source ~/.bashrc
command -v code
code .
```

!!! note
    Nếu không cần `code .`, bạn vẫn có thể kết nối hoàn toàn bằng giao diện VS Code Windows và chọn **Open Folder** trong WSL; không bắt buộc sửa `~/.bashrc`.

### 3.4. Extensions và kiểm tra công cụ chạy trong Ubuntu

Trong cửa sổ VS Code đang kết nối WSL, cài các extension cần thiết vào môi trường **WSL: Ubuntu**:

| Nhóm | Extension gợi ý |
|---|---|
| Java/Spring | Extension Pack for Java; Spring Boot Extension Pack (nếu dùng Spring Boot) |
| Maven | Maven for Java (thường có trong Java Extension Pack) |
| Nuxt/Vue | Vue (Official), ESLint |
| Docker | Docker extension (nếu cần giao diện quản lý container) |

Trong Terminal VS Code chạy:

```bash
pwd
command -v java mvn node npm git docker
mvn -version
node -v
npm -v
docker info
```

Các lệnh trên phải chạy bằng Ubuntu. Docker CLI trong Ubuntu phải kết nối được Docker Engine ở Ubuntu; **không cần Docker Desktop** cho mô hình này.

## 4. Git Ubuntu là công cụ Git duy nhất

### 4.1. Cấu hình Git trong Ubuntu

```bash
git --version
command -v git
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Dùng thông tin thực tế của bạn thay cho `Your Name` và email ví dụ. Kiểm tra:

```bash
git config --show-origin --get user.name
git config --show-origin --get user.email
git config --show-origin --get core.autocrlf || true
```

!!! tip "Line endings"
    Với dự án nhiều hệ điều hành, ưu tiên thống nhất EOL bằng `.gitattributes` trong repository thay vì mỗi người tùy chỉnh khác nhau. Không đổi `core.autocrlf` hoặc chạy chuẩn hóa toàn bộ file hàng loạt khi chưa đánh giá ảnh hưởng tới diff và quy ước của nhóm.

### 4.2. Commit và xem thay đổi bằng VS Code

- Mở **Source Control** (`Ctrl+Shift+G`) trong cửa sổ **WSL: Ubuntu**.
- Review file changes → Stage → nhập commit message → Commit.
- Branch, Pull, Push, lịch sử/graph có thể thao tác qua Source Control hoặc terminal.
- Git được VS Code Remote WSL sử dụng nằm trong **Ubuntu**, không phải Git for Windows.

Các lệnh tương đương:

```bash
git status
git diff
git add src/main/java/.../LoginService.java
git commit -m "fix: handle login validation"
git push
```

!!! warning
    Không dùng TortoiseGit Windows để commit/merge/rebase trực tiếp trên cùng repo nằm trong `\\wsl.localhost\Ubuntu\...`. Cách này có thể dùng được trong một số trường hợp, nhưng dễ tạo khác biệt về cấu hình, đường dẫn và hiệu năng. **TortoiseGitMerge** trong hướng dẫn này chỉ là GUI sửa kết quả merge.

## 5. Tích hợp TortoiseGitMerge (Windows) vào Git Ubuntu

### 5.1. Điều kiện

TortoiseGit đã được cài trên Windows, và file sau tồn tại (đường dẫn mặc định):

```text
C:\Program Files\TortoiseGit\bin\TortoiseGitMerge.exe
```

Trong Ubuntu kiểm tra:

```bash
command -v wslpath
ls -l "/mnt/c/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe"
```

Nếu đường dẫn khác, thay biến `TORTOISE_GIT_MERGE_EXE` trong script dưới đây hoặc đặt biến môi trường trỏ tới file thực tế.

### 5.2. Git truyền những file nào cho mergetool?

| Biến Git | Tham số TortoiseGitMerge | Mục đích |
|---|---|---|
| `$BASE` | `/base:` | Phiên bản tổ tiên chung (nếu có) |
| `$LOCAL` | `/mine:` | Phiên bản phía hiện tại theo ngữ cảnh Git |
| `$REMOTE` | `/theirs:` | Phiên bản phía còn lại |
| `$MERGED` | `/merged:` | Đường dẫn file kết quả phải lưu |

!!! warning "`ours` và `theirs` khi rebase"
    Trong **rebase**, ý nghĩa trực giác của current/incoming có thể bị đảo so với merge thường. Luôn đọc nội dung từng phía trước khi chọn; không mặc định `mine` luôn là "code của tôi".

### 5.3. Tạo wrapper Bash chuyển đường dẫn WSL → Windows

Trong Ubuntu:

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/tgit-merge-wsl
```

Nội dung `~/.local/bin/tgit-merge-wsl`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Git cung cấp BASE, LOCAL, REMOTE, MERGED theo thứ tự này.
if (( $# != 4 )); then
    echo "Usage: $0 BASE LOCAL REMOTE MERGED" >&2
    exit 2
fi

BASE_FILE=$1
LOCAL_FILE=$2
REMOTE_FILE=$3
MERGED_FILE=$4

# Chỉ gọi .exe trên Windows, KHÔNG dùng Git for Windows.
TGM_EXE="${TORTOISE_GIT_MERGE_EXE:-/mnt/c/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe}"

if [[ ! -f "$TGM_EXE" ]]; then
    echo "TortoiseGitMerge not found: $TGM_EXE" >&2
    exit 1
fi

if ! command -v wslpath >/dev/null 2>&1; then
    echo "wslpath is not available" >&2
    exit 1
fi

# Wrapper dành cho conflict text có đủ input/output file.
for file in "$LOCAL_FILE" "$REMOTE_FILE" "$MERGED_FILE"; do
    if [[ ! -f "$file" ]]; then
        echo "Missing merge file: $file" >&2
        echo "Handle delete/modify or special conflicts manually with Git." >&2
        exit 1
    fi
done

TEMP_BASE=""
cleanup() {
    if [[ -n "$TEMP_BASE" ]]; then
        rm -f -- "$TEMP_BASE"
    fi
}
trap cleanup EXIT

# Một số conflict không có common ancestor; dùng file base rỗng.
if [[ -n "$BASE_FILE" && -f "$BASE_FILE" ]]; then
    BASE_WIN=$(wslpath -aw "$BASE_FILE")
else
    TEMP_BASE=$(mktemp)
    BASE_WIN=$(wslpath -aw "$TEMP_BASE")
fi

LOCAL_WIN=$(wslpath -aw "$LOCAL_FILE")
REMOTE_WIN=$(wslpath -aw "$REMOTE_FILE")
MERGED_WIN=$(wslpath -aw "$MERGED_FILE")

# Đợi chương trình đóng; Git sẽ tự xác nhận trạng thái kết quả.
"$TGM_EXE" \
    "/base:$BASE_WIN" \
    "/mine:$LOCAL_WIN" \
    "/theirs:$REMOTE_WIN" \
    "/merged:$MERGED_WIN" \
    /saverequired
```

Cấp quyền và kiểm tra cú pháp:

```bash
chmod +x ~/.local/bin/tgit-merge-wsl
bash -n ~/.local/bin/tgit-merge-wsl
```

**Giải thích:** `wslpath -aw` đổi các file tạm và file kết quả của Git từ đường dẫn Linux sang đường dẫn Windows UNC; các đối số được đặt trong dấu nháy để xử lý tên file có khoảng trắng. `/saverequired` khiến TortoiseGitMerge hỏi lưu khi đóng, kể cả khi chưa sửa file.

!!! danger "Quan trọng về xác nhận thành công"
    Script không tự chứng minh nội dung merge là đúng. Sau khi GUI đóng, Git có thể đánh dấu đã xử lý dựa vào việc file kết quả thay đổi. **Bạn phải review diff và kiểm tra conflict markers trước khi commit.** Nếu chương trình không chờ tới lúc cửa sổ đóng trên máy của bạn, không sử dụng wrapper cho đến khi kiểm tra và sửa được cơ chế chờ.

### 5.4. Đăng ký Git mergetool

Trong **Ubuntu**:

```bash
git config --global merge.tool tgit-wsl

git config --global mergetool.tgit-wsl.cmd \
  '"$HOME/.local/bin/tgit-merge-wsl" "$BASE" "$LOCAL" "$REMOTE" "$MERGED"'

# Không mặc định tin cậy exit code của GUI.
git config --global mergetool.tgit-wsl.trustExitCode false

# Giữ .orig backup trong giai đoạn đầu thử nghiệm.
git config --global mergetool.keepBackup true
```

Kiểm tra:

```bash
git config --global --get merge.tool
git config --global --get mergetool.tgit-wsl.cmd
git config --global --get mergetool.tgit-wsl.trustExitCode
```

Kết quả lần lượt phải chứa `tgit-wsl`, đường dẫn script và `false`.

!!! info "Thay đổi tác dụng của cấu hình"
    Đây là **global Git config của user Ubuntu** (`~/.gitconfig`), nên áp dụng cho nhiều repo Linux. Nếu chỉ muốn dùng cho **một project**, bỏ `--global` và chạy trong repository đó. Không chỉnh `.gitconfig` của Windows.

## 6. Workflow merge thực tế cho project

Ví dụ merge branch `feature/login` vào branch `develop`:

### Bước 1. Cập nhật nhánh đích, đảm bảo working tree sạch

```bash
cd ~/workspace/backend/my-spring-app
code .
git status

git fetch origin
git switch develop
git pull --ff-only origin develop
```

!!! warning
    Không merge khi còn thay đổi chưa commit/stash mà bạn chưa chủ động xử lý. Nếu `develop` là protected branch hoặc quy trình nhóm dùng Pull Request, hãy merge qua PR thay vì tự đẩy lên branch chung.

### Bước 2. Merge và phát hiện conflict

```bash
git merge feature/login
```

Git có thể báo:

```text
CONFLICT (content): Merge conflict in src/main/java/.../LoginService.java
Automatic merge failed; fix conflicts and then commit the result.
```

Liệt kê file chưa giải quyết:

```bash
git diff --name-only --diff-filter=U
```

### Bước 3. Mở TortoiseGitMerge

Chỉ một file:

```bash
git mergetool -- src/main/java/.../LoginService.java
```

Hoặc toàn bộ file conflict theo thứ tự:

```bash
git mergetool
```

Trên TortoiseGitMerge:

1. Đọc **Mine**, **Theirs** và nội dung **Merged**.
2. Chọn/chỉnh từng khối conflict phù hợp logic nghiệp vụ.
3. Lưu file kết quả rồi đóng cửa sổ.
4. Nếu Git hỏi conflict đã được giải quyết chưa, chỉ xác nhận **yes** sau khi đã lưu và kiểm tra.

### Bước 4. Review và kết thúc merge

```bash
# Còn file nào unmerged?
git diff --name-only --diff-filter=U

# Kiểm tra trạng thái, phần đã stage và whitespace/conflict markers.
git status
git diff --cached
git diff --cached --check

# Hoàn tất khi không còn conflict và đã review.
git merge --continue
```

`git mergetool` thường stage file sau khi bạn xác nhận resolved. Nếu Git chưa stage một file đã xử lý, cần kiểm tra lại file rồi dùng `git add <file>`.

Có thể chạy build/test liên quan trước khi hoàn tất, ví dụ:

```bash
mvn test
# hoặc với dự án frontend:
# npm test
```

`npm test` chỉ chạy nếu project có script `test` tương ứng.

Đẩy code nếu quy trình nhóm cho phép:

```bash
git push origin develop
```

### Trường hợp rebase hoặc cần hủy thao tác

| Tình huống | Lệnh sau khi đã xử lý conflict |
|---|---|
| Merge | `git merge --continue` |
| Rebase | `git rebase --continue` |
| Cherry-pick | `git cherry-pick --continue` |
| Hủy merge chưa hoàn tất | `git merge --abort` |
| Hủy rebase chưa hoàn tất | `git rebase --abort` |

!!! warning
    `merge --abort`/`rebase --abort` không phải bản sao lưu thay thế commit/stash; khả năng phục hồi có thể bị giới hạn nếu trước đó working tree chứa thay đổi không được lưu.

## 7. Tạo VS Code Task để gọi TortoiseGitMerge

Tạo file `.vscode/tasks.json` trong dự án, nếu chưa có (nếu đã có, **gộp** task thay vì ghi đè toàn bộ):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Git: Resolve Conflicts (TortoiseGitMerge)",
      "type": "shell",
      "command": "git mergetool",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    }
  ]
}
```

Trong cửa sổ **WSL: Ubuntu** → **Terminal → Run Task** → chọn task trên. Task dùng terminal của WSL, do đó sử dụng Git Ubuntu và custom mergetool vừa cấu hình.

!!! tip
    Nếu task chỉ hữu ích cho một cá nhân, không nhất thiết commit `tasks.json` vào repository chung của cả nhóm.

## 8. Troubleshooting

| Hiện tượng | Kiểm tra và xử lý |
|---|---|
| `code: command not found` | Mở qua VS Code UI hoặc thêm **chỉ** VS Code bin vào PATH trong Ubuntu (mục 3.3). |
| `WSL: Ubuntu` không xuất hiện | Kiểm tra extension WSL, mở đúng distro thay vì `docker-desktop`, kiểm tra `wsl -l -v`. |
| `mvn`/`npm` trỏ về `/mnt/c/...` | Kiểm tra `type -a`, `~/.bashrc`, `appendWindowsPath=false`; ưu tiên công cụ Ubuntu. |
| `TortoiseGitMerge not found` | Xem đường dẫn TortoiseGitMerge.exe; nếu không mặc định, đặt `TORTOISE_GIT_MERGE_EXE` sang đường dẫn đúng. |
| TortoiseGitMerge không mở từ Ubuntu | Kiểm tra `enabled=true`; test gọi `.exe` trực tiếp bằng đường dẫn đầy đủ; kiểm tra chính sách Windows/antivirus. |
| GUI không mở được file | Kiểm tra `wslpath -aw <file>` và quyền truy cập `\\wsl.localhost\Ubuntu\...` từ Windows Explorer. |
| Git nói resolved nhưng file vẫn sai | Review `git diff --cached`; xem conflict markers, chạy test; không dựa duy nhất vào GUI. |
| File `.orig` xuất hiện | Git mergetool backup. Review xong mới xóa hoặc cấu hình `mergetool.keepBackup=false`. |
| Conflict kiểu delete/modify, rename, binary, submodule | Xử lý Git index và file bằng Git/VS Code; wrapper này ưu tiên conflict **text** có đủ file. |
| GUI không chờ đóng / file bị khóa | Kiểm tra ứng dụng TortoiseGitMerge trên máy; không đánh dấu resolved nếu tiến trình GUI chưa kết thúc; cân nhắc VS Code Merge Editor. |

## 9. Checklist nghiệm thu

- [ ] Source code và `.git` nằm trong `/home/vinhnt/workspace/...`.
- [ ] VS Code hiển thị **WSL: Ubuntu**.
- [ ] `command -v git` trả về Git trong Ubuntu.
- [ ] Java, Maven, Node/npm và Docker CLI hoạt động trong terminal VS Code WSL.
- [ ] `appendWindowsPath=false` (nếu lựa chọn cách cô lập PATH).
- [ ] `~/.local/bin/tgit-merge-wsl` tồn tại, thực thi được và `bash -n` không lỗi.
- [ ] Git Ubuntu đã đặt `merge.tool=tgit-wsl`.
- [ ] Đã thử **một repository test** có conflict thực tế: mở GUI → lưu → Git nhận file → review diff.
- [ ] Đã xác minh GUI không đóng sớm khi merge chưa được lưu.
- [ ] Build/test project sau conflict thành công.

## 10. Tài liệu chính thức

- [VS Code — Developing in WSL](https://code.visualstudio.com/docs/remote/wsl)
- [VS Code — Remote Development Troubleshooting](https://code.visualstudio.com/docs/remote/troubleshooting)
- [Microsoft — Set up a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
- [Microsoft — Advanced WSL configuration (`wsl.conf`)](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)
- [Microsoft — WSL interoperability](https://learn.microsoft.com/en-us/windows/wsl/interop)
- [Git — git-mergetool](https://git-scm.com/docs/git-mergetool)
- [TortoiseGitMerge — Command Line Switches](https://tortoisegit.org/docs/tortoisegitmerge/tme-automation.html)

---