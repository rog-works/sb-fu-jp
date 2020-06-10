import os
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
from timezone import Timezone


@dataclass
class RecordRow:
    digest: str
    created_at: str
    updated_at: str
    filepath: str


class Record:
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        self._rows = self._load(filepath)

    def translated(self, filepath: str, digest: str) -> bool:
        return filepath in self._rows and self._rows[filepath].digest == digest

    def translation(self, filepath: str, digest: str):
        translated_at = datetime.now(tz=Timezone()).strftime('%Y-%m-%d %H:%M:%S')
        if filepath in self._rows:
            self._rows[filepath].digest = digest
            self._rows[filepath].updated_at = translated_at
        else:
            self._rows[filepath] = RecordRow(digest, translated_at, translated_at, filepath)

    def clear(self):
        self._rows = {}

    def flush(self):
        self._save()

    def _load(self, filepath: str) -> Dict[str, RecordRow]:
        if not os.path.exists(filepath):
            return {}

        with open(filepath) as f:
            lines = [line for line in f.read().split('\n') if line]
            columns = lines[0].split(',')
            rows: Dict[str, RecordRow] = {}
            for line in lines[1:]:
                row = RecordRow(**{columns[index]: value for index, value in enumerate(line.split(','))})
                rows[row.filepath] = row

            return rows

    def _save(self):
        with open(self._filepath, mode='w') as f:
            f.write('{}\n'.format(','.join(self._row_keys())))
            for row in self._rows.values():
                f.write('{}\n'.format(','.join(row.__dict__.values())))

    def _row_keys(self) -> List[str]:
        return list(RecordRow('', '', '', '').__dict__.keys())
