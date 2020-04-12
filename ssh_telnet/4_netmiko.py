from netmiko import ConnectHandler
import yaml


def send_show_command(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
    return output


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for device in devices:
        print(send_show_command(device, "sh ip int br"))
