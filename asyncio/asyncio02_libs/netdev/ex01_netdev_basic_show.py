import asyncio
import netdev


r1 = {
    "device_type": "cisco_ios",
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


async def send_show(device, command):
    async with netdev.create(**device) as ssh:
        result = await ssh.send_command(command)
        return result


if __name__ == "__main__":
    output = asyncio.run(send_show(r1, "show ip int br"))
    print(output)
