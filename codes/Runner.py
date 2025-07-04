from typing import Any, TypedDict

# 从其他模块导入的部分，这里仅做类型声明
from codes.config import Config

# 全局变量
config: Config = Config()
KernelName: str = ""
version: Any = ""

# 关键字、运算符、标点符号、错误表、内置函数和内置包列表
keys: list[str] = []
operators: list[str] = []
punctuation: list[str] = []
ErrorTable: list[str] = []
BuiltinsFunctoins: list[str] = []
BuiltinsPackages: list[str] = []

# 包文件夹路径和当前导入列表
PackagesFolderPath: str = ""
NowImport: list[str] = []

# 配置类型
class configType(TypedDict):
    """
    配置类型，包含发生错误时是否继续运行的配置项。
    """
    ContinueRunningAfterError: bool

class Raiser:
    """
    报错器，用于处理和输出错误信息。
    """
    def __init__(
        self,
        type_: str,
        message: str,
        line: int,
        text: str,
        path: str,
        pythonserror: Exception | None = None,
        config: configType = {'ContinueRunningAfterError': False}
    ) -> None:
        """
        :param type_: 报错类型
        :param message: 报错信息
        :param line: 报错行数
        :param text: 报错行文本
        :param path: 文件路径
        :param pythonserror: Python层面错误
        :param config: 一些配置（ContinueRunningAfterError是发生错误时是否继续运行，false为不继续运行，true为继续运行）
        """
        pass

def boolean(value: Any) -> bool: # type: ignore
    """
    将值转换为布尔值。

    :param value: 值
    :return: 布尔值
    """
    pass

class Environment:
    """
    环境实现，用于管理环境变量和导入的环境。
    """
    def __init__(self, name: str, values: dict[str, dict[str, dict]]) -> None: # type: ignore
        """
        :param name: 环境名称
        :param values: 环境值（字典）
        """
        pass

    def set_values(self, values: dict) -> None: # type: ignore
        """
        :param values: 要增加的环境值（字典）
        :return: None
        """
        pass

    def AddImportsEnvironment(self, name: str) -> None:
        """
        :param name: 要增加的导入的环境名称
        :return: None
        """
        pass

    def getImportsEnvironment(self) -> list[str]: # type: ignore
        """
        :return: 返回导入的环境名称列表
        """
        pass

    def __getitem__(self, item: Any) -> Any:
        pass

    def __str__(self) -> str: # type: ignore
        pass

# 环境字典
Environments: dict[str, Environment]
FunctionEnvironments: dict[str, Environment]

class Object:
    """
    基础对象类，实现了加法和乘法运算。
    """
    def __init__(self, value: object) -> None:
        pass

    def __add__(self, other: Any) -> 'Object': # type: ignore
        pass

    def __mul__(self, other: Any) -> 'Object': # type: ignore
        pass

    def __repr__(self) -> str: # type: ignore # type: ignore
        pass

class Str(Object):
    """
    字符串对象类，继承自Object类。
    """
    def __init__(self, value: object) -> None:
        pass

    def __add__(self, other: Any) -> 'Str': # type: ignore
        pass

    def __mul__(self, other: Any) -> 'Str': # type: ignore
        pass

    def __repr__(self) -> str: # type: ignore
        pass

class Int(Object):
    """
    整数对象类，继承自Object类。
    """
    def __init__(self, value: object, number: int, linetext: str, path: str | None) -> None:
        pass

    def __add__(self, other: Any) -> 'Int': # type: ignore
        pass

    def __mul__(self, other: Any) -> 'Int': # type: ignore
        pass

    def __repr__(self) -> str: # type: ignore
        pass

class Float(Object):
    """
    浮点数对象类，继承自Object类。
    """
    def __init__(self, value: object, number: int, linetext: str, path: str | None) -> None:
        pass

    def __add__(self, other: Any) -> 'Float': # type: ignore
        pass

    def __mul__(self, other: Any) -> 'Float': # type: ignore
        pass

    def __repr__(self) -> str: # type: ignore
        pass

class Nonetype(Object):
    """
    空类型对象类，继承自Object类。
    """
    def __init__(self, v: None) -> None:
        pass

    def __repr__(self) -> str: # type: ignore
        pass

def GetType(value: object) -> str: # type: ignore
    """
    获取值的类型。
    """
    pass

class Function:
    """
    函数实现类，用于定义和运行函数。
    """
    def __init__(self, name: str, args: list[str], body: list[str], isBuiltins: bool, number: int, linetext: str) -> None:
        """
        :param name: 函数名称
        :param args: 函数参数名字
        :param body: 函数体
        :param isBuiltins: 是否为内置函数
        :param number: 函数定义行号
        :param linetext: 函数定义行文本
        """
        pass

    def run(self, args: list[object]) -> None:
        """
        :param args: 传入函数参数
        :return: None （暂时没有函数返回值）
        """
        pass

    def __repr__(self) -> str: # type: ignore
        pass

def isNumbericString(value: str) -> bool: # type: ignore
    """
    判断字符串是否为数字字符串。

    :param value: 字符串
    :return: 布尔值
    """
    pass

class Runner:
    """
    运行器实现类，用于运行文件、文本和单行文本。
    """
    def __init__(self, EnvironmentName: str, *, config: configType = {'ContinueRunningAfterError': False}, function: bool = False) -> None:
        """
        :param EnvironmentName: 环境名称
        :param config: 一些配置（ContinueRunningAfterError是发生错误时是否继续运行，false为不继续运行，true为继续运行）
        :param function: 是否为函数运行器
        """
        self.raiser = Raiser
        self.environment = Environment(EnvironmentName, {})
        self.EnvironmentName = EnvironmentName
        self.config = config

    def run_file(self, filepath: str) -> None:
        """
        运行文件。

        :param filepath: 文件路径
        :return: None
        """
        pass

    def run_manylines(self, texts: str, path: str | None = None) -> None:
        """
        运行多行文本。

        :param texts: 多行文本
        :param path: 文件路径（不传则为<String\\>）
        :return: None
        """
        pass

    def End(self) -> None:
        """
        结束运行，清空当前导入列表。
        """
        pass

    def run_oneline(self, linetext: str, alltextlist: list[str], path: str | None = None, number: int = 1) -> None:
        """
        运行单行文本。

        :param linetext: 单行文本
        :param alltextlist: 所有文本的列表
        :param path: 文件路径（不传则为<String>）
        :param number: 行号
        :return: None
        """
        pass

class Keys:
    """
    关键字实现类，处理关键字逻辑。
    """
    @staticmethod
    def KeysLogic(clsobj: Runner, linetext: str, number: int, path: str, alltexts: list[str]) -> None:
        """
        关键字逻辑。

        :param clsobj: Runner对象
        :param linetext: 单行文本
        :param number: 行号
        :param path: 文件路径
        :param alltexts: 所有文本的列表
        :return: None
        """
        pass

class Expressions:
    """
    表达式实现类，处理表达式逻辑。
    """
    @staticmethod
    def ExpressionsLogic(clsobj: Runner, value: str, linetext: str, number: int, path: str) -> tuple[Any, Any, bool] | None:
        """
        表达式逻辑。

        :param clsobj: Runner对象
        :param value: 表达式
        :param linetext: 单行文本（报错使用的）
        :param number: 行号（报错使用的）
        :param path: 文件路径（报错使用的）
        :return: 元组（返回值，返回值类型，是否私有（永远为False））；None表示报错
        """
        pass

class Functions:
    """
    运行函数实现类，处理函数调用逻辑。
    """
    @staticmethod
    def FunctionsLogic(clsobj: Runner, linetext: str, number: int, path: str) -> tuple[Any, Any, bool] | None:
        """
        运行函数逻辑。

        :param clsobj: Runner对象
        :param linetext: 单行文本
        :param number: 行号
        :param path: 文件路径
        :return: 元组（变量，类型，是否是私有变量）；None表示发生错误
        """
        pass

class Variable:
    """
    变量实现类，处理变量逻辑。
    """
    @staticmethod
    def VariableLogic(clsobj: Runner, value: object, number: int, linetext: str, path: str) -> tuple | None: # type: ignore
        """
        变量逻辑。

        :param clsobj: Runner对象
        :param value: 变量值
        :param number: 行号
        :param linetext: 单行文本
        :param path: 文件路径
        :return: 元组（变量值，变量类型，是否私有变量）；None表示报错
        """
        pass

# 根运行器
root: Runner

def config_root(config: configType) -> None:
    """
    配置根运行器的配置项。

    :param config: 配置项
    """
    pass

def del___pycache__() -> None:
    """
    删除__pycache__文件夹。
    """
    pass
