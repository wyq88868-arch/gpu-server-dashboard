# GPU Server Dashboard V3

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Remote-Linux-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GPU-NVIDIA-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-SSH%20%2B%20Python3-purple?style=for-the-badge" />
</p>

<p align="center">
  <b>A lightweight Windows desktop dashboard for monitoring Linux GPU servers over SSH.</b>
</p>

<p align="center">
  <b>一个基于 SSH 的 Windows 桌面端 GPU 服务器资源监控面板。</b>
</p>

---

## 中文说明

### 项目简介

**GPU Server Dashboard V3** 是一个用于监控远程 Linux GPU 服务器的 Windows 桌面工具。

它通过 SSH 连接远程服务器，并实时展示：

- 系统内存；
- CPU 负载；
- NVIDIA GPU 利用率；
- 显存占用；
- GPU 温度；
- GPU 功耗；
- GPU 上正在运行的进程；
- CPU 占用较高的进程。

V3 基于前一版本继续整理，当前主程序为：

```text
gpu_server_dashboard_v24.py
```

### 主要特性

- 桌面窗口界面，不需要打开浏览器；
- 通过 SSH 连接远程 Linux 服务器；
- 支持多 GPU 信息展示；
- 显示 GPU 利用率、显存、温度、功耗和进程；
- 显示 CPU 高占用进程；
- 支持从源码直接运行；
- 提供无控制台窗口 exe 打包脚本；
- 提供干净 Conda 环境打包脚本，避免 base 环境依赖污染。

### 环境要求

本地 Windows：

- Windows 10 / Windows 11；
- Python 3；
- OpenSSH Client；
- `pywebview`；
- 如果要打包 exe，需要 `pyinstaller`。

远程 Linux 服务器：

- Linux；
- Python 3；
- NVIDIA 驱动；
- `nvidia-smi`；
- SSH 可连接。

### 快速启动

克隆仓库后，切换到 `v3` 分支：

```bash
git clone https://github.com/wyq88868-arch/gpu-server-dashboard.git
cd gpu-server-dashboard
git checkout v3
```

在 Windows 中双击：

```text
run_from_source_v24.bat
```

该脚本会安装 `pywebview`，然后启动：

```text
gpu_server_dashboard_v24.py
```

### 手动运行

也可以在 PowerShell 或 CMD 中运行：

```cmd
py -3 -m pip install -r requirements.txt
py -3 gpu_server_dashboard_v24.py
```

如果系统没有 `py` 命令，可以改用：

```cmd
python -m pip install -r requirements.txt
python gpu_server_dashboard_v24.py
```

### 打包 exe

推荐使用干净 Conda 环境打包：

```text
build_exe_clean_conda_FIXED.bat
```

或使用普通无控制台窗口打包脚本：

```text
build_exe_no_console_v24.bat
```

生成结果通常位于：

```text
dist\GPU-Server-Dashboard.exe
```

如果需要调试控制台输出，可以运行：

```text
build_exe_debug_console_v24.bat
```

### SSH 使用说明

如果你已经能在 Windows 终端中运行：

```cmd
ssh user@server_ip
```

并成功登录服务器，那么软件中也可以填写相同的 SSH 主机信息。

也可以在 Windows 的 SSH config 中配置别名：

```sshconfig
Host your-server
    HostName 192.168.1.100
    User yourname
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

然后在软件中填写：

```text
your-server
```

### 安全说明

请不要把以下内容上传到 GitHub：

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

当前 `.gitignore` 已经排除了这些敏感或运行时文件。

### 项目结构

```text
gpu-server-dashboard/
├── gpu_server_dashboard_v24.py
├── run_from_source_v24.bat
├── build_exe_no_console_v24.bat
├── build_exe_debug_console_v24.bat
├── build_exe_clean_conda.bat
├── build_exe_clean_conda_FIXED.bat
├── build_manual_visible.bat
├── requirements.txt
├── app.ico
├── app_icon.png
├── README.md
└── .gitignore
```

### 贡献者

- wyq88868-arch
- Codex

---

## English Documentation

### Introduction

**GPU Server Dashboard V3** is a lightweight Windows desktop application for monitoring Linux GPU servers over SSH.

It displays real-time information including:

- system memory;
- CPU load;
- NVIDIA GPU utilization;
- GPU memory usage;
- GPU temperature;
- GPU power draw;
- running GPU processes;
- top CPU processes.

The main V3 application file is:

```text
gpu_server_dashboard_v24.py
```

### Features

- Desktop window UI, no browser required;
- SSH-based remote Linux server monitoring;
- Multi-GPU display;
- GPU utilization, memory, temperature, power, and process information;
- CPU process table;
- Source launch script;
- No-console exe build script;
- Clean Conda build script for avoiding polluted base environments.

### Requirements

Local Windows machine:

- Windows 10 / Windows 11;
- Python 3;
- OpenSSH Client;
- `pywebview`;
- `pyinstaller` for exe builds.

Remote Linux server:

- Linux;
- Python 3;
- NVIDIA driver;
- `nvidia-smi`;
- SSH access.

### Quick Start

```bash
git clone https://github.com/wyq88868-arch/gpu-server-dashboard.git
cd gpu-server-dashboard
git checkout v3
```

On Windows, double-click:

```text
run_from_source_v24.bat
```

Or run manually:

```cmd
py -3 -m pip install -r requirements.txt
py -3 gpu_server_dashboard_v24.py
```

### Build

Recommended clean Conda build:

```text
build_exe_clean_conda_FIXED.bat
```

No-console exe build:

```text
build_exe_no_console_v24.bat
```

Debug build:

```text
build_exe_debug_console_v24.bat
```

The generated executable is usually:

```text
dist\GPU-Server-Dashboard.exe
```

### Privacy and Security

This project should not include SSH passwords, private keys, runtime logs, server data, API tokens, or GitHub tokens.

### Contributors

- wyq88868-arch
- Codex
