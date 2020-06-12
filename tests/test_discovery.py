from unittest import TestCase
from discovery import Discovery


class TestDiscovery(TestCase):
    def test_search(self):
        discoveries = Discovery().search('fu_assets/quests', r'\.questtemplate')
        self.assertEqual(len(discoveries), 252)
