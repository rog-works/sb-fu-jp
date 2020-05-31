import os
import sys
from typing import Dict
from args import Args
from storage import Storage
from translator import Translator
from worker import Worker
from logging import getLogger


logger = getLogger(__name__)


class App:
    GAS_URL = os.environ['GAS_URL']
    TOHGHER_LIMIT_SIZE = 50000

    @classmethod
    def run(cls, args: Args):
        if len(args.files) == 0:
            return

        try:
            translator = Translator(cls.GAS_URL, cls.TOHGHER_LIMIT_SIZE)
            storage = Storage()
            workers: Dict[str, Worker] = {}
            for filepath in args.files:
                data = storage.load(filepath)
                worker = Worker(data)
                for json_path in args.keys:
                    pre_text, controls = worker.prepare(json_path)
                    worker.context(json_path, controls, translator.future(pre_text))

                workers[filepath] = worker

            translator.perform()

            number = 1
            for filepath, worker in workers.items():
                logger.info(f'{number}/{len(args.files)} {filepath}')
                storage.save(f'{args.dest}/{filepath}', worker.get_result())
                number = number + 1
        except Exception as e:
            logger.error(e)
            raise


if __name__ == '__main__':
    App.run(Args(sys.argv))
