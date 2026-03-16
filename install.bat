@echo off
REM CCTV13 自动播放脚本 - 一键安装

echo ========================
echo CCTV13 自动播放脚本
echo 一键安装脚本
echo ========================
echo.

REM 检查 Python
python --version >nul 2<&1
if {%errorlevel%} neq 0 (
    echo ❌ 错误：未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    echo.
    echo 注意：安装时务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 安装依赖
echo 正在安装 playwright...
py -m pip install playwright

echo.
echo 正在下载 Chromium 浏览器（约 100MB，可能需要几分钟）...
py -m playwright install chromium

echo.
echo 正在安装系统依赖...
py -m playwright install-deps chromium

echo.
echo ========================
echo ✅ 安装完成！
echo.
echo 运行脚本：python cctv13_auto_play.py
echo 停止脚本：Ctrl+C
echo.
echo 注意事项：
echo 1. 首次运行需下载浏览器（约 1-5 分钟）
echo 2. 如遇问题查看日志文件：cctv13_auto_play.log
echo 3. 杀毒软件可能拦截，请添加例外
echo ========================
echo.
pause
