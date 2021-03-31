import asyncio
from scrapli.driver.core import AsyncIOSXEDriver

r1 = {
   "host": "192.168.100.1",
   "auth_username": "cisco",
   "auth_password": "cisco",
   "auth_secondary": "cisco",
   "auth_strict_key": False,
   "transport": "asyncssh",
}

async def send_show(device, command):
    async with AsyncIOSXEDriver(**device) as conn:
        result = await conn.send_command(command)
    return result.result


if __name__ == "__main__":
    output = asyncio.run(send_show(r1, "show ip int br"))
    print(output)

