from pprint import pprint
import pexpect
import yaml


def send_show_command(host, username, password, enable_pass, command):
    print(f"Connecting to {host}")
    with pexpect.spawn(f"telnet {host}", encoding="utf-8") as telnet:
        telnet.expect("[Uu]sername")
        telnet.sendline(username)
        telnet.expect("[Pp]assword")
        telnet.sendline(password)
        telnet.expect(">")
        telnet.sendline("enable")
        telnet.expect("Password")
        telnet.sendline(enable_pass)
        telnet.expect("#")

        telnet.sendline("terminal length 0")
        telnet.expect("#")

        telnet.sendline(command)
        telnet.expect("#")
        output = telnet.before
    return output.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_command(**device, command="sh ip int br")
            pprint(out, width=120)
