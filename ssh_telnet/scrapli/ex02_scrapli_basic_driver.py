from scrapli.driver.core import IOSXEDriver
from scrapli.exceptions import ScrapliException


r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
    "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
}


def send_show(device, show_command):
    try:
        with IOSXEDriver(**device) as ssh:
            reply = ssh.send_command(show_command)
            return reply.result
    except ScrapliException as error:
        print(error, device["host"])


def send_cfg(device, cfg_commands):
    try:
        with IOSXEDriver(**device) as ssh:
            reply = ssh.send_configs(cfg_commands)
            return reply.result
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    output = send_show(r1, "sh ip int br")
    print(output)

    output_cfg = send_cfg(r1, ["interface lo11", "ip address 11.1.1.1 255.255.255.255"])
    print(output_cfg)
