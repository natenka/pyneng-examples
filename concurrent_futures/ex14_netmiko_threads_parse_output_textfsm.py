from concurrent.futures import ThreadPoolExecutor
import re
from pprint import pprint
from itertools import repeat
import logging

import netmiko
import yaml
from textfsm import clitable


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show(device, command):
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            return result
    except netmiko.NetmikoTimeoutException as error:
        print(f"Failed to connect to {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication error on {device['host']}")


def parse_command_textfsm(
    command_output, attributes_dict, index_file="index", templ_path="templates"
):

    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    return [dict(zip(cli_table.header, row)) for row in cli_table]


def send_and_parse_show_command(device_dict, command, templates_path):
    attributes = {"Command": command, "Vendor": device_dict["device_type"]}
    output = send_show(device_dict, command)
    parsed_data = parse_command_textfsm(
        output, attributes, templ_path=templates_path
    )
    return parsed_data


def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result_all = [
            executor.submit(send_and_parse_show_command, device, command, templates_path)
            for device in devices
        ]
        output = {device["host"]: f.result() for device, f in zip(devices, result_all)}
    return output


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    results = send_and_parse_command_parallel(devices, "sh ip int br", "templates")
    pprint(results, width=130)

