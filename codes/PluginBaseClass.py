from abc import ABCMeta
# from 
from typing import Any

def abstractstaticmethod(func): # type: ignore
    func.__isabstractmethod__ = True # type: ignore
    return staticmethod(func) # type: ignore

class PluginBaseClass(type, metaclass=ABCMeta):
    Register: list[type] = []

    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any] | None) -> Any:
        # 检查子类是否实现了 UsePlugin 方法
        if attrs is None:
            attrs = {}
        if 'UsePlugin' not in attrs:
            raise TypeError(f"Class {name} must implement the 'UsePlugin' method")
        
        # 创建类实例，避免递归调用
        new_cls = super().__new__(cls, name, bases, attrs)
        PluginModifyTextBaseClass.Register.append(new_cls)
        return new_cls

    @abstractstaticmethod
    def UsePlugin() -> Any:
        raise NotImplementedError

class PluginModifyTextBaseClass(type, metaclass=ABCMeta):
    Register: list[type] = []

    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any] | None) -> Any:
        # 检查子类是否实现了 UsePlugin 方法
        if attrs is None:
            attrs = {}
        if 'UsePlugin' not in attrs:
            raise TypeError(f"Class {name} must implement the 'UsePlugin' method")
        
        # 创建类实例，避免递归调用
        new_cls = super().__new__(cls, name, bases, attrs)
        PluginModifyTextBaseClass.Register.append(new_cls)
        return new_cls

    @abstractstaticmethod
    def UsePlugin() -> Any:
        raise NotImplementedError

class PluginNormalBaseClass(type, metaclass=ABCMeta):
    Register: list[type] = []

    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any] | None) -> Any:
        # 检查子类是否实现了 UsePlugin 方法
        if attrs is None:
            attrs = {}
        if 'UsePlugin' not in attrs:
            raise TypeError(f"Class {name} must implement the 'UsePlugin' method")
        
        # 创建类实例，避免递归调用
        new_cls = super().__new__(cls, name, bases, attrs)
        PluginModifyTextBaseClass.Register.append(new_cls)
        return new_cls

    @abstractstaticmethod
    def UsePlugin() -> Any:
        raise NotImplementedError
