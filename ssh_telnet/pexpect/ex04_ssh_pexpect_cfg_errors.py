from pprint import pprint
import logging
import pexpect
import yaml


logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_cfg_commands(host, username, password, enable_pass, cfg_commands):
    logging.info(f"Connecting to {host}")
    try:
        with pexpect.spawn(f"ssh {username}@{host}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("[Pp]assword")
            ssh.sendline(password)
            enable_mode = ssh.expect([">", "#"])
            if enable_mode == 0:
                ssh.sendline("enable")
                ssh.expect("Password")
                ssh.sendline(enable_pass)
                ssh.expect("#")

            ssh.sendline("terminal length 0")
            ssh.expect("#")

            cfg_commands = ["conf t", *cfg_commands, "end"]
            result = ""
            for cmd in cfg_commands:
                ssh.sendline(cmd)
                ssh.expect(["config\S+#", "#"])
                output = ssh.before
                if "%" in output:
                    logging.warning(
                        f'When executing the command "{cmd}" an error occurred'
                    )
                    logging.info(output)
                result += output + ssh.after
        return result.replace("\r\n", "\n")
    except pexpect.exceptions.TIMEOUT as error:
        logging.debug(error)
        logging.info("pexpect.exceptions.TIMEOUT")


if __name__ == "__main__":
    cfg_cmds = ["int lo200", "ip address 10.2.2.2 255.255.255.255"]
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_cfg_commands(**device, cfg_commands=cfg_cmds)
            pprint(out, width=120)
