import re
from typing import List, TypeVar


JsonNode = TypeVar('JsonNode', int, float, str, dict, list)


class JsonQuery:
    def __init__(self, root: JsonNode, path: str = '') -> None:
        self._root = root
        self._path = path

    def find(self, pattern: str) -> List['JsonQuery']:
        reg = re.compile(pattern)
        elements = self._parse(self._root, self._path)
        return [element for element in elements if reg.search(element._path)]

    def below(self, pattern: str) -> List['JsonQuery']:
        reg = re.compile(pattern)
        elements = self._parse(self._root, self._path)
        sub_reg = re.compile('^' + self._path.replace(".", "\\.") + '\\.')
        return [element for element in elements if reg.search(sub_reg.sub('', element._path))]

    @property
    def value(self) -> JsonNode:
        return self._pluck(self._root, self._path)

    @value.setter
    def value(self, value: JsonNode):
        self._infuse(self._root, self._path, value)

    def _parse(self, root: JsonNode, path: str) -> List['JsonQuery']:
        node = self._pluck(root, path) if path else root
        return [JsonQuery(root, fullpath) for fullpath in self._fullpathfy(node, path)]

    def _fullpathfy(self, node: JsonNode, fullpath: str) -> List[str]:
        in_paths: List[str] = []
        if fullpath:
            in_paths.append(fullpath)

        if type(node) is dict:
            for key in node.keys():
                in_paths.extend(self._fullpathfy(node[key], f'{fullpath}.{key}' if fullpath else key))
        elif type(node) is list:
            for index in range(len(node)):
                in_paths.extend(self._fullpathfy(node[index], f'{fullpath}.{index}' if fullpath else str(index)))

        return in_paths

    def _pluck(self, node: JsonNode, path: str) -> JsonNode:
        routes = path.split('.')
        if type(node) is dict and path:
            key = routes[0]
            return self._pluck(node[key], '.'.join(routes[1:]))
        elif type(node) is list and path:
            index = int(routes[0])
            return self._pluck(node[index], '.'.join(routes[1:]))
        else:
            return node

    def _infuse(self, node: JsonNode, path: str, value: JsonNode):
        routes = path.split('.')
        key = routes[0]
        remain_path = '.'.join(routes[1:])
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
