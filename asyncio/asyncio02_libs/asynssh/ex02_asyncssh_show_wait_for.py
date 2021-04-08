"""
asyncio.wait_for используется для asyncssh.connect чтобы добавить
таймаут на подключение и чтобы добавить таймаут на reader.readuntil.
"""
from pprint import pprint
import asyncio
import asyncssh


async def send_show(
    host, username, password, enable_password, command, connection_timeout=5
):
    try:
        ssh = await asyncio.wait_for(
            asyncssh.connect(
                host=host,
                username=username,
                password=password,
                encryption_algs="+aes128-cbc,aes256-cbc",
            ),
            timeout=connection_timeout,
        )
    except asyncio.TimeoutError:
        print(f"Connection Timeout on {host}")
    except asyncssh.PermissionDenied:
        print(f"Authentication Error on {host}")
    except asyncssh.Error as error:
        print(f"{error} on {host}")
    else:
        writer, reader, _ = await ssh.open_session(
            term_type="Dumb", term_size=(200, 24)
        )
        try:
            await asyncio.wait_for(reader.readuntil(">"), timeout=3)
            writer.write("enable\n")
            await asyncio.wait_for(reader.readuntil("Password"), timeout=3)
            writer.write(f"{enable_password}\n")
            await asyncio.wait_for(reader.readuntil([">", "#"]), timeout=3)
            writer.write("terminal length 0\n")
            await asyncio.wait_for(reader.readuntil("#"), timeout=3)

            writer.write(f"{command}\n")
            output = await asyncio.wait_for(reader.readuntil("#"), timeout=3)
            return output
        except asyncio.TimeoutError as error:
            print("TimeoutError reader.readuntil")


if __name__ == "__main__":
    r1 = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    result = asyncio.run(send_show(**r1, command="sh ip int br"))
    print(result)
