from pprint import pprint
import logging
import pexpect
import yaml


logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_commands(host, username, password, enable_pass, commands):
    logging.info(f"Connecting to {host}")
    try:
        with pexpect.spawn(
            f"ssh {username}@{host}", encoding="utf-8", timeout=10
        ) as ssh:
            ssh.expect("[Pp]assword")
            ssh.sendline(password)
            ssh.expect(">")
            ssh.sendline("enable")
            ssh.expect("Password")
            ssh.sendline(enable_pass)
            ssh.expect("\S+#")
            prompt = ssh.after

            ssh.sendline("terminal length 0")
            ssh.expect(prompt)

            result = {}
            if type(commands) == str:
                commands = [commands]
            for cmd in commands:
                ssh.sendline(cmd)
                ssh.expect("\r\n")
                ssh.expect(prompt)
                output = ssh.before
                result[cmd] = output.replace("\r\n", "\n")
        return result
    except pexpect.exceptions.TIMEOUT as error:
        logging.debug(error)
        logging.info("pexpect.exceptions.TIMEOUT")


if __name__ == "__main__":
    cmds = ["sh clock", "sh int desc"]
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_commands(**device, commands=cmds)
            pprint(out, width=120)
