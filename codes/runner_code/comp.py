import py_compile, os

# with open('./Runner.py', 'r') as f:
#     text = f.read()
#     text.replace('folder = pathlib.Path(__file__).parent.parent.resolve()', 'folder = pathlib.Path(__file__).parent.resolve()')

# with open('./Runner_.py', 'w') as f:
#     f.write(text)

_ = py_compile.compile('./Runner.py')
print(_)

# os.remove('./Runner_.py')