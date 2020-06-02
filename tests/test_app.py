from unittest import TestCase, mock
from args import Args


class TestApp(TestCase):
    CONFIG = {'GAS_URL': 'https://example.com/path'}
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
        '--dest', 'dest',
        '--keys', 'description',
        '--files', ','.join([
            'fu_assets/items/active/crewcontracts/crewcontract_arctic.activeitem',
            'fu_assets/items/active/fishingrod/profishingrod.activeitem',
            'fu_assets/items/armors/slimenobleblack/slimenobleblack.chest',
            'fu_assets/items/active/shields/durasteelshield.activeitem',
        ]),
    ]

    def test_run(self):
        with mock.patch('config.config', return_value=self.CONFIG):
            with mock.patch('translator.Translator._fetch', return_value=self.RES):
                with mock.patch('storage.Storage.save') as save_mock:
                    from app import App

                    args = Args(self.ARGV)
                    App(args).run()

                    for index, src_filepath in enumerate(args.files):
                        call = save_mock.call_args_list[index][0]
                        actual_filepath, actual_data = call
                        expected_filepath = f'{args.dest}/{src_filepath}'
                        expected_text = self.RES['results'][f't{index}']
                        self.assertEqual(expected_filepath, actual_filepath)
                        self.assertEqual(expected_text, actual_data['description'])
