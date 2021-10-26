from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
from pprint import pprint
import logging
from typing import Optional, List

import netmiko
import paramiko
import yaml
import typer


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    filename="log_ex04.txt",
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


def cli(
    command: str,
    ip_list: List[str],
    username: str = typer.Option(..., "-u", "--username", prompt=True),
    password: str = typer.Option(
        ..., "-p", "--password", prompt=True, hide_input=True
    ),
    enable_password: str = typer.Option(
        ..., "-e", "--enable", prompt=True, hide_input=True
    ),
    device_type: str = "cisco_ios",
    max_threads: int = typer.Option(10, min=1, max=50, clamp=True),
):
    device_params = {
        "device_type": device_type,
        "username": username,
        "password": password,
        "secret": enable_password,
    }
    device_list = [{**device_params, "host": ip} for ip in ip_list]

    results = send_show_to_devices(device_list, command, max_threads)
    pprint(results)


if __name__ == "__main__":
    typer.run(cli)

"""
$ python ex04_typer_options_params.py --help
Usage: ex04_typer_options_params.py [OPTIONS] COMMAND IP_LIST...

Arguments:
  COMMAND     [required]
  IP_LIST...  [required]

Options:
  -u, --username TEXT          [required]
  -p, --password TEXT          [required]
  -e, --enable TEXT            [required]
  --device-type TEXT           [default: cisco_ios]
  --max-threads INTEGER RANGE  [default: 10]
  --help                       Show this message and exit.

$ python ex04_typer_options_params.py "sh clock" 192.168.100.1 -u cisco -p cisco -e cisco
Connecting  [####################################]  100%
{'192.168.100.1': '*04:56:12.905 UTC Mon May 24 2021'}

$ python ex04_typer_options_params.py "sh clock" 192.168.100.1
Username: cisco
Password:
Enable password:
Connecting  [####################################]  100%
{'192.168.100.1': '*04:56:25.463 UTC Mon May 24 2021'}

"""
