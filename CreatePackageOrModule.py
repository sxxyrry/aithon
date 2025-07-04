import py7zr
import os
from codes import folder
import base64


TempPath = os.path.join(folder.folder, "./temp")
PackagePath = os.path.join(folder.folder, "./packages/")

def CreateAithonPackageOrModule():
    Type = input("输入aithon库的类型（包/模块）：")

    if Type == "包":
        author = input("输入包作者：")
        version = input("输入包版本：")
        name = input("输入包名：")
        path = input("输入包路径：")
        RunPythonPath = input("输入释放完成后运行Python代码的路径：")

        OutputPath = os.path.join(TempPath, f"./{name}.7z")

        with py7zr.SevenZipFile(OutputPath, 'w') as archive:
            def _a(DirPath: str):
                for i in os.listdir(DirPath):
                    if os.path.isfile(os.path.join(path, i)):
                        archive.write(os.path.join(path, i), i)
                    else:
                        _a(os.path.join(path, i))
            _a(path)
        
        with open(os.path.join(PackagePath, f"./{name}.aithon"), 'w') as f:
            with open(OutputPath, 'rb') as f2:
                with open(RunPythonPath, 'r') as f3:
                    f.write(f"author={author}\nversion={version}\ntype=package\nname={name}\ncontent={base64.b64encode(f2.read()).decode('utf-8')}\n[runpython]{f3.read()}[end runpython]")

        os.remove(OutputPath)
    
    elif Type == "模块":
        author = input("输入模块作者：")
        version = input("输入模块版本：")
        name = input("输入模块名：")
        path = input("输入模块路径：")
        RunPythonPath = input("输入释放完成后运行Python代码的路径：")

        OutputPath = os.path.join(PackagePath, f"./{name}.aithon")

        with open(OutputPath, 'w') as f:
            with open(path, 'rb') as f2:
                with open(RunPythonPath, 'r') as f3:
                    f.write(f"author={author}\nversion={version}\ntype=module\nname={name}\ncontent={base64.b64encode(f2.read()).decode('utf-8')}\n[runpython]{f3.read()}[end runpython]")

CreateAithonPackageOrModule()
