# Work in progress! 10/48 topics done

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Python code examples for Network Engineers

On the course/in the book, code examples are limited, since not all topics
have been covered yet, so here I am trying to show examples without restrictions
on topics, closer to how they will be used in life. The purpose of the repository
is to show examples of using different modules, with more or less ready-made
functions and classes that you can use in your scripts.

> All examples are shown on Cisco IOS.

Each directory has a README file with useful links on the topic.

## Python version

All examples were written and tested for Python 3.8. Formatting - black.

## Topics

* asyncio - asyncio basics, modules for Telnet/SSH/HTTP(S) connection, working with asyncio
* cli_interface - modules for creating a command line interface: click, typer, argparse
* concurrent_futures - concurrent connection to network devices using the concurrent.futures module
* data_classes
* decorator
* generator
* logging - the logging module
* misc - everything that is not included in a particular topic
* oop - basics, special methods, property, etc.
* package - a Python package example
* regex - examples of using regular expressions to process show command output
* ssh_telnet_telnet - Telnet/SSH connection
* subprocess
* textfsm - examples of templates and using TextFSM in Python and modules netmiko, scrapli
* type_annotations - examples of type annotations for different code

## Progress (11/48)

For now, these are just examples copied from the basic and advanced course 
repository. As I review and rewrite the examples, I mark them here. So far, 
I am writing only code, then there will be a stage of describing examples,
adding docstrings to functions.


| Topic                                  | done  | docstrings |
| -------------------------------------- | ----- | ---------- |
| asyncio01_basics                       | | |
| asyncio02_libs aiohttp                 | | |
| asyncio02_libs asynssh                 | done  | |
| asyncio02_libs httpx                   | | |
| asyncio02_libs netdev                  | done  | |
| asyncio02_libs scrapli                 | done  | |
| asyncio03_api async_decorators         | | |
| asyncio03_api async_generators         | | |
| asyncio03_api asyncio_loop             | | |
| asyncio03_api asyncio_subprocess       | | |
| asyncio03_api asyncio_wait             | | |
| asyncio03_api class_with_async_methods | | |
| asyncio03_api run_in_thread            | | |
| asyncio03_api semaphore                | | |
| asyncio03_api task_class               | | |
| cli_interface argparse                 | | |
| cli_interface click                    | | |
| cli_interface typer                    | done  | |
| concurrent_futures                     | done  | |
| data_classes                           | | |
| decorator                              | | |
| generator                              | | |
| logging                                | | |
| misc cisco_config_diff                 | | |
| misc colored_dict                      | | |
| misc config_to_dict                    | | |
| misc explore_map                       | | |
| misc get_info_from_network             | | |
| oop abc_class                          | | |
| oop basic_class                        | | |
| oop classmethod                        | | |
| oop data_classes                       | | |
| oop inheritance                        | | |
| oop magic_methods                      | | |
| oop mixin_class                        | | |
| oop namedtuple_class                   | | |
| oop property                           | | |
| oop staticmethod                       | | |
| python package                         | | |
| regex                                  | | |
| ssh_telnet netmiko                     | done  | |
| ssh_telnet paramiko                    | done  | |
| ssh_telnet pexpect                     | done  | |
| ssh_telnet scrapli                     | done  | |
| ssh_telnet telnetlib                   | done  | |
| subprocess                             | done | |
| textfsm                                | | |
| type_annotations                       | | |
