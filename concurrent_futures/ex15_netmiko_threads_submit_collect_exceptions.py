from pprint import pprint
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
import random
from itertools import repeat

import yaml
from netmiko import (
    Netmiko,
    NetmikoAuthenticationException,
    NetmikoBaseException,
    NetmikoTimeoutException,
)

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="{threadName} {asctime} {name} {levelname} {message}",
    datefmt="%H:%M:%S",
    style="{",
    level=logging.DEBUG,
)


def send_show(device_dict, command):
    device = device_dict.get("host")
    logging.info(f">>> Подключаюсь {device}")
    with Netmiko(**device_dict) as conn:
        conn.enable()
        output = conn.send_command(command)
        return output


def send_cmd_to_all(devices, command, threads=10):
    ip_out_dict = {}
    errors_on_devices = {}
    with ThreadPoolExecutor(max_workers=threads) as ex:
        task_queue = [ex.submit(send_show, dev, command=command) for dev in devices]
        for dev, future in zip(devices, task_queue):
            host = dev["host"]
            exception = future.exception()
            if exception:
                errors_on_devices[host] = exception
            else:
                ip_out_dict[ip] = future.result()
    return ip_out_dict, errors_on_devices


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    cmd = "sh run | i hostname"
    correct, errors = send_cmd_to_all(devices, cmd)
    pprint(errors)
