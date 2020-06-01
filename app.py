import os
import sys
from typing import List
from args import Args
from storage import Storage
from translator import Translator
from mod import Mod
from logger import logger


class App:
    GAS_URL = os.environ['GAS_URL']
    TOHGHER_LIMIT_SIZE = 5000

    @classmethod
    def run(cls, args: Args):
        if len(args.files) == 0:
            return

        try:
            translator = Translator(cls.GAS_URL, cls.TOHGHER_LIMIT_SIZE)
            storage = Storage()
            mods: List[Mod] = []
            for filepath in args.files:
                data = storage.load(filepath)
                mod = Mod(filepath, data)
                mods.append(mod)
                for worker in mod.works(args.keys):
                    translator.promise(worker.prepare(), worker.post)

            translator.perform()

            for mod in mods:
                if mod.has_translate:
                    storage.save(f'{args.dest}/{mod.filepath}', mod.translated())
        except Exception as e:
            logger.error(e)
            raise


if __name__ == '__main__':
    App.run(Args(sys.argv))
