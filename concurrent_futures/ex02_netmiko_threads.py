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
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)


def send_show_command(device, show):
    host = device['host']
    logging.info(f">>> Подключаюсь к {host}")
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        time.sleep(random.random() * 10)
        output = ssh.send_command(show)
        logging.debug(f"\n{output}\n")
        logging.info(f"<<< Получена информация от {host}")
        return output


def send_show_to_devices(devices, show):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        f = executor.sumbit(send_show_command, device, show)
        for dev, output in zip(devices, results):
            host = dev['host']
            result_dict[host] = output
    print("### Все потоки отработали")
    return result_dict


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    r = send_show_to_devices(devices, "sh int desc")
    pprint(r)
