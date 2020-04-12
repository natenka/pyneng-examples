import ipaddress


class IPAddress:
    def __init__(self, ip):
        address, mask = ip.split("/")
        self.address = address
        self.mask = int(mask)

    def __str__(self):
        return f"{self.address}/{self.mask}"

    def __repr__(self):
        return f"IPAddress('{self.address}/{self.mask}')"

    def __add__(self, second):
        if not isinstance(second, int):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'IPAddress' and '{type(second).__name__}'"
            )
        ip_int = int(ipaddress.ip_address(self.address))
        result_ip = str(ipaddress.ip_address(ip_int + second))
        return IPAddress(f"{result_ip}/{self.mask}")

    def __radd__(self, number):
        return self + number


if __name__ == "__main__":
    ip1 = IPAddress("10.1.1.1/25")
    print(ip1 + 5)
    print(5 + ip1)
    print(ip1.__radd__(5))

