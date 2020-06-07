from unittest import TestCase, mock
from args import Args
from target import Target


class TestApp(TestCase):
    CONFIG = {
        'GAS_URL': 'https://example.com/path',
        'REQUEST_SIZE_LIMIT': 5000,
        'RECORD_FILEPATH': 'tests/record.csv',
        'DEST_DIR': 'dest/',
    }
    RES = {
        'code': 200,
        'results': {
            't0': 'あ',
            't1': 'い',
            't2': 'う',
            't3': 'え',
        },
    }
    ARGV = [
        'trans.py',
        '--target', 'tests',
        '--force'
    ]

    def test_run(self):
        with mock.patch.dict('config.config', self.CONFIG):
            with mock.patch('translator.Translator._fetch', return_value=self.RES):
                with mock.patch('storage.Storage.save') as save_mock:
                    from app import App

                    args = Args(self.ARGV)
                    App(args).run()

                    trans_index = 0
                    for target_key in args.targets:
                        target = Target(target_key)
                        for file_index, src_filepath in enumerate(target.files):
                            call = save_mock.call_args_list[file_index][0]
                            actual_filepath, actual_data = call
                            expected_filepath = f'{self.CONFIG["DEST_DIR"]}/{src_filepath}'
                            self.assertEqual(expected_filepath, actual_filepath)
                            for json_path in target.json_paths:
                                expected_text = self.RES['results'][f't{trans_index}']
                                self.assertEqual(expected_text, actual_data[json_path])
                                trans_index = trans_index + 1
