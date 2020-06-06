from unittest import TestCase
from jsonquery import JsonQuery


class TestJsonQuery(TestCase):
    JSON = {
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
                [
                    'e'
                ]
            ],
        },
        'd': [
            5,
            'f',
            {
                'd-2-a': 6,
                'd-2-b': 'g',
            },
            [
                7,
                'h'
            ],
        ],
    }

    def test_find(self):
        jq = JsonQuery(self.JSON)

        int_elem = jq.find(r'^a$')[0]
        self.assertEqual(int_elem.value, 1)
        self.assertEqual(int_elem.value, self.JSON['a'])

        str_elem = jq.find(r'^b$')[0]
        self.assertEqual(str_elem.value, 'a')
        self.assertEqual(str_elem.value, self.JSON['b'])

        obj_elem = jq.find(r'^c.c-c$')[0]
        self.assertEqual(type(obj_elem.value), dict)
        self.assertEqual(obj_elem.value, self.JSON['c']['c-c'])

        arr_elem = jq.find(r'^d.3$')[0]
        self.assertEqual(type(arr_elem.value), list)
        self.assertEqual(arr_elem.value, self.JSON['d'][3])

    def test_setter(self):
        jq = JsonQuery(self.JSON)

        str_elem = jq.find(r'^c.c-d.0.c-d-0-b$')[0]
        self.assertEqual(str_elem.value, 'd')
        self.assertEqual(str_elem.value, self.JSON['c']['c-d'][0]['c-d-0-b'])
        str_elem.value = 'd+'
        self.assertEqual(str_elem.value, 'd+')
        self.assertEqual(str_elem.value, self.JSON['c']['c-d'][0]['c-d-0-b'])
