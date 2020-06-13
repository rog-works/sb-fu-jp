from unittest import TestCase
from rogw.jsonquery import JsonQuery


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

    def test_search(self):
        jq = JsonQuery(self.JSON)

        int_elem = jq.search(r'^a$')
        self.assertEqual(len(int_elem), 1)
        self.assertEqual(int_elem.first.value, 1)
        self.assertEqual(int_elem.first.value, self.JSON['a'])

        str_elem = jq.search(r'^b$')
        self.assertEqual(str_elem.first.value, 'a')
        self.assertEqual(str_elem.first.value, self.JSON['b'])

        obj_elem = jq.search(r'^c\.c-c$')
        self.assertEqual(type(obj_elem.first.value), dict)
        self.assertEqual(obj_elem.first.value, self.JSON['c']['c-c'])

        obj_int_elem = obj_elem.search(r'^c-c-a$')
        self.assertEqual(obj_int_elem.first.value, 3)
        self.assertEqual(obj_int_elem.first.value, self.JSON['c']['c-c']['c-c-a'])

        arr_elem = jq.search(r'^d\.3$')
        self.assertEqual(type(arr_elem.first.value), list)
        self.assertEqual(arr_elem.first.value, self.JSON['d'][3])

        arr_str_elem = arr_elem.search(r'^1$')
        self.assertEqual(arr_str_elem.first.value, 'h')
        self.assertEqual(arr_str_elem.first.value, self.JSON['d'][3][1])

        jq = JsonQuery(self.JSON, delimiter='/')

        int_elem = jq.search(r'^d/2/d-2-a$')
        self.assertEqual(int_elem.first.value, 6)
        self.assertEqual(int_elem.first.value, self.JSON['d'][2]['d-2-a'])

    def test_equals(self):
        jq = JsonQuery(self.JSON)

        obj_elem = jq.equals('d.2')
        self.assertEqual(len(obj_elem), 1)
        self.assertEqual(type(obj_elem.first.value), dict)
        self.assertEqual(obj_elem.first.value, self.JSON['d'][2])

    def test_startswith(self):
        jq = JsonQuery(self.JSON)

        elems = jq.startswith('d.2')
        self.assertEqual(len(elems), 3)

    def test_setter(self):
        jq = JsonQuery(self.JSON)

        str_elem = jq.search(r'^c\.c-d\.0\.c-d-0-b$')
        self.assertEqual(str_elem.first.value, 'd')
        self.assertEqual(str_elem.first.value, self.JSON['c']['c-d'][0]['c-d-0-b'])
        str_elem.value = 'd+'
        self.assertEqual(str_elem.first.value, 'd+')
        self.assertEqual(str_elem.first.value, self.JSON['c']['c-d'][0]['c-d-0-b'])
