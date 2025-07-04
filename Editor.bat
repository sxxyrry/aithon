@echo off
setlocal enabledelayedexpansion

:: 获取脚本所在目录并切换到该目录
set "scriptDir=%~dp0"
pushd "%scriptDir%"

:: 参数检查
if "%~1"=="" (
    echo 错误: 未指定 Python 解释器路径
    exit /b 1
)
if "%~2"=="" (
    echo 错误: 未指定 Aithon 文件路径
    exit /b 1
)

:: 验证文件路径
if not exist "%~1" (
    echo 错误: Python 解释器路径不存在: %~1
    exit /b 1
)

if not exist "%~2" (
    echo 错误: Aithon 文件路径不存在: %~2
    exit /b 1
)

:: 检查文件扩展名
set "aitFile=%~2"
if not "!aitFile:~-4!"==".ait" (
    echo 错误: 文件扩展名不是 .ait: %~2
    exit /b 1
)

:: 运行 Python 脚本
"%~1" Editor.py "%~2"
if errorlevel 1 (
    echo 错误: 执行失败
    exit /b 1
)

:: 恢复原始目录
popd