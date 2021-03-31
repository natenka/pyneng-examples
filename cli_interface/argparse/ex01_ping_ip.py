import subprocess
import argparse

def ping_ip(ip_address, count):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    reply = subprocess.run(
        f"ping -c {count} -n {ip_address}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    if reply.returncode == 0:
        return True, reply.stdout
    else:
        return False, reply.stdout + reply.stderr


parser = argparse.ArgumentParser(description="Ping script")

parser.add_argument("host", help="IP or name to ping")
parser.add_argument("-c", dest="count", default=2, type=int, help="Number of packets")

args = parser.parse_args()
print(args)

rc, message = ping_ip(args.host, args.count)
print(message)
