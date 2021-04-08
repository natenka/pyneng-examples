from pprint import pprint
import asyncio
import asyncssh


class ConnectAsyncSSH:
    def __init__(self, host, username, password, enable_password, connection_timeout=5):
        self.host = host
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.connection_timeout = connection_timeout

    async def connect(self):
        self.ssh = await asyncio.wait_for(
            asyncssh.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                encryption_algs="+aes128-cbc,aes256-cbc",
            ),
            timeout=self.connection_timeout,
        )
        self.writer, self.reader, _ = await self.ssh.open_session(
            term_type="Dumb", term_size=(200, 24)
        )
        await self._read_until(">")
        self.writer.write("enable\n")
        await self._read_until("Password")
        self.writer.write(f"{self.enable_password}\n")
        await self._read_until([">", "#"])
        self.writer.write("terminal length 0\n")
        await self._read_until()

    async def _read_until(self, prompt="#", timeout=3):
        try:
            return await asyncio.wait_for(self.reader.readuntil(prompt), timeout)
        except asyncio.TimeoutError as error:
            output = ""
            while True:
                try:
                    output += await asyncio.wait_for(self.reader.read(1000), 0.1)
                except asyncio.TimeoutError as error:
                    break
            message = (
                f"TimeoutError while executing self.reader.readuntil('{prompt}')\n"
                f"Last output from device:\n{output}"
            )
            raise asyncio.TimeoutError(message)

    async def send_show_command(self, command):
        self.writer.write(command + "\n")
        output = await self._read_until()
        return output

    async def send_config_commands(self, commands):
        cfg_output = ""
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        for cmd in commands:
            self.writer.write(cmd + "\n")
            cfg_output += await self._read_until()
        return cfg_output

    async def close(self):
        self.ssh.close()
        await self.ssh.wait_closed()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def main():
    r1 = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    config_commands = ["logging buffered 20010", "ip http server"]
    async with ConnectAsyncSSH(**r1) as ssh:
        print(await ssh.send_show_command("sh ip int br"))
        print(await ssh.send_config_commands(config_commands))


if __name__ == "__main__":
    asyncio.run(main())
