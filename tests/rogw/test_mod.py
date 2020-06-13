from unittest import TestCase
from rogw.mod import Mod


class TestMod(TestCase):
    def test_build_workers(self):
        data = {
            'aaaa': '^green;abcd^reset;',
            'bbbb': '^green;+1 +2 +3',
            'cccc': '^ green;abcd. abcd. abcd.^reset;',
            'dddd': '^ green;abcd',
            'eeee': '^green;abcd^reset;efgh^orange;ijkl^reset;',
            'ffff': '^ orange;[abcd^reset;efgh^ orange;ijkl^reset;mnop]',
        }
        prepare_expected = [
            '${0000}abcd${/}',
            '${0000}+1 +2 +3${/}',
            '${0000}abcd. abcd. abcd.${/}',
            '${0000}abcd${/}',
            '${0000}abcd${/}efgh${0001}ijkl${/}',
            '${0000}[abcd${/}efgh${0001}ijkl${/}mnop]',
        ]
        transes = [
            '${0000}あいう${/}',
            '${0000}+1 +2 +3${/}',
            '$ {0000} あいう. あいう. あいう.$ {/}',
            '$ {0000}あいう $ {/}',
            '$ {0000} あいう ${/}えおか $ {0001} きくけ ${/}',
            '$ {0000}[あいう${/}えおか$ {0001}きくけ$ {/} こさし]',
        ]
        post_expected = [
            '^green;あいう (org: abcd)^reset;',
            '^green;+1 +2 +3 (org: +1 +2 +3)^reset;',
            '^green; あいう. あいう. あいう. (org: abcd. abcd. abcd.)^reset;',
            '^green;あいう  (org: abcd)^reset;',
            '^green; あいう  (org: abcd)^reset;えおか ^orange; きくけ  (org: ijkl)^reset;',
            '^orange;[あいう (org: [abcd)^reset;えおか^orange;きくけ (org: ijkl)^reset; こさし]',
        ]
        keys = list(data.keys())
        mod = Mod('filepath', data)
        for index, worker in enumerate(mod.build_workers(keys).values()):
            self.assertEqual(worker.prepare(), prepare_expected[index])
            worker.post(transes[index])
            self.assertEqual(worker.result, post_expected[index])
