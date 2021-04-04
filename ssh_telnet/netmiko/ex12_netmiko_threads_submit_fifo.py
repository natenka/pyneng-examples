from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
import logging

import yaml
import netmiko
import paramiko


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show(device, show_commands):
    host = device["host"]
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    logging.info(f">>> Connecting to {host}")
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            for cmd in show_commands:
                output = ssh.send_command(cmd)
                cmd_dict[cmd] = output
        logging.info(f"<<< Received output from {host}")
        return cmd_dict
    except netmiko.NetmikoTimeoutException as error:
        print(f"Failed to connect to {host}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication error on {host}")


def send_show_to_devices(devices, commands, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_list = [
            executor.submit(send_show, dev, commands[dev["host"]]) for dev in devices
        ]
        for dev, f in zip(devices, future_list):
            result_dict[dev["host"]] = f.result()
    return result_dict


if __name__ == "__main__":
    ip_command_map = {
        "192.168.100.3": ["sh ip int br", "sh arp"],
        "192.168.100.1": "sh arp",
        "192.168.100.2": ["sh ip int br", "sh int desc"],
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, ip_command_map)
    pprint(output, width=130)
