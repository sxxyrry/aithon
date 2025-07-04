import importlib.util
import sys
from . import Runner as RunnerType

# 定义模块名
module_name = 'Runner'
# 构建 .pyc 文件的路径
spec = importlib.util.spec_from_file_location(module_name, './codes/Runner.cpython-313.pyc')
# 根据模块规范创建模块对象
Runner_module = importlib.util.module_from_spec(spec) # type: ignore # type: ignore
# 将模块添加到 sys.modules 中，方便后续引用
sys.modules[module_name] = Runner_module
# 执行模块的加载操作
spec.loader.exec_module(Runner_module) # type: ignore

Runner: RunnerType = Runner_module # type: ignore