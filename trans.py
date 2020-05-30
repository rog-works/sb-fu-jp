import os
import sys
import json
import re
from urllib import parse as urlparse
from typing import List
import requests
from jsoncomment import JsonComment


GAS_URL = os.environ['GAS_URL']
TOGETHERS = 25


def run(file_paths: List[str], dest_dir: str, keys: List[str]):
    if len(file_paths) == 0:
        return

    try:
        save_counts = 0
        file_counts = len(file_paths)
        loops = int(file_counts / TOGETHERS) + 1
        for i in range(loops):
            exchanges = {}
            in_count = min(file_counts - (i * TOGETHERS), TOGETHERS)
            for j in range(in_count):
                index = i * TOGETHERS + j
                filepath = file_paths[index]
                data = load(filepath)
                exchanges[filepath] = {
                    'data': data,
                    'targets': parse_targets(data, keys),
                }

            exchanges = trans(exchanges)

            for filepath, exchange in exchanges.items():
                print(f'{save_counts + 1}/{file_counts} {filepath}')
                destpath = f'dest/{filepath}'
                save(destpath, exchange['data'])
                save_counts = save_counts + 1
    except Exception as e:
        print(f'error! [{type(e)}] {e}')


def load(filepath: str) -> dict:
    try:
        print(f'load {filepath}')
        with open(filepath) as f:
            loader = JsonComment()
            return loader.load(f)
    except Exception as e:
        raise Exception(f'file = {filepath} error = [{type(e)}] {e}')


def save(filepath: str, data: dict):
    with open(filepath, mode='w', newline='\r\n') as f:
        f.write(json.dumps(data, indent=2))


def parse_targets(data: dict, paths: List[str]) -> dict:
    return {path: parse(data[path]) for path in paths if path in data}


def parse(text: str) -> dict:
    matches = re.finditer(r'\^([a-z]+);([^\^]+)\^reset;', text)
    result = {
        'org_text': text,
        'pre_text': text,
        'controls': [],
    }
    for index, match in enumerate(matches):
        code, org_words = match.group(1, 2)
        pattern = re.compile('\\^' + code + ';([^^]+)\\^reset;')
        replace = '${' + code + str(index) + '}' + org_words + '${reset}'
        result['pre_text'] = re.sub(pattern, replace, result['pre_text'])
        result['controls'].append({
            'code': code,
            'org_words': org_words,
        })

    return result


def trans(exchanges: dict) -> dict:
    pre_texts = []
    for _, exchange in exchanges.items():
        for _, target in exchange['targets'].items():
            pre_texts.append(target['pre_text'])

    index = 0
    results = trans_to_jp(pre_texts)
    for _, exchange in exchanges.items():
        for key, target in exchange['targets'].items():
            trans_text = post_trans(results[index], target['controls'])
            exchange['data'][key] = trans_text
            index = index + 1

    return exchanges


def post_trans(trans_text: str, controls: dict) -> str:
    for index, values in enumerate(controls):
        pattern = re.compile('\\$\\s*{' + values['code'] + str(index) + '}\\s*([^$]+)\\s*\\$\\s*{reset}')
        replace = f'^{values["code"]};\\1 (org: {values["org_words"]})^reset;'
        trans_text = re.sub(pattern, replace, trans_text)

    return trans_text


def trans_to_jp(texts: List[str]) -> List[str]:
    query = ''
    prefix = ''
    for index, text in enumerate(texts):
        query = f'{query}{prefix}{urlparse.quote(text)}'
        prefix = f'&text[{index + 1}]='
        index = index = 1

    url = f'{GAS_URL}?text[0]={query}'
    return fetch(url)['texts']


def fetch(url) -> dict:
    with requests.get(url, allow_redirects=True) as res:
        return res.json()


def parse_argv(argv: List[str]) -> dict:
    option = ''
    args = {
        'dest': '',
        'keys': [],
        'files': [],
    }
    for index, value in enumerate(argv):
        if index == 0:
            continue

        if value.startswith('--'):
            option = value[2:]
            continue

        if option == 'files':
            if value.endswith(','):
                value = value[:-1]
            if len(value) > 0:
                args[option] = value.split(',')
        elif option == 'keys':
            args[option] = value.split(',')
        elif option == 'dest':
            args[option] = value

        option = ''

    return args


if __name__ == '__main__':
    args = parse_argv(sys.argv)
    run(args['files'], args['dest'], args['keys'])
