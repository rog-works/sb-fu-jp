import json
import os
from typing import List, Dict

from rogw.discovery import Discovery


class Target:
    @classmethod
    def from_config(cls, key: str) -> 'Target':
        config = cls._load_config(os.path.join('targets', key, 'config.json'))
        files = cls._load_files(os.path.join('targets', key, 'files.txt'))
        return cls(key, {filepath: config['paths'] for filepath in files})

    @classmethod
    def _load_config(cls, filepath: str) -> dict:
        with open(filepath) as f:
            return json.load(f)

    @classmethod
    def _load_files(cls, filepath: str) -> List[str]:
        with open(filepath) as f:
            return [line for line in f.read().split('\n') if line]

    @classmethod
    def auto_discovery(cls, key: str) -> 'Target':
        discoveries = Discovery().search(os.path.join('fu_assets', key), f'\\.({"|".join(cls.EXTENTIONS)})$')
        return cls(key, discoveries)

    def __init__(self, key: str, targets: Dict[str, List[str]]) -> None:
        self.key = key
        self.targets = targets

    EXTENTIONS = [
        'MONSTERPART',
        # 'PNG',
        # 'TXT',
        'activeitem',
        'aimission',
        # !'animation',
        # 'ase',
        # 'aseprite',
        'augment',
        'back',
        'beamaxe',
        # !'behavior',
        # !'biome',
        # !'bossability',
        'bush',
        'chest',
        # !'cinematic',
        'codex',
        'collection',
        # !'combofinisher',
        'config',
        'consumable',
        'currency',
        # !'cursor',
        # !'damage',
        # !'disabled',
        # !'dungeon',
        # !'effectsource',
        # !'evo',
        'flashlight',
        # !'frames',
        # !'fuck',
        # !'functions',
        # !'gitignore',
        # !'grass',
        'gun',
        'harvestingtool',
        'head',
        # 'ico',
        'instrument',
        'item',
        # !'itemdescription',
        # !'json',
        'legs',
        'liqitem',
        'liquid',
        # 'lua',
        'material',
        'matitem',
        'matmod',
        # 'md',
        'miningtool',
        # !'modularfoliage',
        # !'modularstem',
        # !'monstercolors',
        # !'monsterpart',
        # !'monsterskill',
        'monstertype',
        # !'namesource',
        # !'nodes',
        'npctype',
        'object',
        # 'ogg',
        # !'parallax',
        # !'particle',
        # !'particlesource',
        # !'partparams',
        'patch',
        # !'pattern',
        # 'pdn',
        # 'png',
        # !'projectile',
        # +'questtemplat',
        'questtemplate',
        # !'raceeffect',
        'radiomessages',
        # 'rar',
        # !'recipe',
        # !'ridgeblocks',
        'sbvn',
        # !'spawntypes',
        'species',
        # !'stagehand',
        # !'statuseffect',
        # !'structure',
        'tech',
        # !'tenant',
        # !'terrain',
        'thrownitem',
        'tillingtool',
        # 'tmx',
        # !'tooltip',
        # !'treasurepools',
        # 'tsx',
        # 'txt',
        'ui',
        # !'vehicle',
        # 'wav',
        # !'weaponability',
        # !'weaponcolors',
        # !'weather',
        'wiretool',
        # 'xcf',
        # 'zip',
    ]
