chcp 65001

@echo off

:: 检查 Python 装了没
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python 3 未安装，请安装后继续操作。
    exit /b 1
)

:: 检查 pip 装了没
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: pip 未安装，请安装后继续操作。
    exit /b 1
)

:: 检查虚拟环境
if not exist "venv" (
    echo 虚拟环境未创建，正在创建...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

:: 安装依赖
if exist "requirements.txt" (
    echo 根据项目依赖描述文件安装依赖包...
    pip install -r requirements.txt
) else (
    echo 依赖描述文件读取有误，请检查项目是否完整。
)

:: 激活虚拟环境
echo ==========
echo.
echo 输入 call .venv\Scripts\activate.bat 来激活虚拟环境；deactivate 退出虚拟环境。
echo.
echo ==========

echo.
echo 初始化完成 √

pause