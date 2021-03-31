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


def parse_sh_cdp(output):
    logging.info(f">>> Парсим вывод sh cdp")
    regex = (
        r"^Device ID: (?P<device>\S+)"
        r".*?"
        r"^ +host address: (?P<host>\S+)\n"
        r"^Platform: (?P<platform>.+?),"
        r".*?"
        r", Version (?P<ios>\S+),"
    )
    result = {}
    match = re.finditer(regex, output, re.DOTALL | re.MULTILINE)
    for m in match:
        device = m.group("device")
        params = m.groupdict()
        del params["device"]
        result[device] = params
    return result


def parse_sh_ip_int_br(output):
    logging.info(f">>> Парсим вывод sh ip int br")
    match_all = re.finditer(r"(\S+) +(\S+) .+ up +up", output)
    results = [m.groups() for m in match_all]
    return results


def send_show_command(device, show):
    host = device['host']
    logging.info(f">>> Подключаюсь к {host}")
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        time.sleep(random.random())
        output = ssh.send_command(show)
        logging.debug(f"\n{output}\n")
        logging.info(f"<<< Получена информация от {host}")
        return output


def send_and_parse_command(devices, command, parse_function, threads=10):
    logging.info(f"### Начало работы с потоками")
    result_dict = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(
            send_show_command, devices, repeat(command)
        )
        logging.info(f"### Все функции запущены")
        for dev, output in zip(devices, results):
            host = dev['host']
            result_dict[host] = parse_function(output)
    logging.info("### Все потоки отработали")
    return result_dict


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    r = send_and_parse_command(devices, "sh ip int br", parse_sh_ip_int_br)
    pprint(r)
