from concurrent.futures import ThreadPoolExecutor
import re
from pprint import pprint
import time
import random
from itertools import repeat
from datetime import datetime
import logging
import netmiko
import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def parse_sh_ip_int_br(output):
    logging.info(f">>> Parse sh ip int br")
    regex = (
        r"(\S+) +([\d.]+) +\w+ +\w+ +(up|down|administratively down) +(up|down)"
    )
    result = [m.groups() for m in re.finditer(regex, output)]
    return result


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


def send_and_parse_command(devices, command, parse_function, threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(send_show, devices, repeat(command))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = parse_function(output)
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    results = send_and_parse_command(devices, "sh ip int br", parse_sh_ip_int_br)
    pprint(results, width=120)

