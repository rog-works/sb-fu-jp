from unittest import TestCase, mock


class TestDiscovery(TestCase):
    CONFIG = {
        'GAS_URL': 'https://example.com/path',
        'REQUEST_SIZE_LIMIT': 5000,
        'RECORD_FILEPATH': 'tests/save/record.csv',
        'DEST_DIR': 'tests/dest/',
        'CACHE_DIR': 'tests/caches/',
        'REPORT_FILEPATH': 'tests/logs/report.log',
    }

    def test_search(self):
        with mock.patch.dict('rogw.config.config', self.CONFIG):
            from rogw.discovery import Discovery

            discoveries = Discovery().search('tests/fu_assets/', r'\.(questtemplate|monstertype|config|codex)$')
            self.assertEqual(len(discoveries), 5)
