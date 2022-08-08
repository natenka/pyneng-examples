from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from netmiko import Netmiko

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

### stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(
    "{threadName} {asctime} {name} {levelname} {message}",
     datefmt="%H:%M:%S", style="{"
)
console.setFormatter(formatter)

logger.addHandler(console)

### File
logfile = logging.FileHandler("exceptions_report.log")
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter("{asctime} {threadName} {name} {levelname} {message}", style="{")
logfile.setFormatter(formatter)

logger.addHandler(logfile)


def send_show(device_dict, command):
    device = device_dict.get("host")
    logger.info(f">>> Connecting to {device}")
    try:
        with Netmiko(**device_dict) as conn:
            conn.enable()
            output = conn.send_command(command)
            return output
    except Exception as error:
        logger.debug(f"Error on {device} {error}", exc_info=True) # exc_info добавляет traceback


def send_cmd_to_all(devices, command, threads=10):
    ip_out_dict = {}
    with ThreadPoolExecutor(max_workers=threads) as ex:
        task_queue = [ex.submit(send_show, dev, command=command) for dev in devices]
        for dev, future in zip(devices, task_queue):
            host = dev["host"]
            output = future.result()
            if output:
                ip_out_dict[host] = future.result()
    return ip_out_dict


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
    result = send_cmd_to_all(devices, cmd)
    pprint(result)

