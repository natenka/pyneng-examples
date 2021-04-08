from pprint import pprint
import asyncio
import asyncssh


# from ex03_asyncssh_show_read_until import read_until
async def read_until(reader, prompt="#", timeout=3, strict=True):
    try:
        return await asyncio.wait_for(reader.readuntil(prompt), timeout)
    except asyncio.TimeoutError as error:
        output = ""
        while True:
            try:
                output += await asyncio.wait_for(reader.read(1000), 0.1)
            except asyncio.TimeoutError as error:
                break
        message = (
            f"TimeoutError while executing reader.readuntil('{prompt}')\n"
            f"Last output from device:\n{output}"
        )
        if strict:
            raise asyncio.TimeoutError(message)
        else:
            print(message)
            return output


async def send_config(
    host, username, password, enable_password, cfg_commands, connection_timeout=5
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
        await read_until(reader, ">")
        writer.write("enable\n")
        await read_until(reader, "Password")
        writer.write(f"{enable_password}\n")
        await read_until(reader, [">", "#"])
        writer.write("terminal length 0\n")
        await read_until(reader)

        if type(cfg_commands) == str:
            cfg_commands = ["conf t", cfg_commands, "end"]
        else:
            cfg_commands = ["conf t", *cfg_commands, "end"]
        output = ""
        for cmd in cfg_commands:
            writer.write(f"{cmd}\n")
            output += await read_until(reader)
        return output


if __name__ == "__main__":
    r1 = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    config_commands = ["interface lo11", "ip address 11.1.1.1 255.255.255.255"]
    result = asyncio.run(send_config(**r1, cfg_commands=config_commands))
    print(result)
