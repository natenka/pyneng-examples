import subprocess
import click


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


@click.command()
@click.argument("ip_address")
@click.option("--count", default=3)
def main(ip_address, count):
    """
    Ping IP_ADDRESS
    """
    status = ping_ip(ip_address, count)
    if status:
        click.secho(f"ICMP reply received from address {ip_address}", fg="green")
    else:
        click.secho(f"No ICMP reply received from address {ip_address}", fg="red")


if __name__ == "__main__":
    main()

