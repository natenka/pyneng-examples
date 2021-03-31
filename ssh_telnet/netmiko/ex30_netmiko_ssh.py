from pprint import pprint
import yaml
import netmiko
import paramiko


def send_show(device, commands):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            result = {}
            if type(commands) == str:
                commands = [commands]
            for cmd in commands:
                output = ssh.send_command(cmd)
                result[cmd] = output
            return result
    except netmiko.NetmikoTimeoutException as error:
        print(f"Не удалось подключиться к {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Ошибка аутентификации с {device['host']}")



if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show(device, "sh ip int br")
            pprint(out)
