import os
from .folder import folder


with open(os.path.join(folder, './TextFIles/Edition_logs/English/Edition_logsForaithon.txt'), 'r', encoding='UTF-8') as f:
    English_Edition_logsForaithon: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/English/Edition_logsForEditor.txt'), 'r', encoding='UTF-8') as f:
    English_Edition_logsForEditor: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/Chinese/Edition_logsForaithon.txt'), 'r', encoding='UTF-8') as f:
    Chinese_Edition_logsForaithon: str = f.read()

with open(os.path.join(folder, './TextFIles/Edition_logs/Chinese/Edition_logsForEditor.txt'), 'r', encoding='UTF-8') as f:
    Chinese_Edition_logsForEditor: str = f.read()
