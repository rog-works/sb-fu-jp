import sys
from typing import List
from args import Args
from storage import Storage
from translator import Translator
from mod import Mod
from logger import logger
from config import config


class App:
    GAS_URL = config['GAS_URL']
    TOHGHER_LIMIT_SIZE = 5000

    def __init__(self, args: Args) -> None:
        self._translator = Translator(self.GAS_URL, self.TOHGHER_LIMIT_SIZE)
        self._storage = Storage()
        self._args = args

    def run(self):
        if len(self._args.files) == 0:
            return

        mods: List[Mod] = []
        for filepath in self._args.files:
            try:
                mods.append(self._run_prepare(filepath))
            except Exception as e:
                logger.error(f'Prepare procesing error! file = {filepath} error = {e}')

        self._translator.perform()

        for mod in mods:
            try:
                self._run_post(mod)
            except Exception as e:
                logger.error(f'Post procesing error! file = {mod.filepath} error = {e}')

    def _run_prepare(self, filepath: str) -> Mod:
        data = self._storage.load(filepath)
        mod = Mod(filepath, data)
        for worker in mod.works(self._args.keys):
            self._translator.promise(worker.prepare(), worker.post)

        return mod

    def _run_post(self, mod: Mod):
        if mod.has_translate:
            self._storage.save(f'{self._args.dest}/{mod.filepath}', mod.translated())


if __name__ == '__main__':
    App(Args(sys.argv)).run()
