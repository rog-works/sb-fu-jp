import os
from typing import Dict
from dataclasses import dataclass
from datetime import datetime
from timezone import Timezone


@dataclass
class RecordRow:
    digest: str
    created_at: str
    updated_at: str
    filepath: str
    json_path: str


class Record:
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        self._rows = self._load(filepath)

    def translated(self, filepath: str, json_path: str, digest: str) -> bool:
        identifer = self._to_identifer(filepath, json_path)
        return identifer in self._rows and self._rows[identifer].digest == digest

    def translation(self, filepath: str, json_path: str, digest: str):
        identifer = self._to_identifer(filepath, json_path)
        translated_at = datetime.now(tz=Timezone()).strftime('%Y-%m-%d %H:%M:%S')
        if self.translated(filepath, json_path, digest):
            self._rows[identifer].digest = digest
            self._rows[identifer].updated_at = translated_at
            self._rows[identifer].json_path = json_path
        else:
            self._rows[identifer] = RecordRow(digest, translated_at, translated_at, filepath, json_path)

    def clear(self):
        self._rows = {}

    def flush(self):
        self._save()

    def _to_identifer(self, filepath: str, json_path: str) -> str:
        return f'{filepath}#{json_path}'

    def _load(self, filepath: str) -> Dict[str, RecordRow]:
        if not os.path.exists(filepath):
            return {}

        with open(filepath) as f:
            lines = [line for line in f.read().split('\n') if line]
            columns = lines[0].split(',')
            rows: Dict[str, RecordRow] = {}
            for line in lines[1:]:
                row = RecordRow(**{columns[index]: value for index, value in enumerate(line.split(','))})
                identifer = self._to_identifer(row.filepath, row.json_path)
                rows[identifer] = row

            return rows

    def _save(self):
        with open(self._filepath, mode='w') as f:
            f.write('{}\n'.format(','.join(['digest', 'created_at', 'updated_at', 'filepath', 'json_path'])))
            for row in self._rows.values():
                f.write('{}\n'.format(','.join([row.digest, row.created_at, row.updated_at, row.filepath, row.json_path])))
