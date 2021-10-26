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
    typer.secho(f"ICMP reply received from addresses:\n{pformat(reach)}", fg="green")
    typer.secho(f"No ICMP reply received from addresses:\n{pformat(unreach)}", fg="red")


if __name__ == "__main__":
    typer.run(main)

"""
$ python ex02_typer_arg_multiple_values.py --help
Usage: ex02_typer_arg_multiple_values.py [OPTIONS] IP_ADDRESSES...

  Ping IP_ADDRESSES

Arguments:
  IP_ADDRESSES...  [required]

Options:
  --count INTEGER        [default: 3]
  --max-threads INTEGER  [default: 10]
  --help                 Show this message and exit.

$ python ex02_typer_arg_multiple_values.py 8.8.8.8 10.1.1.1 8.8.4.4 --count 1
ICMP reply received from addresses:
['8.8.8.8', '8.8.4.4']
No ICMP reply received from addresses:
['10.1.1.1']
"""
