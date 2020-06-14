import json
import re

from jsoncomment import JsonComment


class ModJson:
    def __init__(self) -> None:
        self._loader = JsonComment()

    def load(self, filepath: str) -> dict:
        try:
            with open(filepath) as f:
                content = self._cleanup(f.read())
                return self._loader.loads(content)
        except Exception as e:
            raise Exception(f'filepath = {filepath} error = [{type(e)}] {e}')

    def _cleanup(self, content: str) -> str:
        _clean = re.sub('(?<!:)//.*\n', '', content)
        _clean = re.sub(r'/\*[^*]*\*/', '', _clean)
        return _clean

    def save(self, filepath: str, data: dict):
        try:
            with open(filepath, mode='w', newline='\r\n') as f:
                f.write(json.dumps(data, indent=2))
        except Exception as e:
            raise Exception(f'filepath = {filepath} error = [{type(e)}] {e}')
