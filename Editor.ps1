# 定义参数
param(
    [Parameter(Mandatory=$true)]
    [string]$pythonPath,
    
    [Parameter(Mandatory=$true)]
    [string]$aitFilePath
)

# 获取脚本所在目录并切换到该目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir
try {
    # 验证文件路径是否存在
    if (-not (Test-Path $pythonPath)) {
        Write-Error "Python 解释器路径不存在: $pythonPath"
        exit 1
    }

    if (-not (Test-Path $aitFilePath)) {
        Write-Error "Aithon 文件路径不存在: $aitFilePath"
        exit 1
    }

    # 检查文件扩展名
    if (-not $aitFilePath.EndsWith('.ait')) {
        Write-Error "文件扩展名不是 .ait: $aitFilePath"
        exit 1
    }

    # 运行 Python 脚本
    try {
        & $pythonPath ./Editor.py $aitFilePath
    } catch {
        Write-Error "执行失败: $_"
        exit 1
    }
} finally {
    # 恢复原始工作目录
    Pop-Location
}