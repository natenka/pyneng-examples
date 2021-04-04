from pprint import pprint
import yaml
import netmiko
import paramiko


def send_cmd_with_prompt(device, command, *, wait_for, confirmation):
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        result = ssh.send_command_timing(
            command, strip_prompt=False, strip_command=False
        )
        if wait_for in result:
            result += ssh.send_command_timing(
                confirmation, strip_prompt=False, strip_command=False
            )
        return result


def send_cmd_with_prompt_expect(device, command, *, wait_for, confirmation):
    with netmiko.Netmiko(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(
            command, expect_string=wait_for, strip_prompt=False, strip_command=False
        )
        result += ssh.send_command(
            confirmation, expect_string="#", strip_prompt=False, strip_command=False
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

        out = send_cmd_with_prompt_expect(
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
