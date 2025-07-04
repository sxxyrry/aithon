import py7zr
import os
from codes import folder
import base64
from typing import TypedDict


TempPath = os.path.join(folder.folder, "./temp")
PackagePath = os.path.join(folder.folder, "./packages/")

class Parsed(TypedDict):
    author: str
    version: str
    type: str
    name: str
    content: str
    run_python: str

class AithonFileParser:
    def __init__(self, path: str):
        self.path = path

    def parse(self):
        with open(self.path, 'r') as f:
            text = f.read()
        
        parsed: Parsed = {
            'author': '',
            'version': '',
            'type': '',
            'name': '',
            'content': '',
            'run_python' : '',
        }

        list_ = text.splitlines()

        # for line in list_:  # 使用 splitlines() 替代 split('\n')
        i = 0
        while 1:
            line = list_[i]
            line = line.strip()  # 去除首尾空白
            if line.startswith('author='): parsed['author'] = line.split('=')[1].strip()
            if line.startswith('version='): parsed['version'] = line.split('=')[1].strip()
            if line.startswith('type='): parsed['type'] = line.split('=')[1].strip()
            if line.startswith('name='): parsed['name'] = line.split('=')[1].strip()
            if line.startswith('content='):
                # 直接截取等号后的全部内容（避免换行符干扰）
                parsed['content'] = line.split('=', 1)[1].strip()
            if line == '[runpython]':
                # 读取直到遇到 '[end runpython]'
                i = list_.index(line) + 1
                while True:
                    line_ = list_[i]
                    if line == '[end runpython]': break
                    parsed['run_python'] += line + '\n'
                    i += 1
                
                i -= 1
            i += 1

        return parsed

def OutputAithonPackageOrModule(path: str):
    parser = AithonFileParser(path)
    parsed = parser.parse()

    if parsed['type'] == 'package':
        OutputPath = os.path.join(TempPath, f"./{parsed['name']}.7z")
        with open(OutputPath, 'wb') as f: f.write(base64.b64decode(parsed['content']))
        os.makedirs(os.path.join(PackagePath, f"./{parsed['name']}"), exist_ok=True)
        with py7zr.SevenZipFile(OutputPath, 'r') as archive: archive.extractall(os.path.join(TempPath, f"./{parsed['name']}"))
        os.remove(OutputPath)
        exec(parsed['run_python'])
    elif parsed['type'] == 'module':
        OutputPath = os.path.join(PackagePath, f"./{parsed['name']}.ait")
        with open(OutputPath, 'wb') as f: f.write(base64.b64decode(parsed['content']))
        exec(parsed['run_python'])

OutputAithonPackageOrModule("./codes/temp/Test1Module.aithon")
