from unittest import TestCase
from rogw.modjson import ModJson


class TestModJson(TestCase):
    def test_load(self):
        filepaths = [
            'tests/fu_assets/interface/scripted/collections/collectionsgui.config',
            'tests/fu_assets/codex/documents/networkguide2.codex',
            'tests/fu_assets/bees/beeData.config',
            'tests/fu_assets/bees/monsters/aquarum.monstertype',
        ]
        modjson = ModJson()
        for filepath in filepaths:
            modjson.load(filepath)
