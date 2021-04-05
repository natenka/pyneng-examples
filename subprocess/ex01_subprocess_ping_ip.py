from platform import system as system_name
import subprocess


def ping_ip(ip_address):
    """
    Ping IP address and return:
    True on success:
    False on failure:
    """
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip_address]
    reply = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip_is_reachable = reply.returncode == 0
    return ip_is_reachable


if __name__ == "__main__":
    print(ping_ip("8.8.8.8"))
    print(ping_ip("10.1.1.1"))
