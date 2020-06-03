from unittest import TestCase
from mod import Mod


class TestMod(TestCase):
    def test_works(self):
        data = {
            'aaaa': '^green;abcd^reset;',
            'bbbb': '^green;+1 +2 +3',
            'cccc': '^ green;abcd. abcd. abcd.^reset;',
            'dddd': '^ green;abcd',
            'eeee': '^green;abcd^reset;efgh^orange;ijkl^reset;',
            'ffff': '^ green;abcd^reset;efgh^ orange;ijkl^reset;mnop',
        }
        prepare_expected = [
            '${0000}abcd${/}',
            '${0000}+1 +2 +3${/}',
            '${0000}abcd. abcd. abcd.${/}',
            '${0000}abcd${/}',
            '${0000}abcd${/}efgh${0001}ijkl${/}',
            '${0000}abcd${/}efgh${0001}ijkl${/}mnop',
        ]
        transes = [
            '${0000}あいう${/}',
            '${0000}+1 +2 +3${/}',
            '$ {0000} あいう. あいう. あいう.$ {/}',
            '$ {0000}あいう $ {/}',
            '$ {0000} あいう ${/}えおか $ {0001} きくけ ${/}',
            '$ {0000}あいう${/}えおか$ {0001}きくけ$ {/} こさし',
        ]
        post_expected = [
            '^green;あいう (org: abcd)^reset;',
            '^green;+1 +2 +3 (org: +1 +2 +3)^reset;',
            '^green; あいう. あいう. あいう. (org: abcd. abcd. abcd.)^reset;',
            '^green;あいう  (org: abcd)^reset;',
            '^green; あいう  (org: abcd)^reset;えおか ^orange; きくけ  (org: ijkl)^reset;',
            '^green;あいう (org: abcd)^reset;えおか^orange;きくけ (org: ijkl)^reset; こさし',
        ]
        keys = list(data.keys())
        mod = Mod('filepath', data)
        for index, work in enumerate(mod.works(keys)):
            self.assertEqual(work.prepare(), prepare_expected[index])
            work.post(transes[index])
            self.assertEqual(work.result, post_expected[index])
