# 🚀 GPU Server Dashboard / GPU 服务器资源监控面板

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-SSH%20%2B%20Python3-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-Desktop%20Dashboard-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GPU-NVIDIA-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
  <b>A beautiful desktop-style GPU server resource dashboard over SSH.</b>
</p>

<p align="center">
  <b>一个基于 SSH 的高颜值 GPU 服务器资源监控桌面面板。</b>
</p>

---

## 🌐 Language / 语言

* [中文说明](#-中文说明)
* [English Documentation](#-english-documentation)

---

# 🇨🇳 中文说明

## 📌 项目简介

**GPU Server Dashboard** 是一个面向 Windows 用户的服务器资源监控工具。
它可以通过 **SSH 持久连接** 到 Linux GPU 服务器，并以一个美观的桌面窗口实时展示服务器资源状态。

它适合以下场景：

* 你有一台或多台 Linux GPU 服务器；
* 你经常需要查看显卡占用、显存、功耗、温度；
* 你不想每次都手动敲 `nvidia-smi`；
* 你想要一个比命令行更直观、更好看的资源面板；
* 你希望通过 Windows 桌面软件查看服务器运行状态。

---

## ✨ 功能特点

### 🧠 系统内存监控

* 显示内存总量；
* 显示已用内存；
* 显示可用内存；
* 显示缓存内存；
* 环形进度图展示内存占用比例。

### 🎮 GPU 资源监控

每张 GPU 单独显示一个卡片，包括：

* GPU 编号；
* GPU 型号；
* 显存占用；
* GPU 利用率；
* 温度；
* 当前功耗；
* 功率上限；
* 当前运行在该 GPU 上的进程。

### 🧾 GPU 进程监控

可以看到：

* PID；
* 用户名；
* 运行时间；
* 使用显存；
* 运行命令。

### ⚙️ CPU 进程监控

展示 CPU 占用较高的进程，并区分：

* `Core %`：Linux `ps` 原始 CPU 占用，多线程任务可能超过 100%；
* `Total %`：按服务器总 CPU 核心数归一化后的整机 CPU 占比。

例如：

```text
Core % = 640%
CPU cores = 128
Total % = 640 / 128 = 5.0%
```

这表示该进程大约使用了 6.4 个 CPU 核心，占整台服务器约 5%。

### 🔁 稳定刷新

* 使用单个 SSH 持久连接；
* 不是每次刷新都重新 SSH；
* 前端增量更新，减少滚动卡顿；
* 默认刷新间隔为 `0.6` 秒。

---

## 🖼️ 界面预览

你可以在这里放一张截图：

```markdown
![Dashboard Preview](docs/preview.png)
```

建议新建一个 `docs` 文件夹，把截图命名为：

```text
docs/preview.png
```

---

## 🧩 工作原理

```text
Windows 本地软件
        │
        │  1 个持久 SSH 连接
        ▼
Linux GPU 服务器
        │
        │  远程 python3 采集资源信息
        ▼
本地 Dashboard 窗口
        │
        │  每 0.6 秒刷新 UI
        ▼
实时显示 CPU / Memory / GPU / Processes
```

核心流程：

```text
点击连接
→ 本地启动 SSH
→ 服务器端运行 python3 资源采集脚本
→ 采集 nvidia-smi、内存、CPU、进程信息
→ 本地桌面窗口展示
```

---

## ✅ 环境要求

### 本地 Windows 电脑

需要：

* Windows 10 / Windows 11；
* Python 3；
* OpenSSH Client；
* `pywebview`。

### 远程 Linux 服务器

需要：

* Linux；
* Python 3；
* NVIDIA 驱动；
* `nvidia-smi`；
* 可以通过 SSH 连接。

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/wyq88868-arch/gpu-server-dashboard.git
cd gpu-server-dashboard
```

### 2. 检查本地 Python 3

Windows 下双击：

```text
check_python3.bat
```

或者在 CMD / PowerShell 中运行：

```cmd
py -3 --version
```

如果能看到类似：

```text
Python 3.12.x
```

说明 Python 3 正常。

### 3. 安装依赖

双击：

```text
install_dependencies_py3_only.bat
```

如果网络较慢，可以使用清华源版本：

```text
install_dependencies_tuna_mirror_py3_only.bat
```

手动安装方式：

```cmd
py -3 -m pip install pywebview
```

### 4. 启动软件

双击：

```text
run_desktop_app_v23.bat
```

然后在软件界面输入服务器地址，例如：

```text
your-server
```

或者：

```text
user@192.168.1.100
```

端口默认：

```text
22
```

刷新间隔默认：

```text
0.6
```

---

# 🔐 SSH 密钥配置教程：新手小白版

如果你以前没有配置过 SSH 密钥，可以按下面步骤来。

## 1. 什么是 SSH 密钥？

SSH 密钥可以理解为一把“电子钥匙”。

你本地电脑有一把：

```text
私钥 private key
```

服务器上保存一把：

```text
公钥 public key
```

当你连接服务器时，系统会自动验证这两把钥匙是否匹配。
这样你就可以不用每次输入密码。

---

## 2. 在 Windows 上生成 SSH 密钥

打开 PowerShell 或 CMD，运行：

```cmd
ssh-keygen -t ed25519 -C "your_email@example.com"
```

如果你的系统不支持 `ed25519`，可以用：

```cmd
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

一路回车即可。

默认会生成在：

```text
C:\Users\你的用户名\.ssh\
```

里面通常会有两个文件：

```text
id_ed25519        私钥，不要发给别人
id_ed25519.pub    公钥，可以放到服务器
```

⚠️ 注意：

```text
id_ed25519 是私钥，千万不要上传到 GitHub，也不要发给别人。
id_ed25519.pub 是公钥，可以放到服务器。
```

---

## 3. 查看你的公钥

运行：

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

如果你用的是 RSA：

```cmd
type %USERPROFILE%\.ssh\id_rsa.pub
```

复制输出的整行内容。

它看起来像这样：

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

---

## 4. 把公钥添加到服务器

先用密码登录服务器：

```cmd
ssh user@server_ip
```

然后在服务器上执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

把刚才复制的公钥粘贴进去，保存退出。

然后执行：

```bash
chmod 600 ~/.ssh/authorized_keys
```

---

## 5. 测试免密登录

回到 Windows，运行：

```cmd
ssh user@server_ip
```

如果可以直接登录，说明 SSH 密钥配置成功。

---

## 6. 配置 SSH 别名

你可以给服务器配置一个好记的名字。

编辑这个文件：

```text
C:\Users\你的用户名\.ssh\config
```

如果没有 `config` 文件，就新建一个。

写入：

```sshconfig
Host your-server
    HostName 192.168.1.100
    User yourname
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

之后你就可以直接运行：

```cmd
ssh your-server
```

如果能连上，那么软件里也可以直接填：

```text
your-server
```

---

## 🧪 测试服务器环境

运行：

```text
test_remote_server_python3.bat
```

或者手动测试：

```cmd
ssh your-server python3 --version
```

测试 GPU：

```cmd
ssh your-server nvidia-smi
```

如果都正常，Dashboard 就可以正常读取服务器资源。

---

## 🧹 关闭本地端口

本软件默认使用本地端口：

```text
8766
```

正常关闭软件窗口后，端口会自动释放。

如果你想手动清理旧端口，可以运行：

```text
close_dashboard_ports.bat
```

它会清理：

```text
8765
8766
```

---

## 📂 项目结构

```text
gpu-server-dashboard/
├── beautiful_server_dashboard_desktop_v23.py
├── run_desktop_app_v23.bat
├── close_dashboard_ports.bat
├── check_python3.bat
├── install_dependencies_py3_only.bat
├── install_dependencies_tuna_mirror_py3_only.bat
├── test_remote_server_python3.bat
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔒 隐私与安全说明

本项目不会内置：

* SSH 密码；
* SSH 私钥；
* 服务器实时数据；
* 训练日志；
* API token；
* GitHub token。

本项目通过你本地系统已有的 SSH 配置进行连接。

请不要上传以下文件：

```text
dashboard_config.json
run_log*.txt
install_log*.txt
*.pem
*.key
id_rsa
id_ed25519
.ssh/
```

`.gitignore` 中已经默认忽略这些文件。

---

## ❓ 常见问题

### Q1：为什么 CPU 会显示 600%？

这是 Linux 的正常行为。

`ps` 命令中的 CPU 百分比是按“单个 CPU 核心”为 100% 计算的。
如果一个多线程程序用了 6 个核心，就可能显示：

```text
600%
```

所以本项目额外显示了 `Total %`，表示它占整台服务器的比例。

---

### Q2：这个软件会不会一直创建 SSH？

不会。

它使用的是单个持久 SSH 连接：

```text
点击连接
→ 创建一个 SSH 进程
→ 服务器端启动 python3 采集循环
→ 持续返回数据
```

不是每 0.6 秒重新连接一次。

---

### Q3：关闭软件后端口会释放吗？

正常情况下会自动释放。

如果异常退出，可以运行：

```text
close_dashboard_ports.bat
```

---

### Q4：为什么看不到 GPU？

请先在本地测试：

```cmd
ssh your-server nvidia-smi
```

如果这个命令没有输出 GPU 信息，Dashboard 也无法显示 GPU。

---

### Q5：服务器必须安装 Python 3 吗？

是的。远程服务器需要有 `python3`。

测试：

```cmd
ssh your-server python3 --version
```

---

## 🛠️ TODO

* [ ] 支持多服务器切换；
* [ ] 支持暗色模式；
* [ ] 支持历史曲线；
* [ ] 支持 GPU 空闲提醒；
* [ ] 支持进程一键复制；
* [ ] 支持 Linux/macOS 客户端。

---

## 📜 License

This project is released under the MIT License.

---

# 🇺🇸 English Documentation

## 📌 Introduction

**GPU Server Dashboard** is a beautiful desktop-style resource monitor for Linux GPU servers.
It connects to a remote server through a **persistent SSH connection** and displays real-time system and GPU information in a modern desktop dashboard.

It is designed for users who:

* manage Linux GPU servers;
* frequently check `nvidia-smi`;
* want a better visual dashboard than command-line tools;
* use Windows as their local machine;
* need a lightweight SSH-based monitoring tool.

---

## ✨ Features

### 🧠 System Memory Monitoring

* Total memory;
* Used memory;
* Available memory;
* Cache memory;
* Circular memory usage indicator.

### 🎮 GPU Monitoring

Each GPU is displayed as an independent card with:

* GPU index;
* GPU name;
* VRAM usage;
* GPU utilization;
* temperature;
* power draw;
* power limit;
* running processes.

### 🧾 GPU Process Monitoring

For each GPU process, the dashboard shows:

* PID;
* user;
* elapsed time;
* used GPU memory;
* command.

### ⚙️ CPU Process Monitoring

The dashboard shows top CPU processes with:

* `Core %`: raw Linux `ps` CPU percentage;
* `Total %`: normalized CPU usage based on total CPU cores.

Example:

```text
Core % = 640%
CPU cores = 128
Total % = 640 / 128 = 5.0%
```

This means the process uses about 6.4 CPU cores, or about 5% of the whole machine.

---

## 🖼️ Preview

You can add a screenshot here:

```markdown
![Dashboard Preview](docs/preview.png)
```

---

## 🧩 How It Works

```text
Windows desktop app
        │
        │  one persistent SSH connection
        ▼
Linux GPU server
        │
        │  remote Python3 resource collector
        ▼
Local dashboard window
        │
        │  UI refresh every 0.6 seconds
        ▼
CPU / Memory / GPU / Process monitoring
```

---

## ✅ Requirements

### Local Windows Machine

* Windows 10 / Windows 11;
* Python 3;
* OpenSSH Client;
* `pywebview`.

### Remote Linux Server

* Linux;
* Python 3;
* NVIDIA driver;
* `nvidia-smi`;
* SSH access.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/wyq88868-arch/gpu-server-dashboard.git
cd gpu-server-dashboard
```

### 2. Check Python 3

Double-click:

```text
check_python3.bat
```

Or run:

```cmd
py -3 --version
```

### 3. Install Dependencies

Double-click:

```text
install_dependencies_py3_only.bat
```

Or manually run:

```cmd
py -3 -m pip install pywebview
```

### 4. Start the App

Double-click:

```text
run_desktop_app_v23.bat
```

Enter your SSH host:

```text
your-server
```

or:

```text
user@192.168.1.100
```

Default port:

```text
22
```

Default refresh interval:

```text
0.6
```

---

# 🔐 SSH Key Setup for Beginners

## 1. What Is an SSH Key?

An SSH key is like a digital key pair:

```text
private key: stays on your local machine
public key: placed on the remote server
```

The private key must never be shared.

---

## 2. Generate an SSH Key on Windows

Open PowerShell or CMD:

```cmd
ssh-keygen -t ed25519 -C "your_email@example.com"
```

If `ed25519` is not supported:

```cmd
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Press Enter to use the default path.

The key files are usually stored in:

```text
C:\Users\YourName\.ssh\
```

You will see:

```text
id_ed25519        private key, never share this
id_ed25519.pub    public key, safe to copy to the server
```

---

## 3. Copy the Public Key

Run:

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

Copy the entire output line.

---

## 4. Add the Public Key to the Server

Log in to your server:

```cmd
ssh user@server_ip
```

On the server:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

Paste your public key into this file.

Then run:

```bash
chmod 600 ~/.ssh/authorized_keys
```

---

## 5. Test Passwordless Login

From Windows:

```cmd
ssh user@server_ip
```

If you can log in without typing a password, the SSH key is working.

---

## 6. Configure SSH Alias

Edit:

```text
C:\Users\YourName\.ssh\config
```

Example:

```sshconfig
Host your-server
    HostName 192.168.1.100
    User yourname
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Then test:

```cmd
ssh your-server
```

If it works, you can enter:

```text
your-server
```

in the dashboard.

---

## 🧪 Test Remote Environment

Test remote Python 3:

```cmd
ssh your-server python3 --version
```

Test NVIDIA GPU:

```cmd
ssh your-server nvidia-smi
```

---

## 🧹 Close Local Ports

The app uses local port:

```text
8766
```

Normally, it is released automatically when the app exits.

If needed, run:

```text
close_dashboard_ports.bat
```

---

## 🔒 Privacy and Security

This project does not include:

* SSH passwords;
* SSH private keys;
* server runtime data;
* training logs;
* API tokens;
* GitHub tokens.

Do not upload:

```text
dashboard_config.json
run_log*.txt
install_log*.txt
*.pem
*.key
id_rsa
id_ed25519
.ssh/
```

---

## ❓ FAQ

### Why can CPU usage exceed 100%?

Linux reports CPU usage per core.
A multi-threaded process can use multiple cores, so it can show values like:

```text
600%
```

This means about 6 CPU cores are being used.

---

### Does this app create SSH connections repeatedly?

No.

It uses one persistent SSH connection and keeps a remote Python3 collector running.

---

### Why are GPUs not displayed?

Run:

```cmd
ssh your-server nvidia-smi
```

If this command does not show GPU information, the dashboard cannot display GPU information either.

---

### Does the remote server need Python 3?

Yes.

Test it with:

```cmd
ssh your-server python3 --version
```

---

## 🛠️ Roadmap

* [ ] Multi-server support;
* [ ] Dark mode;
* [ ] History charts;
* [ ] GPU idle notification;
* [ ] Process copy button;
* [ ] Linux/macOS desktop client.

---

## 📜 License

MIT License.

---

## ⭐ Star

If this project helps you, feel free to give it a star!

如果这个项目对你有帮助，欢迎点一个 Star！
