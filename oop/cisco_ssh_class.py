from connect_ssh_class import ConnectSSH
import time


class CiscoSSH(ConnectSSH):
    def __init__(self, ip, username, password, enable_password, disable_paging=True):
        super().__init__(ip, username, password)
        self._ssh.send("enable\n")
        self._ssh.send(enable_password + "\n")
        if disable_paging:
            self._ssh.send("terminal length 0\n")
        time.sleep(1)
        self._ssh.recv(self._MAX_READ)

    def config_mode(self):
        self._ssh.send("conf t\n")
        time.sleep(0.2)
        result = self._ssh.recv(self._MAX_READ).decode("ascii")
        return result

    def exit_config_mode(self):
        self._ssh.send("end\n")
        time.sleep(0.2)
        result = self._ssh.recv(self._MAX_READ).decode("ascii")
        return result

    def send_config_commands(self, commands):
        output = self.config_mode()
        output += super().send_config_commands(commands)
        output += self.exit_config_mode()
        return output
