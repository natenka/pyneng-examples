import collections
import sys

import yaml
from colorama import Fore, init


init(autoreset=True)
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]


def coloring_playbook(data, level=0):
    result = ''

    key_template = colors[level]+'    '*(level)+'{}: '
    value_template = colors[level]+'{}\n'
    seq_item_template = ''

    if type(data) is dict:
        result += Fore.WHITE+'\n'
        for key, value in data.items():
            result += key_template.format(key)
            result += coloring_playbook(value, level+1)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            result += coloring_playbook(item, level+1)
    else:
        return value_template.format(data)
    return result

if __name__ == '__main__':
    playbook_filename = sys.argv[1]
    with open(playbook_filename) as f:
        playbook = yaml.load(f)

        print(coloring_playbook(playbook))
