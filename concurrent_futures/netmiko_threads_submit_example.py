"""
Тестовый пример кода для демонстрации работы submit.
"""
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import logging

from netmiko import ConnectHandler
import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_command(device, command):
    time.sleep(random.random() * 10)
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return result


def function1(device, command):
    logging.info(f"FUNC1 Running {device['ip']}, command {command}")
    return send_show_command(device, command)


def function2(device, command):
    logging.info(f"FUNC2 Running {device['ip']}, command {command}")
    return send_show_command(device, command)


def send_show_command_to_devices(devices, commands, limit=5):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future1_output = []
        future2_output = []
        for dev in devices:
            for command in commands:
                future1 = executor.submit(function1, dev, command)
                future1_output.append(future1)
            for command in commands:
                future2 = executor.submit(function2, dev, command)
                future2_output.append(future2)
        for future in as_completed(future1_output + future2_output):
            future.result()


if __name__ == "__main__":
    commands = ["sh ip int br", "sh arp", "sh version", "sh ip int br | ex un",
                "sh run | i interface", "sh vers | i IOS"]
    with open("devices.yaml") as f:
        devices = yaml.load(f)
    send_show_command_to_devices(devices, commands)

