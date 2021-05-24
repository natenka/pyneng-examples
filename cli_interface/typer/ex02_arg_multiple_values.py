from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
import subprocess
from pprint import pformat
from typing import List

import typer


def ping_ip(ip_address, count):
    """
    Ping IP_ADDRESS and return True/False
    """
    reply = subprocess.run(
        f"ping -c {count} -n {ip_address}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    if reply.returncode == 0:
        return True
    else:
        return False


def ping_ip_addresses(ip_addresses, count, limit):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_addresses, repeat(count))
        for ip, status in zip(ip_addresses, results):
            if status:
                reachable.append(ip)
            else:
                unreachable.append(ip)
    return reachable, unreachable


def main(ip_addresses: List[str], count: int = 3, max_threads: int = 10):
    """
    Ping IP_ADDRESSES
    """
    reach, unreach = ping_ip_addresses(ip_addresses, count, max_threads)
    typer.secho("ICMP reply received from addresses", fg="green")
    print(typer.style(pformat(reach), fg="green"))

    typer.secho("No ICMP reply received from addresses", fg="red")
    print(typer.style(pformat(unreach), fg="red"))


if __name__ == "__main__":
    typer.run(main)
