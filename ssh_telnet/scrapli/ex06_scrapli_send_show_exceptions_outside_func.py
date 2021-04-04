from pprint import pprint
import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException


def send_show(device, show_commands):
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    with Scrapli(**device) as ssh:
        for cmd in show_commands:
            reply = ssh.send_command(cmd)
            cmd_dict[cmd] = reply.result
    return cmd_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        print(f" {dev['host']} ".center(60, "#"))
        try:
            output = send_show(dev, ["sh ip int br", "sh ver | i uptime"])
        except ScrapliException as error:
            print(error, dev["host"])
        else:
            pprint(output, width=120)
