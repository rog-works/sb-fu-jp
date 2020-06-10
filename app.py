import sys
from typing import List
from args import Args
from cache import Cache
from translator import Translator
from mod import Mod
from logger import logger
from config import config
from record import Record
from target import Target


class App:
    def __init__(self, args: Args) -> None:
        self._args = args
        self._translator = Translator(config['GAS_URL'], Cache(config['CACHE_DIR']), config['REQUEST_SIZE_LIMIT'])
        self._record = Record(config['RECORD_FILEPATH'])
        if self._args.force:
            self._record.clear()

    def run(self):
        if len(self._args.targets) == 0:
            logger.info('target none.')
            return

        logger.info('Start tranlation.')

        for target_key in self._args.targets:
            if self._args.discover:
                self._run_target(Target.auto_discovery(target_key))
            else:
                self._run_target(Target.from_config(target_key))

        self._finish()

        logger.info('Finish tranlation.')

    def _run_target(self, target: Target):
        logger.info(f'Start {target.key} translation. counts = {len(target.targets)}')

        mods: List[Mod] = []
        for filepath, json_paths in target.targets.items():
            try:
                mods.append(self._run_prepare(filepath, json_paths))
            except Exception as e:
                logger.error(f'Prepare procesing error! file = {filepath} error = {e}')

        try:
            self._translator.perform()
        except Exception as e:
            logger.error(f'Translation error. error = {e}')

        for mod in mods:
            try:
                self._run_post(mod)
            except Exception as e:
                logger.error(f'Post procesing error! file = {mod.filepath} error = {e}')

        logger.info(f'Finish {target.key} tranlation.')

    def _run_prepare(self, filepath: str, json_paths: List[str]) -> Mod:
        mod = Mod.load(filepath)
        if not self._record.translated(mod.filepath, mod.digest):
            for worker in mod.build_workers(json_paths).values():
                self._translator.promise(worker.prepare(), worker.post)

        return mod

    def _run_post(self, mod: Mod):
        if mod.can_translation:
            mod.save(f'{config["DEST_DIR"]}/{mod.filepath}', mod.translation())
            self._record.translation(mod.filepath, mod.digest)

            logger.info(f'Mod translation. {config["DEST_DIR"]}/{mod.filepath}')

    def _finish(self):
        self._record.flush()


if __name__ == '__main__':
    App(Args(sys.argv)).run()
