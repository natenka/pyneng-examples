from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
from pprint import pprint
import logging
from typing import Optional

import netmiko
import paramiko
import yaml
import typer


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    filename="log_ex03.txt",
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


def main(
    command: str,
    ssh_params: typer.FileText,
    output: Optional[typer.FileTextWrite] = None,
    max_threads: int = typer.Option(10, min=1, max=50, clamp=True),
):
    devices = yaml.safe_load(ssh_params)

    result_dict = send_show_to_devices(devices, command, max_threads)
    for ip, out in result_dict.items():
        if output:
            output.write(ip.center(30, "=") + "\n")
            output.write(out + "\n")
        else:
            print(ip.center(30, "="))
            print(out)


if __name__ == "__main__":
    typer.run(main)


"""
$ python ex03_typer_param_type_file.py --help
Usage: ex03_typer_param_type_file.py [OPTIONS] COMMAND SSH_PARAMS

Arguments:
  COMMAND     [required]
  SSH_PARAMS  [required]

Options:
  --output FILENAME
  --max-threads INTEGER RANGE  [default: 10]
  --help                       Show this message and exit.

$ python ex03_typer_param_type_file.py "sh clock" devices.yaml
Connecting  [####################################]  100%
========192.168.100.1=========
*04:44:58.179 UTC Mon May 24 2021
========192.168.100.2=========
*04:44:58.310 UTC Mon May 24 2021
========192.168.100.3=========
*04:44:58.300 UTC Mon May 24 2021

"""
