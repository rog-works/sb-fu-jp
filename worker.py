import re
from copy import deepcopy
from typing import List, Tuple
from dataclasses import dataclass
from translator import Promise


@dataclass
class Control:
    code: str
    org_words: str


class Worker:
    def __init__(self, data: dict) -> None:
        self._data = data
        self._result = deepcopy(data)
        self._contexts: List[self.Context] = []

    def prepare(self, json_path: str) -> Tuple[str, List[Control]]:
        org_text, controls = self.parse(json_path)
        pre_text = org_text
        for index, control in enumerate(controls):
            pattern = re.compile('\\^' + control.code + ';([^^]+)\\^reset;')
            replace = '${' + control.code + str(index) + '}' + control.org_words + '${reset}'
            pre_text = re.sub(pattern, replace, pre_text)

        return pre_text, controls

    def post(self, json_path: str, controls: List[Control], trans_text: str):
        post_text = trans_text
        for index, control in enumerate(controls):
            pattern = re.compile('\\$\\s*{' + control.code + str(index) + '}\\s*([^$]+)\\s*\\$\\s*{reset}')
            replace = f'^{control.code};\\1 (org: {control.org_words})^reset;'
            post_text = re.sub(pattern, replace, post_text)

        return post_text

    def parse(self, json_path: str) -> Tuple[str, List[Control]]:
        org_text = self.extract(json_path)
        return org_text, self.controls(org_text)

    def extract(self, json_path: str) -> str:
        return self._data[json_path]

    def infuse(self, json_path: str, post_text: str):
        self._result[json_path] = post_text

    def controls(self, org_text: str) -> List[Control]:
        matches = re.finditer(r'\^([a-z]+);([^\^]+)\^reset;', org_text)
        controls = []
        for match in matches:
            code, org_words = match.group(1, 2)
            controls.append(Control(code, org_words))

        return controls

    def context(self, json_path: str, controls: List[Control], promise: Promise):
        self._contexts.append(self.Context(json_path, controls, promise))

    def get_result(self) -> dict:
        for context in self._contexts:
            post_text = self.post(context.json_path, context.controlls, context.promise.resolve())
            self.infuse(context.json_path, post_text)

        return self._result

    @dataclass
    class Context:
        json_path: str
        controlls: List[Control]
        promise: Promise
