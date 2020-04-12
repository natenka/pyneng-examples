import netmiko
print('Import cisco_connect/ssh.py')

__all__ = ['CiscoSSH']

class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)


enable = True
