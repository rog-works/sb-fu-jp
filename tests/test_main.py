import os
from unittest import TestCase, mock
from rogw.args import Args
from rogw.target import Target


class TestMain(TestCase):
    CONFIG = {
        'GAS_URL': 'https://example.com/path',
        'REQUEST_SIZE_LIMIT': 5000,
        'RECORD_FILEPATH': 'tests/save/record.csv',
        'DEST_DIR': 'tests/dest/',
        'CACHE_DIR': 'tests/caches/',
    }
    RES = {
        'code': 200,
        'results': {
            't0': 'あ',
            't1': 'い',
            't2': 'う',
            't3': 'え',
            't4': 'お',
            't5': 'か',
        },
    }
    ARGV = [
        'trans.py',
        '--target', 'tests',
        '--force'
    ]

    def test_run(self):
        with mock.patch.dict('rogw.config.config', self.CONFIG):
            with mock.patch('rogw.translator.Translator._fetch', return_value=self.RES):
                with mock.patch('rogw.modjson.ModJson.save') as save_mock:
                    from rogw.app import App

                    args = Args(self.ARGV)
                    App(args).run()

                    trans_index = 0
                    for target_key in args.targets:
                        target = Target.from_config(target_key)
                        for file_index, src_filepath in enumerate(target.targets.keys()):
                            call = save_mock.call_args_list[file_index][0]
                            actual_filepath, actual_data = call
                            expected_filepath = os.path.join(self.CONFIG['DEST_DIR'], src_filepath)
                            self.assertEqual(expected_filepath, actual_filepath)
                            for json_path in target.targets[src_filepath]:
                                expected_text = self.RES['results'][f't{trans_index}']
                                self.assertEqual(expected_text, actual_data[json_path])
                                trans_index = trans_index + 1
