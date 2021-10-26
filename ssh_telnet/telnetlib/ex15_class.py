import time
import telnetlib
import re
import logging

import yaml


class CiscoTelnet:
    def __init__(
        self,
        host,
        username,
        password,
        secret=None,
        disable_paging=True,
        read_timeout=5,
        encoding="utf-8",
    ):
        self.host = host
        self.username = username
        self.prompt = ">"
        self.read_timeout = read_timeout
        self.encoding = encoding

        self._telnet = telnetlib.Telnet(host)
        self._read_until("Username")
        self._write_line(username)
        self._read_until("Password")
        self._write_line(password)

        match_index, _, output = self._telnet.expect([b">", b"#"])
        self.hostname = re.search(r"(\S+)[#>]", output.decode(self.encoding)).group(1)
        if match_index == 0 and secret:
            self._write_line("enable")
            self._read_until("Password")
            self._write_line(secret)
            self._read_until("#")
            self.prompt = "#"
        if disable_paging:
            self._write_line("terminal length 0")
            self._read_until(self.prompt)

    def _read_until(self, regex_list):
        if isinstance(regex_list, str):
            regex_list = [regex_list]
        regex_list_bytes = [r.encode(self.encoding) for r in regex_list]
        match_index, match_obj, output = self._telnet.expect(
            regex_list_bytes, timeout=self.read_timeout
        )
        if match_obj:
            logging.info(f"Found match {match_obj.group()} index {match_index}")
        else:
            logging.error(
                f"No match found for regex list {regex_list}. Returning buffer content"
            )
        return output.decode(self.encoding).replace("\r\n", "\n")

    def _write_line(self, line):
        self._telnet.write(f"{line}\n".encode(self.encoding))

    def send_show_command(self, command):
        self._write_line(command)
        command_output = self._read_until(self.prompt)
        return command_output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._telnet.close()


if __name__ == "__main__":
    r1_params = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with CiscoTelnet(**r1_params) as r1:
        print(r1.send_show_command("sh clock"))
        print(r1.send_show_command("sh ip int br"))
        print(r1.send_show_command("sh run | i hostname"))
