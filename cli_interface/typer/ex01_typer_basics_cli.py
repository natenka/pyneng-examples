import subprocess
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


def main(ip_address: str, count: int = 3):
    """
    Ping IP_ADDRESS
    """
    status = ping_ip(ip_address, count)
    if status:
        typer.secho(f"ICMP reply received from address {ip_address}", fg="green")
    else:
        typer.secho(f"No ICMP reply received from address {ip_address}", fg="red")


if __name__ == "__main__":
    typer.run(main)

"""
$ python ex01_typer_basics_cli.py --help
Usage: ex01_typer_basics_cli.py [OPTIONS] IP_ADDRESS

  Ping IP_ADDRESS

Arguments:
  IP_ADDRESS  [required]

Options:
  --count INTEGER       [default: 3]
  --help                Show this message and exit.

$ python ex01_typer_basics_cli.py 8.8.8.8
ICMP reply received from address 8.8.8.8

$ python ex01_typer_basics_cli.py 10.1.1.1
No ICMP reply received from address 10.1.1.1
"""
