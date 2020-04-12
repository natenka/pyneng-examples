print('ssh')

import netmiko


__all__ = ['CiscoSSH', 'parse_data']

class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)


def parse_data():
    pass


def error_check():
    pass

