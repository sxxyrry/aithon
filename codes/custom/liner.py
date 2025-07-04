from collections.abc import Callable
from . import indrxer
import tkinter as tk
import tkinter.font as font
import re
import ast
# from types import NoneType
# from typing import Any, TypedDict

# 从运行器代码获取关键字、运算符和标点符号
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

linenum = 0

variable: list[str] = []

function: list[str] = []

class Liner(indrxer.IndexText):
    def __init__(self, parent: tk.Frame | tk.Toplevel, *args, **kwargs): # type: ignore
        super().__init__(parent, *args, **kwargs) # type: ignore
        self.breakpoints: set[int] = set()  # 初始化空集合用于存放断点行号
        self.y_scrollbar = tk.Scrollbar(parent)
        self.x_scrollbar = tk.Scrollbar(parent, orient='horizontal')
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.config(undo=True, xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set, wrap='none')
        self.x_scrollbar.config(command=self.xview) # type: ignore
        self.y_scrollbar.config(command=self.yview) # type: ignore
        self.font = self.settings.family
        self.font_size = self.settings.size
        self.numl = tk.Canvas(parent,
                              width=font.Font(root=parent, family=self.font, size=self.font_size).measure('0') + 5,
                              bg=self.bg, highlightthickness=0)
        self.numl.pack(side=tk.LEFT, fill=tk.BOTH)
        self.is_bold = self.settings.bold
        self.is_italic = self.settings.italic
        self.lineall = 0
        self._context_menus: dict[str, tuple[tk.Menu, str]] = {}  # 存储所有右键菜单 {menu_id: (menu_obj, creator_tag)}
        self._setup_default_context_menu()
        self.binds()
        self.focus_set()
        self.breakpoint_dot = {
            'size': 8,              # 更大的圆点
            'color': '#FF0000',     # 更亮的红色
            'offset': 5,            # 水平偏移
            'outline': '#880000'    # 深红色边框
        }
        
        # 初始化语法高亮标签
        self.tag_configure('variable', foreground='blue')
        self.tag_configure('function', foreground='yellow')
        self.tag_configure('keyword', foreground='orange')
        self.tag_configure('operator', foreground='purple')
        self.tag_configure('punctuation', foreground='gray')
        self.tag_configure('error', foreground='red', underline=True)
        
        # 绑定文本变化事件
        self.bind('<<Modified>>', self.on_content_changed)
        
        # 绑定鼠标悬停事件
        self.bind('<Motion>', self.on_mouse_move)
        self.bind('<Leave>', self.on_mouse_leave)
        self.tooltip = None

    def highlight_varAndFunc(self):
        """高亮变量和函数"""
        for i in variable:
            self.tag_add('variable', f'1.0 + {i}c', f'1.0 + {i}c + {len(i)}c')
        for i in function:
            self.tag_add('function', f'1.0 + {i}c', f'1.0 + {i}c + {len(i)}c')

    def on_content_changed(self, event=None):
        """文本内容变化时触发语法高亮和错误检查"""
        if self.edit_modified():
            self.highlight_syntax()
            self.check_errors()
            self.edit_modified(False)

    def highlight_syntax(self):
        """执行语法高亮"""
        self.tag_remove('variable', '1.0', tk.END)
        self.tag_remove('function', '1.0', tk.END)
        self.tag_remove('keyword', '1.0', tk.END)
        self.tag_remove('operator', '1.0', tk.END)
        self.tag_remove('punctuation', '1.0', tk.END)
        
        text = self.get('1.0', tk.END)
        
        # 匹配关键字
        for keyword in keys:
            pattern = rf'\b{re.escape(keyword)}\b'
            for match in re.finditer(pattern, text):
                start = f'1.0 + {match.start()}c'
                end = f'1.0 + {match.end()}c'
                self.tag_add('keyword', start, end)
        
        # 匹配运算符
        for operator in operators:
            pattern = re.escape(operator)
            for match in re.finditer(pattern, text):
                start = f'1.0 + {match.start()}c'
                end = f'1.0 + {match.end()}c'
                self.tag_add('operator', start, end)
        
        # 匹配标点符号
        for punct in punctuation:
            pattern = re.escape(punct)
            for match in re.finditer(pattern, text):
                start = f'1.0 + {match.start()}c'
                end = f'1.0 + {match.end()}c'
                self.tag_add('punctuation', start, end)
        
        # 匹配变量
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', text):
            start = f'1.0 + {match.start(1)}c'
            end = f'1.0 + {match.end(1)}c'
            self.tag_add('variable', start, end)
            variable.append(match.group(1))
        
        # 匹配函数名
        for match in re.finditer(r'def_func\s+([a-zA-Z_][a-zA-Z0-9_]*)', text):
            start = f'1.0 + {match.start(1)}c'
            end = f'1.0 + {match.end(1)}c'
            self.tag_add('function', start, end)
            function.append(match.group(1))

    def check_errors(self):
        """检查代码错误"""
        self.tag_remove('error', '1.0', tk.END)
        text = self.get('1.0', tk.END)
        try:
            ast.parse(text)
        except SyntaxError as e:
            line = e.lineno
            column = e.offset
            start = f'{line}.{column - 1}'
            end = f'{line}.{column}'
            # 若：不符合 AITN 规范，添加错误标记
            self.tag_add('error', start, end)

    def on_mouse_move(self, event):
        """鼠标移动时显示提示信息"""
        index = self.index(f'@{event.x},{event.y}')
        word = self.get(f'{index} wordstart', f'{index} wordend')
        if word:
            # 简单示例：显示变量名作为类型提示
            tooltip_text = f'Type: {word}'
            self.show_tooltip(event.x_root, event.y_root, tooltip_text)

    def show_tooltip(self, x, y, text):
        """显示提示框"""
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{x}+{y}')
        label = tk.Label(self.tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1)
        label.pack()

    def on_mouse_leave(self, event):
        """鼠标离开时隐藏提示框"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def _setup_default_context_menu(self):
        """初始化默认右键菜单"""
        menu_id = "default"
        self._context_menus[menu_id] = (tk.Menu(self, tearoff=0), "system")
        
        # # 添加默认菜单项
        # self._context_menus[menu_id][0].add_command(
        #     label="设置断点", 
        #     command=lambda: self.set_breakpoint(self.get_lineno_at_cursor())
        # )
        # self._context_menus[menu_id][0].add_command(
        #     label="删除断点", 
        #     command=lambda: self._remove_breakpoint_if_owned(self.get_lineno_at_cursor())
        # )
        # self._context_menus[menu_id][0].add_separator()
        # self._context_menus[menu_id][0].add_command(
        #     label="清空所有断点", 
        #     command=self._clear_all_breakpoints
        # )


    def _remove_breakpoint_if_owned(self, line_number: int):
        """仅删除当前行存在的断点"""
        if line_number in self.breakpoints:
            self.remove_breakpoint(line_number)
            self.redraw()

    def _clear_all_breakpoints(self):
        """清空所有断点"""
        self.breakpoints.clear()
        self.redraw()

    def _show_context_menu(self, event: tk.Event): # type: ignore
        """右键菜单显示方法"""
        # 创建主菜单
        context_menu = tk.Menu(self, tearoff=0)
        
        # 添加所有菜单项
        for menu_id, (menu, _) in self._context_menus.items(): # type: ignore
            index = menu.index(tk.END)
            if index is None:
                index = -1
            for i in range(index + 1):  # 遍历所有菜单项 # type: ignore
                # item_text = menu.entrycget(i, 'label')
                item_type = menu.type(i)
                if item_type == 'separator':
                    context_menu.add_separator()
                elif item_type == 'command':
                    context_menu.add_command(
                        label=menu.entrycget(i, 'label'),
                        command=menu.entrycget(i, 'command')
                    )
        
        # 显示菜单
        context_menu.tk_popup(event.x_root, event.y_root) # type: ignore
        
        # 关键修复：确保菜单保持显示
        def on_menu_close():
            context_menu.grab_release()
            context_menu.destroy()
        
        context_menu.bind("<Unmap>", lambda e: self.after(100, on_menu_close))

    # ---- 外部可调用的菜单管理接口 ----
    def add_context_menu(self, label: str, command: Callable[..., None], creator_tag: str = "external"):
        """添加新的右键菜单项"""
        menu_id = f"menu_{len(self._context_menus)}"
        new_menu = tk.Menu(self, tearoff=0)
        new_menu.add_command(label=label, command=command)
        self._context_menus[menu_id] = (new_menu, creator_tag)
        return menu_id  # 返回菜单ID用于后续管理

    def remove_context_menu(self, menu_id: str, creator_tag: str):
        """删除指定的右键菜单项"""
        if menu_id in self._context_menus and self._context_menus[menu_id][1] == creator_tag:
            self._context_menus.pop(menu_id)

    def update_context_menu(self,
                            menu_id: str,
                            new_label: str | None = None,
                            new_command: Callable[..., None] | None = None,
                            creator_tag: str | None = None):
        """修改已有的右键菜单项"""
        if menu_id in self._context_menus and (creator_tag is None or self._context_menus[menu_id][1] == creator_tag):
            menu, tag = self._context_menus[menu_id] # type: ignore
            if new_label:
                menu.entryconfig(0, label=new_label)
            if new_command:
                menu.entryconfig(0, command=new_command)
            if creator_tag:
                self._context_menus[menu_id] = (menu, creator_tag)

    def binds(self):
        self.bind("<Button-3>", self._show_context_menu, add='+') # type: ignore
        self.bind("<Button-2>", self._show_context_menu, add='+') # type: ignore
        self.bind("<Key>", lambda event: self._see())
        self.bind("<Button-1>", lambda event: self._see())
        self.bind("<B2-Motion>", lambda event: self._see())
        self.bind("<MouseWheel>", lambda event: self._see())
        self.bind("<Control-b>", self.toggle_breakpoint)  # type: ignore # 添加断点快捷键

    def toggle_breakpoint(self, event=None): # type: ignore
        line_number = self.get_lineno_at_cursor()
        if line_number in self.breakpoints:
            self.remove_breakpoint(line_number)
        else:
            self.set_breakpoint(line_number)
        self.redraw()

    def _see(self):
        self.see(str(float(int(float(self.index('insert'))) + 2)))  # 一直显示光标所在行

    def update_fonts(self):
        self.config(font=(
            self.font, self.font_size, 'bold' if self.is_bold else 'normal', 'italic' if self.is_italic else 'roman'
            ) # type: ignore
        )

    def redraw(self):
        self.update_fonts()
        try:
            global linenum
            self.numl.delete("all")
            i = self.index("@0,0")
            while True:
                dline = self.dlineinfo(i)
                if dline is None:
                    break
                    
                # 获取行号和位置信息
                y = dline[1]
                line_height = dline[3]  # 行高度
                linenum = str(i).split(".")[0]
                line_num = int(linenum)  # 当前行号(从1开始)
                
                # 计算文本和圆点的位置
                text_x = 15  # 文本向右偏移，给圆点留空间
                text_y = y + (line_height - self.font_size) // 2  # 垂直居中
                
                # 先绘制红色圆点(如果是断点行)
                if (line_num - 1) in self.breakpoints:  # 注意这里减1，因为breakpoints存储的是0-based索引
                    dot_x = 5
                    dot_y = y + line_height // 2  # 圆点垂直居中
                    dot_size = self.breakpoint_dot['size']
                    self.numl.create_oval(dot_x, dot_y - dot_size//2,  # type: ignore
                                        dot_x + dot_size, dot_y + dot_size//2, # type: ignore
                                        fill=self.breakpoint_dot['color'],  # type: ignore
                                        outline=self.breakpoint_dot['color']) # type: ignore
                
                # 绘制行号文本
                self.numl.create_text(text_x, text_y, anchor="nw", text=linenum, 
                                    fill=self.line,
                                    font=(self.font, self.font_size, 
                                         'bold' if self.is_bold else 'normal',
                                         'italic' if self.is_italic else 'roman'))
                
                i = self.index("%s+1line" % i)

            # 调整左侧区域宽度
            _font = font.Font(root=self.master, family=self.font, size=self.font_size)
            max_width = max(_font.measure(str(n)) for n in range(1, int(self.lineall or 1) + 1))
            self.numl.config(width=max_width + 30)  # 额外空间给圆点和边距
        except RuntimeError:
            pass

    def load_content(self, content: str):
        self.delete("1.0", "end")  # 删除已有内容
        self.insert("1.0", content)  # 插入新内容

    def get_text(self):
        _ = self.get("1.0", tk.END).split('\n')
        print(_)
        _.pop()
        print(_)
        print(f"{'\n'.join(_)=}")
        return '\n'.join(_)

    def set_breakpoint(self, line_number: int):
        self.breakpoints.add(line_number)

    def remove_breakpoint(self, line_number: int):
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
    
    def get_lineno_at_cursor(self):
        index = self.index("insert")
        return int(index.split('.')[0]) - 1  # 减一是因为Tkinter的行索引从1开始


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", 1) # type: ignore
    text = Liner(root) # type: ignore
    text.pack(fill="both", expand=1)
    while True:  # use this instead of mainloop
        text.redraw()
        root.update()