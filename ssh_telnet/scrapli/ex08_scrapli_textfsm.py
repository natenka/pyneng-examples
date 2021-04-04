from pprint import pprint
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException


r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
    "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
    "platform": "cisco_iosxe",
}


def send_show(device, show_commands):
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    try:
        with Scrapli(**device) as ssh:
            for cmd in show_commands:
                reply = ssh.send_command(cmd)
                parsed_data = reply.textfsm_parse_output()
                if parsed_data:
                    cmd_dict[cmd] = parsed_data
                else:
                    cmd_dict[cmd] = reply.result
        return cmd_dict
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    output = send_show(r1, ["sh ip int br", "sh run | i ^interface"])
    pprint(output, width=120)
