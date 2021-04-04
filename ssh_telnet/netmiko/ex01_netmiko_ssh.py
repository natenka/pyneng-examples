from pprint import pprint
import yaml
import netmiko
import paramiko


def send_show(device, commands):
    result = {}
    if type(commands) == str:
        commands = [commands]
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            for cmd in commands:
                output = ssh.send_command(cmd)
                result[cmd] = output
            return result
    except netmiko.NetmikoTimeoutException as error:
        print(f"Failed to connect to {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication error on {device['host']}")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show(device, "sh ip int br")
            pprint(out, width=120)
