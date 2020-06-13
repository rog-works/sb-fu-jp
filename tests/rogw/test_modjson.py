from unittest import TestCase
from rogw.modjson import ModJson


class TestModJson(TestCase):
    def test_load(self):
        filepaths = [
            'fu_assets/codex/documents/networkguide2.codex',
            'fu_assets/bees/beeData.config',
            'fu_assets/bees/monsters/aquarum.monstertype',
        ]
        modjson = ModJson()
        for filepath in filepaths:
            modjson.load(filepath)
