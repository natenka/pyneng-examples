from netmiko.cisco.cisco_ios import CiscoIosSSH


class ErrorInCommand(Exception):
    """Это исключение генерируется при ошибке в команде"""


class MyNetmiko(CiscoIosSSH):
    def send_command(self, command, **kwargs):
        output = super().send_command(command, **kwargs)
        if "Invalid input" in output:
            raise ErrorInCommand("Возникла ошибка")
        return output
