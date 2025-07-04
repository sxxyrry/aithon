import os
import sys
import tkinter as tk
import webbrowser
import time
import json
import pyperclip
from typing import Literal
from PIL import Image, ImageTk
import tkintertools as tkt # type: ignore
import tkinter.ttk as ttk
import _tkinter as _tk
from tkinter import filedialog, messagebox, scrolledtext
from colorama import Fore, Style, init
import yaml
from .custom.liner import Liner
from .ImportRunner_pyc import Runner as RunnerModule
Runner = RunnerModule.Runner
from .Edition_logs import English_Edition_logsForEditor, Chinese_Edition_logsForEditor
from .VersionSystem import VersionSystem
from .folder import folder
from .versions import GetVersionForEditor, GetVersionForaithon
from ._del_ import del___pycache__
from .GithubAboutFile import GetFileText, DownloadFile
from .BaseGConfig import token
from .PluginAPI import (
    root,
    frames,
    parent,
    Up,
    Bottom,
    config,
    GetVersion,
    JudgeVersion_Less_Plugin,
    framesInfo,
    MainNotebook,
    InfoNB,
    InfoNBFrame,
    AddInfoPage,
    notice,
    TextList,
    CustomNotebook,
)
from .Plugin import (
    LoadPluginModifyText,
    GetInstalledPluginsList,
    GetAllPlugins,
    FindPlugin,
    InstallPlugin,
    LoadPluginsNormal,
    PluginsPath,
    RegisterPlugins,
    UninstallPlugin,
    LoadPluginsAddContentMenu,
)
import threading
from .logs import Check_log, Runner_log
import urllib3
from PIL import Image, ImageTk


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init()

version = GetVersionForEditor()
if VersionSystem.CheckVersion(version if '/NVSFT: ' not in version else version.split('/NVSFT: ')[1]):
    Check_log.info(f'{Fore.GREEN}检查：你的 aithon 编辑器 版本格式是正常的。{Style.RESET_ALL}')
else:
    Check_log.warning(f'{Fore.RED}检查：你的 aithon 编辑器 版本格式是无效的。{Style.RESET_ALL}')
AithonVersion = GetVersionForaithon()
if VersionSystem.CheckVersion(AithonVersion if '/NVSFT: ' not in AithonVersion else AithonVersion.split('/NVSFT: ')[1]):
    Check_log.info(f'{Fore.GREEN}检查：你的 aithon 版本格式是正常的。{Style.RESET_ALL}')
else:
    Check_log.warning(f'{Fore.RED}检查：你的 aithon 版本格式是无效的。{Style.RESET_ALL}')


TempPath = os.path.join(folder, './temp')

class Editor():
    def __init__(self, NewTextList: list[str] | None = None):
        self.frames: list[tuple[tk.Frame, Liner]] = frames
        self.framesInfo: list[tk.Frame] = framesInfo
        self.frame_id = -1
        self.i = 0
        self.Now_frame_id = 0
        self.root: tkt.Tk = root
        self.parent: tk.Frame = parent
        self.Up: tk.Menu = Up
        self.Bottom: tk.Frame = Bottom
        self.style = ttk.Style()
        self.bind_shortcuts()
        self.config = config

        self.texts = NewTextList if NewTextList is not None else TextList

        self.Run_Button = tk.Button(self.Bottom, text=self.texts[0], command=self.RunCode)
        self.Run_Button.pack(side=tk.RIGHT)

        self.add_editor_page_Button = tk.Button(self.Bottom, text=self.texts[1], command=self.add_editor_page)
        self.add_editor_page_Button.pack(side=tk.RIGHT)

        self.File_menu = tk.Menu(self.Up)
        self.File_menu.add_command(label=self.texts[2], command=self.open_file)
        self.File_menu.add_command(label=self.texts[3], command=self.save_file)
        self.File_menu.add_command(label=self.texts[4], command=self.choose_file_and_run)

        self.About_menu = tk.Menu(self.Up)
        self.About_menu.add_command(label=self.texts[5], command=self.AboutInterface)
        self.About_menu.add_command(label=self.texts[6], command=self.AboutUsInterface)

        self.Plugin_menu = tk.Menu(self.Up)
        self.Plugin_menu.add_command(label=self.texts[28], command=self.AllPluginsInterface)
        self.Plugin_menu.add_command(label=self.texts[7], command=self.InstalledPluginsInterface)

        self.EditionLogs_menu = tk.Menu(self.Up)
        self.EditionLogs_menu.add_command(label=self.texts[8], command=self.EditionLogsInterface_English)
        self.EditionLogs_menu.add_command(label=self.texts[9], command=self.EditionLogsInterface_Chinese)

        self.Up.add_cascade(label=self.texts[10], menu=self.File_menu)
        self.Up.add_cascade(label=self.texts[11], menu=self.About_menu)
        self.Up.add_cascade(label=self.texts[12], menu=self.Plugin_menu)
        self.Up.add_cascade(label=self.texts[13], menu=self.EditionLogs_menu)
        if self.config.Mode == 'DEV':
            self.Up.add_command(label="Restart", command=self.Restart)
            # self.Up.add_command(label=self.texts[24], command=self.Restart)

            pass
        self.Up.add_command(label=self.texts[22], command=self.switch_language)
        self.Up.add_command(label=self.texts[23], command=self.Introduction_Website)
        self.Up.add_command(label=self.texts[14], command=self.VersionInterface)
        self.Up.add_command(label=self.texts[15], command=lambda: os._exit(0))
        self.Up.add_command(label='问卷调查', command=lambda: webbrowser.open('https://wj.qq.com/s2/22532965/60f7/'))
        
        self.root.config(menu=self.Up)

        self.ResourceManager = tk.Frame(self.parent, bd=2, relief="solid")
        # _f_ = tk.Frame(self.ResourceManager)
        # _f_.pack(fill=tk.BOTH)
        _f = tk.Frame(self.ResourceManager)
        _f.pack(side=tk.TOP)
        _text = tk.Label(_f, text=self.texts[50])
        _text.grid(row=0, column=0)
        _btn = tk.Button(_f, text=self.texts[51], command=self.ChooseDirToResourceManager)
        _btn.grid(row=0, column=1)
        _a = tk.Label(self.ResourceManager, text=' '*100)
        _a.pack()
        self.FileViewRoot = tk.Frame(self.ResourceManager)

        
        # 创建一个包含滚动条的Canvas
        canvas = tk.Canvas(self.FileViewRoot) # 移除了宽度和高度的直接设定
        self.FileView = tk.Frame(canvas)
        self.FileView.pack(fill=tk.BOTH)
        self.FileView_ = tk.Frame(self.FileView)
        self.FileView_.pack()

        scrollbar = tk.Scrollbar(self.FileViewRoot, orient="vertical", command=canvas.yview) # type: ignore
        h_scrollbar = tk.Scrollbar(self.FileView_, orient="horizontal", command=canvas.xview)  # type: ignore


        # 绑定滚动条到Canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="right", fill="both", expand=True) # 使用pack()之前设置fill和expand
        scrollbar.pack(side="right", fill="y") # 保持在Canvas pack之后
        h_scrollbar.pack(side="bottom", fill="x")

        # 在 Canvas 中绑定鼠标中键事件
        canvas.bind("<Button-2>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        # 如果你希望支持鼠标滚轮滚动，可以绑定 <MouseWheel> 事件
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        canvas.bind("<Control-MouseWheel>", lambda event: canvas.xview_scroll(-1 * (event.delta // 120), "units"))

        # 在Canvas内部创建窗口
        canvas.create_window((0, 0), window=self.FileView, anchor='nw')

        # 配置Canvas的滚动行为
        self.FileView.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # 绑定横向滚动条到 Canvas
        canvas.configure(xscrollcommand=h_scrollbar.set)

        # 配置 Canvas 的滚动区域
        self.FileView.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # # CTRL+鼠标滚轮横向滚动 Canvas
        # self.FileView.bind("<Control-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))
        
        # self.Frames__: Toolslist[tk.Frame | tk.Canvas | tk.Scrollbar] = Toolslist()

        # self.Frames__.append_more(canvas, self.FileView, self.FileViewRoot, self.FileView_, h_scrollbar, scrollbar)

        # def _a_():
        #     for i in self.Frames__:
        #         i.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        #         i.bind("<Control-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        #     root.after(100, _a_)

        # root.after(100, _a_)

        # def mouse_wheel(e: tk.Event):
        #     # print(e.widget.winfo_class())
        #     # print(e.widget in self.Frames__)
        #     if e.widget == self.FileView or e.widget == canvas or e.widget == self.FileViewRoot or e.widget in self.Frames__:
        #         canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        #     if hasattr(e.widget, 'yview'):
        #         e.widget.yview_scroll(int(-1 * (e.delta / 120)), "units")

        
        # def control_mouse_wheel(e: tk.Event):
        #     # print(e.widget.winfo_class())
        #     # print(e.widget in self.Frames__)
        #     if e.widget == self.FileView or e.widget == canvas or e.widget == self.FileViewRoot or e.widget in self.Frames__:
        #         canvas.xview_scroll(int(-1 * (e.delta / 120)), "units")
                
        #     if hasattr(e.widget, 'xview'):
        #         e.widget.xview_scroll(int(-1 * (e.delta / 120)), "units")

        # # 添加鼠标滚轮纵向滚动绑定

        # # 保留现有的Ctrl+滚轮横向滚动
        # # canvas.bind("<Control-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))
        # self.root.bind("<MouseWheel>", mouse_wheel)
        # self.root.bind("<Control-MouseWheel>", control_mouse_wheel)

        self.ResourceManager.pack(side=tk.LEFT, fill=tk.Y)
        self.FileViewRoot.pack(fill=tk.BOTH, expand=True)
        self.MainNotebook = MainNotebook
        self.MainNotebook.pack(fill=tk.BOTH, expand=True)

        self.EditorNBFrame = tk.Frame(self.parent)
        self.EditorNB = CustomNotebook(self.EditorNBFrame)
        self.EditorNB.pack(fill=tk.BOTH, expand=True)

        self.InfoNB = InfoNB
        self.InfoNBFrame = InfoNBFrame

        self.Bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.Notice = notice
        self.Notice.title.config(text=self.texts[43])

        self.MainNotebook.add(self.EditorNBFrame, text=self.texts[48])
        self.MainNotebook.add(self.InfoNBFrame, text=self.texts[49])
        self.MainNotebook.protect_tab(0)
        self.MainNotebook.protect_tab(1)

        self.TestCanConnectTheDatabase()

        # self.root.after(100, self.CheckUpdate)
        self.CheckUpdate()

    def ChooseDirToResourceManager(self):
        Dir = filedialog.askdirectory()
        if Dir:
            Frame = tk.Frame(self.FileView)
            Frame.pack(fill=tk.BOTH, expand=True)
            self.AddResourceManagerDir(Dir, Frame)
    
    # def AddResourceManagerDir(self, Dir: str, Frame: tk.Frame):
    #     DirList = os.listdir(Dir)
    #     # print(DirList)
    #     # 以文件夹，文件的顺序进行排列
    #     DirList.sort(key=lambda x: os.path.isdir(os.path.join(Dir, x)), reverse=True)
    #     # DirList.sort(key=lambda x: os.path.isdir(os.path.join(Dir, x)))
    #     for i in DirList:
    #         if os.path.isdir(os.path.join(Dir, i)):
    #             DirFrame = tk.Frame(Frame)
    #             DirFrame.pack(fill=tk.X)
    #             Frame_ = tk.Frame(DirFrame)
    #             Frame_.pack(side=tk.BOTTOM)
    #             # Frame_.pack()
    #             DirImg: ImageFile.ImageFile = Image.open(os.path.join(folder, './Images/Dir.png')) # type: ignore
    #             DirImgTk = ImageTk.PhotoImage(DirImg.resize((23, 23))) # type: ignore

    #             DirImgLabel = tk.Label(DirFrame, image=DirImgTk)
    #             DirImgLabel.image = DirImgTk # type: ignore
    #             DirImgLabel.pack(side=tk.LEFT)

    #             _lbl = tk.Label(DirFrame, text=self.texts[52])
    #             _lbl.pack(side=tk.LEFT)

    #             DirLabel = tk.Label(DirFrame, text=i)
    #             DirLabel.pack(side=tk.LEFT)
    #             DirButton = tk.Button(DirFrame, text='+')
    #             DirButton.config(command=lambda i=i, Frame_=Frame_, DirButton=DirButton: self._ARMDCommand(os.path.join(Dir, i), Frame_, DirButton))
    #             DirButton.pack(side=tk.RIGHT)
    #         else:
    #             self.AddResourceManagerFile(i, Frame, Dir)
    
    # def _ARMDCommand(self, Dir: str, Frame: tk.Frame, Btn: tk.Button):
    #     if Btn['text'] == '+':
    #         Btn.config(text='-')
    #         self.AddResourceManagerDir(Dir, Frame)
    #     else:
    #         Btn.config(text='+')
    #         for i in [i for i in Frame.winfo_children()]:
    #             i.destroy()
    #         Frame.config(height=0)
    #         Frame.configure(height=0)
    #         Frame.update_idletasks()
    #         Frame.update()

    # def AddResourceManagerFile(self, File: str, Frame: tk.Frame, Dir:str):
    #     FileFrame = tk.Frame(Frame)
    #     FileFrame.pack(fill=tk.X)
        
    #     FileImg: ImageFile.ImageFile = Image.open(os.path.join(folder, './Images/File.png')) # type: ignore
    #     if File.endswith('.ait'):
    #         FileImg: ImageFile.ImageFile = Image.open(os.path.join(folder, './Images/aithonFile.png')) # type: ignore
    #     FileImgTk = ImageTk.PhotoImage(FileImg.resize((23, 23))) # type: ignore

    #     FileImgLabel = tk.Label(FileFrame, image=FileImgTk)
    #     FileImgLabel.image = FileImgTk # type: ignore
    #     FileImgLabel.pack(side=tk.LEFT)

    #     _lbl = tk.Label(FileFrame, text=self.texts[53])
    #     if File.endswith('.ait'):
    #         _lbl.config(text=self.texts[54])
    #     _lbl.pack(side=tk.LEFT)

    #     if File.endswith('.ait'):
    #         FileBtn = tk.Button(FileFrame, text=File, command=lambda File=os.path.join(Dir, File): self.OpenAithonFile(File))
    #         FileBtn.pack(side=tk.LEFT)
    #     else:
    #         FileLabel = tk.Label(FileFrame, text=File)
    #         FileLabel.pack(side=tk.LEFT)

    def AddResourceManagerDir(self, Dir: str, Frame: tk.Frame, indent_level=0):
        """创建类似VSCode资源管理器的树形结构"""
        DirList = os.listdir(Dir)
        # 将文件夹排在前面，文件排在后面
        dirs = [d for d in DirList if os.path.isdir(os.path.join(Dir, d))]
        files = [f for f in DirList if os.path.isfile(os.path.join(Dir, f))]
        sorted_items = dirs + files

        for i in sorted_items:
            full_path = os.path.join(Dir, i)
            is_dir = os.path.isdir(full_path)
            
            # 创建每行的Frame
            ItemFrame = tk.Frame(Frame)
            ItemFrame.grid(row=0, column=indent_level, sticky="nsew")  # 添加缩进来表示层级

            # self.Frames__.append(ItemFrame)
            
            # 添加缩进和图标之间的空白
            indent_space = tk.Frame(ItemFrame, width=indent_level * 20)
            indent_space.grid(row=0, column=0)
            # self.Frames__.append(indent_space)
            
            if is_dir:
                # 文件夹 - 带有折叠/展开功能
                self._add_directory(ItemFrame, i, full_path, indent_level)
            else:
                # 文件 - 显示文件图标和名称
                self._add_file(ItemFrame, i, full_path, Dir, indent_level)

    def _add_directory(self, parent_frame, name, full_path, indent_level):
        """添加可展开/折叠的文件夹项"""
        # 创建子Frame来容纳文件夹内容（用于展开时添加内容）

        ContentFrame = tk.Frame(parent_frame)

        # self.Frames__.append(ContentFrame)
        
        # 文件夹图标和标签
        img = Image.open(os.path.join(folder, './Images/Dir.png'))
        
        img_tk = ImageTk.PhotoImage(img.resize((23, 23)))
        
        # 状态标志 (0: 关闭, 1: 打开)
        state = {'is_open': False, 
                'content_frame': ContentFrame,
                'img': img_tk}
        
        info_frame = tk.Frame(parent_frame)
        info_frame.grid(row=indent_level, column=10, sticky='w')

        # 切换按钮
        toggle_btn = tk.Button(info_frame, text='►', width=2, command=lambda: self._toggle_folder(state, full_path, indent_level+1))
        toggle_btn.pack(side=tk.LEFT)
        
        # 文件夹图标标签
        icon_label = tk.Label(info_frame, image=img_tk)
        icon_label.image = img_tk  # 保持引用
        icon_label.pack(side=tk.LEFT, padx=2)
        
        # 文件夹名称标签
        name_label = tk.Label(info_frame, text=name, fg="#579ADB", cursor="hand2")
        name_label.bind("<Button-1>", lambda e: self._toggle_folder(state, full_path, indent_level+1))
        name_label.pack(side=tk.LEFT)
        
        # 存储状态信息
        state['toggle_btn'] = toggle_btn

    def _add_file(self, parent_frame, name, full_path, parent_dir, indent_level):
        """添加文件项"""
        # 使用通用文件图标（或根据扩展名特殊处理）
        file_img = Image.open(os.path.join(folder, './Images/File.png'))
        if name.endswith('.ait'):
            file_img = Image.open(os.path.join(folder, './Images/aithonFile.png'))
        
        file_img_tk = ImageTk.PhotoImage(file_img.resize((23, 25)))
        
        info_frame = tk.Frame(parent_frame)
        info_frame.grid(row=indent_level, column=100)

        # 文件图标
        icon_label = tk.Label(info_frame, image=file_img_tk)
        icon_label.image = file_img_tk
        icon_label.pack(side=tk.LEFT)
        
        # 文件名称（可点击打开）
        if name.endswith('.ait'):
            btn = tk.Button(info_frame, text=name, fg="#4EC9B0", relief="flat", 
                            command=lambda p=full_path: self.OpenAithonFile(p))
            btn.pack(side=tk.LEFT, padx=2)
        else:
            label = tk.Label(info_frame, text=name, fg="#D4D4D4", relief="flat")
            label.pack(side=tk.LEFT, padx=2)

    def _toggle_folder(self, state, full_path, indent_level):
        """切换文件夹的展开/折叠状态"""
        if state['is_open']:
            # 折叠文件夹
            state['toggle_btn'].config(text='►')
            # state['icon_label'].config(image=state['closed_img'])
            # 隐藏内容
            for widget in state['content_frame'].winfo_children():
                widget.destroy()
            state['is_open'] = False
        else:
            # 展开文件夹
            state['toggle_btn'].config(text='▼')
            # state['icon_label'].config(image=state['open_img'])
            # 添加文件夹内容
            state['content_frame'].grid(row=2, column=0, sticky='nsew')  # 先显示再添加内容
            self.AddResourceManagerDir(full_path, state['content_frame'], indent_level)
            state['is_open'] = True

    def OpenAithonFile(self, File: str):
        self.add_editor_page()
        self.frames[-1][1].load_content(open(File, 'r', encoding='UTF-8').read())

    def TestCanConnectTheDatabase_(self):
        # 发送网络请求到 Github 私人仓库，如果请求速度超过2秒，视为网络连接失败
        import requests
        def check_repo(url: str):
            try: response = requests.get(url, timeout=2, verify=False); return response.status_code == 200
            except requests.exceptions.RequestException: return False
        repos = [
            'https://api.github.com/repos/sxxyrry/aithonPluginsDatabase',
            'https://api.github.com/repos/sxxyrry/aithon',
            'https://api.github.com/repos/sxxyrry/aithonDatabase'
        ]
        for repo in repos:
            if check_repo(repo): del requests; return True
        del requests; return False

    def TestCanConnectTheDatabase(self):
        if self.TestCanConnectTheDatabase_():
            self.Notice.EmitNotice(self.texts[44], self.texts[45])
        else: 
            self.Notice.EmitErrorNotice(self.texts[46], self.texts[47])

    def Introduction_Website(self):
        webbrowser.open('https://sxxyrry.github.io/aithon_Project/')

    def Restart(self):
        # os.startfile(os.path.join(folder, "./Editor.py"), show_cmd=1)
        # os._exit(0)
        global root
        self.root.destroy()
        root = tkt.Tk((1920, 1032), (0, 0), title=" aithon 编辑器")
        start()

    def switch_language(self):
        _ = tkt.Tk(title=self.texts[22])

        value = [
            "简体中文",
            "English"
        ]

        selected_value = tk.StringVar(_)
        value_: dict[str, str] = {
            "zh-cn" : "简体中文",
            "en" : "English"
        }
        value_a: dict[Literal['简体中文', 'English'], Literal['zh-cn', 'en']] = {j : i for i, j in value_.items()} # type: ignore
        selected_value.set(value_[self.config.language]) # 设置默认值
        a = tk.OptionMenu(_, selected_value, *value, command=lambda x: self.SwitchLanguage(value_a[str(x)])) # type: ignore
        a.pack()

    def SwitchLanguage(self, language: Literal['en', 'zh-cn']):
        self.config.SwitchLanguage(language)
        messagebox.showinfo(self.texts[16], self.texts[17]) # type: ignore

    def bind_shortcuts(self):
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-n>", lambda event: self.add_editor_page())
        self.root.bind("<Control-q>", lambda event: self.root.destroy())
        self.root.bind("<Control-S>", lambda event: self.save_all_files())

    def save_all_files(self):
        for _, (_, line) in enumerate(self.frames):
            file_path = filedialog.asksaveasfilename(title=self.texts[20],defaultextension='.XRthon', filetypes=[("XRthon Files", "*.XRthon")], initialdir=os.getcwd())
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(line.get_text())

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.style.configure("CustomNotebook", background="black", fieldbackground="black", foreground="black") # type: ignore
            self.style.map("CustomNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "black")]) # type: ignore
            for _, line in self.frames:
                line.config(bg="black", fg="white")
        else:
            self.theme = "light"
            self.style.configure("CustomNotebook", background="white", fieldbackground="white", foreground="black") # type: ignore
            self.style.map("CustomNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "white")]) # type: ignore
            for _, line in self.frames:
                line.config(bg="white", fg="black")

    def InstalledPluginsInterface(self):
        _ = tkt.Tk(title=self.texts[7])

        PluginsList: list[tuple[str, Literal['Enabled', 'Disabled'], Image.Image, str, str]] = GetInstalledPluginsList()

        for i in range(len(PluginsList)):
            img_ = PluginsList[i][2]

            img = ImageTk.PhotoImage(img_, master=_)

            f = tk.Frame(_)

            state_: str = PluginsList[i][1]

            state: str = self.texts[26] if state_ == 'Enabled' else self.texts[27]

            PluName = PluginsList[i][0]

            iLbl = tk.Label(f, text=f"{i + 1}")
            iLbl.grid(row=0, column=0)

            imgLbl = tk.Label(f, image=img)
            imgLbl.image = img # type: ignore
            imgLbl.grid(row=0, column=1, sticky='w')

            t = tk.Label(f, text=f"{self.texts[25]}: {PluName} ({state})")
            t.grid(row=0, column=2, sticky='w')

            UninstallBtn = tk.Button(f, text=self.texts[34], command=lambda PluName=PluName: self.UninstallPlugin(PluName))
            UninstallBtn.grid(row=0, column=3, sticky='w')

            UpdateBtn = tk.Button(f, text=self.texts[37], command=lambda PluName=PluName: self.UpdatePlugin(PluName))
            UpdateBtn.config(state='disabled')

            info = f'{PluginsList[i][3]}\n\n{PluginsList[i][4]}'

            InfoBtn = tk.Button(f, text=self.texts[49], command=lambda PluName=PluName, info=info: AddInfoPage(PluName, info))
            InfoBtn.grid(row=0, column=5, sticky='w')

            EODBtn = tk.Button(f, text=self.texts[27] if state_ == 'Enabled' else self.texts[26], command=lambda PluName=PluName, state=state_: self.EnableOrDisablePlugin(PluName, state_))
            EODBtn.grid(row=0, column=6, sticky='w')

            if JudgeVersion_Less_Plugin(
                PluName,
                GetVersion(
                    GetFileText(
                        token,
                        'sxxyrry',
                        'aithonPluginsDatabase',
                        f'plugins/{PluName}/{yaml.safe_load(
                            GetFileText(
                                token,
                                'sxxyrry',
                                'aithonPluginsDatabase',
                                f'plugins/{PluName}/config.json'
                            )
                        )['EditionLogsFilePath'][2::]}'
                    )
                )
            ):
                UpdateBtn.config(state='normal')

            UpdateBtn.grid(row=0, column=4, sticky='w')

            f.pack(fill='x')
        
        _.mainloop()

    def EnableOrDisablePlugin(self, PluName: str, state: str):
        path = os.path.join(PluginsPath, f'./{PluName}/config.json')
        with open(path, 'r', encoding='UTF-8') as file:
            config: dict[str, str] = json.load(file)
        
        if state == 'Enabled':
            config['state'] = 'Disabled'
        else:
            config['state'] = 'Enabled'
        
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(config, file)
        
        messagebox.showinfo(self.texts[16], self.texts[17]) # type: ignore

    def UninstallPlugin(self, PluName: str):
        if messagebox.askyesno(self.texts[34], self.texts[35].format(PluName)): # type: ignore

            UninstallPlugin(PluName)

            messagebox.showinfo(self.texts[34], self.texts[36]) # type: ignore

            messagebox.showinfo(self.texts[16], self.texts[17]) # type: ignore
        else:
            return

    def AllPluginsInterface(self):
        _ = tkt.Tk(title=self.texts[29])

        PluginsList: list[str] = GetAllPlugins()

        for i in range(len(PluginsList)):
            f = tk.Frame(_)

            PluName = PluginsList[i]

            _iLbl = tk.Label(f, text=f"{i + 1}")
            _iLbl.grid(row=0, column=0, sticky='w')

            t = tk.Label(f, text=f"{self.texts[25]}: {PluName}")
            t.grid(row=0, column=2, sticky='w')

            btn = tk.Button(f, text=self.texts[29], command=lambda PluName=PluName: self.InstallPlugin(PluName))

            config: dict[str, str] = json.loads(GetFileText(
                token,
                'sxxyrry',
                'aithonPluginsDatabase',
                f'plugins/{PluName}/config.json'
            ))

            IconFP = config['IconFilePath']

            IconFP = IconFP[2::] if IconFP[:2] == './' else IconFP

            IconLFP = os.path.join(TempPath, f'{IconFP}')

            DownloadFile(
                token,
                'sxxyrry',
                'aithonPluginsDatabase',
                f'plugins/{PluName}/{IconFP}',
                IconLFP
            )

            img = Image.open(IconLFP)
            img = img.resize((64, 64)) # type: ignore
            img = ImageTk.PhotoImage(img, master=_)

            ImgLbl = tk.Label(f, image=img)
            ImgLbl.image = img # type: ignore
            ImgLbl.grid(row=0, column=1, sticky='w')

            os.remove(IconLFP)

            info = f'{config['OverviewText']}\n\n{GetFileText(
                token,
                'sxxyrry',
                'aithonPluginsDatabase',
                f'plugins/{PluName}/{config['MarkdownFilePathForDescribingInformation']}'
            )}'

            InfoBtn = tk.Button(f, text=self.texts[49], command=lambda PluName=PluName, info=info: AddInfoPage(PluName, info))
            InfoBtn.grid(row=0, column=5, sticky='w')

            s = tk.Label(f, text=self.texts[32])

            if FindPlugin(PluName):
                btn.config(state='disabled')
            else:
                s.config(text=self.texts[33])
            
            s.grid(row=0, column=3, sticky='w')
            btn.grid(row=0, column=4, sticky='w')

            f.pack(fill='x')
        
        _.mainloop()

    def InstallPlugin(self, PluName: str):
        if messagebox.askyesno(self.texts[29], self.texts[30].format(PluName)): # type: ignore # type: ignore
            
            InstallPlugin(PluName)

            messagebox.showinfo(self.texts[29], self.texts[31]) # type: ignore

            messagebox.showinfo(self.texts[16], self.texts[17]) # type: ignore
        else:
            return

    def UpdatePlugin(self, PluName: str):
        if messagebox.askyesno(self.texts[37], self.texts[38].format(PluName)): # type: ignore
            
            UninstallPlugin(PluName)
            InstallPlugin(PluName)

            messagebox.showinfo(self.texts[37], self.texts[39]) # type: ignore

            messagebox.showinfo(self.texts[16], self.texts[17]) # type: ignore
        else:
            return

    def VersionInterface(self):
        _ = tkt.Tk(title=self.texts[14])

        lable = tk.Label(_, text=f'{self.texts[14]}: {version}')
        lable.pack()

        _.mainloop()
    
    def AboutInterface(self):
        _ = tkt.Tk(title=self.texts[5])

        text1 = tk.Label(_,
            text="这是由 23XR 工作室 提供的 aithon 编辑器。使用 GUN GPL v3.0 许可证。",
        )
        text1.pack(fill='x', side='left')
        _F = tk.Frame(_)
        _F.pack(fill='x')
        text2 = tk.Label(_F,
            text="赞助：",
        )
        text2.grid(row=0, column=0, sticky='w')
        text3 = tk.Label(_F,
            text="https://ifdian.net/order/create?plan_id=b2d954aa5c7711ef8af952540025c377&product_type=0&remark=&affiliate_code=",
            highlightbackground='black', relief='solid', fg='grey'
        )
        text3.grid(row=1, column=1, sticky='w')
        Copytext3Btb = tk.Button(_F,
            text="复制",
            command=lambda: pyperclip.copy("https://ifdian.net/order/create?plan_id=b2d954aa5c7711ef8af952540025c377&product_type=0&remark=&affiliate_code=")
        )
        Copytext3Btb.grid(row=1, column=2, sticky='w')

        _.mainloop()

    def AboutUsInterface(self):
        _ = tkt.Tk(title=self.texts[6])

        StudioFrame = tk.Frame(_)
        StudioFrame.pack(fill='x')

        StudioImgFrame = tk.Frame(StudioFrame)
        StudioImgFrame.grid(row=0, column=0)

        StudioImg = ImageTk.PhotoImage(Image.open(os.path.join(folder, "./Images/Sign_23XR_Bigger.png")).resize((66, 40)), master=_) # type: ignore
        StudioLbl = tk.Label(StudioImgFrame, image=StudioImg)
        StudioLbl.image = StudioImg # type: ignore
        StudioLbl.pack()

        StudioLblFrame = tk.Frame(StudioFrame)
        StudioLblFrame.grid(row=0, column=1, sticky='w')

        StudioNameLbl = tk.Label(StudioLblFrame, text="23XR 工作室 23XR Studio")
        StudioNameLbl.grid(row=0, column=0, sticky='w')

        StudioINCELbl = tk.Label(StudioLblFrame, text="什么都做的工作室（网站： https://sxxyrry.github.io ）【主要开发工作室】", highlightbackground='black', relief='solid', fg='grey')
        StudioINCELbl.grid(row=1, column=0, sticky='w')

        CopyWebsiteBtn = tk.Button(StudioLblFrame, text="复制网站", command=lambda: pyperclip.copy("https://sxxyrry.github.io"))
        CopyWebsiteBtn.grid(row=1, column=1, sticky='w')

        sxxyrryFrame = tk.Frame(_)
        sxxyrryFrame.pack(fill='x')

        sxxyrryImgFrame = tk.Frame(sxxyrryFrame)
        sxxyrryImgFrame.grid(row=0, column=0, sticky='w')

        sxxyrryImg = ImageTk.PhotoImage(Image.open(os.path.join(folder, "./Images/_23XRAvatar.png")).resize((round(85.4), 48)), master=_) # type: ignore
        sxxyrryLbl = tk.Label(sxxyrryImgFrame, image=sxxyrryImg)
        sxxyrryLbl.image = sxxyrryImg # type: ignore
        sxxyrryLbl.grid(row=0, column=0)

        sxxyrryLblFrame = tk.Frame(sxxyrryFrame)
        sxxyrryLblFrame.grid(row=0, column=1, sticky='w')

        sxxyrryNameLbl = tk.Label(sxxyrryLblFrame, text="23XR是星星与然然呀 23XR_sxxyrry")
        sxxyrryNameLbl.grid(row=0, column=0, sticky='w')

        sxxyrryINCELbl = tk.Label(sxxyrryLblFrame, text="23XR工作室室长【主要开发者】", highlightbackground='black', relief='solid', fg='grey')
        sxxyrryINCELbl.grid(row=1, column=0, sticky='w')

        _.mainloop()

    def EditionLogsInterface_English(self):
        _ = tkt.Tk(title=self.texts[13])

        t = scrolledtext.ScrolledText(_, width=100, height=20)
        t.insert(tk.END, English_Edition_logsForEditor)
        t.config(state='disabled')
        t.pack()

        _.mainloop()

    def EditionLogsInterface_Chinese(self):
        _ = tkt.Tk(title='版本记录')

        t = scrolledtext.ScrolledText(_, width=100, height=20)
        t.insert(tk.END, Chinese_Edition_logsForEditor)
        t.config(state='disabled')
        t.pack()

        _.mainloop()

    def open_file(self):
        _ = filedialog.askopenfiles(title=self.texts[21], filetypes=[('XRthon Files', '*.XRthon')], initialdir=os.getcwd())

        for i in _:
            self.add_editor_page()
            self.frames[self.frame_id][1].load_content(i.read())

    def save_file(self):
        _ = filedialog.asksaveasfile(title=self.texts[20], defaultextension='.XRthon', filetypes=[('XRthon Files', '*.XRthon')], initialdir=os.getcwd())
        if _:
            _.write(self.frames[self.Now_frame_id][1].get_text())

    def choose_file_and_run(self):
        self.open_file()
        self.RunCode()

    def RunCode(self):
        _ = self.frames[self.Now_frame_id][1].get_text()
        runner = Runner(f'temp_{self.Now_frame_id + 1}')
        Runner_log.info(f'\nStart Run temp_{self.Now_frame_id + 1}\n-----------------------')

        try:
            runner.run_manylines(_)
        except SystemExit:
            pass
        
        Runner_log.info(f'\n---------------------\nEnd Run temp_{self.Now_frame_id + 1}\n')

        runner.End()

    def OnCloseEditorPage(self, e: tk.Event): # type: ignore
        widget: tk.Frame = e.widget # type: ignore

        frames_ = [i[0] for i in self.frames]

        self.frames.remove(self.frames[frames_.index(widget)]) # type: ignore
        self.i -= 1
        self.frame_id -= 1

    def OnCloseInfoPage(self, e: tk.Event): # type: ignore
        widget: tk.Frame = e.widget # type: ignore

        self.framesInfo.remove(self.framesInfo[self.framesInfo.index(widget)]) # type: ignore

    def add_updater(self, frame: tk.Frame, line: Liner):
        try:
            self.Now_frame_id = self.frames.index((frame, line))
        except ValueError:
            self.Now_frame_id = self.frame_id

    def add_editor_page(self):
        frame = tk.Frame(self.root)
        line = Liner(frame)
        line.pack(fill="both", expand=True)
        self.frames.append((frame, line))
        frame.bind('<Visibility>', lambda event: self.add_updater(frame, line))
        frame.bind('<<NotebookTabClosed>>', self.OnCloseEditorPage) # type: ignore
        if self.i == 0:
            self.EditorNB.add(frame, text=f"aithon{self.texts[24]}")
            self.EditorNB.protect_tab(len(self.frames) - 1)
        else:
            self.EditorNB.add(frame, text=f"aithon{self.texts[24]} {self.i + 1}")
        
        self.MainNotebook.select(0) # type: ignore
        self.EditorNB.select(len(self.frames) - 1) # type: ignore
        
        self.frame_id = len(self.frames) - 1
        self.i += 1

        LoadPluginsAddContentMenu(line)
    
    def CheckUpdate(self):
        def StartCU():
            while True:
                ELForaithon = GetFileText(
                    token,
                    'sxxyrry',
                    'aithon',
                    '/codes/TextFIles/Edition_logs/Chinese/Edition_logsForaithon.txt'
                )

                Version_ = GetVersion(ELForaithon)

                ELForEditor = GetFileText(
                    token,
                    'sxxyrry',
                    'aithon',
                    '/codes/TextFIles/Edition_logs/Chinese/Edition_logsForEditor.txt'
                )

                Version__ = GetVersion(ELForEditor)

                if VersionSystem.JudgeVersion_Less(AithonVersion, Version_):
                    _ = tkt.Tk(title='aithon 新版本更新')

                    # 添加更新内容
                    msg = tk.Label(_, text=f"发现新版本: {Version_}\n当前版本: {AithonVersion}")
                    msg.pack(pady=10)

                    _.mainloop()
                
                if VersionSystem.JudgeVersion_Less(version, Version__):
                    _ = tkt.Tk(title='aithon 编辑器 新版本更新')

                    # 添加更新内容
                    msg = tk.Label(_, text=f"发现新版本: {Version__}\n当前版本: {version}")
                    msg.pack(pady=10)

                    _.mainloop()
                
                else:
                    break
        
        threading.Thread(target=StartCU).start()

            
    def update(self):
        try:
            if self.root.wm_state() == "iconic":
                pass
            if self.frame_id == -1:
                return
            if isinstance(self.frames[self.frame_id][1], Liner) and not isinstance(self.frames[self.frame_id][1], tk.Label):  # type: ignore
                self.frames[self.frame_id][1].redraw()
        except _tk.TclError:
            del___pycache__()
            quit()

    def pack(self):
        self.parent.pack(fill=tk.NONE, expand=True)

def start():
    global root, TextList  # 确保使用全局的 root 变量

    texts = []

    def _EN():
        texts = [
            'Start Screen',
            'We greatly appreciate your use of our program',
        ]
        return texts
    
    if config.language == 'en':
        texts = _EN()
    elif config.language == 'zh-cn':
        texts = [
            '启动界面',
            '我们非常欢迎您使用我们的程序',
        ]
    else:
        texts = _EN()

    IconPNG = ImageTk.PhotoImage(Image.open(os.path.join(folder, './Images/Icon_aithon_BIGGER.png')).resize((370, 70))) # type: ignore

    SignPNG = ImageTk.PhotoImage(Image.open(os.path.join(folder, './Images/Sign_23XR_Bigger.png')).resize((330, 180))) # type: ignore

    IconLbl = tk.Label(root, image=IconPNG)
    IconLbl.image = IconPNG # type: ignore
    IconLbl.pack()

    SignLbl = tk.Label(root, image=SignPNG)
    SignLbl.image = SignPNG # type: ignore
    SignLbl.pack()

    root.update()

    time.sleep(1)

    IconLbl.destroy()
    SignLbl.destroy()

    # gif = GifTkinter.AnimatedGif(root, os.path.join(folder, './Images/_23XRStudio.gif')) # type: ignore

    # gif.start()

    # gif.master.destroy()

    RegisterPlugins()
    TextList = LoadPluginModifyText()

    notice.pack()

    try:
        editor = Editor(TextList)
        editor.pack()

        editor.add_editor_page()

        AddInfoPage(texts[0], texts[1])

        if len(sys.argv) == 2:
            editor.frames[-1][1].load_content(open(sys.argv[1], 'r', encoding='UTF-8').read())

        root.update()
        editor.update()
        
        LoadPluginsNormal()

        try:
            while True:
                root.update()
                editor.update()
        except KeyboardInterrupt:
            del___pycache__()
    except Exception as e:
        raise e
        messagebox.showerror('Error', str(e)) # type: ignore
        pass

    del___pycache__()

def main():
    if len(sys.argv) == 1 or len(sys.argv) == 2:
        start()
    else:
        raise Exception('Invalid arguments')

if __name__ == '__main__':
    main()
