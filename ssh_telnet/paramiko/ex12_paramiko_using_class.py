from pprint import pprint
import socket
import paramiko
import yaml
from ex11_paramiko_basic_class import ConnectSSH


def send_show_command(device, command):
    try:
        with ConnectSSH(**device) as ssh:
            output = ssh.send_command(command)
            return output
    except socket.timeout:
        print(f"Failed to connect to {host}")
    except paramiko.SSHException as error:
        print(f"{error} on {host}")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for dev in devices:
            out = send_show_command(dev, command="sh ip int br")
            pprint(out, width=120)
