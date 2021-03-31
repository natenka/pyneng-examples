from pprint import pprint
import yaml
import netmiko
import paramiko


def send_cfg(device, commands):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ""
            result += ssh.config_mode()
            for cmd in commands:
                output = ssh.send_config_set(cmd, exit_config_mode=False)
                if "%" in output:
                    raise ValueError(
                        f"При выполнении команды {cmd} возникла ошибка"
                    )
                result += output
            result += ssh.exit_config_mode()
            return result.replace("\r\n", "\n")
    except netmiko.NetmikoTimeoutException as error:
        print(f"Не удалось подключиться к {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Ошибка аутентификации с {device['host']}")



if __name__ == "__main__":
    commands = {
        "192.168.100.1": ["int lo9", "ipaddress 10.90.90.1 255.255.255.255"],
        "192.168.100.2": ["int lo9"],
        "192.168.100.3": ["int lo9"],
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            try:
                out = send_cfg(
                    device, commands[device['host']]
                )
                pprint(out)
            except ValueError as error:
                print(error)

