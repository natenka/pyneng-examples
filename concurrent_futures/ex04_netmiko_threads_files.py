from concurrent.futures import ThreadPoolExecutor
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
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(
            send_show_command, devices, repeat(show)
        )
        with open(f"config_all.txt", "w") as f:
            for dev, output in zip(devices, results):
                host = dev['host']
                f.write(f"\n\n{host}\n")
                f.write(output)
    print("### Все потоки отработали")


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    send_show_to_devices(devices, "sh run")
