from typing import Any, Generic, TypeVar, overload, Iterable, Iterator

T = TypeVar('T')

class Toolslist(Generic[T]):
    """自定义列表类，完美替代内置list"""
    def __init__(self, iterable: Iterable[T] = None):
        self._data: list[T] | list[Any] = [] if iterable is None else list(iterable) # type: ignore
    
    def append_more(self, *items: T) -> None:
        """批量添加元素"""
        for item in items:
            self._data.append(item)
    
    # 实现内置list的所有必要方法
    def append(self, item: T) -> None:
        self._data.append(item)
    
    def extend(self, iterable: Iterable[T]) -> None:
        self._data.extend(iterable)
    
    def __getitem__(self, index: int) -> T:
        return self._data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)
    
    def __repr__(self) -> str:
        return repr(self._data)
    
    # 添加其他必要方法...
    def insert(self, index: int, item: T) -> None:
        self._data.insert(index, item)
    
    def remove(self, item: T) -> None:
        self._data.remove(item)
    
    def pop(self, index: int = -1) -> T:
        return self._data.pop(index)
    
    def clear(self) -> None:
        self._data.clear()
    
    def index(self, item: T, start: int = 0, end: int = None) -> int:
        return self._data.index(item, start, end or len(self._data))
    
    def count(self, item: T) -> int:
        return self._data.count(item)
    
    def sort(self, *, key=None, reverse=False) -> None:
        self._data.sort(key=key, reverse=reverse)
    
    def reverse(self) -> None:
        self._data.reverse()
    
    def copy(self) -> 'list[T]':
        return list(self._data)

# class Toolsdict():
    
