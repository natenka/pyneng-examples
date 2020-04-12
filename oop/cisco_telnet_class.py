import telnetlib
import time


class CiscoTelnet:
    def __init__(
        self, ip, username, password, enable_password=None, disable_paging=True
    ):
        self.ip = ip
        self._telnet = telnetlib.Telnet(ip)
        self._telnet.read_until(b"Username:")
        self._telnet.write(username.encode("ascii") + b"\n")

        self._telnet.read_until(b"Password:")
        self._telnet.write(password.encode("ascii") + b"\n")
        if enable_password:
            self._telnet.write(b"enable\n")
            self._telnet.read_until(b"Password:")
            self._telnet.write(enable_password.encode("ascii") + b"\n")
        if disable_paging:
            self._telnet.write(b"terminal length 0\n")
        time.sleep(0.5)
        self._telnet.read_very_eager()

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__")
        self.close()

    def send_show_command(self, command):
        self._telnet.write(command.encode("ascii") + b"\n")
        time.sleep(1)
        output = self._telnet.read_very_eager().decode("ascii")
        self._check_errors(output)
        return output

    def close(self):
        self._telnet.close()

    def _check_errors(self, command_output):
        if "Invalid input detected" in command_output:
            raise ValueError("Возникла ошибка Invalid input detected")

    def config_mode(self):
        self._telnet.write(b"conf t\n")
        time.sleep(0.5)
        return self._telnet.read_very_eager().decode("ascii")

    def exit_config_mode(self):
        self._telnet.write(b"end\n")
        time.sleep(0.5)
        return self._telnet.read_very_eager().decode("ascii")

    def send_config_commands(self, commands):
        # if type(commands) == str:
        #    commands = [commands]
        output = self.config_mode()
        for command in commands:
            self._telnet.write(command.encode("ascii") + b"\n")
            time.sleep(0.2)
        output += self._telnet.read_very_eager().decode("ascii")
        output += self.exit_config_mode()
        return output


if __name__ == "__main__":
    with CiscoTelnet("192.168.100.1", "cisco", "cisco", "cisco") as r1:
        print(r1.send_show_command("sh ip int br"))
        raise ValueError
