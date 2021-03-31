import difflib
from collections import OrderedDict as odict
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
import argparse

from colorama import Fore, init


# Ignore command which contains words
ignore = ['---', '+++', '@@', '-^C', '+^C', '*********',
          'duplex', 'description', 'version 15',
          'ipv6', 'sh run',
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
                     if not '!' in line[:3]
                        and line.rstrip()
                        and not ignore_command(line, ignore)]
    return clean_cfg


def clean_diff(diff_generator):
    return (line for line in diff_generator
            if not ignore_command(line, ignore))


def make_diff(base_cfg_commands, check_cfg_commands):
    """
    Generate difference with difflib. Unified diff adds context to diff.
    base_cfg_commands - list of commands from base config,
    check_cfg_commands - list of commands from config to check.
    Returns result as a generator.
    """
    return difflib.unified_diff(base_cfg_commands, check_cfg_commands, n=30)


def ignore_command(command, ignore):
    """
    Checks command if it contains words from ignore list.
    command - string, command to check,
    ignore - list of words.
    Return True if command contains word from ignore list, False otherwise.
    """

    return any(word in command for word in ignore)


def child_is_flat(children, level=1):
    """
    Check if all children in section is in same level.
    children - list of section children.
    level - integer, current level of depth.
    Returns True if all children in the same level, False otherwise.
    """
    return all(len(child) <= level+1 or child[(level+1):][0].isalpha()
               for child in children)


def all_children_flat(section_dict, level):
    """
    Function checks if all children in ALL sections is in same level.
    * section_dict - dictionary with sections.
    * level - integer, current level of depth.
    Returns True if all children in all sections is in the same level, False otherwise.
    """
    return all(child_is_flat(children, level)
               for children in section_dict.values())


def parse_cfg_section(section,level=1):
    """
    Function parse section of config.
    In result only sections with changed children returned.
    * section - List of commands.
    * level - integer, current level of depth.
    Returns dictionary with section header as a keys,
    and a list of commands as a value.
    """
    current_section = ''
    section_children = []
    changed = False
    section_dict = odict()

    for command in section:
        if not (level == 1 and len(command) < max(2, level)):
            if command[level].isalpha():
                if current_section:
                    if changed:
                        section_dict[current_section] = section_children
                    section_children = []
                    changed = False
                current_section = command
            else:
               section_children.append(command)
        if command[0] in ['-','+']:
            changed = True
    if changed:
        section_dict[current_section] = section_children
    return section_dict


def parse_config(section,level=1):
    """
    Function recursively parse config file.
    Return:
    dictionary with section header as a keys, and a list of commands as a value.
    all_flat - True if all children flat, False overwise.
    """
    section_dict = parse_cfg_section(section, level)
    all_flat = all_children_flat(section_dict, level)

    while not all_flat:
        level += 1
        for key, children in section_dict.items():
            if not child_is_flat(children):
                s_dict, all_flat = parse_config(children,level)
                if s_dict:
                    section_dict[key] = s_dict
    return section_dict, all_flat


def yield_lines_from_diff_dict(parced_diff_dict, level = 0):
    """
    Function converts difference dictionary to list.
    * parced_diff_dict - dictionary, result of parse_config function.
    * Return generator
    If value is dictionary, function is recursively calls itself.
    """
    for key, value in parced_diff_dict.items():
        if level == 0:
            yield '\n'
            yield key
        else:
            yield key
        if type(value) == list:
            yield from value
        else:
            yield from yield_lines_from_diff_dict(value, level=1)


def main(base_config, config_to_check):
    """
    * base_config - base configuration filename
    * config_to_check - configuration to check (filename)
    Returns generator
    """
    base = clean_config(base_config)
    to_check = clean_config(config_to_check)

    cfg_difference = make_diff(base, to_check)
    cleaned_diff = clean_diff(cfg_difference)

    diff_dict = parse_config(cleaned_diff)[0]
    diff_list = yield_lines_from_diff_dict(diff_dict)
    return diff_list


def print_colored_diff(diff_generator):
    #turn off color changes at the end of every print
    init(autoreset=True)

    for line in result:
        if line.startswith('-'):
            print(Fore.RED+line)
        elif line.startswith('+'):
            print(Fore.GREEN+line)
        else:
            print(line)


def generate_html(data, template, dest_file):

    env = Environment(loader=FileSystemLoader('templates'),
                      trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template)

    with open(dest_file, 'w') as output:
        output.write(template.render(diff=data))
    print('HTML output saved to', dest_file)


parser = argparse.ArgumentParser(description='Generate config diff')

parser.add_argument('base_cfg_file', action="store")
parser.add_argument('check_cfg_file', action="store")
parser.add_argument('-f', action="store", dest="format",
                    choices=['html', 'print'], default='print',
                    help="Output format")
parser.add_argument('-d', action="store", dest="html_dst_file",
                    default='result.html', help="HTML destination file")


if __name__ == '__main__':
    args = parser.parse_args()
    base_cfg, cfg_to_check = args.base_cfg_file, args.check_cfg_file
    result = main(base_cfg, cfg_to_check)
    if args.format == 'print':
        print_colored_diff(result)
    else:
        generate_html(result, 'html_report_template.html',
                      args.html_dst_file)


'''

$ python generate_cfg_diff.py base_cfg.txt cfg1.txt -h
usage: generate_cfg_diff.py [-h] [-f {html,print}] [-d HTML_DST_FILE]
                            base_cfg_file check_cfg_file

Generate config diff

positional arguments:
  base_cfg_file
  check_cfg_file

optional arguments:
  -h, --help        show this help message and exit
  -f {html,print}   Output format
  -d HTML_DST_FILE  HTML destination file

$ python generate_cfg_diff.py base_cfg.txt cfg1.txt


 policy-map OUT_QOS
  class COMPARE
-  set dscp cs4
+  set dscp cs7


 interface Ethernet0/0
- ip address 192.168.100.1 255.255.255.0
+ ip address 192.168.120.1 255.255.255.0


-router eigrp 1
- network 0.0.0.0


 line con 0
  exec-timeout 0 0
+ privilege level 15
  logging synchronous

$ python generate_cfg_diff.py base_cfg.txt cfg1.txt -f html
HTML output saved to result.html

'''
