import re
from typing import List, Optional, Callable, TypeVar
import itertools


JsonNode = TypeVar('JsonNode', int, float, str, dict, list)


class JsonQueryResult:
    def __init__(self, elements: List['JsonQuery']) -> None:
        self._elements = elements

    def find(self, pattern: str) -> 'JsonQueryResult':
        return JsonQueryResult(list(itertools.chain.from_iterable([element.find(pattern)._elements for element in self._elements])))

    def equals(self, pattern: str) -> 'JsonQueryResult':
        return JsonQueryResult(list(itertools.chain.from_iterable([element.equals(pattern)._elements for element in self._elements])))

    def startswith(self, pattern: str) -> 'JsonQueryResult':
        return JsonQueryResult(list(itertools.chain.from_iterable([element.startswith(pattern)._elements for element in self._elements])))

    @property
    def value(self) -> List[JsonNode]:
        return [element.value for element in self._elements]

    @value.setter
    def value(self, value: JsonNode):
        for element in self._elements:
            element.value = value

    @property
    def first(self) -> 'JsonQuery':
        return self._elements[0]

    def __iter__(self):
        for element in self._elements:
            yield element

        raise StopIteration()

    def __len__(self) -> int:
        return len(self._elements)


class JsonQuery:
    def __init__(self, node: JsonNode, path: str = '', full_path: str = '', root: Optional[JsonNode] = None, delimiter: str = '.') -> None:
        self._node = node
        self._path = path
        self._root = root if root else self._node
        self._full_path = full_path
        self._delimiter = delimiter

    def find(self, pattern: str) -> JsonQueryResult:
        reg = re.compile(pattern)
        return self._find(lambda path: reg.search(path))

    def equals(self, pattern: str) -> JsonQueryResult:
        return self._find(lambda path: path == pattern)

    def startswith(self, pattern: str) -> JsonQueryResult:
        return self._find(lambda path: path.startswith(pattern))

    def _find(self, tester: Callable) -> JsonQueryResult:
        elements = self._parse(self._root, self._full_path)
        return JsonQueryResult([element for element in elements if tester(element._path)])

    @property
    def value(self) -> JsonNode:
        return self._pluck(self._root, self._full_path)

    @value.setter
    def value(self, value: JsonNode):
        self._infuse(self._root, self._full_path, value)

    def _parse(self, root: JsonNode, full_path: str) -> List['JsonQuery']:
        parent_node = self._pluck(root, full_path) if full_path else root
        elements: List[JsonQuery] = []
        for path in self._pathfy(parent_node, ''):
            node_of_full_path = f'{full_path}{self._delimiter}{path}' if full_path else path
            node = self._pluck(root, node_of_full_path)
            elements.append(JsonQuery(node, root=root, path=path, full_path=node_of_full_path, delimiter=self._delimiter))

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
