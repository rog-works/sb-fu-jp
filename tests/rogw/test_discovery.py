from unittest import TestCase
from rogw.discovery import Discovery


class TestDiscovery(TestCase):
    def test_search(self):
        discoveries = Discovery().search('tests/fu_assets/', r'\.(questtemplate|monstertype|config|codex)$')
        self.assertEqual(len(discoveries), 5)
