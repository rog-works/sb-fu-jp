from unittest import TestCase
from jsonquery import JsonQuery


class TestJsonPath(TestCase):
    def test_find(self):
        data = {
            'a': 1,
            'b': 'a',
            'c': {
                'c-a': 2,
                'c-b': 'b',
                'c-c': {
                    'c-c-a': 3,
                    'c-c-b': 'c',
                },
                'c-d': [
                    {
                        'c-d-0-a': 4,
                        'c-d-0-b': 'd',
                    },
                ],
            },
            'd': [
                5,
                'e',
                {
                    'd-3-a': 6,
                    'd-3-b': 'f',
                },
                [
                    7,
                    'g'
                ],
            ],
        }
        jq = JsonQuery(data)
        int_elem = jq.find(r'^a$')[0]
        self.assertEqual(int_elem.value, 1)
        int_elem.value = 2
        self.assertEqual(int_elem.value, 2)
        self.assertEqual(data['a'], 2)

        obj_elem = jq.find(r'^c$')[0]
        self.assertEqual(type(obj_elem.value), dict)
        self.assertEqual(obj_elem.value, data['c'])

        rel_str_elem = obj_elem.below(r'^c-b$')[0]
        self.assertEqual(rel_str_elem.value, 'b')
        rel_str_elem.value = 'b+'
        self.assertEqual(rel_str_elem.value, 'b+')
        self.assertEqual(data['c']['c-b'], 'b+')
