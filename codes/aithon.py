import sys, time
# from .Runner import Runner, config_root
from .ImportRunner_pyc import Runner as RunnerModule
Runner = RunnerModule.Runner
config_root = RunnerModule.config_root
# from Edition_logs import Edition_logsForXRthon
from .VersionSystem import VersionSystem
from colorama import init, Fore, Style, Back
from .versions import GetVersionForaithon
from ._del_ import del___pycache__
from .logs import Check_log


init()

def main():
    SleepTime = 0.5

    version = GetVersionForaithon()

    time.sleep(SleepTime)

    if VersionSystem.CheckVersion(version if '/NVSFT: ' not in version else version.split('/NVSFT: ')[1]):
        Check_log.info(f'{Fore.GREEN}检查：你的 aithon 版本格式是正常的。{Style.RESET_ALL}')
    else:
        Check_log.warning(f'{Fore.RED}检查：你的 aithon 版本格式是无效的。{Style.RESET_ALL}')
        raise SystemExit()

    time.sleep(SleepTime)

    print(f'{Fore.LIGHTCYAN_EX}{Style.BRIGHT}{Back.LIGHTYELLOW_EX} aithon 编程语言{Style.RESET_ALL}')

    time.sleep(SleepTime)

    print(f'{Fore.LIGHTCYAN_EX}{Style.BRIGHT}{Back.LIGHTYELLOW_EX}版本：{version}{Style.RESET_ALL}')

    time.sleep(SleepTime)

    print(f'{Fore.LIGHTCYAN_EX}你可以使用 “import(English_Edition_logsForaithon)” 去查看版本日志{Style.RESET_ALL}')

    time.sleep(SleepTime)

    print(f'{Fore.LIGHTCYAN_EX}你可以使用 “import(Chinese_Edition_logsForaithon)” 去查看版本日志（中文版）{Style.RESET_ALL}')

    time.sleep(SleepTime)

    print(f'{Fore.LIGHTCYAN_EX}你可以使用 “help()” 去查看帮助{Style.RESET_ALL}')

    runner = Runner('main', config={'ContinueRunningAfterError': True})
    config_root({'ContinueRunningAfterError': True})

    running = True
    while running:
        try:

            time.sleep(SleepTime)

            command = input(' > ')

            time.sleep(SleepTime)

            # if command == 'help':
            #     print('a')

            if '.' in command:
                parts = command.split('.')
                if '(' in parts[0]:
                    runner.run_oneline(command, [command], None, 1)
                else:
                    name = parts[0]
                    attr_path = '.'.join(parts[1:])
                    
                    try:
                        # 获取环境中的对象
                        obj = runner.environment.values[name]['value'] # type: ignore
                        
                        # 逐层获取属性或方法
                        attr = obj # type: ignore
                        for part in attr_path.split('.'):
                            _ = attr[part] # type: ignore
                            attr = _['value'] if isinstance(_, dict) else _ # type: ignore
                        
                        # 执行属性或方法
                        # if callable(attr):
                        #     result = attr()
                        # else:
                        result = attr['value'] if isinstance(attr, dict) and 'value' in attr else attr # type: ignore
                        
                        print(result) # type: ignore
                    except Exception as e:
                        runner.raiser(f'{e.__class__.__name__}', f'{e}', 1, command, '<String>', e, runner.config)
            elif command == 'help()':
                text = '''\
使用“print()”输出文本。
""是一个字符串。
''是一个字符串。
1是一个数字。
使用“input()”获取输入。
使用“name=value”设置变量。使用“name=input()”获取输入。使用“import(name)”导入模块。使用“quit()”结束程序的运行。
使用“def_func name{args}:
    # 代码
”创建一个名为“name”的函数，其参数为“args”。
使用“name(args)”运行名为“name”的函数，该函数具有参数“args”。
使用“python {args}：
    # Python代码
”创建和运行python代码，并具有参数‘args’（提示：‘args’参数已在前面定义）。
使用 “if {1}:
    # 代码
” 去创建 if 语句 （1是可以用另一个表达式替换的表达式）。
使用 “while {1}:
    # 代码
” 去创建 while 语句 （1是可以用另一个表达式替换的表达式）。
\
'''
                print(text)
            else:
                if command in runner.environment.values.keys(): # type: ignore
                    print(runner.environment.values[command]['value']) # type: ignore
                else:
                    runner.run_oneline(command, [command], None, 1)
        except KeyboardInterrupt as e:
            print('^C\n', end='')
            runner.raiser('KeyboardInterrupt', 'User pressed Ctrl+C', 1, '^C', '<String>', e) # type: ignore
        except EOFError as e:
            print('^V\n', end='')
            runner.raiser('EOFError', 'User pressed Ctrl+V', 1, '^V', '<String>', e)

    del___pycache__()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        path = sys.argv[1]
        runner = Runner(path)
        try:
            runner.run_file(path)
        finally:
            input('---------------------\n文件运行结束，输入 回车 键退出\n')
    else:
        raise Exception('无效参数')
