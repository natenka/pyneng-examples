from platform import system as system_name
import re
from pprint import pprint
import time
from datetime import datetime
import random
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging
import subprocess

import netmiko
import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def ping_ip(ip):
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    reply = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip_is_reachable = reply.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


def send_command(device, show):
    host = device["host"]
    logging.info(f">>> Подключаюсь к {host}")
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        time.sleep(random.random() * 10)
        output = ssh.send_command(show)
        logging.debug(f"\n{output}\n")
        logging.info(f"<<< Получена информация от {host}")
        return output


def send_command_to_devices(devices, show):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(send_command, devices, repeat(show))
        for dev, output in zip(devices, results):
            host = dev["host"]
            result_dict[host] = output
    return result_dict


def main():
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    check_ip_list = [dev["host"] for dev in devices]
    reach, unreach = ping_ip_addresses(check_ip_list)
    if unreach:
        print(f"Недоступные адреса:\n{unreach}")

    # Подключение идет только к тем адресам, которые пингуются
    reachable_devices = [dev for dev in devices if dev["host"] in reach]
    results = send_command_to_devices(reachable_devices, "sh int desc")
    pprint(results, width=120)


if __name__ == "__main__":
    main()
