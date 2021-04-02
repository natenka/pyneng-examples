import asyncio
from scrapli.driver.core import AsyncIOSXEDriver
from scrapli.exceptions import ScrapliException
from async_timeout import timeout

r1 = {
    "host": "192.168.100.11",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
    "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
    "transport": "asynctelnet",
    "port": 23,
}


async def send_show(device, command):
    # На данный момент (scrapli 2021.1.30) таймаут при подключении к недоступному
    # хосту будет 2 минуты, поэтому пока что лучше добавлять wait_for или
    # async_timeout вокруг подключения
    try:
        #async with timeout(10):
            async with AsyncIOSXEDriver(**device) as ssh:
                result = await ssh.send_command(command)
                return result.result
    except ScrapliException as error:
        print(error, device["host"])
    except asyncio.exceptions.TimeoutError:
        print("asyncio.exceptions.TimeoutError", device["host"])


if __name__ == "__main__":
    output = asyncio.run(send_show(r1, "show ip int br"))
    print(output)


# An open stream object is being garbage collected; call "stream.close()" explicitly.
# asyncio problem
