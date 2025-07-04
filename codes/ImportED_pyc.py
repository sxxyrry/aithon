import importlib.util
import sys

# 定义模块名
module_name = 'Encrypt_Decrypt'
# 构建 .pyc 文件的路径
spec = importlib.util.spec_from_file_location(module_name, './codes/Encrypt_Decrypt.cpython-313.pyc')
# 根据模块规范创建模块对象
Encrypt_Decrypt_module = importlib.util.module_from_spec(spec) # type: ignore # type: ignore
# 将模块添加到 sys.modules 中，方便后续引用
sys.modules[module_name] = Encrypt_Decrypt_module
# 执行模块的加载操作
spec.loader.exec_module(Encrypt_Decrypt_module) # type: ignore
