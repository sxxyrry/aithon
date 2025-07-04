from .Edition_logs import Chinese_Edition_logsForaithon, Chinese_Edition_logsForEditor


def GetVersionForaithon():
    version = ''

    for _ in Chinese_Edition_logsForaithon.split('\n'):
        if _.endswith(' 版本：'):
            version: str = _[:-4]
        elif _.endswith(' 版本：\r'):
            version: str = _[:-5]
    
    return version

def GetVersionForEditor():
    version = ''

    for _ in Chinese_Edition_logsForEditor.split('\n'):
        if _.endswith(' 版本：'):
            version: str = _[:-4]
        elif _.endswith(' 版本：\r'):
            version: str = _[:-5]
    
    return version

def GetVersion(EditionLogs: str) -> str:
    version = ''

    for _ in EditionLogs.split('\n'):
        if _.endswith(' 版本：'):
            version: str = _[:-4]
        elif _.endswith(' 版本：\r'):
            version: str = _[:-5]
    
    return version
