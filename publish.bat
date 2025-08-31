@echo off
chcp 65001 >nul
echo === Loki SDK Python 发布工具 ===
echo.
echo 正在检查发布工具...
python install_tools.py
echo.
echo 启动发布脚本...
python publish.py
pause
