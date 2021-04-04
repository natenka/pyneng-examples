# Репозиторий в процессе наполнения!

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Python code examples for Network Engineers

> Не забывайте про поиск GitHub по репозиторию, так можно найти все примеры
> по какому-то конкретному модулю.

На курсе/в книге примеры кода ограничены, так как не все темы еще
изучены, а тут я пытаюсь показать примеры без ограничений по темам, ближе к тому
как они будут использоваться в жизни.
Цель репозитория показать примеры использования разных модулей, с более-менее готовыми
функциями и классами, которые можно использовать в своих скриптах.

> Все примеры показаны на Cisco IOS.

В каждом каталоге есть файл README с полезными ссылками по теме.

## Версия Python

Все примеры писались и проверялись для Python 3.8. Форматирование black.

## Темы

* asyncio - основы asyncio, модули для подключения Telnet/ssh_telnet/HTTP(S), работа с asyncio
* cli_interface - модули для создания интерфейса командной строки: click, typer, argparse
* concurrent_futures - параллельное подключение к оборудованию с помощью модуля concurrent.futures
* data_classes
* decorator
* generator
* logging - модуль logging
* misc - все что не попало в какую-то конкретную тему
* oop - основы, специальные методы, property и т.д.
* package - пример Python package
* regex - примеры использования регулярных выражений для обработки вывода show команд
* ssh_telnet_telnet - подключение Telnet/ssh_telnet
* subprocess
* textfsm - примеры шаблонов и использования TextFSM в Python и модулях netmiko, scrapli
* type_annotations - примеры аннотации типов для разного кода

## Progress (5/48)

| Topic                                  | done  | docstrings |
| -------------------------------------- | ----- | ---------- |
| asyncio01_basics                       | | |
| asyncio02_libs aiohttp_basics          | | |
| asyncio02_libs asynssh_telnet         | | |
| asyncio02_libs httpx         | | |
| asyncio02_libs netdev         | | |
| asyncio02_libs scrapli         | done | |
| asyncio03_api async_decorators         | | |
| asyncio03_api async_generators         | | |
| asyncio03_api asyncio_loop         | | |
| asyncio03_api asyncio_subprocess         | | |
| asyncio03_api asyncio_wait         | | |
| asyncio03_api class_with_async_methods         | | |
| asyncio03_api run_in_thread         | | |
| asyncio03_api semaphore         | | |
| asyncio03_api task_class         | | |
| cli_interface argparse          | | |
| cli_interface click          | | |
| cli_interface typer          | | |
| concurrent_futures            | | |
| data_classes              | | |
| decorator             | | |
| generator             | | |
| logging          | | |
| misc cisco_config_diff          | | |
| misc colored_dict          | | |
| misc config_to_dict          | | |
| misc explore_map          | | |
| misc get_info_from_network          | | |
| oop abc_class          | | |
| oop basic_class          | | |
| oop classmethod          | | |
| oop data_classes          | | |
| oop inheritance          | | |
| oop magic_methods          | | |
| oop mixin_class          | | |
| oop namedtuple_class          | | |
| oop property          | | |
| oop staticmethod          | | |
| python package            | | |
| regex             | | |
| ssh_telnet netmiko          | done | |
| ssh_telnet paramiko          | done | |
| ssh_telnet pexpect          | done | |
| ssh_telnet scrapli          | done | |
| ssh_telnet telnetlib          | | |
| subprocess            | | |
| textfsm           | | |
| type_annotations              | | |
