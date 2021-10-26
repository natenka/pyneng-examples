from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from typing import Optional, List

from netmiko import ConnectHandler
import yaml
import typer

from ex05_typer_param_choice import send_show_to_devices



app = typer.Typer()

@app.command("file", help="Read params from file")
def params_from_file(
    command: str,
    ssh_params: typer.FileText,
    max_threads: int = typer.Option(10, min=1, max=50, clamp=True),
):
    devices = yaml.safe_load(ssh_params)
    result_dict = send_show_to_devices(devices, command, max_threads)
    pprint(result_dict)


@app.command(help="Enter params as options/input")
def options(
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
    app()


"""
$ python ex06_typer_commands.py --help
Usage: ex06_typer_commands.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help                Show this message and exit.

Commands:
  file     Read params from file
  options  Enter params as options/input


$ python ex06_typer_commands.py file --help
Usage: ex06_typer_commands.py file [OPTIONS] COMMAND SSH_PARAMS

  Read params from file

Arguments:
  COMMAND     [required]
  SSH_PARAMS  [required]

Options:
  --max-threads INTEGER RANGE  [default: 10]
  --help                       Show this message and exit.


$ python ex06_typer_commands.py options --help
Usage: ex06_typer_commands.py options [OPTIONS] COMMAND IP_LIST...

  Enter params as options/input

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

"""
