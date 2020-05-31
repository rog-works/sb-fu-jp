import json
from jsoncomment import JsonComment


class Storage:
    def __init__(self) -> None:
        self._loader = JsonComment()

    def load(self, filepath: str) -> dict:
        try:
            with open(filepath) as f:
                return self._loader.load(f)
        except Exception as e:
            raise Exception(f'file = {filepath} error = [{type(e)}] {e}')

    def save(self, filepath: str, data: dict):
        try:
            with open(filepath, mode='w', newline='\r\n') as f:
                f.write(json.dumps(data, indent=2))
        except Exception as e:
            raise Exception(f'file = {filepath} error = [{type(e)}] {e}')
