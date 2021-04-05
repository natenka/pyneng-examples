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
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show(device, command):
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            prompt = ssh.find_prompt()
            return f"\n{prompt}{command}\n{result}\n"
    except netmiko.NetmikoTimeoutException as error:
        print(f"Failed to connect to {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication error on {device['host']}")


def send_show_to_devices(devices, show, output_filename, workers=10):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(send_show, devices, repeat(show))
        with open(output_filename, "w") as f:
            for output in results:
                f.write(output)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_to_devices(devices, "sh run", output_filename="config_all.txt")
