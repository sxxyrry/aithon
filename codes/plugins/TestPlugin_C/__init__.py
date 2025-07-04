from ...PluginAPI import (
    root, # type: ignore
    frames, # type: ignore
    parent, # type: ignore
    Up,
    Bottom, # type: ignore
    tk,
    JudgeVersion_Equal_Plugin, # type: ignore
    JudgeVersion_Greater_Plugin, # type: ignore
    JudgeVersion_Less_Plugin, # type: ignore
    FindPlugin, # type: ignore
    ImportPlugin, # type: ignore
    GetVersionForEditionLogs_Plugin, # type: ignore
    PluginAddContentMenuBaseClass,
    frames,
    Liner,
)


class Plugin_(metaclass=PluginAddContentMenuBaseClass):
    @staticmethod
    def CallBack(liner: Liner):
        menu_id = liner.add_context_menu('c', lambda: print('a'))
        # print(menu_id)
        
