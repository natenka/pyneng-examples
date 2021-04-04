from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from pprint import pprint

import pexpect
import yaml
import logging


logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_command(host, username, password, enable_pass, command):
    logging.info(f"Connecting to {host}")
    with pexpect.spawn(f"ssh {username}@{host}", encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect(">")
        ssh.sendline("enable")
        ssh.expect("Password")
        ssh.sendline(enable_pass)
        ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")

        ssh.sendline(command)
        ssh.expect("#")
        output = ssh.before
        logging.info(f"<<< Received output from {host}")
    return output.replace("\r\n", "\n")


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_list = [
            executor.submit(send_show_command, **dev, command=show) for dev in devices
        ]
        for dev, f in zip(devices, future_list):
            result_dict[dev["host"]] = f.result()
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r = send_show_to_devices(devices, "sh int desc")
    pprint(r, width=120)
