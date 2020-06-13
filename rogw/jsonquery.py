import re
from typing import List, Optional, Callable, TypeVar
import itertools


flatten = itertools.chain.from_iterable
JsonNode = TypeVar('JsonNode', int, float, str, dict, list)


class JsonQueryElement:
    def __init__(self, node: JsonNode, path: str = '', full_path: str = '', root: Optional[JsonNode] = None, delimiter: str = '.') -> None:
        self._node = node
        self._path = path
        self._root = root if root else self._node
        self._full_path = full_path
        self._delimiter = delimiter

    def all(self) -> List['JsonQueryElement']:
        return self._find(lambda elem: True)

    def search(self, pattern: str) -> List['JsonQueryElement']:
        reg = re.compile(pattern)
        return self._find(lambda elem: reg.search(elem._path))

    def equals(self, pattern: str) -> List['JsonQueryElement']:
        return self._find(lambda elem: elem._path == pattern)

    def startswith(self, pattern: str) -> List['JsonQueryElement']:
        return self._find(lambda elem: elem._path.startswith(pattern))

    def leaf(self) -> List['JsonQueryElement']:
        return self._find(lambda elem: type(elem.value) not in [dict, list])

    def _find(self, tester: Callable) -> List['JsonQueryElement']:
        elements = self._parse(self._root, self._full_path)
        return [element for element in elements if tester(element)]

    @property
    def full_path(self) -> str:
        return self._full_path

    @property
    def value(self) -> JsonNode:
        return self._pluck(self._root, self._full_path)

    @value.setter
    def value(self, value: JsonNode):
        self._infuse(self._root, self._full_path, value)

    @property
    def text(self) -> str:
        return str(self.value)

    def _parse(self, root: JsonNode, full_path: str) -> List['JsonQueryElement']:
        parent_node = self._pluck(root, full_path) if full_path else root
        elements: List[JsonQueryElement] = []
        for path in self._pathfy(parent_node, ''):
            node_of_full_path = f'{full_path}{self._delimiter}{path}' if full_path else path
            node = self._pluck(root, node_of_full_path)
            elements.append(JsonQueryElement(node, root=root, path=path, full_path=node_of_full_path, delimiter=self._delimiter))

        return elements

    def _pathfy(self, node: JsonNode, path: str) -> List[str]:
        in_paths: List[str] = []
        if path:
            in_paths.append(path)

        if type(node) is dict:
            for key in node.keys():
                in_paths.extend(self._pathfy(node[key], f'{path}{self._delimiter}{key}' if path else key))
        elif type(node) is list:
            for index in range(len(node)):
                in_paths.extend(self._pathfy(node[index], f'{path}{self._delimiter}{index}' if path else str(index)))

        return in_paths

    def _pluck(self, node: JsonNode, path: str) -> JsonNode:
        if type(node) is dict and path:
            key, *remain = path.split(self._delimiter)
            return self._pluck(node[key], self._delimiter.join(remain))
        elif type(node) is list and path:
            key, *remain = path.split(self._delimiter)
            index = int(key)
            return self._pluck(node[index], self._delimiter.join(remain))
        else:
            return node

    def _infuse(self, node: JsonNode, path: str, value: JsonNode):
        key, *remain = path.split(self._delimiter)
        remain_path = self._delimiter.join(remain)
        if type(node) is dict:
            if type(node[key]) is dict:
                self._infuse(node[key], remain_path, value)
            elif type(node[key]) is list:
                self._infuse(node[key], remain_path, value)
            else:
                node[key] = value
        elif type(node) is list:
            index = int(key)
            if type(node[index]) is dict:
                self._infuse(node[index], remain_path, value)
            elif type(node[index]) is list:
                self._infuse(node[index], remain_path, value)
            else:
                node[index] = value


class JsonQuery:
    def __init__(self, node: JsonNode, delimiter: str = '.') -> None:
        self._root_elem = JsonQueryElement(node, delimiter=delimiter)
        self._elements: List[JsonQueryElement] = []

    def all(self) -> 'JsonQuery':
        return self._invoke('all')

    def search(self, pattern: str) -> 'JsonQuery':
        return self._invoke('search', pattern)

    def equals(self, pattern: str) -> 'JsonQuery':
        return self._invoke('equals', pattern)

    def startswith(self, pattern: str) -> 'JsonQuery':
        return self._invoke('startswith', pattern)

    def leaf(self) -> 'JsonQuery':
        return self._invoke('leaf')

    def _invoke(self, method: str, *args) -> 'JsonQuery':
        jq = JsonQuery(self._root_elem._node, delimiter=self._root_elem._delimiter)
        jq._elements = list(flatten([getattr(element, method)(*args) for element in self._elements])) if self._elements else getattr(self._root_elem, method)(*args)
        return jq

    @property
    def full_path(self) -> List[str]:
        return [element.full_path for element in self._elements]

    @property
    def value(self) -> List[JsonNode]:
        return [element.value for element in self._elements]

    @value.setter
    def value(self, value: JsonNode):
        for element in self._elements:
            element.value = value

    @property
    def text(self) -> str:
        return ''.join(map(str, self.value))

    @property
    def first(self) -> JsonQueryElement:
        return self._elements[0]

    def __iter__(self):
        for element in self._elements:
            yield element

        return

    def __len__(self) -> int:
        return len(self._elements)
