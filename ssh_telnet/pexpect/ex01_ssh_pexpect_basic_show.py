from pprint import pprint
import pexpect
import yaml


def send_show_command(host, username, password, enable_pass, command):
    print(f"Connecting to {host}")
    with pexpect.spawn(f"ssh {username}@{host}", encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect(">")
        ssh.sendline("enable")
        ssh.expect("Password")
        ssh.sendline(enable_pass)
        ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")

        ssh.sendline(command)
        ssh.expect("#")
        output = ssh.before
    return output.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_command(**device, command="sh ip int br")
            pprint(out, width=120)
