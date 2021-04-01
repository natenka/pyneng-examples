# Репозиторий в процессе наполнения!

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Examples of using Python for network engineers

> Не забывайте про поиск GitHub по репозиторию, так можно найти все примеры
> по какому-то конкретному модулю.

Цель создания репозитория - предоставить примеры работы с модулями от простых
до более сложных. На курсе/в книге примеры ограничены, так как не все темы еще
изучены, тут я пытаюсь показать примеры без ограничений по темам, ближе к тому
как они будут использоваться в жизни.

> Все примеры показаны на Cisco IOS.

В каждом каталоге есть файл README с полезными ссылками по теме.

## Версия Python

Все примеры писались и проверялись для Python 3.8. Форматирование black.

## Темы

* asyncio - основы asyncio, модули для подключения Telnet/SSH/HTTP(S), работа с asyncio
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
* ssh_telnet - подключение Telnet/SSH
* subprocess
* textfsm - примеры шаблонов и использования TextFSM в Python и модулях netmiko, scrapli
* type_annotations - примеры аннотации типов для разного кода

