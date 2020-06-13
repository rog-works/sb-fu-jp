from dataclasses import dataclass
import re
from typing import List

from rogw.logger import logger
from rogw.worker import IWorker


@dataclass
class Control:
    code: str
    org_words: str


class TransWorker(IWorker):
    def __init__(self, org_text: str, context: str) -> None:
        self._org_text = org_text
        self._controls = self._parse_controls(org_text)
        self._pre_text = self._prepare(self._org_text, self._controls)
        self._context = context

    def _parse_controls(self, org_text: str) -> List[Control]:
        matches = re.finditer(r'\^\s*([a-z]+);([^\^]+)(\^reset;)?', org_text)
        controls = []
        for match in matches:
            code, org_words = match.group(1, 2)
            controls.append(Control(code, org_words))

        return controls

    def _prepare(self, org_text: str, controls: List[Control]) -> str:
        pre_text = self._org_text
        for index, control in enumerate(self._controls):
            pattern = re.compile('\\^\\s*' + control.code + ';\\s*' + re.escape(control.org_words) + '\\s*(\\^reset;)?')
            replace = '${' + str(index).zfill(4) + '}' + control.org_words + '${/}'
            pre_text = re.sub(pattern, replace, pre_text)

        return pre_text

    @property
    def text(self) -> str:
        return self._pre_text

    def run(self, trans_text: str) -> str:
        post_text = trans_text
        for index, control in enumerate(self._controls):
            pattern = re.compile('\\$\\s*\\{\\s*' + str(index).zfill(4) + '\\s*\\}([^$]+)\\$\\s*\\{/\\}')
            replace = f'^{control.code};\\1 (org: {control.org_words})^reset;'
            post_text = re.sub(pattern, replace, post_text)

        self._finish_log()
        return post_text

    def _finish_log(self):
        logger.info(f'Finish work. {self._context}')
