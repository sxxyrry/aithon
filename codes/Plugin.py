import os, shutil
from PIL import Image, ImageTk
# from PIL.ImageFile import ImageFile
from typing import Literal, TypedDict
from .folder import folder
from .PluginAPI import *
from .GithubAboutFile import ListDir, DownloadDir
from .BaseGConfig import token
from .logs import Plugins_log
from .PluginBaseClass import PluginModifyTextBaseClass, PluginNormalBaseClass, PluginBaseClass, PluginAddContentMenuBaseClass


PluginsPath = os.path.join(folder, './plugins')
PluginsIconDict: dict[str, ImageTk.PhotoImage] = {}

def GetAllPlugins() -> list[str]:
    PluginsList: list[str] = ListDir(token, 'sxxyrry', 'aithonPluginsDatabase', 'plugins')
    NewPL: list[str] = []
    for PluName in PluginsList:
        if PluName == 'a' or PluName == '__init__.py' or PluName == '__pycache__':
            continue
        else:
            NewPL.append(PluName)
    return NewPL

def UninstallPlugin(PluName: str):
    if os.path.exists(os.path.join(PluginsPath, f'./{PluName}')):
        shutil.rmtree(os.path.join(PluginsPath, f'./{PluName}'))

def InstallPlugin(PluName: str):
    DownloadDir(token, 'sxxyrry', 'aithonPluginsDatabase', f'plugins/{PluName}', os.path.join(PluginsPath, f'./{PluName}'))

def LoadPluginModifyText() -> list[str]:
    TL: list[str] = TextList.copy()
    for cls in PluginModifyTextBaseClass.Register:
        clsobj: PluginBaseClass = cls()
        
        TL: list[str] = clsobj.UsePlugin() # type: ignore
    return TL if TL else TextList # type: ignore

def LoadPluginsNormal() -> None:
    for cls in PluginNormalBaseClass.Register:
        clsobj: PluginBaseClass = cls()
        
        clsobj.UsePlugin() # type: ignore
    return

def LoadPluginsAddContentMenu(liner: Liner) -> None:
    for cls in PluginAddContentMenuBaseClass.Register:
        clsobj: PluginBaseClass = cls()
        
        clsobj.CallBack(liner) # type: ignore
    return

def RegisterPlugins():
    for dir_ in os.listdir(PluginsPath):
        if dir_ == 'a' and os.path.isfile(os.path.join(PluginsPath, dir_)):
            continue
        if dir_ == '__init__.py' and os.path.isfile(os.path.join(PluginsPath, dir_)):
            continue
        if dir_ == '__pycache__' and os.path.isdir(os.path.join(PluginsPath, dir_)):
            continue
        path = os.path.join(PluginsPath, dir_)

        if IsPlugin(path):
            path = pathlib.Path(path).resolve()
            
            with open(os.path.join(path, './config.json'), 'r', encoding='UTF-8') as f:
                config: dict[str, str] = yaml.safe_load(f)
            
            if config['state'] == 'Disabled':
                continue
            else:
                Plugins_log.info(f"注册插件······ {dir_} （{path}）")
                filePath = os.path.join(path, '__init__.py')

                try:
                    with open(filePath, 'r', encoding='UTF-8') as f:
                        c = f.read()
                        c = c.replace('../../', './codes/')
                        c = c.replace('...', 'codes.')
                        exec(c)
                   
                    LoadedPluginsList.append(dir_)
                    Plugins_log.info(f"插件 {dir_} 注册完成 （{path}）")
                except Exception as e:
                    Plugins_log.warning(f"注册插件时发生错误 {dir_}： {e} （{path}）")
                    
        else:
            Plugins_log.warning(f"插件 {dir_} 不是一个插件 （{path}）")

def IsPlugin(Path: str) -> bool:
    if os.path.isdir(Path):
        if os.path.exists(os.path.join(Path, './AithonEditorPlugin')):
            try:
                with open(os.path.join(Path, './AithonEditorPlugin'), 'r') as f:
                    text = f.read()
            except Exception: return False
            if text == '1376046_1421686_1434237_1420545_1428532_1427391_1380610_1415981_1421686_1434237_1428532_1431955_1393161_1425109_1435378_1419404_1421686_1427391_':
                if os.path.exists(os.path.join(Path, '__init__.py')):
                    if os.path.exists(os.path.join(Path, 'config.json')):
                        try:
                            with open(os.path.join(Path, 'config.json'), 'r', encoding="UTF-8") as f: config: dict[str, str] = json.load(f)
                        except Exception: return False
                        
                        if "EditionLogsFilePath" in config and "state" in config and "IconFilePath" in config and "OverviewText" in config and "MarkdownFilePathForDescribingInformation" in config:
                            if config["state"] == "Enabled" or config["state"] == "Disabled":
                                if os.path.exists(os.path.join(Path, config["EditionLogsFilePath"])) and os.path.exists(os.path.join(Path, config["IconFilePath"])) and os.path.exists(os.path.join(Path, config["MarkdownFilePathForDescribingInformation"])):
                                    if config["EditionLogsFilePath"].endswith('txt'):
                                        try: 
                                            with open(os.path.join(Path, config["EditionLogsFilePath"]), 'r', encoding='UTF-8') as f: f.read();f.close()
                                        except Exception: return False
                                    if config["IconFilePath"].endswith('png') or config["IconFilePath"].endswith('jpg') or config["IconFilePath"].endswith('jpeg') or config["IconFilePath"].endswith('gif'):
                                        try: Image.open(os.path.join(Path, config["IconFilePath"]))
                                        except Exception: return False
                                    if config["MarkdownFilePathForDescribingInformation"].endswith('md'):
                                        try: 
                                            with open(os.path.join(Path, config["MarkdownFilePathForDescribingInformation"]), 'r', encoding='UTF-8') as f: f.read();f.close()
                                        except Exception: return False
                                    return True
                                else: return False
                            else: return False
                        else: return False
                    else: return False
                else: return False
            else: return False
        else: return False
    else: return False

def GetLoadedPlugins() -> list[str]:
    return LoadedPluginsList

class PluginType_(TypedDict):
    EditionLogsFilePath: str
    state: Literal["Enabled", "Disabled"]
    IconFilePath: str
    OverviewText: str
    MarkdownFilePathForDescribingInformation: str

def GetInstalledPluginsList() -> list[tuple[str, Literal['Enabled', 'Disabled'], Image.Image, str, str]]:
    InstalledPluginsList: list[tuple[str, Literal['Enabled', 'Disabled'], Image.Image, str, str]] = []
    for dir_ in os.listdir(PluginsPath):
        if IsPlugin(os.path.join(PluginsPath, dir_)):
            with open(os.path.join(PluginsPath, dir_, './config.json'), 'r', encoding='UTF-8') as jsonf:
                config: PluginType_ = yaml.safe_load(jsonf)
            IFP = os.path.join(PluginsPath, dir_, config["IconFilePath"])
            img = Image.open(IFP)
            img = img.resize((64, 64)) # type: ignore

            OverviewText = config["OverviewText"]
            MDFPFDI = config["MarkdownFilePathForDescribingInformation"]
            with open(os.path.join(PluginsPath, dir_, MDFPFDI), 'r', encoding='UTF-8') as f:
                InfoMDContent = f.read()

            # image = ImageTk.PhotoImage(img)
            InstalledPluginsList.append((dir_, config['state'], img, OverviewText, InfoMDContent))
    return InstalledPluginsList
