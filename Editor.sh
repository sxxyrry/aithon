#!/bin/bash

# 参数检查
if [ $# -ne 2 ]; then
    echo "用法: $0 <python解释器路径> <aithon文件路径>"
    exit 1
fi

python_path="$1"
ait_file="$2"

# 获取脚本所在目录并切换到该目录
script_dir=$(dirname "$(readlink -f "$0")")
cd "$script_dir" || exit 1

# 验证文件路径
if [ ! -f "$python_path" ]; then
    echo "错误: Python 解释器路径不存在: $python_path" >&2
    exit 1
fi

if [ ! -f "$ait_file" ]; then
    echo "错误: Aithon 文件路径不存在: $ait_file" >&2
    exit 1
fi

# 检查文件扩展名
if [[ "$ait_file" != *.ait ]]; then
    echo "错误: 文件扩展名不是 .ait: $ait_file" >&2
    exit 1
fi

# 运行 Python 脚本
if ! "$python_path" ./Editor.py "$ait_file"; then
    echo "错误: 执行失败" >&2
    exit 1
fi