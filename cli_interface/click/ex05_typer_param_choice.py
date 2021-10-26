from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
from pprint import pprint
import logging
from enum import Enum

import netmiko
import paramiko
import yaml
import typer


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    filename="log_ex05.txt",
    format="%(asctime)s %(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO,
)


def send_show(device, command):
    host = device["host"]
    logging.info(f">>> Connecting to {host}")
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
        return {host: output}
    except netmiko.NetmikoTimeoutException as error:
        logging.info(f"Failed to connect to {host}")
    except paramiko.ssh_exception.AuthenticationException:
        logging.info(f"Authentication error on {host}")


def send_show_to_devices(devices, command, max_threads):
    host_output_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(send_show, devices, repeat(command))
        with typer.progressbar(results, length=len(devices), label="Connecting") as bar:
            for data in bar:
                host_output_dict.update(data)
    return host_output_dict


class Commands(str, Enum):
    clock = "sh clock"
    interface = "sh ip int br"
    config = "sh run"


def main(
    command: Commands,
    yaml_file: typer.FileText = "devices.yaml",
    max_threads: int = typer.Option(10, min=1, max=50, clamp=True),
):
    devices = yaml.safe_load(yaml_file)
    pprint(send_show_to_devices(devices, command, max_threads))


if __name__ == "__main__":
    typer.run(main)
