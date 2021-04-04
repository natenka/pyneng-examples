import os
from pprint import pprint
import yaml
import netmiko
import paramiko


def send_and_parse_show_commands(device, commands, templates_path=None):
    if "NET_TEXTFSM" not in os.environ:
        if not templates_path:
            raise ValueError(
                "For the function to work, you must either specify an"
                "environment variable NET_TEXTFSM or specify a templates_path"
            )
        os.environ["NET_TEXTFSM"] = templates_path

    result = {}
    if type(commands) == str:
        commands = [commands]
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        for cmd in commands:
            output = ssh.send_command(cmd, use_textfsm=True)
            result[cmd] = output
        return result


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), "templates")
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        result = send_and_parse_show_commands(
            dev, "sh ip int br", templates_path=full_pth
        )
        pprint(result, width=130)

