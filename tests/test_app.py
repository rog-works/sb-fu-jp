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
        '--keys', 'text,title',
        '--files', ','.join([
            'fu_assets/quests/ancienttemple.questtemplate',
            'fu_assets/quests/alienjungle.questtemplate',
        ]),
        # '--keys', 'description',
        # '--files', ','.join([
        #     'fu_assets/items/active/crewcontracts/crewcontract_arctic.activeitem',
        #     'fu_assets/items/active/fishingrod/profishingrod.activeitem',
        #     'fu_assets/items/armors/slimenobleblack/slimenobleblack.chest',
        #     'fu_assets/items/active/shields/durasteelshield.activeitem',
        # ]),
    ]

    def test_run(self):
        with mock.patch('config.config', return_value=self.CONFIG):
            with mock.patch('translator.Translator._fetch', return_value=self.RES):
                with mock.patch('storage.Storage.save') as save_mock:
                    from app import App

                    args = Args(self.ARGV)
                    App(args).run()

                    trans_index = 0
                    for file_index, src_filepath in enumerate(args.files):
                        call = save_mock.call_args_list[file_index][0]
                        actual_filepath, actual_data = call
                        expected_filepath = f'{args.dest}/{src_filepath}'
                        self.assertEqual(expected_filepath, actual_filepath)
                        for json_path in args.keys:
                            expected_text = self.RES['results'][f't{trans_index}']
                            self.assertEqual(expected_text, actual_data[json_path])
                            trans_index = trans_index + 1
