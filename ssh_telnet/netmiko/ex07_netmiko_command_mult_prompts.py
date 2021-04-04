from pprint import pprint
import yaml
import netmiko
import paramiko


def send_cmd_with_prompt(device, command, *, wait_for, confirmation):
    if type(wait_for) == str:
        wait_for = [wait_for]
    if type(confirmation) == str:
        confirmation = [confirmation]
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        result = ssh.send_command_timing(
            command, strip_prompt=False, strip_command=False
        )
        for wait, confirm in zip(wait_for, confirmation):
            if wait in result:
                result += ssh.send_command_timing(
                    confirm, strip_prompt=False, strip_command=False
                )
        return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        out = send_cmd_with_prompt(
            r1, "copy run start", wait_for="Destination filename", confirmation="\n"
        )
        print(out)


"""
R1#copy run start
Destination filename [startup-config]?
Building configuration...
[OK]
R1#
"""
