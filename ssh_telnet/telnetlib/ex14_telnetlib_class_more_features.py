import telnetlib
import time
from pprint import pprint
import socket
import re

from textfsm import clitable
import yaml


class CiscoTelnet:
    def __init__(
        self, host, username, password, enable_pass, encoding="utf-8", timeout=10
    ):
        self.host = host
        self.username = username
        self.password = password
        self.enable_pass = enable_pass
        self.encoding = encoding

        self.telnet = telnetlib.Telnet(host, timeout=timeout)
        self.telnet.read_until(b"Username:")
        self._write_line(username)
        self.telnet.read_until(b"Password:")
        self._write_line(password)

        idx, *trash = self.telnet.expect([b">", b"#"])
        if idx == 0:
            self._write_line("enable")
            self.telnet.read_until(b"Password")
            self._write_line(password)
            self.telnet.read_until(b"#")

        self._write_line("terminal length 0")
        self.telnet.read_until(b"#")

    def _write_line(self, line):
        self.telnet.write(line.encode(self.encoding) + b"\n")

    def _read_until_prompt(self):
        output = self.telnet.read_until(b"#").decode(self.encoding)
        return output.replace("\r\n", "\n")

    def _error_in_command(self, command, result, strict=False):
        regex = "% (?P<err>.+)"
        template = (
            'When executing the command "{cmd}" on device {device}, '
            "an error occurred -> {error}"
        )
        error_in_cmd = re.search(regex, result)
        if error_in_cmd:
            message = template.format(
                cmd=command, device=self.host, error=error_in_cmd.group("err")
            )
            if strict:
                raise ValueError(message)
            else:
                print(message)

    def _parse_output(self, command, command_output, templates_dir="templates"):
        attributes = {"Command": command, "Vendor": "cisco_ios"}
        cli = clitable.CliTable("index", templates_dir)
        cli.ParseCmd(command_output, attributes)
        parsed_output = [dict(zip(cli.header, row)) for row in cli]
        if parsed_output:
            return parsed_output
        else:
            return command_output

    def send_command(self, command, parse=False, templates_dir="templates"):
        self._write_line(command)
        output = self._read_until_prompt()
        if parse:
            result = self._parse_output(command, output, templates_dir)
            return result
        else:
            return output

    def send_config_commands(self, commands, strict=False):
        cfg_output = ""
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        for cmd in commands:
            self._write_line(cmd)
            current_output = self._read_until_prompt()
            cfg_output += current_output
            self._error_in_command(cmd, current_output, strict=strict)
        return cfg_output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.telnet.close()

    def close(self):
        self.telnet.close()


if __name__ == "__main__":
    commands_with_errors = ["logging 0255.255.1", "logging", "a"]
    correct_commands = ["logging buffered 20010", "ip http server"]
    commands = commands_with_errors + correct_commands

    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        with CiscoTelnet(**r1) as r1_ssh:
            output = r1_ssh.send_command("sh ip int br", parse=False)
            pprint(output, width=120)

            parsed_output = r1_ssh.send_command("sh ip int br", parse=True)
            pprint(parsed_output, width=120)

            out1 = r1_ssh.send_config_commands(correct_commands)
            pprint(out1, width=120)

            out2 = r1_ssh.send_config_commands(commands_with_errors)
            # out2 = r1_ssh.send_config_commands(commands_with_errors, strict=True)
            pprint(out2, width=120)
