#!/bin/bash

# CCTV13 自动播放脚本 - 一键安装脚本（macOS/Linux）

echo "========================"
echo "CCTV13 自动播放脚本"
echo "一键安装脚本 (macOS/Linux)"
echo "========================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未检测到 Python3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

echo "✅ Python3 版本："
python3 --version
echo ""

# 安装 playwright
echo "正在安装 playwright..."
pip3 install playwright

# 安装浏览器
echo ""
echo "正在下载 Chromium 浏览器..."
playwright install chromium

# 安装系统依赖
echo ""
echo "正在安装系统依赖..."
playwright install-deps chromium

echo ""
echo "========================"
echo "✅ 安装完成！"
echo ""
echo "运行脚本：python3 cctv13_auto_play.py"
echo "停止脚本：Ctrl+C"
echo "========================"
