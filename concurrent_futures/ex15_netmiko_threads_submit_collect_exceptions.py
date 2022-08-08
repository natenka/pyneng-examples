from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
import random
from itertools import repeat

from netmiko import Netmiko

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
    logging.info(f">>> Connect to {device}")
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
                ip_out_dict[host] = future.result()
    return ip_out_dict, errors_on_devices


if __name__ == "__main__":
    devices = [
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.1",
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
            "timeout": 5,
        },
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.2",
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
            "timeout": 5,
        },
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.3",
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
            "timeout": 5,
        },
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.11",  # unreachable IP
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
            "timeout": 5,
        },
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.2",
            "username": "cisco",
            "password": "ciscowrong",  # wrong password
            "secret": "cisco",
            "timeout": 5,
        },
        {
            "device_type": "cisco_ios",
            "host": "192.168.100.3",
            "username": "cisco",
            "password": "cisco",
            "secret": "ciscowrong",  # wrong secret
            "timeout": 5,
        },
    ]
    cmd = "sh run | i hostname"
    correct, errors = send_cmd_to_all(devices, cmd)
    pprint(errors)
