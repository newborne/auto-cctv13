# CCTV13 自动播放监控脚本

<div align="center">

![版本](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.35%2B-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**24 小时无人值守 · CCTV13 自动播放监控**

[中文](README.md) | [English](README_EN.md)

</div>

---

## 📖 目录

- [项目介绍](#项目介绍)
- [功能特点](#功能特点)
- [效果展示](#效果展示)
- [系统要求](#系统要求)
- [安装教程](#安装教程)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [技术架构](#技术架构)
- [已知问题](#已知问题)
- [更新日志](#更新日志)
- [许可证](#许可证)

---

## 🎯 项目介绍

这是一个基于 **Playwright** 的 **CCTV13 自动播放监控脚本**，能够实现：

- ✅ **自动启动浏览器**并打开 CCTV13 直播
- ✅ **自动全屏显示**（视频/浏览器级别）
- ✅ **24 小时持续监控**，每 30 秒检测播放状态
- ✅ **自动恢复播放**（暂停自动恢复）
- ✅ **定期刷新页面**（每 10 分钟，防止卡死）
- ✅ **无人值守运行**，全程自动化

适用于：
- 🏠 家庭背景音播放
- 🏫 学校/办公室监控
- 📺 直播间辅助工具
- 🔧 自动化测试场景

---

## ✨ 功能特点

| 功能 | 说明 |
|-----|-|--
| 🖥️ **自动启动** | 自动打开浏览器并加载 CCTV13 |
| 🎬 **自动全屏** | 使用 JS/F11 双重保障全屏 |
| ⏱️ **实时检测** | 每 30 秒检测全屏 + 播放状态 |
| 🔄 **自动恢复** | 暂停自动恢复播放 |
| ♻️ **定期刷新** | 每 10 分钟自动刷新（防止卡死） |
| 📊 **详细日志** | 记录所有操作和状态变化 |
| 🛠️ **异常处理** | 自动处理异常情况 |
| ⚡ **一键启动** | 单文件运行，开箱即用 |

---

## 🎬 效果展示

### 启动后效果

```
==================================================
CCTV13 自动播放监控脚本 - 强制全屏版
核心改进：
  ✅ 不依赖 F11 快捷键
  ✅ 直接使用 JS requestFullscreen
  ✅ 多方法尝试：video/container/body/document
  ✅ 每 10 分钟自动刷新 + 全屏
  ✅ 每 30 秒检测全屏 + 播放状态
功能：
  - 自动启动浏览器并最大化窗口
  - 自动加载 CCTV13 直播
  - 强制 JS 全屏（多种方法）
  - 每 600 秒自动刷新并全屏
  - 暂停自动恢复播放
  - 24 小时持续监控
提示：
  - 放弃 F11，使用 JS 强制全屏
  - 如果全屏无效，可能是播放器拦截
  - 按 Ctrl+C 停止程序
==================================================

2026-03-17 00:20:00 [INFO] 正在启动浏览器...
2026-03-17 00:20:02 [INFO] 设置视口尺寸：1920x1080
2026-03-17 00:20:06 [INFO] ✅ 浏览器已启动
2026-03-17 00:20:10 [INFO] ✅ CCTV13 页面加载完成
2026-03-17 00:20:10 [INFO] ✅ 已强制全屏
```

### 监控日志示例

```
2026-03-17 00:20:40 [INFO] 状态检查：全屏=是，播放=是
2026-03-17 00:20:40 [INFO] [检查 #1] ✅ 视频全屏播放中
2026-03-17 00:21:10 [INFO] [检查 #2] ✅ 视频全屏播放中

# 检测到暂停
2026-03-17 00:25:30 [WARNING] ⚠️ 视频已暂停，正在恢复...
2026-03-17 00:25:32 [INFO] ✅ 已通过 JS 恢复播放

# 每 10 分钟自动刷新
2026-03-17 00:35:00 [WARNING] ⚠️ 准备刷新页面...
2026-03-17 00:35:08 [INFO] ✅ 页面已刷新并全屏
```

---

## 💻 系统要求

| 配置 | 要求 | 推荐 |
|-----|-|-|--|
| **系统** | Windows 10/11 | Windows 11 |
| **Python** | 3.8+ | 3.10+ |
| **内存** | 4GB+ | 8GB+ |
| **屏幕** | 1920x1080 | 1920x1080+ |
| **网络** | 稳定宽带 | 10Mbps+ |

---

## 📦 安装教程

### 方法一：一键安装（推荐）

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/cctv-autoplay.git
   cd cctv-autoplay
   ```

2. **运行安装脚本**
   ```bash
   # Windows
   install.bat
   
   # macOS/Linux
   chmod +x install.sh
   ./install.sh
   ```

3. **验证安装**
   ```bash
   # 检查 Python
   python --version
   
   # 检查 Playwright
   playwright --version
   
   # 检查浏览器
   playwright show-installed-browsers
   ```

### 方法二：手动安装

#### 1. 安装 Python

- 访问：https://www.python.org/downloads/
- 下载 Python 3.8+ 版本
- **务必勾选** `Add Python to PATH`
- 重启终端

#### 2. 安装依赖

```bash
# 安装 playwright
pip install playwright

# 安装 Chromium 浏览器
playwright install chromium

# 安装系统依赖（需要管理员权限）
playwright install-deps chromium
```

#### 3. 验证安装

```bash
# 检查 Python
python --version

# 检查 playwright
playwright --version

# 检查浏览器
playwright show-installed-browsers
```

---

## 🚀 使用指南

### 基础使用

```bash
# 直接运行脚本
python cctv13_auto_play.py
```

### 自定义配置

编辑 `cctv13_auto_play.py` 文件顶部参数：

```python
# 检测间隔（秒）
CHECK_INTERVAL = 30  # 默认 30 秒检测一次

# 刷新间隔（秒）
REFRESH_INTERVAL = 600  # 默认 600 秒（10 分钟）刷新一次

# CCTV13 直播地址
CCTV13_URL = "https://tv.cctv.com/live/cctv13/"  # 默认 CCTV13
```

### 后台运行（Linux/macOS）

```bash
# 使用 nohup 后台运行
nohup python cctv13_auto_play.py > cctv13.log 2>&1 &

# 停止后台运行
pkill -f cctv13_auto_play.py
```

### Windows 任务计划（开机自启）

1. 创建 `start.bat`
   ```batch
   @echo off
   cd /d "%~dp0"
   python cctv13_auto_play.py
   ```

2. 打开"任务计划程序"
3. 创建任务 → 触发器："登录时"
4. 操作："启动程序" → 选择 `start.bat`

---

## ⚙️ 配置说明

### 核心参数

| 参数 | 默认值 | 说明 |
|-----|--------|-|--
| `CHECK_INTERVAL` | 30 秒 | 检测播放状态的间隔 |
| `REFRESH_INTERVAL` | 600 秒 | 自动刷新页面的间隔 |
| `CCTV13_URL` | `tv.cctv.com` | CCTV13 直播地址 |

### 日志文件

```bash
# 日志文件位置
cctv13_auto_play.log

# 查看实时日志
# Windows
Get-Content cctv13_auto_play.log -Tail 50 -Wait

# Linux/macOS
tail -f cctv13_auto_play.log
```

---

## ❓ 常见问题

### Q1: 安装 Python 时需要注意什么？

**A**: 务必勾选 **"Add Python to PATH"**，否则无法使用命令行。

### Q2: `pip` 命令不存在？

**A**: 
```bash
# 使用 py 命令替代
py -m pip install playwright
py -m playwright install chromium
```

### Q3: 浏览器启动后闪退？

**A**: 
1. 检查杀毒软件/防火墙是否拦截
2. 使用管理员权限运行
3. 查看日志文件：`cctv13_auto_play.log`

### Q4: 全屏不生效？

**A**: 
- 脚本使用 4 种方法强制全屏
- 如果播放器拦截，请**手动双击视频全屏一次**
- 刷新后脚本会尝试重新全屏

### Q5: 视频一直暂停？

**A**: 
- 脚本会自动检测并恢复播放
- 检查网络连接是否稳定
- 检查 CCTV13 服务器是否正常

### Q6: 如何停止脚本？

**A**: 
- **控制台**：按 `Ctrl+C`
- **任务管理器**：结束 `python.exe` 进程
- **命令行**：
  ```bash
  # Windows
  taskkill /F /IM python.exe
  
  # macOS/Linux
  pkill -f cctv13_auto_play.py
  ```

### Q7: 首次运行很慢？

**A**: 
- 首次运行需下载 Chromium 浏览器（约 100MB）
- 需要 1-5 分钟，耐心等待

---

## 🏗️ 技术架构

### 技术栈

| 技术 | 版本 | 用途 |
|-----|-|-|
| Python | 3.8+ | 脚本语言 |
| Playwright | 1.35+ | 浏览器自动化 |
| Chromium | 内置 | 浏览器内核 |
| AsyncIO | 内置 | 异步处理 |

### 架构流程

```
┌─────────────────────────────────┐
│   启动脚本                      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  启动浏览器（无头模式）         │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  加载 CCTV13 页面                │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  强制全屏（4 种方法）           │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  定时监控循环（每 30 秒）        │
│  ├─ 检测全屏状态                │
│  ├─ 检测播放状态                │
│  └─ 自动恢复异常                │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  每 10 分钟刷新页面              │
│  └─ 重新全屏                    │
└─────────────────────────────────┘
```

### 核心模块

```python
class CCTV13AutoPlayer:
    def setup_browser()      # 启动浏览器
    def load_page()          # 加载页面
    def force_fullscreen()   # 强制全屏
    def check_fullscreen()   # 检查全屏
    def check_video_status() # 检查播放
    def click_play()         # 恢复播放
    def refresh()            # 刷新页面
    def monitor()            # 监控循环
```

---

## ⚠️ 已知问题

| 问题 | 说明 | 解决方案 |
|-----|-|--|
| 全屏可能不生效 | CCTV 播放器可能拦截 |
| 首次运行慢 | 需下载浏览器内核 | 耐心等待 |
| 杀毒软件拦截 | 浏览器启动可能被杀 |
| 视频卡顿 | 网络问题 | 检查网络 |
| 刷新后未全屏 | 播放器重置 | 手动 F11 |

---

## 📝 更新日志

### v1.0.0 (2026-03-17)

- ✅ 初始版本发布
- ✅ 基础功能：自动启动、全屏、监控
- ✅ 日志系统完善
- ✅ 异常处理优化

### 计划更新

- [ ] 支持多个频道切换
- [ ] 添加 Telegram/SMTP 通知
- [ ] 支持 Docker 部署
- [ ] 图形化管理界面

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可。

```
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 贡献指南

欢迎贡献代码！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📧 联系方式

- **Email**: newborne@foxmail.com
- **GitHub**: github.com/newborne
- **Issues**: 欢迎提交问题和建议

---

## 🙏 致谢

- [Playwright](https://playwright.dev/)
- [CCTV 官网](https://tv.cctv.com/)
- 所有贡献者

---

<div align="center">

**如果觉得这个项目对你有帮助，请给一个 ⭐ Star！**

[![Star](https://img.shields.io/github/stars/your-username/cctv-autoplay?style=social)](https://github.com/your-username/cctv-autoplay)

</div>

---

**© 2026 Your Name. All rights reserved.**
