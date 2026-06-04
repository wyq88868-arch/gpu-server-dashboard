# 🚀 GPU Server Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Remote-Linux-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GPU-NVIDIA-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-SSH%20%2B%20Python3-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
  <b>A lightweight desktop dashboard for monitoring GPU server resources over SSH.</b>
</p>

<p align="center">
  <b>一个基于 SSH 的轻量级 GPU 服务器资源监控桌面面板。</b>
</p>

---

## 🌐 Language / 语言

* [中文说明](#-中文说明)
* [English Documentation](#-english-documentation)

---

# 🇨🇳 中文说明

## 📌 项目简介

**GPU Server Dashboard** 是一个 Windows 桌面端 GPU 服务器资源监控工具。

它通过 **SSH 持久连接** 到远程 Linux 服务器，并实时展示：

* 系统内存；
* CPU 负载；
* NVIDIA GPU 利用率；
* 显存占用；
* GPU 温度；
* GPU 功耗；
* GPU 上正在运行的进程；
* CPU 占用较高的进程。

它适合经常需要查看 `nvidia-smi`、管理训练任务、监控多卡服务器资源的用户。

---

## ✨ 特性

* 🖥️ **桌面窗口界面**：不需要打开浏览器；
* 🔗 **SSH 持久连接**：不是每次刷新都重新登录；
* 🎮 **多 GPU 支持**：每张 GPU 独立显示；
* 📊 **实时资源监控**：显存、温度、功耗、利用率；
* 🧾 **进程级信息**：查看每张 GPU 上运行的任务；
* ⚙️ **CPU 进程表**：显示 CPU 占用较高的进程；
* 🚫 **无 CMD 黑窗口**：exe 版本可无控制台运行；
* 🧹 **端口清理脚本**：异常退出时可手动释放本地端口。

---

## 🧩 工作方式

```text
Windows Desktop App
        │
        │  persistent SSH connection
        ▼
Linux GPU Server
        │
        │  remote python3 collector
        ▼
Local Dashboard Window
        │
        │  incremental UI refresh
        ▼
CPU / Memory / GPU / Process Info
```

软件点击“连接”后，会创建一个 SSH 连接，并在远程服务器上运行一个轻量级 `python3` 采集脚本。
之后资源数据会通过同一个 SSH 通道持续返回本地界面。

---

## ✅ 环境要求

### 本地 Windows

需要：

* Windows 10 / Windows 11；
* Python 3；
* OpenSSH Client；
* `pywebview`；
* 如果要打包 exe，需要 `pyinstaller`。

### 远程 Linux 服务器

需要：

* Linux；
* Python 3；
* NVIDIA 驱动；
* `nvidia-smi`；
* SSH 可连接。

---

## 🚀 快速使用

### 1. 克隆项目

```bash
git clone https://github.com/wyq88868-arch/gpu-server-dashboard.git
cd gpu-server-dashboard
```

### 2. 检查 Python 3

Windows 下双击：

```text
check_python3.bat
```

或在 CMD / PowerShell 中运行：

```cmd
py -3 --version
```

如果能看到 Python 3 版本，说明环境正常。

---

### 3. 安装依赖

双击：

```text
install_dependencies_py3_only.bat
```

如果网络较慢，可以使用：

```text
install_dependencies_tuna_mirror_py3_only.bat
```

手动安装方式：

```cmd
py -3 -m pip install pywebview
```

---

### 4. 启动桌面版

双击：

```text
run_desktop_app_v23.bat
```

在软件中填写 SSH 主机，例如：

```text
your-server
```

或者：

```text
user@192.168.1.100
```

默认端口：

```text
22
```

默认刷新间隔：

```text
0.6
```

然后点击 **连接**。

---

## 📦 打包成无黑框 exe

如果你希望生成真正的 `.exe` 文件，并且不显示 CMD 黑窗口，可以使用 V2.4 打包脚本。

双击：

```text
build_exe_no_console_v24.bat
```

生成结果在：

```text
dist/GPU-Server-Dashboard.exe
```

如果打包失败，请查看：

```text
build_log.txt
```

如果 exe 运行异常，可以构建调试版：

```text
build_exe_debug_console_v24.bat
```

---

# 🔐 SSH 密钥配置教程：新手版

如果你已经可以直接运行：

```cmd
ssh your-server
```

并成功登录服务器，可以跳过本节。

如果你还没有配置 SSH 密钥，可以按下面步骤操作。

---

## 1. 什么是 SSH 密钥？

SSH 密钥是一对文件：

```text
私钥：放在你自己的电脑上，绝对不能发给别人
公钥：放到服务器上，用来识别你的电脑
```

常见文件名：

```text
id_ed25519        私钥
id_ed25519.pub    公钥
```

⚠️ 注意：

```text
不要把 id_ed25519、id_rsa、*.pem、*.key 上传到 GitHub。
```

---

## 2. 在 Windows 上生成密钥

打开 CMD 或 PowerShell，运行：

```cmd
ssh-keygen -t ed25519 -C "your_email@example.com"
```

一路回车即可。

如果你的系统不支持 `ed25519`，可以用：

```cmd
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

默认会生成在：

```text
C:\Users\你的用户名\.ssh\
```

---

## 3. 查看公钥

运行：

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

如果你生成的是 RSA：

```cmd
type %USERPROFILE%\.ssh\id_rsa.pub
```

复制输出的整行内容，例如：

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

---

## 4. 把公钥放到服务器

先用密码登录服务器：

```cmd
ssh user@server_ip
```

在服务器上执行：

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

你可以给服务器设置一个短名字，例如 `your-server`。

编辑或新建：

```text
C:\Users\你的用户名\.ssh\config
```

写入：

```sshconfig
Host your-server
    HostName 192.168.1.100
    User yourname
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

然后测试：

```cmd
ssh your-server
```

如果能登录，那么软件里也可以直接填：

```text
your-server
```

---

## 🧪 测试服务器环境

测试远程 Python 3：

```cmd
ssh your-server python3 --version
```

测试 NVIDIA GPU：

```cmd
ssh your-server nvidia-smi
```

如果这两个命令都正常，Dashboard 一般就可以正常显示服务器资源。

---

## 🧹 清理本地端口

软件默认使用本地端口：

```text
8766
```

正常关闭软件窗口后，端口会自动释放。

如果异常退出，可以运行：

```text
close_dashboard_ports.bat
```

它会尝试清理旧的本地 Dashboard 服务端口。

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

## 🔒 隐私与安全

本项目不会内置：

* SSH 密码；
* SSH 私钥；
* 服务器实时数据；
* 训练日志；
* API Token；
* GitHub Token。

请不要上传以下文件：

```text
dashboard_config.json
dashboard_runtime.log
run_log*.txt
install_log*.txt
build_log.txt
*.pem
*.key
id_rsa
id_ed25519
.ssh/
```

建议在 `.gitignore` 中忽略这些文件。

---

## ❓ 常见问题

### 1. CPU 为什么会显示 600%？

Linux 的 `ps` 命令以单个 CPU 核心为 100%。
如果一个进程使用了 6 个核心，就可能显示：

```text
600%
```

所以项目中同时显示：

```text
Core %：原始 CPU 占用
Total %：按服务器总核心数归一化后的整机占比
```

---

### 2. 软件会一直创建 SSH 连接吗？

不会。

它使用一个持久 SSH 连接：

```text
点击连接
→ 创建一个 SSH 进程
→ 远程服务器运行 python3 采集循环
→ 数据持续返回本地界面
```

不是每 0.6 秒重新连接一次。

---

### 3. 为什么没有显示 GPU？

先测试：

```cmd
ssh your-server nvidia-smi
```

如果这个命令无法显示 GPU，软件也无法显示 GPU 信息。

---

### 4. 服务器必须安装 Python 3 吗？

是的。远程服务器需要 `python3`。

测试：

```cmd
ssh your-server python3 --version
```

---

### 5. 关闭软件后端口还会占用吗？

正常不会。关闭软件窗口后，本地服务和 SSH 子进程会退出。

如果异常残留，可以运行：

```text
close_dashboard_ports.bat
```

---

## 🛠️ Roadmap

* [ ] 多服务器管理；
* [ ] 暗色模式；
* [ ] 资源历史曲线；
* [ ] GPU 空闲提醒；
* [ ] 进程搜索；
* [ ] 进程命令复制；
* [ ] Linux/macOS 客户端。

---

## 📜 License

This project is licensed under the MIT License.

---

# 🇺🇸 English Documentation

## 📌 Introduction

**GPU Server Dashboard** is a lightweight Windows desktop application for monitoring Linux GPU servers over SSH.

It displays real-time information including:

* system memory;
* CPU load;
* NVIDIA GPU utilization;
* GPU memory usage;
* GPU temperature;
* GPU power draw;
* running GPU processes;
* top CPU processes.

It is designed for users who frequently check `nvidia-smi` and manage GPU training tasks.

---

## ✨ Features

* 🖥️ **Desktop window UI**: no browser required;
* 🔗 **Persistent SSH connection**: no repeated login on every refresh;
* 🎮 **Multi-GPU support**;
* 📊 **Real-time GPU monitoring**;
* 🧾 **Per-GPU process display**;
* ⚙️ **CPU process table**;
* 🚫 **No console window in exe build**;
* 🧹 **Port cleanup script**.

---

## 🧩 How It Works

```text
Windows Desktop App
        │
        │  persistent SSH connection
        ▼
Linux GPU Server
        │
        │  remote python3 collector
        ▼
Local Dashboard Window
        │
        │  incremental UI refresh
        ▼
CPU / Memory / GPU / Process Info
```

When you click **Connect**, the app opens one SSH connection and starts a lightweight remote Python3 collector.
Resource data is streamed back through the same SSH channel.

---

## ✅ Requirements

### Local Windows Machine

* Windows 10 / Windows 11;
* Python 3;
* OpenSSH Client;
* `pywebview`;
* `pyinstaller` if you want to build an exe.

### Remote Linux Server

* Linux;
* Python 3;
* NVIDIA driver;
* `nvidia-smi`;
* SSH access.

---

## 🚀 Quick Start

### 1. Clone

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

---

### 3. Install Dependencies

Double-click:

```text
install_dependencies_py3_only.bat
```

Or install manually:

```cmd
py -3 -m pip install pywebview
```

---

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

Then click **Connect**.

---

## 📦 Build No-Console exe

To build a no-console Windows exe, run:

```text
build_exe_no_console_v24.bat
```

The generated executable will be:

```text
dist/GPU-Server-Dashboard.exe
```

If the build fails, check:

```text
build_log.txt
```

For debugging:

```text
build_exe_debug_console_v24.bat
```

---

# 🔐 SSH Key Setup for Beginners

If you can already run:

```cmd
ssh your-server
```

successfully, you can skip this section.

---

## 1. What Is an SSH Key?

An SSH key pair includes:

```text
private key: stored on your local computer, never share it
public key: copied to the remote server
```

Common files:

```text
id_ed25519        private key
id_ed25519.pub    public key
```

Do not upload private keys to GitHub.

---

## 2. Generate an SSH Key on Windows

Open CMD or PowerShell:

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

---

## 3. View Your Public Key

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

For RSA:

```cmd
type %USERPROFILE%\.ssh\id_rsa.pub
```

Copy the full output line.

---

## 4. Add the Public Key to the Server

Log in with password first:

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

## 6. Configure an SSH Alias

Edit or create:

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

Test it:

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

## 🧹 Close Local Port

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
dashboard_runtime.log
run_log*.txt
install_log*.txt
build_log.txt
*.pem
*.key
id_rsa
id_ed25519
.ssh/
```

---

## ❓ FAQ

### Why can CPU usage exceed 100%?

Linux reports CPU usage per CPU core.
A multi-threaded process can use multiple cores, so it may show:

```text
600%
```

This means the process is using about 6 CPU cores.

---

### Does the app create SSH connections repeatedly?

No.

It uses one persistent SSH connection and keeps a remote Python3 collector running.

---

### Why are GPUs not displayed?

Run:

```cmd
ssh your-server nvidia-smi
```

If this command does not show GPU information, the dashboard cannot show it either.

---

### Does the remote server need Python 3?

Yes.

Test it with:

```cmd
ssh your-server python3 --version
```

---

## 🛠️ Roadmap

* [ ] Multi-server management;
* [ ] Dark mode;
* [ ] History charts;
* [ ] GPU idle notification;
* [ ] Process search;
* [ ] Copy process command;
* [ ] Linux/macOS clients.

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Star

If this project helps you, feel free to give it a star.
