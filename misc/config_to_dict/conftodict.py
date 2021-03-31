from pprint import pprint
from itertools import chain
import sys



# Ignore command which contains words
ignore = ['ipv6', 'sh run',
          'Current configuration', 'Building configuration',
          'aqm-register-fnf',
          'clock timezone',
          'vlan internal allocation', 'banner motd']


def clean_config(config):
    """
    Delete ! sign and lines with commands in ignore list.
    config - file of configuration.
    Return config as a list
    """
    with open(config) as cfg:
        clean_cfg = [line.rstrip() for line in cfg
                     if not line.strip().startswith('!')
                        and line.rstrip()
                        and not ignore_command(line, ignore)]
    return clean_cfg


def ignore_command(command, ignore):
    """
    Проверяет содержатся ли в с команде строки из списка ignore
    command - строка
    ignore - список слов
    Возвращает True если в команде найдено слово из списка ignore, False иначе.
    """

    return any(word in command for word in ignore)


def all_children_flat(section, level):
    """
    Функция проверяет, что все строки в секции находятся на одном уровне отступа.
    Возвращает True, если да и Flase иначе.
    """
    result = []
    for child in section:
        try:
            is_alpha = child[(LEVELQ*level+1):][0].isalpha()
            result.append(is_alpha)
        except IndexError:
            print(child)
    if not result:
        return True
    return all(result)


def takewhile_partition(predicate, iterable):
    """
    Работает похоже на takewhile из модуля itertools,
    но чтобы не терять элемент до которого считывался
    итерируемый объект, возвращает две части:
    1. все что попало пока выполнялся predicate (список)
    2. все остальное (итератор)
    """
    x = ''
    items_iterator = iter(iterable)
    items_before = []

    for x in items_iterator:
        if predicate(x):
            items_before.append(x)
        else:
            break
    return items_before, chain([x], items_iterator)


def parse_cfg_to_sections(config, level=0):
    """
    Функция парсит конфигурацию и возвращает словарь.
    Рекурсивно парсит каждую секцию в которой не все команды на одном уровне.
    """
    config_dict = {}

    while True:
        try:
            line = next(config)
        except StopIteration:
            break
        try:
            if line[LEVELQ*level].isalnum():
                section = line
                section_content, config = takewhile_partition(
                    lambda line: not line[LEVELQ*level].isalpha(), config)
                if section_content and not all_children_flat(section_content, level):
                    # рекурсивный вызов
                    section_content = parse_cfg_to_sections(iter(section_content), level+1)
                config_dict[section] = section_content
        except IndexError:
            break
    # если в словаре все значения пустые списки:
    if sum(map(len, config_dict.values())) == 0:
        return list(config_dict.keys())
    return config_dict


def strip_lines(cfg_dict):
    for key, value in list(cfg_dict.items()):
        if isinstance(value, dict):
            del cfg_dict[key]
            cfg_dict[key.strip()] = strip_lines(value)
        elif isinstance(value, list):
            del cfg_dict[key]
            cfg_dict[key.strip()] = list(map(str.strip, value))
    return cfg_dict


def parse_config(filename):
    """
    Функция ожидает имя файла и возвращает конфигурацию в виде словаря
    """
    cleaned_config = iter(clean_config(filename))
    return strip_lines(parse_cfg_to_sections(cleaned_config))


if __name__ == "__main__":
    # сколько пробелов используется для отступа
    LEVELQ = 2
    result = parse_config('example_cfg_2.txt')
    pprint(result, width=140)

    LEVELQ = 1
    result = parse_config('example_cfg.txt')
    pprint(result, width=140)
