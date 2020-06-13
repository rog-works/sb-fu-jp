from unittest import TestCase
from rogw.transworker import TransWorker


class TestTransWorker(TestCase):
    def test_run(self):
        org_texts = [
            '^green;abcd^reset;',
            '^green;+1 +2 +3',
            '^ green;abcd. abcd. abcd.^reset;',
            '^ green;abcd',
            '^green;abcd^reset;efgh^orange;ijkl^reset;',
            '^ orange;[abcd^reset;efgh^ orange;ijkl^reset;mnop]',
        ]
        prepare_expected = [
            '${0000}abcd${/}',
            '${0000}+1 +2 +3${/}',
            '${0000}abcd. abcd. abcd.${/}',
            '${0000}abcd${/}',
            '${0000}abcd${/}efgh${0001}ijkl${/}',
            '${0000}[abcd${/}efgh${0001}ijkl${/}mnop]',
        ]
        trans_texts = [
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
        for index, org_text in enumerate(org_texts):
            worker = TransWorker(org_text, org_text)
            self.assertEqual(worker._pre_text, prepare_expected[index])
            self.assertEqual(worker.run(trans_texts[index]), post_expected[index])
