import os
import pathlib


# folder = pathlib.Path(__file__).parent.parent.resolve()
folder = pathlib.Path(__file__).parent.resolve()

from types import NoneType
from typing import Any, TypedDict


def GetVersionForXRthon():
    version = ''

    for _ in English_Edition_logsForXRthon.split('\n'):
        if _.endswith(' Version:'):
            version: str = _[:-9]
        elif _.endswith(' Version:\r'):
            version: str = _[:-10]
    
    return version

def GetVersionForEditor():
    version = ''

    for _ in English_Edition_logsForEditor.split('\n'):
        if _.endswith(' Version:'):
            version: str = _[:-9]
        elif _.endswith(' Version:\r'):
            version: str = _[:-10]
    
    return version

def GetVersion(EditionLogs: str) -> str:
    version = ''

    for _ in EditionLogs.split('\n'):
        if _.endswith(' Version:'):
            version: str = _[:-9]
        elif _.endswith(' Version:\r'):
            version: str = _[:-10]
    
    return version


with open(os.path.join(folder, './TextFIles/Edition_logs/English/Edition_logsForaithon.txt'), 'r', encoding='UTF-8') as f:
    English_Edition_logsForXRthon: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/English/Edition_logsForEditor.txt'), 'r', encoding='UTF-8') as f:
    English_Edition_logsForEditor: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/Chinese/Edition_logsForaithon.txt'), 'r', encoding='UTF-8') as f:
    Chinese_Edition_logsForXRthon: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/Chinese/Edition_logsForEditor.txt'), 'r', encoding='UTF-8') as f:
    Chinese_Edition_logsForEditor: str = f.read()

import shutil
def del_file(path: str):
    shutil.rmtree(path)

def del___pycache__():
    if os.path.exists('./custom/__pycache__/'):
        del_file('./custom/__pycache__/')
    if os.path.exists('./log/__pycache__/'):
        del_file('./log/__pycache__/')
    if os.path.exists('./VersionSystem/__pycache__'):
        del_file('./VersionSystem/__pycache__')
    if os.path.exists('./__pycache__'):
        del_file('./__pycache__')

KernelName = 'XRXRthonRunner'

version = GetVersionForXRthon()

# 定义关键字、运算符和标点符号
keys = [
    'def_class',
    'def_function',
    'END',
    'if',
    'else',
    'elif',
    'for',
    'while',
    'in',
    'and',
    'or',
    'not',
    'True',
    'False',
    'None',
    'return',
    'pass',
    'continue',
    'break',
    'lambda',
    'try',
    'except',
    'finally',
    'raise',
    'assert',
    'global',
    'nonlocal',
    'del',
    'import',
    'from',
    'as',
    'with',
    'yield',
    'async',
    'await',
]

operators = [
    '==', '!=', '>', '<', '>=', '<=',
    '+', '-', '*', '/', '//', '%', '**',
    '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=',
    '&=', '|=', '^=', '<<=', '>>=',
]

punctuation = [
    '(', ')', '[', ']', '{', '}', ',', ':', ';', '.',
]

ErrorTable = [
    ''
]

BuiltinsFunctoins = [
    'print',
    'input',
    'import',
    'quit',
    # 'len',
    # 'type',
    # 'int',
    # 'float',
    # 'str',
    # 'bool',
    # 'list',
    # 'dict',
    # 'tuple',
    # 'set',
    # 'range',
    # 'min',
    # 'max',
    # 'sum',
    # 'eval',
    # 'exec',
    # 'open',
]

BuiltinsPackages = [
    'os',
    'sys',
    # 'math',
    # 'random',
    # 'time',
    # 'datetime',
    # 'json',
    # 'pickle',
    # 're',
    # 'requests',
    # 'tkinter',
]

PackagesFolderPath = os.path.join(folder, './packages')

NowImport = []

# class XRTypes():
#     def __init__(self, type: str, value: str):
#         self.type = type
#         self.value = value


class configType(TypedDict):
    ContinueRunningAfterError: bool

class Raiser():
    '''
    报错器
    '''
    def __init__(
                 self,
                 type_: str,
                 message: str,
                 line: int,
                 text: str,
                 path: str,
                 pythonserror: Exception | None = None,
                 config: configType={'ContinueRunningAfterError': False}
                ):
        '''
        :param: type_ 报错类型
        :param: message 报错信息
        :param: line 报错行数
        :param: text 报错行文本
        :param: path 文件路径
        :param: pythonserror Python层面错误
        :param: config 一些配置（ ContinueRunningAfterError 是发生错误时是否继续运行，false 为不继续运行，true 为继续运行 ）
        '''
        if type_ == 'SystemExit':
            raise SystemExit()
        print(f'Traceback (most recent call last):')
        print(f'    File "{path}", line {line}')
        print(f'        {text}')
        print(f'        {len(text) * '^'}')
        print(f'{type_}(RunTimeError) : {message}')
        if pythonserror is not None:
            print(f'Python Level Errors:')
            print(f'{pythonserror.__class__.__name__} : {pythonserror}')
        if config['ContinueRunningAfterError'] == False:
            del___pycache__()
            raise SystemExit()
        # elif config['ContinueRunningAfterError'] == 'warn':
        #     print('Warning: The program will continue running after an error.')
        # elif config['ContinueRunningAfterError'] == 'ignore':
        #     print('Warning: The program will ignore the error.')
        elif config['ContinueRunningAfterError'] == True:
            pass

# class valuesType(TypedDict):
def boolean(value: Any) -> bool:
    '''
    将值转换为布尔值

    :param: value 值
    :return: 布尔值
    '''

    return bool(value)

class Environment():
    '''
    环境实现
    '''
    def __init__(self, name: str, values: dict[str, dict[str, dict]]): # type: ignore
        '''
        :param: name 环境名称
        :param: values 环境值（字典）
        '''
        # self.values = values
        # self.keys = keys
        # self.operators = operators
        # self.punctuation = punctuation
        # self.BuiltinsFunctoins = BuiltinsFunctoins
        self.name = name
        self.values = values # type: ignore
        self.iE = []
        # self.
        pass

    def set_values(self, values: dict): # type: ignore
        '''
        :param: values 要增加的环境值（字典）

        :return: None
        '''
        self.values.update(values) # type: ignore

    def AddImportsEnvironment(self, name: str):
        '''
        :param: name 要增加的导入的环境名称

        :return: None
        '''
        self.iE.append(name) # type: ignore

    def getImportsEnvironment(self) -> list[str]:
        '''
        :return: list[str] 返回导入的环境名称列表
        '''
        return self.iE # type: ignore
    
    def __getitem__(self, item): # type: ignore
        return self.values[item] # type: ignore

    def __str__(self):
        return f'Environment: {self.name}, Values: {self.values}' # type: ignore

Environments: dict[str, Environment] = {}

FunctionEnvironments: dict[str, Environment] = {}

class Object(object):
    def __init__(self, value: object):
        self.value = value
    
    def __add__(self, other): # type: ignore
        return Object(self.value + other.value) # type: ignore

    def __mul__(self, other): # type: ignore
        return Object(self.value * other.value) # type: ignore
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} [{self.value}]>'

class Str(Object):
    def __init__(self, value: object):
        self.value = str(value)
    
    def __add__(self, other): # type: ignore
        return Str(self.value + other.value) # type: ignore

    def __mul__(self, other): # type: ignore
        return Str(self.value * other.value) # type: ignore
    
    def __repr__(self) -> str:
        return f'<Object.{self.__class__.__name__} [\'{self.value}\']>'

class Int(Object):
    def __init__(self, value: object, number: int, linetext: str, path: str | None):
        # 取消 try-except 块，直接进行类型转换
        self.value = int(value) if str(value).isdigit() else Raiser( # type: ignore
            'ValueError',
            f'Cannot convert {value} to int',
            number,
            linetext,
            path if not path is None else '<String>',
            ValueError(f'Cannot convert {value} to int')
        )
        
        self.number = number
        self.linetext = linetext
        self.path = path
    
    def __add__(self, other): # type: ignore
        return Int(self.value + other.value, self.number, self.linetext, self.path) # type: ignore

    def __mul__(self, other): # type: ignore
        return Int(self.value * other.value, self.number, self.linetext, self.path) # type: ignore
    
    def __repr__(self) -> str:
        return f'<Object{self.__class__.__name__} [{self.value}]>'

class Float(Object):
    def __init__(self, value: object, number: int, linetext: str, path: str | None):
        try:
            self.value = float(value) # type: ignore
        except Exception as e:
            Raiser(
                   'ValueError',
                   f'Cannot convert {value} to float',
                   number,
                   linetext,
                   path if not path is None else '<String>',
                   e
                  )
        self.value = float(value) if str(value).isdigit() else Raiser( # type: ignore
            'ValueError',
            f'Cannot convert {value} to float',
            number,
            linetext,
            path if not path is None else '<String>',
            ValueError(f'Cannot convert {value} to float')
        )
        
        self.number = number
        self.linetext = linetext
        self.path = path
    
    def __add__(self, other): # type: ignore
        return Float(self.value + other.value, self.number, self.linetext, self.path) # type: ignore

    def __mul__(self, other): # type: ignore
        return Float(self.value * other.value, self.number, self.linetext, self.path) # type: ignore
    
    def __repr__(self) -> str:
        return f'<Object{self.__class__.__name__} [{self.value}]>'

class Nonetype(Object):
    def __init__(self, v: None):
        self.v: None = v
    
    def __repr__(self) -> str:
        return f'<Object{self.__class__.__name__} [{self.value}]>'

def GetType(value: object) -> str: # type: ignore
    pass

class Function():
    '''
    函数实现
    '''
    def __init__(self, name: str, args: list[str], body: list[str], isBuiltins: bool, number: int, linetext: str):
        '''
        :param: name 函数名称
        :param: args 函数参数名字
        :param: body 函数体
        :param: isBuiltins 是否为内置函数
        :param: number 函数定义行号
        :param: linetext 函数定义行文本
        '''
        self.name = name
        self.args = args
        self.body = body
        self.number = number
        self.isBuiltins = isBuiltins
        # self.Returns = None

        self.env = Environment(name, {})
        self.raiser = Raiser
    
    def run(self, args: list[object]) -> None:
        '''
        :param: args 传入函数参数

        :return: None （暂时没有函数返回值）
        '''
        if len(args) != len(self.args):
            self.raiser(
                'ValueError',
                f'Function {self.name} requires {len(self.args)} arguments, but {len(args)} arguments were given',
                self.number,
                self.body, # type: ignore
                self.name
            )
        
        globals_ = {
            self.args[i]: {
                'value' :  args[i],
                'type'  :  type(args[i]).__name__,
                'len'   :  len(str(args[i])),
            } for i in range(len(self.args))
        }

        if self.isBuiltins == True:
            exec(f'{self.body[0]}', globals=globals_)
        else:
            runner = Runner(self.name, function=True)
            self.env.set_values(globals_) # type: ignore
            runner.environment = self.env
            runner.raiser = self.raiser
            texts = '\n'.join(self.body)
            runner.run_fortexts(texts, None)
    
    def __repr__(self) -> str:
        return f'<Function {self.name}-{self.args}-isBuiltins={self.isBuiltins}>'

def isNumbericString(value: str):
    return str(value).isdigit() or str(value).replace('.', '').isdigit()

class Runner():

    '''
    运行器实现
    '''
    def __init__(self, EnvironmentName: str, *, config: configType={'ContinueRunningAfterError': False}, function: bool=False):
        '''
        :param: EnvironmentName 环境名称
        :param: config 一些配置（ ContinueRunningAfterError 是发生错误时是否继续运行，false 为不继续运行，true 为继续运行 ）
        :param: function 是否为函数运行器
        '''
        self.raiser = Raiser
        self.environment = Environment(EnvironmentName, {})
        self.EnvironmentName = EnvironmentName
        self.environment.set_values( # type: ignore
            {
                'Kernel' : {
                    'value' : {
                        'Name' : {
                            'value' : KernelName,
                            'type' : Str(KernelName),
                            'len' : len(KernelName)
                        },
                        'Version' : {
                            'value' : version,
                            'type' : Str(version),
                            'len' : len(version)
                        },
                    },
                    'type' : Object({
                        'Name' : {
                                'value' : KernelName,
                                'type' : Str(KernelName),
                                'len' : len(KernelName)
                            },
                            'Version' : {
                                'value' : version,
                                'type' : Str(version),
                                'len' : len(version)
                            }
                        }
                    ),
                    'len' : 2
                    # 'type' : {

                    # }
                },
                '__SYSTEM__' : {
                    'value' : {
                        'Name' : {
                            'value' : EnvironmentName,
                            'type' : Str(EnvironmentName),
                            'len' : len(EnvironmentName)
                        },
                    },
                    'type' : Object({
                        'Name' : {
                            'value' : EnvironmentName,
                            'type' : Str(EnvironmentName),
                            'len' : len(EnvironmentName)
                        },
                    }),
                    'len' : 1
                }
            }
        )
        if not function:
            Environments.update({EnvironmentName : self.environment})
        self.config = config
        # self.from_ = from_

    def run_forfilepath(self, filepath: str):
        '''
        运行文件

        :param: filepath 文件路径

        :return: None
        '''
        with open(os.path.join(filepath), 'r', encoding="utf-8") as f:
            texts = f.read()
        
        self.run_fortexts(texts, filepath)

    def run_fortexts(self, texts: str, path: str | None = None):
        '''
        运行多行文本

        :param: texts 多行文本
        :param: path 文件路径（不传则为<String\\>）
        
        :return: None
        '''
        number = 0
        alltextlist = texts.split('\n')
        for line in alltextlist:
            number += 1

            if line == '':
                continue
            
            self.run_forlinetext(line, alltextlist, path, number)

    def End(self):
        NowImport.clear()
        del self

    def run_forlinetext(self, linetext: str, alltextlist: list[str], path: str | None = None, number: int = 1):
        '''
        运行单行文本

        :param linetext 单行文本
        :param alltextlist 所有文本的列表
        :param path 文件路径（不传则为<String>）
        :param number 行号

        :return: None
        '''
        try:
            # 获取除注释的行文本
            linetext = '#'.join(linetext.split('#')[0:-1]) if '#' in linetext else linetext

            if 'END ' in linetext:
                return

            elif '=' in linetext and not linetext.startswith('    '):
                IsPrivateVariable = False
                list_ = linetext.split('=')
                name = list_[0]
                name = name if name[-1] != ' ' else name[:-1]
                v = '='.join(list_[1:])
                v = v if v[0] != ' ' else v[1:]
                type_ = None
                
                if name.split('(')[0] in BuiltinsFunctoins:
                    _1: tuple[int | str | Any | None, Int | Str | Nonetype, bool] = Functions.FunctionsLogic(self, v, number, path if not path is None else '<String>', name) # type: ignore

                    v = _1[0] # type: ignore

                    _2 =  Expressions.ExpressionsLogic(self, v, linetext, number, path) # type: ignore

                    v = _2[0] # type: ignore
                    type_ = _2[1] # type: ignore
                    IsPrivateVariable = _2[2] # type: ignore

                try:
                    exec(f'{name} = \'\'')
                except Exception as e:
                    root.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', e, root.config)
                    return

                _2: tuple[float | dict[Any, Any] | str | object, Float | Any | Str | Int | Object | None, False] = Variable.VariableLogic(self, v, number, linetext, path if not path is None else '<String>') # type: ignore

                v = _2[0]
                type_ = _2[1]
                IsPrivateVariable = _2[2] # type: ignore

                self.environment.set_values({name : {'value' : v, 'len' : len(str(v)), 'IsPrivateVariable' : IsPrivateVariable, 'type' : type_}}) # type: ignore

            elif '(' in linetext:
                Functions.FunctionsLogic(self, linetext, number, path if not path is None else '<String>')

            elif linetext.startswith('    '):
                return

            else:
                Keys.KeysLogic(self, linetext, number, path if not path is None else '<String>', alltextlist)

            Environments[self.EnvironmentName] = self.environment
        except KeyboardInterrupt as e:
            print('^C\n', end='')
            root.raiser('KeyboardInterrupt', 'User pressed Ctrl+C', 1, '^C', path if not path is None else '<String>', e) # type: ignore
        except EOFError as e:
            root.raiser('EOFError', 'User pressed Ctrl+V', 1, '^V', path if not path is None else '<String>', e)

class Keys():
    '''
    关键字实现
    '''
    @staticmethod
    def KeysLogic(clsobj: Runner, linetext: str, number: int, path: str, alltexts: list[str]):
        '''
        关键字逻辑

        :param clsobj Runner对象
        :param linetext 单行文本
        :param number 行号
        :param path 文件路径
        :param alltexts 所有文本的列表

        :return: None
        '''
        if linetext.startswith('def_func '):
            name = linetext.split('{')[0][9:]
            args_ = linetext.split('{')[1][0:-2].replace(' ', '').split(',')

            args = []

            for arg in args_:
                if arg == '': continue
                args.append(arg) # type: ignore

            body = []
            try:
                exec(f'def {name}({','.join(args)}):pass') # type: ignore
            except Exception as e:
                clsobj.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', e, clsobj.config) # type: ignore
        
            i = number

            while 1:
                if i >= len(alltexts): break
                    # root.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', config=clsobj.config) # type: ignore

                lt = alltexts[i]

                if not lt.startswith('    '): break

                body.append(lt[4:]) # type: ignore

                i += 1
            
            clsobj.environment.set_values( # type: ignore
                {
                    name : 
                    {
                        'value': 
                            Function(
                                name, args, body, False, number, linetext # type: ignore
                            ),
                        'len' : len(body), # type: ignore
                        'type' : 'function'
                    }
                }
            )

        elif linetext.startswith('python '):
            args_: list[str] = linetext.split('{')[1][:-2].replace(' ', '').split(',')
            if args_ == ['']:
                args_ = []
            
            args = {}

            for arg in args_:
                if arg in clsobj.environment.values: # type: ignore
                    args.update({arg : clsobj.environment.values[arg]['value']}) # type: ignore
                else:
                    clsobj.raiser('NameError', 'Name Error', number, linetext, path if not path is None else '<String>', config=clsobj.config) # type: ignore

            body = []
            try:
                exec(f'def test({','.join(args)}):pass') # type: ignore
            except Exception as e:
                clsobj.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', e, clsobj.config) # type: ignore
            
            i = number

            while 1:
                if i >= len(alltexts): break
                    # root.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', config=clsobj.config) # type: ignore

                lt = alltexts[i]

                if not lt.startswith('    '): break

                body.append(lt[4:]) # type: ignore

                i += 1

            try:
                exec('\n'.join(body), args) # type: ignore
            except Exception as e:
                clsobj.raiser(e.__class__.__name__, str(e), number, linetext, path if not path is None else '<String>', e, clsobj.config) # type: ignore

        elif linetext.startswith('if '):
            expr = linetext.split('{')[1][:-2]

            value = Expressions.ExpressionsLogic(clsobj, expr, linetext, number, path) # type: ignore

            if not isinstance(value, bool): # type: ignore
                value = boolean(value)

            if value:
                i = number

                body = []

                while 1:
                    if i >= len(alltexts): break
                        # root.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', config=clsobj.config) # type: ignore

                    lt = alltexts[i]

                    if not lt.startswith('    '): break

                    body.append(lt[4:]) # type: ignore

                    i += 1

                runner = Runner(linetext, config=clsobj.config, function=True)
                runner.environment.set_values(clsobj.environment.values) # type: ignore

                runner.run_fortexts('\n'.join(body), path) # type: ignore

                clsobj.environment.set_values(runner.environment.values) # type: ignore
            
        elif linetext.startswith('while '):
            expr = linetext.split('{')[1][:-2]

            i = number

            body = []

            while 1:
                if i >= len(alltexts): break
                    # root.raiser('SyntaxError', 'Syntax Error', number, linetext, path if not path is None else '<String>', config=clsobj.config) # type: ignore

                lt = alltexts[i]

                if not lt.startswith('    '): break

                body.append(lt[4:]) # type: ignore

                i += 1

            runner = Runner(linetext, config=clsobj.config, function=True)
            runner.environment.set_values(clsobj.environment.values) # type: ignore

            while boolean(Expressions.ExpressionsLogic(clsobj, expr, linetext, number, path)):

                runner.run_fortexts('\n'.join(body), path) # type: ignore

                clsobj.environment.set_values(runner.environment.values) # type: ignore

class Expressions():
    '''
    表达式实现
    '''
    @staticmethod
    def ExpressionsLogic(clsobj: Runner, value: str, linetext: str, number: int, path: str): # type: ignore
        '''
        表达式逻辑

        :param: clsobj Runner对象
        :param: value 表达式
        :param: linetext 单行文本 # 报错使用的
        :param: number 行号 # 报错使用的
        :param: path 文件路径 # 报错使用的

        :return: tuple 返回值 返回值类型 是否私有（永远为False）
        :return: None 表示报错
        '''

        _ = clsobj.environment.values # type: ignore

        v_: list[str] = []

        for i__ in value:
            v_.append(i__)

        i = 0
        while i < len(value):
            char = v_[i]
            
            if char == '[':
                i_ = i + 1
                i__ = i_ + 1

                __ = '[\"value\"]['
                while i_ < len(value):
                    if value[i_] == ']':
                        __ += ']'

                        break
                    else:
                        __ += value[i_]
                                        
                    i_ += 1
                    i__ += 1
                
                v_[i:i__] = __

            if char == '.':
                # char = '['
                if v_[i - 1].isdigit() and v_[i + 1].isdigit():
                    continue
            
                i_ = i + 1

                __ = ''
                while i_ < len(value):
                    if value[i_] == ' ' or value[i_] == '.':
                        __ = ']'
                        break
                    else:
                        __ = ''
                                        
                    i_ += 1
                
                if i_ == len(value):
                    if __ != ']':
                        __ = ']'

                if __ != ']':
                    root.raiser(
                        'Syntax Error', 
                        'Syntax Error', 
                        number, 
                        linetext, 
                        path if not path is None else '<String>',  # type: ignore
                        config=clsobj.config
                    )
                else:
                    v_[i] = '[\"value\"][\"'
                    if i_ == len(value):
                        v_.append('')
                    # v_[i_] = '\"]'
                    v_[i_] = '\"][\"value\"]'
                
            i += 1
        
        value = ''.join(v_)

        try:
            # 使用 compile 替代 eval
            code = compile(value, '<string>', 'eval')
            a = eval(code, globals=_) # type: ignore
        except Exception as e:
            if value == '':
                a = ''
            else:
                root.raiser(e.__class__.__name__, str(e), number, linetext, path if not path is None else '<String>', e, clsobj.config) # type: ignore
                return

        if isinstance(a, str):
            type_ = Str(a)
        
        elif isinstance(a, int):
            type_ = Int(a, number, linetext, path)
        
        elif isinstance(a, float):
            type_ = Float(a, number, linetext, path)
        
        else:
            type_ = Nonetype(None)
        
        return a, type_, False

class Functions():
    '''
    运行函数实现
    '''
    @staticmethod
    def FunctionsLogic(clsobj: Runner, linetext: str, number: int, path: str):
        '''
        运行函数逻辑

        :param: clsobj Runner对象
        :param: linetext 单行文本
        :param: number 行号
        :param: path 文件路径

        :return: tuple 变量 类型 是否是私有变量
        :return: None 发生错误
        '''
        if linetext.split('(')[0].startswith('print'):
            p: str = linetext[6:][:-1]
            
            try:
                # _ = Variable.VariableLogic(clsobj, p, number, linetext, path if not path is None else '<String>') # type: ignore
                # p = _[0] # type: ignore
                p = Expressions.ExpressionsLogic(clsobj, p, linetext, number, path)[0] # type: ignore
            except Exception as e:
                if not p == '':
                    root.raiser('NameError', 'Name is not defined', number, linetext, path if not path is None else '<String>', e, root.config) # type: ignore
                    return

            print(p) # type: ignore
            v = None
        
        elif linetext.split('(')[0].startswith('input'):
            p = linetext[6:][:-1]

            try:
                _ = Variable.VariableLogic(clsobj, p, number, linetext, path if not path is None else '<String>') # type: ignore
                p = _[0] # type: ignore
                p = Expressions.ExpressionsLogic(clsobj, p, linetext, number, path)[0] # type: ignore
            except Exception as e:
                if not p == '':
                    root.raiser('NameError', 'Name is not defined', number, linetext, path if not path is None else '<String>', e, root.config) # type: ignore
                    return

            v = input(p) # type: ignore

        elif linetext.split('(')[0].startswith('import'):
            p = linetext[7:][:-1]

            if p == 'English_Edition_logsForXRthon':
                print(English_Edition_logsForXRthon)

            elif p == 'Chinese_Edition_logsForXRthon':
                print(Chinese_Edition_logsForXRthon)

            elif p in os.listdir(PackagesFolderPath):
                if p in NowImport:
                    root.raiser('LoopImportError', 'Package was loop import', number, linetext, path if not path is None else '<String>', None, root.config) # type: ignore
                
                path = f'{PackagesFolderPath}/{p}' # /{p}
            
                runner = Runner(p)
            
                NowImport.append(p) # type: ignore

                if not os.path.isfile(path):
                    for fn in os.listdir(path):
                        if fn.endswith('.ait'):
                            fp = f'{path}/{fn}'
                            
                            runner.run_forfilepath(fp)

                clsobj.environment.set_values({p : {'value' : runner.environment.values}}) # type: ignore

                clsobj.environment.AddImportsEnvironment(runner.EnvironmentName)

                NowImport.remove(p) # type: ignore

            elif f'{p}.ait' in os.listdir(PackagesFolderPath):
                if f'{p}.ait' in NowImport:
                    root.raiser('LoopImportError', 'Package was loop import', number, linetext, path if not path is None else '<String>', None, root.config) # type: ignore
                else:
                    runner = Runner(p)
                    
                    path = f'{PackagesFolderPath}/{p}.ait'

                    NowImport.append(f'{p}.ait') # type: ignore

                    runner.run_forfilepath(path)
                
                    clsobj.environment.set_values({p : {'value' : runner.environment.values}}) # type: ignore
                
                    clsobj.environment.AddImportsEnvironment(runner.EnvironmentName)

                    NowImport.remove(f'{p}.ait') # type: ignore

            elif p in BuiltinsPackages:
                if p == 'os':
                    clsobj.environment.set_values({'os' : {'value' : { # type: ignore
                        'environ' : os.environ,
                        'name' : os.name,
                    }}})
                elif p == 'sys':
                    clsobj.environment.set_values({'sys' : {'value' : { # type: ignore
                        'version' : version
                    }}})
                elif p == 'XRthon':
                    clsobj.environment.set_values({'XRthon' : {'value' : { # type: ignore
                        'version' : version,
                        
                    }}})
                elif p == 'this':
                    # print('This is XRthon')
                    pass
                else:
                    pass
                
            elif p in Environments.keys():
                clsobj.environment.set_values({p : {'value' : Environments[p].values}}) # type: ignore
            
            else:
                root.raiser('NameError', 'Name is not defined', number, linetext, path if not path is None else '<String>', config=root.config) # type: ignore
                return

            v = 'None'

        elif linetext.split('(')[0].startswith('quit'):
            # name = linetext[4:][:-1]

            root.raiser('SystemExit', '', number, linetext, path if not path is None else '<String>', config=root.config) # type: ignore

            pass

        elif linetext.split('(')[0].startswith('type'):
            pass

        elif linetext.split('(')[0] in clsobj.environment.values.keys(): # type: ignore
            # type: ignore
            name = linetext.split('(')[0]
            _= clsobj.environment.values[name] # type: ignore
            func: Function = _['value'] # type: ignore
            if not isinstance(func, Function): # type: ignore
                clsobj.raiser('TypeError', f'The name \'{func}\' is not a function', number, linetext, path if not path is None else '<String>', config=root.config)

            args_: list[str] = linetext.split('(')[1][:-1].replace(' ', '').split(',')
            if args_ == ['']:
                args_ = []
            
            args = []

            for arg in args_:
                tle = Variable.VariableLogic(clsobj, arg, number, linetext, path if not path is None else '<String>') # type: ignore

                arg = tle[0] # type: ignore

                arg =  Expressions.ExpressionsLogic(clsobj, arg, linetext, number, path) # type: ignore

                args.append(arg) # type: ignore

            func.run(args) # type: ignore

            v = 'None'

            pass

        else:
            if '.' in linetext.split('(')[0]:
                if linetext.startswith(' '):
                    return
                _ = Variable.VariableLogic(clsobj, linetext.split('(')[0], number, linetext, path if not path is None else '<String>') # type: ignore
                if _[1] == 'function': # type: ignore
                    args_ = linetext.split('(')[1][:-1].replace(' ', '').split(',')
                    if args_ == ['']:
                        args_ = []

                    args = []

                    for arg in args_:
                        tle = Variable.VariableLogic(clsobj, arg, number, linetext, path if not path is None else '<String>') # type: ignore

                        arg: str = tle[0] # type: ignore

                        arg = Expressions.ExpressionsLogic(clsobj, arg, linetext, number, path)[0] # type: ignore
                        
                        args.append(arg) # type: ignore

                    func: Function = _[0] # type: ignore

                    func.run(args) # type: ignore
            v = 'None'

        v = f'\'{v}\''.replace('\\', '\\\\') # type: ignore

        type_ = Str(v)

        try:
            # 使用 compile 替代 eval
            code = compile(v, '<string>', 'eval')
            v = eval(code)
        except Exception as e:
            if type(e) == NameError:
                root.raiser(
                            'NameError',
                            f'The name ({v}) is not defined',
                            number,
                            linetext,
                            path if not path is None else '<String>', # type: ignore
                            e,
                            root.config
                        )
                return
            else:
                root.raiser(
                            'SyntaxError',
                            'Invalid syntax',
                            number,
                            linetext, path if not path is None else '<String>', # type: ignore
                            e,
                            root.config
                        )
                return

        try:
            try:
                name = 'a'
                if type(v) == str:
                    if '\'' in v:
                        exec(f'{name} = "{v}"')
                    if '\"' in v:
                        exec(f'{name} = \'{v}\'')
                else:
                    exec(f'{name} = {v}')
                if name in keys:
                    root.raiser(
                                'SyntaxError',
                                'Invalid syntax',
                                number,
                                linetext,
                                path if not path is None else '<String>', # type: ignore
                                SyntaxError('invalid syntax'),
                                root.config
                            )
                    return
            except Exception as e:
                root.raiser(
                            'SyntaxError',
                            'Invalid syntax',
                            number,
                            linetext,
                            path if not path is None else '<String>', # type: ignore
                            e,
                            root.config
                        )
                return

            IsPrivateVariable = False

            if name.startswith('__'): # type: ignore
                IsPrivateVariable = True

            if type(v) == int:
                type_ = Int(v, number, linetext, path)
            elif type(v) == str:
                type_ = Str(v)
            elif type(v) == NoneType:
                type_ = Nonetype(v)

            return v, type_, IsPrivateVariable
        except Exception as e:
            return

class Variable():
    '''
    变量实现
    '''
    @staticmethod
    def VariableLogic(clsobj: Runner, value: object, number: int, linetext: str, path: str) -> tuple | None: # type: ignore
        '''
        变量逻辑

        :param: clsobj Runner对象
        :param: value 变量值
        :param: number 行号
        :param: linetext 单行文本
        :param: path 文件路径

        :return: tuple 变量值 变量类型 是否私有变量
        :return: None 报错
        '''
        type_ = None # type: ignore
        
        def _a(value: str): # type: ignore
            if (value.startswith('"') and value.endswith('"')) \
               or (value.startswith('\'') and value.endswith('\'')):
                value = value[1:-1]
                type_ = Str(value)

            else:
                try:
                    value = '' if value == '' else eval(value) if value not in clsobj.environment.values.keys() else clsobj.environment.values[value]['value'] # type: ignore

                    t = type(value)

                    type_: Int | Float | Str | Nonetype | Object  = Int(value, number, linetext, path) if t == int else Float(value, number, linetext, path) if t == float else Str(value) if t == str else Nonetype(None) if t == NoneType else Object(value) # type: ignore
                except Exception as e:
                    root.raiser(
                                'SyntaxError',
                                'Invalid syntax',
                                number,
                                linetext,
                                path if not path is None else '<String>', # type: ignore
                                e,
                                root.config
                            )
                    return
            
            return (value, type_, False)

        value = str(value)
        if '.' in value:
            try:
                value = float(value)
                type_ = Float(value, number, linetext, path)
            except:
                parts = str(value).split('.')
                name = parts[0]
                attr_path = '.'.join(parts[1:])

                # 获取环境中的对象
                if name not in clsobj.environment.values.keys(): # type: ignore
                    value, type_, IsPrivateVariable = _a(value) # type: ignore
                    return (value, type_, IsPrivateVariable) # type: ignore
                obj = clsobj.environment.values[name]['value'] # type: ignore
                
                # 逐层获取属性或方法
                attr = obj # type: ignore
                for part in attr_path.split('.'):
                    _ = attr[part] # type: ignore
                    type_ = _['type'] if isinstance(_, dict) and ('type' in _) else Nonetype(None) # type: ignore
                    attr = _['value'] if isinstance(_, dict) else _ # type: ignore
                
                # 执行属性或方法
                # if callable(attr):
                #     result = attr()
                # else:
                result = attr['value'] if isinstance(attr, dict) and 'value' in attr else attr # type: ignore
                # type_ = attr['type']
                

                return (result, type_, False) # type: ignore
        else:
            value, type_, IsPrivateVariable = _a(value) # type: ignore
        
        return (value, type_, IsPrivateVariable) # type: ignore

root = Runner('root')

def config_root(config: configType):
    root.config = config

del___pycache__()
