from pprint import pprint
import re

import pexpect
import yaml


def cisco_send_show_command(host, username, password, enable_pass, command):
    with pexpect.spawn(f"ssh {username}@{host}", encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect(">")
        ssh.sendline("enable")
        ssh.expect("Password")
        ssh.sendline(enable_pass)
        ssh.expect("#")

        output = ""
        ssh.sendline(command)

        while True:
            match = ssh.expect(["#", "--More--", pexpect.TIMEOUT], timeout=5)
            page = ssh.before
            page = re.sub(r" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match == 1:
                ssh.send(" ")
            else:
                break
    return output.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
    out = cisco_send_show_command(**r1, command="sh run")
    with open("result_r1.txt", "w") as f:
        f.write(out)
