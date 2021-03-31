from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from pprint import pprint
import time
import random
from itertools import repeat
from datetime import datetime
import logging
import netmiko
import yaml
import threading


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)


def send_show_command(device, show):
    print(threading.current_thread())
    ip = device['host']
    logging.info(f">>> Подключаюсь к {ip}")
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            time.sleep(random.random() * 10)
            output = ssh.send_command(show)
            logging.debug(f"\n{output}\n")
            logging.info(f"<<< Получена информация от {ip}")
            return ip, output
    except netmiko.NetmikoTimeoutException as error:
        print(f"Не удалось подключиться к {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Ошибка аутентификации с {device['host']}")



def send_show_to_devices(devices, command):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for dev in devices:
            f = executor.submit(send_show_command, dev, show=command)
            futures.append(f)
        for f in as_completed(futures):
            output = f.result()
            print(output)
    logging.info("### Все потоки отработали")
    print(threading.current_thread())
    return result_dict


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    r = send_show_to_devices(devices, "sh clock")
    pprint(r)
