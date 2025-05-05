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
    PluginNormalBaseClass,
)


class Plugin_(metaclass=PluginNormalBaseClass):
    @staticmethod
    def UsePlugin():
        _ = tk.Menu()
        _.add_command(label="b", command=lambda: print("b"))
        Up.add_cascade(label="b", menu=_)
