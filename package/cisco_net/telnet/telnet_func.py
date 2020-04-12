import time
import telnetlib
print('Import cisco_connect/telnet.py')

__all__ = ['CiscoTelnet']

class CiscoTelnet:
    def __init__(self, ip, username, password, enable, disable_paging=True):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self.telnet.write(username.encode('utf-8') + b'\n')
        self.telnet.read_until(b'Password:')
        self.telnet.write(password.encode('utf-8') + b'\n')
        self.telnet.write(b'enable\n')
        self.telnet.read_until(b'Password:')
        self.telnet.write(enable.encode('utf-8') + b'\n')
        if disable_paging: self.telnet.write(b'terminal length 0\n')
        time.sleep(1)
        self.telnet.read_very_eager()

    def send_show_command(self, command):
        self.telnet.write(command.encode('utf-8') + b'\n')
        time.sleep(2)
        command_output = self.telnet.read_very_eager().decode('utf-8')
        return command_output
