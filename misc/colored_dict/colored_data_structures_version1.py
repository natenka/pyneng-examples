import collections

import yaml
from colorama import Fore, init

from dict_examples import playbook, int_d, london_co, list_of_tuples

init(autoreset=True)
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]


def coloring_data(data, level=0, seq_item=False):
    result = ''

    key_template = colors[level]+'    '*(level)+'{}: '
    value_template = colors[level]+'{},\n'
    seq_item_template = colors[level]+'    '*(level)+'{},\n'

    if type(data) is dict:
        result += Fore.WHITE+'   '*(level)+'\n'
        for key, value in data.items():
            result += key_template.format(key)
            result += coloring_data(value, level+1)
    elif isinstance(data, collections.Sequence) and not isinstance(data, str):
        result += Fore.WHITE+'\n'
        for item in data:
            result += coloring_data(item, level+1, seq_item=True)
        result += Fore.WHITE+'   '*(level)
    else:
        if seq_item:
            return seq_item_template.format(data)
        return value_template.format(data)
    return result+'   '*(level)+'\n'


if __name__ == '__main__':
    #print(coloring_data(int_d))
    print(coloring_data(london_co))
    print(coloring_data(playbook))
    print(coloring_data(list_of_tuples))
