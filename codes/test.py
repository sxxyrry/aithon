from lark import Lark, Transformer, Token

# 定义语法
grammar = """\
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /\\d+(\\.\\d+)?/
STRING: /"[^"\\\\]*(\\\\.[^"\\\\]*)*"/ | /'[^'\\\\]*(\\\\.[^'\\\\]*)*'/ 
WS: /[ \\t\\f\\r\\n]+/
%ignore WS

LPAREN: "("
RPAREN: ")"
LBRACE: "{"
RBRACE: "}"
COLON: ":"
EQUAL: "="
PLUS: "+"
MINUS: "-"
STAR: "*"
SLASH: "/"
POWER: "**"

?start: statements

statements: statement*

statement: def_func
         | if_statement
         | import_statement
         | simple_statement

def_func: "def_func" NAME LBRACE NAME RBRACE COLON simple_statement

if_statement: "if" LBRACE expr RBRACE COLON block
              | "elif" LBRACE expr RBRACE COLON block
              | "else" COLON block

import_statement: "import" LPAREN NAME RPAREN

dotted_name: NAME ("." NAME)*

block: statement*

while_statement: "while" LBRACE expr RBRACE COLON block

simple_statement: NAME EQUAL expr
                | function_call
                | "print" LPAREN expr RPAREN
                | "while" LBRACE expr RBRACE COLON block

function_call: NAME LPAREN (expr ("," expr)*)? RPAREN

expr: NUMBER
    | STRING
    | dotted_name
    | function_call
    | expr PLUS expr
    | expr MINUS expr
    | expr STAR expr
    | expr SLASH expr
    | expr POWER expr
    | LPAREN expr RPAREN
"""

# 定义转换器
class CustomTransformer(Transformer):
    def def_func(self, items):
        if len(items) == 6:  # 修改判断条件以支持大括号语法
            name, arg, block = items[1], items[3], items[5]
            return {"type": "def_func", "name": name, "arg": arg, "block": [block]}
        elif len(items) == 5:
            name, block = items[1], items[4]
            return {"type": "def_func", "name": name, "arg": None, "block": [block]}  # 新增对无参数函数的支持
        else:
            raise ValueError(f"Unexpected items in def_func: {items}")

    def if_statement(self, items):
        conditions = []
        blocks = []
        else_block = None
        i = 0
        while i < len(items):
            if isinstance(items[i], Token) and items[i].type == "LBRACE":
                i += 1  # 跳过 '{'
                continue
            if isinstance(items[i], Token) and items[i].type == "RBRACE":
                i += 1  # 跳过 '}'
                continue
            if isinstance(items[i], Token) and items[i].type == "if":
                conditions.append(items[i + 1])  # expr
                blocks.append(items[i + 6])      # block
                i += 7
            elif isinstance(items[i], Token) and items[i].type == "elif":
                conditions.append(items[i + 1])  # expr
                blocks.append(items[i + 6])      # block
                i += 7
            elif isinstance(items[i], Token) and items[i].type == "else":
                else_block = items[i + 3]        # block
                i += 4
            else:
                i += 1
        return {"type": "if_statement", "conditions": conditions, "blocks": blocks, "else_block": else_block}

    def while_statement(self, items):
        return {"type": "while_statement", "condition": items[1], "block": items[3]}

    def import_statement(self, items):
        return {"type": "import_statement", "module": items[0]}

    def dotted_name(self, items):
        return {"type": "dotted_name", "names": items}

    def block(self, items):
        return items

    def simple_statement(self, items):
        if len(items) == 3 and isinstance(items[0], str) and isinstance(items[1], Token) and items[1].type == "EQUAL":
            return {"type": "assignment", "name": items[0], "value": items[2]}
        return {"type": "simple_statement", "items": items}

    def function_call(self, items):
        name = items[0]
        args = [item for item in items[2:-1] if not isinstance(item, Token)]  # 过滤掉 Token
        return {"type": "function_call", "name": name, "args": args}

    def expr(self, items):
        if len(items) == 1:
            return items[0]
        return {"type": "expr", "items": [item for item in items if not isinstance(item, Token)]}  # 过滤掉 Token

    def NAME(self, token):
        return token.value

    def NUMBER(self, token):
        return float(token.value)  # 支持浮点数

    def STRING(self, token):
        return token.value[1:-1]  # 去掉字符串两边的引号

# 创建解析器
parser = Lark(grammar, parser='lalr', transformer=CustomTransformer())

# 读取文件内容
# with open("./test.ait", 'r') as file:
#     code = file.read()

code = """
a = "a"
b = "b"
c = 1 + 2 * (3 + 4)
d = 1 + 2 * (3 + 4)
e = 2 ** 3 + 1
f = 2 ** 3 + 1
g = 2.0 ** 3 + 1
h = print
i = print("Hello World")

def_func func{arg}:
    print(arg)

if {1}:
    print("1")
elif {2}:
    print("2")
else:
    print("3")

while {1}:
    print("1")
"""

# 解析代码
parsed_code = parser.parse(code)
print(parsed_code)
