import os
from typing import List

from rogw.args import Args
from rogw.cache import Cache
from rogw.config import config
from rogw.jsonquery import JsonQuery
from rogw.logger import logger
from rogw.mod import Mod
from rogw.modjson import ModJson
from rogw.record import Record
from rogw.target import Target
from rogw.translator import Translator
from rogw.transworker import TransWorker


class App:
    def __init__(self, args: Args) -> None:
        self._args = args
        self._json = ModJson()
        self._record = Record(config['RECORD_FILEPATH'])
        if self._args.force:
            self._record.clear()

    def run(self):
        if len(self._args.targets) == 0:
            logger.info('target none.')
            return

        logger.info('Start tranlation.')

        for target_key in self._args.targets:
            target = Target.auto_discovery(target_key) if self._args.discover else Target.from_config(target_key)
            if not self._run_target(target):
                break

        self._finish()

        logger.info('Finish tranlation.')

    def _run_target(self, target: Target) -> bool:
        logger.info(f'Start "{target.key}" translation. counts = {len(target.targets)}')

        translator = self._new_translator()

        mods: List[Mod] = []
        for filepath, paths in target.targets.items():
            mods.append(Mod(filepath, self._json.load(filepath)))
            self._prepare(mods[-1], paths, translator)

        continued = self._translation(translator)

        for mod in mods:
            self._post(mod)

        logger.info(f'Finish "{target.key}" tranlation.')
        return continued

    def _new_translator(self) -> Translator:
        return Translator(config['GAS_URL'], Cache(config['CACHE_DIR']), config['REQUEST_SIZE_LIMIT'])

    def _prepare(self, mod: Mod, paths: List[str], translator: Translator):
        if self._record.translated(mod.filepath, mod.digest):
            return

        for elem in JsonQuery(mod.data).equals(*paths):
            worker = TransWorker(elem.value, f'{mod.filepath} {elem.full_path}')
            mod.promises[elem.full_path] = translator.enqueue(worker)

    def _translation(self, translator: Translator) -> bool:
        try:
            translator.perform()
            return True
        except Exception as e:
            logger.error(f'Translation error. error = [{type(e)}] {e}')
            return False

    def _post(self, mod: Mod):
        if not mod.can_translation:
            return

        self._json.save(os.path.join(config['DEST_DIR'], mod.filepath), mod.translation())
        self._record.translation(mod.filepath, mod.digest)

        logger.info(f'Mod translation. {os.path.join(config["DEST_DIR"], mod.filepath)}')

    def _finish(self):
        self._record.flush()
